# 工程版复测报告（2026-04-01 ICBR backend 对照）

## 1. 实验目标

本报告对应 `2026-04-01` 的当前工程版 ICBR backend 对照，目标是回答三个问题：

1. 在 shared numeric 与 shared symbolic-prep 边界成立的前提下，`baseline` 与 `baseline_icbr` 的差异能否被解释为 backend-only compare。
2. 当函数库从 layered 扩展到 `FAST_LIB` 后，ICBR 的速度收益和质量变化如何。
3. 当 `baseline_fulllib` 过慢而不继续跑时，`baseline_icbr_fulllib` 能否作为补充单边切片证明 ICBR 让 full library 路径仍然可运行并带来收益。

## 2. 实验环境与共同条件

### 2.1 运行环境

1. 操作系统：Windows 11 专业版 `23H2`。
2. Python：`C:\Users\chenpeng\miniconda3\envs\kan\python.exe`（Python `3.9.25`）。
3. 运行时：`PyTorch 2.1.2+cpu`。

### 2.2 数据、种子与模型骨架

1. 数据路径：`data/X_train.npy`、`data/X_test.npy`、`data/Y_train_cat.npy`、`data/Y_test_cat.npy`。
2. 数据形状：`X_train = (60000, 784)`、`Y_train_cat = (60000, 10)`、`X_test = (10000, 784)`、`Y_test_cat = (10000, 10)`。
3. 数据集口径：固定使用仓库内预制的 MNIST `train/test` 切分，本轮 rerun 不重新随机划分训练集与测试集。
4. 类别集合：`[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]`。
5. stagewise seeds：`42,52,62`。
6. runtime seeds：`global_seed = 123`，`baseline_seed = 123`，`layerwise_validation_seed = 123`。
7. 实际 batch size：`64`。
8. 模型骨架：`inner_dim = 16`、`grid = 5`、`k = 3`、`top_k = 120`。
9. 评估抽样：`validate_n_sample = 500`。
10. 共同 workflow：`disable_stagewise_train = false`、`e2e_steps = 0`、`guard_mode = light`。
11. 结果归档根：`outputs/rerun_v2_engine_safe_20260401/benchmark_ab/`。

### 2.3 三套函数库口径

1. layered 切片：`LIB_HIDDEN = ["x", "x^2", "tanh"]`，`LIB_OUTPUT = ["x", "x^2"]`。
2. FAST_LIB 切片：`FAST_LIB = ["x", "x^2", "x^3", "tanh", "sin", "cos", "exp", "log", "sqrt", "abs"]`。
3. full library 补充切片：`FULL_LIB = ["x", "x^2", "x^3", "x^4", "x^5", "1/x", "1/x^2", "1/x^3", "1/x^4", "1/x^5", "sqrt", "x^0.5", "x^1.5", "1/sqrt(x)", "1/x^0.5", "exp", "log", "abs", "sin", "cos", "tan", "tanh", "sgn", "arcsin", "arccos", "arctan", "arctanh", "0", "gaussian"]`。
4. shared symbolize 主参数：`target_edges = 90`、`max_prune_rounds = 30`、`weight_simple = 0.1`。
5. shared 微调参数：`finetune_steps = 50`、`finetune_lr = 0.0005`、`layerwise_finetune_steps = 60`、`layerwise_finetune_lr = 0.005`、`layerwise_finetune_lamb = 0.00001`、`affine_finetune_steps = 200`。

### 2.4 数据切分与符号阶段样本口径

1. numeric stage 本轮不额外划出验证集，因为 `stagewise.use_validation = false`；因此数值训练与剪枝阶段直接使用全部 `60000` 个训练样本。
2. symbolize 的逐层微调启用 `layerwise_use_validation = true` 且 `layerwise_validation_ratio = 0.15`，因此在符号阶段会从 `60000` 个训练样本中固定划出 `9000` 个样本作为 layerwise validation，剩余 `51000` 个样本作为 layerwise fit 数据。
3. 上述 `9000 / 51000` 划分只发生在训练集内部，不会动到 `10000` 个测试样本。
4. layerwise early stop 的公式验证抽样上限为 `layerwise_validation_n_sample = 300`，因此逐层微调中的公式 R² 选择最多只看验证子集中的前 `300` 个样本。
5. 最终 `formula_validation.csv` 与文中 `validation_mean_r2` 对应的是 `validate_formula_numerically(..., n_sample=500)`，即在 `10000` 个测试样本上截取前 `500` 个样本做最终公式数值验证。
6. shared symbolic-prep 的剪枝归因采用自适应样本数；当前这组实验的 `pre_symbolic_n_edge` 约为 `105`、目标边数为 `90`，因此会命中 `attr_n_sample = 2048`，也就是每轮剪枝归因最多使用 `2048` 个训练样本。
7. input compaction 只压缩输入维度，不压缩样本数；例如 `run_01_seed42` 中 `selected_input_dim = 120`，最终 `effective_input_dim = 58`，但符号拟合阶段可用的训练样本数仍按前述 `51000 / 9000` 切分执行。
8. ICBR backend 额外引入 `icbr_calibration_n_sample = 512`，实际实现会从符号阶段训练输入中截取前 `512` 个样本作为 backend calibration / replay rerank 输入；baseline backend 没有这一步。

## 3. 变体定义与配置边界

### 3.1 paired layered 切片

1. `configs/benchmark_ab/baseline.yaml`：默认工程口径，`lib_preset = layered`，symbolic backend 保持 `baseline`。
2. `configs/benchmark_ab/baseline_icbr.yaml`：保持 numeric stage 与 shared symbolic-prep 语义不变，只把 `symbolize.symbolic_backend` 切到 `icbr`。

### 3.2 paired FAST_LIB 切片

1. `configs/benchmark_ab/baseline_fastlib.yaml`：保持非 `symbolize` 配置与 `baseline.yaml` 一致，只把 `symbolize.lib` 写成 `FAST_LIB`。
2. `configs/benchmark_ab/baseline_icbr_fastlib.yaml`：在 `baseline_fastlib.yaml` 基础上仅把 `symbolize.symbolic_backend` 切到 `icbr`。
3. 两个 FAST_LIB 变体都保持 `library.lib_preset = layered`，因此 numeric/shared-prep cache key 不会因为扩库而漂移。

### 3.3 full library 单边补充切片

1. `configs/benchmark_ab/baseline_icbr_fulllib.yaml`：在 ICBR backend 下把 `symbolize.lib` 写成全量函数库。
2. `baseline_fulllib` 本轮没有继续跑，原因是 full library 下 baseline 路径成本过高。
3. 因此 `baseline_icbr_fulllib` 只作为 supplementary single-arm slice，不承担 paired fairness 证明职责。

## 4. 执行命令

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

## 5. Shared-State 对齐核验

### 5.1 layered 切片

`comparison/baseline_icbr_shared_check.csv` 对 `42/52/62` 三个 seed 均报告：

| stage_seed | shared_numeric_aligned | trace_aligned | shared_symbolic_prep_aligned | baseline_numeric_cache_hit | icbr_numeric_cache_hit | baseline_symbolic_prep_cache_hit | icbr_symbolic_prep_cache_hit |
| ---: | --- | --- | --- | --- | --- | --- | --- |
| 42 | True | True | True | True | True | True | True |
| 52 | True | True | True | True | True | True | True |
| 62 | True | True | True | True | True | True | True |

### 5.2 FAST_LIB 切片

`comparison_fastlib/baseline_icbr_shared_check.csv` 对 `42/52/62` 三个 seed 也均报告：

| stage_seed | shared_numeric_aligned | trace_aligned | shared_symbolic_prep_aligned | baseline_numeric_cache_hit | icbr_numeric_cache_hit | baseline_symbolic_prep_cache_hit | icbr_symbolic_prep_cache_hit |
| ---: | --- | --- | --- | --- | --- | --- | --- |
| 42 | True | True | True | True | True | True | True |
| 52 | True | True | True | True | True | True | True |
| 62 | True | True | True | True | True | True | True |

解释：

1. 两套 paired compare 都满足 shared numeric、shared symbolic-prep 与 trace rhythm 对齐。
2. 因此这两套结果都可以被解释为 backend-only compare。
3. 两套 paired compare 的共同公平性前提是：比较只发生在 backend-specific symbolic completion，训练、剪枝、输入压缩和 pre-symbolic fit 已经共享。
4. `baseline_icbr_fulllib` 没有 paired baseline compare，不在本节 fairness 结论范围内。

## 6. Layered 库 paired 对照

### 6.1 变体均值

| 变体 | final_acc | final_n_edge | macro_auc | run_total_wall_time_s | symbolic_core_seconds | symbolize_wall_time_s | validation_mean_r2 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| baseline | 0.777467 | 88.333333 | 0.951264 | 69.864499 | 33.297856 | 68.013948 | -0.486988 |
| baseline_icbr | 0.788667 | 88.333333 | 0.961440 | 62.462939 | 19.013927 | 60.000633 | -0.409281 |

### 6.2 pairwise 差分

| 指标 | mean_delta (baseline_icbr - baseline) | win / lose / tie |
| --- | ---: | ---: |
| `final_acc` | +0.011200 | 3 / 0 / 0 |
| `final_n_edge` | +0.000000 | 0 / 0 / 3 |
| `macro_auc` | +0.010176 | 3 / 0 / 0 |
| `run_total_wall_time_s` | -7.401560 | 3 / 0 / 0 |
| `symbolic_core_seconds` | -14.283929 | 3 / 0 / 0 |
| `symbolize_wall_time_s` | -8.013315 | 3 / 0 / 0 |
| `validation_mean_r2` | +0.077707 | 2 / 1 / 0 |

### 6.3 主效应与机制拆解

| 指标 | mean |
| --- | ---: |
| `symbolic_core_speedup_vs_baseline` | 1.751763 |
| `final_teacher_imitation_mse_shift` | -0.006330 |
| `final_target_mse_shift` | -0.008691 |
| `final_target_r2_shift` | +0.096602 |
| `baseline_formula_export_success_rate` | 1.000000 |
| `icbr_formula_export_success_rate` | 1.000000 |

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
2. ICBR 在保持 `final_n_edge` 完全一致的前提下，实现了约 `1.75x` 的 core speedup。
3. 这一切片不只是速度改善，`final_acc`、`macro_auc` 与 target-side 指标也同步改善。

## 7. FAST_LIB paired 对照

### 7.1 变体均值

| 变体 | final_acc | final_n_edge | macro_auc | run_total_wall_time_s | symbolic_core_seconds | symbolize_wall_time_s | validation_mean_r2 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| baseline_fastlib | 0.794000 | 88.333333 | 0.962537 | 112.233492 | 75.187859 | 110.162969 | -0.451777 |
| baseline_icbr_fastlib | 0.793233 | 88.333333 | 0.962634 | 69.944645 | 31.990798 | 67.817348 | -0.456489 |

### 7.2 pairwise 差分

| 指标 | mean_delta (baseline_icbr_fastlib - baseline_fastlib) | win / lose / tie |
| --- | ---: | ---: |
| `final_acc` | -0.000767 | 0 / 3 / 0 |
| `final_n_edge` | +0.000000 | 0 / 0 / 3 |
| `macro_auc` | +0.000097 | 3 / 0 / 0 |
| `run_total_wall_time_s` | -42.288847 | 3 / 0 / 0 |
| `symbolic_core_seconds` | -43.197061 | 3 / 0 / 0 |
| `symbolize_wall_time_s` | -42.345621 | 3 / 0 / 0 |
| `validation_mean_r2` | -0.004712 | 1 / 2 / 0 |

### 7.3 主效应与机制拆解

| 指标 | mean |
| --- | ---: |
| `symbolic_core_speedup_vs_baseline` | 2.350452 |
| `final_teacher_imitation_mse_shift` | +0.000062 |
| `final_target_mse_shift` | -0.000023 |
| `final_target_r2_shift` | +0.000258 |
| `baseline_formula_export_success_rate` | 1.000000 |
| `icbr_formula_export_success_rate` | 1.000000 |

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
2. 当前 FAST_LIB 主效应应写成约 `2.35x` 的 `symbolic_core_speedup_vs_baseline`，而不是旧口径里的 `6.09x`。
3. 质量侧更适合写成“近似持平”：`final_acc` 略低，`macro_auc` 与 target-side 指标只有极小变化。

## 8. `baseline_icbr_fulllib` 补充单边切片

`baseline_fulllib` 本轮没有继续跑，原因是 full library 下 baseline 路径过慢。因此这里只保留 ICBR 单边切片，目的不是 paired fairness，而是证明 ICBR 让 full library 路径仍然可跑。

### 8.1 单边均值

| 变体 | final_acc | final_n_edge | macro_auc | final_target_mse | final_target_r2 | symbolic_core_seconds | symbolize_wall_time_s | run_total_wall_time_s |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| baseline_icbr_fulllib | 0.795433 | 88.333333 | 0.963225 | 0.035896 | 0.601003 | 35.218785 | 39.693965 | 41.757397 |

### 8.2 相对 `baseline_icbr_fastlib` 的单边收益

1. `final_acc +0.002200`
2. `macro_auc +0.000592`
3. `final_target_r2 +0.004067`
4. `symbolic_core_seconds +3.227987`

解释：

1. full library 给 ICBR 带来了一定单边质量收益。
2. 代价是 core symbolization 时间略有增加。
3. 但即使切到 full library，`baseline_icbr_fulllib` 的 `symbolic_core_seconds` 均值仍比 paired `baseline_fastlib` 低 `39.969074s`，说明 ICBR 让 full library 方案保持了工程上可接受的速度。

## 9. 论文式写法建议

1. 若要强调 backend-only 语义边界已经修干净，优先引用第 6 节 layered paired report。
2. 若要强调更大候选库下的 paired 速度收益，优先引用第 7 节 FAST_LIB paired report。
3. 若要补充 full library 的单边收益，引用第 8 节，并明确写出：`baseline_fulllib` 未跑是因为过慢，所以这里只是 supplementary single-arm slice。
4. backend compare 的主速度指标优先使用 `symbolic_core_seconds`，不要只看 `symbolize_wall_time_s`。

## 10. 结论

1. `2026-04-01` 当前正式报告同时保留了两套 paired backend-only compare 和一套单边补充切片。
2. layered 切片支持“ICBR 在同复杂度下约 `1.75x` 提速，并伴随质量改善”的表述。
3. FAST_LIB 切片支持“ICBR 在更大候选库下约 `2.35x` 提速，质量近似持平”的表述。
4. `baseline_icbr_fulllib` 支持“ICBR 让 full library 路径仍然可跑，并带来单边收益”的补充结论，但不替代 paired compare。
