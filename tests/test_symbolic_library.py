from __future__ import annotations

import numpy as np
import sympy as sp
import torch

from kan.Symbolic_KANLayer import SYMBOLIC_LIB as _SYM_LIB_REG
from symkan.eval.metrics import _get_compiled_formula
from symkan.symbolic.library import register_custom_functions


def test_register_custom_functions_adds_softsign_aliases() -> None:
    register_custom_functions()

    assert "softsign" in _SYM_LIB_REG
    assert "SoftSign" in _SYM_LIB_REG

    torch_fn = _SYM_LIB_REG["softsign"][0]
    x = torch.tensor([-2.0, -0.5, 0.0, 0.5, 2.0], dtype=torch.float32)
    expected = x / (1.0 + torch.abs(x))
    assert torch.allclose(torch_fn(x), expected)

    sympy_fn = _SYM_LIB_REG["softsign"][1]
    sym_x = sp.Symbol("x")
    expected_expr = sym_x / (1 + sp.Abs(sym_x))
    assert sp.simplify(sympy_fn(sym_x) - expected_expr) == 0


def test_formula_eval_supports_softsign_aliases() -> None:
    register_custom_functions()
    compiled = _get_compiled_formula("softsign(x_0) + SoftSign(x_1)", n_feat=2)

    x0 = np.array([-2.0, 0.0, 2.0], dtype=np.float64)
    x1 = np.array([1.0, -1.0, 0.5], dtype=np.float64)
    y = np.asarray(compiled(x0, x1), dtype=np.float64)

    expected = x0 / (1.0 + np.abs(x0)) + x1 / (1.0 + np.abs(x1))
    assert np.allclose(y, expected)
