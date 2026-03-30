# TASK_STATUS

## Date
2026-03-30

## Task
完成 Stage 20 的最终版图表收敛：围绕论文使用场景，修正五张 benchmark 图的统计口径、尺度表达、图例/scale 标注遮挡问题，以及只重绘流程；其中 `Q2/Q3` 已改为相对 `icbr_full` 的比值证据图。

## Current Stage
Stage 20: Per-Task Vertical Variant Overview Layout

## Status
Complete

## Latest Completed Work
- `scripts/icbr_benchmark.py`：
  - 保留统一视觉风格层，但将关键统计图的统计口径进一步按指标语义细分。
  - `icbr_benchmark_symbolic_time_errorbar.png`：
    - 保持 `point + 95% CI`
    - 对正值偏态时间指标改用“几何均值 + log 轴上的 95% CI”
    - 图例移到 figure 顶部保留区，避免压住 `minimal`/`poly_cubic` 一类 task 的点与误差条
    - y 轴说明改为显式包含真实尺度，例如 `Symbolic wall time (s) (log scale)`
    - 使大跨度 task 下的时间比较更稳健
  - `icbr_benchmark_q123_evidence_by_task.png`：
    - 继续使用 `point + 95% CI`
    - `Q1` 改成 `log2(no_shared/full)` 后再做区间估计，使相对 `1` 的乘法证据围绕 `0` 对称表达
    - `Q2/Q3` 从线性差值改成相对 `icbr_full` 的 `log2 ratio`：
      - `Q2 = log2(no_replay MSE / full MSE)`
      - `Q3 = log2(refit_commit MSE / full MSE)`
    - 这样不会因为原始 MSE 本身很小而把机制差异压缩成“不显眼的小差值”
    - 每个 panel 的 `scale=...` 从 axes 内部改到 title band，避免遮挡上方数据
    - y 轴说明改为与实际尺度语义一致：三者都明示为 `log2 ratio`
    - target-MSE、rank inversion、param drift 等次级证据继续保留在 summary/表格口径中，不堆叠进主图
  - `icbr_benchmark_variant_overview.png`：
    - 从“每行 3 子图”改为“每行 2 子图”
    - 左列：`SymbolicTime`，使用几何均值 + `95% CI` + `log`
    - 右列：把 `ImitationMSE` 与 `TargetMSE` 合并到同一子图，用图例区分，并使用 `log`
    - `scale=...` 改放到 title band；MSE 图例提升到 figure 顶部保留区，避免多行 facet 中反复压住数据
    - y 轴说明显式写明真实尺度，例如 `Time (s) (log scale)`、`MSE / Target MSE (log scale)`
  - `icbr_benchmark_mse_shift_boxplot.png`：
    - y 轴说明随真实尺度动态更新，`symlog` 时明确写为 `ICBR MSE - baseline MSE (symlog scale)`
  - `icbr_benchmark_speedup_boxplot.png`：
    - y 轴说明明确为 `linear scale`，避免与其他非线性尺度图混淆
  - `artifacts.visualizations.plots` 中增加了更完整的图设计元数据，记录 chart type、scale、stat note 和 design reason。
  - `artifacts.visualizations.plots` 额外记录了 `legend_placement`、`scale_label_placement` 与各图/各 panel 的 y 轴标签，便于后续 smoke test 约束“不要再挡住数据”。
  - `--replot-only` 继续可用，可对已有 benchmark 产物直接重绘。
- `tests/test_icbr_benchmark_script_smoke.py`：
  - 更新 `variant_overview` 的布局断言与 metadata 断言，适配“两列版 final layout”。
  - 新增图例位置、尺度标注位置和 y 轴文案断言，防止回退到“标签压数据”或“轴标签与尺度不一致”。
  - 将 `Q123` 的 metadata 断言更新为“Q1/Q2/Q3 全部为 `log2_ratio` 主证据”。
  - 将 `quality profile` 默认值断言对齐到代码当前真实默认值：`train_steps=200`、`lr=1e-2`。
- 已重绘：
  - `outputs/icbr_benchmark_stage20_quality_ablation_4tasks_10seeds/*`

## Files Changed
- scripts/icbr_benchmark.py
- tests/test_icbr_benchmark_script_smoke.py
- IMPLEMENTATION_PLAN.md
- TASK_STATUS.md

## Validation Run
- `C:\Users\chenpeng\miniconda3\envs\kan\python.exe -m py_compile scripts/icbr_benchmark.py tests/test_icbr_benchmark_script_smoke.py`
- `C:\Users\chenpeng\miniconda3\envs\kan\python.exe -m pytest tests/test_icbr_benchmark_script_smoke.py -k "quality_profile_resolves_expected_defaults or visualization_upgrade_emits_variant_and_q123_plots or replot_only_rebuilds_visualizations_from_existing_artifacts"`
- `C:\Users\chenpeng\miniconda3\envs\kan\python.exe -m scripts.icbr_benchmark --replot-only --output-dir outputs/icbr_benchmark_stage20_quality_ablation_4tasks_10seeds --quiet`

## Validation Result
- `py_compile` 通过。
- 关键 smoke 子集通过：`3 passed`。
- `stage20` 目标目录已按新版逻辑重绘完成。

## Decisions
- `point + 95% CI` 继续保留，但不再机械使用算术均值：
  - 正值偏态指标（时间、MSE）改为几何均值口径
  - 乘法比值证据（Q1/Q2/Q3）统一改为 `log2 ratio`
- `variant_overview` 中两种 MSE 合并到同一列，以减少子图数量并提高论文版面效率。
- 尺度信息必须直接显示在图上，但不能进入 axes 数据区；本阶段统一改为 title band 或 figure 顶部保留区。
- y 轴说明必须和真实尺度同步更新，避免把 `log` / `symlog` 图误读成线性图。
- `Q123` 主图只保留每个 critique 的 primary evidence；其余次级指标更适合放在论文表格或附录表格中承接解释。

## Remaining Work
- Stage 16 已完成（10-seed 扩展验证）。
- Stage 17 已完成（多变体公式报告完整性修复）。
- Stage 18 已完成（可视化升级）。
- Stage 19 已完成（quiet + 展示精简 + 流程复核）。
- Stage 20 已完成（论文导向图表最终收敛 + stage20 目录重绘）。

## Blockers
- 无
