from typing import Optional

import torch

from .runtime import get_device, resolve_device


def _resolve_device(device: Optional[str] = None) -> str:
    """@brief 解析数据构建阶段使用的设备字符串。

    @param device 传入设备；为空或 `auto` 时返回当前全局设备。
    @return str 设备字符串。
    """
    if device is None or device == "auto":
        return get_device()
    return device


def build_dataset(Xtr, Ytr, Xte, Yte, device: Optional[str] = None):
    """@brief 构建 KAN/symkan 统一 dataset 字典。

    @param Xtr 训练输入数组。
    @param Ytr 训练标签数组（通常为 one-hot）。
    @param Xte 测试输入数组。
    @param Yte 测试标签数组（通常为 one-hot）。
    @param device 目标设备，支持 `auto/cpu/cuda`。
    @return dict 包含 `train_input/train_label/test_input/test_label` 的张量字典。
    """
    dev = resolve_device(_resolve_device(device))
    return {
        "train_input": torch.as_tensor(Xtr, dtype=torch.float32, device=dev),
        "train_label": torch.as_tensor(Ytr, dtype=torch.float32, device=dev),
        "test_input": torch.as_tensor(Xte, dtype=torch.float32, device=dev),
        "test_label": torch.as_tensor(Yte, dtype=torch.float32, device=dev),
    }
