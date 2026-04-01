# 工程版复测与历史结果口径说明

## 1. 文档目的

本文档用于界定“历史参考版本”与“当前工程版本”在实验口径上的差异，并给出统一的报告叙述框架。当前还额外承担一个职责：说明 `2026-04-01` 的 `baseline` vs `baseline_icbr` 对照为什么可以被解释为“同一工程版内部的后端比较”，而不是新的训练实验。

## 2. 版本分层定义

1. 历史参考版：`d8e09b5edadb988bd4a1638ea7109cf3ff5ef7d7`，对应 pre-release `v1.0.0-legacy-d8`。
2. 当前工程版：`main` 分支（包含配置模块化、守护策略分级、可观测性增强、共享 symbolic-prep cache 与 ICBR 后端接入等工程化改造）。

建议在论文、报告或答辩材料中显式声明：历史版本仅作为参考锚点，工程版本用于当前正式结论。

## 3. 两代结果不可直接等价的原因

1. 训练与剪枝守护策略存在实质差异，尤其体现在失败边界判定与回滚机制。
2. 工程版扩展了耗时指标体系，新增 `run_total_wall_time_s`、`symbolize_wall_time_s`、`symbolic_core_seconds` 等字段，统计口径较历史版本更细。
3. 配置管理方式由分散参数传递转为 `AppConfig` 统一入口，CLI 仅承担受控覆盖，实验可重复性语义发生变化。
4. 跨版本耗时字段并非完全同名：跨代对照时仅允许将 `export_wall_time_s` 语义映射到 `symbolize_wall_time_s`；`run_total_wall_time_s` 为工程版新增字段，历史版无同名可比项。

因此，工程版与历史版间出现时延差异属于方法学差异下的预期现象，不宜直接解释为模型性能退化。

## 4. 当前工程版复测锚点

当前工程版建议区分两个锚点：

1. 工程版总体口径锚点：
   - `outputs/rerun_v2_engine_safe_20260318/`
   - `outputs/rerun_v2_engine_safe_20260318_rerun/`
   用于说明工程版相对历史版的总体变化。
2. ICBR 后端对照锚点：
   - `outputs/rerun_v2_engine_safe_20260401/benchmark_ab/`
   用于说明当前工程版内部 `baseline` vs `baseline_icbr` 的 backend-only 对照。

若当前写作主题是 ICBR 接入结果，应优先引用第二组锚点及其配套报告 [engineering_rerun_report.md](engineering_rerun_report.md)。

## 5. 当前工程版默认设定（2026-04）

1. `stagewise.guard_mode = light`
2. `stagewise.prune_acc_drop_tol = 0.08`
3. 常规 CLI 入口使用 `python -m scripts.*`
4. 工程归档输出目录采用 `outputs/rerun_v2_engine_safe_<date>/*`
5. 对 `baseline` vs `baseline_icbr`，默认要求共享：
   - numeric stage
   - shared symbolic-prep
   - `symbolize_trace`

当前 ICBR 比较的关键口径是：

1. `baseline_icbr.yaml` 仅切换 `symbolize.symbolic_backend: icbr`。
2. compare 结论必须优先检查 `baseline_icbr_shared_check.csv`。
3. 若 `shared_numeric_aligned=True`、`trace_aligned=True`、`shared_symbolic_prep_aligned=True`，才可将差异解释为 backend-only 差异。

## 6. 推荐执行环境

1. 操作系统：Windows 11 专业版 `23H2`（OS Build `22631.5472`）。
2. Python 环境：`Miniconda` 的 `kan` 环境，解释器路径 `C:\Users\chenpeng\miniconda3\envs\kan\python.exe`（Python `3.9.25`）。
3. CPU：`12th Gen Intel(R) Core(TM) i5-12500H`。
4. 内存：`16 GB`。
5. 运行路径：`PyTorch 2.1.2+cpu`，当前工程归档按 CPU 路径执行。

## 7. 报告书写建议

建议采用“三层叙述”结构：

1. 历史参考结果（基于 `d8` 版本）：用于提供研究脉络与可复现边界。
2. 工程版总体复测结果（基于 `2026-03-18` 工程 rerun）：用于说明工程版相对历史版的总体口径。
3. 工程版内部 ICBR 对照（基于 `2026-04-01` backend compare）：用于说明 ICBR 改动只发生在符号拟合阶段，且当前已满足 shared numeric / trace 对齐。

同时应设置“差异归因”小节，至少覆盖以下维度：

1. 守护策略变化带来的稳定性与安全收益。
2. 配置与可观测性增强带来的工程可维护性收益。
3. ICBR 对照中 shared symbolic-prep cache 与 trace 对齐的公平性含义。
4. 指标口径升级对耗时解释的影响。

## 8. 建议配套文档

建议同时维护以下两类报告：

1. 工程版总体口径报告：
   - 历史版 vs 工程版的总体差异
   - 主要指标统计表
2. ICBR 后端对照报告：
   - shared-state 检查
   - primary effect
   - mechanism breakdown

当前对应文件为：

1. [engineering_rerun_report.md](engineering_rerun_report.md)
2. [symkanbenchmark_usage.md](symkanbenchmark_usage.md)

## 9. 当前状态

1. 历史参考版已通过 release 冻结，不再建议频繁回切旧版本重跑。
2. 工程版总体口径仍可参考 `2026-03-18` 的 rerun 归档。
3. 当前关于 ICBR 接入的正式引用锚点应优先使用 `outputs/rerun_v2_engine_safe_20260401/benchmark_ab/` 及其配套报告。
4. 后续若继续扩展 symbolic backend，对外口径仍应保持：历史版用于参考，工程版用于正式结论，而 backend compare 需明确共享边界与专用 compare 产物。
