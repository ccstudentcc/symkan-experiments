# docs 文档索引

本文档用于说明 `docs/` 目录的知识结构、阅读路径与文档间依赖关系，可作为项目文档系统的统一入口。

## 0. 统一口径速查

1. 入口口径：常规 CLI 使用 `python -m scripts.*`；工程版复测可使用 `scripts/run_engineering_rerun.ps1` 作为编排封装入口。
2. 输出口径：项目默认输出为 `outputs/benchmark_*`；手册示例输出为 `outputs/rerun/*`；工程归档输出为 `outputs/rerun_v2_engine_safe_<date>/*`。
3. 配置来源口径：自动默认来源仅 `configs/symkanbenchmark.default.yaml`；`configs/ablation_runner.default.yaml` 与 `configs/benchmark_ab/*.yaml` 均为显式模板，需通过 `--config` 传入。
4. 跨版本指标口径：仅将 `export_wall_time_s` 语义映射到 `symbolize_wall_time_s`；`run_total_wall_time_s` 为工程版新增字段，历史版无同名可比项。

## 0.1 文档写作规范速查

1. 代码块语言：命令示例统一使用 `powershell` 代码块，不使用 `bash` / `sh` / `shell`。
2. 运行目录注释：每个命令代码块首行必须注明 `# 运行目录：仓库根目录（symkan-experiments/）`。
3. 命令换行风格：多行命令统一使用 PowerShell 续行符 `` ` ``，不使用反斜杠 `\`。
4. 参考环境放置规则：
   - 执行类文档（如 `symkanbenchmark_usage.md`、`ablation_usage.md`、`full_experiment_runbook.md`）应在“运行方式/运行入口”章节前给出“参考环境（用于结果解释）”。
   - 报告类文档应在“研究设定与口径/默认设定”章节给出设备与运行时环境。
   - 同一轮实验复测使用同一套环境描述，避免跨文档表述不一致。

## 0.2 最近改动同步基线（2026-03-19）

本节用于把“最近工程改动”显式绑定到文档系统，避免只改代码不改叙述。

1. 配置统一：Notebook / CLI / 库层统一收敛到 `AppConfig`；相关叙述应与 `README.md`、`symkan_usage.md` 保持一致。
2. Notebook 桥接收口：`symkan.config.notebook` 负责 canonical 化；`symkan.notebook_compat` 仅为薄桥接，不应在其他文档中被描述为“主配置层”。
3. 命令风格统一：执行命令统一 `python -m scripts.*`（工程复测可补充 `scripts/run_engineering_rerun.ps1`），并保持 PowerShell 代码块风格。
4. 指标口径统一：跨版本耗时字段仅允许 `export_wall_time_s -> symbolize_wall_time_s` 语义映射；`run_total_wall_time_s` 视为工程版新增字段。
5. 发布前一致性检查：每次 release 前应对 `README.md` 与 `docs/` 执行一次“口径同步复核”（见 `engineering_release_checklist.md`）。

## 0.3 文档同步矩阵（SSOT）

文档同步规则的单一真源见 [doc_sync_matrix.md](doc_sync_matrix.md)。

1. 日常改动：先按矩阵判断“本次改动影响哪些文档”。
2. 发布前：在 `engineering_release_checklist.md` 中逐项勾选，并以矩阵为准做最终收口。

## 1. 建议起始阅读路径

对于首次接触本仓库的读者，建议按如下顺序建立整体认知：

1. [project_map.md](project_map.md)：理解仓库结构、脚本职责与结果目录组织方式。
2. [symkan_usage.md](symkan_usage.md)：理解核心库接口、配置入口及方法边界。
3. [symkanbenchmark_usage.md](symkanbenchmark_usage.md)：理解批量实验入口、输出产物与统计口径。

完成上述阅读后，通常可形成对项目定位、实现边界与实验流程的完整基础认知。

## 2. 按主题导航

### 2.1 架构与设计

1. [project_map.md](project_map.md)：项目地图与阅读入口。
2. [design.md](design.md)：模块边界、设计约束与默认策略依据。
3. [../ARCHITECTURE.md](../ARCHITECTURE.md)：库层与脚本层的系统级架构。

### 2.2 核心库与参数体系

1. [symkan_usage.md](symkan_usage.md)：核心 API、`AppConfig` 与结果字段语义。
2. [kan_parameters.md](kan_parameters.md)：`notebooks/kan.ipynb` 的参数位置、作用与调节顺序。

补充口径：

1. `symkan.config` 不只负责 YAML；旧 notebook 的函数式参数兼容与 canonical 名字归一化也收敛在该层。
2. `symkan.notebook_compat` 仅保留 notebook 调用到现有运行时入口的薄桥接职责。

### 2.3 实验执行与复现

1. [symkanbenchmark_usage.md](symkanbenchmark_usage.md)：主 benchmark CLI 与 A/B 结果口径。
2. [ablation_usage.md](ablation_usage.md)：单因素消融与 LayerwiseFT 专项实验说明。
3. [full_experiment_runbook.md](full_experiment_runbook.md)：完整复跑操作手册。
4. [engineering_version_rerun_note.md](engineering_version_rerun_note.md)：历史版与工程版口径分层说明。
5. [engineering_rerun_report.md](engineering_rerun_report.md)：工程版复测报告及对照分析。
6. [engineering_release_checklist.md](engineering_release_checklist.md)：工程版发布前检查清单。

### 2.4 报告与结论解释

1. [ablation_report.md](ablation_report.md)：单因素消融结论与解释边界。
2. [layerwiseft_improved_report.md](layerwiseft_improved_report.md)：改进版 LayerwiseFT 比较结果。
3. [ablation_plan.md](ablation_plan.md)：实验设计目标、约束与风险控制。

### 2.5 发布记录归档

1. [archive/releases/engineering_release_record_20260319.md](archive/releases/engineering_release_record_20260319.md)：`2026-03-19` 工程版发布记录示例。
2. 后续发布记录统一归档到 `docs/archive/releases/`，文件命名建议为 `engineering_release_record_YYYYMMDD.md`。

## 3. 按任务场景选择路径

1. 项目全貌快速建立：`project_map -> symkan_usage -> symkanbenchmark_usage`
2. 架构与实现边界梳理：`project_map -> ../ARCHITECTURE.md -> design`
3. 实验复现：`symkanbenchmark_usage -> ablation_usage`
4. 全流程复跑：`full_experiment_runbook -> symkanbenchmark_usage -> ablation_usage`
5. 报告撰写：`engineering_version_rerun_note -> engineering_rerun_report -> ablation_report`
6. 发布前确认：`engineering_release_checklist -> engineering_version_rerun_note -> engineering_rerun_report`

## 4. 返回项目入口

1. 项目总览：[../README.md](../README.md)
