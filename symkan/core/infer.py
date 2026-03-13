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


def model_logits(model, X, device: Optional[str] = None):
    """@brief 计算模型 logits（NumPy 输入路径）。

    @param model KAN/symkan 模型对象。
    @param X 输入特征数组。
    @param device 可选设备；为空时自动推断模型设备。
    @return numpy.ndarray logits 数组。
    """
    model.eval()
    dev = _pick_device(model, device)
    with torch.no_grad():
        x = torch.as_tensor(X, dtype=torch.float32, device=dev)
        return model(x).detach().cpu().numpy()


def model_logits_ds(model, dataset, split: str = "test", device: Optional[str] = None):
    """@brief 计算模型 logits（Tensor 快路径）。

    @param model KAN/symkan 模型对象。
    @param dataset 由 `build_dataset` 构建的数据字典。
    @param split 数据划分，支持 `train` 或 `test`。
    @param device 可选设备；为空时自动推断模型设备。
    @return torch.Tensor logits 张量。
    """
    model.eval()
    dev = _pick_device(model, device)
    x = dataset[f"{split}_input"]
    if not torch.is_tensor(x):
        x = torch.as_tensor(x, dtype=torch.float32, device=dev)
    else:
        x = x.to(dev)
    with torch.inference_mode():
        logits = model(x)
    return logits


def model_acc(model, X, y_cls, device: Optional[str] = None):
    """@brief 基于 NumPy 路径计算分类准确率。

    @param model KAN/symkan 模型对象。
    @param X 输入特征数组。
    @param y_cls 类别索引标签。
    @param device 可选设备；为空时自动推断模型设备。
    @return float 分类准确率。
    """
    pred = np.argmax(model_logits(model, X, device=device), axis=1)
    return accuracy_score(y_cls, pred)


def model_acc_ds_fast(model, dataset, split: str = "test", device: Optional[str] = None):
    """@brief 基于 Tensor 快路径计算分类准确率。

    @param model KAN/symkan 模型对象。
    @param dataset 由 `build_dataset` 构建的数据字典。
    @param split 数据划分，支持 `train` 或 `test`。
    @param device 可选设备；为空时自动推断模型设备。
    @return float 分类准确率。
    """
    logits = model_logits_ds(model, dataset, split=split, device=device)
    pred = torch.argmax(logits, dim=1)
    y = torch.argmax(dataset[f"{split}_label"], dim=1).to(pred.device)
    return (pred == y).float().mean().item()


def model_acc_ds(model, dataset, split: str = "test", device: Optional[str] = None):
    """@brief 统一准确率接口（优先快路径，失败时自动回退）。

    @param model KAN/symkan 模型对象。
    @param dataset 由 `build_dataset` 构建的数据字典。
    @param split 数据划分，支持 `train` 或 `test`。
    @param device 可选设备；为空时自动推断模型设备。
    @return float 分类准确率。
    """
    try:
        return model_acc_ds_fast(model, dataset, split=split, device=device)
    except Exception:
        x = dataset[f"{split}_input"].detach().cpu().numpy()
        y = np.argmax(dataset[f"{split}_label"].detach().cpu().numpy(), axis=1)
        return model_acc(model, x, y, device=device)


def get_n_edge(model):
    """@brief 获取模型当前边数。

    @param model KAN/symkan 模型对象。
    @return int|float 当可读时返回整数边数，否则返回 `numpy.nan`。
    """
    try:
        return int(model.n_edge)
    except Exception:
        return np.nan
