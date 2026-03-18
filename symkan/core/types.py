"""symkan 公共类型定义。

所有跨模块传递的结构化对象在此定义，消除裸字典和魔法字符串键。
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union

import torch

from symkan.config import StagewiseConfig, SymbolizeConfig, TrainConfig


# ---------------------------------------------------------------------------
# Dataset
# ---------------------------------------------------------------------------

@dataclass
class DatasetBundle:
    """结构化数据集容器，替代旧版裸字典。"""

    train_input: torch.Tensor
    train_label: torch.Tensor
    test_input: torch.Tensor
    test_label: torch.Tensor
    val_input: Optional[torch.Tensor] = None
    val_label: Optional[torch.Tensor] = None

    # ---- 兼容旧 dict 接口 ----

    def __getitem__(self, key: str) -> torch.Tensor:
        _MAP = {
            "train_input": "train_input",
            "train_label": "train_label",
            "val_input": "val_input",
            "val_label": "val_label",
            "test_input": "test_input",
            "test_label": "test_label",
        }
        attr = _MAP.get(key)
        if attr is None:
            raise KeyError(key)
        return getattr(self, attr)

    def __contains__(self, key: str) -> bool:
        return key in ("train_input", "train_label", "val_input", "val_label", "test_input", "test_label")

    @classmethod
    def from_dict(cls, d: dict) -> "DatasetBundle":
        return cls(
            train_input=d["train_input"],
            train_label=d["train_label"],
            val_input=d.get("val_input"),
            val_label=d.get("val_label"),
            test_input=d["test_input"],
            test_label=d["test_label"],
        )

    def to_dict(self) -> dict:
        return {
            "train_input": self.train_input,
            "train_label": self.train_label,
            "val_input": self.val_input,
            "val_label": self.val_label,
            "test_input": self.test_input,
            "test_label": self.test_label,
        }


# ---------------------------------------------------------------------------
# Config objects
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Report / Result objects
# ---------------------------------------------------------------------------

@dataclass
class FitReport:
    """safe_fit 结构化返回。"""

    success: bool
    result: dict = field(default_factory=dict)
    fallback_used: Optional[str] = None
    error_type: Optional[str] = None
    error_message: Optional[str] = None


@dataclass
class AttributeReport:
    """safe_attribute 结构化返回。"""

    success: bool
    score: Any = None  # numpy array
    fallback_used: Optional[str] = None
    error_type: Optional[str] = None
    error_message: Optional[str] = None


@dataclass
class StageSnapshot:
    """单阶段快照信息。"""

    stage: Union[int, str]
    acc: float
    n_edges: Union[int, float]
    score: float
    model: Any = None


@dataclass
class StagewiseResult:
    """stagewise_train 结构化返回。"""

    best_model: Any
    train_loss: List[float] = field(default_factory=list)
    test_loss: List[float] = field(default_factory=list)
    stage_logs: List[dict] = field(default_factory=list)
    best_acc: float = 0.0
    selected_stage: Union[int, str] = 0
    selected_edges: Union[int, float] = 0
    selected_score: float = 0.0
    best_state_dict: Optional[dict] = None
    stage_snapshots: List[dict] = field(default_factory=list)
    topk_models: Optional[List[dict]] = None
    stage_guard_mode: str = "light"
    stage_early_stopped: bool = False
    stage_early_stop_reason: str = ""
    stage_timings: List[dict] = field(default_factory=list)
    stage_train_total_seconds: float = 0.0
    stage_prune_total_seconds: float = 0.0
    final_finetune_seconds: float = 0.0
    final_fit_success: bool = False
    final_fit_error: str = ""
    successful_fit_count: int = 0
    stage_total_seconds: float = 0.0

    def to_legacy_dict(self) -> dict:
        """转换回旧版 dict 格式以保持向后兼容。"""
        d = {
            "train_loss": self.train_loss,
            "test_loss": self.test_loss,
            "stage_logs": self.stage_logs,
            "best_acc": self.best_acc,
            "selected_stage": self.selected_stage,
            "selected_edges": self.selected_edges,
            "selected_score": self.selected_score,
            "best_state_dict": self.best_state_dict,
            "stage_snapshots": self.stage_snapshots,
            "stage_guard_mode": self.stage_guard_mode,
            "stage_early_stopped": self.stage_early_stopped,
            "stage_early_stop_reason": self.stage_early_stop_reason,
            "stage_timings": self.stage_timings,
            "stage_train_total_seconds": self.stage_train_total_seconds,
            "stage_prune_total_seconds": self.stage_prune_total_seconds,
            "final_finetune_seconds": self.final_finetune_seconds,
            "final_fit_success": self.final_fit_success,
            "final_fit_error": self.final_fit_error,
            "successful_fit_count": self.successful_fit_count,
            "stage_total_seconds": self.stage_total_seconds,
        }
        if self.topk_models is not None:
            d["topk_models"] = self.topk_models
        return d


@dataclass
class SymbolizeResult:
    """symbolize_pipeline 结构化返回。"""

    model: Any = None
    formulas: Any = None
    valid_expressions: List[dict] = field(default_factory=list)
    trace: Any = None  # DataFrame
    sym_stats: Dict[str, Any] = field(default_factory=dict)
    final_n_edge: Union[int, float] = 0
    final_n_edge_raw: Union[int, float] = 0
    final_acc: float = 0.0
    effective_target_edges: int = 0
    input_n_edge: Union[int, float] = 0
    effective_input_indices: List[int] = field(default_factory=list)
    effective_input_dim: int = 0
    timing: Dict[str, Any] = field(default_factory=dict)

    def to_legacy_dict(self) -> dict:
        """转换回旧版 dict 格式以保持向后兼容。"""
        return {
            "model": self.model,
            "formulas": self.formulas,
            "valid_expressions": self.valid_expressions,
            "trace": self.trace,
            "sym_stats": self.sym_stats,
            "final_n_edge": self.final_n_edge,
            "final_n_edge_raw": self.final_n_edge_raw,
            "final_acc": self.final_acc,
            "effective_target_edges": self.effective_target_edges,
            "input_n_edge": self.input_n_edge,
            "effective_input_indices": self.effective_input_indices,
            "effective_input_dim": self.effective_input_dim,
            "timing": self.timing,
        }
