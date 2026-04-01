# 工程版复测报告（2026-04-01 ICBR backend 对照更新）

## 1. 研究设定与引用层级

1. 本报告讨论的是当前工程版内部的 ICBR backend 对照，而不是“工程版 vs 历史版”。
2. 复测执行日期：`2026-04-01`。
3. 当前证据分为三层：
   - paired layered 库对照：
     - `outputs/rerun_v2_engine_safe_20260401/benchmark_ab/comparison/`
   - paired FAST_LIB 对照：
     - `outputs/rerun_v2_engine_safe_20260401/benchmark_ab/comparison_fastlib/`
   - full symbolic library 的补充单变体切片：
     - `outputs/rerun_v2_engine_safe_20260401/benchmark_ab/baseline_icbr_fulllib/`
4. `baseline_fulllib` 本轮未跑，原因是 full library 下 baseline 路径成本过高。
5. 前两层满足 backend-only compare 的 shared-state 约束，可直接用于 paired 结论；第三层是有意保留的 ICBR 单边补充切片，用于说明 ICBR 在 full library 下仍具备可接受速度，并观察 full library 带来的单边收益。
6. 本轮三套函数库口径分别是：layered 切片使用 `LIB_HIDDEN = ["x", "x^2", "tanh"]` 与 `LIB_OUTPUT = ["x", "x^2"]`；FAST_LIB 切片使用 `FAST_LIB = ["x", "x^2", "x^3", "tanh", "sin", "cos", "exp", "log", "sqrt", "abs"]`；full library 补充切片使用 `EXPRESSIVE_LIB = list(_SYM_LIB_REG.keys())`，`FULL_LIB = EXPRESSIVE_LIB`。

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

C:\Users\chenpeng\miniconda3\envs\kan\python.exe -m scripts.symkanbenchmark `
  --tasks full `
  --stagewise-seeds 42,52,62 `
  --config configs/benchmark_ab/baseline_icbr_fulllib.yaml `
  --output-dir outputs/rerun_v2_engine_safe_20260401/benchmark_ab/baseline_icbr_fulllib `
  --quiet
```

## 2. Shared-State 对齐核验

paired compare 能否解释为 backend-only 差异，首先取决于 shared numeric、shared symbolic-prep 与 trace rhythm 是否对齐。

### 2.1 layered 库切片

`comparison/baseline_icbr_shared_check.csv` 对 `42/52/62` 三个 seed 均报告：

| stage_seed | shared_numeric_aligned | trace_aligned | shared_symbolic_prep_aligned | baseline_numeric_cache_hit | icbr_numeric_cache_hit | baseline_symbolic_prep_cache_hit | icbr_symbolic_prep_cache_hit |
| ---: | --- | --- | --- | --- | --- | --- | --- |
| 42 | True | True | True | True | True | True | True |
| 52 | True | True | True | True | True | True | True |
| 62 | True | True | True | True | True | True | True |

### 2.2 FAST_LIB 切片

`comparison_fastlib/baseline_icbr_shared_check.csv` 对 `42/52/62` 三个 seed 也均报告：

| stage_seed | shared_numeric_aligned | trace_aligned | shared_symbolic_prep_aligned | baseline_numeric_cache_hit | icbr_numeric_cache_hit | baseline_symbolic_prep_cache_hit | icbr_symbolic_prep_cache_hit |
| ---: | --- | --- | --- | --- | --- | --- | --- |
| 42 | True | True | True | True | True | True | True |
| 52 | True | True | True | True | True | True | True |
| 62 | True | True | True | True | True | True | True |

解释：

1. 两套 paired compare 都满足 `shared_numeric_aligned=True`、`trace_aligned=True` 与 `shared_symbolic_prep_aligned=True`。
2. 两套 paired compare 的 `trace_summary.csv` 都显示相同的 `Symbolize Trace Rhythm`。
3. 因此，两套切片都可以解释为“同一 numeric stage、同一 shared symbolic-prep 之后的 backend-only compare”。

## 3. Layered 库 paired 对照

### 3.1 变体均值

`comparison/variant_summary.csv` 给出的当前均值如下：

| 变体 | final_acc | final_n_edge | macro_auc | run_total_wall_time_s | symbolic_core_seconds | symbolize_wall_time_s | validation_mean_r2 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| baseline | 0.777467 | 88.333333 | 0.951264 | 69.864499 | 33.297856 | 68.013948 | -0.486988 |
| baseline_icbr | 0.788667 | 88.333333 | 0.961440 | 62.462939 | 19.013927 | 60.000633 | -0.409281 |

### 3.2 pairwise 差分

`comparison/pairwise_delta_summary.csv` 报告：

| 指标 | mean_delta (baseline_icbr - baseline) | win / lose / tie |
| --- | ---: | ---: |
| `final_acc` | +0.011200 | 3 / 0 / 0 |
| `final_n_edge` | +0.000000 | 0 / 0 / 3 |
| `macro_auc` | +0.010176 | 3 / 0 / 0 |
| `run_total_wall_time_s` | -7.401560 | 3 / 0 / 0 |
| `symbolic_core_seconds` | -14.283929 | 3 / 0 / 0 |
| `symbolize_wall_time_s` | -8.013315 | 3 / 0 / 0 |
| `validation_mean_r2` | +0.077707 | 2 / 1 / 0 |

### 3.3 主效应与机制拆解

`comparison/baseline_icbr_primary_effect.csv` 当前应引用：

| 指标 | mean |
| --- | ---: |
| `symbolic_core_speedup_vs_baseline` | 1.751763 |
| `final_teacher_imitation_mse_shift` | -0.006330 |
| `final_target_mse_shift` | -0.008691 |
| `final_target_r2_shift` | +0.096602 |
| `baseline_formula_export_success_rate` | 1.000000 |
| `icbr_formula_export_success_rate` | 1.000000 |

`comparison/baseline_icbr_mechanism_summary.csv` 当前应引用：

| 指标 | mean |
| --- | ---: |
| `icbr_candidate_generation_wall_time_s` | 0.333292 |
| `icbr_replay_rerank_wall_time_s` | 18.566778 |
| `icbr_candidate_share_of_core_time` | 0.017539 |
| `icbr_replay_share_of_core_time` | 0.976469 |
| `icbr_other_core_seconds` | 0.113857 |
| `icbr_replay_rank_inversion_rate` | 0.113253 |

解释：

1. 这是当前最保守的 paired backend-only 切片。
2. ICBR 在保持 `final_n_edge` 完全一致的前提下，把 `symbolic_core_seconds` 提升到约 `1.75x` 的速度优势。
3. 这一切片不只是速度改善，`final_acc`、`macro_auc` 与 target-side 指标也都朝有利方向移动。
4. 这一切片的具体库设置是：`LIB_HIDDEN = ["x", "x^2", "tanh"]`，`LIB_OUTPUT = ["x", "x^2"]`。

## 4. FAST_LIB paired 对照

### 4.1 变体均值

`comparison_fastlib/variant_summary.csv` 给出的当前均值如下：

| 变体 | final_acc | final_n_edge | macro_auc | run_total_wall_time_s | symbolic_core_seconds | symbolize_wall_time_s | validation_mean_r2 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| baseline_fastlib | 0.794000 | 88.333333 | 0.962537 | 112.233492 | 75.187859 | 110.162969 | -0.451777 |
| baseline_icbr_fastlib | 0.793233 | 88.333333 | 0.962634 | 69.944645 | 31.990798 | 67.817348 | -0.456489 |

### 4.2 pairwise 差分

`comparison_fastlib/pairwise_delta_summary.csv` 报告：

| 指标 | mean_delta (baseline_icbr_fastlib - baseline_fastlib) | win / lose / tie |
| --- | ---: | ---: |
| `final_acc` | -0.000767 | 0 / 3 / 0 |
| `final_n_edge` | +0.000000 | 0 / 0 / 3 |
| `macro_auc` | +0.000097 | 3 / 0 / 0 |
| `run_total_wall_time_s` | -42.288847 | 3 / 0 / 0 |
| `symbolic_core_seconds` | -43.197061 | 3 / 0 / 0 |
| `symbolize_wall_time_s` | -42.345621 | 3 / 0 / 0 |
| `validation_mean_r2` | -0.004712 | 1 / 2 / 0 |

### 4.3 主效应与机制拆解

`comparison_fastlib/baseline_icbr_primary_effect.csv` 当前应引用：

| 指标 | mean |
| --- | ---: |
| `symbolic_core_speedup_vs_baseline` | 2.350452 |
| `final_teacher_imitation_mse_shift` | +0.000062 |
| `final_target_mse_shift` | -0.000023 |
| `final_target_r2_shift` | +0.000258 |
| `baseline_formula_export_success_rate` | 1.000000 |
| `icbr_formula_export_success_rate` | 1.000000 |

`comparison_fastlib/baseline_icbr_mechanism_summary.csv` 当前应引用：

| 指标 | mean |
| --- | ---: |
| `icbr_candidate_generation_wall_time_s` | 1.138059 |
| `icbr_replay_rerank_wall_time_s` | 30.739668 |
| `icbr_candidate_share_of_core_time` | 0.035573 |
| `icbr_replay_share_of_core_time` | 0.960892 |
| `icbr_other_core_seconds` | 0.113072 |
| `icbr_replay_rank_inversion_rate` | 0.252852 |

解释：

1. 这是当前更能体现 ICBR 在更大候选库下速度潜力的 paired 切片。
2. 与旧口径不同，当前 FAST_LIB 主效应不应再写成 `6.09x`，而应更新为约 `2.35x` 的 `symbolic_core_speedup_vs_baseline`。
3. 质量侧整体更接近“近似持平”：`final_acc` 略低，`macro_auc` 与 target-side 指标仅有极小变化。
4. 这一切片的具体库设置是：`FAST_LIB = ["x", "x^2", "x^3", "tanh", "sin", "cos", "exp", "log", "sqrt", "abs"]`。

## 5. `baseline_icbr_fulllib` 补充单变体切片

`baseline_icbr_fulllib/` 当前只有 ICBR 单边运行，没有配套 `baseline_fulllib` compare，也没有 `baseline_icbr_shared_check.csv`。这是有意为之：本轮没有再跑 `baseline_fulllib`，因为 full library 下 baseline 路径过慢。该切片的职责不是替代 paired compare，而是补充证明 ICBR 在 full library 下依然可运行，并观察 full library 对 ICBR 单边结果带来的收益。

`baseline_icbr_fulllib/symkanbenchmark_runs.csv` 的当前均值如下：

| 变体 | final_acc | final_n_edge | macro_auc | final_target_mse | final_target_r2 | symbolic_core_seconds | symbolize_wall_time_s | run_total_wall_time_s |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| baseline_icbr_fulllib | 0.795433 | 88.333333 | 0.963225 | 0.035896 | 0.601003 | 35.218785 | 39.693965 | 41.757397 |

当前可安全引用的补充事实：

1. 三个 seed 都命中了 `numeric_cache_hit=True` 与 `symbolic_prep_cache_hit=True`。
2. 三个 seed 的公式导出都成功。
3. 相对 `baseline_icbr_fastlib`，该切片的单边均值表现为：
   - `final_acc` 从 `0.793233` 提升到 `0.795433`
   - `macro_auc` 从 `0.962634` 提升到 `0.963225`
   - `final_target_r2` 从 `0.596936` 提升到 `0.601003`
   - `symbolic_core_seconds` 从 `31.990798` 上升到 `35.218785`
4. 即使切到 full symbolic library，`baseline_icbr_fulllib` 的 `symbolic_core_seconds` 均值仍比 paired `baseline_fastlib` 低 `39.969074s`，说明 ICBR 的速度优势在更大全库下依然具备工程意义。
5. 因此，该切片适合支持“ICBR 让 full library 方案仍然可跑，且能换来一定单边质量收益”的表述，但不承担 paired fairness 证明职责。
6. 这一切片的具体库设置是：`EXPRESSIVE_LIB = list(_SYM_LIB_REG.keys())`，`FULL_LIB = EXPRESSIVE_LIB`。

## 6. 报告书写建议

当前更稳妥的引用方式是按论点拆分：

1. 若要强调 backend-only 语义边界已经修干净，优先引用 `comparison/`。
2. 若要强调更大候选库下的 paired 速度收益，优先引用 `comparison_fastlib/`。
3. 若只想补充说明 ICBR 在 full library 下的单边运行画像，可附带引用 `baseline_icbr_fulllib/`，并明确说明：`baseline_fulllib` 本轮未跑是因为过慢，而该切片用于证明 ICBR 在 full library 下仍具备可接受速度并带来单边收益。
4. backend compare 的主速度指标仍应优先使用 `symbolic_core_seconds`，而不是单独使用 `symbolize_wall_time_s`。

## 7. 方法学限制

1. 当前统计仍只基于固定三 seed，具备工程判断意义，但不应表述为充分统计显著性结论。
2. `symbolize_wall_time_s` 仍包含导出前后的额外墙钟开销，因此 backend compare 应优先看 `symbolic_core_seconds`。
3. `baseline_icbr_fulllib/` 没有 paired baseline compare，不能被升格为正式 backend-only 结论。

## 8. 结论

1. 当前工程版同时具备两套 paired backend-only 对照和一套单边补充切片。
2. layered 库切片当前支持“ICBR 在相同复杂度下约 `1.75x` 提速，并伴随质量指标改善”的表述。
3. FAST_LIB 切片当前支持“ICBR 在更大候选库下约 `2.35x` 提速，质量近似持平”的表述。
4. `baseline_icbr_fulllib/` 可作为 full symbolic library 下的补充运行画像，但不应替代 paired compare 的正式证据。
