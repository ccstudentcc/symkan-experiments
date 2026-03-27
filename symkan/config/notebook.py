from __future__ import annotations

from typing import Any, Optional
import warnings

from symkan.config.exceptions import ConfigError
from symkan.config.loader import validate_app_config
from symkan.config.schema import AppConfig


def validated_app_config_update(config: AppConfig, **sections: Any) -> AppConfig:
    """Return a revalidated AppConfig after replacing selected sections.

    Args:
        config: Base application config to copy and update.
        **sections: Section payloads or Pydantic section models keyed by
            AppConfig field name, such as ``runtime`` or ``symbolize``.

    Returns:
        AppConfig: A fresh config validated through the canonical config loader.
    """
    payload = config.model_dump(mode="python")
    for name, section in sections.items():
        payload[name] = section.model_dump(mode="python") if hasattr(section, "model_dump") else section
    return validate_app_config(payload)


def _resolve_legacy_aliases(
    *,
    kind: str,
    values: dict[str, Any],
    aliases: dict[str, str],
) -> dict[str, Any]:
    """Rewrite supported legacy kwargs to canonical ``symkan`` names.

    Args:
        kind: Human-readable caller label used in warning and error messages.
        values: Raw kwargs provided by notebook-style callers.
        aliases: Mapping from legacy parameter names to canonical names.

    Returns:
        dict[str, Any]: Normalized kwargs keyed by canonical names.

    Raises:
        ConfigError: If both a legacy alias and its canonical name are present.
    """
    normalized = dict(values)
    used_aliases: list[tuple[str, str]] = []
    for legacy_name, canonical_name in aliases.items():
        if legacy_name not in normalized:
            continue
        if canonical_name in normalized:
            raise ConfigError(
                f"conflicting {kind} kwargs: got both legacy '{legacy_name}' and canonical '{canonical_name}'"
            )
        normalized[canonical_name] = normalized.pop(legacy_name)
        used_aliases.append((legacy_name, canonical_name))
    if used_aliases:
        alias_summary = ", ".join(f"{legacy!r}->{canonical!r}" for legacy, canonical in used_aliases)
        warnings.warn(
            f"{kind} kwargs used legacy aliases ({alias_summary}); prefer symkan canonical names",
            category=UserWarning,
            stacklevel=3,
        )
    return normalized


def _reject_explicit_and_legacy_conflicts(
    *,
    kind: str,
    explicit_values: dict[str, Any],
    legacy_values: dict[str, Any],
    aliases: dict[str, str],
) -> None:
    """Reject mixed canonical and legacy kwargs when both target one field.

    Args:
        kind: Human-readable caller label used in error messages.
        explicit_values: Canonical kwargs already bound in the function
            signature.
        legacy_values: Extra kwargs passed through ``**legacy_kwargs``.
        aliases: Mapping from legacy parameter names to canonical names.

    Raises:
        ConfigError: If a canonical field is explicitly set while its legacy
            alias is also present.
    """
    for legacy_name, canonical_name in aliases.items():
        if legacy_name not in legacy_values:
            continue
        if canonical_name not in explicit_values:
            continue
        explicit_value = explicit_values[canonical_name]
        if explicit_value is None:
            continue
        raise ConfigError(
            f"conflicting {kind} kwargs: got both legacy '{legacy_name}' and canonical '{canonical_name}'"
        )


def _reject_unknown_kwargs(*, kind: str, values: dict[str, Any], allowed: set[str]) -> None:
    """Fail fast on unsupported notebook compatibility kwargs.

    Args:
        kind: Human-readable caller label used in error messages.
        values: Normalized kwargs to validate.
        allowed: Canonical compatibility keys accepted by the helper.

    Raises:
        ConfigError: If unexpected kwargs remain after alias normalization.
    """
    unknown = sorted(key for key in values if key not in allowed)
    if unknown:
        raise ConfigError(f"unknown {kind} kwargs: {unknown}")


def build_stagewise_notebook_config(
    *,
    width: list[int],
    grid: int = 5,
    k: int = 3,
    numeric_basis: str = "bspline",
    seed: int = 123,
    lamb_schedule: tuple[float, ...] = (0.0, 1e-4, 3e-4),
    lr_schedule: tuple[float, ...] = (0.02, 0.012, 0.006),
    steps_per_stage: int = 70,
    batch_size: Optional[int] = None,
    prune_start_stage: int = 1,
    target_edges: int = 100,
    prune_edge_threshold_init: float = 0.005,
    prune_edge_threshold_step: float = 0.005,
    prune_acc_drop_tol: float = 0.08,
    post_prune_ft_steps: int = 40,
    sym_target_edges: int = 50,
    acc_weight: float = 0.4,
    keep_topk_models: int = 0,
    keep_full_snapshots: bool = False,
    use_disk_clone: bool = False,
    clone_ckpt_path: str = "_safe_copy_temp",
    use_validation: bool = False,
    validation_ratio: float = 0.0,
    validation_seed: Optional[int] = None,
    validation_min_samples: int = 10,
    adaptive_threshold: bool = False,
    threshold_base_step: float = 0.005,
    threshold_min: float = 0.001,
    threshold_max: float = 0.1,
    success_boost: float = 0.5,
    failure_penalty: float = 0.3,
    min_gain_threshold: int = 3,
    max_prune_attempts: int = 20,
    adaptive_lamb: bool = False,
    min_lamb_ratio: float = 0.3,
    max_lamb_ratio: float = 1.5,
    adaptive_ft: bool = False,
    min_ft_ratio: float = 0.3,
    stage_early_stop: bool = False,
    stage_early_stop_patience: int = 2,
    stage_early_stop_min_acc_gain: float = 0.002,
    stage_early_stop_edge_buffer: int = 0,
    guard_mode: str = "light",
    verbose: bool = True,
    runtime_device: str = "auto",
    runtime_global_seed: int = 123,
    runtime_quiet: bool = False,
    base_config: Optional[AppConfig] = None,
    **legacy_kwargs: Any,
) -> AppConfig:
    """Build an AppConfig for stagewise notebook-style function calls.

    This helper keeps the notebook's flat keyword-call style while normalizing
    arguments into the canonical ``AppConfig`` structure used by current
    ``symkan`` internals.

    Args:
        width: Stagewise model width, usually ``[input_dim, hidden_dim, output_dim]``.
        grid: KAN spline grid size.
        k: KAN spline order.
        numeric_basis: Numeric frontend used by KAN edges.
        seed: Stagewise model seed.
        lamb_schedule: Per-stage regularization schedule.
        lr_schedule: Per-stage learning-rate schedule.
        steps_per_stage: Training steps executed in each stage.
        batch_size: Canonical runtime and stagewise batch size override.
        prune_start_stage: First stage that enables edge pruning.
        target_edges: Stagewise pruning target.
        prune_edge_threshold_init: Initial prune threshold.
        prune_edge_threshold_step: Threshold increment between prune rounds.
        prune_acc_drop_tol: Allowed post-prune accuracy drop.
        post_prune_ft_steps: Fine-tune steps after each prune round.
        sym_target_edges: Symbolic readiness target edge count.
        acc_weight: Accuracy weight inside readiness scoring.
        keep_topk_models: Number of top snapshots to retain.
        keep_full_snapshots: Whether to keep full-stage snapshots.
        use_disk_clone: Whether to use disk-backed clone checkpoints.
        clone_ckpt_path: Temporary clone checkpoint path prefix.
        use_validation: Whether to create/use a validation split.
        validation_ratio: Validation split ratio.
        validation_seed: Validation split seed.
        validation_min_samples: Minimum validation sample count.
        adaptive_threshold: Whether to adapt prune thresholds online.
        threshold_base_step: Base threshold adjustment step.
        threshold_min: Minimum adaptive threshold.
        threshold_max: Maximum adaptive threshold.
        success_boost: Threshold boost after successful prune rounds.
        failure_penalty: Threshold penalty after failed prune rounds.
        min_gain_threshold: Minimum edges gained before considering a prune useful.
        max_prune_attempts: Maximum prune attempts per stage.
        adaptive_lamb: Whether to adapt lambda during stagewise training.
        min_lamb_ratio: Lower bound for adaptive lambda ratio.
        max_lamb_ratio: Upper bound for adaptive lambda ratio.
        adaptive_ft: Whether to adapt fine-tune steps online.
        min_ft_ratio: Lower bound for adaptive fine-tune ratio.
        stage_early_stop: Whether to enable stage-level early stop.
        stage_early_stop_patience: Early-stop patience in stages.
        stage_early_stop_min_acc_gain: Minimum accuracy gain to reset patience.
        stage_early_stop_edge_buffer: Extra edge buffer before stopping early.
        guard_mode: Canonical stagewise guard mode.
        verbose: Whether to enable verbose stagewise logging.
        runtime_device: Canonical runtime device override.
        runtime_global_seed: Canonical runtime global seed override.
        runtime_quiet: Canonical runtime quiet flag.
        base_config: Optional base config to update instead of starting from defaults.
        **legacy_kwargs: Legacy notebook aliases kept only as compatibility
            fallbacks. Canonical names are preferred and conflicting dual use
            raises ``ConfigError``.

    Returns:
        AppConfig: A validated config ready for ``stagewise_train``.

    Raises:
        ConfigError: If unknown legacy kwargs are provided or if legacy and
            canonical names conflict.
    """
    stagewise_aliases = {
        "batch": "batch_size",
        "device": "runtime_device",
        "global_seed": "runtime_global_seed",
        "quiet": "runtime_quiet",
        "basis": "numeric_basis",
        "stage_guard_mode": "guard_mode",
        "topk_models": "keep_topk_models",
        "full_snapshots": "keep_full_snapshots",
        "disk_clone": "use_disk_clone",
        "clone_temp_path": "clone_ckpt_path",
        "validation_min": "validation_min_samples",
        "early_stop_patience": "stage_early_stop_patience",
        "early_stop_min_acc_gain": "stage_early_stop_min_acc_gain",
        "early_stop_edge_buffer": "stage_early_stop_edge_buffer",
    }
    _reject_explicit_and_legacy_conflicts(
        kind="stagewise notebook",
        explicit_values={
            "batch_size": batch_size if batch_size is not None else None,
            "runtime_device": runtime_device if runtime_device != "auto" else None,
            "runtime_global_seed": runtime_global_seed if runtime_global_seed != 123 else None,
            "runtime_quiet": runtime_quiet if runtime_quiet else None,
            "numeric_basis": numeric_basis if numeric_basis != "bspline" else None,
            "guard_mode": guard_mode if guard_mode != "light" else None,
            "keep_topk_models": keep_topk_models if keep_topk_models != 0 else None,
            "keep_full_snapshots": keep_full_snapshots if keep_full_snapshots else None,
            "use_disk_clone": use_disk_clone if use_disk_clone else None,
            "clone_ckpt_path": clone_ckpt_path if clone_ckpt_path != "_safe_copy_temp" else None,
            "validation_min_samples": validation_min_samples if validation_min_samples != 10 else None,
            "stage_early_stop_patience": stage_early_stop_patience if stage_early_stop_patience != 2 else None,
            "stage_early_stop_min_acc_gain": (
                stage_early_stop_min_acc_gain if stage_early_stop_min_acc_gain != 0.002 else None
            ),
            "stage_early_stop_edge_buffer": stage_early_stop_edge_buffer if stage_early_stop_edge_buffer != 0 else None,
        },
        legacy_values=legacy_kwargs,
        aliases=stagewise_aliases,
    )
    legacy_kwargs = _resolve_legacy_aliases(
        kind="stagewise notebook",
        values=legacy_kwargs,
        aliases=stagewise_aliases,
    )
    _reject_unknown_kwargs(
        kind="stagewise notebook",
        values=legacy_kwargs,
        allowed={
            "batch_size",
            "runtime_device",
            "runtime_global_seed",
            "runtime_quiet",
            "numeric_basis",
            "guard_mode",
            "keep_topk_models",
            "keep_full_snapshots",
            "use_disk_clone",
            "clone_ckpt_path",
            "validation_min_samples",
            "stage_early_stop_patience",
            "stage_early_stop_min_acc_gain",
            "stage_early_stop_edge_buffer",
        },
    )
    if "batch_size" in legacy_kwargs:
        batch_size = legacy_kwargs["batch_size"]
    if "runtime_device" in legacy_kwargs:
        runtime_device = legacy_kwargs["runtime_device"]
    if "runtime_global_seed" in legacy_kwargs:
        runtime_global_seed = legacy_kwargs["runtime_global_seed"]
    if "runtime_quiet" in legacy_kwargs:
        runtime_quiet = legacy_kwargs["runtime_quiet"]
    if "numeric_basis" in legacy_kwargs:
        numeric_basis = legacy_kwargs["numeric_basis"]
    if "guard_mode" in legacy_kwargs:
        guard_mode = legacy_kwargs["guard_mode"]
    if "keep_topk_models" in legacy_kwargs:
        keep_topk_models = legacy_kwargs["keep_topk_models"]
    if "keep_full_snapshots" in legacy_kwargs:
        keep_full_snapshots = legacy_kwargs["keep_full_snapshots"]
    if "use_disk_clone" in legacy_kwargs:
        use_disk_clone = legacy_kwargs["use_disk_clone"]
    if "clone_ckpt_path" in legacy_kwargs:
        clone_ckpt_path = legacy_kwargs["clone_ckpt_path"]
    if "validation_min_samples" in legacy_kwargs:
        validation_min_samples = legacy_kwargs["validation_min_samples"]
    if "stage_early_stop_patience" in legacy_kwargs:
        stage_early_stop_patience = legacy_kwargs["stage_early_stop_patience"]
    if "stage_early_stop_min_acc_gain" in legacy_kwargs:
        stage_early_stop_min_acc_gain = legacy_kwargs["stage_early_stop_min_acc_gain"]
    if "stage_early_stop_edge_buffer" in legacy_kwargs:
        stage_early_stop_edge_buffer = legacy_kwargs["stage_early_stop_edge_buffer"]

    config = base_config.model_copy(deep=True) if base_config is not None else AppConfig()
    width_list = [int(item) for item in width]
    model_update = {
        "inner_dim": int(width_list[1]) if len(width_list) >= 2 else config.model.inner_dim,
        "grid": int(grid),
        "k": int(k),
        "numeric_basis": str(numeric_basis),
    }
    runtime_update = {
        "device": runtime_device,
        "global_seed": int(runtime_global_seed),
        "batch_size": int(batch_size) if batch_size is not None else config.runtime.batch_size,
        "quiet": bool(runtime_quiet),
        "verbose": bool(verbose and not runtime_quiet),
    }
    stagewise_update = {
        "width": width_list,
        "grid": int(grid),
        "k": int(k),
        "seed": int(seed),
        "lamb_schedule": tuple(float(item) for item in lamb_schedule),
        "lr_schedule": tuple(float(item) for item in lr_schedule),
        "steps_per_stage": int(steps_per_stage),
        "batch_size": int(batch_size) if batch_size is not None else None,
        "prune_start_stage": int(prune_start_stage),
        "target_edges": int(target_edges),
        "prune_edge_threshold_init": float(prune_edge_threshold_init),
        "prune_edge_threshold_step": float(prune_edge_threshold_step),
        "prune_acc_drop_tol": float(prune_acc_drop_tol),
        "post_prune_ft_steps": int(post_prune_ft_steps),
        "sym_target_edges": int(sym_target_edges),
        "acc_weight": float(acc_weight),
        "keep_topk_models": int(keep_topk_models),
        "keep_full_snapshots": bool(keep_full_snapshots),
        "use_disk_clone": bool(use_disk_clone),
        "clone_ckpt_path": clone_ckpt_path,
        "use_validation": bool(use_validation),
        "validation_ratio": float(validation_ratio),
        "validation_seed": validation_seed,
        "validation_min_samples": int(validation_min_samples),
        "adaptive_threshold": bool(adaptive_threshold),
        "threshold_base_step": float(threshold_base_step),
        "threshold_min": float(threshold_min),
        "threshold_max": float(threshold_max),
        "success_boost": float(success_boost),
        "failure_penalty": float(failure_penalty),
        "min_gain_threshold": int(min_gain_threshold),
        "max_prune_attempts": int(max_prune_attempts),
        "adaptive_lamb": bool(adaptive_lamb),
        "min_lamb_ratio": float(min_lamb_ratio),
        "max_lamb_ratio": float(max_lamb_ratio),
        "adaptive_ft": bool(adaptive_ft),
        "min_ft_ratio": float(min_ft_ratio),
        "stage_early_stop": bool(stage_early_stop),
        "stage_early_stop_patience": int(stage_early_stop_patience),
        "stage_early_stop_min_acc_gain": float(stage_early_stop_min_acc_gain),
        "stage_early_stop_edge_buffer": int(stage_early_stop_edge_buffer),
        "guard_mode": guard_mode,
        "verbose": bool(verbose),
    }
    return validated_app_config_update(
        config,
        runtime=runtime_update,
        model=model_update,
        stagewise=stagewise_update,
    )


def build_symbolize_notebook_config(
    *,
    target_edges: int = 60,
    max_prune_rounds: int = 40,
    lib: Optional[list[Any]] = None,
    lib_hidden: Optional[list[Any]] = None,
    lib_output: Optional[list[Any]] = None,
    weight_simple: float = 0.0,
    finetune_steps: int = 30,
    finetune_lr: float = 0.005,
    affine_finetune_steps: int = 600,
    affine_finetune_lr_schedule: Optional[list[float]] = None,
    layerwise_finetune_steps: int = 60,
    layerwise_finetune_lr: float = 0.005,
    layerwise_finetune_lamb: float = 1e-5,
    layerwise_use_validation: bool = True,
    layerwise_validation_ratio: float = 0.15,
    layerwise_validation_seed: Optional[int] = None,
    layerwise_early_stop_patience: int = 2,
    layerwise_early_stop_min_delta: float = 1e-3,
    layerwise_eval_interval: int = 20,
    layerwise_validation_n_sample: int = 300,
    batch_size: Optional[int] = None,
    parallel_mode: str = "auto",
    parallel_workers: Optional[int] = None,
    parallel_min_tasks: int = 16,
    enable_input_compaction: bool = True,
    prune_collapse_floor: float = 0.6,
    prune_eval_interval: int = 1,
    prune_attr_sample_adaptive: bool = False,
    prune_attr_sample_min: int = 512,
    prune_attr_sample_max: int = 2048,
    prune_threshold_start: float = 0.02,
    prune_threshold_end: float = 0.03,
    prune_max_drop_ratio_per_round: float = 1.0,
    prune_threshold_backoff: float = 0.7,
    prune_adaptive_threshold: bool = False,
    prune_adaptive_step: float = 0.0,
    prune_adaptive_acc_drop_tol: float = 0.02,
    prune_adaptive_min_edges_gain: int = 1,
    prune_adaptive_low_gain_patience: int = 4,
    heavy_ft_early_stop_patience: int = 0,
    heavy_ft_early_stop_min_delta: float = 1e-4,
    collect_timing: bool = True,
    verbose: bool = True,
    runtime_device: str = "auto",
    runtime_global_seed: int = 123,
    runtime_quiet: bool = False,
    numeric_basis: str = "bspline",
    evaluation_validate_n_sample: Optional[int] = None,
    base_config: Optional[AppConfig] = None,
    **legacy_kwargs: Any,
) -> AppConfig:
    """Build an AppConfig for symbolize notebook-style function calls.

    This helper preserves the notebook's flat function-parameter style while
    translating kwargs into the canonical ``AppConfig`` sections used by the
    current symbolic pipeline.

    Args:
        target_edges: Symbolic pruning target edge count.
        max_prune_rounds: Maximum symbolic prune rounds.
        lib: Optional flat symbolic library override.
        lib_hidden: Hidden-layer symbolic library override.
        lib_output: Output-layer symbolic library override.
        weight_simple: Simplicity weight for symbolic function selection.
        finetune_steps: Sparse fine-tuning steps before symbolic export.
        finetune_lr: Sparse fine-tuning learning rate.
        affine_finetune_steps: Affine refinement steps after symbolic fixing.
        affine_finetune_lr_schedule: Affine refinement learning-rate schedule.
        layerwise_finetune_steps: Layerwise fine-tune steps.
        layerwise_finetune_lr: Layerwise fine-tune learning rate.
        layerwise_finetune_lamb: Layerwise fine-tune regularization weight.
        layerwise_use_validation: Whether layerwise tuning uses validation.
        layerwise_validation_ratio: Validation split ratio for layerwise tuning.
        layerwise_validation_seed: Validation split seed for layerwise tuning.
        layerwise_early_stop_patience: Layerwise early-stop patience.
        layerwise_early_stop_min_delta: Minimum layerwise improvement threshold.
        layerwise_eval_interval: Layerwise evaluation interval.
        layerwise_validation_n_sample: Validation sample count for layerwise tuning.
        batch_size: Canonical runtime and symbolize batch size override.
        parallel_mode: Canonical requested parallel mode label.
        parallel_workers: Requested parallel worker count.
        parallel_min_tasks: Minimum tasks required before parallel execution.
        enable_input_compaction: Whether symbolic input compaction is enabled.
        prune_collapse_floor: Minimum allowed collapse ratio during pruning.
        prune_eval_interval: Symbolic prune evaluation interval.
        prune_attr_sample_adaptive: Whether prune attribution sampling is adaptive.
        prune_attr_sample_min: Minimum adaptive attribution sample size.
        prune_attr_sample_max: Maximum adaptive attribution sample size.
        prune_threshold_start: Start threshold for symbolic pruning.
        prune_threshold_end: End threshold for symbolic pruning.
        prune_max_drop_ratio_per_round: Maximum drop ratio allowed per round.
        prune_threshold_backoff: Threshold backoff ratio after failure.
        prune_adaptive_threshold: Whether prune threshold adapts online.
        prune_adaptive_step: Adaptive threshold step size.
        prune_adaptive_acc_drop_tol: Accuracy-drop tolerance in adaptive pruning.
        prune_adaptive_min_edges_gain: Minimum edge gain to treat a round as useful.
        prune_adaptive_low_gain_patience: Patience for low-gain prune rounds.
        heavy_ft_early_stop_patience: Heavy fine-tune early-stop patience.
        heavy_ft_early_stop_min_delta: Heavy fine-tune early-stop min delta.
        collect_timing: Whether timing diagnostics are collected.
        verbose: Whether to enable verbose symbolic logging.
        runtime_device: Canonical runtime device override.
        runtime_global_seed: Canonical runtime global seed override.
        runtime_quiet: Canonical runtime quiet flag.
        numeric_basis: Numeric frontend used by KAN edges.
        evaluation_validate_n_sample: Canonical evaluation sample-count override.
        base_config: Optional base config to update instead of starting from defaults.
        **legacy_kwargs: Legacy notebook aliases kept only as compatibility
            fallbacks. Canonical names are preferred and conflicting dual use
            raises ``ConfigError``.

    Returns:
        AppConfig: A validated config ready for ``symbolize_pipeline``.

    Raises:
        ConfigError: If unknown legacy kwargs are provided or if legacy and
            canonical names conflict.
    """
    symbolize_aliases = {
        "batch": "batch_size",
        "device": "runtime_device",
        "global_seed": "runtime_global_seed",
        "quiet": "runtime_quiet",
        "basis": "numeric_basis",
        "input_compaction": "enable_input_compaction",
        "use_validation": "layerwise_use_validation",
        "validation_ratio": "layerwise_validation_ratio",
        "validation_seed": "layerwise_validation_seed",
        "early_stop_patience": "layerwise_early_stop_patience",
        "early_stop_min_delta": "layerwise_early_stop_min_delta",
        "eval_interval": "layerwise_eval_interval",
        "validation_n_sample": "layerwise_validation_n_sample",
        "attr_sample_adaptive": "prune_attr_sample_adaptive",
        "attr_sample_min": "prune_attr_sample_min",
        "attr_sample_max": "prune_attr_sample_max",
        "heavy_ft_patience": "heavy_ft_early_stop_patience",
        "heavy_ft_min_delta": "heavy_ft_early_stop_min_delta",
    }
    _reject_explicit_and_legacy_conflicts(
        kind="symbolize notebook",
        explicit_values={
            "batch_size": batch_size if batch_size is not None else None,
            "runtime_device": runtime_device if runtime_device != "auto" else None,
            "runtime_global_seed": runtime_global_seed if runtime_global_seed != 123 else None,
            "runtime_quiet": runtime_quiet if runtime_quiet else None,
            "numeric_basis": numeric_basis if numeric_basis != "bspline" else None,
            "enable_input_compaction": enable_input_compaction if enable_input_compaction is not True else None,
            "layerwise_use_validation": layerwise_use_validation if layerwise_use_validation is not True else None,
            "layerwise_validation_ratio": (
                layerwise_validation_ratio if layerwise_validation_ratio != 0.15 else None
            ),
            "layerwise_validation_seed": layerwise_validation_seed,
            "layerwise_early_stop_patience": (
                layerwise_early_stop_patience if layerwise_early_stop_patience != 2 else None
            ),
            "layerwise_early_stop_min_delta": (
                layerwise_early_stop_min_delta if layerwise_early_stop_min_delta != 1e-3 else None
            ),
            "layerwise_eval_interval": layerwise_eval_interval if layerwise_eval_interval != 20 else None,
            "layerwise_validation_n_sample": (
                layerwise_validation_n_sample if layerwise_validation_n_sample != 300 else None
            ),
            "prune_attr_sample_adaptive": prune_attr_sample_adaptive if prune_attr_sample_adaptive else None,
            "prune_attr_sample_min": prune_attr_sample_min if prune_attr_sample_min != 512 else None,
            "prune_attr_sample_max": prune_attr_sample_max if prune_attr_sample_max != 2048 else None,
            "heavy_ft_early_stop_patience": (
                heavy_ft_early_stop_patience if heavy_ft_early_stop_patience != 0 else None
            ),
            "heavy_ft_early_stop_min_delta": (
                heavy_ft_early_stop_min_delta if heavy_ft_early_stop_min_delta != 1e-4 else None
            ),
        },
        legacy_values=legacy_kwargs,
        aliases=symbolize_aliases,
    )
    legacy_kwargs = _resolve_legacy_aliases(
        kind="symbolize notebook",
        values=legacy_kwargs,
        aliases=symbolize_aliases,
    )
    _reject_unknown_kwargs(
        kind="symbolize notebook",
        values=legacy_kwargs,
        allowed={
            "batch_size",
            "runtime_device",
            "runtime_global_seed",
            "runtime_quiet",
            "numeric_basis",
            "enable_input_compaction",
            "layerwise_use_validation",
            "layerwise_validation_ratio",
            "layerwise_validation_seed",
            "layerwise_early_stop_patience",
            "layerwise_early_stop_min_delta",
            "layerwise_eval_interval",
            "layerwise_validation_n_sample",
            "prune_attr_sample_adaptive",
            "prune_attr_sample_min",
            "prune_attr_sample_max",
            "heavy_ft_early_stop_patience",
            "heavy_ft_early_stop_min_delta",
        },
    )
    if "batch_size" in legacy_kwargs:
        batch_size = legacy_kwargs["batch_size"]
    if "runtime_device" in legacy_kwargs:
        runtime_device = legacy_kwargs["runtime_device"]
    if "runtime_global_seed" in legacy_kwargs:
        runtime_global_seed = legacy_kwargs["runtime_global_seed"]
    if "runtime_quiet" in legacy_kwargs:
        runtime_quiet = legacy_kwargs["runtime_quiet"]
    if "numeric_basis" in legacy_kwargs:
        numeric_basis = legacy_kwargs["numeric_basis"]
    if "enable_input_compaction" in legacy_kwargs:
        enable_input_compaction = legacy_kwargs["enable_input_compaction"]
    if "layerwise_use_validation" in legacy_kwargs:
        layerwise_use_validation = legacy_kwargs["layerwise_use_validation"]
    if "layerwise_validation_ratio" in legacy_kwargs:
        layerwise_validation_ratio = legacy_kwargs["layerwise_validation_ratio"]
    if "layerwise_validation_seed" in legacy_kwargs:
        layerwise_validation_seed = legacy_kwargs["layerwise_validation_seed"]
    if "layerwise_early_stop_patience" in legacy_kwargs:
        layerwise_early_stop_patience = legacy_kwargs["layerwise_early_stop_patience"]
    if "layerwise_early_stop_min_delta" in legacy_kwargs:
        layerwise_early_stop_min_delta = legacy_kwargs["layerwise_early_stop_min_delta"]
    if "layerwise_eval_interval" in legacy_kwargs:
        layerwise_eval_interval = legacy_kwargs["layerwise_eval_interval"]
    if "layerwise_validation_n_sample" in legacy_kwargs:
        layerwise_validation_n_sample = legacy_kwargs["layerwise_validation_n_sample"]
    if "prune_attr_sample_adaptive" in legacy_kwargs:
        prune_attr_sample_adaptive = legacy_kwargs["prune_attr_sample_adaptive"]
    if "prune_attr_sample_min" in legacy_kwargs:
        prune_attr_sample_min = legacy_kwargs["prune_attr_sample_min"]
    if "prune_attr_sample_max" in legacy_kwargs:
        prune_attr_sample_max = legacy_kwargs["prune_attr_sample_max"]
    if "heavy_ft_early_stop_patience" in legacy_kwargs:
        heavy_ft_early_stop_patience = legacy_kwargs["heavy_ft_early_stop_patience"]
    if "heavy_ft_early_stop_min_delta" in legacy_kwargs:
        heavy_ft_early_stop_min_delta = legacy_kwargs["heavy_ft_early_stop_min_delta"]

    config = base_config.model_copy(deep=True) if base_config is not None else AppConfig()
    runtime_update = {
        "device": runtime_device,
        "global_seed": int(runtime_global_seed),
        "batch_size": int(batch_size) if batch_size is not None else config.runtime.batch_size,
        "quiet": bool(runtime_quiet),
        "verbose": bool(verbose and not runtime_quiet),
    }
    evaluation_update = {
        "validate_n_sample": (
            int(evaluation_validate_n_sample)
            if evaluation_validate_n_sample is not None
            else config.evaluation.validate_n_sample
        )
    }
    model_update = {
        "numeric_basis": str(numeric_basis),
    }
    symbolize_update = {
        "target_edges": int(target_edges),
        "max_prune_rounds": int(max_prune_rounds),
        "lib": lib,
        "lib_hidden": lib_hidden,
        "lib_output": lib_output,
        "weight_simple": float(weight_simple),
        "finetune_steps": int(finetune_steps),
        "finetune_lr": float(finetune_lr),
        "affine_finetune_steps": int(affine_finetune_steps),
        "affine_finetune_lr_schedule": (
            [float(item) for item in affine_finetune_lr_schedule]
            if affine_finetune_lr_schedule is not None
            else None
        ),
        "layerwise_finetune_steps": int(layerwise_finetune_steps),
        "layerwise_finetune_lr": float(layerwise_finetune_lr),
        "layerwise_finetune_lamb": float(layerwise_finetune_lamb),
        "layerwise_use_validation": bool(layerwise_use_validation),
        "layerwise_validation_ratio": float(layerwise_validation_ratio),
        "layerwise_validation_seed": layerwise_validation_seed,
        "layerwise_early_stop_patience": int(layerwise_early_stop_patience),
        "layerwise_early_stop_min_delta": float(layerwise_early_stop_min_delta),
        "layerwise_eval_interval": int(layerwise_eval_interval),
        "layerwise_validation_n_sample": int(layerwise_validation_n_sample),
        "batch_size": int(batch_size) if batch_size is not None else None,
        "parallel_mode": parallel_mode,
        "parallel_workers": int(parallel_workers) if parallel_workers is not None else None,
        "parallel_min_tasks": int(parallel_min_tasks),
        "enable_input_compaction": bool(enable_input_compaction),
        "prune_collapse_floor": float(prune_collapse_floor),
        "prune_eval_interval": int(prune_eval_interval),
        "prune_attr_sample_adaptive": bool(prune_attr_sample_adaptive),
        "prune_attr_sample_min": int(prune_attr_sample_min),
        "prune_attr_sample_max": int(prune_attr_sample_max),
        "prune_threshold_start": float(prune_threshold_start),
        "prune_threshold_end": float(prune_threshold_end),
        "prune_max_drop_ratio_per_round": float(prune_max_drop_ratio_per_round),
        "prune_threshold_backoff": float(prune_threshold_backoff),
        "prune_adaptive_threshold": bool(prune_adaptive_threshold),
        "prune_adaptive_step": float(prune_adaptive_step),
        "prune_adaptive_acc_drop_tol": float(prune_adaptive_acc_drop_tol),
        "prune_adaptive_min_edges_gain": int(prune_adaptive_min_edges_gain),
        "prune_adaptive_low_gain_patience": int(prune_adaptive_low_gain_patience),
        "heavy_ft_early_stop_patience": int(heavy_ft_early_stop_patience),
        "heavy_ft_early_stop_min_delta": float(heavy_ft_early_stop_min_delta),
        "collect_timing": bool(collect_timing),
        "verbose": bool(verbose),
    }
    return validated_app_config_update(
        config,
        runtime=runtime_update,
        model=model_update,
        evaluation=evaluation_update,
        symbolize=symbolize_update,
    )
