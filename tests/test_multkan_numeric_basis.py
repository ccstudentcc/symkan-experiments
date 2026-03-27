from pathlib import Path
import shutil
import uuid

import torch

from kan.FastKANLayer import FastKANLayer
from kan.KANLayer import KANLayer
from kan.MultKAN import MultKAN


def test_multkan_default_numeric_basis_is_bspline() -> None:
    model = MultKAN(width=[2, 3, 1], grid=5, k=3, auto_save=False)
    assert model.numeric_basis == "bspline"
    assert isinstance(model.act_fun[0], KANLayer)


def test_multkan_radial_bf_builds_fast_layers_and_runs_backward() -> None:
    torch.manual_seed(0)
    model = MultKAN(width=[2, 3, 1], grid=5, k=3, auto_save=False, numeric_basis="radial_bf")
    x = torch.randn(8, 2)

    y = model(x)
    loss = y.pow(2).mean()
    loss.backward()

    assert y.shape == (8, 1)
    assert isinstance(model.act_fun[0], FastKANLayer)
    assert isinstance(model.act_fun[1], FastKANLayer)


def test_multkan_radial_bf_survives_prune_input_and_checkpoint_roundtrip() -> None:
    torch.manual_seed(1)
    model = MultKAN(width=[2, 3, 1], grid=5, k=3, auto_save=False, numeric_basis="radial_bf")
    pruned = model.prune_input(active_inputs=[0], log_history=False)

    assert pruned.numeric_basis == "radial_bf"
    assert isinstance(pruned.act_fun[0], FastKANLayer)
    assert pruned(torch.randn(4, 1)).shape == (4, 1)

    tmp_dir = Path("tmp") / f"multkan_ckpt_{uuid.uuid4().hex}"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    try:
        ckpt_path = str(tmp_dir / "radial_bf_ckpt")
        pruned.saveckpt(ckpt_path)
        loaded = MultKAN.loadckpt(ckpt_path)

        assert loaded.numeric_basis == "radial_bf"
        assert isinstance(loaded.act_fun[0], FastKANLayer)
        assert loaded(torch.randn(4, 1)).shape == (4, 1)
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


def test_multkan_radial_bf_cache_alignment_for_symbolic_fitting() -> None:
    torch.manual_seed(2)
    model = MultKAN(width=[1, 1], grid=5, k=3, auto_save=False, numeric_basis="radial_bf")
    x = torch.linspace(-1.0, 1.0, steps=16).unsqueeze(1)

    y = model(x)
    assert y.shape == (16, 1)
    assert isinstance(model.act_fun[0], FastKANLayer)

    layer = model.act_fun[0]
    _, preacts_expected, postacts_expected, postsplines_expected = layer(model.acts[0])

    assert model.spline_preacts[0].shape == preacts_expected.shape
    assert model.spline_postacts[0].shape == postacts_expected.shape
    assert model.spline_postsplines[0].shape == postsplines_expected.shape

    assert torch.allclose(model.spline_preacts[0], preacts_expected, atol=1e-6, rtol=1e-5)
    assert torch.allclose(model.spline_postacts[0], postacts_expected, atol=1e-6, rtol=1e-5)
    assert torch.allclose(model.spline_postsplines[0], postsplines_expected, atol=1e-6, rtol=1e-5)


def test_multkan_radial_bf_supports_suggest_fix_and_formula_export() -> None:
    torch.manual_seed(3)
    model = MultKAN(width=[1, 1], grid=5, k=3, auto_save=False, numeric_basis="radial_bf")
    x = torch.linspace(-1.0, 1.0, steps=24).unsqueeze(1)
    model(x)

    best_name, _, best_r2, _ = model.suggest_symbolic(
        0,
        0,
        0,
        lib=["x", "x^2", "gaussian"],
        topk=2,
        verbose=False,
        weight_simple=0.0,
    )
    assert best_name in {"x", "x^2", "gaussian"}
    assert float(best_r2) > -1e7

    r2 = model.fix_symbolic(0, 0, 0, best_name, fit_params_bool=True, verbose=False, log_history=False)
    assert r2 is not None
    assert model.act_fun[0].mask[0, 0].item() == 0.0
    assert model.symbolic_fun[0].mask[0, 0].item() == 1.0

    y_after = model(x)
    assert y_after.shape == (24, 1)

    formulas, variables = model.symbolic_formula(var=["x"])
    assert len(formulas) == 1
    assert str(formulas[0]) != ""
    assert len(variables) == 1
