from pathlib import Path
import shutil
import uuid

import torch

from kan.FastKANLayer import FastKANLayer
from kan.KANLayer import KANLayer
from kan.MultKAN import MultKAN
from symkan.io.checkpoint import clone_model
from symkan.pruning.attribution import safe_attribute
from symkan.symbolic.compact import compact_inputs_for_symbolic


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


def test_multkan_radial_bf_disk_clone_keeps_numeric_basis() -> None:
    torch.manual_seed(6)
    model = MultKAN(width=[2, 3, 1], grid=5, k=3, auto_save=False, numeric_basis="radial_bf")
    _ = model(torch.randn(6, 2))

    tmp_dir = Path("tmp") / f"multkan_clone_{uuid.uuid4().hex}"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    try:
        clone = clone_model(model, use_disk_clone=True, ckpt_path=str(tmp_dir / "clone_ckpt"))
        assert clone.numeric_basis == "radial_bf"
        assert isinstance(clone.act_fun[0], FastKANLayer)
        assert clone(torch.randn(4, 2)).shape == (4, 1)
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


def test_multkan_radial_bf_attribute_drives_prune_edge() -> None:
    torch.manual_seed(4)
    model = MultKAN(width=[3, 3, 1], grid=5, k=3, auto_save=False, numeric_basis="radial_bf")
    x = torch.randn(32, 3)
    y = (x[:, :1] * 0.5) - (x[:, 1:2] * 0.2)
    dataset = {
        "train_input": x,
        "train_label": y,
        "test_input": x.clone(),
        "test_label": y.clone(),
    }

    _ = model(x)
    feature_score = safe_attribute(model, dataset, n_sample=16)
    assert feature_score.shape == (3,)

    active_before = int((model.act_fun[0].mask != 0).sum().item())
    model.prune_edge(threshold=1e9, log_history=False)
    active_after = int((model.act_fun[0].mask != 0).sum().item())
    assert active_after <= active_before
    assert active_after == 0


def test_multkan_radial_bf_input_compaction_returns_usable_model() -> None:
    torch.manual_seed(5)
    model = MultKAN(width=[3, 3, 1], grid=5, k=3, auto_save=False, numeric_basis="radial_bf")
    x = torch.randn(20, 3)
    dataset = {
        "train_input": x,
        "train_label": torch.randn(20, 1),
        "test_input": x.clone(),
        "test_label": torch.randn(20, 1),
    }

    _ = model(x)
    model.act_fun[0].mask.data.zero_()
    model.symbolic_fun[0].mask.data.zero_()
    model.act_fun[0].mask.data[1, 0] = 1.0

    compact_state = compact_inputs_for_symbolic(model, dataset)
    assert compact_state is not None
    assert compact_state["active_inputs"] == [1]

    compact_model = compact_state["model"]
    assert compact_model.numeric_basis == "radial_bf"
    assert isinstance(compact_model.act_fun[0], FastKANLayer)

    compact_dataset = compact_state["dataset"]
    assert compact_dataset["train_input"].shape == (20, 1)
    assert compact_dataset["test_input"].shape == (20, 1)
    assert compact_model(torch.randn(8, 1)).shape == (8, 1)
