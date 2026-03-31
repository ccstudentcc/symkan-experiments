from __future__ import annotations

import copy
import pytest
import torch

from kan import icbr as icbr_module
from kan.MultKAN import MultKAN
from kan.icbr import (
    _build_layer_shortlists_shared,
    _clear_model_runtime_caches,
    _ensure_fully_symbolic_completion,
    _run_auto_symbolic_icbr_with_models,
)


def test_auto_symbolic_icbr_minimal_integration() -> None:
    torch.manual_seed(0)
    model = MultKAN(width=[1, 1], grid=5, k=3, auto_save=False)
    x = torch.linspace(-1.0, 1.0, steps=24).unsqueeze(1)

    work_model = model.auto_symbolic_icbr(
        calibration_split=x,
        lib=["x", "x^2"],
        topk=2,
        grid_number=17,
        iteration=1,
        verbose=0,
    )

    assert work_model is not model
    assert model.act_fun[0].mask[0, 0].item() == 1.0
    assert model.symbolic_fun[0].mask[0, 0].item() == 0.0
    assert work_model.act_fun[0].mask[0, 0].item() == 0.0
    assert work_model.symbolic_fun[0].mask[0, 0].item() == 1.0

    formulas, variables = work_model.symbolic_formula(var=["x"])
    assert len(formulas) == 1
    assert str(formulas[0]) != ""
    assert len(variables) == 1


def test_auto_symbolic_icbr_requires_teacher_work_separation() -> None:
    model = MultKAN(width=[1, 1], grid=5, k=3, auto_save=False)
    x = torch.linspace(-0.8, 0.8, steps=16).unsqueeze(1)

    with pytest.raises(ValueError, match="different objects"):
        _run_auto_symbolic_icbr_with_models(
            model,
            model,
            x,
            lib_names=["x"],
            topk=1,
            a_range=(-2.0, 2.0),
            b_range=(-2.0, 2.0),
            grid_number=11,
            iteration=1,
            verbose=0,
        )


def test_auto_symbolic_verbose_zero_is_silent(capsys: pytest.CaptureFixture[str]) -> None:
    model = MultKAN(width=[1, 1], grid=5, k=3, auto_save=False)
    x = torch.linspace(-1.0, 1.0, steps=16).unsqueeze(1)
    model(x)

    model.auto_symbolic(lib=["x"], verbose=0, weight_simple=0.0, r2_threshold=0.0)

    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""


def test_build_layer_shortlists_shared_keeps_fixed_capacity_topk(monkeypatch: pytest.MonkeyPatch) -> None:
    teacher_acts_layer = torch.zeros((8, 2), dtype=torch.float32)
    teacher_edge_targets_layer = torch.zeros((8, 1, 2), dtype=torch.float32)
    edge_indices = [(0, 0), (1, 0)]
    candidate_payloads = {
        "f1": [(0.60, 3.0), (0.50, 3.0)],
        "f2": [(0.90, 4.0), (0.80, 5.0)],
        "f3": [(0.80, 2.0), (0.40, 1.0)],
    }

    def fake_generate_layer_candidates(
        teacher_acts: torch.Tensor,
        teacher_edge_targets: torch.Tensor,
        *,
        lib,
        edge_indices,
        a_range,
        b_range,
        grid_number,
        iteration,
    ):
        del teacher_acts, teacher_edge_targets, a_range, b_range, grid_number, iteration
        fun_name = list(lib)[0]
        specs = candidate_payloads[fun_name]
        candidates = []
        for (input_idx, output_idx), (r2, complexity) in zip(edge_indices, specs):
            candidates.append(
                {
                    "i": input_idx,
                    "j": output_idx,
                    "fun_name": fun_name,
                    "params": torch.tensor([1.0, 0.0, 1.0, 0.0]),
                    "r2": r2,
                    "complexity": complexity,
                    "diagnostics": {},
                }
            )
        return {"candidates": candidates}

    monkeypatch.setattr(icbr_module, "generate_layer_candidates", fake_generate_layer_candidates)

    shortlists = _build_layer_shortlists_shared(
        teacher_acts_layer,
        teacher_edge_targets_layer,
        edge_indices=edge_indices,
        lib_names=["f1", "f2", "f3"],
        topk=2,
        a_range=(-2.0, 2.0),
        b_range=(-2.0, 2.0),
        grid_number=11,
        iteration=1,
    )

    assert [item["fun_name"] for item in shortlists[(0, 0)]] == ["f2", "f3"]
    assert [item["fun_name"] for item in shortlists[(1, 0)]] == ["f2", "f1"]
    assert all(len(items) == 2 for items in shortlists.values())


def test_auto_symbolic_shared_mode_only_builds_candidates_for_active_edges(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    model = MultKAN(width=[1, 3, 1], grid=5, k=3, auto_save=False)
    teacher_model = copy.deepcopy(model)
    work_model = copy.deepcopy(model)
    calibration_input = torch.linspace(-1.0, 1.0, steps=16).unsqueeze(1)

    # edge (0,0) stays active; edge (0,1) is already symbolic; edge (0,2) is explicit zero
    work_model.act_fun[0].mask.data[0, 0] = 1.0
    work_model.symbolic_fun[0].mask.data[0, 0] = 0.0
    work_model.act_fun[0].mask.data[0, 1] = 0.0
    work_model.symbolic_fun[0].mask.data[1, 0] = 1.0
    work_model.act_fun[0].mask.data[0, 2] = 0.0
    work_model.symbolic_fun[0].mask.data[2, 0] = 0.0

    captured: dict[str, object] = {}

    def fake_build_layer_shortlists_shared(
        teacher_acts_layer: torch.Tensor,
        teacher_edge_targets_layer: torch.Tensor,
        *,
        edge_indices,
        lib_names,
        topk,
        a_range,
        b_range,
        grid_number,
        iteration,
    ):
        del teacher_acts_layer, teacher_edge_targets_layer, lib_names, topk, a_range, b_range, grid_number, iteration
        captured["edge_indices"] = list(edge_indices)
        raise RuntimeError("captured_active_edges")

    monkeypatch.setattr(icbr_module, "_build_layer_shortlists_shared", fake_build_layer_shortlists_shared)

    with pytest.raises(RuntimeError, match="captured_active_edges"):
        _run_auto_symbolic_icbr_with_models(
            teacher_model,
            work_model,
            calibration_input,
            lib_names=["x"],
            topk=1,
            a_range=(-2.0, 2.0),
            b_range=(-2.0, 2.0),
            grid_number=11,
            iteration=1,
            verbose=0,
            candidate_mode="shared",
            rerank_mode="local",
            commit_mode="explicit",
        )

    assert captured["edge_indices"] == [(0, 0)]


def test_clear_model_runtime_caches_removes_forward_artifacts() -> None:
    model = MultKAN(width=[1, 1], grid=5, k=3, auto_save=False)
    x = torch.linspace(-1.0, 1.0, steps=8).unsqueeze(1)
    model(x)
    model.symbolic_formula(var=["x"])

    assert model.acts is not None
    assert model.spline_postacts is not None
    assert model.cache_data is not None
    assert hasattr(model, "symbolic_acts")

    _clear_model_runtime_caches(model)

    assert model.acts is None
    assert model.spline_postacts is None
    assert model.spline_postsplines is None
    assert model.cache_data is None
    assert model.symbolic_acts is None


def test_fully_symbolic_completion_guard_rejects_partial_symbolic_state() -> None:
    model = MultKAN(width=[1, 1], grid=5, k=3, auto_save=False)
    with pytest.raises(RuntimeError, match="not fully symbolic"):
        _ensure_fully_symbolic_completion(model)
