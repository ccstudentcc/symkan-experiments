# 完整实验复跑手册

## 文档导航

- 返回总览：[README](../README.md)
- docs 总入口：[index](index.md)
- 主 benchmark 说明：[symkanbenchmark_usage](symkanbenchmark_usage.md)
- 消融实验说明：[ablation_usage](ablation_usage.md)
- 项目地图：[project_map](project_map.md)

## 目录

- [1. 适用范围](#1-适用范围)
- [2. 运行前准备](#2-运行前准备)
- [3. 推荐复跑顺序](#3-推荐复跑顺序)
- [4. Step 1: 主 benchmark 复跑](#4-step-1-主-benchmark-复跑)
- [5. Step 2: A/B 实验与汇总](#5-step-2-ab-实验与汇总)
- [6. Step 3: 单因素消融复跑](#6-step-3-单因素消融复跑)
- [7. Step 4: LayerwiseFT 专项分析](#7-step-4-layerwiseft-专项分析)
- [8. 预期输出目录树](#8-预期输出目录树)
- [9. 复跑后快速检查清单](#9-复跑后快速检查清单)

## 1. 适用范围

本文面向“从零开始复现当前项目完整实验链路”的场景，覆盖：

1. 主 benchmark 多 seed 复跑。
2. A/B 对照及汇总（含 adaptive 系列与 baseline/icbr 后端对照）。
3. 单因素消融矩阵。
4. LayerwiseFT 专项分析与改进版对比。

说明：

1. 常规 CLI 入口统一推荐使用 `python -m scripts.*`，不建议使用仓库根目录兼容 shim。
2. 工程版一键复测可使用 `scripts/run_engineering_rerun.ps1`，它是脚本编排封装入口，不属于 shim 入口。
3. 本文采用“手册示例输出”口径，默认写为 `outputs/rerun/`，用于避免覆盖既有 `outputs/benchmark_runs/`、`outputs/benchmark_ab/`、`outputs/benchmark_ablation/`。
4. 若需沿用“项目默认输出”口径，可将文中 `outputs/rerun/...` 替换为 `outputs/benchmark_*` 对应路径。

路径命名建议：

1. 通用复跑与流程演示：使用 `outputs/rerun/...`。
2. 工程版归档复测：使用 `scripts/run_engineering_rerun.ps1`，默认输出到 `outputs/rerun_v2_engine_safe_<date>/...`。

## 2. 运行前准备

默认约定：本文所有命令均在 `PowerShell` 环境下执行，代码块中的行续接符与参数换行也按 PowerShell 语法给出。

### 2.1 环境检查

推荐在仓库根目录执行：

```powershell
# 运行目录：仓库根目录（symkan-experiments/）
python --version
python -m pytest -q
python -m scripts.symkanbenchmark --help
python -m scripts.ablation_runner --help
python -m scripts.benchmark_ab_compare --help
```

预期结果：

1. `python --version` 显示 Python 3.9.x。
2. `python -m pytest -q` 全部通过。
3. 三个 CLI 的 `--help` 均可正常打印，且不出现导入失败或依赖缺失导致的提前退出。

本轮工程复测参考环境（用于结果解释）：

1. 操作系统：Windows 11 专业版 `23H2`（OS Build `22631.5472`）。
2. Python：`Miniconda` 的 `kan` 环境，解释器路径 `C:\Users\chenpeng\miniconda3\envs\kan\python.exe`（`3.9.25`）。
3. CPU：`12th Gen Intel(R) Core(TM) i5-12500H`。
4. 内存：`16 GB`。
5. 深度学习运行时：`PyTorch 2.1.2+cpu`（CPU 路径）。

### 2.2 数据检查

默认数据路径来自配置文件：

- `data/X_train.npy`
- `data/X_test.npy`
- `data/Y_train_cat.npy`
- `data/Y_test_cat.npy`

`scripts.symkanbenchmark` 也兼容旧版根目录路径 `X_train.npy`、`X_test.npy`、`Y_train_cat.npy`、`Y_test_cat.npy`；若配置中的 `data/` 路径不存在，会继续尝试这些 legacy 文件名。

若上述文件缺失且配置中 `data.auto_fetch_mnist: true`，脚本将尝试自动补齐 MNIST 数据。默认仅允许写入仓库 `data/` 目录；如需写入 `data/` 目录外路径，必须显式设置 `data.allow_auto_fetch_outside_data_dir: true`。

### 2.3 配置文件

当前仓库内置的配置模板与来源口径如下：

- 自动默认来源（仅一项）：
  - `configs/symkanbenchmark.default.yaml`
- 显式模板（需通过 `--config` 传入）：
  - `configs/ablation_runner.default.yaml`
  - `configs/benchmark_ab/baseline.yaml`
  - `configs/benchmark_ab/adaptive.yaml`
  - `configs/benchmark_ab/adaptive_auto.yaml`

其中 `configs/benchmark_ab/` 下的 3 份文件已按原始 A/B 实验口径预置，可直接使用。

若需在此基础上派生新的 A/B 变体，建议复制这三份模板后再修改，而非将差异重新分散到命令行参数中。

补充说明：

- `configs/symkanbenchmark.default.yaml` 是 `scripts.symkanbenchmark` 在未传 `--config` 时的默认来源。
- `configs/ablation_runner.default.yaml` 是给 `scripts.ablation_runner --config ...` 使用的共享 `AppConfig` 模板，不会在你省略 `--config` 时被自动选中。
- `configs/benchmark_ab/*.yaml` 是仓库内置的 A/B 变体模板，也都需要通过 `--config` 显式传入，不属于自动默认回退来源。
- 当前默认模板把 `stagewise.guard_mode` 设为 `light`（研究复跑优先）；做回归核对时可显式传 `--stage-guard-mode full`。
- 当前工程版模板把 `stagewise.prune_acc_drop_tol` 设为 `0.08`，用于降低过于保守回滚对时延的影响；若做严格回归，可临时降回更保守值。

## 3. 推荐复跑顺序

推荐顺序如下：

1. 先跑主 benchmark，确认基础链路和主要结果可复现。
2. 再跑 A/B 对照，并生成对比汇总表。
3. 再跑单因素消融矩阵。
4. 最后基于消融结果做 LayerwiseFT 专项分析。

若仅用于生成论文主表且不涉及性能专题分析，建议 `symkanbenchmark` 使用 `--tasks full`。

若还需补充 `eval-bench` 与 `parallel-bench` 结果，可将 `--tasks full` 改为 `--tasks all`，一次生成：

- `full`
- `eval-bench`
- `parallel-bench`

## 4. Step 1: 主 benchmark 复跑

### 4.1 主结果链路

```powershell
# 运行目录：仓库根目录（symkan-experiments/）
python -m scripts.symkanbenchmark `
  --config configs/symkanbenchmark.default.yaml `
  --tasks full `
  --stagewise-seeds 42,52,62 `
  --output-dir outputs/rerun/benchmark_runs `
  --quiet
```

若需补充 benchmark 专题分析，可将 `--tasks full` 改为：

```powershell
# 运行目录：仓库根目录（symkan-experiments/）
--tasks all
```

### 4.2 预期生成的文件

根目录下应至少包含：

- `outputs/rerun/benchmark_runs/symkanbenchmark_runs.csv`

每个 seed 对应一个 run 目录，例如：

- `outputs/rerun/benchmark_runs/run_01_seed42/`
- `outputs/rerun/benchmark_runs/run_02_seed52/`
- `outputs/rerun/benchmark_runs/run_03_seed62/`

每个 run 目录下应至少包含：

- `kan_stage_logs.csv`
- `kan_symbolic_summary.csv`
- `formula_validation.csv`
- `roc_auc_summary.csv`
- `symbolize_trace.csv`
- `metrics.json`

若使用 `--tasks all`，还会额外生成：

- `outputs/rerun/benchmark_runs/symkanbenchmark_eval_runs.csv`
- `outputs/rerun/benchmark_runs/symkanbenchmark_parallel_runs.csv`

以及每个 run 目录中的补充 benchmark 文件：

- `benchmark_single_round.csv`
- `benchmark_multi_round_raw.csv`
- `benchmark_multi_round_summary_cn.csv`
- `benchmark_multi_round_summary_en.csv`
- `benchmark_symbolic_parallel_quick.csv`

### 4.3 重点检查的结果文件

1. `symkanbenchmark_runs.csv`
   该文件是多 seed 主表，适合用于均值、方差与论文表格统计。
2. `metrics.json`
   该文件是单次 run 的结构化指标快照，同时记录符号化阶段的可观测性字段，例如：
  - `symbolic_abort_stage`
  - `symbolic_abort_reason`
  - `symbolic_abort_error_type`
  - `symbolic_warning_count`
  - `input_compaction_fallback`
  - `input_compaction_reason`
3. `symbolize_trace.csv`
   用于检查剪枝轮次、`drop_ratio` 与节奏异常。
4. `formula_validation.csv`
   用于检查导出公式的数值 `R²` 与数值稳定性。

## 5. Step 2: A/B 实验与汇总

### 5.1 跑常规 A/B 变体

常规 adaptive A/B 复跑：

- `configs/benchmark_ab/baseline.yaml`
- `configs/benchmark_ab/adaptive.yaml`
- `configs/benchmark_ab/adaptive_auto.yaml`

```powershell
# 运行目录：仓库根目录（symkan-experiments/）
python -m scripts.symkanbenchmark `
  --tasks full `
  --stagewise-seeds 42,52,62 `
  --config configs/benchmark_ab/baseline.yaml `
  --output-dir outputs/rerun/benchmark_ab/baseline `
  --quiet
```

```powershell
# 运行目录：仓库根目录（symkan-experiments/）
python -m scripts.symkanbenchmark `
  --tasks full `
  --stagewise-seeds 42,52,62 `
  --config configs/benchmark_ab/adaptive.yaml `
  --output-dir outputs/rerun/benchmark_ab/adaptive `
  --quiet
```

```powershell
# 运行目录：仓库根目录（symkan-experiments/）
python -m scripts.symkanbenchmark `
  --tasks full `
  --stagewise-seeds 42,52,62 `
  --config configs/benchmark_ab/adaptive_auto.yaml `
  --output-dir outputs/rerun/benchmark_ab/adaptive_auto `
  --quiet
```

### 5.2 baseline vs baseline_icbr 后端对照

若本轮目标是验证 ICBR 仅改变符号拟合后端，建议额外运行：

```powershell
# 运行目录：仓库根目录（symkan-experiments/）
python -m scripts.symkanbenchmark `
  --tasks full `
  --stagewise-seeds 42,52,62 `
  --config configs/benchmark_ab/baseline.yaml `
  --output-dir outputs/rerun_v2_engine_safe_20260401/benchmark_ab/baseline `
  --quiet
```

```powershell
# 运行目录：仓库根目录（symkan-experiments/）
python -m scripts.symkanbenchmark `
  --tasks full `
  --stagewise-seeds 42,52,62 `
  --config configs/benchmark_ab/baseline_icbr.yaml `
  --output-dir outputs/rerun_v2_engine_safe_20260401/benchmark_ab/baseline_icbr `
  --quiet
```

### 5.3 生成 A/B 汇总

```powershell
# 运行目录：仓库根目录（symkan-experiments/）
python -m scripts.benchmark_ab_compare `
  --root outputs/rerun/benchmark_ab `
  --baseline baseline `
  --variants adaptive,adaptive_auto `
  --output outputs/rerun/benchmark_ab/comparison
```

若本轮是 `baseline` vs `baseline_icbr` 后端对照，则改为：

```powershell
# 运行目录：仓库根目录（symkan-experiments/）
python -m scripts.benchmark_ab_compare `
  --root outputs/rerun_v2_engine_safe_20260401/benchmark_ab `
  --baseline baseline `
  --variants baseline_icbr `
  --output outputs/rerun_v2_engine_safe_20260401/benchmark_ab/comparison
```

### 5.4 预期生成的文件

三组实验各自会生成与 Step 1 相同结构的 benchmark 结果：

- `outputs/rerun/benchmark_ab/baseline/symkanbenchmark_runs.csv`
- `outputs/rerun/benchmark_ab/adaptive/symkanbenchmark_runs.csv`
- `outputs/rerun/benchmark_ab/adaptive_auto/symkanbenchmark_runs.csv`

汇总目录 `outputs/rerun/benchmark_ab/comparison/` 下应生成：

- `variant_summary.csv`
- `pairwise_delta_summary.csv`
- `seedwise_delta.csv`
- `trace_seedwise.csv`
- `trace_summary.csv`
- `comparison_summary.md`

若 compare 对是 `baseline` vs `baseline_icbr`，则还应额外生成：

- `baseline_icbr_shared_check.csv`
- `baseline_icbr_primary_effect.csv`
- `baseline_icbr_mechanism_summary.csv`

## 6. Step 3: 单因素消融复跑

### 6.1 跑消融矩阵

```powershell
# 运行目录：仓库根目录（symkan-experiments/）
python -m scripts.ablation_runner `
  --config configs/ablation_runner.default.yaml `
  --stagewise-seeds 42,52,62 `
  --output-dir outputs/rerun/benchmark_ablation `
  --quiet
```

默认会覆盖以下 5 个变体：

- `full`
- `wostagewise`
- `wopruning`
- `wocompact`
- `wolayerwiseft`

说明：

- 推荐显式传入 `--config configs/ablation_runner.default.yaml`，这样 5 个变体共享同一份基础 `AppConfig`。
- 若省略 `--config`，每个变体最终会回退到 `scripts.symkanbenchmark` 的默认配置来源，即 `configs/symkanbenchmark.default.yaml`。

### 6.2 只重新汇总已有结果

若各变体目录已存在且仅需重算总表，可执行：

```powershell
# 运行目录：仓库根目录（symkan-experiments/）
python -m scripts.ablation_runner `
  --aggregate-only `
  --output-dir outputs/rerun/benchmark_ablation
```

### 6.3 预期生成的文件

根目录应生成：

- `outputs/rerun/benchmark_ablation/ablation_runs_raw.csv`
- `outputs/rerun/benchmark_ablation/ablation_runs_summary.csv`

每个变体目录下应至少有：

- `symkanbenchmark_runs.csv`
- `run_01_seed42/`
- `run_02_seed52/`
- `run_03_seed62/`

而每个 run 目录内部结构与 Step 1 的单次 benchmark run 相同，至少包含：

- `kan_stage_logs.csv`
- `kan_symbolic_summary.csv`
- `formula_validation.csv`
- `roc_auc_summary.csv`
- `symbolize_trace.csv`
- `metrics.json`

## 7. Step 4: LayerwiseFT 专项分析

### 7.1 基于已有消融结果做专项分析

```powershell
# 运行目录：仓库根目录（symkan-experiments/）
python -m scripts.analyze_layerwiseft `
  --ablation-dir outputs/rerun/benchmark_ablation `
  --seeds 42,52,62
```

预期输出目录：

- `outputs/rerun/benchmark_ablation/layerwiseft_analysis/`

其中应包含：

- `run_level_comparison.csv`
- `class_level_comparison.csv`

### 7.2 跑改进版 LayerwiseFT 并做比较

```powershell
# 运行目录：仓库根目录（symkan-experiments/）
python -m scripts.compare_layerwiseft_improved `
  --ablation-dir outputs/rerun/benchmark_ablation `
  --seeds 42,52,62 `
  --quiet
```

若 `layerwiseft_esreg/` 已存在且仅需重新聚合：

```powershell
# 运行目录：仓库根目录（symkan-experiments/）
python -m scripts.compare_layerwiseft_improved `
  --ablation-dir outputs/rerun/benchmark_ablation `
  --seeds 42,52,62 `
  --skip-run
```

预期输出：

- `outputs/rerun/benchmark_ablation/layerwiseft_esreg/`
- `outputs/rerun/benchmark_ablation/layerwiseft_improved_analysis/comparison_raw.csv`
- `outputs/rerun/benchmark_ablation/layerwiseft_improved_analysis/comparison_summary.csv`
- `outputs/rerun/benchmark_ablation/layerwiseft_improved_analysis/delta_new_vs_full.csv`
- `outputs/rerun/benchmark_ablation/layerwiseft_improved_analysis/delta_new_vs_wolayerwiseft.csv`

补充说明：

- `scripts.compare_layerwiseft_improved` 当前不会额外读取一份 `AppConfig` YAML。
- 它运行 `layerwiseft_esreg` 时，会基于 `scripts.symkanbenchmark` 的默认配置来源，再叠加 layerwise 相关 CLI 覆盖与 `--global-seed`。

## 8. 预期输出目录树

若按本文全部跑完，`outputs/rerun/` 下大致会出现如下结构：

```plaintext
outputs/rerun/
  benchmark_runs/
    symkanbenchmark_runs.csv
    run_01_seed42/
    run_02_seed52/
    run_03_seed62/
  benchmark_ab/
    baseline/
      symkanbenchmark_runs.csv
    adaptive/
      symkanbenchmark_runs.csv
    adaptive_auto/
      symkanbenchmark_runs.csv
    comparison/
      variant_summary.csv
      pairwise_delta_summary.csv
      seedwise_delta.csv
      trace_seedwise.csv
      trace_summary.csv
      comparison_summary.md
  rerun_v2_engine_safe_20260401/
    benchmark_ab/
      baseline/
      baseline_icbr/
      comparison/
        variant_summary.csv
        pairwise_delta_summary.csv
        seedwise_delta.csv
        trace_seedwise.csv
        trace_summary.csv
        comparison_summary.md
        baseline_icbr_shared_check.csv
        baseline_icbr_primary_effect.csv
        baseline_icbr_mechanism_summary.csv
  benchmark_ablation/
    ablation_runs_raw.csv
    ablation_runs_summary.csv
    full/
    wostagewise/
    wopruning/
    wocompact/
    wolayerwiseft/
    layerwiseft_analysis/
      run_level_comparison.csv
      class_level_comparison.csv
    layerwiseft_esreg/
    layerwiseft_improved_analysis/
      comparison_raw.csv
      comparison_summary.csv
      delta_new_vs_full.csv
      delta_new_vs_wolayerwiseft.csv
```

## 9. 复跑后快速检查清单

复跑完成后，建议至少做以下检查：

1. `symkanbenchmark_runs.csv`、`ablation_runs_raw.csv`、`ablation_runs_summary.csv` 都能正常打开，且行数与 seed 数、变体数匹配。
2. 每个 `run_xx_seedyy/` 目录都存在 `metrics.json`、`symbolize_trace.csv`、`formula_validation.csv`。
3. 若某次 run 出现异常回退，检查对应 `metrics.json` 中的：
   - `symbolic_abort_stage`
   - `symbolic_abort_reason`
   - `input_compaction_fallback`
4. `outputs/rerun/benchmark_ab/comparison/comparison_summary.md` 已生成，表明通用 A/B 汇总链路执行成功。
5. 若本轮做了 ICBR 后端对照，还应确认 `outputs/rerun_v2_engine_safe_20260401/benchmark_ab/comparison/` 中：
   - `baseline_icbr_shared_check.csv` 已生成，且三条 seed 都为 `shared_symbolic_prep_aligned=True`
   - `trace_summary.csv` 中 `baseline` 与 `baseline_icbr` 的节奏一致
   - `baseline_icbr_primary_effect.csv` 与 `baseline_icbr_mechanism_summary.csv` 已生成
6. `outputs/rerun/benchmark_ablation/layerwiseft_analysis/` 与 `layerwiseft_improved_analysis/` 均有 CSV 输出，表明专项分析链路执行成功。

如需进一步解读结果，继续参考：

- [symkanbenchmark_usage.md](symkanbenchmark_usage.md)
- [ablation_usage.md](ablation_usage.md)
- [ablation_report.md](ablation_report.md)
- [layerwiseft_improved_report.md](layerwiseft_improved_report.md)
