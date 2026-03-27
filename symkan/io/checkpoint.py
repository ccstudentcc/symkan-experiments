"""Model cloning and checkpoint utilities for symkan."""

import copy
import io
import uuid
from contextlib import contextmanager
from pathlib import Path
from typing import Optional

import torch
import yaml as _yaml
from kan import KAN as _KAN
from kan.Symbolic_KANLayer import SYMBOLIC_LIB as _SYM_LIB

from symkan.core.runtime import get_device, resolve_device


DEFAULT_CLONE_CKPT_PREFIX = "_safe_copy_temp"
_CKPT_SUFFIXES = ("_config.yml", "_state", "_cache_data")


def _load_tensor_artifact(path: str, device: torch.device):
    """Load a Torch checkpoint artifact with backward-compatible kwargs.

    Args:
        path: Artifact path on disk.
        device: Target device for deserialization.

    Returns:
        Any: Deserialized artifact content.
    """
    try:
        return torch.load(path, map_location=device, weights_only=True)
    except TypeError:
        return torch.load(path, map_location=device)


def _cleanup_ckpt_artifacts(prefix: Path) -> None:
    """Delete checkpoint sidecar files created during clone operations.

    Args:
        prefix: Shared checkpoint prefix without suffixes.
    """
    for suffix in _CKPT_SUFFIXES:
        artifact = Path(f"{prefix}{suffix}")
        try:
            artifact.unlink()
        except FileNotFoundError:
            continue


@contextmanager
def _checkpoint_prefix(path: str = DEFAULT_CLONE_CKPT_PREFIX):
    """Create a temporary checkpoint prefix and always clean it up.

    Args:
        path: Optional explicit checkpoint prefix. The default generates a
            unique temporary prefix in the current working directory.

    Yields:
        Path: Prefix path to use with pykan checkpoint helpers.
    """
    if path != DEFAULT_CLONE_CKPT_PREFIX:
        prefix = Path(path)
        prefix.parent.mkdir(parents=True, exist_ok=True)
        try:
            yield prefix
        finally:
            _cleanup_ckpt_artifacts(prefix)
        return

    prefix = Path.cwd() / f"symkan-clone-{uuid.uuid4().hex}"
    try:
        yield prefix
    finally:
        _cleanup_ckpt_artifacts(prefix)


def clone_model_in_memory(model, device: Optional[str] = None):
    """Deep copy a model in memory and move it to the requested device.

    Args:
        model: Model to clone.
        device: Target device; defaults to the current runtime device.

    Returns:
        Any: Cloned model instance.
    """
    dev = resolve_device(device or get_device())
    try:
        model_load = copy.deepcopy(model)
    except Exception:
        # Fallback to torch serialization when deepcopy is not supported.
        buf = io.BytesIO()
        torch.save(model, buf)
        buf.seek(0)
        model_load = torch.load(buf, map_location=dev)

    if hasattr(model, "training"):
        model_load.train(model.training)
    return model_load.to(dev)


def clone_model_via_ckpt(model, path: str = DEFAULT_CLONE_CKPT_PREFIX, device: Optional[str] = None):
    """Clone a KAN model by writing and reading a checkpoint on disk.

    Args:
        model: Model to clone.
        path: Temporary checkpoint prefix path.
        device: Target device; defaults to the current runtime device.

    Returns:
        Any: Cloned model moved to the target device.
    """
    dev = resolve_device(device or get_device())
    with _checkpoint_prefix(path) as ckpt_prefix:
        prefix = str(ckpt_prefix)
        model.saveckpt(prefix)

        with open(f"{prefix}_config.yml", "r", encoding="utf-8") as f:
            config = _yaml.safe_load(f)

        state = _load_tensor_artifact(f"{prefix}_state", dev)

        model_load = _KAN(
            width=config["width"],
            grid=config["grid"],
            k=config["k"],
            numeric_basis=config.get("numeric_basis", getattr(model, "numeric_basis", "bspline")),
            mult_arity=config["mult_arity"],
            base_fun=config["base_fun_name"],
            symbolic_enabled=config["symbolic_enabled"],
            affine_trainable=config["affine_trainable"],
            grid_eps=config["grid_eps"],
            grid_range=config["grid_range"],
            sp_trainable=config["sp_trainable"],
            sb_trainable=config["sb_trainable"],
            state_id=config["state_id"],
            auto_save=config["auto_save"],
            first_init=False,
            ckpt_path=config["ckpt_path"],
            round=config["round"] + 1,
            device=str(dev),
        )

        model_load.load_state_dict(state)
        model_load.cache_data = _load_tensor_artifact(f"{prefix}_cache_data", dev)

        depth = len(model_load.width) - 1
        for l in range(depth):
            out_dim = model_load.symbolic_fun[l].out_dim
            in_dim = model_load.symbolic_fun[l].in_dim
            funs_name = config[f"symbolic.funs_name.{l}"]
            for j in range(out_dim):
                for i in range(in_dim):
                    fn = funs_name[j][i]
                    model_load.symbolic_fun[l].funs_name[j][i] = fn
                    if fn in _SYM_LIB:
                        model_load.symbolic_fun[l].funs[j][i] = _SYM_LIB[fn][0]
                        model_load.symbolic_fun[l].funs_sympy[j][i] = _SYM_LIB[fn][1]
                        model_load.symbolic_fun[l].funs_avoid_singularity[j][i] = _SYM_LIB[fn][3]

        if hasattr(model, "input_id") and model.input_id is not None:
            model_load.input_id = model.input_id.clone()

        return model_load.to(dev)


def clone_model(
    model,
    device: Optional[str] = None,
    use_disk_clone: bool = False,
    ckpt_path: str = DEFAULT_CLONE_CKPT_PREFIX,
):
    """Unified cloning entry point that prefers memory cloning.

    Memory cloning is attempted first; disk checkpoints are used when the
    user forces disk clones or when memory cloning fails.

    Args:
        model: Model to clone.
        device: Target device; defaults to the current runtime device.
        use_disk_clone: Force disk-based cloning when True.
        ckpt_path: Prefix for temporary disk checkpoints.

    Returns:
        Any: Cloned model instance.
    """
    if use_disk_clone:
        return clone_model_via_ckpt(model, path=ckpt_path, device=device)
    try:
        return clone_model_in_memory(model, device=device)
    except Exception:
        return clone_model_via_ckpt(model, path=ckpt_path, device=device)
