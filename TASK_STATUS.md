# TASK_STATUS

## Date
2026-03-29

## Task
推进 Stage 9：新增数值教师质量门禁，并补充符号模型对真实目标函数误差指标。

## Current Stage
Stage 9: Add Teacher Quality Gate and Target-Error Metrics

## Status
Complete

## Latest Completed Work
- `kan/icbr.py`：
  - 为 `benchmark_icbr_vs_baseline` 新增真实目标误差指标导出。
  - 新增 `teacher/baseline/icbr` 对真实目标的 `MSE/R2` 与 `symbolic_target_mse_shift`、`symbolic_target_r2_shift`。
  - 保持原有 imitation 指标不变，兼容无标签调用（返回 NaN）。
- `scripts/icbr_benchmark.py`：
  - 新增 teacher 数值质量门禁（`teacher_test_mse`、`teacher_test_r2` 对阈值判定）。
  - 行级新增 `teacher_quality_gate_pass` 与 `teacher_quality_gate_reason`。
  - 门禁失败时按策略跳过 baseline/ICBR 符号化对比并显式导出跳过原因。
  - CSV/JSON/Markdown 增加 target-error 与门禁字段；聚合统计对 NaN 做稳健处理。
  - 可视化对“全部被门禁跳过”场景增加安全兜底，不再异常中断。
  - CLI 新增 `--teacher-max-test-mse` 与 `--teacher-min-test-r2`。
- `scripts/icbr_benchmark_regression.py`：
  - 新增回归检查项：`teacher_quality_gate_pass`（mean 下限）与 `symbolic_target_mse_shift`（mean 上限）。
  - 新增 CLI 门禁阈值：`--min-teacher-quality-gate-pass-rate`、`--max-target-mse-shift-mean`。
  - 对 non-finite 聚合值给出明确 fail reason。
- 测试更新：
  - `tests/test_icbr_benchmark_smoke.py` 校验 target-error 新指标。
  - `tests/test_icbr_benchmark_script_smoke.py` 校验新导出列、门禁配置与“门禁跳过”路径。
  - `tests/test_icbr_benchmark_regression_smoke.py` 覆盖新门禁检查字段。
- 文档同步：
  - `IMPLEMENTATION_PLAN.md` Stage 9 标记为 `Complete` 并补充验证口径。

## Files Changed
- IMPLEMENTATION_PLAN.md
- kan/icbr.py
- scripts/icbr_benchmark.py
- scripts/icbr_benchmark_regression.py
- tests/test_icbr_benchmark_smoke.py
- tests/test_icbr_benchmark_script_smoke.py
- tests/test_icbr_benchmark_regression_smoke.py
- TASK_STATUS.md

## Validation Run
- `C:\Users\chenpeng\miniconda3\envs\kan\python.exe -m py_compile kan\icbr.py scripts\icbr_benchmark.py scripts\icbr_benchmark_regression.py tests\test_icbr_benchmark_smoke.py tests\test_icbr_benchmark_script_smoke.py tests\test_icbr_benchmark_regression_smoke.py`
- `C:\Users\chenpeng\miniconda3\envs\kan\python.exe -m pytest tests\test_icbr_benchmark_smoke.py tests\test_icbr_benchmark_script_smoke.py tests\test_icbr_benchmark_regression_smoke.py`
- `C:\Users\chenpeng\miniconda3\envs\kan\python.exe -m scripts.icbr_benchmark --tasks minimal,combo --seeds 0,1 --output-dir outputs\icbr_benchmark_stage9_smoke --train-num 24 --test-num 24 --train-steps 4 --lr 0.05 --topk 2 --grid-number 11 --iteration 1 --quiet`
- `C:\Users\chenpeng\miniconda3\envs\kan\python.exe -m scripts.icbr_benchmark_regression --summary-json outputs\icbr_benchmark_stage9_smoke\icbr_benchmark_summary.json --output-dir outputs\icbr_benchmark_stage9_smoke`
- `C:\Users\chenpeng\miniconda3\envs\kan\python.exe -m scripts.icbr_benchmark --tasks minimal,combo --seeds 0,1 --output-dir outputs\icbr_benchmark_stage9_smoke_pass --train-num 24 --test-num 24 --train-steps 4 --lr 0.05 --topk 2 --grid-number 11 --iteration 1 --teacher-max-test-mse 1.0 --teacher-min-test-r2 -1.0 --quiet`
- `C:\Users\chenpeng\miniconda3\envs\kan\python.exe -m scripts.icbr_benchmark_regression --summary-json outputs\icbr_benchmark_stage9_smoke_pass\icbr_benchmark_summary.json --output-dir outputs\icbr_benchmark_stage9_smoke_pass --min-formula-pass-rate 0.0 --min-speedup-median 0.0 --max-mse-shift-mean 1.0 --min-teacher-quality-gate-pass-rate 0.0 --max-target-mse-shift-mean 1.0`

## Validation Result
- 通过：`py_compile` 无语法错误。
- 通过：`pytest`（6 项）全部通过。
- 通过：Stage 9 benchmark 脚本成功产出新结构导出（rows/csv/json/md）。
- 通过（预期）：在默认门禁阈值 + 快速训练配置下，regression gate 返回 `fail`，且 fail reason 明确显示 teacher 质量门禁未通过与非有限统计值。
- 通过：放宽阈值后，regression gate 返回 `pass`，验证新门禁链路可执行且可判定。

## Decisions
- 维持“只改 benchmark/regression 层，不改 ICBR 主路径”。
- teacher 质量门禁采用“先判定再执行符号化”的策略，避免低质量 teacher 污染符号对比结论。
- 任务级阈值采用“支持覆盖但默认不写死”，以 CLI 全局阈值为默认主入口。
- 对门禁跳过导致的 NaN 统计，聚合与可视化均做显式兜底，保证导出稳定。

## Remaining Work
- 当前 Stage 9 已完成。
- 下一步建议：进入下一阶段，将 10 seeds + 全任务集作为常规口径运行，并基于新门禁输出调优数值训练配置（提高 teacher gate pass rate）。

## Blockers
- 无
