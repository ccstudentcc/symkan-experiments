# 工程版发布前清单

本文档用于回答一个实际问题：当前 `main` 是否已经达到“可以发布工程版”的最低条件，以及发布前还需要补哪些动作。

适用范围：

1. 论文配套工程版；
2. 内部归档或答辩提交版；
3. 面向熟悉本项目背景读者的公开仓库版本。

不适用范围：

1. 面向零上下文陌生用户的一键安装产品；
2. 需要长期兼容承诺的正式软件发行版。

## 1. 当前结论

截至 `2026-03-19`，当前仓库已经满足“可发布工程版”的基本条件，建议按“工程版 v1”对外发布。

当前判断依据：

1. 在 `kan` 环境中执行 `C:\Users\chenpeng\miniconda3\envs\kan\python.exe -m pytest`，`82` 个测试全部通过。
2. `C:\Users\chenpeng\miniconda3\envs\kan\python.exe -m scripts.symkanbenchmark --help` 与 `C:\Users\chenpeng\miniconda3\envs\kan\python.exe -m scripts.ablation_runner --help` 均可正常运行。
3. 仓库已有完整入口文档、复跑手册、工程版口径说明与 rerun 报告。
4. `docs/engineering_rerun_report.md` 已给出当前工程版的结果归档与解释框架。
5. `notebooks/kan.ipynb` 已于 `2026-03-19` 重跑，结构化结果已刷新到 `outputs/notebooks/`。

建议发布口径：

1. 历史参考版仅作为研究脉络锚点；
2. 当前工程版作为正式结论载体；
3. 对外说明默认验证环境为 Windows + PowerShell + `kan` 环境。

## 2. 发布阻断项

以下项目建议视为“必须完成”，若其中任一项不满足，则不建议发布。

- [x] 工作区无待处理代码改动：`git status --short` 未发现仓库内业务文件脏改动。
- [x] 核心测试通过：`python -m pytest` 已在 `kan` 环境中全量通过。
- [x] 主要 CLI 入口可用：`scripts.symkanbenchmark`、`scripts.ablation_runner` 的帮助信息可正常输出。
- [x] 交互式 notebook 主链路已完成本地重跑：`notebooks/kan.ipynb` 的结构化 CSV 已刷新到 `outputs/notebooks/`。
- [x] 入口文档存在且口径一致：`README.md`、`ARCHITECTURE.md`、`CONTRIBUTING.md` 已齐备。
- [x] 完整复跑手册存在：`docs/full_experiment_runbook.md` 已给出全流程步骤与产物检查项。
- [x] 工程版结论有归档支撑：`docs/engineering_rerun_report.md` 已记录输出目录、指标表与解释边界。
- [x] 历史版与工程版口径已拆分：`docs/engineering_version_rerun_note.md` 已明确“双锚点”叙述。

## 3. 建议项

以下项目不构成当前发布阻断，但完成后会让工程版更稳、更适合公开协作。

- [ ] 增加 CI：当前没有看到显式的 GitHub Actions 或等价持续集成入口，建议至少自动运行 `python -m pytest`。
- [ ] 固定发布标签：若准备对外引用，建议打一个明确 tag，例如 `v1.0.0-engineering`。
- [ ] 补一段发布说明：建议单独说明默认环境、推荐命令、已知限制、与 Legacy 的关系。
- [ ] 清理第三方告警：当前测试通过，但仍有 `mpmath`、`matplotlib/pyparsing`、`pandas`、`pydantic` 的 warning。
- [ ] 做一次最小 smoke run 归档：除了测试，最好再保留一轮最小命令执行记录，确认从入口到输出目录的链路可复现。

## 4. 最小发布动作

如果你的目标是“现在就发工程版”，建议按下面顺序执行。

1. 确认当前发布引用的结果目录：优先使用 `outputs/rerun_v2_engine_safe_20260318_rerun/`。
2. 在发布说明中声明当前正式结论基于工程版 rerun，而不是历史参考版。
3. 明确推荐运行环境：Windows、PowerShell、`C:\Users\chenpeng\miniconda3\envs\kan\python.exe`、Python `3.9.25`。
4. 在发布说明中给出最常用入口：
   - `python -m scripts.symkanbenchmark --config configs/symkanbenchmark.default.yaml --quiet`
   - `python -m scripts.ablation_runner --config configs/ablation_runner.default.yaml`
5. 附上文档入口顺序：
   - `README.md`
   - `docs/full_experiment_runbook.md`
   - `docs/engineering_version_rerun_note.md`
   - `docs/engineering_rerun_report.md`

## 5. 对外表述模板

若你要在 README、release note、论文附录或答辩材料中简短说明，可直接沿用下面的口径：

> 当前仓库已完成工程化收口。历史参考版用于研究脉络说明，当前 `main` 上的工程版 rerun 结果用于正式结论。默认验证环境为 Windows PowerShell 下的 `kan` Python 环境，核心测试已全量通过。

## 6. 发布后快速回看

发布后建议再做一次非常轻量的自检：

1. 新读者能否仅靠 `README.md` 找到正确入口。
2. 新读者能否从 `docs/index.md` 找到 runbook、口径说明和 rerun 报告。
3. 文档中是否始终把 Legacy 与工程版分开叙述。
4. 若后续 rerun 更新，是否同步更新引用目录和报告日期。

## 7. 相关文档

1. [README.md](../README.md)
2. [../ARCHITECTURE.md](../ARCHITECTURE.md)
3. [full_experiment_runbook.md](full_experiment_runbook.md)
4. [engineering_version_rerun_note.md](engineering_version_rerun_note.md)
5. [engineering_rerun_report.md](engineering_rerun_report.md)
