# ICBR-KAN Phase I Implementation Plan

状态: Active  
日期: 2026-03-29  
范围: 本计划只覆盖 `ICBR-KAN_design.md` 中已经收缩后的 **Phase I**。实现对象是 **冻结已训练数值 KAN 之后的 post-hoc symbolic fitting**，不是训练器、不是通用 symbolic regression、不是程序搜索、不是全局公式树发现。  
交付口径: **CPU-first**。Phase I 不以 CUDA 作为交付目标或验收条件。

## 1. Goals

在当前 `kan/` 实现契约下，新增一条严格对齐设计稿的 Phase I symbolic fitting 路线，使其相对 baseline `MultKAN.auto_symbolic()` 只包含两个核心改进点:

1. `shared-tensor symbolic candidate evaluation`
2. `teacher-replay contextual reranking`

Phase I 完成后应满足:

- 输入仍然是已经训练完成的数值 `MultKAN`
- 数值训练流程、数值层表示与训练器语义保持不变
- 最终输出仍然必须能够通过 `symbolic_formula()` 导出
- 导出前必须达到 fully symbolic completion
- 所有 wall time、复杂度解释与 benchmark 默认按 CPU 路线汇报

## 2. Non-Goals

以下内容不属于 Phase I 主实施范围；如需提及，只能作为非目标或后续扩展:

- 训练器改造
- 全网重训练
- 通用 symbolic regression 框架
- 程序搜索或全局公式树发现
- block planning
- pairwise coupling / coupling graph / pairwise synergy
- active set
- behavior-diverse shortlist heuristic 扩张
- affine-only polish
- node affine / subnode affine 优化
- CUDA candidate path
- 任何以设备切换替代算法收益归因的验收方式

## 3. Implementation Principles

### 3.1 Phase I Baseline Semantics to Respect

当前 baseline 不是全局搜索，而是:

1. `auto_symbolic()` 逐层、逐边遍历
2. 每条边调用 `suggest_symbolic()`
3. `suggest_symbolic()` 对函数库逐个调用 `fix_symbolic()` 做单边拟合
4. `suggest_symbolic()` 再调用 `unfix_symbolic()` 回退
5. 按局部 `r2` 与复杂度排序
6. `auto_symbolic()` 将 top-1 再次 `fix_symbolic()` 真正提交

因此，Phase I 只允许替换两件事:

- 候选生成的组织方式
- 最终提交的评分方式

外层遍历顺序保持与 baseline 一致，避免把 Phase I 扩张为新的全局 planning 系统。

### 3.2 Exporter Contract Is a Hard Constraint

必须显式尊重以下事实:

- `symbolic_formula()` 只读取 `symbolic_fun` 中的 `funs_sympy` 与 `affine`，并按层组合导出
- `symbolic_formula()` 不把 numeric branch 作为导出真源
- `symbolic_formula()` 也不把 mask 当作唯一真源

因此，Phase I 结束时必须满足:

- 每条有效边都有明确 symbolic assignment
- 被剪掉的边必须显式提交为 `0`
- `funs`
- `funs_sympy`
- `funs_avoid_singularity`
- `funs_name`
- `affine`
- numeric mask
- symbolic mask

以上状态必须彼此一致，不能留下历史残留。

### 3.3 Teacher Cache and Work State Must Be Explicitly Separated

Phase I 必须显式区分:

- `teacher cache`: 来自冻结教师模型的缓存
- `work state`: 当前逐步提交 symbolic candidate 的工作模型状态

使用规则固定为:

- 候选生成只使用 `teacher cache`
- shortlist replay 只在当前 `work state` 上执行
- teacher 输出只作为 imitation target，不参与提交状态写入

### 3.4 Cache Semantics Must Follow Current Forward Behavior

根据当前 `MultKAN.forward()`:

- `acts[l]` 是每层节点级缓存
- `spline_postacts[l]` 保存的是当前 forward 下的 edge-level postacts
- `spline_postsplines[l]` 保存 numeric branch 的 edge response cache

必须写清楚:

- `acts` 与 `spline_postacts` 只有在 **纯数值教师 forward** 下采集时，才能作为 teacher cache 使用
- 一旦 symbolic branch 打开，`spline_postacts` 就混入 symbolic contribution，不能再被当作纯教师边目标
- `spline_postsplines` 可以作为 numeric response 辅助检查，但不是 exporter 真源

### 3.5 Replay Helpers Must Be Memory-Resident

Phase I replay 内环不能依赖现有高开销或不完整的 primitive:

- `MultKAN.copy()` 当前通过 `saveckpt()` / `loadckpt()` 走磁盘式复制，不适合作为 replay 内环
- `unfix_symbolic()` 只切换 mode 并把 `funs_name` 改为 `"0"`，不是完整 rollback primitive
- replay 内环必须绕开 `log_history()` / `auto_save` / checkpoint 落盘路径

因此，Phase I 必须新增内存态 snapshot/apply/restore helper。

### 3.6 `fit_params()` Is Only a Candidate Generator

Phase I 复用 `fit_params()` 的参数化边界:

- 搜索 `(a, b)` 网格
- 用相关性式 `r2` 做局部代理排序
- 用 `LinearRegression` 在固定 `(a, b)` 后拟合 `(c, d)`
- 对非法数值用 `torch.nan_to_num` 兜底

但必须明确:

- `fit_params()` 不是单边全局最优求解器
- 局部 `r2` 只能用于生成 shortlist，不能直接作为最终提交分数

### 3.7 Why Phase I Is CPU-First

Phase I 固定 CPU 路线，不是保守退让，而是由当前 `kan/` 的真实结构决定:

- symbolic fitting 的基本单位是单边一元函数
- baseline 的主要低效来自 `suggest_symbolic()` 的状态试写，而不是大规模张量训练
- 当前函数库异构，开销大量来自 Python 枚举、对象状态写入与回滚
- replay、commit、export 具有显著控制流与对象状态语义
- `fit_params()` 当前仍依赖 `LinearRegression`
- `symbolic_formula()` / `sympy` 路径也不在 CUDA 友好主链上

所以 Phase I 的收益目标应当是:

- 降低 Python 调度常数项
- 消除状态污染
- 共享同层候选评估中的中间张量
- 用 replay 改善最终提交质量

而不是把 CUDA 加速写成第一版验收前提。

## 4. Staged Plan

### Stage 0: Freeze Phase I Scope

Goal:

将当前设计稿中的 Phase I 范围收紧并冻结为唯一实施边界，只保留两个核心改进点，不保留任何训练器或 planning 扩张。

Target Files:

- `ICBR-KAN_design.md`
- `IMPLEMENTATION_PLAN.md`

Required Behavior:

- 计划文档必须明确 baseline 的真实语义是“逐边局部拟合 + 立即硬提交”
- 计划文档必须明确 Phase I 只包含:
  - `shared-tensor symbolic candidate evaluation`
  - `teacher-replay contextual reranking`
- 计划文档必须把以下内容写入非目标:
  - block planning
  - coupling
  - active set
  - affine polish
  - CUDA optimization
  - 训练器改造
  - 全网重训练
- 计划文档必须把 CPU-first 口径写死

Success Criteria:

- `IMPLEMENTATION_PLAN.md` 与 `ICBR-KAN_design.md` 的 Phase I 范围一致
- 不再把 Phase I 描述成训练系统或通用 symbolic regression 系统
- 不再把 CUDA 写成 Phase I 主交付目标

Validation:

- 人工逐节核对 `ICBR-KAN_design.md` 第 2、4、5、7、10、12 节
- 人工核对本计划的 Goals / Non-Goals / Stage 定义是否超出 Phase I

Status:

Complete

### Stage 1: Add CPU Batched Candidate Evaluation

Goal:

新增无状态的 CPU 候选生成 helper，直接对冻结教师 cache 中的 `(x_e, y_e)` 做按函数固定、按边成批的候选评估，替代 `suggest_symbolic()` 的状态型试探。

Target Files:

- `kan/icbr.py`（新文件，推荐）
- `kan/MultKAN.py`（仅在需要增加 opt-in 调用入口时修改）
- `tests/test_icbr_candidates.py`（建议）

Required Behavior:

- 输入同层一批边的 `teacher_acts[l][:, i]` 与 `teacher_edge_targets[l][:, j, i]`
- 对固定函数族共享 `(a, b)` 搜索网格
- 共享 `u = a x + b`、均值、方差、相关性等局部统计量
- 返回每条边的:
  - `fun_name`
  - `(a, b, c, d)` 候选参数
  - 局部 `r2`
  - complexity
  - 最小诊断量
- 整个候选生成过程不触碰:
  - `symbolic_fun`
  - `act_fun.mask`
  - `symbolic_fun.mask`
  - `log_history`
  - `auto_save`

Implementation Constraints:

- 复用 `fit_params()` 的问题定义与参数化边界
- 不把本阶段扩张成新优化器或新训练器
- 不依赖当前 `suggest_symbolic()` 实现路径
- teacher cache 只能由纯数值教师 forward 采集

Success Criteria:

- 候选生成与 baseline 单边 `fit_params()` 在参数化语义上兼容
- 调用前后模型 symbolic state、numeric mask 与 symbolic mask 均保持不变
- 可稳定输出最小诊断量:
  - `boundary_hit`
  - `nan_to_num_trigger`
  - `top1_top2_margin`

Validation:

- 最小单元测试: batched candidate 与单边 `fit_params()` 的结果兼容性检查
- 无副作用测试: 候选生成前后比较 `funs` / `funs_sympy` / `funs_avoid_singularity` / `funs_name` / `affine` / numeric mask / symbolic mask
- CPU benchmark smoke test: 记录 `candidate_generation_wall_time_s`

Status:

Complete

### Stage 2: Add Safe Replay Evaluator

Goal:

新增内存态 replay evaluator，对单边 shortlist 做 teacher-replay contextual reranking，并保证 replay 无副作用。

Target Files:

- `kan/icbr.py`
- `tests/test_icbr_replay.py`（建议）

Required Behavior:

- 输入:
  - 当前 `work model`
  - 冻结 `teacher model`
  - calibration split
  - 目标边
  - 单边 shortlist candidate
- 临时将候选写入当前 work state
- 在 calibration split 上执行完整 forward replay
- 以 squared imitation loss 作为默认 replay score
- replay 结束后完整恢复目标边状态

Must Restore:

- `funs`
- `funs_sympy`
- `funs_avoid_singularity`
- `funs_name`
- `affine`
- numeric mask
- symbolic mask

Implementation Constraints:

- 不允许调用 `MultKAN.copy()` 作为 replay 内环 primitive
- 不允许依赖 `unfix_symbolic()` 作为完整 rollback primitive
- 不允许触发 `log_history()`、checkpoint 保存或 `state_id` 递增
- teacher 只提供对照输出，不允许在 replay 中被修改

Success Criteria:

- replay 前后目标边 symbolic state 完整一致
- replay 内环对磁盘、history 与 checkpoint 无副作用
- 可对同一 shortlist 返回稳定 replay 排序

Validation:

- 最小单元测试: replay 前后逐项比较 `funs` / `funs_sympy` / `funs_avoid_singularity` / `funs_name` / `affine` / masks
- replay 无副作用测试: 比较 `state_id`、history 文件、checkpoint 目录是否未变化
- 排序差异测试: 构造案例验证 replay top-1 与局部 `r2` top-1 可以不同

Status:

Complete

### Stage 3: Add Explicit Commit Helper

Goal:

新增显式 commit helper，把外部已选 candidate 直接提交到 `symbolic_fun`，而不是再次调用 `fix_symbolic()` 重新拟合。

Target Files:

- `kan/icbr.py`
- `tests/test_icbr_commit.py`（建议）

Required Behavior:

- 直接注册 candidate 对应的:
  - `funs`
  - `funs_sympy`
  - `funs_avoid_singularity`
  - `funs_name`
- 直接写入 candidate affine
- 明确切换 numeric mask 与 symbolic mask
- 支持将剪掉边或无效边显式提交为 `0`

Implementation Constraints:

- commit helper 不能把“外部已选 candidate”再次交回 `fix_symbolic()` 重新做拟合
- commit 后 symbolic state 必须可被 `symbolic_formula()` 正确读取
- 不允许仅通过修改 mask 来宣称完成 symbolic commit

Success Criteria:

- 对任意单边 shortlist candidate 可直接提交，无需重新跑 `fit_params()`
- 提交后 `forward()` 可继续运行
- 提交后 `symbolic_formula()` 行为与 symbolic state 一致

Validation:

- exporter correctness 测试: `commit_symbolic_candidate()` 后 `symbolic_formula()` 可导出
- 零函数提交测试: 显式提交 `0` 候选后导出与 forward 均可运行
- 一致性测试: `funs` / `funs_sympy` / `funs_avoid_singularity` / `funs_name` / `affine` / masks 逐项匹配

Status:

Complete

### Stage 4: Add `auto_symbolic_icbr(...)` Entry

Goal:

将 batched candidate generation、teacher replay reranking 与 explicit commit 串成新的 Phase I 入口。

Target Files:

- `kan/icbr.py`
- `kan/MultKAN.py`（如需挂接 `MultKAN.auto_symbolic_icbr(...)`）
- `tests/test_icbr_integration.py`（建议）

Required Behavior:

- 冻结教师模型
- 在纯数值教师状态下采集 teacher cache
- 显式创建与教师区分开的 `work model`
- 沿用 baseline 的层序与边序遍历
- 每条边:
  - 基于 teacher cache 生成 shortlist
  - 基于当前 work state 做 replay rerank
  - 提交最优候选
- 导出前达到 fully symbolic completion

Implementation Constraints:

- teacher cache 与 work state 必须显式区分
- 若教师当前不是纯数值状态，必须先恢复到纯数值教师状态再收集 cache
- `symbolic_formula()` 只看 `symbolic_fun`，因此 fully symbolic completion 是导出前硬约束
- 不把本阶段扩张为新选边策略、新 block 策略或新训练流程

Success Criteria:

- 能从已训练 `MultKAN` 运行一条新的 ICBR Phase I 路线
- 最终每条有效边都有 symbolic assignment
- `symbolic_formula()` 可在最终 work model 上完成导出

Validation:

- 最小集成测试: 小模型跑通 `auto_symbolic_icbr(...)`
- teacher/work 分离测试: 混用 cache 与 work state 时应触发失败或暴露不一致
- fully symbolic completion 测试: 未 fully symbolic 时 exporter 不应被判定为通过

Status:

Complete

### Stage 5: Benchmark and Verify Phase I Claims

Goal:

用最小可复现实验验证 Phase I 的两个核心主张，并只按 CPU 路线验收。

Target Files:

- `tests/test_icbr_benchmark_smoke.py`（建议）
- 如有必要，最小 benchmark 脚本或 notebook
- 结果汇总文档或 markdown 记录

Required Behavior:

- 固定同一批已训练数值教师模型
- 对比:
  - baseline `MultKAN.auto_symbolic()`
  - Phase I `auto_symbolic_icbr(...)`
- 至少分别汇报:
  - `candidate_generation_wall_time_s`
  - `replay_rerank_wall_time_s`
  - `symbolic_wall_time_s`
  - replay imitation gap
  - final MSE loss shift
  - formula validation result

Success Criteria:

- 至少在最小任务和一个组合任务上完成 CPU 结果
- 能说明 contextual rerank 相比局部 `r2` top-1 的收益或边界
- 能说明 shared-tensor candidate evaluation 相比 baseline 候选生成的 CPU 常数级收益
- 不以 CUDA 加速结果作为 Phase I 是否通过的依据

Validation:

- 最小 benchmark: 记录 `candidate_generation_wall_time_s`
- 最小 benchmark: 记录 `replay_rerank_wall_time_s`
- replay 无副作用测试必须通过
- exporter correctness 检查必须通过
- 最小单元测试与最小集成测试必须通过

Status:

Complete

### Stage 6: Extended Multi-Seed Benchmark Validation

Goal:

在保持 CPU-first 与 baseline 对照口径不变的前提下，扩展 benchmark 到多 seeds 与更大任务集，并增加可用于误差条与统计检验的结构化统计与可视化汇总。

Target Files:

- `scripts/icbr_benchmark.py`
- `tests/test_icbr_benchmark_script_smoke.py`
- `tests/test_icbr_benchmark_smoke.py`（如需补充指标结构检查）
- `TASK_STATUS.md`

Required Behavior:

- benchmark 支持多 seeds 运行，并保留 `rows` 级明细结果用于后续统计检验
- benchmark 支持大于当前 `minimal/combo` 的任务集（可通过 task 列表扩展）
- 按 task 聚合时，至少对核心数值指标输出:
  - `count`
  - `mean`
  - `median`
  - `std`
  - `min`
  - `max`
- 汇总中保留 baseline vs ICBR 的对照可读性（时间、MSE、公式验证）
- 增加统计显著性相关输出（至少覆盖 wall time delta 与 MSE shift）
- 生成可视化汇总产物（用于快速对比 task 间差异）

Implementation Constraints:

- 不改动 ICBR 算法主路径，只扩展 benchmark 与报告层
- 不删除现有 `rows` 明细字段
- 不把扩展验证改写为全量大规模实验平台；保持可复现、可 smoke 的默认执行
- 继续遵守 CPU-first 验收口径，不引入 CUDA 作为通过条件

Success Criteria:

- 同一次 benchmark 运行可产出:
  - 明细级 `rows`（含 seed 级结果）
  - task 级聚合统计（含 `mean | median | std | min | max`）
  - 统计显著性摘要
  - 可视化汇总文件
- 测试覆盖新的聚合结构与导出文件存在性
- 脚本实跑可在多 seed 条件下完成并落盘

Validation:

- `pytest tests/test_icbr_benchmark_smoke.py tests/test_icbr_benchmark_script_smoke.py`
- 运行 `scripts.icbr_benchmark`（多 tasks + 多 seeds）并检查:
  - `icbr_benchmark_rows.csv`
  - `icbr_benchmark_summary.json`
  - `icbr_benchmark_summary.md`
  - 新增统计/可视化产物
- 人工核对 JSON 聚合字段是否包含 `count | mean | median | std | min | max`

Status:

Complete

### Stage 7: Regression Gating and Stability Verification

Goal:

在 Stage 6 扩展 benchmark 基础上，新增可执行回归门禁机制，确保多 seed 结果具备稳定可判定的“通过/失败”信号，用于后续版本回归与自动化验收。

Target Files:

- `scripts/icbr_benchmark_regression.py`（新脚本，建议）
- `scripts/icbr_benchmark.py`（如需补充 machine-readable summary 支撑）
- `tests/test_icbr_benchmark_regression_smoke.py`（建议）
- `TASK_STATUS.md`

Required Behavior:

- 输入:
  - benchmark summary JSON（来自 `scripts.icbr_benchmark`）
  - 可配置的门禁阈值配置（JSON 或内置默认）
- 输出:
  - 逐任务与 overall 的门禁判定结果（pass/fail）
  - 每条判定的实际值、阈值与方向说明
  - 机器可读结果文件（JSON）与人类可读简报（Markdown）
- 默认门禁至少覆盖:
  - `formula_validation_result` pass rate 下限
  - `symbolic_speedup_vs_baseline` median 下限
  - `final_mse_loss_shift` mean 上限
- 对任何失败项给出明确 fail reason，且脚本返回非零退出码

Implementation Constraints:

- 不修改 ICBR 算法路径，只扩展 benchmark 验收层
- 不覆盖 Stage 6 产物结构；新脚本应消费现有 summary JSON
- 门禁阈值默认取保守值，避免把小样本偶然波动误判为稳定收益
- 保持 CPU-first 验收口径

Success Criteria:

- 同一份 benchmark summary 可被 regression 脚本稳定判定
- smoke 测试覆盖:
  - 全部通过场景
  - 至少一个门禁失败场景
- 回归脚本输出包含:
  - `overall_status`
  - `checks` 明细
  - fail reason（如有）

Validation:

- `pytest tests/test_icbr_benchmark_regression_smoke.py`
- 基于 `outputs/icbr_benchmark_extended/icbr_benchmark_summary.json` 实跑:
  - `python -m scripts.icbr_benchmark_regression --summary-json ...`
- 人工核对:
  - 失败时退出码非零
  - JSON/Markdown 报告中阈值与实际值一致

Status:

Complete

### Stage 8: Diagnose and Fix `trig_interaction` Regression

Goal:

在不扩张 Phase I 算法范围的前提下，针对 `trig_interaction` 的 `final_mse_loss_shift` 超门禁问题做最小范围诊断与修复，并以 10 seeds 重新验证 Stage 7 门禁结果。

Target Files:

- `scripts/icbr_benchmark.py`
- `scripts/icbr_benchmark_regression.py`（如需阈值覆盖或门禁配置入口增强）
- `tests/test_icbr_benchmark_script_smoke.py`（如需补充结构/默认参数断言）
- `tests/test_icbr_benchmark_regression_smoke.py`（如需补充门禁覆盖）
- `TASK_STATUS.md`

Required Behavior:

- 先完成诊断:
  - 明确 `trig_interaction` 回归是否与 candidate lib、replay topk 或门禁策略直接相关
  - 给出最小可解释的修复路径，不进行无关扩张
- 实施最小修复:
  - 优先围绕 `trig_interaction` 的候选库/重排参数做任务级调优
  - 保持其他任务行为与口径稳定
- 固化 10 seeds 验证口径:
  - benchmark 使用 `0..9` 共 10 个 seeds
  - 复跑 Stage 7 regression gate 并产出新报告

Implementation Constraints:

- 不改动 ICBR 主算法核心流程，只调 benchmark task 配置与验收策略
- 不删除 rows 明细与 Stage 6/7 既有导出结构
- 若修复后仍有单项失败，必须如实记录，不得“假通过”

Success Criteria:

- 使用 10 seeds 重新生成扩展 benchmark summary
- regression gate 在新结果上通过；若未通过，必须明确剩余失败项与下一步处理方案
- 相关 smoke 测试通过

Validation:

- `pytest tests/test_icbr_benchmark_smoke.py tests/test_icbr_benchmark_script_smoke.py tests/test_icbr_benchmark_regression_smoke.py`
- `python -m scripts.icbr_benchmark --seeds 0,1,2,3,4,5,6,7,8,9 ...`
- `python -m scripts.icbr_benchmark_regression --summary-json ...`
- 人工核对 regression gate JSON:
  - `overall_status`
  - `failed_check_count`
  - `checks` 中 `trig_interaction` 相关项

Status:

Complete

### Stage 9: Add Teacher Quality Gate and Target-Error Metrics

Goal:

新增“数值教师质量门禁”与“符号模型对真实目标函数误差”指标，确保 benchmark 结论不会在教师数值拟合质量不足时被误读。

Target Files:

- `kan/icbr.py`
- `scripts/icbr_benchmark.py`
- `scripts/icbr_benchmark_regression.py`
- `tests/test_icbr_benchmark_smoke.py`
- `tests/test_icbr_benchmark_script_smoke.py`
- `tests/test_icbr_benchmark_regression_smoke.py`
- `TASK_STATUS.md`

Required Behavior:

- benchmark 行级结果必须新增真实目标误差指标（至少包含）:
  - `teacher_target_mse`
  - `teacher_target_r2`
  - `baseline_target_mse`
  - `baseline_target_r2`
  - `icbr_target_mse`
  - `icbr_target_r2`
  - `symbolic_target_mse_shift`
  - `symbolic_target_r2_shift`
- benchmark 必须新增 teacher 门禁字段（至少包含）:
  - `teacher_quality_gate_pass`
  - `teacher_quality_gate_reason`
- 当 teacher 质量未通过门禁时，默认不执行 baseline/ICBR 符号化对比，并在导出中如实标记为门禁失败。
- regression gate 必须新增与 teacher 门禁及 target-error 指标相关的检查项。

Implementation Constraints:

- 不改动 ICBR 主算法路径，只扩展 benchmark 与 regression 验收层。
- 保持 rows 明细导出；新字段必须贯通 CSV/JSON/Markdown。
- 对缺失真实标签的调用路径保持兼容（可返回 NaN 或空原因，但不得 silently 伪造通过）。

Success Criteria:

- 多 seed benchmark 导出中可直接读取 teacher 质量门禁结果与 target-error 对照指标。
- regression gate 可对 teacher 质量与 target-error shift 进行 pass/fail 判定。
- 相关 smoke 测试覆盖新字段与新门禁逻辑并通过。

Validation:

- `pytest tests/test_icbr_benchmark_smoke.py tests/test_icbr_benchmark_script_smoke.py tests/test_icbr_benchmark_regression_smoke.py`
- `python -m scripts.icbr_benchmark --tasks minimal,combo --seeds 0,1 --output-dir outputs/icbr_benchmark_stage9_smoke --train-num 24 --test-num 24 --train-steps 4 --lr 0.05 --topk 2 --grid-number 11 --iteration 1 --quiet`
- `python -m scripts.icbr_benchmark_regression --summary-json outputs/icbr_benchmark_stage9_smoke/icbr_benchmark_summary.json --output-dir outputs/icbr_benchmark_stage9_smoke`（默认门禁下预期 fail，用于验证 teacher 质量门禁生效）
- `python -m scripts.icbr_benchmark --tasks minimal,combo --seeds 0,1 --output-dir outputs/icbr_benchmark_stage9_smoke_pass --train-num 24 --test-num 24 --train-steps 4 --lr 0.05 --topk 2 --grid-number 11 --iteration 1 --teacher-max-test-mse 1.0 --teacher-min-test-r2 -1.0 --quiet`
- `python -m scripts.icbr_benchmark_regression --summary-json outputs/icbr_benchmark_stage9_smoke_pass/icbr_benchmark_summary.json --output-dir outputs/icbr_benchmark_stage9_smoke_pass --min-formula-pass-rate 0.0 --min-speedup-median 0.0 --max-mse-shift-mean 1.0 --min-teacher-quality-gate-pass-rate 0.0 --max-target-mse-shift-mean 1.0`（放宽阈值后验证管线可 pass）

Status:

Complete

### Stage 10: Calibrate Teacher Convergence and Run 10-Seed Full-Task Verification

Goal:

在不改动 ICBR 主算法的前提下，补充“高质量数值教师”验证口径：提供可复用的高质量 benchmark 配置入口，并在 10 seeds + 全任务集下完成一次门禁复验。

Target Files:

- `scripts/icbr_benchmark.py`
- `tests/test_icbr_benchmark_script_smoke.py`
- `TASK_STATUS.md`

Required Behavior:

- benchmark 提供可显式选择的运行 profile（至少含 `quick` 与 `quality`）:
  - `quick` 用于 smoke/快速回归
  - `quality` 用于教师收敛质量评估
- `quality` profile 至少覆盖:
  - 更高 `train_steps`
  - 更大 `train_num/test_num`
  - 稀疏正则 `lamb`
  - 可与 teacher 质量门禁共同使用
- summary 导出必须明确记录 profile 与实际生效的训练参数。
- 使用 10 seeds + 全任务集运行一次 `quality` profile，并输出门禁结果。

Implementation Constraints:

- 不改动 ICBR 算法路径，只扩展 benchmark 执行与报告层。
- 不删除 Stage 9 新增字段；继续保留 rows 明细导出。
- 不把本 stage 扩展为新训练器或自动调参系统。

Success Criteria:

- benchmark 可通过 profile 选择快速配置或高质量配置。
- 10 seeds 全任务 `quality` 运行可落盘产出 summary/rows/report。
- `TASK_STATUS.md` 如实记录门禁通过率与是否仍有薄弱任务。

Validation:

- `pytest tests/test_icbr_benchmark_script_smoke.py`
- `python -m scripts.icbr_benchmark --profile quality --train-num 2000 --test-num 1000 --lamb 1e-3 --tasks minimal,combo,poly_cubic,trig_interaction --seeds 0,1,2,3,4,5,6,7,8,9 --output-dir outputs/icbr_benchmark_stage10_quality_10seeds_2000_1000_l1e3 --quiet --no-plots`
- `python -m scripts.icbr_benchmark_regression --summary-json outputs/icbr_benchmark_stage10_quality_10seeds_2000_1000_l1e3/icbr_benchmark_summary.json --output-dir outputs/icbr_benchmark_stage10_quality_10seeds_2000_1000_l1e3`
- `python -c "from scripts.icbr_benchmark import _generate_visualizations; ..."`（基于已落盘 rows 生成 PNG 并回写 summary 的 `artifacts.visualizations`）

Status:

Complete

### Stage 11: Add Cross-Run Persistent Teacher Cache

Goal:

为 benchmark 增加跨脚本多次运行可复用的 teacher 持久缓存，避免同一 `task+seed+训练配置` 重复训练，降低总耗时并保证 baseline/ICBR 对照变量稳定。

Target Files:

- `scripts/icbr_benchmark.py`
- `tests/test_icbr_benchmark_script_smoke.py`
- `TASK_STATUS.md`

Required Behavior:

- 支持可配置的 teacher cache 目录与模式:
  - `readwrite`（默认，命中读取，未命中训练后写入）
  - `readonly`（仅读取，未命中时可回退为仅本次训练不写入）
  - `refresh`（忽略旧缓存并重训后覆盖写入）
  - `off`（禁用缓存）
- 缓存键必须覆盖关键训练语义：
  - task、seed、网络结构、训练样本规模、训练步数、lr、lamb、profile、版本标识
- summary/rows 必须新增缓存可观测字段（至少）：
  - `teacher_cache_hit`
  - `teacher_cache_key`
  - `teacher_cache_path`
  - `teacher_cache_mode`
- 命中缓存时不得重复训练 teacher。

Implementation Constraints:

- 不改动 ICBR 主算法，只扩展 benchmark teacher 训练入口层。
- 不删除 Stage 9/10 已有导出字段。
- 使用文件系统缓存但保持最小复杂度；先实现可用版，再考虑更重的并发优化。

Success Criteria:

- 同一参数运行两次 benchmark，第二次出现稳定 cache hit。
- 缓存命中时 rows 与 summary 中可追踪 cache 来源。
- 脚本 smoke 测试覆盖至少一条“首轮 miss + 二轮 hit”路径。

Validation:

- `pytest tests/test_icbr_benchmark_script_smoke.py`
- `python -m scripts.icbr_benchmark --profile quality --tasks minimal,combo,poly_cubic,trig_interaction --seeds 0,1 --output-dir outputs/icbr_benchmark_stage11_cache_run1_qualitydefaults --teacher-cache-dir outputs/teacher_cache_stage11_quality --teacher-cache-mode readwrite --teacher-cache-version stage11_v1 --quiet --no-plots`
- `python -m scripts.icbr_benchmark --profile quality --tasks minimal,combo,poly_cubic,trig_interaction --seeds 0,1 --output-dir outputs/icbr_benchmark_stage11_cache_run2_qualitydefaults --teacher-cache-dir outputs/teacher_cache_stage11_quality --teacher-cache-mode readwrite --teacher-cache-version stage11_v1 --quiet --no-plots`
- 人工核对第二次运行 summary/rows 中 `teacher_cache_hit` 比例与 `teacher_cache_key` 一致性

Status:

Complete

### Stage 12: Add Feynman Dataset Support to `icbr_benchmark.py`

Goal:

在保持现有 benchmark 导出结构、可视化导出与 teacher cache 机制不退化的前提下，为 `scripts/icbr_benchmark.py` 增加对 Feynman 本地数据集目录的直接支持，覆盖 `In-Context-Symbolic-Regression-KAN-main/README.md` 描述的主要数据读取与 CLI 使用方式。

Target Files:

- `scripts/icbr_benchmark.py`
- `tests/test_icbr_benchmark_script_smoke.py`
- `IMPLEMENTATION_PLAN.md`
- `TASK_STATUS.md`

Required Behavior:

- benchmark 支持 Feynman 本地目录参数（与 in-context README 口径对齐）：
  - `--feynman-root`（默认 `datasets`）
  - `--feynman-variant`（`Feynman_without_units` / `Feynman_with_units` / `bonus_without_units` / `bonus_with_units`）
  - `--feynman-equations-csv`（可选；默认尝试 `<feynman_root>/FeynmanEquations.csv`）
  - `--feynman-max-datasets`
  - `--feynman-dataset-select-seed`
  - `--feynman-split-strategy`（`random` / `linspace`）
- 支持 `README` 的两类数据集选择模式：
  - 显式 10 个 paper 数据集（`feynman_paper10`）
  - 随机子集（可复现，受 `dataset_select_seed` 控制）
- 本地 Feynman 文件加载后应可用于 teacher 训练与 baseline/ICBR 符号化对比。
- 现有 benchmark 产物结构保持兼容：
  - `icbr_benchmark_rows.csv`
  - `icbr_benchmark_summary.json`
  - `icbr_benchmark_summary.md`
  - 可视化 PNG（启用绘图时）
- teacher cache 对 Feynman 任务继续有效，且 cache key 要包含必要数据来源语义（至少任务名、variant、split 策略、训练参数与版本）。

Implementation Constraints:

- 不改动 ICBR 主算法，只扩展 benchmark 数据接入层与 CLI。
- 不破坏现有非 Feynman 任务（`minimal/combo/poly_cubic/trig_interaction`）行为与测试。
- 保持 CPU-first 验收口径。
- 若本地 `datasets/` 尚未准备好，必须在文档中如实记录，并使用最小可执行 smoke 验证证明代码路径可用。

Success Criteria:

- `icbr_benchmark.py` 可直接消费本地 Feynman 文件目录完成训练与符号化流程。
- 现有导出字段与 teacher cache 字段保持可用；新增 Feynman 来源信息可读可追溯。
- 脚本测试覆盖至少一个 Feynman 数据加载 smoke 路径并通过。

Validation:

- `python -m py_compile scripts/icbr_benchmark.py tests/test_icbr_benchmark_script_smoke.py`
- `pytest tests/test_icbr_benchmark_script_smoke.py`
- `pytest tests/test_icbr_benchmark_smoke.py tests/test_icbr_benchmark_script_smoke.py tests/test_icbr_benchmark_regression_smoke.py`
- 使用本地数据（若已就绪）运行：
  - `python -m scripts.icbr_benchmark --tasks feynman_paper10 --profile quality --feynman-root datasets --feynman-variant Feynman_with_units --feynman-max-datasets 10 --feynman-dataset-select-seed 2 --output-dir outputs/icbr_benchmark_stage12_feynman_paper10 --quiet --no-plots`
- 若数据尚未就绪，运行最小 mock/fallback smoke，验证 Feynman CLI 解析、数据读取与导出路径（已通过 `tests/test_icbr_benchmark_script_smoke.py::test_feynman_dataset_file_loading_smoke`）。

Status:

Complete

### Stage 13: Add Feynman Reference Preset and Prune-Refit Teacher Flow

Goal:

为 Feynman 实验提供可直接调用的参考配置（对齐 `In-Context-Symbolic-Regression-KAN-main/README.md` 与 `ablation.py` 的核心设定），并将 teacher 训练流程调整为“先训练 -> 自动剪枝 -> 微调 100 步 -> 缓存 -> baseline/ICBR 符号化对比”。

Target Files:

- `scripts/icbr_benchmark.py`
- `tests/test_icbr_benchmark_script_smoke.py`
- `IMPLEMENTATION_PLAN.md`
- `TASK_STATUS.md`

Required Behavior:

- benchmark 提供 Feynman 参考配置入口，默认参数至少包含：
  - `train_num=2000`
  - `test_num=1000`
  - `lamb=1e-2`
  - `lr=1e-2`
  - `train_steps=200`
  - `seed=1`（参考调用默认）
  - `feynman_width_mid=5,2`
  - `grid=20`
  - `k=3`
  - `device=cpu`
  - `opt=Adam`
  - `feynman_dataset_select_seed=1`
  - `feynman_split_strategy_seed=1`
- Feynman teacher 训练完成后，执行：
  - `model.prune(...)`（阈值采用参考口径 `1e-2`）
  - 再微调 `100` 步（`lr=1e-3`，`lamb=1e-2`）
  - 微调阶段启用早停：每 `5` 步检查一次训练误差变化
- teacher cache 写入的是“剪枝 + 微调”后的 teacher，并保持 cache key 语义完备。
- benchmark 导出与报告需传递 Feynman 任务元数据（公式名、数据文件名、样本规模、变量数、切分参数、`FeynmanEquations.csv` 对应元信息），并在 `icbr_benchmark_summary.md` 中展示。
- 保持 Stage 12 既有导出与可视化能力不退化。

Implementation Constraints:

- 不改动 ICBR 主算法路径，只改 benchmark teacher 训练与配置层。
- 不破坏非 Feynman 任务默认行为。
- 保持 CPU-first 口径。

Success Criteria:

- 一条参考调用命令可在不额外指定大量参数时落到上述配置。
- Feynman teacher 路径确实执行 prune + refit（含每 5 步检查的早停逻辑，非文档声称）。
- 脚本测试通过，且现有 benchmark 相关测试不回归。

Validation:

- `python -m py_compile scripts/icbr_benchmark.py tests/test_icbr_benchmark_script_smoke.py`
- `pytest tests/test_icbr_benchmark_script_smoke.py`
- `pytest tests/test_icbr_benchmark_smoke.py tests/test_icbr_benchmark_script_smoke.py tests/test_icbr_benchmark_regression_smoke.py`
- 数据就绪后参考调用：
  - `python -m scripts.icbr_benchmark --profile feynman_reference --feynman-root datasets --feynman-variant Feynman_with_units --quiet --no-plots`

Status:

Complete

### Stage 14: Feynman Pilot Run on I.12.1 and I.12.4 (Seeds 1,2)

Goal:

在保持 `feynman_reference` 口径不变的前提下，先对 `I.12.1` 与 `I.12.4` 两个数据集执行小范围实跑（`seeds=1,2`），并验证 teacher 持久缓存命中行为与导出结果完整性。

Target Files:

- `IMPLEMENTATION_PLAN.md`
- `TASK_STATUS.md`
- `outputs/icbr_benchmark_stage14_feynman_i12_pilot/*`（运行产物）

Required Behavior:

- benchmark 运行参数保持与 `feynman_reference` 一致，仅覆盖：
  - `tasks=feynman_I_12_1,feynman_I_12_4`
  - `seeds=1,2`
- 使用持久 teacher cache（`readwrite`），并在结果中保留 cache 命中信息。
- 导出产物至少包含：
  - `icbr_benchmark_rows.csv`
  - `icbr_benchmark_summary.json`
  - `icbr_benchmark_summary.md`

Success Criteria:

- 运行成功完成并产出上述文件。
- 行级结果中可观察 `teacher_cache_hit` / `teacher_cache_status`。
- `summary.md` 能查看两个任务、两个 seed 的结果与公式导出信息。

Validation:

- `python -m scripts.icbr_benchmark --profile feynman_reference --tasks feynman_I_12_1,feynman_I_12_4 --seeds 1,2 --feynman-root datasets --feynman-variant Feynman_with_units --teacher-cache-dir outputs/teacher_cache_feynman_reference --teacher-cache-mode readwrite --output-dir outputs/icbr_benchmark_stage14_feynman_i12_pilot --quiet`
- 人工核对 `outputs/icbr_benchmark_stage14_feynman_i12_pilot/icbr_benchmark_summary.json` 中 `rows` 条数与 cache 字段。

Status:

Complete

### Stage 15: Quality 4-Task Ablation Benchmark and Critique-Evidence Validation

Goal:

在 `quality` 口径下对 `minimal/combo/poly_cubic/trig_interaction` 四任务执行启用 teacher 剪枝的多变体 benchmark，并新增能直接回应三类质疑（shared-tensor 是否仅框架红利、contextual replay 是否真改进局部误选、explicit commit 是否引入偏差）的结构化实证导出。

Target Files:

- `kan/icbr.py`
- `scripts/icbr_benchmark.py`
- `tests/test_icbr_benchmark_smoke.py`
- `tests/test_icbr_benchmark_script_smoke.py`
- `IMPLEMENTATION_PLAN.md`
- `TASK_STATUS.md`

Required Behavior:

- benchmark 支持 `quality` 配置下四任务默认运行，并保持 teacher 剪枝路径启用与可观测。
- benchmark 支持不止 `baseline/icbr` 的多变体运行（至少包含）:
  - `baseline`
  - `icbr_full`（shared + replay + explicit commit）
  - `icbr_no_replay`
  - `icbr_no_shared`
  - `icbr_refit_commit`
- 导出中新增可用于回答三类质疑的证据字段（至少）:
  - Q1（shared-tensor）：`icbr_full` vs `icbr_no_shared` 的候选生成时间与总符号化时间对照
  - Q2（contextual replay）：`icbr_full` vs `icbr_no_replay` 的误差对照 + replay rank inversion 统计
  - Q3（explicit commit）：`icbr_full` vs `icbr_refit_commit` 的误差对照 + commit 参数漂移统计
- 保持原有 baseline vs icbr_full 主导出兼容，不破坏既有 rows/summary/report 字段。

Implementation Constraints:

- 不改动 ICBR 主算法核心语义，只扩展 benchmark 变体与证据导出层。
- 不删除 Stage 9~14 已有字段与文件产物。
- 默认运行口径继续 CPU-first，不引入 CUDA 作为通过条件。

Success Criteria:

- 单次 benchmark 可产出：
  - 原有主导出（rows/task_stats/significance/summary/md）
  - 多变体明细与质疑证据导出（JSON/CSV 至少一种 machine-readable 结构）
- 四任务 `quality` 运行可直接读取三类质疑对应的实证指标。
- 相关 smoke 测试覆盖新增变体参数与导出结构并通过。

Validation:

- `python -m py_compile kan/icbr.py scripts/icbr_benchmark.py tests/test_icbr_benchmark_smoke.py tests/test_icbr_benchmark_script_smoke.py`
- `pytest tests/test_icbr_benchmark_smoke.py tests/test_icbr_benchmark_script_smoke.py`
- `python -m scripts.icbr_benchmark --profile quality --tasks minimal,combo,poly_cubic,trig_interaction --seeds 0,1 --variants baseline,icbr_full,icbr_no_replay,icbr_no_shared,icbr_refit_commit --output-dir outputs/icbr_benchmark_stage15_quality_ablation_4tasks --quiet --no-plots`
- 人工核对 summary 中三类质疑证据字段与变体对照结果是否完整。

Status:

Complete

### Stage 16: Quality 4-Task Ablation 10-Seed Extension Validation

Goal:

将 Stage 15 的四任务多变体质量消融基准从 `2 seeds` 扩展到 `10 seeds`，并完成可复查产物沉淀。

Target Files:

- `scripts/icbr_benchmark.py`
- `IMPLEMENTATION_PLAN.md`
- `TASK_STATUS.md`
- `outputs/icbr_benchmark_stage16_quality_ablation_4tasks_10seeds/*`

Required Behavior:

- 沿用 Stage 15 变体集合（`baseline,icbr_full,icbr_no_replay,icbr_no_shared,icbr_refit_commit`）与四任务集合（`minimal,combo,poly_cubic,trig_interaction`）。
- 将 seeds 扩展为 `0,1,2,3,4,5,6,7,8,9`，并输出完整 summary/rows/variant_rows 证据。
- 运行结果固定沉淀在 `outputs/icbr_benchmark_stage16_quality_ablation_4tasks_10seeds/`。

Implementation Constraints:

- 不改变 ICBR 算法语义；仅做规模扩展验证与结果归档。
- 不回退 Stage 15 已有多变体导出字段与报告结构。

Success Criteria:

- 10-seed 运行完成且产物目录齐全可读。
- summary 中包含四任务、多变体、Q1/Q2/Q3 相关聚合证据。

Validation:

- `python -m scripts.icbr_benchmark --profile quality --tasks minimal,combo,poly_cubic,trig_interaction --seeds 0,1,2,3,4,5,6,7,8,9 --variants baseline,icbr_full,icbr_no_replay,icbr_no_shared,icbr_refit_commit --output-dir outputs/icbr_benchmark_stage16_quality_ablation_4tasks_10seeds --teacher-cache-dir outputs/teacher_cache_stage16_quality_10seeds --teacher-cache-mode readwrite --teacher-cache-version stage16_v1 --quiet`
- 人工核对 `outputs/icbr_benchmark_stage16_quality_ablation_4tasks_10seeds` 目录下 `summary.{json,md}` 与 rows/variant_rows 文件。

Status:

Complete

### Stage 17: Multi-Variant Formula Report Completeness Fix

Goal:

修复 Stage 16 报告可读性缺口：`icbr_benchmark_summary.md` 的 `## Formula Comparison` 必须覆盖当前运行启用的全部 benchmark variants，而不仅是 `baseline` 与 `icbr_full`。

Target Files:

- `scripts/icbr_benchmark.py`
- `tests/test_icbr_benchmark_script_smoke.py`
- `IMPLEMENTATION_PLAN.md`
- `TASK_STATUS.md`

Required Behavior:

- `Formula Comparison` 按 `config.variants` 展示每个 `task+seed` 的全部变体：
  - 变体级概要（`symbolic_wall_time_s / mse / target_mse / formula_ok`）
  - `display` 公式列表
  - `raw` 公式列表
  - 变体级 `formula_error`（如有）
- 当 teacher gate 导致符号化跳过时，变体项要保持显式可读（例如 `<none>` 与跳过原因），不得静默缺失。
- 不破坏既有 CSV/JSON 结构与 baseline/icbr_full 主指标兼容。

Implementation Constraints:

- 不改动 ICBR 算法路径，仅修复报告层渲染逻辑与测试覆盖。
- 保持 Stage 16 的变体与证据导出结构不回退。

Success Criteria:

- 运行含 `icbr_no_replay/icbr_no_shared/icbr_refit_commit` 的 benchmark 后，`summary.md` 中可直接看到这些变体的公式与状态。
- smoke 测试覆盖“非 baseline/icbr_full 变体出现在 Formula Comparison”并通过。

Validation:

- `python -m py_compile scripts/icbr_benchmark.py tests/test_icbr_benchmark_script_smoke.py`
- `pytest tests/test_icbr_benchmark_script_smoke.py -k "variants or generates_outputs or formula_comparison"`

Status:

Not Started

### Stage 18: Visualization Upgrade for Stage 16 10-Seed Outputs

Goal:

针对 `outputs/icbr_benchmark_stage16_quality_ablation_4tasks_10seeds` 已完成实跑结果，补齐当前“画图不够完善”的问题，提升报告可读性与变体对照清晰度。

Target Files:

- `scripts/icbr_benchmark.py`
- `tests/test_icbr_benchmark_script_smoke.py`
- `IMPLEMENTATION_PLAN.md`
- `TASK_STATUS.md`

Required Behavior:

- 在保留现有 3 张图的基础上，新增至少以下可读图：
  - 变体级总览图（`baseline/icbr_full/icbr_no_replay/icbr_no_shared/icbr_refit_commit` 的 symbolic time 与 mse/target_mse 对照）
  - Q1/Q2/Q3 证据图（按 task 聚合展示）
- 新图必须写入 `summary.json -> artifacts.visualizations.files`，并在 `summary.md` 的可视化摘要中列出。
- 图表标题与坐标轴必须明确“指标定义与方向性”（例如 gain>0 表示哪种方法更优）。

Implementation Constraints:

- 不改 ICBR 算法路径，仅增强 benchmark 报告层可视化。
- 不删除既有图与既有产物路径，保持向后兼容。

Success Criteria:

- 基于 Stage 16 10-seed 运行参数再次生成报告时，可得到更完整的变体对照图与证据图。
- smoke 测试覆盖新增图产物存在性并通过。

Validation:

- `python -m py_compile scripts/icbr_benchmark.py tests/test_icbr_benchmark_script_smoke.py`
- `pytest tests/test_icbr_benchmark_script_smoke.py -k visual`
- `pytest tests/test_icbr_benchmark_script_smoke.py -k "variants or generates_outputs or formula_comparison"`
- `python -m scripts.icbr_benchmark --profile quality --tasks minimal,combo,poly_cubic,trig_interaction --seeds 0,1,2,3,4,5,6,7,8,9 --variants baseline,icbr_full,icbr_no_replay,icbr_no_shared,icbr_refit_commit --output-dir outputs/icbr_benchmark_stage16_quality_ablation_4tasks_10seeds --teacher-cache-dir outputs/teacher_cache_stage16_quality_10seeds --teacher-cache-mode readwrite --teacher-cache-version stage16_v1 --quiet`

Status:

Complete

## 5. Acceptance Criteria

Phase I 仅在以下条件全部满足时视为完成:

- `auto_symbolic_icbr(...)` 可运行
- 实现范围仍然只包含两个核心改进点
- 第一版只按 CPU 路线验收
- 不以 CUDA 加速作为 Phase I 验收条件
- 候选生成是无状态的
- replay evaluator 是无副作用的
- commit helper 能维护完整 symbolic state 一致性
- 最终达到 fully symbolic completion
- `symbolic_formula()` 导出正确
- 至少具备:
  - 最小单元测试
  - replay 无副作用测试
  - exporter correctness 检查
  - candidate generation wall time benchmark
  - replay rerank wall time benchmark

## 6. Execution Order

推荐执行顺序固定为:

1. Stage 1: Add CPU Batched Candidate Evaluation
2. Stage 2: Add Safe Replay Evaluator
3. Stage 3: Add Explicit Commit Helper
4. Stage 4: Add `auto_symbolic_icbr(...)` Entry
5. Stage 5: Benchmark and Verify Phase I Claims
6. Stage 6: Extended Multi-Seed Benchmark Validation
7. Stage 7: Regression Gating and Stability Verification
8. Stage 8: Diagnose and Fix `trig_interaction` Regression
9. Stage 9: Add Teacher Quality Gate and Target-Error Metrics
10. Stage 10: Calibrate Teacher Convergence and Run 10-Seed Full-Task Verification
11. Stage 11: Add Cross-Run Persistent Teacher Cache
12. Stage 12: Add Feynman Dataset Support to `icbr_benchmark.py`
13. Stage 13: Add Feynman Reference Preset and Prune-Refit Teacher Flow
14. Stage 14: Feynman Pilot Run on I.12.1 and I.12.4 (Seeds 1,2)
15. Stage 15: Quality 4-Task Ablation Benchmark and Critique-Evidence Validation
16. Stage 16: Quality 4-Task Ablation 10-Seed Extension Validation
17. Stage 17: Multi-Variant Formula Report Completeness Fix
18. Stage 18: Visualization Upgrade for Stage 16 10-Seed Outputs
