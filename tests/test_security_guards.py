from __future__ import annotations

import shutil
import uuid
from contextlib import contextmanager
from pathlib import Path

import torch
import pytest

from scripts.ablation_runner import normalize_optional_path
from scripts.project_paths import resolve_named_child, validate_child_name
from symkan.config import ConfigError, load_config
from symkan.eval.metrics import validate_formula_numerically
from symkan.io.checkpoint import DEFAULT_CLONE_CKPT_PREFIX, _checkpoint_prefix
from symkan.io.results import load_export_bundle, save_export_bundle
from symkan.symbolic.library import collect_valid_formulas


@contextmanager
def local_temp_dir():
    root = Path("outputs/test_tmp")
    path = (root / f"security-{uuid.uuid4().hex}").resolve()
    path.mkdir(parents=True, exist_ok=True)
    try:
        yield path
    finally:
        shutil.rmtree(path, ignore_errors=True)


class IdentityModel:
    def eval(self):
        return self

    def __call__(self, x):
        return x


def test_load_export_bundle_requires_explicit_trust() -> None:
    with local_temp_dir() as temp_dir:
        bundle_path = temp_dir / "bundle.pkl"
        save_export_bundle({"ok": True}, path=str(bundle_path))

        with pytest.raises(ValueError, match="trusted=True"):
            load_export_bundle(str(bundle_path))


def test_load_export_bundle_accepts_trusted_local_bundle() -> None:
    with local_temp_dir() as temp_dir:
        bundle_path = temp_dir / "bundle.pkl"
        save_export_bundle({"ok": True}, path=str(bundle_path))

        loaded = load_export_bundle(str(bundle_path), trusted=True)

        assert loaded == {"ok": True}


def test_checkpoint_prefix_uses_unique_temp_dir_and_cleans_up(monkeypatch: pytest.MonkeyPatch) -> None:
    with local_temp_dir() as temp_dir:
        monkeypatch.chdir(temp_dir)

        with _checkpoint_prefix(DEFAULT_CLONE_CKPT_PREFIX) as prefix:
            artifact = Path(f"{prefix}_state")
            artifact.write_text("checkpoint", encoding="utf-8")
            assert prefix.parent == temp_dir
            assert prefix.name.startswith("symkan-clone-")
            assert artifact.exists()

        assert not Path(f"{prefix}_state").exists()


def test_checkpoint_prefix_cleans_custom_prefix_artifacts() -> None:
    with local_temp_dir() as temp_dir:
        prefix = temp_dir / "custom" / "clone"

        with _checkpoint_prefix(str(prefix)) as active_prefix:
            artifact = Path(f"{active_prefix}_cache_data")
            artifact.write_text("cache", encoding="utf-8")
            assert artifact.exists()

        assert prefix.parent.exists()
        assert not Path(f"{prefix}_cache_data").exists()


def test_collect_valid_formulas_rejects_unsafe_expression_text() -> None:
    formulas = ["__import__('os').system('echo bad')", "x_0 + 1"]

    valid = collect_valid_formulas(formulas)

    assert valid == [{"index": 1, "expr": "x_0 + 1", "complexity": 3}]


def test_validate_formula_numerically_handles_short_test_sets() -> None:
    dataset = {
        "test_input": torch.tensor([[1.0], [2.0]], dtype=torch.float32),
        "test_label": torch.tensor([[1.0], [2.0]], dtype=torch.float32),
    }

    result = validate_formula_numerically(IdentityModel(), ["x_0"], dataset, n_sample=5)

    assert result is not None
    assert len(result) == 1
    assert result.loc[0, "index"] == 0
    assert result.loc[0, "r2"] == pytest.approx(1.0)


def test_validate_formula_numerically_returns_empty_frame_for_empty_test_split() -> None:
    dataset = {
        "test_input": torch.empty((0, 1), dtype=torch.float32),
        "test_label": torch.empty((0, 1), dtype=torch.float32),
    }

    result = validate_formula_numerically(IdentityModel(), ["x_0"], dataset, n_sample=5)

    assert result is not None
    assert result.empty


def test_validate_child_name_rejects_path_traversal() -> None:
    with pytest.raises(ValueError, match="invalid variant name"):
        validate_child_name("..\\outside", kind="variant name")


def test_resolve_named_child_stays_within_root() -> None:
    with local_temp_dir() as temp_dir:
        resolved = resolve_named_child(temp_dir, "variant-01", kind="variant name")

        assert resolved == (temp_dir / "variant-01").resolve()


def test_normalize_optional_path_returns_absolute_path(monkeypatch: pytest.MonkeyPatch) -> None:
    with local_temp_dir() as temp_dir:
        monkeypatch.chdir(temp_dir)
        relative = Path("configs/example.yaml")

        normalized = normalize_optional_path(str(relative))

        assert normalized == str((temp_dir / relative).resolve())


def test_load_config_wraps_yaml_parse_errors() -> None:
    with local_temp_dir() as temp_dir:
        config_path = temp_dir / "broken.yaml"
        config_path.write_text("runtime: [", encoding="utf-8")

        with pytest.raises(ConfigError, match="failed to parse YAML"):
            load_config(config_path)
