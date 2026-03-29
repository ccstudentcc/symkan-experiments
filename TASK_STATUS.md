# TASK_STATUS

## Date
2026-03-29

## Task
完成 Stage 11：增加跨脚本多次运行可复用的 teacher 持久缓存，并完成 quality 参数口径验证。

## Current Stage
Stage 11: Add Cross-Run Persistent Teacher Cache

## Status
Complete

## Latest Completed Work
- 在 `scripts/icbr_benchmark.py` 实现 teacher 持久缓存主流程：
  - 缓存 key（覆盖 task/seed/width/train_num/test_num/train_steps/lr/lamb/profile/cache_version）
  - 缓存模式（`readwrite`/`readonly`/`refresh`/`off`）
  - 原子写入与锁文件（`teacher_state.pt`、`teacher_meta.json`、`teacher_cache.lock`）
  - 行级与汇总可观测字段（`teacher_cache_hit`、`teacher_cache_key`、`teacher_cache_path`、`teacher_cache_mode`、`teacher_cache_status`）
- benchmark summary 新增 `config.teacher_cache` 配置块，并在 Markdown 报告中展示 cache 状态。
- 在 `tests/test_icbr_benchmark_script_smoke.py` 增加“首轮 miss + 二轮 hit”测试，验证跨运行缓存命中。
- 实跑 quality 配置（`train_num=1000, test_num=500, train_steps=80, lr=0.03, lamb=1e-3`）两次同参 benchmark：
  - run1：`teacher_cache_hit` 全部为 `False`（写入缓存）
  - run2：`teacher_cache_hit` 全部为 `True`（命中缓存）
  - `teacher_cache_key` 在 run1/run2 对应 task+seed 保持一致

## Files Changed
- scripts/icbr_benchmark.py
- tests/test_icbr_benchmark_script_smoke.py
- IMPLEMENTATION_PLAN.md
- TASK_STATUS.md

## Validation Run
- `C:\Users\chenpeng\miniconda3\envs\kan\python.exe -m pytest tests/test_icbr_benchmark_script_smoke.py`
- `C:\Users\chenpeng\miniconda3\envs\kan\python.exe -m scripts.icbr_benchmark --profile quality --tasks minimal,combo,poly_cubic,trig_interaction --seeds 0,1 --output-dir outputs/icbr_benchmark_stage11_cache_run1_qualitydefaults --teacher-cache-dir outputs/teacher_cache_stage11_quality --teacher-cache-mode readwrite --teacher-cache-version stage11_v1 --quiet --no-plots`
- `C:\Users\chenpeng\miniconda3\envs\kan\python.exe -m scripts.icbr_benchmark --profile quality --tasks minimal,combo,poly_cubic,trig_interaction --seeds 0,1 --output-dir outputs/icbr_benchmark_stage11_cache_run2_qualitydefaults --teacher-cache-dir outputs/teacher_cache_stage11_quality --teacher-cache-mode readwrite --teacher-cache-version stage11_v1 --quiet --no-plots`
- `C:\Users\chenpeng\miniconda3\envs\kan\python.exe -c "..."`（对两次 summary 做命中率与 key 一致性核对）

## Validation Result
- `pytest` 通过：`5 passed`
- run1 与 run2 均成功落盘 `icbr_benchmark_summary.json`
- run1: `teacher_cache_hit_mean = 0.0`，状态计数 `{'miss_write': 8}`
- run2: `teacher_cache_hit_mean = 1.0`，状态计数 `{'hit': 8}`
- `keys_consistent = True`（同 task+seed 的缓存 key 一致）

## Decisions
- 继续维持“只改 benchmark/regression 层，不改 ICBR 主路径”。
- `quality` 默认训练参数采用：
  - `train_num=1000`
  - `test_num=500`
  - `train_steps=80`
  - `lr=0.03`
  - `lamb=1e-3`
- Stage 11 保持最小可用缓存方案，先交付跨运行复用与可观测性，再考虑更重并发/清理策略。

## Remaining Work
- Stage 11 范围内无剩余工作。
- 下一步建议新增后续 stage：基于持久 cache 做更大 seeds/任务规模的回归门禁复验与统计可视化加固。

## Blockers
- 无
