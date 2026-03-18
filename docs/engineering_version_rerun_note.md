# 工程版复测与历史结果口径说明

本文档用于统一“重构前参考结果”与“当前工程版结果”的叙述口径，避免将两代版本直接混作同一统计总体。

## 1. 版本分层

1. 历史参考版：`d8e09b5edadb988bd4a1638ea7109cf3ff5ef7d7`
   对应 pre-release：`v1.0.0-legacy-d8`
2. 当前工程版：`main`（配置模块、守护策略、可观测性增强）

建议在报告中显式写明：历史结果用于参考基线；新结果用于工程版结论与后续迭代。

## 2. 为什么两代结果不能直接等价

1. 训练/剪枝守护策略不同（尤其是失败边界与回滚逻辑）。
2. 耗时指标口径更细：工程版新增了 `run_total_wall_time_s`、`symbolize_wall_time_s` 等字段。
3. 配置组织方式变化：工程版以 `AppConfig` 为统一入口，CLI 仅做白名单覆盖。

因此出现时延差异属于预期，不应简单归因为“模型退化”。

## 3. 当前工程版复测默认口径（2026-03）

1. `stagewise.guard_mode = light`
2. `stagewise.prune_acc_drop_tol = 0.08`
3. 工程版复测归档目录（首轮）：`outputs/rerun_v2_engine_safe_20260318/`
4. 工程版复测归档目录（本轮 rerun）：`outputs/rerun_v2_engine_safe_20260318_rerun/`
5. 复跑脚本 `scripts/run_engineering_rerun.ps1` 支持 `-PythonExe` 与 `-OutRoot` 参数，便于跨机器与按日期归档。

推荐命令示例（PowerShell）：

```powershell
.\scripts\run_engineering_rerun.ps1 -PythonExe C:\Users\chenpeng\miniconda3\envs\kan\python.exe
.\scripts\run_engineering_rerun.ps1 -PythonExe C:\Users\chenpeng\miniconda3\envs\kan\python.exe -OutRoot outputs/rerun_v2_engine_safe_20260318_rerun
```

## 4. 报告建议写法

建议在论文/汇报中分两段描述：

1. 历史参考结果（基于 `d8` 版本）
2. 工程版复测结果（基于当前 `main`）

并增加“差异原因”小节，至少覆盖：

1. 守护策略变化（安全性与稳定性收益）
2. 配置与可观测性增强（工程可维护性收益）
3. 指标口径升级（耗时字段定义变化）

## 5. 推荐单独文档

建议单独维护一份复测报告（例如：`docs/engineering_rerun_report.md`），包含：

1. 复测命令与配置快照
2. 关键结果表（acc/auc/edges/耗时）
3. 与 `d8` 参考结果对比表
4. 差异原因归因
5. 结论与下一步行动

这样做可以把“历史可复现性边界”和“工程版可交付结论”清晰隔离。

## 6. 当前状态

1. 历史参考版已经以 release 形式冻结，因此后续不需要频繁回到旧版本重新运行。
2. 工程版复测已完成两轮归档；当前建议优先引用最新 rerun：`outputs/rerun_v2_engine_safe_20260318_rerun/` 与 `docs/engineering_rerun_report.md`。
3. 后续新实验若继续基于当前主线，建议沿用同一文档口径：历史版只做参考锚点，工程版承担正式结论。
