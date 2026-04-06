# 文档治理规范

本文档定义本仓库文档系统的分层角色、维护链路、写作边界与发布收口要求。其作用不是替代具体用法文档或实验报告，而是约束这些文档如何协同维护。

## 1. 治理目标

1. 保持“入口、设计、执行、证据、发布”五类信息分层明确，不把不同职责混写到同一文档。
2. 保持稳定入口与带日期正文分离，避免新一轮 rerun 覆盖历史证据。
3. 保持代码、配置、结果目录与文档表述同步，避免出现“实现已变更、文档仍停留在旧口径”的漂移。
4. 保持写作风格克制、可引用、可审阅，不使用 AI 助手式口吻、教程式闲聊或未落盘证据支撑的判断。

## 2. 分层角色

### 2.1 仓库级入口

1. `README.md`：项目总览、最小运行入口、核心导航与统一口径速查。
2. `ARCHITECTURE.md`：模块边界、主数据流、接口关系与系统级约束。
3. `CONTRIBUTING.md`：协作流程、提交流程、检查要求与文档收口要求。
4. `AGENTS.md`：面向代理的非显然规则、路由提示与强制同步约束。

### 2.2 docs 导航层

1. `docs/index.md`：`docs/` 目录统一入口、主题导航、任务路径与写作规范速查。
2. `docs/project_map.md`：仓库结构、代码入口、文档入口与结果目录地图。
3. `docs/documentation_governance.md`：文档体系的治理规则、角色边界与维护链路。
4. `docs/doc_sync_matrix.md`：改动类型到必同步文档集合的单一真源。

### 2.3 方法、手稿与展示层

1. `docs/design.md`：方法设计、约束、证据边界与论文式论证。
2. `docs/symkan_manuscript.md`：面向论文投稿或学位正文的手稿式主叙述稿，用于重组设计、实验协议、结果与讨论，不替代设计文档或带日期报告。
3. `docs/slides/`：与 `symkan_manuscript.md` 对齐的 Beamer 展示层源码；负责答辩或报告压缩叙事，不作为独立证据源。
4. `docs/symkan_usage.md`、`docs/kan_parameters.md`：库层与 notebook 参数说明。
5. `docs/symkanbenchmark_usage.md`、`docs/ablation_usage.md`：脚本执行语义、参数与输出约定。
6. `docs/full_experiment_runbook.md`：完整复跑步骤、检查项与产物核对。

### 2.4 证据与发布层

1. `docs/engineering_version_rerun_note.md`：历史版与工程版、paired compare 与补充切片的口径分层。
2. `docs/engineering_rerun_report.md`：工程版实验报告稳定入口。
3. `docs/engineering_rerun_report_YYYYMMDD.md`：单轮正式正文、证据边界与引用目录。
4. `docs/engineering_release_checklist.md`：发布前阻断项与文档收口清单。
5. `docs/archive/releases/`：已完成发布记录归档。

### 2.5 当前任务层

1. `SPEC.md`：复杂或多会话任务的目标、约束与验收范围。
2. `IMPLEMENTATION_PLAN.md`：阶段划分、执行顺序、验证方式与当前状态。
3. `TASK_STATUS.md`：当前目标、关键决定、风险与下一步。

## 3. 全链路维护流程

1. 先判断改动属于哪一层：
   - 入口或导航变化
   - 设计边界变化
   - 执行流程变化
   - 结果证据变化
   - 发布或归档变化
2. 依据 [doc_sync_matrix.md](doc_sync_matrix.md) 确定必须同步的文档集合。
3. 若改动影响实验主引用或 rerun 口径：
   - 更新稳定入口 `engineering_rerun_report.md`
   - 新建或修订带日期正文 `engineering_rerun_report_YYYYMMDD.md`
   - 同步 `engineering_version_rerun_note.md`
   - 同步 `engineering_release_checklist.md`
4. 若任务跨多文件、多阶段或多会话：
   - 在主改动前刷新 `SPEC.md`、`IMPLEMENTATION_PLAN.md`、`TASK_STATUS.md`
   - 每次会话开始前复核 `SPEC.md` 与 `TASK_STATUS.md`
   - 每次阶段结束后回写 `TASK_STATUS.md`
5. 若改动影响文档系统本身：
   - 先更新本文档
   - 再同步 `README.md`、`docs/index.md`、`docs/project_map.md`、`CONTRIBUTING.md`
   - 复核 `docs/engineering_release_checklist.md`
   - 若规则对代理可见性重要，再同步 `AGENTS.md`
6. 完成文本改动后执行最小一致性检查：
   - 导航入口是否可达
   - 相对链接是否有效
   - 命令口径是否仍为 `python -m scripts.*`
   - 文风是否回退为对话式或教程式

## 4. 写作边界

1. 入口文档写“去哪里看什么”，不承担带日期实验正文。
2. 设计文档写“为什么这样设计、哪些结论可写、哪些不可写”，不承担命令级操作手册。
3. 手稿文档写“如何将设计、实验协议与结果重组成论文主叙述”，不替代 `docs/design.md` 的边界说明，也不覆盖带日期报告。
4. 展示层文档写“如何将手稿主张压缩为口头报告或答辩叙事”，可以重组图表顺序，但不得引入超出手稿与带日期报告的新结论。
5. 执行文档写“如何运行、检查什么产物、哪些参数属于哪一层”，不承担研究结论归纳。
6. 报告文档写“本轮实验看到了什么、证据边界在哪里”，不把补充切片写成正式 paired 证据。
7. 发布文档写“发布前必须检查什么”，不重写方法说明或报告正文。
8. 任务跟踪文档写“当前在做什么、做到哪一步、还有哪些风险”，不承担方法说明或发布记录职责。

## 5. 文风约束

1. 使用严谨、克制、工程化表述，不使用“你只需要”“很简单”“这里我们来看”等对话式引导。
2. 执行类文档可以保留必要操作指令，但应以契约和步骤为中心，不堆砌教程式解释。
3. 结论应绑定可定位的输出目录、报告文件或结构化产物，不依赖终端瞬时输出。
4. 任何跨版本比较都应先说明口径是否可比，再给出指标解释。
5. 若同一事实已在稳定入口中定义，不在其他文档重复扩写其背景故事，只保留必要链接。

## 6. 禁止模式

1. 用 `README.md` 或 `docs/index.md` 承载单轮实验的完整数值正文。
2. 用 `docs/engineering_rerun_report.md` 覆盖历史带日期正文。
3. 把单变体补充切片写成 paired backend-only compare 证据。
4. 在执行类文档中混入未经验证的研究结论。
5. 改动文档结构后只更新单一入口，放任导航、矩阵或发布清单失配。

## 7. 最小验证要求

1. 检查 `README.md` 与 `docs/index.md` 的导航是否一致。
2. 检查新增或改名文档是否已出现在 `docs/project_map.md` 与相关入口页。
3. 检查与本次改动对应的矩阵命中文档是否已同步。
4. 检查命令示例的代码块语言、运行目录注释与入口口径是否一致。
5. 若 `docs/slides/` 存在，检查其是否仍明确声明“手稿 companion 而非独立证据源”，且入口页可达。
6. 检查是否需要同步 `AGENTS.md`，以减少未来重复摸索。
7. 若为复杂任务，检查 `SPEC.md`、`IMPLEMENTATION_PLAN.md`、`TASK_STATUS.md` 是否仍反映当前目标。

## 8. 关联文档

1. [index.md](index.md)
2. [project_map.md](project_map.md)
3. [doc_sync_matrix.md](doc_sync_matrix.md)
4. [engineering_release_checklist.md](engineering_release_checklist.md)
5. [../README.md](../README.md)
6. [../CONTRIBUTING.md](../CONTRIBUTING.md)
7. [../AGENTS.md](../AGENTS.md)
8. [../SPEC.md](../SPEC.md)
9. [../IMPLEMENTATION_PLAN.md](../IMPLEMENTATION_PLAN.md)
10. [../TASK_STATUS.md](../TASK_STATUS.md)
