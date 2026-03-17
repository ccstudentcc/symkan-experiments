# symkan 单点消融实验报告

## 文档导航

- 返回总览：[README](../README.md)
- docs 总入口：[index](index.md)
- 消融说明：[ablation_usage](ablation_usage.md)
- 消融计划：[ablation_plan](ablation_plan.md)
- LayerwiseFT 改进报告：[layerwiseft_improved_report](layerwiseft_improved_report.md)
- benchmark 文档：[symkanbenchmark_usage](symkanbenchmark_usage.md)

## 目录

- [1. 实验设计回顾](#1-实验设计回顾)
- [2. 主要指标汇总（mean ± std，n=3）](#2-主要指标汇总mean--stdn3)
- [3. 各模块单点消融分析](#3-各模块单点消融分析)
- [4. 综合分析](#4-综合分析)
- [5. 结论（统一口径）](#5-结论统一口径)

**实验日期**：2026-03-14
**数据集**：内部 MNIST 特征集（10 类，784 维输入）
**数据来源**：`outputs/benchmark_ablation/ablation_runs_summary.csv`
**实验设定**：seeds 42 / 52 / 62（n=3），global-seed=123，lib-preset=layered，symbolic-target-edges=90

---

## 1. 实验设计回顾

本实验基于 `docs/ablation_plan.md` 的框架，对 symkan 流水线的四个核心模块做单点消融：

| 变体 ID | 变体名称 | 关闭的模块 | 关键 CLI 开关 |
| --- | --- | --- | --- |
| V0 | Full Pipeline | —（基线） | 默认配置 |
| V1 | w/o Stagewise Train | 分阶段训练 | `--disable-stagewise-train --prune-collapse-floor 0.0` |
| V2 | w/o Progressive Pruning | 渐进剪枝 | `--max-prune-rounds 0` |
| V3 | w/o Input Compaction | 输入压缩 | `--no-input-compaction` |
| V4 | w/o Layerwise Finetune | 层间微调 | `--layerwise-finetune-steps 0` |

除被关闭模块外，其余超参与基线完全一致。

---

## 2. 主要指标汇总（mean ± std，n=3）

> 标记规则：`↑` / `↓` 表示相对基线上升/下降；`↑↑` / `↓↓` 表示绝对变化 >= 10%；`≈` 表示变化在误差范围内（绝对变化 < 1%）。

| 变体 | 最终精度 | Macro-AUC | 表达式复杂度 | 公式 R²（验证） | 有效输入维数 | 阶段训练耗时 (s) | 符号化耗时 (s) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| V0 Full | **0.7807 ± 0.0013** | **0.9548 ± 0.0028** | **126.90 ± 31.17** | **-0.6135 ± 0.0331** | **57.67 ± 2.31** | **40.33 ± 1.76** | **33.58 ± 0.31** |
| V1 w/o Stagewise | 0.4430 ± 0.0319 ↓↓ | 0.8379 ± 0.0095 ↓↓ | 48.44 ± 16.44 ↓↓ | -0.7657 ± 0.1535 ↓↓ | 23.00 ± 4.00 ↓↓ | 13.68 ± 0.07 ↓↓ | 16.64 ± 2.74 ↓↓ |
| V2 w/o Pruning | 0.8017 ± 0.0088 ↑ | 0.9639 ± 0.0011 ≈ | 194.33 ± 37.22 ↑↑ | -0.4976 ± 0.1376 ↑↑ | 70.00 ± 2.65 ↑↑ | 39.24 ± 1.62 ↓ | 43.51 ± 0.40 ↑↑ |
| V3 w/o Compact | 0.7577 ± 0.0278 ↓ | 0.9491 ± 0.0083 ≈ | 120.10 ± 2.26 ↓ | +0.0275 ± 0.1365 ↑↑ | 120.00 ± 0.00 ↑↑ | 39.52 ± 1.13 ≈ | 41.34 ± 0.64 ↑↑ |
| V4 w/o LayerwiseFT | 0.7838 ± 0.0014 ≈ | 0.9544 ± 0.0047 ≈ | 126.90 ± 31.17 ≈ | -0.5937 ± 0.0151 ↑↑ | 57.67 ± 2.31 ≈ | 39.54 ± 1.66 ≈ | 20.41 ± 0.06 ↓↓ |

---

## 3. 各模块单点消融分析

### 3.1 V1：去掉 Stagewise Train

该变体表明，Stagewise 训练是当前流程的关键组成部分；移除后，整条符号化链路的可用性显著下降。

- `final_acc`: 0.7807 -> 0.4430，下降 **43.26%**（绝对 -0.3377）。
- `macro_auc`: 0.9548 -> 0.8379，下降 **12.25%**（绝对 -0.1169）。
- `effective_target_edges`: 90 -> 1040，提升 **1055.56%**（11.56 倍）。
- `effective_input_dim`: 57.67 -> 23.00，下降 **60.12%**。

虽然 `stage_total_seconds` 与 `symbolic_total_seconds` 分别下降 66.07% 和 50.46%，但这种下降主要来自必要稀疏化准备阶段的缺失，因此最终输出质量并不具备可用性。该结果支持“先实现可控稀疏化，再进行符号化”的流程设计。

### 3.2 V2：去掉 Progressive Pruning

该变体表明，取消渐进剪枝可以在部分分类指标上获得提升，但其代价是模型与公式复杂度明显增加。

- `final_acc`: +2.68%（0.7807 -> 0.8017）。
- `macro_auc`: +0.95%（误差范围内）。
- `expr_complexity_mean`: **+53.14%**（126.90 -> 194.33）。
- `effective_input_dim`: **+21.39%**（57.67 -> 70.00）。
- `symbolic_total_seconds`: **+29.56%**（33.58s -> 43.51s）。

`validation_mean_r2` 从 -0.6135 提升到 -0.4976（绝对 +0.1159），说明保留更多边有助于改善数值拟合，但结果仍位于负值区间。因此，该模块的主要作用仍是复杂度控制，而非分类精度提升。

### 3.3 V3：去掉 Input Compaction

该变体表明，输入压缩对应的是公式数值拟合质量与符号化成本之间的显著权衡。

- `final_acc`: -2.95%（0.7807 -> 0.7577）。
- `macro_auc`: -0.60%（误差范围内）。
- `validation_mean_r2`: -0.6135 -> **+0.0275**，绝对提升 **+0.6410**（跨越 0）。
- `effective_input_dim`: 57.67 -> 120.00，增加 **108.09%**。
- `symbolic_total_seconds`: 33.58s -> 41.34s，增加 **23.10%**。

保留全部输入维度后，公式数值拟合质量明显提升，但符号化开销也同步增加。因而该模块的取舍应取决于研究重点是运行成本还是公式一致性。

### 3.4 V4：去掉 LayerwiseFT

该变体表明，在当前 2 层 KAN 设置下，关闭 LayerwiseFT 能够在保持近似分类表现的同时显著降低符号化耗时。

- `final_acc`: 0.7807 -> 0.7838，+0.39%（误差范围内）。
- `macro_auc`: 0.9548 -> 0.9544，-0.05%（误差范围内）。
- `expr_complexity_mean` 与 `effective_input_dim`: 0 变化。
- `validation_mean_r2`: -0.6135 -> -0.5937，绝对改善 +0.0198。
- `symbolic_total_seconds`: 33.58s -> 20.41s，下降 **39.21%**。

`full` 与 `w/o LayerwiseFT` 的精度方差处于同一量级（0.0013 vs 0.0014），因此不宜再将“方差显著缩小”作为核心论据；但“精度变化有限、时间成本明显”的判断仍然成立。

### 3.4.1 LayerwiseFT 效果差异的理论解释

#### 理论起点：有损替换 + 冻结约束

KAN 的表示可写为：$f(x)=\sum_q\Phi_q\bigl(\sum_p\phi_{qp}(x_p)\bigr)$。逐层符号化时，B-spline 会被替换为解析原子 $a\cdot g(bx+c)+d$。该过程属于有损替换：候选函数族一旦选定，后续只能调整仿射参数，而无法回退并重新选择函数族。

#### 结构与实现：2 层网络的单窗口补偿 + 贪心序列偏差

在 2 层 KAN（`depth=2`）中，LayerwiseFT 仅在 `l < depth - 1` 条件下触发一次，因此补偿窗口有限。`fix_symbolic` 冻结函数族后，LayerwiseFT 实际上成为受限模型上的局部修正，容易引入序列偏差。

旧版 LayerwiseFT（长步数、无验证约束）更容易放大该问题；改进版（早停 + 轻正则 + 60 步）主要是在降风险，而不是改变结构上“单次补偿窗口”的事实。

#### 从最新数据看（与理论一致）

- `full` 与 `w/o LayerwiseFT` 的分类指标几乎重叠（`final_acc` 差 0.0030，`macro_auc` 差 0.0004）。
- 改进版 `layerwiseft_esreg` 相对 `full` 的收益主要是亚秒级时间差（`symbolic_total_seconds` -0.3046s，`stage_total_seconds` -0.3089s），对精度与复杂度无实质影响；这也与“当前 `full` 已对齐 `layerwiseft_esreg` 默认参数”一致。
- 相对 `w/o LayerwiseFT`，改进版仍多消耗 12.86s 符号化时间，同时 `final_acc` 低 0.0030、`validation_mean_r2` 低 0.0198。

上述结果与理论分析一致：在 2 层设置中，LayerwiseFT 并未表现为决定性增益项，而更接近高成本的可选微调步骤。

---

## 4. 综合分析

### 4.1 模块贡献矩阵

| 模块 | 分类精度贡献 | 公式复杂度 | 数值一致性（R²） | 工程效率 |
| --- | --- | --- | --- | --- |
| 分阶段训练 | **决定性**（去掉后 acc -43.26%） | 复杂度下降但输出失效 | 变差 | 耗时减少但无意义 |
| 渐进剪枝 | 小幅波动 | **显著抑制复杂度膨胀** | 略负向 | 显著降低符号化开销 |
| 输入压缩 | 小幅负向 | 略降 | **显著负向（关掉后 R² 提升 +0.641）** | 显著加速 |
| 层间微调 | 不显著 | 近零影响 | 边际影响 | **显著增加符号化耗时** |

### 4.2 关键权衡

1. `stagewise_train` 是“可用/不可用”分界线，不是调参开关。
2. 渐进剪枝主要控制表达式体积与符号化成本，可读性目标下应保留。
3. 输入压缩牺牲部分公式数值拟合，换取更低输入维数和更低耗时。
4. LayerwiseFT 在 2 层 KAN 中不构成默认收益项，默认关闭更符合收益/代价比。

---

## 5. 结论（统一口径）

| 优先级 | 模块 | 建议 |
| --- | --- | --- |
| 必须保留 | 分阶段训练 | 去掉会导致符号化入口过密，输出质量失效 |
| 默认保留 | 渐进剪枝 | 控制复杂度与符号化成本的关键模块 |
| 场景取舍 | 输入压缩 | 吞吐优先保留；若追求公式数值拟合可按需关闭 |
| 默认关闭（2 层 KAN） | LayerwiseFT | 精度收益不稳定且幅度小，符号化耗时成本明确 |

---

## 6. 数据与复现路径

- 原始汇总：`outputs/benchmark_ablation/ablation_runs_summary.csv`
- 原始明细：`outputs/benchmark_ablation/ablation_runs_raw.csv`
- LayerwiseFT 改进对比：`outputs/benchmark_ablation/layerwiseft_improved_analysis/{comparison_summary.csv,delta_new_vs_full.csv,delta_new_vs_wolayerwiseft.csv}`
- 各变体运行目录：`outputs/benchmark_ablation/{full,wostagewise,wopruning,wocompact,wolayerwiseft}/`
- 运行脚本：`ablation_runner.py`、`compare_layerwiseft_improved.py`
