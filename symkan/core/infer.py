"""symkan inference and evaluation primitives.

Migrated from the original modeling.py module. Provides logits computation,
accuracy helpers, and edge-count reporting.
"""

from typing import Optional

import numpy as np
import torch
from sklearn.metrics import accuracy_score

from .runtime import get_device, resolve_device


def _infer_model_device(model):
    """Infer the device currently used by a model.

    Args:
        model: Model-like object exposing parameters or buffers.

    Returns:
        torch.device: Inferred model device, or the current global runtime
        device as a fallback.
    """
    try:
        return next(model.parameters()).device
    except Exception:
        pass
    try:
        return next(model.buffers()).device
    except Exception:
        pass
    return resolve_device(get_device())


def _pick_device(model, device: Optional[str] = None):
    """Resolve the effective inference device for a call.

    Args:
        model: Model-like object used for fallback device inference.
        device: Optional explicit device override.

    Returns:
        torch.device: Resolved device object.
    """
    if device is not None and str(device).lower() != "auto":
        return resolve_device(device)
    return _infer_model_device(model)


def _label_tensor_to_indices(labels, *, device: torch.device, split: str) -> torch.Tensor:
    """Convert labels to integer class indices for metric computation.

    Args:
        labels: Raw labels as indices, one-hot labels, or probability labels.
        device: Target device for the normalized tensor.
        split: Dataset split name used in validation errors.

    Returns:
        torch.Tensor: Rank-1 tensor of integer class indices.

    Raises:
        ValueError: If labels are invalid or have an unsupported rank.
    """
    if not torch.is_tensor(labels):
        tensor = torch.as_tensor(labels, device=device)
    else:
        tensor = labels.to(device)

    if tensor.ndim == 1:
        if tensor.dtype.is_floating_point:
            rounded = tensor.round()
            if not torch.allclose(tensor, rounded):
                raise ValueError(f"{split} 1D labels must be integer class indices")
            tensor = rounded
        indices = tensor.to(torch.long)
        if torch.any(indices < 0):
            raise ValueError(f"{split} labels must be non-negative class indices")
        return indices

    if tensor.ndim == 2:
        if tensor.shape[1] <= 0:
            raise ValueError(f"{split} 2D labels must have non-zero class dimension")
        return torch.argmax(tensor, dim=1).to(torch.long)

    raise ValueError(
        f"{split} labels must be rank-1 class indices or rank-2 one-hot/probability matrix; "
        f"got rank={tensor.ndim}"
    )


def model_logits(model, X, device: Optional[str] = None):
    """Compute model logits using a NumPy-friendly path.

    Args:
        model: KAN/symkan model object.
        X: Input feature array.
        device: Optional override device; auto-infer if ``None``.

    Returns:
        numpy.ndarray: Logits array.
    """
    was_training = bool(getattr(model, "training", False))
    model.eval()
    dev = _pick_device(model, device)
    try:
        with torch.no_grad():
            x = torch.as_tensor(X, dtype=torch.float32, device=dev)
            return model(x).detach().cpu().numpy()
    finally:
        if hasattr(model, "train"):
            model.train(was_training)


def model_logits_ds(model, dataset, split: str = "test", device: Optional[str] = None):
    """Compute model logits directly from dataset tensors.

    Args:
        model: KAN/symkan model object.
        dataset: Dataset dictionary produced by ``build_dataset``.
        split: Split name to read (``train``, ``val``, or ``test``).
        device: Optional override device; auto-infer if ``None``.

    Returns:
        torch.Tensor: Logits tensor.

    Raises:
        ValueError: When the requested split is missing or empty.
    """
    was_training = bool(getattr(model, "training", False))
    model.eval()
    dev = _pick_device(model, device)
    try:
        input_key = f"{split}_input"
        if input_key not in dataset or dataset[input_key] is None:
            raise ValueError(f"Dataset missing usable split: {split}")
        x = dataset[input_key]
        if not torch.is_tensor(x):
            x = torch.as_tensor(x, dtype=torch.float32, device=dev)
        else:
            x = x.to(dev)
        with torch.inference_mode():
            logits = model(x)
        return logits
    finally:
        if hasattr(model, "train"):
            model.train(was_training)


def model_acc(model, X, y_cls, device: Optional[str] = None):
    """Compute classification accuracy via the NumPy logits path.

    Args:
        model: KAN/symkan model object.
        X: Input feature array.
        y_cls: Class index labels.
        device: Optional override device; auto-infer if ``None``.

    Returns:
        float: Classification accuracy.
    """
    pred = np.argmax(model_logits(model, X, device=device), axis=1)
    return accuracy_score(y_cls, pred)


def model_acc_ds_fast(model, dataset, split: str = "test", device: Optional[str] = None):
    """Compute classification accuracy via the tensor-based fast path.

    Args:
        model: KAN/symkan model object.
        dataset: Dataset dictionary produced by ``build_dataset``.
        split: Split name to use (``train``, ``val``, or ``test``).
        device: Optional override device; auto-infer if ``None``.

    Returns:
        float: Classification accuracy.

    Raises:
        ValueError: When the requested split is missing or empty.
    """
    logits = model_logits_ds(model, dataset, split=split, device=device)
    label_key = f"{split}_label"
    if label_key not in dataset or dataset[label_key] is None:
        raise ValueError(f"Dataset missing usable split: {split}")
    pred = torch.argmax(logits, dim=1)
    y = _label_tensor_to_indices(dataset[label_key], device=pred.device, split=split)
    return (pred == y).float().mean().item()


def model_acc_ds(model, dataset, split: str = "test", device: Optional[str] = None):
    """Unified accuracy helper that prefers the fast tensor path with fallback.

    Args:
        model: KAN/symkan model object.
        dataset: Dataset dictionary produced by ``build_dataset``.
        split: Split name to use (``train``, ``val``, or ``test``).
        device: Optional override device; auto-infer if ``None``.

    Returns:
        float: Classification accuracy.

    Raises:
        ValueError: When ``split='val'`` but the validation split is unavailable.
    """
    try:
        return model_acc_ds_fast(model, dataset, split=split, device=device)
    except (KeyError, ValueError) as exc:
        if split == "val":
            raise ValueError(
                "Validation split unavailable; set validation_ratio>0 in build_dataset"
                " or disable use_validation in stagewise_train."
            ) from exc
        raise
    except Exception:
        # In extreme cases fall back to the NumPy path to maximize availability.
        x = dataset[f"{split}_input"]
        y = dataset[f"{split}_label"]
        if torch.is_tensor(x):
            x = x.detach().cpu().numpy()
        else:
            x = np.asarray(x)
        if torch.is_tensor(y):
            y = y.detach().cpu().numpy()
        else:
            y = np.asarray(y)
        if y.ndim == 1:
            if np.issubdtype(y.dtype, np.floating):
                rounded = np.rint(y)
                if not np.allclose(y, rounded):
                    raise ValueError(f"{split} 1D labels must be integer class indices")
                y = rounded
            y = y.astype(np.int64, copy=False)
            if np.any(y < 0):
                raise ValueError(f"{split} labels must be non-negative class indices")
        elif y.ndim == 2:
            if y.shape[1] <= 0:
                raise ValueError(f"{split} 2D labels must have non-zero class dimension")
            y = np.argmax(y, axis=1)
        else:
            raise ValueError(
                f"{split} labels must be rank-1 class indices or rank-2 one-hot/probability matrix; "
                f"got rank={y.ndim}"
            )
        return model_acc(model, x, y, device=device)


def get_n_edge(model):
    """Return the current edge count for the model.

    Args:
        model: KAN/symkan model object.

    Returns:
        int | float: Integer edge count when available, otherwise ``numpy.nan``.
    """
    try:
        return int(model.n_edge)
    except Exception:
        return np.nan
