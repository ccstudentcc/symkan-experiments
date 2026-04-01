from __future__ import annotations

import copy

import pytest
import torch

from kan.Symbolic_KANLayer import Symbolic_KANLayer
from kan import icbr


class _NumericMaskLayer:
    def __init__(self, mask: torch.Tensor) -> None:
        self.mask = torch.nn.Parameter(mask.clone(), requires_grad=False)


class _MiniIcbModel:
    def __init__(self, numeric_mask: torch.Tensor, symbolic_mask: torch.Tensor) -> None:
        self.width_in = [2, 1]
        self.width_out = [2, 1]
        self.act_fun = [_NumericMaskLayer(numeric_mask)]
        symbolic_layer = Symbolic_KANLayer(in_dim=2, out_dim=1, device="cpu")
        symbolic_layer.mask.data = symbolic_mask.clone()
        self.symbolic_fun = [symbolic_layer]
        self.auto_save = False
        self.acts = [None]
        self.spline_postacts = [None]

    def __call__(self, x: torch.Tensor, singularity_avoiding: bool = False, y_th: float = 10.0) -> torch.Tensor:
        self.acts[0] = x
        self.spline_postacts[0] = torch.zeros((x.shape[0], 1, 2), dtype=x.dtype)
        return torch.zeros((x.shape[0], 1), dtype=x.dtype)


def test_run_auto_symbolic_icbr_keeps_pruned_edges_inactive(monkeypatch: pytest.MonkeyPatch) -> None:
    numeric_mask = torch.tensor([[1.0], [0.0]], dtype=torch.float32)
    symbolic_mask = torch.zeros((1, 2), dtype=torch.float32)
    work_model = _MiniIcbModel(numeric_mask, symbolic_mask)
    teacher_model = copy.deepcopy(work_model)

    candidate = {
        "fun_name": "x",
        "params": torch.tensor([1.0, 0.0, 1.0, 0.0], dtype=torch.float32),
        "r2": 1.0,
        "complexity": 1.0,
    }

    monkeypatch.setattr(
        icbr,
        "_build_layer_shortlists_shared",
        lambda *args, **kwargs: {(0, 0): [candidate]},
    )
    monkeypatch.setattr(
        icbr,
        "replay_rerank_edge_candidates",
        lambda *args, **kwargs: {
            "best_candidate": {
                "candidate_index": 0,
                "fun_name": "x",
                "params": torch.tensor([1.0, 0.0, 1.0, 0.0], dtype=torch.float32),
                "r2": 1.0,
                "complexity": 1.0,
                "replay_score": 0.0,
            },
            "replay_rerank_wall_time_s": 0.0,
        },
    )

    symbolized_model, metrics = icbr._run_auto_symbolic_icbr_with_models(
        teacher_model,
        work_model,
        torch.zeros((4, 2), dtype=torch.float32),
        lib_names=["x"],
        topk=1,
        a_range=(-1.0, 1.0),
        b_range=(-1.0, 1.0),
        grid_number=3,
        iteration=1,
        verbose=0,
        collect_metrics=True,
    )

    assert metrics["candidate_mode"] == "shared"
    assert float(symbolized_model.act_fun[0].mask[0][0].item()) == 0.0
    assert float(symbolized_model.symbolic_fun[0].mask[0, 0].item()) == 1.0
    assert float(symbolized_model.act_fun[0].mask[1][0].item()) == 0.0
    assert float(symbolized_model.symbolic_fun[0].mask[0, 1].item()) == 0.0

