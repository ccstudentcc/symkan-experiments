# symkanbenchmark.py 使用说明

## 文档导航

- 返回总览：[README](../README.md)
- docs 总入口：[index](index.md)
- 项目地图：[project_map](project_map.md)
- 总体使用文档：[symkan_usage](symkan_usage.md)
- 设计与兼容策略：[design](design.md)
- 参数解释（notebook 侧）：[kan_parameters](kan_parameters.md)
- 消融实验说明：[ablation_usage](ablation_usage.md)

## 目录

- [1. 运行入口](#1-运行入口)
- [2. 任务与命令速查](#2-任务与命令速查)
- [3. 输出目录与文件含义](#3-输出目录与文件含义)
- [4. 参数速查](#4-参数速查)
- [5. 结果解读最小集合](#5-结果解读最小集合)
- [6. A/B Experiments And Backend Compare](#6-ab-experiments-and-backend-compare)
- [7. 报告口径](#7-报告口径)
- [8. 与总文档统一口径（2026-03）](#8-与总文档统一口径2026-03)

[symkanbenchmark.py](../symkanbenchmark.py) 将 [../notebooks/kan.ipynb](../notebooks/kan.ipynb) 中的主实验流程及两个 benchmark 流程脚本化，其主要目的包括：

1. 支持同一参数集的批量多 seed 运行。
2. 稳定导出结构化 CSV 结果。
3. 避免 notebook 手工执行带来的覆盖和漏记。

## 1. 运行入口

参考环境（用于结果解释）：

1. 操作系统：Windows 11 专业版 `23H2`（OS Build `22631.5472`）。
2. Python：`Miniconda` 的 `kan` 环境，解释器路径 `C:\Users\chenpeng\miniconda3\envs\kan\python.exe`（`3.9.25`）。
3. CPU：`12th Gen Intel(R) Core(TM) i5-12500H`。
4. 内存：`16 GB`。
5. 深度学习运行时：`PyTorch 2.1.2+cpu`（CPU 路径）。

### 1.1 完整流程

```powershell
# 运行目录：仓库根目录（symkan-experiments/）
python -m scripts.symkanbenchmark --tasks all --verbose
```

其中，`all = full + eval-bench + parallel-bench`。

脚本默认优先读取 `data/X_train.npy`、`data/X_test.npy`、`data/Y_train_cat.npy`、`data/Y_test_cat.npy`（兼容旧版根目录 `X_train.npy`、`X_test.npy`、`Y_train_cat.npy`、`Y_test_cat.npy`）。若文件缺失且启用了 `data.auto_fetch_mnist`，脚本默认只会在仓库 `data/` 下补齐缺失文件；若配置把目标路径指向 `data/` 之外，需显式设置 `data.allow_auto_fetch_outside_data_dir: true`。自动下载优先使用 `tensorflow.keras.datasets.mnist`，失败时会先发出 warning，再回退到 `sklearn.fetch_openml`。

## 配置管理建议

`symkanbenchmark.py` 现支持通过 `--config` 加载 YAML 运行配置，例如：

```powershell
# 运行目录：仓库根目录（symkan-experiments/）
python -m scripts.symkanbenchmark --config configs/symkanbenchmark.default.yaml --quiet
```

若未显式传入 `--config`，脚本当前会默认读取：

```powershell
# 运行目录：仓库根目录（symkan-experiments/）
configs/symkanbenchmark.default.yaml
```

约定如下：

- `AppConfig` YAML 管算法运行逻辑：训练参数、设备、数据路径、符号化策略等。
- 环境变量管敏感项或环境差异：支持 `${ENV_VAR}` 和 `${ENV_VAR:-default}`，且只会在 YAML 解析后的标量字符串上展开，避免把环境变量内容当成新的配置结构。
- CSV 管输入数据与结果产物：例如 `symkanbenchmark_runs.csv`、`kan_stage_logs.csv`、`kan_symbolic_summary.csv`。

命令行参数不再由 `load_config()` 自动合并进配置对象；脚本会先 `load_config()` 得到 `AppConfig`，再仅对白名单字段做显式且重新校验的覆盖。当前覆盖点分布在 `runtime / library / workflow / evaluation / symbolize` 五段，因此适合“固定主配置 + 少量局部覆盖”的工作流。

## 配置分层原则

当前项目采用三层口径：

1. notebook / Python 调用：直接构造 `AppConfig` 并传给核心函数。
2. CLI：先 `load_config()` 得到 `AppConfig`，再做一小组显式白名单覆盖。
3. 核心编排：统一只认 `AppConfig`，而不是 `argparse.Namespace` 或脚本私有配置模型。

`symkanbenchmark.py` 现在直接把 `AppConfig` 传给 `stagewise_train` / `symbolize_pipeline`。也就是说，YAML、CLI 和 notebook 最终都收敛到同一份库层配置对象。

还需注意一层运行期注入：

- `stagewise.width`、`stagewise.grid`、`stagewise.k`、`stagewise.seed`、`stagewise.batch_size`
- `stagewise.validation_seed` 若在 YAML 中留空，则运行时继承 `runtime.global_seed`
- `symbolize.batch_size`
- `symbolize.layerwise_validation_seed` 若在 YAML 中留空，则运行时继承 `runtime.global_seed`
- 当 `symbolize.lib / lib_hidden / lib_output` 都未显式指定时，由 `library.lib_preset` 派生对应函数库

这些字段由脚本在运行时基于数据形状、seed、batch size 和函数库预设补入，不要求在 YAML 中手工硬编码。

### 1.2 主实验

```powershell
# 运行目录：仓库根目录（symkan-experiments/）
python -m scripts.symkanbenchmark --tasks full
```

静默模式：

```powershell
# 运行目录：仓库根目录（symkan-experiments/）
python -m scripts.symkanbenchmark --tasks full --quiet
```

`--quiet` 用于抑制训练与符号化过程输出；若与 `--verbose` 同时设置，则 `--quiet` 优先。

说明：

- 当前脚本把算法参数统一收敛到 `AppConfig` YAML。
- CLI 主要保留任务调度、输出目录、seed 列表和一小组显式白名单覆盖。
- 更细的训练/剪枝/符号化参数，推荐直接修改 `configs/symkanbenchmark.default.yaml` 或你自己的 `AppConfig` 文件。

### 1.3 多 seed 运行

```powershell
# 运行目录：仓库根目录（symkan-experiments/）
python -m scripts.symkanbenchmark --tasks all --stagewise-seeds 42,52,62
```

## 2. 任务与命令速查

- 主实验：

```powershell
# 运行目录：仓库根目录（symkan-experiments/）
python -m scripts.symkanbenchmark --tasks full
```

- 评估链路 benchmark（仍会先构造主流程上下文）：

```powershell
# 运行目录：仓库根目录（symkan-experiments/）
python -m scripts.symkanbenchmark --tasks eval-bench
```

- 并行策略 benchmark：

```powershell
# 运行目录：仓库根目录（symkan-experiments/）
python -m scripts.symkanbenchmark --tasks parallel-bench --parallel-modes auto,off,thread4,thread8
```

说明：当前 `parallel-bench` 仍是 correctness-first 的 requested-mode 对照。脚本会保留 `auto/off/threadN` 这些请求标签做横向记录，但 `suggest_symbolic` 的实际 worker 数会保守回落到 1；可在输出列 `parallel_workers_effective` 中确认。

- 组合任务：

```powershell
# 运行目录：仓库根目录（symkan-experiments/）
python -m scripts.symkanbenchmark --tasks full,parallel-bench
```

## 3. 输出目录与文件含义

默认输出目录为 `outputs/benchmark_runs/`。每个 seed 对应一个独立的 run 子目录，以避免结果覆盖：

```plaintext
outputs/benchmark_runs/
  symkanbenchmark_runs.csv
  symkanbenchmark_eval_runs.csv
  symkanbenchmark_parallel_runs.csv
  run_01_seed42/
    kan_stage_logs.csv
    kan_symbolic_summary.csv
    formula_validation.csv
    roc_auc_summary.csv
    symbolize_trace.csv
    metrics.json
    benchmark_single_round.csv
    benchmark_multi_round_raw.csv
    benchmark_multi_round_summary_cn.csv
    benchmark_multi_round_summary_en.csv
    benchmark_symbolic_parallel_quick.csv
```

主要结果文件包括：

1. `symkanbenchmark_runs.csv`：多 seed/多配置横向对比主表。
2. `kan_stage_logs.csv`：阶段训练是否频繁回滚。
3. `symbolize_trace.csv`：剪枝节奏是否过猛。
4. `formula_validation.csv`：R² 与数值稳定性。
5. `benchmark_symbolic_parallel_quick.csv`：requested mode 标签与实际 `parallel_workers_effective` 的对照结果。

## 4. 参数速查

### 4.1 主实验参数来源

当前实现中，大多数算法参数不再作为长 CLI 直接暴露，而是来自 `AppConfig` YAML，例如：

- `model.inner_dim`
- `stagewise.target_edges`
- `stagewise.steps_per_stage`
- `symbolize.target_edges`
- `symbolize.layerwise_finetune_steps`
- `symbolize.affine_finetune_steps`
- `model.numeric_basis`（`bspline` 或 `radial_bf`）

口径说明如下：

1. 算法参数的正式默认值以 `AppConfig` 模型和示例 YAML 为准。
2. CLI 主要承担任务调度和一小组显式白名单覆盖，不再承载整套研究参数。
3. 对典型 2 层 KAN（`[in, hidden, class]`），项目层设定通常仍将 `layerwise_finetune_steps` 视为按需开关。

逐层符号化属于有损替换；`fix_symbolic` 选定函数族后无法回退。在 2 层 KAN 中，LayerwiseFT 仅有一次层间补偿窗口，因此其改进版更接近风险控制选项，而非默认增益模块。

### 4.2 常用控制参数

- `--tasks full`：只跑主实验链路。
- `--tasks eval-bench`：只跑评估性能专题（会复用主流程上下文）。
- `--tasks parallel-bench`：只跑 requested-mode 对照；当前实现会把实际 worker 数保守回落到 1。
- `--tasks all`：一次跑完 full + eval-bench + parallel-bench。
- `--stagewise-seeds 42,52,62`：指定一组 stagewise 随机种子并逐个运行。
- `--output-dir outputs/benchmark_runs_alt`：指定输出根目录，避免和已有实验互相覆盖。
- `--verbose`：打印过程日志，便于观察训练与剪枝过程。
- `--quiet`：静默运行，只保留必要结果输出。
- 数据路径、MNIST 自动拉取、类别集合等参数现在统一由 `AppConfig.data` 管理。
- `data.auto_fetch_mnist=true`：缺少 `.npy` 文件时自动补齐 MNIST 数据。
- `data.allow_auto_fetch_outside_data_dir=true`：显式允许把自动补齐文件写到仓库 `data/` 目录之外。

### 4.3 常见显式覆盖

- `--lib-preset layered`：分层函数库，精度与复杂度较均衡。
- `--lib-preset fast`：精简函数库，优先降低搜索成本与运行时间。
- `--lib-preset expressive`：增强表达能力，可在分层库不足时试验。
- `--lib-preset full`：完整函数库，搜索空间最大，通常最慢但最灵活。
- `--run-profile engineering`：保持当前工程化口径（默认行为）。
- `--run-profile legacy`：按 `d8` 历史参考版本的关键默认值回退（用于口径对齐）。
- `--run-profile fast`：一键切到速度优先口径（并不等同于 legacy）。

- `--device cpu`：覆盖 `runtime.device`。
- `--global-seed 321`：覆盖 `runtime.global_seed`。
- `--baseline-seed 321`：覆盖 `runtime.baseline_seed`。
- `--batch-size 256`：覆盖 `runtime.batch_size`。
- `--numeric-basis bspline|radial_bf`：显式覆盖 `model.numeric_basis`。
- `--stage-guard-mode light`：覆盖 `stagewise.guard_mode`（默认研究复跑建议）。
- `--stage-guard-mode full`：覆盖 `stagewise.guard_mode`（回归验证建议，耗时更高）。
- `--max-prune-rounds 12`：覆盖 `symbolize.max_prune_rounds`。
- `--layerwise-finetune-steps 0`：覆盖 `symbolize.layerwise_finetune_steps`。
- `--no-input-compaction`：覆盖 `symbolize.enable_input_compaction`。
- `--prune-collapse-floor 0.0`：覆盖 `symbolize.prune_collapse_floor`。

### 4.4 评估 benchmark 参数

- `--bench-repeat 3`：每项 benchmark 的正式重复次数（用于统计均值/方差）。
- `--bench-warmup 1`：预热轮数（减少首次执行的冷启动偏差）。
- `--eval-rounds 3`：评估回合数（跨回合汇总稳定性）。
- `--validate-n-sample 500`：验证抽样规模（越大越稳，耗时也更高）。

### 4.5 并行 benchmark 参数

- `--parallel-modes auto,off,thread4`：requested mode 候选集合；当前主要用于记录标签与串行基线对照，而不是验证真实多 worker 提速。
- `--parallel-target-min 40`：并行实验中的最小目标边数。
- `--parallel-target-max 80`：并行实验中的最大目标边数。
- `--parallel-max-prune-rounds 8`：并行实验允许的最大剪枝轮数。
- `--parallel-finetune-steps 20`：并行实验常规微调步数。
- `--parallel-layerwise-finetune-steps 20`：并行实验逐层微调步数。
- `--parallel-affine-finetune-steps 0`：并行实验仿射微调步数（0 代表跳过）。

## 5. 结果解读最小集合

结果解读时可优先关注 `symkanbenchmark_runs.csv` 中以下字段：

- `base_acc`
- `enhanced_acc`
- `final_acc`
- `final_n_edge`
- `effective_target_edges`
- `effective_input_dim`
- `macro_auc`
- `validation_mean_r2`
- `symbolic_total_seconds`
- `symbolic_core_seconds`
- `symbolize_wall_time_s`
- `post_symbolic_eval_wall_time_s`
- `run_total_wall_time_s`
- `stage_guard_mode`
- `numeric_cache_hit`
- `symbolic_prep_cache_hit`
- `cached_stage_total_seconds_ref`
- `cached_symbolic_prep_seconds_ref`
- `final_teacher_imitation_mse`
- `final_target_mse`
- `final_target_r2`

若用于论文写作，不宜依据单次运行结果下结论，至少应在 3 个 seeds 上统计：

1. `symkanbenchmark_runs.csv` 的均值与方差。
2. `benchmark_multi_round_summary_cn.csv` 的速度均值与标准差。
3. `benchmark_symbolic_parallel_quick.csv` 的 `vs_off_speedup_x`。

耗时字段口径（新旧兼容）：

1. `symbolic_total_seconds` / `symbolic_core_seconds`：符号化核心阶段耗时（`fast_symbolic` 主段）。
2. `symbolize_wall_time_s`：`symbolize_pipeline` 的墙钟耗时（包含 pre-symbolic fit / post-symbolic affine 等）。
3. `export_wall_time_s`：兼容旧字段，值等于 `symbolize_wall_time_s`。
4. `post_symbolic_eval_wall_time_s`：符号化完成后到指标导出（验证、AUC、summary 写出）的耗时。
5. `run_total_wall_time_s`：单次 run 的端到端墙钟耗时。

其中与当前 baseline/icbr 对照最相关的补充字段含义如下：

1. `numeric_cache_hit`：当前 run 是否复用了共享 numeric stage 缓存。
2. `symbolic_prep_cache_hit`：当前 run 是否复用了 shared symbolic-prep 缓存。
3. `cached_stage_total_seconds_ref` / `cached_symbolic_prep_seconds_ref`：共享阶段参考时长，只用于说明被复用的阶段成本，不应被计作当前 symbolization-only run 的实时耗时。
4. `final_teacher_imitation_mse`：最终符号模型相对共享 numeric teacher 的 imitation 误差。
5. `final_target_mse` / `final_target_r2`：最终符号模型相对真实目标的误差与拟合优度。
6. `icbr_candidate_generation_wall_time_s` / `icbr_replay_rerank_wall_time_s` / `icbr_replay_rank_inversion_rate`：仅在 ICBR backend 下有意义，用于机制拆解。

---

## 6. A/B Experiments And Backend Compare

### 6.1 当前常用变体

当前仓库中的 benchmark A/B 变体至少包括四类：

1. `baseline`：默认工程口径。
2. `adaptive`：启用验证反馈 + 自适应阈值 + 自适应 lamb/ft。
3. `adaptive_auto`：在 `adaptive` 上增加阶段早停与 symbolize 自适应剪枝节奏。
4. `baseline_icbr`：与 `baseline` 共享 numeric stage 和 shared symbolic-prep，只把 `symbolize.symbolic_backend` 切到 `icbr`。
5. `baseline_fastlib`：与 `baseline` 共享非 `symbolize` 配置，但把函数库扩大到 `FAST_LIB`。
6. `baseline_icbr_fastlib`：与 `baseline_fastlib` 共享 numeric stage 和 shared symbolic-prep，只把 `symbolize.symbolic_backend` 切到 `icbr`。

本轮 compare 涉及的函数库口径如下：

1. layered 库：`LIB_HIDDEN = ["x", "x^2", "tanh"]`，`LIB_OUTPUT = ["x", "x^2"]`。
2. FAST_LIB：`FAST_LIB = ["x", "x^2", "x^3", "tanh", "sin", "cos", "exp", "log", "sqrt", "abs"]`。
3. full library：`FULL_LIB = ["x", "x^2", "x^3", "x^4", "x^5", "1/x", "1/x^2", "1/x^3", "1/x^4", "1/x^5", "sqrt", "x^0.5", "x^1.5", "1/sqrt(x)", "1/x^0.5", "exp", "log", "abs", "sin", "cos", "tan", "tanh", "sgn", "arcsin", "arccos", "arctan", "arctanh", "0", "gaussian"]`。

### 6.2 命令模板

公共参数：

```powershell
# 运行目录：仓库根目录（symkan-experiments/）
python -m scripts.symkanbenchmark `
  --tasks full `
  --stagewise-seeds 42,52,62 `
  --config <VARIANT_APP_CONFIG> `
  --output-dir <OUT_DIR> `
  --quiet
```

实例：

```powershell
# 运行目录：仓库根目录（symkan-experiments/）
python -m scripts.symkanbenchmark --tasks full --stagewise-seeds 42,52,62 --config configs/benchmark_ab/baseline.yaml --output-dir outputs/rerun_v2_engine_safe_20260401/benchmark_ab/baseline --quiet
python -m scripts.symkanbenchmark --tasks full --stagewise-seeds 42,52,62 --config configs/benchmark_ab/baseline_icbr.yaml --output-dir outputs/rerun_v2_engine_safe_20260401/benchmark_ab/baseline_icbr --quiet
python -m scripts.symkanbenchmark --tasks full --stagewise-seeds 42,52,62 --config configs/benchmark_ab/baseline_fastlib.yaml --output-dir outputs/rerun_v2_engine_safe_20260401/benchmark_ab/baseline_fastlib --quiet
python -m scripts.symkanbenchmark --tasks full --stagewise-seeds 42,52,62 --config configs/benchmark_ab/baseline_icbr_fastlib.yaml --output-dir outputs/rerun_v2_engine_safe_20260401/benchmark_ab/baseline_icbr_fastlib --quiet
python -m scripts.symkanbenchmark --tasks full --stagewise-seeds 42,52,62 --config configs/benchmark_ab/baseline_icbr_fulllib.yaml --output-dir outputs/rerun_v2_engine_safe_20260401/benchmark_ab/baseline_icbr_fulllib --quiet
```

当前 `baseline_icbr.yaml` 的设计意图是：保持 baseline 数值训练与 shared symbolic-prep 语义不变，只切换 symbolic backend。

`baseline_fastlib.yaml` / `baseline_icbr_fastlib.yaml` 的设计意图是：在不改变 numeric cache key 的前提下扩大符号函数库。因此库覆盖写在 `symbolize.lib`，而不是改 `library` section；这样同一 `benchmark_ab/` 父根下的 rerun 仍可命中既有 `_numeric_cache/` 与 `_symbolic_prep_cache/`。

### 6.3 配置建议

这一组实验不再推荐通过长 CLI 逐项传参。

1. 变体差异应直接体现在各自的 `AppConfig` YAML 中。
2. 当前仓库已内置 `configs/benchmark_ab/baseline.yaml`、`adaptive.yaml`、`adaptive_auto.yaml`、`baseline_icbr.yaml`、`baseline_fastlib.yaml`、`baseline_icbr_fastlib.yaml` 与 `baseline_icbr_fulllib.yaml`。
3. benchmark CLI 主要保留 `--config`、`--output-dir`、`--stagewise-seeds` 和一小组显式白名单覆盖项。
4. 若对比目标是 ICBR，优先保留独立的 `baseline_icbr.yaml`，不要只在命令行临时覆盖 `--symbolic-backend icbr` 后丢失可追踪配置。

### 6.4 结果自动汇总

结果汇总可使用 [benchmark_ab_compare.py](../benchmark_ab_compare.py)。

通用 compare 示例：

```powershell
# 运行目录：仓库根目录（symkan-experiments/）
python -m scripts.benchmark_ab_compare --root outputs/benchmark_ab --baseline baseline --variants adaptive,adaptive_auto --output outputs/benchmark_ab/comparison
```

baseline/icbr 专用 compare 示例：

```powershell
# 运行目录：仓库根目录（symkan-experiments/）
python -m scripts.benchmark_ab_compare `
  --root outputs/rerun_v2_engine_safe_20260401/benchmark_ab `
  --baseline baseline `
  --variants baseline_icbr `
  --output outputs/rerun_v2_engine_safe_20260401/benchmark_ab/comparison
```

FAST_LIB 对照示例：

```powershell
# 运行目录：仓库根目录（symkan-experiments/）
python -m scripts.benchmark_ab_compare `
  --root outputs/rerun_v2_engine_safe_20260401/benchmark_ab `
  --baseline baseline_fastlib `
  --variants baseline_icbr_fastlib `
  --output outputs/rerun_v2_engine_safe_20260401/benchmark_ab/comparison_fastlib
```

通用输出：

- `variant_summary.csv`
- `pairwise_delta_summary.csv`
- `seedwise_delta.csv`
- `trace_seedwise.csv`
- `trace_summary.csv`
- `comparison_summary.md`

当 compare 对为单个 baseline-backend vs 单个 icbr-backend pair 时，还会额外生成：

- `baseline_icbr_shared_check.csv`
- `baseline_icbr_primary_effect.csv`
- `baseline_icbr_mechanism_summary.csv`

### 6.5 当前 backend compare 引用分层（2026-04-01）

当前 `2026-04-01` 的 ICBR 结果不宜再写成“只有一个主引用切片”，更稳妥的做法是按论点拆分为两套 paired compare 和一套补充单变体切片。

#### 6.5.1 layered 库 paired 切片

较保守的 paired backend-only 对照位于：

- [outputs/rerun_v2_engine_safe_20260401/benchmark_ab/comparison/comparison_summary.md](../outputs/rerun_v2_engine_safe_20260401/benchmark_ab/comparison/comparison_summary.md)
- [outputs/rerun_v2_engine_safe_20260401/benchmark_ab/comparison/baseline_icbr_shared_check.csv](../outputs/rerun_v2_engine_safe_20260401/benchmark_ab/comparison/baseline_icbr_shared_check.csv)
- [outputs/rerun_v2_engine_safe_20260401/benchmark_ab/comparison/baseline_icbr_primary_effect.csv](../outputs/rerun_v2_engine_safe_20260401/benchmark_ab/comparison/baseline_icbr_primary_effect.csv)
- [outputs/rerun_v2_engine_safe_20260401/benchmark_ab/comparison/baseline_icbr_mechanism_summary.csv](../outputs/rerun_v2_engine_safe_20260401/benchmark_ab/comparison/baseline_icbr_mechanism_summary.csv)

优先关注以下事实：

1. `baseline_icbr_shared_check.csv` 对 `42/52/62` 三个 seed 均报告：
   - `shared_numeric_aligned=True`
   - `trace_aligned=True`
   - `shared_symbolic_prep_aligned=True`
2. `trace_summary.csv` 中 `baseline` 与 `baseline_icbr` 的 `Symbolize Trace Rhythm` 完全一致。
3. `baseline_icbr_primary_effect.csv` 报告：
   - mean `symbolic_core_speedup_vs_baseline = 1.751763`
   - mean `final_teacher_imitation_mse_shift = -0.006330`
   - mean `final_target_mse_shift = -0.008691`
   - mean `final_target_r2_shift = 0.096602`
4. `variant_summary.csv` 中两边 `final_n_edge` 均值完全一致，说明 ICBR 没有恢复已剪掉的边。
5. layered 切片当前更适合支持“paired fairness 成立，且速度与质量同时改善”的表述。
6. 这一切片的具体库设置是：`LIB_HIDDEN = ["x", "x^2", "tanh"]`，`LIB_OUTPUT = ["x", "x^2"]`。

#### 6.5.2 FAST_LIB paired 切片

更能体现更大候选库下 paired 速度收益的切片位于：

- [outputs/rerun_v2_engine_safe_20260401/benchmark_ab/comparison_fastlib/comparison_summary.md](../outputs/rerun_v2_engine_safe_20260401/benchmark_ab/comparison_fastlib/comparison_summary.md)
- [outputs/rerun_v2_engine_safe_20260401/benchmark_ab/comparison_fastlib/baseline_icbr_shared_check.csv](../outputs/rerun_v2_engine_safe_20260401/benchmark_ab/comparison_fastlib/baseline_icbr_shared_check.csv)
- [outputs/rerun_v2_engine_safe_20260401/benchmark_ab/comparison_fastlib/baseline_icbr_primary_effect.csv](../outputs/rerun_v2_engine_safe_20260401/benchmark_ab/comparison_fastlib/baseline_icbr_primary_effect.csv)
- [outputs/rerun_v2_engine_safe_20260401/benchmark_ab/comparison_fastlib/baseline_icbr_mechanism_summary.csv](../outputs/rerun_v2_engine_safe_20260401/benchmark_ab/comparison_fastlib/baseline_icbr_mechanism_summary.csv)

优先关注以下事实：

1. `baseline_icbr_shared_check.csv` 对 `42/52/62` 三个 seed 均报告：
   - `shared_numeric_aligned=True`
   - `trace_aligned=True`
   - `shared_symbolic_prep_aligned=True`
2. `trace_summary.csv` 中 `baseline_fastlib` 与 `baseline_icbr_fastlib` 的 `Symbolize Trace Rhythm` 完全一致。
3. `baseline_icbr_primary_effect.csv` 报告：
   - mean `symbolic_core_speedup_vs_baseline = 2.350452`
   - mean `final_teacher_imitation_mse_shift = 0.000062`
   - mean `final_target_mse_shift = -0.000023`
   - mean `final_target_r2_shift = 0.000258`
4. `variant_summary.csv` 中两边 `final_n_edge` 均值完全一致，说明 ICBR 仍未破坏复杂度口径。
5. 两侧 `numeric_cache_hit=True` 且 `symbolic_prep_cache_hit=True`，说明 FAST_LIB 扩库并未破坏既有 cache reuse 边界。
6. 与旧口径不同，当前 FAST_LIB 切片不应再写成 `6.09x` 提速，而应更新为约 `2.35x` 的 core speedup。
7. 这一切片的具体库设置是：`FAST_LIB = ["x", "x^2", "x^3", "tanh", "sin", "cos", "exp", "log", "sqrt", "abs"]`。

#### 6.5.3 `baseline_icbr_fulllib` 补充切片

补充单变体结果位于：

- [outputs/rerun_v2_engine_safe_20260401/benchmark_ab/baseline_icbr_fulllib/symkanbenchmark_runs.csv](../outputs/rerun_v2_engine_safe_20260401/benchmark_ab/baseline_icbr_fulllib/symkanbenchmark_runs.csv)

当前应只把它当作 ICBR 在 full symbolic library 下的单边运行画像：

1. `baseline_fulllib` 本轮没有继续跑，因为 full symbolic library 下的 baseline 路径过慢；因此这里改用 ICBR 单边切片做补充说明。
2. `final_acc` 均值约 `0.795433`，`macro_auc` 均值约 `0.963225`，`final_target_r2` 均值约 `0.601003`。
3. `final_n_edge` 均值仍为 `88.333333`。
4. `symbolic_core_seconds` 均值约 `35.218785`，三 seed 都命中了 `numeric_cache_hit=True` 与 `symbolic_prep_cache_hit=True`。
5. 相对 `baseline_icbr_fastlib`，full library 版本的 ICBR 单边均值表现为：
   - `final_acc +0.002200`
   - `macro_auc +0.000592`
   - `final_target_r2 +0.004067`
   - `symbolic_core_seconds +3.227987`
6. 因此，这一切片适合支持“ICBR 让 full library 方案仍然可跑，并带来一定单边收益”的表述，但不得替代 paired backend compare 证据。
7. 这一切片的具体库设置是：`FULL_LIB = ["x", "x^2", "x^3", "x^4", "x^5", "1/x", "1/x^2", "1/x^3", "1/x^4", "1/x^5", "sqrt", "x^0.5", "x^1.5", "1/sqrt(x)", "1/x^0.5", "exp", "log", "abs", "sin", "cos", "tan", "tanh", "sgn", "arcsin", "arccos", "arctan", "arctanh", "0", "gaussian"]`。

当前报告建议：

1. backend compare 优先使用 `symbolic_core_seconds`，而不是单独使用 `symbolize_wall_time_s`。
2. 若要证明“比较只发生在后端”，必须先引用 `baseline_icbr_shared_check.csv`。
3. 若要解释 ICBR 为什么更快，应进一步引用 mechanism summary，而不是只引用最终 wall-time。
4. 若要强调“paired fairness 已成立且质量同步改善”，优先引用 `comparison/`。
5. 若要强调“在更大候选库下的 paired 速度收益”，优先引用 `comparison_fastlib/`。
6. 若要补充 ICBR 在全量函数库下的单边运行画像，可附带引用 `baseline_icbr_fulllib/`，并说明 `baseline_fulllib` 本轮未跑是因为过慢；该切片的意义是展示 ICBR 的可运行性与单边收益，而不是替代 paired compare。

### 6.6 历史参考结果

下列结果仍保留为历史或专题参考，但不再是当前 ICBR 接入的主引用：

1. `baseline / adaptive / adaptive_auto`
   - 主要用于说明 adaptive 系列的历史工程口径。
2. `rerun_v2_engine_safe_20260327` 的 `baseline (bspline) vs radial_bf`
   - 主要用于说明 numeric basis 专题，不应与当前 baseline/icbr 后端对照混用。

## 7. 报告口径

避免只报告均值，至少同时给出：

1. 均值与标准差。
2. 中位数差值。
3. 相对 baseline 的胜负计数（win/lose/tie）。
4. 运行代价指标（`symbolic_core_seconds`、`symbolize_wall_time_s`、`run_total_wall_time_s`）与结构指标（`final_n_edge`）。
5. 若 compare 为单个 baseline-backend vs 单个 icbr-backend pair，还应给出 shared-state 检查和机制拆解。

正文可采用以下较为保守的表述方式：

1. “在当前 `n=3` seeds 下，baseline-backend 与 icbr-backend 变体共享 numeric stage 与 shared symbolic-prep，因此该对照可解释为 backend-only 差异。”
2. “ICBR 在不改变 `final_n_edge` 的前提下显著降低了 `symbolic_core_seconds`；layered 切片当前同时表现出质量改善，而 FAST_LIB 切片更适合表述为提速更强、质量近似持平。”
3. “后续若需强化统计结论，应扩展 seed 样本并补充非参数检验。”

## 8. 与总文档统一口径（2026-04）

为避免跨文档“默认值”和“项目层设定”混用，统一采用以下写法：

1. **CLI 默认值**：指脚本当前保留的调度参数与少量显式覆盖项默认值。
2. **项目配置**：指基于实验结论所采用的 `AppConfig` 组合（见 [symkan_usage.md](symkan_usage.md) 与 [design.md](design.md)）。
3. **默认 symbolic backend**：仍指 `baseline`，`icbr` 仅作为显式 opt-in backend。
4. **backend compare 引用分层**：`comparison/` 用于较保守的 paired backend-only 结论，`comparison_fastlib/` 用于更大候选库下的 paired speed 结论，`baseline_icbr_fulllib/` 只用于补充单变体观察。
