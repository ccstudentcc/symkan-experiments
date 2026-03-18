from __future__ import annotations

import argparse
import re
import warnings
from pathlib import Path
from typing import Dict, List

from scripts.project_paths import (
    DEFAULT_BENCHMARK_AB_DIR,
    LEGACY_BENCHMARK_AB_DIR,
    resolve_preferred_dir,
    resolve_named_child,
    validate_child_name,
)


np = None
pd = None
EmptyDataError = None
_RUN_SEED_PATTERN = re.compile(r"^run_(\d+)_seed(-?\d+)$")


def _ensure_analysis_deps() -> None:
    global np, pd, EmptyDataError
    if np is None:
        import numpy as _np

        np = _np
    if pd is None:
        import pandas as _pd
        from pandas.errors import EmptyDataError as _EmptyDataError

        pd = _pd
        EmptyDataError = _EmptyDataError


def _read_runs(root: Path, variant: str) -> pd.DataFrame:
    _ensure_analysis_deps()
    path = resolve_named_child(root, variant, kind="variant name") / "symkanbenchmark_runs.csv"
    if not path.exists():
        raise FileNotFoundError(f"missing file: {path}")
    df = pd.read_csv(path)
    return _dedupe_stage_seed(df, source_label=str(path))


def _dedupe_stage_seed(df: pd.DataFrame, source_label: str) -> pd.DataFrame:
    _ensure_analysis_deps()
    if "stage_seed" not in df.columns:
        raise ValueError(f"stage_seed column not found in {source_label}")

    out = df.copy()
    dup_mask = out["stage_seed"].duplicated(keep=False)
    if not dup_mask.any():
        return out

    duplicate_count = int(dup_mask.sum())
    unique_duplicate_seeds = int(out.loc[dup_mask, "stage_seed"].nunique())

    if "run_index" in out.columns:
        out["_run_index_numeric"] = pd.to_numeric(out["run_index"], errors="coerce")
        out = (
            out.sort_values(["stage_seed", "_run_index_numeric"], kind="mergesort")
            .drop_duplicates(subset=["stage_seed"], keep="last")
            .drop(columns=["_run_index_numeric"])
        )
        warnings.warn(
            (
                f"duplicate stage_seed rows found in {source_label}: {duplicate_count} rows "
                f"({unique_duplicate_seeds} seeds); keeping largest run_index per seed"
            ),
            category=UserWarning,
            stacklevel=2,
        )
    else:
        out = out.sort_values(["stage_seed"], kind="mergesort").drop_duplicates(subset=["stage_seed"], keep="last")
        warnings.warn(
            (
                f"duplicate stage_seed rows found in {source_label}: {duplicate_count} rows "
                f"({unique_duplicate_seeds} seeds); run_index missing, keeping last row per seed"
            ),
            category=UserWarning,
            stacklevel=2,
        )
    return out.reset_index(drop=True)


def _ensure_columns(df: pd.DataFrame, columns: List[str], source_label: str) -> None:
    missing = [col for col in columns if col not in df.columns]
    if missing:
        raise ValueError(f"missing columns in {source_label}: {missing}")


def _variant_summary(df: pd.DataFrame, variant: str, metrics: List[str]) -> pd.DataFrame:
    _ensure_analysis_deps()
    _ensure_columns(df, metrics, source_label=f"variant={variant}")
    rows = []
    for m in metrics:
        s = df[m]
        rows.append(
            {
                "variant": variant,
                "metric": m,
                "mean": float(s.mean()),
                "median": float(s.median()),
                "std": float(s.std(ddof=0)),
                "min": float(s.min()),
                "max": float(s.max()),
            }
        )
    return pd.DataFrame(rows)


def _pairwise_delta(
    base_df: pd.DataFrame,
    cur_df: pd.DataFrame,
    base_name: str,
    cur_name: str,
    metrics: List[str],
) -> pd.DataFrame:
    _ensure_analysis_deps()
    b_df = _dedupe_stage_seed(base_df, source_label=f"pairwise baseline={base_name}")
    c_df = _dedupe_stage_seed(cur_df, source_label=f"pairwise variant={cur_name}")
    _ensure_columns(b_df, metrics, source_label=f"pairwise baseline={base_name}")
    _ensure_columns(c_df, metrics, source_label=f"pairwise variant={cur_name}")

    b = b_df.set_index("stage_seed")
    c = c_df.set_index("stage_seed")
    merged = b.join(c, lsuffix="_base", rsuffix="_cur", how="inner")

    rows = []
    for m in metrics:
        d = merged[f"{m}_cur"] - merged[f"{m}_base"]
        prefer_higher = _metric_prefers_higher(m)
        if prefer_higher:
            win_count = int((d > 0).sum())
            lose_count = int((d < 0).sum())
        else:
            win_count = int((d < 0).sum())
            lose_count = int((d > 0).sum())
        rows.append(
            {
                "baseline": base_name,
                "variant": cur_name,
                "metric": m,
                "mean_delta": float(d.mean()),
                "median_delta": float(d.median()),
                "std_delta": float(d.std(ddof=0)),
                "win_count": win_count,
                "lose_count": lose_count,
                "tie_count": int((d == 0).sum()),
            }
        )
    return pd.DataFrame(rows)


def _seedwise_delta(
    base_df: pd.DataFrame,
    cur_df: pd.DataFrame,
    base_name: str,
    cur_name: str,
    metrics: List[str],
) -> pd.DataFrame:
    _ensure_analysis_deps()
    b_df = _dedupe_stage_seed(base_df, source_label=f"seedwise baseline={base_name}")
    c_df = _dedupe_stage_seed(cur_df, source_label=f"seedwise variant={cur_name}")
    _ensure_columns(b_df, metrics, source_label=f"seedwise baseline={base_name}")
    _ensure_columns(c_df, metrics, source_label=f"seedwise variant={cur_name}")

    b = b_df.set_index("stage_seed")
    c = c_df.set_index("stage_seed")
    merged = b.join(c, lsuffix="_base", rsuffix="_cur", how="inner")

    out = pd.DataFrame(index=merged.index)
    out.index.name = "stage_seed"
    out["baseline"] = base_name
    out["variant"] = cur_name
    for m in metrics:
        out[f"delta_{m}"] = merged[f"{m}_cur"] - merged[f"{m}_base"]
    return out.reset_index()


def _trace_effective_rounds(root: Path, variant: str, seeds: List[int]) -> pd.DataFrame:
    _ensure_analysis_deps()
    rows = []
    variant_dir = resolve_named_child(root, variant, kind="variant name")
    if not variant_dir.exists() or not variant_dir.is_dir():
        raise FileNotFoundError(f"variant directory not found: {variant_dir}")
    trace_paths_by_seed: Dict[int, tuple[int, Path]] = {}

    for child in variant_dir.iterdir():
        if not child.is_dir():
            continue
        match = _RUN_SEED_PATTERN.fullmatch(child.name)
        if not match:
            continue
        run_index = int(match.group(1))
        seed = int(match.group(2))
        trace_path = child / "symbolize_trace.csv"
        if trace_path.exists():
            existing = trace_paths_by_seed.get(seed)
            if existing is not None and existing[0] != run_index:
                warnings.warn(
                    (
                        f"multiple runs found for variant={variant}, stage_seed={seed}; "
                        f"using run_{max(existing[0], run_index):02d}"
                    ),
                    category=UserWarning,
                    stacklevel=2,
                )
            if existing is None or run_index > existing[0]:
                trace_paths_by_seed[seed] = (run_index, trace_path)

    def _append_empty_row(stage_seed: int) -> None:
        rows.append(
            {
                "variant": variant,
                "stage_seed": stage_seed,
                "rounds": 0,
                "effective_rounds": 0,
                "total_edges_removed": 0,
                "mean_drop_ratio": np.nan,
                "max_drop_ratio": np.nan,
            }
        )

    for seed in seeds:
        run_info = trace_paths_by_seed.get(int(seed))
        if run_info is None:
            warnings.warn(
                f"missing symbolize_trace.csv for variant={variant}, stage_seed={seed}",
                category=UserWarning,
                stacklevel=2,
            )
            _append_empty_row(int(seed))
            continue
        _, p = run_info
        if not p.exists():
            warnings.warn(
                f"missing file: {p}",
                category=UserWarning,
                stacklevel=2,
            )
            _append_empty_row(int(seed))
            continue

        # Some runs may leave a whitespace-only trace file; treat it as empty trace.
        try:
            t = pd.read_csv(p)
        except EmptyDataError:
            _append_empty_row(seed)
            continue

        if t.empty:
            _append_empty_row(seed)
            continue

        removed = (t["edges_before"] - t["edges_after"]).clip(lower=0)
        drop_ratio = t["drop_ratio"] if "drop_ratio" in t.columns else pd.Series(np.nan, index=t.index)
        rows.append(
            {
                "variant": variant,
                "stage_seed": seed,
                "rounds": int(len(t)),
                "effective_rounds": int((removed > 0).sum()),
                "total_edges_removed": int(removed.sum()),
                "mean_drop_ratio": float(drop_ratio.mean()),
                "max_drop_ratio": float(drop_ratio.max()),
            }
        )
    return pd.DataFrame(rows)


def _pick_metric_name(all_frames: List[pd.DataFrame], candidates: List[str]) -> str:
    _ensure_analysis_deps()
    for name in candidates:
        if all(name in frame.columns for frame in all_frames):
            return name
    raise ValueError(f"none of metric columns found: {candidates}")


def _metric_prefers_higher(metric: str) -> bool:
    lower_is_better = {
        "symbolic_total_seconds",
        "symbolic_core_seconds",
        "symbolize_wall_time_s",
        "export_wall_time_s",
        "post_symbolic_eval_wall_time_s",
        "run_total_wall_time_s",
        "run_overhead_wall_time_s",
        "stage_total_seconds",
        "stage_train_total_seconds",
        "stage_prune_total_seconds",
        "stage_final_finetune_seconds",
        "final_n_edge",
    }
    return metric not in lower_is_better


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate benchmark_ab comparison tables.")
    parser.add_argument("--root", default=DEFAULT_BENCHMARK_AB_DIR, help="benchmark root directory")
    parser.add_argument("--baseline", default="baseline", help="baseline variant name")
    parser.add_argument("--variants", default="adaptive,adaptive_auto", help="comma-separated compare variants")
    parser.add_argument(
        "--output",
        default=f"{DEFAULT_BENCHMARK_AB_DIR}/comparison",
        help="output directory",
    )
    args = parser.parse_args()
    _ensure_analysis_deps()

    repo_root = Path(__file__).resolve().parents[1]
    root = resolve_preferred_dir(
        str(args.root),
        repo_root=repo_root,
        default_dir=DEFAULT_BENCHMARK_AB_DIR,
        legacy_dir=LEGACY_BENCHMARK_AB_DIR,
    )
    out_dir = resolve_preferred_dir(
        str(args.output),
        repo_root=repo_root,
        default_dir=f"{DEFAULT_BENCHMARK_AB_DIR}/comparison",
        legacy_dir=f"{LEGACY_BENCHMARK_AB_DIR}/comparison",
    )
    out_dir.mkdir(parents=True, exist_ok=True)

    baseline_name = validate_child_name(args.baseline, kind="baseline name")
    variant_names = [validate_child_name(v, kind="variant name") for v in args.variants.split(",") if v.strip()]

    baseline_df = _read_runs(root, baseline_name)
    variant_dfs = {name: _read_runs(root, name) for name in variant_names}
    all_frames = [baseline_df, *variant_dfs.values()]
    frame_map = {baseline_name: baseline_df, **variant_dfs}
    symbolic_metric = _pick_metric_name(all_frames, ["symbolic_core_seconds", "symbolic_total_seconds"])
    symbolize_wall_metric = _pick_metric_name(all_frames, ["symbolize_wall_time_s", "export_wall_time_s"])
    metrics = [
        "final_acc",
        "macro_auc",
        symbolic_metric,
        symbolize_wall_metric,
    ]
    missing_validation_r2 = [name for name, frame in frame_map.items() if "validation_mean_r2" not in frame.columns]
    if missing_validation_r2:
        warnings.warn(
            f"skip validation_mean_r2 because missing in variants: {missing_validation_r2}",
            category=UserWarning,
            stacklevel=2,
        )
    else:
        metrics.append("validation_mean_r2")
    if all("run_total_wall_time_s" in frame.columns for frame in all_frames):
        metrics.append("run_total_wall_time_s")
    metrics.append("final_n_edge")
    for name, frame in frame_map.items():
        _ensure_columns(frame, ["final_acc", "macro_auc", "final_n_edge"], source_label=f"variant={name}")
    seeds = sorted({int(v) for v in baseline_df["stage_seed"].tolist()})

    all_variant_summaries: List[pd.DataFrame] = []
    all_pairwise: List[pd.DataFrame] = []
    all_seedwise: List[pd.DataFrame] = []
    all_trace_seedwise: List[pd.DataFrame] = []

    all_variant_summaries.append(_variant_summary(baseline_df, baseline_name, metrics))
    all_trace_seedwise.append(_trace_effective_rounds(root, baseline_name, seeds))

    for variant in variant_names:
        cur_df = variant_dfs[variant]
        all_variant_summaries.append(_variant_summary(cur_df, variant, metrics))
        all_pairwise.append(_pairwise_delta(baseline_df, cur_df, baseline_name, variant, metrics))
        all_seedwise.append(_seedwise_delta(baseline_df, cur_df, baseline_name, variant, metrics))
        all_trace_seedwise.append(_trace_effective_rounds(root, variant, seeds))

    variant_summary = pd.concat(all_variant_summaries, ignore_index=True)
    pairwise_summary = pd.concat(all_pairwise, ignore_index=True) if all_pairwise else pd.DataFrame()
    seedwise_delta = pd.concat(all_seedwise, ignore_index=True) if all_seedwise else pd.DataFrame()
    trace_seedwise = pd.concat(all_trace_seedwise, ignore_index=True)

    trace_summary = (
        trace_seedwise.groupby("variant", as_index=False)
        .agg(
            rounds_mean=("rounds", "mean"),
            effective_rounds_mean=("effective_rounds", "mean"),
            total_edges_removed_mean=("total_edges_removed", "mean"),
            mean_drop_ratio_mean=("mean_drop_ratio", "mean"),
            max_drop_ratio_mean=("max_drop_ratio", "mean"),
        )
        .sort_values("variant")
        .reset_index(drop=True)
    )

    variant_summary.to_csv(out_dir / "variant_summary.csv", index=False, encoding="utf-8-sig")
    pairwise_summary.to_csv(out_dir / "pairwise_delta_summary.csv", index=False, encoding="utf-8-sig")
    seedwise_delta.to_csv(out_dir / "seedwise_delta.csv", index=False, encoding="utf-8-sig")
    trace_seedwise.to_csv(out_dir / "trace_seedwise.csv", index=False, encoding="utf-8-sig")
    trace_summary.to_csv(out_dir / "trace_summary.csv", index=False, encoding="utf-8-sig")

    # Markdown summary for paper/report usage.
    md_lines = []
    md_lines.append("# Benchmark AB Comparison Summary")
    md_lines.append("")
    md_lines.append(f"- baseline: {baseline_name}")
    md_lines.append(f"- variants: {', '.join(variant_names)}")
    md_lines.append("")

    md_lines.append("## Variant Metrics")
    md_lines.append("")
    md_lines.append("| variant | metric | mean | median | std | min | max |")
    md_lines.append("|---|---|---:|---:|---:|---:|---:|")
    for _, row in variant_summary.sort_values(["variant", "metric"]).iterrows():
        md_lines.append(
            f"| {row['variant']} | {row['metric']} | {row['mean']:.6f} | {row['median']:.6f} | {row['std']:.6f} | {row['min']:.6f} | {row['max']:.6f} |"
        )
    md_lines.append("")

    if not pairwise_summary.empty:
        md_lines.append("## Baseline Pairwise Delta")
        md_lines.append("")
        md_lines.append("| baseline | variant | metric | mean_delta | median_delta | std_delta | win | lose | tie |")
        md_lines.append("|---|---|---|---:|---:|---:|---:|---:|---:|")
        for _, row in pairwise_summary.sort_values(["variant", "metric"]).iterrows():
            md_lines.append(
                f"| {row['baseline']} | {row['variant']} | {row['metric']} | {row['mean_delta']:.6f} | {row['median_delta']:.6f} | {row['std_delta']:.6f} | {int(row['win_count'])} | {int(row['lose_count'])} | {int(row['tie_count'])} |"
            )
        md_lines.append("")

    md_lines.append("## Symbolize Trace Rhythm")
    md_lines.append("")
    md_lines.append("| variant | rounds_mean | effective_rounds_mean | total_edges_removed_mean | mean_drop_ratio_mean | max_drop_ratio_mean |")
    md_lines.append("|---|---:|---:|---:|---:|---:|")
    for _, row in trace_summary.sort_values("variant").iterrows():
        mean_drop = row["mean_drop_ratio_mean"]
        max_drop = row["max_drop_ratio_mean"]
        mean_drop_s = "" if pd.isna(mean_drop) else f"{mean_drop:.6f}"
        max_drop_s = "" if pd.isna(max_drop) else f"{max_drop:.6f}"
        md_lines.append(
            f"| {row['variant']} | {row['rounds_mean']:.4f} | {row['effective_rounds_mean']:.4f} | {row['total_edges_removed_mean']:.4f} | {mean_drop_s} | {max_drop_s} |"
        )
    md_lines.append("")

    md_lines.append("## Auto Conclusion")
    md_lines.append("")
    def _pick(metric: str, prefer_higher: bool = True):
        piv = variant_summary[variant_summary["metric"] == metric].set_index("variant")
        if prefer_higher:
            best = piv["mean"].idxmax()
        else:
            best = piv["mean"].idxmin()
        most_stable = piv["std"].idxmin()
        return best, most_stable

    best_final_acc, stable_final_acc = _pick("final_acc", prefer_higher=True)
    best_macro_auc, stable_macro_auc = _pick("macro_auc", prefer_higher=True)
    fastest_symbolic, _ = _pick(symbolic_metric, prefer_higher=False)
    fastest_wall, _ = _pick(symbolize_wall_metric, prefer_higher=False)

    md_lines.append(f"- Highest mean final_acc: {best_final_acc}")
    md_lines.append(f"- Most stable final_acc (lowest std): {stable_final_acc}")
    md_lines.append(f"- Highest mean macro_auc: {best_macro_auc}")
    md_lines.append(f"- Fastest {symbolic_metric}: {fastest_symbolic}")
    md_lines.append(f"- Fastest {symbolize_wall_metric}: {fastest_wall}")

    if not pairwise_summary.empty:
        target = pairwise_summary[pairwise_summary["metric"].isin(["final_acc", "macro_auc"])].copy()
        if len(target) > 0:
            md_lines.append("")
            md_lines.append("- Pairwise note vs baseline:")
            for _, row in target.sort_values(["variant", "metric"]).iterrows():
                md_lines.append(
                    f"  - {row['variant']} on {row['metric']}: win={int(row['win_count'])}, lose={int(row['lose_count'])}, median_delta={row['median_delta']:.6f}, mean_delta={row['mean_delta']:.6f}"
                )

    (out_dir / "comparison_summary.md").write_text("\n".join(md_lines) + "\n", encoding="utf-8")

    print("generated files:")
    for name in [
        "variant_summary.csv",
        "pairwise_delta_summary.csv",
        "seedwise_delta.csv",
        "trace_seedwise.csv",
        "trace_summary.csv",
        "comparison_summary.md",
    ]:
        print(str(out_dir / name))


if __name__ == "__main__":
    main()
