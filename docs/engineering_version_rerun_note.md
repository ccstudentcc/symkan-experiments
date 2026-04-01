# 工程版复测与历史结果口径说明

## 1. 文档目的

本文档用于界定“历史参考版本”与“当前工程版本”在实验口径上的差异，并统一说明当前工程版内部的两组 ICBR 后端对照：

1. `baseline` vs `baseline_icbr`
   用于最保守的 layered 库 backend-only 对照。
2. `baseline_fastlib` vs `baseline_icbr_fastlib`
   用于在更大候选函数库下观察 ICBR 的速度潜力。

两组对照都只允许解释为“同一工程版内部的后端比较”，而不是新的训练实验。

## 2. 版本分层定义

1. 历史参考版：`d8e09b5edadb988bd4a1638ea7109cf3ff5ef7d7`，对应 pre-release `v1.0.0-legacy-d8`。
2. 当前工程版：`main` 分支，包含配置模块化、守护策略分级、共享 symbolic-prep cache 与 ICBR 后端接入等工程化改造。

建议在论文、报告或答辩材料中显式声明：历史版本仅作为参考锚点，工程版本用于当前正式结论。

## 3. 两代结果不可直接等价的原因

1. 训练与剪枝守护策略存在实质差异，尤其体现在失败边界判定与回滚机制。
2. 工程版扩展了耗时指标体系，新增 `run_total_wall_time_s`、`symbolize_wall_time_s`、`symbolic_core_seconds` 等字段。
3. 配置管理方式已收敛到 `AppConfig` 统一入口，CLI 仅承担受控覆盖。
4. 跨版本耗时字段并非完全同名：跨代对照时仅允许将 `export_wall_time_s` 语义映射到 `symbolize_wall_time_s`；`run_total_wall_time_s` 为工程版新增字段。

因此，工程版与历史版间出现时延差异属于方法学差异下的预期现象，不宜直接解释为模型性能退化。

## 4. 当前工程版复测锚点

当前工程版建议区分三个锚点：

1. 工程版总体口径锚点：
   - `outputs/rerun_v2_engine_safe_20260318/`
   - `outputs/rerun_v2_engine_safe_20260318_rerun/`
2. layered 库 ICBR 对照锚点：
   - `outputs/rerun_v2_engine_safe_20260401/benchmark_ab/comparison/`
3. FAST_LIB ICBR 对照锚点：
   - `outputs/rerun_v2_engine_safe_20260401/benchmark_ab/comparison_fastlib/`

若当前写作主题是“ICBR 在更大候选库下的速度潜力”，应优先引用第三组锚点及其配套报告 [engineering_rerun_report.md](engineering_rerun_report.md)。

## 5. 当前工程版默认设定（2026-04）

1. `stagewise.guard_mode = light`
2. `stagewise.prune_acc_drop_tol = 0.08`
3. 常规 CLI 入口使用 `python -m scripts.*`
4. 工程归档输出目录采用 `outputs/rerun_v2_engine_safe_<date>/*`
5. 对任一单个 baseline-backend vs icbr-backend compare，默认要求共享：
   - numeric stage
   - shared symbolic-prep
   - `symbolize_trace`

当前 ICBR 比较的关键口径是：

1. backend compare 结论必须优先检查 `baseline_icbr_shared_check.csv`。
2. 若 `shared_numeric_aligned=True`、`trace_aligned=True`、`shared_symbolic_prep_aligned=True`，才可将差异解释为 backend-only 差异。
3. 若只想扩大函数库但继续复用 numeric/shared-prep cache，应把库覆盖写在 `symbolize.lib` / `symbolize.lib_hidden` / `symbolize.lib_output`，而不是改非 `symbolize` section。

## 6. 推荐执行环境

1. 操作系统：Windows 11 专业版 `23H2`（OS Build `22631.5472`）。
2. Python 环境：`Miniconda` 的 `kan` 环境，解释器路径 `C:\Users\chenpeng\miniconda3\envs\kan\python.exe`（Python `3.9.25`）。
3. CPU：`12th Gen Intel(R) Core(TM) i5-12500H`。
4. 内存：`16 GB`。
5. 运行路径：`PyTorch 2.1.2+cpu`。

## 7. 报告书写建议

建议采用“四层叙述”结构：

1. 历史参考结果：用于提供研究脉络与可复现边界。
2. 工程版总体复测结果：用于说明工程版相对历史版的总体口径。
3. layered 库 ICBR 对照：用于证明 backend-only compare 语义已经修干净。
4. FAST_LIB ICBR 对照：用于说明在更大候选库下 ICBR 的速度潜力。

同时应设置“差异归因”小节，至少覆盖以下维度：

1. 守护策略变化带来的稳定性与安全收益。
2. 配置与可观测性增强带来的工程可维护性收益。
3. shared symbolic-prep cache 与 trace 对齐的公平性含义。
4. 函数库扩大后，候选生成与 replay rerank 在总耗时中的占比变化。

## 8. 建议配套文档

建议同时维护以下两类报告：

1. 工程版总体口径报告。
2. ICBR 后端对照报告。

当前对应文件为：

1. [engineering_rerun_report.md](engineering_rerun_report.md)
2. [symkanbenchmark_usage.md](symkanbenchmark_usage.md)

## 9. 当前状态

1. 历史参考版已通过 release 冻结，不再建议频繁回切旧版本重跑。
2. 工程版总体口径仍可参考 `2026-03-18` 的 rerun 归档。
3. 当前关于 ICBR 接入的正式引用锚点应优先使用 `outputs/rerun_v2_engine_safe_20260401/benchmark_ab/comparison_fastlib/` 及其配套报告；`comparison/` 保留为更保守的 layered 库参考切片。
4. 后续若继续扩展 symbolic backend 或 library-only compare 变体，对外口径仍应保持：历史版用于参考，工程版用于正式结论，而 backend compare 需明确共享边界与专用 compare 产物。
