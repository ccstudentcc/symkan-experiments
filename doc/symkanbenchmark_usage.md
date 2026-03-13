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

---

## 7. Adaptive 与 Baseline A/B 对比实验

`stagewise_train` 新增了一组可选优化参数。这节给出一套可复现的 A/B 实验配置：在固定所有其他参数条件下，仅切换 adaptive 开关，观察对 `final_acc`、`final_n_edge`、`validation_mean_r2` 以及训练阶段日志的影响。

### 7.1 新增参数说明

| 参数 | 默认值 | 含义 |
|---|---|---|
| `--use-validation` | 关闭 | 将训练集切出一部分作验证集，用于剪枝接受判断而非 test 集 |
| `--validation-ratio` | `0.15` | 验证集比例；`--use-validation` 开启时生效 |
| `--validation-seed` | 跟随 `--global-seed` | 验证集切分随机种子 |
| `--adaptive-threshold` | 关闭 | 根据最近剪枝成败动态调整阈值，取代固定步长递增 |
| `--threshold-base-step` | `0.005` | 自适应阈值的基础调整步长 |
| `--threshold-min` | `0.001` | 阈值下界 |
| `--threshold-max` | `0.1` | 阈值上界 |
| `--success-boost` | `0.5` | 连续成功时的阈值加速系数 |
| `--failure-penalty` | `0.3` | 连续失败时的阈值惩罚系数 |
| `--stage-min-gain-threshold` | `3` | 最近三次剪枝平均移除边数低于该值时停止当阶段剪枝 |
| `--stage-max-prune-attempts` | `20` | 单阶段最多剪枝尝试次数 |
| `--adaptive-lamb` | 关闭 | 按当前稀疏进度动态调整 `lamb` |
| `--min-lamb-ratio` | `0.3` | lamb 下界倍数 |
| `--max-lamb-ratio` | `1.5` | lamb 上界倍数 |
| `--adaptive-ft` | 关闭 | 按当前稀疏进度缩放剪枝后恢复步数，模型越稀疏恢复步数越少 |
| `--min-ft-ratio` | `0.3` | 恢复步数下界比例 |

所有新参数默认关闭，旧脚本调用一字不改仍等价于 baseline 行为。

### 7.2 Baseline 组命令

```bash
python symkanbenchmark.py \
  --tasks full \
  --stagewise-seeds 42,52,62 \
  --global-seed 123 \
  --output-dir benchmark_ab/baseline \
  --quiet
```

### 7.3 Adaptive 组命令（全功能开启）

```bash
python symkanbenchmark.py \
  --tasks full \
  --stagewise-seeds 42,52,62 \
  --global-seed 123 \
  --output-dir benchmark_ab/adaptive \
  --use-validation \
  --validation-ratio 0.15 \
  --adaptive-threshold \
  --adaptive-lamb \
  --adaptive-ft \
  --quiet
```

其余所有参数（`--stage-lamb-schedule`、`--steps-per-stage`、`--stage-target-edges` 等）均保持脚本默认值，确保两组唯一变量只有 adaptive 开关。

### 7.4 分步对照（逐项开启）

如果想知道每个开关单独贡献了多少，可以按以下顺序依次新增参数，每次一个前缀目录：

```bash
# 只开验证集引导
python symkanbenchmark.py --tasks full --stagewise-seeds 42,52,62 \
  --global-seed 123 --output-dir benchmark_ab/val_only \
  --use-validation --validation-ratio 0.15 --quiet

# 验证集 + 自适应阈值
python symkanbenchmark.py --tasks full --stagewise-seeds 42,52,62 \
  --global-seed 123 --output-dir benchmark_ab/val_thresh \
  --use-validation --validation-ratio 0.15 \
  --adaptive-threshold --quiet

# 验证集 + 自适应阈值 + 自适应 lamb
python symkanbenchmark.py --tasks full --stagewise-seeds 42,52,62 \
  --global-seed 123 --output-dir benchmark_ab/val_thresh_lamb \
  --use-validation --validation-ratio 0.15 \
  --adaptive-threshold --adaptive-lamb --quiet
```

### 7.5 对比结果的做法

运行结束后，用以下 Python 片段快速提取核心对比指标：

```python
import pandas as pd

baseline = pd.read_csv("benchmark_ab/baseline/symkanbenchmark_runs.csv")
adaptive  = pd.read_csv("benchmark_ab/adaptive/symkanbenchmark_runs.csv")

cols = ["stage_seed", "enhanced_acc", "final_acc", "final_n_edge",
        "macro_auc", "validation_mean_r2", "symbolic_total_seconds"]

comp = (
    baseline[cols].set_index("stage_seed")
    .join(adaptive[cols].set_index("stage_seed"), lsuffix="_base", rsuffix="_adapt")
)

# 核心差值
for metric in ["final_acc", "macro_auc", "validation_mean_r2"]:
    comp[f"Δ{metric}"] = comp[f"{metric}_adapt"] - comp[f"{metric}_base"]

print(comp[[c for c in comp.columns if c.startswith("Δ")]].to_string())
print("\n--- 均值 ---")
print(comp[[c for c in comp.columns if c.startswith("Δ")]].mean())
```

### 7.6 解读要点

- **`Δfinal_acc` > 0**：adaptive 提升了进入符号化之前的模型精度；这通常源于剪枝决策更稳、触发回滚更少。
- **`Δvalidation_mean_r2` > 0**：符号化后的表达式数值拟合质量更好，说明传递给 symbolize_pipeline 的模型本身精度更高。
- **`final_n_edge` 变化**：adaptive 模式不保证边数更少，它优化的是稳定性而非极端稀疏度。如果 `final_n_edge` 大幅升高，说明 `prune_acc_drop_tol` 偏严，可以适当放宽。
- **`symbolic_total_seconds` 升高**：adaptive 在单阶段内允许多次剪枝尝试（`--stage-max-prune-attempts`），带来更多计算；如果时间超出预算，可降低 `--stage-max-prune-attempts` 或仅开 `--use-validation` 而不开 `--adaptive-threshold`。

如果三个 seed 的 `Δfinal_acc` 符号不一致，说明改进效果不稳定，不应在论文中下结论。
