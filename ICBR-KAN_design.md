# ICBR-KAN Design

状态: Draft  
日期: 2026-03-29  
范围: 设计一种替代当前逐边贪心符号拟合的后处理算法, 在**完全复用已经训练好的数值 KAN**前提下, 以尽量小的算法增量改进符号恢复质量与候选评估效率。

## 1. 摘要

本文将 ICBR-KAN 重新收缩为一个更稳健、更可实现的 Phase I 设计。

它严格满足以下边界:

- **训练阶段完全不改**
- **直接复用已训练完成的数值 KAN**
- **只改动符号拟合阶段**
- **不是新的训练器**
- **不是通用 symbolic regression**
- **不是程序搜索**
- **不是全局公式树发现**

相对当前 baseline `MultKAN.auto_symbolic()`，本文只保留两个核心改进点:

1. **shared-tensor symbolic candidate evaluation**  
   将 `suggest_symbolic()` 背后的逐边逐函数状态型试探，改写为对缓存 `(x_e, y_e)` 的无状态、按函数固定按边成批的候选评估。
2. **teacher-replay contextual reranking**  
   对每条边不再按局部 `R^2` 直接提交 top-1，而是在冻结教师 KAN 的上下文中用小校准集 replay 选择最终提交候选。

除此之外，第一版**明确不做**:

- block planning
- coupling graph
- active set
- affine polish
- 提交后再训练数值 KAN

换言之，本文不是把原方案扩张成一个复杂的 planning 系统，而是把它收紧为:

**更高效的候选生成 + 更正确的提交决策。**

## 2. 设计前提

### 2.1 控制变量原则

本设计遵循一个明确的实验原则:

**实验中完全复用已经训练好的数值 KAN。**

因此，所有对比实验都应在**相同的训练后数值模型**上运行:

- baseline 符号拟合器
- ICBR-KAN
- 两个核心改进点的消融

训练、剪枝、输入压缩如无特别说明均保持不变。

### 2.2 当前仓库中的真实任务

当前 `kan/` 中，符号恢复的真实工作流不是“重新从原始数据发现公式”，而是:

1. 先训练出数值 `MultKAN`;
2. 执行 forward，读取缓存的 `acts` 与 `spline_postacts`;
3. 对每条活跃边拟合一个单变量候选:

$$
\hat{\phi}_{l,j,i}(u)=c\,g(au+b)+d;
$$

4. 通过 `fix_symbolic()` 把该边从数值支路切到符号支路;
5. 最终由 `symbolic_formula()` 导出公式。

因此，ICBR-KAN 的真实任务是:

**给定一个已经训练好的数值 KAN，设计一个更优的 post-hoc symbolic fitting algorithm，以替代当前逐边局部贪心提交策略。**

### 2.3 第一版允许改什么，不改什么

允许改动:

- 候选生成方式
- 候选排序方式
- 最终提交决策方式
- replay 评估与诊断接口

不改动:

- 数值 KAN 的训练流程
- `KANLayer` / `FastKANLayer` 的数值表示
- spline / radial-bf 主体参数训练机制
- `symbolic_formula()` 的导出语义
- 已训练数值模型作为教师模型的身份

### 2.4 必须写清楚的实现事实

本文把以下三条视为**设计前提**，而不是实现细节:

1. `symbolic_formula()` 只读取 `symbolic_fun`，不读取数值支路。  
   因此，在导出前，每条有效边都必须有符号项。
2. `suggest_symbolic()` 当前会通过 `fix_symbolic()` / `unfix_symbolic()` 临时改模型状态。  
   因此候选生成与最终提交在当前实现中是耦合的。
3. `MultKAN.copy()` 当前是 checkpoint 式磁盘复制。  
   它不能直接作为高频 replay 内环 primitive。
4. `symbolic_formula()` 不把 `mask` 作为唯一真源。  
   因此，导出前不仅要 fully symbolic，还必须保证 `funs`、`funs_sympy`、`funs_avoid_singularity`、`funs_name`、`affine` 与 mask 处于一致状态，不能留下历史残留。

这三条分别决定了:

- 为什么第一版必须 fully symbolic 收口
- 为什么第一版必须重写候选生成
- 为什么第一版必须新增内存态 replay helper

## 3. KAN 理论与当前实现给出的直接约束

### 3.1 KAN 的核心结构

KAN 借用了 Kolmogorov-Arnold 表示中的“一元函数组合”思想，但当前 `kan/` 的真正实现结构是:

- 每条边对应一个一元函数响应;
- 多变量结构来自层级组合;
- 组合关系还会经过 `subnode_scale / subnode_bias / node_scale / node_bias` 与乘法节点传播。

因此，KAN 的 post-hoc symbolic fitting 既不是:

- 从零做公式树搜索

也不是:

- 完全逐边独立的局部替换

而是:

**在一个冻结的组合网络上，对边级一元函数做逐步符号替换。**

### 3.2 当前 `kan/` 中真正可直接复用的对象

对第 `l` 层边 `(i -> j)`，当前实现已经提供:

- 边输入缓存: `acts[l][:, i]`
- 边目标缓存: `spline_postacts[l][:, j, i]`
- 单边参数化: `c g(a x + b) + d`
- 符号写入口: `symbolic_fun[l]` 与 `fix_symbolic()`

其中最重要的是:

$$
x_e = \texttt{acts}[l][:, i],\qquad
y_e = \texttt{spline\_postacts}[l][:, j, i].
$$

需要加一条实现条件:

- `spline_postacts` 只有在**纯数值教师状态**下，才能直接被当作 teacher edge target
- `acts` 也只有在**纯数值教师 forward** 下采集时，才能与 `spline_postacts` 一起构成 teacher cache

这说明第一版最自然的算法重写点就在这里:

- 候选生成不必再经由 `suggest_symbolic()` 反复改状态;
- 可以直接把 `(x_e, y_e)` 当作 batched candidate evaluation 的输入。

### 3.3 为什么局部拟合分数不能直接等价于最终提交分数

当前单边拟合处理的是:

$$
\phi_e(u)\approx \hat{\phi}_e(u),
$$

但真正关心的是，在当前 work model 状态下替换该边之后:

$$
f_{\text{work+}e}(x)\approx f_{\text{teacher}}(x).
$$

两者之间隔着:

- 当前层的组合
- subnode affine
- node affine
- 下游 suffix

因此，单边局部 `R^2` 最多只能作为候选生成代理，而不应直接充当最终提交分数。

## 4. 当前 baseline 的真实语义

### 4.1 baseline 的代码路径

当前 `MultKAN.auto_symbolic()` 的关键路径是:

1. 遍历每条边;
2. 调用 `suggest_symbolic()`;
3. `suggest_symbolic()` 对函数库逐个调用 `fix_symbolic()` 做单边拟合;
4. 按复杂度与局部 `r2` 排序;
5. 由 `auto_symbolic()` 把 top-1 再次 `fix_symbolic()` 真正提交。

也就是说，baseline 的核心不是“全局搜索”，而是:

**逐边局部拟合 + 立即硬提交。**

### 4.2 baseline 的两个真实问题

当前 baseline 的结构性问题只有两个，而且都与当前 `kan/` 实现直接相关:

1. **候选生成是状态污染式的**  
   `suggest_symbolic()` 在枚举候选时会反复触碰模型内部 symbolic state。
2. **最终提交仍由局部拟合分数决定**  
   top-1 局部候选被直接提交，没有经过冻结教师上下文中的 replay 重排。

因此，相对 baseline 最稳健的改进也应只对应这两点，而不是一下子引入更多高风险机制。

### 4.3 `fit_params()` 的真实能力边界

当前 `kan.utils.fit_params()` 的真实语义是:

- 对 `(a,b)` 做有限网格扫描与缩窗搜索;
- 用相关性式 `r2` 作为局部排序代理;
- 在固定 `(a,b)` 后，用线性回归拟合 `(c,d)`;
- 对非法数值用 `nan_to_num` 兜底。

因此，本文只把它视为:

**candidate generator**

而不是:

**单边全局最优求解器**

## 5. ICBR-KAN 的重新定义

### 5.1 方法定义

本文将 ICBR-KAN 重新定义为:

**Imitation-Context Batched Reranking for KAN**

它是一个严格面向**冻结数值 KAN 后处理**的符号拟合器。

输入:

- 已训练好的数值 KAN

输出:

- fully symbolic KAN
- 或由 `symbolic_formula()` 导出的公式

### 5.2 仅保留的两个核心改进点

#### 改进点 1: Shared-Tensor Symbolic Candidate Evaluation

用缓存的 `(x_e, y_e)` 直接做无状态候选评估，替代 `suggest_symbolic()` 的状态式试探。

这一点的主要价值是:

- **工程与接口一致性**
- **状态去耦**
- **候选生成阶段的常数级提速空间**

#### 改进点 2: Teacher-Replay Contextual Reranking

对每条边的 shortlist，不再按局部 `R^2` 直接提交，而是在冻结教师上下文中用 replay imitation loss 选择最终提交候选。

这一点的主要价值是:

- **目标函数一致性**
- **最终提交分数与真实 post-hoc 目标更贴近**

### 5.3 第一版明确不包含的内容

为控制实现风险，第一版不把以下内容作为方法核心:

- active set
- coupling score
- block planning
- pairwise synergy
- behavior-diverse shortlist
- affine-only polish

这些都可以作为后续扩展，但不应混入 Phase I 的主设计。

### 5.4 算法主线

ICBR-KAN 第一版的整体流程为:

1. Freeze teacher and collect teacher cache
2. Build edge shortlists by shared-tensor batched evaluation
3. For each edge, rerank shortlist by teacher replay
4. Commit best candidate
5. Continue until every effective edge has a symbolic assignment
6. Export by `symbolic_formula()`

这条流程的特征是:

- 候选生成和提交决策被拆开
- 最终决策引入冻结教师上下文
- 仍保持逐边、逐层、可控、易实现

## 6. 问题形式化

### 6.1 冻结教师模型与工作模型

设已经训练好的数值 KAN 记为:

$$
f_{\text{teacher}}.
$$

post-hoc 阶段中，我们显式区分两个对象:

1. **teacher model**  
   完全冻结，不做任何提交，只用于提供目标缓存和 replay 对照输出。
2. **work model**  
   从教师初始化，逐边提交符号候选，最终用于导出公式。

这是第一版必须写清楚的边界。  
否则“冻结教师边曲线”与“提交后 work state 已变化”会在定义上混淆。

### 6.2 边级候选参数化

对第 `l` 层边 `e=(l,j,i)`，设候选函数库为 `\mathcal{G}_l`。  
每个候选保持与当前 `kan/` 一致的参数化:

$$
\hat{\phi}_{e}(u)=c_e\,g_e(a_e u+b_e)+d_e.
$$

其中 `(a,b,c,d)` 与 `fit_params()` / `Symbolic_KANLayer.affine` 的语义一致。

### 6.3 teacher cache 与 work state 的职责划分

本文把每条边用到的数据分成两类:

1. **teacher cache**  
   来自冻结教师模型的 forward:
   - `x_e^{T}`
   - `y_e^{T}`
2. **work state**
   来自当前已部分符号化的 work model:
   - 当前已提交的 symbolic assignments
   - replay 时的整体输出

第一版固定如下使用规则:

- 候选生成只使用 `teacher cache`
- 最终提交分数只使用 `work state` 上的 replay imitation

### 6.4 与通用 symbolic regression 的区别

本文不是:

- 从原始样本直接生成全局公式树
- 重新学习整体函数

而是:

**对冻结 KAN 中的单边一元函数做候选生成，并在网络上下文中做最终提交决策。**

### 6.5 teacher imitation 与任务损失的桥接

当前 `kan/` 的默认训练损失是回归型 MSE。  
因此第一版理论桥接固定在这一设定。

定义:

$$
\mathcal{L}_{\text{imit}}^{\text{sq}}(f; f_{\text{teacher}})
=
\frac{1}{n}\sum_{t=1}^n
\|f(x_t)-f_{\text{teacher}}(x_t)\|_2^2.
$$

$$
\mathcal{L}_{\text{task}}^{\text{mse}}(f)
=
\frac{1}{n}\sum_{t=1}^n
\|f(x_t)-y_t\|_2^2.
$$

记教师残差为

$$
r_t=f_{\text{teacher}}(x_t)-y_t,
$$

工作模型扰动为

$$
d_t=f(x_t)-f_{\text{teacher}}(x_t).
$$

则

$$
\mathcal{L}_{\text{task}}^{\text{mse}}(f)
-\mathcal{L}_{\text{task}}^{\text{mse}}(f_{\text{teacher}})
=
\frac{1}{n}\sum_{t=1}^{n}
\left(2\langle r_t,d_t\rangle+\|d_t\|_2^2\right).
$$

若 $\|r_t\|_2 \le R$，则

$$
\left|
\mathcal{L}_{\text{task}}^{\text{mse}}(f)
-\mathcal{L}_{\text{task}}^{\text{mse}}(f_{\text{teacher}})
\right|
\le
2R\,\mathcal{L}_{\text{imit}}(f;f_{\text{teacher}})
+
\mathcal{L}_{\text{imit}}^{\text{sq}}(f;f_{\text{teacher}}).
$$

因此，在当前回归/MSE 设定下，用 imitation gap 做最终提交评分是有直接理论动机的。

### 6.6 第一版的逐边决策目标

第一版不做联合 block 规划，而是对当前 work state 下的每条边 `e` 做 shortlist 重排。

设 `\mathcal{S}_e` 为边 `e` 的候选集合。  
对任一候选 `z \in \mathcal{S}_e`，记把它临时写入当前 work model 后得到的模型为 `f_{\text{work}}^{(e \leftarrow z)}`。

第一版的最终提交分数定义为:

$$
\mathcal{J}_e(z)=
\mathcal{L}_{\text{imit}}^{\text{sq}}
\big(
f_{\text{work}}^{(e \leftarrow z)};
f_{\text{teacher}}
\big)
+
\lambda_c\,\mathcal{C}(z).
$$

然后提交

$$
z_e^\star=\arg\min_{z\in\mathcal{S}_e}\mathcal{J}_e(z).
$$

这就是第一版的核心决策规则。

## 7. ICBR-KAN 的关键设计

### 7.1 Freeze Teacher and Collect Teacher Cache

在符号拟合开始前，先固定一个**纯数值教师模型**并收集:

- `teacher_acts[l][:, i]`
- `teacher_edge_targets[l][:, j, i]`
- 小校准集上的教师输出

这里必须强调:

- 这些 cache 来自教师模型，而不是后续逐步变化的 work model
- cache 一旦收集完成，第一版候选生成阶段不再刷新它们

更具体地说，若教师仍是纯数值 KAN，则可以直接复用当前 `forward()` 中在该状态下得到的:

- `acts`
- `spline_postacts`

作为 `teacher cache` 的底座。  
若教师模型中已有 symbolic branch 打开，则不能直接把当前 `spline_postacts` 当成纯 teacher edge target，必须先回到纯数值教师状态再收集 cache。

### 7.2 Shared-Tensor Symbolic Candidate Evaluation

这是第一核心改进点，也是你特别强调应保留的部分。

对每条边 `e=(l,j,i)`，从 teacher cache 取:

$$
x_e = \texttt{teacher\_acts}[l][:, i],\qquad
y_e = \texttt{teacher\_edge\_targets}[l][:, j, i].
$$

随后不再走 `suggest_symbolic()` 的状态型循环，而是对固定函数族 `g` 做同层批量候选评估。

在当前 KAN 后处理场景中，真正可共享的不是公式树搜索中的 DAG 子式，而是:

- 同层所有边的输入缓存 `x_e`
- 同层所有边的目标缓存 `y_e`
- 固定函数族共享的仿射搜索网格 `(a,b)`
- 中间张量 `u = a x + b`
- 批量相关性、均值、方差等排序统计量

因此，更准确的表述不是抽象的“并行 symbolic enumeration”，而是:

**shared-tensor symbolic candidate evaluation for KAN edges**

它的直接收益是:

- 消除 `suggest_symbolic()` 的状态污染
- 候选生成与最终提交解耦
- 为批处理和缓存复用提供空间
- 在不改变问题定义的前提下争取常数级速度收益

需要明确:

- 这不是主阶复杂度改进
- 它首先是计算重组与状态去耦
- 常数级收益来自共享 tensor 与减少无谓状态写入

### 7.3 Simple Shortlist Instead of Rich Heuristics

为控制实现风险，第一版 shortlist 不做复杂的“行为多样性标签工程”。

对每条边，只保留一个简单 shortlist:

- 局部拟合分数高的若干候选
- 同时保留函数族复杂度信息
- 记录必要的拟合诊断

第一版建议保留的诊断量只有:

- `boundary_hit`
- `nan_to_num_trigger`
- `top1_top2_margin`

这样做的目的是:

- 保留足够的候选可供 replay 重排
- 不把大量启发式塞进第一版核心方法

### 7.4 Teacher-Replay Contextual Reranking

这是第二核心改进点。

对每条边 `e` 的 shortlist `\mathcal{S}_e`，第一版不再根据局部 `R^2` 直接提交 top-1，而是:

1. 在当前 work model 状态下，临时写入候选 `z`
2. 在小校准集上完整 forward
3. 与冻结教师输出比较 imitation gap
4. 按 `\mathcal{J}_e(z)` 选最终候选

这一步的关键意义是:

- 局部 `R^2` 只看边曲线
- replay imitation 直接看“当前网络上下文中的真实提交后果”

因此，这里的“contextual”不是通用 planning，而是一个更收紧的概念:

**single-edge contextual reranking inside a frozen KAN**

### 7.5 提交顺序保持简单

为了控制变量，第一版不额外发明复杂的选边策略。

建议直接沿用当前 `auto_symbolic()` 的基本外层顺序:

- 逐层
- 层内逐输入、逐输出

新的内容只发生在:

- 如何生成 shortlist
- 如何在 shortlist 内做最终重排

而不发生在:

- 重新设计全局选边顺序

### 7.6 Fully Symbolic Completion 是接口约束，不是可选功能

由于 `symbolic_formula()` 只读取 `symbolic_fun`，所以第一版必须保证:

- 每条有效边最终都写入一个符号候选
- 被剪掉的边显式写为 `0`

这里不能把“fully symbolic 收口”写成附加美观目标。  
它是 exporter correctness 的硬约束。

### 7.7 第一版明确不做的事情

以下内容全部移出第一版主方法:

- edge active set
- pairwise coupling
- block 决策
- block replay
- 提交后 affine polish
- node/subnode affine 优化

这样做的理由不是这些想法没价值，而是:

- 它们超出了“相对 baseline 的适量改进”
- 它们会显著提高实现与调参不稳定性
- 它们并不是取得第一轮有效提升的必要条件

## 8. 算法伪代码

### 8.1 Algorithm 1: Batched Candidate Generation

```python
def build_edge_shortlist_batched(edge_packets, layer_lib, cfg):
    shortlists = {}
    diagnostics = {}

    for fun_name in layer_lib:
        batch_result = batched_symbolic_candidates(
            edge_packets=edge_packets,
            fun_name=fun_name,
            a_range=cfg.a_range,
            b_range=cfg.b_range,
        )

        for edge, result in batch_result.items():
            shortlists.setdefault(edge, []).append(
                Candidate(
                    fun_name=fun_name,
                    params=result.params,
                    local_score=result.local_score,
                    complexity=result.complexity,
                )
            )
            diagnostics.setdefault(edge, []).append(
                CandidateDiagnostic(
                    fun_name=fun_name,
                    boundary_hit=result.boundary_hit,
                    nan_to_num_trigger=result.nan_to_num_trigger,
                )
            )

    for edge in shortlists:
        shortlists[edge] = keep_topk_by_local_score(
            shortlists[edge],
            k=cfg.shortlist_size,
        )

    return shortlists, diagnostics
```

### 8.2 Algorithm 2: Teacher-Replay Contextual Reranking

```python
def rerank_edge_by_teacher_replay(work, teacher, calib, edge, shortlist, cfg):
    best = None
    best_obj = float("inf")

    for cand in shortlist:
        replay_loss = evaluate_edge_candidate_by_replay(
            work=work,
            teacher=teacher,
            calib=calib,
            edge=edge,
            candidate=cand,
        )
        obj = replay_loss + cfg.lambda_c * cand.complexity
        if obj < best_obj:
            best_obj = obj
            best = cand

    return best, best_obj
```

### 8.3 Algorithm 3: Full ICBR-KAN Procedure

```python
def auto_symbolic_icbr(teacher, dataset, cfg):
    teacher_cache = collect_teacher_cache(teacher, dataset, cfg)
    work = clone_numeric_teacher_as_work_model(teacher, cfg)

    for layer_idx in range(work.depth):
        edge_packets = build_layer_edge_packets(teacher_cache, layer_idx, cfg)
        layer_lib = resolve_layer_library(layer_idx, work.depth, cfg)
        shortlists, diagnostics = build_edge_shortlist_batched(
            edge_packets, layer_lib, cfg
        )

        for edge in iterate_edges_in_baseline_order(work, layer_idx):
            best, score = rerank_edge_by_teacher_replay(
                work=work,
                teacher=teacher,
                calib=dataset["calibration"],
                edge=edge,
                shortlist=shortlists[edge],
                cfg=cfg,
            )
            commit_symbolic_candidate(work, edge, best)

    return finalize_symbolic_report(work, teacher_cache, cfg)
```

## 9. 理论分析

### 9.1 基本假设

第一版只依赖以下假设:

**假设 A1: 教师充分性**  
冻结数值 KAN 已位于可接受性能区间，因此 post-hoc 阶段的目标是逼近教师而不是重新学习任务。

**假设 A2: suffix 局部正则性**  
当前 work state 附近的下游组合映射在工作域上局部稳定。

**假设 A3: 校准子集代表性**  
小校准集上的 replay 排序能近似整体数据上的 imitation 风险排序。

需要提前说明的是，两个核心改进点的理论地位并不相同:

- 改进点 1 主要解决计算组织与接口语义问题
- 改进点 2 主要解决最终提交分数与目标错配问题

### 9.2 定理 1: 在当前回归/MSE 设定下，teacher imitation 控制任务损失偏移

沿用第 6.5 节定义。若教师残差满足 `\|r_t\|_2 \le R`，则

$$
\left|
\mathcal{L}_{\text{task}}^{\text{mse}}(f)
-\mathcal{L}_{\text{task}}^{\text{mse}}(f_{\text{teacher}})
\right|
\le
2R\sqrt{\mathcal{L}_{\text{imit}}^{\text{sq}}(f;f_{\text{teacher}})}
\mathcal{L}_{\text{imit}}^{\text{sq}}(f;f_{\text{teacher}}).
$$

因此，在当前 `kan/` 的默认回归场景中，最终提交分数以 imitation gap 为主是合理的。

### 9.3 命题 2: 局部 `R^2` 不是最终提交分数

对同一条边的两个候选 `z_1, z_2`，即便它们在 teacher cache 上的局部 `R^2` 排名满足

$$
R^2(z_1) > R^2(z_2),
$$

也不能推出在当前 work state 下有

$$
\mathcal{J}_e(z_1) < \mathcal{J}_e(z_2).
$$

原因是 `R^2` 只评估边曲线拟合，而 `\mathcal{J}_e(z)` 评估的是当前网络上下文中的整体 imitation 偏移。

因此:

- `R^2` 适合作为候选生成代理
- replay imitation 才适合作为最终提交分数

### 9.4 命题 3: shared-tensor candidate evaluation 是计算重组，不是问题重定义

对固定层与固定函数族 `g`，若使用同一组 `(x_e, y_e)`、同一参数化 `c g(a x+b)+d` 与同一局部打分规则，则:

- 逐边逐函数串行评估
- 按函数固定、按边成批的 batched 评估

在数学目标上等价，区别只在于计算组织方式。

因此，改写为 shared-tensor batched evaluation:

- 不会改变候选空间
- 不会改变每个候选的定义
- 只是在工程上减少状态污染并争取常数级收益

这正是第一核心改进点的理论与实现边界。

### 9.5 理论上必须被实验验证的断言

第一版需要实验验证的断言只有三个:

1. imitation gap 与最终 MSE loss shift 在当前任务族上显著相关
2. contextual rerank 相比局部 `R^2` top-1 有更高的最终提交质量
3. shared-tensor candidate evaluation 能带来稳定的常数级时间收益

## 10. 复杂度分析

记:

- `E` 为有效边数
- `F` 为函数库大小
- `K` 为每边 shortlist 大小
- `C_fit` 为单边 `fit_params` 成本
- `C_replay` 为一次 replay evaluator cycle 成本
- `C_commit` 为一次提交成本

### 10.1 baseline 复杂度

当前 baseline 的主要成本可写成:

$$
T_{\text{base}}
=
O(E F C_{\text{fit}} + E C_{\text{commit}}).
$$

其中 `E F C_fit` 对应候选拟合，`E C_commit` 对应最终 top-1 提交。

### 10.2 ICBR-KAN Phase I 复杂度

第一版 ICBR-KAN 的总成本为:

$$
T_{\text{ICBR}}
=
T_{\text{cand}}
+
T_{\text{rerank}}
+
T_{\text{commit}}.
$$

其中:

#### A. 候选生成

$$
T_{\text{cand}}=O(E F C_{\text{fit}}).
$$

主阶与 baseline 相同。  
但 shared-tensor evaluation 带来的是:

- 更少的状态写入
- 更高的缓存复用
- 更强的按函数批处理能力
- 在保留当前 `sklearn.LinearRegression` 路径时，收益主要来自前半段共享计算与状态去耦，而不是完整意义上的批量闭式求解

因此，这里的主张应明确写成:

**常数级改进，而不是主阶下降。**

#### B. 单边 contextual rerank

每条边对 `K` 个 shortlist 候选做 replay:

$$
T_{\text{rerank}}=O(E K C_{\text{replay}}).
$$

#### C. 最终提交

每条边提交一次:

$$
T_{\text{commit}}=O(E C_{\text{commit}}).
$$

### 10.3 为什么这是合理的复杂度分配

第一版新增成本只花在真正更接近目标的地方:

- 候选生成阶段做更干净的批量评估
- 决策阶段用 replay 做最终重排

而没有把预算投入到:

- block 规划
- 全网重训
- 高维交互搜索

这符合本文“适量有效提升”的设计原则。

### 10.4 11.3 所强调的常数级收益应如何表述

这部分需要特别保留并写清楚:

共享的不是公式树中的“中间表达式”，而是:

- 同层所有边的 `x_e`
- 同层所有边的 `y_e`
- 固定函数族共享的 `(a,b)` 网格
- 中间张量 `u = a x + b`
- 批量相关性/方差统计量

因此，第一版复杂度收益不应写成“并行枚举改变大 O”，而应写成:

**通过 shared-tensor symbolic candidate evaluation 降低候选生成的常数项。**

### 10.5 第一版的硬件口径: 只实现 CPU 路线

第一版明确固定为 **CPU-first implementation**。  
也就是说，Phase I 只承诺实现 CPU 路线，不把 CUDA 作为交付目标。

更重要的是，这种选择不是保守退让，而是因为当前 `kan/` 的 post-hoc symbolic fitting 结构，本来就更吻合 CPU 路线的稳健优化。

#### A. 为什么第一版应实现 CPU 路线

在当前保留 `fit_params()` + `sklearn.LinearRegression` 的前提下，CPU 路径最现实的收益来源是:

- 减少 `suggest_symbolic()` 带来的 state mutation
- 减少 `fix_symbolic()` / `unfix_symbolic()` 的重复写入
- 共享 `(a,b)` 搜索网格
- 共享 `u = a x + b` 与相关统计量
- 按函数固定、按边成批，减少 Python 循环与对象调度开销

因此，CPU 路径的第一目标应写成:

**降低 Python 调度、状态写入和重复张量计算的常数项。**

这与当前 KAN 的吻合点在于:

- 当前 symbolic fitting 的基本单位本来就是**单边一元函数**
- `suggest_symbolic()` 的主要低效本来就来自**状态试写**而不是大矩阵训练
- `SYMBOLIC_LIB` 是异构函数库，很多开销来自 Python 层枚举与对象管理
- replay、commit、export 都带有明显的控制流与对象状态语义，而不是纯张量大算子

因此，对当前 KAN 而言，CPU 路径不是“退而求其次”，而是更贴合第一版问题结构的默认实现方向。

#### B. 为什么第一版不实现 CUDA 路线

若后续将候选生成更多留在 torch 侧，并把 `(c,d)` 拟合改为 torch 内闭式批量求解，则 CUDA 路径的主要收益来源会变成:

- 同层多边共享大张量计算
- 固定函数族下的大批量 `u = a x + b` 与 `g(u)` 评估
- 批量均值、方差、相关性统计
- 减少 CPU/GPU 往返

若未来进入 Phase II，CUDA 路径的目标才应写成:

**把候选生成链尽量保持在同一设备上，利用大张量批处理放大 shared-tensor 评估收益。**

但这里必须明确它与 KAN 的**部分吻合、部分不吻合**:

吻合的部分:

- KAN 的边缓存天然提供了同层多边的 `x_e / y_e`
- 对固定函数族 `g`，`u = a x + b` 与 `g(u)` 的评估可以写成同构大张量计算
- 若层宽较大、候选库较大，teacher-cache candidate generation 确实可能从 GPU 批处理获益

不吻合的部分:

- 当前函数库是**异构**的，不是单一算子族
- replay contextual rerank 需要频繁做**候选写入 / 回滚 / 整网 forward**，这不是最典型的 GPU 优势场景
- `symbolic_formula()`、`sympy`、以及当前 `sklearn.LinearRegression` 路径都不在 CUDA 友好主链上
- 第一版若模型较小、层宽较窄，GPU 往返与 kernel launch 常数项可能吞掉收益

因此，CUDA 优化只应被视为**候选生成子阶段**的潜在放大器，而不应被写成整个 ICBR-KAN Phase I 的默认实现路线。

#### C. 第一版的硬件承诺

第一版的硬件承诺直接写死为:

- **只实现 CPU 路线**
- **不以 CUDA 加速作为 Phase I 验收条件**
- **所有复杂度与 wall time 报告默认按 CPU 路线解释**

这样做的理由是:

- 与当前 `fit_params()` 的真实实现一致
- 与当前 KAN 的控制流型 symbolic fitting 结构一致
- 更容易把收益归因到算法本身，而不是设备差异

### 10.6 这些硬件优化为什么与当前 KAN 场景吻合

为了避免把一般硬件优化叙事硬套到 KAN 上，本文把“吻合”明确限定为以下三点:

1. **是否顺着 KAN 的边级一元函数结构发力**  
   shared-tensor candidate evaluation 直接围绕 `x_e -> y_e` 展开，因此与当前 KAN 的边函数结构吻合。
2. **是否顺着当前 `kan/` 的真实瓶颈发力**  
   当前 baseline 的主要额外开销来自 `suggest_symbolic()` 的状态污染与逐边枚举，而不是大规模参数训练；因此 CPU-first 的状态去耦与共享计算是吻合的。
3. **是否不破坏 post-hoc symbolic fitting 的边界**  
   若某种“优化”实质上要求重写训练器、改写模型主体或引入全网重训练，那它就不再吻合本文的 KAN 问题设定。

据此，本文对两类优化的最终判断是:

- **CPU 改进**: 与当前 KAN Phase I 高度吻合，且是第一版唯一实现目标
- **CUDA 改进**: 只与 candidate generation 子问题局部吻合，保留为 Phase II 可选扩展

## 11. 与相关方法的关系

### 11.1 来自 KAN 本身的启发

KAN 的核心启发是:

- 一元函数在边上
- 高维结构由层级组合形成

这直接支持本文的基本立场:

**post-hoc symbolic fitting 的自然单位是边函数，而不是全局公式树。**

### 11.2 关于“生成/决策分离”的内部设计原则

这一节不必再挂到一般 symbolic regression 框架上。

在当前 `kan/` 场景中，更准确的表述就是:

**候选生成与最终提交应分离。**

也就是说:

- `suggest_symbolic()` 不应继续同时承担“生成候选”和“诱导最终提交”的双重角色
- 局部 top-1 只能进入 shortlist
- 最终提交应由 replay contextual score 决定

### 11.3 来自并行枚举与共享评估的启发

这一节应被保留，而且应被提升为第一核心改进点的直接方法学来源。

从当前 `kan/` 的实现组织来看，`suggest_symbolic()` 的最大低效并不在函数库本身，而在它不能共享同层候选评估中的中间张量。

与之同向的是，近期并行 symbolic enumeration 强调:

- 共享中间表达式
- 批量评估候选
- 将生成与评估解耦

ICBR-KAN 在当前 `kan/` 里的对应落点是:

- 直接在缓存的 `(x_e, y_e)` 上做纯函数式候选评估
- 避开 `suggest_symbolic()` 的状态污染
- 把“逐边逐函数的状态型搜索”改写成“按函数固定、按边成批的无状态评估”
- 为批处理、缓存和后续并行保留可能性

这里还应写得更尖锐一点:

- `suggest_symbolic()` 不是只“建议”，而是通过**试写 symbolic state**来完成候选评估
- 因此 shared-tensor candidate evaluation 改写的是候选生成的组织方式，而不是最终决策目标

这里必须把“共享中间表达式”改写为更符合 `kan/` 现实的表述。  
在当前 KAN 后处理场景中，真正可共享的不是公式树搜索里的 DAG 子式，而是:

- 同层所有边的输入缓存 `x_e`
- 同层所有边的目标缓存 `y_e`
- 对固定函数族共享的仿射搜索网格 `(a,b)`
- 中间张量 `u = a x + b`
- 批量相关性/方差等排序统计量

因此，第一版更精确的表述应是:

**shared-tensor symbolic candidate evaluation for KAN edges**

而不是泛泛地说“并行 symbolic enumeration”。

这一节在第一版中的地位不是外围包装，而是:

**候选生成阶段的直接工程与方法学核心。**  
但也必须明确: 这里的核心更多是工程半边，而不是新的理论目标。

### 11.4 关于局部上下文决策的设计原则

第二核心改进点同样不需要借助抽象 planning 话语。

在当前 `kan/` 场景中，更贴切的事实是:

**我们不需要通用 lookahead，也不需要 block 规划；只需要把每条边的最终提交分数从局部 `R^2` 换成冻结教师上下文中的 replay imitation。**

这就是第一版 contextual reranking 的全部含义。

## 12. 与当前 `kan/` 实现的接口对接

### 12.1 推荐集成位置

建议新增:

- `kan/icbr.py`
- `auto_symbolic_icbr(...)`

也可在 `MultKAN` 上增加 opt-in 入口:

- `MultKAN.auto_symbolic_icbr(...)`

### 12.2 保持不变的本体行为

以下部分保持不变:

- `MultKAN` 的训练行为
- `MultKAN.forward()` 的缓存契约
- `symbolic_formula()` 导出语义
- 数值模型作为冻结教师模型的身份

### 12.3 直接复用的现有对象

ICBR-KAN 直接复用:

- `acts`
- `spline_postacts`（仅在纯数值教师状态下作为 teacher cache）
- `spline_postsplines`（若后续实现需要进一步逼近 numeric-only response，可作为辅助检查对象）
- `SYMBOLIC_LIB`
- `Symbolic_KANLayer.affine`
- `fit_params()`

### 12.4 第一版真正需要新增的 helper

第一版只需要新增三个 helper。

#### Helper 1: `batched_symbolic_candidates(...)`

最小语义:

1. 输入同层一批边的 `(x_e, y_e)`
2. 对固定函数族共享 `(a,b)` 网格与中间张量
3. 返回每条边的候选参数、局部分数与诊断量
4. 不触碰模型 symbolic state

#### Helper 2: `evaluate_edge_candidate_by_replay(...)`

最小语义:

1. 保存目标边的 `funs` / `funs_sympy` / `funs_avoid_singularity` / `funs_name` / `affine` / numeric mask / symbolic mask
2. 在当前 work model 上临时写入某个边候选
3. 在校准集上执行完整 forward
4. 与冻结教师输出比较 imitation gap
5. 逐项恢复上述状态

这里必须是**内存态 snapshot/apply/restore**，不能直接反复调用当前磁盘式 `copy()`。
并且 replay 内环必须完全绕开 `log_history/auto_save` 机制，不能借用会触发落盘的现有 API 作为实现路径。

#### Helper 3: `commit_symbolic_candidate(...)`

最小语义:

1. 注册 `funs` / `funs_sympy` / `funs_avoid_singularity` / `funs_name`
2. 直接写入外部候选 affine
3. 切换 numeric / symbolic mask

之所以必须有这个 helper，是因为当前 `fix_symbolic()` 默认会重新拟合或用默认参数初始化，而不是“提交外部已选候选”。
同时，这个 helper 必须维护 symbolic state 的内部一致性，保证后续 `symbolic_formula()` 不会读到历史残留。

### 12.5 第一版明确不需要的 helper

由于我们已把方法收缩为两个核心改进点，因此第一版不再需要:

- active set helper
- pairwise synergy helper
- block planner
- affine subset optimizer

这能显著降低实现风险。

## 13. 实验设计

### 13.1 对照原则

实验中始终使用**同一批已经训练好的数值 KAN**。  
只替换 `kan/` 层的符号拟合器。

正式对照只需要:

1. baseline `MultKAN.auto_symbolic()`
2. ICBR-KAN

### 13.2 主要验证问题

第一版只回答三个问题:

1. 在相同数值 KAN 上，ICBR-KAN 是否提升最终符号恢复质量?
2. contextual rerank 是否优于局部 `R^2` 直接提交?
3. shared-tensor candidate evaluation 是否带来稳定的常数级时间收益?

### 13.3 数据切分

冻结教师后，post-hoc 阶段至少拆成两个互不重叠子集:

1. **calibration split**  
   仅用于 replay contextual rerank
2. **final-report split**  
   仅用于最终报告

若需要单独验证理论相关性，可再增加:

3. **theory-validation split**

### 13.4 任务层次

#### A. 精确恢复小任务

- `x1 + x2`
- `x1 * x2`
- `sin(x1)`
- `x1^2 + x2^2`

作用:

- 观察 exact family recovery 的经验表现
- 验证 contextual rerank 是否减少明显错误提交

#### B. 组合层级任务

- `exp(sin(x1)+x2^2)`
- `sqrt(x1^2+x2^2+x3^2)`

作用:

- 验证 replay contextual score 是否优于局部 `R^2`

### 13.5 主要指标

1. calibration 上的 replay imitation gap
2. final-report 上的 MSE loss shift
3. formula validation `R^2`
4. valid formula rate
5. symbolic wall time
6. candidate generation wall time
7. replay rerank wall time

### 13.6 必做消融

这部分必须严格围绕两个核心改进点展开。

1. 去掉 shared-tensor batching，回退为状态型候选生成，但保留 contextual rerank
2. 去掉 contextual rerank，回退为局部 top-1 提交，但保留 batched candidates

这两个消融足以回答:

- 增益是否来自候选评估重组
- 增益是否来自最终提交分数改写

### 13.7 理论验证指标

1. imitation gap 与 MSE loss shift 的相关系数
2. contextual rerank 相对局部 `R^2` top-1 的胜率
3. batched candidate evaluation 相对 baseline candidate generation 的时间比
4. teacher cache 与 work state 混用时的退化程度
5. 若不 fully symbolic completion 或 symbolic state 不一致，exporter correctness 被破坏的比例

### 13.8 失败判据

若出现以下现象，则说明第一版建模需要回退修正:

1. contextual rerank 对最终结果几乎无增益
2. batched evaluation 没有带来稳定的时间收益
3. imitation gap 与最终 MSE shift 基本无关

## 14. 风险与应对

### 风险 1: replay rerank 仍然偏贵

应对:

- 控制 shortlist 大小
- 只在小 calibration split 上 replay
- 保持逐边而非 block 级 replay

### 风险 2: batched candidate evaluation 被 CPU 拖尾抵消收益

应对:

- 第一版先接受 `fit_params()` 中 `sklearn` 路径
- 若收益不足，再把 `(c,d)` 拟合改写为 torch 内闭式批量求解

### 风险 3: teacher cache 与 work state 混用

应对:

- 显式维护 `teacher_cache`
- 候选生成永不刷新 teacher cache
- replay 只读取当前 work model 输出与教师输出

## 15. 结论

ICBR-KAN 第一版的最终立场是:

1. **训练好的数值 KAN 应被完整复用**
2. **相对 baseline 的增量应控制在两个核心点内**
3. **第一核心点是 shared-tensor symbolic candidate evaluation**
4. **第二核心点是 teacher-replay contextual reranking**

因此，第一版选择的路线不是:

- 扩展成复杂的 planning 框架
- 引入大量新的启发式组件

而是:

- 用更干净、更可批处理的方式生成候选
- 用更贴近真实目标的方式决定最终提交

这一路线同时满足:

- 与当前 `kan/` 实现直接对齐
- 理论链条足够短
- 相对 baseline 是适量而有效的提升
- 更有机会产出稳健、可实现、可验证的结果
