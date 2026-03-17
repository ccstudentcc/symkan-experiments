# symkan 单点消融实验计划

## 文档导航

- 返回总览：[README](../README.md)
- docs 总入口：[index](index.md)
- 消融说明：[ablation_usage](ablation_usage.md)
- 消融报告：[ablation_report](ablation_report.md)
- LayerwiseFT 改进报告：[layerwiseft_improved_report](layerwiseft_improved_report.md)
- benchmark 文档：[symkanbenchmark_usage](symkanbenchmark_usage.md)

## 目录

- [1. 实验目标](#1-实验目标)
- [2. 实验约定](#2-实验约定)
- [3. 基线定义](#3-基线定义)
- [4. 单点消融设计](#4-单点消融设计)
- [5. 实验矩阵](#5-实验矩阵)
- [6. 结果记录字段](#6-结果记录字段)
- [7. 结果分析框架](#7-结果分析框架)
- [8. 工程实现框架](#8-工程实现框架)
- [9. 风险控制](#9-风险控制)
- [10. 交付物](#10-交付物)

## 1. 实验目标

本计划围绕 symkan 的两段式流程展开单点消融，以识别各设计项在分类性能、复杂度、数值一致性与运行成本上的实际作用。

核心问题包括：

1. 分阶段训练是否能够提供更适于后续符号化的模型快照。
2. 渐进剪枝、输入压缩与层间微调分别贡献了哪些收益或代价。
3. 各模块的作用主要体现在精度、复杂度、稳定性还是运行时间上。

## 2. 实验约定

### 2.1 数据与随机性

1. 数据输入沿用 `symkanbenchmark.py` 的默认逻辑：`data/X_train.npy`、`data/X_test.npy`、`data/Y_train_cat.npy`、`data/Y_test_cat.npy`（兼容旧版根目录 `X_train.npy`、`X_test.npy`、`Y_train_cat.npy`、`Y_test_cat.npy`）。
2. 全局随机数固定为 `--global-seed 123`。
3. 变体比较采用 `--stagewise-seeds 42,52,62`。
4. 核心指标统一报告为 `mean ± std`（n=3）。

### 2.2 公平性约束

1. 网络结构固定为 `inner_dim=16, grid=5, k=3`。
2. 函数库固定为 `lib-preset=layered`。
3. 符号化目标固定为 `symbolic_target_edges=90`。
4. 除被消融模块外，其余参数与基线保持一致。
5. 每个变体均须保留完整中间文件，而非仅保留最终指标。

### 2.3 执行环境

1. 全部实验使用统一 Python 环境。
2. 全部变体在同一硬件条件下运行。
3. 每个变体使用独立 `output_dir`，以避免结果覆盖。

## 3. 基线定义

基线采用 `symkanbenchmark.py` 的 `full` 流程与三随机种子设置。

参考命令如下：

```bash
python symkanbenchmark.py \
  --tasks full \
  --stagewise-seeds 42,52,62 \
  --global-seed 123 \
  --output-dir outputs/benchmark_ablation/full \
  --quiet
```

基线流程包括：

1. baseline KAN 训练与归因筛选。
2. `stagewise_train` 分阶段训练、剪枝与选模。
3. `symbolize_pipeline` 的渐进剪枝、输入压缩、逐层符号化、层间微调与 affine 微调。

## 4. 单点消融设计

### 4.1 `w/o Stagewise Train`

定义：以端到端一次性训练替代 `stagewise_train`，其余流程不变。

控制要点：

1. 保持数据构建、特征筛选与 `symbolize_pipeline` 不变。
2. 训练预算按阶段训练总步数进行对齐。
3. 同时设置 `--prune-collapse-floor 0.0` 与较宽松的 `--symbolic-prune-adaptive-acc-drop-tol`，以避免稠密入口导致剪枝阶段直接回滚。

### 4.2 `w/o Progressive Pruning`

定义：关闭符号化阶段的渐进剪枝。

实现方式：

- `max_prune_rounds = 0`

### 4.3 `w/o Input Compaction`

定义：关闭输入压缩步骤，在原始输入维度上执行符号化。

实现方式：

- `--no-input-compaction`

### 4.4 `w/o Layerwise Finetune`

定义：取消逐层符号化后的层间微调，仅保留后续统一微调。

实现方式：

- `layerwise_finetune_steps = 0`

## 5. 实验矩阵

| variant_id | 变体名 | Stagewise | Progressive Pruning | Input Compaction | Layerwise FT | 备注 |
| --- | --- | --- | --- | --- | --- | --- |
| V0 | Full Pipeline | on | on | on | on | 基线 |
| V1 | w/o Stagewise Train | off | on | on | on | 需同时设置 `--prune-collapse-floor 0.0` |
| V2 | w/o Progressive Pruning | on | off | on | on | `--max-prune-rounds 0` |
| V3 | w/o Input Compaction | on | on | off | on | `--no-input-compaction` |
| V4 | w/o Layerwise Finetune | on | on | on | off | `--layerwise-finetune-steps 0` |

总运行规模为 `5 variants × 3 seeds = 15 runs`。

## 6. 结果记录字段

本次实验至少应记录以下字段：

| 字段名 | 说明 | 来源 |
| --- | --- | --- |
| variant_id | 变体编号 | 运行配置 |
| seed | 随机种子 | CLI |
| effective_target_edges | 符号化有效目标边数 | metrics |
| effective_input_dim | 符号化有效输入维度 | metrics |
| final_acc | 符号化后精度 | metrics |
| expr_complexity_mean | 表达式平均复杂度 | `kan_symbolic_summary.csv` |
| macro_auc | 多分类宏平均 AUC | metrics |
| validation_mean_r2 | 公式数值验证平均 `R²` | metrics |
| symbolic_total_seconds | 符号化总耗时 | metrics |
| stage_total_seconds | 训练准备总耗时 | metrics / stage logs |
| rounds | 剪枝轮数 | `symbolize_trace.csv` |
| edges_drop_total | 总剪枝边数 | trace 聚合 |

## 7. 结果分析框架

各变体应按照相同框架进行分析：

1. 精度变化：比较 `final_acc` 与 `macro_auc`。
2. 表达式复杂度变化：比较 `expr_complexity_mean` 与有效表达式数量。
3. 数值一致性：比较 `validation_mean_r2` 与负 `R²` 比例。
4. 稀疏结构变化：比较 `effective_target_edges`、`effective_input_dim` 与 `rounds`。
5. 运行成本：比较 `stage_total_seconds` 与 `symbolic_total_seconds`。
6. 稳定性：比较 3 个 seeds 下的标准差。

## 8. 工程实现框架

当前工程实现采用 `ablation_runner.py` 作为统一入口，其职责包括：

1. 使用 `VARIANT_SPECS` 定义各变体的额外参数。
2. 调用 `symkanbenchmark.py` 运行各变体。
3. 读取 `symkanbenchmark_runs.csv` 并附加变体标签。
4. 跨 seed 生成原始结果表与汇总结果表。
5. 在 `--aggregate-only` 模式下直接聚合已有结果目录。

为支持消融实验，相关代码修改主要包括：

1. `symkan/symbolic/pipeline.py`
   - 增加输入压缩开关。
   - 增加 `prune_collapse_floor` 参数。
2. `symkan/tuning/stagewise.py`
   - 增加每阶段计时字段。
   - 增加阶段总耗时汇总字段。
3. `symkanbenchmark.py`
   - 增加 `--disable-stagewise-train`
   - 增加 `--no-input-compaction`
   - 增加 `--layerwise-finetune-steps`
   - 增加 `--max-prune-rounds`
   - 增加与端到端训练相关的控制参数

## 9. 风险控制

实验执行中应满足以下要求：

1. 不跨变体改动无关超参数。
2. 不省略失败运行，须记录失败原因。
3. 统计报告同时给出均值与标准差。
4. 对 `w/o Stagewise Train` 须明确说明训练预算对齐方式。

## 10. 交付物

实验完成后，至少应包含以下产物：

1. `outputs/benchmark_ablation/<variant>/run_xx_seedyy/metrics.json`
2. `outputs/benchmark_ablation/<variant>/run_xx_seedyy/kan_stage_logs.csv`
3. `outputs/benchmark_ablation/<variant>/run_xx_seedyy/symbolize_trace.csv`
4. `outputs/benchmark_ablation/ablation_runs_raw.csv`
5. `outputs/benchmark_ablation/ablation_runs_summary.csv`
6. `docs/ablation_report.md`
7. `outputs/benchmark_ablation/layerwiseft_analysis/`

上述产物齐备后，实验结果方可视为可复审、可复现。
