# 文档同步矩阵

本文档定义“改动类型 -> 必须同步的文档”，作为文档治理的单一真源（SSOT）。

## 1. 使用方式

1. 日常开发：在提交前按本矩阵核对受影响文档。
2. 发布前：结合 `engineering_release_checklist.md` 执行完整收口检查。
3. 若与其他文档检查项冲突：以本矩阵为准，并同步修正文档引用方。
4. 若改动影响文档系统本身的层次、入口或写作规则，先读 [documentation_governance.md](documentation_governance.md) 再使用本矩阵。

## 2. 同步矩阵

| 改动类型 | 需要同步的文档 | 重点核对点 |
| --- | --- | --- |
| 目录结构变化（新增/重命名模块、入口脚本职责变化） | `docs/project_map.md`、`docs/index.md`、`README.md` | 阅读路径、脚本职责、入口描述一致 |
| 设计边界变化（模块职责、配置边界、指标语义） | `docs/design.md`、`docs/index.md`、`README.md` | 设计语义与实现行为一致 |
| `symkan` 使用语义变化（调用方式、参数语义、返回结构） | `docs/symkan_usage.md`、`docs/kan_parameters.md`（若影响 notebook） | API 说明、参数含义、返回字段一致 |
| 实验流程变化（执行顺序、关键命令、检查项） | `docs/full_experiment_runbook.md`、`docs/symkanbenchmark_usage.md`、`docs/ablation_usage.md` | 命令可执行、流程顺序与产物检查一致 |
| benchmark A/B compare 语义或输出产物变化 | `docs/symkanbenchmark_usage.md`、`docs/full_experiment_runbook.md`、`docs/engineering_rerun_report.md`、最新 `docs/engineering_rerun_report_YYYYMMDD.md`、`docs/engineering_version_rerun_note.md`、`docs/engineering_release_checklist.md` | baseline/variant 定义、专用 compare 产物、shared-state 检查口径，以及入口页与带日期正文的分工一致 |
| 配置模型/配置来源变化（`AppConfig`、YAML 来源、白名单覆盖） | `docs/symkan_usage.md`、`docs/symkanbenchmark_usage.md`、`docs/design.md`、`README.md` | 配置入口、默认来源、覆盖策略一致 |
| 输出目录口径变化（默认/手册/工程归档） | `README.md`、`docs/index.md`、`docs/engineering_version_rerun_note.md`、`outputs/README.md` | `outputs/benchmark_*`、`outputs/rerun/*`、`outputs/rerun_v2_engine_safe_<date>/*` 口径一致 |
| 跨版本指标口径变化（字段映射、新增指标） | `docs/engineering_version_rerun_note.md`、`docs/engineering_rerun_report.md`、最新 `docs/engineering_rerun_report_YYYYMMDD.md`、`docs/design.md`、`docs/index.md` | `export_wall_time_s -> symbolize_wall_time_s` 映射与新增字段边界清晰 |
| 工程版主引用目录变化（rerun 日期或归档路径变化） | `docs/engineering_rerun_report.md`、最新 `docs/engineering_rerun_report_YYYYMMDD.md`、`docs/engineering_version_rerun_note.md`、`docs/index.md`、`docs/engineering_release_checklist.md`、`README.md`、发布说明 | 稳定入口、带日期正文、目录路径与日期一致 |
| 发布记录新增或更新 | `docs/archive/releases/engineering_release_record_YYYYMMDD.md`、`docs/engineering_release_checklist.md`、`docs/index.md` | 归档路径、命名规则、索引入口一致 |
| 文档导航变化（新增/下线核心文档） | `docs/index.md`、`docs/project_map.md`、`README.md`、`docs/documentation_governance.md`、`CONTRIBUTING.md`、`docs/engineering_release_checklist.md` | 导航链路完整，工程版三件套可达 |
| 文档治理规则变化（分层角色、写作边界、维护链路变化） | `docs/documentation_governance.md`、`docs/index.md`、`docs/project_map.md`、`README.md`、`CONTRIBUTING.md`、`AGENTS.md`、`docs/engineering_release_checklist.md` | 角色定义、入口链路、代理约束与发布收口一致 |
| 复杂任务范围或阶段变化（多会话任务的目标、计划、状态变化） | `SPEC.md`、`IMPLEMENTATION_PLAN.md`、`TASK_STATUS.md`、`docs/documentation_governance.md`（若规则层发生变化） | 当前目标、阶段状态、风险与下一步一致 |
| 辅助说明文档口径变化（非主 docs） | `outputs/README.md`、`notebooks/README.md`、`examples/README.md` | 不回退到旧入口或旧叙述 |

## 3. 全局必检项

1. 命令示例统一为 `powershell`，执行入口统一为 `python -m scripts.*`（工程复测可用 `scripts/run_engineering_rerun.ps1`）。
2. 命令代码块首行包含运行目录注释：`# 运行目录：仓库根目录（symkan-experiments/）`。
3. `README.md` 与 `docs/index.md` 的导航口径一致。
4. `README.md` 与 `docs/` 相对链接可访问，无失效项。
5. 若改动涉及文档治理规则，`documentation_governance.md`、`CONTRIBUTING.md` 与 `AGENTS.md` 的约束不得互相冲突。

## 4. 关联文档

1. [index.md](index.md)
2. [engineering_release_checklist.md](engineering_release_checklist.md)
3. [documentation_governance.md](documentation_governance.md)
4. [../CONTRIBUTING.md](../CONTRIBUTING.md)
