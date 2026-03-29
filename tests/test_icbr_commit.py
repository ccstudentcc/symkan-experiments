from __future__ import annotations

import torch

from kan.MultKAN import MultKAN
from kan.icbr import commit_symbolic_candidate, generate_layer_candidates
from kan.utils import SYMBOLIC_LIB


def _single_edge_candidate(
    model: MultKAN,
    x: torch.Tensor,
    *,
    fun_name: str,
) -> dict[str, object]:
    _ = model(x)
    result = generate_layer_candidates(
        model.acts[0],
        model.spline_postacts[0],
        lib=[fun_name],
        edge_indices=[(0, 0)],
        a_range=(-2.0, 2.0),
        b_range=(-2.0, 2.0),
        grid_number=21,
        iteration=2,
    )
    return result["candidates"][0]


def test_commit_symbolic_candidate_supports_formula_export() -> None:
    torch.manual_seed(0)
    model = MultKAN(width=[1, 1], grid=5, k=3, auto_save=False)
    x = torch.linspace(-1.0, 1.0, steps=32).unsqueeze(1)
    candidate = _single_edge_candidate(model, x, fun_name="x")

    commit_symbolic_candidate(model, layer_idx=0, input_idx=0, output_idx=0, candidate=candidate)
    y = model(x)

    formulas, variables = model.symbolic_formula(var=["x"])
    assert y.shape == (32, 1)
    assert len(formulas) == 1
    assert str(formulas[0]) != ""
    assert len(variables) == 1


def test_commit_symbolic_candidate_supports_zero_function() -> None:
    model = MultKAN(width=[1, 1], grid=5, k=3, auto_save=False)
    x = torch.linspace(-1.0, 1.0, steps=24).unsqueeze(1)

    commit_symbolic_candidate(
        model,
        layer_idx=0,
        input_idx=0,
        output_idx=0,
        candidate={"fun_name": "0"},
    )

    y = model(x)
    formulas, _ = model.symbolic_formula(var=["x"])
    assert torch.allclose(y, torch.zeros_like(y), atol=1e-6, rtol=1e-6)
    assert str(formulas[0]) in {"0", "0.0"}


def test_commit_symbolic_candidate_keeps_symbolic_state_consistent() -> None:
    model = MultKAN(width=[1, 1], grid=5, k=3, auto_save=False)
    x = torch.linspace(-0.8, 0.8, steps=20).unsqueeze(1)
    candidate = _single_edge_candidate(model, x, fun_name="x^2")

    commit_symbolic_candidate(model, layer_idx=0, input_idx=0, output_idx=0, candidate=candidate)
    symbolic_layer = model.symbolic_fun[0]

    assert symbolic_layer.funs_name[0][0] == candidate["fun_name"]
    assert symbolic_layer.funs[0][0] is SYMBOLIC_LIB[candidate["fun_name"]][0]
    assert symbolic_layer.funs_sympy[0][0] is SYMBOLIC_LIB[candidate["fun_name"]][1]
    assert symbolic_layer.funs_avoid_singularity[0][0] is SYMBOLIC_LIB[candidate["fun_name"]][3]
    assert torch.allclose(symbolic_layer.affine.data[0, 0], torch.as_tensor(candidate["params"]), atol=1e-6, rtol=1e-6)
    assert model.act_fun[0].mask[0, 0].item() == 0.0
    assert symbolic_layer.mask[0, 0].item() == 1.0
