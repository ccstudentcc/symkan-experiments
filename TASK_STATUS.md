# TASK_STATUS

## Date
2026-03-29

## Task
完成 Stage 14：在 `feynman_reference` 配置下对 `I.12.1` 与 `I.12.4` 进行 seeds=1,2 先导实跑，并验证 teacher 持久缓存链路。

## Current Stage
Stage 14: Feynman Pilot Run on I.12.1 and I.12.4 (Seeds 1,2)

## Status
Complete

## Latest Completed Work
- 新增并执行 Stage 14（最小范围实跑）：
  - `tasks=feynman_I_12_1,feynman_I_12_4`
  - `seeds=1,2`
  - 其余保持 `feynman_reference` 口径
  - teacher cache 模式 `readwrite`
- 首轮实跑出现运行时失败：
  - 在 teacher `prune()` 阶段触发 `RuntimeError: stack expects a non-empty TensorList`
- 在当前 stage 范围内完成最小修复：
  - `scripts/icbr_benchmark.py` 的 teacher 剪枝流程增加安全回退：
    - 先按配置阈值 `prune`
    - 失败则回退到 `node_th=0, edge_th=0` 的保守剪枝
    - 再失败则保留未剪枝 teacher 并继续流程
- 修复后重跑 Stage 14 成功，产出完整 benchmark 导出文件：
  - `outputs/icbr_benchmark_stage14_feynman_i12_pilot/icbr_benchmark_rows.csv`
  - `outputs/icbr_benchmark_stage14_feynman_i12_pilot/icbr_benchmark_summary.json`
  - `outputs/icbr_benchmark_stage14_feynman_i12_pilot/icbr_benchmark_summary.md`

## Files Changed
- scripts/icbr_benchmark.py
- IMPLEMENTATION_PLAN.md
- TASK_STATUS.md

## Validation Run
- `C:\Users\chenpeng\miniconda3\envs\kan\python.exe -m py_compile scripts\icbr_benchmark.py`
- `C:\Users\chenpeng\miniconda3\envs\kan\python.exe -m pytest tests\test_icbr_benchmark_script_smoke.py::test_feynman_dataset_file_loading_smoke`
- （首轮失败）`C:\Users\chenpeng\miniconda3\envs\kan\python.exe -m scripts.icbr_benchmark --profile feynman_reference --tasks feynman_I_12_1,feynman_I_12_4 --seeds 1,2 --feynman-root datasets --feynman-variant Feynman_with_units --teacher-cache-dir outputs/teacher_cache_feynman_reference --teacher-cache-mode readwrite --output-dir outputs/icbr_benchmark_stage14_feynman_i12_pilot --quiet`
- （修复后通过）`C:\Users\chenpeng\miniconda3\envs\kan\python.exe -m scripts.icbr_benchmark --profile feynman_reference --tasks feynman_I_12_1,feynman_I_12_4 --seeds 1,2 --feynman-root datasets --feynman-variant Feynman_with_units --teacher-cache-dir outputs/teacher_cache_feynman_reference --teacher-cache-mode readwrite --output-dir outputs/icbr_benchmark_stage14_feynman_i12_pilot --quiet`

## Validation Result
- 代码修复验证通过（`py_compile` + Feynman smoke 单测）
- Stage 14 目标命令最终执行成功，`rows=4`（2 tasks × 2 seeds）
- 缓存状态可观测：
  - `feynman_I_12_1` seeds 1/2：`cache_hit=True`（hit）
  - `feynman_I_12_4` seeds 1/2：`cache_hit=False`（miss_write）
- 结果中 teacher quality gate 均未通过，导致符号化对比被跳过（该行为符合当前门禁策略）：
  - `feynman_I_12_1`: teacher `test_mse≈0.24`（高于默认阈值 0.10）
  - `feynman_I_12_4`: teacher `test_r2≈-0.53`（低于默认阈值 0.75）

## Decisions
- 保持“其他参数一致”的前提下完成你指定任务/seed 的先导验证。
- 不放宽 teacher 门禁阈值，先保留真实失败信号，避免误判符号化流程收益。
- 对 prune 运行时异常采用最小安全回退方案，优先保障 benchmark 流程可执行性与可观测性。

## Remaining Work
- 若你希望继续对比 baseline/ICBR 符号化效果，需要先提升这两个任务的 teacher 质量，或临时放宽门禁阈值做探索性对比。
- 建议下一步：
  - 先对 `I.12.1/I.12.4` 做 teacher 收敛增强（如增步数/调 lr/lamb）再复跑本 stage。
  - 或按你的决策，先用放宽门禁做一次符号化可行性试跑。

## Blockers
- 无硬 blocker；当前主要问题是 teacher 质量门禁未通过。
