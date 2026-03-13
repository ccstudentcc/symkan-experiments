# symkan 使用说明

本文对应当前仓库里的分层式 symkan 实现，不再描述旧版把所有逻辑堆在 notebook 或单文件里的用法。现在的重点是三件事：入口在哪、返回什么、怎样按稳定顺序把训练和符号化串起来。

## 1. 模块结构

当前对外公开的模块只有 6 组：

- `symkan.core`：设备、数据、训练封装、推理评估、类型定义。
- `symkan.pruning`：安全归因接口。
- `symkan.tuning`：阶段训练与符号化就绪评分。
- `symkan.symbolic`：函数库、表达式工具、主符号化流水线。
- `symkan.eval`：公式数值验证、ROC/AUC。
- `symkan.io`：stage 日志、符号汇总和 bundle 导出。

顶层入口 [symkan/__init__.py](symkan/__init__.py) 只导出这些子模块，不直接塞进一堆函数名。你要用什么，就从对应层导入。

## 2. 最小工作流

最稳的顺序如下：

1. `set_device(...)`
2. `build_dataset(...)`
3. `safe_fit(...)` 训练 baseline
4. `safe_attribute(...)` 做输入筛选
5. `stagewise_train(...)` 选增强模型
6. `symbolize_pipeline(...)` 做剪枝和逐层符号化
7. `validate_formula_numerically(...)` 和 `compute_multiclass_roc_auc(...)` 做评估
8. `save_stage_logs(...)`、`save_symbolic_summary(...)`、`save_export_bundle(...)` 做导出

这不是教条，是当前代码最少坑的调用顺序。

## 3. 基础接口

### 3.1 运行时与数据

来自 [symkan/core/__init__.py](symkan/core/__init__.py)：

- `set_device(device)`
- `get_device()`
- `build_dataset(Xtr, Ytr, Xte, Yte, device=None)`
- `model_logits(model, X)`
- `model_acc(model, X, y_cls)`
- `model_acc_ds(model, dataset)`
- `get_n_edge(model)`
- `safe_fit(model, dataset, ...)`

`build_dataset` 当前返回的是兼容旧接口的字典：

- `train_input`
- `train_label`
- `test_input`
- `test_label`

这意味着 notebook、老脚本和新分层接口都还能共存，不需要为了“优雅”强行一次性改全仓库。

### 3.2 结构化类型

来自 [symkan/core/types.py](symkan/core/types.py)：

- `DatasetBundle`
- `TrainConfig`
- `StagewiseConfig`
- `SymbolizeConfig`
- `FitReport`
- `AttributeReport`
- `StagewiseResult`
- `SymbolizeResult`

当前风格是“双轨兼容”：

- 旧入口仍返回字典，保证 notebook 不炸。
- 新入口提供 `*_report` 版本，返回 dataclass，方便脚本和后续封装。

## 4. 阶段训练

入口：`from symkan.tuning import stagewise_train, stagewise_train_report`

### 4.1 `stagewise_train`

它做的事情不是简单循环 `fit`，而是：

1. 按 `lamb_schedule/lr_schedule` 分阶段训练。
2. 达到 `prune_start_stage` 后尝试剪枝。
3. 剪枝失败或精度掉太多时自动回滚。
4. 对每个 stage 记录 `acc/n_edges/score`。
5. 用 `sym_readiness_score` 从多个快照中选最终模型。

返回值是：

- `best_model`
- `result_dict`

`result_dict` 的主要字段：

- `train_loss`
- `test_loss`
- `stage_logs`
- `best_acc`
- `selected_stage`
- `selected_edges`
- `selected_score`
- `stage_snapshots`

### 4.2 `stagewise_train_report`

如果你不想在脚本里到处写字符串键，直接用它。它返回 `StagewiseResult`，字段和上面一一对应。

## 5. 安全归因

入口：`from symkan.pruning import safe_attribute, safe_attribute_report`

`safe_attribute` 做了几件实用但必要的事：

- 先前向一遍，刷新内部激活。
- 优先走 `torch.inference_mode()`。
- 如果碰到 pykan 的 backward 保存限制，再退回 `torch.no_grad()`。
- 最后恢复模型原来的 `train/eval` 状态。

如果你直接裸调 `model.attribute()`，你当然也许能跑通。但一旦环境或模型状态稍微复杂一点，失败率就会上来。这就是为什么这里要有一个安全封装。

## 6. 主符号化流水线

入口：`from symkan.symbolic import symbolize_pipeline, symbolize_pipeline_report`

### 6.1 流程

`symbolize_pipeline` 当前固定做 5 件事：

1. 渐进剪枝并做短微调。
2. 尝试压缩有效输入维度。
3. 调 `fast_symbolic` 做严格逐层符号化。
4. 做 affine-heavy 强化微调。
5. 导出公式、统计和耗时结构。

### 6.2 函数库选择

来自 [symkan/symbolic/__init__.py](symkan/symbolic/__init__.py)：

- `LIB_HIDDEN`
- `LIB_OUTPUT`
- `FAST_LIB`
- `EXPRESSIVE_LIB`
- `FULL_LIB`

优先级如下：

1. 传了 `lib`，所有层统一用它。
2. 没传 `lib`，则隐藏层用 `lib_hidden`，输出层用 `lib_output`。
3. 这两个都不传，就回退到 `LIB_HIDDEN/LIB_OUTPUT`。

### 6.3 返回字段

`symbolize_pipeline` 当前返回字典，核心字段如下：

- `model`
- `formulas`
- `valid_expressions`
- `trace`
- `sym_stats`
- `final_n_edge`
- `final_n_edge_raw`
- `final_acc`
- `effective_target_edges`
- `input_n_edge`
- `effective_input_indices`
- `effective_input_dim`
- `timing`

`sym_stats` 里最常用的是：

- `total`
- `fixed`
- `low_r2`
- `r2_records`
- `parallel_workers`

`timing` 里最常用的是：

- `symbolic_total_seconds`
- `symbolic_layers`
- `prune_rounds`
- `fit`

## 7. 评估接口

入口：`from symkan.eval import validate_formula_numerically, compute_multiclass_roc_auc`

### 7.1 `validate_formula_numerically`

来自 [symkan/eval/metrics.py](symkan/eval/metrics.py)。

它会：

- 从 `formulas` 中提取有效表达式。
- 使用 sympy `lambdify` 编译表达式。
- 对极值、NaN、Inf 做裁剪和替换。
- 逐个输出表达式的 R² 与数值稳定性标记。

内部有 `_LAMBDA_CACHE` 缓存，所以第二次验证通常更快。这也是 notebook 第 11 节要专门做首次/缓存对照的原因。

### 7.2 `compute_multiclass_roc_auc`

输入是 one-hot 标签和每类分数或概率，输出每个类别的：

- `fpr`
- `tpr`
- `auc`

它只做数值计算，不强依赖 notebook 的绘图环境。

## 8. 导出接口

入口：`from symkan.io import save_stage_logs, save_symbolic_summary, save_export_bundle`

用途：

- `save_stage_logs(stage_df, csv_path=...)`：保存阶段训练日志。
- `save_symbolic_summary(summary_df, csv_path=...)`：保存公式汇总表。
- `save_export_bundle(bundle, path=...)`：打包整个实验资产到 pkl。

如果你做批量实验，建议至少保留：

1. stage 日志 CSV
2. 符号汇总 CSV
3. metrics JSON 或 bundle

否则你最后只会剩一行精度数字，然后什么都解释不了。

## 9. Notebook 对齐示例

下面这段和当前 kan.ipynb 的主实验一致，只去掉了绘图和 display：

```python
import numpy as np
from symkan.core import build_dataset, model_acc_ds, safe_fit, set_device
from symkan.pruning import safe_attribute
from symkan.symbolic import LIB_HIDDEN, LIB_OUTPUT, symbolize_pipeline
from symkan.tuning import stagewise_train

set_device("cuda")

X_train = np.load("X_train.npy").astype(np.float32)
X_test = np.load("X_test.npy").astype(np.float32)
Y_train = np.load("Y_train_cat.npy").astype(np.float32)
Y_test = np.load("Y_test_cat.npy").astype(np.float32)

dataset_full = build_dataset(X_train, Y_train, X_test, Y_test)

# baseline -> attribution -> top-k
# stagewise_train -> symbolize_pipeline
```

如果你要命令行复现这条流程，直接用 [symkanbenchmark.py](symkanbenchmark.py)。它就是把 notebook 主线拆成了可批量跑的脚本。

补充：脚本支持 `--quiet` 静默运行。如果你只是想后台批量落结果，不想看终端里一堆进度条和中间日志，直接加这个参数。

## symkan 使用文档（详细改进版）

本文专门回答一个问题：
__symkan 为了符号回归，相对原始 kan 包到底做了哪些具体改进？__

文档按“基线能力 → 改进项 → 参数映射 → 实验建议”展开，尽量避免泛化描述。

---

## 1. 先说结论：symkan 不是重写 KAN，而是做了“可复现实验流水线层”

`kan.MultKAN` 本身已提供：

- `fit`：训练；
- `prune_edge / prune_input`：剪枝；
- `suggest_symbolic / auto_symbolic`：符号函数建议与自动符号化；
- `symbolic_formula`：导出表达式。

`symkan` 的核心改进是把这些“单点能力”组织成__稳定、可控、可观测__的端到端流程：

- 训练侧：分阶段稀疏化 + 快照筛选（不是只看最后一步）；
- 符号化侧：剪枝→分层拟合→分层微调→强化微调；
- 工程侧：设备/批量/克隆/回退策略统一，减少 notebook 偶发失败；
- 评估侧：数值一致性、AUC、复杂度和耗时统一产出。

---

## 2. 改进总览（逐项、可定位）

下面所有改进都对应当前仓库代码实现。

### 2.1 训练调度从“单次 fit”升级为“分阶段 + 可回滚 + 评分选优”

相比原生 `fit` 一次跑完，`symkan.tuning.stagewise_train` 新增：

1) __阶段化正则与学习率调度__

- `lamb_schedule`、`lr_schedule` 分阶段推进；
- 首阶段可 `update_grid=True`，后续默认关闭，降低训练不稳定。

1) __阶段内剪枝与回滚__

- 达到 `prune_start_stage` 后，若边数超标则尝试 `prune_edge`；
- 剪枝后做短微调（`post_prune_ft_steps`）；
- 若精度跌幅超过 `prune_acc_drop_tol`，自动回滚到剪枝前快照。

1) __符号化就绪度评分（而非只看 acc）__

- `sym_readiness_score = acc_weight * acc + (1-acc_weight) * sparsity_score`；
- 在精度可接受前提下偏好更稀疏模型，减少后续符号化负担。

1) __快照保留与最终选优__

- 每阶段保存 state_dict 到 CPU；
- 用“精度下限 + readiness score”选最终模型（可选 top-k 模型保留）。

### 2.2 引入训练安全封装，降低 pykan 常见失败率

`symkan.core.safe_fit` 对 `model.fit` 做了工程化兜底：

- 自动确保 `history.txt` 存在（处理部分环境下的路径问题）；
- `update_grid` 失败时自动降级重试；
- 训练异常返回空结果而不中断主流程。

这让长流水线在 notebook 和批处理场景都更稳。

### 2.3 归因计算加“安全调用路径”

`symkan.pruning.safe_attribute` 处理了归因前后状态与推理模式兼容：

- 先做前向刷新内部激活；
- `inference_mode` 触发特定错误时自动回退到 `no_grad`；
- 自动恢复模型 train/eval 状态；
- 若 `feature_score` 缺失，返回全 1 默认分数避免流程中断。

### 2.4 符号化从 `auto_symbolic` 升级为“严格分层流水线”

`symkan.symbolic.symbolize_pipeline` 并非简单调用 `auto_symbolic`，而是：

1) __先剪枝到可符号化规模__

- 多轮阈值剪枝（`max_prune_rounds` + threshold 序列）；
- 每轮可做短微调（`finetune_steps`）；
- 低精度保护：若精度跌破基线比例则回滚。

1) __再逐层符号拟合（严格 layer-wise）__

- 每层遍历活跃边，调用 `suggest_symbolic` 后立即 `fix_symbolic`；
- 不做跨层联合回归，保持层级可解释性；
- 每层 fix 后可做层间微调（`layerwise_finetune_steps`）。

1) __最后做强化微调（affine-heavy）__

- `affine_finetune_steps` + 学习率分段日程；
- 可启用早停（`heavy_ft_early_stop_*`）控制收益递减阶段耗时。

### 2.5 输入维度自动压缩（符号化前）

`_compact_inputs_for_symbolic` 会先识别第一层有效输入，再 `prune_input(active_inputs=...)`：

- 降低 `suggest_symbolic` 的候选边数量；
- 同步压缩 dataset；
- 符号化完成后恢复原始 `input_id` 映射。

这是一项对大输入维度任务非常关键的提速改进。

### 2.6 设备感知并行：并行只放在收益最高的位置

`_layerwise_symbolic_parallel` 仅并行 `suggest_symbolic`，`fix_symbolic` 仍串行：

- 避免并发修改模型状态导致不一致；
- 在 CPU 模式通常采用 4 workers；
- 在 CUDA 模式默认保守为 1 worker（避免线程开销/竞争抵消收益）；
- 任务量小于 `parallel_min_tasks` 时自动退化为串行。

### 2.7 低风险提速开关（主要面向论文批量实验）

`symbolize_pipeline` 提供三类“速度-风险”控制：

1) __剪枝评估降频__：`prune_eval_interval`

- 不是每轮都测精度，减少评估开销。

1) __归因采样分级__：`prune_attr_sample_adaptive`

- 根据当前边数与目标边数比例，动态选 `n_sample`（`min/max` 区间）。

1) __强化微调早停__：`heavy_ft_early_stop_patience/min_delta`

- 当提升不足时提前停止后期微调。

### 2.8 可观测性增强：不仅输出结果，还输出“过程证据”

`symbolize_pipeline` 返回：

- `trace`：每轮剪枝阈值、边数变化、精度轨迹；
- `timing`：剪枝轮耗时、逐层符号化耗时、各阶段 fit 耗时；
- `sym_stats`：活跃边、fix 数、低 R² 数、逐边 R² 记录、并行 worker 数；
- `effective_target_edges`、`effective_input_dim`：自动策略后的实际规模。

这解决了“结果可复现但过程不可解释”的常见问题。

### 2.9 边计数语义修正：区分原始边数与有效边数

新增 `_count_effective_edges`，联合 `act_fun.mask` 与 `symbolic_fun.mask` 统计有效连接：

- `final_n_edge_raw`：原始字段；
- `final_n_edge`：掩码语义下的有效边数。

对符号化后模型复杂度评估更准确。

### 2.10 函数库与表达式处理增强

`symkan.symbolic.library` 侧新增：

- 分层函数库：`LIB_HIDDEN` 与 `LIB_OUTPUT`；
- 自定义函数注册：`sigmoid`、`softplus` 注入 SYMBOLIC_LIB；
- 公式有效性筛选、复杂度计数、表达式格式化。

这让“函数搜索空间设计”从硬编码变成可配置策略。

### 2.11 数值验证更健壮，且带缓存

`symkan.eval.validate_formula_numerically`：

- 用 sympy lambdify 编译公式并缓存（第二次更快）；
- 对极值/NaN/Inf 做裁剪和替换，减少脆弱样本影响；
- 给出每个输出表达式的 R² 与数值稳定标记。

### 2.12 导出与复用链路补齐

`symkan.io` 提供：

- 模型克隆：优先内存深拷贝，失败回退 ckpt 克隆；
- 结果导出：summary/stage logs CSV、bundle pkl。

这让实验从 notebook 单次运行变为可复盘资产。

---

## 3. 与原生 kan 接口的一一对照

| 原生 kan 能力 | symkan 对应增强 | 实际收益 |
| --- | --- | --- |
| `fit` | `safe_fit` + `stagewise_train` | 稳定训练、可回滚、可选优 |
| `prune_edge` | 剪枝轮次调度 + 精度守护 + 自适应归因采样 | 更稳的稀疏化过程 |
| `suggest_symbolic/auto_symbolic` | 严格分层拟合 + 并行 suggest + 层间微调 | 速度与可解释性平衡 |
| `prune_input` | 自动输入压缩并回写映射 | 降低高维输入计算量 |
| `symbolic_formula` | 有效表达式筛选 + 数值一致性验证 | 公式可用性提升 |
| 无统一导出 | `io.results` 与 bundle | 实验可复盘、可批处理 |

---

## 4. 关键参数如何映射到改进点

### 4.1 训练阶段（`stagewise_train`）

- 稳定性：`steps_per_stage`、`post_prune_ft_steps`、`prune_acc_drop_tol`
- 稀疏目标：`target_edges`、`prune_edge_threshold_*`
- 选模偏好：`sym_target_edges`、`acc_weight`

### 4.2 符号化阶段（`symbolize_pipeline`）

- 结构复杂度：`target_edges`、`max_prune_rounds`
- 函数搜索：`lib_hidden/lib_output/lib`、`weight_simple`
- 提速开关：`parallel_mode`、`parallel_min_tasks`、`prune_eval_interval`
- 采样策略：`prune_attr_sample_adaptive`、`prune_attr_sample_min/max`
- 后期收敛：`affine_finetune_steps`、`affine_finetune_lr_schedule`
- 早停：`heavy_ft_early_stop_patience/min_delta`

### 4.3 `lib` 参数说明（新增）

`symbolize_pipeline` 的函数库参数优先级如下：

1. 若传入 `lib`，则所有层统一使用该库；
2. 若 `lib is None`，则按层使用 `lib_hidden` 与 `lib_output`；
3. 若分层库也为空，则回退到默认 `LIB_HIDDEN/LIB_OUTPUT`。

当前可直接使用的预设库：

- `LIB_HIDDEN`：默认隐藏层函数库：`[x, x^2, tanh]`。
- `LIB_OUTPUT`：默认输出层函数库：`[x, x^2]`。
- `FAST_LIB`：速度优先小型库：`[x, x^2, tanh, sin, cos, exp, log, sqrt]`。
- `EXPRESSIVE_LIB`：全量候选符号库（自动对齐 kan 原生 `SYMBOLIC_LIB`），当前包含：
    `[x, x^2, x^3, x^4, x^5, 1/x, 1/x^2, 1/x^3, 1/x^4, 1/x^5, sqrt, x^0.5, x^1.5, 1/sqrt(x), 1/x^0.5, exp, log, abs, sin, cos, tan, tanh, sgn, arcsin, arccos, arctan, arctanh, 0, gaussian]`。
- `FULL_LIB`：`EXPRESSIVE_LIB` 的别名（便于旧代码迁移）。

补充：`sigmoid`、`softplus` 已在 `register_custom_functions()` 中注册，可手工加入你的 `lib` 列表（默认不在 `EXPRESSIVE_LIB` 内）。

推荐用法示例：

```python
from symkan.symbolic import LIB_HIDDEN, LIB_OUTPUT, FAST_LIB, EXPRESSIVE_LIB

# 方案A：分层库（默认推荐，适用于分类任务）
symbolize_pipeline(model, dataset, lib=None, lib_hidden=LIB_HIDDEN, lib_output=LIB_OUTPUT)

# 方案B：统一快速库（速度优先）
symbolize_pipeline(model, dataset, lib=FAST_LIB)

# 方案C：统一全量表达库（表达能力优先）
symbolize_pipeline(model, dataset, lib=EXPRESSIVE_LIB)
```

实务建议：

- 先用分层库（方案A）获得稳定可解释结果；
- 若表达式能力不足，再切换到 `EXPRESSIVE_LIB`；
- 使用全量库时可同步提高 `weight_simple`，抑制过复杂函数被优先选中。

---

## 5. 返回字段应该怎么读（论文表格高频）

- `final_acc`：最终分类精度。
- `final_n_edge`：有效边数（推荐用于复杂度主指标）。
- `final_n_edge_raw`：原始边计数字段（用于对照）。
- `effective_target_edges`：目标边数自动修正后的值。
- `effective_input_dim`：输入压缩后实际参与符号化的维度。
- `sym_stats.fixed / sym_stats.low_r2`：符号替换规模与风险点。
- `trace`：剪枝全过程轨迹（建议直接导 CSV）。
- `timing.symbolic_total_seconds`：符号化总耗时。
- `timing.symbolic_layers`：逐层耗时与 fix 数（可做瓶颈分析）。

---

## 6. 快速开始（与当前 notebook 一致）

```python
import numpy as np
from symkan.core import set_device, get_device, build_dataset
from symkan.tuning import stagewise_train
from symkan.symbolic import symbolize_pipeline, LIB_HIDDEN, LIB_OUTPUT

set_device('cuda')  # 或 'cpu'
print('device =', get_device())

X_train = np.load('X_train.npy').astype(np.float32)
X_test  = np.load('X_test.npy').astype(np.float32)
Y_train = np.load('Y_train_cat.npy').astype(np.float32)
Y_test  = np.load('Y_test_cat.npy').astype(np.float32)

dataset = build_dataset(X_train, Y_train, X_test, Y_test)
best_model, train_res = stagewise_train(
    dataset,
    width=[X_train.shape[1], 16, Y_train.shape[1]],
    grid=5,
    k=3,
    steps_per_stage=60,
    target_edges=120,
    sym_target_edges=50,
    acc_weight=0.5,
    batch_size=None,
    verbose=True,
)

export_res = symbolize_pipeline(
    best_model,
    dataset,
    target_edges=90,
    max_prune_rounds=30,
    lib_hidden=LIB_HIDDEN,
    lib_output=LIB_OUTPUT,
    weight_simple=0.10,
    finetune_steps=50,
    finetune_lr=0.0005,
    layerwise_finetune_steps=120,
    affine_finetune_steps=200,
    affine_finetune_lr_schedule=[0.003, 0.001, 0.0005, 0.0002],
    parallel_mode='auto',
    parallel_workers=None,
    parallel_min_tasks=16,
    prune_eval_interval=2,
    prune_attr_sample_adaptive=True,
    prune_attr_sample_min=768,
    prune_attr_sample_max=2048,
    heavy_ft_early_stop_patience=2,
    heavy_ft_early_stop_min_delta=5e-4,
    collect_timing=True,
    verbose=True,
)

print('final_acc =', export_res['final_acc'])
print('final_n_edge =', export_res['final_n_edge'])
print('symbolic_t =', export_res['timing'].get('symbolic_total_seconds'))
```

---

## 7. 推荐工作流（论文/实验）

1. `build_dataset` + `set_device`，先固定设备与数据张量化路径。  
2. `stagewise_train`，记录 `selected_stage/selected_score/selected_edges`。  
3. `symbolize_pipeline`，重点留存 `trace/sym_stats/timing`。  
4. `validate_formula_numerically` + `compute_multiclass_roc_auc` 做可靠性补充评估。  
5. `save_symbolic_summary` + `save_export_bundle` 做结果归档。  

---

## 8. FAQ（结合当前实现）

### Q1：并行只有 1.05x~1.10x 正常吗？

正常。并行主要覆盖 `suggest_symbolic`，剪枝、微调和评估仍是主要耗时。

### Q2：为什么符号化后精度可能下降？

本质是稀疏化 + 函数离散化 + 复杂度偏好共同作用。可提高 `target_edges`、`layerwise_finetune_steps`、`affine_finetune_steps` 缓解。

### Q3：`validate_formula_numerically` 第二次更快是否正常？

正常，表达式编译存在缓存。

### Q4：归因偶发异常如何处理？

`safe_attribute` 已包含推理模式回退与默认分数兜底，通常重跑即可恢复。

---

## 9. 配套文件

- 主实验：`kan.ipynb`
- 参数说明：`doc/kan_parameters.md`

建议先在 notebook 跑通单次流程，再迁移到脚本化批处理，以便稳定复现实验表格。
