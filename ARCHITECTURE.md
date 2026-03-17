# 架构总览

## 目标

该仓库围绕 KAN 的训练、符号化、实验复现与结果导出展开。

架构上分为两层：

- 能力层：`kan/` 和 `symkan/`
- 实验层：根目录脚本与结果目录

运行 `notebooks/kan.ipynb` 时，会在 `notebooks/` 下自动生成 `model/` 目录，用于承接运行期模型产物；该目录不属于仓库整理后的固定功能分层。

这一划分用于区分模型能力实现与实验编排逻辑，从而降低接口和产物格式的耦合程度。

## 模块边界

### `kan/`

提供 KAN 相关底层实现与兼容能力。这里更接近模型本体，不承担实验编排职责。

### `symkan/`

该层作为仓库的公共库层，负责组织训练、符号化、评估和导出接口。

- `symkan.core`
  负责设备管理、数据集构建、训练基础函数、结构化类型。
- `symkan.tuning`
  负责 `stagewise_train`、阶段快照、选模和自适应节奏控制。
- `symkan.symbolic`
  负责函数库、表达式处理、输入压缩和 `symbolize_pipeline`。
- `symkan.pruning`
  负责归因和剪枝辅助逻辑。
- `symkan.eval`
  负责 ROC/AUC 与公式数值验证。
- `symkan.io`
  负责 CSV、JSON、bundle 的导出与读取。

### 根目录脚本

这些脚本构成实验编排层。为保持使用方式稳定，根目录保留同名入口文件（shim）；脚本实现统一放在 `scripts/` 下。

- `symkanbenchmark.py`
  主实验入口，负责多 seed 运行、结果汇总和标准导出。
- `ablation_runner.py`
  单因素消融矩阵执行器。
- `benchmark_ab_compare.py`
  A/B 结果汇总器。
- `analyze_layerwiseft.py`
  LayerwiseFT 专项离线分析。
- `compare_layerwiseft_improved.py`
  改进版 LayerwiseFT 的运行与聚合。

## 主要数据流

主链路按顺序分为五步：

1. 读入 `X/Y` 数据并构造成统一 `dataset`。
2. `stagewise_train` 训练并筛选更便于符号化的模型快照。
3. `symbolize_pipeline` 做渐进剪枝、输入压缩、逐层符号化和微调。
4. `validate_formula_numerically` 验证导出公式与模型输出的一致性。
5. 导出 `metrics.json`、`kan_stage_logs.csv`、`symbolize_trace.csv`、`formula_validation.csv` 等结果。

关键数据结构只有三类：

- `dataset` 字典
- KAN 模型实例
- 结构化结果对象或结果字典

上述数据流与数据结构构成了仓库的基本骨架。

## 公共接口

外部调用与实验脚本宜优先依赖以下入口：

- `symkan.core`
- `symkan.tuning.stagewise_train`
- `symkan.symbolic.symbolize_pipeline`
- `symkan.eval.validate_formula_numerically`
- `symkan.io.*`

兼容原则：

1. 旧返回值尽量保持不变。
2. 新能力优先通过 `*_report` 或新增字段补充。
3. 不为了“更优雅”破坏 notebook 和现有脚本。

## 工作流分层

### 库层工作流

库层关注单次流程的正确性：

- 模型怎么训练
- 剪枝如何回滚
- 符号化如何逐层推进
- 公式如何验证

### 实验层工作流

脚本层关注批量运行与结果管理：

- 多 seed 如何调度
- 结果如何落盘
- 变体如何比较
- 报告表格如何生成

两层分离有助于在实验脚本参数口径发生变化时保持公共库接口稳定。

## 输出约定

当前项目最重要的产物约定如下：

- `symkanbenchmark_runs.csv`
  主实验横向对比表。
- `kan_stage_logs.csv`
  阶段训练日志。
- `symbolize_trace.csv`
  剪枝与符号化轨迹。
- `formula_validation.csv`
  公式数值验证结果。
- `metrics.json`
  单次运行关键指标。

如需接入现有分析链，宜复用上述产物格式。

## 设计约束

当前架构遵守四条约束：

1. 不重写 `pykan` 的核心模型行为。
2. 不破坏已有 notebook / CLI / CSV 工作流。
3. 项目层默认设定优先稳定复现，而不是单次最高分。
4. 实验结论必须能追溯到落盘文件，而不是只存在于终端输出。

## 阅读顺序

进一步阅读时，可按以下顺序：

1. [README.md](README.md)
2. [docs/project_map.md](docs/project_map.md)
3. [docs/design.md](docs/design.md)
4. [docs/symkan_usage.md](docs/symkan_usage.md)
5. [docs/symkanbenchmark_usage.md](docs/symkanbenchmark_usage.md)
