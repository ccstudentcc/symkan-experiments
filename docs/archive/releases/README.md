# 发布记录归档说明

本目录用于归档每次工程版发布的“已填写记录”，不存放模板。

## 命名规则

1. 文件命名：`engineering_release_record_YYYYMMDD.md`
2. 示例：`engineering_release_record_20260319.md`
3. 同一天多次发布可追加后缀：`engineering_release_record_YYYYMMDD_rerun.md`

## 记录内容建议

1. 发布日期、分支、tag、主引用结果目录。
2. 默认验证环境（OS / Shell / Python）。
3. 本次发布关键结论与边界说明。
4. 与模板检查项对应的执行摘要（测试、入口命令、工作区状态）。

## 与模板关系

1. 模板文件位于 [../../engineering_release_checklist.md](../../engineering_release_checklist.md)。
2. 每次发布先按模板执行，再将“本次结果”沉淀到本目录归档文件。

## 关联入口

1. docs 总入口：[../../index.md](../../index.md)
2. 文档同步矩阵（SSOT）：[../../doc_sync_matrix.md](../../doc_sync_matrix.md)
