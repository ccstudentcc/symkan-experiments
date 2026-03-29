# TASK_STATUS

## Task
按 `IMPLEMENTATION_PLAN.md` 推进 ICBR-KAN Phase I，并完成当前首个可执行 stage。

## Current Stage
Stage 5: Benchmark and Verify Phase I Claims

## Status
Complete

## Latest Completed Work
- 在 `kan/icbr.py` 新增 `_clone_model_memory(...)`，替换 benchmark 路径中的 `copy.deepcopy(model)`，避免 `fit()` 后非叶子缓存导致 deepcopy 失败。
- 在 `kan/icbr.py` 的 benchmark 指标中补充 baseline 对照信息：
  - `baseline_symbolic_wall_time_s`
  - `symbolic_speedup_vs_baseline`
  - `baseline_formula_validation_result`
  - `icbr_formula_validation_result`
- 新增 `scripts/icbr_benchmark.py`，在 `scripts/` 下提供可执行的最小 benchmark 脚本（minimal + combo 任务、baseline vs ICBR 对照、CSV/JSON/Markdown 落盘）。
- 新增计时聚合：
  - `candidate_generation_wall_time_s`
  - `replay_rerank_wall_time_s`
  - `symbolic_wall_time_s`
- 新增最小对照指标：
  - `replay_imitation_gap`
  - `final_mse_loss_shift`
  - `formula_validation_result`
  - `baseline_symbolic_wall_time_s`
  - `baseline_mse` / `icbr_mse`
- 在 `tests/test_icbr_benchmark_smoke.py` 增加 smoke 验证，确保上述关键指标可生成且数值有效。
- 新增 `tests/test_icbr_benchmark_script_smoke.py`，验证脚本可执行且产出包含 baseline 字段的结果文件。

## Files Changed
- kan/icbr.py
- scripts/icbr_benchmark.py
- tests/test_icbr_benchmark_smoke.py
- tests/test_icbr_benchmark_script_smoke.py
- IMPLEMENTATION_PLAN.md
- TASK_STATUS.md

## Validation Run
- `C:\Users\chenpeng\miniconda3\envs\kan\python.exe -m pytest tests\test_icbr_candidates.py tests\test_icbr_replay.py tests\test_icbr_commit.py tests\test_icbr_integration.py tests\test_icbr_benchmark_smoke.py`
- `C:\Users\chenpeng\miniconda3\envs\kan\python.exe -m pytest tests\test_icbr_benchmark_smoke.py tests\test_icbr_benchmark_script_smoke.py`
- `C:\Users\chenpeng\miniconda3\envs\kan\python.exe -m scripts.icbr_benchmark --tasks minimal,combo --seeds 0 --output-dir outputs\icbr_benchmark_smoke --train-num 64 --test-num 64 --train-steps 8 --lr 0.05 --topk 3 --grid-number 21 --iteration 2 --quiet`

## Validation Result
- 通过：`tests/test_icbr_candidates.py` + `tests/test_icbr_replay.py` + `tests/test_icbr_commit.py` + `tests/test_icbr_integration.py` + `tests/test_icbr_benchmark_smoke.py` 共 13 项，13 项通过。
- 通过：脚本相关测试 2 项全部通过；`scripts.icbr_benchmark` 实跑成功并产出：
  - `outputs/icbr_benchmark_smoke/icbr_benchmark_rows.csv`
  - `outputs/icbr_benchmark_smoke/icbr_benchmark_summary.json`
  - `outputs/icbr_benchmark_smoke/icbr_benchmark_summary.md`

## Decisions
- Stage 5 采用“最小可复现 benchmark smoke”策略，不引入额外脚本，先通过测试固定核心指标接口。
- baseline 与 ICBR 都基于同一输入与同一模型拷贝体系，避免统计口径混用。
- 现阶段以 CPU 路线和单测 smoke 验收为主，后续再扩展到更大任务对照。

## Remaining Work
- Phase I 五个 stage 已全部完成。
- 下一步建议：补充更大任务规模的 benchmark 结果落盘与汇总文档（例如独立 markdown 报告或 CSV 产物）。

## Blockers
- 无
