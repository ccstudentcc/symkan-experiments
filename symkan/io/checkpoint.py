"""symkan 模型克隆与检查点复制工具。"""

import copy
import io
from typing import Optional

import torch
import yaml as _yaml
from kan import KAN as _KAN
from kan.Symbolic_KANLayer import SYMBOLIC_LIB as _SYM_LIB

from symkan.core.runtime import get_device, resolve_device


def clone_model_in_memory(model, device: Optional[str] = None):
    """使用内存路径深拷贝模型。

    Args:
        model: 待克隆模型。
        device: 目标设备；为空时使用当前运行时设备。

    Returns:
        Any: 模型副本（迁移到目标设备）。
    """
    dev = resolve_device(device or get_device())
    try:
        model_load = copy.deepcopy(model)
    except Exception:
        # deepcopy 失败时回退到 torch 序列化路径，兼容不可 deepcopy 的对象。
        buf = io.BytesIO()
        torch.save(model, buf)
        buf.seek(0)
        model_load = torch.load(buf, map_location=dev)

    if hasattr(model, "training"):
        model_load.train(model.training)
    return model_load.to(dev)


def clone_model_via_ckpt(model, path: str = "_safe_copy_temp", device: Optional[str] = None):
    """通过 ckpt 文件路径深拷贝 KAN 模型。

    Args:
        model: 待克隆模型。
        path: 临时 ckpt 前缀路径。
        device: 目标设备；为空时使用当前运行时设备。

    Returns:
        Any: 模型副本（迁移到目标设备）。
    """
    dev = resolve_device(device or get_device())
    model.saveckpt(path)

    with open(f"{path}_config.yml", "r", encoding="utf-8") as f:
        config = _yaml.safe_load(f)

    state = torch.load(f"{path}_state", map_location=dev)

    model_load = _KAN(
        width=config["width"],
        grid=config["grid"],
        k=config["k"],
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
    model_load.cache_data = torch.load(f"{path}_cache_data", map_location=dev)

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

    if hasattr(model, "input_id"):
        model_load.input_id = model.input_id.clone()

    return model_load.to(dev)


def clone_model(
    model,
    device: Optional[str] = None,
    use_disk_clone: bool = False,
    ckpt_path: str = "_safe_copy_temp",
):
    """统一模型克隆入口。

    默认优先内存克隆；当失败或显式指定时回退到磁盘 ckpt 克隆。

    Args:
        model: 待克隆模型。
        device: 目标设备；为空时使用当前运行时设备。
        use_disk_clone: 是否强制使用磁盘克隆。
        ckpt_path: 磁盘克隆临时路径前缀。

    Returns:
        Any: 模型副本。
    """
    if use_disk_clone:
        return clone_model_via_ckpt(model, path=ckpt_path, device=device)
    try:
        return clone_model_in_memory(model, device=device)
    except Exception:
        return clone_model_via_ckpt(model, path=ckpt_path, device=device)
