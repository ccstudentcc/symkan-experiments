# 项目地图

本文围绕以下三个问题组织：

1. 仓库包含哪些组成部分。
2. 各文档与代码入口之间的关系是什么。
3. 在实验复现、代码阅读和报告撰写情形下，应参考哪些位置。

本文提供仓库结构、代码入口与结果位置的结构化地图；完整文档导航以 [index.md](index.md) 为准。

## 概述

该仓库围绕 KAN 的符号化流程组织。`symkan/` 提供工程化库接口，其中既包括算法执行模块，也包括统一配置入口；根目录脚本负责批量实验与分析，`docs/` 提供方法、参数和实验结论的说明。

## 工程版口径入口（2026-04）

1. 口径边界入口：[engineering_version_rerun_note.md](engineering_version_rerun_note.md)。
2. 工程版实验报告稳定入口：[engineering_rerun_report.md](engineering_rerun_report.md)。
3. 发布收口入口：[engineering_release_checklist.md](engineering_release_checklist.md)。
4. 本文只负责结构地图；跨版本结论与正式证据引用以上述文档为准。

## 仓库组成

### 1. `symkan/`

该目录是仓库的核心实现层，也是主要复用逻辑所在。

- `symkan/config/`：统一配置层，负责 `AppConfig`、子配置 schema、YAML 加载、环境变量占位符展开、配置校验，以及 notebook 函数式参数到 `AppConfig` 的 canonical 化转换；脚本与库层最终都收敛到这一层。
- `symkan/core/`：设备、数据集、训练基础接口、结构化类型；dataset 构建同时兼容 1D 类别索引和 2D one-hot/概率标签。
- `symkan/tuning/`：`stagewise_train` 和相关自适应控制逻辑。
- `symkan/symbolic/`：函数库、输入压缩、逐层符号化、主流水线。
- `symkan/pruning/`：归因与剪枝辅助逻辑。
- `symkan/eval/`：ROC/AUC 和公式数值验证。
- `symkan/io/`：结果导出、bundle 读写；bundle 读取仅面向显式信任的本地 pickle 文件。

因此，`symkan/` 不只是“算法核心层”，也是“统一配置口径”的实现层。理解项目主流程时，通常应把 `symkan/config/` 与 `symkan/tuning/`、`symkan/symbolic/` 一起看，而不是只看训练和符号化模块。

### 2. `kan/`

该目录对应与 `pykan` 兼容或紧耦合的实现层；`symkan/` 在其上构建更稳定的流程封装。

### 3. 根目录脚本

这些脚本分别对应不同的实验任务。为保持命令与文档示例稳定，根目录保留同名入口文件（shim）；脚本的可读实现统一放在 `scripts/` 下。

- `symkanbenchmark.py`
  主实验入口。负责批量运行完整流程，导出主表、阶段日志、符号化轨迹和验证结果；当前还负责 `_numeric_cache/` 与 `_symbolic_prep_cache/` 两级缓存。
- `ablation_runner.py`
  单因素消融矩阵。用统一参数运行 `full / wostagewise / wopruning / wocompact / wolayerwiseft`。
- `benchmark_ab_compare.py`
  A/B 对比汇总。默认生成通用 compare 表；当比较对为单个 baseline-backend vs 单个 icbr-backend pair 时，会额外生成 shared-check、primary-effect 与 mechanism-summary 三份专用 compare 产物。
- `analyze_layerwiseft.py`
  专门分析 `full` 和 `wolayerwiseft` 的差异。
- `compare_layerwiseft_improved.py`
  运行并汇总改进版 LayerwiseFT 相对 `full / wolayerwiseft` 的结果。

这些脚本当前统一采用“`AppConfig` + 脚本编排参数”的模式：

- `symkanbenchmark.py` 先用 `symkan.config.load_config()` 读取 `AppConfig`；若省略 `--config`，会回退到 `configs/symkanbenchmark.default.yaml`，再只对白名单字段做显式覆盖。
- `ablation_runner.py` 可把一份共享 `AppConfig` 透传给各变体；若省略 `--config`，每次委托运行最终仍回退到 `symkanbenchmark.py` 的默认配置来源。脚本层还负责组织 variants / output-dir / seeds / quiet / verbose。
- `compare_layerwiseft_improved.py` 当前没有单独的 `AppConfig` YAML 入口；它基于 benchmark 默认配置来源，再叠加少量 layerwise / seed 相关 CLI 覆盖。
- 更底层的训练/符号化逻辑继续直接依赖 `symkan.config.AppConfig`。

### 4. `docs/`

该目录用于集中放置面向读者的说明性文档。

- 导航文档：`index.md`、`project_map.md`，负责入口与阅读路径。
- 治理文档：`documentation_governance.md`、`doc_sync_matrix.md`、`engineering_release_checklist.md`，负责维护链路、同步规则与发布收口。
- 用法文档：说明运行方式与参数。
- 设计/手稿文档：`design.md` 负责设计动机、约束与证据边界，`symkan_manuscript.md` 负责论文式主叙述。
- 展示文档：`docs/slides/` 负责与手稿对齐的 Beamer 源码与口头报告压缩叙事。
- 实验报告：说明当前证据所支持的结论范围。

### 5. 结果目录

- `outputs/benchmark_ab/`：A/B 对比结果。
- `outputs/benchmark_ablation/`：单因素消融与 LayerwiseFT 分析结果。
- `outputs/notebooks/`：`notebooks/kan.ipynb` 导出的结构化 CSV。
- `outputs/rerun_v2_engine_safe_20260318_rerun/`：当前工程版总体 rerun 的正式归档目录。
- `outputs/rerun_v2_engine_safe_20260401/benchmark_ab/`：当前 ICBR 接入结果的工程归档目录。

这些目录既保存实验产物，也构成当前文档结论的主要证据来源。

补充说明：运行 `notebooks/kan.ipynb` 时，会在 `notebooks/` 下自动生成 `model/` 目录，用于存放运行期模型文件；结构化 CSV 则统一写入 `outputs/notebooks/`。

当前 notebook 兼容链路的职责拆分为：

1. `symkan.config.notebook`：负责旧 notebook flat kwargs 的参数转换、canonical 名字归一化与 alias 兜底兼容。
2. `symkan.notebook_compat`：负责将 notebook 风格调用接到现有 `stagewise_train` / `symbolize_pipeline` 运行时入口。

## 结构相关入口

完整文档导航见 [index.md](index.md)。本页只保留与仓库结构、代码入口和结果位置直接相关的入口：

1. 仓库总览：[../README.md](../README.md)
2. 系统级架构：[../ARCHITECTURE.md](../ARCHITECTURE.md)
3. 核心库与参数说明：[symkan_usage.md](symkan_usage.md)
4. 主 benchmark 入口与输出：[symkanbenchmark_usage.md](symkanbenchmark_usage.md)
5. 设计与结论入口：[design.md](design.md)、[symkan_manuscript.md](symkan_manuscript.md)、[slides/README.md](slides/README.md)、[engineering_rerun_report.md](engineering_rerun_report.md)
6. 文档治理与发布收口：[documentation_governance.md](documentation_governance.md)、[doc_sync_matrix.md](doc_sync_matrix.md)、[engineering_release_checklist.md](engineering_release_checklist.md)

## 主工作流

项目主流程可概括为：

1. 准备数据，统一成 `dataset` 字典。
2. 用 `stagewise_train` 将模型推进到可符号化区间。
3. 用共享 symbolic-prep 阶段完成渐进剪枝、输入压缩与 pre-symbolic fit。
4. 用 backend-specific symbolic completion 执行 `baseline` 或 `icbr` 后端。
5. 用 `validate_formula_numerically` 检查导出公式是否仍能近似模型输出。
6. 把日志、轨迹、指标和公式导出到 CSV / JSON / bundle。

训练阶段的作用是将模型推进到适于符号化的区间；符号化阶段的作用是生成可验证、可导出的表达式。两者在实现上保持分离，有助于控制复杂度并提高结果可追溯性。

## 代码阅读入口

如需进一步阅读代码，可优先从以下入口开始：

- `symkan/config/loader.py`
- `symkan/config/schema.py`
- `symkan/config/notebook.py`
- `symkan/notebook_compat.py`
- `symkan/core/__init__.py`
- `symkan/tuning/stagewise.py`
- `symkan/symbolic/pipeline.py`
- `symkan/eval/metrics.py`
- `symkanbenchmark.py`

这些位置共同决定了配置流、数据流、结果落盘方式以及实验脚本与公共库之间的接口关系。

## 结论入口

1. 默认流程、模块职责与设计边界：见 [design.md](design.md)、[symkan_manuscript.md](symkan_manuscript.md)、[slides/README.md](slides/README.md) 与 [ablation_report.md](ablation_report.md)。
2. LayerwiseFT 专题结论：见 [layerwiseft_improved_report.md](layerwiseft_improved_report.md)。
3. 工程版总体 rerun 与 ICBR backend compare 的正式结论：见 [engineering_rerun_report.md](engineering_rerun_report.md) 及对应带日期正文。
