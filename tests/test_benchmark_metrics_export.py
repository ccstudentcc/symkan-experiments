from __future__ import annotations

from pathlib import Path

import pytest

from scripts.symkanbenchmark import (
    _build_experiment_metrics,
    _validated_app_config_update,
)
from symkan.config import AppConfig


def test_build_experiment_metrics_surfaces_symbolic_observability(monkeypatch) -> None:
    monkeypatch.setattr("scripts.symkanbenchmark.get_device", lambda: "cpu")
    monkeypatch.setattr("scripts.symkanbenchmark.get_n_edge", lambda model: 17)

    config = AppConfig()
    config.runtime.global_seed = 123
    config.stagewise.target_edges = 40
    config.symbolize.enable_input_compaction = True

    metrics = _build_experiment_metrics(
        config=config,
        run_dir=Path("outputs/test"),
        run_index=1,
        total_runs=3,
        stage_seed=99,
        batch_size=16,
        base_model=object(),
        base_acc=0.81,
        keep_idx=[0, 1],
        enhanced_model=object(),
        enhanced_acc=0.88,
        stage_result={"selected_stage": "stage_2", "selected_score": 0.75},
        symbolize_result={
            "final_acc": 0.9,
            "final_n_edge": 12,
            "effective_target_edges": 8,
            "effective_input_dim": 2,
            "input_n_edge": 120,
            "timing": {
                "symbolic_total_seconds": 0.8,
                "abort_stage": "prune_round",
                "abort_reason": "attribute exploded",
                "abort_error_type": "RuntimeError",
                "input_compaction_fallback": True,
                "input_compaction_reason": "compaction exploded",
                "input_compaction_error_type": "ValueError",
                "pipeline_warnings": [{}, {}],
            },
        },
        valid_exprs=[{"expr": "x0"}],
        expr_complexity_mean=3.5,
        auc_macro=0.92,
        val_df=None,
        stage_total_seconds=10.0,
        stage_train_total_seconds=6.0,
        stage_prune_total_seconds=3.0,
        stage_final_finetune_seconds=1.0,
        symbolize_wall_time=2.5,
        post_symbolic_eval_wall_time=1.25,
        run_total_wall_time=14.0,
    )

    assert metrics["device"] == "cpu"
    assert metrics["pre_symbolic_too_dense"] is True
    assert metrics["symbolic_abort_stage"] == "prune_round"
    assert metrics["symbolic_abort_reason"] == "attribute exploded"
    assert metrics["symbolic_abort_error_type"] == "RuntimeError"
    assert metrics["symbolic_warning_count"] == 2
    assert metrics["symbolic_total_seconds"] == 0.8
    assert metrics["symbolize_wall_time_s"] == 2.5
    assert metrics["symbolic_non_core_seconds"] == 1.7
    assert metrics["symbolic_non_core_valid"] is True
    assert metrics["export_wall_time_s"] == metrics["symbolize_wall_time_s"]
    assert metrics["post_symbolic_eval_wall_time_s"] == 1.25
    assert metrics["run_total_wall_time_s"] == 14.0
    assert metrics["input_compaction_enabled"] is True
    assert metrics["input_compaction_fallback"] is True
    assert metrics["input_compaction_reason"] == "compaction exploded"
    assert metrics["input_compaction_error_type"] == "ValueError"


def test_build_experiment_metrics_marks_invalid_non_core_seconds(monkeypatch) -> None:
    monkeypatch.setattr("scripts.symkanbenchmark.get_device", lambda: "cpu")
    monkeypatch.setattr("scripts.symkanbenchmark.get_n_edge", lambda model: 17)

    config = AppConfig()
    metrics = _build_experiment_metrics(
        config=config,
        run_dir=Path("outputs/test"),
        run_index=1,
        total_runs=1,
        stage_seed=42,
        batch_size=16,
        base_model=object(),
        base_acc=0.8,
        keep_idx=[0],
        enhanced_model=object(),
        enhanced_acc=0.8,
        stage_result={"selected_stage": "stage_1", "selected_score": 0.8},
        symbolize_result={"final_acc": 0.8, "final_n_edge": 10, "timing": {"symbolic_total_seconds": 3.0}},
        valid_exprs=[],
        expr_complexity_mean=0.0,
        auc_macro=0.9,
        val_df=None,
        stage_total_seconds=1.0,
        stage_train_total_seconds=1.0,
        stage_prune_total_seconds=0.0,
        stage_final_finetune_seconds=0.0,
        symbolize_wall_time=2.5,
        post_symbolic_eval_wall_time=0.1,
        run_total_wall_time=3.0,
    )

    assert metrics["symbolic_non_core_valid"] is False
    assert metrics["symbolic_non_core_seconds"] != metrics["symbolic_non_core_seconds"]


def test_validated_app_config_update_normalizes_pair_like_width() -> None:
    config = AppConfig()
    polluted = config.model_copy(deep=True)
    polluted.stagewise = polluted.stagewise.model_construct(
        **{
            **polluted.stagewise.model_dump(mode="python"),
            "width": [[120, 0], [16, 0], [10, 0]],
        }
    )

    with pytest.warns(UserWarning, match="normalized pair-like stagewise.width"):
        updated = _validated_app_config_update(polluted, symbolize={"target_edges": 80})

    assert updated.stagewise.width == [120, 16, 10]
    assert updated.symbolize.target_edges == 80
