# 工程版复测报告（2026-04-01 ICBR 集成对照）

## 1. 研究设定与口径

1. 本报告对应的比较问题不是“工程版 vs 历史版”，而是“在当前工程版中，baseline symbolic backend 与 ICBR symbolic backend 的对照”。
2. 复测执行日期：`2026-04-01`。
3. 主引用输出目录：`outputs/rerun_v2_engine_safe_20260401/benchmark_ab/`。
4. 对照目录包括：
   - `outputs/rerun_v2_engine_safe_20260401/benchmark_ab/baseline/`
   - `outputs/rerun_v2_engine_safe_20260401/benchmark_ab/baseline_icbr/`
   - `outputs/rerun_v2_engine_safe_20260401/benchmark_ab/comparison/`
5. 本报告的结论边界是：只讨论符号拟合后端差异，不把结果解释成训练策略差异。
6. 入口口径：常规 CLI 使用 `python -m scripts.*`；本轮对照通过 `scripts.symkanbenchmark.py` 与 `scripts.benchmark_ab_compare.py` 直接完成。
7. 命令默认执行环境：`PowerShell`（Windows）。
8. 测试设备与运行时环境：
   - 操作系统：Windows 11 专业版 `23H2`（OS Build `22631.5472`）
   - Python：`Miniconda` 的 `kan` 环境，解释器路径 `C:\Users\chenpeng\miniconda3\envs\kan\python.exe`（`3.9.25`）
   - CPU：`12th Gen Intel(R) Core(TM) i5-12500H`
   - 内存：`16 GB`
   - 深度学习运行时：`PyTorch 2.1.2+cpu`

执行命令（PowerShell）：

```powershell
# 运行目录：仓库根目录（symkan-experiments/）
C:\Users\chenpeng\miniconda3\envs\kan\python.exe -m scripts.symkanbenchmark `
  --tasks full `
  --stagewise-seeds 42,52,62 `
  --config configs/benchmark_ab/baseline.yaml `
  --output-dir outputs/rerun_v2_engine_safe_20260401/benchmark_ab/baseline `
  --quiet

C:\Users\chenpeng\miniconda3\envs\kan\python.exe -m scripts.symkanbenchmark `
  --tasks full `
  --stagewise-seeds 42,52,62 `
  --config configs/benchmark_ab/baseline_icbr.yaml `
  --output-dir outputs/rerun_v2_engine_safe_20260401/benchmark_ab/baseline_icbr `
  --quiet

C:\Users\chenpeng\miniconda3\envs\kan\python.exe -m scripts.benchmark_ab_compare `
  --root outputs/rerun_v2_engine_safe_20260401/benchmark_ab `
  --baseline baseline `
  --variants baseline_icbr `
  --output outputs/rerun_v2_engine_safe_20260401/benchmark_ab/comparison
```

## 2. 实现边界

本轮对照建立在两个明确的工程边界上：

1. ICBR 只改变符号拟合后端，不改变数值训练。
2. `baseline` 与 `baseline_icbr` 共享 numeric cache 与 shared symbolic-prep 边界。

当前 `symkan.symbolic.pipeline` 的内部结构是：

1. `prepare_symbolic_bundle(...)`
   负责共享 symbolic-prep：渐进剪枝、输入压缩、pre-symbolic fit 和 trace 生成。
2. `symbolize_pipeline_from_prepared(...)`
   负责 backend-specific symbolic completion：
   - `baseline` 走原有 layered symbolic search。
   - `icbr` 调用 `kan.icbr` 中的 ICBR 后端。

因此，本报告中的任何性能或质量差异，都只能解释为“同一数值 KAN、同一 shared symbolic-prep 之后的后端差异”。

## 3. 产物完整性核验

核验结论：本轮产物完整，具备对 `baseline` 与 `baseline_icbr` 做 backend-only 对照的条件。

1. `baseline/` 与 `baseline_icbr/` 各包含 `3` 个 run 目录，且各自 `symkanbenchmark_runs.csv` 完整。
2. 通用 compare 产物齐全：
   - `variant_summary.csv`
   - `pairwise_delta_summary.csv`
   - `seedwise_delta.csv`
   - `trace_seedwise.csv`
   - `trace_summary.csv`
   - `comparison_summary.md`
3. baseline/icbr 专用 compare 产物齐全：
   - `baseline_icbr_shared_check.csv`
   - `baseline_icbr_primary_effect.csv`
   - `baseline_icbr_mechanism_summary.csv`

## 4. Shared-State 对齐核验

`baseline_icbr_shared_check.csv` 的核心作用是验证当前 compare 是否真的只反映后端差异。

| stage_seed | shared_numeric_aligned | trace_aligned | shared_symbolic_prep_aligned | baseline_numeric_cache_hit | icbr_numeric_cache_hit | baseline_symbolic_prep_cache_hit | icbr_symbolic_prep_cache_hit |
| ---: | --- | --- | --- | --- | --- | --- | --- |
| 42 | True | True | True | True | True | False | True |
| 52 | True | True | True | True | True | False | True |
| 62 | True | True | True | True | True | False | True |

解释：

1. 三个 seed 的 `shared_numeric_aligned=True`，说明数值训练结果一致。
2. 三个 seed 的 `trace_aligned=True`，说明 `symbolize_trace.csv` 记录的节奏来自相同的 shared symbolic-prep。
3. 三个 seed 的 `shared_symbolic_prep_aligned=True`，说明 ICBR 并未重新执行一套不同的剪枝或输入压缩流程。
4. baseline 侧的 `baseline_symbolic_prep_cache_hit=False`、ICBR 侧的 `icbr_symbolic_prep_cache_hit=True` 是当前实现预期：baseline 首次生成 prepared bundle，ICBR 复用同一 prepared bundle。

## 5. 主结果

### 5.1 变体均值

`comparison_summary.md` 给出的核心均值如下：

| 变体 | final_acc | final_n_edge | macro_auc | run_total_wall_time_s | symbolic_core_seconds | symbolize_wall_time_s | validation_mean_r2 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| baseline | 0.777767 | 88.333333 | 0.951587 | 149.814120 | 56.559906 | 128.000426 | -0.482755 |
| baseline_icbr | 0.788667 | 88.333333 | 0.961440 | 71.447204 | 26.114427 | 68.817573 | -0.409281 |

直接观察有三点：

1. `final_n_edge` 均值完全一致，说明 ICBR 不再恢复被剪掉的边，也不会把零占位边重新计入最终复杂度。
2. `symbolic_core_seconds` 和 `symbolize_wall_time_s` 都明显下降，说明 ICBR 的速度优势已经在当前工程版中稳定落地。
3. `final_acc`、`macro_auc` 与 `validation_mean_r2` 没有表现出退化，当前样本下甚至略优于 baseline。

### 5.2 pairwise 差分

| 指标 | mean_delta (baseline_icbr - baseline) | win / lose / tie |
| --- | ---: | ---: |
| `final_acc` | +0.010900 | 3 / 0 / 0 |
| `final_n_edge` | +0.000000 | 0 / 0 / 3 |
| `macro_auc` | +0.009853 | 3 / 0 / 0 |
| `run_total_wall_time_s` | -78.366916 | 3 / 0 / 0 |
| `symbolic_core_seconds` | -30.445479 | 3 / 0 / 0 |
| `symbolize_wall_time_s` | -59.182853 | 3 / 0 / 0 |
| `validation_mean_r2` | +0.073474 | 2 / 1 / 0 |

解释：

1. `final_n_edge` 差分为零，是这轮 repair 最关键的正确性信号之一。
2. `symbolic_core_seconds` 与 `symbolize_wall_time_s` 均为 `3/3` 更快，说明 ICBR 的速度优势不是单个 seed 偶然造成。
3. 由于当前样本量只有 3 个 seed，精度相关提升应表述为“未观察到退化，且当前样本下方向有利”，而不是直接写成充分统计显著性结论。

## 6. ICBR 主效应与机制拆解

### 6.1 主效应

`baseline_icbr_primary_effect.csv` 汇总如下：

| 指标 | mean | median | std |
| --- | ---: | ---: | ---: |
| `symbolic_core_speedup_vs_baseline` | 2.174967 | 1.411476 | 1.086859 |
| `final_teacher_imitation_mse_shift` | -0.006009 | -0.006910 | 0.001299 |
| `final_target_mse_shift` | -0.008364 | -0.008328 | 0.000504 |
| `final_target_r2_shift` | 0.092972 | 0.092567 | 0.005597 |
| `baseline_formula_export_success_rate` | 1.000000 | 1.000000 | 0.000000 |
| `icbr_formula_export_success_rate` | 1.000000 | 1.000000 | 0.000000 |

解释：

1. 当前工程版已经满足 ICBR 设计文档中的核心边界：比较只发生在符号拟合后端。
2. `final_teacher_imitation_mse_shift < 0` 与 `final_target_mse_shift < 0` 说明 ICBR 并未为了加速而牺牲当前样本下的后端拟合质量。
3. 两侧公式导出成功率都为 `1.0`，可以支持“导出链路稳定”这一工程性结论，但不应外推为真实公式恢复正确率。

### 6.2 机制拆解

`baseline_icbr_mechanism_summary.csv` 汇总如下：

| 指标 | mean | median | std |
| --- | ---: | ---: | ---: |
| `icbr_candidate_generation_wall_time_s` | 0.349936 | 0.338095 | 0.016835 |
| `icbr_replay_rerank_wall_time_s` | 19.251307 | 19.356854 | 0.189021 |
| `icbr_candidate_share_of_core_time` | 0.013407 | 0.012895 | 0.000762 |
| `icbr_replay_share_of_core_time` | 0.737183 | 0.737223 | 0.001157 |
| `icbr_other_core_seconds` | 6.513185 | 6.513407 | 0.055354 |
| `icbr_replay_rank_inversion_rate` | 0.113253 | 0.101124 | 0.051747 |

解释：

1. 当前 ICBR 的核心时间主要仍落在 replay rerank，而不是 candidate generation。
2. candidate generation 占比约 `1.34%`，说明“shared-tensor candidate evaluation” 已把候选生成本身压到了很低的常数开销。
3. replay rank inversion rate 当前均值约 `0.113`，说明 replay 仍然在实际改写部分候选排序，而不是一个空转模块。

## 7. Symbolize Trace Rhythm

`trace_summary.csv` 当前结果如下：

| variant | rounds_mean | effective_rounds_mean | total_edges_removed_mean | mean_drop_ratio_mean | max_drop_ratio_mean |
| --- | ---: | ---: | ---: | ---: | ---: |
| baseline | 5.0000 | 3.6667 | 15.3333 | 0.033881 | 0.080582 |
| baseline_icbr | 5.0000 | 3.6667 | 15.3333 | 0.033881 | 0.080582 |

这组结果的重要性在于：

1. 它直接证明 `Symbolize Trace Rhythm` 已经对齐。
2. 这意味着 ICBR 的速度优势不来自“少做了剪枝轮次”或“绕开了 shared symbolic-prep”。
3. 当前 compare 可以被解释为同一 shared trace 之后的后端差异，而不是阶段语义污染。

## 8. 与历史文档的关系

1. `2026-03-18` 和 `2026-03-27` 的 rerun 结果仍是历史参考，尤其用于说明工程版相对历史版、`adaptive` 系列以及 `radial_bf` 专题的口径。
2. 本报告是当前关于 ICBR 接入结果的主引用文档。
3. 若论文或答辩需要说明“工程版总体口径”，可继续引用 `engineering_version_rerun_note.md`；若需要说明“ICBR 在当前工程版中的实际表现”，应优先引用本报告与 `outputs/rerun_v2_engine_safe_20260401/benchmark_ab/comparison/`。

## 9. 方法学限制

1. 当前统计仅基于固定三 seed，具备工程判断意义，但不应表述为充分统计显著性结论。
2. `symbolize_wall_time_s` 仍包含导出前后的额外墙钟开销，因此 backend 比较应优先看 `symbolic_core_seconds`。
3. 当前报告只覆盖 `baseline` vs `baseline_icbr`，不替代已有 adaptive、ablation、LayerwiseFT 专题文档。

## 10. 结论

1. 当前工程版已经实现了“baseline 默认、ICBR 可显式选择”的后端接入目标。
2. `baseline` 与 `baseline_icbr` 现已共享 numeric stage 与 shared symbolic-prep 边界，`trace` 完全对齐。
3. 在当前三 seed 对照中，ICBR 没有改变最终边数，却把 `symbolic_core_seconds` 平均提升到约 `2.17x` 的速度优势。
4. 这使得当前 ICBR 结果与 `ICBR-KAN_design.md` 的核心设计预期保持一致：改动集中在符号拟合后端，而不是训练本身。
