from __future__ import annotations

import csv
import uuid
from pathlib import Path

from scripts.icbr_benchmark import main


def test_icbr_benchmark_script_generates_outputs() -> None:
    out_dir = Path("tmp") / f"icbr_benchmark_script_{uuid.uuid4().hex}"

    main(
        [
            "--tasks",
            "minimal,combo",
            "--seeds",
            "0",
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
            "--quiet",
        ]
    )

    rows_path = out_dir / "icbr_benchmark_rows.csv"
    summary_json = out_dir / "icbr_benchmark_summary.json"
    summary_md = out_dir / "icbr_benchmark_summary.md"

    assert rows_path.exists()
    assert summary_json.exists()
    assert summary_md.exists()

    with rows_path.open("r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 2
    assert {row["task"] for row in rows} == {"minimal", "combo"}
    required_cols = {
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
    }
    assert required_cols.issubset(set(rows[0].keys()))
