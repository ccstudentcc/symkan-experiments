from __future__ import annotations

import shutil
import uuid
from contextlib import contextmanager
from pathlib import Path

import numpy as np
import pytest

from scripts.symkanbenchmark import ensure_numpy_dataset_files
from symkan.config import ConfigError, load_config, validate_app_config


@contextmanager
def local_temp_dir():
    root = Path("outputs/test_tmp")
    path = (root / f"config-boundary-{uuid.uuid4().hex}").resolve()
    path.mkdir(parents=True, exist_ok=True)
    try:
        yield path
    finally:
        shutil.rmtree(path, ignore_errors=True)


def _synthetic_mnist():
    x_train = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=np.float32)
    x_test = np.array([[0.5, 0.5]], dtype=np.float32)
    y_train = np.array([[1.0, 0.0], [0.0, 1.0]], dtype=np.float32)
    y_test = np.array([[1.0, 0.0]], dtype=np.float32)
    return x_train, x_test, y_train, y_test


def test_load_config_expands_env_as_scalar_without_yaml_injection(monkeypatch: pytest.MonkeyPatch) -> None:
    with local_temp_dir() as temp_dir:
        config_path = temp_dir / "app.yaml"
        config_path.write_text(
            "runtime:\n"
            "  device: ${SYMKAN_DEVICE}\n"
            "symbolize:\n"
            "  target_edges: 47\n",
            encoding="utf-8",
        )
        monkeypatch.setenv("SYMKAN_DEVICE", "cpu\nsymbolize:\n  target_edges: 1")

        config = load_config(config_path)

        assert config.runtime.device == "cpu\nsymbolize:\n  target_edges: 1"
        assert config.symbolize.target_edges == 47


def test_ensure_numpy_dataset_files_rejects_autofetch_outside_data_dir() -> None:
    with local_temp_dir() as temp_dir:
        repo_root = temp_dir / "repo"
        repo_root.mkdir()
        config = validate_app_config(
            {
                "data": {
                    "x_train": "custom/X_train.npy",
                    "x_test": "custom/X_test.npy",
                    "y_train": "custom/Y_train_cat.npy",
                    "y_test": "custom/Y_test_cat.npy",
                    "auto_fetch_mnist": True,
                }
            }
        )

        with pytest.raises(ConfigError, match="allow_auto_fetch_outside_data_dir"):
            ensure_numpy_dataset_files(config, repo_root)


def test_ensure_numpy_dataset_files_allows_opted_in_external_autofetch(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    with local_temp_dir() as temp_dir:
        repo_root = temp_dir / "repo"
        repo_root.mkdir()
        config = validate_app_config(
            {
                "data": {
                    "x_train": "custom/X_train.npy",
                    "x_test": "custom/X_test.npy",
                    "y_train": "custom/Y_train_cat.npy",
                    "y_test": "custom/Y_test_cat.npy",
                    "auto_fetch_mnist": True,
                    "allow_auto_fetch_outside_data_dir": True,
                    "mnist_classes": [0, 1],
                }
            }
        )

        monkeypatch.setattr("scripts.symkanbenchmark._fetch_mnist_via_keras", lambda classes: (_ for _ in ()).throw(OSError("keras unavailable")))
        monkeypatch.setattr("scripts.symkanbenchmark._fetch_mnist_via_openml", lambda classes: _synthetic_mnist())

        with pytest.warns(UserWarning, match="falling back to OpenML"):
            ensure_numpy_dataset_files(config, repo_root)

        assert (repo_root / "custom" / "X_train.npy").exists()
        assert (repo_root / "custom" / "X_test.npy").exists()
        assert (repo_root / "custom" / "Y_train_cat.npy").exists()
        assert (repo_root / "custom" / "Y_test_cat.npy").exists()
