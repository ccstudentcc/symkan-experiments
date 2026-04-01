# ICBR Integration Specification

## 1. 目标

本规格定义 `symkan` 当前工程版中 ICBR 接入后的正式行为边界。目标不是引入新的训练器，而是在保持 baseline 默认行为不变的前提下，为符号拟合阶段增加一个可显式选择的 `icbr` 后端，并保证任一单个 baseline-backend vs icbr-backend compare 只反映符号拟合差异。

## 2. 范围

### 2.1 In Scope

- `SymbolizeConfig` 支持 `symbolic_backend`，默认值为 `baseline`。
- `scripts.symkanbenchmark` 支持通过 YAML 或 CLI 显式切换 `symbolic_backend`。
- `symkan.symbolic.pipeline` 显式拆分为共享 symbolic-prep 与 backend-specific completion 两段。
- `scripts.benchmark_ab_compare` 在单个 baseline-backend vs icbr-backend compare 时，生成专用 compare 产物。

### 2.2 Out of Scope

- 不修改数值训练算法。
- 不修改 `stagewise_train` 的目标与训练语义。
- 不把 ICBR 扩展为新的通用 symbolic regression 系统。
- 不改变现有 generic compare workflow 的默认输出集合。

## 3. 行为约束

### 3.1 默认行为

1. 若未显式指定 `symbolic_backend`，系统必须使用 baseline 符号拟合后端。
2. 现有 notebook、CLI 和库层入口 `symbolize_pipeline(...)` 的调用方式必须保持兼容。
3. `baseline.yaml` 仍是当前默认 A/B 基准口径；`baseline_icbr.yaml` 与 `baseline_icbr_fastlib.yaml` 仅在符号后端或符号函数库相关设置上偏离对应 baseline 变体。

### 3.2 Shared-State Fairness

对 `baseline` 与 `baseline_icbr` 的公平比较必须满足以下条件：

1. 数值训练阶段完全一致。
2. shared symbolic-prep 阶段完全一致。
3. `symbolize_trace.csv` 的节奏语义一致。
4. backend 差异只能从 backend-specific symbolic completion 开始出现。

该约束意味着：

- numeric cache key 必须排除 `symbolize` 配置，使 backend-only 变体共享同一数值模型。
- symbolic-prep cache key 必须绑定 numeric cache identity 与剪枝/输入压缩/pre-symbolic fit 相关设置，但不得被 backend-only 设置污染。
- symbolization-only 指标不得把共享训练和共享 symbolic-prep 的参考时间记成当前 run 的实时成本。
- 若只想扩大函数库但继续复用 numeric cache，应把库覆盖编码在 `symbolize.lib` / `symbolize.lib_hidden` / `symbolize.lib_output`，而不是修改非 `symbolize` section。

### 3.3 Metric Hygiene

以下指标属于当前比较口径的一部分：

- 通用指标：
  - `final_acc`
  - `macro_auc`
  - `final_n_edge`
  - `symbolic_core_seconds`
  - `symbolize_wall_time_s`
  - `run_total_wall_time_s`
- 共享阶段与缓存指标：
  - `numeric_cache_hit`
  - `symbolic_prep_cache_hit`
  - `cached_stage_total_seconds_ref`
  - `cached_symbolic_prep_seconds_ref`
- baseline/icbr 专用指标：
  - `final_teacher_imitation_mse`
  - `final_target_mse`
  - `final_target_r2`
  - `icbr_candidate_generation_wall_time_s`
  - `icbr_replay_rerank_wall_time_s`
  - `icbr_replay_rank_inversion_rate`

解释要求：

1. `symbolic_core_seconds` 是 baseline vs ICBR 的主速度指标。
2. `symbolize_wall_time_s` 仍可用于总体墙钟比较，但不得替代 core metric。
3. `cached_*_ref` 仅是参考时长，不属于当前 run 的实时阶段耗时。

### 3.4 Compare Output Contract

`scripts.benchmark_ab_compare` 必须满足两层输出契约：

1. Generic compare 始终生成：
   - `variant_summary.csv`
   - `pairwise_delta_summary.csv`
   - `seedwise_delta.csv`
   - `trace_seedwise.csv`
   - `trace_summary.csv`
   - `comparison_summary.md`
2. 当且仅当比较对为单个 baseline-backend vs 单个 icbr-backend pair 且关键字段齐全时，额外生成：
   - `baseline_icbr_shared_check.csv`
   - `baseline_icbr_primary_effect.csv`
   - `baseline_icbr_mechanism_summary.csv`

其中：

- `baseline_icbr_shared_check.csv` 用于验证 shared numeric、trace 与 shared symbolic-prep 是否对齐。
- `baseline_icbr_primary_effect.csv` 用于报告 ICBR 的主效应。
- `baseline_icbr_mechanism_summary.csv` 用于拆解 ICBR 内部时间占比与 replay 行为。

## 4. 结果解释边界

当前工程版允许得出的结论边界如下：

1. ICBR 改动的是符号拟合后端，不是数值训练。
2. 若 `shared_numeric_aligned=True`、`trace_aligned=True`、`shared_symbolic_prep_aligned=True`，则可将比较解释为“同一数值 KAN、同一 shared symbolic-prep 边界下的 backend-only 对比”。
3. `formula_export_success_rate=1.0` 仅表示导出链路成功，不等价于恢复了真实闭式公式。
4. 当前 `n=3` seeds 的结果具备工程判断意义，但不应表述为充分统计显著性结论。

## 5. 2026-04-01 验收切片

本规格当前对应两组可引用验收产物目录：

- `outputs/rerun_v2_engine_safe_20260401/benchmark_ab/baseline/`
- `outputs/rerun_v2_engine_safe_20260401/benchmark_ab/baseline_icbr/`
- `outputs/rerun_v2_engine_safe_20260401/benchmark_ab/comparison/`
- `outputs/rerun_v2_engine_safe_20260401/benchmark_ab/baseline_fastlib/`
- `outputs/rerun_v2_engine_safe_20260401/benchmark_ab/baseline_icbr_fastlib/`
- `outputs/rerun_v2_engine_safe_20260401/benchmark_ab/comparison_fastlib/`
- `outputs/rerun_v2_engine_safe_20260401/benchmark_ab/baseline_icbr_fulllib/`

### 5.1 Layered 库对照

当前已完成的 layered 库验收事实如下：

1. `baseline_icbr_shared_check.csv` 对 `42/52/62` 三个 seed 均报告：
   - `shared_numeric_aligned=True`
   - `trace_aligned=True`
   - `shared_symbolic_prep_aligned=True`
2. `baseline` 与 `baseline_icbr` 的 `final_n_edge` 均值一致，说明 ICBR 不再恢复已剪掉的边。
3. `baseline_icbr_primary_effect.csv` 报告：
   - `symbolic_core_speedup_vs_baseline` 均值约 `1.751763`
   - `final_teacher_imitation_mse_shift < 0`
   - `final_target_mse_shift < 0`
   - `final_target_r2_shift > 0`
4. `baseline_icbr_mechanism_summary.csv` 与 markdown summary 已生成；其中 candidate generation 占核心时间约 `1.7539%`，replay rerank 占比约 `97.6469%`。
5. baseline 与 icbr 两侧公式导出成功率当前均为 `1.0`。

### 5.2 FAST_LIB 对照

当前已完成的 FAST_LIB 验收事实如下：

1. `comparison_fastlib/baseline_icbr_shared_check.csv` 对 `42/52/62` 三个 seed 均报告：
   - `shared_numeric_aligned=True`
   - `trace_aligned=True`
   - `shared_symbolic_prep_aligned=True`
2. `baseline_fastlib` 与 `baseline_icbr_fastlib` 的 `numeric_cache_hit=True`、`symbolic_prep_cache_hit=True`，说明本轮库扩展仍复用了既有 numeric/shared-prep 缓存。
3. `comparison_fastlib/variant_summary.csv` 报告两侧 `final_n_edge` 均值同为 `88.333333`。
4. `comparison_fastlib/baseline_icbr_primary_effect.csv` 报告：
   - `symbolic_core_speedup_vs_baseline` 均值约 `2.350452`
   - `final_target_mse_shift < 0`
   - `final_target_r2_shift > 0`
5. `comparison_fastlib/baseline_icbr_mechanism_summary.csv` 报告 candidate generation 占核心时间约 `3.5573%`，replay rerank 占比约 `96.0892%`。

### 5.3 Full symbolic library 的补充单变体切片

当前还存在一组补充结果：

- `outputs/rerun_v2_engine_safe_20260401/benchmark_ab/baseline_icbr_fulllib/`

其解释边界如下：

1. `baseline_fulllib` 本轮未跑，原因是 full symbolic library 下 baseline 路径过慢。
2. 因此 `baseline_icbr_fulllib/` 不是 paired backend-only compare 证据，也不受第 3.2 节 shared-state fairness 合同的 paired compare 解释保护。
3. 该切片仅用于补充说明：ICBR 在 full symbolic library 下仍可运行，并带来单边收益。
4. 当前单边均值约为：
   - `final_acc = 0.795433`
   - `macro_auc = 0.963225`
   - `final_target_r2 = 0.601003`
   - `symbolic_core_seconds = 35.218785`

## 6. 失效条件

若出现以下任一情形，应视为当前规格失效并重新审查实现与文档：

1. `baseline` 与 `baseline_icbr` 的 shared numeric 或 trace 不再对齐。
2. backend-only rerun 重新触发数值训练或 shared symbolic-prep。
3. ICBR 重新计入已剪除边，或把零占位边计入有效复杂度。
4. generic compare 被 baseline/icbr 专用逻辑污染。

## 7. 关联文档

1. [ARCHITECTURE.md](ARCHITECTURE.md)
2. [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md)
3. [TASK_STATUS.md](TASK_STATUS.md)
4. [docs/design.md](docs/design.md)
5. [docs/symkanbenchmark_usage.md](docs/symkanbenchmark_usage.md)
6. [docs/engineering_rerun_report.md](docs/engineering_rerun_report.md)
