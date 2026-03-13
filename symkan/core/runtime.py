"""symkan 运行时设备管理。

该模块维护全局默认设备，并提供统一的设备解析与批大小建议。
"""

import torch

_DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


def get_device() -> str:
    """返回当前 symkan 运行时设备字符串。

    Returns:
        str: 当前设备字符串，例如 ``cpu`` 或 ``cuda:0``。
    """
    return str(resolve_device(_DEVICE))


def set_device(device: str):
    """设置 symkan 全局运行时设备。

    Args:
        device: 目标设备，支持 ``auto/cpu/cuda/cuda:0`` 等写法。
    """
    global _DEVICE
    _DEVICE = str(resolve_device(device))


def resolve_device(device=None) -> torch.device:
    """解析并校验设备对象。

    Args:
        device: 可选设备；为空或 ``auto`` 时使用当前全局设备。

    Returns:
        torch.device: 可用设备；当 CUDA 不可用时自动回退为 CPU。
    """
    if device is None or str(device).lower() == "auto":
        device = _DEVICE
    dev = torch.device(device)
    # 容错回退，避免在无 CUDA 环境抛出运行时错误。
    if dev.type == "cuda" and not torch.cuda.is_available():
        return torch.device("cpu")
    return dev


def is_cuda_device(device=None) -> bool:
    """判断目标设备是否为 CUDA。

    Args:
        device: 可选设备；为空时使用当前全局设备。

    Returns:
        bool: 若为 CUDA 设备返回 True，否则返回 False。
    """
    return resolve_device(device).type == "cuda"


def default_batch_size(device=None, cuda_batch: int = 256, cpu_batch: int = 64) -> int:
    """根据设备返回推荐默认 batch 大小。

    Args:
        device: 可选设备；为空时使用当前全局设备。
        cuda_batch: CUDA 默认 batch。
        cpu_batch: CPU 默认 batch。

    Returns:
        int: 推荐的 batch 大小。
    """
    return cuda_batch if is_cuda_device(device) else cpu_batch
