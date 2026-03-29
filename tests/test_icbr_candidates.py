from __future__ import annotations

import copy
import math

import pytest
import torch

from kan.MultKAN import MultKAN
from kan.icbr import generate_layer_candidates
from kan.utils import SYMBOLIC_LIB, fit_params


def _snapshot_symbolic_state(model: MultKAN) -> list[dict[str, object]]:
    snapshots: list[dict[str, object]] = []
    for layer_idx, symbolic_layer in enumerate(model.symbolic_fun):
        out_dim = symbolic_layer.out_dim
        in_dim = symbolic_layer.in_dim
        snapshots.append(
            {
                "layer_idx": layer_idx,
                "funs_name": copy.deepcopy(symbolic_layer.funs_name),
                "affine": symbolic_layer.affine.detach().clone(),
                "symbolic_mask": symbolic_layer.mask.detach().clone(),
                "numeric_mask": model.act_fun[layer_idx].mask.detach().clone(),
                "funs_ids": [[id(symbolic_layer.funs[j][i]) for i in range(in_dim)] for j in range(out_dim)],
                "funs_sympy_ids": [
                    [id(symbolic_layer.funs_sympy[j][i]) for i in range(in_dim)] for j in range(out_dim)
                ],
                "funs_avoid_singularity_ids": [
                    [id(symbolic_layer.funs_avoid_singularity[j][i]) for i in range(in_dim)]
                    for j in range(out_dim)
                ],
            }
        )
    return snapshots


def _assert_symbolic_state_unchanged(model: MultKAN, before: list[dict[str, object]]) -> None:
    after = _snapshot_symbolic_state(model)
    assert len(after) == len(before)
    for previous, current in zip(before, after):
        assert previous["layer_idx"] == current["layer_idx"]
        assert previous["funs_name"] == current["funs_name"]
        assert torch.equal(previous["affine"], current["affine"])
        assert torch.equal(previous["symbolic_mask"], current["symbolic_mask"])
        assert torch.equal(previous["numeric_mask"], current["numeric_mask"])
        assert previous["funs_ids"] == current["funs_ids"]
        assert previous["funs_sympy_ids"] == current["funs_sympy_ids"]
        assert previous["funs_avoid_singularity_ids"] == current["funs_avoid_singularity_ids"]


def test_icbr_batched_candidates_match_single_edge_fit_params() -> None:
    torch.manual_seed(0)
    batch_size = 48
    x0 = torch.linspace(-0.9, 0.9, steps=batch_size)
    x1 = torch.linspace(-1.2, 0.8, steps=batch_size)
    teacher_acts = torch.stack([x0, x1], dim=1)

    y0 = 1.3 * (1.2 * x0 - 0.1).pow(3) + 0.4
    y1 = -0.8 * (-0.7 * x1 + 0.3).pow(3) - 0.2
    teacher_edge_targets = torch.zeros(batch_size, 1, 2)
    teacher_edge_targets[:, 0, 0] = y0
    teacher_edge_targets[:, 0, 1] = y1

    result = generate_layer_candidates(
        teacher_acts,
        teacher_edge_targets,
        lib=["x^3"],
        a_range=(-3.0, 3.0),
        b_range=(-3.0, 3.0),
        grid_number=41,
        iteration=2,
    )
    candidates = {(item["i"], item["j"]): item for item in result["candidates"]}

    for edge_i in (0, 1):
        params_ref, r2_ref = fit_params(
            teacher_acts[:, edge_i],
            teacher_edge_targets[:, 0, edge_i],
            SYMBOLIC_LIB["x^3"][0],
            a_range=(-3.0, 3.0),
            b_range=(-3.0, 3.0),
            grid_number=41,
            iteration=2,
            verbose=False,
        )
        candidate = candidates[(edge_i, 0)]
        assert candidate["fun_name"] == "x^3"
        assert candidate["complexity"] == float(SYMBOLIC_LIB["x^3"][2])
        a_hat, b_hat, c_hat, d_hat = candidate["params"]
        y_hat = c_hat * SYMBOLIC_LIB["x^3"][0](a_hat * teacher_acts[:, edge_i] + b_hat) + d_hat
        a_ref, b_ref, c_ref, d_ref = params_ref
        y_ref = c_ref * SYMBOLIC_LIB["x^3"][0](a_ref * teacher_acts[:, edge_i] + b_ref) + d_ref
        assert torch.allclose(y_hat, y_ref, atol=3e-4, rtol=2e-4)
        assert candidate["r2"] == pytest.approx(float(r2_ref.item()), rel=1e-5, abs=1e-5)


def test_icbr_candidate_generation_is_side_effect_free() -> None:
    torch.manual_seed(1)
    model = MultKAN(width=[2, 2, 1], grid=5, k=3, auto_save=False)
    x = torch.randn(32, 2)
    _ = model(x)

    state_before = _snapshot_symbolic_state(model)
    result = generate_layer_candidates(
        model.acts[0],
        model.spline_postacts[0],
        lib=["x", "x^2", "gaussian"],
        a_range=(-2.0, 2.0),
        b_range=(-2.0, 2.0),
        grid_number=21,
        iteration=2,
    )

    assert result["edge_count"] == 4
    _assert_symbolic_state_unchanged(model, state_before)


def test_icbr_candidate_generation_wall_time_smoke() -> None:
    torch.manual_seed(2)
    teacher_acts = torch.randn(64, 3)
    teacher_edge_targets = torch.randn(64, 2, 3)

    result = generate_layer_candidates(
        teacher_acts,
        teacher_edge_targets,
        lib=["x", "x^2", "gaussian"],
        a_range=(-2.0, 2.0),
        b_range=(-2.0, 2.0),
        grid_number=17,
        iteration=1,
    )

    assert result["edge_count"] == 6
    wall_time_s = result["candidate_generation_wall_time_s"]
    assert math.isfinite(wall_time_s)
    assert wall_time_s >= 0.0

    for candidate in result["candidates"]:
        diagnostics = candidate["diagnostics"]
        assert isinstance(diagnostics["boundary_hit"], bool)
        assert isinstance(diagnostics["nan_to_num_trigger"], bool)
        assert math.isfinite(diagnostics["top1_top2_margin"])
