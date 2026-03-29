# TASK_STATUS

## Date
2026-03-29

## Task
完成 Stage 12：增强 `icbr_benchmark.py` 支持本地 Feynman 数据集目录（含 variant/选择策略/CLI），并保持现有导出与 teacher cache 功能。

## Current Stage
Stage 12: Add Feynman Dataset Support to `icbr_benchmark.py`

## Status
Complete

## Latest Completed Work
- 在 `scripts/icbr_benchmark.py` 增加 Feynman 数据接入层与 CLI：
  - 新增参数：`--feynman-root`、`--feynman-variant`、`--feynman-equations-csv`、`--feynman-max-datasets`、`--feynman-dataset-select-seed`、`--feynman-split-strategy`、`--feynman-width-mid`、`--feynman-datasets`
  - 支持 task token：`feynman_paper10`（README 的固定 10 集）与 `feynman_random`（可复现随机子集）
  - 支持显式任务名（如 `feynman_I_10_7`）从本地文件 `datasets/<variant>/<filename>` 读取
- 新增 Feynman 数据处理能力：
  - 本地文件加载与 train/test 切分（`random` / `linspace`）
  - 自动读取 `FeynmanEquations.csv`（若存在）并写入 `target_formula`
  - 依据 Feynman 文件列数自动推断 `n_var`，并按 `feynman_width_mid` 构建网络宽度
- 保持并扩展现有导出结构：
  - `rows` 新增 `task_kind`、`task_source`、`target_formula`
  - `summary.config` 新增 `feynman` 配置块
  - Markdown 报告增加 Feynman 运行配置与每条任务来源信息
- teacher cache 保持可用且缓存键增强：
  - 额外纳入 `dataset_kind/dataset_path/dataset_variant/dataset_split_strategy`，避免 Feynman 多来源冲突缓存
- 新增测试覆盖：
  - `test_feynman_dataset_file_loading_smoke`（临时 mock 本地 Feynman 文件验证完整路径）
  - `test_feynman_task_tokens_expand`（验证 `feynman_paper10` token 展开）

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
- `pytest` 通过：`7 passed`
- benchmark 相关回归测试通过：`10 passed`（`test_icbr_benchmark_smoke + test_icbr_benchmark_script_smoke + test_icbr_benchmark_regression_smoke`）
- 新增 Feynman smoke 测试通过，证明在本地文件数据模式下：
  - CLI 参数可解析
  - 数据可读取并切分
  - benchmark 可完成导出（CSV/JSON/MD）
  - teacher cache 与既有导出结构未破坏

## Decisions
- 继续维持“只改 benchmark/数据接入层，不改 ICBR 主算法”。
- 对 Feynman 任务采用“本地文件优先”的真实数据模式（与你的 `datasets/` 目录约定一致）。
- 通过 token + 显式列表双通道支持 README 风格操作（固定 10 集 / 随机子集 / 指定集合）。
- 在你尚未完成数据下载前，先用 mock 数据集完成可执行验证，避免虚报已跑真实 benchmark。

## Remaining Work
- 等你把数据下载到 `datasets/` 后，执行真实 10 集实验（建议命令）：
  - `python -m scripts.icbr_benchmark --tasks feynman_paper10 --profile quality --feynman-root datasets --feynman-variant Feynman_with_units --feynman-max-datasets 10 --feynman-dataset-select-seed 2 --output-dir outputs/icbr_benchmark_stage12_feynman_paper10 --quiet --no-plots`
- 完成真实数据实跑后，再进行多 seeds 聚合与回归门禁复验。

## Blockers
- 本地真实 Feynman 数据尚未下载完成（你已说明将放到仓库相对路径 `datasets/`）。
