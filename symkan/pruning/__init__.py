"""symkan 剪枝与归因模块公共接口导出。

该模块暴露带容错逻辑的特征归因计算入口。
"""

from .attribution import safe_attribute, safe_attribute_report

__all__ = ["safe_attribute", "safe_attribute_report"]
