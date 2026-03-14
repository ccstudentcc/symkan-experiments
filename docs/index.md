# docs 文档导航

本页用于集中导航 `docs/` 下的说明文档，帮助你按目标快速找到对应内容。

## 快速入口

- 返回项目总览：[README](../README.md)
- 首次使用建议先读：[symkan_usage.md](symkan_usage.md)
- 批量实验建议先读：[symkanbenchmark_usage.md](symkanbenchmark_usage.md)

## 按任务导航

### 1. 快速上手与整体理解

- [symkan_usage.md](symkan_usage.md)：项目定位、理论背景、核心 API、快速示例。
- [design.md](design.md)：架构边界、设计取舍、兼容原则。

### 2. 跑实验与看结果

- [symkanbenchmark_usage.md](symkanbenchmark_usage.md)：CLI 参数、输出文件、A/B 结论口径。
- [kan_parameters.md](kan_parameters.md)：`kan.ipynb` 与主流程参数解释。

### 3. 做消融与写报告

- [ablation_usage.md](ablation_usage.md)：消融脚本命令与输出结构。
- [ablation_plan.md](ablation_plan.md)：消融实验设计与约束。
- [ablation_report.md](ablation_report.md)：单点消融结果与结论。
- [layerwiseft_improved_report.md](layerwiseft_improved_report.md)：LayerwiseFT 改进版对比结论。

## 推荐阅读顺序

1. 新用户：`symkan_usage` -> `symkanbenchmark_usage` -> `kan_parameters`
2. 论文复现：`symkanbenchmark_usage` -> `ablation_usage` -> `ablation_report`
3. 方法论讨论：`design` -> `ablation_plan` -> `layerwiseft_improved_report`
