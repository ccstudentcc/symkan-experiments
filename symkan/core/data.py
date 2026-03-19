"""symkan dataset construction and optional validation-split utilities."""

import warnings
from typing import Optional

import numpy as np
import torch
import torch.nn.functional as F

from .runtime import get_device, resolve_device


def _resolve_device(device: Optional[str] = None) -> str:
    """Resolve the device string used during dataset construction.

    Args:
        device: Override device; uses the global default for ``None`` or ``auto``.

    Returns:
        str: Device string such as ``cpu`` or ``cuda``.
    """
    if device is None or device == "auto":
        return get_device()
    return device


def _split_train_validation(
    train_input: torch.Tensor,
    train_label: torch.Tensor,
    validation_ratio: float = 0.0,
    seed: Optional[int] = None,
    min_val_samples: int = 10,
):
    """Create an optional validation split from the training data.

    Args:
        train_input: Training input tensor.
        train_label: Training label tensor.
        validation_ratio: Fraction of data to reserve for validation.
        seed: RNG seed for splitting.
        min_val_samples: Minimum number of validation samples.

    Returns:
        tuple[torch.Tensor, torch.Tensor, torch.Tensor | None, torch.Tensor | None]:
        Train and validation tensors.
    """
    if validation_ratio <= 0:
        return train_input, train_label, None, None

    n_total = int(train_input.shape[0])
    if n_total <= 1:
        warnings.warn(
            f"训练样本过少 (n_total={n_total})，禁用验证集切分。",
            category=UserWarning,
            stacklevel=2,
        )
        return train_input, train_label, None, None

    ratio = float(validation_ratio)
    n_val = int(n_total * ratio)
    # Inflate the ratio when the naive split would leave too few validation samples.
    if n_val < min_val_samples:
        adjusted_ratio = min(float(min_val_samples) / float(n_total), 0.3)
        if adjusted_ratio > ratio:
            warnings.warn(
                f"validation_ratio 从 {ratio:.3f} 调整为 {adjusted_ratio:.3f}，"
                f"以保证至少 {min_val_samples} 个验证样本。",
                category=UserWarning,
                stacklevel=2,
            )
            ratio = adjusted_ratio
            n_val = int(n_total * ratio)

    if n_val < min_val_samples:
        warnings.warn(
            f"训练样本不足以稳定切分验证集 (n_total={n_total})，已禁用验证集。",
            category=UserWarning,
            stacklevel=2,
        )
        return train_input, train_label, None, None

    rng = np.random.default_rng(seed)
    indices = rng.permutation(n_total)
    device = train_input.device
    val_idx = torch.as_tensor(indices[:n_val], dtype=torch.long, device=device)
    train_idx = torch.as_tensor(indices[n_val:], dtype=torch.long, device=device)
    return (
        train_input[train_idx],
        train_label[train_idx],
        train_input[val_idx],
        train_label[val_idx],
    )


def _to_label_tensor(y, *, device: torch.device, split: str) -> torch.Tensor:
    """Normalize raw labels into a validated tensor representation.

    Args:
        y: Raw label payload, typically a NumPy array or tensor.
        device: Target device for the returned tensor.
        split: Dataset split name used in validation errors.

    Returns:
        torch.Tensor: Rank-1 class indices or rank-2 float labels.

    Raises:
        ValueError: If labels are empty, negative, non-integer 1D floats, or
            have an unsupported rank.
    """
    tensor = torch.as_tensor(y, device=device)
    if tensor.ndim == 1:
        if tensor.numel() == 0:
            raise ValueError(f"{split} labels cannot be empty")
        if tensor.dtype.is_floating_point:
            rounded = tensor.round()
            if not torch.allclose(tensor, rounded):
                raise ValueError(f"{split} 1D labels must be integer class indices")
            tensor = rounded.to(torch.long)
        else:
            tensor = tensor.to(torch.long)
        if torch.any(tensor < 0):
            raise ValueError(f"{split} labels must be non-negative class indices")
        return tensor
    if tensor.ndim == 2:
        if tensor.shape[1] <= 0:
            raise ValueError(f"{split} 2D labels must have non-zero class dimension")
        return tensor.to(torch.float32)
    raise ValueError(
        f"{split} labels must be rank-1 class indices or rank-2 one-hot/probability matrix; "
        f"got rank={tensor.ndim}"
    )


def _to_one_hot_if_needed(
    train_label: torch.Tensor,
    test_label: torch.Tensor,
) -> tuple[torch.Tensor, torch.Tensor]:
    """Convert index labels to one-hot labels while preserving valid 2D labels.

    Args:
        train_label: Training labels as class indices or 2D label matrix.
        test_label: Test labels as class indices or 2D label matrix.

    Returns:
        tuple[torch.Tensor, torch.Tensor]: Training and test labels in a shared
        one-hot-compatible 2D format.

    Raises:
        ValueError: If train and test labels imply incompatible class
            dimensions.
    """
    train_is_index = train_label.ndim == 1
    test_is_index = test_label.ndim == 1

    if not train_is_index and not test_is_index:
        if train_label.shape[1] != test_label.shape[1]:
            raise ValueError(
                "train/test 2D labels must use the same class dimension; "
                f"got train={train_label.shape[1]}, test={test_label.shape[1]}"
            )
        return train_label, test_label

    if train_is_index and test_is_index:
        n_classes = int(max(train_label.max().item(), test_label.max().item())) + 1
        return (
            F.one_hot(train_label, num_classes=n_classes).to(torch.float32),
            F.one_hot(test_label, num_classes=n_classes).to(torch.float32),
        )

    if not train_is_index:
        n_classes = int(train_label.shape[1])
        if torch.any(test_label >= n_classes):
            raise ValueError(
                f"test labels contain class index >= train class dimension ({n_classes})"
            )
        return train_label, F.one_hot(test_label, num_classes=n_classes).to(torch.float32)

    n_classes = int(test_label.shape[1])
    if torch.any(train_label >= n_classes):
        raise ValueError(
            f"train labels contain class index >= test class dimension ({n_classes})"
        )
    return F.one_hot(train_label, num_classes=n_classes).to(torch.float32), test_label


def _validate_sample_count(
    x: torch.Tensor,
    y: torch.Tensor,
    *,
    split: str,
) -> None:
    """Validate that inputs and labels contain the same number of samples.

    Args:
        x: Input tensor for the split.
        y: Label tensor for the split.
        split: Dataset split name used in validation errors.

    Raises:
        ValueError: If the sample counts do not match.
    """
    if x.shape[0] != y.shape[0]:
        raise ValueError(
            f"{split} input/label sample count mismatch: "
            f"input={int(x.shape[0])}, labels={int(y.shape[0])}"
        )


def build_dataset(
    Xtr,
    Ytr,
    Xte,
    Yte,
    device: Optional[str] = None,
    validation_ratio: float = 0.0,
    seed: Optional[int] = None,
    min_val_samples: int = 10,
):
    """Build a unified dataset dictionary for KAN and symkan.

    Args:
        Xtr: Training inputs array.
        Ytr: Training labels array (often one-hot).
        Xte: Test inputs array.
        Yte: Test labels array (often one-hot).
        device: Target device string, supports ``auto``, ``cpu``, ``cuda``.
        validation_ratio: Fraction reserved for validation; ``0.0`` disables.
        seed: RNG seed for validation split.
        min_val_samples: Minimum number of validation samples.

    Returns:
        dict: Tensor dictionary with ``train_input``, ``train_label``, ``val_input``,
        ``val_label``, ``test_input``, and ``test_label``.
    """
    if validation_ratio < 0 or validation_ratio >= 1:
        raise ValueError(f"validation_ratio must be in [0, 1); got {validation_ratio}")

    dev = resolve_device(_resolve_device(device))
    train_input = torch.as_tensor(Xtr, dtype=torch.float32, device=dev)
    test_input = torch.as_tensor(Xte, dtype=torch.float32, device=dev)
    train_label_raw = _to_label_tensor(Ytr, device=dev, split="train")
    test_label_raw = _to_label_tensor(Yte, device=dev, split="test")
    train_label, test_label = _to_one_hot_if_needed(train_label_raw, test_label_raw)
    _validate_sample_count(train_input, train_label, split="train")
    _validate_sample_count(test_input, test_label, split="test")
    train_input, train_label, val_input, val_label = _split_train_validation(
        train_input,
        train_label,
        validation_ratio=validation_ratio,
        seed=seed,
        min_val_samples=min_val_samples,
    )
    return {
        "train_input": train_input,
        "train_label": train_label,
        "val_input": val_input,
        "val_label": val_label,
        "test_input": test_input,
        "test_label": test_label,
    }
