# 工程版复测报告（2026-03-27 bspline baseline vs radial_bf）

## 1. 实验目标

本报告对应 `2026-03-27` 的历史工程专题切片，关注的问题不是 ICBR backend，而是当前工程版早期对 `baseline (bspline)` 与 `radial_bf` 方案的工程化对照。

本轮结论边界如下：

1. 它是历史专题结果，不是当前 `2026-04-01` ICBR backend compare 的主引用。
2. 它也不是“只改一个 numeric basis 的纯隔离实验”，因为 `radial_bf.yaml` 同时调整了训练和符号化阶段的一组工程参数。
3. 因此，这份报告更适合支持“历史工程权衡”叙述，而不是当前正式口径。

## 2. 实验环境与数据

### 2.1 运行环境

1. 操作系统：Windows 11 专业版 `23H2`。
2. Python：`C:\Users\chenpeng\miniconda3\envs\kan\python.exe`（Python `3.9.25`）。
3. 运行时：`PyTorch 2.1.2+cpu`。

### 2.2 数据与种子

1. 数据路径：`data/X_train.npy`、`data/X_test.npy`、`data/Y_train_cat.npy`、`data/Y_test_cat.npy`。
2. 数据形状：`X_train = (60000, 784)`、`Y_train_cat = (60000, 10)`、`X_test = (10000, 784)`、`Y_test_cat = (10000, 10)`。
3. 数据集口径：固定使用仓库内预制的 MNIST `train/test` 切分，本轮历史 rerun 不重新随机划分训练集与测试集。
4. 类别集合：`[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]`。
5. stagewise seeds：`42,52,62`。
6. runtime seeds：`global_seed = 123`，`baseline_seed = 123`，`layerwise_validation_seed = 123`。
7. 实际 batch size：`64`。
8. 评估抽样：`validate_n_sample = 500`。
9. 结果归档根：`outputs/rerun_v2_engine_safe_20260327/benchmark_ab/`。

### 2.3 模型与共同设置

两侧共同设置包括：

1. 模型骨架：`inner_dim = 16`、`grid = 5`、`k = 3`、`top_k = 120`。
2. workflow：`disable_stagewise_train = false`、`e2e_steps = 0`。
3. library preset：`layered`。
4. 分层函数库：`LIB_HIDDEN = ["x", "x^2", "tanh"]`，`LIB_OUTPUT = ["x", "x^2"]`。
5. symbolize 主参数：`target_edges = 90`、`max_prune_rounds = 30`、`weight_simple = 0.1`。
6. 微调主参数：`finetune_steps = 50`、`finetune_lr = 0.0005`、`layerwise_finetune_steps = 60`。
7. stage guard：`guard_mode = light`。

两侧共同的数据切分与样本口径如下：

1. numeric stage 不额外划出验证集，因为 `stagewise.use_validation = false`；因此数值训练与 stagewise 剪枝直接使用全部 `60000` 个训练样本。
2. symbolize 的逐层微调启用 `layerwise_use_validation = true` 且 `layerwise_validation_ratio = 0.15`，因此符号阶段会在训练集内部切出 `9000` 个 layerwise validation 样本，并保留 `51000` 个 layerwise fit 样本。
3. 最终公式数值验证使用 `validate_n_sample = 500`，即在 `10000` 个测试样本中截取前 `500` 个样本生成 `formula_validation.csv` 与 `validation_mean_r2`。
4. shared symbolic-prep 的剪枝归因采用自适应样本数；本轮 `pre_symbolic_n_edge` 约为 `105`、目标边数为 `90`，因此每轮归因使用的上限样本数为 `2048`。

## 3. 变体定义与配置差异

### 3.1 `baseline`

`baseline.yaml` 对应的是 `bspline` 数值路径，关键配置为：

1. 配置文件：`configs/benchmark_ab/baseline.yaml`。
2. `numeric_basis` 沿用默认 `bspline`。
3. `baseline_lr = 0.02`，`baseline_lamb = 0.0001`，`baseline_log = 12`。
4. `stagewise.prune_start_stage = 3`。
5. `symbolize.max_prune_rounds = 30`。
6. `layerwise_finetune_lr = 0.005`，`layerwise_finetune_lamb = 0.00001`。
7. `affine_finetune_steps = 200`，`affine_finetune_lr_schedule = [0.003, 0.001, 0.0005, 0.0002]`。

### 3.2 `radial_bf`

`radial_bf.yaml` 是一条调过参的历史工程路径，关键配置为：

1. 配置文件：`configs/benchmark_ab/radial_bf.yaml`。
2. `model.numeric_basis = radial_bf`。
3. `baseline_lr = 0.005`，`baseline_lamb = 0.00004`，`baseline_log = 15`。
4. `stagewise.prune_start_stage = 1`，并使用另一套 `lamb_schedule` 与 `lr_schedule`。
5. `symbolize.max_prune_rounds = 20`。
6. `layerwise_finetune_lr = 0.003`，`layerwise_finetune_lamb = 0.00005`。
7. `affine_finetune_steps = 80`，`affine_finetune_lr_schedule = [0.0015, 0.0007]`。

因此，本轮应写成“工程版历史 `radial_bf` 专题切片”，而不是“只把 numeric basis 从 bspline 切到 radial_bf 的纯单因素实验”。

## 4. 执行命令

```powershell
# 运行目录：仓库根目录（symkan-experiments/）
C:\Users\chenpeng\miniconda3\envs\kan\python.exe -m scripts.symkanbenchmark `
  --tasks full `
  --stagewise-seeds 42,52,62 `
  --config configs/benchmark_ab/baseline.yaml `
  --output-dir outputs/rerun_v2_engine_safe_20260327/benchmark_ab/baseline `
  --quiet

C:\Users\chenpeng\miniconda3\envs\kan\python.exe -m scripts.symkanbenchmark `
  --tasks full `
  --stagewise-seeds 42,52,62 `
  --config configs/benchmark_ab/radial_bf.yaml `
  --output-dir outputs/rerun_v2_engine_safe_20260327/benchmark_ab/radial_bf `
  --quiet

C:\Users\chenpeng\miniconda3\envs\kan\python.exe -m scripts.benchmark_ab_compare `
  --root outputs/rerun_v2_engine_safe_20260327/benchmark_ab `
  --baseline baseline `
  --variants radial_bf `
  --output outputs/rerun_v2_engine_safe_20260327/benchmark_ab/comparison
```

## 5. 主要结果

### 5.1 变体均值

`outputs/rerun_v2_engine_safe_20260327/benchmark_ab/comparison/variant_summary.csv` 给出的均值如下：

| 变体 | final_acc | final_n_edge | macro_auc | run_total_wall_time_s | symbolic_core_seconds | symbolize_wall_time_s | validation_mean_r2 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| baseline | 0.777433 | 88.666667 | 0.956107 | 201.644621 | 44.329937 | 118.647711 | -0.549509 |
| radial_bf | 0.765400 | 89.000000 | 0.953788 | 136.664280 | 40.865443 | 76.367098 | -0.746382 |

### 5.2 pairwise 差分

`pairwise_delta_summary.csv` 报告：

| 指标 | mean_delta (radial_bf - baseline) | win / lose / tie |
| --- | ---: | ---: |
| `final_acc` | -0.012033 | 0 / 3 / 0 |
| `final_n_edge` | +0.333333 | 1 / 2 / 0 |
| `macro_auc` | -0.002319 | 1 / 2 / 0 |
| `run_total_wall_time_s` | -64.980341 | 3 / 0 / 0 |
| `symbolic_core_seconds` | -3.464494 | 3 / 0 / 0 |
| `symbolize_wall_time_s` | -42.280613 | 3 / 0 / 0 |
| `validation_mean_r2` | -0.196873 | 1 / 2 / 0 |

解释：

1. `radial_bf` 在三 seed 上都更快，端到端时间和符号化时间都有明显下降。
2. 但 `final_acc` 和 `macro_auc` 整体弱于 baseline。
3. `validation_mean_r2` 波动更大，说明这条历史路径在公式侧稳定性上并不占优。

## 6. Symbolize Trace 与复杂度

`trace_summary.csv` 当前结果如下：

| variant | rounds_mean | effective_rounds_mean | total_edges_removed_mean | mean_drop_ratio_mean | max_drop_ratio_mean |
| --- | ---: | ---: | ---: | ---: | ---: |
| baseline | 10.666667 | 6.666667 | 23.333333 | 0.027671 | 0.088960 |
| radial_bf | 3.000000 | 2.666667 | 15.000000 | 0.044928 | 0.108470 |

这说明：

1. `radial_bf` 路径的 symbolize trace 更短、更激进。
2. baseline 路径删边更多、轮次更长。
3. 因为两侧不共享完全一致的训练与 symbolize 参数，所以这份对照不能被解释成当前 ICBR 那种 backend-only compare。

## 7. 论文式写法建议

若在论文或附录中引用这一轮结果，更稳妥的表述是：

1. “在 `2026-03-27` 的历史工程专题中，调参后的 `radial_bf` 方案显著降低了运行时间，但在 `final_acc`、`macro_auc` 与公式验证指标上整体弱于 `bspline baseline`。”
2. “由于 `radial_bf` 变体同时调整了数值训练和 symbolize 阶段的多项参数，该专题更适合作为工程权衡参考，而非纯 numeric basis 单因素结论。”
3. “当前正式结论仍以 `2026-04-01` 的 ICBR 带日期正式报告为准。”

## 8. 结论

1. `2026-03-27` 结果保留了一个清晰的历史工程权衡：`radial_bf` 更快，但整体质量不如 `baseline`。
2. 这轮实验共享 layered 函数库，但并不满足当前 backend-only compare 的 fairness 口径。
3. 因此，它应该作为带日期历史报告保留，而不是被当前 `20260401` 报告覆盖。
