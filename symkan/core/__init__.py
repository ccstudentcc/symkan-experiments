"""@file
@brief symkan 核心运行时与模型基础接口导出模块。

该模块集中导出设备管理、数据构建、训练封装与基础评估接口。
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
