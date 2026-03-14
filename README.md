# symkan-experiments

symkan 是构建在 pykan 之上的工程化符号化工作流。你可以把它理解成一条“能稳定复现”的流水线：训练 KAN、逐步剪枝、生成符号表达式、做数值验证、导出报告文件。

如果你是第一次使用这个仓库，先看“3 分钟上手”，再看“结果怎么看”和“常见报错”。

## 目录

- [symkan-experiments](#symkan-experiments)
  - [目录](#目录)
  - [0. 快速导航（按你的目标）](#0-快速导航按你的目标)
  - [1. 项目简介：用途、优势与适用场景](#1-项目简介用途优势与适用场景)
    - [1.1 解决的问题](#11-解决的问题)
    - [1.2 symkan 的实际用途](#12-symkan-的实际用途)
    - [1.3 相比直接用 pykan 的优势](#13-相比直接用-pykan-的优势)
  - [2. 3 分钟上手（新手必读）](#2-3-分钟上手新手必读)
  - [3. 安装与环境检查](#3-安装与环境检查)
  - [4. 数据准备](#4-数据准备)
  - [5. 第一次跑通：最短闭环代码](#5-第一次跑通最短闭环代码)
  - [6. 跑完后先看什么结果](#6-跑完后先看什么结果)
  - [7. 默认策略（2026-03，附原因）](#7-默认策略2026-03附原因)
  - [8. 常用命令（完整清单）](#8-常用命令完整清单)
  - [9. 包结构与兼容原则](#9-包结构与兼容原则)
  - [10. 进阶阅读](#10-进阶阅读)
  - [11. 常见报错与排查](#11-常见报错与排查)
    - [11.1 `ModuleNotFoundError`（例如 `kan`、`symkan`、`sympy`）](#111-modulenotfounderror例如-kansymkansympy)
    - [11.2 `python` 或 `pip` 命令不可用](#112-python-或-pip-命令不可用)
    - [11.3 首次运行很慢或卡在下载](#113-首次运行很慢或卡在下载)
    - [11.4 `FileNotFoundError`（找不到 `X_train.npy` 等文件）](#114-filenotfounderror找不到-x_trainnpy-等文件)
    - [11.5 标签形状或类别维度报错（shape mismatch）](#115-标签形状或类别维度报错shape-mismatch)
    - [11.6 CUDA 可见但实际未使用，或报显存不足（OOM）](#116-cuda-可见但实际未使用或报显存不足oom)
    - [11.7 Notebook 能跑、脚本不能跑（或反过来）](#117-notebook-能跑脚本不能跑或反过来)
    - [11.8 并行模式没有明显加速](#118-并行模式没有明显加速)
    - [11.9 结果波动大，看不出哪个配置更好](#119-结果波动大看不出哪个配置更好)
    - [11.10 `benchmark_ab_compare.py` 运行失败](#1110-benchmark_ab_comparepy-运行失败)
    - [11.11 消融脚本聚合失败（`ablation_runner.py --aggregate-only`）](#1111-消融脚本聚合失败ablation_runnerpy---aggregate-only)
    - [11.12 结果文件被覆盖或难以追溯](#1112-结果文件被覆盖或难以追溯)
  - [12. 术语速查](#12-术语速查)

## 0. 快速导航（按你的目标）

如果你是第一次接触这个仓库，建议按下面路径读：

1. 想快速跑通一次：先看 [2. 3 分钟上手](#2-3-分钟上手新手必读) -> 再看 [6. 跑完后先看什么结果](#6-跑完后先看什么结果)。
2. 想批量复现实验：先跑 [8. 常用命令](#8-常用命令完整清单) 的 full，再读 [`docs/symkanbenchmark_usage.md`](docs/symkanbenchmark_usage.md)。
3. 想理解方法与设计动机：先看 [1. 项目简介](#1-项目简介用途优势与适用场景)，再读 [`docs/symkan_usage.md`](docs/symkan_usage.md) 与 [`docs/design.md`](docs/design.md)。
4. 想写论文/做消融：先看 [7. 默认策略](#7-默认策略2026-03附原因)，再读 [`docs/ablation_usage.md`](docs/ablation_usage.md) 与 [`docs/ablation_report.md`](docs/ablation_report.md)。
5. 想调参：直接看 [`docs/kan_parameters.md`](docs/kan_parameters.md)。
6. 不确定从哪篇开始：直接打开 [`docs/index.md`](docs/index.md)。

## 1. 项目简介：用途、优势与适用场景

### 1.1 解决的问题

在 KAN 实验实践中，常见痛点通常是：

1. 参数调整后结果波动大，复现成本高。
2. 实验产物分散在终端与临时文件，难以追溯。
3. 符号化策略缺少保护机制，容易在压缩时引入明显精度损失。

### 1.2 symkan 的实际用途

symkan 面向以下工作场景：

1. 论文实验：需要多 seed 对比、结果可回溯、指标可复核。
2. 可解释建模：需要将神经网络近似转换为可读解析式。
3. 工程调参：需要稳定的阶段日志与统一导出格式。

### 1.3 相比直接用 pykan 的优势

1. 训练阶段可控：`stagewise_train` 提供阶段化训练、剪枝保护和回滚逻辑。
2. 符号化链路可控：`symbolize_pipeline` 将剪枝、压缩、逐层符号化、微调拆解为可观测步骤。
3. 实验结果可复用：默认输出 CSV/trace/summary，便于后续统计分析和写作引用。
4. 策略口径统一：基于 `kan.ipynb` 与 `docs/` 实验结论给出可解释的默认配置。

如果你希望先看完整方法背景（含 KAN 与符号化关系、流程图、API 分层），建议继续阅读 [`docs/symkan_usage.md`](docs/symkan_usage.md)。

## 2. 3 分钟上手（新手必读）

按顺序做这 3 步，通常就能跑起来：

1. 安装依赖

推荐版本：Python 3.9.25

```bash
pip install -r requirements.txt
```

1. 跑主流程（含多 seed）

```bash
python symkanbenchmark.py --tasks full --stagewise-seeds 42,52,62 --quiet
```

3. 看结果文件

- `benchmark_runs/symkanbenchmark_runs.csv`：主指标汇总。
- `benchmark_runs/run_01_seed42/kan_stage_logs.csv`：阶段训练日志。
- `benchmark_runs/run_01_seed42/symbolize_trace.csv`：符号化剪枝轨迹。

如果你只想快速体验单次流程，也可以直接打开 `kan.ipynb` 逐单元运行。

如果你已经在 conda 环境管理 Python，建议先激活项目环境再执行命令。

若你准备长期复现，建议直接用同一环境执行全部命令，避免混用解释器导致依赖漂移。

## 3. 安装与环境检查

推荐环境：Python 3.9（CUDA 可选）。

```bash
pip install -r requirements.txt
```

关键依赖：`torch`、`pykan`、`sympy`、`scikit-learn`、`pandas`、`matplotlib`。

安装后建议执行自检：

```python
import torch
import kan
import symkan

print("torch:", torch.__version__)
print("symkan import ok")
```

## 4. 数据准备

`kan.ipynb` 和 `symkanbenchmark.py` 默认优先读取以下文件：

- `X_train.npy`
- `X_test.npy`
- `Y_train_cat.npy`
- `Y_test_cat.npy`

若缺失，会自动下载并生成同名文件：

1. 优先 `tensorflow.keras.datasets.mnist`
2. 回退 `sklearn.fetch_openml("mnist_784")`

新手提示：第一次自动下载可能较慢，这是正常现象。

如果你已有预处理数据，放置在仓库根目录并保持文件名一致即可跳过下载。

## 5. 第一次跑通：最短闭环代码

下面代码覆盖完整最小链路：构建数据集 -> 分阶段训练 -> 符号化 -> 公式数值验证。

```python
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

from symkan.core import build_dataset, set_device
from symkan.tuning import stagewise_train
from symkan.symbolic import LIB_HIDDEN, LIB_OUTPUT, symbolize_pipeline
from symkan.eval import validate_formula_numerically

X, y = make_classification(
    n_samples=1200,
    n_features=10,
    n_informative=6,
    n_redundant=2,
    n_classes=3,
    random_state=42,
)
X = X.astype(np.float32)
Y = np.eye(3, dtype=np.float32)[y]

X_train, X_test, Y_train, Y_test = train_test_split(
    X, Y, test_size=0.2, random_state=42, stratify=y
)

set_device("cuda")  # 无 GPU 时改为 "cpu"
dataset = build_dataset(
    X_train,
    Y_train,
    X_test,
    Y_test,
    validation_ratio=0.15,
    seed=42,
)

best_model, train_result = stagewise_train(
    dataset=dataset,
    width=[X_train.shape[1], 16, Y_train.shape[1]],
    steps_per_stage=60,
    target_edges=120,
    sym_target_edges=60,
    use_validation=True,
    adaptive_threshold=True,
    verbose=False,
)

symbolic_result = symbolize_pipeline(
    model=best_model,
    dataset=dataset,
    target_edges=90,
    max_prune_rounds=20,
    lib_hidden=LIB_HIDDEN,
    lib_output=LIB_OUTPUT,
    layerwise_finetune_steps=0,
    affine_finetune_steps=200,
    prune_adaptive_threshold=True,
    collect_timing=True,
    verbose=False,
)

print("final_acc:", symbolic_result["final_acc"])
print("final_n_edge:", symbolic_result["final_n_edge"])
print("valid_expressions:", len(symbolic_result["valid_expressions"]))

validation_df = validate_formula_numerically(
    symbolic_result["model"],
    symbolic_result["formulas"],
    dataset,
)
print(validation_df.head() if validation_df is not None else "No valid formulas")
```

## 6. 跑完后先看什么结果

新手最容易迷路的点是“跑完了，但不知道结果是不是正常”。先看这 5 项：

1. `final_acc`：最终分类精度。
2. `macro_auc`：多分类整体 AUC。
3. `final_n_edge`：最终边数，反映表达式规模。
4. `validation_mean_r2`：公式数值拟合质量。
5. `symbolic_total_seconds`：符号化总耗时。

对应输出文件建议：

- `benchmark_runs/symkanbenchmark_runs.csv`
- `benchmark_runs/run_01_seed42/formula_validation.csv`
- `benchmark_runs/run_01_seed42/symbolize_trace.csv`

建议判断顺序：

1. 先看 `final_acc` 与 `macro_auc`，确认分类质量。
2. 再看 `final_n_edge` 与 `symbolic_total_seconds`，评估复杂度与开销。
3. 最后看 `validation_mean_r2`，判断符号表达式的数值一致性。

## 7. 默认策略（2026-03，附原因）

这部分是“项目推荐默认”，用于统一口径，不等于所有 CLI 的技术默认值。

基于 `kan.ipynb` 最新产物、`benchmark_ablation/` 与 `benchmark_ab/comparison/`：

1. `stagewise_train` 必开。
   关闭后 `final_acc 0.7807 -> 0.4430`，`macro_auc 0.9548 -> 0.8379`，基本不可用。
2. 渐进剪枝默认开启。
   主要负责复杂度与时延治理；关闭后复杂度 `126.90 -> 194.33`，符号化耗时 `33.58s -> 43.51s`。
3. 输入压缩默认开启。
   关闭后 `R2 -0.6135 -> +0.0275` 可能变好，但维度 `57.67 -> 120.00` 且更慢。
4. 典型 2 层 KAN 默认关闭 LayerwiseFT（`layerwise_finetune_steps=0`）。
   分类指标变化很小，但耗时明显下降（`33.58s -> 20.41s`）。

一句话：默认配置优先“稳定复现 + 可控成本”，不是追求单次最高分。

口径说明：

1. 这里的“默认策略”是项目推荐配置。
2. CLI 的技术默认值可能不同，实验复现时应显式传参。

补充：CLI 参数技术默认值、A/B 结论口径和报告字段定义，请以 [`docs/symkanbenchmark_usage.md`](docs/symkanbenchmark_usage.md) 为准。

## 8. 常用命令（完整清单）

主实验：

```bash
python symkanbenchmark.py --tasks full --stagewise-seeds 42,52,62 --quiet
```

主实验（指定输出目录）：

```bash
python symkanbenchmark.py --tasks full --stagewise-seeds 42,52,62 --output-dir benchmark_runs_exp1 --quiet
```

一次跑完整流程（full + eval-bench + parallel-bench）：

```bash
python symkanbenchmark.py --tasks all --stagewise-seeds 42,52,62 --quiet
```

评估链路测速：

```bash
python symkanbenchmark.py --tasks eval-bench
```

并行策略对照：

```bash
python symkanbenchmark.py --tasks parallel-bench --parallel-modes auto,off,thread4
```

只运行 notebook（交互式）：

```bash
jupyter lab kan.ipynb
```

A/B 汇总对比：

```bash
python benchmark_ab_compare.py --root benchmark_ab --baseline baseline --variants adaptive,adaptive_auto --output benchmark_ab/comparison
```

单点消融：

```bash
python ablation_runner.py --stagewise-seeds 42,52,62 --global-seed 123 --quiet
```

只聚合已有消融结果：

```bash
python ablation_runner.py --aggregate-only --output-dir benchmark_ablation
```

LayerwiseFT 对比分析（已有结果）：

```bash
python analyze_layerwiseft.py --ablation-dir benchmark_ablation --seeds 42,52,62
```

LayerwiseFT 改进版对比（含运行）：

```bash
python compare_layerwiseft_improved.py --ablation-dir benchmark_ablation --seeds 42,52,62 --quiet
```

LayerwiseFT 改进版对比（只汇总，不重跑）：

```bash
python compare_layerwiseft_improved.py --ablation-dir benchmark_ablation --seeds 42,52,62 --skip-run
```

参数说明和更多命令模板请看：

- [`docs/symkanbenchmark_usage.md`](docs/symkanbenchmark_usage.md)
- [`docs/ablation_usage.md`](docs/ablation_usage.md)

## 9. 包结构与兼容原则

- `symkan.core`：设备管理、数据构建、训练封装、推理与结构化类型。
- `symkan.tuning`：分阶段训练、验证集驱动剪枝、自适应阈值和选模。
- `symkan.symbolic`：函数库、输入压缩、逐层符号搜索和主流水线。
- `symkan.pruning`：容错归因入口。
- `symkan.eval`：公式数值验证和 ROC/AUC 评估。
- `symkan.io`：模型克隆、结果导出与 bundle 读写。

兼容原则：

1. 公开入口优先保持向后兼容。
2. 新能力通过 `*_report` 补充，不破坏旧返回值。

## 10. 进阶阅读

先看文档总入口：[`docs/index.md`](docs/index.md)

- [`docs/symkan_usage.md`](docs/symkan_usage.md)：完整使用说明、理论背景、核心 API 与流程图。
- [`docs/design.md`](docs/design.md)：设计动机、阶段划分、算法取舍与兼容原则。
- [`docs/symkanbenchmark_usage.md`](docs/symkanbenchmark_usage.md)：benchmark 参数、输出含义与 A/B 结论写作口径。
- [`docs/kan_parameters.md`](docs/kan_parameters.md)：`kan.ipynb` 参数解释与推荐调参顺序。
- [`docs/ablation_usage.md`](docs/ablation_usage.md)：消融脚本、命令模板与输出结构。
- [`docs/ablation_report.md`](docs/ablation_report.md)：当前消融实验结论总览。
- [`docs/layerwiseft_improved_report.md`](docs/layerwiseft_improved_report.md)：LayerwiseFT 改进版对比报告。

建议阅读顺序：

1. 新用户：`symkan_usage` -> `symkanbenchmark_usage`。
2. 调参与复现：`kan_parameters` -> `ablation_usage`。
3. 写作与方法论：`design` -> `ablation_report` -> `layerwiseft_improved_report`。

## 11. 常见报错与排查

### 11.1 `ModuleNotFoundError`（例如 `kan`、`symkan`、`sympy`）

原因：解释器与安装依赖不在同一环境，或依赖未完整安装。

处理：

1. 先确认当前 Python 路径与预期环境一致。
2. 在同一环境重新执行 `pip install -r requirements.txt`。
3. 运行第 3 节“环境检查”代码验证导入是否恢复。

### 11.2 `python` 或 `pip` 命令不可用

原因：Python 未加入 PATH，或终端未激活 conda/venv。

处理：

1. 先激活你的项目环境再执行命令。
2. 使用 `python -m pip install -r requirements.txt`，避免 `pip` 指向错误环境。
3. 若仍报错，检查系统是否已正确安装 Python。

### 11.3 首次运行很慢或卡在下载

原因：自动下载 MNIST、首次编译或缓存构建。

处理：

1. 首次运行适当等待，避免中途中断。
2. 确认网络可访问数据源。
3. 第二次运行通常会明显变快。

### 11.4 `FileNotFoundError`（找不到 `X_train.npy` 等文件）

原因：数据文件不在仓库根目录，或文件名不匹配。

处理：

1. 确认四个文件名与大小写完全一致：`X_train.npy`、`X_test.npy`、`Y_train_cat.npy`、`Y_test_cat.npy`。
2. 若你想走自动下载流程，删除不完整文件后重跑主命令。
3. 若你用自定义数据，确保放在仓库根目录且格式兼容。

### 11.5 标签形状或类别维度报错（shape mismatch）

原因：`Y` 不是 one-hot，或训练/测试集类别维度不一致。

处理：

1. 确认标签格式为 one-hot，且 train/test 的列数一致。
2. 确认 `width` 最后一维与类别数一致。
3. 先用第 5 节最小示例跑通，再迁移到你的数据。

### 11.6 CUDA 可见但实际未使用，或报显存不足（OOM）

原因：设备选择与环境不一致，或 batch/参数设置过大。

处理：

1. 显式设置 `set_device("cpu")` 验证流程可运行，再切回 GPU。
2. 降低批大小或减少训练步数、目标边数。
3. 并行实验先用 `off` 或更小线程数，避免额外内存开销。

### 11.7 Notebook 能跑、脚本不能跑（或反过来）

原因：Jupyter 内核与终端 Python 不是同一环境。

处理：

1. 在 Notebook 和终端分别打印 Python 路径并对比。
2. 保证两边都使用同一 conda/venv 环境。
3. 统一后再执行 benchmark，避免“同代码不同结果”。

### 11.8 并行模式没有明显加速

原因：当前并行只覆盖部分符号搜索，小规模任务时线程开销可能抵消收益。

处理：

1. 把并行实验与主实验分开看，不要混在同一结论里。
2. 用 `benchmark_symbolic_parallel_quick.csv` 的 `vs_off_speedup_x` 判断是否真正加速。
3. 优先在更大任务规模下评估并行收益。

### 11.9 结果波动大，看不出哪个配置更好

原因：单 seed 偶然性高。

处理：

1. 至少跑 3 个 seed（建议 `42,52,62`）。
2. 同时报均值、标准差和胜负计数（win/lose/tie）。
3. 不要只报告最好一次结果。

### 11.10 `benchmark_ab_compare.py` 运行失败

常见原因：

1. 输入目录缺少某个 variant 的 `symkanbenchmark_runs.csv`。
2. `--baseline` 或 `--variants` 名称与目录名不一致。
3. 前序 full 实验未完成，导致汇总输入不完整。

处理：

1. 检查 `benchmark_ab/<variant>/` 目录结构是否完整。
2. 先分别完成 baseline 与 variant 的 full。
3. 再执行 compare 脚本做汇总。

### 11.11 消融脚本聚合失败（`ablation_runner.py --aggregate-only`）

原因：某些变体目录存在，但关键 CSV 缺失或列不完整。

处理：

1. 检查 `benchmark_ablation/<variant>/symkanbenchmark_runs.csv` 是否存在。
2. 对缺失变体先补跑对应实验。
3. 再执行聚合命令。

### 11.12 结果文件被覆盖或难以追溯

原因：多次运行共用同一输出目录。

处理：

1. 每次实验显式传 `--output-dir`（例如 `benchmark_runs_exp1`）。
2. 对 A/B、ablation 使用固定目录命名规则。
3. 保留 `run_*` 子目录，不要手动混拷文件。

更多参数级排查可查：[`docs/symkanbenchmark_usage.md`](docs/symkanbenchmark_usage.md) 与 [`docs/ablation_usage.md`](docs/ablation_usage.md)。

## 12. 术语速查

训练与选模：

- Stagewise training：分阶段训练，并在阶段间执行剪枝与回滚保护。
- Sym readiness score：综合精度与稀疏度的选模分数，用于挑选更适合符号化的快照。
- Stage early stop：阶段早停策略；当连续阶段收益不足时提前停止，避免无效训练。
- Validation-driven training：用验证集而非仅训练集来驱动剪枝和选模，降低过拟合风险。

剪枝与结构控制：

- Progressive pruning：多轮渐进剪枝，不是一次性强剪。
- Adaptive threshold：根据近期精度跌幅与边数收益动态调整剪枝阈值。
- Threshold backoff：当某轮剪枝过猛时，回退阈值以降低破坏性。
- Max drop ratio per round：单轮允许的最大性能回落比例，防止一次剪穿。
- Input compaction：删除失活输入维度，降低后续符号搜索成本。
- Effective target edges：流水线自适应后实际采用的目标边数，可能与传入值不同。
- Effective input dim：输入压缩后保留的实际维度数。

符号化与微调：

- Symbolize pipeline：从渐进剪枝到逐层符号化再到强化微调的完整主流程。
- Layer-wise symbolic search：按层执行候选函数搜索与固定，降低全局状态污染风险。
- LayerwiseFT：逐层符号化后的短微调；对典型 2 层 KAN 常作为可选开关。
- Affine finetune：在函数族固定后，重点优化仿射参数以恢复精度。
- Symbolic formula：把样条近似替换为解析表达式后得到的公式集合。
- Valid expressions：通过有效性筛选后可用于验证和导出的表达式子集。

评估与结果解读：

- Final acc：符号化后模型在测试集上的最终分类准确率。
- Macro AUC：多分类任务中对各类 AUC 的宏平均。
- Final n_edge：符号化后模型剩余边数，反映复杂度。
- Validation mean R2：公式输出与模型输出数值一致性的平均 R2。
- Symbolic total seconds：符号化全流程总耗时。
- Trace：每轮剪枝与微调的关键轨迹表（边数、精度、耗时等）。
- Sym stats：符号搜索统计（如 fixed 条目数、低 R2 条目数等）。

实验与复现：

- Baseline / adaptive / adaptive_auto：三组常见 A/B 方案，分别对应无自适应、部分自适应、带早停与节奏控制的自适应。
- Seedwise comparison：按 seed 逐一对比差分，避免只看均值掩盖波动。
- Win / lose / tie：与基线逐 seed 比较得到的胜负计数口径。
- Bundle export：将指标、轨迹、公式与配置打包导出，便于复现与审计。
