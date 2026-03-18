from __future__ import annotations

from pathlib import Path
import shutil
from uuid import uuid4

import pandas as pd
import pytest

from scripts.benchmark_ab_compare import _pairwise_delta, _trace_effective_rounds


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
