"""Evaluation metrics and visualization helpers for symkan."""

import numpy as np
import pandas as pd
import sympy as sp
from sklearn.metrics import auc, roc_curve

from symkan.core import model_logits, model_logits_ds
from symkan.symbolic.library import collect_valid_formulas


_LAMBDA_CACHE = {}


def _get_compiled_formula(expr_str, n_feat):
    """Compile and cache a symbolic expression for NumPy evaluation.

    Args:
        expr_str: Symbolic expression text.
        n_feat: Number of input features referenced by the expression.

    Returns:
        Callable[..., Any]: Cached callable produced by ``sympy.lambdify``.
    """
    key = (expr_str, int(n_feat))
    cached = _LAMBDA_CACHE.get(key)
    if cached is not None:
        return cached

    expr = sp.sympify(expr_str)
    sym_vars = [sp.Symbol(f"x_{i}") for i in range(n_feat)]
    numpy_modules = [
        {
            "softplus": lambda x: np.log1p(np.exp(np.clip(x, -500, 500))),
            "Abs": np.abs,
            "sigmoid": lambda x: 1.0 / (1.0 + np.exp(np.clip(-x, -500, 500))),
        },
        "numpy",
    ]
    compiled = sp.lambdify(sym_vars, expr, modules=numpy_modules)
    _LAMBDA_CACHE[key] = compiled
    return compiled


def validate_formula_numerically(model, formulas, dataset, n_sample: int = 500):
    """Validate symbolic formulas numerically against model outputs.

    Args:
        model: Symbolized model instance.
        formulas: Payload from ``symbolic_formula()``.
        dataset: Dataset dict from ``build_dataset``.
        n_sample: Maximum number of samples used in validation.

    Returns:
        pandas.DataFrame | None: R², complexity, and stability information per expression.
    """
    if formulas is None:
        return None

    valid = collect_valid_formulas(formulas)
    if not valid:
        return None

    test_input = dataset["test_input"][:n_sample]
    actual_n = int(test_input.shape[0])
    if actual_n <= 0:
        return pd.DataFrame(columns=["index", "r2", "complexity", "numerically_unstable"])

    X = test_input.detach().cpu().numpy()
    y_model = model_logits_ds(model, {"test_input": test_input}, split="test").detach().cpu().numpy()

    n_feat = X.shape[1]

    results = []
    for item in valid:
        try:
            f = _get_compiled_formula(item["expr"], n_feat)
            y_sym = f(*[X[:, i] for i in range(n_feat)])
            if isinstance(y_sym, (int, float)):
                y_sym = np.full(actual_n, y_sym)
            y_sym = np.array(y_sym, dtype=np.float64).flatten()

            has_extreme = bool(np.any(np.abs(y_sym) > 1e6) or np.any(np.isnan(y_sym)) or np.any(np.isinf(y_sym)))
            y_sym = np.clip(y_sym, -100, 100)
            y_sym = np.nan_to_num(y_sym, nan=0.0, posinf=100.0, neginf=-100.0)

            idx = item["index"]
            y_ref = y_model[:, idx] if idx < y_model.shape[1] else np.zeros(actual_n)
            ss_res = np.sum((y_ref - y_sym) ** 2)
            ss_tot = np.sum((y_ref - np.mean(y_ref)) ** 2) + 1e-12
            r2 = 1.0 - ss_res / ss_tot

            results.append({"index": idx, "r2": float(r2), "complexity": item["complexity"], "numerically_unstable": has_extreme})
        except Exception as e:
            results.append({"index": item["index"], "r2": np.nan, "complexity": item["complexity"], "error": str(e), "numerically_unstable": True})

    return pd.DataFrame(results)


def compute_multiclass_roc_auc(y_true_onehot, y_score):
    """Compute ROC curves and AUC for each class.

    Args:
        y_true_onehot: One-hot encoded true labels.
        y_score: Prediction scores or probabilities per class.

    Returns:
        dict: ``fpr/tpr/auc`` entries for each class.
    """
    n_classes = y_true_onehot.shape[1]
    roc_data = {}
    for c in range(n_classes):
        try:
            fpr, tpr, _ = roc_curve(y_true_onehot[:, c], y_score[:, c])
            roc_auc = auc(fpr, tpr)
        except Exception:
            fpr, tpr, roc_auc = np.array([0, 1]), np.array([0, 1]), 0.5
        roc_data[c] = {"fpr": fpr, "tpr": tpr, "auc": float(roc_auc)}
    return roc_data


def plot_roc_curves(roc_data, class_labels=None, title="ROC Curves (Per Class)"):
    """Plot multiclass ROC curves.

    Args:
        roc_data: Result dict returned by ``compute_multiclass_roc_auc``.
        class_labels: Optional display names for each class.
        title: Chart title.
    """
    import matplotlib.pyplot as plt

    n_classes = len(roc_data)
    if class_labels is None:
        class_labels = [str(i) for i in range(n_classes)]

    fig, ax = plt.subplots(figsize=(8, 6))
    cmap = plt.cm.get_cmap("tab10", n_classes)

    for c in range(n_classes):
        d = roc_data[c]
        ax.plot(d["fpr"], d["tpr"], color=cmap(c), lw=1.5, label=f"Class {class_labels[c]}, AUC = {d['auc']:.3f}")

    ax.plot([0, 1], [0, 1], "k--", lw=0.8, alpha=0.5, label="Random Baseline")
    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate")
    ax.set_title(title)
    ax.set_xlim([0, 1])
    ax.set_ylim([0, 1.02])
    ax.legend(loc="lower right", fontsize=8, framealpha=0.8)
    ax.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()


__all__ = [
    "validate_formula_numerically",
    "compute_multiclass_roc_auc",
    "plot_roc_curves",
    "model_logits",
]
