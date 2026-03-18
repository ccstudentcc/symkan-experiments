from __future__ import annotations

from typing import Any, Optional

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
    batch_size: int = 0
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
    top_k: int = 120


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

    validate_n_sample: int = 500


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
    stage_early_stop: bool = False
    stage_early_stop_patience: int = 2
    stage_early_stop_min_acc_gain: float = 0.002
    stage_early_stop_edge_buffer: int = 0
    verbose: bool = True


class SymbolizeConfig(BaseModel):
    """symbolize_pipeline runtime configuration."""

    model_config = ConfigDict(extra="forbid", arbitrary_types_allowed=True)

    target_edges: int = 60
    max_prune_rounds: int = 40
    lib: Optional[list[Any]] = None
    lib_hidden: Optional[list[Any]] = None
    lib_output: Optional[list[Any]] = None
    weight_simple: float = 0.0
    finetune_steps: int = 30
    finetune_lr: float = 0.005
    affine_finetune_steps: int = 600
    affine_finetune_lr_schedule: Optional[list[float]] = None
    layerwise_finetune_steps: int = 60
    layerwise_finetune_lr: float = 0.005
    layerwise_finetune_lamb: float = 1e-5
    layerwise_use_validation: bool = True
    layerwise_validation_ratio: float = 0.15
    layerwise_validation_seed: Optional[int] = None
    layerwise_early_stop_patience: int = 2
    layerwise_early_stop_min_delta: float = 1e-3
    layerwise_eval_interval: int = 20
    layerwise_validation_n_sample: int = 300
    batch_size: Optional[int] = None
    parallel_mode: str = "auto"
    parallel_workers: Optional[int] = None
    parallel_min_tasks: int = 16
    enable_input_compaction: bool = True
    prune_collapse_floor: float = 0.6
    prune_eval_interval: int = 1
    prune_attr_sample_adaptive: bool = False
    prune_attr_sample_min: int = 512
    prune_attr_sample_max: int = 2048
    prune_threshold_start: float = 0.02
    prune_threshold_end: float = 0.03
    prune_max_drop_ratio_per_round: float = 1.0
    prune_threshold_backoff: float = 0.7
    prune_adaptive_threshold: bool = False
    prune_adaptive_step: float = 0.0
    prune_adaptive_acc_drop_tol: float = 0.02
    prune_adaptive_min_edges_gain: int = 1
    prune_adaptive_low_gain_patience: int = 4
    heavy_ft_early_stop_patience: int = 0
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
