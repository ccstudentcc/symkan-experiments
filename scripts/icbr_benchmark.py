from __future__ import annotations

import argparse
import csv
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

import torch

from kan.MultKAN import MultKAN
from kan.icbr import benchmark_icbr_vs_baseline
from kan.utils import create_dataset


@dataclass(frozen=True)
class _TaskSpec:
    name: str
    n_var: int
    width: list[int]
    target_fn: Callable[[torch.Tensor], torch.Tensor]
    lib: list[str]


def _task_specs() -> dict[str, _TaskSpec]:
    return {
        "minimal": _TaskSpec(
            name="minimal",
            n_var=1,
            width=[1, 1],
            target_fn=lambda x: torch.sin(torch.pi * x[:, [0]]),
            lib=["x", "x^2", "sin", "cos"],
        ),
        "combo": _TaskSpec(
            name="combo",
            n_var=2,
            width=[2, 2, 1],
            target_fn=lambda x: torch.sin(torch.pi * x[:, [0]]) + x[:, [1]] ** 2,
            lib=["x", "x^2", "sin", "cos", "gaussian"],
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


def _mean(values: list[float]) -> float:
    if not values:
        return float("nan")
    return float(sum(values) / len(values))


def _serialize_formula_list(formulas: list[str]) -> str:
    return " || ".join(formulas)


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
                topk=topk,
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
                "lib": list(spec.lib),
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

    csv_path = output_dir / "icbr_benchmark_rows.csv"
    fieldnames = [
        "task",
        "seed",
        "n_var",
        "width",
        "lib",
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
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    "task": row["task"],
                    "seed": row["seed"],
                    "n_var": row["n_var"],
                    "width": json.dumps(row["width"], ensure_ascii=False),
                    "lib": json.dumps(row["lib"], ensure_ascii=False),
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

    summary_by_task: dict[str, dict[str, float]] = {}
    for task_name in tasks:
        task_rows = [row for row in rows if row["task"] == task_name]
        summary_by_task[task_name] = {
            "candidate_generation_wall_time_s_mean": _mean(
                [float(row["candidate_generation_wall_time_s"]) for row in task_rows]
            ),
            "replay_rerank_wall_time_s_mean": _mean([float(row["replay_rerank_wall_time_s"]) for row in task_rows]),
            "icbr_symbolic_wall_time_s_mean": _mean([float(row["symbolic_wall_time_s"]) for row in task_rows]),
            "baseline_symbolic_wall_time_s_mean": _mean(
                [float(row["baseline_symbolic_wall_time_s"]) for row in task_rows]
            ),
            "symbolic_wall_time_delta_s_mean": _mean([float(row["symbolic_wall_time_delta_s"]) for row in task_rows]),
            "symbolic_speedup_vs_baseline_mean": _mean(
                [float(row["symbolic_speedup_vs_baseline"]) for row in task_rows]
            ),
            "final_mse_loss_shift_mean": _mean([float(row["final_mse_loss_shift"]) for row in task_rows]),
            "baseline_mse_mean": _mean([float(row["baseline_mse"]) for row in task_rows]),
            "icbr_mse_mean": _mean([float(row["icbr_mse"]) for row in task_rows]),
            "formula_validation_pass_rate": _mean(
                [1.0 if bool(row["formula_validation_result"]) else 0.0 for row in task_rows]
            ),
            "baseline_formula_validation_pass_rate": _mean(
                [1.0 if bool(row["baseline_formula_validation_result"]) else 0.0 for row in task_rows]
            ),
            "icbr_formula_validation_pass_rate": _mean(
                [1.0 if bool(row["icbr_formula_validation_result"]) else 0.0 for row in task_rows]
            ),
        }

    overall = {
        "candidate_generation_wall_time_s_mean": _mean([float(row["candidate_generation_wall_time_s"]) for row in rows]),
        "replay_rerank_wall_time_s_mean": _mean([float(row["replay_rerank_wall_time_s"]) for row in rows]),
        "icbr_symbolic_wall_time_s_mean": _mean([float(row["symbolic_wall_time_s"]) for row in rows]),
        "baseline_symbolic_wall_time_s_mean": _mean([float(row["baseline_symbolic_wall_time_s"]) for row in rows]),
        "symbolic_speedup_vs_baseline_mean": _mean([float(row["symbolic_speedup_vs_baseline"]) for row in rows]),
        "final_mse_loss_shift_mean": _mean([float(row["final_mse_loss_shift"]) for row in rows]),
        "row_count": len(rows),
    }

    summary = {
        "metadata": {
            "generated_at_utc": datetime.now(timezone.utc).isoformat(),
            "benchmark_name": "icbr_phase1_cpu_smoke",
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
        },
        "rows": rows,
        "aggregates": {"overall": overall, "by_task": summary_by_task},
        "notes": {
            "field_guide": {
                "symbolic_wall_time_delta_s": "baseline_symbolic_wall_time_s - icbr_symbolic_wall_time_s",
                "final_mse_loss_shift": "icbr_mse - baseline_mse; negative means ICBR has lower MSE",
            },
            "extensibility": [
                "Add new tasks in _task_specs() with target_fn, width, and symbolic lib.",
                "For larger studies, run with multiple seeds and aggregate via summary JSON.",
                "For complex formula post-processing, consume formula lists from summary JSON rows.",
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
        "## Task-Level Comparison (Mean over seeds)",
        "",
        "| task | baseline_symbolic_s | icbr_symbolic_s | delta_s (baseline-icbr) | speedup_x | baseline_mse | icbr_mse | mse_shift (icbr-baseline) | baseline_formula_pass | icbr_formula_pass |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for task_name in tasks:
        item = summary_by_task[task_name]
        md_lines.append(
            "| "
            + f"{task_name} | "
            + f"{item['baseline_symbolic_wall_time_s_mean']:.6f} | "
            + f"{item['icbr_symbolic_wall_time_s_mean']:.6f} | "
            + f"{item['symbolic_wall_time_delta_s_mean']:.6f} | "
            + f"{item['symbolic_speedup_vs_baseline_mean']:.4f} | "
            + f"{item['baseline_mse_mean']:.6e} | "
            + f"{item['icbr_mse_mean']:.6e} | "
            + f"{item['final_mse_loss_shift_mean']:.6e} | "
            + f"{item['baseline_formula_validation_pass_rate']:.4f} | "
            + f"{item['icbr_formula_validation_pass_rate']:.4f} |"
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

    md_lines.extend(
        [
            "## Extensibility Notes",
            "",
            "- 任务可扩展：在 `scripts/icbr_benchmark.py::_task_specs()` 新增任务条目即可接入同一导出链路。",
            "- 指标可扩展：`kan.icbr.benchmark_icbr_vs_baseline` 返回字段会原样进入 JSON rows；CSV/MD 仅需补字段映射。",
            "- 大规模实验建议：增加 seeds 并按 task 聚合，同时保留 rows 级明细用于误差条或统计检验。",
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
    parser = argparse.ArgumentParser(description="Run a minimal CPU benchmark for ICBR Phase I.")
    parser.add_argument("--tasks", default="minimal,combo", help="Comma-separated tasks: minimal,combo")
    parser.add_argument("--seeds", default="0", help="Comma-separated integer seeds")
    parser.add_argument("--output-dir", default="outputs/icbr_benchmark_smoke", help="Output directory")
    parser.add_argument("--train-num", type=int, default=64, help="Training sample count per task")
    parser.add_argument("--test-num", type=int, default=64, help="Test/calibration sample count per task")
    parser.add_argument("--train-steps", type=int, default=20, help="Teacher training steps")
    parser.add_argument("--lr", type=float, default=0.05, help="Teacher training learning rate")
    parser.add_argument("--topk", type=int, default=3, help="Replay shortlist size")
    parser.add_argument("--grid-number", type=int, default=21, help="Grid size for (a,b) search")
    parser.add_argument("--iteration", type=int, default=2, help="Zoom iterations for (a,b) search")
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
        quiet=args.quiet,
    )


if __name__ == "__main__":
    main()
