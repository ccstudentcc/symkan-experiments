"""symkan 符号候选搜索与逐层拟合原语。

从 pipeline.py 迁移。所有搜索操作都在单一模型上顺序执行，
避免共享模型并行 suggest 导致的状态竞争。
"""

from collections import Counter

import torch

from symkan.core.train import safe_fit
from symkan.core.runtime import default_batch_size


def _resolve_parallel_workers(parallel_mode="auto", parallel_workers=None):
    """解析并行配置。

    当前版本出于正确性考虑，始终返回 1（串行），
    待隔离 worker 模式就绪后可放开。
    """
    # NOTE: 旧版允许 thread 模式在共享模型上并行 suggest_symbolic，
    # 这会导致 pykan 内部状态竞争。在引入 per-worker clone 之前，
    # 强制串行。
    return 1


def layerwise_symbolic(work, dataset, layer_idx, lib, weight_simple=0.0, verbose=True):
    """逐层符号候选搜索与 fix。

    Args:
        work: KAN 模型，会被就地修改。
        dataset: 数据集字典。
        layer_idx: 目标层索引。
        lib: 符号函数库。
        weight_simple: 简洁性偏好权重。
        verbose: 是否打印日志。

    Returns:
        dict: 搜索结果统计。
    """
    work.eval()
    with torch.no_grad():
        n_samples = min(len(dataset["train_input"]), 1024)
        work(dataset["train_input"][:n_samples])

    fixed_count = 0
    low_r2_count = 0
    active_count = 0
    r2_records = []

    l = layer_idx
    n_in = work.width_in[l]
    n_out = work.width_out[l + 1]

    for i in range(n_in):
        for j in range(n_out):
            sym_mask = work.symbolic_fun[l].mask[j, i].item()
            act_mask = work.act_fun[l].mask[i][j].item()

            if sym_mask > 0 and act_mask == 0:
                continue
            if act_mask == 0:
                continue

            active_count += 1
            try:
                # suggest_symbolic 会暂时修改模型内部状态，因此这里必须严格串行执行。
                name, _, r2, _ = work.suggest_symbolic(
                    l, i, j, lib=lib, verbose=False, weight_simple=weight_simple
                )
                r2_records.append({"layer": l, "i": i, "j": j, "name": name, "r2": float(r2)})
                work.fix_symbolic(l, i, j, name, verbose=False, log_history=False)
                fixed_count += 1
                if r2 < 0.5:
                    low_r2_count += 1
                    if verbose:
                        print(f"    ⚠ 低R² fix ({l},{i},{j}) → {name}  R²={r2:.4f}")
            except Exception as e:
                if verbose:
                    print(f"    ({l},{i},{j}) suggest 失败: {e}")

    if verbose:
        print(f"  Layer {l}: 活跃={active_count}, fix={fixed_count}")

    return {
        "active": active_count,
        "fixed": fixed_count,
        "low_r2": low_r2_count,
        "r2_records": r2_records,
    }


def fast_symbolic(
    work,
    dataset,
    lib=None,
    weight_simple=0.0,
    lib_hidden=None,
    lib_output=None,
    layerwise_finetune_steps=200,
    batch_size=None,
    parallel_mode="auto",
    parallel_workers=None,
    parallel_min_tasks=16,
    verbose=True,
):
    """逐层符号化主入口。

    遍历所有层，依次执行候选搜索与 fix，层间可选微调。

    Args:
        work: 待符号化模型。
        dataset: 数据集字典。
        lib: 统一函数库。
        weight_simple: 简洁性偏好权重。
        lib_hidden: 隐藏层函数库。
        lib_output: 输出层函数库。
        layerwise_finetune_steps: 每层符号化后的微调步数。
        batch_size: 批大小。
        parallel_mode: 并行模式配置。
        parallel_workers: 期望 worker 数。
        parallel_min_tasks: 启用并行的最小任务阈值。
        verbose: 是否打印日志。

    Returns:
        dict: 包含逐层 fix 统计、R2 记录和耗时信息的结果。
    """
    from .library import LIB_HIDDEN, LIB_OUTPUT, get_layer_lib, register_custom_functions
    import time

    register_custom_functions()

    if batch_size is None:
        batch_size = default_batch_size()

    depth = len(work.width_in) - 1
    all_records = []
    total_fixed = 0
    total_active = 0
    total_low_r2 = 0
    layer_times = []
    suggest_workers = _resolve_parallel_workers(
        parallel_mode=parallel_mode, parallel_workers=parallel_workers
    )

    for l in range(depth):
        layer_lib = get_layer_lib(l, depth, lib_hidden, lib_output, lib)
        t0 = time.perf_counter()

        result = layerwise_symbolic(
            work, dataset, l, layer_lib,
            weight_simple=weight_simple, verbose=verbose,
        )

        layer_times.append(
            {
                "layer": int(l),
                "active": int(result["active"]),
                "fixed": int(result["fixed"]),
                "seconds": float(time.perf_counter() - t0),
                "workers": int(suggest_workers),
            }
        )
        all_records.extend(result["r2_records"])
        total_fixed += result["fixed"]
        total_active += result["active"]
        total_low_r2 += result["low_r2"]

        if result["fixed"] > 0 and l < depth - 1 and layerwise_finetune_steps > 0:
            safe_fit(
                work,
                dataset,
                opt="Adam",
                steps=layerwise_finetune_steps,
                lr=0.005,
                lamb=0.0,
                batch=batch_size,
                update_grid=False,
                singularity_avoiding=True,
                log=max(1, layerwise_finetune_steps // 5),
            )

    if verbose and all_records:
        name_counts = Counter(r["name"] for r in all_records)
        print(f"  函数分布: {dict(name_counts)}")

    return {
        "active": total_active,
        "fixed": total_fixed,
        "low_r2": total_low_r2,
        "r2_records": all_records,
        "layer_times": layer_times,
        "parallel_workers": int(suggest_workers),
    }
