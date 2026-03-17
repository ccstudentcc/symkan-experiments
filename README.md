# symkan-experiments

`symkan-experiments` 是一个面向 KAN 符号化实验的工程化仓库。其目标是在 `pykan` 基础上提供较稳定的实验流程、结果导出与复现支持。

训练 KAN -> 逐步剪枝 -> 符号化 -> 数值验证 -> 导出结构化结果 -> 批量复现实验

阅读仓库时，可先参考以下三份文档：

1. [docs/project_map.md](docs/project_map.md)：项目地图，先知道仓库里每个目录和脚本负责什么。
2. [docs/symkan_usage.md](docs/symkan_usage.md)：核心库 `symkan/` 的使用方式和方法背景。
3. [docs/symkanbenchmark_usage.md](docs/symkanbenchmark_usage.md)：批量实验脚本怎么跑、结果怎么读。

## 项目背景

在基于 `pykan` 的探索性实验基础上，进入批量复现或论文写作阶段时，通常会遇到以下问题：

- 训练、剪枝、符号化混在一起，流程不可控。
- 结果散落在 notebook 输出和临时文件里，难以追溯。
- 参数很多，但缺少统一口径，不知道哪些是技术默认值，哪些是项目层研究设定。
- 单次 seed 看起来很好，换个 seed 结论就变。

本仓库的基本思路是先统一数据结构、输出格式和实验入口，再在此基础上组织训练、剪枝、符号化和评估流程。核心模块 `symkan/` 提供训练、符号化、评估和导出接口；根目录脚本负责批量实验、A/B 对比和消融分析。

## 文档路径

可按使用目的选择以下阅读路径：

- 项目结构：读 [docs/project_map.md](docs/project_map.md)。
- 最小示例：读 [docs/symkan_usage.md](docs/symkan_usage.md) 第 4 节。
- 实验复现：读 [docs/symkanbenchmark_usage.md](docs/symkanbenchmark_usage.md)。
- 设计依据：读 [docs/design.md](docs/design.md)。
- 单因素消融：读 [docs/ablation_usage.md](docs/ablation_usage.md)。
- 结果报告：读 [docs/ablation_report.md](docs/ablation_report.md) 和 [docs/layerwiseft_improved_report.md](docs/layerwiseft_improved_report.md)。

## 基本运行

运行环境：Python 3.9。

```bash
pip install -r requirements.txt
python symkanbenchmark.py --tasks full --stagewise-seeds 42,52,62 --quiet
```

也支持将“程序如何运行”的参数集中写入 YAML，并继续保留 CLI 覆盖能力：

```bash
python symkanbenchmark.py --config configs/symkanbenchmark.default.yaml --quiet
```

推荐约定：

- YAML：运行配置、实验参数、输出目录、设备、seed 等。
- 环境变量：敏感配置或机器相关差异，通过 `${ENV_VAR}` / `${ENV_VAR:-default}` 注入。
- CSV：结果表、分析表、可直接插入 LaTeX 的产物。

也就是说，本仓库继续保留 CSV 产物，但不再把 CSV 视作运行时配置载体。

运行结果通常写入以下位置：

- `outputs/benchmark_runs/symkanbenchmark_runs.csv`：多 seed 主表。
- `outputs/benchmark_runs/run_01_seed42/kan_stage_logs.csv`：阶段训练日志。
- `outputs/benchmark_runs/run_01_seed42/symbolize_trace.csv`：剪枝与符号化轨迹。
- `outputs/benchmark_runs/run_01_seed42/formula_validation.csv`：导出公式的数值验证结果。

最小可运行示例见 [docs/symkan_usage.md](docs/symkan_usage.md)；交互式实验入口位于 [notebooks/kan.ipynb](notebooks/kan.ipynb)。

## 仓库结构

```text
symkan-experiments/
├─ data/                        # 数据集与本地缓存
├─ symkan/                      # 工程化核心库：训练、符号化、评估、导出
├─ kan/                         # 本地 pykan 相关实现与兼容层
├─ docs/                        # 面向读者的说明文档与实验报告
├─ outputs/                     # 脚本运行产物与实验归档
├─ scripts/                     # 脚本实现（推荐阅读入口）
├─ symkanbenchmark.py           # 批量主实验入口（兼容 shim，实际实现见 scripts/）
├─ ablation_runner.py           # 单因素消融矩阵（兼容 shim）
├─ benchmark_ab_compare.py      # A/B 对比汇总（兼容 shim）
├─ analyze_layerwiseft.py       # LayerwiseFT 专项分析（兼容 shim）
├─ compare_layerwiseft_improved.py  # 改进版 LayerwiseFT 对比（兼容 shim）
├─ examples/                    # 示例输出与参考产物
├─ notebooks/                   # 交互式研究 notebook
└─ outputs/README.md            # 运行产物目录说明
```

目录和脚本职责的详细说明见 [docs/project_map.md](docs/project_map.md)。

补充说明：运行 `notebooks/kan.ipynb` 时，会在 `notebooks/` 下自动生成 `model/` 目录；而 notebook 导出的 CSV 结果会统一写入 `outputs/notebooks/`，避免污染 notebook 目录。

## 工作流概览

主工作流可划分为两个阶段：

1. `stagewise_train`
   该阶段用于将模型推进到适于符号化的区间，而非直接追求单次最优精度。
2. `symbolize_pipeline`
   该阶段用于进一步压缩结构、完成逐层符号搜索、微调仿射参数并导出表达式。

对应模块分工：

- `symkan.core`：设备、数据集、训练基础接口。
- `symkan.tuning`：分阶段训练、选模、自适应节奏控制。
- `symkan.symbolic`：函数库、输入压缩、逐层符号化主流程。
- `symkan.eval`：ROC/AUC、公式数值验证。
- `symkan.io`：CSV / bundle 导出。

架构视角的完整说明见 [ARCHITECTURE.md](ARCHITECTURE.md) 和 [docs/design.md](docs/design.md)。

## 项目层默认设定

以下内容指项目层面的默认设定，不等同于 CLI 参数解析器中的技术默认值。

- `stagewise_train` 默认开启。
- 渐进剪枝默认开启，其主要作用在于复杂度控制。
- 输入压缩默认开启，以控制符号化成本。
- 对典型 2 层 KAN，`LayerwiseFT` 的默认设置为关闭，即显式传入 `--layerwise-finetune-steps 0`。

相关依据见：

- [docs/design.md](docs/design.md)
- [docs/ablation_report.md](docs/ablation_report.md)
- [docs/layerwiseft_improved_report.md](docs/layerwiseft_improved_report.md)

## 文档导航

- [docs/index.md](docs/index.md)：文档总入口。
- [docs/project_map.md](docs/project_map.md)：项目地图与阅读路线。
- [docs/symkan_usage.md](docs/symkan_usage.md)：核心库使用说明。
- [docs/symkanbenchmark_usage.md](docs/symkanbenchmark_usage.md)：批量实验脚本说明。
- [docs/design.md](docs/design.md)：架构设计、边界和项目层默认设定。
- [docs/kan_parameters.md](docs/kan_parameters.md)：`notebooks/kan.ipynb` 参数解释。
- [docs/ablation_usage.md](docs/ablation_usage.md)：消融脚本使用说明。
- [docs/ablation_report.md](docs/ablation_report.md)：当前单因素消融结论。
- [docs/layerwiseft_improved_report.md](docs/layerwiseft_improved_report.md)：LayerwiseFT 改进版对比。

## 治理文件

- [CONTRIBUTING.md](CONTRIBUTING.md)
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)
- [SECURITY.md](SECURITY.md)
- [LICENSE](LICENSE)

## License

本项目使用 [MIT License](LICENSE)。
