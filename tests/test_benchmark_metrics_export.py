from __future__ import annotations

import os
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
import torch

from scripts.symkanbenchmark import (
    BenchmarkRunnerConfig,
    _build_experiment_metrics,
    _stable_topk_feature_indices,
    _validated_app_config_update,
    run_single_experiment,
)
from symkan.config import AppConfig


class _DummyKANModel:
    def __init__(self, width, numeric_basis: str = "bspline") -> None:
        self.width = width
        self.numeric_basis = numeric_basis


class _DummyExportResult:
    def __init__(self, model) -> None:
        self.model = model
        self.formulas = None
        self.valid_expressions = []
        self.trace = pd.DataFrame()
        self.sym_stats = {"backend": "baseline", "pipeline_warnings": []}
        self.final_acc = 0.9
        self.final_n_edge = 9
        self.timing = {"pipeline_warnings": [], "symbolic_total_seconds": 0.0}

    def to_legacy_dict(self) -> dict[str, object]:
        return {
            "model": self.model,
            "formulas": self.formulas,
            "valid_expressions": self.valid_expressions,
            "trace": self.trace,
            "sym_stats": self.sym_stats,
            "final_acc": self.final_acc,
            "final_n_edge": self.final_n_edge,
            "effective_target_edges": 8,
            "effective_input_dim": 2,
            "input_n_edge": 11,
            "timing": self.timing,
        }


def test_build_experiment_metrics_surfaces_symbolic_observability(monkeypatch) -> None:
    monkeypatch.setattr("scripts.symkanbenchmark.get_device", lambda: "cpu")
    monkeypatch.setattr("scripts.symkanbenchmark.get_n_edge", lambda model: 17)

    config = AppConfig()
    config.runtime.global_seed = 123
    config.stagewise.target_edges = 40
    config.symbolize.enable_input_compaction = True
    base_model = _DummyKANModel(width=[[784, 0], [16, 0], [10, 0]], numeric_basis="radial_bf")
    enhanced_model = _DummyKANModel(width=[[120, 0], [16, 0], [10, 0]], numeric_basis="radial_bf")

    metrics = _build_experiment_metrics(
        config=config,
        run_dir=Path("outputs/test"),
        run_index=1,
        total_runs=3,
        stage_seed=99,
        batch_size=16,
        base_model=base_model,
        base_acc=0.81,
        keep_idx=[0, 1],
        enhanced_model=enhanced_model,
        enhanced_acc=0.88,
        stage_result={"selected_stage": "stage_2", "selected_score": 0.75},
        symbolize_result={
            "final_acc": 0.9,
            "final_n_edge": 12,
            "effective_target_edges": 8,
            "effective_input_dim": 2,
            "input_n_edge": 120,
            "sym_stats": {"backend": "icbr"},
            "timing": {
                "symbolic_total_seconds": 0.8,
                "symbolic_prep_cache_hit": True,
                "symbolic_prep_total_seconds_ref": 1.2,
                "abort_stage": "prune_round",
                "abort_reason": "attribute exploded",
                "abort_error_type": "RuntimeError",
                "input_compaction_fallback": True,
                "input_compaction_reason": "compaction exploded",
                "input_compaction_error_type": "ValueError",
                "icbr_candidate_generation_wall_time_s": 0.3,
                "icbr_replay_rerank_wall_time_s": 0.1,
                "icbr_replay_rank_inversion_rate": 0.25,
                "pipeline_warnings": [{}, {}],
            },
        },
        valid_exprs=[{"expr": "x0"}],
        expr_complexity_mean=3.5,
        auc_macro=0.92,
        val_df=None,
        final_teacher_imitation_mse=0.02,
        final_target_mse=0.03,
        final_target_r2=0.91,
        formula_export_success=True,
        stage_total_seconds=10.0,
        stage_train_total_seconds=6.0,
        stage_prune_total_seconds=3.0,
        stage_final_finetune_seconds=1.0,
        symbolize_wall_time=2.5,
        post_symbolic_eval_wall_time=1.25,
        run_total_wall_time=14.0,
    )

    assert metrics["device"] == "cpu"
    assert metrics["numeric_basis"] == "radial_bf"
    assert metrics["kan_width"] == [784, 16, 10]
    assert metrics["enhanced_kan_width"] == [120, 16, 10]
    assert metrics["numeric_cache_hit"] is False
    assert metrics["symbolic_backend"] == "icbr"
    assert metrics["symbolic_prep_cache_hit"] is True
    assert metrics["cached_symbolic_prep_seconds_ref"] == pytest.approx(1.2)
    assert metrics["pre_symbolic_too_dense"] is True
    assert metrics["final_teacher_imitation_mse"] == pytest.approx(0.02)
    assert metrics["final_target_mse"] == pytest.approx(0.03)
    assert metrics["final_target_r2"] == pytest.approx(0.91)
    assert metrics["formula_export_success"] is True
    assert metrics["symbolic_abort_stage"] == "prune_round"
    assert metrics["symbolic_abort_reason"] == "attribute exploded"
    assert metrics["symbolic_abort_error_type"] == "RuntimeError"
    assert metrics["symbolic_warning_count"] == 2
    assert metrics["symbolic_total_seconds"] == 0.8
    assert metrics["symbolize_wall_time_s"] == 2.5
    assert metrics["symbolic_non_core_seconds"] == 1.7
    assert metrics["symbolic_non_core_valid"] is True
    assert metrics["icbr_candidate_generation_wall_time_s"] == pytest.approx(0.3)
    assert metrics["icbr_replay_rerank_wall_time_s"] == pytest.approx(0.1)
    assert metrics["icbr_replay_rank_inversion_rate"] == pytest.approx(0.25)
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
    base_model = _DummyKANModel(width=[[784, 0], [16, 0], [10, 0]], numeric_basis="bspline")
    enhanced_model = _DummyKANModel(width=[[120, 0], [16, 0], [10, 0]], numeric_basis="bspline")
    metrics = _build_experiment_metrics(
        config=config,
        run_dir=Path("outputs/test"),
        run_index=1,
        total_runs=1,
        stage_seed=42,
        batch_size=16,
        base_model=base_model,
        base_acc=0.8,
        keep_idx=[0],
        enhanced_model=enhanced_model,
        enhanced_acc=0.8,
        stage_result={"selected_stage": "stage_1", "selected_score": 0.8},
        symbolize_result={
            "final_acc": 0.8,
            "final_n_edge": 10,
            "sym_stats": {"backend": "baseline"},
            "timing": {"symbolic_total_seconds": 3.0},
        },
        valid_exprs=[],
        expr_complexity_mean=0.0,
        auc_macro=0.9,
        val_df=None,
        final_teacher_imitation_mse=0.04,
        final_target_mse=0.05,
        final_target_r2=0.8,
        formula_export_success=False,
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
    assert metrics["numeric_basis"] == "bspline"
    assert metrics["kan_width"] == [784, 16, 10]
    assert metrics["enhanced_kan_width"] == [120, 16, 10]


def test_stable_topk_feature_indices_preserves_tie_order() -> None:
    feature_score = np.array([0.9, 0.4, 0.4, 0.4], dtype=np.float32)
    keep_idx = _stable_topk_feature_indices(feature_score, top_k=3)

    assert keep_idx.tolist() == [0, 1, 2]


def test_run_single_experiment_reseeds_numeric_phases(monkeypatch: pytest.MonkeyPatch) -> None:
    import scripts.symkanbenchmark as benchmark

    seed_calls: list[int] = []
    numeric_fit_calls = {"baseline": 0, "stagewise": 0}
    symbolic_prep_calls = {"prepare": 0, "finish": 0}

    class _KAN:
        def __init__(self, *, width, numeric_basis: str, seed: int, **kwargs) -> None:
            self.width = width
            self.numeric_basis = numeric_basis
            self.seed = seed
            self.n_edge = 13 if width[0] == 4 else 11
            self._state = {"weight": torch.tensor([float(seed)], dtype=torch.float32)}

        def state_dict(self) -> dict[str, torch.Tensor]:
            return {key: value.clone() for key, value in self._state.items()}

        def load_state_dict(self, state_dict: dict[str, torch.Tensor]) -> None:
            self._state = {key: value.clone() for key, value in state_dict.items()}

    monkeypatch.setattr(benchmark, "_ensure_runtime_deps", lambda: None)
    monkeypatch.setattr(benchmark, "np", np)
    monkeypatch.setattr(benchmark, "pd", pd)
    monkeypatch.setattr(benchmark, "torch", torch)
    monkeypatch.setattr(benchmark, "KAN", _KAN)
    monkeypatch.setattr(benchmark, "resolve_device", lambda device: "cpu")
    monkeypatch.setattr(benchmark, "set_device", lambda device: None)
    monkeypatch.setattr(benchmark, "get_device", lambda: "cpu")
    monkeypatch.setattr(benchmark, "default_batch_size", lambda: 4)
    monkeypatch.setattr(benchmark, "set_global_seed", lambda seed: seed_calls.append(int(seed)))
    monkeypatch.setattr(
        benchmark,
        "load_data",
        lambda config, repo_root: {
            "X_train": np.arange(16, dtype=np.float32).reshape(4, 4),
            "Y_train": np.eye(2, dtype=np.float32)[np.array([0, 1, 0, 1])],
            "X_test": np.arange(8, dtype=np.float32).reshape(2, 4),
            "Y_test": np.eye(2, dtype=np.float32)[np.array([0, 1])],
            "y_test": np.array([0, 1], dtype=np.int64),
            "input_dim": 4,
            "n_classes": 2,
        },
    )
    monkeypatch.setattr(
        benchmark,
        "build_dataset",
        lambda x_train, y_train, x_test, y_test: {
            "train_input": torch.as_tensor(x_train, dtype=torch.float32),
            "train_label": torch.as_tensor(y_train, dtype=torch.float32),
            "test_input": torch.as_tensor(x_test, dtype=torch.float32),
            "test_label": torch.as_tensor(y_test, dtype=torch.float32),
        },
    )
    monkeypatch.setattr(
        benchmark,
        "safe_fit",
        lambda *args, **kwargs: numeric_fit_calls.__setitem__("baseline", numeric_fit_calls["baseline"] + 1)
        or {"train_loss": [], "test_loss": []},
    )
    monkeypatch.setattr(benchmark, "model_acc", lambda *args, **kwargs: 0.75)
    monkeypatch.setattr(benchmark, "model_acc_ds", lambda *args, **kwargs: 0.8)
    monkeypatch.setattr(benchmark, "safe_attribute", lambda *args, **kwargs: np.array([0.9, 0.4, 0.4, 0.4]))
    monkeypatch.setattr(
        benchmark,
        "stagewise_train_report",
        lambda dataset, app_config: numeric_fit_calls.__setitem__("stagewise", numeric_fit_calls["stagewise"] + 1)
        or (
            _KAN(width=[dataset["train_input"].shape[1], 16, 2], numeric_basis="bspline", seed=app_config.stagewise.seed),
            {
                "selected_stage": "final",
                "selected_score": 0.8,
                "stage_logs": [],
                "stage_total_seconds": 1.0,
                "stage_train_total_seconds": 0.6,
                "stage_prune_total_seconds": 0.2,
                "final_finetune_seconds": 0.2,
            },
        ),
    )
    monkeypatch.setattr(benchmark, "save_stage_logs", lambda *args, **kwargs: None)
    monkeypatch.setattr(benchmark, "save_symbolic_summary", lambda *args, **kwargs: None)
    monkeypatch.setattr(benchmark, "save_export_bundle", lambda *args, **kwargs: None)
    monkeypatch.setattr(benchmark, "validate_formula_numerically", lambda *args, **kwargs: None)
    monkeypatch.setattr(benchmark, "model_logits", lambda model, x: np.zeros((x.shape[0], 2), dtype=np.float32))
    monkeypatch.setattr(benchmark, "scipy_softmax", lambda logits, axis=1: np.full_like(logits, 0.5))
    monkeypatch.setattr(
        benchmark,
        "compute_multiclass_roc_auc",
        lambda labels, prob: {0: {"auc": 0.9}, 1: {"auc": 0.8}},
    )
    monkeypatch.setattr(
        benchmark,
        "build_formula_summary",
        lambda *args, **kwargs: pd.DataFrame({"expr_full": [], "复杂度": []}),
    )
    
    def fake_prepare_symbolic_bundle(model, dataset, config):
        symbolic_prep_calls["prepare"] += 1
        return {
            "prepared_model": model,
            "prepared_dataset": dataset,
            "trace": pd.DataFrame([{"edges_before": 11, "edges_after": 10, "drop_ratio": 1 / 11}]),
            "timing": {"pipeline_warnings": [], "symbolic_total_seconds": 0.0, "symbolic_prep_total_seconds": 0.25},
            "effective_target_edges": 8,
            "input_n_edge": 11,
            "effective_input_indices": [0, 1, 2],
            "effective_input_dim": 3,
            "original_input_id": None,
        }

    def fake_symbolize_pipeline_from_prepared_report(prepared_bundle, dataset, config):
        symbolic_prep_calls["finish"] += 1
        result = _DummyExportResult(prepared_bundle["prepared_model"])
        result.trace = prepared_bundle["trace"]
        result.timing = {
            **prepared_bundle["timing"],
            "pipeline_warnings": [],
            "symbolic_total_seconds": 0.0,
        }
        result.sym_stats = {"backend": str(config.symbolize.symbolic_backend), "pipeline_warnings": []}
        return result

    monkeypatch.setattr(benchmark, "prepare_symbolic_bundle", fake_prepare_symbolic_bundle)
    monkeypatch.setattr(
        benchmark,
        "symbolize_pipeline_from_prepared_report",
        fake_symbolize_pipeline_from_prepared_report,
    )

    config = AppConfig()
    config.runtime.global_seed = 101
    config.runtime.baseline_seed = 202
    config.runtime.quiet = True
    config.model.top_k = 3
    output_root = Path("outputs/test_tmp") / f"test_run_single_experiment_reseeds_numeric_phases_{os.getpid()}"
    runner = BenchmarkRunnerConfig(
        config_path=None,
        tasks="full",
        output_dir=str(output_root / "baseline"),
        stagewise_seeds="42",
        save_bundle=False,
        quiet=True,
        verbose=False,
        bench_repeat=1,
        bench_warmup=0,
        eval_rounds=1,
        parallel_modes="off",
        parallel_target_min=40,
        parallel_target_max=80,
        parallel_max_prune_rounds=8,
        parallel_finetune_steps=20,
        parallel_layerwise_finetune_steps=20,
        parallel_affine_finetune_steps=0,
        parallel_prune_eval_interval=2,
        parallel_prune_attr_sample_adaptive=True,
        parallel_prune_attr_sample_min=512,
        parallel_prune_attr_sample_max=1536,
        parallel_heavy_ft_patience=1,
        parallel_heavy_ft_min_delta=5e-4,
    )

    result = run_single_experiment(config, runner, Path.cwd(), run_index=1, total_runs=1, stage_seed=42)

    assert seed_calls == [101, 202, 42, 42]
    assert numeric_fit_calls == {"baseline": 1, "stagewise": 1}
    assert symbolic_prep_calls == {"prepare": 1, "finish": 1}
    assert result["metrics"]["selected_input_dim"] == 3
    assert result["metrics"]["pre_symbolic_n_edge"] == 11
    assert result["metrics"]["symbolic_prep_cache_hit"] is False
    assert result["metrics"]["cached_symbolic_prep_seconds_ref"] == pytest.approx(0.25)

    seed_calls.clear()
    config_icbr = config.model_copy(deep=True)
    config_icbr.symbolize.symbolic_backend = "icbr"
    runner_icbr = BenchmarkRunnerConfig(**{**runner.__dict__, "output_dir": str(output_root / "baseline_icbr")})
    result_icbr = run_single_experiment(config_icbr, runner_icbr, Path.cwd(), run_index=1, total_runs=1, stage_seed=42)

    assert seed_calls == [101]
    assert numeric_fit_calls == {"baseline": 1, "stagewise": 1}
    assert symbolic_prep_calls == {"prepare": 1, "finish": 2}
    assert result_icbr["metrics"]["base_acc"] == result["metrics"]["base_acc"]
    assert result_icbr["metrics"]["enhanced_acc"] == result["metrics"]["enhanced_acc"]
    assert result_icbr["metrics"]["pre_symbolic_n_edge"] == result["metrics"]["pre_symbolic_n_edge"]
    assert result_icbr["metrics"]["numeric_cache_hit"] is True
    assert result_icbr["metrics"]["cached_stage_total_seconds_ref"] == pytest.approx(1.0)
    assert result_icbr["metrics"]["symbolic_prep_cache_hit"] is True
    assert result_icbr["metrics"]["cached_symbolic_prep_seconds_ref"] == pytest.approx(0.25)


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
