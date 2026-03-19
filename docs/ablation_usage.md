# 消融实验使用说明

## 文档导航

- 返回总览：[README](../README.md)
- docs 总入口：[index](index.md)
- 项目地图：[project_map](project_map.md)
- 总体使用文档：[symkan_usage](symkan_usage.md)
- benchmark 文档：[symkanbenchmark_usage](symkanbenchmark_usage.md)
- 消融计划：[ablation_plan](ablation_plan.md)
- 消融报告：[ablation_report](ablation_report.md)
- LayerwiseFT 改进报告：[layerwiseft_improved_report](layerwiseft_improved_report.md)

## 工程版口径入口（2026-03）

1. 若需要区分历史参考版与当前工程版的结论边界，优先阅读 [engineering_version_rerun_note.md](engineering_version_rerun_note.md)。
2. 若需要工程版主引用结果（目录、指标与对照解释），优先阅读 [engineering_rerun_report.md](engineering_rerun_report.md)。
3. 若用于发布前检查，请同步执行 [engineering_release_checklist.md](engineering_release_checklist.md)。
4. 本文聚焦消融脚本与执行方式；跨版本统一叙述以上述工程版文档为准。

## 目录

- [1. 说明范围](#1-说明范围)
- [2. 脚本与功能](#2-脚本与功能)
- [3. 运行方式](#3-运行方式)
- [4. 参数说明](#4-参数说明)
- [5. 输出目录与结果文件](#5-输出目录与结果文件)
- [6. 统一口径](#6-统一口径)
- [7. 当前结果摘要](#7-当前结果摘要)

## 1. 说明范围

本文说明以下三个脚本的用途、参数与输出结果：

1. [ablation_runner.py](../ablation_runner.py)：运行单因素消融矩阵。
2. [analyze_layerwiseft.py](../analyze_layerwiseft.py)：基于已有结果分析 `full` 与 `wolayerwiseft` 的差异。
3. [compare_layerwiseft_improved.py](../compare_layerwiseft_improved.py)：运行并比较改进版 LayerwiseFT（默认 `layerwiseft_esreg`）与 `full`、`wolayerwiseft` 的差异。

## 2. 脚本与功能

### 2.1 `ablation_runner.py`

该脚本用于运行单因素消融矩阵，默认覆盖以下变体：

- `full`
- `wostagewise`
- `wopruning`
- `wocompact`
- `wolayerwiseft`

### 2.2 `analyze_layerwiseft.py`

该脚本读取已有消融结果，对 `full` 与 `wolayerwiseft` 进行运行级与类别级比较。

### 2.3 `compare_layerwiseft_improved.py`

该脚本可运行改进版 LayerwiseFT，并生成其相对于 `full` 与 `wolayerwiseft` 的比较结果。

## 3. 运行方式

参考环境（用于结果解释）：

1. 操作系统：Windows 11 专业版 `23H2`（OS Build `22631.5472`）。
2. Python：`Miniconda` 的 `kan` 环境，解释器路径 `C:\Users\chenpeng\miniconda3\envs\kan\python.exe`（`3.9.25`）。
3. CPU：`12th Gen Intel(R) Core(TM) i5-12500H`。
4. 内存：`16 GB`。
5. 深度学习运行时：`PyTorch 2.1.2+cpu`（CPU 路径）。

### 3.1 完整单因素消融

```powershell
# 运行目录：仓库根目录（symkan-experiments/）
python -m scripts.ablation_runner --quiet
```

这条命令若不传 `--config`，`ablation_runner` 本身不会加载 `configs/ablation_runner.default.yaml`；它会把每个变体委托给 `scripts.symkanbenchmark`，而后者再回退到默认的 `configs/symkanbenchmark.default.yaml`。

若希望显式固定所有变体共享的 `AppConfig`，建议传入：

```powershell
# 运行目录：仓库根目录（symkan-experiments/）
python -m scripts.ablation_runner --config configs/ablation_runner.default.yaml
```

该命令默认在 `outputs/benchmark_ablation/` 下生成各变体结果目录，并输出：

- `outputs/benchmark_ablation/ablation_runs_raw.csv`
- `outputs/benchmark_ablation/ablation_runs_summary.csv`

### 3.2 仅聚合已有结果

```powershell
# 运行目录：仓库根目录（symkan-experiments/）
python -m scripts.ablation_runner --aggregate-only --output-dir outputs/benchmark_ablation
```

该模式适用于各变体结果已存在，仅需重新汇总总表的情形。

### 3.3 LayerwiseFT 专项分析

```powershell
# 运行目录：仓库根目录（symkan-experiments/）
python -m scripts.analyze_layerwiseft --ablation-dir outputs/benchmark_ablation --seeds 42,52,62
```

默认输出目录为：

- `outputs/benchmark_ablation/layerwiseft_analysis/`

### 3.4 改进版 LayerwiseFT 比较

```powershell
# 运行目录：仓库根目录（symkan-experiments/）
python -m scripts.compare_layerwiseft_improved --ablation-dir outputs/benchmark_ablation --seeds 42,52,62 --quiet
```

默认输出包括：

- `outputs/benchmark_ablation/layerwiseft_esreg/`
- `outputs/benchmark_ablation/layerwiseft_improved_analysis/comparison_raw.csv`
- `outputs/benchmark_ablation/layerwiseft_improved_analysis/comparison_summary.csv`
- `outputs/benchmark_ablation/layerwiseft_improved_analysis/delta_new_vs_full.csv`
- `outputs/benchmark_ablation/layerwiseft_improved_analysis/delta_new_vs_wolayerwiseft.csv`

若 `layerwiseft_esreg` 已存在，可跳过重新训练：

```powershell
# 运行目录：仓库根目录（symkan-experiments/）
python -m scripts.compare_layerwiseft_improved --ablation-dir outputs/benchmark_ablation --seeds 42,52,62 --skip-run
```

## 4. 参数说明

### 4.1 `ablation_runner.py`

常用参数如下：

- `--config configs/ablation_runner.default.yaml`
- `--variants full,wostagewise,wopruning,wocompact,wolayerwiseft`
- `--stagewise-seeds 42,52,62`
- `--output-dir outputs/benchmark_ablation`
- `--python <path>`
- `--quiet`
- `--verbose`
- `--aggregate-only`

若用于论文统计，常见设置为：

```powershell
# 运行目录：仓库根目录（symkan-experiments/）
python -m scripts.ablation_runner --config configs/ablation_runner.default.yaml --stagewise-seeds 42,52,62 --quiet
```

推荐实践是：

- 用一份 `AppConfig` YAML 固定所有变体共享的算法参数。
- `ablation_runner` 自身不解析算法配置细节；它只是把这份 YAML 透传给每次 `scripts.symkanbenchmark` 调用。
- 在 `ablation_runner` 层主要保留变体矩阵、共享 YAML、输出目录、Python 路径、seed 列表与日志控制（`--quiet / --verbose`）。
- 各变体只保留少量 benchmark CLI 覆盖；其中 `wostagewise` 实际会打包 `--disable-stagewise-train`、`--prune-collapse-floor 0.0` 与 `--symbolic-prune-adaptive-acc-drop-tol 0.7` 三项覆盖，而不只是单个 flag。

这样可以保证不同变体共享同一套基础实验设定，而不是在多个子命令里重复拷贝 `AppConfig` 字段。

### 4.2 `analyze_layerwiseft.py`

常用参数如下：

- `--ablation-dir outputs/benchmark_ablation`
- `--seeds 42,52,62`
- `--out-dir <path>`

输出内容主要包括：

1. 运行级对比。
2. 类别级对比。
3. 终端中的假设验证报告。

### 4.3 `compare_layerwiseft_improved.py`

常用参数如下：

- `--ablation-dir outputs/benchmark_ablation`
- `--new-variant layerwiseft_esreg`
- `--seeds 42,52,62`
- `--global-seed 123`
- `--python <path>`
- `--skip-run`
- `--quiet / --verbose`

改进版 LayerwiseFT 的默认参数包括：

- `--layerwise-finetune-steps 60`
- `--layerwise-finetune-lamb 1e-5`
- `--layerwise-validation-ratio 0.15`
- `--layerwise-validation-seed <None>`
- `--layerwise-early-stop-patience 2`
- `--layerwise-early-stop-min-delta 1e-3`
- `--layerwise-eval-interval 20`
- `--layerwise-validation-n-sample 300`

说明：这里的 60 步是 `compare_layerwiseft_improved.py` 为了可比性设置的实验技术默认值，不等同项目推荐基线。

配置来源补充说明：

- `analyze_layerwiseft.py` 是纯读取已有结果的离线分析脚本，不消费 `AppConfig`。
- `compare_layerwiseft_improved.py` 当前不会读取单独的 `AppConfig` YAML；它运行新变体时会基于 `scripts.symkanbenchmark` 的默认配置来源（即 `configs/symkanbenchmark.default.yaml`），再叠加少量 layerwise 相关 CLI 覆盖与 `--global-seed`。
- 因此，如果你希望改进版 LayerwiseFT 建立在自定义主配置之上，当前更稳妥的做法是先手动运行一组自定义 `scripts.symkanbenchmark` 结果，再按输出目录做后续比较。

## 5. 输出目录与结果文件

典型目录结构如下：

```plaintext
outputs/benchmark_ablation/
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

主要文件包括：

1. `ablation_runs_summary.csv`：各变体的总体统计结果。
2. `layerwiseft_analysis/run_level_comparison.csv`：`full` 与 `wolayerwiseft` 的运行级比较。
3. `layerwiseft_analysis/class_level_comparison.csv`：`full` 与 `wolayerwiseft` 的类别级比较。
4. `layerwiseft_improved_analysis/comparison_summary.csv`：改进版与对照项的总体比较。
5. `layerwiseft_improved_analysis/delta_new_vs_full.csv`：改进版相对 `full` 的逐指标差值。

## 6. 统一口径

与 [design.md](design.md) 和 [symkan_usage.md](symkan_usage.md) 保持一致，本文采用以下口径：

1. `stagewise_train` 视为当前流程的必要组成部分，而非可选优化项。
2. 渐进剪枝与输入压缩主要体现为复杂度与成本控制，不预设其带来稳定精度提升。
3. 对 2 层 KAN，`LayerwiseFT` 更适合作为可选实验配置；项目推荐基线通常为 `--layerwise-finetune-steps 0`（而 4.3 节的 60 步用于改进版对照实验）。
4. 对 `n=3` 的结果，应优先描述趋势与边界，而不宜作过度确定性表述。

## 7. 当前结果摘要

根据 `outputs/benchmark_ablation/ablation_runs_summary.csv` 与 `outputs/benchmark_ablation/layerwiseft_improved_analysis/*.csv`，当前结果可概括如下：

1. `full` 的统计结果为 `final_acc=0.7807 ± 0.0013`，`macro_auc=0.9548 ± 0.0028`。
2. `wostagewise` 中，`final_acc=0.4430 ± 0.0319`，且 `effective_target_edges` 由 90 增至 1040，说明 `stagewise_train` 对当前流程具有基础性作用。
3. `wopruning` 中，`final_acc` 有所提高，但 `expr_complexity_mean` 与 `symbolic_total_seconds` 明显增加，说明其代价主要体现在复杂度与耗时上。
4. `wolayerwiseft` 中，`final_acc=0.7838 ± 0.0014`，同时 `symbolic_total_seconds=20.41 ± 0.06`，在 2 层 KAN 设定下具有较高的成本收益比。
5. `layerwiseft_esreg` 相对 `full` 仅表现出亚秒级时间差；相对 `wolayerwiseft` 则增加约 12.86 秒符号化时间，因此尚不足以支持默认切换。
