import torch

_DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


def get_device() -> str:
    """@brief 获取当前 symkan 运行时设备。

    @return str 当前设备字符串（例如 `cpu` 或 `cuda:0`）。
    """
    return str(resolve_device(_DEVICE))


def set_device(device: str):
    """@brief 设置 symkan 全局运行时设备。

    @param device 目标设备，支持 `auto/cpu/cuda/cuda:0` 等写法。
    """
    global _DEVICE
    _DEVICE = str(resolve_device(device))


def resolve_device(device=None) -> torch.device:
    """@brief 解析并校验设备对象。

    @param device 可选设备；为空或 `auto` 时使用当前全局设备。
    @return torch.device 可用设备；当 CUDA 不可用时自动回退为 CPU。
    """
    if device is None or str(device).lower() == "auto":
        device = _DEVICE
    dev = torch.device(device)
    if dev.type == "cuda" and not torch.cuda.is_available():
        return torch.device("cpu")
    return dev


def is_cuda_device(device=None) -> bool:
    """@brief 判断目标设备是否为 CUDA。

    @param device 可选设备；为空时使用当前全局设备。
    @return bool 若为 CUDA 设备返回 True，否则返回 False。
    """
    return resolve_device(device).type == "cuda"


def default_batch_size(device=None, cuda_batch: int = 256, cpu_batch: int = 64) -> int:
    """@brief 根据设备返回推荐默认 batch 大小。

    @param device 可选设备；为空时使用当前全局设备。
    @param cuda_batch CUDA 默认 batch。
    @param cpu_batch CPU 默认 batch。
    @return int 推荐的 batch 大小。
    """
    return cuda_batch if is_cuda_device(device) else cpu_batch
