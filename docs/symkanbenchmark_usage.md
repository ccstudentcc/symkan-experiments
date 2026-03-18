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

[symkanbenchmark.py](../symkanbenchmark.py) 将 [../notebooks/kan.ipynb](../notebooks/kan.ipynb) 中的主实验流程及两个 benchmark 流程脚本化，其主要目的包括：

1. 支持同一参数集的批量多 seed 运行。
2. 稳定导出结构化 CSV 结果。
3. 避免 notebook 手工执行带来的覆盖和漏记。

## 1. 运行入口

### 1.1 完整流程

```bash
python -m scripts.symkanbenchmark --tasks all --verbose
```

其中，`all = full + eval-bench + parallel-bench`。

脚本默认优先读取 `data/X_train.npy`、`data/X_test.npy`、`data/Y_train_cat.npy`、`data/Y_test_cat.npy`（兼容旧版根目录 `X_train.npy`、`X_test.npy`、`Y_train_cat.npy`、`Y_test_cat.npy`）。若文件缺失且启用了 `data.auto_fetch_mnist`，脚本默认只会在仓库 `data/` 下补齐缺失文件；若配置把目标路径指向 `data/` 之外，需显式设置 `data.allow_auto_fetch_outside_data_dir: true`。自动下载优先使用 `tensorflow.keras.datasets.mnist`，失败时会先发出 warning，再回退到 `sklearn.fetch_openml`。

## 配置管理建议

`symkanbenchmark.py` 现支持通过 `--config` 加载 YAML 运行配置，例如：

```bash
python -m scripts.symkanbenchmark --config configs/symkanbenchmark.default.yaml --quiet
```

若未显式传入 `--config`，脚本当前会默认读取：

```bash
configs/symkanbenchmark.default.yaml
```

约定如下：

- `AppConfig` YAML 管算法运行逻辑：训练参数、设备、数据路径、符号化策略等。
- 环境变量管敏感项或环境差异：支持 `${ENV_VAR}` 和 `${ENV_VAR:-default}`，且只会在 YAML 解析后的标量字符串上展开，避免把环境变量内容当成新的配置结构。
- CSV 管输入数据与结果产物：例如 `symkanbenchmark_runs.csv`、`kan_stage_logs.csv`、`kan_symbolic_summary.csv`。

命令行参数不再由 `load_config()` 自动合并进配置对象；脚本会先 `load_config()` 得到 `AppConfig`，再仅对白名单字段做显式且重新校验的覆盖。当前覆盖点分布在 `runtime / library / workflow / evaluation / symbolize` 五段，因此适合“固定主配置 + 少量局部覆盖”的工作流。

## 配置分层原则

当前项目采用三层口径：

1. notebook / Python 调用：直接构造 `AppConfig` 并传给核心函数。
2. CLI：先 `load_config()` 得到 `AppConfig`，再做一小组显式白名单覆盖。
3. 核心编排：统一只认 `AppConfig`，而不是 `argparse.Namespace` 或脚本私有配置模型。

`symkanbenchmark.py` 现在直接把 `AppConfig` 传给 `stagewise_train` / `symbolize_pipeline`。也就是说，YAML、CLI 和 notebook 最终都收敛到同一份库层配置对象。

还需注意一层运行期注入：

- `stagewise.width`、`stagewise.grid`、`stagewise.k`、`stagewise.seed`、`stagewise.batch_size`
- `stagewise.validation_seed` 若在 YAML 中留空，则运行时继承 `runtime.global_seed`
- `symbolize.batch_size`
- `symbolize.layerwise_validation_seed` 若在 YAML 中留空，则运行时继承 `runtime.global_seed`
- 当 `symbolize.lib / lib_hidden / lib_output` 都未显式指定时，由 `library.lib_preset` 派生对应函数库

这些字段由脚本在运行时基于数据形状、seed、batch size 和函数库预设补入，不要求在 YAML 中手工硬编码。

### 1.2 主实验

```bash
python -m scripts.symkanbenchmark --tasks full
```

静默模式：

```bash
python -m scripts.symkanbenchmark --tasks full --quiet
```

`--quiet` 用于抑制训练与符号化过程输出；若与 `--verbose` 同时设置，则 `--quiet` 优先。

说明：

- 当前脚本把算法参数统一收敛到 `AppConfig` YAML。
- CLI 主要保留任务调度、输出目录、seed 列表和一小组显式白名单覆盖。
- 更细的训练/剪枝/符号化参数，推荐直接修改 `configs/symkanbenchmark.default.yaml` 或你自己的 `AppConfig` 文件。

### 1.3 多 seed 运行

```bash
python -m scripts.symkanbenchmark --tasks all --stagewise-seeds 42,52,62
```

## 2. 任务与命令速查

- 主实验：

```bash
python -m scripts.symkanbenchmark --tasks full
```

- 评估链路 benchmark（仍会先构造主流程上下文）：

```bash
python -m scripts.symkanbenchmark --tasks eval-bench
```

- 并行策略 benchmark：

```bash
python -m scripts.symkanbenchmark --tasks parallel-bench --parallel-modes auto,off,thread4,thread8
```

说明：当前 `parallel-bench` 仍是 correctness-first 的 requested-mode 对照。脚本会保留 `auto/off/threadN` 这些请求标签做横向记录，但 `suggest_symbolic` 的实际 worker 数会保守回落到 1；可在输出列 `parallel_workers_effective` 中确认。

- 组合任务：

```bash
python -m scripts.symkanbenchmark --tasks full,parallel-bench
```

## 3. 输出目录与文件含义

默认输出目录为 `outputs/benchmark_runs/`。每个 seed 对应一个独立的 run 子目录，以避免结果覆盖：

```text
outputs/benchmark_runs/
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
5. `benchmark_symbolic_parallel_quick.csv`：requested mode 标签与实际 `parallel_workers_effective` 的对照结果。

## 4. 参数速查

### 4.1 主实验参数来源

当前实现中，大多数算法参数不再作为长 CLI 直接暴露，而是来自 `AppConfig` YAML，例如：

- `model.inner_dim`
- `stagewise.target_edges`
- `stagewise.steps_per_stage`
- `symbolize.target_edges`
- `symbolize.layerwise_finetune_steps`
- `symbolize.affine_finetune_steps`

口径说明如下：

1. 算法参数的正式默认值以 `AppConfig` 模型和示例 YAML 为准。
2. CLI 主要承担任务调度和一小组显式白名单覆盖，不再承载整套研究参数。
3. 对典型 2 层 KAN（`[in, hidden, class]`），项目层设定通常仍将 `layerwise_finetune_steps` 视为按需开关。

逐层符号化属于有损替换；`fix_symbolic` 选定函数族后无法回退。在 2 层 KAN 中，LayerwiseFT 仅有一次层间补偿窗口，因此其改进版更接近风险控制选项，而非默认增益模块。

### 4.2 常用控制参数

- `--tasks full`：只跑主实验链路。
- `--tasks eval-bench`：只跑评估性能专题（会复用主流程上下文）。
- `--tasks parallel-bench`：只跑 requested-mode 对照；当前实现会把实际 worker 数保守回落到 1。
- `--tasks all`：一次跑完 full + eval-bench + parallel-bench。
- `--stagewise-seeds 42,52,62`：指定一组 stagewise 随机种子并逐个运行。
- `--output-dir outputs/benchmark_runs_alt`：指定输出根目录，避免和已有实验互相覆盖。
- `--verbose`：打印过程日志，便于观察训练与剪枝过程。
- `--quiet`：静默运行，只保留必要结果输出。
- 数据路径、MNIST 自动拉取、类别集合等参数现在统一由 `AppConfig.data` 管理。
- `data.auto_fetch_mnist=true`：缺少 `.npy` 文件时自动补齐 MNIST 数据。
- `data.allow_auto_fetch_outside_data_dir=true`：显式允许把自动补齐文件写到仓库 `data/` 目录之外。

### 4.3 常见显式覆盖

- `--lib-preset layered`：分层函数库，精度与复杂度较均衡。
- `--lib-preset fast`：精简函数库，优先降低搜索成本与运行时间。
- `--lib-preset expressive`：增强表达能力，可在分层库不足时试验。
- `--lib-preset full`：完整函数库，搜索空间最大，通常最慢但最灵活。

- `--device cpu`：覆盖 `runtime.device`。
- `--global-seed 321`：覆盖 `runtime.global_seed`。
- `--baseline-seed 321`：覆盖 `runtime.baseline_seed`。
- `--batch-size 256`：覆盖 `runtime.batch_size`。
- `--max-prune-rounds 12`：覆盖 `symbolize.max_prune_rounds`。
- `--layerwise-finetune-steps 0`：覆盖 `symbolize.layerwise_finetune_steps`。
- `--no-input-compaction`：覆盖 `symbolize.enable_input_compaction`。
- `--prune-collapse-floor 0.0`：覆盖 `symbolize.prune_collapse_floor`。

### 4.4 评估 benchmark 参数

- `--bench-repeat 3`：每项 benchmark 的正式重复次数（用于统计均值/方差）。
- `--bench-warmup 1`：预热轮数（减少首次执行的冷启动偏差）。
- `--eval-rounds 3`：评估回合数（跨回合汇总稳定性）。
- `--validate-n-sample 500`：验证抽样规模（越大越稳，耗时也更高）。

### 4.5 并行 benchmark 参数

- `--parallel-modes auto,off,thread4`：requested mode 候选集合；当前主要用于记录标签与串行基线对照，而不是验证真实多 worker 提速。
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
python -m scripts.symkanbenchmark \
  --tasks full \
  --stagewise-seeds 42,52,62 \
  --config <VARIANT_APP_CONFIG> \
  --output-dir <OUT_DIR> \
  <EXTRA_FLAGS> \
  --quiet
```

实例：

```bash
# baseline
python -m scripts.symkanbenchmark --tasks full --stagewise-seeds 42,52,62 --config configs/benchmark_ab/baseline.yaml --output-dir outputs/benchmark_ab/baseline --quiet

# adaptive
python -m scripts.symkanbenchmark --tasks full --stagewise-seeds 42,52,62 --config configs/benchmark_ab/adaptive.yaml --output-dir outputs/benchmark_ab/adaptive --quiet

# adaptive_auto
python -m scripts.symkanbenchmark --tasks full --stagewise-seeds 42,52,62 --config configs/benchmark_ab/adaptive_auto.yaml --output-dir outputs/benchmark_ab/adaptive_auto --quiet
```

### 6.2 配置建议

这一组实验不再推荐通过长 CLI 逐项传参。

- `baseline`、`adaptive`、`adaptive_auto` 的差异应直接体现在各自的 `AppConfig` YAML 中。
- 当前仓库已内置 `configs/benchmark_ab/baseline.yaml`、`configs/benchmark_ab/adaptive.yaml` 与 `configs/benchmark_ab/adaptive_auto.yaml` 三份模板；若需扩展，再从它们复制出你自己的 variant 配置文件。
- benchmark CLI 主要保留 `--config`、`--output-dir`、`--stagewise-seeds` 和一小组显式白名单覆盖项。
- 需要复现实验时，优先保留完整 YAML，而不是把研究参数重新散落回命令行。
- 不建议把三个变体都指向同一份 YAML；否则只会得到不同输出目录下的同配置结果，而不是有效对照。

### 6.3 结果自动汇总

结果汇总可使用 [benchmark_ab_compare.py](../benchmark_ab_compare.py)：

```bash
python -m scripts.benchmark_ab_compare --root outputs/benchmark_ab --baseline baseline --variants adaptive,adaptive_auto --output outputs/benchmark_ab/comparison
```

输出：

- [outputs/benchmark_ab/comparison/variant_summary.csv](../outputs/benchmark_ab/comparison/variant_summary.csv)
- [outputs/benchmark_ab/comparison/pairwise_delta_summary.csv](../outputs/benchmark_ab/comparison/pairwise_delta_summary.csv)
- [outputs/benchmark_ab/comparison/seedwise_delta.csv](../outputs/benchmark_ab/comparison/seedwise_delta.csv)
- [outputs/benchmark_ab/comparison/trace_seedwise.csv](../outputs/benchmark_ab/comparison/trace_seedwise.csv)
- [outputs/benchmark_ab/comparison/trace_summary.csv](../outputs/benchmark_ab/comparison/trace_summary.csv)
- [outputs/benchmark_ab/comparison/comparison_summary.md](../outputs/benchmark_ab/comparison/comparison_summary.md)

### 6.4 当前统计结果（seed: 42/52/62）

基于 [outputs/benchmark_ab/comparison/variant_summary.csv](../outputs/benchmark_ab/comparison/variant_summary.csv)、[outputs/benchmark_ab/comparison/pairwise_delta_summary.csv](../outputs/benchmark_ab/comparison/pairwise_delta_summary.csv) 与 [outputs/benchmark_ab/comparison/trace_summary.csv](../outputs/benchmark_ab/comparison/trace_summary.csv)，可优先报告以下三张表。

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

1. **CLI 默认值**：指脚本当前保留的调度参数与少量显式覆盖项默认值。
2. **项目配置**：指基于实验结论所采用的 `AppConfig` 组合（见 [symkan_usage.md](symkan_usage.md) 与 [design.md](design.md)）。
3. 对 2 层 KAN：运行稳定与效率优先时可将 `layerwise_finetune_steps` 设为 0；改进版 LayerwiseFT（steps=60 等）仅作为按需实验开关，不默认承诺分类增益。
