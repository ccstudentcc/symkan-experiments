"""Export module for symkan core runtime and foundational model interfaces.

This module centralizes exports for device management, dataset construction,
training wrappers, and basic evaluation helpers.
"""

from .runtime import get_device, set_device
from .data import build_dataset
from .infer import model_logits, model_logits_ds, model_acc, model_acc_ds_fast, model_acc_ds, get_n_edge
from .train import safe_fit, safe_fit_report
from .types import (
    DatasetBundle,
    TrainConfig,
    StagewiseConfig,
    SymbolizeConfig,
    FitReport,
    AttributeReport,
    StageSnapshot,
    StagewiseResult,
    SymbolizeResult,
)

__all__ = [
    "get_device",
    "set_device",
    "build_dataset",
    "model_logits",
    "model_logits_ds",
    "model_acc",
    "model_acc_ds_fast",
    "model_acc_ds",
    "get_n_edge",
    "safe_fit",
    "safe_fit_report",
    "DatasetBundle",
    "TrainConfig",
    "StagewiseConfig",
    "SymbolizeConfig",
    "FitReport",
    "AttributeReport",
    "StageSnapshot",
    "StagewiseResult",
    "SymbolizeResult",
]
