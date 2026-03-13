"""symkan 公共类型定义。

所有跨模块传递的结构化对象在此定义，消除裸字典和魔法字符串键。
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union

import torch


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

@dataclass
class TrainConfig:
    """safe_fit 训练参数。"""

    opt: str = "Adam"
    steps: int = 50
    lr: float = 0.01
    lamb: float = 0.0
    lamb_l1: float = 1.0
    lamb_entropy: float = 0.0
    batch: int = -1
    update_grid: bool = False
    singularity_avoiding: bool = True
    log: int = 10


@dataclass
class StagewiseConfig:
    """stagewise_train 参数。"""

    width: Optional[list] = None
    grid: int = 5
    k: int = 3
    seed: int = 123
    lamb_schedule: tuple = (0.0, 1e-4, 3e-4)
    lr_schedule: tuple = (0.02, 0.012, 0.006)
    steps_per_stage: int = 70
    batch_size: Optional[int] = None
    prune_start_stage: int = 1
    target_edges: int = 100
    prune_edge_threshold_init: float = 0.005
    prune_edge_threshold_step: float = 0.005
    prune_acc_drop_tol: float = 0.03
    post_prune_ft_steps: int = 40
    sym_target_edges: int = 50
    acc_weight: float = 0.4
    keep_topk_models: int = 0
    keep_full_snapshots: bool = False
    use_disk_clone: bool = False
    clone_ckpt_path: str = "_safe_copy_temp"
    use_validation: bool = False
    validation_ratio: float = 0.0
    validation_seed: Optional[int] = None
    validation_min_samples: int = 10
    adaptive_threshold: bool = False
    threshold_base_step: float = 0.005
    threshold_min: float = 0.001
    threshold_max: float = 0.1
    success_boost: float = 0.5
    failure_penalty: float = 0.3
    min_gain_threshold: int = 3
    max_prune_attempts: int = 20
    adaptive_lamb: bool = False
    min_lamb_ratio: float = 0.3
    max_lamb_ratio: float = 1.5
    adaptive_ft: bool = False
    min_ft_ratio: float = 0.3
    verbose: bool = True


@dataclass
class SymbolizeConfig:
    """symbolize_pipeline 参数。"""

    target_edges: int = 60
    max_prune_rounds: int = 40
    lib: Optional[list] = None
    lib_hidden: Optional[list] = None
    lib_output: Optional[list] = None
    weight_simple: float = 0.0
    finetune_steps: int = 30
    finetune_lr: float = 0.005
    affine_finetune_steps: int = 600
    affine_finetune_lr_schedule: Optional[list] = None
    layerwise_finetune_steps: int = 200
    batch_size: Optional[int] = None
    parallel_mode: str = "auto"
    parallel_workers: Optional[int] = None
    parallel_min_tasks: int = 16
    prune_eval_interval: int = 1
    prune_attr_sample_adaptive: bool = False
    prune_attr_sample_min: int = 512
    prune_attr_sample_max: int = 2048
    heavy_ft_early_stop_patience: int = 0
    heavy_ft_early_stop_min_delta: float = 1e-4
    collect_timing: bool = True
    verbose: bool = True


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
