# FastKAN-Style Numeric Frontend Migration Plan

## Goal

在不破坏现有 `symkan -> kan.MultKAN` 工作流的前提下，为本仓库引入一个可选的 `radial_bf` 数值前端，使其具备：

- 可训练
- 可剪枝
- 可符号化
- 可导出公式

当前优先级是“工程可跑通”，不是立即追求论文级最优结果。

## Scope

本计划只覆盖最小侵入迁移路线：

- 保留现有 `symkan` 流水线与 `kan/` 主体 API。
- 在 `kan/` 中增加 FastKAN 风格的数值边前端。
- 保持默认 `bspline` 路径不变。

本计划暂不包含：

- 全量 benchmark 重跑
- 大规模消融分析
- 论文最终图表与结论撰写

## AI Execution Protocol (Added After Stage 1)

为降低后续代理执行偏差，后续 Stage 必须遵守以下执行协议。

### 1. Environment and command rules

- 所有 Python 测试与脚本默认使用 `kan` 环境解释器：
  - `C:\\Users\\chenpeng\\miniconda3\\envs\\kan\\python.exe`
- 避免使用 `conda run -n kan ...` 作为主执行路径（当前终端存在编码异常风险，可能误报失败）。
- 命令执行目录固定为仓库根目录：`symkan-experiments/`。

### 2. Minimal-change policy

- 每个 Stage 仅修改其 `Target files`，不要顺手改不相关模块。
- 默认行为必须保持 `bspline` 不变；新增能力只能走显式开关。
- 不允许把 `symkan` 逻辑回退为脚本私有逻辑。

### 3. Stage completion checklist (mandatory)

每完成一个 Stage，必须同步完成以下事项：

1. 代码实现与该 Stage 的 `Required behavior` / `Focus` 对齐；
2. 执行该 Stage 的最小验证命令并记录结果；
3. 将该 Stage 状态从 `Not Started` 更新为 `Complete`；
4. 若存在 blocker，记录“失败命令 + 错误 + 下一步方案”。

### 4. Stop conditions for agents

出现以下情况时，代理应停止扩展开发并先修正计划或请求确认：

- 发现需要跨 Stage 才能落地（例如 Stage 2 尚未完成却需要 Stage 5 配置才能验证）；
- 需要修改 `symkan` 公共配置语义或默认值；
- 发现 `symbolic` 或 `pruning` 契约与当前计划描述冲突。

## Must-Read Before Implementation

以下文件是执行当前计划前的真正必读项，只保留与 Stage 1 到 Stage 4 直接相关的最小集合。

### 1. Project constraints

- `ARCHITECTURE.md`
  了解 `kan/` 与 `symkan/` 的模块边界，避免把迁移做成跨层重写。
- `docs/design.md`
  这里明确了“不重写 pykan 核心行为”和“保持 notebook / CLI / CSV 工作流兼容”的约束。

### 2. Current pykan implementation that must stay compatible

- `kan/KANLayer.py`
  新数值层必须对齐的接口基线。
- `kan/MultKAN.py`
  迁移的核心文件；必须重点阅读：
  `__init__`、`forward`、`attribute`、`prune_edge`、`prune_input`、
  `suggest_symbolic`、`fix_symbolic`、`auto_symbolic`、`symbolic_formula`。
- `kan/Symbolic_KANLayer.py`
  符号边固定与参数拟合逻辑，决定新数值前端缓存如何接入。

### 3. symkan integration points that depend on the model contract

- `symkan/symbolic/pipeline.py`
  当前完整符号化主链路，决定模型至少要提供哪些能力。
- `symkan/symbolic/search.py`
  直接使用 `suggest_symbolic` / `fix_symbolic` 的地方。
- `symkan/symbolic/compact.py`
  直接依赖 `prune_input()`，是迁移兼容性的关键点。
- `symkan/tuning/stagewise.py`
  直接依赖训练、attribution 和 `prune_edge()` 行为。

### 4. FastKAN / AutoSym reference files

- `In-Context-Symbolic-Regression-KAN-main/symbolic_kan/gated_kan.py`
  `radial_bf` 数值原子与兼容层设计的最直接参考。
- `In-Context-Symbolic-Regression-KAN-main/symbolic_kan/MultKAN.py`
  `numeric_atom_configs` 如何接入 `MultKAN`，以及 AutoSym 风格后处理如何与数值前端解耦。
- `In-Context-Symbolic-Regression-KAN-main/example_simple.py`
  作者对“fastkan 只改变 numeric basis，symbolic regression step 不变”的最短说明。

## Nice-to-Read If Needed

以下文件不是开工前必读，但在遇到对应问题时建议回看：

- `README.md`
  仓库整体运行方式与输出口径。
- `symkan/pruning/attribution.py`
  若迁移过程中 attribution 行为异常，再读这个包装层。
- `symkan/io/checkpoint.py`
  若后续 checkpoint / reload 出问题，再补读。
- `symkan/config/schema.py`
  等进入 Stage 5 再读即可。
- `In-Context-Symbolic-Regression-KAN-main/symbolic_kan/Symbolic_KANLayer.py`
  若需要对照其 `old_fix_symbolic` 细节，再补读。
- `In-Context-Symbolic-Regression-KAN-main/symbolic_kan/utils.py`
  若需要对照其局部拟合函数，再补读。

## Compatibility Contract

新的数值前端必须继续满足 `symkan` 当前依赖的模型契约：

- `attribute()`
- `prune_edge()`
- `prune_input()`
- `suggest_symbolic()`
- `fix_symbolic()`
- `symbolic_formula()`
- `act_fun[l].mask`
- `symbolic_fun[l].mask`
- 训练后可读取的边曲线缓存：`acts`、`spline_preacts`、`spline_postacts`、`spline_postsplines`

说明：

- 即使 `radial_bf` 路径下不再使用真实 spline，这些缓存字段也应继续存在。
- 其中 `spline_postacts` / `spline_postsplines` 在新路径下可解释为 “numeric edge response cache”。

## Stage 0: Baseline Lock

Goal:
锁定当前 `bspline` 路径行为，避免迁移过程中引入无意回归。

Success criteria:

- 当前默认配置下的关键 smoke test 可以在迁移前后保持通过。
- 不修改任何已有默认参数语义。

Tests:

- 记录当前 `python -m pytest` 的通过/失败范围。
- 记录一个最小 notebook/CLI 路径的现状输出。

Status:
Complete

## Stage 1: Introduce a Compatible FastKAN-Style Layer

Goal:
在 `kan/` 下新增一个与 `KANLayer` 接口兼容的 `radial_bf` 数值层。

Target files:

- `kan/FastKANLayer.py` 或等价命名的新文件
- `kan/__init__.py`

Required behavior:

- `forward(x)` 返回 `(y, preacts, postacts, postspline)`
- 支持 `mask`
- 支持 `get_subset(in_id, out_id)`
- 支持 `swap(i1, i2, mode)`
- 提供 `update_grid_from_samples()` 和 `initialize_grid_from_parent()` 的兼容实现
- 保留 `grid` / `k` / `coef` / `scale_*` 等必要兼容字段

Success criteria:

- 新层单独前向不报错。
- 输出张量 shape 与 `KANLayer` 对齐。
- `get_subset()` 后仍可前向。

Tests:

- 新增层级 smoke test
- 手动检查 shape、mask、生效边数量

Status:
Complete

Implementation notes (from practice):

- 实际新增文件为 `kan/FastKANLayer.py`，并在 `kan/__init__.py` 导出。
- 兼容字段建议最小集：`grid / k / coef / scale_base / scale_sp / mask`。
- `postspline` 在该路径下代表 numeric edge response（非真实 spline），但 shape/读取语义与旧路径一致。
- Stage 1 验证命令（推荐）：
  - `C:\\Users\\chenpeng\\miniconda3\\envs\\kan\\python.exe -m pytest tests\\test_fastkan_layer.py`

## Stage 2: Wire the Layer into `kan.MultKAN`

Goal:
让 `kan.MultKAN` 支持在 `bspline` 和 `radial_bf` 两种数值前端之间切换。

Target files:

- `kan/MultKAN.py`

Planned changes:

- 增加 `numeric_atom_configs` 或更简单的 `numeric_basis` 配置入口
- 默认仍构造原始 `KANLayer`
- 当配置为 `radial_bf` 时构造新的兼容层

Execution checklist:

1. 在 `kan.MultKAN.__init__` 引入数值前端选择入口（推荐 `numeric_basis`，候选值 `bspline|radial_bf`）；
2. 保持默认 `bspline` 分支构造 `KANLayer`；
3. `radial_bf` 分支构造 `FastKANLayer`；
4. 确保 `refine` / `prune_input` / `expand_*` 等内部重新构造模型路径不会丢失该配置。

Success criteria:

- 原有构造方式完全不受影响。
- 新配置能成功实例化 `MultKAN` 并完成一次训练前向/反向。

Tests:

- 旧代码路径回归 smoke test
- 新路径最小训练 smoke test

Suggested validation commands:

- `C:\\Users\\chenpeng\\miniconda3\\envs\\kan\\python.exe -m pytest tests\\test_fastkan_layer.py`
- `C:\\Users\\chenpeng\\miniconda3\\envs\\kan\\python.exe -m pytest tests\\test_symbolic_pipeline_regressions.py -k \"symbolic or prune\"`

Status:
Not Started

## Stage 3: Align Symbolic-Fitting Caches

Goal:
确保 `suggest_symbolic()` / `fix_symbolic()` 在 `radial_bf` 路径下读取到正确的一维边曲线。

Target files:

- `kan/MultKAN.py`
- `kan/FastKANLayer.py`
- 如有需要，`kan/Symbolic_KANLayer.py`

Focus:

- `self.acts[l][:, i]`
- `self.spline_preacts[l][:, j, i]`
- `self.spline_postacts[l][:, j, i]`
- `self.spline_postsplines[l][:, j, i]`

Execution checklist:

1. 明确 `radial_bf` 路径下四类缓存的来源与 shape；
2. 保证 `suggest_symbolic()` 读取的是单边一维曲线；
3. 保证 `fix_symbolic()` 后 `forward()` 和 `symbolic_formula()` 可继续执行；
4. 对 cache 语义差异写入必要注释（仅解释约束，不写冗余注释）。

Success criteria:

- `suggest_symbolic()` 在 `radial_bf` 路径下能正常返回候选函数。
- `fix_symbolic()` 后模型仍可前向。
- `symbolic_formula()` 能导出非空结果。

Tests:

- 合成函数小样本测试
- 单边曲线可视化/打印抽查

Status:
Not Started

## Stage 4: Restore Pruning and Input Compaction

Goal:
让新路径在 `symkan` 所需的剪枝与输入压缩流程下保持可用。

Target files:

- `kan/MultKAN.py`
- `symkan/symbolic/compact.py`
- `symkan/pruning/attribution.py`

Focus:

- `attribute()`
- `prune_edge()`
- `prune()`
- `prune_input()`

Execution checklist:

1. 验证 `attribute()` 输出可驱动 `prune_edge()`；
2. 验证 `prune_input(active_inputs=...)` 返回模型在新路径可继续前向；
3. 验证 `symkan.symbolic.compact` 的输入压缩在新路径不触发结构错误。

Success criteria:

- `radial_bf` 路径可完成 edge pruning。
- `prune_input()` 返回的新模型结构正确。
- input compaction 后仍可继续符号化。

Tests:

- 最小 stagewise + prune smoke test
- input compaction smoke test

Status:
Not Started

## Stage 5: Expose Configuration in `symkan`

Goal:
让 notebook / YAML / CLI 能显式选择数值前端。

Target files:

- `symkan/config/schema.py`
- `symkan/config/template.yaml`
- `symkan/config/notebook.py`
- 如有需要，相关脚本入口

Planned config:

- 候选：`model.numeric_basis = bspline | radial_bf`
- 或 `model.numeric_atom_configs`

Execution checklist:

1. schema、template、notebook 三处字段命名必须一致；
2. CLI / YAML / notebook 三入口都能显式切换；
3. 不得改变未显式配置时的默认行为（仍为 `bspline`）。

Success criteria:

- 默认配置仍走 `bspline`
- 显式配置后可走 `radial_bf`
- notebook / CLI / YAML 三条入口口径一致

Tests:

- 配置解析单测或 smoke test
- CLI 最小运行验证

Status:
Not Started

## Stage 6: End-to-End Engineering Smoke Test

Goal:
验证 `symkan` 主链路在 `radial_bf` 路径下工程上可以跑通。

Target flow:

- train
- stagewise prune
- symbolic search
- formula export

Success criteria:

- 不依赖手工 patch 流程即可跑通一次完整实验
- 输出 `metrics`、`trace`、`formula_validation` 等关键产物
- 没有接口级崩溃

Tests:

- 一个最小 synthetic dataset
- 一个小规模 benchmark 配置

Suggested validation commands:

- `C:\\Users\\chenpeng\\miniconda3\\envs\\kan\\python.exe -m scripts.symkanbenchmark --config configs/symkanbenchmark.default.yaml --quiet`

Status:
Not Started

## Stage 7: Compare Against Baseline

Goal:
在“工程可跑通”完成后，再进入 `bspline` 与 `radial_bf` 的初步对照。

Comparison dimensions:

- train/test loss
- final edge count
- symbolic success rate
- valid expression count
- symbolic wall time

Success criteria:

- 至少得到一组可复现的 `bspline vs radial_bf` 对照结果
- 能判断是否值得继续做论文级实验

Tests:

- 统一 seed 的 A/B 对照运行

Execution checklist:

1. 固定同一组 seeds；
2. 只改变 numeric frontend 相关配置；
3. 输出统一写入可比较目录并生成 summary 表。

Status:
Not Started

## Risks

1. `symkan` 对 `pykan` 的缓存命名和对象结构耦合较深，数值前端虽可替换，但缓存语义必须严格保持。
2. `attribute()` 与 pruning 可能依赖现有 spline 路径的数值尺度，迁移后阈值未必可直接复用。
3. `prune_input()` 是现有 `symkan` 流程的关键能力，若新路径在该处行为不一致，整体链路会断。
4. 即便工程上跑通，`radial_bf` 路径的符号提取质量也未必与 `bspline` 相同，需要后续实验确认。

## Immediate Next Action

执行 Stage 2：

- 在 `kan.MultKAN` 中接入 `numeric_basis` 切换（默认 `bspline`）；
- 新增 `radial_bf` 构造分支并保持现有训练/剪枝入口兼容；
- 用 `kan` 环境跑最小回归测试，确认旧路径不回退。
