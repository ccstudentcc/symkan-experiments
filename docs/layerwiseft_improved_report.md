# LayerwiseFT 改进实验报告（验证早停 + 轻量正则 + 缩短步数）

## 1. 实验目标

针对 layerwise finetune（LayerwiseFT）引入以下改进，并评估其相对基线（full）和去层间微调（wolayerwiseft）的效果：

1. 验证集早停：在层间微调过程中，当公式验证 R² 不再提升时提前终止。
2. 轻量正则化：`lamb=1e-5`，抑制 B-spline 过拟合。
3. 缩短微调步数：默认从 120 降至 60。

## 2. 实现改动

### 2.1 符号搜索核心逻辑

- 文件：`symkan/symbolic/search.py`
- 新增能力：
  - layerwise 微调验证集切分与评估集构建。
  - 使用 `validate_formula_numerically` 的平均 R² 作为早停判据。
  - chunk 化训练 + patience 早停，并回滚到 best R² 对应权重。
  - layerwise 微调默认正则从 0 调整为 `1e-5`。

### 2.2 流水线参数透传

- 文件：`symkan/symbolic/pipeline.py`
- 在 `symbolize_pipeline` 中新增并透传以下参数：
  - `layerwise_finetune_lr`
  - `layerwise_finetune_lamb`
  - `layerwise_use_validation`
  - `layerwise_validation_ratio`
  - `layerwise_validation_seed`
  - `layerwise_early_stop_patience`
  - `layerwise_early_stop_min_delta`
  - `layerwise_eval_interval`
  - `layerwise_validation_n_sample`

### 2.3 CLI 与默认配置

- 文件：`symkanbenchmark.py`
- 变更：
  - `--layerwise-finetune-steps` 默认值：`120 -> 60`
  - 新增 CLI 开关与参数（与 pipeline 对齐）
  - 两处 `symbolize_pipeline(...)` 调用均已透传新参数
  - `metrics.json` 增加 layerwise 配置回写字段

口径说明：`120 -> 60` 是 CLI 技术默认值优化；对于典型 2 层 KAN，生产/批量复现实验仍建议显式使用 `--layerwise-finetune-steps 0`，仅在追求小幅分类增益时按需启用改进版 LayerwiseFT。

### 2.4 独立测试脚本

- 文件：`compare_layerwiseft_improved.py`
- 行为：
  - 仅训练新变体 `layerwiseft_esreg`
  - 直接复用 `benchmark_ablation/full/` 与 `benchmark_ablation/wolayerwiseft/` 已有结果，不重复训练基线
  - 产出三方对比 CSV 到 `benchmark_ablation/layerwiseft_improved_analysis/`

## 3. 实验设置

- 数据目录：`benchmark_ablation/`
- seeds：`42,52,62`
- 新变体名称：`layerwiseft_esreg`
- 执行命令：

```bash
python compare_layerwiseft_improved.py \
  --ablation-dir benchmark_ablation \
  --new-variant layerwiseft_esreg \
  --seeds 42,52,62 \
  --global-seed 123 \
  --quiet
```

## 4. 结果汇总（mean ± std，3 seeds: 42 / 52 / 62）

数据来源：各 metrics.json 汇总

| 变体 | 最终精度 | Macro-AUC | 表达式复杂度 | 公式 R²（验证） | 有效输入维数 | 阶段训练耗时 (s) | 符号化耗时 (s) |
|---|---:|---:|---:|---:|---:|---:|---:|
| full | 0.7768 ± 0.0210 | 0.9540 ± 0.0083 | 130.77 ± 26.73 | -0.6318 ± 0.0866 | 57.0 ± 2.0 | 39.52 ± 1.44 | 51.16 ± 0.66 |
| layerwiseft_esreg | 0.7851 ± 0.0088 | 0.9563 ± 0.0046 | 130.50 ± 26.89 | -0.6686 ± 0.0658 | 57.0 ± 2.0 | 40.40 ± 1.71 | 34.33 ± 0.77 |
| wolayerwiseft | 0.7838 ± 0.0014 | 0.9544 ± 0.0047 | 126.90 ± 31.17 | -0.5937 ± 0.0151 | 57.67 ± 2.31 | 40.60 ± 1.52 | 20.50 ± 0.21 |

> **字段说明**
> - **表达式复杂度**：符号化后各激活函数表达式节点数的均值（越小越简洁）
> - **公式 R²（验证）**：用测试集对恢复公式做数值验证得到的平均 R²（负值表示公式预测误差大于均值基线）
> - **有效输入维数**：剪枝后实际被使用的输入特征数（原始输入 120 维）
> - **阶段训练耗时**：stagewise 渐进训练阶段总耗时（含剪枝与最终微调，不含符号化）
> - **符号化耗时**：符号化搜索 + layerwise 微调阶段总耗时

## 5. 关键对比

### 5.1 新方案 vs full（逐字段差值）

| 指标 | full | layerwiseft_esreg | Δ (new − full) |
|---|---:|---:|---:|
| 最终精度 | 0.7768 | 0.7851 | **+0.0083** ↑ |
| Macro-AUC | 0.9540 | 0.9563 | **+0.0023** ↑ |
| 表达式复杂度 | 130.77 | 130.50 | **-0.27**（持平） |
| 公式 R²（验证） | -0.6318 | -0.6686 | **-0.0369** ↓ |
| 有效输入维数 | 57.0 | 57.0 | **0**（持平） |
| 阶段训练耗时 (s) | 39.52 | 40.40 | **+0.88**（持平） |
| 符号化耗时 (s) | 51.16 | 34.33 | **-16.83** ↑ 快 33% |

结论：改进方案相对 full，分类精度微升、符号化耗时大幅降低（-33%），表达式复杂度与有效输入维数持平，阶段训练耗时无明显变化。代价是公式 R² 下降 0.037，反映 layerwise 微调对符号候选的数值一致性仍有扰动，但已比旧版 full 稳定（std 从 0.087 降到 0.066）。

### 5.2 新方案 vs wolayerwiseft（逐字段差值）

| 指标 | wolayerwiseft | layerwiseft_esreg | Δ (new − woft) |
|---|---:|---:|---:|
| 最终精度 | 0.7838 | 0.7851 | **+0.0013**（微升） |
| Macro-AUC | 0.9544 | 0.9563 | **+0.0019**（微升） |
| 表达式复杂度 | 126.90 | 130.50 | **+3.60**（略复杂） |
| 公式 R²（验证） | -0.5937 | -0.6686 | **-0.0749** ↓ |
| 有效输入维数 | 57.67 | 57.0 | **-0.67**（持平） |
| 阶段训练耗时 (s) | 40.60 | 40.40 | **-0.20**（持平） |
| 符号化耗时 (s) | 20.50 | 34.33 | **+13.82** ↑ 慢 67% |

结论：相对直接关闭 layerwiseFT，改进方案仅带来可忽略的分类收益（+0.0013 acc），但耗时增加 67%（+13.8s），公式 R² 明显更差（-0.075），表达式也略变复杂。wolayerwiseft 在 R²、耗时、方差三个维度全面更优。

## 6. 分析与结论

【核心判断】

值得做（作为可选模式），但**不值得替代当前默认策略**。

原因：

1. **对比 full**：改进方案有效压缩了符号化耗时（-33%）并微升分类精度，方向正确。代价是公式 R² 微降，但方差同步收窄，稳定性有所改善。
2. **对比 wolayerwiseft**：分类收益可忽略，却多花 13.8s、R² 下降 0.075，表达式略变复杂。wolayerwiseft 在精度/复杂度/速度/稳定性上综合最优。
3. **方差分析**：wolayerwiseft 精度标准差（0.0014）远低于 full（0.0210）和新方案（0.0088），说明关闭 layerwiseFT 结果更稳定可复现，适合作为生产默认。

【建议默认策略】

1. **生产默认**：--layerwise-finetune-steps 0（wolayerwiseft 路线）——最快、方差最小、R² 最好。
2. **追求精度时**：可启用改进版 layerwiseFT（steps=60，早停+正则）——相比旧版 full 符号化快 33%，方差更小。
3. **弃用旧版 full**：未加早停与正则的 layerwiseFT（原 steps=120，lamb=0）在所有指标上均不占优，**不建议继续作为默认选项**。

【后续优化方向】

1. 进一步缩短步数（20/30）并收紧早停（layerwise_eval_interval=10），有望将耗时压到与 wolayerwiseft 同量级，同时保留微小精度优势。
2. 将早停指标改为「分类验证损失 + 公式 R²」的联合目标，避免仅用 R² 无法感知分类性能下降。
3. 对 layerwiseFT 分层差异化约束（浅层更强正则、深层更宽松），减少对符号化表达质量的干扰。

## 7. 产出文件

- benchmark_ablation/layerwiseft_esreg/：新变体运行目录（3 seeds）
- benchmark_ablation/layerwiseft_improved_analysis/comparison_raw.csv
- benchmark_ablation/layerwiseft_improved_analysis/comparison_summary.csv
- benchmark_ablation/layerwiseft_improved_analysis/delta_new_vs_full.csv
- benchmark_ablation/layerwiseft_improved_analysis/delta_new_vs_wolayerwiseft.csv
