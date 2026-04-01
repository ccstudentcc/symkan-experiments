# 工程版复测报告（2026-04-01 ICBR FAST_LIB 对照）

## 1. 研究设定与口径

1. 本报告对应的比较问题不是“工程版 vs 历史版”，而是“在当前工程版中，较大的 `FAST_LIB` 候选函数库下，baseline symbolic backend 与 ICBR symbolic backend 的对照”。
2. 复测执行日期：`2026-04-01`。
3. 主引用输出目录：`outputs/rerun_v2_engine_safe_20260401/benchmark_ab/`。
4. 当前主引用对照目录包括：
   - `outputs/rerun_v2_engine_safe_20260401/benchmark_ab/baseline_fastlib/`
   - `outputs/rerun_v2_engine_safe_20260401/benchmark_ab/baseline_icbr_fastlib/`
   - `outputs/rerun_v2_engine_safe_20260401/benchmark_ab/comparison_fastlib/`
5. 较保守的 layered 库对照仍保留在：
   - `outputs/rerun_v2_engine_safe_20260401/benchmark_ab/baseline/`
   - `outputs/rerun_v2_engine_safe_20260401/benchmark_ab/baseline_icbr/`
   - `outputs/rerun_v2_engine_safe_20260401/benchmark_ab/comparison/`
6. 本报告的结论边界是：只讨论符号拟合后端差异，不把结果解释成训练策略差异。

执行命令（PowerShell）：

```powershell
# 运行目录：仓库根目录（symkan-experiments/）
C:\Users\chenpeng\miniconda3\envs\kan\python.exe -m scripts.symkanbenchmark `
  --tasks full `
  --stagewise-seeds 42,52,62 `
  --config configs/benchmark_ab/baseline_fastlib.yaml `
  --output-dir outputs/rerun_v2_engine_safe_20260401/benchmark_ab/baseline_fastlib `
  --quiet

C:\Users\chenpeng\miniconda3\envs\kan\python.exe -m scripts.symkanbenchmark `
  --tasks full `
  --stagewise-seeds 42,52,62 `
  --config configs/benchmark_ab/baseline_icbr_fastlib.yaml `
  --output-dir outputs/rerun_v2_engine_safe_20260401/benchmark_ab/baseline_icbr_fastlib `
  --quiet

C:\Users\chenpeng\miniconda3\envs\kan\python.exe -m scripts.benchmark_ab_compare `
  --root outputs/rerun_v2_engine_safe_20260401/benchmark_ab `
  --baseline baseline_fastlib `
  --variants baseline_icbr_fastlib `
  --output outputs/rerun_v2_engine_safe_20260401/benchmark_ab/comparison_fastlib
```

## 2. 实现边界

本轮对照建立在三个明确的工程边界上：

1. ICBR 只改变符号拟合后端，不改变数值训练。
2. `baseline_fastlib` 与 `baseline_icbr_fastlib` 共享 numeric cache 与 shared symbolic-prep 边界。
3. `FAST_LIB` 扩库只写入 `symbolize.lib`，不改变非 `symbolize` section，因此不会 fork numeric cache key。

因此，本报告中的任何性能或质量差异，都只能解释为“同一数值 KAN、同一 shared symbolic-prep、同一较大函数库之后的后端差异”。

## 3. 产物完整性核验

核验结论：本轮产物完整，具备对 `baseline_fastlib` 与 `baseline_icbr_fastlib` 做 backend-only 对照的条件。

1. `baseline_fastlib/` 与 `baseline_icbr_fastlib/` 各包含 `3` 个 run 目录，且各自 `symkanbenchmark_runs.csv` 完整。
2. 通用 compare 产物齐全：
   - `variant_summary.csv`
   - `pairwise_delta_summary.csv`
   - `seedwise_delta.csv`
   - `trace_seedwise.csv`
   - `trace_summary.csv`
   - `comparison_summary.md`
3. ICBR 专用 compare 产物齐全：
   - `baseline_icbr_shared_check.csv`
   - `baseline_icbr_primary_effect.csv`
   - `baseline_icbr_mechanism_summary.csv`

## 4. Shared-State 对齐核验

`comparison_fastlib/baseline_icbr_shared_check.csv` 的核心作用是验证当前 compare 是否真的只反映后端差异。

| stage_seed | shared_numeric_aligned | trace_aligned | shared_symbolic_prep_aligned | baseline_numeric_cache_hit | icbr_numeric_cache_hit | baseline_symbolic_prep_cache_hit | icbr_symbolic_prep_cache_hit |
| ---: | --- | --- | --- | --- | --- | --- | --- |
| 42 | True | True | True | True | True | True | True |
| 52 | True | True | True | True | True | True | True |
| 62 | True | True | True | True | True | True | True |

解释：

1. 三个 seed 的 `shared_numeric_aligned=True`，说明数值训练结果一致。
2. 三个 seed 的 `trace_aligned=True`，说明 `symbolize_trace.csv` 节奏来自相同的 shared symbolic-prep。
3. 三个 seed 的 `shared_symbolic_prep_aligned=True`，说明 ICBR 并未重新执行不同的剪枝或输入压缩流程。
4. 两侧 `numeric_cache_hit=True`、`symbolic_prep_cache_hit=True`，说明这轮 FAST_LIB 扩库没有破坏既有 cache reuse 路径。

## 5. 主结果

### 5.1 变体均值

`comparison_fastlib/variant_summary.csv` 给出的核心均值如下：

| 变体 | final_acc | final_n_edge | macro_auc | run_total_wall_time_s | symbolic_core_seconds | symbolize_wall_time_s | validation_mean_r2 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| baseline_fastlib | 0.794000 | 88.333333 | 0.962537 | 334.638446 | 211.949580 | 328.139783 | -0.451777 |
| baseline_icbr_fastlib | 0.793233 | 88.333333 | 0.962634 | 76.947981 | 34.899150 | 74.484392 | -0.456489 |

直接观察有三点：

1. `final_n_edge` 均值完全一致，说明 ICBR 没有破坏复杂度口径。
2. `symbolic_core_seconds` 与 `run_total_wall_time_s` 都明显下降，说明在更大候选库下 ICBR 的速度优势更强。
3. 质量指标接近持平：`final_acc` 小幅低于 baseline_fastlib，`macro_auc` 与 target-side 指标基本不退化，因此更适合写成“明显提速、质量近似持平”，而不是“全面提质”。

### 5.2 pairwise 差分

| 指标 | mean_delta (baseline_icbr_fastlib - baseline_fastlib) | win / lose / tie |
| --- | ---: | ---: |
| `final_acc` | -0.000767 | 0 / 3 / 0 |
| `final_n_edge` | +0.000000 | 0 / 0 / 3 |
| `macro_auc` | +0.000097 | 3 / 0 / 0 |
| `run_total_wall_time_s` | -257.690465 | 3 / 0 / 0 |
| `symbolic_core_seconds` | -177.050431 | 3 / 0 / 0 |
| `symbolize_wall_time_s` | -253.655391 | 3 / 0 / 0 |
| `validation_mean_r2` | -0.004712 | 1 / 2 / 0 |

解释：

1. `final_n_edge` 差分为零，是本轮结果仍然可被解释为同复杂度 backend compare 的前提。
2. `symbolic_core_seconds` 为 `3/3` 更快，是本轮最强的 headline。
3. 精度与验证指标没有出现大幅波动，但符号侧质量改善并不显著，因此论文或答辩表述应以速度为主。

## 6. ICBR 主效应与机制拆解

### 6.1 主效应

`comparison_fastlib/baseline_icbr_primary_effect.csv` 汇总如下：

| 指标 | mean | median | std |
| --- | ---: | ---: | ---: |
| `symbolic_core_speedup_vs_baseline` | 6.092446 | 4.579196 | 2.789792 |
| `final_teacher_imitation_mse_shift` | 0.000062 | 0.000060 | 0.000006 |
| `final_target_mse_shift` | -0.000023 | -0.000015 | 0.000028 |
| `final_target_r2_shift` | 0.000258 | 0.000162 | 0.000311 |
| `baseline_formula_export_success_rate` | 1.000000 | 1.000000 | 0.000000 |
| `icbr_formula_export_success_rate` | 1.000000 | 1.000000 | 0.000000 |

解释：

1. 当前 FAST_LIB 切片已经把 `symbolic_core_speedup_vs_baseline` 推高到约 `6.09x`。
2. `final_target_mse_shift < 0`、`final_target_r2_shift > 0` 方向仍然有利，但量级很小。
3. `final_teacher_imitation_mse_shift` 略为正值，说明这轮结果不适合再写成“ICBR 在质量上明显更好”；更稳妥的说法是“速度明显更强，质量近似持平”。
4. 两侧公式导出成功率都为 `1.0`，可以支持“导出链路稳定”这一工程性结论。

### 6.2 机制拆解

`comparison_fastlib/baseline_icbr_mechanism_summary.csv` 汇总如下：

| 指标 | mean | median | std |
| --- | ---: | ---: | ---: |
| `icbr_candidate_generation_wall_time_s` | 1.192465 | 1.220830 | 0.045347 |
| `icbr_replay_rerank_wall_time_s` | 33.592179 | 33.632677 | 0.217455 |
| `icbr_candidate_share_of_core_time` | 0.034162 | 0.034719 | 0.001067 |
| `icbr_replay_share_of_core_time` | 0.962558 | 0.962263 | 0.001277 |
| `icbr_other_core_seconds` | 0.114505 | 0.106490 | 0.011592 |
| `icbr_replay_rank_inversion_rate` | 0.252852 | 0.247191 | 0.014482 |

解释：

1. 即便扩大到 `FAST_LIB`，candidate generation 占核心时间的比例仍然很低，均值约 `3.42%`。
2. replay rerank 仍是 ICBR 的主要剩余成本，占核心时间约 `96.26%`。
3. 这说明复用整轮 `teacher_output` 之后，剩余瓶颈更加集中在逐候选的 replay 回放本身，而不是 teacher 侧重复前向。

## 7. Symbolize Trace Rhythm

`comparison_fastlib/trace_summary.csv` 当前结果如下：

| variant | rounds_mean | effective_rounds_mean | total_edges_removed_mean | mean_drop_ratio_mean | max_drop_ratio_mean |
| --- | ---: | ---: | ---: | ---: | ---: |
| baseline_fastlib | 5.0000 | 3.6667 | 15.3333 | 0.033881 | 0.080582 |
| baseline_icbr_fastlib | 5.0000 | 3.6667 | 15.3333 | 0.033881 | 0.080582 |

这组结果的重要性在于：

1. 它直接证明 `Symbolize Trace Rhythm` 已经对齐。
2. 这意味着 ICBR 的速度优势不来自“少做了剪枝轮次”或“绕开了 shared symbolic-prep”。
3. 当前 compare 可以被解释为同一 shared trace 之后的后端差异。

## 8. 与 layered 库对照的关系

1. `comparison/` 仍是较保守、较小函数库下的 backend-only 对照切片。
2. `comparison/` 当前 `symbolic_core_speedup_vs_baseline` 约为 `2.377025`，机制表显示 replay rerank 占核心时间约 `97.76%`。
3. `comparison_fastlib/` 是当前更能体现 ICBR 速度潜力的主引用切片。
4. 若需要强调“语义边界修复已经完成”，可继续引用 `comparison/`。
5. 若需要强调“在更大候选库下 ICBR 的实际速度收益”，应优先引用 `comparison_fastlib/`。

## 9. 方法学限制

1. 当前统计仍只基于固定三 seed，具备工程判断意义，但不应表述为充分统计显著性结论。
2. `symbolize_wall_time_s` 仍包含导出前后的额外墙钟开销，因此 backend 比较应优先看 `symbolic_core_seconds`。
3. 当前 FAST_LIB 切片的质量差异接近于零，不应把这轮结果写成“普遍质量显著提升”。

## 10. 结论

1. 当前工程版已经同时具备了“最保守的 layered 库 backend-only 对照”和“更能体现速度潜力的 FAST_LIB backend-only 对照”。
2. `baseline_fastlib` 与 `baseline_icbr_fastlib` 在 `42/52/62` 三个 seed 上共享 numeric stage、shared symbolic-prep 与 trace rhythm，且两侧都命中了既有缓存。
3. 在当前三 seed 对照中，ICBR 没有改变最终边数，却把 `symbolic_core_seconds` 平均提升到约 `6.09x` 的速度优势。
4. 因此，本轮更适合支持这样的表述：ICBR 在更大候选函数库下仍保持 backend-only 语义干净，并显著强化了符号拟合阶段的速度优势；质量侧目前以“近似持平”表述最稳妥。
