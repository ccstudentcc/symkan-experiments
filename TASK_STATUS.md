# TASK_STATUS

## Date
2026-03-30

## Task
完成 Stage 17：Multi-Variant Formula Report Completeness Fix。

## Current Stage
Stage 17: Multi-Variant Formula Report Completeness Fix

## Status
Complete

## Latest Completed Work
- `scripts/icbr_benchmark.py`：
  - `Formula Comparison` 改为按 `config.variants` 渲染每个 `task+seed` 的全部变体。
  - 新增变体级摘要（`symbolic_s/mse/target_mse/formula_ok`）与每个变体的 display/raw 公式输出。
  - 当变体缺失或被 gate 跳过时，显式写出 `missing`/`<none>`/`formula_error`，避免信息静默丢失。
- `tests/test_icbr_benchmark_script_smoke.py`：
  - 增加断言，确保包含 `icbr_no_replay` 的运行在 `summary.md` 里出现 `icbr_no_replay formula (display, rounded)`。
  - 新增 teacher gate 跳过场景断言，确保请求变体在 `Formula Comparison` 中仍完整可见，且包含跳过错误信息。

## Files Changed
- scripts/icbr_benchmark.py
- tests/test_icbr_benchmark_script_smoke.py
- IMPLEMENTATION_PLAN.md
- TASK_STATUS.md

## Validation Run
- `C:\Users\chenpeng\miniconda3\envs\kan\python.exe -m py_compile scripts/icbr_benchmark.py tests/test_icbr_benchmark_script_smoke.py`
- `C:\Users\chenpeng\miniconda3\envs\kan\python.exe -m pytest tests/test_icbr_benchmark_script_smoke.py -k "variants or generates_outputs or formula_comparison"`

## Validation Result
- `py_compile` 通过。
- 目标测试通过：`4 passed, 11 deselected`（`variants/generates_outputs/formula_comparison` 相关用例）。
- `Formula Comparison` 现可覆盖所有启用变体；在 teacher gate 跳过时也不会静默丢失变体信息。

## Decisions
- 不改 summary JSON 主结构，仅修复 markdown 渲染层，确保变体信息不丢失。
- 保持 `rows` 与 `variant_rows` 为机器可读真源，`summary.md` 专注人类可读汇报。

## Remaining Work
- Stage 16 已完成（10-seed 扩展验证）。
- Stage 17 已完成（多变体公式报告完整性修复）。
- Stage 18 未开始（可视化升级）。

## Blockers
- 无
