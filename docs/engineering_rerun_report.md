# 工程版复测报告（Rerun）

## 1. 研究设定与口径

1. 历史参考版（Legacy）：`d8e09b5edadb988bd4a1638ea7109cf3ff5ef7d7`，对应 pre-release `v1.0.0-legacy-d8`。
2. 工程版（Current）：当前 `main`。
3. 本轮复测默认参数：`stagewise.guard_mode=light`，`stagewise.prune_acc_drop_tol=0.08`。
4. 复测执行日期：`2026-03-18`。
5. 本轮输出目录：`outputs/rerun_v2_engine_safe_20260318_rerun/`。
6. 对照目录（上一轮工程归档）：`outputs/rerun_v2_engine_safe_20260318/`。
7. 命令默认执行环境：`PowerShell`（Windows）。
8. 测试设备与运行时环境：
   - 操作系统：Windows 11 专业版 `23H2`（OS Build `22631.5472`）
   - Python：`Miniconda` 的 `kan` 环境，解释器路径 `C:\Users\chenpeng\miniconda3\envs\kan\python.exe`（`3.9.25`）
   - CPU：`12th Gen Intel(R) Core(TM) i5-12500H`
   - 内存：`16 GB`
   - 深度学习运行时：`PyTorch 2.1.2+cpu`（本轮复测按 CPU 路径执行）
9. 执行命令（PowerShell）：

```powershell
# 运行目录：仓库根目录（symkan-experiments/）
.\scripts\run_engineering_rerun.ps1 -PythonExe C:\Users\chenpeng\miniconda3\envs\kan\python.exe -OutRoot outputs/rerun_v2_engine_safe_20260318_rerun
```

## 2. 产物完整性核验

核验结论：本轮产物完整，具备后续统计分析条件。

1. 主 benchmark：`benchmark_runs/` 下共 `3` 个 run 目录，并存在 `symkanbenchmark_runs.csv`。
2. A/B 三变体：`baseline/adaptive/adaptive_auto` 各包含 `3` 个 run，且各自 `symkanbenchmark_runs.csv` 完整。
3. A/B 汇总文件齐全：`variant_summary.csv`、`pairwise_delta_summary.csv`、`seedwise_delta.csv`、`trace_seedwise.csv`、`trace_summary.csv`、`comparison_summary.md`。
4. 消融五变体齐全：`full/wostagewise/wopruning/wocompact/wolayerwiseft` 各包含 `3` 个 run，并生成 `ablation_runs_raw.csv` 与 `ablation_runs_summary.csv`。

## 3. 主 benchmark 统计结果（本轮 rerun）

数据源：`outputs/rerun_v2_engine_safe_20260318_rerun/benchmark_runs/symkanbenchmark_runs.csv`

| 指标 | 均值 | 标准差 |
| --- | ---: | ---: |
| `final_acc` | 0.7692 | 0.0054 |
| `macro_auc` | 0.9568 | 0.0014 |
| `final_n_edge` | 87.6667 | 2.6247 |
| `stage_total_seconds` | 45.1728 | 1.4216 |
| `symbolic_total_seconds` | 35.6519 | 2.3925 |
| `symbolize_wall_time_s` | 75.6998 | 2.8740 |
| `run_total_wall_time_s` | 140.3330 | 3.5777 |

## 4. 与上一轮工程归档对照（`...20260318`）

数据源：

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

解释：

1. 相较上一轮工程归档，本轮端到端 wall-time 明显收敛并下降。
2. `macro_auc` 基本稳定，而 `final_acc` 出现轻微回落。
3. `final_n_edge` 进一步降低，提示结构压缩程度提高，与精度轻微下降方向一致。

## 5. 与历史参考版（Legacy）对照

历史参考数据源：`outputs/benchmark_ab/baseline/symkanbenchmark_runs.csv`

口径说明：

1. Legacy 使用 `export_wall_time_s`，其语义对应工程版 `symbolize_wall_time_s`。
2. Legacy 不含 `run_total_wall_time_s`，该指标无法做一一对应比较。

| 指标 | 本轮 rerun | 历史参考版 | 差值 | 相对变化 |
| --- | ---: | ---: | ---: | ---: |
| `final_acc` | 0.7692 | 0.7807 | -0.0116 | -1.48% |
| `macro_auc` | 0.9568 | 0.9548 | +0.0019 | +0.20% |
| `final_n_edge` | 87.6667 | 89.6667 | -2.0000 | -2.23% |
| `stage_total_seconds` | 45.1728 | 39.7912 | +5.3817 | +13.52% |
| `symbolic_total_seconds` | 35.6519 | 33.2678 | +2.3841 | +7.17% |
| `symbolize_wall_time_s` | 75.6998 | 73.1687 | +2.5311 | +3.46% |

解释：

1. 工程版在增强可观测性与稳健性后，仍保持与 Legacy 接近的 AUC 水平。
2. `final_acc` 仍存在可见差距，阶段训练与符号化核心耗时也高于 Legacy。
3. 与上一轮工程归档相比，本轮 `symbolize_wall_time_s` 的下降幅度较大，提示工程链路内部仍有可优化空间。

## 6. 工程版 A/B 结果（本轮 rerun）

数据源：

1. `outputs/rerun_v2_engine_safe_20260318_rerun/benchmark_ab/comparison/variant_summary.csv`
2. `outputs/rerun_v2_engine_safe_20260318_rerun/benchmark_ab/comparison/pairwise_delta_summary.csv`

关键均值：

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

说明：

1. 对 `run_total_wall_time_s`，`win` 定义为“耗时更低（delta < 0）”。
2. `adaptive` 在本轮呈现较高方差（`symbolize_wall_time_s` 标准差约 `59.78s`），存在 seed 级异常放大风险。
3. `adaptive_auto` 在端到端耗时上最优，但准确率仍低于 baseline。

## 7. 工程版消融结果（本轮 rerun）

数据源：`outputs/rerun_v2_engine_safe_20260318_rerun/benchmark_ablation/ablation_runs_summary.csv`

| 变体 | `final_acc_mean` | `macro_auc_mean` | `symbolic_total_seconds_mean` | `effective_input_dim_mean` |
| --- | ---: | ---: | ---: | ---: |
| `full` | 0.7750 | 0.9526 | 34.9771 | 57.6667 |
| `wostagewise` | 0.4060 | 0.8303 | 17.1687 | 22.6667 |
| `wopruning` | 0.7998 | 0.9635 | 44.3185 | 70.0000 |
| `wocompact` | 0.7907 | 0.9561 | 44.8960 | 120.0000 |
| `wolayerwiseft` | 0.7821 | 0.9566 | 21.6407 | 53.0000 |

主要观察：

1. `wostagewise` 依旧显著失效，说明 stagewise 训练是核心必要组件。
2. `wopruning` 与 `wocompact` 虽提高精度，但符号化成本显著上升。
3. `wolayerwiseft` 在当前口径下仍体现较高成本收益比。

## 8. 方法学限制

1. 历史版与工程版的指标体系并非完全同构，部分对比仅可做语义映射而非严格同名比较。
2. 本轮统计基于固定三 seed，结论具备工程决策意义，但不应外推为充分统计显著性结论。
3. `adaptive` 的高方差提示其在局部随机条件下仍可能出现不稳定行为，后续需结合更细粒度日志进一步定位。

## 9. 结论与后续工作

1. 本轮 rerun 产物完整、口径一致，可作为当前工程版的主引用结果。
2. 建议继续采用“双锚点”叙述：Legacy 作为历史参考，工程版 rerun 作为当前正式结论。
3. 后续优化优先级建议：
   - 针对 `adaptive` 的 seed 级异常放大进行机制性排查；
   - 持续压缩 `symbolize_wall_time_s` 的非核心开销；
   - 在维持 `macro_auc` 稳定前提下，回收 `final_acc` 的小幅损失。
