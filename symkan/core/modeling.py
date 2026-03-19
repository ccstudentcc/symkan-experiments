"""Compatibility export layer.

All public names have migrated to ``infer.py`` and ``train.py``.
Legacy code can still import through ``symkan.core.modeling`` for backward compatibility.
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
