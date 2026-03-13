"""@file
@brief 兼容层 — 所有公共名字已迁移到 infer.py 和 train.py。

旧代码可继续 ``from symkan.core.modeling import ...`` 而不会中断。
"""

# Re-export inference primitives
from .infer import (  # noqa: F401
    _infer_model_device,
    _pick_device,
    model_logits,
    model_logits_ds,
    model_acc,
    model_acc_ds_fast,
    model_acc_ds,
    get_n_edge,
)

# Re-export training primitives
from .train import (  # noqa: F401
    _ensure_model_history_path,
    safe_fit,
    safe_fit_report,
)
