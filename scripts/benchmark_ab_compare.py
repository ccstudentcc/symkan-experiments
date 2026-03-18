from __future__ import annotations

import argparse
from pathlib import Path
from typing import Dict, List

import numpy as np
import pandas as pd
from pandas.errors import EmptyDataError

from scripts.project_paths import (
    DEFAULT_BENCHMARK_AB_DIR,
    LEGACY_BENCHMARK_AB_DIR,
    resolve_preferred_dir,
    resolve_named_child,
    validate_child_name,
)


def _read_runs(root: Path, variant: str) -> pd.DataFrame:
    path = resolve_named_child(root, variant, kind="variant name") / "symkanbenchmark_runs.csv"
    if not path.exists():
        raise FileNotFoundError(f"missing file: {path}")
    df = pd.read_csv(path)
    if "stage_seed" not in df.columns:
        raise ValueError(f"stage_seed column not found in {path}")
    return df


def _variant_summary(df: pd.DataFrame, variant: str, metrics: List[str]) -> pd.DataFrame:
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
    b = base_df.set_index("stage_seed")
    c = cur_df.set_index("stage_seed")
    merged = b.join(c, lsuffix="_base", rsuffix="_cur", how="inner")

    rows = []
    for m in metrics:
        d = merged[f"{m}_cur"] - merged[f"{m}_base"]
        rows.append(
            {
                "baseline": base_name,
                "variant": cur_name,
                "metric": m,
                "mean_delta": float(d.mean()),
                "median_delta": float(d.median()),
                "std_delta": float(d.std(ddof=0)),
                "win_count": int((d > 0).sum()),
                "lose_count": int((d < 0).sum()),
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
    b = base_df.set_index("stage_seed")
    c = cur_df.set_index("stage_seed")
    merged = b.join(c, lsuffix="_base", rsuffix="_cur", how="inner")

    out = pd.DataFrame(index=merged.index)
    out.index.name = "stage_seed"
    out["baseline"] = base_name
    out["variant"] = cur_name
    for m in metrics:
        out[f"delta_{m}"] = merged[f"{m}_cur"] - merged[f"{m}_base"]
    return out.reset_index()


def _trace_effective_rounds(root: Path, variant: str, seeds: List[int]) -> pd.DataFrame:
    rows = []

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

    for idx, seed in enumerate(seeds, start=1):
        p = resolve_named_child(root, variant, kind="variant name") / f"run_{idx:02d}_seed{seed}" / "symbolize_trace.csv"
        if not p.exists():
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

    metrics = [
        "final_acc",
        "macro_auc",
        "validation_mean_r2",
        "symbolic_total_seconds",
        "export_wall_time_s",
        "final_n_edge",
    ]

    baseline_name = validate_child_name(args.baseline, kind="baseline name")
    variant_names = [validate_child_name(v, kind="variant name") for v in args.variants.split(",") if v.strip()]

    baseline_df = _read_runs(root, baseline_name)
    seeds = [int(v) for v in baseline_df["stage_seed"].tolist()]

    all_variant_summaries: List[pd.DataFrame] = []
    all_pairwise: List[pd.DataFrame] = []
    all_seedwise: List[pd.DataFrame] = []
    all_trace_seedwise: List[pd.DataFrame] = []

    all_variant_summaries.append(_variant_summary(baseline_df, baseline_name, metrics))
    all_trace_seedwise.append(_trace_effective_rounds(root, baseline_name, seeds))

    for variant in variant_names:
        cur_df = _read_runs(root, variant)
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
    fastest_symbolic, _ = _pick("symbolic_total_seconds", prefer_higher=False)
    fastest_wall, _ = _pick("export_wall_time_s", prefer_higher=False)

    md_lines.append(f"- Highest mean final_acc: {best_final_acc}")
    md_lines.append(f"- Most stable final_acc (lowest std): {stable_final_acc}")
    md_lines.append(f"- Highest mean macro_auc: {best_macro_auc}")
    md_lines.append(f"- Fastest symbolic_total_seconds: {fastest_symbolic}")
    md_lines.append(f"- Fastest export_wall_time_s: {fastest_wall}")

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
