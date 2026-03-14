# symkan 单点消融实验计划（Ablation Plan）

## 1. 实验目标与核心问题

目标：围绕 symkan 的两段式架构（训练与准备、符号化流水线）做单点消融，回答每个设计是否真的带来可观测收益，而不是“看起来合理”。

核心问题：

1. 分阶段训练是否能提供更优的 KAN 快照，从而提升后续符号化质量？
2. 渐进剪枝、输入压缩、层间微调三项机制各自贡献了什么？
3. 这些机制的收益是精度收益、可解释性收益，还是稳定性/时间收益？

---

## 2. 实验约定（必须固定）

### 2.1 数据与随机性约定

1. 数据集来源与切分：沿用当前 `symkanbenchmark.py` 的默认数据输入逻辑（`X_train.npy/X_test.npy/Y_train_cat.npy/Y_test_cat.npy`）。
2. 全局随机数固定：`--global-seed 123`。
3. 基线/对照随机数：`--stagewise-seeds 42,52,62`（三次重复）。
4. 结果统计口径：所有核心指标统一报告 `mean ± std`（n=3）。

### 2.2 训练与符号化公平性约定

1. 网络结构固定：`inner_dim=16, grid=5, k=3`。
2. 函数库固定：`lib-preset=layered`。
3. 符号化目标固定：`symbolic_target_edges=90`。
4. 除被消融模块外，其余参数与 baseline 完全一致。
5. 每个变体必须输出完整中间文件，不允许只保留最终精度。

### 2.3 环境与执行约定

1. 统一 Python 环境（建议使用项目既有环境）。
2. 同一硬件条件运行全部变体（尤其 GPU/CPU 不混跑）。
3. 每个变体单独 output-dir，避免覆盖。

---

## 3. 基线定义（Full Pipeline）

基线严格参照 `symkanbenchmark.py` 的 full 流程与三随机数设置。

建议命令：

```bash
python symkanbenchmark.py \
  --tasks full \
  --stagewise-seeds 42,52,62 \
  --global-seed 123 \
  --output-dir benchmark_ablation/full \
  --quiet
```

基线流程包括：

1. baseline KAN 训练 + 归因选特征。
2. stagewise_train 分阶段训练/剪枝/选模。
3. symbolize_pipeline 渐进剪枝 + 输入压缩 + 逐层符号化 + 层间微调 + affine-heavy 微调。

---

## 4. 单点消融设计

## 4.1 训练与准备阶段消融

### A1: w/o Stagewise Train

定义：将 `stagewise_train` 替换为端到端一次性训练（同等总训练预算），其余流程不变。

控制原则：

1. 保持数据构建、特征筛选、symbolize_pipeline 完全一致。
2. 训练预算对齐：`--e2e-steps` 自动继承 `stage_lr_schedule` 长度乘以 `steps_per_stage`，学习率与正则系数取调度中位值。
3. **关键附加开关**：必须同时指定 `--prune-collapse-floor 0.0`，否则渐进剪枝检测到精度从稠密入口崩塌时会回滚至原始边数（~2080），导致符号化在稠密图上卡死。`--symbolic-prune-adaptive-acc-drop-tol 0.7` 同步放宽，容许更大的精度下降而不中止剪枝。
4. 问题导向：是否因为缺少中间快照选择与逐步稀疏化，导致符号化入口模型质量变差。

实际 CLI（`ablation_runner.py` 内已固化）：

```bash
python symkanbenchmark.py --tasks full \
  --disable-stagewise-train \
  --prune-collapse-floor 0.0 \
  --symbolic-prune-adaptive-acc-drop-tol 0.7
```

## 4.2 符号化流水线阶段消融

### B1: w/o Progressive Pruning

定义：关闭符号化阶段的渐进剪枝。

实现建议：

1. `max_prune_rounds=0`（或等价开关）。
2. 其余符号化步骤保持不变。

要回答的问题：剪枝是否是表达式可读性与最终稳定性的必要前提。

### B2: w/o Input Compaction

定义：关闭输入压缩步骤，直接在原输入维度执行符号化。

实现建议：

1. 已提供开关：`symbolize_pipeline(enable_input_compaction=...)`。
2. CLI 可直接关闭：`--no-input-compaction`。

要回答的问题：输入压缩是“真贡献”还是仅仅工程加速。

### B3: w/o Layerwise Finetune

定义：取消逐层符号化后的层间微调，直接完成所有层符号拟合后再做统一微调。

实现建议：

1. `layerwise_finetune_steps=0`。
2. 保留 `affine_finetune_steps`，避免把“无层间微调”变成“完全无微调”。

要回答的问题：层间微调对最终精度、AUC、公式稳定性是否关键。

---

## 5. 实验矩阵总览

| variant_id | 变体名 | Stagewise | Progressive Pruning | Input Compaction | Layerwise FT | 备注 |
| --- | --- | --- | --- | --- | --- | --- |
| V0 | Full Pipeline | on | on | on | on | 基线 |
| V1 | w/o Stagewise Train | off | on | on | on | 须同时加 `--prune-collapse-floor 0.0` |
| V2 | w/o Progressive Pruning | on | off | on | on | `--max-prune-rounds 0` |
| V3 | w/o Input Compaction | on | on | off | on | `--no-input-compaction` |
| V4 | w/o Layerwise Finetune | on | on | on | off | `--layerwise-finetune-steps 0` |

运行矩阵：`5 variants × 3 seeds = 15 runs`。

---

## 6. 结果记录字段（必须包含）

下面字段是本次结论可成立的最小集合：

| 字段名 | 说明 | 来源 |
| --- | --- | --- |
| variant_id | 变体编号 V0~V4 | 运行配置 |
| seed | 随机种子（42/52/62） | CLI |
| effective_target_edges | 符号化有效目标边数 | metrics / symbolize result |
| effective_input_dim | 符号化有效输入维度 | metrics / symbolize result |
| final_acc | 符号化后精度 | metrics |
| expr_complexity_mean | 表达式平均复杂度 | `kan_symbolic_summary.csv` 中 complexity 均值 |
| macro_auc | 多分类宏平均 AUC | metrics |
| validation_mean_r2 | 公式数值验证平均 R² | metrics |
| symbolic_total_seconds | 符号化总耗时 | metrics |
| stage_total_seconds | 训练准备总耗时 | 建议新增计时字段 |
| stage_i_seconds | 各阶段训练耗时 | 建议在 stage logs 扩展字段 |
| rounds | 剪枝轮数 | `symbolize_trace.csv` |
| edges_drop_total | 总剪枝边数 | trace 聚合 |

说明：

1. 你明确要求“各阶段训练时间”，当前已在 `kan_stage_logs.csv` 增加 `train_seconds/prune_seconds/stage_seconds`。
2. `expr_complexity_mean` 建议对有效表达式计算均值，并同时记录有效表达式数量。

---

## 7. 结果表模板

## 7.1 明细表（每次运行一行）

```csv
variant_id,seed,effective_target_edges,effective_input_dim,final_acc,expr_complexity_mean,macro_auc,validation_mean_r2,symbolic_total_seconds,stage_total_seconds,rounds,edges_drop_total
V0,42,90,59,0.7771,120.0,0.9558,-0.599,51.9,38.2,7,26
```

> 注：`validation_mean_r2` 在当前实验中普遍为负值，反映符号化公式对测试集的数值拟合仍有差距，与分类 AUC 指标不构成矛盾。

## 7.2 汇总表（mean ± std）

| variant_id | final_acc | expr_complexity_mean | macro_auc | validation_mean_r2 | symbolic_total_seconds | stage_total_seconds |
| --- | --- | --- | --- | --- | --- | --- |
| V0 | 0.777 ± 0.021 | 130.8 ± 26.7 | 0.954 ± 0.008 | −0.632 ± 0.087 | 51.2 ± 0.7 | 39.5 ± 1.4 |
| V1 | 0.442 ± 0.020 | 48.2 ± 16.4 | 0.835 ± 0.011 | −0.813 ± 0.155 | 26.3 ± 3.6 | 13.7 ± 0.1 |
| V2 | 0.775 ± 0.034 | 217.1 ± 38.4 | 0.959 ± 0.007 | −0.475 ± 0.030 | 67.8 ± 10.2 | 39.9 ± 1.6 |
| V3 | 0.769 ± 0.023 | 117.0 ± 22.1 | 0.953 ± 0.005 | +0.096 ± 0.141 | 77.2 ± 0.7 | 39.8 ± 1.7 |
| V4 | 0.784 ± 0.001 | 126.9 ± 31.2 | 0.954 ± 0.005 | −0.594 ± 0.015 | 20.5 ± 0.2 | 40.6 ± 1.5 |

---

## 8. 结论分析框架（统一口径）

每个变体统一按以下顺序分析，避免“只看一个分数”：

1. 精度影响：`Δ final_acc`、`Δ macro_auc` 相对 V0。
2. 可解释性影响：`Δ expr_complexity_mean` 与有效表达式数量变化。
3. 公式可信度：`Δ validation_mean_r2` 与负 R² 比例。
4. 稀疏结构影响：`effective_target_edges/effective_input_dim/rounds` 的变化。
5. 成本影响：`stage_total_seconds` 与 `symbolic_total_seconds` 的变化。
6. 稳定性：3 seed 下标准差是否显著放大。

建议结论模板：

1. 是否值得保留该模块（是/否）。
2. 主要收益维度（精度/稳定性/复杂度/时间）。
3. 主要代价维度。
4. 适用条件（何时值得开、何时可关）。

---

## 9. 消融脚本工程化设计框架

目标：在不破坏现有 `symkanbenchmark.py` 用法的前提下，新增可复用的消融入口。

### 9.1 设计原则

1. 单一入口：新增 `ablation_runner.py`（调用现有函数，避免复制主逻辑）。
2. 配置驱动：每个变体由配置字典描述，不写 if-else 地狱。
3. 全量留痕：每次 run 输出 metrics + trace + stage logs + summary。
4. 向后兼容：保留 `symkanbenchmark.py` 原有参数行为。

### 9.2 实际实现方案

最终采用单文件实现：`ablation_runner.py`，无需额外子模块。

文件职责：
1. `VARIANT_SPECS` 字典（文件顶部）：定义每个变体的 `extra_args`，无 if-else。
2. `run_variant()`：调用 `symkanbenchmark.py` 子进程，透传 common_args + variant extra_args。
3. `collect_variant_results()`：读取 `symkanbenchmark_runs.csv`，合并变体标签。
4. `summarize_results()`：跨 seed 计算 mean ± std，输出汇总表。
5. `--aggregate-only` 标志：跳过运行，直接从已有目录聚合结果，支持分批运行后统一汇总。

### 9.3 实际 CLI 接口

**单次全量运行（5 变体 × 3 seed = 15 runs）：**
```bash
python ablation_runner.py \
  --variants full,wostagewise,wopruning,wocompact,wolayerwiseft \
  --stagewise-seeds 42,52,62 \
  --global-seed 123 \
  --output-dir benchmark_ablation
```

**分批运行后汇总（各变体独立时间窗口）：**
```bash
# 分批运行每个变体
python ablation_runner.py --variants wostagewise --output-dir benchmark_ablation
# ...其余变体同理

# 全部完成后汇总
python ablation_runner.py --aggregate-only --output-dir benchmark_ablation
```

### 9.4 已完成的代码改造清单

1. **`symkan/symbolic/pipeline.py`**
   - 新增 `enable_input_compaction` 参数（默认 True）→ 控制输入压缩开关（V3）
   - 新增 `prune_collapse_floor` 参数（默认 0.6）→ 剪枝精度崩塌保护阈值；设为 0.0 可完全关闭，供 V1（稠密入口）使用

2. **`symkan/tuning/stagewise.py`**
   - 新增每阶段计时，写入 `kan_stage_logs.csv`：`train_seconds / prune_seconds / stage_seconds`
   - 新增汇总字段：`stage_total_seconds / stage_train_total_seconds / stage_prune_total_seconds / final_finetune_seconds`

3. **`symkanbenchmark.py`**
   - 新增 `--disable-stagewise-train`：替换为端到端训练（V1）
   - 新增 `--no-input-compaction`：关闭输入压缩（V3）
   - 新增 `--layerwise-finetune-steps`：层间微调步数，设 0 为关闭（V4）
   - 新增 `--max-prune-rounds`：最大剪枝轮数，设 0 为关闭（V2）
   - 新增 `--prune-collapse-floor`：透传到 `symbolize_pipeline`
   - 新增 `--e2e-steps / --e2e-lr / --e2e-lamb`：控制端到端训练超参（V1）
   - `metrics.json` 新增字段：`pre_symbolic_n_edge`（进入符号化前的边数）、`pre_symbolic_too_dense`（超过 `stage_target_edges × 2` 时为 True，标记稠密入口）

4. **`ablation_runner.py`**（新建）
   - 单文件消融编排器，见 §9.2

---

## 10. 风险与防偏差检查

1. 不允许跨变体改动超参（除消融目标）。
2. 不允许省略失败 run（必须记录失败原因）。
3. 统计报告必须同时给出均值和标准差，避免单次 cherry-pick。
4. 对 `w/o Stagewise Train` 需明确训练预算对齐公式，避免因预算不公平导致伪结论。

---

## 11. 交付物清单

1. `benchmark_ablation/<variant>/run_xx_seedyy/metrics.json`（含 `pre_symbolic_n_edge`、`pre_symbolic_too_dense` 等新字段）
2. `benchmark_ablation/<variant>/run_xx_seedyy/kan_stage_logs.csv`（含 `train_seconds / prune_seconds / stage_seconds` 每阶段计时）
3. `benchmark_ablation/<variant>/run_xx_seedyy/symbolize_trace.csv`
4. `benchmark_ablation/ablation_runs_raw.csv`
5. `benchmark_ablation/ablation_runs_summary.csv`
6. `docs/ablation_report.md`（消融实验分析报告）
7. `benchmark_ablation/layerwiseft_analysis/`（层间微调专项对毕，由 `analyze_layerwiseft.py` 生成）

以上 7 项齐备后，才能认为消融实验可复审、可复现实证结论。
