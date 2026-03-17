# KAN 参数说明

## 文档导航

- 返回总览：[README](../README.md)
- docs 总入口：[index](index.md)
- 总体使用文档：[symkan_usage](symkan_usage.md)
- benchmark 参数文档：[symkanbenchmark_usage](symkanbenchmark_usage.md)
- 设计文档：[design](design.md)
- 消融说明：[ablation_usage](ablation_usage.md)

## 目录

- [1. 说明范围](#1-说明范围)
- [2. 主流程与参数位置](#2-主流程与参数位置)
- [3. 数据与运行时](#3-数据与运行时)
- [4. Baseline KAN 参数](#4-baseline-kan-参数)
- [5. 输入筛选参数](#5-输入筛选参数)
- [6. 阶段训练参数](#6-阶段训练参数)
- [7. 主符号化参数](#7-主符号化参数)
- [8. 评估与导出参数](#8-评估与导出参数)
- [9. 性能基准与并行对照参数](#9-性能基准与并行对照参数)
- [10. 调参顺序](#10-调参顺序)
- [11. 命令行运行说明](#11-命令行运行说明)

## 1. 说明范围

本文说明当前仓库中 `notebooks/kan.ipynb` 所采用的实验参数，不涉及旧版接口或未使用配置。文中关注的是参数所在阶段、作用对象及其在实验流程中的位置。

## 2. 主流程与参数位置

当前 notebook 主流程可概括为六个阶段：

1. 读取数据并统一运行时设置。
2. 训练 baseline KAN 并计算输入归因。
3. 基于归因结果进行输入筛选。
4. 通过 `stagewise_train` 获得适于符号化的模型快照。
5. 通过 `symbolize_pipeline` 完成剪枝、符号化、微调与导出。
6. 对结果进行数值验证、ROC/AUC 评估以及性能基准测试。

参数解释应结合这一流程理解。单个参数的作用通常依赖于其所在阶段。

## 3. 数据与运行时

### 3.1 数据输入

- `X_train/X_test`：输入特征，当前使用 `float32`。
- `Y_train_cat/Y_test_cat`：标签，可为 one-hot 或类别索引；notebook 中会统一转换为 one-hot。
- 若 `*.npy` 文件不存在，将优先尝试 `tensorflow.keras.datasets.mnist.load_data()`；若 TensorFlow 不可用，则回退到 `sklearn.fetch_openml("mnist_784")`，并生成同名 `*.npy` 文件。
- `input_dim`：输入维度，来自 `X_train.shape[1]`。
- `n_classes`：类别数，来自标签维度。

### 3.2 设备与批大小

- `device = 'cuda' if torch.cuda.is_available() else 'cpu'`
- `set_device(device)`：将设备设置同步到 `symkan` 运行时。
- `BATCH_SIZE = default_batch_size()`：给出与设备类型匹配的默认 batch 大小。

该 `BATCH_SIZE` 同时影响 baseline 训练、阶段训练与符号化阶段的微调。若不存在显存或内存约束，通常不建议在 notebook 中途更改。

## 4. Baseline KAN 参数

该部分对应 notebook 中 baseline 训练阶段。

- `inner_dim = 16`
- `width_base = [input_dim, inner_dim, n_classes]`
- `grid = 5`
- `k = 3`
- `seed = 123`

训练参数如下：

- `steps = 150`
- `lr = 0.02`
- `lamb = 1e-4`
- `update_grid = True`
- `log = 12`

该阶段的目的不是追求 baseline 的极限性能，而是获得一个适于稳定归因的参考模型。

## 5. 输入筛选参数

该部分对应归因与降维阶段。

- `feature_score = safe_attribute(base_model, dataset_full)`
- `top_k = 120`

`top_k` 表示保留归因分数最高的前 `K` 个输入特征，并据此构造后续增强模型与符号化流程所使用的数据集。

一般而言：

- `top_k` 较小：符号化成本较低，但精度上限可能下降。
- `top_k` 较大：保留信息更多，但符号搜索成本与不稳定性也会提高。

对于当前 MNIST 任务，`top_k = 120` 是已有实验中较为平衡的设置。

## 6. 阶段训练参数

该部分对应 `symkan.tuning.stagewise_train`。

### 6.1 结构与调度参数

- `width = [sel_dim, 16, n_classes]`
- `grid = 5`
- `k = 3`
- `seed = 42`
- `lamb_schedule = (0.0, 0.0, 2e-5, 5e-5, 1e-4, 2e-4, 3e-4, 5e-4, 7e-4, 1e-3)`
- `lr_schedule = (0.02, 0.015, 0.012, 0.01, 0.008, 0.006, 0.005, 0.004, 0.003, 0.002)`
- `steps_per_stage = 60`

### 6.2 剪枝参数

- `prune_start_stage = 3`
- `target_edges = 120`
- `prune_edge_threshold_init = 0.003`
- `prune_edge_threshold_step = 0.003`
- `prune_acc_drop_tol = 0.04`
- `post_prune_ft_steps = 50`

这些参数共同决定阶段训练中的渐进剪枝节奏。其作用是控制模型稀疏化速度，并为后续符号化保留可接受的精度。

### 6.3 选模参数

- `sym_target_edges = 50`
- `acc_weight = 0.5`

`stagewise_train` 并非简单选取最后一个阶段或最高精度阶段，而是依据

$$
\text{sym\_readiness\_score} = \text{acc\_weight} \cdot acc + (1 - \text{acc\_weight}) \cdot sparsity
$$

在多个阶段快照中选出更适于后续符号化的模型。

## 7. 主符号化参数

该部分对应 `symkan.symbolic.symbolize_pipeline`。

### 7.1 结构控制参数

- `target_edges = 90`
- `max_prune_rounds = 30`
- `weight_simple = 0.10`

`target_edges` 表示目标边数；实际输出中还应同时关注 `effective_target_edges`，因为流水线内部可能进行自适应调整。

### 7.2 函数库参数

- `lib = None`
- `lib_hidden = LIB_HIDDEN`
- `lib_output = LIB_OUTPUT`

当前 notebook 使用分层函数库。默认预设包括：

- `LIB_HIDDEN = ["x", "x^2", "tanh"]`
- `LIB_OUTPUT = ["x", "x^2"]`
- `FAST_LIB`
- `EXPRESSIVE_LIB`
- `FULL_LIB`

### 7.3 微调参数

- `finetune_steps = 50`
- `finetune_lr = 0.0005`
- `layerwise_finetune_steps = 60`
- `affine_finetune_steps = 200`
- `affine_finetune_lr_schedule = [0.003, 0.001, 0.0005, 0.0002]`

对于典型 2 层 KAN（`[in, hidden, class]`），当前实验结果支持优先将 `layerwise_finetune_steps` 设为 `0`；改进版 LayerwiseFT（60 步、早停、轻正则）更适合作为按需启用的实验开关。

### 7.4 并行参数

- `parallel_mode = 'auto'`
- `parallel_workers = None`
- `parallel_min_tasks = 16`

当前并行主要作用于 `suggest_symbolic` 阶段。由于 `fix_symbolic` 会修改模型状态，其余部分并不适合直接并行化。

### 7.5 低风险提速参数

- `prune_eval_interval = 2`
- `prune_attr_sample_adaptive = True`
- `prune_attr_sample_min = 768`
- `prune_attr_sample_max = 2048`
- `heavy_ft_early_stop_patience = 2`
- `heavy_ft_early_stop_min_delta = 5e-4`

这组参数主要用于减少低收益评估与无明显收益的微调步骤。

## 8. 评估与导出参数

### 8.1 公式数值验证

- `validate_formula_numerically(..., n_sample=500)`

关注指标包括：

- 平均 `R²`
- 负 `R²` 数量
- `numerically_unstable` 数量

### 8.2 ROC/AUC

- `compute_multiclass_roc_auc(Y_test_sel, y_prob_sym)`
- `plot_roc_curves(...)`

关注指标包括：

- 每类 AUC
- macro AUC

### 8.3 结果导出

- `collect_all_formulas(export_formulas)`
- `save_symbolic_summary(summary_df, csv_path=str(notebook_output_dir / 'kan_symbolic_summary.csv'))`

其中 `notebook_output_dir = repo_root / 'outputs' / 'notebooks'`，用于避免把结构化结果直接落在 `notebooks/` 目录下。

## 9. 性能基准与并行对照参数

### 9.1 单轮与多轮基准

- `repeat = 3`
- `warmup = 1`
- `rounds = 3`

输出文件包括：

- `outputs/notebooks/benchmark_multi_round_raw.csv`
- `outputs/notebooks/benchmark_multi_round_summary_cn.csv`
- `outputs/notebooks/benchmark_multi_round_summary_en.csv`

### 9.2 并行对照参数

- `bench_modes = ['auto', 'off', 'thread4']`
- `_target_quick = max(40, min(80, n_edge_now))`
- `max_prune_rounds = 8`
- `finetune_steps = 20`
- `layerwise_finetune_steps = 40`
- `affine_finetune_steps = 0`
- `prune_eval_interval = 2`
- `prune_attr_sample_adaptive = True`
- `prune_attr_sample_min = 512`
- `prune_attr_sample_max = 1536`
- `heavy_ft_early_stop_patience = 1`
- `heavy_ft_early_stop_min_delta = 5e-4`

该组参数主要用于速度专题对照，而非常规主实验设置。

对应并行专题 CSV 默认导出到 `outputs/notebooks/benchmark_symbolic_parallel_quick.csv`。

## 10. 调参顺序

若结果不理想，可按以下顺序调整：

1. 先调整 `top_k`，确认输入维度是否过高。
2. 再调整 `stage_target_edges` 与 `symbolic_target_edges`，确认剪枝是否过度。
3. 随后调整 `layerwise_finetune_steps` 与 `affine_finetune_steps`，补偿符号化造成的精度损失。
4. 最后再考虑调整 `lib_preset` 或扩展函数库。

这一顺序的依据在于，问题往往首先来自模型规模与剪枝节奏，而不是函数库表达能力本身。

## 11. 命令行运行说明

若使用 [symkanbenchmark.py](../symkanbenchmark.py) 进行批量实验，通常应将参数调试与正式运行分开：

- `--verbose`：用于观察阶段训练与符号化细节。
- `--quiet`：用于正式批量运行，以减少终端输出干扰。

`--quiet` 不会改变训练参数，仅影响输出行为。
