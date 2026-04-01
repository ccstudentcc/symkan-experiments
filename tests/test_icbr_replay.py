from __future__ import annotations

import copy
from pathlib import Path
import uuid

import torch

from kan.MultKAN import MultKAN
from kan.icbr import generate_layer_candidates, replay_rerank_edge_candidates
from kan.utils import SYMBOLIC_LIB


def _edge_state_snapshot(model: MultKAN, layer_idx: int, input_idx: int, output_idx: int) -> dict[str, object]:
    symbolic_layer = model.symbolic_fun[layer_idx]
    return {
        "fun_id": id(symbolic_layer.funs[output_idx][input_idx]),
        "fun_sympy_id": id(symbolic_layer.funs_sympy[output_idx][input_idx]),
        "fun_avoid_id": id(symbolic_layer.funs_avoid_singularity[output_idx][input_idx]),
        "fun_name": symbolic_layer.funs_name[output_idx][input_idx],
        "affine": symbolic_layer.affine.data[output_idx, input_idx].detach().clone(),
        "numeric_mask": model.act_fun[layer_idx].mask.data[input_idx][output_idx].detach().clone(),
        "symbolic_mask": symbolic_layer.mask.data[output_idx][input_idx].detach().clone(),
    }


def _assert_edge_state_equal(before: dict[str, object], after: dict[str, object]) -> None:
    assert before["fun_id"] == after["fun_id"]
    assert before["fun_sympy_id"] == after["fun_sympy_id"]
    assert before["fun_avoid_id"] == after["fun_avoid_id"]
    assert before["fun_name"] == after["fun_name"]
    assert torch.equal(before["affine"], after["affine"])
    assert torch.equal(before["numeric_mask"], after["numeric_mask"])
    assert torch.equal(before["symbolic_mask"], after["symbolic_mask"])


def _single_edge_candidate(
    teacher_model: MultKAN,
    calibration_input: torch.Tensor,
    *,
    fun_name: str,
) -> dict[str, object]:
    _ = teacher_model(calibration_input)
    result = generate_layer_candidates(
        teacher_model.acts[0],
        teacher_model.spline_postacts[0],
        lib=[fun_name],
        edge_indices=[(0, 0)],
        a_range=(-2.0, 2.0),
        b_range=(-2.0, 2.0),
        grid_number=21,
        iteration=2,
    )
    return result["candidates"][0]


def _directory_snapshot(path: Path) -> list[tuple[str, int]]:
    if not path.exists():
        return []
    records: list[tuple[str, int]] = []
    for file_path in sorted(item for item in path.rglob("*") if item.is_file()):
        records.append((str(file_path.relative_to(path)), file_path.stat().st_size))
    return records


def test_replay_rerank_restores_symbolic_edge_state() -> None:
    torch.manual_seed(0)
    work_model = MultKAN(width=[1, 1], grid=5, k=3, auto_save=False)
    teacher_model = copy.deepcopy(work_model)
    calibration_input = torch.linspace(-1.0, 1.0, steps=32).unsqueeze(1)

    shortlist = [
        _single_edge_candidate(teacher_model, calibration_input, fun_name="x"),
        _single_edge_candidate(teacher_model, calibration_input, fun_name="x^2"),
    ]

    before = _edge_state_snapshot(work_model, layer_idx=0, input_idx=0, output_idx=0)
    replay_result = replay_rerank_edge_candidates(
        work_model,
        teacher_model,
        calibration_input,
        layer_idx=0,
        input_idx=0,
        output_idx=0,
        shortlist=shortlist,
    )
    after = _edge_state_snapshot(work_model, layer_idx=0, input_idx=0, output_idx=0)

    assert len(replay_result["ranked_candidates"]) == 2
    _assert_edge_state_equal(before, after)


def test_replay_rerank_has_no_history_or_checkpoint_side_effects() -> None:
    torch.manual_seed(1)
    run_root = Path("tmp") / f"icbr_replay_{uuid.uuid4().hex}"
    work_ckpt_path = run_root / "work_ckpt"
    teacher_ckpt_path = run_root / "teacher_ckpt"

    work_model = MultKAN(width=[1, 1], grid=5, k=3, auto_save=True, ckpt_path=str(work_ckpt_path))
    teacher_model = MultKAN(width=[1, 1], grid=5, k=3, auto_save=True, ckpt_path=str(teacher_ckpt_path))
    teacher_model.load_state_dict(work_model.state_dict())

    calibration_input = torch.linspace(-0.8, 0.8, steps=24).unsqueeze(1)
    shortlist = [
        _single_edge_candidate(teacher_model, calibration_input, fun_name="x"),
        _single_edge_candidate(teacher_model, calibration_input, fun_name="x^2"),
    ]

    work_state_id_before = work_model.state_id
    teacher_state_id_before = teacher_model.state_id
    work_history_before = (work_ckpt_path / "history.txt").read_text(encoding="utf-8")
    teacher_history_before = (teacher_ckpt_path / "history.txt").read_text(encoding="utf-8")
    work_files_before = _directory_snapshot(work_ckpt_path)
    teacher_files_before = _directory_snapshot(teacher_ckpt_path)

    replay_rerank_edge_candidates(
        work_model,
        teacher_model,
        calibration_input,
        layer_idx=0,
        input_idx=0,
        output_idx=0,
        shortlist=shortlist,
    )

    assert work_model.state_id == work_state_id_before
    assert teacher_model.state_id == teacher_state_id_before
    assert (work_ckpt_path / "history.txt").read_text(encoding="utf-8") == work_history_before
    assert (teacher_ckpt_path / "history.txt").read_text(encoding="utf-8") == teacher_history_before
    assert _directory_snapshot(work_ckpt_path) == work_files_before
    assert _directory_snapshot(teacher_ckpt_path) == teacher_files_before


class _ToyActLayer:
    def __init__(self) -> None:
        self.mask = torch.ones((1, 1), dtype=torch.float32)


class _ToySymbolicLayer:
    def __init__(self) -> None:
        self.in_dim = 1
        self.out_dim = 1
        self.funs = [[SYMBOLIC_LIB["0"][0]]]
        self.funs_sympy = [[SYMBOLIC_LIB["0"][1]]]
        self.funs_avoid_singularity = [[SYMBOLIC_LIB["0"][3]]]
        self.funs_name = [["0"]]
        self.affine = torch.nn.Parameter(torch.tensor([[[1.0, 0.0, 1.0, 0.0]]], dtype=torch.float32))
        self.mask = torch.zeros((1, 1), dtype=torch.float32)


class _ToyWorkModel:
    def __init__(self) -> None:
        self.symbolic_fun = [_ToySymbolicLayer()]
        self.act_fun = [_ToyActLayer()]
        self.state_id = 0

    def __call__(self, x: torch.Tensor, singularity_avoiding: bool = False, y_th: float = 10.0) -> torch.Tensor:
        del singularity_avoiding, y_th
        symbolic_layer = self.symbolic_fun[0]
        if self.act_fun[0].mask[0, 0].item() == 0.0 and symbolic_layer.mask[0, 0].item() == 1.0:
            a, b, c, d = symbolic_layer.affine.data[0, 0]
            fun = symbolic_layer.funs[0][0]
            output = c * fun(a * x[:, 0] + b) + d
            return output.unsqueeze(1)
        return torch.zeros((x.shape[0], 1), dtype=x.dtype)


class _ToyTeacherModel:
    def __init__(self) -> None:
        self.state_id = 0

    def __call__(self, x: torch.Tensor, singularity_avoiding: bool = False, y_th: float = 10.0) -> torch.Tensor:
        del singularity_avoiding, y_th
        return (x[:, 0] ** 2).unsqueeze(1)


class _CountingToyTeacherModel(_ToyTeacherModel):
    def __init__(self) -> None:
        super().__init__()
        self.call_count = 0

    def __call__(self, x: torch.Tensor, singularity_avoiding: bool = False, y_th: float = 10.0) -> torch.Tensor:
        self.call_count += 1
        return super().__call__(x, singularity_avoiding=singularity_avoiding, y_th=y_th)


def test_replay_rerank_can_disagree_with_local_r2_top1() -> None:
    work_model = _ToyWorkModel()
    teacher_model = _ToyTeacherModel()
    calibration_input = torch.linspace(-1.0, 1.0, steps=21).unsqueeze(1)

    shortlist = [
        {"fun_name": "x", "params": torch.tensor([1.0, 0.0, 1.0, 0.0]), "r2": 0.99, "complexity": 1.0},
        {"fun_name": "x^2", "params": torch.tensor([1.0, 0.0, 1.0, 0.0]), "r2": 0.92, "complexity": 2.0},
    ]

    result = replay_rerank_edge_candidates(
        work_model,
        teacher_model,
        calibration_input,
        layer_idx=0,
        input_idx=0,
        output_idx=0,
        shortlist=shortlist,
    )

    assert max(shortlist, key=lambda item: item["r2"])["fun_name"] == "x"
    assert result["best_candidate"]["fun_name"] == "x^2"
    assert work_model.symbolic_fun[0].funs_name[0][0] == "0"
    assert work_model.act_fun[0].mask[0, 0].item() == 1.0
    assert work_model.symbolic_fun[0].mask[0, 0].item() == 0.0


def test_replay_rerank_reuses_precomputed_teacher_output_when_provided() -> None:
    work_model = _ToyWorkModel()
    teacher_model = _CountingToyTeacherModel()
    calibration_input = torch.linspace(-1.0, 1.0, steps=21).unsqueeze(1)
    cached_teacher_output = (calibration_input[:, 0] ** 2).unsqueeze(1)

    shortlist = [
        {"fun_name": "x", "params": torch.tensor([1.0, 0.0, 1.0, 0.0]), "r2": 0.99, "complexity": 1.0},
        {"fun_name": "x^2", "params": torch.tensor([1.0, 0.0, 1.0, 0.0]), "r2": 0.92, "complexity": 2.0},
    ]

    result = replay_rerank_edge_candidates(
        work_model,
        teacher_model,
        calibration_input,
        layer_idx=0,
        input_idx=0,
        output_idx=0,
        shortlist=shortlist,
        teacher_output=cached_teacher_output,
    )

    assert teacher_model.call_count == 0
    assert result["best_candidate"]["fun_name"] == "x^2"
