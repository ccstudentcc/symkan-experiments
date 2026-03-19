"""symkan runtime device management helpers.

This module drives the global default device and provides unified device
resolution and batch-size guidance.
"""

import torch

_DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


def get_device() -> str:
    """Return the current symkan runtime device string.

    Returns:
        str: Device string such as ``cpu`` or ``cuda:0``.
    """
    return str(resolve_device(_DEVICE))


def set_device(device: str):
    """Set the global symkan runtime device.

    Args:
        device: Target device string, e.g. ``auto``, ``cpu``, ``cuda``, or ``cuda:0``.
    """
    global _DEVICE
    _DEVICE = str(resolve_device(device))


def resolve_device(device=None) -> torch.device:
    """Resolve and validate a device specification.

    Args:
        device: Optional device spec; uses the global default when ``None`` or ``auto``.

    Returns:
        torch.device: Validated device (falling back to CPU when CUDA is unavailable).
    """
    if device is None or str(device).lower() == "auto":
        device = _DEVICE
    dev = torch.device(device)
    # Fallback guard to avoid runtime errors when CUDA is not available.
    if dev.type == "cuda" and not torch.cuda.is_available():
        return torch.device("cpu")
    return dev


def is_cuda_device(device=None) -> bool:
    """Check whether a device spec refers to CUDA.

    Args:
        device: Optional device spec; uses the global default when ``None``.

    Returns:
        bool: ``True`` when the resolved device is CUDA.
    """
    return resolve_device(device).type == "cuda"


def default_batch_size(device=None, cuda_batch: int = 256, cpu_batch: int = 64) -> int:
    """Recommend a default batch size based on the device.

    Args:
        device: Optional device spec; uses the global default when ``None``.
        cuda_batch: Default batch size when using CUDA.
        cpu_batch: Default batch size when using CPU.

    Returns:
        int: Recommended batch size.
    """
    return cuda_batch if is_cuda_device(device) else cpu_batch
