# SymKAN 中文论文材料

本目录用于把 `symkan-experiments` 现有的设计文档、工程复测报告、主手稿和答辩材料，重新整理成更适合毕业论文正文复用的中文写作入口。

这里不替代原有 `docs/design.md`、`docs/symkan_manuscript.md`、各类 rerun report 或 runbook，而是做三件事：收束研究定位、固定证据层级、给出可以直接搬进论文的表述边界。

## 文件说明

- [`01_研究定位.md`](01_研究定位.md)：说明 SymKAN 研究对象是什么，哪些说法不宜写成本文贡献。
- [`02_方法边界与系统结构.md`](02_方法边界与系统结构.md)：整理配置边界、阶段拆分、公平比较边界与结构化导出逻辑。
- [`03_证据层级与结果引用.md`](03_证据层级与结果引用.md)：把总体 rerun、消融、LayerwiseFT、paired compare 和补充单边结果分层。
- [`04_论文结果写法与禁用表述.md`](04_论文结果写法与禁用表述.md)：给出正文常用句式、易误写点和更稳妥的替代表述。
- [`05_术语表与推荐译法.md`](05_术语表与推荐译法.md)：统一中英文术语，减少不同章节里的语义漂移。

## 使用建议

- 写“本文方法”与“工程化符号化流程”时，先读 `01` 和 `02`。
- 写实验章节时，先读 `03`，再按需要引用现有 report。
- 写答辩稿、摘要或结果讨论时，优先参照 `04`。
- 写整篇论文前，先用 `05` 固定术语。

## 固定边界

- 本目录是 `symkan-experiments` 的主实验论文材料入口。
- 这里整理的是写作口径，不是新的实验结果目录。
- 若需要运行命令、复现实操或输出字段解释，仍应回到 `docs/symkan_usage.md`、`docs/symkanbenchmark_usage.md`、`docs/ablation_usage.md` 和 `docs/full_experiment_runbook.md`。

## 可引用的参考报告

- [`docs/design.md`](../design.md)：适合引用研究定位、方法边界与证据分层原则。
- [`docs/symkan_manuscript.md`](../symkan_manuscript.md)：适合引用论文式主叙述、结果组织顺序与外部文献定位。
- [`docs/engineering_rerun_report_20260318.md`](../engineering_rerun_report_20260318.md)：适合引用当前工程版总体 rerun、默认主路径与工程策略对照。
- [`docs/engineering_rerun_report_20260401.md`](../engineering_rerun_report_20260401.md)：适合引用 layered paired、FAST_LIB paired 与 `baseline_icbr_fulllib` 的边界说明。
- [`docs/ablation_report.md`](../ablation_report.md)：适合引用 Stagewise、Pruning、Input Compaction 与 LayerwiseFT 的模块职责。
- [`docs/layerwiseft_improved_report.md`](../layerwiseft_improved_report.md)：适合引用改进版 LayerwiseFT 仍不宜作为默认设置的专题结论。

## 可引用的数据来源

- [`outputs/rerun_v2_engine_safe_20260318_rerun/benchmark_runs/symkanbenchmark_runs.csv`](../../outputs/rerun_v2_engine_safe_20260318_rerun/benchmark_runs/symkanbenchmark_runs.csv)：总体 rerun 的主汇总表。
- [`outputs/rerun_v2_engine_safe_20260401/benchmark_ab/comparison/variant_summary.csv`](../../outputs/rerun_v2_engine_safe_20260401/benchmark_ab/comparison/variant_summary.csv)：layered paired 的主汇总表。
- [`outputs/rerun_v2_engine_safe_20260401/benchmark_ab/comparison/baseline_icbr_shared_check.csv`](../../outputs/rerun_v2_engine_safe_20260401/benchmark_ab/comparison/baseline_icbr_shared_check.csv)：backend-only compare 的 shared-state 对齐依据。
- [`outputs/rerun_v2_engine_safe_20260401/benchmark_ab/comparison_fastlib/variant_summary.csv`](../../outputs/rerun_v2_engine_safe_20260401/benchmark_ab/comparison_fastlib/variant_summary.csv)：FAST_LIB paired 的主汇总表。
- [`outputs/benchmark_ablation/ablation_runs_summary.csv`](../../outputs/benchmark_ablation/ablation_runs_summary.csv)：四模块单点消融的主汇总表。
- [`outputs/benchmark_ablation/layerwiseft_improved_analysis/comparison_summary.csv`](../../outputs/benchmark_ablation/layerwiseft_improved_analysis/comparison_summary.csv)：LayerwiseFT 专题比较汇总。

## 可引用的参考图表或图表来源

- [`docs/slides/symkan_manuscript_companion.pdf`](../slides/symkan_manuscript_companion.pdf)：可作为答辩展示层的现成图表汇总，但不替代正文原始证据。
- [`docs/slides/symkan_slide_data.tex`](../slides/symkan_slide_data.tex)：当前 slide 中表格与数值的直接来源，适合核对展示稿口径。
- [`outputs/rerun_v2_engine_safe_20260401/benchmark_ab/comparison/pairwise_delta_summary.csv`](../../outputs/rerun_v2_engine_safe_20260401/benchmark_ab/comparison/pairwise_delta_summary.csv)：可据此重画 backend paired 对比图。
- [`outputs/rerun_v2_engine_safe_20260401/benchmark_ab/comparison_fastlib/pairwise_delta_summary.csv`](../../outputs/rerun_v2_engine_safe_20260401/benchmark_ab/comparison_fastlib/pairwise_delta_summary.csv)：可据此重画 FAST_LIB paired 对比图。
- [`outputs/benchmark_ablation/ablation_runs_summary.csv`](../../outputs/benchmark_ablation/ablation_runs_summary.csv)：可据此重画模块消融柱状图或表格。
- 当前仓库没有单独维护“论文主文图目录”；正文图表更稳妥的做法，是从上述 CSV、JSON 和现有 report 中重新制图，而不是截取 notebook 画面。
