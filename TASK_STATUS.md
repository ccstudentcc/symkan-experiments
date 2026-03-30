# TASK_STATUS

## Date
2026-03-30

## Task
完成 Stage 21：修正 `scripts/icbr_benchmark.py` 对 KAN multiplication-aware `width` 的支持，使 Feynman benchmark 能正确表达类似 `[n_var, [5,2], 1]` 的中间层配置；同时对齐 Feynman teacher 默认配置，新增 `prune_iters` 控制 teacher 的“剪枝 + 微调”轮数，并补齐 benchmark 图表在 log / ratio 轴下的标签与尺度口径。

## Current Stage
Stage 21: Support Multiplication-Aware Feynman Width Specs and Teacher Default Alignment

## Status
Complete

## Latest Completed Work
- `scripts/icbr_benchmark.py`：
  - 新增 width token 归一化逻辑，支持显式 multiplication-aware layer spec，例如 `[5,2]`
  - 保留旧式纯整数写法兼容：`5,3` 仍按 `width=[n_var,5,3,1]` 解析
  - Feynman width 构造改为允许原样插入 multiplication-aware layer，因此 `[5,2]` 会生成 `width=[n_var,[5,2],1]`
  - `run_benchmark()` 的默认 `feynman_width_mid` 改为 `[[5,2]]` 内部表达，summary/config 对外展示为 `[5,2]`
  - CLI `--feynman-width-mid` 默认值改为 `"[5,2]"`，帮助文本同步说明三类用法：
    - `[5,2]`
    - `5,3`
    - `[[5,2],3]`
  - Feynman teacher 默认口径已对齐为：
    - `fit_opt=Adam`
    - `post_prune_steps=100`
    - `post_prune_lr=1e-3`
    - `post_prune_lamb=1e-3`
    - `post_prune_eval_every=5`
    - `post_prune_min_delta=1e-6`
    - `post_prune_patience=3`
    - `teacher_max_test_mse=0.1`
    - `teacher_min_test_r2=None`（默认不要求）
  - teacher quality gate 现在支持“阈值为空即不检查该指标”，用于 Feynman 默认不要求 `R2`
  - 新增 `--prune-iters` / `run_benchmark(prune_iters=...)`
    - `prune + refit` 记作一轮
    - 默认值 `1`
    - 适用于 synthetic / Feynman teacher prune 路径
  - teacher cache key、summary config、markdown run config 已纳入 `prune_iters`
  - 图表格式补充：
    - `speedup_boxplot` 改为 ratio 值的 log 轴，y 轴标签为 `Speedup Ratio (×)`，基准线为 `1x`
    - `q123_evidence_by_task` 从 `log2(ratio)` 改为 ratio 值本身，使用 log 轴与 `1x` 基准线，并以几何均值 + 95% CI 汇总
    - `variant_overview` 的时间列 y 轴标签改为 `Symbolic Wall Time (s)`，不再把 `log scale` 写进标签文本
    - `mse_shift_boxplot` 的 y 轴标签改为 `ICBR MSE - Baseline MSE`，scale 仅由坐标轴表达
    - log 轴 formatter 固定为数学形式刻度，避免被 scientific formatter 回写覆盖
  - Stage 21 补充修正：
    - `symbolic_time_errorbar` / `speedup_boxplot` / `mse_shift_boxplot` 在对数尺度时统一显示标题左侧 `scale=log`
    - `symbolic_time_errorbar` 的 y 轴标签固定为 `Symbolic Wall Time (s)`，不再把 scale 写进标签
    - `q123_evidence_by_task` 的三个 y 轴标签拆成两行，括号部分放到第二行，避免与面板内容重叠
    - ratio 刻度去掉重复的 `×` 后缀，并优先显示普通数值，例如 `10` 而不是 `1e1`
    - `speedup_boxplot` 的 ratio 轴边界改为收紧到已有数据附近，避免基准线下方留下大段空白
- `tests/test_icbr_benchmark_script_smoke.py`：
  - 新增 `_parse_width_mid()` 单元测试，覆盖 multiplication-aware 与兼容写法
  - 新增 teacher quality gate 关闭 `R2` 约束的单元测试
  - Feynman dataset smoke 改为显式传入 `--feynman-width-mid [5,2]`
  - 断言 summary/config 的 `width_mid` 为 `[5,2]`
  - 断言行级 `width` 的中间层保留 `[5,2]`
  - 新增省略 `feynman_width_mid` 时默认落到 `[5,2]`，并同时断言 Feynman 默认 teacher 配置与 gate 阈值
  - 新增 `prune_iters` 透传到 synthetic teacher 配置的 smoke test
  - 更新可视化 metadata 断言，覆盖：
    - `speedup` 使用 `log` scale + `Speedup Ratio (×)`
    - `variant_overview` 标签不再写 scale
    - `q123` 使用 ratio 值而不是 `log2_ratio`
    - `symbolic_time_errorbar` 改回纯单位标签，并为对数图记录 `scale_label_placement`
    - `q123` 的面板标签改为两行格式
- `IMPLEMENTATION_PLAN.md`：
  - 新增 Stage 21，记录需求、约束、成功标准与验证命令

## Files Changed
- scripts/icbr_benchmark.py
- tests/test_icbr_benchmark_script_smoke.py
- IMPLEMENTATION_PLAN.md
- TASK_STATUS.md

## Validation Run
- `C:\Users\chenpeng\miniconda3\envs\kan\python.exe -m py_compile scripts/icbr_benchmark.py tests/test_icbr_benchmark_script_smoke.py`
- `C:\Users\chenpeng\miniconda3\envs\kan\python.exe -m pytest tests/test_icbr_benchmark_script_smoke.py -k "feynman or width_mid or prune_iters or teacher_quality_gate_can_disable_r2_requirement or quality_profile_enables_teacher_prune_by_default"`
- `C:\Users\chenpeng\miniconda3\envs\kan\python.exe -m pytest tests/test_icbr_benchmark_script_smoke.py -k "visualization_upgrade_emits_variant_and_q123_plots or replot_only_rebuilds_visualizations_from_existing_artifacts"`
- `C:\Users\chenpeng\miniconda3\envs\kan\python.exe -m pytest tests/test_icbr_benchmark_script_smoke.py -k "visualization_upgrade_emits_variant_and_q123_plots or replot_only_rebuilds_visualizations_from_existing_artifacts"`

## Validation Result
- `py_compile` 通过。
- `pytest tests/test_icbr_benchmark_script_smoke.py -k "feynman or width_mid or prune_iters or teacher_quality_gate_can_disable_r2_requirement or quality_profile_enables_teacher_prune_by_default"` 通过：`10 passed, 11 deselected`。
- `pytest tests/test_icbr_benchmark_script_smoke.py -k "visualization_upgrade_emits_variant_and_q123_plots or replot_only_rebuilds_visualizations_from_existing_artifacts"` 通过：`2 passed, 19 deselected`。
- Stage 21 补充后的可视化 smoke test 重新通过。
- 已验证：
  - `--feynman-width-mid [5,2]` 可正确生成 multiplication-aware 中间层
  - 省略 `feynman_width_mid` 时默认落到 `[5,2]`
  - 旧式 `5,2` 纯整数写法仍可由解析器按兼容路径处理
  - Feynman 默认 `post_prune_lamb=1e-3`、`post_prune_patience=3`
  - Feynman 默认 teacher quality gate 为 `max_mse=0.1` 且不要求 `min_r2`
  - `prune_iters` 已透传到 teacher config，并进入 benchmark summary / cache 语义
  - `speedup` / `q123` ratio 图已改为 log 轴 + `1x` 基准线
  - `variant_overview` / `mse_shift` 标签已改为保留原始单位/量纲，不再把 `log` 写进标签文本
  - 对数尺度图现在统一以左侧 `scale=log` badge 标注，ratio 刻度不再重复显示 `×`

## Decisions
- `feynman_width_mid` 对外仍保留“中间层配置”概念，但内部区分：
  - 单个 multiplication-aware layer：`[5,2]`
  - 多个纯整数 hidden layers：`5,3`
  - 混合/多层显式写法：`[[5,2],3]`
- summary/config 在只有一个中间层时展示单层值，而不是额外包一层列表，便于与用户口径对齐
- Feynman 默认 teacher gate 采用“只约束 MSE，不约束 R2”的策略；实现上使用 `teacher_min_test_r2=None`
- `prune_iters` 不区分数据集类型；是否实际生效仍由 `teacher_post_train_prune` 控制

## Remaining Work
- 无

## Blockers
- 无
