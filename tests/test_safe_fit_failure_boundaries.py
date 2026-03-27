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


class CountingKAN(FakeKAN):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.state_dict_call_count = 0

    def state_dict(self):
        self.state_dict_call_count += 1
        return super().state_dict()


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


def patch_stagewise_success(monkeypatch: pytest.MonkeyPatch) -> None:
    reports = iter(
        [
            FitReport(success=True, result={"train_loss": [0.1], "test_loss": [0.2]}),
            FitReport(success=True, result={"train_loss": [0.05], "test_loss": [0.1]}),
        ]
    )
    monkeypatch.setattr(stagewise_module, "KAN", FakeKAN)
    monkeypatch.setattr(stagewise_module, "clone_model", lambda model, **kwargs: copy.deepcopy(model))
    monkeypatch.setattr(stagewise_module, "model_acc_ds", lambda *args, **kwargs: 0.8)
    monkeypatch.setattr(stagewise_module, "get_n_edge", lambda model: model.n_edge)
    monkeypatch.setattr(stagewise_module, "safe_fit_report", lambda **kwargs: next(reports))


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
    assert result["stage_logs"][0]["guard_mode"] == "light"
    assert "stage_0_fit failed" in result["stage_logs"][0]["rollback"]
    assert result["final_fit_success"] is True
    assert result["successful_fit_count"] == 1


def test_stagewise_light_guard_reduces_prefit_snapshot_overhead(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    instances: list[CountingKAN] = []

    def _new_kan(**kwargs):
        model = CountingKAN(**kwargs)
        instances.append(model)
        return model

    monkeypatch.setattr(stagewise_module, "KAN", _new_kan)
    monkeypatch.setattr(stagewise_module, "clone_model", lambda model, **kwargs: copy.deepcopy(model))
    monkeypatch.setattr(stagewise_module, "model_acc_ds", lambda *args, **kwargs: 0.8)
    monkeypatch.setattr(stagewise_module, "get_n_edge", lambda model: model.n_edge)

    def _run(mode: str) -> int:
        reports = iter(
            [
                FitReport(success=True, result={"train_loss": [0.1], "test_loss": [0.2]}),
                FitReport(success=True, result={"train_loss": [0.05], "test_loss": [0.1]}),
            ]
        )
        monkeypatch.setattr(stagewise_module, "safe_fit_report", lambda **kwargs: next(reports))

        config = AppConfig()
        config.stagewise.width = [1, 1]
        config.stagewise.lamb_schedule = (0.0,)
        config.stagewise.lr_schedule = (0.01,)
        config.stagewise.steps_per_stage = 1
        config.stagewise.prune_start_stage = 99
        config.stagewise.verbose = False
        config.stagewise.guard_mode = mode

        stagewise_module.stagewise_train(make_dataset(), config)
        return instances[-1].state_dict_call_count

    full_calls = _run("full")
    light_calls = _run("light")

    assert full_calls > light_calls


def test_stagewise_forwards_model_numeric_basis_to_kan(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: dict[str, object] = {}

    def _new_kan(**kwargs):
        captured["kwargs"] = dict(kwargs)
        return FakeKAN(**kwargs)

    reports = iter(
        [
            FitReport(success=True, result={"train_loss": [0.1], "test_loss": [0.2]}),
            FitReport(success=True, result={"train_loss": [0.05], "test_loss": [0.1]}),
        ]
    )
    monkeypatch.setattr(stagewise_module, "KAN", _new_kan)
    monkeypatch.setattr(stagewise_module, "clone_model", lambda model, **kwargs: copy.deepcopy(model))
    monkeypatch.setattr(stagewise_module, "model_acc_ds", lambda *args, **kwargs: 0.8)
    monkeypatch.setattr(stagewise_module, "get_n_edge", lambda model: model.n_edge)
    monkeypatch.setattr(stagewise_module, "safe_fit_report", lambda **kwargs: next(reports))

    config = AppConfig()
    config.model.numeric_basis = "radial_bf"
    config.stagewise.width = [1, 1]
    config.stagewise.lamb_schedule = (0.0,)
    config.stagewise.lr_schedule = (0.01,)
    config.stagewise.steps_per_stage = 1
    config.stagewise.prune_start_stage = 99
    config.stagewise.verbose = False

    stagewise_module.stagewise_train(make_dataset(), config)

    assert captured["kwargs"]["numeric_basis"] == "radial_bf"


def test_stagewise_prints_concise_progress_when_not_verbose(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    patch_stagewise_success(monkeypatch)

    config = AppConfig()
    config.runtime.quiet = False
    config.stagewise.width = [1, 1]
    config.stagewise.lamb_schedule = (0.0,)
    config.stagewise.lr_schedule = (0.01,)
    config.stagewise.steps_per_stage = 1
    config.stagewise.prune_start_stage = 99
    config.stagewise.verbose = False

    stagewise_module.stagewise_train(make_dataset(), config)

    stdout = capsys.readouterr().out
    assert "[stagewise] start:" in stdout
    assert "[stagewise] stage 1/1 start:" in stdout
    assert "[stagewise] final finetune start" in stdout
    assert "[stagewise] selected stage=" in stdout


def test_stagewise_suppresses_concise_progress_in_quiet_mode(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    patch_stagewise_success(monkeypatch)

    config = AppConfig()
    config.runtime.quiet = True
    config.stagewise.width = [1, 1]
    config.stagewise.lamb_schedule = (0.0,)
    config.stagewise.lr_schedule = (0.01,)
    config.stagewise.steps_per_stage = 1
    config.stagewise.prune_start_stage = 99
    config.stagewise.verbose = False

    stagewise_module.stagewise_train(make_dataset(), config)

    assert capsys.readouterr().out == ""


def test_stagewise_report_preserves_timing_fields(monkeypatch: pytest.MonkeyPatch) -> None:
    patch_stagewise_success(monkeypatch)

    config = AppConfig()
    config.stagewise.width = [1, 1]
    config.stagewise.lamb_schedule = (0.0,)
    config.stagewise.lr_schedule = (0.01,)
    config.stagewise.steps_per_stage = 1
    config.stagewise.prune_start_stage = 99
    config.stagewise.verbose = False

    _, report = stagewise_module.stagewise_train_report(make_dataset(), config)
    legacy = report.to_legacy_dict()

    assert "stage_total_seconds" in legacy
    assert "stage_train_total_seconds" in legacy
    assert legacy["final_fit_success"] is True
    assert legacy["successful_fit_count"] == 2


def test_stagewise_rolls_back_when_final_finetune_fails(monkeypatch: pytest.MonkeyPatch) -> None:
    call_count = {"n": 0}

    def _fake_safe_fit_report(**kwargs):
        model = kwargs["model"]
        call_count["n"] += 1
        if call_count["n"] == 1:
            model._state["weight"] = torch.tensor([2.0], dtype=torch.float32)
            return FitReport(success=True, result={"train_loss": [0.1], "test_loss": [0.2]})
        if call_count["n"] == 2:
            model._state["weight"] = torch.tensor([9.0], dtype=torch.float32)
            return FitReport(success=False, error_type="RuntimeError", error_message="final fit failed")
        raise AssertionError(f"unexpected safe_fit_report call index: {call_count['n']}")

    monkeypatch.setattr(stagewise_module, "KAN", FakeKAN)
    monkeypatch.setattr(stagewise_module, "clone_model", lambda model, **kwargs: copy.deepcopy(model))
    monkeypatch.setattr(stagewise_module, "model_acc_ds", lambda *args, **kwargs: 0.8)
    monkeypatch.setattr(stagewise_module, "get_n_edge", lambda model: model.n_edge)
    monkeypatch.setattr(stagewise_module, "safe_fit_report", _fake_safe_fit_report)

    config = AppConfig()
    config.stagewise.width = [1, 1]
    config.stagewise.lamb_schedule = (0.0,)
    config.stagewise.lr_schedule = (0.01,)
    config.stagewise.steps_per_stage = 1
    config.stagewise.prune_start_stage = 99
    config.stagewise.verbose = False

    best_model, result = stagewise_module.stagewise_train(make_dataset(), config)

    assert result["final_fit_success"] is False
    assert "final fit failed" in result["final_fit_error"]
    assert float(best_model.state_dict()["weight"].item()) == pytest.approx(2.0)


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
