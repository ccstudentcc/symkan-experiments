# 工程版复测与历史结果口径说明

## 1. 文档目的

本文档用于界定“历史参考版本”与“当前工程版本”在实验口径上的差异，并统一说明当前工程版内部的两组 paired ICBR 后端对照与一组补充单变体切片：

1. `baseline` vs `baseline_icbr`
   用于最保守的 layered 库 backend-only 对照。
2. `baseline_fastlib` vs `baseline_icbr_fastlib`
   用于在更大候选函数库下观察 ICBR 的速度潜力。
3. `baseline_icbr_fulllib`
   用于补充观察 ICBR 在 full symbolic library 下的单边运行表现；由于 `baseline_fulllib` 过慢而未纳入本轮复测，它不构成 paired backend-only compare。

前两组 paired 对照可解释为“同一工程版内部的后端比较”；第三组仅是补充单边实验，不应用来替代 paired compare 结论。

## 2. 版本分层定义

1. 历史参考版：`d8e09b5edadb988bd4a1638ea7109cf3ff5ef7d7`，对应 pre-release `v1.0.0-legacy-d8`。
2. 当前工程版：`main` 分支，包含配置模块化、守护策略分级、共享 symbolic-prep cache 与 ICBR 后端接入等工程化改造。

论文、报告或答辩材料应显式声明：历史版本仅作为参考锚点，工程版本用于当前正式结论。

## 3. 两代结果不可直接等价的原因

1. 训练与剪枝守护策略存在实质差异，尤其体现在失败边界判定与回滚机制。
2. 工程版扩展了耗时指标体系，新增 `run_total_wall_time_s`、`symbolize_wall_time_s`、`symbolic_core_seconds` 等字段。
3. 配置管理方式已收敛到 `AppConfig` 统一入口，CLI 仅承担受控覆盖。
4. 跨版本耗时字段并非完全同名：跨代对照时仅允许将 `export_wall_time_s` 语义映射到 `symbolize_wall_time_s`；`run_total_wall_time_s` 为工程版新增字段。

因此，工程版与历史版间出现时延差异属于方法学差异下的预期现象，不宜直接解释为模型性能退化。

## 4. 当前工程版复测锚点

当前工程版建议区分四个锚点：

1. 工程版总体口径锚点：
   - 正式主引用归档：`outputs/rerun_v2_engine_safe_20260318_rerun/`
   - 同日较早归档：`outputs/rerun_v2_engine_safe_20260318/`（前序结果保留，不作为当前总体 rerun 正式正文主锚点）
2. layered 库 ICBR 对照锚点：
   - `outputs/rerun_v2_engine_safe_20260401/benchmark_ab/comparison/`
3. FAST_LIB ICBR 对照锚点：
   - `outputs/rerun_v2_engine_safe_20260401/benchmark_ab/comparison_fastlib/`
4. full symbolic library 的补充单变体锚点：
   - `outputs/rerun_v2_engine_safe_20260401/benchmark_ab/baseline_icbr_fulllib/`

若当前写作主题是“paired backend compare 的公平性与质量变化”，优先引用第二组与第三组锚点；若只是补充说明“baseline_fulllib 太慢，因此改用 ICBR full library 单边切片观察速度与收益”，可附带引用第四组锚点，但需显式写明它不是 paired compare 证据。

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

## 6. 参考执行环境

1. 操作系统：Windows 11 专业版 `23H2`（OS Build `22631.5472`）。
2. Python 环境：`Miniconda` 的 `kan` 环境，解释器路径 `C:\Users\chenpeng\miniconda3\envs\kan\python.exe`（Python `3.9.25`）。
3. CPU：`12th Gen Intel(R) Core(TM) i5-12500H`。
4. 内存：`16 GB`。
5. 运行路径：`PyTorch 2.1.2+cpu`。

## 7. 报告书写结构

当前维护口径按“五层叙述”结构组织：

1. 历史参考结果：用于提供研究脉络与可复现边界。
2. 工程版总体复测结果：用于说明工程版相对历史版的总体口径。
3. layered 库 ICBR 对照：用于证明 backend-only compare 语义已经修干净。
4. FAST_LIB ICBR 对照：用于说明在更大候选库下 ICBR 的速度潜力。
5. full symbolic library 单变体补充：用于说明 baseline full library 成本过高时，ICBR 自身在更大全库下仍可运行并带来单边收益，但不承担 paired fairness 证明职责。

“差异归因”小节至少覆盖以下维度：

1. 守护策略变化带来的稳定性与安全收益。
2. 配置与可观测性增强带来的工程可维护性收益。
3. shared symbolic-prep cache 与 trace 对齐的公平性含义。
4. 函数库扩大后，候选生成与 replay rerank 在总耗时中的占比变化。

## 8. 配套文档结构

当前应同时维护以下三类文档：

1. 稳定入口页：负责最新带日期报告与历史报告导航。
2. 带日期正式报告：负责单轮实验的配置、命令、结果表与结论。
3. benchmark 使用文档：负责命令口径、指标语义与 compare 产物解释。

当前对应文件为：

1. [engineering_rerun_report.md](engineering_rerun_report.md)
2. [engineering_rerun_report_20260318.md](engineering_rerun_report_20260318.md)
3. [engineering_rerun_report_20260401.md](engineering_rerun_report_20260401.md)
4. [symkanbenchmark_usage.md](symkanbenchmark_usage.md)

## 9. 当前状态

1. 历史参考版已通过 release 冻结，不再建议频繁回切旧版本重跑。
2. 工程版总体口径当前以 `2026-03-18` 的带日期正式正文和 `outputs/rerun_v2_engine_safe_20260318_rerun/` 为主引用。
3. 当前关于 ICBR 接入的正式引用应按论点拆分：`comparison/` 用于较保守的 paired backend-only 结论，`comparison_fastlib/` 用于更大候选库下的 paired speed 结论，`baseline_icbr_fulllib/` 只用于补充单变体观察。
4. 后续若继续扩展 symbolic backend 或 library-only compare 变体，对外口径仍应保持：历史版用于参考，工程版用于正式结论，而 backend compare 需明确共享边界、paired compare 产物与单边补充切片之间的差异。
5. 以后新增 rerun 报告时，应新建 `engineering_rerun_report_YYYYMMDD.md`，并只在 [engineering_rerun_report.md](engineering_rerun_report.md) 更新 latest/history 导航，不覆盖旧带日期正文。
