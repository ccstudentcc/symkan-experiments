# TASK_STATUS

## Date
2026-03-29

## Task
完成 Stage 13 收口：在 Feynman 参考流程中补齐“剪枝后微调早停机制”，并固定微调超参（`lr=1e-3`, `lamb=1e-2`）。

## Current Stage
Stage 13: Add Feynman Reference Preset and Prune-Refit Teacher Flow

## Status
Complete

## Latest Completed Work
- 增加 `feynman_reference` 参考 profile，参数与目标口径：
  - `train_num=2000`
  - `test_num=1000`
  - `train_steps=200`
  - `lr=1e-2`
  - `lamb=1e-2`
- 默认调用增强（便于直接使用参考配置）：
  - 当 `--profile feynman_reference` 且未显式给 `--tasks/--seeds` 时，默认：
    - `tasks=["feynman_paper10"]`
    - `seeds=[1]`
- Feynman teacher 训练流已升级为：
  - 初始训练（`opt=Adam`）
  - `model.prune(node_th=1e-2, edge_th=1e-2)`
  - 微调最多 `100` 步（`lr=1e-3`, `lamb=1e-2`）
  - 微调阶段启用早停：每 `5` 步检查一次 train MSE 变化，若连续若干次变化不超过 `min_delta` 则提前停止
  - 再落入持久 cache，并用于 baseline/ICBR 符号化对比
- Feynman 模型结构口径已固定在 task 规格中：
  - `grid=20`
  - `k=3`
  - `width_mid=5,2`（通过 `--feynman-width-mid` 默认值）
  - `device=cpu`
- cache key 继续增强，纳入 teacher 结构与 prune/refit 语义，避免错命中：
  - `teacher_grid/teacher_k/teacher_fit_opt/teacher_post_train_prune/prune_th/post_prune_steps/post_prune_lr/post_prune_lamb/post_prune_early_stop/eval_every/min_delta/patience`
- summary 输出新增 `config.teacher_training`，每个 task 可追踪 teacher 训练与 prune/refit 配置。
- 测试更新：Feynman smoke 额外校验 `post_prune_lr/post_prune_lamb/post_prune_early_stop/post_prune_eval_every/post_prune_min_delta/post_prune_patience` 字段。

## Files Changed
- scripts/icbr_benchmark.py
- tests/test_icbr_benchmark_script_smoke.py
- IMPLEMENTATION_PLAN.md
- TASK_STATUS.md

## Validation Run
- `C:\Users\chenpeng\miniconda3\envs\kan\python.exe -m py_compile scripts\icbr_benchmark.py tests\test_icbr_benchmark_script_smoke.py`
- `C:\Users\chenpeng\miniconda3\envs\kan\python.exe -m pytest tests\test_icbr_benchmark_script_smoke.py`
- `C:\Users\chenpeng\miniconda3\envs\kan\python.exe -m pytest tests\test_icbr_benchmark_smoke.py tests\test_icbr_benchmark_script_smoke.py tests\test_icbr_benchmark_regression_smoke.py`

## Validation Result
- `py_compile` 通过
- 脚本 smoke 测试通过：`9 passed`
- benchmark 回归相关测试通过：`12 passed`
- Feynman smoke 路径与旧路径均可运行，导出字段与 cache 语义无回归

## Decisions
- 继续维持“只改 benchmark 层，不改 ICBR 主算法”。
- prune 阈值按你提供口径采用 `1e-2`（通过 `model.prune(node_th=1e-2, edge_th=1e-2)` 显式固定）。
- 剪枝后微调默认超参固定为 `lr=1e-3`, `lamb=1e-2`，并启用“每 5 步检测变化”的早停策略。

## Remaining Work
- 等你把真实数据下载到 `datasets/` 后，可直接参考调用：
  - `python -m scripts.icbr_benchmark --profile feynman_reference --feynman-root datasets --feynman-variant Feynman_with_units --output-dir outputs/icbr_benchmark_feynman_reference --quiet --no-plots`
- 完成真实数据实跑后，再进行多 seeds 聚合与回归门禁复验。

## Blockers
- 本地真实 Feynman 数据尚未下载完成（你已说明将放到仓库相对路径 `datasets/`）。
