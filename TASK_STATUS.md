# TASK_STATUS

## Date
2026-03-31

## Task
实现 Stage 26：基于两组已完成的 Feynman benchmark 产物，完善论文草稿所需的实验叙述，更新 `IMPLEMENTATION_PLAN.md` 与 `TASK_STATUS.md`，并将结果系统写入 `ICBR-KAN_design.md`。

## Current Stage
Stage 26: Consolidate Feynman Reference Benchmark Evidence into Paper-Ready Experimental Sections

## Status
Complete

## Latest Completed Work
- `IMPLEMENTATION_PLAN.md`：
  - 新增 Stage 26，明确目标、输入产物、约束、成功标准与验证方式
  - 将 Stage 26 标记为 `Complete`
- `ICBR-KAN_design.md`：
  - 将文档状态从“基于 Stage 24”的收敛稿升级为“基于 Stage 24 + Stage 26”的设计与实验文档
  - 在摘要中补入两组 Feynman 输出目录，明确当前证据同时来自：
    - `outputs/icbr_benchmark_stage24_quality_4tasks_20seeds_all_variants/`
    - `outputs/icbr_benchmark_feynman_reference_paper10_seeds1_20/`
    - `outputs/icbr_benchmark_feynman_reference_paper10_seeds1_20_icbr_ablation/`
  - 更新“两个核心改进点”的论文口径：
    - 将 shared-tensor 的收益从 synthetic 结果扩展到 Feynman 外部验证
    - 将 replay rerank 的收益表述收紧为任务相关，而非统一显著
  - 将原“计划中的 Feynman benchmark 任务”重写为“当前已完成的外部验证层”，补入：
    - `10` 个 Feynman reference tasks
    - `20` 个 benchmark seeds
    - `2000 / 1000 / 1000` 的 `train / calibration / test` split
    - `teacher_cache readonly`
    - `topk=3`、`grid_number=21`、`iteration=2`
    - `width_mid=[5, 2]`
    - teacher quality gate 边界样本
  - 新增 `## 14. Stage 26: Feynman Reference Benchmark Results` 章节，并写成四个论文式小节：
    - 实验设计与准备
    - Baseline 与 `icbr_full` 的主要结果分析
    - 消融研究：shared / replay / explicit commit
    - 综合讨论与结论
  - 将结果中的图像直接接入设计稿：
    - `icbr_benchmark_symbolic_time_errorbar.png`
    - `icbr_benchmark_speedup_boxplot.png`
    - `icbr_benchmark_q123_evidence_by_task.png`
  - 新增两张结果表：
    - baseline vs `icbr_full` 的 task-level 主结果表
    - `q1/q2/q3` 消融证据表
  - 将异常与边界情况写入正文：
    - `feynman_I_12_1, seed=4` 因 `teacher_test_mse=0.300906 > 0.1` 被 gate 拒绝
    - `feynman_II_6_15a` 上 replay 并未表现出统一收益
    - `feynman_I_6_2a` 上 shared-tensor 的速度优势接近消失
  - 将风险与结论章节顺延为 `## 15` 与 `## 16`
- `TASK_STATUS.md`：
  - 当前任务切换为 Stage 26
  - 记录本轮设计稿、计划与状态文档的统一收口

## Files Changed
- ICBR-KAN_design.md
- IMPLEMENTATION_PLAN.md
- TASK_STATUS.md

## Validation Run
- 人工对照：
  - `outputs/icbr_benchmark_feynman_reference_paper10_seeds1_20/icbr_benchmark_summary.md`
  - `outputs/icbr_benchmark_feynman_reference_paper10_seeds1_20/icbr_benchmark_significance.csv`
  - `outputs/icbr_benchmark_feynman_reference_paper10_seeds1_20_icbr_ablation/icbr_benchmark_summary.md`
  - `outputs/icbr_benchmark_feynman_reference_paper10_seeds1_20_icbr_ablation/icbr_benchmark_variant_rows.csv`
- 文本检查：
  - `ICBR-KAN_design.md` 已显式出现 `Stage 26: Feynman Reference Benchmark Results`
  - `ICBR-KAN_design.md` 已显式出现 `图 14-1`
  - `ICBR-KAN_design.md` 已显式出现 `Q1/Q2/Q3`
  - `ICBR-KAN_design.md` 已显式出现 `teacher quality gate`
  - `ICBR-KAN_design.md` 已显式出现 `feynman_I_12_1`
  - `ICBR-KAN_design.md` 已显式出现 `icbr_no_replay`
  - `ICBR-KAN_design.md` 已显式出现 `icbr_no_shared`
  - `ICBR-KAN_design.md` 已显式出现 `icbr_refit_commit`

## Validation Result
- Stage 26 已完成文档级执行，且设计稿已从“仅依赖 synthetic 初步结果”扩展为“同时吸收 Feynman 主对比与消融证据”的论文草稿支撑文档。
- 主对比结果已在正文中明确收敛为：
  - `199/199` 个有效配对样本的 symbolic 时间收益均为正
  - baseline 与 `icbr_full` 的几何均值 symbolic wall time 约为 `16.07s` 与 `0.73s`
  - 几何均值 speedup 约为 `21.93x`
- 消融结果已在正文中明确收敛为：
  - `icbr_no_shared / icbr_full` 的总体 symbolic time ratio 均值约为 `1.30`
  - replay 的总体 `replay_rank_inversion_rate` 约为 `0.39`
  - `icbr_refit_commit` 的平均 `commit_param_drift_l2_mean` 约为 `6.81`
- 设计稿已明确区分：
  - 稳定主结论：速度优势与导出稳定性
  - 任务相关结论：replay 的质量收益
  - 异常与边界：teacher gate、弱共享收益任务、replay 反向波动任务
  - 不应外推的结论：`formula_export_success` 不等价于真实公式恢复正确率

## Decisions
- Stage 26 的主叙事固定为：
  - ICBR 的 headline result 是 CPU symbolic fitting 显著提速
  - shared-tensor 是主要速度杠杆
  - replay 是条件性的质量修正器
  - explicit commit 是稳定性条件，而不是可省略的实现细节
- Feynman 实验在设计稿中的角色固定为：
  - 当前已完成的外部验证层
  - 不是“未来工作占位”
  - 也不是足以替代更大规模外部评测的最终证明
- `feynman_I_12_1, seed=4` 固定解释为 teacher quality gate 边界样本，不得写成 ICBR 导出失败。

## Remaining Work
- 无；Stage 26 当前范围内目标已完成。

## Blockers
- 无
