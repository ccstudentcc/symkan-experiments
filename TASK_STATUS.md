# TASK_STATUS

## Date
2026-03-29

## Task
推进 Stage 10：补充高质量数值教师 profile，并完成 10 seeds 全任务门禁复验。

## Current Stage
Stage 10: Calibrate Teacher Convergence and Run 10-Seed Full-Task Verification

## Status
Complete

## Latest Completed Work
- `scripts/icbr_benchmark.py`：
  - 新增 benchmark profile 机制：`--profile quick|quality`。
  - 新增训练配置解析 helper（支持 profile 默认值 + CLI 覆盖）。
  - 训练参数新增 `--lamb`，并将其传入 `model.fit(..., lamb=...)`。
  - summary 新增 `config.profile`（含 `name/defaults/overrides`）并记录 `lamb`。
  - markdown 报告的 run config 增加 `profile` 与 `lamb` 展示。
- `tests/test_icbr_benchmark_script_smoke.py`：
  - 覆盖 `profile` 字段与 override 结构。
  - 新增 `quality` profile 默认参数解析测试（含 `lamb`）。
  - 同步 `run_benchmark(...)` 调用，显式传入 `lamb`。
- 完成实跑验证（你指定参数）：
  - `train_num=2000`
  - `test_num=1000`
  - `lamb=1e-3`
  - 10 seeds + 全任务 + 全量函数库
  - regression gate 通过
- 已基于该次实跑结果生成可视化 PNG，并回写 `summary.json` 的 `artifacts.visualizations`。

## Files Changed
- IMPLEMENTATION_PLAN.md
- scripts/icbr_benchmark.py
- tests/test_icbr_benchmark_script_smoke.py
- TASK_STATUS.md

## Validation Run
- `C:\Users\chenpeng\miniconda3\envs\kan\python.exe -m pytest tests\test_icbr_benchmark_script_smoke.py`
- `C:\Users\chenpeng\miniconda3\envs\kan\python.exe -m pytest tests\test_icbr_benchmark_smoke.py tests\test_icbr_benchmark_script_smoke.py tests\test_icbr_benchmark_regression_smoke.py`
- `C:\Users\chenpeng\miniconda3\envs\kan\python.exe -m scripts.icbr_benchmark --profile quality --train-num 2000 --test-num 1000 --lamb 1e-3 --output-dir outputs\icbr_benchmark_stage10_quality_10seeds_2000_1000_l1e3 --quiet --no-plots`
- `C:\Users\chenpeng\miniconda3\envs\kan\python.exe -m scripts.icbr_benchmark_regression --summary-json outputs\icbr_benchmark_stage10_quality_10seeds_2000_1000_l1e3\icbr_benchmark_summary.json --output-dir outputs\icbr_benchmark_stage10_quality_10seeds_2000_1000_l1e3`
- `C:\Users\chenpeng\miniconda3\envs\kan\python.exe -c "from scripts.icbr_benchmark import _generate_visualizations; ..."`（对既有 rows 生成 PNG 并回写 summary）

## Validation Result
- 通过：`pytest` 脚本 smoke（4 项）全部通过。
- 通过：benchmark 相关 smoke（7 项）全部通过。
- 通过：10 seeds 全任务实跑完成并落盘。
- 通过：regression gate `overall_status=pass`（退出码 0）。
- 关键结果（`outputs/icbr_benchmark_stage10_quality_10seeds_2000_1000_l1e3`）：
  - overall `teacher_quality_gate_pass.mean = 1.0`
  - overall `teacher_test_mse.mean = 1.4907e-03`
  - overall `teacher_test_r2.mean = 0.9970`
  - overall `symbolic_speedup_vs_baseline.median = 13.5790`
  - overall `final_mse_loss_shift.mean = -7.7933e-05`
  - overall `symbolic_target_mse_shift.mean = -7.6226e-05`
- 已生成图：
  - `icbr_benchmark_symbolic_time_errorbar.png`
  - `icbr_benchmark_speedup_boxplot.png`
  - `icbr_benchmark_mse_shift_boxplot.png`

## Decisions
- 继续维持“只改 benchmark/regression 层，不改 ICBR 主路径”。
- `quality` profile 固化为更强训练口径（80 steps、更大样本、`lamb=1e-3`）。
- 你指定的 `train=2000/test=1000/lamb=1e-3` 优先于 profile 默认值，并在 summary 中显式记录为 override。
- 为避免重复长时训练，图表基于已落盘 rows 二次生成并同步写回 summary。

## Remaining Work
- 当前 Stage 10 已完成。
- 下一步建议：新增 Stage 11，围绕 `quality + 大样本` 结果做统计显著性门限细化（例如按任务单独阈值与置信区间门禁）。

## Blockers
- 无
