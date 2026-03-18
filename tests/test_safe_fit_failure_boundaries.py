from __future__ import annotations

import copy

import pytest
import torch

from symkan.config import AppConfig
from symkan.core.train import SafeFitError, safe_fit
from symkan.core.types import FitReport
from symkan.symbolic import pipeline as symbolic_pipeline
from symkan.symbolic import search as symbolic_search
from symkan.tuning import stagewise as stagewise_module


class FailingFitModel:
    def __init__(self) -> None:
        self.ckpt_path = ""

    def fit(self, **kwargs):
        raise RuntimeError("fit exploded")


class HistoryRetryModel:
    def __init__(self) -> None:
        self.ckpt_path = ""
        self.calls = 0

    def fit(self, **kwargs):
        self.calls += 1
        if self.calls == 1:
            raise RuntimeError("missing history.txt entry")
        return {"train_loss": [0.1], "test_loss": [0.2]}


class GridFallbackModel:
    def __init__(self) -> None:
        self.ckpt_path = ""
        self.update_grid_flags: list[bool] = []

    def fit(self, **kwargs):
        update_grid = bool(kwargs.get("update_grid", False))
        self.update_grid_flags.append(update_grid)
        if update_grid:
            raise RuntimeError("grid update failed")
        return {"train_loss": [0.3], "test_loss": [0.4]}


class FakeKAN:
    def __init__(self, **kwargs) -> None:
        self.n_edge = 10
        self.training = True
        self.width_in = [1]
        self.width_out = [1, 1]
        self._state = {"weight": torch.tensor([1.0], dtype=torch.float32)}

    def state_dict(self):
        return {key: value.clone() for key, value in self._state.items()}

    def load_state_dict(self, state_dict):
        self._state = {key: value.clone() for key, value in state_dict.items()}

    def parameters(self):
        yield torch.nn.Parameter(torch.tensor([0.0], dtype=torch.float32))

    def train(self, mode: bool = True):
        self.training = mode
        return self


class FakeSymbolicModel:
    def __init__(self) -> None:
        self.n_edge = 5
        self.width_in = [1, 1]
        self.width_out = [1, 1]
        self._state = {"weight": torch.tensor([1.0], dtype=torch.float32)}

    def state_dict(self):
        return {key: value.clone() for key, value in self._state.items()}

    def load_state_dict(self, state_dict):
        self._state = {key: value.clone() for key, value in state_dict.items()}


class FakeLayerwiseModel:
    def __init__(self) -> None:
        self._state = {"weight": torch.tensor([1.0], dtype=torch.float32)}

    def state_dict(self):
        return {key: value.clone() for key, value in self._state.items()}

    def load_state_dict(self, state_dict):
        self._state = {key: value.clone() for key, value in state_dict.items()}


def make_dataset() -> dict[str, torch.Tensor]:
    features = torch.zeros((4, 1), dtype=torch.float32)
    labels = torch.zeros((4, 1), dtype=torch.float32)
    return {
        "train_input": features,
        "train_label": labels,
        "test_input": features.clone(),
        "test_label": labels.clone(),
    }


def test_safe_fit_can_raise_in_strict_mode() -> None:
    with pytest.raises(SafeFitError, match="unit_test_fit failed"):
        safe_fit(
            FailingFitModel(),
            dataset=make_dataset(),
            steps=1,
            raise_on_failure=True,
            context="unit_test_fit",
        )


def test_safe_fit_retries_when_history_file_error_occurs() -> None:
    model = HistoryRetryModel()

    result = safe_fit(
        model,
        dataset=make_dataset(),
        steps=1,
    )

    assert model.calls == 2
    assert result["train_loss"] == [0.1]
    assert result["test_loss"] == [0.2]


def test_safe_fit_disables_grid_update_after_initial_failure() -> None:
    model = GridFallbackModel()

    result = safe_fit(
        model,
        dataset=make_dataset(),
        steps=1,
        update_grid=True,
    )

    assert model.update_grid_flags == [True, False]
    assert result["train_loss"] == [0.3]
    assert result["test_loss"] == [0.4]


def test_stagewise_logs_failed_stage_fit_and_recovers(monkeypatch: pytest.MonkeyPatch) -> None:
    reports = iter(
        [
            FitReport(success=False, error_type="RuntimeError", error_message="stage fit failed"),
            FitReport(success=True, result={"train_loss": [0.1], "test_loss": [0.2]}),
        ]
    )

    monkeypatch.setattr(stagewise_module, "KAN", FakeKAN)
    monkeypatch.setattr(stagewise_module, "clone_model", lambda model, **kwargs: copy.deepcopy(model))
    monkeypatch.setattr(stagewise_module, "model_acc_ds", lambda *args, **kwargs: 0.8)
    monkeypatch.setattr(stagewise_module, "get_n_edge", lambda model: model.n_edge)
    monkeypatch.setattr(stagewise_module, "safe_fit_report", lambda **kwargs: next(reports))

    config = AppConfig()
    config.stagewise.width = [1, 1]
    config.stagewise.lamb_schedule = (0.0,)
    config.stagewise.lr_schedule = (0.01,)
    config.stagewise.steps_per_stage = 1
    config.stagewise.prune_start_stage = 99
    config.stagewise.verbose = False

    _, result = stagewise_module.stagewise_train(make_dataset(), config)

    assert result["stage_logs"][0]["fit_success"] is False
    assert "stage_0_fit failed" in result["stage_logs"][0]["rollback"]
    assert result["final_fit_success"] is True
    assert result["successful_fit_count"] == 1


def test_symbolize_pipeline_raises_on_pre_symbolic_fit_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(symbolic_pipeline, "clone_model", lambda model, **kwargs: copy.deepcopy(model))
    monkeypatch.setattr(symbolic_pipeline, "model_acc_ds", lambda *args, **kwargs: 0.9)
    monkeypatch.setattr(symbolic_pipeline, "get_n_edge", lambda model: model.n_edge)
    monkeypatch.setattr(
        symbolic_pipeline,
        "safe_fit_report",
        lambda **kwargs: FitReport(success=False, error_type="RuntimeError", error_message="pre fit failed"),
    )

    config = AppConfig()
    config.symbolize.max_prune_rounds = 0
    config.symbolize.enable_input_compaction = False
    config.symbolize.verbose = False

    with pytest.raises(RuntimeError, match="pre_symbolic_fit failed"):
        symbolic_pipeline.symbolize_pipeline(FakeSymbolicModel(), make_dataset(), config)


def test_layerwise_finetune_reports_fit_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        symbolic_search,
        "safe_fit_report",
        lambda *args, **kwargs: FitReport(success=False, error_type="RuntimeError", error_message="layerwise failed"),
    )

    info = symbolic_search._layerwise_finetune_with_early_stop(
        FakeLayerwiseModel(),
        fit_dataset=make_dataset(),
        val_dataset=None,
        total_steps=5,
        lr=0.01,
        lamb=0.0,
        batch_size=2,
        use_validation=False,
        eval_interval=1,
        early_stop_patience=1,
        early_stop_min_delta=1e-4,
        validation_n_sample=10,
        verbose=False,
    )

    assert info["fit_failed"] is True
    assert info["steps_used"] == 0
    assert "layerwise_finetune failed" in info["fit_error"]
