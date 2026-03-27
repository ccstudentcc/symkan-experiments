from __future__ import annotations

import csv
import json
from pathlib import Path

import numpy as np
import pytest
import yaml

from scripts.symbolnet import (
    DEFAULT_SYMBOLNET_CONFIG_PATH,
    SymbolNetConfigError,
    SymbolNetRunnerConfig,
    _onehot_from_labels,
    _select_classes,
    parse_symbolnet_cli_config,
    run_symbolnet,
)


def test_select_classes_filters_only_requested_labels() -> None:
    x = np.array([[0.0], [1.0], [2.0], [3.0]], dtype=np.float32)
    y = np.array([0, 1, 2, 3], dtype=np.int64)

    selected_x, selected_y = _select_classes(x, y, [1, 3])

    assert selected_x.shape == (2, 1)
    assert selected_y.tolist() == [1, 3]


def test_onehot_mapping_follows_class_order() -> None:
    y = np.array([7, 3, 7, 9], dtype=np.int64)
    onehot = _onehot_from_labels(y, [3, 7, 9])

    assert onehot.shape == (4, 3)
    assert onehot[0].tolist() == [0.0, 1.0, 0.0]
    assert onehot[1].tolist() == [1.0, 0.0, 0.0]
    assert onehot[3].tolist() == [0.0, 0.0, 1.0]


def test_parse_symbolnet_cli_config_maps_overrides() -> None:
    cfg = parse_symbolnet_cli_config(
        [
            "--seeds",
            "42,52",
            "--classes",
            "0,1",
            "--epochs",
            "5",
            "--batch-size",
            "64",
            "--learning-rate",
            "0.001",
            "--num-hidden-layers",
            "2",
            "--unary-ops",
            "sin,tanh",
            "--binary-ops",
            "+,*",
            "--num-unary",
            "8",
            "--num-binary",
            "2",
            "--quiet",
        ]
    )

    assert cfg.seeds == "42,52"
    assert cfg.classes == "0,1"
    assert cfg.epochs == 5
    assert cfg.batch_size == 64
    assert cfg.learning_rate == 0.001
    assert cfg.num_hidden_layers == 2
    assert cfg.unary_ops == ["sin", "tanh"]
    assert cfg.binary_ops == ["+", "*"]
    assert cfg.num_unary == 8
    assert cfg.num_binary == 2
    assert cfg.quiet is True


def test_parse_symbolnet_cli_config_uses_default_template() -> None:
    cfg = parse_symbolnet_cli_config([])
    template_path = Path(cfg.config_path)
    template_payload = yaml.safe_load(template_path.read_text(encoding="utf-8"))

    assert cfg.config_path is not None
    assert cfg.config_path.replace("\\", "/").endswith(DEFAULT_SYMBOLNET_CONFIG_PATH)
    assert cfg.output_dir == str(template_payload["run"]["output_dir"])
    assert cfg.epochs == int(template_payload["model"]["epochs"])
    assert cfg.batch_size == int(template_payload["model"]["batch_size"])
    assert cfg.quiet is bool(template_payload["run"]["quiet"])


def test_parse_symbolnet_cli_config_accepts_custom_template_and_cli_override(tmp_path: Path) -> None:
    config_path = tmp_path / "symbolnet.custom.yaml"
    config_path.write_text(
        "template:\n"
        "  kind: symbolnet\n"
        "  version: 1\n"
        "run:\n"
        "  output_dir: outputs/custom_symbolnet\n"
        "  seeds: \"11,22\"\n"
        "  quiet: true\n"
        "data:\n"
        "  classes: \"0,1\"\n"
        "model:\n"
        "  epochs: 9\n"
        "  batch_size: 64\n"
        "  unary_ops: \"sin,tanh\"\n"
        "  binary_ops: \"*\"\n"
        "  num_unary: 6\n"
        "  num_binary: 2\n"
        "sparsity:\n"
        "  alpha_sparsity_input: 0.9\n"
        "  alpha_sparsity_model: 0.8\n"
        "  alpha_sparsity_unary: 0.3\n"
        "  alpha_sparsity_binary: 0.2\n",
        encoding="utf-8",
    )

    cfg = parse_symbolnet_cli_config(
        [
            "--config",
            str(config_path),
            "--epochs",
            "5",
            "--no-quiet",
        ]
    )

    assert cfg.seeds == "11,22"
    assert cfg.classes == "0,1"
    assert cfg.batch_size == 64
    assert cfg.epochs == 5
    assert cfg.quiet is False


def test_parse_symbolnet_cli_config_rejects_mismatched_template_kind(tmp_path: Path) -> None:
    bad_config_path = tmp_path / "bad.yaml"
    bad_config_path.write_text(
        "template:\n"
        "  kind: symkan\n"
        "  version: 1\n",
        encoding="utf-8",
    )

    with pytest.raises(SymbolNetConfigError, match="template.kind"):
        parse_symbolnet_cli_config(["--config", str(bad_config_path)])


def test_run_symbolnet_writes_summary_and_run_artifacts(
    monkeypatch,
    tmp_path: Path,
) -> None:
    runner = SymbolNetRunnerConfig(
        output_dir=str(tmp_path / "runs"),
        seeds="42,52",
        classes="0,1",
        epochs=2,
        batch_size=8,
        quiet=True,
    )
    runner.normalize()

    fake_dataset = {
        "X_train": np.zeros((12, 4), dtype=np.float32),
        "X_test": np.zeros((6, 4), dtype=np.float32),
        "Y_train": np.zeros((12, 2), dtype=np.float32),
        "Y_test": np.zeros((6, 2), dtype=np.float32),
        "source": "synthetic",
        "input_dim": 4,
        "output_dim": 2,
    }
    monkeypatch.setattr("scripts.symbolnet.load_mnist_data", lambda classes, mt, me: fake_dataset)

    def _fake_train_once(runner_cfg, dataset, seed):
        return {
            "history": {"loss": [1.2, 0.8], "accuracy": [0.5, 0.75]},
            "accuracy": 0.75 if seed == 42 else 0.8,
            "macro_auc_ovr": 0.81 if seed == 42 else 0.84,
            "class_auc": {0: 0.8, 1: 0.82},
            "train_seconds": 0.12,
            "predict_seconds": 0.02,
            "samples_train": int(dataset["X_train"].shape[0]),
            "samples_test": int(dataset["X_test"].shape[0]),
            "symbolic_model": object(),
            "model_dim": [4, 1, 2],
            "operators": [[["sin"], ["*"]]],
            "num_operators": [[2, 0]],
        }

    monkeypatch.setattr("scripts.symbolnet.train_symbolnet_once", _fake_train_once)
    monkeypatch.setattr(
        "scripts.symbolnet._build_symbolic_summary_rows",
        lambda **kwargs: [
            {"类别": 0, "表达式": "x_0", "复杂度": 1, "AUC": 0.8, "expr_full": "x_0"},
            {"类别": 1, "表达式": "x_1", "复杂度": 1, "AUC": 0.82, "expr_full": "x_1"},
        ],
    )

    run_symbolnet(runner)

    output_dir = Path(runner.output_dir)
    summary_path = output_dir / "symbolnet_runs.csv"
    assert summary_path.exists()

    with summary_path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 2
    assert rows[0]["seed"] == "42"
    assert rows[1]["seed"] == "52"

    metrics_path = output_dir / "run_01_seed42" / "metrics.json"
    history_path = output_dir / "run_01_seed42" / "history.csv"
    symbolic_summary_path = output_dir / "run_01_seed42" / "symbolnet_symbolic_summary.csv"
    assert metrics_path.exists()
    assert history_path.exists()
    assert symbolic_summary_path.exists()

    metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
    assert metrics["dataset_source"] == "synthetic"
    assert metrics["accuracy"] == 0.75
    assert metrics["samples_train"] == 12
    assert metrics["seed_train_wall_time_s"] == 0.12


def test_run_symbolnet_applies_cnn_boost_stability_params_only_when_enabled(
    monkeypatch,
    tmp_path: Path,
) -> None:
    runner = SymbolNetRunnerConfig(
        output_dir=str(tmp_path / "runs"),
        seeds="42",
        classes="0,1",
        epochs=2,
        batch_size=8,
        learning_rate=0.005,
        unary_ops_csv="sin,cos,exp,gauss",
        alpha_sparsity_input=0.95,
        alpha_sparsity_model=0.99,
        enable_cnn_boost=True,
        quiet=True,
    )
    runner.normalize()

    fake_dataset = {
        "X_train": np.zeros((10, 4), dtype=np.float32),
        "X_test": np.zeros((4, 4), dtype=np.float32),
        "Y_train": np.zeros((10, 2), dtype=np.float32),
        "Y_test": np.zeros((4, 2), dtype=np.float32),
        "source": "synthetic",
        "input_dim": 4,
        "output_dim": 2,
    }
    boosted_dataset = {
        **fake_dataset,
        "input_dim": 3,
        "raw_input_dim": 4,
        "source": "synthetic + cnn_boost",
    }

    monkeypatch.setattr("scripts.symbolnet.load_mnist_data", lambda classes, mt, me: fake_dataset)
    monkeypatch.setattr("scripts.symbolnet._apply_cnn_boost", lambda dataset, **kwargs: boosted_dataset)

    def _fake_train_once(runner_cfg, dataset, seed):
        assert runner_cfg.learning_rate == 0.001
        assert runner_cfg.unary_ops == ["identity", "square", "cube", "softsign"]
        assert runner_cfg.alpha_sparsity_input == 0.85
        assert runner_cfg.alpha_sparsity_model == 0.95
        return {
            "history": {"loss": [1.0, 0.8], "accuracy": [0.6, 0.7]},
            "accuracy": 0.7,
            "macro_auc_ovr": 0.75,
            "class_auc": {0: 0.74, 1: 0.76},
            "train_seconds": 0.1,
            "predict_seconds": 0.01,
            "samples_train": int(dataset["X_train"].shape[0]),
            "samples_test": int(dataset["X_test"].shape[0]),
            "symbolic_model": object(),
            "model_dim": [3, 1, 2],
            "operators": [[["sin"], ["*"]]],
            "num_operators": [[2, 0]],
        }

    monkeypatch.setattr("scripts.symbolnet.train_symbolnet_once", _fake_train_once)
    monkeypatch.setattr(
        "scripts.symbolnet._build_symbolic_summary_rows",
        lambda **kwargs: [
            {"类别": 0, "表达式": "x_0", "复杂度": 1, "AUC": 0.74, "expr_full": "x_0"},
            {"类别": 1, "表达式": "x_1", "复杂度": 1, "AUC": 0.76, "expr_full": "x_1"},
        ],
    )

    run_symbolnet(runner)

    metrics_path = Path(runner.output_dir) / "run_01_seed42" / "metrics.json"
    metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
    assert metrics["enable_cnn_boost"] is True
    assert metrics["learning_rate"] == 0.001
    assert metrics["unary_ops"] == ["identity", "square", "cube", "softsign"]
    assert metrics["alpha_sparsity_input"] == 0.85
    assert metrics["alpha_sparsity_model"] == 0.95
