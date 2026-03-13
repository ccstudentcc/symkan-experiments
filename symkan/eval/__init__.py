"""symkan 评估模块公共接口导出。

提供公式数值一致性验证、多分类 ROC/AUC 计算与可视化接口。
"""
from .metrics import (
    validate_formula_numerically,
    compute_multiclass_roc_auc,
    plot_roc_curves,
)

__all__ = [
    "validate_formula_numerically",
    "compute_multiclass_roc_auc",
    "plot_roc_curves",
]
