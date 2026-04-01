from __future__ import annotations

from pathlib import Path
import shutil
from uuid import uuid4

import pandas as pd
import pytest

from scripts.benchmark_ab_compare import (
    _baseline_icbr_compare_enabled,
    _baseline_icbr_mechanism_summary,
    _baseline_icbr_primary_effect,
    _baseline_icbr_shared_check,
    _pairwise_delta,
    _trace_effective_rounds,
)


def _write_trace_csv(path: Path, rows: list[tuple[int, int, float]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = ["edges_before,edges_after,drop_ratio"]
    for before, after, ratio in rows:
        lines.append(f"{before},{after},{ratio}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _make_local_tmpdir() -> Path:
    root = (Path("outputs") / f"trace_effective_rounds_{uuid4().hex}").resolve()
    root.mkdir(parents=True, exist_ok=False)
    return root


def test_trace_effective_rounds_scans_by_seed_not_run_index() -> None:
    root = _make_local_tmpdir()
    try:
        variant = "baseline"
        _write_trace_csv(
            root / variant / "run_99_seed42" / "symbolize_trace.csv",
            [(100, 95, 0.05), (95, 95, 0.0)],
        )
        _write_trace_csv(
            root / variant / "run_01_seed62" / "symbolize_trace.csv",
            [(90, 80, 0.111111)],
        )

        with pytest.warns(UserWarning, match="stage_seed=52"):
            out = _trace_effective_rounds(root, variant, seeds=[42, 52, 62])

        assert list(out["stage_seed"]) == [42, 52, 62]
        seed42 = out[out["stage_seed"] == 42].iloc[0]
        seed52 = out[out["stage_seed"] == 52].iloc[0]
        seed62 = out[out["stage_seed"] == 62].iloc[0]

        assert int(seed42["rounds"]) == 2
        assert int(seed42["effective_rounds"]) == 1
        assert int(seed42["total_edges_removed"]) == 5
        assert int(seed52["rounds"]) == 0
        assert int(seed62["rounds"]) == 1
        assert int(seed62["total_edges_removed"]) == 10
    finally:
        shutil.rmtree(root, ignore_errors=True)


def test_trace_effective_rounds_prefers_largest_run_index_for_same_seed() -> None:
    root = _make_local_tmpdir()
    try:
        variant = "baseline"
        _write_trace_csv(
            root / variant / "run_01_seed42" / "symbolize_trace.csv",
            [(100, 99, 0.01)],
        )
        _write_trace_csv(
            root / variant / "run_02_seed42" / "symbolize_trace.csv",
            [(100, 90, 0.10)],
        )

        with pytest.warns(UserWarning, match="multiple runs found for variant=baseline, stage_seed=42"):
            out = _trace_effective_rounds(root, variant, seeds=[42])

        seed42 = out[out["stage_seed"] == 42].iloc[0]
        assert int(seed42["rounds"]) == 1
        assert int(seed42["total_edges_removed"]) == 10
    finally:
        shutil.rmtree(root, ignore_errors=True)


def test_pairwise_delta_counts_lower_time_as_win() -> None:
    base_df = pd.DataFrame(
        {
            "stage_seed": [42, 52],
            "run_total_wall_time_s": [100.0, 110.0],
        }
    )
    cur_df = pd.DataFrame(
        {
            "stage_seed": [42, 52],
            "run_total_wall_time_s": [90.0, 108.0],
        }
    )

    out = _pairwise_delta(
        base_df=base_df,
        cur_df=cur_df,
        base_name="baseline",
        cur_name="adaptive_auto",
        metrics=["run_total_wall_time_s"],
    )

    row = out.iloc[0]
    assert int(row["win_count"]) == 2
    assert int(row["lose_count"]) == 0


def test_pairwise_delta_counts_higher_metric_as_win() -> None:
    base_df = pd.DataFrame(
        {
            "stage_seed": [42, 52],
            "final_acc": [0.70, 0.72],
        }
    )
    cur_df = pd.DataFrame(
        {
            "stage_seed": [42, 52],
            "final_acc": [0.75, 0.71],
        }
    )

    out = _pairwise_delta(
        base_df=base_df,
        cur_df=cur_df,
        base_name="baseline",
        cur_name="adaptive_auto",
        metrics=["final_acc"],
    )

    row = out.iloc[0]
    assert int(row["win_count"]) == 1
    assert int(row["lose_count"]) == 1


def test_pairwise_delta_counts_lower_edge_as_win() -> None:
    base_df = pd.DataFrame(
        {
            "stage_seed": [42, 52],
            "final_n_edge": [100, 120],
        }
    )
    cur_df = pd.DataFrame(
        {
            "stage_seed": [42, 52],
            "final_n_edge": [90, 130],
        }
    )

    out = _pairwise_delta(
        base_df=base_df,
        cur_df=cur_df,
        base_name="baseline",
        cur_name="adaptive_auto",
        metrics=["final_n_edge"],
    )

    row = out.iloc[0]
    assert int(row["win_count"]) == 1
    assert int(row["lose_count"]) == 1


def test_pairwise_delta_dedupes_duplicate_stage_seed_by_run_index() -> None:
    base_df = pd.DataFrame(
        {
            "stage_seed": [42, 42],
            "run_index": [1, 2],
            "final_acc": [0.80, 0.90],
        }
    )
    cur_df = pd.DataFrame(
        {
            "stage_seed": [42, 42],
            "run_index": [1, 2],
            "final_acc": [0.85, 0.95],
        }
    )

    with pytest.warns(UserWarning, match="duplicate stage_seed rows found"):
        out = _pairwise_delta(
            base_df=base_df,
            cur_df=cur_df,
            base_name="baseline",
            cur_name="adaptive_auto",
            metrics=["final_acc"],
        )

    row = out.iloc[0]
    assert pytest.approx(float(row["mean_delta"]), abs=1e-12) == 0.05
    assert int(row["win_count"]) == 1
    assert int(row["lose_count"]) == 0


def test_trace_effective_rounds_raises_when_variant_dir_missing() -> None:
    missing_root = Path("outputs") / f"trace_missing_{uuid4().hex}"
    with pytest.raises(FileNotFoundError, match="variant directory not found"):
        _trace_effective_rounds(missing_root, variant="baseline", seeds=[42])


def test_baseline_icbr_compare_enabled_only_for_expected_pair() -> None:
    base_df = pd.DataFrame(
        {
            "symbolic_core_seconds": [1.0],
            "final_teacher_imitation_mse": [0.1],
            "final_target_mse": [0.2],
            "final_target_r2": [0.7],
            "formula_export_success": [True],
            "base_acc": [0.8],
            "enhanced_acc": [0.85],
            "enhanced_n_edge": [10],
            "selected_stage": ["final"],
            "pre_symbolic_n_edge": [9],
            "symbolic_backend": ["baseline"],
        }
    )
    icbr_df = base_df.copy()
    icbr_df["symbolic_backend"] = ["icbr"]
    frame_map = {
        "baseline": base_df,
        "baseline_icbr": icbr_df,
        "baseline_fastlib": base_df.copy(),
        "baseline_icbr_fastlib": icbr_df.copy(),
    }

    assert _baseline_icbr_compare_enabled(
        baseline_name="baseline",
        variant_names=["baseline_icbr"],
        frame_map=frame_map,
    )
    assert _baseline_icbr_compare_enabled(
        baseline_name="baseline_fastlib",
        variant_names=["baseline_icbr_fastlib"],
        frame_map=frame_map,
    )
    assert not _baseline_icbr_compare_enabled(
        baseline_name="baseline",
        variant_names=["baseline_fastlib"],
        frame_map=frame_map,
    )


def test_baseline_icbr_special_summaries_capture_alignment_and_effects() -> None:
    base_df = pd.DataFrame(
        {
            "stage_seed": [42, 52],
            "base_acc": [0.8, 0.81],
            "enhanced_acc": [0.85, 0.86],
            "enhanced_n_edge": [10, 11],
            "selected_stage": ["final", "final"],
            "pre_symbolic_n_edge": [9, 9],
            "numeric_cache_hit": [False, False],
            "symbolic_prep_cache_hit": [False, False],
            "symbolic_core_seconds": [4.0, 5.0],
            "final_teacher_imitation_mse": [0.20, 0.18],
            "final_target_mse": [0.30, 0.28],
            "final_target_r2": [0.70, 0.72],
            "formula_export_success": [True, True],
            "symbolic_backend": ["baseline", "baseline"],
        }
    )
    icbr_df = pd.DataFrame(
        {
            "stage_seed": [42, 52],
            "base_acc": [0.8, 0.81],
            "enhanced_acc": [0.85, 0.86],
            "enhanced_n_edge": [10, 11],
            "selected_stage": ["final", "final"],
            "pre_symbolic_n_edge": [9, 9],
            "numeric_cache_hit": [True, True],
            "symbolic_prep_cache_hit": [True, True],
            "symbolic_core_seconds": [2.0, 2.5],
            "final_teacher_imitation_mse": [0.10, 0.12],
            "final_target_mse": [0.25, 0.22],
            "final_target_r2": [0.75, 0.78],
            "formula_export_success": [True, True],
            "symbolic_backend": ["icbr", "icbr"],
            "icbr_candidate_generation_wall_time_s": [0.8, 1.0],
            "icbr_replay_rerank_wall_time_s": [0.4, 0.5],
            "icbr_replay_rank_inversion_rate": [0.25, 0.5],
        }
    )
    trace_seedwise = pd.DataFrame(
        {
            "variant": [
                "baseline_fastlib",
                "baseline_fastlib",
                "baseline_icbr_fastlib",
                "baseline_icbr_fastlib",
            ],
            "stage_seed": [42, 52, 42, 52],
            "rounds": [2, 3, 2, 3],
            "effective_rounds": [1, 2, 1, 2],
            "total_edges_removed": [5, 7, 5, 7],
            "mean_drop_ratio": [0.1, 0.2, 0.1, 0.2],
            "max_drop_ratio": [0.1, 0.25, 0.1, 0.25],
        }
    )

    shared = _baseline_icbr_shared_check(
        base_df,
        icbr_df,
        trace_seedwise,
        baseline_name="baseline_fastlib",
        icbr_name="baseline_icbr_fastlib",
    )
    primary = _baseline_icbr_primary_effect(base_df, icbr_df)
    mechanism = _baseline_icbr_mechanism_summary(icbr_df)

    assert shared["shared_symbolic_prep_aligned"].tolist() == [True, True]
    speedup_row = primary[primary["metric"] == "symbolic_core_speedup_vs_baseline"].iloc[0]
    assert float(speedup_row["mean"]) == pytest.approx(2.0)
    target_shift_row = primary[primary["metric"] == "final_target_mse_shift"].iloc[0]
    assert float(target_shift_row["mean"]) == pytest.approx(-0.055)
    candidate_share_row = mechanism[mechanism["metric"] == "icbr_candidate_share_of_core_time"].iloc[0]
    assert float(candidate_share_row["mean"]) == pytest.approx(0.4)
