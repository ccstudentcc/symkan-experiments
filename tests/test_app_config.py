from __future__ import annotations

from pathlib import Path

import pytest

from scripts.symkanbenchmark import BenchmarkRunnerConfig, load_benchmark_app_config, parse_benchmark_cli_config
from symkan.config import AppConfig, ConfigError, StagewiseConfig, SymbolizeConfig, load_config, validate_app_config
from symkan.core.types import StagewiseConfig as CoreStagewiseConfig
from symkan.core.types import SymbolizeConfig as CoreSymbolizeConfig


FIXTURE_DIR = Path(__file__).resolve().parent / "fixtures"


def make_runner(**overrides: object) -> BenchmarkRunnerConfig:
    values = {
        "config_path": None,
        "tasks": "full",
        "output_dir": "outputs/test",
        "stagewise_seeds": "42",
        "save_bundle": False,
        "quiet": False,
        "verbose": False,
        "bench_repeat": 1,
        "bench_warmup": 0,
        "eval_rounds": 1,
        "parallel_modes": "off",
        "parallel_target_min": 40,
        "parallel_target_max": 80,
        "parallel_max_prune_rounds": 8,
        "parallel_finetune_steps": 20,
        "parallel_layerwise_finetune_steps": 20,
        "parallel_affine_finetune_steps": 0,
        "parallel_prune_eval_interval": 2,
        "parallel_prune_attr_sample_adaptive": True,
        "parallel_prune_attr_sample_min": 512,
        "parallel_prune_attr_sample_max": 1536,
        "parallel_heavy_ft_patience": 1,
        "parallel_heavy_ft_min_delta": 5e-4,
    }
    values.update(overrides)
    return BenchmarkRunnerConfig(**values)


def test_validate_app_config_nested_sections() -> None:
    config = validate_app_config(
        {
            "runtime": {
                "device": "cpu",
                "global_seed": 7,
            },
            "stagewise": {
                "width": [12, 16, 3],
                "steps_per_stage": 80,
            },
            "symbolize": {
                "target_edges": 48,
                "layerwise_finetune_steps": 0,
            },
        }
    )

    assert isinstance(config, AppConfig)
    assert config.runtime.device == "cpu"
    assert config.runtime.global_seed == 7
    assert config.stagewise.width == [12, 16, 3]
    assert config.stagewise.steps_per_stage == 80
    assert config.symbolize.target_edges == 48
    assert config.symbolize.layerwise_finetune_steps == 0


def test_core_types_reexport_runtime_config_models() -> None:
    assert CoreStagewiseConfig is StagewiseConfig
    assert CoreSymbolizeConfig is SymbolizeConfig


def test_load_config_expands_env_default_and_nested_override(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("SYMKAN_DEVICE", raising=False)
    config_path = FIXTURE_DIR / "app_config_env.yaml"

    config = load_config(config_path)

    assert config.runtime.device == "cpu"
    assert config.stagewise.steps_per_stage == 88
    assert config.symbolize.target_edges == 47


def test_load_config_rejects_missing_env_var(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("SYMKAN_REQUIRED", raising=False)
    config_path = FIXTURE_DIR / "app_config_missing_env.yaml"

    with pytest.raises(ConfigError, match="SYMKAN_REQUIRED"):
        load_config(config_path)


def test_load_config_rejects_invalid_nested_field() -> None:
    config_path = FIXTURE_DIR / "app_config_invalid_nested.yaml"

    with pytest.raises(ConfigError, match="stagewise.unknown_field"):
        load_config(config_path)


@pytest.mark.parametrize(
    ("payload", "error_match"),
    [
        ({"stagewise": {"validation_ratio": 1.0}}, "stagewise.validation_ratio"),
        ({"symbolize": {"layerwise_validation_ratio": -0.1}}, "symbolize.layerwise_validation_ratio"),
        ({"stagewise": {"prune_acc_drop_tol": -0.01}}, "stagewise.prune_acc_drop_tol"),
        ({"stagewise": {"prune_acc_drop_tol": 1.5}}, "stagewise.prune_acc_drop_tol"),
        ({"data": {"mnist_classes": []}}, "mnist_classes"),
        ({"evaluation": {"validate_n_sample": 0}}, "evaluation.validate_n_sample"),
    ],
)
def test_validate_app_config_rejects_invalid_boundary_values(
    payload: dict[str, object],
    error_match: str,
) -> None:
    with pytest.raises(ConfigError, match=error_match):
        validate_app_config(payload)


def test_template_yaml_loads() -> None:
    template_path = Path("symkan/config/template.yaml")
    config = load_config(template_path)

    assert isinstance(config, AppConfig)
    assert config.library.lib_preset == "layered"


def test_benchmark_cli_overrides_are_applied_to_nested_app_config() -> None:
    config_path = FIXTURE_DIR / "app_config_benchmark_override.yaml"
    runner = make_runner(
        config_path=str(config_path),
        verbose=True,
        device="cpu",
        global_seed=321,
        max_prune_rounds=12,
        layerwise_finetune_steps=5,
        layerwise_finetune_lamb=2e-5,
        layerwise_use_validation=False,
        layerwise_validation_ratio=0.2,
        layerwise_validation_seed=999,
        layerwise_early_stop_patience=4,
        layerwise_early_stop_min_delta=5e-4,
        layerwise_eval_interval=10,
        layerwise_validation_n_sample=128,
        input_compaction=False,
    )

    config = load_benchmark_app_config(str(config_path), runner)

    assert config.runtime.device == "cpu"
    assert config.runtime.global_seed == 321
    assert config.symbolize.max_prune_rounds == 12
    assert config.symbolize.layerwise_finetune_steps == 5
    assert config.symbolize.layerwise_finetune_lamb == pytest.approx(2e-5)
    assert config.symbolize.layerwise_use_validation is False
    assert config.symbolize.layerwise_validation_ratio == pytest.approx(0.2)
    assert config.symbolize.layerwise_validation_seed == 999
    assert config.symbolize.layerwise_early_stop_patience == 4
    assert config.symbolize.layerwise_early_stop_min_delta == pytest.approx(5e-4)
    assert config.symbolize.layerwise_eval_interval == 10
    assert config.symbolize.layerwise_validation_n_sample == 128
    assert config.symbolize.enable_input_compaction is False


def test_benchmark_cli_overrides_are_revalidated() -> None:
    runner = make_runner(layerwise_validation_ratio=1.0)

    with pytest.raises(ConfigError, match="layerwise_validation_ratio"):
        load_benchmark_app_config(None, runner)


def test_benchmark_without_config_uses_checked_in_runner_defaults() -> None:
    config = load_benchmark_app_config(None, make_runner())

    assert config.stagewise.steps_per_stage == 60
    assert config.stagewise.prune_start_stage == 3
    assert config.stagewise.target_edges == 120
    assert config.stagewise.guard_mode == "light"
    assert config.symbolize.target_edges == 90


def test_benchmark_parser_accepts_layerwise_cli_overrides() -> None:
    runner = parse_benchmark_cli_config(
        [
            "--layerwise-finetune-lamb",
            "2e-5",
            "--layerwise-use-validation",
            "--layerwise-validation-ratio",
            "0.2",
            "--layerwise-validation-seed",
            "999",
            "--layerwise-early-stop-patience",
            "4",
            "--layerwise-early-stop-min-delta",
            "5e-4",
            "--layerwise-eval-interval",
            "10",
            "--layerwise-validation-n-sample",
            "128",
        ]
    )

    assert runner.layerwise_finetune_lamb == pytest.approx(2e-5)
    assert runner.layerwise_use_validation is True
    assert runner.layerwise_validation_ratio == pytest.approx(0.2)
    assert runner.layerwise_validation_seed == 999
    assert runner.layerwise_early_stop_patience == 4
    assert runner.layerwise_early_stop_min_delta == pytest.approx(5e-4)
    assert runner.layerwise_eval_interval == 10
    assert runner.layerwise_validation_n_sample == 128


def test_benchmark_parser_accepts_stage_guard_mode_override() -> None:
    runner = parse_benchmark_cli_config(["--stage-guard-mode", "full"])
    assert runner.stage_guard_mode == "full"
