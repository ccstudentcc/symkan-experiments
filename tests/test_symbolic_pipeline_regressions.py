from __future__ import annotations

import copy

import numpy as np
import pytest
import torch

from symkan.config import AppConfig
from symkan.pruning.attribution import safe_attribute
from symkan.symbolic import pipeline as symbolic_pipeline
from symkan.symbolic.compact import select_dataset_inputs
from symkan.symbolic.search import _build_layerwise_ft_datasets, layerwise_symbolic


class MissingFeatureScoreModel(torch.nn.Module):
    def __init__(self, input_dim: int) -> None:
        super().__init__()
        self.anchor = torch.nn.Parameter(torch.zeros(1))
        self.width_in = [input_dim]
        self.feature_score = None

    def forward(self, x: torch.Tensor, singularity_avoiding: bool = True) -> torch.Tensor:
        return x

    def attribute(self, plot: bool = False) -> None:
        return None


class _MaskHolder:
    def __init__(self, mask: torch.Tensor) -> None:
        self.mask = mask


class _SymbolicMaskHolder(_MaskHolder):
    def __init__(self, mask: torch.Tensor, funs_name: list[list[str]]) -> None:
        super().__init__(mask)
        self.funs_name = funs_name


class FailingSuggestModel:
    def __init__(self) -> None:
        self.width_in = [1]
        self.width_out = [1, 1]
        self.act_fun = [_MaskHolder(torch.tensor([[1]], dtype=torch.int64))]
        self.symbolic_fun = [_MaskHolder(torch.tensor([[0]], dtype=torch.int64))]

    def eval(self):
        return self

    def __call__(self, x: torch.Tensor) -> torch.Tensor:
        return x

    def suggest_symbolic(self, l, i, j, lib=None, verbose=False, weight_simple=0.0):
        raise RuntimeError("symbolic search exploded")

    def fix_symbolic(self, l, i, j, name, verbose=False, log_history=False):
        raise AssertionError("fix_symbolic should not run after suggest failure")


class PipelineModel:
    def __init__(self, input_dim: int = 2) -> None:
        self.n_edge = 6
        self.width_in = [input_dim, 1]
        self.width_out = [1, 1]
        self._state = {"weight": torch.tensor([1.0], dtype=torch.float32)}

    def state_dict(self):
        return {key: value.clone() for key, value in self._state.items()}

    def load_state_dict(self, state_dict):
        self._state = {key: value.clone() for key, value in state_dict.items()}

    def prune_edge(self, threshold: float) -> None:
        self.n_edge = max(1, self.n_edge - 1)

    def symbolic_formula(self):
        return None


def _make_pipeline_dataset(input_dim: int = 2) -> dict[str, torch.Tensor]:
    features = torch.arange(0, 6 * input_dim, dtype=torch.float32).reshape(6, input_dim)
    labels = torch.zeros((6, 1), dtype=torch.float32)
    return {
        "train_input": features,
        "train_label": labels,
        "test_input": features.clone(),
        "test_label": labels.clone(),
    }


def _fake_symbolic_result() -> dict[str, object]:
    return {
        "active": 1,
        "fixed": 1,
        "low_r2": 0,
        "failed": 0,
        "r2_records": [],
        "failed_records": [],
        "layer_times": [],
        "parallel_workers": 1,
    }


def _set_optional_symbolize_attr(config: AppConfig, name: str, value) -> None:
    object.__setattr__(config.symbolize, name, value)


def test_select_dataset_inputs_preserves_validation_split() -> None:
    dataset = {
        "train_input": torch.tensor([[1.0, 2.0], [3.0, 4.0]], dtype=torch.float32),
        "train_label": torch.tensor([[1.0], [0.0]], dtype=torch.float32),
        "val_input": torch.tensor([[5.0, 6.0]], dtype=torch.float32),
        "val_label": torch.tensor([[1.0]], dtype=torch.float32),
        "test_input": torch.tensor([[7.0, 8.0]], dtype=torch.float32),
        "test_label": torch.tensor([[0.0]], dtype=torch.float32),
    }

    selected = select_dataset_inputs(dataset, [1])

    assert torch.equal(selected["train_input"], torch.tensor([[2.0], [4.0]], dtype=torch.float32))
    assert torch.equal(selected["val_input"], torch.tensor([[6.0]], dtype=torch.float32))
    assert torch.equal(selected["test_input"], torch.tensor([[8.0]], dtype=torch.float32))
    assert torch.equal(selected["val_label"], dataset["val_label"])


def test_layerwise_validation_keeps_existing_val_split_after_compaction() -> None:
    dataset = {
        "train_input": torch.tensor([[1.0, 2.0], [3.0, 4.0], [9.0, 10.0]], dtype=torch.float32),
        "train_label": torch.tensor([[1.0], [0.0], [1.0]], dtype=torch.float32),
        "val_input": torch.tensor([[5.0, 6.0]], dtype=torch.float32),
        "val_label": torch.tensor([[1.0]], dtype=torch.float32),
        "test_input": torch.tensor([[7.0, 8.0]], dtype=torch.float32),
        "test_label": torch.tensor([[0.0]], dtype=torch.float32),
    }

    compacted = select_dataset_inputs(dataset, [1])
    fit_ds, val_ds = _build_layerwise_ft_datasets(
        compacted,
        use_validation=True,
        validation_ratio=0.0,
        validation_seed=123,
    )

    assert torch.equal(fit_ds["train_input"], compacted["train_input"])
    assert val_ds is not None
    assert torch.equal(val_ds["test_input"], compacted["val_input"])
    assert torch.equal(val_ds["test_label"], compacted["val_label"])


def test_safe_attribute_raises_when_feature_score_is_missing() -> None:
    dataset = {
        "train_input": torch.tensor([[1.0, 2.0], [3.0, 4.0]], dtype=torch.float32),
        "train_label": torch.tensor([[1.0], [0.0]], dtype=torch.float32),
    }

    with pytest.raises(RuntimeError, match="feature_score"):
        safe_attribute(MissingFeatureScoreModel(input_dim=2), dataset, n_sample=1)


def test_count_effective_edges_ignores_symbolic_zero_functions() -> None:
    class _EdgeCountModel:
        width_in = [2, 1]
        act_fun = [_MaskHolder(torch.zeros((2, 1), dtype=torch.int64))]
        symbolic_fun = [_SymbolicMaskHolder(torch.ones((1, 2), dtype=torch.int64), [["0", "x"]])]

    assert symbolic_pipeline._count_effective_edges(_EdgeCountModel()) == 1


def test_layerwise_symbolic_reports_suggest_failures() -> None:
    dataset = {
        "train_input": torch.tensor([[1.0]], dtype=torch.float32),
        "train_label": torch.tensor([[1.0]], dtype=torch.float32),
    }

    result = layerwise_symbolic(
        FailingSuggestModel(),
        dataset,
        layer_idx=0,
        lib=["x"],
        verbose=False,
    )

    assert result["active"] == 1
    assert result["fixed"] == 0
    assert result["failed"] == 1
    assert result["failed_records"] == [
        {
            "layer": 0,
            "i": 0,
            "j": 0,
            "error_type": "RuntimeError",
            "error_message": "symbolic search exploded",
        }
    ]


def test_symbolize_pipeline_records_prune_abort_details(monkeypatch: pytest.MonkeyPatch) -> None:
    dataset = _make_pipeline_dataset()

    monkeypatch.setattr(symbolic_pipeline, "clone_model", lambda model, **kwargs: copy.deepcopy(model))
    monkeypatch.setattr(symbolic_pipeline, "model_acc_ds", lambda *args, **kwargs: 0.9)
    monkeypatch.setattr(symbolic_pipeline, "get_n_edge", lambda model: model.n_edge)
    monkeypatch.setattr(
        symbolic_pipeline,
        "safe_attribute",
        lambda *args, **kwargs: (_ for _ in ()).throw(RuntimeError("attribute exploded")),
    )
    monkeypatch.setattr(symbolic_pipeline, "_fit_or_raise", lambda *args, **kwargs: None)
    monkeypatch.setattr(symbolic_pipeline, "_heavy_finetune", lambda *args, **kwargs: None)
    monkeypatch.setattr(symbolic_pipeline, "fast_symbolic", lambda *args, **kwargs: _fake_symbolic_result())
    monkeypatch.setattr(symbolic_pipeline, "collect_valid_formulas", lambda formulas: [])

    config = AppConfig()
    config.symbolize.target_edges = 1
    config.symbolize.max_prune_rounds = 1
    config.symbolize.enable_input_compaction = False
    config.symbolize.verbose = False

    result = symbolic_pipeline.symbolize_pipeline(PipelineModel(), dataset, config)
    timing = result["timing"]
    warning = timing["pipeline_warnings"][0]

    assert timing["abort_stage"] == "prune_round"
    assert timing["abort_reason"] == "attribute exploded"
    assert timing["abort_error_type"] == "RuntimeError"
    assert len(timing["pipeline_warnings"]) == 1
    assert warning["code"] == "prune_round_failed"
    assert warning["stage"] == "prune_round"
    assert warning["message"] == "attribute exploded"
    assert warning["error_type"] == "RuntimeError"
    assert warning["round"] == 0
    assert warning["threshold"] == pytest.approx(config.symbolize.prune_threshold_start)
    assert warning["attr_n_sample"] == 2048
    assert result["sym_stats"]["pipeline_warnings"] == timing["pipeline_warnings"]


def test_symbolize_pipeline_records_input_compaction_fallback(monkeypatch: pytest.MonkeyPatch) -> None:
    dataset = _make_pipeline_dataset()
    captured: dict[str, tuple[int, ...]] = {}

    monkeypatch.setattr(symbolic_pipeline, "clone_model", lambda model, **kwargs: copy.deepcopy(model))
    monkeypatch.setattr(symbolic_pipeline, "model_acc_ds", lambda *args, **kwargs: 0.9)
    monkeypatch.setattr(symbolic_pipeline, "get_n_edge", lambda model: model.n_edge)
    monkeypatch.setattr(
        symbolic_pipeline,
        "compact_inputs_for_symbolic",
        lambda *args, **kwargs: (_ for _ in ()).throw(ValueError("compaction exploded")),
    )
    monkeypatch.setattr(symbolic_pipeline, "_fit_or_raise", lambda *args, **kwargs: None)
    monkeypatch.setattr(symbolic_pipeline, "_heavy_finetune", lambda *args, **kwargs: None)
    monkeypatch.setattr(symbolic_pipeline, "collect_valid_formulas", lambda formulas: [])

    def fake_fast_symbolic(model, fit_dataset, **kwargs):
        captured["train_shape"] = tuple(fit_dataset["train_input"].shape)
        return _fake_symbolic_result()

    monkeypatch.setattr(symbolic_pipeline, "fast_symbolic", fake_fast_symbolic)

    config = AppConfig()
    config.symbolize.max_prune_rounds = 0
    config.symbolize.enable_input_compaction = True
    config.symbolize.verbose = False

    result = symbolic_pipeline.symbolize_pipeline(PipelineModel(), dataset, config)
    timing = result["timing"]

    assert timing["input_compaction_fallback"] is True
    assert timing["input_compaction_reason"] == "compaction exploded"
    assert timing["input_compaction_error_type"] == "ValueError"
    assert captured["train_shape"] == tuple(dataset["train_input"].shape)
    assert result["effective_input_dim"] == int(dataset["train_input"].shape[1])
    assert result["sym_stats"]["pipeline_warnings"] == [
        {
            "code": "input_compaction_fallback",
            "stage": "input_compaction",
            "message": "compaction exploded",
            "error_type": "ValueError",
        }
    ]


def test_symbolize_pipeline_keeps_baseline_backend_as_default(monkeypatch: pytest.MonkeyPatch) -> None:
    dataset = _make_pipeline_dataset()
    captured: dict[str, object] = {"fast_symbolic_called": 0}

    monkeypatch.setattr(symbolic_pipeline, "clone_model", lambda model, **kwargs: copy.deepcopy(model))
    monkeypatch.setattr(symbolic_pipeline, "model_acc_ds", lambda *args, **kwargs: 0.9)
    monkeypatch.setattr(symbolic_pipeline, "get_n_edge", lambda model: model.n_edge)
    monkeypatch.setattr(symbolic_pipeline, "_fit_or_raise", lambda *args, **kwargs: None)
    monkeypatch.setattr(symbolic_pipeline, "_heavy_finetune", lambda *args, **kwargs: None)
    monkeypatch.setattr(symbolic_pipeline, "collect_valid_formulas", lambda formulas: [])
    monkeypatch.setattr(
        symbolic_pipeline,
        "auto_symbolic_icbr",
        lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("ICBR backend should stay disabled by default")),
    )

    def fake_fast_symbolic(model, fit_dataset, **kwargs):
        captured["fast_symbolic_called"] = int(captured["fast_symbolic_called"]) + 1
        captured["fit_shape"] = tuple(fit_dataset["train_input"].shape)
        captured["lib_hidden"] = list(kwargs["lib_hidden"])
        captured["lib_output"] = list(kwargs["lib_output"])
        return _fake_symbolic_result()

    monkeypatch.setattr(symbolic_pipeline, "fast_symbolic", fake_fast_symbolic)

    config = AppConfig()
    config.symbolize.max_prune_rounds = 0
    config.symbolize.enable_input_compaction = False
    config.symbolize.verbose = False

    result = symbolic_pipeline.symbolize_pipeline(PipelineModel(), dataset, config)

    assert captured["fast_symbolic_called"] == 1
    assert captured["fit_shape"] == tuple(dataset["train_input"].shape)
    assert captured["lib_hidden"] == symbolic_pipeline.LIB_HIDDEN
    assert captured["lib_output"] == symbolic_pipeline.LIB_OUTPUT
    assert result["timing"]["symbolic_backend"] == "baseline"
    assert result["sym_stats"]["backend"] == "baseline"


def test_symbolize_pipeline_icbr_backend_uses_flattened_library_and_preserves_result_shape(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    dataset = _make_pipeline_dataset()
    captured: dict[str, object] = {}

    monkeypatch.setattr(symbolic_pipeline, "clone_model", lambda model, **kwargs: copy.deepcopy(model))
    monkeypatch.setattr(symbolic_pipeline, "model_acc_ds", lambda *args, **kwargs: 0.9)
    monkeypatch.setattr(symbolic_pipeline, "get_n_edge", lambda model: model.n_edge)
    monkeypatch.setattr(symbolic_pipeline, "_fit_or_raise", lambda *args, **kwargs: None)
    monkeypatch.setattr(symbolic_pipeline, "_heavy_finetune", lambda *args, **kwargs: None)
    monkeypatch.setattr(symbolic_pipeline, "collect_valid_formulas", lambda formulas: [])
    monkeypatch.setattr(
        symbolic_pipeline,
        "fast_symbolic",
        lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("baseline symbolic backend should not run")),
    )

    def fake_run_auto_symbolic_icbr_with_models(
        teacher_model,
        work_model,
        calibration_input,
        *,
        lib_names,
        topk,
        a_range,
        b_range,
        grid_number,
        iteration,
        verbose,
        collect_metrics,
        **kwargs,
    ):
        captured["calibration_shape"] = tuple(calibration_input.shape)
        captured["lib"] = list(lib_names)
        captured["topk"] = int(topk)
        captured["a_range"] = tuple(a_range)
        captured["b_range"] = tuple(b_range)
        captured["grid_number"] = int(grid_number)
        captured["iteration"] = int(iteration)
        captured["verbose"] = int(verbose)
        work = copy.deepcopy(work_model)
        work.n_edge = 2
        return work, {
            "candidate_generation_wall_time_s": 0.2,
            "replay_rerank_wall_time_s": 0.1,
            "replay_rank_inversion_count": 1,
            "replay_rank_inversion_total": 2,
            "replay_rank_inversion_rate": 0.5,
            "commit_param_drift_l2_mean": float("nan"),
            "commit_param_drift_l2_max": float("nan"),
        }

    monkeypatch.setattr(symbolic_pipeline, "_run_auto_symbolic_icbr_with_models", fake_run_auto_symbolic_icbr_with_models)

    config = AppConfig()
    config.symbolize.max_prune_rounds = 0
    config.symbolize.enable_input_compaction = False
    config.symbolize.verbose = False
    config.symbolize.lib_hidden = ["x", "tanh"]
    config.symbolize.lib_output = ["x^2", "tanh"]
    config.symbolize.symbolic_backend = "icbr"
    _set_optional_symbolize_attr(config, "icbr_topk", 7)
    _set_optional_symbolize_attr(config, "icbr_a_range", (-3.0, 3.0))
    _set_optional_symbolize_attr(config, "icbr_b_range", (-1.5, 1.5))
    _set_optional_symbolize_attr(config, "icbr_grid_number", 33)
    _set_optional_symbolize_attr(config, "icbr_iteration", 2)

    result = symbolic_pipeline.symbolize_pipeline(PipelineModel(), dataset, config)

    assert captured["calibration_shape"] == tuple(dataset["train_input"].shape)
    assert captured["lib"] == ["x", "tanh", "x^2"]
    assert captured["topk"] == 7
    assert captured["a_range"] == (-3.0, 3.0)
    assert captured["b_range"] == (-1.5, 1.5)
    assert captured["grid_number"] == 33
    assert captured["iteration"] == 2
    assert captured["verbose"] == 0
    assert result["timing"]["symbolic_backend"] == "icbr"
    assert result["timing"]["symbolic_backend_library"] == ["x", "tanh", "x^2"]
    assert result["timing"]["symbolic_backend_topk"] == 7
    assert result["sym_stats"]["backend"] == "icbr"
    assert result["sym_stats"]["library"] == ["x", "tanh", "x^2"]
    assert set(result) >= {"model", "formulas", "final_acc", "final_n_edge", "timing", "sym_stats"}


def test_symbolize_pipeline_from_prepared_reuses_shared_trace_across_backends(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    dataset = _make_pipeline_dataset()

    monkeypatch.setattr(symbolic_pipeline, "clone_model", lambda model, **kwargs: copy.deepcopy(model))
    monkeypatch.setattr(symbolic_pipeline, "model_acc_ds", lambda *args, **kwargs: 0.9)
    monkeypatch.setattr(symbolic_pipeline, "get_n_edge", lambda model: model.n_edge)
    monkeypatch.setattr(symbolic_pipeline, "_fit_or_raise", lambda *args, **kwargs: None)
    monkeypatch.setattr(symbolic_pipeline, "_heavy_finetune", lambda *args, **kwargs: None)
    monkeypatch.setattr(symbolic_pipeline, "collect_valid_formulas", lambda formulas: [])

    def fake_fast_symbolic(model, fit_dataset, **kwargs):
        return _fake_symbolic_result()

    def fake_run_auto_symbolic_icbr_with_models(
        teacher_model,
        work_model,
        calibration_input,
        *,
        lib_names,
        topk,
        a_range,
        b_range,
        grid_number,
        iteration,
        verbose,
        collect_metrics,
        **kwargs,
    ):
        work = copy.deepcopy(work_model)
        work.n_edge = 2
        return work, {
            "candidate_generation_wall_time_s": 0.2,
            "replay_rerank_wall_time_s": 0.1,
            "replay_rank_inversion_count": 0,
            "replay_rank_inversion_total": 1,
            "replay_rank_inversion_rate": 0.0,
            "commit_param_drift_l2_mean": float("nan"),
            "commit_param_drift_l2_max": float("nan"),
        }

    monkeypatch.setattr(symbolic_pipeline, "fast_symbolic", fake_fast_symbolic)
    monkeypatch.setattr(symbolic_pipeline, "_run_auto_symbolic_icbr_with_models", fake_run_auto_symbolic_icbr_with_models)

    config = AppConfig()
    config.symbolize.max_prune_rounds = 1
    config.symbolize.enable_input_compaction = False
    config.symbolize.verbose = False

    prepared = symbolic_pipeline.prepare_symbolic_bundle(PipelineModel(), dataset, config)
    baseline_result = symbolic_pipeline.symbolize_pipeline_from_prepared(copy.deepcopy(prepared), dataset, config)

    config_icbr = config.model_copy(deep=True)
    config_icbr.symbolize.symbolic_backend = "icbr"
    icbr_result = symbolic_pipeline.symbolize_pipeline_from_prepared(copy.deepcopy(prepared), dataset, config_icbr)

    assert baseline_result["trace"].to_dict(orient="records") == icbr_result["trace"].to_dict(orient="records")
    assert baseline_result["effective_input_indices"] == icbr_result["effective_input_indices"]
    assert baseline_result["sym_stats"]["backend"] == "baseline"
    assert icbr_result["sym_stats"]["backend"] == "icbr"
