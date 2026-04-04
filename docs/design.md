# SymKAN Design

状态: Rewritten as a paper-style design manuscript
日期: 2026-04-04
范围: 以当前 `symkan-experiments` 仓库为对象，说明 SymKAN 如何在不改写 `pykan` 数值训练语义的前提下，把 KAN 的训练、剪枝、符号化、验证与结果归档组织成可复现、可比较、可引用的工程化研究流程。

## 1. 摘要

本文将 SymKAN 重新表述为一个面向符号化实验的工程化流水线，而不是对 `pykan` 的替代实现，也不是单一算法模块的说明书。其核心目标不是重新发明 KAN 训练器，而是在保持既有 notebook、CLI 与脚本入口兼容的前提下，把数值训练后的 KAN 模型推进到可验证、可导出、可比较的符号表达式状态，并把相关证据落实到结构化文件而非终端输出。

当前版本的设计主张固定为以下五点：

1. `AppConfig` 作为 notebook、CLI 与库层共享的配置边界，负责把“程序如何运行”的描述统一到同一对象上。
2. `stagewise_train` 与 `symbolize_pipeline` 必须分离；前者负责把模型送入可符号化区间，后者负责在受控复杂度下完成符号替换与验证。
3. 符号化流程内部需要区分 shared symbolic-prep 与 backend-specific symbolic completion，以保证 `baseline` 与 `icbr` 的 backend-only compare 具有清晰的公平性边界。
4. 结果归档必须依赖结构化输出，包括运行主表、阶段日志、轨迹表、公式验证表和 compare 汇总，而不是散落的临时记录。
5. 设计层结论必须以维护中的证据目录为依据，并显式区分 paired evidence、supplementary evidence 与不可混写的历史切片。

相应地，本文明确不作以下主张：

- 不把 SymKAN 描述为新的 KAN 数值训练算法。
- 不把 SymKAN 描述为从原始样本直接发现闭式公式的通用 symbolic regression 系统。
- 不把工程版 `n=3` seeds 结果表述为充分的统计显著性结论。
- 不把 `formula_export_success_rate=1.0` 表述为“真实公式恢复成功率”。
- 不把 `baseline_icbr_fulllib` 的单边结果表述为 paired backend-only compare 证据。

为防止后文在不同证据来源之间混写，本文在摘要阶段固定如下证据矩阵。

| 论断类型 | 允许引用的来源 | 不应混入的来源 |
| --- | --- | --- |
| 当前工程版总体 rerun 的主流程表现、工程策略速度/质量权衡与默认主引用归档 | [docs/engineering_rerun_report_20260318.md](engineering_rerun_report_20260318.md), `outputs/rerun_v2_engine_safe_20260318_rerun/` | `2026-04-01` ICBR backend compare 的 paired fairness 结论 |
| 模块角色、默认设定、Stagewise/剪枝/压缩/LayerwiseFT 的职责判断 | [docs/ablation_report.md](ablation_report.md), [docs/layerwiseft_improved_report.md](layerwiseft_improved_report.md), `outputs/benchmark_ablation/` | `benchmark_ab` 的 backend compare 结果 |
| `baseline` vs `baseline_icbr` 的 backend-only compare | [docs/engineering_rerun_report_20260401.md](engineering_rerun_report_20260401.md), `outputs/rerun_v2_engine_safe_20260401/benchmark_ab/comparison/` | 历史 `radial_bf` 工程切片、单边 full library 切片 |
| `baseline_fastlib` vs `baseline_icbr_fastlib` 的更大函数库 paired compare | [docs/engineering_rerun_report_20260401.md](engineering_rerun_report_20260401.md), `outputs/rerun_v2_engine_safe_20260401/benchmark_ab/comparison_fastlib/` | layered paired compare 之外的旧 compare 目录 |
| full library 下 ICBR 的可运行性补充说明 | [docs/engineering_rerun_report_20260401.md](engineering_rerun_report_20260401.md), `outputs/rerun_v2_engine_safe_20260401/benchmark_ab/baseline_icbr_fulllib/` | 任何 paired backend-only 语义表述 |

需要额外强调的是，当前仓库中的几条工程实验线路并不是同一问题的重复测量，而是面向不同设计问题的分层证据：

1. `2026-03-18` 总体 rerun 关注“当前工程版整体能否稳定跑通，以及默认主流程、`baseline/adaptive/adaptive_auto` 工程策略、Full Pipeline 默认设定应如何落档引用”。
2. `benchmark_ablation` 关注“模块职责与默认设定为何成立”，因此更适合回答 Stagewise、剪枝、输入压缩和 LayerwiseFT 的角色问题。
3. `2026-03-27` `radial_bf` 专题关注历史工程权衡，而不是当前正式 compare 口径。
4. `2026-04-01` ICBR 系列报告关注 shared symbolic-prep 边界成立后的 backend-only compare，以及更大函数库下的速度边界。

因此，本文不把这些线路压扁成一个“统一大表”，而是要求每条线路只回答它真正被设计来回答的问题。

本文余下结构安排如下。第 2-4 节说明设计前提、实现约束与当前 baseline 流水线的真实语义；第 5-8 节给出 SymKAN 的方法重定义、形式化对象与关键设计；第 9-10 节说明接口落点、实验问题与证据边界；第 11 节汇总当前可引用结果；第 12-13 节收束风险、适用边界与结论。

## 2. 设计前提

### 2.1 控制变量原则

SymKAN 的核心对象不是“任意神经网络”，而是已经训练完成并可继续进入符号阶段的数值 KAN。设计时必须坚持以下控制变量原则：

1. 不改写 `pykan` 的基础训练语义。
2. 不把数值训练、剪枝、符号替换、公式验证混成一个不可分解的黑箱步骤。
3. 对同一组实验，只允许在被显式声明的阶段引入差异；其余阶段必须共享。

这一原则在当前仓库中有两个直接后果：

1. 模块级默认设定要由单点消融结果约束，而不是由局部直觉决定。
2. backend compare 必须把差异严格限制在 backend-specific symbolic completion，而不能回溯污染 numeric stage 或 shared symbolic-prep。

### 2.2 当前仓库中的真实任务

在当前实现中，SymKAN 面对的真实任务不是“从原始数据直接搜索完整公式树”，而是：

1. 训练一个数值 KAN；
2. 通过 `stagewise_train` 与相关治理机制把模型推进到可符号化区间；
3. 在可控复杂度下执行符号替换；
4. 对导出公式做数值验证；
5. 将运行过程与结果整理为结构化产物。

因此，SymKAN 更准确的定位是：

**一个围绕训练后 KAN 的符号化实验与比较框架。**

### 2.3 第一版允许改什么，不改什么

允许改动的对象包括：

- 配置边界与参数归一化方式；
- 流水线阶段划分；
- 缓存边界与 compare 语义；
- 结构化导出与报告层组织；
- 符号后端的实现与比较方式。

不改动的对象包括：

- `pykan` 的基础数值训练器；
- notebook / CLI / CSV 的既有使用习惯；
- 根目录 shim 入口的兼容职责；
- “YAML 负责描述运行方式、CSV 负责承载输入与结果”的分层约束。

## 3. KAN 与当前实现给出的直接约束

### 3.1 KAN 的符号化不是从零开始的公式搜索

当前 SymKAN 处理的是“训练后 KAN 的符号替换问题”，而不是从原始输入输出对直接进行全局 symbolic regression。KAN 的多变量结构仍由层级组合给出，符号化阶段处理的对象主要是一元边函数及其组合关系。

这一点决定了三个事实：

1. 符号阶段必须尊重已经形成的数值结构；
2. 复杂度治理必须发生在符号搜索之前，而不是之后；
3. 公式导出结果应被视为训练后模型的符号近似，而不是对真实生成机制的自动恢复证明。

### 3.2 `symbolic_formula()` 与 fully symbolic 收口约束

当前导出语义要求有效边在导出前处于符号状态。由此可知，符号阶段不仅要找到候选函数，还要保证导出状态、掩码、仿射参数与相关结构保持一致。这意味着：

1. 符号化不是单纯的局部打分问题，而是状态一致性问题；
2. 任何“部分替换、部分残留”的策略都需要谨慎，否则导出语义会失真；
3. 显式的阶段边界与结构化轨迹记录是必要条件，而不是装饰性工程。

### 3.3 符号化入口的复杂度必须受控

当前单点消融已经表明，若不对数值模型做阶段训练、剪枝与输入治理，符号化入口将迅速失控。其直接原因在于：

1. 候选空间对有效边数和有效输入维度高度敏感；
2. 数值模型若过密，符号搜索的计算负担和误差传播风险都会扩大；
3. 复杂度治理不足时，单次训练指标即使可接受，也不意味着导出公式具备可解释性和可验证性。

### 3.4 兼容性不是附属要求，而是设计约束

SymKAN 不是全新仓库，而是对 `pykan` 使用方式的工程化组织。由此必须保留：

1. notebook 入口；
2. CLI 入口；
3. 根目录 shim；
4. CSV 与报告工作流；
5. 既有 `python -m scripts.*` 的运行习惯。

因此，任何设计改动都必须回答一个问题：它是否在提升可复现性的同时维持了既有工作流的连续性。

## 4. 当前 baseline 流水线的真实语义

### 4.1 当前主链路

以当前仓库实现为准，SymKAN 主链路可概括为六步：

1. 读取数据并构造统一的数据集对象；
2. `stagewise_train` 训练并筛选更适合符号化的模型状态；
3. 共享 symbolic-prep 处理，包括渐进剪枝、输入压缩与 pre-symbolic fit；
4. backend-specific symbolic completion；
5. 公式数值验证；
6. 导出结构化日志、表格与 compare 产物。

### 4.2 baseline 的角色

在当前仓库中，`baseline` 不是“旧版实现的残留别名”，而是默认符号后端。其含义是：

1. 若未显式指定 `symbolic_backend`，系统使用 `baseline`；
2. paired backend compare 的基线语义由 `baseline` 提供；
3. 所有 opt-in backend 都必须在不破坏 `baseline` 默认行为的前提下接入。

### 4.3 模块角色的经验边界

来自 [docs/ablation_report.md](ablation_report.md) 与 [docs/layerwiseft_improved_report.md](layerwiseft_improved_report.md) 的当前结论表明：

1. `stagewise_train` 是“可用/不可用”的分界，而不是装饰性增强模块。
2. progressive pruning 的主要职责是复杂度控制，而不是默认的精度提升器。
3. input compaction 是速度与公式数值一致性之间的明确权衡开关。
4. 在典型 2 层 KAN 下，LayerwiseFT 不构成稳定的默认净收益。

因此，当前 baseline 流水线应被理解为一套经过模块角色约束后的默认工程方案，而不是随意堆叠的启发式集合。

## 5. SymKAN 的重新定义

### 5.1 方法定义

本文将 SymKAN 重新定义为：

**一个面向训练后 KAN 的工程化符号实验流水线，其任务是在兼容既有工作流的前提下，为符号化过程提供统一配置边界、可控的复杂度治理、可解释的 backend compare 语义和结构化结果归档。**

### 5.2 核心组成

在这一重新定义下，SymKAN 的核心不再是单个函数，而是四类协同对象：

1. 配置对象：`AppConfig`
2. 训练后模型对象：数值 KAN 与 prepared symbolic bundle
3. 过程对象：stagewise、shared symbolic-prep、backend completion、validation
4. 结果对象：CSV / JSON / markdown compare artifacts

### 5.3 第一版只保留的核心设计点

当前版本的核心设计点可压缩为以下六条：

1. 用 `AppConfig` 统一 notebook、CLI 与库层配置来源。
2. 将 `stagewise_train` 从符号阶段显式分离。
3. 把 shared symbolic-prep 作为 backend-only compare 的公平性边界。
4. 把 backend-specific symbolic completion 视作 compare 的真实差异来源。
5. 用结构化输出而非终端日志承载结果。
6. 用 evidence-boundary 文档约束结果叙述，而不是让结论漂浮在目录之外。

### 5.4 第一版明确不包含的内容

为保持问题边界清晰，当前版本明确不把以下内容写成 SymKAN 的核心贡献：

- 新的 KAN 数值训练算法；
- 分布式或大规模任务调度框架；
- 全局公式树搜索系统；
- 脱离仓库实现的纯理论性能保证；
- 任何超出当前维护结果目录的“默认显著提升”表述。

## 6. 问题形式化

### 6.1 对象定义

记数据对象为

$$
\mathcal{D}=(X_{\text{train}}, Y_{\text{train}}, X_{\text{test}}, Y_{\text{test}}),
$$

配置对象为

$$
c \in \mathcal{C},
$$

其中 `c` 由 `AppConfig` 表示。记数值训练与阶段筛选后的模型为

$$
M_{\text{num}} = T(\mathcal{D}, c_{\text{stagewise}}),
$$

shared symbolic-prep 之后的 prepared state 为

$$
B = P(M_{\text{num}}, c_{\text{shared}}),
$$

backend-specific symbolic completion 之后的符号模型为

$$
M_{\text{sym}} = S(B, c_{\text{backend}}),
$$

结构化结果集合为

$$
R = E(M_{\text{sym}}, \mathcal{D}, c_{\text{eval}}).
$$

### 6.2 流水线目标

SymKAN 当前追求的不是单一标量最优，而是受约束的多目标平衡：

1. 保持任务指标可接受；
2. 控制表达式复杂度与符号阶段时间；
3. 保持导出与验证链路稳定；
4. 保证结果可复现、可比较、可归档；
5. 不破坏现有 notebook / CLI / CSV 工作流。

因此，当前设计更接近如下约束优化问题：

$$
\max \; \text{quality}(R)
\quad
\text{s.t.}
\quad
\text{complexity}(R), \text{runtime}(R), \text{compatibility}(c), \text{traceability}(R)
$$

其中 `quality` 不是单一精度指标，而是由 `final_acc`、`macro_auc`、`validation_mean_r2`、target-side 指标等共同描述。

### 6.3 readiness score 与可符号化状态

`stagewise_train` 的职责不是直接给出最终公式，而是把模型推进到可符号化区间。当前仓库中用于阶段选择的思路可抽象为精度与稀疏度的折中，即：

$$
\text{score}
=
w_{\text{acc}} \cdot \text{acc}

+ (1-w_{\text{acc}}) \cdot \text{sparsity}.
$$

这一定义的作用不是宣称理论最优，而是说明：当前阶段选择必须同时考虑任务可用性与符号阶段负担，不能只看单次精度。

### 6.4 backend-only compare 的公平性约束

当比较 `baseline` 与 `baseline_icbr` 时，当前设计要求：

$$
M_{\text{num}}^{\text{baseline}} = M_{\text{num}}^{\text{icbr}},
$$

$$
B^{\text{baseline}} = B^{\text{icbr}},
$$

并要求 compare 结果满足：

1. `shared_numeric_aligned=True`
2. `trace_aligned=True`
3. `shared_symbolic_prep_aligned=True`

只有在这些条件成立时，当前 paired compare 才可被解释为“backend-only compare”。

## 7. 关键设计

### 7.1 `AppConfig` 作为统一配置边界

配置统一的主要价值不在于“更优雅”，而在于减少 notebook、CLI 与脚本实现之间的漂移。当前仓库选择让 `AppConfig` 成为唯一正式配置对象，并把旧 notebook 风格参数归一化到该对象之下。这一设计的直接收益是：

1. 校验逻辑不再在多处分裂；
2. YAML 与 CLI 的覆盖关系更易追踪；
3. 后续比较与缓存键定义可以围绕同一配置对象进行。

### 7.2 `stagewise_train` 的独立地位

单点消融表明，去掉 `stagewise_train` 后，`final_acc` 从 `0.7807` 降到 `0.4430`，`macro_auc` 从 `0.9548` 降到 `0.8379`；虽然时间下降，但输出失去可用性。由此可见，`stagewise_train` 在当前体系中的角色不是“让结果再好一点”，而是建立可符号化入口。

### 7.3 progressive pruning 与 input compaction 的治理角色

当前证据显示：

1. 去掉 progressive pruning 后，`final_acc` 略升到 `0.8017`，但表达式复杂度从 `126.90` 增至 `194.33`，`symbolic_total_seconds` 从 `33.58s` 增至 `43.51s`。
2. 去掉 input compaction 后，`validation_mean_r2` 从 `-0.6135` 升至 `+0.0275`，但有效输入维数翻倍到 `120`，`symbolic_total_seconds` 增至 `41.34s`。

因此，这两个模块的主要职责应分别表述为：

- pruning：复杂度治理；
- compaction：时间与数值一致性之间的显式权衡。

### 7.4 shared symbolic-prep 作为 compare 公平性边界

当前架构最重要的工程性收敛之一，是把符号流程显式拆为：

1. shared symbolic-prep；
2. backend-specific symbolic completion。

这一拆分的意义有三层：

1. 它把比较边界从“整条符号链”收紧到“后端差异真正发生的位置”；
2. 它使 `_numeric_cache/` 与 `_symbolic_prep_cache/` 的职责更明确；
3. 它使 `baseline` 与 `icbr` 的公平性不再依赖口头解释，而能通过 shared-check 文件验证。

### 7.5 generic compare 与 specialized compare 的分层

当前 `benchmark_ab_compare` 的设计并不追求“一种表覆盖所有语义”。相反，它坚持两层输出：

1. generic compare：适用于一般 A/B 工作流；
2. specialized compare：仅在单个 baseline-backend vs icbr-backend pair 时生成。

这一分层的价值在于：既保留通用工作流的稳定性，又避免把 backend-only compare 的特殊语义污染到所有 compare 结果中。

### 7.6 结构化导出与指标卫生

SymKAN 当前强调以下结果对象：

- `symkanbenchmark_runs.csv`
- `kan_stage_logs.csv`
- `symbolize_trace.csv`
- `formula_validation.csv`
- `metrics.json`
- compare 目录下的 summary 表与 markdown

这意味着“实验结论”必须能够回指到具体文件。对应的指标卫生约束包括：

1. backend 速度比较优先使用 `symbolic_core_seconds`；
2. `symbolize_wall_time_s` 仍可报告，但不应替代核心后端指标；
3. `formula_export_success_rate` 只表示导出链路成功，不等于真实公式恢复成功。

### 7.7 LayerwiseFT 在 2 层 KAN 中的默认决策

来自 [docs/layerwiseft_improved_report.md](layerwiseft_improved_report.md) 的当前结论是：在 2 层 KAN 下，改进版 LayerwiseFT 相对 `wolayerwiseft` 没有形成稳定净收益，却引入约 `63%` 的符号阶段时间增量。因此，更准确的默认表述应为：

**LayerwiseFT 是可选微调开关，而不是当前 2 层 KAN 的默认收益模块。**

## 8. 流水线伪代码

```text
Input:
  dataset D
  config c = AppConfig(...)

1. normalize config sources
   c <- load_config(yaml, cli_overrides, notebook_kwargs)

2. numeric preparation
   M_num <- stagewise_train(D, c.stagewise, c.training)

3. shared symbolic preparation
   B <- prepare_symbolic_bundle(M_num, D, c.symbolize_shared)

4. backend-specific completion
   if c.symbolize.symbolic_backend == baseline:
       M_sym <- baseline_completion(B, c.symbolize)
   else if c.symbolize.symbolic_backend == icbr:
       M_sym <- icbr_completion(B, c.symbolize)

5. validation and export
   R_single <- validate_formula_numerically(M_sym, D, c.eval)
   export metrics, traces, validation tables, structured artifacts

6. benchmark compare (optional)
   if benchmark_ab workflow is enabled:
       emit generic compare outputs
       if exactly one baseline-backend vs one icbr-backend pair:
           emit specialized shared-check and mechanism outputs

Output:
  symbolic model, validation tables, benchmark summaries, compare artifacts
```

该伪代码的重点不在于列出所有函数，而在于明确：当前仓库把配置统一、可符号化准备、后端差异、结果验证和报告导出视为相互独立但可衔接的阶段。

## 9. 接口、工作流与文档分层

### 9.1 与 `pykan` 的关系

SymKAN 不取代 `pykan`，而是围绕其训练后模型组织实验流程。换言之，`pykan` 提供模型本体与基本能力，SymKAN 提供工程化实验边界、比较语义与结果组织。

### 9.2 与脚本层的关系

脚本层承担批量实验与结果管理职责，而不是重新定义库层语义。当前仓库中：

- `scripts/symkanbenchmark.py` 负责多 seed 运行、缓存复用与结果汇总；
- `scripts/benchmark_ab_compare.py` 负责 compare 汇总；
- 根目录 shim 负责兼容入口，而不是实现主体。

### 9.3 与文档体系的关系

当前文档分层应理解为：

1. [README.md](../README.md)：总入口与阅读路径；
2. [../ARCHITECTURE.md](../ARCHITECTURE.md)：模块边界与数据流；
3. 本文：设计动机、阶段划分、证据边界与结果口径；
4. [symkanbenchmark_usage.md](symkanbenchmark_usage.md) 与 [full_experiment_runbook.md](full_experiment_runbook.md)：运行契约与操作步骤；
5. [engineering_rerun_report.md](engineering_rerun_report.md)：日期化实验报告入口。

因此，本文不承担命令级教程职责，也不重复 runbook 内容。

在日期化报告内部，还应继续区分三类用途不同的正文：

1. 总体 rerun 报告，例如 [engineering_rerun_report_20260318.md](engineering_rerun_report_20260318.md)，用于说明当前工程版总体复测和主引用归档。
2. 历史专题报告，例如 [engineering_rerun_report_20260327.md](engineering_rerun_report_20260327.md)，用于保存某条旧实验线路的工程权衡。
3. 当前正式 compare 报告，例如 [engineering_rerun_report_20260401.md](engineering_rerun_report_20260401.md)，用于承载 shared-state 已校验的 paired backend compare。

## 10. 实验设计

### 10.1 研究问题与证据组织

本节关注的不是“仓库中有哪些实验目录”，而是当前维护结果究竟回答了哪些设计问题。围绕 SymKAN 的默认流水线与当前工程版 compare 语义，实验部分需要回答以下五个问题：

1. 当前工程版是否已经形成可稳定引用的总体 rerun 基线。
2. 默认流水线中的 Stagewise Train、Progressive Pruning、Input Compaction 与 LayerwiseFT 分别承担什么职责，默认设定为何成立。
3. 在当前 2 层 KAN 中，LayerwiseFT 改进版是否足以改变“默认关闭”的项目层决策。
4. 在 shared numeric 与 shared symbolic-prep 对齐的前提下，`baseline` 与 `baseline_icbr` 的差异能否被解释为 backend-only compare；若函数库扩大到 `FAST_LIB`，该结论如何变化。
5. 历史专题线路应如何归档，以及它们为何不能与当前正式结论混写。

上述问题并非由单一实验同时回答。当前仓库中的维护结果由若干条并列但不可互相替代的实验线路构成：总体 rerun 线路负责建立当前工程版基线；模块消融与 LayerwiseFT 专题负责约束默认设定；backend compare 线路负责回答 shared-state 对齐后的后端差异；历史专题线路仅保留为旧工程权衡记录。设计文档的实验叙事必须尊重这种分工，否则“当前默认流水线为何如此设置”与“ICBR backend 是否带来 paired 收益”会被错误地写成同一类证据。

### 10.2 共同实验条件与指标口径

尽管各线路的研究问题不同，当前维护中的正式结果共享一组基础实验背景，用于保证跨线路阅读时的口径一致性：

1. 运行环境：Windows 11 专业版 `23H2`，`C:\Users\chenpeng\miniconda3\envs\kan\python.exe`，`PyTorch 2.1.2+cpu`。
2. 数据与切分：固定使用仓库内预制的 MNIST `train/test` 切分，即 `data/X_train.npy`、`data/X_test.npy`、`data/Y_train_cat.npy`、`data/Y_test_cat.npy`，不在 rerun 中重新随机划分训练集与测试集。
3. 种子与骨架：stagewise seeds 为 `42,52,62`，`global_seed = 123`，`baseline_seed = 123`，`layerwise_validation_seed = 123`；共同模型骨架为 `inner_dim = 16`、`grid = 5`、`k = 3`、`top_k = 120`。
4. 共同工程口径：`guard_mode = light`，`validate_n_sample = 500`；默认函数库口径为 layered。

本文使用的指标分为四组：

| 指标组 | 代表指标 | 作用 |
| --- | --- | --- |
| 任务指标 | `final_acc`、`macro_auc` | 描述分类性能 |
| 结构指标 | `final_n_edge`、`effective_input_dim`、表达式复杂度 | 描述符号化后结构规模 |
| 时间指标 | `symbolic_core_seconds`、`symbolize_wall_time_s`、`run_total_wall_time_s` | 区分核心符号阶段耗时与整体墙钟耗时 |
| 验证与机制指标 | `validation_mean_r2`、target-side 指标、shared-check 指标、mechanism breakdown 指标 | 用于公式一致性、fairness 校验与机制解释 |

其中，backend compare 的主速度指标固定为 `symbolic_core_seconds`；`symbolize_wall_time_s` 与 `run_total_wall_time_s` 仍然重要，但其语义更接近整体流程成本，不宜替代 backend-only compare 的主效应描述。

### 10.3 当前维护实验线路总览

| 实验线路 | 研究问题 | 共享配置 | 允许变化 | 主要输出目录 | 支持的结论层级 |
| --- | --- | --- | --- | --- | --- |
| 当前工程版总体 rerun | 当前工程版主流程是否已形成稳定基线；工程策略如何权衡 | 数据、种子、模型骨架、默认 workflow、`guard_mode=light` | 任务入口、A/B 工程策略、归档输出目录 | `outputs/rerun_v2_engine_safe_20260318_rerun/` | 当前工程版总体基线、工程策略折中、主引用归档 |
| 模块消融线路 | 默认流水线中的各模块为何保留或关闭 | 共享基础 `AppConfig`、共享数据、共享 seeds、共享模型骨架 | 单个模块开关：Stagewise、Pruning、Compaction、LayerwiseFT | `outputs/benchmark_ablation/` | 模块职责、默认设定依据 |
| LayerwiseFT 改进专题 | 改进版 LayerwiseFT 是否形成净收益 | 与消融线路共享数据、种子与骨架 | 仅比较 `full`、`layerwiseft_esreg` 与 `wolayerwiseft` | `outputs/benchmark_ablation/layerwiseft_improved_analysis/` | LayerwiseFT 是否应进入默认路径 |
| backend compare：layered paired | 在最保守 shared-state 对齐下，ICBR backend 是否产生 paired 收益 | numeric stage、shared symbolic-prep、trace rhythm、共同 symbolize 主参数 | `symbolize.symbolic_backend` 从 `baseline` 切至 `icbr` | `outputs/rerun_v2_engine_safe_20260401/benchmark_ab/{baseline,baseline_icbr,comparison}/` | 当前最保守的 backend-only paired 证据 |
| backend compare：FAST_LIB paired | 函数库扩展后，ICBR 的 paired 速度边界与质量变化如何 | 与 layered paired 共享 numeric stage 与 shared symbolic-prep | 保持非 `symbolize` 配置不变，仅扩大 `symbolize.lib` 并切换 backend | `outputs/rerun_v2_engine_safe_20260401/benchmark_ab/{baseline_fastlib,baseline_icbr_fastlib,comparison_fastlib}/` | 更大候选库下的 paired 速度边界 |
| backend compare：full library 单边补充 | 当 paired full-library compare 缺失时，ICBR-only 切片能说明什么 | 共享同一工程框架 | 仅运行 `baseline_icbr_fulllib` | `outputs/rerun_v2_engine_safe_20260401/benchmark_ab/baseline_icbr_fulllib/` | full library 可运行性与单边收益补充，不提供 fairness |
| 历史专题线路 | 早期工程权衡如何归档 | 同期共享数据、种子与骨架 | 可同时调整 numeric basis 与多项工程参数 | `outputs/rerun_v2_engine_safe_20260327/benchmark_ab/` | 历史工程权衡，不进入当前正式主结论 |

这个线路划分有两个直接后果。其一，`2026-03-18` 总体 rerun 不能被写成 backend-only compare；其二，`baseline_icbr_fulllib` 也不能被写成 paired fairness 证据。设计文档中的“综合结论”必须来自这些线路的并置与收束，而不是把它们改写成一张统一大表。

### 10.4 当前工程版总体 rerun 线路

`2026-03-18` 总体 rerun 的正式归档根为 `outputs/rerun_v2_engine_safe_20260318_rerun/`。这一线路由 `scripts/run_engineering_rerun.ps1` 编排，内部依次执行 `benchmark_runs/`、`benchmark_ab/` 与 `benchmark_ablation/` 三组任务。它的研究重点不是隔离某一个局部模块，而是回答：当前工程版作为一个完整 workflow，是否已经形成稳定、可复跑、可引用的主流程基线。

因此，这条线路承担三类职责：

1. 通过 `benchmark_runs/` 给出当前工程版主流程的总体量级。
2. 通过 `benchmark_ab/comparison/` 比较 `baseline`、`adaptive` 与 `adaptive_auto` 三种工程策略的速度与质量权衡。
3. 通过同轮 rerun 中的 `benchmark_ablation/` 摘要，为“默认流水线是工程折中而非单点最优”提供辅助背景。

但这条线路并不回答 ICBR backend 的公平性问题。`2026-03-18` 的 compare 仍然属于工程策略对照，而非 shared-state 对齐后的 backend-only compare。其写作作用是建立当前工程版主引用归档，而不是替代 `2026-04-01` 的 backend compare 正文。

### 10.5 模块消融线路：默认设定的专题依据

`docs/ablation_report.md` 对应的专题输出位于 `outputs/benchmark_ablation/`。这条线路的研究对象不是“当前工程版整体表现”，而是“当某个模块被单独关闭时，流水线的哪一部分语义发生变化”。因此，它采用单点消融设计：除被关闭模块外，其余超参与基线保持一致，仅在 Stagewise Train、Progressive Pruning、Input Compaction 与 LayerwiseFT 四个模块上做单因素切片。

这条线路之所以构成默认设定的主要依据，是因为它直接回答了模块职责，而不是仅给出一个 rerun 末端的总体结果。具体而言：

1. `w/o Stagewise Train` 测试 Stagewise 是否属于“可选调参项”。
2. `w/o Progressive Pruning` 测试剪枝的主要作用是提高分类指标，还是控制复杂度与符号成本。
3. `w/o Input Compaction` 测试输入压缩在符号速度与公式一致性之间的权衡性质。
4. `w/o LayerwiseFT` 测试 LayerwiseFT 是否在当前 2 层 KAN 中构成默认收益模块。

因此，在设计文档中，模块消融线路不应被缩写成“证据边界说明”。它应被明确写成：当前默认流水线的结构分工与默认设定，主要由这条专题线路约束。

### 10.6 LayerwiseFT 改进专题：默认决策的补充检验

`docs/layerwiseft_improved_report.md` 对应的专题输出位于 `outputs/benchmark_ablation/layerwiseft_improved_analysis/`。这条线路的目的不是重复四模块消融，而是对 LayerwiseFT 进行二次检验：在引入“验证早停 + 轻正则 + 60 步短微调”的改进版设置后，LayerwiseFT 是否足以从“高成本可选项”转变为“默认收益模块”。

这一专题在设计上有两个关键边界：

1. 它比较的是 `full`、`layerwiseft_esreg` 与 `wolayerwiseft` 三者之间的差异，因此其结论只约束 LayerwiseFT 的默认地位。
2. 它不承担总体 rerun 基线归档职责，也不承担 backend compare 语义，因此不能被并入 `2026-03-18` 总体 rerun 或 `2026-04-01` backend compare 的主叙述。

换言之，LayerwiseFT 专题的研究问题更窄，但正因为其问题收束得更窄，它才适合作为“项目层默认关闭 LayerwiseFT”的直接证据来源。

### 10.7 backend compare 线路：paired 证据、扩库边界与单边补充

`2026-04-01` 的 backend compare 对应 `outputs/rerun_v2_engine_safe_20260401/benchmark_ab/`。与前两条线路不同，这里的核心任务不是描述“工程版整体是否稳定”，也不是说明“模块各自做什么”，而是回答一个更严格的归因问题：当 numeric stage 与 shared symbolic-prep 保持一致时，`baseline` 与 `baseline_icbr` 的差异能否被解释为 backend-specific symbolic completion 引起。

围绕这一问题，当前维护结果进一步分成三条子线路：

1. layered paired 切片
   `baseline.yaml` 与 `baseline_icbr.yaml` 在 numeric stage 与 shared symbolic-prep 上保持一致，仅从 backend-specific symbolic completion 开始分化。这是当前最保守的 backend-only paired 证据。

2. FAST_LIB paired 切片
   `baseline_fastlib.yaml` 与 `baseline_icbr_fastlib.yaml` 保持非 `symbolize` 配置不变，仅扩大 `symbolize.lib` 并切换 backend。它回答的是“当候选库扩大时，paired 速度边界如何变化”，而不是替代 layered paired 的公平性主叙述。

3. full library 单边补充切片
   `baseline_icbr_fulllib.yaml` 只保留了 ICBR 单边运行结果，因为 `baseline_fulllib` 本轮未继续跑。它能够回答“ICBR 是否让 full library 路径在工程上仍可运行”，但不能回答 paired fairness。

backend compare 线路由此形成清晰的证据分层：layered paired 是当前 fairness 主证据，FAST_LIB paired 是扩库下的速度边界，full library 单边切片只是补充运行性与单边收益。三者不能混写成“ICBR 在所有函数库下都已被 paired 证明”。

### 10.8 历史专题线路的角色

`2026-03-27` 的 `baseline (bspline)` 与 `radial_bf` 对照保留在 `outputs/rerun_v2_engine_safe_20260327/benchmark_ab/`。这条线路的意义是保存历史工程权衡，而不是承担当前正式口径。根据 `docs/engineering_rerun_report_20260327.md`，`radial_bf.yaml` 并非只修改 numeric basis，而是同时调整了训练与符号化阶段的多项工程参数。因此，它不能被视为当前主文叙述中的纯单因素 compare。

在设计文档中保留这条历史线路，有助于解释仓库为何存在多条 dated rerun 报告；但其功能仅止于历史归档。当前正式的默认路径、模块角色与 backend compare 结论，均不应以 `2026-03-27` 的结果为主锚点。

## 11. 结果分析、机制解释与结论边界

### 11.1 当前工程版总体 rerun：主流程基线已经形成正式归档

`outputs/rerun_v2_engine_safe_20260318_rerun/benchmark_runs/symkanbenchmark_runs.csv` 给出了当前工程版主流程的三 seed 均值：

| 指标 | 均值 |
| --- | ---: |
| `final_acc` | 0.769167 |
| `final_n_edge` | 87.666667 |
| `macro_auc` | 0.956765 |
| `stage_total_seconds` | 45.172832 |
| `symbolic_core_seconds` | 35.651883 |
| `symbolize_wall_time_s` | 75.699789 |
| `run_total_wall_time_s` | 140.332975 |
| `validation_mean_r2` | -0.630428 |

这组结果支持的并不是某个局部模块的优劣，而是两个更基础的判断。第一，当前工程版已经具备稳定落盘、可复跑、可带日期引用的主流程基线，而不再依赖单次探索性终端输出。第二，当前工程版主流程大致稳定在 `final_n_edge ≈ 88`、`macro_auc ≈ 0.957`、`run_total_wall_time_s ≈ 140s` 的工程量级，这一量级可以作为设计文档中的总体性能锚点。

因此，`2026-03-18` 的主要作用是为全文提供“当前工程版已收敛到什么运行区间”的背景，而不是为 ICBR backend 或 LayerwiseFT 专题代答。

### 11.2 工程策略对照：默认主路径为何仍是 `baseline`

同一轮总体 rerun 中，`benchmark_ab/comparison/` 比较了 `baseline`、`adaptive` 与 `adaptive_auto` 三条工程策略：

| 变体 | final_acc | final_n_edge | macro_auc | run_total_wall_time_s | symbolic_core_seconds | symbolize_wall_time_s | validation_mean_r2 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| baseline | 0.777433 | 88.666667 | 0.956107 | 153.470521 | 33.867724 | 88.751556 | -0.672284 |
| adaptive | 0.742533 | 86.000000 | 0.945706 | 209.552334 | 47.499191 | 104.127099 | -0.646339 |
| adaptive_auto | 0.751467 | 89.000000 | 0.946249 | 130.715215 | 33.259280 | 74.526931 | -0.552361 |

当前维护结果显示：

1. `baseline` 仍是三条工程路径中质量最稳的主引用路径，`final_acc` 与 `macro_auc` 均为最高。
2. `adaptive` 没有换来稳定质量收益，却显著抬高了整体耗时，因此不能写成当前默认路径的替代者。
3. `adaptive_auto` 在速度侧优于 `baseline`，但其质量指标在三 seed 上并未形成支配，因此更适合作为可选加速分支，而不是主叙述中的默认路径。

由此可见，当前默认主路径之所以保留 `baseline`，不是因为仓库尚未尝试工程调节策略，而是因为 `2026-03-18` 当前维护结果尚未支持把 `adaptive` 或 `adaptive_auto` 上升为新的质量主基线。

### 11.3 模块消融：默认流水线的职责分工来自专题证据

`docs/ablation_report.md` 给出了 `outputs/benchmark_ablation/` 的单点消融结果。这条线路的核心意义，不在于“哪些数值更大”，而在于不同模块被拿掉后，哪一部分系统语义失守。

首先，Stagewise Train 是当前流程中的必要前提，而不是普通调参开关。去掉后，`final_acc` 从 `0.7807` 降至 `0.4430`，`macro_auc` 从 `0.9548` 降至 `0.8379`，同时 `effective_target_edges` 急剧上升到 `1040`。这说明不经过可控稀疏化准备，符号化入口会失去可治理性。默认开启 Stagewise Train，因而不是经验偏好，而是当前“可用/不可用”分界的直接要求。

其次，Progressive Pruning 的主要作用是复杂度治理，而不是追求单点精度。关闭后，`final_acc` 上升到 `0.8017`，但表达式复杂度由 `126.90` 升至 `194.33`，`effective_input_dim` 由 `57.67` 升至 `70.00`，`symbolic_total_seconds` 由 `33.58s` 升至 `43.51s`。当前结果表明，剪枝的核心价值在于把结构规模与符号成本压回可接受区间，而不是保证每个点估计都最优。

再次，Input Compaction 对应的是“公式一致性与运行成本”的显式权衡。关闭后，`validation_mean_r2` 从 `-0.6135` 提升到 `+0.0275`，但 `effective_input_dim` 同时升到 `120`，`symbolic_total_seconds` 升到 `41.34s`。这意味着输入压缩并非纯收益模块：它牺牲部分公式数值一致性，换取更低输入维数与更低符号化成本。当前默认保留该模块，反映的是工程版对吞吐与复杂度的优先级，而不是“所有指标都更好”。

最后，LayerwiseFT 在当前 2 层 KAN 中没有体现出默认收益模块的性质。相对 `full`，`w/o LayerwiseFT` 的 `final_acc` 为 `0.7838`，`macro_auc` 为 `0.9544`，与基线处于近似同一量级；但 `symbolic_total_seconds` 从 `33.58s` 降到 `20.41s`。因此，模块消融线路已经给出一个明确方向：LayerwiseFT 更接近高成本可选修正，而非必须保留的默认步骤。

这组结果共同解释了当前默认流水线的结构分工：Stagewise 负责保证可符号化入口，剪枝负责控制复杂度，输入压缩负责工程成本治理，而 LayerwiseFT 在当前 2 层结构中不具备默认开启的充分理由。

### 11.4 LayerwiseFT 改进专题：为何改进版仍未改变默认决策

如果仅依据四模块消融，还不足以断定“LayerwiseFT 在任何合理实现下都不应默认开启”。`docs/layerwiseft_improved_report.md` 的作用，正是在这一点上给出更细的专题回答。该报告显示，在 `full` 与 `layerwiseft_esreg` 已对齐到“验证早停 + 轻正则 + 60 步短微调”的前提下，二者几乎没有可观测差异：

| 变体 | final_acc | macro_auc | 表达式复杂度 | `validation_mean_r2` | 符号化耗时 (s) | 阶段训练耗时 (s) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| full | 0.7807 ± 0.0013 | 0.9548 ± 0.0028 | 126.90 ± 31.17 | -0.6135 ± 0.0331 | 33.58 ± 0.31 | 40.33 ± 1.76 |
| layerwiseft_esreg | 0.7807 ± 0.0013 | 0.9548 ± 0.0028 | 126.90 ± 31.17 | -0.6135 ± 0.0331 | 33.28 ± 1.34 | 40.02 ± 1.51 |
| wolayerwiseft | 0.7838 ± 0.0014 | 0.9544 ± 0.0047 | 126.90 ± 31.17 | -0.5937 ± 0.0151 | 20.41 ± 0.06 | 39.54 ± 1.66 |

当前维护结果显示，两点结论最为关键。

第一，改进版 LayerwiseFT 并未相对 `full` 形成新增收益。`full` 与 `layerwiseft_esreg` 的分类指标、复杂度与公式验证指标均无实质差异，这说明“改进版修复了旧风险”并不等于“改进版已经构成默认收益模块”。

第二，相对 `wolayerwiseft`，改进版仍然主要体现为耗时增加，而非稳定质量改进。`delta_new_vs_wolayerwiseft.csv` 显示，改进版相对关闭 LayerwiseFT 的主要变化是 `symbolic_total_seconds` 增加 `12.8624s`，约为 `+63.00%`；与此同时，`final_acc` 未出现稳定提升，`validation_mean_r2` 反而更低。

这一现象在当前 2 层 KAN 中并非偶然。专题报告给出的机制解释可以概括为三点：逐层符号化本质上是有损替换；`fix_symbolic` 之后函数族被冻结，后续调整只能在受限参数空间内进行；而 2 层结构只提供一次局部补偿窗口，难以将局部修正转化为稳定的全局净收益。因而，当前专题结果支持的稳妥表述是：LayerwiseFT 在 2 层 KAN 中仍应被视为可选实验开关，而非默认模块。

### 11.5 Layered paired backend compare：当前最保守的 fairness 主证据

`2026-04-01` 的 layered paired 切片对应 `outputs/rerun_v2_engine_safe_20260401/benchmark_ab/comparison/`。其前提不是“两个结果目录都跑完了”，而是 shared-state 对齐已经被显式核验。`baseline_icbr_shared_check.csv` 在 `42/52/62` 三个 seeds 上均报告：

1. `shared_numeric_aligned = True`
2. `trace_aligned = True`
3. `shared_symbolic_prep_aligned = True`

这意味着当前 layered paired 切片可以被解释为 backend-only compare。其变体均值如下：

| 变体 | final_acc | final_n_edge | macro_auc | run_total_wall_time_s | symbolic_core_seconds | symbolize_wall_time_s | validation_mean_r2 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| baseline | 0.777467 | 88.333333 | 0.951264 | 69.864499 | 33.297856 | 68.013948 | -0.486988 |
| baseline_icbr | 0.788667 | 88.333333 | 0.961440 | 62.462939 | 19.013927 | 60.000633 | -0.409281 |

当前维护结果支持如下表述：在 shared numeric、trace rhythm 与 shared symbolic-prep 均对齐的条件下，ICBR 在 layered 函数库设置中实现了约 `1.751763x` 的 `symbolic_core_speedup_vs_baseline`，同时在 `final_acc`、`macro_auc` 与 `validation_mean_r2` 上出现同步改善。由于 `final_n_edge` 两侧均值完全一致，这一结果可以被写成“同复杂度下的 paired backend compare 收益”，而不仅仅是“更快但结构不同”的经验比较。

这一线路因此承担了全文中最保守的 fairness 主证据角色。任何关于“ICBR backend 在当前工程版中带来 paired 收益”的正式写法，都应首先以此处的 layered paired 切片为锚点，而不是改用更宽松或更早期的实验目录。

### 11.6 FAST_LIB paired compare 与 full library 单边补充：扩库后的边界如何变化

FAST_LIB paired 切片对应 `outputs/rerun_v2_engine_safe_20260401/benchmark_ab/comparison_fastlib/`。与 layered paired 相同，该切片在 `42/52/62` 三个 seeds 上同样满足 `shared_numeric_aligned=True`、`trace_aligned=True` 与 `shared_symbolic_prep_aligned=True`，因此仍可解释为 backend-only compare。其均值结果为：

| 变体 | final_acc | final_n_edge | macro_auc | run_total_wall_time_s | symbolic_core_seconds | symbolize_wall_time_s | validation_mean_r2 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| baseline_fastlib | 0.794000 | 88.333333 | 0.962537 | 112.233492 | 75.187859 | 110.162969 | -0.451777 |
| baseline_icbr_fastlib | 0.793233 | 88.333333 | 0.962634 | 69.944645 | 31.990798 | 67.817348 | -0.456489 |

与 layered paired 相比，FAST_LIB paired 的写作重点发生了变化。当前结果显示，`symbolic_core_speedup_vs_baseline` 约为 `2.350452`，速度收益比 layered 切片更明显；但质量侧更适合写成“近似持平”，因为 `final_acc` 仅出现 `-0.000767` 的微小下降，`macro_auc` 与 target-side 指标变化也极小。因此，这一线路支持的不是“更大函数库下质量全面提升”，而是“扩库条件下 ICBR 仍保持 paired 提速，质量总体近似持平”。

在此基础上，`baseline_icbr_fulllib` 提供了一个更弱的补充切片。该单边结果为：

| 变体 | final_acc | final_n_edge | macro_auc | final_target_mse | final_target_r2 | symbolic_core_seconds | symbolize_wall_time_s | run_total_wall_time_s |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| baseline_icbr_fulllib | 0.795433 | 88.333333 | 0.963225 | 0.035896 | 0.601003 | 35.218785 | 39.693965 | 41.757397 |

相对 `baseline_icbr_fastlib`，该切片呈现出轻微质量收益与有限时间增加。但由于 `baseline_fulllib` 本轮未继续运行，当前证据只能支持如下保守表述：ICBR 使 full library 路径在当前工程版中仍然可运行，并带来单边收益补充。它不支持“full library 下 ICBR 相对 baseline 仍保持 paired fairness”之类写法，也不应被用来替代 FAST_LIB 或 layered 的 paired 证据。

### 11.7 综合讨论：当前默认流水线为何如此设置

将上述线路并置后，当前默认流水线的来源可以收束为一条清晰的设计链条。

首先，`2026-03-18` 总体 rerun 说明当前工程版已经形成稳定的主流程归档，而 `baseline` 在工程策略对照中仍是质量最稳的主引用路径。因此，默认主 workflow 仍以 `baseline` 路径为中心，而不是将 `adaptive` 或 `adaptive_auto` 上升为默认设置。

其次，模块消融说明默认流水线并非任意模块堆叠，而是由职责分工约束出来的工程方案：Stagewise Train 决定符号化入口是否可用；Progressive Pruning 负责复杂度治理；Input Compaction 以牺牲部分公式数值一致性为代价换取更低输入维数与更低符号成本；LayerwiseFT 在当前 2 层 KAN 中不构成默认收益模块，因此项目层默认更接近 `--layerwise-finetune-steps 0`。

再次，LayerwiseFT 改进专题进一步说明，即使引入验证早停与轻正则，改进版 LayerwiseFT 也没有在当前 2 层结构中形成可观测净收益。这使“默认关闭 LayerwiseFT”从一次消融观察上升为更稳健的专题结论。

最后，`2026-04-01` backend compare 表明 ICBR 应被理解为一个显式可选的 backend，而不是对默认 baseline 的静默替换。其 paired 收益成立于 shared numeric 与 shared symbolic-prep 已经对齐这一严格前提之上；因此，ICBR 的实验结论属于“backend compare 线路”，而不是“当前工程版总体 rerun 线路”的一部分。

综合这些结果，当前设计文档能够回答“为什么默认流水线是这样设置的”：它并不是在每一项指标上都最强，而是在当前工程版的复跑稳定性、复杂度治理、符号成本与结论可归因性之间形成了最可维护的折中。

### 11.8 结论边界

基于当前维护结果，设计文档中的实验结论应严格按证据层级收束：

1. 来自 `2026-03-18` 总体 rerun 的结论，只能用于描述当前工程版总体基线、工程策略权衡与主引用归档，不写成 backend-only compare。
2. 来自 `docs/ablation_report.md` 的结论，用于说明默认流水线为何成立，以及各模块的职责边界，不写成 backend 优劣判断。
3. 来自 `docs/layerwiseft_improved_report.md` 的结论，用于说明 LayerwiseFT 在当前 2 层 KAN 中不构成默认收益模块，不写成总体 rerun 或 ICBR compare 的替代证据。
4. 来自 `2026-04-01` layered paired 的结论，是当前最保守的 backend-only fairness 主证据。
5. 来自 `2026-04-01` FAST_LIB paired 的结论，用于说明更大候选库下的 paired 速度边界，其质量表述应保持“近似持平”。
6. 来自 `baseline_icbr_fulllib` 的结论，只能写成 full library 可运行性与单边收益补充，不能补写不存在的 paired fairness。
7. 来自 `2026-03-27` 历史专题的结论，只能作为历史工程权衡存档，不进入当前正式主结论。

因此，当前维护结果真正支持的综合表述可以收束为：当前工程版已形成可带日期引用的总体 rerun 基线；默认流水线的结构来自模块职责与工程折中的专题证据；在 shared-state 对齐成立的前提下，ICBR 在 layered 与 FAST_LIB 两条 paired 线路中均表现出明确的核心符号阶段提速，但两条线路的写作重点不同；而 full library 结果目前仍停留在 ICBR 单边补充层级。超出这一证据等级的“统一大表式”总括，不属于当前维护结果能够稳妥支持的范围。

## 12. 风险与应对

### 风险 1：缓存边界漂移破坏 compare 公平性

若后续配置项变化进入 numeric cache key 或 symbolic-prep cache key 的方式不一致，paired compare 的 shared-state 语义就会失效。当前应对方式是：

1. 保持 compare 公平性由 shared-check 文件落盘验证；
2. 在文档中坚持只有 shared-check 成立时才使用 backend-only compare 表述。

### 风险 2：指标被误读

最常见的误读有两种：

1. 用 `symbolize_wall_time_s` 替代 `symbolic_core_seconds` 作为 backend 主速度指标；
2. 把 `formula_export_success_rate` 解释成真实公式恢复成功率。

当前应对方式是：在设计文档中固定指标优先级与解释边界，不让结果章节自行扩义。

### 风险 3：兼容层长期演化成本

notebook 兼容层、根目录 shim 与脚本入口共同保证了使用连续性，但也带来维护成本。当前更稳妥的策略不是删除兼容层，而是继续把配置转换职责收敛到 `AppConfig`，把桥接层保持为薄接口。

### 风险 4：文档与实现漂移

本仓库已有较完整的文档分层，真正的风险不在于“文档太少”，而在于：

1. compare 语义变化后设计文档未同步；
2. 结果目录更新后工程报告与设计文档混写；
3. 操作性 runbook 内容侵入设计文档。

因此，本文必须保持设计角色，只承载设计论证和证据边界，不承载命令级说明。

## 13. 结论

SymKAN 当前最准确的定位，不是新的 KAN 数值训练器，也不是通用 symbolic regression 框架，而是一个围绕训练后 KAN 组织起来的工程化符号实验流水线。它的核心价值在于把配置、复杂度治理、后端差异、结果验证与 compare 语义放到同一套可复现的结构中。

基于当前仓库实现与维护中的证据，本文最终收束为以下六条稳定表述：

1. `AppConfig` 统一了配置边界，使 notebook、CLI 与脚本层围绕同一对象协同。
2. `stagewise_train`、progressive pruning 与 input compaction 构成了当前可符号化入口的治理基础。
3. LayerwiseFT 在当前 2 层 KAN 设定下更适合作为可选微调开关，而不是默认收益模块。
4. shared symbolic-prep 与 backend-specific symbolic completion 的分离，使 `baseline` 与 `icbr` 的 paired compare 具备了可检查的公平性边界。
5. layered 与 FAST_LIB paired compare 都支持 ICBR 的核心符号阶段提速结论，但 layered 证据更适合承载保守的 backend-only 主叙述，FAST_LIB 证据更适合承载更大候选库下的速度边界说明。
6. `baseline_icbr_fulllib` 只能被写成 full library 可运行性的补充单边证据，不能替代 paired compare。

因此，当前 SymKAN 设计文档更适合被理解为一篇“关于工程化符号流水线如何被约束、如何被比较、以及当前证据允许怎样写”的论文式说明，而不是一份命令手册或泛化过度的性能宣言。
