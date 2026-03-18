from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

PYDANTIC_AVAILABLE = True

DEFAULT_X_TRAIN = "data/X_train.npy"
DEFAULT_X_TEST = "data/X_test.npy"
DEFAULT_Y_TRAIN = "data/Y_train_cat.npy"
DEFAULT_Y_TEST = "data/Y_test_cat.npy"


class RuntimeConfig(BaseModel):
    """Runtime settings shared across symkan workflows."""

    model_config = ConfigDict(extra="forbid", arbitrary_types_allowed=True)

    device: str = "auto"
    global_seed: int = 123
    baseline_seed: int = 123
    batch_size: int = Field(default=0, ge=0)
    quiet: bool = False
    verbose: bool = False


class DataConfig(BaseModel):
    """Input dataset locations and loading behavior."""

    model_config = ConfigDict(extra="forbid", arbitrary_types_allowed=True)

    x_train: str = DEFAULT_X_TRAIN
    x_test: str = DEFAULT_X_TEST
    y_train: str = DEFAULT_Y_TRAIN
    y_test: str = DEFAULT_Y_TEST
    auto_fetch_mnist: bool = True
    allow_auto_fetch_outside_data_dir: bool = False
    mnist_classes: list[int] = Field(default_factory=lambda: list(range(10)))

    @field_validator("mnist_classes")
    @classmethod
    def validate_mnist_classes(cls, value: list[int]) -> list[int]:
        if not value:
            raise ValueError("mnist_classes must not be empty")
        normalized = [int(item) for item in value]
        invalid = [item for item in normalized if item < 0 or item > 9]
        if invalid:
            raise ValueError(f"mnist_classes must stay within [0, 9], got {invalid}")
        return normalized


class ModelConfig(BaseModel):
    """Model construction and baseline-fit settings."""

    model_config = ConfigDict(extra="forbid", arbitrary_types_allowed=True)

    inner_dim: int = 16
    grid: int = 5
    k: int = 3
    baseline_steps: int = 150
    baseline_lr: float = 0.02
    baseline_lamb: float = 1e-4
    baseline_log: int = 12
    top_k: int = Field(default=120, gt=0)


class LibraryConfig(BaseModel):
    """Symbolic library selection settings."""

    model_config = ConfigDict(extra="forbid", arbitrary_types_allowed=True)

    lib_preset: str = "layered"

    @field_validator("lib_preset")
    @classmethod
    def validate_lib_preset(cls, value: str) -> str:
        allowed = {"layered", "fast", "expressive", "full"}
        if value not in allowed:
            raise ValueError(f"lib_preset must be one of {sorted(allowed)}")
        return value


class WorkflowConfig(BaseModel):
    """Workflow switches that change the training path."""

    model_config = ConfigDict(extra="forbid", arbitrary_types_allowed=True)

    disable_stagewise_train: bool = False
    e2e_steps: int = 0
    e2e_lr: float = 0.0
    e2e_lamb: float = -1.0


class EvaluationConfig(BaseModel):
    """Evaluation and export validation settings."""

    model_config = ConfigDict(extra="forbid", arbitrary_types_allowed=True)

    validate_n_sample: int = Field(default=500, gt=0)


class TrainConfig(BaseModel):
    """safe_fit runtime configuration."""

    model_config = ConfigDict(extra="forbid", arbitrary_types_allowed=True)

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


class StagewiseConfig(BaseModel):
    """stagewise_train runtime configuration."""

    model_config = ConfigDict(extra="forbid", arbitrary_types_allowed=True)

    width: Optional[list[int]] = None
    grid: int = 5
    k: int = 3
    seed: int = 123
    lamb_schedule: tuple[float, ...] = (0.0, 1e-4, 3e-4)
    lr_schedule: tuple[float, ...] = (0.02, 0.012, 0.006)
    steps_per_stage: int = Field(default=70, gt=0)
    batch_size: Optional[int] = Field(default=None, gt=0)
    prune_start_stage: int = Field(default=1, ge=0)
    target_edges: int = Field(default=100, ge=0)
    prune_edge_threshold_init: float = 0.005
    prune_edge_threshold_step: float = 0.005
    prune_acc_drop_tol: float = Field(default=0.08, ge=0.0, le=1.0)
    post_prune_ft_steps: int = Field(default=40, ge=0)
    sym_target_edges: int = Field(default=50, ge=0)
    acc_weight: float = 0.4
    keep_topk_models: int = Field(default=0, ge=0)
    keep_full_snapshots: bool = False
    use_disk_clone: bool = False
    clone_ckpt_path: str = "_safe_copy_temp"
    use_validation: bool = False
    validation_ratio: float = Field(default=0.0, ge=0.0, lt=1.0)
    validation_seed: Optional[int] = None
    validation_min_samples: int = Field(default=10, gt=0)
    adaptive_threshold: bool = False
    threshold_base_step: float = 0.005
    threshold_min: float = 0.001
    threshold_max: float = 0.1
    success_boost: float = 0.5
    failure_penalty: float = 0.3
    min_gain_threshold: int = 3
    max_prune_attempts: int = Field(default=20, gt=0)
    adaptive_lamb: bool = False
    min_lamb_ratio: float = 0.3
    max_lamb_ratio: float = 1.5
    adaptive_ft: bool = False
    min_ft_ratio: float = 0.3
    stage_early_stop: bool = False
    stage_early_stop_patience: int = Field(default=2, ge=0)
    stage_early_stop_min_acc_gain: float = 0.002
    stage_early_stop_edge_buffer: int = Field(default=0, ge=0)
    guard_mode: Literal["light", "full"] = "light"
    verbose: bool = True


class SymbolizeConfig(BaseModel):
    """symbolize_pipeline runtime configuration."""

    model_config = ConfigDict(extra="forbid", arbitrary_types_allowed=True)

    target_edges: int = Field(default=60, ge=0)
    max_prune_rounds: int = Field(default=40, ge=0)
    lib: Optional[list[Any]] = None
    lib_hidden: Optional[list[Any]] = None
    lib_output: Optional[list[Any]] = None
    weight_simple: float = 0.0
    finetune_steps: int = Field(default=30, ge=0)
    finetune_lr: float = 0.005
    affine_finetune_steps: int = Field(default=600, ge=0)
    affine_finetune_lr_schedule: Optional[list[float]] = None
    layerwise_finetune_steps: int = Field(default=60, ge=0)
    layerwise_finetune_lr: float = 0.005
    layerwise_finetune_lamb: float = 1e-5
    layerwise_use_validation: bool = True
    layerwise_validation_ratio: float = Field(default=0.15, ge=0.0, lt=1.0)
    layerwise_validation_seed: Optional[int] = None
    layerwise_early_stop_patience: int = Field(default=2, ge=0)
    layerwise_early_stop_min_delta: float = 1e-3
    layerwise_eval_interval: int = Field(default=20, gt=0)
    layerwise_validation_n_sample: int = Field(default=300, gt=0)
    batch_size: Optional[int] = Field(default=None, gt=0)
    parallel_mode: str = "auto"
    parallel_workers: Optional[int] = Field(default=None, gt=0)
    parallel_min_tasks: int = Field(default=16, ge=0)
    enable_input_compaction: bool = True
    prune_collapse_floor: float = 0.6
    prune_eval_interval: int = Field(default=1, gt=0)
    prune_attr_sample_adaptive: bool = False
    prune_attr_sample_min: int = Field(default=512, gt=0)
    prune_attr_sample_max: int = Field(default=2048, gt=0)
    prune_threshold_start: float = 0.02
    prune_threshold_end: float = 0.03
    prune_max_drop_ratio_per_round: float = 1.0
    prune_threshold_backoff: float = 0.7
    prune_adaptive_threshold: bool = False
    prune_adaptive_step: float = 0.0
    prune_adaptive_acc_drop_tol: float = 0.02
    prune_adaptive_min_edges_gain: int = Field(default=1, ge=0)
    prune_adaptive_low_gain_patience: int = Field(default=4, ge=0)
    heavy_ft_early_stop_patience: int = Field(default=0, ge=0)
    heavy_ft_early_stop_min_delta: float = 1e-4
    collect_timing: bool = True
    verbose: bool = True


class AppConfig(BaseModel):
    """Unified runtime configuration for symkan workflows."""

    model_config = ConfigDict(extra="forbid", arbitrary_types_allowed=True)

    runtime: RuntimeConfig = Field(default_factory=RuntimeConfig)
    data: DataConfig = Field(default_factory=DataConfig)
    model: ModelConfig = Field(default_factory=ModelConfig)
    library: LibraryConfig = Field(default_factory=LibraryConfig)
    workflow: WorkflowConfig = Field(default_factory=WorkflowConfig)
    evaluation: EvaluationConfig = Field(default_factory=EvaluationConfig)
    train: TrainConfig = Field(default_factory=TrainConfig)
    stagewise: StagewiseConfig = Field(default_factory=StagewiseConfig)
    symbolize: SymbolizeConfig = Field(default_factory=SymbolizeConfig)
