from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

PYDANTIC_AVAILABLE = True

DEFAULT_X_TRAIN = "data/X_train.npy"
DEFAULT_X_TEST = "data/X_test.npy"
DEFAULT_Y_TRAIN = "data/Y_train_cat.npy"
DEFAULT_Y_TEST = "data/Y_test_cat.npy"


class RuntimeConfig(BaseModel):
    """Runtime settings shared across symkan workflows.

    Attributes:
        device: Preferred runtime device, usually ``auto``, ``cpu``, or
            ``cuda``.
        global_seed: Shared random seed for workflow-level reproducibility.
        baseline_seed: Separate seed used by baseline training paths.
        batch_size: Global batch-size override; ``0`` means caller-managed.
        quiet: Whether human-readable logs should be minimized.
        verbose: Whether detailed progress logs should be emitted.
    """

    model_config = ConfigDict(extra="forbid", arbitrary_types_allowed=True)

    device: str = "auto"
    global_seed: int = 123
    baseline_seed: int = 123
    batch_size: int = Field(default=0, ge=0)
    quiet: bool = False
    verbose: bool = False


class DataConfig(BaseModel):
    """Input dataset locations and loading behavior.

    Attributes:
        x_train: Training feature file path.
        x_test: Test feature file path.
        y_train: Training label file path.
        y_test: Test label file path.
        auto_fetch_mnist: Whether missing MNIST arrays may be auto-generated.
        allow_auto_fetch_outside_data_dir: Whether auto-fetch may write outside
            the repository ``data/`` directory.
        mnist_classes: Subset of MNIST classes to include.
    """

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
    """Model construction and baseline-fit settings.

    Attributes:
        inner_dim: Hidden width used by baseline model construction.
        grid: Spline grid size.
        k: Spline order.
        numeric_basis: Numeric frontend used by KAN edge functions.
        baseline_steps: Baseline fit steps.
        baseline_lr: Baseline fit learning rate.
        baseline_lamb: Baseline fit regularization strength.
        baseline_log: Baseline fit logging interval.
        top_k: Feature-selection width retained after attribution.
    """

    model_config = ConfigDict(extra="forbid", arbitrary_types_allowed=True)

    inner_dim: int = 16
    grid: int = 5
    k: int = 3
    numeric_basis: Literal["bspline", "radial_bf"] = "bspline"
    baseline_steps: int = 150
    baseline_lr: float = 0.02
    baseline_lamb: float = 1e-4
    baseline_log: int = 12
    top_k: int = Field(default=120, gt=0)


class LibraryConfig(BaseModel):
    """Symbolic library selection settings.

    Attributes:
        lib_preset: Named symbolic library preset such as ``layered`` or
            ``expressive``.
    """

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
    """Workflow switches that change the training path.

    Attributes:
        disable_stagewise_train: Whether to bypass stagewise training.
        e2e_steps: Optional end-to-end training steps when bypassing stagewise.
        e2e_lr: End-to-end learning rate.
        e2e_lamb: End-to-end regularization strength.
    """

    model_config = ConfigDict(extra="forbid", arbitrary_types_allowed=True)

    disable_stagewise_train: bool = False
    e2e_steps: int = 0
    e2e_lr: float = 0.0
    e2e_lamb: float = -1.0


class EvaluationConfig(BaseModel):
    """Evaluation and export validation settings.

    Attributes:
        validate_n_sample: Default sample count for formula validation.
    """

    model_config = ConfigDict(extra="forbid", arbitrary_types_allowed=True)

    validate_n_sample: int = Field(default=500, gt=0)


class TrainConfig(BaseModel):
    """Default ``safe_fit`` runtime configuration.

    Attributes:
        opt: Optimizer name.
        steps: Default fit steps.
        lr: Default learning rate.
        lamb: Default sparsity regularization coefficient.
        lamb_l1: Default L1 regularization coefficient.
        lamb_entropy: Default entropy regularization coefficient.
        batch: Default batch size, where ``-1`` means full-batch.
        update_grid: Whether spline grids may be updated during fitting.
        singularity_avoiding: Whether singularity avoidance is enabled.
        log: Logging interval.
    """

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
    """Runtime configuration consumed by ``stagewise_train``.

    Attributes:
        width: Stagewise model width.
        grid: Spline grid size.
        k: Spline order.
        seed: Stagewise model seed.
        lamb_schedule: Per-stage regularization schedule.
        lr_schedule: Per-stage learning-rate schedule.
        steps_per_stage: Training steps executed in each stage.
        batch_size: Optional stagewise batch-size override.
        prune_start_stage: First stage allowed to prune.
        target_edges: Desired edge count after stagewise pruning.
        prune_edge_threshold_init: Initial prune threshold.
        prune_edge_threshold_step: Threshold increment between prune attempts.
        prune_acc_drop_tol: Allowed accuracy drop after prune attempts.
        post_prune_ft_steps: Recovery fine-tune steps after pruning.
        sym_target_edges: Edge target used in readiness scoring.
        acc_weight: Accuracy weight used in readiness scoring.
        keep_topk_models: Number of top snapshots to retain.
        keep_full_snapshots: Whether full cloned models are retained per stage.
        use_disk_clone: Whether snapshot rollback uses checkpoint-based clones.
        clone_ckpt_path: Temporary prefix used by disk clones.
        use_validation: Whether validation-driven stagewise control is enabled.
        validation_ratio: Validation split ratio.
        validation_seed: Validation split seed.
        validation_min_samples: Minimum validation samples.
        adaptive_threshold: Whether prune thresholds adapt online.
        threshold_base_step: Base step size for adaptive thresholds.
        threshold_min: Minimum adaptive threshold.
        threshold_max: Maximum adaptive threshold.
        success_boost: Threshold growth factor after successful prune attempts.
        failure_penalty: Threshold backoff factor after failures.
        min_gain_threshold: Minimum edge gain treated as meaningful progress.
        max_prune_attempts: Maximum adaptive prune attempts per stage.
        adaptive_lamb: Whether lambda adapts with pruning progress.
        min_lamb_ratio: Minimum lambda ratio under adaptive lambda.
        max_lamb_ratio: Maximum lambda ratio under adaptive lambda.
        adaptive_ft: Whether post-prune fine-tune steps adapt online.
        min_ft_ratio: Minimum fine-tune ratio under adaptive FT.
        stage_early_stop: Whether stagewise early stopping is enabled.
        stage_early_stop_patience: Early-stop patience measured in stages.
        stage_early_stop_min_acc_gain: Minimum gain needed to reset patience.
        stage_early_stop_edge_buffer: Edge slack before early-stop triggers.
        guard_mode: Prune-guard strategy.
        verbose: Whether verbose stagewise logs are enabled.
    """

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
    """Runtime configuration consumed by ``symbolize_pipeline``.

    Attributes:
        symbolic_backend: Symbolic fitting backend selector.
        target_edges: Desired edge count before symbolic fixing.
        max_prune_rounds: Maximum prune rounds during symbolic preparation.
        lib: Optional flat symbolic library override.
        lib_hidden: Hidden-layer symbolic library override.
        lib_output: Output-layer symbolic library override.
        weight_simple: Simplicity preference used during function selection.
        finetune_steps: Fine-tune steps after each prune round.
        finetune_lr: Fine-tune learning rate after pruning.
        affine_finetune_steps: Final affine-heavy fine-tune steps.
        affine_finetune_lr_schedule: Learning-rate schedule for affine tuning.
        layerwise_finetune_steps: Layerwise fine-tune steps after each layer.
        layerwise_finetune_lr: Layerwise fine-tune learning rate.
        layerwise_finetune_lamb: Layerwise regularization strength.
        layerwise_use_validation: Whether layerwise FT uses validation metrics.
        layerwise_validation_ratio: Validation split ratio for layerwise FT.
        layerwise_validation_seed: Validation split seed for layerwise FT.
        layerwise_early_stop_patience: Layerwise FT early-stop patience.
        layerwise_early_stop_min_delta: Minimum validation gain treated as
            progress.
        layerwise_eval_interval: Validation interval during layerwise FT.
        layerwise_validation_n_sample: Sample count for formula validation.
        batch_size: Optional symbolize batch-size override.
        parallel_mode: Requested symbolic search parallel mode label.
        parallel_workers: Requested worker count.
        parallel_min_tasks: Minimum tasks before parallelism is considered.
        enable_input_compaction: Whether to compact active inputs.
        prune_collapse_floor: Minimum retained accuracy ratio after pruning.
        prune_eval_interval: Accuracy evaluation interval during pruning.
        prune_attr_sample_adaptive: Whether attribution sample count adapts.
        prune_attr_sample_min: Minimum adaptive attribution sample size.
        prune_attr_sample_max: Maximum adaptive attribution sample size.
        prune_threshold_start: Initial symbolic prune threshold.
        prune_threshold_end: Final symbolic prune threshold.
        prune_max_drop_ratio_per_round: Maximum edge drop ratio per round.
        prune_threshold_backoff: Threshold backoff ratio after collapse.
        prune_adaptive_threshold: Whether symbolic thresholds adapt online.
        prune_adaptive_step: Adaptive threshold step size.
        prune_adaptive_acc_drop_tol: Allowed accuracy drop in adaptive pruning.
        prune_adaptive_min_edges_gain: Minimum edge gain considered useful.
        prune_adaptive_low_gain_patience: Low-gain patience before stopping.
        heavy_ft_early_stop_patience: Early-stop patience for affine tuning.
        heavy_ft_early_stop_min_delta: Minimum gain for affine tuning progress.
        collect_timing: Whether timing diagnostics are collected.
        verbose: Whether verbose symbolic logs are enabled.
    """

    model_config = ConfigDict(extra="forbid", arbitrary_types_allowed=True)

    symbolic_backend: Literal["baseline", "icbr"] = "baseline"
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
    """Unified runtime configuration for symkan workflows.

    Attributes:
        runtime: Shared runtime options.
        data: Dataset input and loading options.
        model: Baseline model construction options.
        library: Symbolic library selection options.
        workflow: High-level workflow switches.
        evaluation: Evaluation defaults.
        train: Default ``safe_fit`` options.
        stagewise: Stagewise training options.
        symbolize: Symbolic pipeline options.
    """

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
