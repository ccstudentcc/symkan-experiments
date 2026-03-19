# symkan-experiments

`symkan-experiments` 是一个面向 KAN 符号化实验的工程化仓库。其目标是在 `pykan` 基础上提供较稳定的实验流程、结果导出与复现支持。

训练 KAN -> 逐步剪枝 -> 符号化 -> 数值验证 -> 导出结构化结果 -> 批量复现实验

## 项目背景

在基于 `pykan` 的探索性实验基础上，进入批量复现或论文写作阶段时，通常会遇到以下问题：

- 训练、剪枝、符号化混在一起，流程不可控。
- 结果散落在 notebook 输出和临时文件里，难以追溯。
- 参数很多，但缺少统一口径，不知道哪些是技术默认值，哪些是项目层研究设定。
- 单次 seed 看起来很好，换个 seed 结论就变。

本仓库的基本思路是先统一配置对象、数据结构、输出格式和实验入口，再在此基础上组织训练、剪枝、符号化和评估流程。核心模块 `symkan/` 提供配置、训练、符号化、评估和导出接口；根目录脚本负责批量实验、A/B 对比和消融分析。

## 文档路径

可按使用目的选择以下阅读路径：

- 项目结构：读 [docs/project_map.md](docs/project_map.md)。
- 最小示例：读 [docs/symkan_usage.md](docs/symkan_usage.md) 第 4 节。
- 实验复现：读 [docs/symkanbenchmark_usage.md](docs/symkanbenchmark_usage.md)。
- 完整复跑手册：读 [docs/full_experiment_runbook.md](docs/full_experiment_runbook.md)。
- 设计依据：读 [docs/design.md](docs/design.md)。
- 单因素消融：读 [docs/ablation_usage.md](docs/ablation_usage.md)。
- 结果报告：读 [docs/ablation_report.md](docs/ablation_report.md) 和 [docs/layerwiseft_improved_report.md](docs/layerwiseft_improved_report.md)。
- 工程版口径说明：读 [docs/engineering_version_rerun_note.md](docs/engineering_version_rerun_note.md)。
- 工程版复测主报告：读 [docs/engineering_rerun_report.md](docs/engineering_rerun_report.md)。
- 工程版发布检查：读 [docs/engineering_release_checklist.md](docs/engineering_release_checklist.md)。
- 文档同步规则（SSOT）：读 [docs/doc_sync_matrix.md](docs/doc_sync_matrix.md)。

## 统一口径（2026-03-19）

为避免“代码已更新、文档未同步”的偏差，当前仓库统一按以下口径描述：

1. 入口口径：常规 CLI 使用 `python -m scripts.*`；工程版复测可使用 `scripts/run_engineering_rerun.ps1` 作为编排封装入口。
2. 配置口径：Notebook / CLI / 库层统一收敛到 `symkan.config.AppConfig`；旧 notebook flat kwargs 的 canonical 化由 `symkan.config.notebook` 负责，`symkan.notebook_compat` 仅保留薄桥接职责。
3. 输出口径：项目默认输出为 `outputs/benchmark_*`；手册示例输出为 `outputs/rerun/*`；工程归档输出为 `outputs/rerun_v2_engine_safe_<date>/*`。
4. 跨版本指标口径：仅将 `export_wall_time_s` 语义映射到 `symbolize_wall_time_s`；`run_total_wall_time_s` 为工程版新增字段，历史版无同名可比项。
5. 导航口径：`README.md` 中“文档路径/文档导航”与 `docs/index.md` 必须保持一致；发生冲突时以 `docs/index.md` 为准并同步回写。

若后续继续迭代 `main`，请同步更新 [docs/index.md](docs/index.md) 的“统一口径速查”与本文对应段落，避免 README 与 docs 叙述漂移。

## 基本运行

运行环境：Python 3.9。

```powershell
# 运行目录：仓库根目录（symkan-experiments/）
pip install -r requirements.txt
python -m scripts.symkanbenchmark --tasks full --stagewise-seeds 42,52,62 --quiet
```

也支持将“程序如何运行”的参数集中写入 YAML，并继续保留 CLI 覆盖能力：

```powershell
# 运行目录：仓库根目录（symkan-experiments/）
python -m scripts.symkanbenchmark --config configs/symkanbenchmark.default.yaml --quiet
```

对于单因素消融，也支持同样的配置方式：

```powershell
# 运行目录：仓库根目录（symkan-experiments/）
python -m scripts.ablation_runner --config configs/ablation_runner.default.yaml
```

补充口径：

- 自动默认来源：`scripts.symkanbenchmark` 省略 `--config` 时，会读取 `configs/symkanbenchmark.default.yaml`。
- 显式模板：`configs/ablation_runner.default.yaml` 与 `configs/benchmark_ab/*.yaml` 都需要通过 `--config` 指定，不属于自动默认回退来源。
- `scripts.ablation_runner` 省略 `--config` 时，不会自动选中 `configs/ablation_runner.default.yaml`；各变体最终仍回退到 `scripts.symkanbenchmark` 的自动默认来源。

推荐约定：

- YAML：运行配置、实验参数、输出目录、设备、seed 等。
- 环境变量：敏感配置或机器相关差异，通过 `${ENV_VAR}` / `${ENV_VAR:-default}` 注入；占位符会在 YAML 解析后仅对标量字符串展开，避免把环境变量内容当成新的 YAML 结构注入。
- CSV：结果表、分析表、可直接插入 LaTeX 的产物。

也就是说，本仓库继续保留 CSV 产物，但不再把 CSV 视作运行时配置载体。

当前项目的分层方式是：

- Notebook / 库调用：统一优先构造 `symkan.config.AppConfig`，由其承载 `stagewise` / `symbolize` 子配置。
- CLI / 批量实验：优先使用 `AppConfig` YAML，并仅在脚本层做一小组显式白名单覆盖。
- 核心编排逻辑：统一依赖 `symkan.config.AppConfig`，而不是脚本私有 `argparse.Namespace` 或另一套配置模型。
- 底层库逻辑：统一依赖 `symkan.config.AppConfig`，而 `StagewiseConfig` / `SymbolizeConfig` 作为其嵌套子配置存在。

输出目录口径：

- 项目默认输出：`outputs/benchmark_*`（脚本默认行为）。
- 手册示例输出：`outputs/rerun/*`（用于演示完整复跑，避免覆盖默认目录）。
- 工程归档输出：`outputs/rerun_v2_engine_safe_<date>/*`（用于工程版复测归档）。

运行结果通常写入以下位置（项目默认输出）：

- `outputs/benchmark_runs/symkanbenchmark_runs.csv`：多 seed 主表。
- `outputs/benchmark_runs/run_01_seed42/kan_stage_logs.csv`：阶段训练日志。
- `outputs/benchmark_runs/run_01_seed42/symbolize_trace.csv`：剪枝与符号化轨迹。
- `outputs/benchmark_runs/run_01_seed42/formula_validation.csv`：导出公式的数值验证结果。

数据补充边界：

- `symkanbenchmark.py` 默认只会在仓库 `data/` 目录下自动补齐缺失的 MNIST `.npy` 文件。
- 若配置把 `x_train/x_test/y_train/y_test` 指向 `data/` 之外，需显式设置 `data.allow_auto_fetch_outside_data_dir: true` 才允许自动写入。
- `symkan.io.load_export_bundle()` 基于 `pickle`，读取时必须显式传入 `trusted=True`，且仅应用于本地生成、来源可信的 bundle。

最小可运行示例见 [docs/symkan_usage.md](docs/symkan_usage.md)；交互式实验入口位于 [notebooks/kan.ipynb](notebooks/kan.ipynb)。

补充说明：当前 notebook 继续保留论文期/探索期的历史参数写法，但参数归一化职责已收敛到 `symkan.config.notebook`：该层会把函数式 flat kwargs 转为统一的 `AppConfig` section 结构，并优先要求使用 `symkan` 内部 canonical 名字；`symkan.notebook_compat` 只保留轻量执行桥接职责。`2026-03-19` 已在本仓库环境中完成一次重跑，结构化结果写入 `outputs/notebooks/`。

## 仓库结构

```plaintext
symkan-experiments/
├─ data/                        # 数据集与本地缓存
├─ symkan/                      # 工程化核心库：配置、训练、符号化、评估、导出
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

- `symkan.config`：`AppConfig`、YAML 加载、环境变量占位符展开、配置校验，以及 notebook 函数式参数到 `AppConfig` 的 canonical 化转换。
- `symkan.core`：设备、数据集、训练基础接口。
- `symkan.tuning`：分阶段训练、选模、自适应节奏控制。
- `symkan.symbolic`：函数库、输入压缩、逐层符号化主流程。
- `symkan.pruning`：归因、剪枝辅助逻辑与安全包装。
- `symkan.eval`：ROC/AUC、公式数值验证。
- `symkan.io`：CSV / bundle 导出。

架构视角的完整说明见 [ARCHITECTURE.md](ARCHITECTURE.md) 和 [docs/design.md](docs/design.md)。

## 项目层默认设定

以下内容指项目层面的默认设定，不等同于 CLI 参数解析器中的技术默认值。

- `stagewise_train` 默认开启。
- 渐进剪枝默认开启，其主要作用在于复杂度控制。
- 输入压缩默认开启，以控制符号化成本。
- 对典型 2 层 KAN，项目推荐基线通常显式传入 `--layerwise-finetune-steps 0`；而 `configs/*.yaml` / schema 中保留的 `60` 属于技术默认值，主要服务于对照实验与兼容配置。

相关依据见：

- [docs/design.md](docs/design.md)
- [docs/ablation_report.md](docs/ablation_report.md)
- [docs/layerwiseft_improved_report.md](docs/layerwiseft_improved_report.md)

## 验证命令

推荐在项目环境中于仓库根目录执行：

```powershell
# 运行目录：仓库根目录（symkan-experiments/）
python -m pytest
```

该写法与文档中的 `python -m scripts.*` 入口保持一致，也更不依赖调用器如何设置 `sys.path`。

## 文档导航

为减少重复维护，完整文档目录与分场景阅读路径以 [docs/index.md](docs/index.md) 为准。常用入口如下：

- [docs/project_map.md](docs/project_map.md)：项目地图与阅读路线。
- [docs/symkan_usage.md](docs/symkan_usage.md)：核心库使用说明。
- [docs/full_experiment_runbook.md](docs/full_experiment_runbook.md)：完整实验复跑步骤与产物检查。
- [docs/engineering_rerun_report.md](docs/engineering_rerun_report.md)：工程版复测主报告与对照解释。
- [docs/doc_sync_matrix.md](docs/doc_sync_matrix.md)：文档同步规则单一真源（SSOT）。

## 治理文件

- [CONTRIBUTING.md](CONTRIBUTING.md)
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)
- [SECURITY.md](SECURITY.md)
- [LICENSE](LICENSE)

## License

本项目使用 [MIT License](LICENSE)。
