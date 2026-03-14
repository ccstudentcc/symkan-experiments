# symkan-experiments

symkan 是构建在 pykan 之上的工程化符号化工作流。它不改写 KAN 的核心表达能力，而是把训练、剪枝、符号化、评估和导出串成一条可复现的流水线，方便论文实验和批量对比。

## 快速安装

推荐环境：Python 3.9，CUDA 可选。

```bash
pip install -r requirements.txt
```

关键依赖包括：`torch`、`pykan`、`sympy`、`scikit-learn`、`pandas`、`matplotlib`。

## 数据准备

`kan.ipynb` 与 `symkanbenchmark.py` 默认优先读取以下数据文件：

- `X_train.npy`
- `X_test.npy`
- `Y_train_cat.npy`
- `Y_test_cat.npy`

若文件缺失，会自动按 SymbolNet 风格获取 MNIST 并生成同名 `*.npy` 文件（优先 `tensorflow.keras.datasets.mnist`，回退 `sklearn.fetch_openml("mnist_784")`）。

## 快速开始

下面的例子展示最短闭环：构建数据集，分阶段训练，再执行符号化。

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

set_device("cuda")
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

print(symbolic_result["final_acc"])
print(symbolic_result["final_n_edge"])
print(symbolic_result["valid_expressions"])

validation_df = validate_formula_numerically(
	symbolic_result["model"],
	symbolic_result["formulas"],
	dataset,
)
print(validation_df.head() if validation_df is not None else "No valid formulas")
```

## 核心流程

```mermaid
%%{
  init: {
    "theme": "base",
    "themeVariables": {
      "fontFamily": "Inter, system-ui, -apple-system, sans-serif",
      "fontSize": "10px",
      "textColor": "#334155",
      "lineColor": "#94a3b8",
      "clusterBkg": "#f8fafc"
    },
    "flowchart": {
      "curve": "basis",
      "nodeSpacing": 30,
      "rankSpacing": 40
    }
  }
}%%
flowchart TB
  %% 现代扁平化配色：蓝色(数据/准备) -> 紫色(核心算法) -> 青绿(输出结果)
  classDef nodeBlue fill:#eff6ff,stroke:#3b82f6,stroke-width:2px,color:#1e40af,rx:8,ry:8
  classDef nodePurple fill:#faf5ff,stroke:#a855f7,stroke-width:2px,color:#6b21a8,rx:8,ry:8
  classDef nodeTeal fill:#f0fdfa,stroke:#14b8a6,stroke-width:2px,color:#0f766e,rx:8,ry:8
  classDef highlight fill:#fffbeb,stroke:#f59e0b,stroke-width:2.5px,color:#92400e,rx:8,ry:8

  %% 左列：训练准备
  subgraph Phase1_A["第一阶段 1/2：训练与准备"]
    direction TB
    A["Raw Data X, Y<br>原始数据"]:::nodeBlue -->|输入| B["build_dataset<br>构建数据集"]:::nodeBlue
    B -->|训练| C["stagewise_train<br>分阶段训练"]:::nodeBlue
    C -->|保存| D["Best KAN Snapshot<br>最优 KAN 快照"]:::highlight
  end

  %% 中列：核心流水线
  subgraph Phase1_B["第一阶段 2/2：符号化流水线"]
    direction TB
    E1["1. Progressive Pruning<br>渐进剪枝"]:::nodePurple --> E2["2. Input Compaction<br>压缩输入维度"]:::nodePurple
    E2 --> E3["3. Layer-wise Symbolic Search<br>逐层候选函数搜索"]:::nodePurple
    E3 --> E4["4. Affine-heavy Finetune<br>仿射参数强化微调"]:::nodePurple
  end

  %% 右列：验证与导出
  subgraph Phase2["第二阶段：输出与导出"]
    direction TB
    F["symbolic_formula<br>符号公式"]:::nodeTeal -->|验证| G["validate_numerically<br>数值验证"]:::nodeTeal
    H["trace / sym_stats<br>耗时与统计"]:::nodeTeal -->|日志写入| I["Export: CSV / PKL<br>导出结果"]:::nodeTeal
    G -->|结果写入| I
  end

  %% 跨列的粗线条引导逻辑
  D ==>|转入流水线| E1
  E4 ==>|公式输出| F
  E4 ==>|日志输出| H

  %% 子图虚线边框及柔和背景
  style Phase1_A fill:#f8fafc,stroke:#cbd5e1,stroke-width:2px,stroke-dasharray: 6 4,rx:12,ry:12
  style Phase1_B fill:#fdf4ff,stroke:#e879f9,stroke-width:2px,stroke-dasharray: 6 4,rx:12,ry:12
  style Phase2 fill:#f0fdf4,stroke:#86efac,stroke-width:2px,stroke-dasharray: 6 4,rx:12,ry:12
```

## 包结构

- `symkan.core`: 设备管理、数据构建、训练封装、推理与结构化类型。
- `symkan.tuning`: 分阶段训练、验证集驱动剪枝、自适应阈值和选模。
- `symkan.symbolic`: 函数库、输入压缩、逐层符号搜索和主流水线。
- `symkan.pruning`: 容错归因入口。
- `symkan.eval`: 公式数值验证和 ROC/AUC 评估。
- `symkan.io`: 模型克隆、结果导出与 bundle 读写。

## 设计要点

- `stagewise_train` 负责把模型推到适合符号化的稀疏区间，而不是一开始就追求最终公式。
- `symbolize_pipeline` 负责把连续样条函数离散成解析式，并在每个阶段做精度保护。
- 所有公开入口优先保持向后兼容，结构化报告版本通过 `*_report` 额外提供，而不是替换旧返回值。

## 默认策略（2026-03）

基于 `benchmark_ablation/` 与 `benchmark_ab/comparison/` 的最新实验，推荐默认配置如下：

- `stagewise_train`：保持开启（关闭会显著破坏可符号化入口质量）。
- 渐进剪枝：保持开启（主要收益是复杂度和时延治理，而非稳定提精度）。
- 输入压缩：默认开启（关闭常可改善部分公式 R2，但会增加搜索维度与耗时）。
- 典型 2 层 KAN：默认关闭 LayerwiseFT（即 `layerwise_finetune_steps=0`），仅在专门对照实验中再开启改进版参数。

一句话：默认配置优先“可复现 + 吞吐 + 兼容”，不承诺单次 seed 的偶然最高分。

更完整的设计原因见 `docs/design.md`。

## 相关文档

- `docs/kan_parameters.md`: notebook 实验参数和调参顺序说明。
- `docs/symkan_usage.md`: 更完整的使用说明和实验背景。
- `docs/symkanbenchmark_usage.md`: benchmark 工具说明。
- `docs/design.md`: 设计动机、阶段划分和算法选型说明。
