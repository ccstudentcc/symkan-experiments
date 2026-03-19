# 工程版发布前清单（模板）

本文档是工程版发布检查模板。每次发布时请复制本模板并填写“本次发布信息”和检查结果。

历史发布记录建议归档到 `docs/archive/releases/`，并按 `engineering_release_record_YYYYMMDD.md` 命名；示例见 [archive/releases/engineering_release_record_20260319.md](archive/releases/engineering_release_record_20260319.md)。

## 1. 本次发布信息

1. 发布日期：`<YYYY-MM-DD>`
2. 发布分支：`<branch>`
3. 发布 tag：`<tag>`
4. 主引用结果目录：`<outputs/...>`
5. 默认验证环境：`<OS + Shell + Python>`

## 2. 发布阻断项（必须全部满足）

- [ ] 工作区无待处理改动（`git status --short` 可解释且可发布）。
- [ ] 核心测试通过（`python -m pytest`）。
- [ ] 主要 CLI 入口可用（`python -m scripts.symkanbenchmark --help`、`python -m scripts.ablation_runner --help`）。
- [ ] 工程版主结论有归档支撑（`engineering_rerun_report.md` 与引用目录一致）。
- [ ] 历史版与工程版口径已拆分（`engineering_version_rerun_note.md` 可追踪）。

## 3. 文档与口径收口（按矩阵执行）

1. 先按 [doc_sync_matrix.md](doc_sync_matrix.md) 确定本次改动影响的文档集合。
2. 对矩阵命中的文档逐项完成同步与人工核对。
3. 勾选全局必检项：
   - [ ] 文档导航一致：`README.md` 与 `docs/index.md` 一致。
   - [ ] 工程版三件套可达：`engineering_version_rerun_note`、`engineering_rerun_report`、`engineering_release_checklist`。
   - [ ] 链接完整性通过：`README.md` 与 `docs/` 相对链接无失效项。

## 4. 建议项（非阻断）

- [ ] CI 自动化检查已覆盖最小发布路径（至少包含 `python -m pytest`）。
- [ ] 发布说明（Release Note）已包含环境、命令、已知限制、与历史版关系。
- [ ] 本次最小 smoke run 已归档（入口到输出链路可复现）。

## 5. 执行命令模板（发布前建议跑一遍）

```powershell
# 运行目录：仓库根目录（symkan-experiments/）
python -m pytest
python -m scripts.symkanbenchmark --help
python -m scripts.ablation_runner --help
git status --short
```

命令执行记录（由本次发布填写）：

1. `pytest` 结果：`<pass/fail + 摘要>`
2. CLI help 结果：`<pass/fail + 摘要>`
3. `git status` 结果：`<clean/有改动 + 说明>`

## 6. 发布后快速回看

1. 新读者能否仅靠 `README.md` 找到正确入口。
2. 新读者能否从 `docs/index.md` 找到 runbook、口径说明和 rerun 报告。
3. 若后续 rerun 更新，是否同步更新引用目录与报告日期。

## 7. 相关文档

1. [README.md](../README.md)
2. [index.md](index.md)
3. [doc_sync_matrix.md](doc_sync_matrix.md)
4. [project_map.md](project_map.md)
5. [design.md](design.md)
6. [symkan_usage.md](symkan_usage.md)
7. [full_experiment_runbook.md](full_experiment_runbook.md)
8. [engineering_version_rerun_note.md](engineering_version_rerun_note.md)
9. [engineering_rerun_report.md](engineering_rerun_report.md)
