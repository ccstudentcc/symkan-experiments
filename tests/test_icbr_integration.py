from __future__ import annotations

import pytest
import torch

from kan.MultKAN import MultKAN
from kan.icbr import _ensure_fully_symbolic_completion, _run_auto_symbolic_icbr_with_models


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


def test_fully_symbolic_completion_guard_rejects_partial_symbolic_state() -> None:
    model = MultKAN(width=[1, 1], grid=5, k=3, auto_save=False)
    with pytest.raises(RuntimeError, match="not fully symbolic"):
        _ensure_fully_symbolic_completion(model)
