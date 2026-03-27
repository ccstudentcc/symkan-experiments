"""Symbolic function library and expression utilities for symkan.

Maintains symbolic search libraries, expression complexity estimation, and
formatting helpers used throughout symbolic search.
"""

import re as _re
from math import floor, log10

import sympy as sp
import torch
from kan.Symbolic_KANLayer import SYMBOLIC_LIB as _SYM_LIB_REG

LIB_HIDDEN = ["x", "x^2", "tanh"]
LIB_OUTPUT = ["x", "x^2"]
FAST_LIB = ["x", "x^2", "x^3", "tanh", "sin", "cos", "exp", "log", "sqrt", "abs"]

EXPRESSIVE_LIB = list(_SYM_LIB_REG.keys())
FULL_LIB = EXPRESSIVE_LIB


_CUSTOM_REGISTERED = False
_SAFE_EXPR_PATTERN = _re.compile(r"^[0-9A-Za-z_+\-*/().,^ \t]+$")


def register_custom_functions():
    """Register symkan-specific symbolic functions into the pykan library.

    The default extensions are ``sigmoid``, ``softplus`` and ``softsign`` to broaden the
    search space. The function is idempotent and safe to call multiple times.
    """
    global _CUSTOM_REGISTERED
    if _CUSTOM_REGISTERED:
        return
    _CUSTOM_REGISTERED = True

    _SYM_LIB_REG["sigmoid"] = (
        lambda x: torch.sigmoid(x),
        lambda x: 1 / (1 + sp.exp(-x)),
        4,
        lambda x, y_th: ((), torch.sigmoid(x)),
    )

    _SYM_LIB_REG["softplus"] = (
        lambda x: torch.nn.functional.softplus(x),
        lambda x: sp.log(1 + sp.exp(x)),
        4,
        lambda x, y_th: ((), torch.nn.functional.softplus(x)),
    )

    _softsign_reg = (
        lambda x: x / (1 + torch.abs(x)),
        lambda x: x / (1 + sp.Abs(x)),
        3,
        lambda x, y_th: ((), x / (1 + torch.abs(x))),
    )
    _SYM_LIB_REG["softsign"] = _softsign_reg
    _SYM_LIB_REG["SoftSign"] = _softsign_reg


def _is_safe_expression_text(expr) -> bool:
    text = str(expr).strip()
    if not text:
        return False
    if "__" in text:
        return False
    return bool(_SAFE_EXPR_PATTERN.fullmatch(text))


def _is_nontrivial_expr(expr):
    if not _is_safe_expression_text(expr):
        return False
    try:
        sx = sp.sympify(expr)
        if sx is sp.S.Zero or sx.is_zero:
            return False
        if sx.is_number:
            return False
        return len(sx.free_symbols) > 0
    except Exception:
        s = str(expr).strip()
        return s not in {"0", "0.0", "0.", "None"} and any(ch.isalpha() for ch in s)


def count_expression_complexity(expr):
    """Estimate the complexity of a possible symbolic expression.

    Args:
        expr: Expression string that can be parsed by SymPy.

    Returns:
        int: Complexity score, where larger values indicate more complex structures.
    """
    if not _is_safe_expression_text(expr):
        return 1
    try:
        sx = sp.sympify(expr)
    except Exception:
        return 1

    def _count_nodes(e):
        if e.is_Atom:
            return 1
        return 1 + sum(_count_nodes(arg) for arg in e.args)

    return _count_nodes(sx)


def _to_formula_list(formulas):
    if formulas is None:
        return []
    if isinstance(formulas, tuple):
        if len(formulas) >= 1 and isinstance(formulas[0], (list, tuple)):
            return list(formulas[0])
        return list(formulas)
    if isinstance(formulas, list):
        return list(formulas)
    return [formulas]


def collect_valid_formulas(formulas):
    """Extract valid expressions together with complexity metadata.

    Args:
        formulas: Payload returned by ``symbolic_formula()`` or similar.

    Returns:
        list[dict]: Records containing ``index``, ``expr``, and ``complexity`` for each valid entry.
    """
    raw = _to_formula_list(formulas)
    valid = []
    for idx, expr in enumerate(raw):
        if _is_nontrivial_expr(expr):
            complexity = count_expression_complexity(expr)
            valid.append({"index": idx, "expr": str(expr), "complexity": complexity})
    return valid


def collect_all_formulas(formulas):
    """Collect all expressions including constants and zero expressions.

    Args:
        formulas: Payload returned by ``symbolic_formula()`` or similar.

    Returns:
        list[dict]: Records containing ``index``, ``expr``, and ``complexity`` for each expression.
    """
    raw = _to_formula_list(formulas)
    result = []
    for idx, expr in enumerate(raw):
        expr_str = str(expr) if expr is not None else "0"
        complexity = count_expression_complexity(expr_str)
        result.append({"index": idx, "expr": expr_str, "complexity": complexity})
    return result


def get_layer_lib(layer_idx, depth, lib_hidden=None, lib_output=None, lib=None):
    """Select the appropriate symbolic library for a given layer.

    Args:
        layer_idx: Layer index.
        depth: Network depth.
        lib_hidden: Hidden-layer library override.
        lib_output: Output-layer library override.
        lib: Single library that overrides the per-layer defaults.

    Returns:
        list: Function library used for symbolic fitting on the layer.
    """
    if lib is not None:
        return lib
    if layer_idx >= depth - 1:
        return lib_output or LIB_OUTPUT
    return lib_hidden or LIB_HIDDEN


def format_expr(expr_str, n_digits: int = 2):
    """Format floating point coefficients in an expression to a limited number of significant digits.

    Args:
        expr_str: Original expression string.
        n_digits: Number of significant digits.

    Returns:
        str: Expression string with formatted floating-point values.
    """
    def _round_match(m):
        val = float(m.group())
        if val == 0:
            return "0"
        magnitude = floor(log10(abs(val)))
        rounded = round(val, -int(magnitude) + (n_digits - 1))
        formatted = f"{rounded:.{max(0, -int(magnitude) + (n_digits - 1))}f}"
        if "." in formatted:
            formatted = formatted.rstrip("0").rstrip(".")
        return formatted

    pattern = r"-?\d+\.\d+(?:[eE][+-]?\d+)?"
    return _re.sub(pattern, _round_match, str(expr_str))
