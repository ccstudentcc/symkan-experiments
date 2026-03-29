# TASK_STATUS

## Date
2026-03-29

## Task
在 Phase I 已完成基础上，落实扩展验证里程碑：多 seeds、更大任务集、统计显著性与可视化汇总。

## Current Stage
Stage 6: Extended Multi-Seed Benchmark Validation

## Status
Complete

## Latest Completed Work
- 在 `IMPLEMENTATION_PLAN.md` 新增并落地 Stage 6，明确扩展验证的范围、统计口径与验收要求。
- 重构 `scripts/icbr_benchmark.py`，支持扩展任务集：`minimal`、`combo`、`poly_cubic`、`trig_interaction`。
- benchmark 脚本默认支持多 seed 运行（默认 `0,1,2,3,4`），并继续保留 rows 级明细。
- 新增 task 聚合统计结构：每个核心指标都输出 `count | mean | median | std | min | max`。
- 新增统计显著性输出（按 task）：
  - `symbolic_wall_time_delta_s`（正向更优）
  - `final_mse_loss_shift`（负向更优）
  - 输出 two-sided sign test p-value、bootstrap mean CI95、improved/worsened/tie 计数。
- 新增导出产物：
  - `icbr_benchmark_task_stats.csv`（任务级统计）
  - `icbr_benchmark_significance.csv`（显著性摘要）
  - 可视化 PNG（时间误差条、speedup 箱线图、mse_shift 箱线图）
- 更新 Markdown 汇报，增加：
  - Task-Level Aggregate Stats（含均值/中位数/标准差）
  - Statistical Significance（每任务显著性对照）
  - Visualization Summary（图文件索引）
- 更新 `tests/test_icbr_benchmark_script_smoke.py`：
  - 改为双 seed smoke（`0,1`）
  - 校验新聚合结构与新增导出文件存在性。

## Files Changed
- IMPLEMENTATION_PLAN.md
- scripts/icbr_benchmark.py
- tests/test_icbr_benchmark_script_smoke.py
- TASK_STATUS.md

## Validation Run
- `C:\Users\chenpeng\miniconda3\envs\kan\python.exe -m pytest tests\test_icbr_benchmark_smoke.py tests\test_icbr_benchmark_script_smoke.py`
- `C:\Users\chenpeng\miniconda3\envs\kan\python.exe -m scripts.icbr_benchmark --tasks minimal,combo,poly_cubic,trig_interaction --seeds 0,1,2 --output-dir outputs\icbr_benchmark_extended --train-num 64 --test-num 64 --train-steps 8 --lr 0.05 --topk 3 --grid-number 21 --iteration 2 --quiet`

## Validation Result
- 通过：benchmark 相关测试 2 项全部通过。
- 通过：扩展 benchmark 实跑成功，产出：
  - `outputs/icbr_benchmark_extended/icbr_benchmark_rows.csv`
  - `outputs/icbr_benchmark_extended/icbr_benchmark_task_stats.csv`
  - `outputs/icbr_benchmark_extended/icbr_benchmark_significance.csv`
  - `outputs/icbr_benchmark_extended/icbr_benchmark_summary.json`
  - `outputs/icbr_benchmark_extended/icbr_benchmark_summary.md`
  - `outputs/icbr_benchmark_extended/icbr_benchmark_symbolic_time_errorbar.png`
  - `outputs/icbr_benchmark_extended/icbr_benchmark_speedup_boxplot.png`
  - `outputs/icbr_benchmark_extended/icbr_benchmark_mse_shift_boxplot.png`

## Decisions
- 只扩展 benchmark/report 层，不改动 ICBR 算法路径，避免引入额外变量。
- 显著性采用轻量且可复现的两类方法：sign test（方向性）+ bootstrap CI（效应区间）。
- 保持 rows 明细不丢失，聚合与显著性仅作为额外视图，便于后续误差条与统计检验复用。

## Remaining Work
- Stage 6 已完成。
- 下一步建议：补充更高 seed 数（例如 `0..9`）并沉淀固定对比报告模板，用于跨版本回归。

## Blockers
- 无
