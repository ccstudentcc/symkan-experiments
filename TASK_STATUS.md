# TASK_STATUS

## Task
按 `IMPLEMENTATION_PLAN.md` 推进 ICBR-KAN Phase I，并完成当前首个可执行 stage。

## Current Stage
Stage 3: Add Explicit Commit Helper

## Status
Complete

## Latest Completed Work
- 在 `kan/icbr.py` 新增公开提交入口 `commit_symbolic_candidate(...)`，直接写入 symbolic state，不经过 `fix_symbolic()` 二次拟合。
- 将候选应用逻辑抽成 `_apply_symbolic_candidate_state(...)`，并复用于 replay 与 commit 路径，保持状态写入口径一致。
- commit 支持显式 `0` 函数提交（可不提供 `params`，默认提交零函数参数）。
- 新增 `tests/test_icbr_commit.py`，覆盖：
  - exporter correctness（提交后 `symbolic_formula()` 可导出）
  - 零函数提交后 forward 与导出可运行
  - `funs/funs_sympy/funs_avoid_singularity/funs_name/affine/masks` 一致性

## Files Changed
- kan/icbr.py
- tests/test_icbr_commit.py
- IMPLEMENTATION_PLAN.md
- TASK_STATUS.md

## Validation Run
- `C:\Users\chenpeng\miniconda3\envs\kan\python.exe -m pytest tests\test_icbr_candidates.py tests\test_icbr_replay.py tests\test_icbr_commit.py`

## Validation Result
- 通过：`tests/test_icbr_candidates.py` + `tests/test_icbr_replay.py` + `tests/test_icbr_commit.py` 共 9 项，9 项通过。

## Decisions
- Stage 3 只新增 commit helper，不提前做 Stage 4 的遍历流程与 teacher/work 协调控制。
- commit 路径与 replay 共享候选应用底座，避免两套状态写入逻辑漂移。
- 对 `0` 候选采用默认参数提交，保证“剪枝边显式提交为 0”可直接落地。

## Remaining Work
- Stage 4: 串接 `auto_symbolic_icbr(...)` 入口。
- Stage 5: CPU 基准与主张验证。

## Blockers
- 无
