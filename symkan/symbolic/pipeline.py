"""Symkan's main symbolic pipeline.

This module advances a trained KAN model into symbolic expression export,
including progressive pruning, optional input compaction, layer-wise symbolic
fitting, and final refinement.
"""

import copy
import time
from typing import Optional

import numpy as np
import pandas as pd
import torch
from kan.icbr import _run_auto_symbolic_icbr_with_models, auto_symbolic_icbr

from symkan.core import get_n_edge, model_acc_ds, safe_fit_report
from symkan.config import AppConfig
from symkan.core.train import format_fit_failure
from symkan.core.runtime import default_batch_size
from symkan.io import clone_model
from symkan.pruning import safe_attribute
from .compact import compact_inputs_for_symbolic
from .library import LIB_HIDDEN, LIB_OUTPUT, collect_valid_formulas, register_custom_functions
from .search import fast_symbolic


def _fit_or_raise(context: str, **fit_kwargs):
    """Run guarded fitting and raise on failure.

    Args:
        context: Human-readable stage label for error messages.
        **fit_kwargs: Keyword arguments forwarded to ``safe_fit_report``.

    Returns:
        dict: Raw fit result payload.

    Raises:
        RuntimeError: If guarded fitting fails.
    """
    report = safe_fit_report(**fit_kwargs)
    if report.success:
        return report.result
    raise RuntimeError(format_fit_failure(report, context=context))


def _fit_or_error(context: str, **fit_kwargs):
    """Run guarded fitting and return a formatted error instead of raising.

    Args:
        context: Human-readable stage label for error messages.
        **fit_kwargs: Keyword arguments forwarded to ``safe_fit_report``.

    Returns:
        tuple[dict | None, str | None]: Fit result and optional formatted error.
    """
    report = safe_fit_report(**fit_kwargs)
    if report.success:
        return report.result, None
    return None, format_fit_failure(report, context=context)


def _set_abort_reason(
    timing: dict[str, object],
    *,
    stage: str,
    reason: str,
    error_type: Optional[str] = None,
) -> None:
    """Record the stage and reason that caused the pipeline to abort.

    Args:
        timing: Timing/diagnostic dictionary updated in place.
        stage: Pipeline stage name.
        reason: Human-readable abort reason.
        error_type: Optional exception type name.
    """
    timing["abort_stage"] = stage
    timing["abort_reason"] = str(reason)
    if error_type is not None:
        timing["abort_error_type"] = error_type


def _append_pipeline_warning(
    warnings_list: list[dict[str, object]],
    *,
    code: str,
    stage: str,
    message: str,
    error_type: Optional[str] = None,
    **extra: object,
) -> None:
    """Append a structured warning record to pipeline diagnostics.

    Args:
        warnings_list: Warning list updated in place.
        code: Stable warning code.
        stage: Pipeline stage name.
        message: Human-readable warning message.
        error_type: Optional exception type name.
        **extra: Additional serializable fields to attach.
    """
    warning: dict[str, object] = {
        "code": code,
        "stage": stage,
        "message": str(message),
    }
    if error_type is not None:
        warning["error_type"] = error_type
    for key, value in extra.items():
        if value is not None:
            warning[key] = value
    warnings_list.append(warning)


def _count_effective_edges(work):
    """Count effective active edges across activation and symbolic masks.

    Args:
        work: KAN model-like object with activation and symbolic masks.

    Returns:
        int: Effective active edge count across all layers.
    """
    depth = len(work.width_in) - 1
    total = 0

    for l in range(depth):
        act_mask = None
        sym_mask = None
        sym_name_mask = None

        try:
            act_mask = torch.as_tensor(work.act_fun[l].mask) != 0
        except Exception:
            act_mask = None

        try:
            sym_mask = torch.as_tensor(work.symbolic_fun[l].mask) != 0
        except Exception:
            sym_mask = None

        try:
            funs_name = getattr(work.symbolic_fun[l], "funs_name", None)
            if funs_name is not None:
                sym_name_mask = torch.as_tensor(
                    [[str(fun_name) != "0" for fun_name in row] for row in funs_name],
                    dtype=torch.bool,
                )
        except Exception:
            sym_name_mask = None

        if act_mask is None and sym_mask is None:
            continue

        if act_mask is None:
            assert sym_mask is not None
            if sym_name_mask is not None:
                if sym_name_mask.shape != sym_mask.shape and sym_name_mask.T.shape == sym_mask.shape:
                    sym_name_mask = sym_name_mask.T
                if sym_name_mask.shape == sym_mask.shape:
                    sym_mask = sym_mask & sym_name_mask
            total += int(sym_mask.sum().item())
            continue

        if sym_mask is None:
            assert act_mask is not None
            total += int(act_mask.sum().item())
            continue

        if sym_mask.shape != act_mask.shape and sym_mask.T.shape == act_mask.shape:
            sym_mask = sym_mask.T
        if sym_name_mask is not None and sym_name_mask.shape != act_mask.shape and sym_name_mask.T.shape == act_mask.shape:
            sym_name_mask = sym_name_mask.T

        if sym_mask.shape == act_mask.shape:
            if sym_name_mask is not None and sym_name_mask.shape == sym_mask.shape:
                sym_mask = sym_mask & sym_name_mask
            total += int((act_mask | sym_mask).sum().item())
        else:
            total += int(act_mask.sum().item())

    return total


def _resolve_symbolic_backend(symbolize_config) -> str:
    """Resolve the symbolic backend name without requiring schema changes.

    Args:
        symbolize_config: ``config.symbolize``-like object.

    Returns:
        str: Canonical backend label.

    Raises:
        ValueError: If an unsupported backend label is requested.
    """
    raw_backend = getattr(symbolize_config, "symbolic_backend", None)
    if raw_backend is None:
        raw_backend = getattr(symbolize_config, "backend", "baseline")
    backend = str(raw_backend).strip().lower() if raw_backend is not None else "baseline"
    if backend in {"", "baseline", "default", "fast_symbolic", "fast", "layered", "layerwise"}:
        return "baseline"
    if backend in {"icbr", "icbr_full"}:
        return "icbr"
    raise ValueError(f"Unsupported symbolic backend: {raw_backend}")


def _resolve_icbr_symbolic_lib(lib, lib_hidden, lib_output):
    """Build the flat symbolic library expected by the ICBR backend.

    The baseline backend keeps the existing layered library semantics. ICBR only
    accepts a flat library, so we preserve ``lib`` when explicitly provided and
    otherwise merge the hidden/output libraries in first-seen order.

    Args:
        lib: Optional flat symbolic library override.
        lib_hidden: Hidden-layer symbolic library override.
        lib_output: Output-layer symbolic library override.

    Returns:
        list: Flat library passed to ``kan.icbr.auto_symbolic_icbr``.
    """
    if lib is not None:
        return list(lib)

    merged = []
    for source in (lib_hidden or LIB_HIDDEN, lib_output or LIB_OUTPUT):
        for item in source:
            if item not in merged:
                merged.append(item)
    return merged


def _copy_timing_payload(timing: dict[str, object]) -> dict[str, object]:
    """Create a shallow-structured copy for timing payload reuse."""
    copied: dict[str, object] = {}
    for key, value in timing.items():
        if isinstance(value, list):
            copied[key] = [dict(item) if isinstance(item, dict) else copy.deepcopy(item) for item in value]
        elif isinstance(value, dict):
            copied[key] = dict(value)
        else:
            copied[key] = copy.deepcopy(value)
    return copied


def _resolve_symbolize_options(config: AppConfig) -> dict[str, object]:
    """Extract symbolize options once so prepare/finalize share one boundary."""
    symbolize_config = config.symbolize
    options: dict[str, object] = {
        "target_edges": symbolize_config.target_edges,
        "max_prune_rounds": symbolize_config.max_prune_rounds,
        "lib": symbolize_config.lib,
        "lib_hidden": symbolize_config.lib_hidden,
        "lib_output": symbolize_config.lib_output,
        "weight_simple": symbolize_config.weight_simple,
        "finetune_steps": symbolize_config.finetune_steps,
        "finetune_lr": symbolize_config.finetune_lr,
        "affine_finetune_steps": symbolize_config.affine_finetune_steps,
        "affine_finetune_lr_schedule": symbolize_config.affine_finetune_lr_schedule,
        "layerwise_finetune_steps": symbolize_config.layerwise_finetune_steps,
        "layerwise_finetune_lr": symbolize_config.layerwise_finetune_lr,
        "layerwise_finetune_lamb": symbolize_config.layerwise_finetune_lamb,
        "layerwise_use_validation": symbolize_config.layerwise_use_validation,
        "layerwise_validation_ratio": symbolize_config.layerwise_validation_ratio,
        "layerwise_validation_seed": symbolize_config.layerwise_validation_seed,
        "layerwise_early_stop_patience": symbolize_config.layerwise_early_stop_patience,
        "layerwise_early_stop_min_delta": symbolize_config.layerwise_early_stop_min_delta,
        "layerwise_eval_interval": symbolize_config.layerwise_eval_interval,
        "layerwise_validation_n_sample": symbolize_config.layerwise_validation_n_sample,
        "batch_size": symbolize_config.batch_size,
        "parallel_mode": symbolize_config.parallel_mode,
        "parallel_workers": symbolize_config.parallel_workers,
        "parallel_min_tasks": symbolize_config.parallel_min_tasks,
        "enable_input_compaction": symbolize_config.enable_input_compaction,
        "symbolic_backend": _resolve_symbolic_backend(symbolize_config),
        "icbr_topk": int(getattr(symbolize_config, "icbr_topk", 5)),
        "icbr_a_range": getattr(symbolize_config, "icbr_a_range", (-10.0, 10.0)),
        "icbr_b_range": getattr(symbolize_config, "icbr_b_range", (-10.0, 10.0)),
        "icbr_grid_number": int(getattr(symbolize_config, "icbr_grid_number", 21)),
        "icbr_iteration": int(getattr(symbolize_config, "icbr_iteration", 2)),
        "icbr_calibration_n_sample": int(getattr(symbolize_config, "icbr_calibration_n_sample", 512)),
        "prune_collapse_floor": symbolize_config.prune_collapse_floor,
        "prune_eval_interval": symbolize_config.prune_eval_interval,
        "prune_attr_sample_adaptive": symbolize_config.prune_attr_sample_adaptive,
        "prune_attr_sample_min": symbolize_config.prune_attr_sample_min,
        "prune_attr_sample_max": symbolize_config.prune_attr_sample_max,
        "prune_threshold_start": symbolize_config.prune_threshold_start,
        "prune_threshold_end": symbolize_config.prune_threshold_end,
        "prune_max_drop_ratio_per_round": symbolize_config.prune_max_drop_ratio_per_round,
        "prune_threshold_backoff": symbolize_config.prune_threshold_backoff,
        "prune_adaptive_threshold": symbolize_config.prune_adaptive_threshold,
        "prune_adaptive_step": symbolize_config.prune_adaptive_step,
        "prune_adaptive_acc_drop_tol": symbolize_config.prune_adaptive_acc_drop_tol,
        "prune_adaptive_min_edges_gain": symbolize_config.prune_adaptive_min_edges_gain,
        "prune_adaptive_low_gain_patience": symbolize_config.prune_adaptive_low_gain_patience,
        "heavy_ft_early_stop_patience": symbolize_config.heavy_ft_early_stop_patience,
        "heavy_ft_early_stop_min_delta": symbolize_config.heavy_ft_early_stop_min_delta,
        "collect_timing": symbolize_config.collect_timing,
        "verbose": symbolize_config.verbose,
    }
    if options["batch_size"] is None:
        options["batch_size"] = default_batch_size()
    return options


def _run_symbolic_backend(
    work,
    dataset,
    *,
    backend: str,
    lib,
    lib_hidden,
    lib_output,
    weight_simple: float,
    layerwise_finetune_steps: int,
    layerwise_finetune_lr: float,
    layerwise_finetune_lamb: float,
    layerwise_use_validation: bool,
    layerwise_validation_ratio: float,
    layerwise_validation_seed,
    layerwise_early_stop_patience: int,
    layerwise_early_stop_min_delta: float,
    layerwise_eval_interval: int,
    layerwise_validation_n_sample: int,
    batch_size: int,
    parallel_mode: str,
    parallel_workers,
    parallel_min_tasks: int,
    verbose: bool,
    icbr_topk: int,
    icbr_a_range,
    icbr_b_range,
    icbr_grid_number: int,
    icbr_iteration: int,
    icbr_calibration_n_sample: int,
):
    """Execute one symbolic backend and normalize its statistics payload."""
    if backend == "baseline":
        sym_result = fast_symbolic(
            work,
            dataset,
            lib=lib,
            weight_simple=weight_simple,
            lib_hidden=lib_hidden or LIB_HIDDEN,
            lib_output=lib_output or LIB_OUTPUT,
            layerwise_finetune_steps=layerwise_finetune_steps,
            layerwise_finetune_lr=layerwise_finetune_lr,
            layerwise_finetune_lamb=layerwise_finetune_lamb,
            layerwise_use_validation=layerwise_use_validation,
            layerwise_validation_ratio=layerwise_validation_ratio,
            layerwise_validation_seed=layerwise_validation_seed,
            layerwise_early_stop_patience=layerwise_early_stop_patience,
            layerwise_early_stop_min_delta=layerwise_early_stop_min_delta,
            layerwise_eval_interval=layerwise_eval_interval,
            layerwise_validation_n_sample=layerwise_validation_n_sample,
            batch_size=batch_size,
            parallel_mode=parallel_mode,
            parallel_workers=parallel_workers,
            parallel_min_tasks=parallel_min_tasks,
            verbose=verbose,
        )
        return work, {
            "backend": "baseline",
            "total": sym_result["active"],
            "fixed": sym_result["fixed"],
            "low_r2": sym_result["low_r2"],
            "failed": sym_result.get("failed", 0),
            "r2_records": sym_result["r2_records"],
            "failed_records": sym_result.get("failed_records", []),
            "layer_times": sym_result.get("layer_times", []),
            "parallel_workers": sym_result.get("parallel_workers", 1),
        }

    icbr_lib = _resolve_icbr_symbolic_lib(lib, lib_hidden, lib_output)
    calibration_input = dataset["train_input"]
    calibration_limit = min(int(icbr_calibration_n_sample), int(calibration_input.shape[0]))
    calibration_input = calibration_input[:calibration_limit]

    teacher_work = clone_model(work)
    symbolized_work, icbr_metrics = _run_auto_symbolic_icbr_with_models(
        teacher_work,
        work,
        calibration_input,
        lib_names=list(icbr_lib),
        topk=int(icbr_topk),
        a_range=tuple(icbr_a_range),
        b_range=tuple(icbr_b_range),
        grid_number=int(icbr_grid_number),
        iteration=int(icbr_iteration),
        verbose=1 if verbose else 0,
        collect_metrics=True,
    )
    icbr_total = _count_effective_edges(symbolized_work)
    return symbolized_work, {
        "backend": "icbr",
        "total": icbr_total,
        "fixed": icbr_total,
        "low_r2": 0,
        "failed": 0,
        "r2_records": [],
        "failed_records": [],
        "layer_times": [],
        "parallel_workers": 1,
        "library": list(icbr_lib),
        "candidate_generation_wall_time_s": float(icbr_metrics["candidate_generation_wall_time_s"]),
        "replay_rerank_wall_time_s": float(icbr_metrics["replay_rerank_wall_time_s"]),
        "replay_rank_inversion_count": int(icbr_metrics["replay_rank_inversion_count"]),
        "replay_rank_inversion_total": int(icbr_metrics["replay_rank_inversion_total"]),
        "replay_rank_inversion_rate": float(icbr_metrics["replay_rank_inversion_rate"]),
        "commit_param_drift_l2_mean": float(icbr_metrics["commit_param_drift_l2_mean"]),
        "commit_param_drift_l2_max": float(icbr_metrics["commit_param_drift_l2_max"]),
    }


def _adaptive_attr_sample_count(n_edge_now, target_edges, min_sample=512, max_sample=2048):
    """Choose attribution sample count based on current pruning burden.

    Args:
        n_edge_now: Current edge count.
        target_edges: Target edge count after pruning.
        min_sample: Lower bound for attribution samples.
        max_sample: Upper bound for attribution samples.

    Returns:
        int: Suggested attribution sample count.
    """
    try:
        n_now = float(n_edge_now)
        tgt = float(max(1, target_edges))
    except Exception:
        return int(max_sample)

    ratio = n_now / tgt
    if ratio >= 2.5:
        return int(min_sample)
    if ratio >= 1.8:
        return int((min_sample + max_sample) // 2)
    return int(max_sample)


def _heavy_finetune(
    work,
    dataset,
    total_steps=240,
    batch_size=None,
    verbose=True,
    lr_schedule=None,
    early_stop_patience=0,
    early_stop_min_delta=1e-4,
):
    """Run the post-symbolic heavy fine-tune procedure.

    Args:
        work: Model to fine-tune.
        dataset: Dataset used for fine-tuning.
        total_steps: Total fine-tuning steps.
        batch_size: Batch size used during fine-tuning.
        verbose: Whether to print progress messaging.
        lr_schedule: Optional learning rate schedule per phase.
        early_stop_patience: Early-stop patience value.
        early_stop_min_delta: Minimum accuracy gain to reset patience.

    Returns:
        float: Accuracy of the work after restoring the best parameters.
    """
    if batch_size is None:
        batch_size = default_batch_size()

    if lr_schedule is None:
        lr_schedule = [0.003, 0.001, 0.0005, 0.0002]
    lr_schedule = list(lr_schedule)
    if len(lr_schedule) == 0:
        return model_acc_ds(work, dataset)

    n_phases = len(lr_schedule)
    steps_per_phase = total_steps // n_phases

    best_acc = model_acc_ds(work, dataset)
    best_state = {k: v.detach().cpu().clone() for k, v in work.state_dict().items()}
    no_improve_count = 0

    for phase_idx, lr in enumerate(lr_schedule):
        phase_steps = steps_per_phase if phase_idx < n_phases - 1 else (total_steps - steps_per_phase * (n_phases - 1))
        if phase_steps <= 0:
            continue

        _, fit_error = _fit_or_error(
            f"heavy_finetune_phase_{phase_idx}",
            model=work,
            dataset=dataset,
            opt="Adam",
            steps=phase_steps,
            lr=lr,
            lamb=0.0,
            batch=batch_size,
            update_grid=False,
            singularity_avoiding=True,
            log=max(1, phase_steps // 5),
        )
        if fit_error is not None:
            if verbose:
                print(f"[heavy_finetune] stop at phase={phase_idx}: {fit_error}")
            break

        acc_now = model_acc_ds(work, dataset)
        improved = acc_now > (best_acc + float(early_stop_min_delta))
        if acc_now > best_acc:
            best_acc = acc_now
            best_state = {k: v.detach().cpu().clone() for k, v in work.state_dict().items()}

        if early_stop_patience > 0:
            if improved:
                no_improve_count = 0
            else:
                no_improve_count += 1

            if no_improve_count >= int(early_stop_patience):
                if verbose:
                    print(f"[heavy_finetune] early stop at phase={phase_idx}, best_acc={best_acc:.4f}")
                break

    work.load_state_dict(best_state)
    return model_acc_ds(work, dataset)


def symbolize_pipeline(
    model,
    dataset,
    config: AppConfig,
):
    """Execute the main symkan symbolic pipeline.

    The pipeline runs progressive pruning, optional input compaction,
    layer-wise symbolic fitting, heavy fine-tuning, and result export.

    Args:
        model: KAN/symkan model to be symbolized.
        dataset: Dataset dictionary returned by ``build_dataset``.
        config: Unified AppConfig instance, primarily using ``config.symbolize``.

    Returns:
        dict: Result payload containing the model, expressions, edge counts, accuracy,
        trace, statistics, and timing diagnostics.
    """
    prepared_bundle = prepare_symbolic_bundle(model, dataset, config)
    return symbolize_pipeline_from_prepared(prepared_bundle, dataset, config)


def prepare_symbolic_bundle(
    model,
    dataset,
    config: AppConfig,
):
    """Run the shared pre-backend symbolic preparation stage."""
    register_custom_functions()
    options = _resolve_symbolize_options(config)
    target_edges = int(options["target_edges"])
    max_prune_rounds = int(options["max_prune_rounds"])
    finetune_steps = int(options["finetune_steps"])
    finetune_lr = float(options["finetune_lr"])
    batch_size = int(options["batch_size"])
    enable_input_compaction = bool(options["enable_input_compaction"])
    prune_collapse_floor = float(options["prune_collapse_floor"])
    prune_eval_interval = int(options["prune_eval_interval"])
    prune_attr_sample_adaptive = bool(options["prune_attr_sample_adaptive"])
    prune_attr_sample_min = int(options["prune_attr_sample_min"])
    prune_attr_sample_max = int(options["prune_attr_sample_max"])
    prune_threshold_start = float(options["prune_threshold_start"])
    prune_threshold_end = float(options["prune_threshold_end"])
    prune_max_drop_ratio_per_round = float(options["prune_max_drop_ratio_per_round"])
    prune_threshold_backoff = float(options["prune_threshold_backoff"])
    prune_adaptive_threshold = bool(options["prune_adaptive_threshold"])
    prune_adaptive_step = float(options["prune_adaptive_step"])
    prune_adaptive_acc_drop_tol = float(options["prune_adaptive_acc_drop_tol"])
    prune_adaptive_min_edges_gain = int(options["prune_adaptive_min_edges_gain"])
    prune_adaptive_low_gain_patience = int(options["prune_adaptive_low_gain_patience"])
    collect_timing = bool(options["collect_timing"])
    verbose = bool(options["verbose"])

    work = clone_model(model)
    baseline_acc = model_acc_ds(work, dataset)
    n_edge_input = get_n_edge(work)

    effective_target = target_edges
    timing_prune_rounds = []
    timing_symbolic_layers = []
    timing_fit = []
    timing_pipeline_warnings = []
    timing: dict[str, object] = {
        "prune_rounds": timing_prune_rounds,
        "symbolic_layers": timing_symbolic_layers,
        "fit": timing_fit,
        "pipeline_warnings": timing_pipeline_warnings,
        "input_compaction_fallback": False,
    }
    if np.isfinite(n_edge_input) and n_edge_input > target_edges * 1.5:
        # Preserve the legacy loose edge target to avoid early-stage collapse on wide models.
        effective_target = max(target_edges, int(n_edge_input * 0.5))

    prep_t0 = time.perf_counter()
    thresholds = np.linspace(float(prune_threshold_start), float(prune_threshold_end), max_prune_rounds)
    trace = []
    prune_eval_interval = max(1, int(prune_eval_interval))
    last_acc = float(baseline_acc)
    adaptive_mode = bool(prune_adaptive_threshold)
    th_low = min(float(prune_threshold_start), float(prune_threshold_end))
    th_high = max(float(prune_threshold_start), float(prune_threshold_end))
    adaptive_step = float(prune_adaptive_step)
    if adaptive_step <= 0:
        adaptive_step = max((th_high - th_low) / max(1, max_prune_rounds - 1), 1e-4)
    current_threshold = th_low
    success_count = 0
    failure_count = 0
    low_gain_rounds = 0

    for rd in range(max_prune_rounds):
        th = float(current_threshold if adaptive_mode else thresholds[rd])
        t_round = time.perf_counter()
        n_before = get_n_edge(work)
        if np.isfinite(n_before) and n_before <= effective_target:
            break
        acc_ref = float(last_acc)

        snap_prune_state = {k: v.detach().cpu().clone() for k, v in work.state_dict().items()}
        try:
            attr_n_sample = 2048
            if prune_attr_sample_adaptive:
                attr_n_sample = _adaptive_attr_sample_count(
                    n_before,
                    effective_target,
                    min_sample=int(prune_attr_sample_min),
                    max_sample=int(prune_attr_sample_max),
                )
            safe_attribute(work, dataset, n_sample=int(attr_n_sample))
            work.prune_edge(threshold=th)
        except Exception as exc:
            work.load_state_dict(snap_prune_state)
            _set_abort_reason(
                timing,
                stage="prune_round",
                reason=str(exc),
                error_type=type(exc).__name__,
            )
            _append_pipeline_warning(
                timing_pipeline_warnings,
                code="prune_round_failed",
                stage="prune_round",
                message=str(exc),
                error_type=type(exc).__name__,
                round=int(rd),
                threshold=float(th),
                attr_n_sample=int(attr_n_sample),
            )
            break

        n_after = get_n_edge(work)
        drop_ratio = 0.0
        if np.isfinite(n_before) and np.isfinite(n_after) and float(n_before) > 0:
            drop_ratio = max(0.0, (float(n_before) - float(n_after)) / float(n_before))

        if drop_ratio > float(prune_max_drop_ratio_per_round):
            # A single prune round removed too many edges; roll back and retry with a lower threshold to prevent collapse.
            work.load_state_dict(snap_prune_state)
            safer_th = max(1e-4, float(th) * float(prune_threshold_backoff))
            try:
                safe_attribute(work, dataset, n_sample=int(attr_n_sample))
                work.prune_edge(threshold=safer_th)
                n_after = get_n_edge(work)
                if np.isfinite(n_before) and np.isfinite(n_after) and float(n_before) > 0:
                    drop_ratio = max(0.0, (float(n_before) - float(n_after)) / float(n_before))
                th = safer_th
            except Exception as exc:
                work.load_state_dict(snap_prune_state)
                _set_abort_reason(
                    timing,
                    stage="prune_round_backoff",
                    reason=str(exc),
                    error_type=type(exc).__name__,
                )
                _append_pipeline_warning(
                    timing_pipeline_warnings,
                    code="prune_round_backoff_failed",
                    stage="prune_round_backoff",
                    message=str(exc),
                    error_type=type(exc).__name__,
                    round=int(rd),
                    threshold=float(safer_th),
                    attr_n_sample=int(attr_n_sample),
                )
                break

        if n_after == 0:
            work.load_state_dict(snap_prune_state)
            break

        if n_after != n_before:
            t_fit = time.perf_counter()
            _, prune_fit_error = _fit_or_error(
                f"prune_round_{rd}_fit",
                model=work,
                dataset=dataset,
                opt="Adam",
                steps=finetune_steps,
                lr=finetune_lr,
                lamb=0.0,
                batch=batch_size,
                update_grid=False,
                singularity_avoiding=True,
                log=max(1, finetune_steps // 5),
            )
            if prune_fit_error is not None:
                work.load_state_dict(snap_prune_state)
                _set_abort_reason(
                    timing,
                    stage="prune_round_fit",
                    reason=prune_fit_error,
                    error_type="RuntimeError",
                )
                _append_pipeline_warning(
                    timing_pipeline_warnings,
                    code="prune_round_fit_failed",
                    stage="prune_round_fit",
                    message=prune_fit_error,
                    error_type="RuntimeError",
                    round=int(rd),
                    threshold=float(th),
                )
                break
            if collect_timing:
                timing_fit.append({"stage": "prune_round", "round": int(rd), "seconds": float(time.perf_counter() - t_fit)})

        should_eval = (rd % prune_eval_interval == 0)
        if adaptive_mode:
            should_eval = True
        if np.isfinite(n_after) and np.isfinite(effective_target) and n_after <= effective_target * 1.3:
            should_eval = True
        if rd == max_prune_rounds - 1:
            should_eval = True

        if should_eval:
            acc_now = model_acc_ds(work, dataset)
            last_acc = float(acc_now)
        else:
            acc_now = float(last_acc)

        edges_removed = 0
        if np.isfinite(n_before) and np.isfinite(n_after):
            edges_removed = max(0, int(round(float(n_before) - float(n_after))))
        acc_drop = float(acc_ref - float(acc_now))

        trace.append(
            {
                "round": rd,
                "threshold": float(th),
                "edges_before": n_before,
                "edges_after": n_after,
                "drop_ratio": float(drop_ratio),
                "edges_removed": int(edges_removed),
                "acc_drop": float(acc_drop),
                "acc": float(acc_now),
            }
        )
        if collect_timing:
            timing_prune_rounds.append(
                {
                    "round": int(rd),
                    "threshold": float(th),
                    "edges_before": float(n_before),
                    "edges_after": float(n_after),
                    "drop_ratio": float(drop_ratio),
                    "edges_removed": int(edges_removed),
                    "acc_drop": float(acc_drop),
                    "attr_n_sample": int(attr_n_sample) if prune_attr_sample_adaptive else 2048,
                    "eval_skipped": bool(not should_eval),
                    "seconds": float(time.perf_counter() - t_round),
                }
            )

        if adaptive_mode:
            no_gain = edges_removed <= 0
            too_much_drop = acc_drop > float(prune_adaptive_acc_drop_tol)
            success = (not no_gain) and (not too_much_drop)

            if no_gain:
                # No edges removed indicates the threshold is too low; increase it instead of decreasing.
                success_count = 0
                failure_count += 1
                low_gain_rounds += 1
                probe = 1.2 + min(2.5, failure_count * 0.5)
                current_threshold = min(th_high, float(th) + adaptive_step * probe)
            elif success:
                success_count += 1
                failure_count = 0
                if edges_removed <= int(prune_adaptive_min_edges_gain):
                    low_gain_rounds += 1
                else:
                    low_gain_rounds = 0
                boost = 1.0 + min(3.0, success_count * 0.4)
                if edges_removed <= int(prune_adaptive_min_edges_gain):
                    boost *= 1.5
                current_threshold = min(th_high, float(th) + adaptive_step * boost)
            else:
                # Pruning occurred but accuracy dropped excessively, so back off the threshold.
                failure_count += 1
                success_count = 0
                low_gain_rounds += 1
                penalty = 0.3 * (1.0 + min(2.0, failure_count * 0.3))
                current_threshold = max(th_low, float(th) - adaptive_step * penalty)

            # Only declare convergence when the threshold is near its upper bound and gains remain low; otherwise continue exploring.
            near_ceiling = current_threshold >= (th_high - max(adaptive_step, 1e-4))
            if near_ceiling and low_gain_rounds >= max(1, int(prune_adaptive_low_gain_patience)):
                break

        if float(prune_collapse_floor) > 0.0 and acc_now < baseline_acc * float(prune_collapse_floor):
            work.load_state_dict(snap_prune_state)
            break

    n_edge_now = get_n_edge(work)
    compact_state = None
    finetune_dataset = dataset
    effective_inputs = list(range(int(work.width_in[0])))

    if np.isfinite(n_edge_now) and n_edge_now > 0:
        try:
            compact_state = compact_inputs_for_symbolic(work, dataset) if enable_input_compaction else None
            if compact_state is not None:
                work = compact_state["model"]
                finetune_dataset = compact_state["dataset"]
                effective_inputs = compact_state["active_inputs"]
                if verbose:
                    print(f"[symbolize_pipeline] 输入压缩: {int(dataset['train_input'].shape[1])} -> {len(effective_inputs)}")
            elif not enable_input_compaction:
                if verbose:
                    print("[symbolize_pipeline] 跳过输入压缩")
        except Exception as exc:
            compact_state = None
            finetune_dataset = dataset
            timing["input_compaction_fallback"] = True
            timing["input_compaction_reason"] = str(exc)
            timing["input_compaction_error_type"] = type(exc).__name__
            _append_pipeline_warning(
                timing_pipeline_warnings,
                code="input_compaction_fallback",
                stage="input_compaction",
                message=str(exc),
                error_type=type(exc).__name__,
            )

        t_pre = time.perf_counter()
        _fit_or_raise(
            "pre_symbolic_fit",
            model=work,
            dataset=finetune_dataset,
            opt="Adam",
            steps=100,
            lr=0.005,
            lamb=0.0,
            batch=batch_size,
            update_grid=False,
            singularity_avoiding=True,
            log=10,
        )
        if collect_timing:
            timing_fit.append({"stage": "pre_symbolic", "seconds": float(time.perf_counter() - t_pre)})
    timing["symbolic_prep_total_seconds"] = float(time.perf_counter() - prep_t0)
    return {
        "prepared_model": work,
        "prepared_dataset": finetune_dataset,
        "trace": pd.DataFrame(trace) if trace else pd.DataFrame(),
        "timing": timing,
        "effective_target_edges": effective_target,
        "input_n_edge": n_edge_input,
        "effective_input_indices": effective_inputs,
        "effective_input_dim": len(effective_inputs),
        "original_input_id": compact_state["original_input_id"] if compact_state is not None else None,
    }


def symbolize_pipeline_from_prepared(
    prepared_bundle,
    dataset,
    config: AppConfig,
):
    """Complete backend-specific symbolic fitting from a prepared bundle."""
    register_custom_functions()
    options = _resolve_symbolize_options(config)
    lib = options["lib"]
    lib_hidden = options["lib_hidden"]
    lib_output = options["lib_output"]
    weight_simple = float(options["weight_simple"])
    affine_finetune_steps = int(options["affine_finetune_steps"])
    affine_finetune_lr_schedule = options["affine_finetune_lr_schedule"]
    layerwise_finetune_steps = int(options["layerwise_finetune_steps"])
    layerwise_finetune_lr = float(options["layerwise_finetune_lr"])
    layerwise_finetune_lamb = float(options["layerwise_finetune_lamb"])
    layerwise_use_validation = bool(options["layerwise_use_validation"])
    layerwise_validation_ratio = float(options["layerwise_validation_ratio"])
    layerwise_validation_seed = options["layerwise_validation_seed"]
    layerwise_early_stop_patience = int(options["layerwise_early_stop_patience"])
    layerwise_early_stop_min_delta = float(options["layerwise_early_stop_min_delta"])
    layerwise_eval_interval = int(options["layerwise_eval_interval"])
    layerwise_validation_n_sample = int(options["layerwise_validation_n_sample"])
    batch_size = int(options["batch_size"])
    parallel_mode = str(options["parallel_mode"])
    parallel_workers = options["parallel_workers"]
    parallel_min_tasks = int(options["parallel_min_tasks"])
    symbolic_backend = str(options["symbolic_backend"])
    icbr_topk = int(options["icbr_topk"])
    icbr_a_range = options["icbr_a_range"]
    icbr_b_range = options["icbr_b_range"]
    icbr_grid_number = int(options["icbr_grid_number"])
    icbr_iteration = int(options["icbr_iteration"])
    icbr_calibration_n_sample = int(options["icbr_calibration_n_sample"])
    heavy_ft_early_stop_patience = int(options["heavy_ft_early_stop_patience"])
    heavy_ft_early_stop_min_delta = float(options["heavy_ft_early_stop_min_delta"])
    collect_timing = bool(options["collect_timing"])
    verbose = bool(options["verbose"])

    work = prepared_bundle["prepared_model"]
    finetune_dataset = prepared_bundle.get("prepared_dataset", dataset)
    timing = _copy_timing_payload(prepared_bundle.get("timing", {}))
    timing["symbolic_backend"] = symbolic_backend
    timing_prune_rounds = timing.setdefault("prune_rounds", [])
    timing_symbolic_layers = timing.setdefault("symbolic_layers", [])
    timing_fit = timing.setdefault("fit", [])
    timing_pipeline_warnings = timing.setdefault("pipeline_warnings", [])
    trace_df = prepared_bundle.get("trace")
    if trace_df is None:
        trace_df = pd.DataFrame()

    if np.isfinite(prepared_bundle.get("input_n_edge", 0)) and float(prepared_bundle.get("input_n_edge", 0)) > 0:
        t_sym = time.perf_counter()
        work, sym_stats = _run_symbolic_backend(
            work,
            finetune_dataset,
            backend=symbolic_backend,
            lib=lib,
            lib_hidden=lib_hidden,
            lib_output=lib_output,
            weight_simple=weight_simple,
            layerwise_finetune_steps=layerwise_finetune_steps,
            layerwise_finetune_lr=layerwise_finetune_lr,
            layerwise_finetune_lamb=layerwise_finetune_lamb,
            layerwise_use_validation=layerwise_use_validation,
            layerwise_validation_ratio=layerwise_validation_ratio,
            layerwise_validation_seed=layerwise_validation_seed,
            layerwise_early_stop_patience=layerwise_early_stop_patience,
            layerwise_early_stop_min_delta=layerwise_early_stop_min_delta,
            layerwise_eval_interval=layerwise_eval_interval,
            layerwise_validation_n_sample=layerwise_validation_n_sample,
            batch_size=batch_size,
            parallel_mode=parallel_mode,
            parallel_workers=parallel_workers,
            parallel_min_tasks=parallel_min_tasks,
            verbose=verbose,
            icbr_topk=icbr_topk,
            icbr_a_range=icbr_a_range,
            icbr_b_range=icbr_b_range,
            icbr_grid_number=icbr_grid_number,
            icbr_iteration=icbr_iteration,
            icbr_calibration_n_sample=icbr_calibration_n_sample,
        )
        if collect_timing:
            timing_symbolic_layers.clear()
            timing_symbolic_layers.extend(sym_stats.get("layer_times", []))
            timing["symbolic_total_seconds"] = float(time.perf_counter() - t_sym)
        if symbolic_backend == "icbr":
            timing["symbolic_backend_library"] = list(sym_stats.get("library", []))
            timing["symbolic_backend_topk"] = int(icbr_topk)
            timing["symbolic_backend_calibration_n_sample"] = int(icbr_calibration_n_sample)
            timing["icbr_candidate_generation_wall_time_s"] = float(
                sym_stats.get("candidate_generation_wall_time_s", float("nan"))
            )
            timing["icbr_replay_rerank_wall_time_s"] = float(
                sym_stats.get("replay_rerank_wall_time_s", float("nan"))
            )
            timing["icbr_replay_rank_inversion_rate"] = float(sym_stats.get("replay_rank_inversion_rate", float("nan")))

        t_heavy = time.perf_counter()
        _heavy_finetune(
            work,
            finetune_dataset,
            total_steps=affine_finetune_steps,
            batch_size=batch_size,
            verbose=verbose,
            lr_schedule=affine_finetune_lr_schedule,
            early_stop_patience=heavy_ft_early_stop_patience,
            early_stop_min_delta=heavy_ft_early_stop_min_delta,
        )
        if collect_timing:
            timing_fit.append({"stage": "post_symbolic_affine", "seconds": float(time.perf_counter() - t_heavy)})

        original_input_id = prepared_bundle.get("original_input_id")
        if original_input_id is not None:
            work.input_id = original_input_id
    else:
        sym_stats = {
            "backend": symbolic_backend,
            "total": 0,
            "fixed": 0,
            "low_r2": 0,
            "failed": 0,
            "r2_records": [],
            "failed_records": [],
            "layer_times": [],
            "parallel_workers": 1,
        }
    sym_stats["pipeline_warnings"] = list(timing_pipeline_warnings)

    formulas = None
    if hasattr(work, "symbolic_formula"):
        try:
            formulas = work.symbolic_formula()
        except Exception:
            formulas = None

    valid = collect_valid_formulas(formulas)
    final_n_edge_raw = get_n_edge(work)
    final_n_edge = _count_effective_edges(work)
    return {
        "model": work,
        "formulas": formulas,
        "valid_expressions": valid,
        "trace": trace_df.copy() if hasattr(trace_df, "copy") else pd.DataFrame(trace_df),
        "sym_stats": sym_stats,
        "final_n_edge": final_n_edge,
        "final_n_edge_raw": final_n_edge_raw,
        "final_acc": float(model_acc_ds(work, dataset)),
        "effective_target_edges": prepared_bundle.get("effective_target_edges", 0),
        "input_n_edge": prepared_bundle.get("input_n_edge", 0),
        "effective_input_indices": list(prepared_bundle.get("effective_input_indices", [])),
        "effective_input_dim": int(prepared_bundle.get("effective_input_dim", 0)),
        "timing": timing,
    }


def symbolize_pipeline_report(model, dataset, config: AppConfig):
    """Return the structured report version of ``symbolize_pipeline``.

    Args:
        model: Model to be symbolized.
        dataset: Dataset dictionary.
        config: Unified AppConfig instance.

    Returns:
        SymbolizeResult: Structured result object.
    """
    from symkan.core.types import SymbolizeResult

    result = symbolize_pipeline(model, dataset, config)
    return SymbolizeResult(
        model=result.get("model"),
        formulas=result.get("formulas"),
        valid_expressions=result.get("valid_expressions", []),
        trace=result.get("trace"),
        sym_stats=result.get("sym_stats", {}),
        final_n_edge=result.get("final_n_edge", 0),
        final_n_edge_raw=result.get("final_n_edge_raw", 0),
        final_acc=result.get("final_acc", 0.0),
        effective_target_edges=result.get("effective_target_edges", 0),
        input_n_edge=result.get("input_n_edge", 0),
        effective_input_indices=result.get("effective_input_indices", []),
        effective_input_dim=result.get("effective_input_dim", 0),
        timing=result.get("timing", {}),
    )


def symbolize_pipeline_from_prepared_report(prepared_bundle, dataset, config: AppConfig):
    """Structured report wrapper for ``symbolize_pipeline_from_prepared``."""
    from symkan.core.types import SymbolizeResult

    result = symbolize_pipeline_from_prepared(prepared_bundle, dataset, config)
    return SymbolizeResult(
        model=result.get("model"),
        formulas=result.get("formulas"),
        valid_expressions=result.get("valid_expressions", []),
        trace=result.get("trace"),
        sym_stats=result.get("sym_stats", {}),
        final_n_edge=result.get("final_n_edge", 0),
        final_n_edge_raw=result.get("final_n_edge_raw", 0),
        final_acc=result.get("final_acc", 0.0),
        effective_target_edges=result.get("effective_target_edges", 0),
        input_n_edge=result.get("input_n_edge", 0),
        effective_input_indices=result.get("effective_input_indices", []),
        effective_input_dim=result.get("effective_input_dim", 0),
        timing=result.get("timing", {}),
    )
