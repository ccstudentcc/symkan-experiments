# symkanbenchmark.py 使用说明

[`symkanbenchmark.py`](../symkanbenchmark.py) 是把当前 kan.ipynb 主实验和后半段两个 benchmark 单元抽成命令行脚本后的版本。它的目标不是取代 notebook 做交互分析，而是把“同一组参数批量跑多次、稳定导出 CSV”这件事做干净。

## 1. 脚本做什么

默认情况下，脚本会按当前 notebook 的参数顺序执行：

1. 训练 baseline KAN。
2. 做 `safe_attribute` 归因并保留 top-k 输入。
3. 执行 `stagewise_train`。
4. 执行 `symbolize_pipeline`。
5. 导出符号汇总、阶段日志、R² 验证和 AUC 摘要。
6. 可选再跑评估链路 benchmark 和并行策略 benchmark。

它不是另起一套配置。默认值就是 notebook 当前那组参数。

## 2. 输出结构

默认输出目录是 `benchmark_runs/`。如果你传了多个 `stagewise` seed，每个 run 会落到独立子目录：

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

如果你只跑一个 seed，也照样会生成一个 run 子目录。这样不会把多轮结果互相覆盖。

## 3. 最常用命令

### 3.1 完整复现 notebook 主流程

```bash
python symkanbenchmark.py --tasks all --verbose
```

这会执行主实验、评估 benchmark 和并行 benchmark。

### 3.2 只跑主实验，不跑额外 benchmark

```bash
python symkanbenchmark.py --tasks full
```

如果你只是想安静地把结果跑完，不想在终端里看训练进度条和阶段日志，直接加：

```bash
python symkanbenchmark.py --tasks full --quiet
```

`--quiet` 会屏蔽 baseline、`stagewise_train`、`symbolize_pipeline` 以及并行 benchmark 中的过程输出，只保留脚本最终完成提示。

### 3.3 批量跑多个 stagewise seed

```bash
python symkanbenchmark.py --tasks all --stagewise-seeds 42,52,62
```

这是脚本支持“命令行批量测试”的核心方式。每个 seed 会单独输出一个 run 目录，顶层再汇总成总表。

### 3.4 只跑性能与内存专题

```bash
python symkanbenchmark.py --tasks eval-bench
```

注意：脚本仍然会先构造完整主流程上下文，因为 benchmark 需要 `enhanced_model` 和 `export_model`。

### 3.5 只跑并行速度对照

```bash
python symkanbenchmark.py --tasks parallel-bench --parallel-modes auto,off,thread4,thread8
```

## 4. 关键参数

### 4.1 与 notebook 一致的默认值

主实验默认值已经和 notebook 对齐：

- `--inner-dim 16`
- `--top-k 120`
- `--stage-target-edges 120`
- `--symbolic-target-edges 90`
- `--steps-per-stage 60`
- `--finetune-steps 50`
- `--layerwise-finetune-steps 120`
- `--affine-finetune-steps 200`

### 4.2 任务开关

- `--tasks full`
- `--tasks eval-bench`
- `--tasks parallel-bench`
- `--tasks all`

多个任务用逗号分隔，例如：

```bash
python symkanbenchmark.py --tasks full,parallel-bench
```

### 4.3 输出控制

- `--verbose`：显示阶段训练和符号化过程日志。
- `--quiet`：静默运行，压掉训练进度条和中间输出。

两者同时传入时，`--quiet` 优先，否则静默就没有意义。

### 4.4 批量测试参数

- `--stagewise-seeds 42,52,62`
- `--output-dir benchmark_runs_alt`

如果你主要想比较不同随机初始化对最终符号化结果的影响，这两个参数就够了。

### 4.5 函数库预设

- `--lib-preset layered`
- `--lib-preset fast`
- `--lib-preset expressive`
- `--lib-preset full`

建议：

- 主实验优先用 `layered`。
- 只关心速度时可以试 `fast`。
- 只有在分层库明显不够表达时再上 `expressive/full`。

### 4.6 评估 benchmark 参数

- `--bench-repeat 3`
- `--bench-warmup 1`
- `--eval-rounds 3`
- `--validate-n-sample 500`

这部分直接对应 notebook 第 11 节。

### 4.7 并行 benchmark 参数

- `--parallel-modes auto,off,thread4`
- `--parallel-target-min 40`
- `--parallel-target-max 80`
- `--parallel-max-prune-rounds 8`
- `--parallel-finetune-steps 20`
- `--parallel-layerwise-finetune-steps 40`
- `--parallel-affine-finetune-steps 0`

这部分直接对应 notebook 第 12 节的快速对照实验。

## 5. 结果怎么看

### 5.1 顶层总表

[`symkanbenchmark_runs.csv`](../benchmark_runs/symkanbenchmark_runs.csv) 里最重要的列是：

- `base_acc`
- `enhanced_acc`
- `final_acc`
- `final_n_edge`
- `effective_target_edges`
- `effective_input_dim`
- `macro_auc`
- `validation_mean_r2`
- `symbolic_total_seconds`

这张表用于横向比较多个 seed 或多组参数。

### 5.2 每个 run 目录

- `kan_stage_logs.csv`：看阶段训练是否频繁回滚。
- `symbolize_trace.csv`：看剪枝轮是否过猛。
- `formula_validation.csv`：看 R² 和数值稳定性。
- `benchmark_symbolic_parallel_quick.csv`：看并行加速是否真的有收益。

## 6. 一个建议

如果你想做论文表格，不要直接拿单次运行结果写结论。至少跑 3 个 seed，然后再看：

1. `symkanbenchmark_runs.csv` 的均值和方差。
2. `benchmark_multi_round_summary_cn.csv` 的速度均值和标准差。
3. `benchmark_symbolic_parallel_quick.csv` 的 `vs_off_speedup_x`。

否则你最后只是拿一次碰巧不错的结果替自己背书，这种结论没有技术说服力。
