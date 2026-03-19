"""Primitive routines for symbolic candidate search and layer-wise fitting.

Migrated from pipeline.py, all search operations run sequentially on a single
model to avoid shared-state contention in concurrent ``suggest_symbolic`` calls.
"""

from collections import Counter
from typing import Optional

import numpy as np
import torch

from symkan.core import safe_fit_report
from symkan.core.train import format_fit_failure
from symkan.core.runtime import default_batch_size


def _resolve_parallel_workers(parallel_mode="auto", parallel_workers=None):
    """Resolve the requested parallel worker count.

    Args:
        parallel_mode: Requested parallel mode label.
        parallel_workers: Requested worker count.

    Returns:
        int: Currently always returns 1 (serial) for correctness until per-worker
        cloning is available.
    """
    # NOTE: Older versions allowed thread mode with shared model suggest_symbolic,
    # causing internal state races. Until per-worker cloning exists, enforce serial execution.
    return 1


def layerwise_symbolic(work, dataset, layer_idx, lib, weight_simple=0.0, verbose=True):
    """Perform layer-wise symbolic candidate search and fixing.

    Args:
        work: KAN model modified in place.
        dataset: Dataset dictionary.
        layer_idx: Target layer index.
        lib: Symbolic function library.
        weight_simple: Simplicity bias weight.
        verbose: Whether to emit logging.

    Returns:
        dict: Search statistics.
    """
    work.eval()
    with torch.no_grad():
        n_samples = min(len(dataset["train_input"]), 1024)
        work(dataset["train_input"][:n_samples])

    fixed_count = 0
    low_r2_count = 0
    active_count = 0
    failed_count = 0
    r2_records = []
    failed_records = []

    l = layer_idx
    n_in = work.width_in[l]
    n_out = work.width_out[l + 1]

    for i in range(n_in):
        for j in range(n_out):
            sym_mask = work.symbolic_fun[l].mask[j, i].item()
            act_mask = work.act_fun[l].mask[i][j].item()

            if sym_mask > 0 and act_mask == 0:
                continue
            if act_mask == 0:
                continue

            active_count += 1
            try:
                # suggest_symbolic temporarily mutates the model, so enforce strict serialization here.
                name, _, r2, _ = work.suggest_symbolic(
                    l, i, j, lib=lib, verbose=False, weight_simple=weight_simple
                )
                r2_records.append({"layer": l, "i": i, "j": j, "name": name, "r2": float(r2)})
                work.fix_symbolic(l, i, j, name, verbose=False, log_history=False)
                fixed_count += 1
                if r2 < 0.5:
                    low_r2_count += 1
                    if verbose:
                        print(f"    ⚠ 低R² fix ({l},{i},{j}) → {name}  R²={r2:.4f}")
            except Exception as e:
                failed_count += 1
                failed_records.append(
                    {
                        "layer": int(l),
                        "i": int(i),
                        "j": int(j),
                        "error_type": type(e).__name__,
                        "error_message": str(e),
                    }
                )
                if verbose:
                    print(f"    ({l},{i},{j}) suggest failed: {e}")

    if verbose:
        print(f"  Layer {l}: 活跃={active_count}, fix={fixed_count}")

    return {
        "active": active_count,
        "fixed": fixed_count,
        "low_r2": low_r2_count,
        "failed": failed_count,
        "r2_records": r2_records,
        "failed_records": failed_records,
    }


def _has_split(dataset, split: str) -> bool:
    """Check whether a dataset dictionary contains a usable split.

    Args:
        dataset: Dataset dictionary.
        split: Split name such as ``train`` or ``val``.

    Returns:
        bool: ``True`` when both input and label tensors are present.
    """
    input_key = f"{split}_input"
    label_key = f"{split}_label"
    return (
        input_key in dataset
        and label_key in dataset
        and dataset[input_key] is not None
        and dataset[label_key] is not None
    )


def _build_layerwise_ft_datasets(dataset, use_validation: bool, validation_ratio: float, validation_seed: Optional[int]):
    """Build fit/validation datasets for layerwise fine-tuning.

    Args:
        dataset: Original dataset dictionary.
        use_validation: Whether validation-driven layerwise FT is enabled.
        validation_ratio: Validation split ratio when no explicit ``val`` split
            already exists.
        validation_seed: Random seed for the synthetic validation split.

    Returns:
        tuple[dict, dict | None]: Dataset used for fitting and optional
        validation dataset mapped onto the ``test_*`` keys expected by metric
        helpers.
    """
    if not bool(use_validation):
        return dataset, None

    if _has_split(dataset, "val"):
        val_ds = dict(dataset)
        val_ds["test_input"] = dataset["val_input"]
        val_ds["test_label"] = dataset["val_label"]
        return dataset, val_ds

    ratio = float(validation_ratio)
    if ratio <= 0:
        return dataset, None

    train_input = dataset["train_input"]
    train_label = dataset["train_label"]
    n_total = int(train_input.shape[0])
    n_val = int(n_total * ratio)
    if n_total <= 20 or n_val < 10 or n_val >= n_total:
        return dataset, None

    rng = np.random.default_rng(validation_seed)
    perm = rng.permutation(n_total)
    device = train_input.device if torch.is_tensor(train_input) else None
    val_idx = torch.as_tensor(perm[:n_val], dtype=torch.long, device=device)
    fit_idx = torch.as_tensor(perm[n_val:], dtype=torch.long, device=device)

    fit_ds = dict(dataset)
    fit_ds["train_input"] = train_input[fit_idx]
    fit_ds["train_label"] = train_label[fit_idx]

    val_ds = dict(dataset)
    val_ds["test_input"] = train_input[val_idx]
    val_ds["test_label"] = train_label[val_idx]
    return fit_ds, val_ds


def _formula_mean_r2(work, eval_dataset, n_sample: int):
    """Estimate mean symbolic formula R² on an evaluation dataset.

    Args:
        work: Symbolized model-like object.
        eval_dataset: Evaluation dataset dictionary.
        n_sample: Maximum number of samples used during formula validation.

    Returns:
        float: Mean R² across valid formulas, or ``nan`` if unavailable.
    """
    from symkan.eval.metrics import validate_formula_numerically

    if eval_dataset is None or not hasattr(work, "symbolic_formula"):
        return float("nan")
    try:
        formulas = work.symbolic_formula()
    except Exception:
        return float("nan")

    val_df = validate_formula_numerically(work, formulas, eval_dataset, n_sample=int(n_sample))
    if val_df is None or len(val_df) == 0 or "r2" not in val_df.columns:
        return float("nan")

    r2_values = val_df["r2"].to_numpy(dtype=float)
    if r2_values.size == 0:
        return float("nan")
    return float(np.nanmean(r2_values))


def _layerwise_finetune_with_early_stop(
    work,
    fit_dataset,
    val_dataset,
    total_steps: int,
    lr: float,
    lamb: float,
    batch_size: int,
    use_validation: bool,
    eval_interval: int,
    early_stop_patience: int,
    early_stop_min_delta: float,
    validation_n_sample: int,
    verbose: bool,
):
    """Run layerwise fine-tuning with optional validation-driven early stop.

    Args:
        work: Model being fine-tuned in place.
        fit_dataset: Dataset used for optimization.
        val_dataset: Optional validation dataset for early stopping.
        total_steps: Maximum fine-tune steps.
        lr: Fine-tune learning rate.
        lamb: Fine-tune regularization strength.
        batch_size: Fit batch size.
        use_validation: Whether validation-based stopping is enabled.
        eval_interval: Validation interval in steps.
        early_stop_patience: Patience measured in validation checks.
        early_stop_min_delta: Minimum R² improvement treated as progress.
        validation_n_sample: Sample count used for formula validation.
        verbose: Whether to print early-stop logs.

    Returns:
        dict[str, object]: Structured summary of used steps, validation metrics,
        and possible fit failures.
    """
    steps = int(total_steps)
    if steps <= 0:
        return {
            "steps_requested": 0,
            "steps_used": 0,
            "early_stopped": False,
            "best_val_r2": float("nan"),
            "last_val_r2": float("nan"),
            "fit_failed": False,
            "fit_error": "",
        }

    if (not use_validation) or (val_dataset is None):
        report = safe_fit_report(
            work,
            fit_dataset,
            opt="Adam",
            steps=steps,
            lr=float(lr),
            lamb=float(lamb),
            batch=batch_size,
            update_grid=False,
            singularity_avoiding=True,
            log=max(1, steps // 5),
        )
        if not report.success:
            return {
                "steps_requested": steps,
                "steps_used": 0,
                "early_stopped": False,
                "best_val_r2": float("nan"),
                "last_val_r2": float("nan"),
                "fit_failed": True,
                "fit_error": format_fit_failure(report, context="layerwise_finetune"),
            }
        return {
            "steps_requested": steps,
            "steps_used": steps,
            "early_stopped": False,
            "best_val_r2": float("nan"),
            "last_val_r2": float("nan"),
            "fit_failed": False,
            "fit_error": "",
        }

    step_chunk = max(1, int(eval_interval))
    patience_limit = max(1, int(early_stop_patience))
    min_delta = float(early_stop_min_delta)

    best_state = {k: v.detach().cpu().clone() for k, v in work.state_dict().items()}
    best_r2 = _formula_mean_r2(work, val_dataset, n_sample=validation_n_sample)
    last_r2 = float(best_r2)
    no_improve = 0
    used_steps = 0
    early_stopped = False

    while used_steps < steps:
        chunk = min(step_chunk, steps - used_steps)
        report = safe_fit_report(
            work,
            fit_dataset,
            opt="Adam",
            steps=int(chunk),
            lr=float(lr),
            lamb=float(lamb),
            batch=batch_size,
            update_grid=False,
            singularity_avoiding=True,
            log=max(1, int(chunk) // 5),
        )
        if not report.success:
            work.load_state_dict(best_state)
            return {
                "steps_requested": steps,
                "steps_used": int(used_steps),
                "early_stopped": False,
                "best_val_r2": float(best_r2),
                "last_val_r2": float(last_r2),
                "fit_failed": True,
                "fit_error": format_fit_failure(report, context="layerwise_finetune"),
            }
        used_steps += int(chunk)

        last_r2 = _formula_mean_r2(work, val_dataset, n_sample=validation_n_sample)
        improved = np.isfinite(last_r2) and ((not np.isfinite(best_r2)) or (last_r2 > best_r2 + min_delta))
        if improved:
            best_r2 = float(last_r2)
            no_improve = 0
            best_state = {k: v.detach().cpu().clone() for k, v in work.state_dict().items()}
        else:
            no_improve += 1
            if no_improve >= patience_limit:
                early_stopped = True
                if verbose:
                    print(
                        f"  LayerwiseFT early-stop: used={used_steps}/{steps}, "
                        f"best_val_r2={best_r2:.4f}, last_val_r2={last_r2:.4f}"
                    )
                break

    work.load_state_dict(best_state)
    return {
        "steps_requested": steps,
        "steps_used": int(used_steps),
        "early_stopped": bool(early_stopped),
        "best_val_r2": float(best_r2),
        "last_val_r2": float(last_r2),
        "fit_failed": False,
        "fit_error": "",
    }


def fast_symbolic(
    work,
    dataset,
    lib=None,
    weight_simple=0.0,
    lib_hidden=None,
    lib_output=None,
    layerwise_finetune_steps=60,
    layerwise_finetune_lr=0.005,
    layerwise_finetune_lamb=1e-5,
    layerwise_use_validation=True,
    layerwise_validation_ratio=0.15,
    layerwise_validation_seed=None,
    layerwise_early_stop_patience=2,
    layerwise_early_stop_min_delta=1e-3,
    layerwise_eval_interval=20,
    layerwise_validation_n_sample=300,
    batch_size=None,
    parallel_mode="auto",
    parallel_workers=None,
    parallel_min_tasks=16,
    verbose=True,
):
    """Main entry point for layer-wise symbolic fitting.

    Iterates through the layers, performing candidate searches and fixes,
    with optional fine-tuning between layers.

    Args:
        work: Model to be symbolized.
        dataset: Dataset dictionary.
        lib: Shared symbolic function library.
        weight_simple: Simplicity preference weight.
        lib_hidden: Hidden-layer library override.
        lib_output: Output-layer library override.
        layerwise_finetune_steps: Fine-tune steps after each layer fix.
        batch_size: Batch size.
        parallel_mode: Parallel execution mode.
        parallel_workers: Requested worker count.
        parallel_min_tasks: Minimum tasks required to enable parallelism.
        verbose: Whether to log progress.

    Returns:
        dict: Statistics including fix counts, R² records, and timing per layer.
    """
    from .library import LIB_HIDDEN, LIB_OUTPUT, get_layer_lib, register_custom_functions
    import time

    register_custom_functions()

    if batch_size is None:
        batch_size = default_batch_size()

    depth = len(work.width_in) - 1
    all_records = []
    total_fixed = 0
    total_active = 0
    total_low_r2 = 0
    total_failed = 0
    layer_times = []
    all_failed_records = []
    fit_dataset, val_dataset = _build_layerwise_ft_datasets(
        dataset,
        use_validation=bool(layerwise_use_validation),
        validation_ratio=float(layerwise_validation_ratio),
        validation_seed=layerwise_validation_seed,
    )
    suggest_workers = _resolve_parallel_workers(
        parallel_mode=parallel_mode, parallel_workers=parallel_workers
    )

    for l in range(depth):
        layer_lib = get_layer_lib(l, depth, lib_hidden, lib_output, lib)
        t0 = time.perf_counter()

        result = layerwise_symbolic(
            work, dataset, l, layer_lib,
            weight_simple=weight_simple, verbose=verbose,
        )

        layer_times.append(
            {
                "layer": int(l),
                "active": int(result["active"]),
                "fixed": int(result["fixed"]),
                "seconds": float(time.perf_counter() - t0),
                "workers": int(suggest_workers),
            }
        )
        all_records.extend(result["r2_records"])
        all_failed_records.extend(result["failed_records"])
        total_fixed += result["fixed"]
        total_active += result["active"]
        total_low_r2 += result["low_r2"]
        total_failed += result["failed"]

        ft_info = {
            "steps_requested": int(layerwise_finetune_steps),
            "steps_used": 0,
            "early_stopped": False,
            "best_val_r2": float("nan"),
            "last_val_r2": float("nan"),
            "fit_failed": False,
            "fit_error": "",
        }
        if result["fixed"] > 0 and l < depth - 1 and layerwise_finetune_steps > 0:
            ft_info = _layerwise_finetune_with_early_stop(
                work,
                fit_dataset=fit_dataset,
                val_dataset=val_dataset,
                total_steps=layerwise_finetune_steps,
                lr=float(layerwise_finetune_lr),
                lamb=float(layerwise_finetune_lamb),
                batch_size=batch_size,
                use_validation=bool(layerwise_use_validation),
                eval_interval=int(layerwise_eval_interval),
                early_stop_patience=int(layerwise_early_stop_patience),
                early_stop_min_delta=float(layerwise_early_stop_min_delta),
                validation_n_sample=int(layerwise_validation_n_sample),
                verbose=bool(verbose),
            )
        layer_times[-1].update({
            "layerwise_ft_steps_requested": int(ft_info["steps_requested"]),
            "layerwise_ft_steps_used": int(ft_info["steps_used"]),
            "layerwise_ft_early_stopped": bool(ft_info["early_stopped"]),
            "layerwise_ft_best_val_r2": float(ft_info["best_val_r2"]),
            "layerwise_ft_last_val_r2": float(ft_info["last_val_r2"]),
            "layerwise_ft_fit_failed": bool(ft_info["fit_failed"]),
            "layerwise_ft_fit_error": str(ft_info["fit_error"]),
        })

    if verbose and all_records:
        name_counts = Counter(r["name"] for r in all_records)
        print(f"  函数分布: {dict(name_counts)}")

    return {
        "active": total_active,
        "fixed": total_fixed,
        "low_r2": total_low_r2,
        "failed": total_failed,
        "r2_records": all_records,
        "failed_records": all_failed_records,
        "layer_times": layer_times,
        "parallel_workers": int(suggest_workers),
    }
