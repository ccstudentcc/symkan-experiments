# TASK_STATUS

## Date
2026-03-31

## Task
推进 Stage 23：按既定口径整理 benchmark 符号拟合的内存生命周期，明确 baseline / 各 ICBR 变体 / 公式导出阶段的对象作用域与运行期缓存清理边界，避免前一阶段的状态或大张量残留影响后一阶段。

## Current Stage
Stage 23: Enforce Benchmark Symbolic-Fitting Memory Lifecycle

## Status
Complete

## Latest Completed Work
- `scripts/icbr_benchmark.py`：
  - 修正 `_infer_teacher_model_width_from_state()` 对 pruning 后 multiplication-aware hidden layer 的宽度反推公式
  - 旧逻辑误把 `num_mult = subnode_width - node_width` 直接代回校验，导致如 `feynman_I_9_18` 这类缓存中的 `(node_width, subnode_width) = (3, 4)` 在 `symbolic-only` 下被错误判定为不兼容
  - 新逻辑按 `delta = subnode_width - node_width = (mult_arity - 1) * num_mult` 反推，因此 `mult_arity=2` 时能正确恢复为 `[num_sum, num_mult] = [2, 1]`
- `tests/test_icbr_benchmark_script_smoke.py`：
  - 新增 pruned multiplication-aware teacher cache 的宽度反推回归测试，防止 `symbolic-only` 载入旧缓存时再次回归
- `kan/icbr.py`：
  - 新增 `_clear_model_runtime_caches()`，统一清理 `acts / spline_postacts / spline_postsplines / acts_scale / symbolic_acts` 等运行期大对象
  - `benchmark_symbolic_variants()` 重构为更清晰的生命周期：
    - 只保留一份跨 baseline/variants 共享的 `teacher_output`
    - baseline 通过 `_run_baseline_symbolic_benchmark()` 独立 clone、独立运行、独立公式导出，结束后立即清理运行期缓存
    - 每个 ICBR 变体通过 `_run_variant_symbolic_benchmark()` 独立 clone 出 `teacher_model/work_model`，只在当前变体作用域内存活，结束后立即清理运行期缓存
  - teacher numeric、baseline、variant 三段路径现在都通过统一 helper 明确释放运行期缓存，而不再依赖零散 `del`
- `scripts/icbr_benchmark.py`：
  - `symbolic-only` 下不再重算 `teacher_test_mse` / `teacher_test_r2`
  - `symbolic-only` rows 中显式记录：
    - `teacher_test_mse = NaN`
    - `teacher_test_r2 = NaN`
    - `teacher_quality_gate_reason = skipped_in_symbolic_only_cached_teacher`
- `tests/test_icbr_integration.py`：
  - 新增运行期缓存清理回归，验证 `_clear_model_runtime_caches()` 会清空前向与公式导出的缓存对象
- `tests/test_icbr_benchmark_script_smoke.py`：
  - 新增 `symbolic-only` 回归，验证该模式不再重算 teacher 指标，而是直接使用缓存教师进入符号拟合
- 文档边界已更新：
  - `IMPLEMENTATION_PLAN.md` 新增 Stage 22 与 Stage 23
  - Stage 22 固定只做两项：
    - 只对活跃 edge 生成候选
    - per-edge 固定容量 top-k shortlist 聚合
  - Stage 23 固定承接 benchmark 符号拟合阶段的内存生命周期整理
- `kan/icbr.py`：
  - 新增 `_candidate_rank_key()` 与 `_update_edge_topk_shortlist()`，将 per-edge shortlist 改为固定容量 `top-k` 聚合，避免按函数保留全量候选列表
  - 新增 `_is_edge_active_for_symbolic()` 与 `_collect_active_edges_for_layer()`，统一 active edge 判定口径
  - `_build_layer_shortlists_shared()` 改为按函数流式处理候选，并对每条 edge 实时维护 top-k
  - `_build_edge_shortlist()` 同步改为固定容量 top-k 聚合，shared / serial 两条候选路径排序语义保持一致
  - `_run_auto_symbolic_icbr_with_models()` 的 shared 候选生成显式只对 active edges 构建 shortlist
- `scripts/icbr_benchmark.py`：
  - 新增 width token 归一化逻辑，支持显式 multiplication-aware layer spec，例如 `[5,2]`
  - 保留旧式纯整数写法兼容：`5,3` 仍按 `width=[n_var,5,3,1]` 解析
  - Feynman width 构造改为允许原样插入 multiplication-aware layer，因此 `[5,2]` 会生成 `width=[n_var,[5,2],1]`
  - `run_benchmark()` 的默认 `feynman_width_mid` 改为 `[[5,2]]` 内部表达，summary/config 对外展示为 `[5,2]`
  - CLI `--feynman-width-mid` 默认值改为 `"[5,2]"`，帮助文本同步说明三类用法：
    - `[5,2]`
    - `5,3`
    - `[[5,2],3]`
  - Feynman teacher 默认口径已对齐为：
    - `fit_opt=Adam`
    - `post_prune_steps=100`
    - `post_prune_lr=1e-3`
    - `post_prune_lamb=1e-3`
    - `post_prune_eval_every=5`
    - `post_prune_min_delta=1e-6`
    - `post_prune_patience=3`
    - `teacher_max_test_mse=0.1`
    - `teacher_min_test_r2=None`（默认不要求）
  - teacher quality gate 现在支持“阈值为空即不检查该指标”，用于 Feynman 默认不要求 `R2`
  - Feynman 路径的随机性进一步对齐到当前 benchmark `seed`：
    - teacher 初始化显式使用当前 `seed`
    - 未显式传 `--feynman-split-strategy-seed` 时，`random` split 自动使用当前 `seed`
    - row / cache 语义中记录实际生效的 `feynman_split_seed`
  - 新增 `--prune-iters` / `run_benchmark(prune_iters=...)`
    - `prune + refit` 记作一轮
    - Feynman 任务 / `feynman_reference` 默认值 `3`
    - 非 Feynman 任务默认值保持 `1`
    - 适用于 synthetic / Feynman teacher prune 路径
  - teacher cache key、summary config、markdown run config 已纳入 `prune_iters`
  - 图表格式补充：
    - `speedup_boxplot` 改为 ratio 值的 log 轴，y 轴标签为 `Speedup Ratio (×)`，基准线为 `1x`
    - `q123_evidence_by_task` 从 `log2(ratio)` 改为 ratio 值本身，使用 log 轴与 `1x` 基准线，并以几何均值 + 95% CI 汇总
    - `variant_overview` 的时间列 y 轴标签改为 `Symbolic Wall Time (s)`，不再把 `log scale` 写进标签文本
    - `mse_shift_boxplot` 的 y 轴标签改为 `ICBR MSE - Baseline MSE`，scale 仅由坐标轴表达
    - log 轴 formatter 固定为数学形式刻度，避免被 scientific formatter 回写覆盖
  - Stage 21 补充修正：
    - `symbolic_time_errorbar` / `speedup_boxplot` / `mse_shift_boxplot` 在对数尺度时统一显示标题左侧 `scale=log`
    - `symbolic_time_errorbar` 的 y 轴标签固定为 `Symbolic Wall Time (s)`，不再把 scale 写进标签
    - `q123_evidence_by_task` 的三个 y 轴标签拆成两行，括号部分放到第二行，避免与面板内容重叠
    - ratio 刻度去掉重复的 `×` 后缀，并优先显示普通数值，例如 `10` 而不是 `1e1`
    - `speedup_boxplot` 的 ratio 轴边界改为收紧到已有数据附近，避免基准线下方留下大段空白
- `tests/test_icbr_benchmark_script_smoke.py`：
  - 新增 `_parse_width_mid()` 单元测试，覆盖 multiplication-aware 与兼容写法
  - 新增 teacher quality gate 关闭 `R2` 约束的单元测试
  - Feynman dataset smoke 改为显式传入 `--feynman-width-mid [5,2]`
  - 断言 summary/config 的 `width_mid` 为 `[5,2]`
  - 断言行级 `width` 的中间层保留 `[5,2]`
  - 新增省略 `feynman_width_mid` 时默认落到 `[5,2]`，并同时断言 Feynman 默认 teacher 配置与 gate 阈值
  - 新增 `prune_iters` 透传到 synthetic teacher 配置的 smoke test
  - 更新可视化 metadata 断言，覆盖：
    - `speedup` 使用 `log` scale + `Speedup Ratio (×)`
    - `variant_overview` 标签不再写 scale
    - `q123` 使用 ratio 值而不是 `log2_ratio`
    - `symbolic_time_errorbar` 改回纯单位标签，并为对数图记录 `scale_label_placement`
    - `q123` 的面板标签改为两行格式
- `IMPLEMENTATION_PLAN.md`：
  - 新增 Stage 21，记录需求、约束、成功标准与验证命令

## Files Changed
- IMPLEMENTATION_PLAN.md
- TASK_STATUS.md
- kan/icbr.py
- scripts/icbr_benchmark.py
- tests/test_icbr_benchmark_script_smoke.py
- tests/test_icbr_integration.py

## Validation Run
- `C:\Users\chenpeng\miniconda3\envs\kan\python.exe -m py_compile scripts\icbr_benchmark.py tests\test_icbr_benchmark_script_smoke.py`
- `C:\Users\chenpeng\miniconda3\envs\kan\python.exe -m pytest tests\test_icbr_benchmark_script_smoke.py -k "feynman_symbolic_only or symbolic_only or teacher_cache or infer_teacher_model_width"`
- `C:\Users\chenpeng\miniconda3\envs\kan\python.exe -m py_compile kan\icbr.py tests\test_icbr_integration.py tests\test_icbr_benchmark_smoke.py tests\test_icbr_benchmark_script_smoke.py scripts\icbr_benchmark.py`
- `C:\Users\chenpeng\miniconda3\envs\kan\python.exe -m pytest tests\test_icbr_integration.py tests\test_icbr_benchmark_smoke.py tests\test_icbr_benchmark_script_smoke.py`
- `C:\Users\chenpeng\miniconda3\envs\kan\python.exe -m py_compile kan\icbr.py tests\test_icbr_integration.py tests\test_icbr_benchmark_smoke.py`
- `C:\Users\chenpeng\miniconda3\envs\kan\python.exe -m pytest tests\test_icbr_integration.py tests\test_icbr_benchmark_smoke.py`

## Validation Result
- `py_compile`（本次 follow-up 修复）通过。
- `pytest tests\test_icbr_benchmark_script_smoke.py -k "feynman_symbolic_only or symbolic_only or teacher_cache or infer_teacher_model_width"` 通过：`5 passed`。
- 已验证：
  - pruning 后的 multiplication-aware teacher cache 能正确恢复隐藏层宽度
  - `symbolic-only` 仍能复用已有 Feynman teacher cache，且不会放宽“缓存 miss 直接报错停止”的约束
- `py_compile`（Stage 23 相关 Python 文件）通过。
- `pytest tests\test_icbr_integration.py tests\test_icbr_benchmark_smoke.py tests\test_icbr_benchmark_script_smoke.py` 通过：`33 passed`。
- 已验证：
  - benchmark baseline / variant 路径的运行期缓存清理逻辑不破坏既有 benchmark 结果结构
  - `symbolic-only` 下 teacher 指标不再重算
  - Feynman / run-mode / benchmark smoke 全部未回归
- `py_compile` 通过。
- `pytest tests\test_icbr_integration.py tests\test_icbr_benchmark_smoke.py` 通过：`8 passed`。
- 已验证：
  - shared 候选生成只会对 active edges 构建候选
  - per-edge shortlist 现在保持固定容量 `top-k`，并保留原有 `r2 desc + complexity asc` 排序语义
  - benchmark smoke 与既有 ICBR integration 行为未回归

## Decisions
- `feynman_width_mid` 对外仍保留“中间层配置”概念，但内部区分：
  - 单个 multiplication-aware layer：`[5,2]`
  - 多个纯整数 hidden layers：`5,3`
  - 混合/多层显式写法：`[[5,2],3]`
- summary/config 在只有一个中间层时展示单层值，而不是额外包一层列表，便于与用户口径对齐
- Feynman 默认 teacher gate 采用“只约束 MSE，不约束 R2”的策略；实现上使用 `teacher_min_test_r2=None`
- `prune_iters` 不区分数据集类型；是否实际生效仍由 `teacher_post_train_prune` 控制
- Stage 22 范围固定为候选生成层优化，不提前混入 replay 门控、两阶段搜索或完整 benchmark 生命周期重构。
- Stage 23 预留给 benchmark 符号拟合阶段的内存生命周期整理，包含 baseline/variant 作用域隔离、teacher_output 共享边界与公式导出后立即释放。
- Stage 23 实现按“作用域清晰 + 统一缓存清理 helper”推进，不继续堆叠零散 `del` 作为主要生命周期管理手段。

## Remaining Work
- 无

## Blockers
- 无
