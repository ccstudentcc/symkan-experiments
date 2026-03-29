from __future__ import annotations

import argparse
import csv
import json
import math
import random
import statistics
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

import torch

from kan.MultKAN import MultKAN
from kan.icbr import benchmark_icbr_vs_baseline
from kan.utils import create_dataset


_NUMERIC_METRICS = [
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
]

_BOOLEAN_METRICS = [
    "formula_validation_result",
    "baseline_formula_validation_result",
    "icbr_formula_validation_result",
]

_SIGNIFICANCE_DIRECTIONS = {
    "symbolic_wall_time_delta_s": "positive",
    "final_mse_loss_shift": "negative",
}


@dataclass(frozen=True)
class _TaskSpec:
    name: str
    n_var: int
    width: list[int]
    target_fn: Callable[[torch.Tensor], torch.Tensor]
    lib: list[str] | None
    icbr_topk: int | None = None


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


def _fit_teacher_model(
    spec: _TaskSpec,
    *,
    seed: int,
    train_num: int,
    test_num: int,
    train_steps: int,
    lr: float,
) -> tuple[MultKAN, dict[str, torch.Tensor]]:
    torch.manual_seed(seed)
    dataset = create_dataset(
        spec.target_fn,
        n_var=spec.n_var,
        train_num=train_num,
        test_num=test_num,
        seed=seed,
        device="cpu",
    )

    model = MultKAN(
        width=spec.width,
        grid=5,
        k=3,
        auto_save=False,
        device="cpu",
    )
    model.fit(
        dataset,
        opt="Adam",
        steps=train_steps,
        lr=lr,
        update_grid=False,
        batch=-1,
        lamb=0.0,
        log=max(train_steps + 1, 999999),
    )
    return model, dataset


def _serialize_formula_list(formulas: list[str]) -> str:
    return " || ".join(formulas)


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
        values = [float(row[metric]) for row in rows]
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
        deltas = [float(row[metric_name]) for row in rows]
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
            "sample_count": len(deltas),
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

    fig, ax = plt.subplots(figsize=(10, 4.5))
    x_positions = list(range(len(tasks)))
    baseline_mean = [
        float(statistics.mean(float(row["baseline_symbolic_wall_time_s"]) for row in by_task_rows[task])) for task in tasks
    ]
    baseline_std = [
        float(statistics.stdev(float(row["baseline_symbolic_wall_time_s"]) for row in by_task_rows[task]))
        if len(by_task_rows[task]) > 1
        else 0.0
        for task in tasks
    ]
    icbr_mean = [float(statistics.mean(float(row["symbolic_wall_time_s"]) for row in by_task_rows[task])) for task in tasks]
    icbr_std = [
        float(statistics.stdev(float(row["symbolic_wall_time_s"]) for row in by_task_rows[task]))
        if len(by_task_rows[task]) > 1
        else 0.0
        for task in tasks
    ]
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
    speedup_data = [[float(row["symbolic_speedup_vs_baseline"]) for row in by_task_rows[task]] for task in tasks]
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
    mse_shift_data = [[float(row["final_mse_loss_shift"]) for row in by_task_rows[task]] for task in tasks]
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
    topk: int,
    grid_number: int,
    iteration: int,
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
            model, dataset = _fit_teacher_model(
                spec,
                seed=seed,
                train_num=train_num,
                test_num=test_num,
                train_steps=train_steps,
                lr=lr,
            )
            metrics = benchmark_icbr_vs_baseline(
                model,
                calibration_split=dataset["test_input"],
                lib=spec.lib,
                topk=effective_topk,
                a_range=(-5.0, 5.0),
                b_range=(-5.0, 5.0),
                grid_number=grid_number,
                iteration=iteration,
            )
            row = {
                "task": task_name,
                "seed": seed,
                "n_var": spec.n_var,
                "width": list(spec.width),
                "lib": list(spec.lib) if spec.lib is not None else ["__FULL_SYMBOLIC_LIB__"],
                "icbr_topk_used": effective_topk,
                **metrics,
            }
            rows.append(row)
            if not quiet:
                print(
                    f"[icbr-benchmark] task={task_name} seed={seed} "
                    f"icbr_symbolic={metrics['symbolic_wall_time_s']:.4f}s "
                    f"baseline_symbolic={metrics['baseline_symbolic_wall_time_s']:.4f}s "
                    f"speedup={metrics['symbolic_speedup_vs_baseline']:.2f}x "
                    f"mse_shift={metrics['final_mse_loss_shift']:.6e}"
                )

    rows_csv = output_dir / "icbr_benchmark_rows.csv"
    row_fieldnames = [
        "task",
        "seed",
        "n_var",
        "width",
        "lib",
        "icbr_topk_used",
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
            "train_num": train_num,
            "test_num": test_num,
            "train_steps": train_steps,
            "lr": lr,
            "topk": topk,
            "grid_number": grid_number,
            "iteration": iteration,
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
                "stats_schema": "Each metric includes count | mean | median | std | min | max",
            },
            "significance_guide": {
                "sign_test_pvalue_two_sided": "Two-sided sign test p-value on non-tie seeds.",
                "mean_delta_ci95": "Bootstrap 95% CI of mean delta across seeds.",
            },
            "extensibility": [
                "Add new tasks in _task_specs() with target_fn, width, and symbolic lib.",
                "Rows-level details are preserved for error bars and downstream statistical tests.",
                "Task stats CSV and significance CSV can be consumed by external plotting/report tools.",
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
        f"- Tasks: {', '.join(tasks)}",
        f"- Seeds: {', '.join(str(seed) for seed in seeds)}",
        f"- Train/Test samples per task: {train_num}/{test_num}",
        f"- Train steps: {train_steps}, lr: {lr}",
        f"- ICBR shortlist topk: {topk}, grid_number: {grid_number}, iteration: {iteration}",
        "",
        "## Task-Level Aggregate Stats",
        "",
        "| task | n | baseline_symbolic_mean | icbr_symbolic_mean | delta_mean | delta_median | delta_std | speedup_mean | speedup_median | mse_shift_mean | mse_shift_std | formula_pass_mean |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for task_name in tasks:
        task_item = summary["aggregates"]["by_task"][task_name]
        metrics = task_item["metrics"]
        md_lines.append(
            "| "
            + f"{task_name} | "
            + f"{task_item['row_count']} | "
            + f"{metrics['baseline_symbolic_wall_time_s']['mean']:.6f} | "
            + f"{metrics['symbolic_wall_time_s']['mean']:.6f} | "
            + f"{metrics['symbolic_wall_time_delta_s']['mean']:.6f} | "
            + f"{metrics['symbolic_wall_time_delta_s']['median']:.6f} | "
            + f"{metrics['symbolic_wall_time_delta_s']['std']:.6f} | "
            + f"{metrics['symbolic_speedup_vs_baseline']['mean']:.4f} | "
            + f"{metrics['symbolic_speedup_vs_baseline']['median']:.4f} | "
            + f"{metrics['final_mse_loss_shift']['mean']:.6e} | "
            + f"{metrics['final_mse_loss_shift']['std']:.6e} | "
            + f"{metrics['formula_validation_result']['mean']:.4f} |"
        )
    md_lines.append("")

    md_lines.extend(
        [
            "## Statistical Significance (by task)",
            "",
            "| task | metric | favorable_direction | n_effective | improved | worsened | ties | p_value_two_sided | mean_delta_ci95 |",
            "|---|---|---|---:|---:|---:|---:|---:|---|",
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
            "| task | seed | candidate_s | replay_s | baseline_symbolic_s | icbr_symbolic_s | speedup_x | baseline_mse | icbr_mse | mse_shift | formula_ok |",
            "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for row in rows:
        md_lines.append(
            "| "
            + f"{row['task']} | {row['seed']} | "
            + f"{float(row['candidate_generation_wall_time_s']):.6f} | "
            + f"{float(row['replay_rerank_wall_time_s']):.6f} | "
            + f"{float(row['baseline_symbolic_wall_time_s']):.6f} | "
            + f"{float(row['symbolic_wall_time_s']):.6f} | "
            + f"{float(row['symbolic_speedup_vs_baseline']):.4f} | "
            + f"{float(row['baseline_mse']):.6e} | "
            + f"{float(row['icbr_mse']):.6e} | "
            + f"{float(row['final_mse_loss_shift']):.6e} | "
            + f"{bool(row['formula_validation_result'])} |"
        )
    md_lines.append("")

    md_lines.append("## Formula Comparison")
    md_lines.append("")
    for row in rows:
        md_lines.append(f"### task={row['task']} seed={row['seed']}")
        md_lines.append("")
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


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Run CPU benchmark for ICBR Phase I with extended multi-seed reporting.")
    parser.add_argument(
        "--tasks",
        default="minimal,combo,poly_cubic,trig_interaction",
        help="Comma-separated tasks: minimal,combo,poly_cubic,trig_interaction",
    )
    parser.add_argument("--seeds", default="0,1,2,3,4,5,6,7,8,9", help="Comma-separated integer seeds")
    parser.add_argument("--output-dir", default="outputs/icbr_benchmark_extended", help="Output directory")
    parser.add_argument("--train-num", type=int, default=64, help="Training sample count per task")
    parser.add_argument("--test-num", type=int, default=64, help="Test/calibration sample count per task")
    parser.add_argument("--train-steps", type=int, default=20, help="Teacher training steps")
    parser.add_argument("--lr", type=float, default=0.05, help="Teacher training learning rate")
    parser.add_argument("--topk", type=int, default=3, help="Replay shortlist size")
    parser.add_argument("--grid-number", type=int, default=21, help="Grid size for (a,b) search")
    parser.add_argument("--iteration", type=int, default=2, help="Zoom iterations for (a,b) search")
    parser.add_argument("--no-plots", action="store_true", help="Disable plot generation")
    parser.add_argument("--quiet", action="store_true", help="Disable per-run progress prints")
    args = parser.parse_args(argv)

    tasks = _parse_str_list(args.tasks)
    seeds = _parse_int_list(args.seeds)
    output_dir = Path(args.output_dir)

    run_benchmark(
        tasks=tasks,
        seeds=seeds,
        output_dir=output_dir,
        train_num=args.train_num,
        test_num=args.test_num,
        train_steps=args.train_steps,
        lr=args.lr,
        topk=args.topk,
        grid_number=args.grid_number,
        iteration=args.iteration,
        make_plots=not args.no_plots,
        quiet=args.quiet,
    )


if __name__ == "__main__":
    main()
