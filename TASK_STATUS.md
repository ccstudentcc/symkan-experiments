# TASK_STATUS

## Date
2026-03-29

## Task
完成 Stage 13 收口补充：固定 Feynman 数据随机种子默认值，并把公式/数据集元数据贯通到 benchmark 导出与 Markdown 报告。

## Current Stage
Stage 13: Add Feynman Reference Preset and Prune-Refit Teacher Flow

## Status
Complete

## Latest Completed Work
- 将 Feynman 随机相关默认值固定为可复现口径：
  - `feynman_dataset_select_seed=1`
  - `feynman_split_strategy_seed=1`
- 将 Feynman train/test 切分随机性从运行 seed 解耦：
  - random split 使用 `feynman_split_strategy_seed`
  - run seed 继续用于模型训练随机性
- 扩展 Feynman 任务规格与导出字段，新增并贯通：
  - `feynman_dataset_filename`
  - `feynman_dataset_rows`
  - `feynman_dataset_columns`
  - `feynman_split_seed`
  - `feynman_equation_metadata`
- 增强 `FeynmanEquations.csv` 解析：
  - 保留按公式文件名匹配公式表达式
  - 透传整行元数据到 summary/rows
  - 清理 BOM 字段名，避免 `﻿Filename` 污染报告字段
- 增强 `icbr_benchmark_summary.md`：
  - Run Config 显示 `split_seed` / `select_seed`
  - 新增 `Feynman Dataset Metadata` 章节，展示每个公式任务的数据文件、样本规模、变量数、切分参数与 CSV 元信息
- 完成真实本地数据链路验证（`datasets/Feynman_with_units` + `datasets/FeynmanEquations.csv`）并生成报告产物。

## Files Changed
- scripts/icbr_benchmark.py
- tests/test_icbr_benchmark_script_smoke.py
- IMPLEMENTATION_PLAN.md
- TASK_STATUS.md

## Validation Run
- `C:\Users\chenpeng\miniconda3\envs\kan\python.exe -m py_compile scripts\icbr_benchmark.py tests\test_icbr_benchmark_script_smoke.py`
- `C:\Users\chenpeng\miniconda3\envs\kan\python.exe -m pytest tests\test_icbr_benchmark_script_smoke.py`
- `C:\Users\chenpeng\miniconda3\envs\kan\python.exe -m pytest tests\test_icbr_benchmark_smoke.py tests\test_icbr_benchmark_script_smoke.py tests\test_icbr_benchmark_regression_smoke.py`
- `C:\Users\chenpeng\miniconda3\envs\kan\python.exe -m scripts.icbr_benchmark --tasks feynman_I_10_7 --seeds 1 --output-dir outputs/icbr_benchmark_feynman_metadata_smoke --train-num 64 --test-num 32 --train-steps 4 --lr 0.03 --lamb 1e-3 --topk 2 --grid-number 11 --iteration 1 --teacher-max-test-mse 10 --teacher-min-test-r2 -10 --feynman-root datasets --feynman-variant Feynman_with_units --feynman-split-strategy random --quiet --no-plots`

## Validation Result
- `py_compile` 通过
- 脚本 smoke 测试通过：`9 passed`
- benchmark 回归 smoke 测试通过：`12 passed`
- 真实数据最小实跑成功，报告产物已生成：
  - `outputs/icbr_benchmark_feynman_metadata_smoke/icbr_benchmark_summary.json`
  - `outputs/icbr_benchmark_feynman_metadata_smoke/icbr_benchmark_summary.md`
- 已确认 Markdown 报告包含：
  - `Feynman Dataset Metadata` 章节
  - 公式任务名、目标公式、数据文件名、样本规模、切分 seed 与 CSV 元数据

## Decisions
- 保持“只改 benchmark 层，不改 ICBR 主算法路径”。
- 为保证多次运行与跨任务可复现，Feynman 数据子集选择 seed 与随机切分 seed 默认统一为 `1`。
- 将 Feynman 元数据直接进 `summary.config.feynman.task_metadata` 与 rows 级字段，保证 JSON/CSV/MD 三种导出一致可追溯。

## Remaining Work
- 使用 `--profile feynman_reference` 对 `feynman_paper10` 执行完整参考配置实跑（2000/1000, steps=200, prune+refit）。
- 在完整 Feynman 多任务结果上执行后续多 seed 聚合与回归门禁复验。

## Blockers
- 无
