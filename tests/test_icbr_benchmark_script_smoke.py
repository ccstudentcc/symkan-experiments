from __future__ import annotations

import csv
import json
import uuid
from pathlib import Path

import numpy as np

from scripts.icbr_benchmark import (
    _expand_feynman_task_tokens,
    _normalize_variants,
    _resolve_default_tasks_and_seeds,
    _resolve_training_config,
    main,
    run_benchmark,
)


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
    variant_rows_path = out_dir / "icbr_benchmark_variant_rows.csv"
    task_stats_csv = out_dir / "icbr_benchmark_task_stats.csv"
    significance_csv = out_dir / "icbr_benchmark_significance.csv"
    summary_json = out_dir / "icbr_benchmark_summary.json"
    summary_md = out_dir / "icbr_benchmark_summary.md"

    assert rows_path.exists()
    assert variant_rows_path.exists()
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
        "feynman_dataset_filename",
        "feynman_dataset_rows",
        "feynman_dataset_columns",
        "feynman_split_seed",
        "feynman_equation_metadata",
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
        "shared_tensor_candidate_time_ratio_no_shared_vs_full",
        "shared_tensor_symbolic_time_ratio_no_shared_vs_full",
        "contextual_replay_mse_gain_full_vs_no_replay",
        "contextual_replay_target_mse_gain_full_vs_no_replay",
        "contextual_replay_rank_inversion_rate_full",
        "explicit_commit_mse_gain_explicit_vs_refit",
        "explicit_commit_target_mse_gain_explicit_vs_refit",
        "explicit_commit_refit_commit_param_drift_l2_mean",
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
    assert summary["config"]["variants"] == ["baseline", "icbr_full"]
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
    assert summary["config"]["teacher_prune_policy"]["enabled"] is False
    assert summary["aggregates"]["variant_ablation"]["overall"]["baseline"]["row_count"] == 4
    assert summary["aggregates"]["variant_ablation"]["overall"]["icbr_full"]["row_count"] == 4
    assert "challenge_evidence" in summary["aggregates"]
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
    assert summary["artifacts"]["variant_rows_csv"].endswith("icbr_benchmark_variant_rows.csv")
    visuals = summary["artifacts"]["visualizations"]
    assert "enabled" in visuals
    assert "files" in visuals

    with variant_rows_path.open("r", encoding="utf-8") as f:
        variant_rows = list(csv.DictReader(f))
    assert len(variant_rows) == 8
    assert {row["variant"] for row in variant_rows} == {"baseline", "icbr_full"}
    assert all(row["teacher_quality_gate_pass"] == "True" for row in variant_rows)


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
    assert resolved["train_steps"] == 200
    assert resolved["lr"] == 1e-2
    assert resolved["lamb"] == 1e-3
    assert overrides == {
        "train_num": False,
        "test_num": False,
        "train_steps": False,
        "lr": False,
        "lamb": False,
    }


def test_feynman_reference_profile_resolves_expected_defaults() -> None:
    resolved, overrides = _resolve_training_config(
        profile="feynman_reference",
        train_num=None,
        test_num=None,
        train_steps=None,
        lr=None,
        lamb=None,
    )
    assert resolved["train_num"] == 2000
    assert resolved["test_num"] == 1000
    assert resolved["train_steps"] == 200
    assert resolved["lr"] == 1e-2
    assert resolved["lamb"] == 1e-2
    assert overrides == {
        "train_num": False,
        "test_num": False,
        "train_steps": False,
        "lr": False,
        "lamb": False,
    }


def test_feynman_reference_defaults_task_and_seed() -> None:
    tasks, seeds = _resolve_default_tasks_and_seeds(
        profile="feynman_reference",
        tasks_raw=None,
        seeds_raw=None,
    )
    assert tasks == ["feynman_paper10"]
    assert seeds == [1]


def test_normalize_variants_keeps_baseline_and_icbr_full() -> None:
    assert _normalize_variants("icbr_no_replay") == ["baseline", "icbr_no_replay", "icbr_full"]
    assert _normalize_variants("baseline,icbr_full,icbr_no_shared") == [
        "baseline",
        "icbr_full",
        "icbr_no_shared",
    ]


def test_run_benchmark_supports_ablation_variants() -> None:
    out_dir = Path("tmp") / f"icbr_benchmark_variants_{uuid.uuid4().hex}"
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
        teacher_max_test_mse=1.0,
        teacher_min_test_r2=-1.0,
        teacher_cache_dir=out_dir / "teacher_cache",
        teacher_cache_mode="off",
        teacher_cache_version="stage15_test_v1",
        variants=["baseline", "icbr_no_replay", "icbr_full"],
        make_plots=False,
        quiet=True,
    )

    variant_rows = result["variant_rows"]
    assert len(variant_rows) == 3
    assert {row["variant"] for row in variant_rows} == {"baseline", "icbr_full", "icbr_no_replay"}
    summary = result["summary"]
    assert summary["config"]["variants"] == ["baseline", "icbr_no_replay", "icbr_full"]
    assert summary["aggregates"]["variant_ablation"]["overall"]["icbr_no_replay"]["row_count"] == 1
    summary_md = (out_dir / "icbr_benchmark_summary.md").read_text(encoding="utf-8")
    assert "Variant formula overview" in summary_md
    assert "icbr_no_replay formula (display, rounded)" in summary_md
    assert "formula (raw)" not in summary_md


def test_formula_comparison_keeps_requested_variants_when_teacher_gate_skips() -> None:
    out_dir = Path("tmp") / f"icbr_benchmark_formula_skip_{uuid.uuid4().hex}"
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
        teacher_cache_version="stage17_formula_skip_test_v1",
        variants=["baseline", "icbr_no_replay", "icbr_full"],
        make_plots=False,
        quiet=True,
    )

    variant_rows = result["variant_rows"]
    assert len(variant_rows) == 3
    assert {row["variant"] for row in variant_rows} == {"baseline", "icbr_no_replay", "icbr_full"}
    assert all(row["formula_display"] == [] for row in variant_rows)
    assert all(row["formula_raw"] == [] for row in variant_rows)

    summary_md = (out_dir / "icbr_benchmark_summary.md").read_text(encoding="utf-8")
    assert "icbr_no_replay: symbolic_s=nan" in summary_md
    assert "icbr_no_replay formula (display, rounded):" in summary_md
    assert "icbr_no_replay formula export error: skipped_by_teacher_quality_gate:" in summary_md
    assert "formula (raw)" not in summary_md


def test_quiet_mode_suppresses_training_and_symbolic_console_output(capsys) -> None:
    out_dir = Path("tmp") / f"icbr_benchmark_quiet_{uuid.uuid4().hex}"
    run_benchmark(
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
        teacher_max_test_mse=1.0,
        teacher_min_test_r2=-1.0,
        teacher_cache_dir=out_dir / "teacher_cache",
        teacher_cache_mode="off",
        teacher_cache_version="stage19_quiet_test_v1",
        variants=["baseline", "icbr_no_replay", "icbr_full"],
        make_plots=False,
        quiet=True,
    )
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""


def test_visualization_upgrade_emits_variant_and_q123_plots() -> None:
    out_dir = Path("tmp") / f"icbr_benchmark_visual_upgrade_{uuid.uuid4().hex}"
    result = run_benchmark(
        tasks=["minimal", "combo"],
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
        teacher_max_test_mse=1.0,
        teacher_min_test_r2=-1.0,
        teacher_cache_dir=out_dir / "teacher_cache",
        teacher_cache_mode="off",
        teacher_cache_version="stage18_visual_test_v1",
        variants=["baseline", "icbr_full", "icbr_no_replay", "icbr_no_shared", "icbr_refit_commit"],
        make_plots=True,
        quiet=True,
    )

    summary = result["summary"]
    visuals = summary["artifacts"]["visualizations"]
    assert visuals["enabled"] is True
    assert "plots" in visuals
    file_names = {Path(path).name for path in visuals["files"]}
    expected = {
        "icbr_benchmark_symbolic_time_errorbar.png",
        "icbr_benchmark_speedup_boxplot.png",
        "icbr_benchmark_mse_shift_boxplot.png",
        "icbr_benchmark_variant_overview.png",
        "icbr_benchmark_q123_evidence_by_task.png",
    }
    assert expected.issubset(file_names)
    for path in visuals["files"]:
        assert Path(path).exists()

    import matplotlib.image as mpimg

    variant_overview_path = out_dir / "icbr_benchmark_variant_overview.png"
    variant_overview_img = mpimg.imread(variant_overview_path)
    # Final Stage20 layout: one task per row, but each row contains two horizontal panels.
    assert variant_overview_img.shape[1] > variant_overview_img.shape[0]
    assert visuals["plots"]["symbolic_time_errorbar"]["chart_type"] == "point_ci95"
    assert visuals["plots"]["symbolic_time_errorbar"]["stat_note"].startswith("point=geometric mean")
    assert visuals["plots"]["symbolic_time_errorbar"]["legend_placement"] == "figure_top_outside"
    assert "scale" in visuals["plots"]["symbolic_time_errorbar"]["y_label"]
    assert visuals["plots"]["speedup_boxplot"]["chart_type"] == "violin_box_points"
    assert visuals["plots"]["speedup_boxplot"]["kde_bandwidth_rule"] == "silverman"
    assert visuals["plots"]["speedup_boxplot"]["y_label"] == "Speedup x (linear scale; higher is better)"
    assert visuals["plots"]["mse_shift_boxplot"]["chart_type"] == "violin_box_points"
    assert "scale" in visuals["plots"]["mse_shift_boxplot"]["y_label"]
    assert visuals["plots"]["variant_overview"]["chart_type"] == "task_row_two_panel_point_ci95"
    assert visuals["plots"]["variant_overview"]["layout"] == "one task per row; two columns = SymbolicTime / merged MSEs"
    assert visuals["plots"]["variant_overview"]["legend_placement"] == "figure_top_outside"
    assert visuals["plots"]["variant_overview"]["scale_label_placement"] == "title_band_left"
    assert all("scale" in label for label in visuals["plots"]["variant_overview"]["time_y_label_by_task"].values())
    assert visuals["plots"]["variant_overview"]["mse_y_label"] == "MSE / Target MSE (log scale)"
    assert visuals["plots"]["q123_evidence_by_task"]["chart_type"] == "point_ci95"
    assert visuals["plots"]["q123_evidence_by_task"]["scale_by_panel"]["shared_tensor_symbolic_time_ratio_no_shared_vs_full"] == "log2_ratio"
    assert visuals["plots"]["q123_evidence_by_task"]["scale_by_panel"]["contextual_replay_mse_ratio_no_replay_vs_full"] == "log2_ratio"
    assert visuals["plots"]["q123_evidence_by_task"]["scale_by_panel"]["explicit_commit_mse_ratio_refit_vs_full"] == "log2_ratio"
    assert visuals["plots"]["q123_evidence_by_task"]["scale_label_placement"] == "title_band_left"
    assert visuals["plots"]["q123_evidence_by_task"]["y_label_by_panel"]["contextual_replay_mse_ratio_no_replay_vs_full"] == "log2(no_replay MSE / full MSE)"
    assert visuals["plots"]["q123_evidence_by_task"]["y_label_by_panel"]["explicit_commit_mse_ratio_refit_vs_full"] == "log2(refit_commit MSE / full MSE)"

    summary_md = (out_dir / "icbr_benchmark_summary.md").read_text(encoding="utf-8")
    assert "icbr_benchmark_variant_overview.png" in summary_md
    assert "icbr_benchmark_q123_evidence_by_task.png" in summary_md


def test_replot_only_rebuilds_visualizations_from_existing_artifacts() -> None:
    out_dir = Path("tmp") / f"icbr_benchmark_replot_only_{uuid.uuid4().hex}"
    run_benchmark(
        tasks=["minimal", "combo"],
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
        teacher_max_test_mse=1.0,
        teacher_min_test_r2=-1.0,
        teacher_cache_dir=out_dir / "teacher_cache",
        teacher_cache_mode="off",
        teacher_cache_version="stage21_replot_test_v1",
        variants=["baseline", "icbr_full", "icbr_no_replay", "icbr_no_shared", "icbr_refit_commit"],
        make_plots=False,
        quiet=True,
    )

    summary_md_before = (out_dir / "icbr_benchmark_summary.md").read_text(encoding="utf-8")
    assert "Visualization disabled" in summary_md_before

    main(
        [
            "--replot-only",
            "--replot-summary-json",
            str(out_dir / "icbr_benchmark_summary.json"),
            "--replot-rows-csv",
            str(out_dir / "icbr_benchmark_rows.csv"),
            "--replot-variant-rows-csv",
            str(out_dir / "icbr_benchmark_variant_rows.csv"),
            "--output-dir",
            str(out_dir),
            "--quiet",
        ]
    )

    summary = json.loads((out_dir / "icbr_benchmark_summary.json").read_text(encoding="utf-8"))
    visuals = summary["artifacts"]["visualizations"]
    assert visuals["enabled"] is True
    assert "plots" in visuals
    expected = {
        "icbr_benchmark_symbolic_time_errorbar.png",
        "icbr_benchmark_speedup_boxplot.png",
        "icbr_benchmark_mse_shift_boxplot.png",
        "icbr_benchmark_variant_overview.png",
        "icbr_benchmark_q123_evidence_by_task.png",
    }
    assert expected.issubset({Path(path).name for path in visuals["files"]})
    assert all(Path(path).exists() for path in visuals["files"])
    assert visuals["plots"]["speedup_boxplot"]["kde_bandwidth_rule"] == "silverman"
    assert visuals["plots"]["variant_overview"]["chart_type"] == "task_row_two_panel_point_ci95"
    assert visuals["plots"]["variant_overview"]["legend_placement"] == "figure_top_outside"
    assert visuals["plots"]["variant_overview"]["scale_label_placement"] == "title_band_left"
    assert visuals["plots"]["q123_evidence_by_task"]["scale_by_panel"]["shared_tensor_symbolic_time_ratio_no_shared_vs_full"] == "log2_ratio"
    assert visuals["plots"]["q123_evidence_by_task"]["scale_by_panel"]["contextual_replay_mse_ratio_no_replay_vs_full"] == "log2_ratio"
    assert visuals["plots"]["q123_evidence_by_task"]["scale_label_placement"] == "title_band_left"

    summary_md_after = (out_dir / "icbr_benchmark_summary.md").read_text(encoding="utf-8")
    assert "Visualization disabled" not in summary_md_after
    assert "icbr_benchmark_variant_overview.png" in summary_md_after


def test_quality_profile_enables_teacher_prune_by_default() -> None:
    out_dir = Path("tmp") / f"icbr_benchmark_quality_prune_{uuid.uuid4().hex}"
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
        teacher_max_test_mse=1.0,
        teacher_min_test_r2=-1.0,
        teacher_cache_dir=out_dir / "teacher_cache",
        teacher_cache_mode="off",
        teacher_cache_version="stage15_quality_prune_test_v1",
        profile_name="quality",
        make_plots=False,
        quiet=True,
    )

    summary = result["summary"]
    assert summary["config"]["teacher_prune_policy"]["enabled"] is True
    assert summary["config"]["teacher_training"]["minimal"]["post_train_prune"] is True


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
            "--feynman-fit-opt",
            "LBFGS",
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
    assert summary["config"]["feynman"]["dataset_select_seed"] == 1
    assert summary["config"]["feynman"]["split_strategy_seed"] == 1
    assert summary["config"]["teacher_training"]["feynman_I_10_7"]["grid"] == 20
    assert summary["config"]["teacher_training"]["feynman_I_10_7"]["k"] == 3
    assert summary["config"]["teacher_training"]["feynman_I_10_7"]["post_train_prune"] is True
    assert summary["config"]["teacher_training"]["feynman_I_10_7"]["post_prune_steps"] == 100
    assert summary["config"]["teacher_training"]["feynman_I_10_7"]["post_prune_lr"] == 1e-3
    assert summary["config"]["teacher_training"]["feynman_I_10_7"]["post_prune_lamb"] == 1e-2
    assert summary["config"]["teacher_training"]["feynman_I_10_7"]["post_prune_early_stop"] is True
    assert summary["config"]["teacher_training"]["feynman_I_10_7"]["post_prune_eval_every"] == 5
    assert summary["config"]["teacher_training"]["feynman_I_10_7"]["post_prune_min_delta"] == 1e-6
    assert summary["config"]["teacher_training"]["feynman_I_10_7"]["post_prune_patience"] == 2
    row = summary["rows"][0]
    assert row["task"] == "feynman_I_10_7"
    assert row["task_kind"] == "feynman_file"
    assert row["task_source"] == "feynman_file"
    assert row["target_formula"] == "m0/sqrt(1-v^2/c^2)"
    assert row["feynman_dataset_filename"] == "I.10.7"
    assert row["feynman_dataset_rows"] == 96
    assert row["feynman_dataset_columns"] == 4
    assert row["feynman_split_seed"] == 1
    assert row["feynman_equation_metadata"]["Filename"] == "I.10.7"
    assert row["feynman_equation_metadata"]["Formula"] == "m0/sqrt(1-v^2/c^2)"
    task_meta = summary["config"]["feynman"]["task_metadata"]["feynman_I_10_7"]
    assert task_meta["filename"] == "I.10.7"
    assert task_meta["total_rows"] == 96
    assert task_meta["total_columns"] == 4
    assert task_meta["n_var"] == 3
    assert task_meta["target_formula"] == "m0/sqrt(1-v^2/c^2)"


def test_feynman_post_prune_override_smoke() -> None:
    base_dir = Path("tmp") / f"icbr_benchmark_feynman_post_prune_{uuid.uuid4().hex}"
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
            "--feynman-fit-opt",
            "LBFGS",
            "--feynman-split-strategy",
            "random",
            "--feynman-width-mid",
            "5,2",
            "--feynman-post-prune-steps",
            "7",
            "--feynman-post-prune-lr",
            "0.002",
            "--feynman-post-prune-lamb",
            "0.001",
            "--feynman-post-prune-eval-every",
            "3",
            "--feynman-post-prune-min-delta",
            "1e-5",
            "--feynman-post-prune-patience",
            "4",
            "--quiet",
            "--no-plots",
        ]
    )

    summary = json.loads((out_dir / "icbr_benchmark_summary.json").read_text(encoding="utf-8"))
    task_cfg = summary["config"]["teacher_training"]["feynman_I_10_7"]
    assert task_cfg["post_prune_steps"] == 7
    assert task_cfg["post_prune_lr"] == 0.002
    assert task_cfg["post_prune_lamb"] == 0.001
    assert task_cfg["post_prune_eval_every"] == 3
    assert task_cfg["post_prune_min_delta"] == 1e-5
    assert task_cfg["post_prune_patience"] == 4
    assert task_cfg["opt"] == "LBFGS"


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
