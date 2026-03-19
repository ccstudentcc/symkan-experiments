"""Input compaction utilities for symkan symbolic workflows.

Migrated from pipeline.py, these helpers identify active inputs via
masks and build compact input subsets.
"""

import torch


def select_dataset_inputs(dataset, input_idx):
    """Select a subset of dataset inputs by index.

    Args:
        dataset: Original dataset dictionary.
        input_idx: Active input indices.

    Returns:
        dict: Dataset dictionary limited to the selected input subset.
    """
    idx = torch.as_tensor(input_idx, dtype=torch.long, device=dataset["train_input"].device)
    selected = {
        "train_input": dataset["train_input"].index_select(1, idx),
        "train_label": dataset["train_label"],
        "test_input": dataset["test_input"].index_select(1, idx.to(dataset["test_input"].device)),
        "test_label": dataset["test_label"],
    }
    if "val_input" in dataset and dataset["val_input"] is not None:
        val_idx = idx.to(dataset["val_input"].device)
        selected["val_input"] = dataset["val_input"].index_select(1, val_idx)
        selected["val_label"] = dataset.get("val_label")
    return selected


def first_layer_active_inputs(work):
    """Identify active input indices for the first layer.

    Args:
        work: KAN model whose first layer masks will be inspected.

    Returns:
        list[int]: Indices of inputs that are active according to activation or
        symbolic masks.
    """
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
    """Attempt to compact the model's input dimensions for symbolic search.

    Args:
        work: Model to compact.
        dataset: Original dataset dictionary.

    Returns:
        dict | None: Returns a dictionary with ``model``, ``dataset``,
        ``active_inputs``, and ``original_input_id`` if compaction occurred; otherwise
        ``None`` when no compaction is needed.
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

    # The compacted model only sees a subset of inputs, so rebuild a consecutive
    # input_id mapping while allowing the outer scope to restore the original mapping.
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
