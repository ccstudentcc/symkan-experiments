"""Public exports for symkan's evaluation module.

Provides formula validation, multiclass ROC/AUC computation, and plotting helpers.
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
