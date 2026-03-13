# symkanbenchmark.py 使用说明（精简版）

[symkanbenchmark.py](../symkanbenchmark.py) 将 kan.ipynb 的主实验流程与两个 benchmark 流程脚本化，核心目标是：

1. 支持同一参数集的批量多 seed 运行。
2. 稳定导出结构化 CSV 结果。
3. 避免 notebook 手工执行带来的覆盖和漏记。

## 1. 快速开始

### 1.1 一条命令跑完整流程

```bash
python symkanbenchmark.py --tasks all --verbose
```

说明：`all = full + eval-bench + parallel-bench`。

### 1.2 只跑主实验（最常用）

```bash
python symkanbenchmark.py --tasks full
```

静默模式：

```bash
python symkanbenchmark.py --tasks full --quiet
```

说明：`--quiet` 会压制训练和符号化的过程输出；若与 `--verbose` 同时设置，`--quiet` 优先。

### 1.3 批量 seed（论文统计建议）

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

默认输出目录为 `benchmark_runs/`，每个 seed 对应一个独立 run 子目录（即使只有一个 seed 也会建子目录，避免覆盖）：

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

重点文件：

1. `symkanbenchmark_runs.csv`：多 seed/多配置横向对比主表。
2. `kan_stage_logs.csv`：阶段训练是否频繁回滚。
3. `symbolize_trace.csv`：剪枝节奏是否过猛。
4. `formula_validation.csv`：R² 与数值稳定性。
5. `benchmark_symbolic_parallel_quick.csv`：并行加速是否真实有效。

## 4. 参数速查

### 4.1 主实验默认值（与 notebook 对齐）

- `--inner-dim 16`：隐藏层宽度（主干表达能力与训练成本的平衡点）。
- `--top-k 120`：归因后保留的输入特征数（越大保留信息越多，搜索也更慢）。
- `--stage-target-edges 120`：stagewise 阶段期望保留的边数目标。
- `--symbolic-target-edges 90`：symbolize 后期望收敛到的边数目标（控制最终复杂度）。
- `--steps-per-stage 60`：每个 stage 的训练步数。
- `--finetune-steps 50`：阶段内常规微调步数。
- `--layerwise-finetune-steps 120`：逐层微调步数（用于稳定结构变更后的收敛）。
- `--affine-finetune-steps 200`：仿射参数微调步数（提高最后拟合质量）。

### 4.2 常用控制参数

- `--tasks full`：只跑主实验链路。
- `--tasks eval-bench`：只跑评估性能专题（会复用主流程上下文）。
- `--tasks parallel-bench`：只跑并行策略对照。
- `--tasks all`：一次跑完 full + eval-bench + parallel-bench。
- `--stagewise-seeds 42,52,62`：指定一组 stagewise 随机种子并逐个运行。
- `--output-dir benchmark_runs_alt`：指定输出根目录，避免和已有实验互相覆盖。
- `--verbose`：打印过程日志，便于观察训练与剪枝过程。
- `--quiet`：静默运行，只保留必要结果输出。

### 4.3 函数库预设

- `--lib-preset layered`：分层函数库，精度与复杂度较均衡（默认推荐）。
- `--lib-preset fast`：精简函数库，优先降低搜索成本与运行时间。
- `--lib-preset expressive`：增强表达能力，适合分层库不足时尝试。
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
- `--parallel-layerwise-finetune-steps 40`：并行实验逐层微调步数。
- `--parallel-affine-finetune-steps 0`：并行实验仿射微调步数（0 代表跳过）。

## 5. 结果解读最小集合

建议重点关注 `symkanbenchmark_runs.csv` 这些列：

- `base_acc`
- `enhanced_acc`
- `final_acc`
- `final_n_edge`
- `effective_target_edges`
- `effective_input_dim`
- `macro_auc`
- `validation_mean_r2`
- `symbolic_total_seconds`

论文用途建议：不要用单次结果下结论，至少跑 3 个 seed，再统计：

1. `symkanbenchmark_runs.csv` 的均值与方差。
2. `benchmark_multi_round_summary_cn.csv` 的速度均值与标准差。
3. `benchmark_symbolic_parallel_quick.csv` 的 `vs_off_speedup_x`。

---

## 6. Adaptive A/B 实验（baseline / adaptive / adaptive_auto）

三组定义：

1. `baseline`：不启用 adaptive。
2. `adaptive`：启用验证反馈 + 自适应阈值 + 自适应 lamb/ft。
3. `adaptive_auto`：在 adaptive 上增加阶段早停与 symbolize 自适应剪枝节奏。

### 6.1 命令模板（减少重复）

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

说明：当前默认启用 `symbolic-prune-adaptive-threshold`。禁用时显式传 `--no-symbolic-prune-adaptive-threshold`。

### 6.3 结果自动汇总

推荐使用 [benchmark_ab_compare.py](../benchmark_ab_compare.py)：

```bash
python benchmark_ab_compare.py --root benchmark_ab --baseline baseline --variants adaptive,adaptive_auto --output benchmark_ab/comparison
```

输出：

- [benchmark_ab/comparison/variant_summary.csv](../benchmark_ab/comparison/variant_summary.csv)
- [benchmark_ab/comparison/pairwise_delta_summary.csv](../benchmark_ab/comparison/pairwise_delta_summary.csv)
- [benchmark_ab/comparison/seedwise_delta.csv](../benchmark_ab/comparison/seedwise_delta.csv)
- [benchmark_ab/comparison/trace_seedwise.csv](../benchmark_ab/comparison/trace_seedwise.csv)
- [benchmark_ab/comparison/trace_summary.csv](../benchmark_ab/comparison/trace_summary.csv)

### 6.4 当前结论（seed: 42/52/62）

基于 [benchmark_ab/comparison/pairwise_delta_summary.csv](../benchmark_ab/comparison/pairwise_delta_summary.csv)：

1. `adaptive` 与 `adaptive_auto` 相对 baseline 在 `final_acc` 均为 `1胜2负`，中位数差值为负。
2. `macro_auc` 同样为 `1胜2负`，中位数差值为负。
3. `validation_mean_r2` 两组均为 `2胜1负`，中位数差值为正。

基于 [benchmark_ab/comparison/trace_summary.csv](../benchmark_ab/comparison/trace_summary.csv)：

1. `adaptive`：`rounds_mean = 1.0`，剪枝过快。
2. `adaptive_auto`：`rounds_mean = 4.33`，`effective_rounds_mean = 3.0`，剪枝节奏改善。
3. `baseline`：`rounds_mean = 16.67`，最慢但有效剪枝轮最多。

结论：

1. baseline 仍是“上限高但波动大”。
2. adaptive 系列主要提升流程稳定性，不保证每个 seed 精度更高。
3. adaptive_auto 修复“单轮过剪”，但暂未形成稳定精度优势。

## 7. 论文写作建议

避免只报告均值，至少同时给出：

1. 均值与标准差。
2. 中位数差值。
3. 相对 baseline 的胜负计数（win/lose/tie）。

如果 `final_acc` 与 `macro_auc` 仍是 `1胜2负`，建议表述为“稳定性改善，但精度优势尚不稳定”，不要写“显著优于 baseline”。
