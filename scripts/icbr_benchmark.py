from __future__ import annotations

import argparse
import csv
import json
from dataclasses import dataclass
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
            row = {"task": task_name, "seed": seed, **metrics}
            rows.append(row)
            if not quiet:
                print(
                    f"[icbr-benchmark] task={task_name} seed={seed} "
                    f"candidate={metrics['candidate_generation_wall_time_s']:.4f}s "
                    f"replay={metrics['replay_rerank_wall_time_s']:.4f}s "
                    f"symbolic={metrics['symbolic_wall_time_s']:.4f}s "
                    f"mse_shift={metrics['final_mse_loss_shift']:.6e}"
                )

    csv_path = output_dir / "icbr_benchmark_rows.csv"
    fieldnames = [
        "task",
        "seed",
        "candidate_generation_wall_time_s",
        "replay_rerank_wall_time_s",
        "symbolic_wall_time_s",
        "baseline_symbolic_wall_time_s",
        "symbolic_speedup_vs_baseline",
        "replay_imitation_gap",
        "final_mse_loss_shift",
        "formula_validation_result",
        "baseline_formula_validation_result",
        "icbr_formula_validation_result",
        "baseline_mse",
        "icbr_mse",
    ]
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    summary_by_task: dict[str, dict[str, float]] = {}
    for task_name in tasks:
        task_rows = [row for row in rows if row["task"] == task_name]
        count = float(len(task_rows))
        summary_by_task[task_name] = {
            "candidate_generation_wall_time_s_mean": float(
                sum(float(row["candidate_generation_wall_time_s"]) for row in task_rows) / count
            ),
            "replay_rerank_wall_time_s_mean": float(
                sum(float(row["replay_rerank_wall_time_s"]) for row in task_rows) / count
            ),
            "symbolic_wall_time_s_mean": float(
                sum(float(row["symbolic_wall_time_s"]) for row in task_rows) / count
            ),
            "baseline_symbolic_wall_time_s_mean": float(
                sum(float(row["baseline_symbolic_wall_time_s"]) for row in task_rows) / count
            ),
            "symbolic_speedup_vs_baseline_mean": float(
                sum(float(row["symbolic_speedup_vs_baseline"]) for row in task_rows) / count
            ),
            "final_mse_loss_shift_mean": float(
                sum(float(row["final_mse_loss_shift"]) for row in task_rows) / count
            ),
            "formula_validation_pass_rate": float(
                sum(1.0 if bool(row["formula_validation_result"]) else 0.0 for row in task_rows) / count
            ),
            "baseline_formula_validation_pass_rate": float(
                sum(1.0 if bool(row["baseline_formula_validation_result"]) else 0.0 for row in task_rows) / count
            ),
            "icbr_formula_validation_pass_rate": float(
                sum(1.0 if bool(row["icbr_formula_validation_result"]) else 0.0 for row in task_rows) / count
            ),
            "baseline_mse_mean": float(sum(float(row["baseline_mse"]) for row in task_rows) / count),
            "icbr_mse_mean": float(sum(float(row["icbr_mse"]) for row in task_rows) / count),
        }

    summary = {
        "tasks": tasks,
        "seeds": seeds,
        "row_count": len(rows),
        "summary_by_task": summary_by_task,
    }
    summary_json_path = output_dir / "icbr_benchmark_summary.json"
    summary_json_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    md_lines: list[str] = [
        "# ICBR Benchmark Summary",
        "",
        f"- tasks: {', '.join(tasks)}",
        f"- seeds: {', '.join(str(seed) for seed in seeds)}",
        "",
        "## Per-Task Means",
        "",
        "| task | candidate_generation_wall_time_s | replay_rerank_wall_time_s | icbr_symbolic_wall_time_s | baseline_symbolic_wall_time_s | symbolic_speedup_vs_baseline | final_mse_loss_shift | baseline_mse | icbr_mse | baseline_formula_pass_rate | icbr_formula_pass_rate |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for task_name in tasks:
        item = summary_by_task[task_name]
        md_lines.append(
            "| "
            + f"{task_name} | "
            + f"{item['candidate_generation_wall_time_s_mean']:.6f} | "
            + f"{item['replay_rerank_wall_time_s_mean']:.6f} | "
            + f"{item['symbolic_wall_time_s_mean']:.6f} | "
            + f"{item['baseline_symbolic_wall_time_s_mean']:.6f} | "
            + f"{item['symbolic_speedup_vs_baseline_mean']:.4f} | "
            + f"{item['final_mse_loss_shift_mean']:.6e} | "
            + f"{item['baseline_mse_mean']:.6e} | "
            + f"{item['icbr_mse_mean']:.6e} | "
            + f"{item['baseline_formula_validation_pass_rate']:.4f} | "
            + f"{item['icbr_formula_validation_pass_rate']:.4f} |"
        )
    md_lines.append("")
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
