from __future__ import annotations

import argparse
from pathlib import Path

import pytest

from symkan.config import BenchmarkConfigError, apply_config_defaults, load_benchmark_config
from symkan.config.loader import PYDANTIC_AVAILABLE

FIXTURE_DIR = Path(__file__).resolve().parent / "fixtures"


def test_load_benchmark_config_defaults_without_file() -> None:
    config = load_benchmark_config(None)
    assert config["output_dir"] == "outputs/benchmark_runs"
    assert config["mnist_classes"] == list(range(10))
    assert config["affine_lr_schedule"] == [0.003, 0.001, 0.0005, 0.0002]


def test_load_benchmark_config_expands_env_vars(monkeypatch) -> None:
    if not PYDANTIC_AVAILABLE:
        pytest.skip("pydantic is not installed in this environment")
    monkeypatch.setenv("SYMKAN_OUTPUT_DIR", "outputs/custom_runs")

    config = load_benchmark_config(FIXTURE_DIR / "config_env.yaml")

    assert config["output_dir"] == "outputs/custom_runs"
    assert config["stagewise_seeds"] == "42,52,62"


def test_load_benchmark_config_rejects_unknown_fields() -> None:
    with pytest.raises(BenchmarkConfigError):
        load_benchmark_config(FIXTURE_DIR / "config_unknown.yaml")


def test_apply_config_defaults_keeps_cli_override() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default="outputs/benchmark_runs")
    parser.add_argument("--quiet", action="store_true")

    apply_config_defaults(
        parser,
        {
            "output_dir": "outputs/from_yaml",
            "quiet": True,
        },
    )

    args = parser.parse_args(["--output-dir", "outputs/from_cli"])

    assert args.output_dir == "outputs/from_cli"
    assert args.quiet is True
