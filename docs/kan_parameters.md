# KAN 参数说明

本文只解释当前仓库里 kan.ipynb 的实际实验参数，不再混入旧版接口或未使用配置。目标很直接：你在 notebook、脚本和论文表格之间切换时，知道每个参数在哪个阶段生效、为什么要这么设，以及该从哪里下手调整。

## 1. 主流程

当前 notebook 主线固定为 6 段：

1. 优先读取 `X_train.npy/X_test.npy/Y_train_cat.npy/Y_test_cat.npy`；缺失时自动按 SymbolNet 风格拉取 MNIST 并落盘，再统一成 one-hot 标签。
2. 初始化 `symkan.core` 运行时，统一设备和 `BATCH_SIZE`。
3. 训练 baseline KAN，得到基准精度与归因分数。
4. 用归因做 top-k 输入筛选，构造降维后的 `dataset_enhanced`。
5. 用 `stagewise_train` 选出精度和稀疏度折中最好的增强模型。
6. 用 `symbolize_pipeline` 做剪枝、逐层符号化、强化微调和公式导出。

理解参数时不要脱离这个顺序。很多参数单看没有意义，只有放在这条链路里才知道它到底控制什么。

## 2. 数据与运行时

### 2.1 数据输入

- `X_train/X_test`：输入特征，当前为 `float32`。
- `Y_train_cat/Y_test_cat`：标签，可以是 one-hot，也可以是类别索引。notebook 会自动转换成 one-hot。
- 当上述 `*.npy` 不存在时，notebook 会自动尝试 `tensorflow.keras.datasets.mnist.load_data()`；若环境无 TensorFlow，则回退到 `sklearn.fetch_openml("mnist_784")`，并生成同名 `*.npy` 文件供后续复用。
- `input_dim`：输入维度，直接来自 `X_train.shape[1]`。
- `n_classes`：类别数，来自标签维度。

### 2.2 设备与批大小

- `device = 'cuda' if torch.cuda.is_available() else 'cpu'`
- `set_device(device)`：把设备同步到 `symkan` 运行时。
- `BATCH_SIZE = default_batch_size()`：当前实现下，CUDA 默认 256，CPU 默认 64。

这个 `BATCH_SIZE` 会同时影响 baseline 训练、阶段训练和主符号化微调。除非显存或内存有问题，否则不建议在 notebook 中途切换。

## 3. Baseline KAN 参数

对应 notebook 第 4 节。

- `inner_dim = 16`
- `width_base = [input_dim, inner_dim, n_classes]`
- `grid = 5`
- `k = 3`
- `seed = 123`

训练参数：

- `steps = 150`
- `lr = 0.02`
- `lamb = 1e-4`
- `update_grid = True`
- `log = 12`

这部分的任务不是把 baseline 推到极致，而是拿到一个能做稳定归因的参考模型。它要够稳，不要太复杂。

## 4. 输入筛选参数

对应 notebook 第 5 节。

- `feature_score = safe_attribute(base_model, dataset_full)`
- `top_k = 120`

含义很简单：保留归因分数最高的前 120 个输入特征，作为增强模型和后续符号化的输入。

调参原则：

- `top_k` 更小：更容易符号化，速度更快，但精度上限会掉。
- `top_k` 更大：精度潜力更高，但 `suggest_symbolic` 的代价会明显上升。

对当前 MNIST 任务，`top_k = 120` 是 notebook 已经验证过的折中点。你当然可以改，但不要假装改到 300 以后还能保持同样的符号化稳定性。

## 5. 阶段训练参数

对应 notebook 第 6 节，入口函数是 `symkan.tuning.stagewise_train`。

### 5.1 结构参数

- `width = [sel_dim, 16, n_classes]`
- `grid = 5`
- `k = 3`
- `seed = 42`

### 5.2 调度参数

- `lamb_schedule = (0.0, 0.0, 2e-5, 5e-5, 1e-4, 2e-4, 3e-4, 5e-4, 7e-4, 1e-3)`
- `lr_schedule = (0.02, 0.015, 0.012, 0.01, 0.008, 0.006, 0.005, 0.004, 0.003, 0.002)`
- `steps_per_stage = 60`

这是当前 notebook 的真实配置，不是旧文档里那组更短的默认 schedule。

### 5.3 剪枝参数

- `prune_start_stage = 3`
- `target_edges = 120`
- `prune_edge_threshold_init = 0.003`
- `prune_edge_threshold_step = 0.003`
- `prune_acc_drop_tol = 0.04`
- `post_prune_ft_steps = 50`

这组参数控制阶段训练里的渐进剪枝。逻辑是先拟合，再慢慢收缩。别一上来就猛剪，那样只会得到一堆回滚日志。

### 5.4 选模参数

- `sym_target_edges = 50`
- `acc_weight = 0.5`

`stagewise_train` 不是只看最后一个 stage，也不是只看最高精度。它会根据

$$
\text{sym\_readiness\_score} = \text{acc\_weight} \cdot acc + (1 - \text{acc\_weight}) \cdot sparsity
$$

从多个快照里选出更适合后续符号化的模型。

## 6. 主符号化参数

对应 notebook 第 8 节，入口函数是 `symkan.symbolic.symbolize_pipeline`。

### 6.1 结构目标

- `target_edges = 90`
- `max_prune_rounds = 30`

这里的 `target_edges` 是你希望最终压到的大致规模。当前实现还会返回 `effective_target_edges`，因为流水线内部可能做自适应调整，所以别只盯着你传进去的值，最终要看返回结果。

### 6.2 函数库

当前 notebook 用的是分层库：

- `lib = None`
- `lib_hidden = LIB_HIDDEN`
- `lib_output = LIB_OUTPUT`

默认预设：

- `LIB_HIDDEN = ["x", "x^2", "tanh"]`
- `LIB_OUTPUT = ["x", "x^2"]`
- `FAST_LIB = ["x", "x^2", "tanh", "sin", "cos", "exp", "log", "sqrt"]`
- `EXPRESSIVE_LIB/FULL_LIB = pykan 当前 SYMBOLIC_LIB 的全量函数名`

### 6.3 剪枝后短微调

- `finetune_steps = 50`
- `finetune_lr = 0.0005`

### 6.4 层间与末端微调

- `layerwise_finetune_steps = 120`
- `affine_finetune_steps = 200`
- `affine_finetune_lr_schedule = [0.003, 0.001, 0.0005, 0.0002]`

如果符号化后精度掉得太厉害，优先试着增加这两组步数，而不是先胡乱加函数库。

### 6.5 并行参数

- `parallel_mode = 'auto'`
- `parallel_workers = None`
- `parallel_min_tasks = 16`

当前并行只放在 `suggest_symbolic`，不是整个流水线全并行。原因很现实：`fix_symbolic` 会改模型状态，乱并发只会把结果搞坏。

### 6.6 低风险提速参数

- `prune_eval_interval = 2`
- `prune_attr_sample_adaptive = True`
- `prune_attr_sample_min = 768`
- `prune_attr_sample_max = 2048`
- `heavy_ft_early_stop_patience = 2`
- `heavy_ft_early_stop_min_delta = 5e-4`

这组参数的目标不是“更聪明”，而是减少不必要的评估和无收益微调。

## 7. 评估参数

对应 notebook 第 9 节。

### 7.1 公式数值验证

- `validate_formula_numerically(..., n_sample=500)`

关键指标：

- 平均 R²
- 负 R² 数量
- `numerically_unstable` 数量

### 7.2 ROC/AUC

- `compute_multiclass_roc_auc(Y_test_sel, y_prob_sym)`

关键指标：

- 每类 AUC
- macro AUC

### 7.3 汇总导出

- `collect_all_formulas(export_formulas)`
- `save_symbolic_summary(summary_df, csv_path='kan_symbolic_summary.csv')`

## 8. 性能基准参数

对应 notebook 第 11 节。

### 8.1 单轮基准

- `repeat = 3`
- `warmup = 1`

对比项：

- `legacy_numpy_path`
- `fast_tensor_path`
- `model_acc_ds_current`
- `validate_formula_first`
- `validate_formula_cached`

### 8.2 多轮统计

- `rounds = 3`

输出文件：

- `benchmark_multi_round_raw.csv`
- `benchmark_multi_round_summary_cn.csv`
- `benchmark_multi_round_summary_en.csv`

## 9. 并行对照参数

对应 notebook 第 12 节。

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

这组参数本来就不是为了追最优精度，而是为了做速度专题对照。别把它拿去当主实验配置。

## 10. 调参顺序

如果结果不理想，建议按这个顺序改：

1. 先调 `top_k`，确认输入维度是不是太高。
2. 再调 `stage_target_edges` 和 `symbolic_target_edges`，确认是不是剪得过头。
3. 然后调 `layerwise_finetune_steps` 和 `affine_finetune_steps`，补偿符号化带来的精度损失。
4. 最后才考虑换 `lib_preset` 或放大全量函数库。

原因很简单：大多数问题不是“函数库不够强”，而是模型规模和剪枝节奏根本没控住。

## 11. 命令行运行建议

如果你使用 [symkanbenchmark.py](symkanbenchmark.py) 做批量实验，建议把参数调试和正式跑表分开：

- `--verbose`：适合调参时看阶段训练和符号化细节。
- `--quiet`：适合正式批量跑实验，减少终端噪声。

`--quiet` 不会改变任何训练参数，只影响输出行为。

<!-- Duplicate H1 removed to comply with MD025 -->

适用范围：`kan.ipynb` 当前实验主线 + `symkan` 分层实现。

本版不再按“模块目录”讲解，而是按 notebook 的真实执行顺序（1)~12)）组织语言，便于边看单元边对参。

---

## 0) 先看总线：参数在实验中的角色

`kan.ipynb` 的主线是：

1. 数据与设备统一；
2. baseline 训练与归因降维；
3. stagewise 增强训练；
4. 主符号化导出；
5. 数值验证 + ROC/AUC + 汇总导出；
6. 性能/内存/并行专题基准。

因此参数应按“在哪个单元生效”理解，而不是孤立记忆。

---

## 1) 数据读取与运行时初始化（对应 notebook 1~3 节）

### 1.1 数据构建：`build_dataset`

- 输入：`X_train/X_test` 与 one-hot 标签 `Y_train/Y_test`（若 `*.npy` 缺失，会先自动生成）。
- 输出：`train_input/train_label/test_input/test_label`（`torch.float32`）。
- 关键点：训练、符号化、评估都复用这一份 dataset 格式。

### 1.2 设备与批大小

- `set_device(device)`：将 notebook 初始 `device` 同步到 `symkan` 运行时。
- `BATCH_SIZE = default_batch_size()`：自动给出设备相关默认 batch。
- 经验：CPU 下 batch 通常较小，CUDA 下较大；统一后尽量不要在后续单元反复切换。

### 1.3 函数库变量命名

- notebook 使用 `_LIB_HIDDEN/_LIB_OUTPUT`（由 `LIB_HIDDEN/LIB_OUTPUT` 赋值而来）。
- 文档中两组名字可视为同义；实际传参以 notebook 当前变量名为准。

---

## 2) Baseline 与归因筛选（对应 notebook 4~5 节）

### 2.1 Baseline KAN（对照组）

- 结构：`width_base=[input_dim, inner_dim, n_classes]`。
- 训练：`safe_fit(..., steps=150, lr=0.02, lamb=1e-4, update_grid=True)`。
- 目的：得到基线 `base_acc` 与 `n_edge`，供后续增强/符号化对比。

### 2.2 归因降维（关键预处理）

- `feature_score = safe_attribute(base_model, dataset_full)`。
- `top_k`：保留前 K 个输入特征，构建 `dataset_enhanced`。
- 调参含义：
  - `top_k` 大：精度潜力更高，但符号化更慢、稳定性更差；
  - `top_k` 小：更易符号化，但可能损伤上限精度。

---

## 3) 增强模型训练（对应 notebook 6 节，第15个代码单元）

本节调用 `stagewise_train`，目标是选出“精度-稀疏度折中最优”快照。

### 3.1 结构与阶段调度参数

- `width=[sel_dim, inner_dim, n_classes]`
- `grid=5, k=3, seed=42`
- `lamb_schedule`：分阶段稀疏正则轨迹
- `lr_schedule`：分阶段学习率轨迹
- `steps_per_stage=60`

### 3.2 渐进剪枝参数

- `prune_start_stage=3`：前 3 阶段先拟合再剪枝
- `target_edges=120`：阶段训练目标边数
- `prune_edge_threshold_init=0.003`
- `prune_edge_threshold_step=0.003`
- `prune_acc_drop_tol=0.04`：允许剪枝后短期精度回落
- `post_prune_ft_steps=50`：每次剪枝后恢复微调

### 3.3 选模评分参数

- `sym_target_edges=50`：符号化就绪参考边数
- `acc_weight=0.5`：精度与稀疏度权重折中

### 3.4 本节输出（后续依赖）

- `enhanced_model`
- `enhanced_res['selected_stage']`
- `enhanced_res['selected_score']`
- `enhanced_res['stage_logs']`

---

## 4) 主符号化导出（对应 notebook 8 节，第19个代码单元）

本节是全文核心：`symbolize_pipeline(...)`。

### 4.1 主控制参数

- `target_edges=90`：主实验符号化目标边数
- `max_prune_rounds=30`
- `weight_simple=0.10`：简单函数偏好（复杂度 vs 拟合）

### 4.2 函数库参数

- `lib=None`：使用分层函数库，而非统一库
- `lib_hidden=_LIB_HIDDEN`：输入→隐藏层函数候选
- `lib_output=_LIB_OUTPUT`：隐藏→输出层函数候选

### 4.3 微调参数

- `finetune_steps=50, finetune_lr=0.0005`：剪枝后短微调
- `layerwise_finetune_steps=60`：逐层符号化后的层间微调（技术默认）
- `affine_finetune_steps=200`：末端强化微调
- `affine_finetune_lr_schedule=[0.003, 0.001, 0.0005, 0.0002]`

口径说明：对典型 2 层 KAN（`[in, hidden, class]`），推荐显式设为 `layerwise_finetune_steps=0`；`60` 主要用于按需开启改进版 LayerwiseFT。

### 4.4 并行参数

- `parallel_mode='auto'`：CPU 倾向并行，CUDA 默认更保守
- `parallel_workers=None`：自动推断
- `parallel_min_tasks=16`：任务太少时回退串行

### 4.5 低风险提速参数

- `prune_eval_interval=2`：剪枝评估降频
- `prune_attr_sample_adaptive=True`
- `prune_attr_sample_min=768`
- `prune_attr_sample_max=2048`
- `heavy_ft_early_stop_patience=2`
- `heavy_ft_early_stop_min_delta=5e-4`

### 4.6 观测参数

- `collect_timing=True`：返回 `timing` 结构化耗时
- `verbose=True`：输出过程日志

### 4.7 本节核心观察项（notebook 已明确）

- `final_acc`
- `final_n_edge`
- `sym_stats`（`total/fixed/low_r2/r2_records/parallel_workers`）
- `timing`（重点看 `symbolic_total_seconds` 与 `symbolic_layers`）

---

## 5) 公式一致性 + ROC/AUC + 汇总（对应 notebook 9 节）

### 5.1 数值一致性参数

- `validate_formula_numerically(..., n_sample=500)`
- 关注：平均 R²、负 R² 数量、`numerically_unstable` 数量

### 5.2 分类能力参数

- `compute_multiclass_roc_auc(Y_test_sel, y_prob_sym)`
- `plot_roc_curves(...)`
- 关注：per-class AUC 与 macro AUC

### 5.3 汇总导出

- `collect_all_formulas(export_formulas)` 收集全量表达式
- `save_symbolic_summary(summary_df, csv_path='kan_symbolic_summary.csv')`

---

## 6) 性能与内存专题（对应 notebook 11 节）

### 6.1 单轮基准

- 对比项：
  - `legacy_numpy_path`
  - `fast_tensor_path`
  - `model_acc_ds_current`
  - `validate_formula_first/cached`
- 输出：`time_mean_s/time_std_s/rss_delta_mean_mb/gpu_peak_mean_mb`

### 6.2 多轮统计（稳健结论）

- `rounds=3`（可加大）
- 输出：`multi_round_raw`、`multi_round_summary`
- 建议论文报告：均值 ± 标准差，而非单轮值

### 6.3 CSV 标准化导出

- `benchmark_multi_round_raw.csv`
- `benchmark_multi_round_summary_cn.csv`
- `benchmark_multi_round_summary_en.csv`

---

## 7) 并行策略快速对照（对应 notebook 12 节）

### 7.1 对照配置

- `bench_modes=['auto','off','thread4']`
- `_target_quick=max(40, min(80, n_edge_now))`
- 轻量化参数：
  - `max_prune_rounds=8`
  - `finetune_steps=20`
  - `layerwise_finetune_steps=40`
  - `affine_finetune_steps=0`
  - `prune_eval_interval=2`
  - `prune_attr_sample_adaptive=True`
  - `prune_attr_sample_min=512`
  - `prune_attr_sample_max=1536`
  - `heavy_ft_early_stop_patience=1`
  - `heavy_ft_early_stop_min_delta=5e-4`

### 7.2 输出字段

- `wall_time_s`
- `symbolic_time_s`
- `final_acc`
- `final_n_edge`
- `vs_off_speedup_x`

### 7.3 导出

- `benchmark_symbolic_parallel_quick.csv`

---

## 8) 直接可用的参数模板（与当前 notebook 对齐）

### 8.1 主实验默认模板

- 使用第15单元 `stagewise_train` 参数 + 第19单元 `symbolize_pipeline` 参数原样复用。

### 8.2 精度优先模板

- `target_edges: 90 -> 100~130`
- `affine_finetune_steps: 200 -> 240~360`
- `layerwise_finetune_steps: 120 -> 120~180`
- `prune_eval_interval: 2 -> 1~2`

### 8.3 速度优先模板

- `target_edges: 90 -> 60~80`
- `prune_eval_interval: 2 -> 2~3`
- 保持 `prune_attr_sample_adaptive=True`
- `heavy_ft_early_stop_patience: 1~2`
- `layerwise_finetune_steps: 60~120`

---

## 9) 常见问题（按 notebook 实测语境）

- 并行加速不明显：正常，瓶颈常在非 suggest 阶段。
- 符号化后精度下降：优先提高 `target_edges`，再增加 `affine_finetune_steps`。
- 公式验证首次慢：正常，后续缓存命中会加速。
- 归因偶发异常：`safe_attribute` 已有回退路径，通常重跑即可。
