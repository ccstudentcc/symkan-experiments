# symkanbenchmark.py 使用说明

## 文档导航

- 返回总览：[README](../README.md)
- docs 总入口：[index](index.md)
- 项目地图：[project_map](project_map.md)
- 总体使用文档：[symkan_usage](symkan_usage.md)
- 设计与兼容策略：[design](design.md)
- 参数解释（notebook 侧）：[kan_parameters](kan_parameters.md)
- 消融实验说明：[ablation_usage](ablation_usage.md)

## 目录

- [1. 运行入口](#1-运行入口)
- [2. 任务与命令速查](#2-任务与命令速查)
- [3. 输出目录与文件含义](#3-输出目录与文件含义)
- [4. 参数速查](#4-参数速查)
- [5. 结果解读最小集合](#5-结果解读最小集合)
- [6. Adaptive A/B 实验（baseline / adaptive / adaptive_auto）](#6-adaptive-ab-实验baseline--adaptive--adaptive_auto)
- [7. 报告口径](#7-报告口径)
- [8. 与总文档统一口径（2026-03）](#8-与总文档统一口径2026-03)

[symkanbenchmark.py](../symkanbenchmark.py) 将 `kan.ipynb` 中的主实验流程及两个 benchmark 流程脚本化，其主要目的包括：

1. 支持同一参数集的批量多 seed 运行。
2. 稳定导出结构化 CSV 结果。
3. 避免 notebook 手工执行带来的覆盖和漏记。

## 1. 运行入口

### 1.1 完整流程

```bash
python symkanbenchmark.py --tasks all --verbose
```

其中，`all = full + eval-bench + parallel-bench`。

脚本默认优先读取 `X_train.npy/X_test.npy/Y_train_cat.npy/Y_test_cat.npy`。若文件缺失，脚本会自动获取 MNIST 并生成对应文件，优先使用 `tensorflow.keras.datasets.mnist`，失败时回退至 `sklearn.fetch_openml`。

### 1.2 主实验

```bash
python symkanbenchmark.py --tasks full
```

静默模式：

```bash
python symkanbenchmark.py --tasks full --quiet
```

`--quiet` 用于抑制训练与符号化过程输出；若与 `--verbose` 同时设置，则 `--quiet` 优先。

### 1.3 多 seed 运行

```bash
python symkanbenchmark.py --tasks all --stagewise-seeds 42,52,62
```

## 2. 任务与命令速查

- 主实验：

```bash
python symkanbenchmark.py --tasks full
```

- 评估链路 benchmark（仍会先构造主流程上下文）：

```bash
python symkanbenchmark.py --tasks eval-bench
```

- 并行策略 benchmark：

```bash
python symkanbenchmark.py --tasks parallel-bench --parallel-modes auto,off,thread4,thread8
```

- 组合任务：

```bash
python symkanbenchmark.py --tasks full,parallel-bench
```

## 3. 输出目录与文件含义

默认输出目录为 `benchmark_runs/`。每个 seed 对应一个独立的 run 子目录，以避免结果覆盖：

```text
benchmark_runs/
  symkanbenchmark_runs.csv
  symkanbenchmark_eval_runs.csv
  symkanbenchmark_parallel_runs.csv
  run_01_seed42/
    kan_stage_logs.csv
    kan_symbolic_summary.csv
    formula_validation.csv
    roc_auc_summary.csv
    symbolize_trace.csv
    metrics.json
    benchmark_single_round.csv
    benchmark_multi_round_raw.csv
    benchmark_multi_round_summary_cn.csv
    benchmark_multi_round_summary_en.csv
    benchmark_symbolic_parallel_quick.csv
```

主要结果文件包括：

1. `symkanbenchmark_runs.csv`：多 seed/多配置横向对比主表。
2. `kan_stage_logs.csv`：阶段训练是否频繁回滚。
3. `symbolize_trace.csv`：剪枝节奏是否过猛。
4. `formula_validation.csv`：R² 与数值稳定性。
5. `benchmark_symbolic_parallel_quick.csv`：并行加速是否真实有效。

## 4. 参数速查

### 4.1 主实验参数默认值（CLI 实际默认）

- `--inner-dim 16`：隐藏层宽度（主干表达能力与训练成本的平衡点）。
- `--top-k 120`：归因后保留的输入特征数（越大保留信息越多，搜索也更慢）。
- `--stage-target-edges 120`：stagewise 阶段期望保留的边数目标。
- `--symbolic-target-edges 90`：symbolize 后期望收敛到的边数目标（控制最终复杂度）。
- `--steps-per-stage 60`：每个 stage 的训练步数。
- `--finetune-steps 50`：阶段内常规微调步数。
- `--layerwise-finetune-steps 60`：逐层微调步数（改进版默认，含早停与轻正则参数）。
- `--affine-finetune-steps 200`：仿射参数微调步数（提高最后拟合质量）。

口径说明如下：

1. 上述是 CLI 技术默认值，用于“不开任何额外开关即可运行”。
2. 对典型 2 层 KAN（`[in, hidden, class]`），项目层设定通常显式传入 `--layerwise-finetune-steps 0`，并将 LayerwiseFT 视为按需开关。
3. 如果确实启用 LayerwiseFT，优先使用当前改进版参数（steps=60 + validation early-stop + `lamb=1e-5`），不要回退到旧版长步数无约束微调。

逐层符号化属于有损替换；`fix_symbolic` 选定函数族后无法回退。在 2 层 KAN 中，LayerwiseFT 仅有一次层间补偿窗口，因此其改进版更接近风险控制选项，而非默认增益模块。

### 4.2 常用控制参数

- `--tasks full`：只跑主实验链路。
- `--tasks eval-bench`：只跑评估性能专题（会复用主流程上下文）。
- `--tasks parallel-bench`：只跑并行策略对照。
- `--tasks all`：一次跑完 full + eval-bench + parallel-bench。
- `--stagewise-seeds 42,52,62`：指定一组 stagewise 随机种子并逐个运行。
- `--output-dir benchmark_runs_alt`：指定输出根目录，避免和已有实验互相覆盖。
- `--verbose`：打印过程日志，便于观察训练与剪枝过程。
- `--quiet`：静默运行，只保留必要结果输出。
- `--auto-fetch-mnist/--no-auto-fetch-mnist`：是否在 `*.npy` 缺失时自动获取并生成 MNIST 数据文件（默认开启）。
- `--mnist-classes 0,1,2,3,4,5,6,7,8,9`：自动获取 MNIST 时保留的类别集合。

### 4.3 函数库预设

- `--lib-preset layered`：分层函数库，精度与复杂度较均衡。
- `--lib-preset fast`：精简函数库，优先降低搜索成本与运行时间。
- `--lib-preset expressive`：增强表达能力，可在分层库不足时试验。
- `--lib-preset full`：完整函数库，搜索空间最大，通常最慢但最灵活。

### 4.4 评估 benchmark 参数

- `--bench-repeat 3`：每项 benchmark 的正式重复次数（用于统计均值/方差）。
- `--bench-warmup 1`：预热轮数（减少首次执行的冷启动偏差）。
- `--eval-rounds 3`：评估回合数（跨回合汇总稳定性）。
- `--validate-n-sample 500`：验证抽样规模（越大越稳，耗时也更高）。

### 4.5 并行 benchmark 参数

- `--parallel-modes auto,off,thread4`：并行策略候选集合（用于横向测速）。
- `--parallel-target-min 40`：并行实验中的最小目标边数。
- `--parallel-target-max 80`：并行实验中的最大目标边数。
- `--parallel-max-prune-rounds 8`：并行实验允许的最大剪枝轮数。
- `--parallel-finetune-steps 20`：并行实验常规微调步数。
- `--parallel-layerwise-finetune-steps 20`：并行实验逐层微调步数。
- `--parallel-affine-finetune-steps 0`：并行实验仿射微调步数（0 代表跳过）。

## 5. 结果解读最小集合

结果解读时可优先关注 `symkanbenchmark_runs.csv` 中以下字段：

- `base_acc`
- `enhanced_acc`
- `final_acc`
- `final_n_edge`
- `effective_target_edges`
- `effective_input_dim`
- `macro_auc`
- `validation_mean_r2`
- `symbolic_total_seconds`

若用于论文写作，不宜依据单次运行结果下结论，至少应在 3 个 seeds 上统计：

1. `symkanbenchmark_runs.csv` 的均值与方差。
2. `benchmark_multi_round_summary_cn.csv` 的速度均值与标准差。
3. `benchmark_symbolic_parallel_quick.csv` 的 `vs_off_speedup_x`。

---

## 6. Adaptive A/B 实验（baseline / adaptive / adaptive_auto）

三组定义：

1. `baseline`：不启用 adaptive。
2. `adaptive`：启用验证反馈 + 自适应阈值 + 自适应 lamb/ft。
3. `adaptive_auto`：在 adaptive 上增加阶段早停与 symbolize 自适应剪枝节奏。

### 6.1 命令模板

公共参数：

```bash
python symkanbenchmark.py \
  --tasks full \
  --stagewise-seeds 42,52,62 \
  --global-seed 123 \
  --output-dir <OUT_DIR> \
  <EXTRA_FLAGS> \
  --quiet
```

实例：

```bash
# baseline
python symkanbenchmark.py --tasks full --stagewise-seeds 42,52,62 --global-seed 123 --output-dir benchmark_ab/baseline --quiet

# adaptive
python symkanbenchmark.py --tasks full --stagewise-seeds 42,52,62 --global-seed 123 --output-dir benchmark_ab/adaptive --use-validation --validation-ratio 0.15 --adaptive-threshold --adaptive-lamb --adaptive-ft --quiet

# adaptive_auto
python symkanbenchmark.py --tasks full --stagewise-seeds 42,52,62 --global-seed 123 --output-dir benchmark_ab/adaptive_auto --use-validation --validation-ratio 0.15 --adaptive-threshold --adaptive-lamb --adaptive-ft --stage-early-stop --stage-early-stop-patience 2 --stage-early-stop-min-acc-gain 0.002 --stage-early-stop-edge-buffer 5 --symbolic-prune-threshold-start 0.010 --symbolic-prune-threshold-end 0.030 --symbolic-prune-max-drop-ratio 0.25 --symbolic-prune-threshold-backoff 0.65 --symbolic-prune-adaptive-threshold --symbolic-prune-adaptive-acc-drop-tol 0.025 --symbolic-prune-adaptive-min-edges-gain 2 --symbolic-prune-adaptive-low-gain-patience 6 --quiet
```

### 6.2 新增参数分组

stagewise 相关：

- `--stage-early-stop`：开启 stagewise 早停。
- `--stage-early-stop-patience`：早停耐心轮数（连续多少轮无改进后停止）。
- `--stage-early-stop-min-acc-gain`：判定“有效改进”的最小精度提升阈值。
- `--stage-early-stop-edge-buffer`：边数缓冲区（避免过早因边数抖动触发早停）。

symbolize 相关：

- `--symbolic-prune-threshold-start`：初始剪枝阈值。
- `--symbolic-prune-threshold-end`：目标/上限剪枝阈值。
- `--symbolic-prune-max-drop-ratio`：单轮允许的最大性能下降比例。
- `--symbolic-prune-threshold-backoff`：触发回退时的阈值收缩系数。
- `--symbolic-prune-adaptive-threshold`：开启自适应阈值调节。
- `--symbolic-prune-adaptive-step`：每轮阈值调节步长。
- `--symbolic-prune-adaptive-acc-drop-tol`：可容忍的精度下降阈值。
- `--symbolic-prune-adaptive-min-edges-gain`：每轮至少要减少的边数下限。
- `--symbolic-prune-adaptive-low-gain-patience`：连续低收益轮数容忍度，超过后调整策略。

当前默认启用 `symbolic-prune-adaptive-threshold`；如需禁用，应显式传入 `--no-symbolic-prune-adaptive-threshold`。

### 6.3 结果自动汇总

结果汇总可使用 [benchmark_ab_compare.py](../benchmark_ab_compare.py)：

```bash
python benchmark_ab_compare.py --root benchmark_ab --baseline baseline --variants adaptive,adaptive_auto --output benchmark_ab/comparison
```

输出：

- [benchmark_ab/comparison/variant_summary.csv](../benchmark_ab/comparison/variant_summary.csv)
- [benchmark_ab/comparison/pairwise_delta_summary.csv](../benchmark_ab/comparison/pairwise_delta_summary.csv)
- [benchmark_ab/comparison/seedwise_delta.csv](../benchmark_ab/comparison/seedwise_delta.csv)
- [benchmark_ab/comparison/trace_seedwise.csv](../benchmark_ab/comparison/trace_seedwise.csv)
- [benchmark_ab/comparison/trace_summary.csv](../benchmark_ab/comparison/trace_summary.csv)

### 6.4 当前统计结果（seed: 42/52/62）

基于 [benchmark_ab/comparison/variant_summary.csv](../benchmark_ab/comparison/variant_summary.csv)、[benchmark_ab/comparison/pairwise_delta_summary.csv](../benchmark_ab/comparison/pairwise_delta_summary.csv) 与 [benchmark_ab/comparison/trace_summary.csv](../benchmark_ab/comparison/trace_summary.csv)，可优先报告以下三张表。

#### 表 1：核心指标汇总（mean ± std）

| 变体 | final_acc | macro_auc | validation_mean_r2 | symbolic_total_seconds | export_wall_time_s | final_n_edge |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| baseline | 0.7807 ± 0.0010 | 0.9548 ± 0.0023 | -0.6135 ± 0.0271 | 33.27 ± 0.37 | 73.17 ± 2.06 | 89.67 ± 0.47 |
| adaptive | 0.7678 ± 0.0117 | 0.9486 ± 0.0021 | -0.5361 ± 0.1061 | 31.05 ± 0.98 | 75.72 ± 12.88 | 85.33 ± 2.49 |
| adaptive_auto | 0.7491 ± 0.0186 | 0.9430 ± 0.0044 | -0.6137 ± 0.0306 | 30.88 ± 1.76 | 72.58 ± 14.62 | 85.33 ± 5.25 |

结果解释：

1. 分类指标上，baseline 仍是当前最优（`final_acc` 与 `macro_auc` 均最高，且 `final_acc` 方差最小）。
2. adaptive 系列在 `symbolic_total_seconds` 上更快（约快 2.2s~2.4s），但分类指标同步下降。
3. `final_n_edge` 在 adaptive 系列下降（约 -4.33），说明确实更激进地压缩了结构。

#### 表 2：相对 baseline 的 pairwise 差分

| 比较 | 指标 | mean_delta (variant-baseline) | median_delta | win/lose/tie |
| --- | --- | ---: | ---: | ---: |
| adaptive vs baseline | final_acc | -0.0130 | -0.0160 | 1 / 2 / 0 |
| adaptive_auto vs baseline | final_acc | -0.0316 | -0.0370 | 0 / 3 / 0 |
| adaptive vs baseline | macro_auc | -0.0063 | -0.0051 | 0 / 3 / 0 |
| adaptive_auto vs baseline | macro_auc | -0.0118 | -0.0149 | 0 / 3 / 0 |
| adaptive vs baseline | validation_mean_r2 | +0.0774 | +0.0640 | 2 / 1 / 0 |
| adaptive_auto vs baseline | validation_mean_r2 | -0.0002 | +0.0279 | 2 / 1 / 0 |
| adaptive vs baseline | symbolic_total_seconds | -2.2148 | -1.7458 | 3 / 0 / 0 |
| adaptive_auto vs baseline | symbolic_total_seconds | -2.3840 | -2.4327 | 2 / 1 / 0 |
| adaptive vs baseline | export_wall_time_s | +2.5513 | +9.5640 | 1 / 2 / 0 |
| adaptive_auto vs baseline | export_wall_time_s | -0.5918 | -6.9048 | 2 / 1 / 0 |

结果解释：

1. 精度主指标（`final_acc` / `macro_auc`）上，adaptive 系列未形成对 baseline 的稳定优势。
2. `validation_mean_r2` 的方向更复杂：adaptive 有改善趋势，但 adaptive_auto 的均值几乎为 0、对 seed 更敏感。
3. `symbolic_total_seconds` 的加速较稳定；`export_wall_time_s` 则受端到端波动影响较大，不宜只看均值。

#### 表 3：symbolize 节奏（trace）

| 变体 | rounds_mean | effective_rounds_mean | total_edges_removed_mean | mean_drop_ratio_mean | max_drop_ratio_mean |
| --- | ---: | ---: | ---: | ---: | ---: |
| baseline | 6.67 | 5.33 | 26.33 | 0.0352 | 0.1281 |
| adaptive | 1.00 | 1.00 | 16.33 | 0.1588 | 0.1588 |
| adaptive_auto | 3.67 | 3.33 | 12.67 | 0.0273 | 0.1002 |

结果解释：

1. adaptive 呈现明显单轮过剪（`rounds_mean=1.00`，且单轮平均 drop ratio 最高）。
2. adaptive_auto 把节奏从“单轮过剪”拉回到“多轮收缩”，但其分类指标仍未追平 baseline。
3. baseline 的探索轮次最多，当前样本下对应了更高的分类指标上限。

综合而言：

1. 现阶段应把 adaptive 系列定位为“流程控制/结构压缩策略”，而不是“已证实精度增强策略”。
2. 如果目标是分类指标，baseline 仍是默认首选；如果目标是符号化时延，可按场景评估 adaptive_auto。
3. 在当前 `n=3` 证据下，更适宜将结果表述为“流程层收益成立，精度增益尚未得到验证”。

样本量与证据边界如下：

1. 当前仅 `3` 个 seed，统计功效有限。
2. 存在“均值与中位数方向不一致”的情况，说明结果对异常 seed 敏感。
3. 若需进一步判断显著性，宜扩展到至少 `10` 个 seed，并补充非参数检验（如 Wilcoxon 符号秩）与效应量。

## 7. 报告口径

避免只报告均值，至少同时给出：

1. 均值与标准差。
2. 中位数差值。
3. 相对 baseline 的胜负计数（win/lose/tie）。
4. 运行代价指标（`export_wall_time_s`、`symbolic_total_seconds`）与结构指标（`final_n_edge`）。

正文可采用以下较为保守的表述方式：

1. “在 `n=3` seeds 下，adaptive 系列在精度指标上未显示稳定优势（`final_acc`: adaptive `1胜2负`，adaptive_auto `0胜3负`；`macro_auc` 均 `0胜3负`）。”
2. “因此更适宜将 adaptive 视为工程稳定化策略，而非已证实的精度增强策略。”
3. “后续通过更大 seed 样本与统计检验确认精度结论。”

若 `final_acc` 与 `macro_auc` 未形成稳定优势，宜表述为“流程改进成立，但精度优势尚未得到验证”，不宜直接写为“显著优于 baseline”。

## 8. 与总文档统一口径（2026-03）

为避免跨文档“默认值”和“项目层设定”混用，统一采用以下写法：

1. **CLI 默认值**：指参数解析器内置默认（本文件第 4 节）。
2. **项目配置**：指基于实验结论所采用的配置组合（见 [symkan_usage.md](symkan_usage.md) 与 [design.md](design.md)）。
3. 对 2 层 KAN：运行稳定与效率优先时使用 `--layerwise-finetune-steps 0`；改进版 LayerwiseFT（steps=60 等）仅作为按需实验开关，不默认承诺分类增益。
