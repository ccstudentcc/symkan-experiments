# Contributing

本文说明本仓库的贡献范围、协作约束与提交流程。项目以研究代码与实验文档为主，因此贡献的核心要求是：改动应当可解释、可复现、可回退，并与现有工作流保持兼容。

## 预备阅读

在修改代码、脚本或文档之前，应先阅读以下文件：

1. [README.md](README.md)
2. [ARCHITECTURE.md](ARCHITECTURE.md)
3. [docs/project_map.md](docs/project_map.md)
4. [docs/documentation_governance.md](docs/documentation_governance.md)（若本次改动涉及文档或入口）
5. 与拟修改内容直接相关的说明文档

对于实验逻辑、结果导出格式或公共接口的改动，上述材料构成基本上下文。

## 贡献范围

以下类型的改动通常适合纳入本仓库：

- 文档勘误、结构重组与术语统一。
- 结果导出、日志结构与复现流程的改进。
- 带有明确复现路径的问题修复。
- 与现有模块边界一致的小规模功能扩展。
- 基于现有实验产物的分析脚本或报告补充。

以下类型的改动通常不宜直接提交：

- 缺乏明确问题定义的大规模重构。
- 以“更优雅”为由改变既有 notebook、CLI 或 CSV 产物格式。
- 未经讨论即升级 major 版本依赖。
- 将实验编排逻辑直接并入公共库层。
- 无法说明影响范围、验证方式或复现条件的修改。

## 协作原则

- 改动规模应尽量小，并保持可回退。
- 优先复用现有数据结构、导出格式与接口约定。
- 向后兼容优先于接口重塑。
- 代码、参数与文档中的表述应保持一致。
- 不在仓库中写入密钥、令牌、机器相关路径或其他敏感配置。
- 文档系统变更应先明确分层角色，再同步入口、项目地图、矩阵与发布清单。

## 提交流程

建议的工作顺序如下：

1. 在 issue 或 pull request 中界定问题、目标与影响范围。
2. 阅读相关代码、文档与已有实验结果。
3. 实施最小必要改动。
4. 运行与改动范围相称的检查。
5. 同步更新相关文档。
6. 在 pull request 中说明改动内容、依据与验证结果。

## 复杂任务跟踪

若本次工作满足以下任一条件，应启用任务跟踪文件：

1. 涉及多个阶段或多个会话。
2. 同时修改多个核心文档、公共接口或仓库级规则。
3. 需要显式记录阶段状态、残余风险或后续收口动作。

执行要求如下：

1. 开始主要编辑前更新 `SPEC.md`、`IMPLEMENTATION_PLAN.md`、`TASK_STATUS.md`。
2. 每次会话开始前复核 `SPEC.md` 与 `TASK_STATUS.md`。
3. 每个阶段结束后回写 `TASK_STATUS.md`，说明当前状态、风险与下一步。

## Pull Request 内容要求

提交 pull request 时，建议至少说明以下内容：

- 问题定义与背景。
- 具体改动内容。
- 本次改动分类（例如：结构 / 设计 / 使用语义 / 实验流程 / 指标口径 / 输出口径）。
- 选择当前方案而非替代方案的原因。
- 是否影响现有 CLI、Notebook 或结果文件格式。
- 已执行的检查、实验或人工核对项。

若本次改动包含文档命令示例，提交前应完成以下自检：

1. 环境段：执行类文档是否包含“参考环境（用于结果解释）”，且与同轮复测文档一致。
2. 代码块语言：命令示例是否统一为 `powershell`，并避免 `bash` / `sh` / `shell`。
3. 换行风格：多行命令是否统一使用 PowerShell 续行符 `` ` ``，且每个命令代码块首行均含运行目录注释。

若本次改动涉及工程版口径、发布说明或文档导航，提交前应额外完成以下自检：

1. 以 [docs/doc_sync_matrix.md](docs/doc_sync_matrix.md) 为单一真源，确认本次改动影响的文档集合已全部同步。
2. 若涉及文档体系规则，核对 [docs/documentation_governance.md](docs/documentation_governance.md) 是否已同步。
3. 导航一致性：`README.md` 的“文档路径/文档导航”与 `docs/index.md` 是否一致。
4. 工程版三件套：`engineering_version_rerun_note`、`engineering_rerun_report`、`engineering_release_checklist` 是否在相关文档中可追踪可跳转。
5. 链接有效性：`README.md` 与 `docs/` 相对链接是否均可访问。
6. 若新增、移除或重定义核心文档：`docs/project_map.md` 是否已同步，且 `docs/index.md` 中的阅读路径已更新。
7. 若为复杂任务：`SPEC.md`、`IMPLEMENTATION_PLAN.md`、`TASK_STATUS.md` 是否仍与当前改动范围一致。
8. 若 `docs/slides/` 作为手稿 companion 存在：其 README、主 deck 与引用资产是否仍与 `docs/symkan_manuscript.md` 保持同一证据边界。

## 检查要求

检查强度应与改动范围相匹配：

- 文档改动：核对链接、标题、命令示例、文件名与交叉引用。
- Python 代码改动：至少运行相关脚本或最小复现场景。
- 实验逻辑改动：说明结果来自已有产物还是重新运行。

推荐的测试入口是在仓库根目录执行：

```powershell
# 运行目录：仓库根目录（symkan-experiments/）
python -m pytest
```

这样可以与仓库当前的模块化入口保持一致，并减少不同 `pytest` 启动方式带来的导入路径差异。

若改动涉及文档治理或发布收口，可执行以下自动检查命令：

```powershell
# 运行目录：仓库根目录（symkan-experiments/）
rg -n "```(bash|sh|shell)" README.md docs CONTRIBUTING.md ARCHITECTURE.md
rg -n "python\\s+scripts\\.|python\\s+symkanbenchmark\\.py|python\\s+ablation_runner\\.py" README.md docs
```

说明：

1. 第一条用于发现不符合规范的代码块语言标记。
2. 第二条用于发现入口命令口径回退（应统一为 `python -m scripts.*`）。
3. 若本次改动涉及文档体系角色或入口，应再人工核对 `README.md`、`docs/index.md`、`docs/project_map.md`、`docs/documentation_governance.md` 与 `docs/engineering_release_checklist.md` 的交叉链接。

若改动影响公共接口或项目入口，通常还需要同步更新：

- [README.md](README.md)
- [ARCHITECTURE.md](ARCHITECTURE.md)
- `docs/` 下对应说明文档

## Commit 与 PR 表述

- Commit 信息应说明改动原因，而非仅描述表面动作。
- Pull request 描述应尽量具体，避免将关键判断留给审阅者自行推断。
- 单个 pull request 宜围绕一个主要主题展开，避免将文档整理、结构重构与实验逻辑修改混合提交。

## 行为规范

参与本仓库即表示同意遵守 [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)。
