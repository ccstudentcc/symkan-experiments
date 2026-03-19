# 项目地图

本文围绕以下三个问题组织：

1. 仓库包含哪些组成部分。
2. 各文档与代码入口之间的关系是什么。
3. 在实验复现、代码阅读和报告撰写情形下，应参考哪些位置。

对于初次接触该仓库的读者，本文可作为文档与代码入口的总览。

## 概述

该仓库围绕 KAN 的符号化流程组织。`symkan/` 提供工程化库接口，其中既包括算法执行模块，也包括统一配置入口；根目录脚本负责批量实验与分析，`docs/` 提供方法、参数和实验结论的说明。

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
  主实验入口。负责批量运行完整流程，导出主表、阶段日志、符号化轨迹和验证结果。
- `ablation_runner.py`
  单因素消融矩阵。用统一参数运行 `full / wostagewise / wopruning / wocompact / wolayerwiseft`。
- `benchmark_ab_compare.py`
  A/B 对比汇总。把 `baseline / adaptive / adaptive_auto` 的结果整理成论文友好的表。
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

- 用法文档：说明运行方式与参数。
- 设计文档：说明设计动机与约束。
- 实验报告：说明当前证据所支持的结论范围。

### 5. 结果目录

- `outputs/benchmark_ab/`：A/B 对比结果。
- `outputs/benchmark_ablation/`：单因素消融与 LayerwiseFT 分析结果。
- `outputs/notebooks/`：`notebooks/kan.ipynb` 导出的结构化 CSV。

这些目录既保存实验产物，也构成当前文档结论的主要证据来源。

补充说明：运行 `notebooks/kan.ipynb` 时，会在 `notebooks/` 下自动生成 `model/` 目录，用于存放运行期模型文件；结构化 CSV 则统一写入 `outputs/notebooks/`。

当前 notebook 兼容链路的职责拆分为：

1. `symkan.config.notebook`：负责旧 notebook flat kwargs 的参数转换、canonical 名字归一化与 alias 兜底兼容。
2. `symkan.notebook_compat`：负责将 notebook 风格调用接到现有 `stagewise_train` / `symbolize_pipeline` 运行时入口。

## 阅读入口

### 总览阅读

可按以下顺序阅读：

1. [../README.md](../README.md)
2. [symkan_usage.md](symkan_usage.md)
3. [symkanbenchmark_usage.md](symkanbenchmark_usage.md)

### 架构阅读

可按以下顺序阅读：

1. [../ARCHITECTURE.md](../ARCHITECTURE.md)
2. [design.md](design.md)
3. [symkan_usage.md](symkan_usage.md)

### 实验复现

可按以下顺序阅读：

1. [symkanbenchmark_usage.md](symkanbenchmark_usage.md)
2. [ablation_usage.md](ablation_usage.md)
3. [ablation_report.md](ablation_report.md)

### 方法说明与结果表述

可按以下顺序阅读：

1. [design.md](design.md)
2. [ablation_report.md](ablation_report.md)
3. [layerwiseft_improved_report.md](layerwiseft_improved_report.md)

## 主工作流

项目主流程可概括为：

1. 准备数据，统一成 `dataset` 字典。
2. 用 `stagewise_train` 将模型推进到可符号化区间。
3. 用 `symbolize_pipeline` 做渐进剪枝、输入压缩、逐层符号化和微调。
4. 用 `validate_formula_numerically` 检查导出公式是否仍能近似模型输出。
5. 把日志、轨迹、指标和公式导出到 CSV / JSON / bundle。

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

## 当前可引用的主要结论

当前文档中相对稳定的结论包括以下三项：

1. `stagewise_train` 不是装饰品，而是整条符号化链路可用性的前提。
2. 渐进剪枝和输入压缩主要负责复杂度与耗时治理，不应简单表述成“默认提精度模块”。
3. 对典型 2 层 KAN，LayerwiseFT 目前更像按需开关，而不是默认收益项。

这些结论的详细证据都在：

- [ablation_report.md](ablation_report.md)
- [layerwiseft_improved_report.md](layerwiseft_improved_report.md)

## 说明

在进入专题文档前先建立项目地图，有助于降低跨文档跳转带来的理解成本。
