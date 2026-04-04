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
| 模块角色、默认设定、Stagewise/剪枝/压缩/LayerwiseFT 的职责判断 | [docs/ablation_report.md](ablation_report.md), [docs/layerwiseft_improved_report.md](layerwiseft_improved_report.md), `outputs/benchmark_ablation/` | `benchmark_ab` 的 backend compare 结果 |
| `baseline` vs `baseline_icbr` 的 backend-only compare | [docs/engineering_rerun_report_20260401.md](engineering_rerun_report_20260401.md), `outputs/rerun_v2_engine_safe_20260401/benchmark_ab/comparison/` | 历史 `radial_bf` 工程切片、单边 full library 切片 |
| `baseline_fastlib` vs `baseline_icbr_fastlib` 的更大函数库 paired compare | [docs/engineering_rerun_report_20260401.md](engineering_rerun_report_20260401.md), `outputs/rerun_v2_engine_safe_20260401/benchmark_ab/comparison_fastlib/` | layered paired compare 之外的旧 compare 目录 |
| full library 下 ICBR 的可运行性补充说明 | [docs/engineering_rerun_report_20260401.md](engineering_rerun_report_20260401.md), `outputs/rerun_v2_engine_safe_20260401/benchmark_ab/baseline_icbr_fulllib/` | 任何 paired backend-only 语义表述 |

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

## 10. 实验设计与证据边界

### 10.1 当前需要回答的三个问题

本文当前只回答三个与设计直接相关的问题：

1. 哪些模块决定了 SymKAN 默认流水线的职责分配与默认设定。
2. 在 shared numeric 与 shared symbolic-prep 对齐时，`baseline` 与 `icbr` 的差异能否被解释为 backend-only compare。
3. 当 paired full library compare 不可得时，单边 ICBR 切片最多能支持什么层次的补充结论。

### 10.2 指标口径

本文使用四类指标：

1. 任务指标：`final_acc`、`macro_auc`
2. 复杂度与结构指标：`final_n_edge`、`effective_input_dim`、表达式复杂度
3. 速度指标：`symbolic_core_seconds`、`symbolize_wall_time_s`、`run_total_wall_time_s`
4. 验证与机制指标：`validation_mean_r2`、target-side 指标、shared-check 指标、mechanism breakdown 指标

其中，backend 主速度指标固定为 `symbolic_core_seconds`。

### 10.3 当前证据边界

当前可直接用于本文的结果边界如下：

1. `outputs/benchmark_ablation/`：
   - 回答模块职责与默认设定问题；
   - 不回答 backend-only compare 问题。
2. `outputs/rerun_v2_engine_safe_20260401/benchmark_ab/comparison/`：
   - 回答 layered paired backend-only compare；
   - 是当前最保守的 ICBR paired evidence。
3. `outputs/rerun_v2_engine_safe_20260401/benchmark_ab/comparison_fastlib/`：
   - 回答更大函数库下的 paired speed/quality 边界；
   - 不应替代 layered paired evidence 的公平性叙述。
4. `outputs/rerun_v2_engine_safe_20260401/benchmark_ab/baseline_icbr_fulllib/`：
   - 只回答“ICBR 让 full library 路径仍可运行”的补充问题；
   - 不得写成 paired compare 证据。

## 11. 当前结果与讨论

### 11.1 模块消融给出的默认设定依据

当前模块角色可以收敛为四条：

1. `stagewise_train` 必须保留。
   - 去掉后 `final_acc` 由 `0.7807` 降到 `0.4430`，`macro_auc` 由 `0.9548` 降到 `0.8379`。
   - 这说明它是“可用/不可用”的边界，而不是普通调参项。
2. progressive pruning 默认保留。
   - 去掉后虽然 `final_acc` 升至 `0.8017`，但复杂度增至 `194.33`，`symbolic_total_seconds` 升至 `43.51s`。
   - 因此它主要是复杂度治理模块。
3. input compaction 需要按目标取舍。
   - 去掉后 `validation_mean_r2` 从 `-0.6135` 升到 `+0.0275`，但输入维数升至 `120`，符号时间升至 `41.34s`。
   - 因此它是速度与公式一致性之间的明确权衡。
4. 2 层 KAN 默认关闭 LayerwiseFT 仍然合理。
   - 相对 `wolayerwiseft`，改进版 LayerwiseFT 未形成稳定质量净收益，却显著增加符号时间。

这些结论共同说明：当前默认流水线不是“平均意义上都更好”，而是围绕可复现性、复杂度治理与工程成本做出的约束性选择。

### 11.2 layered paired compare：当前最保守的 backend-only 证据

来自 `comparison/baseline_icbr_shared_check.csv` 的 `42/52/62` 三个 seeds 均报告：

- `shared_numeric_aligned=True`
- `trace_aligned=True`
- `shared_symbolic_prep_aligned=True`

这意味着 layered paired compare 可以被解释为 backend-only compare。在这一前提下，当前主结果为：

1. `final_n_edge` 两侧均值同为 `88.333333`；
2. `final_acc` 从 `0.777467` 升至 `0.788667`；
3. `macro_auc` 从 `0.951264` 升至 `0.961440`；
4. `symbolic_core_seconds` 从 `33.297856s` 降至 `19.013927s`；
5. `symbolic_core_speedup_vs_baseline` 均值约为 `1.751763`。

因此，当前 layered 切片支持的更稳妥表述是：

**在保持 shared numeric、trace 与 shared symbolic-prep 对齐的前提下，ICBR 在当前 layered 函数库设置中实现了约 `1.75x` 的核心符号阶段提速，并伴随质量指标改善。**

### 11.3 FAST_LIB paired compare：更大候选库下的速度边界

在 FAST_LIB paired compare 中，shared-check 条件同样全部成立，因此仍可解释为 backend-only compare。当前主结果为：

1. `final_n_edge` 两侧均值仍同为 `88.333333`；
2. `symbolic_core_seconds` 从 `75.187859s` 降至 `31.990798s`；
3. `symbolic_core_speedup_vs_baseline` 均值约为 `2.350452`；
4. `final_acc` 均值仅有 `-0.000767` 的微小下降；
5. `macro_auc` 与 target-side 指标变化接近持平。

因此，FAST_LIB 切片支持的更准确写法不是“更大函数库下质量全面提升”，而是：

**在更大候选库下，ICBR 的主要收益体现在约 `2.35x` 的核心符号阶段提速，而质量侧整体近似持平。**

### 11.4 full library 单边补充切片：可运行性而非 paired fairness

`baseline_icbr_fulllib` 的当前单边均值包括：

- `final_acc = 0.795433`
- `macro_auc = 0.963225`
- `final_target_r2 = 0.601003`
- `symbolic_core_seconds = 35.218785`

相对 `baseline_icbr_fastlib`，该切片表现为轻微质量收益和有限的时间增加。但由于 `baseline_fulllib` 本轮未跑，这一结果只能支持以下补充结论：

**ICBR 让 full library 路径在工程上仍保持可运行，并带来单边质量收益。**

它不支持以下表述：

- “full library 下 ICBR 相对 baseline 仍保持 backend-only fairness”
- “full library paired compare 证明 ICBR 全面优于 baseline”

### 11.5 当前结果真正支持的设计结论

综合当前可引用结果，本文能够稳定支持的结论只有以下四条：

1. SymKAN 的默认流水线是由模块角色约束出来的工程方案，而不是任意模块堆叠。
2. shared symbolic-prep 边界使 paired backend compare 具备了可检查的公平性条件。
3. ICBR 在当前 layered 与 FAST_LIB paired compare 中都呈现出明确的核心符号阶段提速。
4. 当前工程证据更适合支持“设计与比较语义已经收敛”，而不是支持广义统计显著性的总括结论。

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
