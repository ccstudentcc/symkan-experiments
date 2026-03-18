# 工程版复测报告（Rerun）

## 1. 版本与口径

1. 历史参考版（Legacy）：`d8e09b5edadb988bd4a1638ea7109cf3ff5ef7d7`，对应 pre-release：`v1.0.0-legacy-d8`。
2. 工程版（Current）：当前 `main`。
3. 本轮复测默认参数：`stagewise.guard_mode=light`，`stagewise.prune_acc_drop_tol=0.08`。
4. 本轮复测执行日期：`2026-03-18`。
5. 本轮输出目录：`outputs/rerun_v2_engine_safe_20260318_rerun/`。
6. 上一轮工程归档目录：`outputs/rerun_v2_engine_safe_20260318/`（用于本报告中的“工程内二次对照”）。
7. 复测执行命令（PowerShell）：

```powershell
.\scripts\run_engineering_rerun.ps1 -PythonExe C:\Users\chenpeng\miniconda3\envs\kan\python.exe -OutRoot outputs/rerun_v2_engine_safe_20260318_rerun
```

## 2. 产物完整性检查

检查结果：完整通过。

1. 主 benchmark：`benchmark_runs/` 下有 `3` 个 run 目录，且存在 `symkanbenchmark_runs.csv`。
2. A/B 三变体：`baseline/adaptive/adaptive_auto` 各有 `3` 个 run，且各自 `symkanbenchmark_runs.csv` 完整。
3. A/B 汇总产物完整：`variant_summary.csv`、`pairwise_delta_summary.csv`、`seedwise_delta.csv`、`trace_seedwise.csv`、`trace_summary.csv`、`comparison_summary.md` 均存在。
4. 消融五变体：`full/wostagewise/wopruning/wocompact/wolayerwiseft` 各有 `3` 个 run，且 `ablation_runs_raw.csv`、`ablation_runs_summary.csv` 存在。

## 3. 主 benchmark 结果（本轮 rerun）

数据来源：`outputs/rerun_v2_engine_safe_20260318_rerun/benchmark_runs/symkanbenchmark_runs.csv`

| 指标 | 均值 | 标准差 |
| --- | ---: | ---: |
| `final_acc` | 0.7692 | 0.0054 |
| `macro_auc` | 0.9568 | 0.0014 |
| `final_n_edge` | 87.6667 | 2.6247 |
| `stage_total_seconds` | 45.1728 | 1.4216 |
| `symbolic_total_seconds` | 35.6519 | 2.3925 |
| `symbolize_wall_time_s` | 75.6998 | 2.8740 |
| `run_total_wall_time_s` | 140.3330 | 3.5777 |

## 4. 与上一轮工程归档对比（`...20260318`）

数据来源：

1. 本轮：`outputs/rerun_v2_engine_safe_20260318_rerun/benchmark_runs/symkanbenchmark_runs.csv`
2. 上轮：`outputs/rerun_v2_engine_safe_20260318/benchmark_runs/symkanbenchmark_runs.csv`

| 指标 | 本轮 rerun | 上轮工程版 | 差值 | 相对变化 |
| --- | ---: | ---: | ---: | ---: |
| `final_acc` | 0.7692 | 0.7786 | -0.0095 | -1.22% |
| `macro_auc` | 0.9568 | 0.9567 | +0.0001 | +0.01% |
| `final_n_edge` | 87.6667 | 89.0000 | -1.3333 | -1.50% |
| `stage_total_seconds` | 45.1728 | 46.1217 | -0.9489 | -2.06% |
| `symbolic_total_seconds` | 35.6519 | 36.0723 | -0.4204 | -1.17% |
| `symbolize_wall_time_s` | 75.6998 | 88.5343 | -12.8345 | -14.50% |
| `run_total_wall_time_s` | 140.3330 | 154.0382 | -13.7053 | -8.90% |

解读：

1. 相比上一轮工程归档，本轮在 wall-time 指标上明显更快。
2. `macro_auc` 基本持平，但 `final_acc` 小幅下降。
3. 本轮 `final_n_edge` 更低，说明结构压缩更激进，这与精度轻微回落同向。

## 5. 与历史参考版（Legacy）对比

历史参考数据来源：`outputs/benchmark_ab/baseline/symkanbenchmark_runs.csv`

说明：

1. Legacy 使用 `export_wall_time_s`，语义对应工程版的 `symbolize_wall_time_s`。
2. Legacy 无 `run_total_wall_time_s`，因此该字段无法直接对齐对比。

| 指标 | 本轮 rerun | 历史参考版 | 差值 | 相对变化 |
| --- | ---: | ---: | ---: | ---: |
| `final_acc` | 0.7692 | 0.7807 | -0.0116 | -1.48% |
| `macro_auc` | 0.9568 | 0.9548 | +0.0019 | +0.20% |
| `final_n_edge` | 87.6667 | 89.6667 | -2.0000 | -2.23% |
| `stage_total_seconds` | 45.1728 | 39.7912 | +5.3817 | +13.52% |
| `symbolic_total_seconds` | 35.6519 | 33.2678 | +2.3841 | +7.17% |
| `symbolize_wall_time_s` | 75.6998 | 73.1687 | +2.5311 | +3.46% |

解读：

1. 工程版在可观测性与稳定性增强后，仍保留了与 Legacy 接近的 AUC 水平。
2. `final_acc` 仍有可见差距，且阶段训练与符号化核心耗时仍高于 Legacy。
3. 相比上一轮工程归档，本轮 `symbolize_wall_time_s` 显著下降，说明工程链路内部仍有优化空间。

## 6. 工程版 A/B 结果（本轮 rerun）

数据来源：

1. `outputs/rerun_v2_engine_safe_20260318_rerun/benchmark_ab/comparison/variant_summary.csv`
2. `outputs/rerun_v2_engine_safe_20260318_rerun/benchmark_ab/comparison/pairwise_delta_summary.csv`

关键均值（mean）：

1. `baseline`：`final_acc=0.7774`，`macro_auc=0.9561`，`run_total_wall_time_s=153.4705`。
2. `adaptive`：`final_acc=0.7425`，`macro_auc=0.9457`，`run_total_wall_time_s=209.5523`。
3. `adaptive_auto`：`final_acc=0.7515`，`macro_auc=0.9462`，`run_total_wall_time_s=130.7152`。

pairwise（variant - baseline）：

| 比较 | 指标 | mean_delta | 胜 / 负 / 平 |
| --- | --- | ---: | ---: |
| `adaptive vs baseline` | `final_acc` | -0.0349 | 0 / 3 / 0 |
| `adaptive vs baseline` | `macro_auc` | -0.0104 | 0 / 3 / 0 |
| `adaptive vs baseline` | `run_total_wall_time_s` | +56.0818 | 1 / 2 / 0 |
| `adaptive_auto vs baseline` | `final_acc` | -0.0260 | 0 / 3 / 0 |
| `adaptive_auto vs baseline` | `macro_auc` | -0.0099 | 0 / 3 / 0 |
| `adaptive_auto vs baseline` | `run_total_wall_time_s` | -22.7553 | 2 / 1 / 0 |

补充说明：

1. 本表中 `run_total_wall_time_s` 的 `win` 定义为“耗时更低（delta<0）”。
2. 本轮 `adaptive` 波动显著（`symbolize_wall_time_s` 标准差约 `59.78s`），存在 seed 级异常放大。
3. `adaptive_auto` 依然是三者中端到端耗时最优，但精度不及 baseline。

## 7. 工程版消融结果（本轮 rerun）

数据来源：`outputs/rerun_v2_engine_safe_20260318_rerun/benchmark_ablation/ablation_runs_summary.csv`

| 变体 | `final_acc_mean` | `macro_auc_mean` | `symbolic_total_seconds_mean` | `effective_input_dim_mean` |
| --- | ---: | ---: | ---: | ---: |
| `full` | 0.7750 | 0.9526 | 34.9771 | 57.6667 |
| `wostagewise` | 0.4060 | 0.8303 | 17.1687 | 22.6667 |
| `wopruning` | 0.7998 | 0.9635 | 44.3185 | 70.0000 |
| `wocompact` | 0.7907 | 0.9561 | 44.8960 | 120.0000 |
| `wolayerwiseft` | 0.7821 | 0.9566 | 21.6407 | 53.0000 |

主要观察：

1. `wostagewise` 仍明显失效，stagewise 训练依然是必要组件。
2. `wopruning` 与 `wocompact` 的精度较高，但都带来显著符号化成本上升。
3. `wolayerwiseft` 在本轮仍保持较高的成本收益比。

## 8. 结论与后续建议

1. 本轮 rerun 产物完整、口径一致，可作为当前工程版的最新主引用结果。
2. 结论层面建议继续采用“双锚点”：Legacy（历史参考）+ 工程版 rerun（当前主结论）。
3. 后续优化优先级建议：
   - 排查 `adaptive` 在特定 seed 下的 wall-time 异常放大；
   - 继续压缩 `symbolize_wall_time_s` 中的非核心开销；
   - 在保持 `macro_auc` 的前提下回收 `final_acc` 的轻微损失。
