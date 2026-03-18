# docs 文档导航

本页说明 `docs/` 目录中文档的主题范围及其相互关系，可作为仓库文档系统的总入口。

## 基础阅读路径

首次阅读本仓库时，可按以下顺序建立整体认识：

1. [project_map.md](project_map.md)：了解仓库组成、脚本职责与结果目录。
2. [symkan_usage.md](symkan_usage.md)：理解核心库接口、主流程与方法边界。
3. [symkanbenchmark_usage.md](symkanbenchmark_usage.md)：了解批量实验入口、输出产物与结果解释方式。

完成上述阅读后，通常即可形成对项目定位、代码结构与实验工作流的基本理解。

## 按任务导航

### 1. 项目结构与设计

- [project_map.md](project_map.md)：仓库地图、脚本职责与阅读入口。
- [design.md](design.md)：模块边界、设计约束与项目层默认设定的依据。
- [../ARCHITECTURE.md](../ARCHITECTURE.md)：公共库层与实验脚本层的整体架构。

### 2. 核心库与参数

- [symkan_usage.md](symkan_usage.md)：核心 API、`AppConfig` 配置层、最小示例与结果字段说明。
- [kan_parameters.md](kan_parameters.md)：`notebooks/kan.ipynb` 的参数含义与调节顺序。

### 3. 实验运行与结果读取

- [symkanbenchmark_usage.md](symkanbenchmark_usage.md)：主 benchmark CLI、输出文件与 A/B 结果口径。
- [ablation_usage.md](ablation_usage.md)：单因素消融与 LayerwiseFT 专项对比脚本说明。
- [full_experiment_runbook.md](full_experiment_runbook.md)：按步骤复跑完整实验链路的操作手册。
- [engineering_version_rerun_note.md](engineering_version_rerun_note.md)：历史参考版与工程版复测的口径分层说明。
- [engineering_rerun_report.md](engineering_rerun_report.md)：工程版复测结果报告（含与历史版对照结构）。

这几份文档同时说明了当前的运行配置约定：Notebook / Python 优先直接构造 `AppConfig`，批量实验优先 `AppConfig` YAML + 少量显式 CLI 覆盖，而底层统一消费 `AppConfig`。

### 4. 结果报告与结论边界

- [ablation_report.md](ablation_report.md)：单因素消融结果及其解释边界。
- [layerwiseft_improved_report.md](layerwiseft_improved_report.md)：改进版 LayerwiseFT 的比较结果。
- [ablation_plan.md](ablation_plan.md)：消融实验设计的背景、目标与约束。

## 按使用情形选择路径

- 阅读项目全貌：`project_map -> symkan_usage -> symkanbenchmark_usage`
- 阅读架构与实现边界：`project_map -> ../ARCHITECTURE.md -> design`
- 复现实验：`symkanbenchmark_usage -> ablation_usage`
- 完整复跑：`full_experiment_runbook -> symkanbenchmark_usage -> ablation_usage`
- 撰写报告或论文：`ablation_report -> layerwiseft_improved_report -> design`

## 返回项目入口

- 项目总览：[../README.md](../README.md)
