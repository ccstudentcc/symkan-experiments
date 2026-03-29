from __future__ import annotations

import csv
import json
import uuid
from pathlib import Path

from scripts.icbr_benchmark import main, run_benchmark


def test_icbr_benchmark_script_generates_outputs() -> None:
    out_dir = Path("tmp") / f"icbr_benchmark_script_{uuid.uuid4().hex}"

    main(
        [
            "--tasks",
            "minimal,combo",
            "--seeds",
            "0,1",
            "--output-dir",
            str(out_dir),
            "--train-num",
            "24",
            "--test-num",
            "24",
            "--train-steps",
            "4",
            "--lr",
            "0.05",
            "--topk",
            "2",
            "--grid-number",
            "11",
            "--iteration",
            "1",
            "--teacher-max-test-mse",
            "1.0",
            "--teacher-min-test-r2",
            "-1.0",
            "--quiet",
        ]
    )

    rows_path = out_dir / "icbr_benchmark_rows.csv"
    task_stats_csv = out_dir / "icbr_benchmark_task_stats.csv"
    significance_csv = out_dir / "icbr_benchmark_significance.csv"
    summary_json = out_dir / "icbr_benchmark_summary.json"
    summary_md = out_dir / "icbr_benchmark_summary.md"

    assert rows_path.exists()
    assert task_stats_csv.exists()
    assert significance_csv.exists()
    assert summary_json.exists()
    assert summary_md.exists()

    with rows_path.open("r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 4
    assert {row["task"] for row in rows} == {"minimal", "combo"}
    assert all(row["lib"] == "[\"__FULL_SYMBOLIC_LIB__\"]" for row in rows)
    required_cols = {
        "candidate_generation_wall_time_s",
        "replay_rerank_wall_time_s",
        "symbolic_wall_time_s",
        "baseline_symbolic_wall_time_s",
        "symbolic_wall_time_delta_s",
        "symbolic_speedup_vs_baseline",
        "replay_imitation_gap",
        "final_mse_loss_shift",
        "teacher_test_mse",
        "teacher_test_r2",
        "teacher_quality_gate_pass",
        "teacher_quality_gate_reason",
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
        "baseline_formula_raw",
        "baseline_formula_display",
        "icbr_formula_raw",
        "icbr_formula_display",
    }
    assert required_cols.issubset(set(rows[0].keys()))

    summary = json.loads(summary_json.read_text(encoding="utf-8"))
    assert "metadata" in summary
    assert "config" in summary
    assert "rows" in summary
    assert "aggregates" in summary
    assert "artifacts" in summary
    assert "notes" in summary
    assert len(summary["rows"]) == 4
    assert summary["config"]["tasks"] == ["minimal", "combo"]
    assert "overall" in summary["aggregates"]
    assert "by_task" in summary["aggregates"]
    assert "teacher_quality_gate" in summary["config"]
    assert summary["config"]["task_lib_mode"]["minimal"] == "full_symbolic_lib"
    assert summary["config"]["task_lib_mode"]["combo"] == "full_symbolic_lib"
    assert "metrics" in summary["aggregates"]["overall"]
    assert "significance" in summary["aggregates"]["overall"]
    minimal = summary["aggregates"]["by_task"]["minimal"]
    assert minimal["row_count"] == 2
    assert "metrics" in minimal
    assert "significance" in minimal
    speedup_stats = minimal["metrics"]["symbolic_speedup_vs_baseline"]
    assert {"count", "mean", "median", "std", "min", "max"}.issubset(set(speedup_stats.keys()))
    for row in summary["rows"]:
        assert row["teacher_quality_gate_pass"] is True
        assert isinstance(row["baseline_formula_raw"], list)
        assert isinstance(row["baseline_formula_display"], list)
        assert isinstance(row["icbr_formula_raw"], list)
        assert isinstance(row["icbr_formula_display"], list)

    assert summary["artifacts"]["task_stats_csv"].endswith("icbr_benchmark_task_stats.csv")
    assert summary["artifacts"]["significance_csv"].endswith("icbr_benchmark_significance.csv")
    visuals = summary["artifacts"]["visualizations"]
    assert "enabled" in visuals
    assert "files" in visuals


def test_trig_interaction_uses_task_specific_topk_override() -> None:
    out_dir = Path("tmp") / f"icbr_benchmark_topk_override_{uuid.uuid4().hex}"
    result = run_benchmark(
        tasks=["trig_interaction"],
        seeds=[0, 1],
        output_dir=out_dir,
        train_num=16,
        test_num=16,
        train_steps=2,
        lr=0.05,
        topk=3,
        grid_number=11,
        iteration=1,
        teacher_max_test_mse=1.0,
        teacher_min_test_r2=-1.0,
        make_plots=False,
        quiet=True,
    )

    rows = result["rows"]
    assert len(rows) == 2
    assert all(int(row["icbr_topk_used"]) == 5 for row in rows)
    assert all(row["lib"] == ["__FULL_SYMBOLIC_LIB__"] for row in rows)
    assert result["summary"]["config"]["task_lib_mode"]["trig_interaction"] == "full_symbolic_lib"


def test_teacher_quality_gate_can_skip_symbolic_comparison() -> None:
    out_dir = Path("tmp") / f"icbr_benchmark_teacher_gate_{uuid.uuid4().hex}"
    result = run_benchmark(
        tasks=["minimal"],
        seeds=[0],
        output_dir=out_dir,
        train_num=16,
        test_num=16,
        train_steps=2,
        lr=0.05,
        topk=2,
        grid_number=11,
        iteration=1,
        teacher_max_test_mse=1e-8,
        teacher_min_test_r2=0.999999,
        make_plots=False,
        quiet=True,
    )

    row = result["rows"][0]
    assert row["teacher_quality_gate_pass"] is False
    assert "teacher_test_mse" in row["teacher_quality_gate_reason"] or "teacher_test_r2" in row["teacher_quality_gate_reason"]
    assert row["formula_validation_result"] is False
    assert row["baseline_formula_raw"] == []
    assert row["icbr_formula_raw"] == []
