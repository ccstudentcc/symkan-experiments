# TASK_STATUS

## Date
2026-03-30

## Task
完成 Stage 15：在 `quality` 配置下完成四任务（`minimal/combo/poly_cubic/trig_interaction`）启用剪枝的多变体 benchmark 扩展，并新增用于回应三类质疑的实证导出。

## Current Stage
Stage 15: Quality 4-Task Ablation Benchmark and Critique-Evidence Validation

## Status
Complete

## Latest Completed Work
- `kan/icbr.py`：
  - 完成多变体 ICBR benchmark 路径（`icbr_full / icbr_no_replay / icbr_no_shared / icbr_refit_commit`）并输出 replay rank inversion 与 refit drift 指标。
  - 新增 `benchmark_symbolic_variants(...)`，保留 `benchmark_icbr_vs_baseline(...)` 兼容层。
- `scripts/icbr_benchmark.py`：
  - 增加 `--variants` CLI 与变体归一化逻辑。
  - 增加 quality 下 synthetic 任务默认启用 teacher prune（可通过 `--enable-teacher-prune/--disable-teacher-prune` 覆盖），并支持 prune 阈值参数。
  - 主 rows 导出补齐三类质疑证据字段（Q1/Q2/Q3）。
  - 新增 `icbr_benchmark_variant_rows.csv` 明细导出与 summary 中 `variant_ablation`、`challenge_evidence` 聚合结构。
  - Markdown 汇总新增 “Variant Ablation Aggregate Stats” 与 “Critique Evidence Summary” 区块。
  - 修正 profile defaults：`quality` 使用 `train=1000/test=500/steps=80/lr=0.03/lamb=1e-3`，`feynman_reference` 默认 `lamb=1e-2`，Feynman post-prune 默认 `lamb=1e-2`。
- 测试补充：
  - `tests/test_icbr_benchmark_smoke.py` 增加 `benchmark_symbolic_variants` 结构检查。
  - `tests/test_icbr_benchmark_script_smoke.py` 增加变体导出、聚合结构、quality 默认 prune、variant 解析等断言。
- 实跑 Stage 15 最小多变体 benchmark（4 tasks × 2 seeds）并生成完整产物。

## Files Changed
- kan/icbr.py
- scripts/icbr_benchmark.py
- tests/test_icbr_benchmark_smoke.py
- tests/test_icbr_benchmark_script_smoke.py
- IMPLEMENTATION_PLAN.md
- TASK_STATUS.md

## Validation Run
- `C:\Users\chenpeng\miniconda3\envs\kan\python.exe -m py_compile scripts/icbr_benchmark.py kan/icbr.py tests/test_icbr_benchmark_smoke.py tests/test_icbr_benchmark_script_smoke.py`
- `C:\Users\chenpeng\miniconda3\envs\kan\python.exe -m pytest tests/test_icbr_benchmark_smoke.py tests/test_icbr_benchmark_script_smoke.py`
- `C:\Users\chenpeng\miniconda3\envs\kan\python.exe -m scripts.icbr_benchmark --profile quality --tasks minimal,combo,poly_cubic,trig_interaction --seeds 0,1 --variants baseline,icbr_full,icbr_no_replay,icbr_no_shared,icbr_refit_commit --output-dir outputs/icbr_benchmark_stage15_quality_ablation_4tasks --teacher-cache-dir outputs/teacher_cache_stage15_quality --teacher-cache-mode readwrite --teacher-cache-version stage15_v1 --quiet --no-plots`
- `C:\Users\chenpeng\miniconda3\envs\kan\python.exe -c "import json, pathlib; ..."`（核对 summary 中 variants / prune policy / challenge evidence / variant ablation 聚合）

## Validation Result
- `py_compile` 通过。
- `pytest` 通过：`15 passed`。
- Stage 15 实跑成功，产物齐全：
  - `outputs/icbr_benchmark_stage15_quality_ablation_4tasks/icbr_benchmark_rows.csv`
  - `outputs/icbr_benchmark_stage15_quality_ablation_4tasks/icbr_benchmark_variant_rows.csv`
  - `outputs/icbr_benchmark_stage15_quality_ablation_4tasks/icbr_benchmark_task_stats.csv`
  - `outputs/icbr_benchmark_stage15_quality_ablation_4tasks/icbr_benchmark_significance.csv`
  - `outputs/icbr_benchmark_stage15_quality_ablation_4tasks/icbr_benchmark_summary.json`
  - `outputs/icbr_benchmark_stage15_quality_ablation_4tasks/icbr_benchmark_summary.md`
- 实跑摘要（overall）：
  - `teacher_quality_gate_pass_mean = 1.0`
  - `formula_validation_result_mean = 1.0`
  - `symbolic_speedup_vs_baseline_mean = 12.0505`
  - `final_mse_loss_shift_mean = 1.1204e-04`
  - Q1 证据：`candidate_time_ratio_no_shared_vs_full_mean = 2.2337`，`symbolic_time_ratio_no_shared_vs_full_mean = 1.9730`
  - Q2 证据：`mse_gain_full_vs_no_replay_mean = 2.0898e-04`，`rank_inversion_rate_full_mean = 0.3203`
  - Q3 证据：`mse_gain_explicit_vs_refit_mean = 3.6036e-02`，`refit_commit_param_drift_l2_mean = 7.3421`

## Decisions
- 保持 baseline/icbr_full 主导出兼容；多变体能力通过新增导出结构追加，不替换旧字段。
- Stage 15 quality 对 synthetic 任务默认启用 prune，以满足“启用剪枝”约束；同时保留 CLI 开关确保可控与可复现实验。
- 三类质疑证据统一同时写入 rows（行级）与 summary 聚合（overall/by_task），并在 markdown 直接展示。

## Remaining Work
- Stage 15 已完成；待用户确认是否进入下一个 stage（例如更大 seeds/任务集或专门围绕 trig_interaction 的进一步稳定性调优）。

## Blockers
- 无
