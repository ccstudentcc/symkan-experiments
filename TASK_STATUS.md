# TASK_STATUS

## Date
2026-03-29

## Task
推进 Stage 8：定位并修复 `trig_interaction` 回归，在 10 seeds 条件下完成 benchmark 与 regression gate 复验。

## Current Stage
Stage 8: Diagnose and Fix `trig_interaction` Regression

## Status
Complete

## Latest Completed Work
- 在 `IMPLEMENTATION_PLAN.md` 新增并执行 Stage 8。
- 先完成诊断实验（10 seeds, `trig_interaction`）：
  - 发现只提升 replay `topk`（3 -> 5）可显著改善 `mse_shift_mean`。
  - 在全量函数库 `SYMBOLIC_LIB` 下，`trig_interaction` 的 `mse_shift_mean` 为负，且 speedup 仍满足门禁目标。
- 按最小范围落地修复（`scripts/icbr_benchmark.py`）：
  - 所有任务切换为全量函数库（`lib=None` -> `SYMBOLIC_LIB`）。
  - 保留 `trig_interaction` 的任务级 replay 参数覆盖：`icbr_topk=5`。
  - benchmark 行级导出新增 `icbr_topk_used`，并在 config 增加 `task_lib_mode`、`task_topk_overrides`。
  - 默认 seeds 改为 `0..9`（10 seeds）。
- 更新 `tests/test_icbr_benchmark_script_smoke.py`：
  - 验证 `minimal/combo` 结果标记为全量函数库模式。
  - 新增 `trig_interaction` 任务级 `topk` 覆盖测试（确认 `icbr_topk_used == 5`）。

## Files Changed
- IMPLEMENTATION_PLAN.md
- scripts/icbr_benchmark.py
- tests/test_icbr_benchmark_script_smoke.py
- TASK_STATUS.md

## Validation Run
- `C:\Users\chenpeng\miniconda3\envs\kan\python.exe -m pytest tests\test_icbr_benchmark_smoke.py tests\test_icbr_benchmark_script_smoke.py tests\test_icbr_benchmark_regression_smoke.py`
- `C:\Users\chenpeng\miniconda3\envs\kan\python.exe -m scripts.icbr_benchmark --tasks minimal,combo,poly_cubic,trig_interaction --seeds 0,1,2,3,4,5,6,7,8,9 --output-dir outputs\icbr_benchmark_stage8_10seeds --train-num 64 --test-num 64 --train-steps 8 --lr 0.05 --topk 3 --grid-number 21 --iteration 2 --quiet`
- `C:\Users\chenpeng\miniconda3\envs\kan\python.exe -m scripts.icbr_benchmark_regression --summary-json outputs\icbr_benchmark_stage8_10seeds\icbr_benchmark_summary.json --output-dir outputs\icbr_benchmark_stage8_10seeds`

## Validation Result
- 通过：benchmark + regression 相关测试共 5 项全部通过。
- 通过：10 seeds 扩展 benchmark 实跑成功并产出 summary/rows/stats/significance/plots。
- 通过：Stage 7 regression gate 在 Stage 8 新结果上 `overall_status=pass`（退出码 0）。
- 关键结果（10 seeds）：
  - overall `symbolic_speedup_vs_baseline.median = 3.6636`
  - overall `final_mse_loss_shift.mean = -2.4557e-4`
  - `trig_interaction` `final_mse_loss_shift.mean = -7.9553e-4`

## Decisions
- 修复不采用缩库策略；对齐日常使用口径，统一采用全量 `SYMBOLIC_LIB`。
- 仅在 `trig_interaction` 做任务级 `topk` 调优（`5`），避免扩张到算法主路径。
- 继续保留 rows 明细与 Stage 6/7 全部导出结构，确保可回归对比。

## Remaining Work
- Stage 8 已完成。
- 下一步建议：新增 Stage 9（长期稳定性），将 10 seeds 结果固化为基线快照并接入 CI 门禁。

## Blockers
- 无
