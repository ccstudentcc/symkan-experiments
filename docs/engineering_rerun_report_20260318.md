# 工程版复测报告（2026-03-18 current engineering rerun）

## 1. 实验目标与引用边界

本报告对应 `outputs/rerun_v2_engine_safe_20260318_rerun/`，用于把 `2026-03-18` 当前工程版总体复测结果整理为可引用的带日期正式正文。

本报告回答三个问题：

1. 当前工程版在主流程复测下给出的总体基线结果是什么。
2. `baseline`、`adaptive` 与 `adaptive_auto` 三条工程策略在 `benchmark_ab` 切片上的速度与质量权衡是什么。
3. `benchmark_ablation` 的单因素消融结果是否支持当前 Full Pipeline 默认设定。

本报告的边界如下：

1. 它是“当前工程版总体 rerun 报告”，不是后续 `2026-04-01` ICBR backend compare 的正式正文。
2. 主引用归档根为 `outputs/rerun_v2_engine_safe_20260318_rerun/`；同日较早的 `outputs/rerun_v2_engine_safe_20260318/` 仅保留为前序归档，不作为本报告主引用结果。
3. `benchmark_runs/`、`benchmark_ab/` 与 `benchmark_ablation/` 的任务口径不同，文中分别引用，不交叉混写：
   - `benchmark_runs/`：`scripts.symkanbenchmark --tasks all`
   - `benchmark_ab/`：`scripts.symkanbenchmark --tasks full`
   - `benchmark_ablation/`：`scripts.ablation_runner` 驱动的 `full` 与单因素变体矩阵

## 2. 运行环境与共同条件

### 2.1 运行环境

1. 操作系统：Windows 11 专业版 `23H2`。
2. Python：`C:\Users\chenpeng\miniconda3\envs\kan\python.exe`（Python `3.9.25`）。
3. 运行时：`PyTorch 2.1.2+cpu`。
4. 主引用输出根：`outputs/rerun_v2_engine_safe_20260318_rerun/`。

### 2.2 数据、种子与模型骨架

1. 数据路径：`data/X_train.npy`、`data/X_test.npy`、`data/Y_train_cat.npy`、`data/Y_test_cat.npy`。
2. 数据形状：`X_train = (60000, 784)`、`Y_train_cat = (60000, 10)`、`X_test = (10000, 784)`、`Y_test_cat = (10000, 10)`。
3. 数据集口径：固定使用仓库内预制的 MNIST `train/test` 切分，本轮 rerun 不重新随机划分训练集与测试集。
4. 类别集合：`[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]`。
5. stagewise seeds：`42,52,62`。
6. runtime seeds：`global_seed = 123`，`baseline_seed = 123`，`layerwise_validation_seed = 123`。
7. 实际 batch size：`64`。
8. 模型骨架：`inner_dim = 16`、`grid = 5`、`k = 3`、`top_k = 120`。
9. 函数库口径：`layered`。
10. 工程守护口径：`stagewise.guard_mode = light`，`stagewise.prune_acc_drop_tol = 0.08`。
11. 公式验证抽样：`validate_n_sample = 500`。

## 3. 执行入口

当前工程版的编排封装入口是 `scripts/run_engineering_rerun.ps1`。对本轮主引用归档，等价执行步骤如下：

```powershell
# 运行目录：仓库根目录（symkan-experiments/）
.\scripts\run_engineering_rerun.ps1 `
  -PythonExe C:\Users\chenpeng\miniconda3\envs\kan\python.exe `
  -OutRoot outputs/rerun_v2_engine_safe_20260318_rerun
```

该脚本内部固定执行六步：

1. `scripts.symkanbenchmark --tasks all` 生成 `benchmark_runs/`。
2. `scripts.symkanbenchmark --tasks full --config configs/benchmark_ab/baseline.yaml`。
3. `scripts.symkanbenchmark --tasks full --config configs/benchmark_ab/adaptive.yaml`。
4. `scripts.symkanbenchmark --tasks full --config configs/benchmark_ab/adaptive_auto.yaml`。
5. `scripts.benchmark_ab_compare` 聚合 `benchmark_ab/comparison/`。
6. `scripts.ablation_runner --config configs/ablation_runner.default.yaml` 生成 `benchmark_ablation/`。

## 4. 变体定义

### 4.1 `benchmark_ab` 三个工程策略

1. `baseline`
   - 配置文件：`configs/benchmark_ab/baseline.yaml`
   - 含义：关闭 stagewise 自适应控制，保留当前工程版的保守默认路径。
2. `adaptive`
   - 配置文件：`configs/benchmark_ab/adaptive.yaml`
   - 含义：在 `baseline` 基础上启用 validation-driven stagewise 控制，以及 adaptive threshold / lamb / ft。
3. `adaptive_auto`
   - 配置文件：`configs/benchmark_ab/adaptive_auto.yaml`
   - 含义：在 `adaptive` 基础上进一步启用 stage early stop，并把 symbolize 自适应剪枝的起始阈值调得更保守。

### 4.2 `benchmark_ablation` 五个单因素切片

1. `full`：Full Pipeline 基线。
2. `wostagewise`：关闭 Stagewise Train。
3. `wopruning`：关闭 Progressive Pruning。
4. `wocompact`：关闭 Input Compaction。
5. `wolayerwiseft`：关闭 Layerwise Finetune。

## 5. 主流程复测结果（`benchmark_runs/`）

`benchmark_runs/symkanbenchmark_runs.csv` 对应的是 `--tasks all` 的总体主流程复测，其三 seed 均值如下：

| 指标 | 均值 |
| --- | ---: |
| `final_acc` | 0.769167 |
| `final_n_edge` | 87.666667 |
| `macro_auc` | 0.956765 |
| `stage_total_seconds` | 45.172832 |
| `symbolic_core_seconds` | 35.651883 |
| `symbolize_wall_time_s` | 75.699789 |
| `run_total_wall_time_s` | 140.332975 |
| `validation_mean_r2` | -0.630428 |

解释：

1. 这组数值是“当前工程版总体复测基线”，用于描述当前工程版默认主流程的整体表现。
2. 它不应与后文 `benchmark_ab` 里的 `baseline` 均值直接混为一谈，因为后者只跑 `full` 任务且使用独立 compare 配置。
3. 当前主流程在三 seed 上保持了 `final_n_edge` 约 `88`、`macro_auc` 约 `0.957`、`run_total_wall_time_s` 约 `140s` 的工程量级。

## 6. A/B 工程策略对照（`benchmark_ab/comparison/`）

### 6.1 变体均值

`variant_summary.csv` 给出的结果如下：

| 变体 | final_acc | final_n_edge | macro_auc | run_total_wall_time_s | symbolic_core_seconds | symbolize_wall_time_s | validation_mean_r2 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| baseline | 0.777433 | 88.666667 | 0.956107 | 153.470521 | 33.867724 | 88.751556 | -0.672284 |
| adaptive | 0.742533 | 86.000000 | 0.945706 | 209.552334 | 47.499191 | 104.127099 | -0.646339 |
| adaptive_auto | 0.751467 | 89.000000 | 0.946249 | 130.715215 | 33.259280 | 74.526931 | -0.552361 |

### 6.2 相对 `baseline` 的差分

`pairwise_delta_summary.csv` 报告：

| 变体 | 指标 | mean_delta (variant - baseline) | win / lose / tie |
| --- | --- | ---: | ---: |
| adaptive | `final_acc` | -0.034900 | 0 / 3 / 0 |
| adaptive | `macro_auc` | -0.010401 | 0 / 3 / 0 |
| adaptive | `run_total_wall_time_s` | +56.081813 | 1 / 2 / 0 |
| adaptive | `symbolic_core_seconds` | +13.631467 | 2 / 1 / 0 |
| adaptive_auto | `final_acc` | -0.025967 | 0 / 3 / 0 |
| adaptive_auto | `macro_auc` | -0.009858 | 0 / 3 / 0 |
| adaptive_auto | `run_total_wall_time_s` | -22.755306 | 2 / 1 / 0 |
| adaptive_auto | `symbolic_core_seconds` | -0.608444 | 2 / 1 / 0 |
| adaptive_auto | `symbolize_wall_time_s` | -14.224624 | 2 / 1 / 0 |

### 6.3 Trace rhythm

`trace_summary.csv` 给出的剪枝节奏均值如下：

| 变体 | rounds_mean | effective_rounds_mean | total_edges_removed_mean | mean_drop_ratio_mean | max_drop_ratio_mean |
| --- | ---: | ---: | ---: | ---: | ---: |
| baseline | 10.666667 | 6.666667 | 23.333333 | 0.027671 | 0.088960 |
| adaptive | 0.666667 | 0.666667 | 14.666667 | 0.203953 | 0.203953 |
| adaptive_auto | 3.333333 | 2.666667 | 9.000000 | 0.019431 | 0.033532 |

解释：

1. `baseline` 仍是当前三条工程策略中质量最稳的路径，`final_acc` 与 `macro_auc` 均为最高。
2. `adaptive` 的自适应控制在这组种子上没有带来质量收益，反而显著拉长总时长并放大波动。
3. `adaptive_auto` 在速度侧优于 `baseline`，`run_total_wall_time_s` 平均减少约 `22.76s`，`symbolize_wall_time_s` 平均减少约 `14.22s`，但 `final_acc` 和 `macro_auc` 仍在三 seed 上全部落后于 `baseline`。
4. 从 trace 节奏看，`adaptive` 更短、更激进，`adaptive_auto` 在此基础上收敛得更稳，但二者都没有转化成对 `baseline` 的稳定质量优势。

## 7. 单因素消融矩阵（`benchmark_ablation/`）

### 7.1 变体均值

`ablation_runs_summary.csv` 给出的主要结果如下：

| 变体 | final_acc_mean | effective_input_dim_mean | expr_complexity_mean_mean | macro_auc_mean | validation_mean_r2_mean | stage_total_seconds_mean | symbolic_total_seconds_mean |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| full | 0.774967 | 57.666667 | 122.333333 | 0.952632 | -0.698252 | 44.567976 | 34.977065 |
| wostagewise | 0.406033 | 22.666667 | 51.258333 | 0.830331 | -0.840263 | 15.308342 | 17.168693 |
| wopruning | 0.799767 | 70.000000 | 186.866667 | 0.963459 | -0.520951 | 44.924998 | 44.318532 |
| wocompact | 0.790700 | 120.000000 | 130.266667 | 0.956052 | 0.143959 | 45.111240 | 44.896039 |
| wolayerwiseft | 0.782067 | 53.000000 | 133.633333 | 0.956629 | -0.686893 | 45.594888 | 21.640743 |

### 7.2 结果解释

1. `wostagewise`
   - `pre_symbolic_too_dense_mean = 1.0`，`effective_target_edges_mean = 1040`。
   - 这说明关闭 Stagewise Train 后，模型在进入 symbolization 前始终过密，工程约束失守。
   - 因此 Stagewise Train 不是可随意移除的装饰项，而是当前工程版可控复杂度的必要前提。
2. `wopruning`
   - 质量指标最高，但 `expr_complexity_mean_mean` 从 `122.33` 升到 `186.87`，`symbolic_total_seconds_mean` 从 `34.98s` 升到 `44.32s`。
   - 这说明 Progressive Pruning 的主要价值不是追求单点精度，而是把表达式复杂度和符号阶段成本压回到可接受区间。
3. `wocompact`
   - 关闭 Input Compaction 后，`effective_input_dim_mean` 固定回到 `120`，符号阶段总时长升到 `44.90s`。
   - 该切片在公式验证均值上更高，但伴随更大的输入维度与更高符号成本，不构成“应删除输入压缩”的充分证据。
4. `wolayerwiseft`
   - `symbolic_total_seconds_mean` 从 `34.98s` 降到 `21.64s`，但质量侧没有形成明显支配。
   - 这说明 Layerwise Finetune 在这组切片里主要体现为“额外成本换取更稳的符号阶段修正空间”，而不是必然带来立刻可见的点估计优势。
5. `full`
   - Full Pipeline 不是每个单项指标都最优，但它保持了复杂度、时长与质量之间最均衡的工程折中，因此仍适合作为默认主路径。

## 8. 结论与写作建议

1. `outputs/rerun_v2_engine_safe_20260318_rerun/` 应作为当前工程版总体 rerun 的主引用归档。
2. `benchmark_runs/` 支持“当前工程版默认主流程在三 seed 上稳定落在 `final_acc ≈ 0.769`、`macro_auc ≈ 0.957`、`run_total_wall_time_s ≈ 140s` 的量级”这一总体描述。
3. `benchmark_ab/comparison/` 支持“`baseline` 仍是当前三条工程策略中质量最稳的默认路径；`adaptive_auto` 能改善时长，但不足以替代 `baseline` 成为质量主引用”这一表述。
4. `benchmark_ablation/` 支持“Stagewise Train、Progressive Pruning 与 Input Compaction 共同构成当前工程版的核心结构约束；Full Pipeline 是当前最平衡的默认设定”这一表述。
5. 若论文或报告需要写“工程版总体 rerun”，优先引用本报告；若需要写“历史 `radial_bf` 专题”或“ICBR backend compare”，应分别转到 `2026-03-27` 与 `2026-04-01` 的带日期报告，而不要混引。
