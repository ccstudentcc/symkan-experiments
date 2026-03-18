"""symkan 推理与评估原语。

从原 modeling.py 迁移。提供 logits 计算、准确率评估与模型边数统计。
"""

from typing import Optional

import numpy as np
import torch
from sklearn.metrics import accuracy_score

from .runtime import get_device, resolve_device


def _infer_model_device(model):
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
    if device is not None and str(device).lower() != "auto":
        return resolve_device(device)
    return _infer_model_device(model)


def _label_tensor_to_indices(labels, *, device: torch.device, split: str) -> torch.Tensor:
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
    """计算模型 logits（NumPy 输入路径）。

    Args:
        model: KAN/symkan 模型对象。
        X: 输入特征数组。
        device: 可选设备；为空时自动推断模型设备。

    Returns:
        numpy.ndarray: logits 数组。
    """
    model.eval()
    dev = _pick_device(model, device)
    with torch.no_grad():
        x = torch.as_tensor(X, dtype=torch.float32, device=dev)
        return model(x).detach().cpu().numpy()


def model_logits_ds(model, dataset, split: str = "test", device: Optional[str] = None):
    """计算模型 logits（Tensor 快路径）。

    Args:
        model: KAN/symkan 模型对象。
        dataset: 由 ``build_dataset`` 构建的数据字典。
        split: 数据划分，支持 ``train``、``val`` 或 ``test``。
        device: 可选设备；为空时自动推断模型设备。

    Returns:
        torch.Tensor: logits 张量。

    Raises:
        ValueError: 当请求的 split 不存在或为空时抛出。
    """
    model.eval()
    dev = _pick_device(model, device)
    input_key = f"{split}_input"
    if input_key not in dataset or dataset[input_key] is None:
        raise ValueError(f"数据集缺少可用 split: {split}")
    x = dataset[input_key]
    if not torch.is_tensor(x):
        x = torch.as_tensor(x, dtype=torch.float32, device=dev)
    else:
        x = x.to(dev)
    with torch.inference_mode():
        logits = model(x)
    return logits


def model_acc(model, X, y_cls, device: Optional[str] = None):
    """基于 NumPy 路径计算分类准确率。

    Args:
        model: KAN/symkan 模型对象。
        X: 输入特征数组。
        y_cls: 类别索引标签。
        device: 可选设备；为空时自动推断模型设备。

    Returns:
        float: 分类准确率。
    """
    pred = np.argmax(model_logits(model, X, device=device), axis=1)
    return accuracy_score(y_cls, pred)


def model_acc_ds_fast(model, dataset, split: str = "test", device: Optional[str] = None):
    """基于 Tensor 快路径计算分类准确率。

    Args:
        model: KAN/symkan 模型对象。
        dataset: 由 ``build_dataset`` 构建的数据字典。
        split: 数据划分，支持 ``train``、``val`` 或 ``test``。
        device: 可选设备；为空时自动推断模型设备。

    Returns:
        float: 分类准确率。

    Raises:
        ValueError: 当请求的 split 不存在或为空时抛出。
    """
    logits = model_logits_ds(model, dataset, split=split, device=device)
    label_key = f"{split}_label"
    if label_key not in dataset or dataset[label_key] is None:
        raise ValueError(f"数据集缺少可用 split: {split}")
    pred = torch.argmax(logits, dim=1)
    y = _label_tensor_to_indices(dataset[label_key], device=pred.device, split=split)
    return (pred == y).float().mean().item()


def model_acc_ds(model, dataset, split: str = "test", device: Optional[str] = None):
    """统一准确率接口（优先快路径，失败时自动回退）。

    Args:
        model: KAN/symkan 模型对象。
        dataset: 由 ``build_dataset`` 构建的数据字典。
        split: 数据划分，支持 ``train``、``val`` 或 ``test``。
        device: 可选设备；为空时自动推断模型设备。

    Returns:
        float: 分类准确率。

    Raises:
        ValueError: 当 ``split='val'`` 且验证集不可用时抛出。
    """
    try:
        return model_acc_ds_fast(model, dataset, split=split, device=device)
    except (KeyError, ValueError) as exc:
        if split == "val":
            raise ValueError(
                "验证集 split 不可用；请在 build_dataset 中设置 validation_ratio>0，"
                "或在 stagewise_train 中关闭 use_validation。"
            ) from exc
        raise
    except Exception:
        # 极端情况下回退到 NumPy 路径，优先保证可用性而非最优性能。
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
    """获取模型当前边数。

    Args:
        model: KAN/symkan 模型对象。

    Returns:
        int | float: 当可读时返回整数边数，否则返回 ``numpy.nan``。
    """
    try:
        return int(model.n_edge)
    except Exception:
        return np.nan
