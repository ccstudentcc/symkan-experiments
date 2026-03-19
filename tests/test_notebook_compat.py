from __future__ import annotations

from typing import Any

import pytest

from symkan.config import ConfigError, build_stagewise_notebook_config, build_symbolize_notebook_config
from symkan import notebook_compat


def test_build_stagewise_notebook_config_maps_canonical_kwargs() -> None:
    config = build_stagewise_notebook_config(
        width=[120, 16, 10],
        grid=7,
        k=4,
        seed=42,
        steps_per_stage=60,
        batch_size=64,
        target_edges=120,
        prune_acc_drop_tol=0.04,
        sym_target_edges=50,
        acc_weight=0.5,
        verbose=True,
        runtime_device="cpu",
        runtime_global_seed=321,
    )

    assert config.runtime.device == "cpu"
    assert config.runtime.global_seed == 321
    assert config.runtime.batch_size == 64
    assert config.model.inner_dim == 16
    assert config.model.grid == 7
    assert config.model.k == 4
    assert config.stagewise.width == [120, 16, 10]
    assert config.stagewise.seed == 42
    assert config.stagewise.steps_per_stage == 60
    assert config.stagewise.batch_size == 64
    assert config.stagewise.target_edges == 120
    assert config.stagewise.prune_acc_drop_tol == pytest.approx(0.04)
    assert config.stagewise.sym_target_edges == 50
    assert config.stagewise.acc_weight == pytest.approx(0.5)


def test_build_symbolize_notebook_config_maps_canonical_kwargs() -> None:
    config = build_symbolize_notebook_config(
        target_edges=90,
        max_prune_rounds=30,
        lib_hidden=["x", "x^2", "tanh"],
        lib_output=["x", "x^2"],
        weight_simple=0.1,
        finetune_steps=50,
        finetune_lr=5e-4,
        layerwise_finetune_steps=0,
        affine_finetune_steps=200,
        affine_finetune_lr_schedule=[0.003, 0.001, 0.0005, 0.0002],
        parallel_mode="auto",
        parallel_workers=None,
        parallel_min_tasks=16,
        prune_eval_interval=2,
        prune_attr_sample_adaptive=True,
        prune_attr_sample_min=768,
        prune_attr_sample_max=2048,
        heavy_ft_early_stop_patience=2,
        heavy_ft_early_stop_min_delta=5e-4,
        collect_timing=True,
        batch_size=64,
        verbose=True,
        runtime_device="cpu",
        runtime_global_seed=999,
        evaluation_validate_n_sample=500,
    )

    assert config.runtime.device == "cpu"
    assert config.runtime.global_seed == 999
    assert config.runtime.batch_size == 64
    assert config.evaluation.validate_n_sample == 500
    assert config.symbolize.target_edges == 90
    assert config.symbolize.max_prune_rounds == 30
    assert config.symbolize.lib_hidden == ["x", "x^2", "tanh"]
    assert config.symbolize.lib_output == ["x", "x^2"]
    assert config.symbolize.weight_simple == pytest.approx(0.1)
    assert config.symbolize.finetune_steps == 50
    assert config.symbolize.finetune_lr == pytest.approx(5e-4)
    assert config.symbolize.layerwise_finetune_steps == 0
    assert config.symbolize.affine_finetune_steps == 200
    assert config.symbolize.affine_finetune_lr_schedule == [0.003, 0.001, 0.0005, 0.0002]
    assert config.symbolize.parallel_mode == "auto"
    assert config.symbolize.parallel_workers is None
    assert config.symbolize.parallel_min_tasks == 16
    assert config.symbolize.prune_eval_interval == 2
    assert config.symbolize.prune_attr_sample_adaptive is True
    assert config.symbolize.prune_attr_sample_min == 768
    assert config.symbolize.prune_attr_sample_max == 2048
    assert config.symbolize.heavy_ft_early_stop_patience == 2
    assert config.symbolize.heavy_ft_early_stop_min_delta == pytest.approx(5e-4)
    assert config.symbolize.collect_timing is True
    assert config.symbolize.batch_size == 64


def test_build_stagewise_notebook_config_accepts_legacy_aliases_as_fallback() -> None:
    with pytest.warns(UserWarning, match="prefer symkan canonical names"):
        config = build_stagewise_notebook_config(
            width=[64, 16, 10],
            batch=32,
            device="cpu",
            global_seed=777,
            stage_guard_mode="full",
            topk_models=3,
            validation_min=12,
            early_stop_patience=4,
            early_stop_min_acc_gain=1e-3,
            early_stop_edge_buffer=2,
        )

    assert config.runtime.device == "cpu"
    assert config.runtime.global_seed == 777
    assert config.runtime.batch_size == 32
    assert config.stagewise.batch_size == 32
    assert config.stagewise.guard_mode == "full"
    assert config.stagewise.keep_topk_models == 3
    assert config.stagewise.validation_min_samples == 12
    assert config.stagewise.stage_early_stop_patience == 4
    assert config.stagewise.stage_early_stop_min_acc_gain == pytest.approx(1e-3)
    assert config.stagewise.stage_early_stop_edge_buffer == 2


def test_build_symbolize_notebook_config_accepts_legacy_aliases_as_fallback() -> None:
    with pytest.warns(UserWarning, match="prefer symkan canonical names"):
        config = build_symbolize_notebook_config(
            batch=32,
            device="cpu",
            global_seed=555,
            input_compaction=False,
            use_validation=False,
            validation_ratio=0.2,
            validation_seed=99,
            early_stop_patience=5,
            early_stop_min_delta=5e-4,
            eval_interval=7,
            validation_n_sample=128,
            attr_sample_adaptive=True,
            attr_sample_min=400,
            attr_sample_max=1200,
            heavy_ft_patience=2,
            heavy_ft_min_delta=1e-4,
        )

    assert config.runtime.device == "cpu"
    assert config.runtime.global_seed == 555
    assert config.runtime.batch_size == 32
    assert config.symbolize.batch_size == 32
    assert config.symbolize.enable_input_compaction is False
    assert config.symbolize.layerwise_use_validation is False
    assert config.symbolize.layerwise_validation_ratio == pytest.approx(0.2)
    assert config.symbolize.layerwise_validation_seed == 99
    assert config.symbolize.layerwise_early_stop_patience == 5
    assert config.symbolize.layerwise_early_stop_min_delta == pytest.approx(5e-4)
    assert config.symbolize.layerwise_eval_interval == 7
    assert config.symbolize.layerwise_validation_n_sample == 128
    assert config.symbolize.prune_attr_sample_adaptive is True
    assert config.symbolize.prune_attr_sample_min == 400
    assert config.symbolize.prune_attr_sample_max == 1200
    assert config.symbolize.heavy_ft_early_stop_patience == 2
    assert config.symbolize.heavy_ft_early_stop_min_delta == pytest.approx(1e-4)


def test_build_stagewise_notebook_config_rejects_unknown_legacy_kwargs() -> None:
    with pytest.raises(ConfigError, match="unknown stagewise notebook kwargs"):
        build_stagewise_notebook_config(width=[32, 16, 10], mystery_knob=1)


def test_build_symbolize_notebook_config_rejects_conflicting_aliases() -> None:
    with pytest.raises(ConfigError, match="conflicting symbolize notebook kwargs"):
        build_symbolize_notebook_config(batch_size=64, batch=32)


def test_stagewise_train_from_notebook_forwards_app_config(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: dict[str, Any] = {}

    def fake_stagewise(dataset: dict[str, Any], config: Any):
        captured["dataset"] = dataset
        captured["config"] = config
        return "model", {"ok": True}

    monkeypatch.setattr(notebook_compat, "_stagewise_train_impl", fake_stagewise)

    dataset = {"train_input": object()}
    model, result = notebook_compat.stagewise_train_from_notebook(
        dataset,
        width=[32, 16, 10],
        seed=7,
        target_edges=80,
    )

    assert model == "model"
    assert result == {"ok": True}
    assert captured["dataset"] is dataset
    assert captured["config"].stagewise.width == [32, 16, 10]
    assert captured["config"].stagewise.seed == 7
    assert captured["config"].stagewise.target_edges == 80


def test_symbolize_pipeline_from_notebook_forwards_app_config(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: dict[str, Any] = {}

    def fake_symbolize(model: Any, dataset: dict[str, Any], config: Any):
        captured["model"] = model
        captured["dataset"] = dataset
        captured["config"] = config
        return {"ok": True}

    monkeypatch.setattr(notebook_compat, "_symbolize_pipeline_impl", fake_symbolize)

    model = object()
    dataset = {"train_input": object()}
    result = notebook_compat.symbolize_pipeline_from_notebook(
        model,
        dataset,
        target_edges=70,
        parallel_mode="thread",
        parallel_workers=4,
    )

    assert result == {"ok": True}
    assert captured["model"] is model
    assert captured["dataset"] is dataset
    assert captured["config"].symbolize.target_edges == 70
    assert captured["config"].symbolize.parallel_mode == "thread"
    assert captured["config"].symbolize.parallel_workers == 4
