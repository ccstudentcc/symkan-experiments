"""symkan 数据集构建与验证集切分工具。"""

import warnings
from typing import Optional

import numpy as np
import torch
import torch.nn.functional as F

from .runtime import get_device, resolve_device


def _resolve_device(device: Optional[str] = None) -> str:
    """解析数据构建阶段使用的设备字符串。

    Args:
        device: 传入设备；为空或 ``auto`` 时返回当前全局设备。

    Returns:
        str: 设备字符串。
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
    """为训练集创建可选验证集切分。

    Args:
        train_input: 训练输入张量。
        train_label: 训练标签张量。
        validation_ratio: 验证集比例。
        seed: 随机种子。
        min_val_samples: 验证集最少样本数。

    Returns:
        tuple[torch.Tensor, torch.Tensor, torch.Tensor | None, torch.Tensor | None]:
        训练集与验证集张量。
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
    # 若按比例切分导致验证样本太少，则上调比例以保证最小统计稳定性。
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
    """构建 KAN/symkan 统一 dataset 字典。

    Args:
        Xtr: 训练输入数组。
        Ytr: 训练标签数组（通常为 one-hot）。
        Xte: 测试输入数组。
        Yte: 测试标签数组（通常为 one-hot）。
        device: 目标设备，支持 ``auto/cpu/cuda``。
        validation_ratio: 验证集比例；默认 ``0.0`` 表示禁用。
        seed: 验证集切分随机种子。
        min_val_samples: 验证集最少样本数。

    Returns:
        dict: 包含 ``train_input/train_label/val_input/val_label/test_input/test_label``
        的张量字典。
    """
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
