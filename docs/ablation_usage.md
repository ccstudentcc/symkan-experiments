# ablation 使用说明

本文档覆盖以下 3 个脚本：

1. [ablation_runner.py](../ablation_runner.py)：运行单因素消融矩阵（full / wostagewise / wopruning / wocompact / wolayerwiseft）。
2. [analyze_layerwiseft.py](../analyze_layerwiseft.py)：基于已有结果对比 full vs wolayerwiseft。
3. [compare_layerwiseft_improved.py](../compare_layerwiseft_improved.py)：训练并评估改进版 layerwiseft（默认 `layerwiseft_esreg`）相对 full / wolayerwiseft 的差异。

## 1. 快速开始

### 1.1 运行完整单因素消融

```bash
python ablation_runner.py --quiet
```

默认会在 `benchmark_ablation/` 下依次运行：

- `full`
- `wostagewise`
- `wopruning`
- `wocompact`
- `wolayerwiseft`

并输出总表：

- `benchmark_ablation/ablation_runs_raw.csv`
- `benchmark_ablation/ablation_runs_summary.csv`

### 1.2 只做聚合（不重复训练）

```bash
python ablation_runner.py --aggregate-only --output-dir benchmark_ablation
```

适用于已有各 variant 结果目录，仅重新生成总表。

### 1.3 分析层间微调是否有效

```bash
python analyze_layerwiseft.py --ablation-dir benchmark_ablation --seeds 42,52,62
```

输出目录默认是：

- `benchmark_ablation/layerwiseft_analysis/`

关键文件：

- `run_level_comparison.csv`
- `class_level_comparison.csv`

### 1.4 运行改进版 LayerwiseFT 并对比

```bash
python compare_layerwiseft_improved.py --ablation-dir benchmark_ablation --seeds 42,52,62 --quiet
```

默认会新增 variant：`benchmark_ablation/layerwiseft_esreg/`，然后输出对比分析到：

- `benchmark_ablation/layerwiseft_improved_analysis/comparison_raw.csv`
- `benchmark_ablation/layerwiseft_improved_analysis/comparison_summary.csv`
- `benchmark_ablation/layerwiseft_improved_analysis/delta_new_vs_full.csv`
- `benchmark_ablation/layerwiseft_improved_analysis/delta_new_vs_wolayerwiseft.csv`

如果你已经跑过 `layerwiseft_esreg`，可跳过训练：

```bash
python compare_layerwiseft_improved.py --ablation-dir benchmark_ablation --seeds 42,52,62 --skip-run
```

---

## 2. ablation_runner.py 参数速查

常用参数：

- `--variants full,wostagewise,wopruning,wocompact,wolayerwiseft`：指定要跑的变体集合。
- `--stagewise-seeds 42,52,62`：多 seed 批量运行。
- `--global-seed 123`：全局随机种子。
- `--output-dir benchmark_ablation`：结果根目录。
- `--python <path>`：指定 Python 可执行文件。
- `--quiet`：静默运行。
- `--verbose`：详细日志（与 `--quiet` 二选一，`--quiet` 优先）。
- `--aggregate-only`：不训练，只读取已存在结果目录并聚合。

推荐（论文统计）：

```bash
python ablation_runner.py --stagewise-seeds 42,52,62 --global-seed 123 --quiet
```

---

## 3. analyze_layerwiseft.py 参数速查

常用参数：

- `--ablation-dir benchmark_ablation`：消融结果根目录，需包含 `full/` 与 `wolayerwiseft/`。
- `--seeds 42,52,62`：分析的 seed 列表。
- `--out-dir <path>`：输出目录；为空时默认写入 `benchmark_ablation/layerwiseft_analysis/`。

建议命令：

```bash
python analyze_layerwiseft.py --ablation-dir benchmark_ablation --seeds 42,52,62
```

脚本会输出：

1. 运行级对比（精度、AUC、R2、耗时、边数等）。
2. 类级对比（每类 R2 / 复杂度 / AUC 及差分）。
3. 终端中的假设验证报告（H1~H4）。

---

## 4. compare_layerwiseft_improved.py 参数速查

训练与对比参数：

- `--ablation-dir benchmark_ablation`：实验根目录。
- `--new-variant layerwiseft_esreg`：新变体目录名。
- `--seeds 42,52,62`：seed 列表。
- `--global-seed 123`：全局随机种子。
- `--python <path>`：Python 可执行文件。
- `--skip-run`：跳过训练，仅做汇总。
- `--quiet / --verbose`：日志级别。

改进版 layerwise 参数（默认值）：

- `--layerwise-finetune-steps 60`
- `--layerwise-finetune-lamb 1e-5`
- `--layerwise-validation-ratio 0.15`
- `--layerwise-validation-seed <None>`
- `--layerwise-early-stop-patience 2`
- `--layerwise-early-stop-min-delta 1e-3`
- `--layerwise-eval-interval 20`
- `--layerwise-validation-n-sample 300`

建议命令：

```bash
python compare_layerwiseft_improved.py \
  --ablation-dir benchmark_ablation \
  --new-variant layerwiseft_esreg \
  --seeds 42,52,62 \
  --layerwise-finetune-steps 60 \
  --layerwise-finetune-lamb 1e-5 \
  --quiet
```

---

## 5. 输出目录与文件含义

典型目录结构：

```text
benchmark_ablation/
  ablation_runs_raw.csv
  ablation_runs_summary.csv
  full/
  wostagewise/
  wopruning/
  wocompact/
  wolayerwiseft/
  layerwiseft_esreg/
  layerwiseft_analysis/
    run_level_comparison.csv
    class_level_comparison.csv
  layerwiseft_improved_analysis/
    comparison_raw.csv
    comparison_summary.csv
    delta_new_vs_full.csv
    delta_new_vs_wolayerwiseft.csv
```

重点文件建议：

1. `ablation_runs_summary.csv`：总览各消融变体均值/方差。
2. `layerwiseft_analysis/run_level_comparison.csv`：full vs wolayerwiseft 的运行级对比。
3. `layerwiseft_analysis/class_level_comparison.csv`：full vs wolayerwiseft 的类级差异。
4. `layerwiseft_improved_analysis/comparison_summary.csv`：改进版对 full / wolayerwiseft 的总体表现。
5. `layerwiseft_improved_analysis/delta_new_vs_full.csv`：改进版相对 full 的逐指标差分。

---

## 6. 实验报告与文档链接

与本页面流程直接相关的报告与计划：

1. [消融实验计划](ablation_plan.md)
2. [消融实验报告](ablation_report.md)
3. [LayerwiseFT 改进实验报告](layerwiseft_improved_report.md)

相关总流程文档：

1. [symkanbenchmark 使用说明](symkanbenchmark_usage.md)
