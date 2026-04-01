# 架构总览

## 目标

该仓库围绕 KAN 的数值训练、符号化、实验复现与结果导出展开。当前工程版的关键变化是：符号化阶段不再被视为一个不可分解的黑盒步骤，而是显式拆成“共享 symbolic-prep 预处理”与“backend-specific symbolic completion”两段，以便在 `baseline` 与 `icbr` 之间复用完全相同的前置状态。

架构上分为两层：

- 能力层：`kan/` 和 `symkan/`
- 实验层：根目录脚本、`scripts/` 与 `outputs/`

运行 `notebooks/kan.ipynb` 时，会在 `notebooks/` 下自动生成 `model/` 目录，用于承接运行期模型产物；该目录不属于仓库整理后的固定功能分层。

## 模块边界

### `kan/`

提供 KAN 相关底层实现与兼容能力。这里更接近模型本体，不承担实验编排职责。当前 ICBR 的核心实现也落在这一层，例如 `kan/icbr.py`，其职责仅限于“给已经训练好的数值 KAN 执行替代性的符号拟合后端”，不改变训练语义。

### `symkan/`

该层作为仓库的公共库层，负责组织配置、训练、符号化、评估和导出接口。

- `symkan.config`
  负责 `AppConfig`、YAML 加载、环境变量占位符展开、Pydantic 校验与 `load_config()`；同时通过 `symkan.config.notebook` 承接 notebook 风格 flat kwargs 到 `AppConfig` 的 canonical 化转换。环境变量只会在 YAML 解析后的标量字符串上展开。
- `symkan.core`
  负责设备管理、数据集构建、训练基础函数、结构化类型；`build_dataset` 统一接受 1D 类别索引或 2D one-hot/概率标签，并在样本数、标签 rank 与类别维度不合法时直接报错。
- `symkan.tuning`
  负责 `stagewise_train`、阶段快照、选模和自适应节奏控制。
- `symkan.symbolic`
  负责函数库、表达式处理、输入压缩和符号化主流水线。当前该层内部显式分为：
  - `prepare_symbolic_bundle(...)`：共享 symbolic-prep 阶段，负责渐进剪枝、输入压缩、pre-symbolic fit 和 `symbolize_trace` 形成。
  - `symbolize_pipeline_from_prepared(...)`：从 prepared bundle 继续执行 backend-specific completion。
  - `symbolize_pipeline(...)`：保持原有公开入口不变，对外仍表现为单函数入口，但内部已经包装上述两段。
- `symkan.pruning`
  负责归因和剪枝辅助逻辑。
- `symkan.eval`
  负责 ROC/AUC 与公式数值验证。
- `symkan.io`
  负责 CSV、JSON、bundle 的导出与读取；其中 bundle 读取基于 `pickle`，仅支持显式信任的本地文件。

### `scripts/` 与工具层

工具脚本保留 CLI 编排职责，但算法运行参数统一通过 `symkan.config.AppConfig` 加载。

- `scripts/symkanbenchmark.py`
  主实验入口，负责多 seed 运行、结果汇总、缓存复用和标准导出。当前有两个明确的缓存边界：
  - `_numeric_cache/`：缓存数值训练后的共享 KAN 状态，key 明确排除 `symbolize` 配置，因此 backend-only 变体可以复用同一数值模型。
  - `_symbolic_prep_cache/`：缓存 shared symbolic-prep 之后的 prepared bundle，key 绑定 numeric cache identity 与剪枝/输入压缩/pre-symbolic fit 相关设置，但不绑定 backend-specific symbolic completion 细节。
- `scripts/benchmark_ab_compare.py`
  A/B 结果汇总器。默认仍生成通用 compare 产物；当比较对精确为 `baseline` vs `baseline_icbr` 时，会额外生成：
  - `baseline_icbr_shared_check.csv`
  - `baseline_icbr_primary_effect.csv`
  - `baseline_icbr_mechanism_summary.csv`
- 其他脚本
  继续负责 ablation、LayerwiseFT 和 rerun 编排，不承担库层接口定义职责。

### 根目录脚本

为保持使用方式稳定，根目录保留同名入口文件（shim）；脚本实现统一放在 `scripts/` 下。

- `symkanbenchmark.py`
  根级兼容入口，实际实现位于 `scripts/symkanbenchmark.py`。
- `ablation_runner.py`
  单因素消融矩阵执行器。
- `benchmark_ab_compare.py`
  A/B 结果汇总器。
- `analyze_layerwiseft.py`
  LayerwiseFT 专项离线分析。
- `compare_layerwiseft_improved.py`
  改进版 LayerwiseFT 的运行与聚合。

## 主要数据流

当前主链路按顺序分为六步：

1. 读入 `X/Y` 数据并构造成统一 `dataset`；标签既可来自 1D 类别索引，也可来自 2D one-hot/概率矩阵。
2. `stagewise_train` 训练并筛选更便于符号化的模型快照。
3. `prepare_symbolic_bundle` 做共享 symbolic-prep：渐进剪枝、输入压缩、pre-symbolic fit，并生成 `symbolize_trace.csv` 所依据的 trace。
4. `symbolize_pipeline_from_prepared` 在 prepared bundle 上执行 backend-specific completion：
   - `baseline`：沿用原有 layered symbolic search 路径。
   - `icbr`：调用 `kan.icbr` 的 ICBR 后端，仅改变符号拟合阶段。
5. `validate_formula_numerically` 验证导出公式与模型输出的一致性。
6. 导出 `metrics.json`、`kan_stage_logs.csv`、`symbolize_trace.csv`、`formula_validation.csv` 等结果。

关键数据结构可概括为五类：

- `symkan.config.AppConfig`
- `dataset` 字典
- 数值 KAN 模型实例
- prepared symbolic bundle
- 结构化结果对象或结果字典

当前 `baseline` 与 `baseline_icbr` 的公平性边界是：数值训练和 shared symbolic-prep 必须对齐，后端差异只能从 backend-specific symbolic completion 开始出现。

## 公共接口

外部调用与实验脚本宜优先依赖以下入口：

- `symkan.config`（含 `AppConfig`、`load_config()`、校验入口）
- `symkan.core`
- `symkan.tuning.stagewise_train`
- `symkan.symbolic.symbolize_pipeline`
- `symkan.symbolic.pipeline.prepare_symbolic_bundle`
- `symkan.symbolic.pipeline.symbolize_pipeline_from_prepared`
- `symkan.eval.validate_formula_numerically`
- `symkan.io.*`

兼容原则：

1. 旧返回值尽量保持不变。
2. 新能力优先通过新增字段、结构化 compare 产物或 `*_report` 补充。
3. 不为了“更优雅”破坏 notebook 和现有脚本。

## 工作流分层

### 库层工作流

库层关注单次流程的正确性：

- 模型怎么训练
- 剪枝如何回滚
- shared symbolic-prep 如何形成
- backend-specific symbolic completion 如何执行
- 公式如何验证

### 实验层工作流

脚本层关注批量运行与结果管理：

- 多 seed 如何调度
- numeric cache 与 symbolic-prep cache 如何复用
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
  shared symbolic-prep 形成的剪枝与压缩轨迹。
- `formula_validation.csv`
  公式数值验证结果。
- `metrics.json`
  单次运行关键指标。
- `outputs/.../comparison/variant_summary.csv`、`pairwise_delta_summary.csv`、`trace_summary.csv`
  通用 compare 产物。
- `outputs/.../comparison/baseline_icbr_shared_check.csv`、`baseline_icbr_primary_effect.csv`、`baseline_icbr_mechanism_summary.csv`
  仅在 `baseline` vs `baseline_icbr` 时生成的专用 compare 产物。

当前时长口径需要区分：

1. `symbolic_core_seconds`
   backend-specific symbolic completion 的核心耗时，适合用作 baseline vs ICBR 的主比较指标。
2. `symbolize_wall_time_s`
   从 prepared bundle 开始到导出前的整体符号化墙钟时间，包含更多后处理开销。
3. `cached_stage_total_seconds_ref` / `cached_symbolic_prep_seconds_ref`
   仅作为共享阶段的参考时长，不应被解释为当前 symbolization-only run 的实时成本。

## 配置与数据分层

运行配置与实验数据需要分开管理：

- YAML 配置：描述程序如何运行，例如 seed、设备、训练节奏、符号后端、输出目录。
- 环境变量：注入敏感信息或机器相关差异，不写入仓库。
- CSV / NPY / JSON：作为输入数据、结果产物和分析中间表。
- `pickle` bundle：仅作为本地可信实验归档格式，不作为跨来源交换格式。

当前实现遵循以下分层：

- notebook / Python 调用层：优先显式构造 `symkan.config.AppConfig`，便于演示和单元测试。
- notebook 兼容层：若保留旧 notebook 的函数式 flat kwargs，则先经 `symkan.config.notebook` 归一化为 canonical `AppConfig` section 名字；`symkan.notebook_compat` 仅负责薄桥接，不再承载配置转换逻辑。
- 脚本入口层：支持 `--config <yaml>`，先 `load_config()` 得到 `AppConfig`，再对一小组白名单字段做显式覆盖。
- 实验编排层：脚本先 `load_config()` 得到 `AppConfig`，再做白名单覆盖与批量调度。
- 底层能力层：统一依赖 `symkan.config.AppConfig`，其中嵌套 `StagewiseConfig` / `SymbolizeConfig`；数据层继续使用 `DatasetBundle`。

这样做的目的是让核心逻辑不关心参数来源，同时避免 YAML 路径和 CLI 路径出现两套不同校验或默认值逻辑。

## 设计约束

当前架构遵守五条约束：

1. 不重写 `pykan` 的核心训练行为。
2. ICBR 只允许改变符号拟合后端，不得污染数值训练与 shared symbolic-prep 语义。
3. 不破坏已有 notebook / CLI / CSV 工作流。
4. 项目层默认设定优先稳定复现，而不是单次最高分。
5. 实验结论必须能追溯到落盘文件，而不是只存在于终端输出。

## 阅读顺序

进一步阅读时，可按以下顺序：

1. [README.md](README.md)
2. [SPEC.md](SPEC.md)
3. [docs/project_map.md](docs/project_map.md)
4. [docs/design.md](docs/design.md)
5. [docs/symkan_usage.md](docs/symkan_usage.md)
6. [docs/symkanbenchmark_usage.md](docs/symkanbenchmark_usage.md)
7. [docs/engineering_rerun_report.md](docs/engineering_rerun_report.md)
