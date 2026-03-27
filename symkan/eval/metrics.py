"""Evaluation metrics and visualization helpers for symkan."""

import re

import numpy as np
import pandas as pd
import sympy as sp
from sklearn.metrics import auc, roc_curve

from symkan.core import model_logits, model_logits_ds
from symkan.symbolic.library import collect_valid_formulas


_LAMBDA_CACHE = {}
_INPUT_SYMBOL_PATTERN = re.compile(r"^x_(\d+)$")


def _extract_input_symbol_indices(expr) -> list[int]:
    indices: list[int] = []
    for symbol in expr.free_symbols:
        match = _INPUT_SYMBOL_PATTERN.fullmatch(str(symbol))
        if match:
            indices.append(int(match.group(1)))
    return sorted(set(indices))


def _build_symbol_maps(symbol_indices: list[int], n_feat: int) -> list[dict[int, int]]:
    if not symbol_indices:
        return [{}]

    min_idx = min(symbol_indices)
    max_idx = max(symbol_indices)
    zero_based_ok = min_idx >= 0 and max_idx < n_feat
    one_based_ok = min_idx >= 1 and max_idx <= n_feat

    maps: list[dict[int, int]] = []
    # symbolic_formula() in MultKAN emits x_1..x_n by default, so prefer one-based
    # when x_0 is absent and both mappings are technically possible.
    if one_based_ok and 0 not in symbol_indices:
        maps.append({idx: idx - 1 for idx in symbol_indices})
    if zero_based_ok:
        maps.append({idx: idx for idx in symbol_indices})
    if one_based_ok and (0 in symbol_indices):
        maps.append({idx: idx - 1 for idx in symbol_indices})

    return maps


def _get_compiled_formula(expr_str, symbol_indices: tuple[int, ...]):
    """Compile and cache a symbolic expression for NumPy evaluation.

    Args:
        expr_str: Symbolic expression text.
        symbol_indices: Ordered input symbol indices used by the expression.

    Returns:
        Callable[..., Any]: Cached callable produced by ``sympy.lambdify``.
    """
    key = (expr_str, symbol_indices)
    cached = _LAMBDA_CACHE.get(key)
    if cached is not None:
        return cached

    expr = sp.sympify(expr_str)
    sym_vars = [sp.Symbol(f"x_{i}") for i in symbol_indices]
    numpy_modules = [
        {
            "softplus": lambda x: np.log1p(np.exp(np.clip(x, -500, 500))),
            "softsign": lambda x: x / (1.0 + np.abs(x)),
            "SoftSign": lambda x: x / (1.0 + np.abs(x)),
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
        idx = item["index"]
        y_ref = y_model[:, idx] if idx < y_model.shape[1] else np.zeros(actual_n)
        try:
            expr = sp.sympify(item["expr"])
            symbol_indices = _extract_input_symbol_indices(expr)
            symbol_maps = _build_symbol_maps(symbol_indices, n_feat)
            if not symbol_maps:
                raise ValueError(
                    f"input symbol indices out of range for n_feat={n_feat}: {symbol_indices}"
                )

            best_result = None
            eval_errors: list[str] = []
            for symbol_map in symbol_maps:
                ordered_symbols = tuple(sorted(symbol_map))
                f = _get_compiled_formula(item["expr"], ordered_symbols)
                args = [X[:, symbol_map[symbol_idx]] for symbol_idx in ordered_symbols]
                try:
                    y_sym = f(*args)
                    if isinstance(y_sym, (int, float)):
                        y_sym = np.full(actual_n, y_sym)
                    y_sym = np.array(y_sym, dtype=np.float64).flatten()

                    has_extreme = bool(
                        np.any(np.abs(y_sym) > 1e6) or np.any(np.isnan(y_sym)) or np.any(np.isinf(y_sym))
                    )
                    y_sym = np.clip(y_sym, -100, 100)
                    y_sym = np.nan_to_num(y_sym, nan=0.0, posinf=100.0, neginf=-100.0)

                    ss_res = np.sum((y_ref - y_sym) ** 2)
                    ss_tot = np.sum((y_ref - np.mean(y_ref)) ** 2) + 1e-12
                    r2 = 1.0 - ss_res / ss_tot

                    candidate = (float(r2), bool(has_extreme))
                    if best_result is None or candidate[0] > best_result[0]:
                        best_result = candidate
                except Exception as mapping_exc:
                    eval_errors.append(str(mapping_exc))

            if best_result is None:
                raise RuntimeError("; ".join(eval_errors) if eval_errors else "formula evaluation failed")

            r2, has_extreme = best_result

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
