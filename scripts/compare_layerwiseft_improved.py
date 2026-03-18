from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Tuple

import pandas as pd

from scripts.project_paths import (
    DEFAULT_BENCHMARK_ABLATION_DIR,
    LEGACY_BENCHMARK_ABLATION_DIR,
    resolve_preferred_dir,
    resolve_named_child,
    validate_child_name,
)


VARIANT_FULL = "full"
VARIANT_WOFT = "wolayerwiseft"
VARIANT_NEW = "layerwiseft_esreg"


def parse_csv_ints(raw: str) -> List[int]:
    return [int(item.strip()) for item in raw.split(",") if item.strip()]


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def run_improved_variant(repo_root: Path, ablation_root: Path, args: argparse.Namespace) -> Path:
    out_dir = ensure_dir(resolve_named_child(ablation_root, args.new_variant, kind="variant name"))
    cmd = [
        args.python,
        str(repo_root / "symkanbenchmark.py"),
        "--tasks",
        "full",
        "--output-dir",
        str(out_dir),
        "--stagewise-seeds",
        args.seeds,
        "--global-seed",
        str(args.global_seed),
        "--layerwise-finetune-steps",
        str(args.layerwise_finetune_steps),
        "--layerwise-finetune-lamb",
        str(args.layerwise_finetune_lamb),
        "--layerwise-use-validation",
        "--layerwise-validation-ratio",
        str(args.layerwise_validation_ratio),
        "--layerwise-early-stop-patience",
        str(args.layerwise_early_stop_patience),
        "--layerwise-early-stop-min-delta",
        str(args.layerwise_early_stop_min_delta),
        "--layerwise-eval-interval",
        str(args.layerwise_eval_interval),
        "--layerwise-validation-n-sample",
        str(args.layerwise_validation_n_sample),
    ]
    if args.layerwise_validation_seed is not None:
        cmd.extend(["--layerwise-validation-seed", str(args.layerwise_validation_seed)])
    if args.quiet:
        cmd.append("--quiet")
    elif args.verbose:
        cmd.append("--verbose")

    print(f"[run] training improved variant -> {out_dir}")
    subprocess.run(cmd, check=True, cwd=str(repo_root))
    return out_dir


def find_runs(variant_dir: Path, seeds: List[int]) -> List[Tuple[int, Path]]:
    pairs: List[Tuple[int, Path]] = []
    for run_dir in sorted(variant_dir.iterdir()):
        if not run_dir.is_dir() or not run_dir.name.startswith("run_"):
            continue
        metrics_path = run_dir / "metrics.json"
        if not metrics_path.exists():
            continue
        with open(metrics_path, encoding="utf-8") as f:
            seed = int(json.load(f)["metrics"].get("stage_seed", -1))
        if seeds and seed not in seeds:
            continue
        pairs.append((seed, run_dir))
    return sorted(pairs, key=lambda x: x[0])


def load_variant_frame(ablation_root: Path, variant: str, seeds: List[int]) -> pd.DataFrame:
    variant_dir = resolve_named_child(ablation_root, variant, kind="variant name")
    if not variant_dir.exists():
        raise FileNotFoundError(f"variant directory not found: {variant_dir}")

    rows = []
    for seed, run_dir in find_runs(variant_dir, seeds):
        metrics_path = run_dir / "metrics.json"
        with open(metrics_path, encoding="utf-8") as f:
            m = json.load(f)["metrics"]

        val_path = run_dir / "formula_validation.csv"
        if val_path.exists():
            val_df = pd.read_csv(val_path)
            r2_mean = float(val_df["r2"].mean()) if len(val_df) > 0 else float("nan")
            r2_neg = int((val_df["r2"] < 0).sum()) if len(val_df) > 0 else 0
        else:
            r2_mean = float("nan")
            r2_neg = 0

        rows.append(
            {
                "variant": variant,
                "seed": int(seed),
                "run_dir": str(run_dir),
                "final_acc": float(m.get("final_acc", float("nan"))),
                "macro_auc": float(m.get("macro_auc", float("nan"))),
                "expr_complexity_mean": float(m.get("expr_complexity_mean", float("nan"))),
                "validation_mean_r2": r2_mean,
                "validation_negative_r2_count": r2_neg,
                "symbolic_total_seconds": float(m.get("symbolic_total_seconds", float("nan"))),
                "stage_total_seconds": float(m.get("stage_total_seconds", float("nan"))),
                "final_n_edge": int(m.get("final_n_edge", -1)),
                "effective_input_dim": int(m.get("effective_input_dim", -1)),
                "layerwise_finetune_steps": int(m.get("layerwise_finetune_steps", -1)),
                "layerwise_finetune_lamb": float(m.get("layerwise_finetune_lamb", float("nan"))),
                "layerwise_use_validation": bool(m.get("layerwise_use_validation", False)),
            }
        )

    return pd.DataFrame(rows)


def summarize(df: pd.DataFrame) -> pd.DataFrame:
    metric_cols = [
        "final_acc",
        "macro_auc",
        "expr_complexity_mean",
        "validation_mean_r2",
        "validation_negative_r2_count",
        "symbolic_total_seconds",
        "stage_total_seconds",
        "final_n_edge",
        "effective_input_dim",
    ]
    rows = []
    for variant, grp in df.groupby("variant", as_index=False):
        row: Dict[str, object] = {"variant": variant, "n_runs": int(len(grp))}
        for col in metric_cols:
            vals = pd.to_numeric(grp[col], errors="coerce")
            if not isinstance(vals, pd.Series):
                vals = pd.Series([vals], dtype=float)
            row[f"{col}_mean"] = float(vals.mean())
            row[f"{col}_std"] = float(vals.std(ddof=1)) if len(vals) > 1 else float("nan")
        rows.append(row)
    return pd.DataFrame(rows).sort_values("variant").reset_index(drop=True)


def pairwise_delta(summary_df: pd.DataFrame, left: str, right: str) -> pd.DataFrame:
    l = summary_df.loc[summary_df["variant"] == left]
    r = summary_df.loc[summary_df["variant"] == right]
    if len(l) != 1 or len(r) != 1:
        raise ValueError(f"missing variant in summary: {left} or {right}")
    l = l.iloc[0]
    r = r.iloc[0]

    metrics = [
        "final_acc_mean",
        "macro_auc_mean",
        "expr_complexity_mean_mean",
        "validation_mean_r2_mean",
        "validation_negative_r2_count_mean",
        "symbolic_total_seconds_mean",
        "stage_total_seconds_mean",
        "final_n_edge_mean",
        "effective_input_dim_mean",
    ]
    rows = []
    for m in metrics:
        rows.append(
            {
                "metric": m,
                "left": left,
                "right": right,
                "left_value": float(l[m]),
                "right_value": float(r[m]),
                "delta_left_minus_right": float(l[m] - r[m]),
            }
        )
    return pd.DataFrame(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run and compare improved layerwiseft against full and wo-layerwiseft")
    parser.add_argument("--ablation-dir", default=DEFAULT_BENCHMARK_ABLATION_DIR)
    parser.add_argument("--new-variant", default=VARIANT_NEW)
    parser.add_argument("--seeds", default="42,52,62")
    parser.add_argument("--global-seed", type=int, default=123)
    parser.add_argument("--python", default=sys.executable)
    parser.add_argument("--skip-run", action="store_true", help="do not train new variant; only aggregate")
    parser.add_argument("--quiet", action="store_true")
    parser.add_argument("--verbose", action="store_true")

    parser.add_argument("--layerwise-finetune-steps", type=int, default=60)
    parser.add_argument("--layerwise-finetune-lamb", type=float, default=1e-5)
    parser.add_argument("--layerwise-validation-ratio", type=float, default=0.15)
    parser.add_argument("--layerwise-validation-seed", type=int, default=None)
    parser.add_argument("--layerwise-early-stop-patience", type=int, default=2)
    parser.add_argument("--layerwise-early-stop-min-delta", type=float, default=1e-3)
    parser.add_argument("--layerwise-eval-interval", type=int, default=20)
    parser.add_argument("--layerwise-validation-n-sample", type=int, default=300)
    args = parser.parse_args()
    args.new_variant = validate_child_name(args.new_variant, kind="variant name")

    repo_root = Path(__file__).resolve().parents[1]
    ablation_root = resolve_preferred_dir(
        str(args.ablation_dir),
        repo_root=repo_root,
        default_dir=DEFAULT_BENCHMARK_ABLATION_DIR,
        legacy_dir=LEGACY_BENCHMARK_ABLATION_DIR,
    )
    seeds = parse_csv_ints(args.seeds)

    if not args.skip_run:
        run_improved_variant(repo_root, ablation_root, args)

    out_dir = ensure_dir(ablation_root / "layerwiseft_improved_analysis")
    print("[analyze] loading variants...")
    df_full = load_variant_frame(ablation_root, VARIANT_FULL, seeds)
    df_woft = load_variant_frame(ablation_root, VARIANT_WOFT, seeds)
    df_new = load_variant_frame(ablation_root, args.new_variant, seeds)

    raw_df = pd.concat([df_full, df_woft, df_new], ignore_index=True)
    summary_df = summarize(raw_df)
    delta_new_vs_full = pairwise_delta(summary_df, args.new_variant, VARIANT_FULL)
    delta_new_vs_woft = pairwise_delta(summary_df, args.new_variant, VARIANT_WOFT)

    raw_path = out_dir / "comparison_raw.csv"
    summary_path = out_dir / "comparison_summary.csv"
    d1_path = out_dir / "delta_new_vs_full.csv"
    d2_path = out_dir / "delta_new_vs_wolayerwiseft.csv"

    raw_df.to_csv(raw_path, index=False, encoding="utf-8-sig")
    summary_df.to_csv(summary_path, index=False, encoding="utf-8-sig")
    delta_new_vs_full.to_csv(d1_path, index=False, encoding="utf-8-sig")
    delta_new_vs_woft.to_csv(d2_path, index=False, encoding="utf-8-sig")

    print(f"[done] raw: {raw_path}")
    print(f"[done] summary: {summary_path}")
    print(f"[done] delta(new-full): {d1_path}")
    print(f"[done] delta(new-woft): {d2_path}")


if __name__ == "__main__":
    main()
