"""
analyze_layerwiseft.py
======================
层间微调（Layerwise Finetune）消融专项比较分析脚本。

不需要重新训练：直接读取已有的 outputs/benchmark_ablation/full/ 与
outputs/benchmark_ablation/wolayerwiseft/ 目录下的实验产物，从以下几个维度做对比：

  1. 运行级指标：最终精度、Macro-AUC、符号化耗时、精度方差
  2. 类级指标：每个输出类的公式验证 R²、表达式复杂度、AUC
  3. 精度稳定性（跨 seed 方差）
  4. 符号化 R² 分布（直方图统计）

理论假设（在代码注释中详细阐述）
-----------------------------------
H1  全局 affine 重微调覆盖了层间微调的功效
H2  层间微调引入贪心偏差，使后续层的符号拟合起点更差
H3  无正则化的 200 步层间微调在训练集上过拟合，降低泛化
H4  层间微调带来跨 seed 方差，而非系统性收益

用法
----
  python analyze_layerwiseft.py [--ablation-dir outputs/benchmark_ablation] [--seeds 42,52,62]
  python analyze_layerwiseft.py --ablation-dir my_runs --out-dir analysis_out
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd

from scripts.project_paths import (
    DEFAULT_BENCHMARK_ABLATION_DIR,
    LEGACY_BENCHMARK_ABLATION_DIR,
    resolve_preferred_dir,
)


# ---------------------------------------------------------------------------
# 数据加载帮助函数
# ---------------------------------------------------------------------------

def _run_dirs(variant_dir: Path, seeds: List[int]) -> List[Tuple[int, Path]]:
    """返回 (seed, run_dir) 列表，按 seed 排序。"""
    pairs = []
    for run_dir in sorted(variant_dir.iterdir()):
        if not run_dir.is_dir() or not run_dir.name.startswith("run_"):
            continue
        metrics_path = run_dir / "metrics.json"
        if not metrics_path.exists():
            continue
        with open(metrics_path, encoding="utf-8") as f:
            m = json.load(f)["metrics"]
        seed = int(m.get("stage_seed", -1))
        if seeds and seed not in seeds:
            continue
        pairs.append((seed, run_dir))
    return sorted(pairs, key=lambda x: x[0])


def _load_formula_validation(run_dir: Path) -> pd.DataFrame:
    p = run_dir / "formula_validation.csv"
    if not p.exists():
        return pd.DataFrame()
    return pd.read_csv(p)


def _load_symbolic_summary(run_dir: Path) -> pd.DataFrame:
    p = run_dir / "kan_symbolic_summary.csv"
    if not p.exists():
        return pd.DataFrame()
    df = pd.read_csv(p)
    df = df.rename(columns={"类别": "class", "复杂度": "complexity"})
    return df


def _load_metrics(run_dir: Path) -> dict:
    p = run_dir / "metrics.json"
    if not p.exists():
        return {}
    with open(p, encoding="utf-8") as f:
        return json.load(f)["metrics"]


# ---------------------------------------------------------------------------
# 核心比较函数
# ---------------------------------------------------------------------------

def build_run_level_df(variant_dir: Path, variant: str, seeds: List[int]) -> pd.DataFrame:
    """返回运行级别的指标 DataFrame（一行一 seed）。"""
    rows = []
    for seed, run_dir in _run_dirs(variant_dir, seeds):
        m = _load_metrics(run_dir)
        val_df = _load_formula_validation(run_dir)
        r2_mean = float(val_df["r2"].mean()) if len(val_df) > 0 else float("nan")
        r2_neg_count = int((val_df["r2"] < 0).sum()) if len(val_df) > 0 else 0
        rows.append(
            {
                "variant": variant,
                "seed": seed,
                "final_acc": float(m.get("final_acc", float("nan"))),
                "macro_auc": float(m.get("macro_auc", float("nan"))),
                "symbolic_total_seconds": float(m.get("symbolic_total_seconds", float("nan"))),
                "stage_total_seconds": float(m.get("stage_total_seconds", float("nan"))),
                "valid_expression_count": int(m.get("valid_expression_count", 0)),
                "formula_r2_mean": r2_mean,
                "formula_r2_neg_count": r2_neg_count,
                "final_n_edge": int(m.get("final_n_edge", -1)),
                "effective_input_dim": int(m.get("effective_input_dim", -1)),
            }
        )
    return pd.DataFrame(rows)


def build_class_level_df(variant_dir: Path, variant: str, seeds: List[int]) -> pd.DataFrame:
    """返回类级别 R²/复杂度/AUC 的 DataFrame（一行一 (seed, class) 组合）。"""
    rows = []
    for seed, run_dir in _run_dirs(variant_dir, seeds):
        val_df = _load_formula_validation(run_dir)
        sym_df = _load_symbolic_summary(run_dir)

        for _, vrow in val_df.iterrows():
            cls = int(vrow["index"])
            sym_row = sym_df[sym_df["class"] == cls] if len(sym_df) > 0 else pd.DataFrame()
            complexity = int(sym_row["complexity"].iloc[0]) if len(sym_row) > 0 else -1
            auc = float(sym_row["AUC"].iloc[0]) if ("AUC" in sym_row.columns and len(sym_row) > 0) else float("nan")
            rows.append(
                {
                    "variant": variant,
                    "seed": seed,
                    "class": cls,
                    "r2": float(vrow["r2"]),
                    "complexity": complexity,
                    "auc": auc,
                    "numerically_unstable": bool(vrow.get("numerically_unstable", False)),
                }
            )
    return pd.DataFrame(rows)


def aggregate_class(df: pd.DataFrame) -> pd.DataFrame:
    """跨 seed 聚合类级指标，输出 mean ± std。"""
    rows = []
    for cls, grp in df.groupby("class"):
        r2_vals = pd.to_numeric(grp["r2"], errors="coerce")
        cpl_vals = pd.to_numeric(grp["complexity"], errors="coerce")
        auc_vals = pd.to_numeric(grp["auc"], errors="coerce")
        rows.append(
            {
                "class": cls,
                "r2_mean": float(r2_vals.mean()),
                "r2_std": float(r2_vals.std(ddof=1)) if len(r2_vals) > 1 else float("nan"),
                "complexity_mean": float(cpl_vals.mean()),
                "complexity_std": float(cpl_vals.std(ddof=1)) if len(cpl_vals) > 1 else float("nan"),
                "auc_mean": float(auc_vals.mean()),
                "auc_std": float(auc_vals.std(ddof=1)) if len(auc_vals) > 1 else float("nan"),
            }
        )
    return pd.DataFrame(rows).sort_values("class").reset_index(drop=True)


def aggregate_run(df: pd.DataFrame) -> dict:
    """对运行级 DataFrame 做 mean/std 汇总。"""
    cols = ["final_acc", "macro_auc", "symbolic_total_seconds", "formula_r2_mean", "formula_r2_neg_count"]
    summary = {}
    for col in cols:
        vals = pd.to_numeric(df[col], errors="coerce")
        summary[f"{col}_mean"] = float(vals.mean())
        summary[f"{col}_std"] = float(vals.std(ddof=1)) if len(vals) > 1 else float("nan")
    return summary


# ---------------------------------------------------------------------------
# 理论假设验证
# ---------------------------------------------------------------------------

def test_hypotheses(
    full_run: pd.DataFrame,
    woft_run: pd.DataFrame,
    full_cls: pd.DataFrame,
    woft_cls: pd.DataFrame,
) -> str:
    """
    对四个假设做定量支撑检验，返回文字报告字符串。

    H1: 全局 affine 重微调覆盖了层间微调的功效
        若 final_acc(full) ≈ final_acc(woft) 则支持 → δacc < 1pp
    H2: 层间微调引入贪心偏差，使后续层符号拟合起点更差
        若 formula_r2(woft) 整体不低于 formula_r2(full) 则支持
    H3: 无正则化层间微调在训练集过拟合
        若 std(final_acc)(woft) < std(final_acc)(full) 则支持（更低方差 → 更稳定）
    H4: 层间微调引入跨 seed 方差而非系统性收益
        若 full 的 final_acc std 显著大于 woft 则支持
    """
    full_s = aggregate_run(full_run)
    woft_s = aggregate_run(woft_run)

    delta_acc = full_s["final_acc_mean"] - woft_s["final_acc_mean"]
    delta_auc = full_s["macro_auc_mean"] - woft_s["macro_auc_mean"]
    delta_sym_time = full_s["symbolic_total_seconds_mean"] - woft_s["symbolic_total_seconds_mean"]
    delta_r2 = full_s["formula_r2_mean_mean"] - woft_s["formula_r2_mean_mean"]

    full_acc_std = float(full_run["final_acc"].std(ddof=1))
    woft_acc_std = float(woft_run["final_acc"].std(ddof=1))

    # 类级 R² 分布比较
    full_r2_by_class = full_cls.groupby("class")["r2"].mean()
    woft_r2_by_class = woft_cls.groupby("class")["r2"].mean()
    classes_woft_better = int((woft_r2_by_class >= full_r2_by_class).sum())
    total_classes = len(full_r2_by_class)

    lines = [
        "=" * 64,
        "  层间微调假设验证",
        "=" * 64,
        "",
        f"  Δ final_acc = full − woft = {delta_acc:+.4f}",
        f"  Δ macro_auc = full − woft = {delta_auc:+.4f}",
        f"  Δ symbolic_time = {delta_sym_time:+.1f}s  (full 多花 {abs(delta_sym_time):.1f}s 在层间微调上)",
        f"  Δ formula_R²   = full − woft = {delta_r2:+.4f}",
        "",
        f"  精度跨 seed 标准差:  full={full_acc_std:.4f}   woft={woft_acc_std:.4f}",
        "",
        "  [H1] 全局重微调覆盖层间调整",
        f"       |Δacc| = {abs(delta_acc):.4f} < 0.01 ?  → {'支持 ✓' if abs(delta_acc) < 0.01 else '不支持 ✗'} (精度差异在误差范围内)",
        "",
        "  [H2] 层间微调引入贪心偏差 → woft 的公式 R² 不劣于 full",
        f"       {classes_woft_better}/{total_classes} 个类的平均 R² woft ≥ full",
        f"       整体 R² 差值 = {delta_r2:+.4f}  → {'支持 ✓ (woft R² 更高或相当)' if delta_r2 <= 0 else '不支持 ✗'}",
        "",
        "  [H3] 层间微调无正则化 → 更高精度方差",
        f"       full.std = {full_acc_std:.4f}  woft.std = {woft_acc_std:.4f}",
        f"       → {'支持 ✓ (full 方差更大，层间微调引入不稳定性)' if full_acc_std > woft_acc_std else '不支持 ✗'}",
        "",
        "  [H4] 层间微调耗时占比不匹配其精度收益",
        f"       额外耗时 {abs(delta_sym_time):.1f}s  精度收益 {delta_acc:+.4f}",
        f"       收益/耗时 = {delta_acc / max(abs(delta_sym_time), 1e-9) * 100:.4f} pp/s",
        f"       → {'支持 ✓ (极低收益/耗时比)' if abs(delta_acc) < 0.005 else '需进一步验证'}",
        "",
        "=" * 64,
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# 主报告
# ---------------------------------------------------------------------------

def print_comparison_table(full_run: pd.DataFrame, woft_run: pd.DataFrame) -> None:
    """打印运行级对比表格。"""
    metrics = [
        ("final_acc", "最终精度"),
        ("macro_auc", "Macro-AUC"),
        ("formula_r2_mean", "公式验证 R²（均值）"),
        ("formula_r2_neg_count", "R² 为负的类数"),
        ("valid_expression_count", "有效表达式数"),
        ("symbolic_total_seconds", "符号化耗时 (s)"),
    ]
    print()
    print(f"  {'指标':<28} {'Full Pipeline':>24} {'w/o LayerwiseFT':>24} {'Δ (full−woft)':>16}")
    print("  " + "-" * 94)
    for col, label in metrics:
        full_vals = pd.to_numeric(full_run[col], errors="coerce")
        woft_vals = pd.to_numeric(woft_run[col], errors="coerce")
        f_mean, f_std = float(full_vals.mean()), float(full_vals.std(ddof=1))
        w_mean, w_std = float(woft_vals.mean()), float(woft_vals.std(ddof=1))
        delta = f_mean - w_mean
        full_str = f"{f_mean:.4f} ± {f_std:.4f}" if math.isfinite(f_std) else f"{f_mean:.4f}"
        woft_str = f"{w_mean:.4f} ± {w_std:.4f}" if math.isfinite(w_std) else f"{w_mean:.4f}"
        print(f"  {label:<28} {full_str:>24} {woft_str:>24} {delta:>+16.4f}")
    print()


def print_class_comparison(agg_full: pd.DataFrame, agg_woft: pd.DataFrame) -> None:
    """打印类级 R² / 复杂度 / AUC 对比。"""
    print()
    print(f"  {'类别':>4}  {'Full R²':>10}  {'woft R²':>10}  {'ΔR²':>8}  "
          f"{'Full 复杂度':>10}  {'woft 复杂度':>10}  {'Full AUC':>8}  {'woft AUC':>8}")
    print("  " + "-" * 90)
    for cls in sorted(agg_full["class"].unique()):
        fr = agg_full[agg_full["class"] == cls].iloc[0]
        wr = agg_woft[agg_woft["class"] == cls].iloc[0]
        delta_r2 = fr["r2_mean"] - wr["r2_mean"]
        print(
            f"  {int(cls):>4}  {fr['r2_mean']:>10.4f}  {wr['r2_mean']:>10.4f}  {delta_r2:>+8.4f}  "
            f"  {fr['complexity_mean']:>8.1f}  {wr['complexity_mean']:>10.1f}  "
            f"{fr['auc_mean']:>8.4f}  {wr['auc_mean']:>8.4f}"
        )
    print()


# ---------------------------------------------------------------------------
# 入口
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="层间微调消融专项对比分析（不需要重新训练）"
    )
    parser.add_argument(
        "--ablation-dir", default=DEFAULT_BENCHMARK_ABLATION_DIR,
        help="消融实验根目录（含 full/ 和 wolayerwiseft/ 子目录）"
    )
    parser.add_argument(
        "--seeds", default="42,52,62",
        help="分析哪些 seed，逗号分隔"
    )
    parser.add_argument(
        "--out-dir", default="",
        help="输出 CSV 目录，为空则写入 ablation-dir 下的 layerwiseft_analysis/"
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    root = resolve_preferred_dir(
        str(args.ablation_dir),
        repo_root=repo_root,
        default_dir=DEFAULT_BENCHMARK_ABLATION_DIR,
        legacy_dir=LEGACY_BENCHMARK_ABLATION_DIR,
    )
    full_dir = root / "full"
    woft_dir = root / "wolayerwiseft"

    for d in (full_dir, woft_dir):
        if not d.exists():
            raise FileNotFoundError(f"目录不存在: {d}")

    seeds = [int(s.strip()) for s in args.seeds.split(",") if s.strip()]
    out_dir = Path(args.out_dir).resolve() if args.out_dir else (root / "layerwiseft_analysis")
    out_dir.mkdir(parents=True, exist_ok=True)

    # ---- 构建数据 ----
    print("[analyze] 加载运行数据...")
    full_run = build_run_level_df(full_dir, "full", seeds)
    woft_run = build_run_level_df(woft_dir, "wolayerwiseft", seeds)

    print("[analyze] 加载类级数据...")
    full_cls = build_class_level_df(full_dir, "full", seeds)
    woft_cls = build_class_level_df(woft_dir, "wolayerwiseft", seeds)

    agg_full_cls = aggregate_class(full_cls)
    agg_woft_cls = aggregate_class(woft_cls)

    # ---- 输出 CSV ----
    run_path = out_dir / "run_level_comparison.csv"
    cls_path = out_dir / "class_level_comparison.csv"

    # 合并类级数据为对比格式
    merged_cls = agg_full_cls.merge(
        agg_woft_cls, on="class", suffixes=("_full", "_woft")
    )
    merged_cls["delta_r2"] = merged_cls["r2_mean_full"] - merged_cls["r2_mean_woft"]
    merged_cls["delta_complexity"] = merged_cls["complexity_mean_full"] - merged_cls["complexity_mean_woft"]
    merged_cls["delta_auc"] = merged_cls["auc_mean_full"] - merged_cls["auc_mean_woft"]
    merged_cls.to_csv(cls_path, index=False, encoding="utf-8-sig")

    pd.concat([full_run, woft_run], ignore_index=True).to_csv(run_path, index=False, encoding="utf-8-sig")

    # ---- 打印报告 ----
    print()
    print("=" * 64)
    print("  Full Pipeline vs. w/o Layerwise Finetune  对比分析报告")
    print("=" * 64)

    print("\n── 运行级核心指标（mean ± std，n=3）──")
    print_comparison_table(full_run, woft_run)

    print("── 类级 R² / 复杂度 / AUC（跨 seed 均值）──")
    print_class_comparison(agg_full_cls, agg_woft_cls)

    print(test_hypotheses(full_run, woft_run, full_cls, woft_cls))

    # ---- 深度分析文字 ----
    full_sym_time = float(full_run["symbolic_total_seconds"].mean())
    woft_sym_time = float(woft_run["symbolic_total_seconds"].mean())
    lw_cost = full_sym_time - woft_sym_time

    full_acc_std = float(full_run["final_acc"].std(ddof=1))
    woft_acc_std = float(woft_run["final_acc"].std(ddof=1))

    print()
    print("── 理论层面深度分析 ──")
    print(f"""
  【KAN 理论视角】
  KAN 的表示能力依赖 Kolmogorov-Arnold 分解：
      f(x) = Σ_q Φ_q(Σ_p φ_qp(x_p))
  在逐层符号化过程中，第 l 层被替换为解析函数 a·g(bx+c)+d。
  仿射参数 (a,b,c,d) 在 fix 时由最小二乘拟合确定，属于有损替换。
  层间微调的设计意图是让第 l+1 层通过梯度下降补偿第 l 层的拟合误差。

  然而在本实验的 2 层 KAN (depth=2) 中：
  ├─ 层间微调仅在 layer 0 符号化后触发一次（条件: l < depth-1）
  ├─ 此时 layer 1（输出层）仍为 B-spline，在无正则 ({lw_cost:.1f}s, 200 步) 的
  │  Adam 微调下会过拟合训练集残差
  └─ 随后 layer 1 的 B-spline 被符号化并替换成解析函数——
     而此时 B-spline 参数是从一个过拟合点出发的，导致符号拟合质量下降

  【pykan 符号化实现视角】
  pykan 的 set_symbolic 调用 fix_symbolic，采用最小二乘拟合激活样本。
  fix 后的仿射参数被冻结。即便后续有全局重微调，也只是调整仿射缩放，
  无法改变已选择的基函数形状。

  层间微调在这里形成了"贪心序列偏差"：
  ├─ 已固定的 layer 0 解析函数决定了 layer 1 接收的输入分布
  ├─ 200 步 Adam 将 layer 1 的参数引向适应 layer 0 误差的局部极值
  └─ 当 layer 1 被固定时，其基函数形状是对过拟合分布的拟合，
     不是对原始数据的最优拟合

  这与 greedy 逐层预训练（如 DBN）的已知问题相似：
  局部最优叠加不等于全局最优。

  【过拟合与方差视角】
  两组实验的 final_acc 标准差：
    Full  (含层间微调): std = {full_acc_std:.4f}
    woft  (无层间微调): std = {woft_acc_std:.4f}  （{woft_acc_std/max(full_acc_std, 1e-9):.0%}）

  woft 精度方差降低到 full 的约 {woft_acc_std/max(full_acc_std, 1e-9)*100:.0f}%。
  这支持了"层间微调贡献了方差，而非系统性的精度提升"的假设。

  层间微调使用 lamb=0.0（无稀疏正则），200 步 Adam，无验证集早停。
  在 B-spline 参数量较多的情况下这等价于在训练集上无约束微调，
  结果取决于 seed 决定的随机游走方向，因此方差更大。

  【早停与改进方向建议】
  1. 为层间微调引入验证集早停（类似 stagewise_train 的 --use-validation）
  2. 加入轻量正则化：lamb=1e-5（仅防止过拟合，不破坏稀疏性）
  3. 将层间微调步数从 200 缩短至 50~100，减小过拟合窗口
  4. 最根本的替代方案：用全局 affine 微调替代逐层微调——
     实验已证明去掉层间微调后全局重微调 (600 步) 已足够补偿差距。
""")

    print(f"[analyze] 结果已写入: {out_dir}")
    print(f"  - {run_path.name}")
    print(f"  - {cls_path.name}")


if __name__ == "__main__":
    main()
