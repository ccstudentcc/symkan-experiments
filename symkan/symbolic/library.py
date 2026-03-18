"""symkan 符号函数库与表达式处理工具。

该模块维护符号搜索函数库、表达式复杂度估计以及格式化辅助函数。
"""

import re as _re
from math import floor, log10

import sympy as sp
import torch
from kan.Symbolic_KANLayer import SYMBOLIC_LIB as _SYM_LIB_REG

LIB_HIDDEN = ["x", "x^2", "tanh"]
LIB_OUTPUT = ["x", "x^2"]
FAST_LIB = ["x", "x^2", "tanh", "sin", "cos", "exp", "log", "sqrt"]

# 全量符号库：自动对齐 kan 原生 SYMBOLIC_LIB（不含后续 symkan 自定义注册项）
EXPRESSIVE_LIB = list(_SYM_LIB_REG.keys())
# 兼容命名别名
FULL_LIB = EXPRESSIVE_LIB


_CUSTOM_REGISTERED = False
_SAFE_EXPR_PATTERN = _re.compile(r"^[0-9A-Za-z_+\-*/().,^ \t]+$")


def register_custom_functions():
    """注册 symkan 额外符号函数到 pykan 符号库。

    当前默认注册 ``sigmoid`` 与 ``softplus``，用于扩展符号搜索空间。
    该函数是幂等的，重复调用不会重复注册。
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
    """估计表达式复杂度。

    Args:
        expr: 可被 sympy 解析的表达式。

    Returns:
        int: 表达式复杂度分数，越大表示结构越复杂。
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
    """提取有效表达式并附带复杂度信息。

    Args:
        formulas: ``symbolic_formula()`` 返回对象或其变体。

    Returns:
        list[dict]: 每项包含 ``index``、``expr`` 和 ``complexity`` 的有效表达式记录。
    """
    raw = _to_formula_list(formulas)
    valid = []
    for idx, expr in enumerate(raw):
        if _is_nontrivial_expr(expr):
            complexity = count_expression_complexity(expr)
            valid.append({"index": idx, "expr": str(expr), "complexity": complexity})
    return valid


def collect_all_formulas(formulas):
    """收集全部表达式，包括零表达式和常数表达式。

    Args:
        formulas: ``symbolic_formula()`` 返回对象或其变体。

    Returns:
        list[dict]: 每项包含 ``index``、``expr`` 和 ``complexity`` 的表达式记录。
    """
    raw = _to_formula_list(formulas)
    result = []
    for idx, expr in enumerate(raw):
        expr_str = str(expr) if expr is not None else "0"
        complexity = count_expression_complexity(expr_str)
        result.append({"index": idx, "expr": expr_str, "complexity": complexity})
    return result


def get_layer_lib(layer_idx, depth, lib_hidden=None, lib_output=None, lib=None):
    """按层选择符号函数库。

    Args:
        layer_idx: 当前层索引。
        depth: 网络深度。
        lib_hidden: 隐藏层函数库。
        lib_output: 输出层函数库。
        lib: 统一函数库；若提供则覆盖分层库。

    Returns:
        list: 当前层用于符号拟合的函数库。
    """
    if lib is not None:
        return lib
    if layer_idx >= depth - 1:
        return lib_output or LIB_OUTPUT
    return lib_hidden or LIB_HIDDEN


def format_expr(expr_str, n_digits: int = 2):
    """将表达式中的浮点系数格式化为有限有效数字。

    Args:
        expr_str: 原始表达式字符串。
        n_digits: 有效数字位数。

    Returns:
        str: 格式化后的表达式字符串。
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
