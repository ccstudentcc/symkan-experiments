from __future__ import annotations

import json
from pathlib import Path
import uuid

from scripts.icbr_benchmark_regression import main, run_regression_gate


def _write_summary_json(
    path: Path,
    *,
    speedup_median: float,
    mse_shift_mean: float,
    target_mse_shift_mean: float,
    formula_pass_mean: float,
    teacher_gate_pass_mean: float,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    summary = {
        "aggregates": {
            "overall": {
                "metrics": {
                    "formula_validation_result": {
                        "count": 4.0,
                        "mean": formula_pass_mean,
                        "median": formula_pass_mean,
                        "std": 0.0,
                        "min": formula_pass_mean,
                        "max": formula_pass_mean,
                    },
                    "teacher_quality_gate_pass": {
                        "count": 4.0,
                        "mean": teacher_gate_pass_mean,
                        "median": teacher_gate_pass_mean,
                        "std": 0.0,
                        "min": teacher_gate_pass_mean,
                        "max": teacher_gate_pass_mean,
                    },
                    "symbolic_speedup_vs_baseline": {
                        "count": 4.0,
                        "mean": speedup_median,
                        "median": speedup_median,
                        "std": 0.0,
                        "min": speedup_median,
                        "max": speedup_median,
                    },
                    "final_mse_loss_shift": {
                        "count": 4.0,
                        "mean": mse_shift_mean,
                        "median": mse_shift_mean,
                        "std": 0.0,
                        "min": mse_shift_mean,
                        "max": mse_shift_mean,
                    },
                    "symbolic_target_mse_shift": {
                        "count": 4.0,
                        "mean": target_mse_shift_mean,
                        "median": target_mse_shift_mean,
                        "std": 0.0,
                        "min": target_mse_shift_mean,
                        "max": target_mse_shift_mean,
                    },
                }
            },
            "by_task": {
                "minimal": {
                    "metrics": {
                        "formula_validation_result": {
                            "count": 2.0,
                            "mean": formula_pass_mean,
                            "median": formula_pass_mean,
                            "std": 0.0,
                            "min": formula_pass_mean,
                            "max": formula_pass_mean,
                        },
                        "teacher_quality_gate_pass": {
                            "count": 2.0,
                            "mean": teacher_gate_pass_mean,
                            "median": teacher_gate_pass_mean,
                            "std": 0.0,
                            "min": teacher_gate_pass_mean,
                            "max": teacher_gate_pass_mean,
                        },
                        "symbolic_speedup_vs_baseline": {
                            "count": 2.0,
                            "mean": speedup_median,
                            "median": speedup_median,
                            "std": 0.0,
                            "min": speedup_median,
                            "max": speedup_median,
                        },
                        "final_mse_loss_shift": {
                            "count": 2.0,
                            "mean": mse_shift_mean,
                            "median": mse_shift_mean,
                            "std": 0.0,
                            "min": mse_shift_mean,
                            "max": mse_shift_mean,
                        },
                        "symbolic_target_mse_shift": {
                            "count": 2.0,
                            "mean": target_mse_shift_mean,
                            "median": target_mse_shift_mean,
                            "std": 0.0,
                            "min": target_mse_shift_mean,
                            "max": target_mse_shift_mean,
                        },
                    }
                },
                "combo": {
                    "metrics": {
                        "formula_validation_result": {
                            "count": 2.0,
                            "mean": formula_pass_mean,
                            "median": formula_pass_mean,
                            "std": 0.0,
                            "min": formula_pass_mean,
                            "max": formula_pass_mean,
                        },
                        "teacher_quality_gate_pass": {
                            "count": 2.0,
                            "mean": teacher_gate_pass_mean,
                            "median": teacher_gate_pass_mean,
                            "std": 0.0,
                            "min": teacher_gate_pass_mean,
                            "max": teacher_gate_pass_mean,
                        },
                        "symbolic_speedup_vs_baseline": {
                            "count": 2.0,
                            "mean": speedup_median,
                            "median": speedup_median,
                            "std": 0.0,
                            "min": speedup_median,
                            "max": speedup_median,
                        },
                        "final_mse_loss_shift": {
                            "count": 2.0,
                            "mean": mse_shift_mean,
                            "median": mse_shift_mean,
                            "std": 0.0,
                            "min": mse_shift_mean,
                            "max": mse_shift_mean,
                        },
                        "symbolic_target_mse_shift": {
                            "count": 2.0,
                            "mean": target_mse_shift_mean,
                            "median": target_mse_shift_mean,
                            "std": 0.0,
                            "min": target_mse_shift_mean,
                            "max": target_mse_shift_mean,
                        },
                    }
                },
            },
        }
    }
    path.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def test_icbr_benchmark_regression_gate_passes_for_good_summary() -> None:
    root = Path("tmp") / f"icbr_regression_gate_{uuid.uuid4().hex}"
    summary_json = root / "summary.json"
    out_dir = root / "report"
    _write_summary_json(
        summary_json,
        speedup_median=1.25,
        mse_shift_mean=2e-4,
        target_mse_shift_mean=1e-4,
        formula_pass_mean=1.0,
        teacher_gate_pass_mean=1.0,
    )

    result = run_regression_gate(
        summary_json_path=summary_json,
        output_dir=out_dir,
    )

    assert result["report"]["overall_status"] == "pass"
    assert Path(result["report_json_path"]).exists()
    assert Path(result["report_md_path"]).exists()


def test_icbr_benchmark_regression_gate_fails_for_bad_summary() -> None:
    root = Path("tmp") / f"icbr_regression_gate_{uuid.uuid4().hex}"
    summary_json = root / "summary_bad.json"
    out_dir = root / "report_bad"
    _write_summary_json(
        summary_json,
        speedup_median=0.95,
        mse_shift_mean=8e-4,
        target_mse_shift_mean=9e-4,
        formula_pass_mean=0.80,
        teacher_gate_pass_mean=0.70,
    )

    exit_code = main(
        [
            "--summary-json",
            str(summary_json),
            "--output-dir",
            str(out_dir),
        ]
    )
    assert exit_code == 1

    report_json = out_dir / "icbr_benchmark_regression_gate.json"
    report = json.loads(report_json.read_text(encoding="utf-8"))
    assert report["overall_status"] == "fail"
    assert report["failed_check_count"] > 0
    assert any(item["status"] == "fail" for item in report["checks"])
