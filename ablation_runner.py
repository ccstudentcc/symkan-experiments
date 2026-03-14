from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List

import numpy as np
import pandas as pd


VARIANT_SPECS: Dict[str, Dict[str, Any]] = {
    "full": {
        "variant_id": "V0",
        "variant_name": "Full Pipeline",
        "extra_args": [],
    },
    "wostagewise": {
        "variant_id": "V1",
        "variant_name": "w/o Stagewise Train",
        "extra_args": [
            "--disable-stagewise-train",
            "--prune-collapse-floor", "0.0",
            "--symbolic-prune-adaptive-acc-drop-tol", "0.7",
        ],
    },
    "wopruning": {
        "variant_id": "V2",
        "variant_name": "w/o Progressive Pruning",
        "extra_args": ["--max-prune-rounds", "0"],
    },
    "wocompact": {
        "variant_id": "V3",
        "variant_name": "w/o Input Compaction",
        "extra_args": ["--no-input-compaction"],
    },
    "wolayerwiseft": {
        "variant_id": "V4",
        "variant_name": "w/o Layerwise Finetune",
        "extra_args": ["--layerwise-finetune-steps", "0"],
    },
}


def parse_csv_list(raw: str) -> List[str]:
    return [item.strip() for item in raw.split(",") if item.strip()]


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def _format_mean_std(mean: float, std: float, ndigits: int = 4) -> str:
    if not np.isfinite(mean):
        return "nan"
    if not np.isfinite(std):
        return f"{mean:.{ndigits}f} ± nan"
    return f"{mean:.{ndigits}f} ± {std:.{ndigits}f}"


def _load_expr_complexity_mean(run_dir: Path) -> float:
    csv_path = run_dir / "kan_symbolic_summary.csv"
    if not csv_path.exists():
        return float("nan")
    try:
        summary_df = pd.read_csv(csv_path)
    except Exception:
        return float("nan")

    if "复杂度" not in summary_df.columns:
        return float("nan")

    if "expr_full" in summary_df.columns:
        valid = summary_df.loc[summary_df["expr_full"] != "N/A (零或常数)", "复杂度"]
    else:
        valid = summary_df["复杂度"]

    if len(valid) == 0:
        return float("nan")
    valid_series = pd.to_numeric(valid, errors="coerce")
    if not isinstance(valid_series, pd.Series):
        valid_series = pd.Series([valid_series], dtype=float)
    return float(valid_series.mean())


def run_variant(
    repo_root: Path,
    output_root: Path,
    variant_key: str,
    common_args: List[str],
    python_executable: str,
) -> Path:
    spec = VARIANT_SPECS[variant_key]
    variant_dir = ensure_dir(output_root / variant_key)

    cmd = [
        python_executable,
        str(repo_root / "symkanbenchmark.py"),
        "--tasks",
        "full",
        "--output-dir",
        str(variant_dir),
        *common_args,
        *spec["extra_args"],
    ]
    subprocess.run(cmd, check=True, cwd=str(repo_root))
    return variant_dir


def collect_variant_results(variant_dir: Path, variant_key: str) -> pd.DataFrame:
    runs_csv = variant_dir / "symkanbenchmark_runs.csv"
    if not runs_csv.exists():
        raise FileNotFoundError(f"missing result file: {runs_csv}")

    df = pd.read_csv(runs_csv)
    spec = VARIANT_SPECS[variant_key]
    df.insert(0, "variant", variant_key)
    df.insert(1, "variant_id", spec["variant_id"])
    df.insert(2, "variant_name", spec["variant_name"])

    expr_means = []
    for _, row in df.iterrows():
        run_dir = Path(str(row["output_dir"]))
        expr_means.append(_load_expr_complexity_mean(run_dir))
    df["expr_complexity_mean"] = expr_means
    return df


def summarize_results(raw_df: pd.DataFrame) -> pd.DataFrame:
    metric_cols = [
        "pre_symbolic_too_dense",
        "effective_target_edges",
        "effective_input_dim",
        "final_acc",
        "expr_complexity_mean",
        "macro_auc",
        "validation_mean_r2",
        "stage_total_seconds",
        "symbolic_total_seconds",
    ]

    rows = []
    for (variant, variant_id, variant_name), grp in raw_df.groupby(["variant", "variant_id", "variant_name"], as_index=False):
        row = {
            "variant": variant,
            "variant_id": variant_id,
            "variant_name": variant_name,
            "n_runs": int(len(grp)),
        }
        for col in metric_cols:
            if col in grp.columns:
                values = pd.to_numeric(grp[col], errors="coerce")
                if not isinstance(values, pd.Series):
                    values = pd.Series([values], dtype=float)
            else:
                values = pd.Series(dtype=float)
            mean = float(values.mean()) if len(values) > 0 else float("nan")
            std = float(values.std(ddof=1)) if len(values) > 1 else float("nan")
            row[f"{col}_mean"] = mean
            row[f"{col}_std"] = std
            row[f"{col}_mean_std"] = _format_mean_std(mean, std)
        rows.append(row)

    return pd.DataFrame(rows).sort_values("variant_id").reset_index(drop=True)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run single-factor ablation matrix for symkan.")
    parser.add_argument(
        "--variants",
        default="full,wostagewise,wopruning,wocompact,wolayerwiseft",
        help="Comma-separated variant keys",
    )
    parser.add_argument("--stagewise-seeds", default="42,52,62")
    parser.add_argument("--global-seed", type=int, default=123)
    parser.add_argument("--output-dir", default="benchmark_ablation")
    parser.add_argument("--python", default=sys.executable, help="Python executable path")
    parser.add_argument("--quiet", action="store_true")
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument(
        "--aggregate-only",
        action="store_true",
        help="跳过运行，直接从 output-dir/<variant>/ 读已有结果做汇总",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent
    output_root = ensure_dir((repo_root / args.output_dir).resolve())

    variant_keys = parse_csv_list(args.variants)
    invalid = [key for key in variant_keys if key not in VARIANT_SPECS]
    if invalid:
        raise ValueError(f"unknown variants: {invalid}")

    common_args = [
        "--stagewise-seeds",
        args.stagewise_seeds,
        "--global-seed",
        str(args.global_seed),
    ]
    if args.quiet:
        common_args.append("--quiet")
    if args.verbose and not args.quiet:
        common_args.append("--verbose")

    all_frames = []
    for key in variant_keys:
        if args.aggregate_only:
            variant_dir = output_root / key
            if not variant_dir.exists():
                print(f"[ablation] skip {key}: directory not found ({variant_dir})")
                continue
            print(f"[ablation] aggregating variant={key} from {variant_dir}")
        else:
            print(f"[ablation] running variant={key}")
            variant_dir = run_variant(
                repo_root=repo_root,
                output_root=output_root,
                variant_key=key,
                common_args=common_args,
                python_executable=args.python,
            )
        frame = collect_variant_results(variant_dir, key)
        all_frames.append(frame)

    if not all_frames:
        raise RuntimeError("no ablation results collected")

    raw_df = pd.concat(all_frames, ignore_index=True)
    summary_df = summarize_results(raw_df)

    raw_path = output_root / "ablation_runs_raw.csv"
    summary_path = output_root / "ablation_runs_summary.csv"
    raw_df.to_csv(raw_path, index=False, encoding="utf-8-sig")
    summary_df.to_csv(summary_path, index=False, encoding="utf-8-sig")

    print(f"[ablation] raw saved: {raw_path}")
    print(f"[ablation] summary saved: {summary_path}")


if __name__ == "__main__":
    main()
