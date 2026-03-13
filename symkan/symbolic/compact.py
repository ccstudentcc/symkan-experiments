"""symkan 输入压缩工具。

从 pipeline.py 迁移。负责根据掩码识别活跃输入并构建紧凑数据子集。
"""

import torch


def select_dataset_inputs(dataset, input_idx):
    """按输入索引子集裁切数据集。"""
    idx = torch.as_tensor(input_idx, dtype=torch.long, device=dataset["train_input"].device)
    return {
        "train_input": dataset["train_input"].index_select(1, idx),
        "train_label": dataset["train_label"],
        "test_input": dataset["test_input"].index_select(1, idx.to(dataset["test_input"].device)),
        "test_label": dataset["test_label"],
    }


def first_layer_active_inputs(work):
    """识别第一层活跃输入索引。"""
    n_in = int(work.width_in[0])
    active = torch.zeros(n_in, dtype=torch.bool)

    try:
        act_mask = torch.as_tensor(work.act_fun[0].mask)
        if act_mask.ndim == 2:
            if act_mask.shape[0] == n_in:
                active |= torch.any(act_mask != 0, dim=1).cpu()
            elif act_mask.shape[1] == n_in:
                active |= torch.any(act_mask != 0, dim=0).cpu()
    except Exception:
        pass

    try:
        sym_mask = torch.as_tensor(work.symbolic_fun[0].mask)
        if sym_mask.ndim == 2:
            if sym_mask.shape[0] == n_in:
                active |= torch.any(sym_mask != 0, dim=1).cpu()
            elif sym_mask.shape[1] == n_in:
                active |= torch.any(sym_mask != 0, dim=0).cpu()
    except Exception:
        pass

    if not torch.any(active):
        return list(range(n_in))
    return torch.where(active)[0].tolist()


def compact_inputs_for_symbolic(work, dataset):
    """尝试压缩模型输入维度。

    Args:
        work: 待压缩的模型。
        dataset: 原始数据集字典。

    Returns:
        dict | None: 成功时返回包含 ``model``、``dataset``、``active_inputs``
        和 ``original_input_id`` 的字典；若无需压缩则返回 ``None``。
    """
    if not hasattr(work, "prune_input"):
        return None

    active_inputs = first_layer_active_inputs(work)
    n_in = int(work.width_in[0])
    if len(active_inputs) == 0 or len(active_inputs) >= n_in:
        return None

    compact_model = work.prune_input(active_inputs=active_inputs, log_history=False)
    if not hasattr(compact_model, "input_id"):
        return None

    if hasattr(compact_model, "auto_save"):
        compact_model.auto_save = False

    # 压缩后模型只看见子集输入，因此需要重建连续 input_id；原始映射会在外层恢复。
    original_input_id = compact_model.input_id.detach().clone()
    compact_model.input_id = torch.arange(
        len(active_inputs), dtype=torch.long, device=original_input_id.device
    )
    compact_dataset = select_dataset_inputs(dataset, active_inputs)

    return {
        "model": compact_model,
        "dataset": compact_dataset,
        "active_inputs": active_inputs,
        "original_input_id": original_input_id,
    }
