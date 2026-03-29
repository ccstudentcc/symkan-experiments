from __future__ import annotations

import csv
import json
import uuid
from pathlib import Path

import numpy as np

from scripts.icbr_benchmark import _expand_feynman_task_tokens, _resolve_training_config, main, run_benchmark


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
            "--teacher-cache-dir",
            str(out_dir / "teacher_cache"),
            "--teacher-cache-mode",
            "readwrite",
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
        "teacher_cache_hit",
        "teacher_cache_key",
        "teacher_cache_path",
        "teacher_cache_mode",
        "teacher_cache_status",
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
    assert summary["config"]["profile"]["name"] == "quick"
    assert summary["config"]["profile"]["overrides"]["train_num"] is True
    assert summary["config"]["profile"]["overrides"]["test_num"] is True
    assert summary["config"]["profile"]["overrides"]["train_steps"] is True
    assert summary["config"]["profile"]["overrides"]["lr"] is True
    assert summary["config"]["profile"]["overrides"]["lamb"] is False
    assert "overall" in summary["aggregates"]
    assert "by_task" in summary["aggregates"]
    assert "teacher_quality_gate" in summary["config"]
    assert "teacher_cache" in summary["config"]
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


def test_quality_profile_resolves_expected_defaults() -> None:
    resolved, overrides = _resolve_training_config(
        profile="quality",
        train_num=None,
        test_num=None,
        train_steps=None,
        lr=None,
        lamb=None,
    )
    assert resolved["train_num"] == 1000
    assert resolved["test_num"] == 500
    assert resolved["train_steps"] == 80
    assert resolved["lr"] == 0.03
    assert resolved["lamb"] == 1e-3
    assert overrides == {
        "train_num": False,
        "test_num": False,
        "train_steps": False,
        "lr": False,
        "lamb": False,
    }


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
        lamb=1e-3,
        topk=3,
        grid_number=11,
        iteration=1,
        teacher_max_test_mse=1.0,
        teacher_min_test_r2=-1.0,
        teacher_cache_dir=out_dir / "teacher_cache",
        teacher_cache_mode="off",
        teacher_cache_version="test_v1",
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
        lamb=1e-3,
        topk=2,
        grid_number=11,
        iteration=1,
        teacher_max_test_mse=1e-8,
        teacher_min_test_r2=0.999999,
        teacher_cache_dir=out_dir / "teacher_cache",
        teacher_cache_mode="off",
        teacher_cache_version="test_v1",
        make_plots=False,
        quiet=True,
    )

    row = result["rows"][0]
    assert row["teacher_quality_gate_pass"] is False
    assert "teacher_test_mse" in row["teacher_quality_gate_reason"] or "teacher_test_r2" in row["teacher_quality_gate_reason"]
    assert row["formula_validation_result"] is False
    assert row["baseline_formula_raw"] == []
    assert row["icbr_formula_raw"] == []


def test_teacher_cache_hit_after_first_run() -> None:
    base_dir = Path("tmp") / f"icbr_benchmark_teacher_cache_{uuid.uuid4().hex}"
    out_dir_1 = base_dir / "run1"
    out_dir_2 = base_dir / "run2"
    cache_dir = base_dir / "cache"

    run1 = run_benchmark(
        tasks=["minimal"],
        seeds=[0],
        output_dir=out_dir_1,
        train_num=16,
        test_num=16,
        train_steps=2,
        lr=0.05,
        lamb=1e-3,
        topk=2,
        grid_number=11,
        iteration=1,
        teacher_max_test_mse=1.0,
        teacher_min_test_r2=-1.0,
        teacher_cache_dir=cache_dir,
        teacher_cache_mode="readwrite",
        teacher_cache_version="stage11_test_v1",
        make_plots=False,
        quiet=True,
    )
    row1 = run1["rows"][0]
    assert row1["teacher_cache_hit"] is False
    assert Path(row1["teacher_cache_path"]).exists()

    run2 = run_benchmark(
        tasks=["minimal"],
        seeds=[0],
        output_dir=out_dir_2,
        train_num=16,
        test_num=16,
        train_steps=2,
        lr=0.05,
        lamb=1e-3,
        topk=2,
        grid_number=11,
        iteration=1,
        teacher_max_test_mse=1.0,
        teacher_min_test_r2=-1.0,
        teacher_cache_dir=cache_dir,
        teacher_cache_mode="readwrite",
        teacher_cache_version="stage11_test_v1",
        make_plots=False,
        quiet=True,
    )
    row2 = run2["rows"][0]
    assert row2["teacher_cache_hit"] is True
    assert row2["teacher_cache_key"] == row1["teacher_cache_key"]


def test_feynman_dataset_file_loading_smoke() -> None:
    base_dir = Path("tmp") / f"icbr_benchmark_feynman_{uuid.uuid4().hex}"
    dataset_root = base_dir / "datasets"
    variant_dir = dataset_root / "Feynman_with_units"
    variant_dir.mkdir(parents=True, exist_ok=True)

    rng = np.random.default_rng(0)
    m0 = rng.uniform(0.1, 1.0, size=(96, 1))
    v = rng.uniform(0.0, 0.9, size=(96, 1))
    c = rng.uniform(1.0, 2.0, size=(96, 1))
    y = m0 / np.sqrt(1.0 - (v**2) / (c**2))
    raw = np.concatenate([m0, v, c, y], axis=1).astype(np.float32)
    np.savetxt(variant_dir / "I.10.7", raw)

    equations_csv = dataset_root / "FeynmanEquations.csv"
    equations_csv.write_text("Filename,Formula\nI.10.7,m0/sqrt(1-v^2/c^2)\n", encoding="utf-8")

    out_dir = base_dir / "out"
    main(
        [
            "--tasks",
            "feynman_I_10_7",
            "--seeds",
            "0",
            "--output-dir",
            str(out_dir),
            "--train-num",
            "48",
            "--test-num",
            "24",
            "--train-steps",
            "2",
            "--lr",
            "0.03",
            "--lamb",
            "1e-3",
            "--topk",
            "2",
            "--grid-number",
            "11",
            "--iteration",
            "1",
            "--teacher-max-test-mse",
            "10.0",
            "--teacher-min-test-r2",
            "-10.0",
            "--teacher-cache-dir",
            str(base_dir / "cache"),
            "--teacher-cache-mode",
            "readwrite",
            "--feynman-root",
            str(dataset_root),
            "--feynman-variant",
            "Feynman_with_units",
            "--feynman-split-strategy",
            "random",
            "--feynman-width-mid",
            "5,2",
            "--quiet",
            "--no-plots",
        ]
    )

    summary = json.loads((out_dir / "icbr_benchmark_summary.json").read_text(encoding="utf-8"))
    assert summary["config"]["tasks"] == ["feynman_I_10_7"]
    assert summary["config"]["feynman"]["enabled"] is True
    assert summary["config"]["feynman"]["variant"] == "Feynman_with_units"
    row = summary["rows"][0]
    assert row["task"] == "feynman_I_10_7"
    assert row["task_kind"] == "feynman_file"
    assert row["task_source"] == "feynman_file"
    assert row["target_formula"] == "m0/sqrt(1-v^2/c^2)"


def test_feynman_task_tokens_expand() -> None:
    assert _expand_feynman_task_tokens(
        ["feynman_paper10"],
        feynman_root=Path("tmp") / f"icbr_benchmark_fake_{uuid.uuid4().hex}",
        feynman_variant="Feynman_with_units",
        feynman_max_datasets=10,
        feynman_dataset_select_seed=2,
    ) == [
        "feynman_I_9_18",
        "feynman_I_10_7",
        "feynman_I_12_1",
        "feynman_I_12_4",
        "feynman_I_13_4",
        "feynman_I_34_1",
        "feynman_II_6_15a",
        "feynman_II_6_15b",
        "feynman_II_21_32",
        "feynman_II_34_29a",
    ]
