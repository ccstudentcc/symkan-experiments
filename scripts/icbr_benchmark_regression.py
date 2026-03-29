from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class RegressionThresholds:
    min_formula_pass_rate: float = 0.95
    min_speedup_median: float = 1.10
    max_mse_shift_mean: float = 5e-4


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _merge_thresholds(
    *,
    defaults: RegressionThresholds,
    override_json: dict[str, Any] | None,
) -> tuple[RegressionThresholds, dict[str, dict[str, float]]]:
    global_cfg = {
        "min_formula_pass_rate": defaults.min_formula_pass_rate,
        "min_speedup_median": defaults.min_speedup_median,
        "max_mse_shift_mean": defaults.max_mse_shift_mean,
    }
    per_task_cfg: dict[str, dict[str, float]] = {}

    if override_json:
        global_override = override_json.get("global", {})
        per_task_override = override_json.get("per_task", {})
        for key in list(global_cfg.keys()):
            if key in global_override:
                global_cfg[key] = float(global_override[key])
        for task_name, task_values in per_task_override.items():
            if not isinstance(task_values, dict):
                continue
            per_task_cfg[str(task_name)] = {}
            for key in list(global_cfg.keys()):
                if key in task_values:
                    per_task_cfg[str(task_name)][key] = float(task_values[key])

    return (
        RegressionThresholds(
            min_formula_pass_rate=float(global_cfg["min_formula_pass_rate"]),
            min_speedup_median=float(global_cfg["min_speedup_median"]),
            max_mse_shift_mean=float(global_cfg["max_mse_shift_mean"]),
        ),
        per_task_cfg,
    )


def _evaluate_check(
    *,
    scope: str,
    task: str,
    metric: str,
    stat: str,
    op: str,
    threshold: float,
    value: float,
    description: str,
) -> dict[str, Any]:
    if op == ">=":
        passed = value >= threshold
    elif op == "<=":
        passed = value <= threshold
    else:  # pragma: no cover - internal misuse guard
        raise ValueError(f"Unsupported operator: {op}")

    return {
        "scope": scope,
        "task": task,
        "metric": metric,
        "stat": stat,
        "operator": op,
        "threshold": float(threshold),
        "value": float(value),
        "status": "pass" if passed else "fail",
        "description": description,
        "fail_reason": "" if passed else f"expected value {op} {threshold}, got {value}",
    }


def evaluate_regression_gate(
    *,
    summary: dict[str, Any],
    thresholds: RegressionThresholds,
    per_task_thresholds: dict[str, dict[str, float]] | None = None,
) -> dict[str, Any]:
    per_task_thresholds = per_task_thresholds or {}
    checks: list[dict[str, Any]] = []

    by_task = summary["aggregates"]["by_task"]
    overall_metrics = summary["aggregates"]["overall"]["metrics"]

    checks.append(
        _evaluate_check(
            scope="overall",
            task="__all__",
            metric="formula_validation_result",
            stat="mean",
            op=">=",
            threshold=thresholds.min_formula_pass_rate,
            value=float(overall_metrics["formula_validation_result"]["mean"]),
            description="Overall formula validation pass rate should stay high.",
        )
    )
    checks.append(
        _evaluate_check(
            scope="overall",
            task="__all__",
            metric="symbolic_speedup_vs_baseline",
            stat="median",
            op=">=",
            threshold=thresholds.min_speedup_median,
            value=float(overall_metrics["symbolic_speedup_vs_baseline"]["median"]),
            description="Overall median speedup should stay above baseline threshold.",
        )
    )
    checks.append(
        _evaluate_check(
            scope="overall",
            task="__all__",
            metric="final_mse_loss_shift",
            stat="mean",
            op="<=",
            threshold=thresholds.max_mse_shift_mean,
            value=float(overall_metrics["final_mse_loss_shift"]["mean"]),
            description="Overall MSE shift mean should not regress beyond tolerated bound.",
        )
    )

    for task_name, task_item in by_task.items():
        task_metrics = task_item["metrics"]
        task_cfg = {
            "min_formula_pass_rate": thresholds.min_formula_pass_rate,
            "min_speedup_median": thresholds.min_speedup_median,
            "max_mse_shift_mean": thresholds.max_mse_shift_mean,
        }
        task_cfg.update(per_task_thresholds.get(task_name, {}))

        checks.append(
            _evaluate_check(
                scope="task",
                task=task_name,
                metric="formula_validation_result",
                stat="mean",
                op=">=",
                threshold=float(task_cfg["min_formula_pass_rate"]),
                value=float(task_metrics["formula_validation_result"]["mean"]),
                description="Task formula validation pass rate should stay high.",
            )
        )
        checks.append(
            _evaluate_check(
                scope="task",
                task=task_name,
                metric="symbolic_speedup_vs_baseline",
                stat="median",
                op=">=",
                threshold=float(task_cfg["min_speedup_median"]),
                value=float(task_metrics["symbolic_speedup_vs_baseline"]["median"]),
                description="Task median speedup should stay above threshold.",
            )
        )
        checks.append(
            _evaluate_check(
                scope="task",
                task=task_name,
                metric="final_mse_loss_shift",
                stat="mean",
                op="<=",
                threshold=float(task_cfg["max_mse_shift_mean"]),
                value=float(task_metrics["final_mse_loss_shift"]["mean"]),
                description="Task MSE shift mean should stay below tolerated bound.",
            )
        )

    failed_checks = [item for item in checks if item["status"] == "fail"]
    overall_status = "pass" if not failed_checks else "fail"
    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "overall_status": overall_status,
        "check_count": len(checks),
        "failed_check_count": len(failed_checks),
        "checks": checks,
    }


def _render_markdown(report: dict[str, Any], *, summary_json_path: Path) -> str:
    lines = [
        "# ICBR Benchmark Regression Gate",
        "",
        f"- Source summary: `{summary_json_path}`",
        f"- Generated at UTC: {report['generated_at_utc']}",
        f"- Overall status: **{report['overall_status'].upper()}**",
        f"- Checks: {report['check_count']}, Failed: {report['failed_check_count']}",
        "",
        "## Check Details",
        "",
        "| scope | task | metric | stat | op | threshold | value | status |",
        "|---|---|---|---|---|---:|---:|---|",
    ]
    for item in report["checks"]:
        lines.append(
            "| "
            + f"{item['scope']} | "
            + f"{item['task']} | "
            + f"{item['metric']} | "
            + f"{item['stat']} | "
            + f"{item['operator']} | "
            + f"{float(item['threshold']):.6g} | "
            + f"{float(item['value']):.6g} | "
            + f"{item['status']} |"
        )
    lines.append("")

    failed = [item for item in report["checks"] if item["status"] == "fail"]
    if failed:
        lines.extend(["## Fail Reasons", ""])
        for item in failed:
            lines.append(f"- `{item['scope']}:{item['task']}:{item['metric']}` -> {item['fail_reason']}")
        lines.append("")
    return "\n".join(lines) + "\n"


def run_regression_gate(
    *,
    summary_json_path: Path,
    output_dir: Path,
    threshold_override_path: Path | None = None,
    min_formula_pass_rate: float = 0.95,
    min_speedup_median: float = 1.10,
    max_mse_shift_mean: float = 5e-4,
) -> dict[str, Any]:
    summary = _load_json(summary_json_path)
    threshold_override = _load_json(threshold_override_path) if threshold_override_path else None

    defaults = RegressionThresholds(
        min_formula_pass_rate=float(min_formula_pass_rate),
        min_speedup_median=float(min_speedup_median),
        max_mse_shift_mean=float(max_mse_shift_mean),
    )
    thresholds, per_task_thresholds = _merge_thresholds(defaults=defaults, override_json=threshold_override)

    report = evaluate_regression_gate(
        summary=summary,
        thresholds=thresholds,
        per_task_thresholds=per_task_thresholds,
    )

    output_dir.mkdir(parents=True, exist_ok=True)
    report_json_path = output_dir / "icbr_benchmark_regression_gate.json"
    report_md_path = output_dir / "icbr_benchmark_regression_gate.md"
    report_json_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    report_md_path.write_text(_render_markdown(report, summary_json_path=summary_json_path), encoding="utf-8")

    return {
        "report": report,
        "report_json_path": str(report_json_path),
        "report_md_path": str(report_md_path),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run regression gate checks on ICBR benchmark summary JSON.")
    parser.add_argument(
        "--summary-json",
        default="outputs/icbr_benchmark_extended/icbr_benchmark_summary.json",
        help="Path to icbr benchmark summary json.",
    )
    parser.add_argument(
        "--output-dir",
        default="outputs/icbr_benchmark_extended",
        help="Directory to write regression gate reports.",
    )
    parser.add_argument(
        "--thresholds-json",
        default=None,
        help="Optional JSON file for threshold overrides with {global, per_task}.",
    )
    parser.add_argument(
        "--min-formula-pass-rate",
        type=float,
        default=0.95,
        help="Global minimum formula validation pass-rate threshold.",
    )
    parser.add_argument(
        "--min-speedup-median",
        type=float,
        default=1.10,
        help="Global minimum median speedup threshold.",
    )
    parser.add_argument(
        "--max-mse-shift-mean",
        type=float,
        default=5e-4,
        help="Global maximum mean mse shift threshold.",
    )
    args = parser.parse_args(argv)

    result = run_regression_gate(
        summary_json_path=Path(args.summary_json),
        output_dir=Path(args.output_dir),
        threshold_override_path=Path(args.thresholds_json) if args.thresholds_json else None,
        min_formula_pass_rate=float(args.min_formula_pass_rate),
        min_speedup_median=float(args.min_speedup_median),
        max_mse_shift_mean=float(args.max_mse_shift_mean),
    )
    report = result["report"]
    print(f"overall_status={report['overall_status']}")
    print(f"report_json={result['report_json_path']}")
    print(f"report_md={result['report_md_path']}")
    return 0 if report["overall_status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
