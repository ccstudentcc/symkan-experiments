# LayerwiseFT 改进实验报告（2026-03 最新重跑）

## 文档导航

- 返回总览：[README](../README.md)
- docs 总入口：[index](index.md)
- 消融说明：[ablation_usage](ablation_usage.md)
- 消融计划：[ablation_plan](ablation_plan.md)
- 消融总报告：[ablation_report](ablation_report.md)
- benchmark 文档：[symkanbenchmark_usage](symkanbenchmark_usage.md)

## 目录

- [1. 实验目标](#1-实验目标)
- [2. 实验配置](#2-实验配置)
- [3. 结果汇总（mean ± std，n=3）](#3-结果汇总mean--stdn3)
- [4. 关键对比](#4-关键对比)
- [5. 核心判断](#5-核心判断)
- [6. 产出文件](#6-产出文件)

## 1. 实验目标

评估改进版 LayerwiseFT（`layerwiseft_esreg`）相对：

1. `full`（当前已与 `layerwiseft_esreg` 默认参数对齐）
2. `wolayerwiseft`（关闭 LayerwiseFT）

核心问题：改进版是否在精度、稳定性、耗时上有可验证净收益。

---

## 2. 实验配置

- seeds：42 / 52 / 62
- 数据来源：`benchmark_ablation/layerwiseft_improved_analysis/`
- 对比文件：
  - `comparison_summary.csv`
  - `delta_new_vs_full.csv`
  - `delta_new_vs_wolayerwiseft.csv`

当前默认口径：`full` 与 `layerwiseft_esreg` 均采用“验证早停 + 轻正则 + 60 步短微调”。

---

## 3. 结果汇总（mean ± std，n=3）

> 标记规则：`↑` / `↓` 表示相对对照项上升/下降；`↑↑` / `↓↓` 表示绝对变化 >= 10%；`≈` 表示变化在误差范围内（绝对变化 < 1%）。

| 变体 | 最终精度 | Macro-AUC | 表达式复杂度 | 公式 R²（验证） | 符号化耗时 (s) | 阶段训练耗时 (s) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| full | 0.7807 ± 0.0013 | 0.9548 ± 0.0028 | 126.90 ± 31.17 | -0.6135 ± 0.0331 | 33.58 ± 0.31 | 40.33 ± 1.76 |
| layerwiseft_esreg | 0.7807 ± 0.0013 ≈ | 0.9548 ± 0.0028 ≈ | 126.90 ± 31.17 ≈ | -0.6135 ± 0.0331 ≈ | 33.28 ± 1.34 ≈ | 40.02 ± 1.51 ≈ |
| wolayerwiseft | 0.7838 ± 0.0014 ≈ | 0.9544 ± 0.0047 ≈ | 126.90 ± 31.17 ≈ | -0.5937 ± 0.0151 ↑ | 20.41 ± 0.06 ↓↓ | 39.54 ± 1.66 ↓ |

---

## 4. 关键对比

### 4.1 改进版 vs full

来自 `delta_new_vs_full.csv`：

- 分类指标：`final_acc` 与 `macro_auc` 差值均为 0（≈）。
- 结构指标：`final_n_edge`、`effective_input_dim`、复杂度均无差异（≈）。
- 时间指标：
  - `symbolic_total_seconds`：-0.3046s（33.58s -> 33.28s，-0.91%，≈）
  - `stage_total_seconds`：-0.3089s（40.33s -> 40.02s，-0.77%，≈）

结论：当前口径下 `full` 与 `layerwiseft_esreg` 已是同一默认参数组合，二者只表现为统计噪声级时间差，未带来可观测精度或结构差异。

### 4.2 改进版 vs 关闭 LayerwiseFT

来自 `delta_new_vs_wolayerwiseft.csv`：

- `final_acc`：-0.00303（0.7838 -> 0.7807，-0.39%，≈）
- `macro_auc`：+0.00044（0.9544 -> 0.9548，+0.05%，≈）
- `validation_mean_r2`：-0.01985（-0.5937 -> -0.6135，数值一致性变差）
- `symbolic_total_seconds`：+12.8624s（20.41s -> 33.28s，+63.00%，↑↑）

结论：相对 `wolayerwiseft`，改进版 LayerwiseFT 的主要效应是显著增时，净收益不成立。

### 4.3 为什么改进版仍难产生净收益（2 层 KAN）

#### 理论起点：有损替换 + 冻结约束

KAN 的表示可写为：$f(x)=\sum_q\Phi_q\bigl(\sum_p\phi_{qp}(x_p)\bigr)$。逐层符号化时，B-spline 会被替换为解析原子 $a\cdot g(bx+c)+d$。这一步本质是有损替换：候选函数族一旦选定，后续只能在仿射参数上调整，不能回退重选函数族。

#### 结构层面：2 层网络只有一次补偿机会

在 2 层 KAN（`depth=2`）里，LayerwiseFT 只在 `l < depth - 1` 条件下触发一次，即 layer 0 符号化后只给输出层一次局部补偿窗口。可优化自由度天然受限，难以形成稳定的全局收益。

#### 实现层面：`fix_symbolic` 的冻结效应与序列偏差

`fix_symbolic` 用激活样本做拟合后会冻结已选函数族。LayerwiseFT 发生在冻结之后，因此更像“在受约束模型上做局部修补”。这会带来典型的序列偏差风险：

1. 前一层已固定解析函数决定后一层输入分布。
2. 后一层局部优化会优先拟合这个中间分布，而非原始任务全局最优。
3. 当后一层再被符号化时，函数族选择会继承这种局部偏差。

这与分层贪心训练的已知结论一致：局部最优叠加不等于全局最优。

#### 为什么“改进版”没有逆转这个结论

旧版 LayerwiseFT（长步数、无验证约束）更容易放大上述偏差；改进版（早停 + 轻正则 + 60 步）是在降低风险，但并没有改变“冻结函数族 + 单次补偿窗口”的结构事实。因此它通常只能把副作用变小，而不是稳定创造净增益。

#### 数据层面（与理论对齐）

最新重跑显示：

- 相对 `full`，改进版所有核心质量指标都为 0 差异（`final_acc`、`macro_auc`、复杂度、`validation_mean_r2` 均不变），这与“二者默认参数已对齐”一致。
- 相对 `wolayerwiseft`，改进版的分类优势不存在（`final_acc` 反而低 0.0030），但符号化耗时增加 63.00%。

这说明在当前 2 层配置下，LayerwiseFT 更像“高成本、低确定性收益”的可选路径，而不是默认路径。

---

## 5. 核心判断

【核心判断】
不值得作为默认路径。

【关键洞察】

1. 数据结构层面：`full` 与 `layerwiseft_esreg` 现已共享同一默认参数，输出统计一致属于预期，不应再解读为新增方法收益。
2. 复杂度层面：增加 LayerwiseFT 仍然主要增加耗时，而非稳定提高分类或公式验证指标。
3. 风险层面：把 LayerwiseFT 作为默认会放大运行成本，但收益不确定。

【默认策略】

1. 2 层 KAN 默认：`--layerwise-finetune-steps 0`。
2. 改进版 LayerwiseFT：保留为可选实验开关，不作为默认。
3. 若后续要再次验证其必要性，建议扩展到至少 10 seeds，并增加更深网络设置（depth >= 3）再判断。

---

## 6. 产出文件

- `benchmark_ablation/layerwiseft_improved_analysis/comparison_summary.csv`
- `benchmark_ablation/layerwiseft_improved_analysis/delta_new_vs_full.csv`
- `benchmark_ablation/layerwiseft_improved_analysis/delta_new_vs_wolayerwiseft.csv`
