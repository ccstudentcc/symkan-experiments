# TASK_STATUS

## Task
按 `IMPLEMENTATION_PLAN.md` 推进 ICBR-KAN Phase I，并完成当前首个可执行 stage。

## Current Stage
Stage 2: Add Safe Replay Evaluator

## Status
Complete

## Latest Completed Work
- 在 `kan/icbr.py` 新增 `replay_rerank_edge_candidates(...)`，实现内存态 replay 排序，默认评分为 squared imitation loss。
- 新增边级 `snapshot/apply/restore` helper，replay 前后完整恢复：
  - `funs`
  - `funs_sympy`
  - `funs_avoid_singularity`
  - `funs_name`
  - `affine`
  - numeric mask
  - symbolic mask
- 实现 `calibration_split` 输入抽取（`val_input/test_input/train_input`）并支持直接张量输入。
- replay 内环不调用 `MultKAN.copy()`、`fix_symbolic(..., log_history=True)`、`unfix_symbolic()` 或 checkpoint 落盘路径。
- 新增 `tests/test_icbr_replay.py`，覆盖：
  - replay 后目标边状态完整恢复
  - `state_id/history/checkpoint` 无副作用
  - replay 排序可与 local `r2` top-1 不同

## Files Changed
- kan/icbr.py
- tests/test_icbr_replay.py
- IMPLEMENTATION_PLAN.md
- TASK_STATUS.md

## Validation Run
- `C:\Users\chenpeng\miniconda3\envs\kan\python.exe -m pytest tests\test_icbr_candidates.py tests\test_icbr_replay.py`（首次：`tmp_path` 锁文件权限错误）
- `C:\Users\chenpeng\miniconda3\envs\kan\python.exe -m pytest tests\test_icbr_candidates.py tests\test_icbr_replay.py`（修复后通过）

## Validation Result
- 通过：`tests/test_icbr_candidates.py` + `tests/test_icbr_replay.py` 共 6 项，6 项通过。
- 失败已处理：`tmp_path` 在当前环境出现 lock 权限错误，改为仓库内 `tmp/` 唯一路径后复测通过。

## Decisions
- Stage 2 继续保持最小侵入：仅扩展 `kan/icbr.py` 与 replay 专属测试，不提前做 Stage 3 commit helper。
- replay 采用“直接写入目标边 + 立即恢复”的内存态路径，避免 `log_history/state_id/checkpoint` 副作用。
- 为验证“contextual rerank 可不同于 local r2”，增加轻量 toy model 测试，避免依赖复杂训练态构造。

## Remaining Work
- Stage 3: Add Explicit Commit Helper。
- Stage 4: 串接 `auto_symbolic_icbr(...)` 入口。
- Stage 5: CPU 基准与主张验证。

## Blockers
- 无
