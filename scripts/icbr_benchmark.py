from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import random
import statistics
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

import torch

from kan.MultKAN import MultKAN
from kan.icbr import benchmark_icbr_vs_baseline
from kan.utils import create_dataset


_NUMERIC_METRICS = [
    "teacher_test_mse",
    "teacher_test_r2",
    "candidate_generation_wall_time_s",
    "replay_rerank_wall_time_s",
    "symbolic_wall_time_s",
    "baseline_symbolic_wall_time_s",
    "symbolic_wall_time_delta_s",
    "symbolic_speedup_vs_baseline",
    "replay_imitation_gap",
    "final_mse_loss_shift",
    "baseline_mse",
    "icbr_mse",
    "teacher_target_mse",
    "teacher_target_r2",
    "baseline_target_mse",
    "baseline_target_r2",
    "icbr_target_mse",
    "icbr_target_r2",
    "symbolic_target_mse_shift",
    "symbolic_target_r2_shift",
]

_BOOLEAN_METRICS = [
    "teacher_cache_hit",
    "teacher_quality_gate_pass",
    "formula_validation_result",
    "baseline_formula_validation_result",
    "icbr_formula_validation_result",
]

_SIGNIFICANCE_DIRECTIONS = {
    "symbolic_wall_time_delta_s": "positive",
    "final_mse_loss_shift": "negative",
}

_BENCHMARK_PROFILES: dict[str, dict[str, float | int]] = {
    "quick": {
        "train_num": 64,
        "test_num": 64,
        "train_steps": 20,
        "lr": 0.05,
        "lamb": 1e-3,
    },
    "quality": {
        "train_num": 1000,
        "test_num": 500,
        "train_steps": 80,
        "lr": 0.03,
        "lamb": 1e-3,
    },
}

_TEACHER_CACHE_MODES = {"readwrite", "readonly", "refresh", "off"}


@dataclass(frozen=True)
class _TaskSpec:
    name: str
    n_var: int
    width: list[int]
    target_fn: Callable[[torch.Tensor], torch.Tensor]
    lib: list[str] | None
    icbr_topk: int | None = None
    teacher_max_test_mse: float | None = None
    teacher_min_test_r2: float | None = None


def _task_specs() -> dict[str, _TaskSpec]:
    return {
        "minimal": _TaskSpec(
            name="minimal",
            n_var=1,
            width=[1, 1],
            target_fn=lambda x: torch.sin(torch.pi * x[:, [0]]),
            lib=None,
        ),
        "combo": _TaskSpec(
            name="combo",
            n_var=2,
            width=[2, 2, 1],
            target_fn=lambda x: torch.sin(torch.pi * x[:, [0]]) + x[:, [1]] ** 2,
            lib=None,
        ),
        "poly_cubic": _TaskSpec(
            name="poly_cubic",
            n_var=2,
            width=[2, 3, 1],
            target_fn=lambda x: 0.8 * x[:, [0]] ** 3 - 0.4 * x[:, [0]] + 0.6 * x[:, [1]] ** 2,
            lib=None,
        ),
        "trig_interaction": _TaskSpec(
            name="trig_interaction",
            n_var=3,
            width=[3, 4, 1],
            target_fn=lambda x: torch.sin(torch.pi * x[:, [0]])
            + 0.5 * torch.cos(torch.pi * x[:, [1]])
            + x[:, [0]] * x[:, [2]],
            lib=None,
            icbr_topk=5,
        ),
    }


def _build_teacher_dataset(
    spec: _TaskSpec,
    *,
    seed: int,
    train_num: int,
    test_num: int,
) -> dict[str, torch.Tensor]:
    torch.manual_seed(seed)
    return create_dataset(
        spec.target_fn,
        n_var=spec.n_var,
        train_num=train_num,
        test_num=test_num,
        seed=seed,
        device="cpu",
    )


def _build_teacher_model(spec: _TaskSpec) -> MultKAN:
    return MultKAN(
        width=spec.width,
        grid=5,
        k=3,
        auto_save=False,
        device="cpu",
    )


def _train_teacher_model(
    spec: _TaskSpec,
    dataset: dict[str, torch.Tensor],
    *,
    train_steps: int,
    lr: float,
    lamb: float,
) -> MultKAN:
    model = _build_teacher_model(spec)
    model.fit(
        dataset,
        opt="Adam",
        steps=train_steps,
        lr=lr,
        update_grid=False,
        batch=-1,
        lamb=lamb,
        log=max(train_steps + 1, 999999),
    )
    return model


def _build_teacher_cache_identity(
    *,
    spec: _TaskSpec,
    seed: int,
    train_num: int,
    test_num: int,
    train_steps: int,
    lr: float,
    lamb: float,
    profile_name: str,
    cache_version: str,
) -> tuple[str, dict[str, object]]:
    payload: dict[str, object] = {
        "task": spec.name,
        "seed": int(seed),
        "n_var": int(spec.n_var),
        "width": list(spec.width),
        "train_num": int(train_num),
        "test_num": int(test_num),
        "train_steps": int(train_steps),
        "lr": float(lr),
        "lamb": float(lamb),
        "profile": profile_name,
        "cache_version": cache_version,
    }
    serialized = json.dumps(payload, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    digest = hashlib.sha256(serialized.encode("utf-8")).hexdigest()[:16]
    return f"{spec.name}_seed{seed}_{digest}", payload


def _acquire_lock(lock_path: Path, *, timeout_s: float = 120.0) -> bool:
    start = time.perf_counter()
    while True:
        try:
            fd = os.open(str(lock_path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.close(fd)
            return True
        except FileExistsError:
            if (time.perf_counter() - start) >= timeout_s:
                return False
            time.sleep(0.1)


def _release_lock(lock_path: Path) -> None:
    try:
        lock_path.unlink()
    except FileNotFoundError:
        pass


def _write_json_atomic(path: Path, payload: dict[str, object]) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    tmp.replace(path)


def _write_torch_state_atomic(path: Path, state_dict: dict[str, torch.Tensor]) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    torch.save(state_dict, tmp)
    tmp.replace(path)


def _resolve_teacher_model_with_cache(
    *,
    spec: _TaskSpec,
    seed: int,
    train_num: int,
    test_num: int,
    train_steps: int,
    lr: float,
    lamb: float,
    profile_name: str,
    cache_dir: Path,
    cache_mode: str,
    cache_version: str,
    lock_timeout_s: float = 120.0,
) -> tuple[MultKAN, dict[str, torch.Tensor], dict[str, object]]:
    if cache_mode not in _TEACHER_CACHE_MODES:
        raise ValueError(f"Unsupported teacher cache mode: {cache_mode}")

    dataset = _build_teacher_dataset(
        spec,
        seed=seed,
        train_num=train_num,
        test_num=test_num,
    )
    cache_key, cache_payload = _build_teacher_cache_identity(
        spec=spec,
        seed=seed,
        train_num=train_num,
        test_num=test_num,
        train_steps=train_steps,
        lr=lr,
        lamb=lamb,
        profile_name=profile_name,
        cache_version=cache_version,
    )

    cache_root = cache_dir / cache_key
    state_path = cache_root / "teacher_state.pt"
    meta_path = cache_root / "teacher_meta.json"
    lock_path = cache_root / "teacher_cache.lock"

    def _train() -> MultKAN:
        return _train_teacher_model(
            spec,
            dataset,
            train_steps=train_steps,
            lr=lr,
            lamb=lamb,
        )

    if cache_mode in {"readwrite", "readonly"} and state_path.exists() and meta_path.exists():
        try:
            model = _build_teacher_model(spec)
            state = torch.load(state_path, map_location="cpu")
            model.load_state_dict(state)
            return model, dataset, {
                "teacher_cache_hit": True,
                "teacher_cache_key": cache_key,
                "teacher_cache_path": str(cache_root),
                "teacher_cache_mode": cache_mode,
                "teacher_cache_status": "hit",
            }
        except Exception as exc:
            cache_load_error = f"{type(exc).__name__}: {exc}"
        else:  # pragma: no cover
            cache_load_error = ""
    else:
        cache_load_error = ""

    if cache_mode == "off":
        model = _train()
        return model, dataset, {
            "teacher_cache_hit": False,
            "teacher_cache_key": cache_key,
            "teacher_cache_path": str(cache_root),
            "teacher_cache_mode": cache_mode,
            "teacher_cache_status": "off_no_cache",
        }

    if cache_mode == "readonly":
        model = _train()
        status = "readonly_miss_no_write"
        if cache_load_error:
            status = f"readonly_load_error_no_write ({cache_load_error})"
        return model, dataset, {
            "teacher_cache_hit": False,
            "teacher_cache_key": cache_key,
            "teacher_cache_path": str(cache_root),
            "teacher_cache_mode": cache_mode,
            "teacher_cache_status": status,
        }

    model = _train()
    cache_root.mkdir(parents=True, exist_ok=True)
    lock_acquired = _acquire_lock(lock_path, timeout_s=lock_timeout_s)
    if lock_acquired:
        try:
            state_dict = {key: value.detach().cpu() for key, value in model.state_dict().items()}
            _write_torch_state_atomic(state_path, state_dict)
            _write_json_atomic(
                meta_path,
                {
                    "cache_key": cache_key,
                    "cache_payload": cache_payload,
                    "cache_mode_written_by": cache_mode,
                    "generated_at_utc": datetime.now(timezone.utc).isoformat(),
                },
            )
            status = "refresh_write" if cache_mode == "refresh" else "miss_write"
            if cache_load_error:
                status = f"{status}_after_load_error"
        finally:
            _release_lock(lock_path)
    else:
        status = "write_skipped_lock_timeout"
        if cache_load_error:
            status = f"{status}_after_load_error"

    return model, dataset, {
        "teacher_cache_hit": False,
        "teacher_cache_key": cache_key,
        "teacher_cache_path": str(cache_root),
        "teacher_cache_mode": cache_mode,
        "teacher_cache_status": status,
    }


def _serialize_formula_list(formulas: list[str]) -> str:
    return " || ".join(formulas)


def _compute_target_mse_and_r2(prediction: torch.Tensor, target: torch.Tensor) -> tuple[float, float]:
    mse = float(torch.mean((prediction - target).pow(2)).item())
    target_centered = target - torch.mean(target, dim=0, keepdim=True)
    ss_tot = float(torch.sum(target_centered.pow(2)).item())
    if ss_tot <= 1e-12:
        return mse, float("nan")
    ss_res = float(torch.sum((prediction - target).pow(2)).item())
    r2 = 1.0 - (ss_res / ss_tot)
    return mse, float(r2)


def _build_teacher_quality_gate_result(
    *,
    teacher_test_mse: float,
    teacher_test_r2: float,
    max_test_mse: float,
    min_test_r2: float,
) -> tuple[bool, str]:
    gate_failures: list[str] = []
    if not math.isfinite(teacher_test_mse) or teacher_test_mse > max_test_mse:
        gate_failures.append(f"teacher_test_mse={teacher_test_mse:.6g} > {max_test_mse:.6g}")
    if not math.isfinite(teacher_test_r2) or teacher_test_r2 < min_test_r2:
        gate_failures.append(f"teacher_test_r2={teacher_test_r2:.6g} < {min_test_r2:.6g}")
    if gate_failures:
        return False, "; ".join(gate_failures)
    return True, ""


def _build_skipped_symbolic_metrics(*, reason: str) -> dict[str, object]:
    nan_metrics = {
        "candidate_generation_wall_time_s": float("nan"),
        "replay_rerank_wall_time_s": float("nan"),
        "symbolic_wall_time_s": float("nan"),
        "baseline_symbolic_wall_time_s": float("nan"),
        "symbolic_wall_time_delta_s": float("nan"),
        "symbolic_speedup_vs_baseline": float("nan"),
        "replay_imitation_gap": float("nan"),
        "final_mse_loss_shift": float("nan"),
        "baseline_mse": float("nan"),
        "icbr_mse": float("nan"),
        "teacher_target_mse": float("nan"),
        "teacher_target_r2": float("nan"),
        "baseline_target_mse": float("nan"),
        "baseline_target_r2": float("nan"),
        "icbr_target_mse": float("nan"),
        "icbr_target_r2": float("nan"),
        "symbolic_target_mse_shift": float("nan"),
        "symbolic_target_r2_shift": float("nan"),
    }
    return {
        **nan_metrics,
        "formula_validation_result": False,
        "baseline_formula_validation_result": False,
        "icbr_formula_validation_result": False,
        "baseline_formula_raw": [],
        "baseline_formula_display": [],
        "icbr_formula_raw": [],
        "icbr_formula_display": [],
        "baseline_formula_error": f"skipped_by_teacher_quality_gate: {reason}",
        "icbr_formula_error": f"skipped_by_teacher_quality_gate: {reason}",
    }


def _describe(values: list[float]) -> dict[str, float]:
    if not values:
        return {
            "count": 0.0,
            "mean": float("nan"),
            "median": float("nan"),
            "std": float("nan"),
            "min": float("nan"),
            "max": float("nan"),
        }
    return {
        "count": float(len(values)),
        "mean": float(statistics.mean(values)),
        "median": float(statistics.median(values)),
        "std": float(statistics.stdev(values)) if len(values) > 1 else 0.0,
        "min": float(min(values)),
        "max": float(max(values)),
    }


def _bootstrap_mean_ci(
    values: list[float],
    *,
    iterations: int = 2000,
    alpha: float = 0.05,
    seed: int = 0,
) -> tuple[float, float]:
    if not values:
        return float("nan"), float("nan")

    rng = random.Random(seed)
    n = len(values)
    bootstrap_means: list[float] = []
    for _ in range(iterations):
        sample = [values[rng.randrange(n)] for _ in range(n)]
        bootstrap_means.append(float(statistics.mean(sample)))
    bootstrap_means.sort()

    lower_idx = int((alpha / 2.0) * (iterations - 1))
    upper_idx = int((1.0 - alpha / 2.0) * (iterations - 1))
    return bootstrap_means[lower_idx], bootstrap_means[upper_idx]


def _sign_test_pvalue_two_sided(successes: int, total: int) -> float:
    if total <= 0:
        return float("nan")
    tail_count = sum(math.comb(total, k) for k in range(0, min(successes, total - successes) + 1))
    return float(min(1.0, 2.0 * tail_count / (2**total)))


def _build_metric_stats(rows: list[dict[str, object]]) -> dict[str, dict[str, float]]:
    stats: dict[str, dict[str, float]] = {}
    for metric in _NUMERIC_METRICS:
        values = []
        for row in rows:
            value = float(row[metric])
            if math.isfinite(value):
                values.append(value)
        stats[metric] = _describe(values)
    for metric in _BOOLEAN_METRICS:
        values = [1.0 if bool(row[metric]) else 0.0 for row in rows]
        stats[metric] = _describe(values)
    return stats


def _build_significance(
    rows: list[dict[str, object]],
    *,
    task_label: str,
) -> dict[str, dict[str, float | int | str | list[float]]]:
    by_metric: dict[str, dict[str, float | int | str | list[float]]] = {}
    for metric_name, favorable_direction in _SIGNIFICANCE_DIRECTIONS.items():
        deltas = []
        for row in rows:
            value = float(row[metric_name])
            if math.isfinite(value):
                deltas.append(value)
        effective = [value for value in deltas if abs(value) > 1e-12]
        tie_count = len(deltas) - len(effective)

        if favorable_direction == "positive":
            improved_count = sum(1 for value in effective if value > 0.0)
        else:
            improved_count = sum(1 for value in effective if value < 0.0)
        worsened_count = len(effective) - improved_count

        ci_seed = sum(ord(ch) for ch in f"{task_label}:{metric_name}") + len(deltas) * 97
        ci_low, ci_high = _bootstrap_mean_ci(deltas, seed=ci_seed)
        p_value = _sign_test_pvalue_two_sided(improved_count, len(effective))

        by_metric[metric_name] = {
            "favorable_direction": favorable_direction,
            "sample_count": len(rows),
            "finite_count": len(deltas),
            "effective_count": len(effective),
            "tie_count": tie_count,
            "improved_count": improved_count,
            "worsened_count": worsened_count,
            "delta_stats": _describe(deltas),
            "mean_delta_ci95": [float(ci_low), float(ci_high)],
            "sign_test_pvalue_two_sided": float(p_value),
        }
    return by_metric


def _build_task_stats_rows(
    *,
    tasks: list[str],
    rows: list[dict[str, object]],
    by_task_metrics: dict[str, dict[str, dict[str, float]]],
    overall_metrics: dict[str, dict[str, float]],
) -> list[dict[str, object]]:
    stats_rows: list[dict[str, object]] = []
    for metric_name, metric_stats in overall_metrics.items():
        stats_rows.append(
            {
                "scope": "overall",
                "task": "__all__",
                "metric": metric_name,
                **metric_stats,
            }
        )
    for task in tasks:
        task_rows = [row for row in rows if row["task"] == task]
        for metric_name, metric_stats in by_task_metrics[task].items():
            stats_rows.append(
                {
                    "scope": "task",
                    "task": task,
                    "metric": metric_name,
                    "seed_count": len(task_rows),
                    **metric_stats,
                }
            )
    return stats_rows


def _build_significance_rows(
    *,
    tasks: list[str],
    by_task_significance: dict[str, dict[str, dict[str, float | int | str | list[float]]]],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for task in tasks:
        task_sig = by_task_significance[task]
        for metric_name, item in task_sig.items():
            ci = item["mean_delta_ci95"]
            rows.append(
                {
                    "task": task,
                    "metric": metric_name,
                    "favorable_direction": item["favorable_direction"],
                    "sample_count": item["sample_count"],
                    "finite_count": item["finite_count"],
                    "effective_count": item["effective_count"],
                    "tie_count": item["tie_count"],
                    "improved_count": item["improved_count"],
                    "worsened_count": item["worsened_count"],
                    "mean_delta": item["delta_stats"]["mean"],
                    "median_delta": item["delta_stats"]["median"],
                    "std_delta": item["delta_stats"]["std"],
                    "min_delta": item["delta_stats"]["min"],
                    "max_delta": item["delta_stats"]["max"],
                    "mean_delta_ci95_low": ci[0],
                    "mean_delta_ci95_high": ci[1],
                    "sign_test_pvalue_two_sided": item["sign_test_pvalue_two_sided"],
                }
            )
    return rows


def _write_task_stats_csv(
    path: Path,
    stats_rows: list[dict[str, object]],
) -> None:
    fieldnames = [
        "scope",
        "task",
        "metric",
        "seed_count",
        "count",
        "mean",
        "median",
        "std",
        "min",
        "max",
    ]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in stats_rows:
            writer.writerow({name: row.get(name, "") for name in fieldnames})


def _write_significance_csv(
    path: Path,
    significance_rows: list[dict[str, object]],
) -> None:
    if not significance_rows:
        return
    fieldnames = list(significance_rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(significance_rows)


def _generate_visualizations(
    *,
    output_dir: Path,
    tasks: list[str],
    by_task_rows: dict[str, list[dict[str, object]]],
) -> dict[str, object]:
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception as exc:  # pragma: no cover - depends on local matplotlib availability
        return {"enabled": False, "error": f"{type(exc).__name__}: {exc}", "files": []}

    created_files: list[str] = []

    def _finite_metric_values(task: str, metric: str) -> list[float]:
        values: list[float] = []
        for row in by_task_rows[task]:
            value = float(row[metric])
            if math.isfinite(value):
                values.append(value)
        return values

    def _safe_mean_std(values: list[float]) -> tuple[float, float]:
        if not values:
            return float("nan"), float("nan")
        if len(values) == 1:
            return float(values[0]), 0.0
        return float(statistics.mean(values)), float(statistics.stdev(values))

    fig, ax = plt.subplots(figsize=(10, 4.5))
    x_positions = list(range(len(tasks)))
    baseline_mean, baseline_std, icbr_mean, icbr_std = [], [], [], []
    for task in tasks:
        base_mean, base_std = _safe_mean_std(_finite_metric_values(task, "baseline_symbolic_wall_time_s"))
        icbr_m, icbr_s = _safe_mean_std(_finite_metric_values(task, "symbolic_wall_time_s"))
        baseline_mean.append(base_mean)
        baseline_std.append(base_std)
        icbr_mean.append(icbr_m)
        icbr_std.append(icbr_s)
    if not all(math.isfinite(value) for value in (baseline_mean + baseline_std + icbr_mean + icbr_std)):
        plt.close(fig)
        return {
            "enabled": False,
            "error": "Insufficient finite symbolic timing metrics for plot generation (likely skipped by teacher quality gate).",
            "files": created_files,
        }
    bar_width = 0.36
    ax.bar(
        [x - bar_width / 2.0 for x in x_positions],
        baseline_mean,
        width=bar_width,
        yerr=baseline_std,
        capsize=4,
        label="Baseline symbolic time",
    )
    ax.bar(
        [x + bar_width / 2.0 for x in x_positions],
        icbr_mean,
        width=bar_width,
        yerr=icbr_std,
        capsize=4,
        label="ICBR symbolic time",
    )
    ax.set_xticks(x_positions)
    ax.set_xticklabels(tasks, rotation=20)
    ax.set_ylabel("seconds")
    ax.set_title("Symbolic Wall Time by Task (mean ± std)")
    ax.legend()
    time_plot = output_dir / "icbr_benchmark_symbolic_time_errorbar.png"
    fig.tight_layout()
    fig.savefig(time_plot, dpi=160)
    plt.close(fig)
    created_files.append(str(time_plot))

    fig, ax = plt.subplots(figsize=(10, 4.5))
    speedup_data = [_finite_metric_values(task, "symbolic_speedup_vs_baseline") for task in tasks]
    if any(len(values) == 0 for values in speedup_data):
        plt.close(fig)
        return {
            "enabled": False,
            "error": "Insufficient finite symbolic metrics for plot generation (likely skipped by teacher quality gate).",
            "files": created_files,
        }
    ax.boxplot(speedup_data, labels=tasks, showmeans=True)
    ax.set_ylabel("speedup x")
    ax.set_title("ICBR Speedup vs Baseline (seed distribution)")
    ax.grid(axis="y", alpha=0.3)
    speedup_plot = output_dir / "icbr_benchmark_speedup_boxplot.png"
    fig.tight_layout()
    fig.savefig(speedup_plot, dpi=160)
    plt.close(fig)
    created_files.append(str(speedup_plot))

    fig, ax = plt.subplots(figsize=(10, 4.5))
    mse_shift_data = [_finite_metric_values(task, "final_mse_loss_shift") for task in tasks]
    if any(len(values) == 0 for values in mse_shift_data):
        plt.close(fig)
        return {
            "enabled": False,
            "error": "Insufficient finite mse shift metrics for plot generation (likely skipped by teacher quality gate).",
            "files": created_files,
        }
    ax.boxplot(mse_shift_data, labels=tasks, showmeans=True)
    ax.axhline(0.0, linestyle="--", linewidth=1.0, color="black", alpha=0.7)
    ax.set_ylabel("icbr_mse - baseline_mse")
    ax.set_title("MSE Shift by Task (seed distribution)")
    ax.grid(axis="y", alpha=0.3)
    mse_plot = output_dir / "icbr_benchmark_mse_shift_boxplot.png"
    fig.tight_layout()
    fig.savefig(mse_plot, dpi=160)
    plt.close(fig)
    created_files.append(str(mse_plot))

    return {"enabled": True, "error": None, "files": created_files}


def run_benchmark(
    *,
    tasks: list[str],
    seeds: list[int],
    output_dir: Path,
    train_num: int,
    test_num: int,
    train_steps: int,
    lr: float,
    lamb: float,
    topk: int,
    grid_number: int,
    iteration: int,
    teacher_max_test_mse: float,
    teacher_min_test_r2: float,
    teacher_cache_dir: Path = Path("outputs/teacher_cache"),
    teacher_cache_mode: str = "readwrite",
    teacher_cache_version: str = "v1",
    profile_name: str = "custom",
    profile_defaults: dict[str, float | int] | None = None,
    profile_overrides: dict[str, bool] | None = None,
    make_plots: bool,
    quiet: bool,
) -> dict[str, object]:
    specs = _task_specs()
    invalid = [name for name in tasks if name not in specs]
    if invalid:
        raise ValueError(f"Unknown benchmark tasks: {invalid}")

    output_dir.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, object]] = []

    for task_name in tasks:
        spec = specs[task_name]
        for seed in seeds:
            effective_topk = int(spec.icbr_topk) if spec.icbr_topk is not None else int(topk)
            effective_teacher_max_test_mse = (
                float(spec.teacher_max_test_mse)
                if spec.teacher_max_test_mse is not None
                else float(teacher_max_test_mse)
            )
            effective_teacher_min_test_r2 = (
                float(spec.teacher_min_test_r2)
                if spec.teacher_min_test_r2 is not None
                else float(teacher_min_test_r2)
            )
            model, dataset, cache_info = _resolve_teacher_model_with_cache(
                spec=spec,
                seed=seed,
                train_num=train_num,
                test_num=test_num,
                train_steps=train_steps,
                lr=lr,
                lamb=lamb,
                profile_name=profile_name,
                cache_dir=teacher_cache_dir,
                cache_mode=teacher_cache_mode,
                cache_version=teacher_cache_version,
            )
            with torch.no_grad():
                teacher_test_pred = model(dataset["test_input"])
                if isinstance(teacher_test_pred, tuple):
                    teacher_test_pred = teacher_test_pred[0]
                teacher_test_pred = teacher_test_pred.detach()
            teacher_test_mse, teacher_test_r2 = _compute_target_mse_and_r2(
                teacher_test_pred,
                dataset["test_label"],
            )
            teacher_quality_gate_pass, teacher_quality_gate_reason = _build_teacher_quality_gate_result(
                teacher_test_mse=teacher_test_mse,
                teacher_test_r2=teacher_test_r2,
                max_test_mse=effective_teacher_max_test_mse,
                min_test_r2=effective_teacher_min_test_r2,
            )

            if teacher_quality_gate_pass:
                metrics = benchmark_icbr_vs_baseline(
                    model,
                    calibration_split={
                        "test_input": dataset["test_input"],
                        "test_label": dataset["test_label"],
                    },
                    calibration_target=dataset["test_label"],
                    lib=spec.lib,
                    topk=effective_topk,
                    a_range=(-5.0, 5.0),
                    b_range=(-5.0, 5.0),
                    grid_number=grid_number,
                    iteration=iteration,
                )
            else:
                metrics = _build_skipped_symbolic_metrics(reason=teacher_quality_gate_reason)
            row = {
                "task": task_name,
                "seed": seed,
                "n_var": spec.n_var,
                "width": list(spec.width),
                "lib": list(spec.lib) if spec.lib is not None else ["__FULL_SYMBOLIC_LIB__"],
                "icbr_topk_used": effective_topk,
                "teacher_test_mse": teacher_test_mse,
                "teacher_test_r2": teacher_test_r2,
                "teacher_max_test_mse_threshold": effective_teacher_max_test_mse,
                "teacher_min_test_r2_threshold": effective_teacher_min_test_r2,
                "teacher_quality_gate_pass": teacher_quality_gate_pass,
                "teacher_quality_gate_reason": teacher_quality_gate_reason,
                "teacher_cache_hit": bool(cache_info["teacher_cache_hit"]),
                "teacher_cache_key": str(cache_info["teacher_cache_key"]),
                "teacher_cache_path": str(cache_info["teacher_cache_path"]),
                "teacher_cache_mode": str(cache_info["teacher_cache_mode"]),
                "teacher_cache_status": str(cache_info["teacher_cache_status"]),
                **metrics,
            }
            rows.append(row)
            if not quiet:
                if teacher_quality_gate_pass:
                    print(
                        f"[icbr-benchmark] task={task_name} seed={seed} "
                        f"cache_hit={bool(cache_info['teacher_cache_hit'])} "
                        f"teacher_mse={teacher_test_mse:.6e} teacher_r2={teacher_test_r2:.4f} "
                        f"icbr_symbolic={metrics['symbolic_wall_time_s']:.4f}s "
                        f"baseline_symbolic={metrics['baseline_symbolic_wall_time_s']:.4f}s "
                        f"speedup={metrics['symbolic_speedup_vs_baseline']:.2f}x "
                        f"mse_shift={metrics['final_mse_loss_shift']:.6e} "
                        f"target_mse_shift={metrics['symbolic_target_mse_shift']:.6e}"
                    )
                else:
                    print(
                        f"[icbr-benchmark] task={task_name} seed={seed} "
                        f"cache_hit={bool(cache_info['teacher_cache_hit'])} "
                        f"teacher_mse={teacher_test_mse:.6e} teacher_r2={teacher_test_r2:.4f} "
                        f"skipped_symbolic_by_gate reason={teacher_quality_gate_reason}"
                    )

    rows_csv = output_dir / "icbr_benchmark_rows.csv"
    row_fieldnames = [
        "task",
        "seed",
        "n_var",
        "width",
        "lib",
        "icbr_topk_used",
        "teacher_test_mse",
        "teacher_test_r2",
        "teacher_max_test_mse_threshold",
        "teacher_min_test_r2_threshold",
        "teacher_quality_gate_pass",
        "teacher_quality_gate_reason",
        "teacher_cache_hit",
        "teacher_cache_key",
        "teacher_cache_path",
        "teacher_cache_mode",
        "teacher_cache_status",
        "candidate_generation_wall_time_s",
        "replay_rerank_wall_time_s",
        "symbolic_wall_time_s",
        "baseline_symbolic_wall_time_s",
        "symbolic_wall_time_delta_s",
        "symbolic_speedup_vs_baseline",
        "replay_imitation_gap",
        "final_mse_loss_shift",
        "baseline_mse",
        "icbr_mse",
        "teacher_target_mse",
        "teacher_target_r2",
        "baseline_target_mse",
        "baseline_target_r2",
        "icbr_target_mse",
        "icbr_target_r2",
        "symbolic_target_mse_shift",
        "symbolic_target_r2_shift",
        "formula_validation_result",
        "baseline_formula_validation_result",
        "icbr_formula_validation_result",
        "baseline_formula_error",
        "icbr_formula_error",
        "baseline_formula_raw",
        "baseline_formula_display",
        "icbr_formula_raw",
        "icbr_formula_display",
    ]
    with rows_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=row_fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    "task": row["task"],
                    "seed": row["seed"],
                    "n_var": row["n_var"],
                    "width": json.dumps(row["width"], ensure_ascii=False),
                    "lib": json.dumps(row["lib"], ensure_ascii=False),
                    "icbr_topk_used": row["icbr_topk_used"],
                    "teacher_test_mse": row["teacher_test_mse"],
                    "teacher_test_r2": row["teacher_test_r2"],
                    "teacher_max_test_mse_threshold": row["teacher_max_test_mse_threshold"],
                    "teacher_min_test_r2_threshold": row["teacher_min_test_r2_threshold"],
                    "teacher_quality_gate_pass": row["teacher_quality_gate_pass"],
                    "teacher_quality_gate_reason": row["teacher_quality_gate_reason"],
                    "teacher_cache_hit": row["teacher_cache_hit"],
                    "teacher_cache_key": row["teacher_cache_key"],
                    "teacher_cache_path": row["teacher_cache_path"],
                    "teacher_cache_mode": row["teacher_cache_mode"],
                    "teacher_cache_status": row["teacher_cache_status"],
                    "candidate_generation_wall_time_s": row["candidate_generation_wall_time_s"],
                    "replay_rerank_wall_time_s": row["replay_rerank_wall_time_s"],
                    "symbolic_wall_time_s": row["symbolic_wall_time_s"],
                    "baseline_symbolic_wall_time_s": row["baseline_symbolic_wall_time_s"],
                    "symbolic_wall_time_delta_s": row["symbolic_wall_time_delta_s"],
                    "symbolic_speedup_vs_baseline": row["symbolic_speedup_vs_baseline"],
                    "replay_imitation_gap": row["replay_imitation_gap"],
                    "final_mse_loss_shift": row["final_mse_loss_shift"],
                    "baseline_mse": row["baseline_mse"],
                    "icbr_mse": row["icbr_mse"],
                    "teacher_target_mse": row["teacher_target_mse"],
                    "teacher_target_r2": row["teacher_target_r2"],
                    "baseline_target_mse": row["baseline_target_mse"],
                    "baseline_target_r2": row["baseline_target_r2"],
                    "icbr_target_mse": row["icbr_target_mse"],
                    "icbr_target_r2": row["icbr_target_r2"],
                    "symbolic_target_mse_shift": row["symbolic_target_mse_shift"],
                    "symbolic_target_r2_shift": row["symbolic_target_r2_shift"],
                    "formula_validation_result": row["formula_validation_result"],
                    "baseline_formula_validation_result": row["baseline_formula_validation_result"],
                    "icbr_formula_validation_result": row["icbr_formula_validation_result"],
                    "baseline_formula_error": row["baseline_formula_error"],
                    "icbr_formula_error": row["icbr_formula_error"],
                    "baseline_formula_raw": _serialize_formula_list(row["baseline_formula_raw"]),
                    "baseline_formula_display": _serialize_formula_list(row["baseline_formula_display"]),
                    "icbr_formula_raw": _serialize_formula_list(row["icbr_formula_raw"]),
                    "icbr_formula_display": _serialize_formula_list(row["icbr_formula_display"]),
                }
            )

    by_task_rows = {task_name: [row for row in rows if row["task"] == task_name] for task_name in tasks}
    by_task_metrics = {task_name: _build_metric_stats(task_rows) for task_name, task_rows in by_task_rows.items()}
    overall_metrics = _build_metric_stats(rows)
    by_task_significance = {
        task_name: _build_significance(task_rows, task_label=task_name) for task_name, task_rows in by_task_rows.items()
    }
    overall_significance = _build_significance(rows, task_label="__overall__")

    task_stats_rows = _build_task_stats_rows(
        tasks=tasks,
        rows=rows,
        by_task_metrics=by_task_metrics,
        overall_metrics=overall_metrics,
    )
    task_stats_csv = output_dir / "icbr_benchmark_task_stats.csv"
    _write_task_stats_csv(task_stats_csv, task_stats_rows)

    significance_rows = _build_significance_rows(tasks=tasks, by_task_significance=by_task_significance)
    significance_csv = output_dir / "icbr_benchmark_significance.csv"
    _write_significance_csv(significance_csv, significance_rows)

    visualization = {"enabled": False, "error": "Disabled by --no-plots", "files": []}
    if make_plots:
        visualization = _generate_visualizations(output_dir=output_dir, tasks=tasks, by_task_rows=by_task_rows)

    summary = {
        "metadata": {
            "generated_at_utc": datetime.now(timezone.utc).isoformat(),
            "benchmark_name": "icbr_phase1_cpu_extended_validation",
            "report_version": "2.0",
        },
        "config": {
            "tasks": tasks,
            "seeds": seeds,
            "profile": {
                "name": profile_name,
                "defaults": profile_defaults if profile_defaults is not None else {},
                "overrides": profile_overrides if profile_overrides is not None else {},
            },
            "train_num": train_num,
            "test_num": test_num,
            "train_steps": train_steps,
            "lr": lr,
            "lamb": lamb,
            "topk": topk,
            "grid_number": grid_number,
            "iteration": iteration,
            "teacher_quality_gate": {
                "enabled": True,
                "teacher_max_test_mse_default": float(teacher_max_test_mse),
                "teacher_min_test_r2_default": float(teacher_min_test_r2),
                "task_overrides": {
                    task_name: {
                        "teacher_max_test_mse": (
                            float(specs[task_name].teacher_max_test_mse)
                            if specs[task_name].teacher_max_test_mse is not None
                            else float(teacher_max_test_mse)
                        ),
                        "teacher_min_test_r2": (
                            float(specs[task_name].teacher_min_test_r2)
                            if specs[task_name].teacher_min_test_r2 is not None
                            else float(teacher_min_test_r2)
                        ),
                    }
                    for task_name in tasks
                },
                "policy": "skip_symbolic_comparison_when_teacher_quality_fails",
            },
            "teacher_cache": {
                "dir": str(teacher_cache_dir),
                "mode": teacher_cache_mode,
                "version": teacher_cache_version,
                "modes_supported": sorted(_TEACHER_CACHE_MODES),
            },
            "output_dir": str(output_dir),
            "plots_enabled": make_plots,
            "task_topk_overrides": {
                task_name: int(specs[task_name].icbr_topk)
                for task_name in tasks
                if specs[task_name].icbr_topk is not None
            },
            "task_lib_mode": {
                task_name: ("full_symbolic_lib" if specs[task_name].lib is None else "task_subset")
                for task_name in tasks
            },
        },
        "rows": rows,
        "aggregates": {
            "overall": {
                "row_count": len(rows),
                "metrics": overall_metrics,
                "significance": overall_significance,
            },
            "by_task": {
                task_name: {
                    "row_count": len(by_task_rows[task_name]),
                    "metrics": by_task_metrics[task_name],
                    "significance": by_task_significance[task_name],
                }
                for task_name in tasks
            },
        },
        "artifacts": {
            "rows_csv": str(rows_csv),
            "task_stats_csv": str(task_stats_csv),
            "significance_csv": str(significance_csv),
            "visualizations": visualization,
        },
        "notes": {
            "field_guide": {
                "symbolic_wall_time_delta_s": "baseline_symbolic_wall_time_s - icbr_symbolic_wall_time_s",
                "final_mse_loss_shift": "icbr_mse - baseline_mse; negative means ICBR has lower MSE",
                "teacher_test_mse": "Teacher numeric model MSE against real test labels before symbolic fitting.",
                "teacher_test_r2": "Teacher numeric model R2 against real test labels before symbolic fitting.",
                "teacher_cache_hit": "Whether teacher model was loaded from persistent cache.",
                "symbolic_target_mse_shift": "icbr_target_mse - baseline_target_mse; negative means ICBR is closer to real targets.",
                "symbolic_target_r2_shift": "icbr_target_r2 - baseline_target_r2; positive means ICBR has higher target R2.",
                "stats_schema": "Each metric includes count | mean | median | std | min | max",
            },
            "significance_guide": {
                "sign_test_pvalue_two_sided": "Two-sided sign test p-value on non-tie seeds.",
                "mean_delta_ci95": "Bootstrap 95% CI of mean delta across seeds.",
            },
            "teacher_quality_gate": {
                "pass_rule": "teacher_test_mse <= threshold_mse AND teacher_test_r2 >= threshold_r2",
                "failure_policy": "Skip baseline/ICBR symbolic comparison for that row and keep explicit gate reason.",
            },
            "teacher_cache": {
                "cache_key_rule": "hash(task, seed, width, train_num, test_num, train_steps, lr, lamb, profile, cache_version)",
                "modes": {
                    "readwrite": "Read cache when available; train+write on miss.",
                    "readonly": "Read cache only; train without writing on miss.",
                    "refresh": "Ignore old cache and retrain, then overwrite cache.",
                    "off": "Disable cache and always train.",
                },
            },
            "extensibility": [
                "Add new tasks in _task_specs() with target_fn, width, and symbolic lib.",
                "Rows-level details are preserved for error bars and downstream statistical tests.",
                "Task stats CSV and significance CSV can be consumed by external plotting/report tools.",
                "Teacher cache key version can be bumped with --teacher-cache-version for compatibility control.",
            ],
        },
    }
    summary_json_path = output_dir / "icbr_benchmark_summary.json"
    summary_json_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    md_lines: list[str] = [
        "# ICBR Benchmark Summary",
        "",
        "## Run Config",
        "",
        f"- Profile: {summary['config']['profile']['name']}",
        f"- Tasks: {', '.join(tasks)}",
        f"- Seeds: {', '.join(str(seed) for seed in seeds)}",
        f"- Train/Test samples per task: {train_num}/{test_num}",
        f"- Train steps: {train_steps}, lr: {lr}, lamb: {lamb}",
        f"- Teacher cache: mode={teacher_cache_mode}, dir={teacher_cache_dir}, version={teacher_cache_version}",
        f"- ICBR shortlist topk: {topk}, grid_number: {grid_number}, iteration: {iteration}",
        "",
        "## Task-Level Aggregate Stats",
        "",
        "| task | n | teacher_cache_hit_mean | teacher_mse_mean | teacher_r2_mean | teacher_gate_pass_mean | baseline_symbolic_mean | icbr_symbolic_mean | delta_mean | delta_median | speedup_mean | speedup_median | mse_shift_mean | target_mse_shift_mean | formula_pass_mean |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for task_name in tasks:
        task_item = summary["aggregates"]["by_task"][task_name]
        metrics = task_item["metrics"]
        md_lines.append(
            "| "
            + f"{task_name} | "
            + f"{task_item['row_count']} | "
            + f"{metrics['teacher_cache_hit']['mean']:.4f} | "
            + f"{metrics['teacher_test_mse']['mean']:.6e} | "
            + f"{metrics['teacher_test_r2']['mean']:.6f} | "
            + f"{metrics['teacher_quality_gate_pass']['mean']:.4f} | "
            + f"{metrics['baseline_symbolic_wall_time_s']['mean']:.6f} | "
            + f"{metrics['symbolic_wall_time_s']['mean']:.6f} | "
            + f"{metrics['symbolic_wall_time_delta_s']['mean']:.6f} | "
            + f"{metrics['symbolic_wall_time_delta_s']['median']:.6f} | "
            + f"{metrics['symbolic_speedup_vs_baseline']['mean']:.4f} | "
            + f"{metrics['symbolic_speedup_vs_baseline']['median']:.4f} | "
            + f"{metrics['final_mse_loss_shift']['mean']:.6e} | "
            + f"{metrics['symbolic_target_mse_shift']['mean']:.6e} | "
            + f"{metrics['formula_validation_result']['mean']:.4f} |"
        )
    md_lines.append("")

    md_lines.extend(
        [
            "## Statistical Significance (by task)",
            "",
            "| task | metric | favorable_direction | n_total | n_finite | n_effective | improved | worsened | ties | p_value_two_sided | mean_delta_ci95 |",
            "|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|",
        ]
    )
    for task_name in tasks:
        sig_item = summary["aggregates"]["by_task"][task_name]["significance"]
        for metric_name in ["symbolic_wall_time_delta_s", "final_mse_loss_shift"]:
            metric_sig = sig_item[metric_name]
            ci = metric_sig["mean_delta_ci95"]
            md_lines.append(
                "| "
                + f"{task_name} | "
                + f"{metric_name} | "
                + f"{metric_sig['favorable_direction']} | "
                + f"{metric_sig['sample_count']} | "
                + f"{metric_sig['finite_count']} | "
                + f"{metric_sig['effective_count']} | "
                + f"{metric_sig['improved_count']} | "
                + f"{metric_sig['worsened_count']} | "
                + f"{metric_sig['tie_count']} | "
                + f"{metric_sig['sign_test_pvalue_two_sided']:.6f} | "
                + f"[{float(ci[0]):.6e}, {float(ci[1]):.6e}] |"
            )
    md_lines.append("")

    md_lines.extend(
        [
            "## Per-Run Performance Details",
            "",
            "| task | seed | cache_hit | cache_status | teacher_mse | teacher_r2 | teacher_gate | candidate_s | replay_s | baseline_symbolic_s | icbr_symbolic_s | speedup_x | baseline_mse | icbr_mse | mse_shift | baseline_target_mse | icbr_target_mse | target_mse_shift | formula_ok |",
            "|---|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for row in rows:
        md_lines.append(
            "| "
            + f"{row['task']} | {row['seed']} | "
            + f"{bool(row['teacher_cache_hit'])} | "
            + f"{row['teacher_cache_status']} | "
            + f"{float(row['teacher_test_mse']):.6e} | "
            + f"{float(row['teacher_test_r2']):.6f} | "
            + f"{bool(row['teacher_quality_gate_pass'])} | "
            + f"{float(row['candidate_generation_wall_time_s']):.6f} | "
            + f"{float(row['replay_rerank_wall_time_s']):.6f} | "
            + f"{float(row['baseline_symbolic_wall_time_s']):.6f} | "
            + f"{float(row['symbolic_wall_time_s']):.6f} | "
            + f"{float(row['symbolic_speedup_vs_baseline']):.4f} | "
            + f"{float(row['baseline_mse']):.6e} | "
            + f"{float(row['icbr_mse']):.6e} | "
            + f"{float(row['final_mse_loss_shift']):.6e} | "
            + f"{float(row['baseline_target_mse']):.6e} | "
            + f"{float(row['icbr_target_mse']):.6e} | "
            + f"{float(row['symbolic_target_mse_shift']):.6e} | "
            + f"{bool(row['formula_validation_result'])} |"
        )
    md_lines.append("")

    md_lines.append("## Formula Comparison")
    md_lines.append("")
    for row in rows:
        md_lines.append(f"### task={row['task']} seed={row['seed']}")
        md_lines.append("")
        md_lines.append(
            f"- Teacher cache: hit={bool(row['teacher_cache_hit'])}, "
            f"mode={row['teacher_cache_mode']}, status={row['teacher_cache_status']}"
        )
        md_lines.append(
            f"- Teacher quality gate: pass={bool(row['teacher_quality_gate_pass'])}; "
            f"reason=`{row['teacher_quality_gate_reason']}`"
        )
        md_lines.append(
            f"- Teacher target metrics: mse={float(row['teacher_target_mse']):.6e}, "
            f"r2={float(row['teacher_target_r2']):.6f}"
        )
        md_lines.append("- Baseline formula (display, rounded):")
        for expr in row["baseline_formula_display"]:
            md_lines.append(f"  - `{expr}`")
        md_lines.append("- ICBR formula (display, rounded):")
        for expr in row["icbr_formula_display"]:
            md_lines.append(f"  - `{expr}`")
        md_lines.append("- Baseline formula (raw):")
        for expr in row["baseline_formula_raw"]:
            md_lines.append(f"  - `{expr}`")
        md_lines.append("- ICBR formula (raw):")
        for expr in row["icbr_formula_raw"]:
            md_lines.append(f"  - `{expr}`")
        if row["baseline_formula_error"] or row["icbr_formula_error"]:
            md_lines.append(f"- Formula export error baseline={row['baseline_formula_error']}, icbr={row['icbr_formula_error']}")
        md_lines.append("")

    md_lines.extend(["## Visualization Summary", ""])
    if visualization["enabled"]:
        for path in visualization["files"]:
            rel = str(Path(path).relative_to(output_dir))
            md_lines.append(f"- `{rel}`")
    else:
        md_lines.append(f"- Visualization disabled: {visualization['error']}")
    md_lines.append("")

    md_lines.extend(
        [
            "## Extensibility Notes",
            "",
            "- 任务可扩展：在 `_task_specs()` 增加任务定义，即可复用统一导出与统计管线。",
            "- 统计可扩展：新增 benchmark 指标后，可自动进入 task stats（count/mean/median/std/min/max）。",
            "- 显著性可扩展：可在 `_SIGNIFICANCE_DIRECTIONS` 增加需要方向性判断的 delta 指标。",
            "- 门禁可扩展：可在 `_TaskSpec` 中为单任务覆盖 teacher MSE/R2 阈值。",
        ]
    )
    (output_dir / "icbr_benchmark_summary.md").write_text("\n".join(md_lines) + "\n", encoding="utf-8")

    return {"rows": rows, "summary": summary, "output_dir": str(output_dir)}


def _parse_int_list(text: str) -> list[int]:
    values = [item.strip() for item in text.split(",") if item.strip()]
    if not values:
        raise ValueError("Expected at least one integer value.")
    return [int(item) for item in values]


def _parse_str_list(text: str) -> list[str]:
    values = [item.strip() for item in text.split(",") if item.strip()]
    if not values:
        raise ValueError("Expected at least one task.")
    return values


def _resolve_training_config(
    *,
    profile: str,
    train_num: int | None,
    test_num: int | None,
    train_steps: int | None,
    lr: float | None,
    lamb: float | None,
) -> tuple[dict[str, float | int], dict[str, bool]]:
    if profile not in _BENCHMARK_PROFILES:
        raise ValueError(f"Unknown benchmark profile: {profile}")

    profile_defaults = _BENCHMARK_PROFILES[profile]
    resolved = {
        "train_num": int(profile_defaults["train_num"]) if train_num is None else int(train_num),
        "test_num": int(profile_defaults["test_num"]) if test_num is None else int(test_num),
        "train_steps": int(profile_defaults["train_steps"]) if train_steps is None else int(train_steps),
        "lr": float(profile_defaults["lr"]) if lr is None else float(lr),
        "lamb": float(profile_defaults["lamb"]) if lamb is None else float(lamb),
    }
    overridden = {
        "train_num": train_num is not None,
        "test_num": test_num is not None,
        "train_steps": train_steps is not None,
        "lr": lr is not None,
        "lamb": lamb is not None,
    }
    return resolved, overridden


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Run CPU benchmark for ICBR Phase I with extended multi-seed reporting.")
    parser.add_argument(
        "--profile",
        default="quick",
        choices=sorted(_BENCHMARK_PROFILES.keys()),
        help="Benchmark run profile: quick for smoke, quality for teacher-convergence verification.",
    )
    parser.add_argument(
        "--tasks",
        default="minimal,combo,poly_cubic,trig_interaction",
        help="Comma-separated tasks: minimal,combo,poly_cubic,trig_interaction",
    )
    parser.add_argument("--seeds", default="0,1,2,3,4,5,6,7,8,9", help="Comma-separated integer seeds")
    parser.add_argument("--output-dir", default="outputs/icbr_benchmark_extended", help="Output directory")
    parser.add_argument("--train-num", type=int, default=None, help="Training sample count per task")
    parser.add_argument("--test-num", type=int, default=None, help="Test/calibration sample count per task")
    parser.add_argument("--train-steps", type=int, default=None, help="Teacher training steps")
    parser.add_argument("--lr", type=float, default=None, help="Teacher training learning rate")
    parser.add_argument("--lamb", type=float, default=None, help="Teacher sparsity regularization lambda")
    parser.add_argument("--topk", type=int, default=3, help="Replay shortlist size")
    parser.add_argument("--grid-number", type=int, default=21, help="Grid size for (a,b) search")
    parser.add_argument("--iteration", type=int, default=2, help="Zoom iterations for (a,b) search")
    parser.add_argument(
        "--teacher-max-test-mse",
        type=float,
        default=0.10,
        help="Default teacher quality gate: max allowed teacher test MSE before symbolic fitting.",
    )
    parser.add_argument(
        "--teacher-min-test-r2",
        type=float,
        default=0.75,
        help="Default teacher quality gate: min required teacher test R2 before symbolic fitting.",
    )
    parser.add_argument(
        "--teacher-cache-dir",
        default="outputs/teacher_cache",
        help="Persistent teacher cache directory used across benchmark runs.",
    )
    parser.add_argument(
        "--teacher-cache-mode",
        default="readwrite",
        choices=sorted(_TEACHER_CACHE_MODES),
        help="Teacher cache mode: readwrite, readonly, refresh, off.",
    )
    parser.add_argument(
        "--teacher-cache-version",
        default="v1",
        help="Teacher cache key version suffix for compatibility control.",
    )
    parser.add_argument("--no-plots", action="store_true", help="Disable plot generation")
    parser.add_argument("--quiet", action="store_true", help="Disable per-run progress prints")
    args = parser.parse_args(argv)

    tasks = _parse_str_list(args.tasks)
    seeds = _parse_int_list(args.seeds)
    output_dir = Path(args.output_dir)
    teacher_cache_dir = Path(args.teacher_cache_dir)
    resolved_training, profile_overrides = _resolve_training_config(
        profile=args.profile,
        train_num=args.train_num,
        test_num=args.test_num,
        train_steps=args.train_steps,
        lr=args.lr,
        lamb=args.lamb,
    )

    run_benchmark(
        tasks=tasks,
        seeds=seeds,
        output_dir=output_dir,
        train_num=int(resolved_training["train_num"]),
        test_num=int(resolved_training["test_num"]),
        train_steps=int(resolved_training["train_steps"]),
        lr=float(resolved_training["lr"]),
        lamb=float(resolved_training["lamb"]),
        topk=args.topk,
        grid_number=args.grid_number,
        iteration=args.iteration,
        teacher_max_test_mse=args.teacher_max_test_mse,
        teacher_min_test_r2=args.teacher_min_test_r2,
        teacher_cache_dir=teacher_cache_dir,
        teacher_cache_mode=args.teacher_cache_mode,
        teacher_cache_version=args.teacher_cache_version,
        profile_name=args.profile,
        profile_defaults=dict(_BENCHMARK_PROFILES[args.profile]),
        profile_overrides=profile_overrides,
        make_plots=not args.no_plots,
        quiet=args.quiet,
    )


if __name__ == "__main__":
    main()
