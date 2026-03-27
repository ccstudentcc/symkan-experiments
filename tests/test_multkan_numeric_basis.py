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
