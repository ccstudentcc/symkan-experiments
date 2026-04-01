# 工程版实验报告入口

本文档不再承载单轮实验的完整正文，而是作为带日期实验报告的统一入口。

## 当前使用规则

1. 若需要查看当前 ICBR backend 对照的正式正文，读 [engineering_rerun_report_20260401.md](engineering_rerun_report_20260401.md)。
2. 若需要查看 `bspline baseline` vs `radial_bf` 的历史工程专题结果，读 [engineering_rerun_report_20260327.md](engineering_rerun_report_20260327.md)。
3. 若需要先理解“历史版、当前工程版、paired compare、单边补充切片”的口径边界，先读 [engineering_version_rerun_note.md](engineering_version_rerun_note.md)。

## 报告清单

### 1. 2026-04-01 ICBR backend 对照

- 文件：[engineering_rerun_report_20260401.md](engineering_rerun_report_20260401.md)
- 主题：`baseline` vs `baseline_icbr`、`baseline_fastlib` vs `baseline_icbr_fastlib`，以及 `baseline_icbr_fulllib` 的补充单边切片。
- 关键用途：
  - paired backend-only 证据
  - FAST_LIB 速度收益
  - full library 下 ICBR 的单边可运行性与收益

### 2. 2026-03-27 radial_bf 工程专题

- 文件：[engineering_rerun_report_20260327.md](engineering_rerun_report_20260327.md)
- 主题：`baseline (bspline)` vs `radial_bf` 的历史工程切片。
- 关键用途：
  - 历史工程参考
  - `radial_bf` 路径的速度/质量权衡
  - 与当前 ICBR backend 对照区分开来的旧专题结果

## 维护规则

1. 新增或重写工程实验报告时，优先新建带日期文件，而不是覆盖旧报告正文。
2. 本入口只负责导航、分层和推荐阅读顺序；具体数值、命令和实验条件应写入对应的带日期报告。
3. 若某轮实验会成为新的主引用，应在本文件、[README.md](../README.md)、[index.md](index.md) 与 [engineering_version_rerun_note.md](engineering_version_rerun_note.md) 中同步更新入口。
