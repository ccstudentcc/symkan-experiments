# 工程版复测与历史结果口径说明

## 1. 文档目的

本文档用于界定“历史参考版本”与“当前工程版本”在实验口径上的差异，并给出统一的报告叙述框架。核心目标是避免将两代实现的结果直接混合比较，从而降低结论解释偏差。

## 2. 版本分层定义

1. 历史参考版：`d8e09b5edadb988bd4a1638ea7109cf3ff5ef7d7`，对应 pre-release `v1.0.0-legacy-d8`。
2. 当前工程版：`main` 分支（包含配置模块化、守护策略分级、可观测性增强等工程化改造）。

建议在论文、报告或答辩材料中显式声明：历史版本仅作为参考锚点，工程版本用于当前正式结论。

## 3. 两代结果不可直接等价的原因

1. 训练与剪枝守护策略存在实质差异，尤其体现在失败边界判定与回滚机制。
2. 工程版扩展了耗时指标体系，新增 `run_total_wall_time_s`、`symbolize_wall_time_s` 等字段，统计口径较历史版本更细。
3. 配置管理方式由分散参数传递转为 `AppConfig` 统一入口，CLI 仅承担受控覆盖，实验可重复性语义发生变化。

因此，工程版与历史版间出现时延差异属于方法学差异下的预期现象，不宜直接解释为模型性能退化。

## 4. 工程版复测默认设定（2026-03）

1. `stagewise.guard_mode = light`
2. `stagewise.prune_acc_drop_tol = 0.08`
3. 首轮归档目录：`outputs/rerun_v2_engine_safe_20260318/`
4. 同日复跑归档目录：`outputs/rerun_v2_engine_safe_20260318_rerun/`
5. 复跑脚本：`scripts/run_engineering_rerun.ps1`，支持 `-PythonExe` 与 `-OutRoot` 参数。
6. 命令默认执行环境：`PowerShell`（Windows）。

本轮工程版复测环境（用于口径说明）：

1. 操作系统：Windows 11 专业版 `23H2`（OS Build `22631.5472`）。
2. Python 环境：`Miniconda` 的 `kan` 环境，解释器路径 `C:\Users\chenpeng\miniconda3\envs\kan\python.exe`（Python `3.9.25`）。
3. CPU：`12th Gen Intel(R) Core(TM) i5-12500H`。
4. 内存：`16 GB`。
5. 运行路径：`PyTorch 2.1.2+cpu`，本轮复测按 CPU 路径执行。

推荐执行命令（PowerShell）：

```powershell
# 运行目录：仓库根目录（symkan-experiments/）
.\scripts\run_engineering_rerun.ps1 -PythonExe C:\Users\chenpeng\miniconda3\envs\kan\python.exe
.\scripts\run_engineering_rerun.ps1 -PythonExe C:\Users\chenpeng\miniconda3\envs\kan\python.exe -OutRoot outputs/rerun_v2_engine_safe_20260318_rerun
```

## 5. 报告书写建议

建议采用“两层叙述”结构：

1. 历史参考结果（基于 `d8` 版本）：用于提供研究脉络与可复现边界。
2. 工程版复测结果（基于当前 `main`）：用于支撑当前版本的正式结论。

同时应设置“差异归因”小节，至少覆盖以下维度：

1. 守护策略变化带来的稳定性与安全收益。
2. 配置与可观测性增强带来的工程可维护性收益。
3. 指标口径升级对耗时对比解释的影响。

## 6. 建议配套文档

建议维护独立复测报告（如 `docs/engineering_rerun_report.md`），至少包含：

1. 复测命令与配置快照；
2. 关键指标统计表（`acc/auc/edges/time`）；
3. 与 `d8` 参考结果的对照表；
4. 差异原因与方法学解释；
5. 后续优化方向与优先级。

该做法可在文档层面清晰区分“历史可复现性边界”与“工程版可交付结论”。

## 7. 当前状态

1. 历史参考版已通过 release 冻结，不再建议频繁回切旧版本重跑。
2. 工程版已完成两轮归档，当前建议优先引用 `outputs/rerun_v2_engine_safe_20260318_rerun/` 及其配套报告。
3. 后续实验若继续基于主线迭代，应保持本口径：历史版用于参考，工程版用于正式结论。
