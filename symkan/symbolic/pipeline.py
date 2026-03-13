import time

import numpy as np
import pandas as pd
import torch

from symkan.core import get_n_edge, model_acc_ds, safe_fit
from symkan.core.runtime import default_batch_size
from symkan.io import clone_model
from symkan.pruning import safe_attribute
from .compact import compact_inputs_for_symbolic
from .library import LIB_HIDDEN, LIB_OUTPUT, collect_valid_formulas, register_custom_functions
from .search import fast_symbolic


def _count_effective_edges(work):
    depth = len(work.width_in) - 1
    total = 0

    for l in range(depth):
        act_mask = None
        sym_mask = None

        try:
            act_mask = torch.as_tensor(work.act_fun[l].mask) != 0
        except Exception:
            act_mask = None

        try:
            sym_mask = torch.as_tensor(work.symbolic_fun[l].mask) != 0
        except Exception:
            sym_mask = None

        if act_mask is None and sym_mask is None:
            continue

        if act_mask is None:
            assert sym_mask is not None
            total += int(sym_mask.sum().item())
            continue

        if sym_mask is None:
            assert act_mask is not None
            total += int(act_mask.sum().item())
            continue

        if sym_mask.shape != act_mask.shape and sym_mask.T.shape == act_mask.shape:
            sym_mask = sym_mask.T

        if sym_mask.shape == act_mask.shape:
            total += int((act_mask | sym_mask).sum().item())
        else:
            total += int(act_mask.sum().item())

    return total


def _adaptive_attr_sample_count(n_edge_now, target_edges, min_sample=512, max_sample=2048):
    try:
        n_now = float(n_edge_now)
        tgt = float(max(1, target_edges))
    except Exception:
        return int(max_sample)

    ratio = n_now / tgt
    if ratio >= 2.5:
        return int(min_sample)
    if ratio >= 1.8:
        return int((min_sample + max_sample) // 2)
    return int(max_sample)


def _heavy_finetune(
    work,
    dataset,
    total_steps=240,
    batch_size=None,
    verbose=True,
    lr_schedule=None,
    early_stop_patience=0,
    early_stop_min_delta=1e-4,
):
    if batch_size is None:
        batch_size = default_batch_size()

    if lr_schedule is None:
        lr_schedule = [0.003, 0.001, 0.0005, 0.0002]
    lr_schedule = list(lr_schedule)
    if len(lr_schedule) == 0:
        return model_acc_ds(work, dataset)

    n_phases = len(lr_schedule)
    steps_per_phase = total_steps // n_phases

    best_acc = model_acc_ds(work, dataset)
    best_state = {k: v.detach().cpu().clone() for k, v in work.state_dict().items()}
    no_improve_count = 0

    for phase_idx, lr in enumerate(lr_schedule):
        phase_steps = steps_per_phase if phase_idx < n_phases - 1 else (total_steps - steps_per_phase * (n_phases - 1))
        if phase_steps <= 0:
            continue

        safe_fit(
            work,
            dataset,
            opt="Adam",
            steps=phase_steps,
            lr=lr,
            lamb=0.0,
            batch=batch_size,
            update_grid=False,
            singularity_avoiding=True,
            log=max(1, phase_steps // 5),
        )

        acc_now = model_acc_ds(work, dataset)
        improved = acc_now > (best_acc + float(early_stop_min_delta))
        if acc_now > best_acc:
            best_acc = acc_now
            best_state = {k: v.detach().cpu().clone() for k, v in work.state_dict().items()}

        if early_stop_patience > 0:
            if improved:
                no_improve_count = 0
            else:
                no_improve_count += 1

            if no_improve_count >= int(early_stop_patience):
                if verbose:
                    print(f"[heavy_finetune] early stop at phase={phase_idx}, best_acc={best_acc:.4f}")
                break

    work.load_state_dict(best_state)
    return model_acc_ds(work, dataset)


def symbolize_pipeline(
    model,
    dataset,
    target_edges=60,
    max_prune_rounds=40,
    lib=None,
    lib_hidden=None,
    lib_output=None,
    weight_simple=0.0,
    finetune_steps=30,
    finetune_lr=0.005,
    affine_finetune_steps=600,
    affine_finetune_lr_schedule=None,
    layerwise_finetune_steps=200,
    batch_size=None,
    parallel_mode="auto",
    parallel_workers=None,
    parallel_min_tasks=16,
    prune_eval_interval=1,
    prune_attr_sample_adaptive=False,
    prune_attr_sample_min=512,
    prune_attr_sample_max=2048,
    heavy_ft_early_stop_patience=0,
    heavy_ft_early_stop_min_delta=1e-4,
    collect_timing=True,
    verbose=True,
):
    """@brief 执行 symkan 主符号化流水线。

    流程包含：
    1) 渐进剪枝与短微调；
    2) 可选输入压缩；
    3) 严格逐层符号拟合（支持 suggest 并行）；
    4) 末端强化微调；
    5) 公式与统计结果导出。

    @param model 待符号化的 KAN/symkan 模型。
    @param dataset 由 `build_dataset` 构建的数据字典。
    @param target_edges 目标边数。
    @param max_prune_rounds 最大剪枝轮数。
    @param lib 统一函数库（可选）。
    @param lib_hidden 隐藏层函数库。
    @param lib_output 输出层函数库。
    @param weight_simple 函数复杂度偏好权重。
    @param finetune_steps 剪枝轮短微调步数。
    @param finetune_lr 剪枝轮短微调学习率。
    @param affine_finetune_steps 末端强化微调总步数。
    @param affine_finetune_lr_schedule 强化微调学习率序列。
    @param layerwise_finetune_steps 每层符号化后微调步数。
    @param batch_size 批大小；为空时自动使用默认值。
    @param parallel_mode 并行模式：`auto/off/thread`。
    @param parallel_workers 并行 worker 数，`None` 表示自动推断。
    @param parallel_min_tasks 并行最小任务阈值。
    @param prune_eval_interval 剪枝评估间隔。
    @param prune_attr_sample_adaptive 是否启用归因采样分级。
    @param prune_attr_sample_min 归因最小采样数。
    @param prune_attr_sample_max 归因最大采样数。
    @param heavy_ft_early_stop_patience 强化微调早停耐心轮数。
    @param heavy_ft_early_stop_min_delta 早停最小改进阈值。
    @param collect_timing 是否收集并返回详细耗时统计。
    @param verbose 是否打印详细日志。
    @return dict 包含模型、表达式、边数、精度、轨迹、统计与耗时信息。
    """
    register_custom_functions()

    if batch_size is None:
        batch_size = default_batch_size()

    work = clone_model(model)
    baseline_acc = model_acc_ds(work, dataset)
    n_edge_input = get_n_edge(work)

    effective_target = target_edges
    timing_prune_rounds = []
    timing_symbolic_layers = []
    timing_fit = []
    timing: dict[str, object] = {
        "prune_rounds": timing_prune_rounds,
        "symbolic_layers": timing_symbolic_layers,
        "fit": timing_fit,
    }
    if np.isfinite(n_edge_input) and n_edge_input > target_edges * 1.5:
        effective_target = max(target_edges, int(n_edge_input * 0.5))

    thresholds = np.linspace(0.02, 0.03, max_prune_rounds)
    trace = []
    prune_eval_interval = max(1, int(prune_eval_interval))
    last_acc = float(baseline_acc)

    for rd, th in enumerate(thresholds):
        t_round = time.perf_counter()
        n_before = get_n_edge(work)
        if np.isfinite(n_before) and n_before <= effective_target:
            break

        snap_prune_state = {k: v.detach().cpu().clone() for k, v in work.state_dict().items()}
        try:
            attr_n_sample = 2048
            if prune_attr_sample_adaptive:
                attr_n_sample = _adaptive_attr_sample_count(
                    n_before,
                    effective_target,
                    min_sample=int(prune_attr_sample_min),
                    max_sample=int(prune_attr_sample_max),
                )
            safe_attribute(work, dataset, n_sample=int(attr_n_sample))
            work.prune_edge(threshold=th)
        except Exception:
            work.load_state_dict(snap_prune_state)
            break

        n_after = get_n_edge(work)
        if n_after == 0:
            work.load_state_dict(snap_prune_state)
            break

        if n_after != n_before:
            t_fit = time.perf_counter()
            safe_fit(
                work,
                dataset,
                opt="Adam",
                steps=finetune_steps,
                lr=finetune_lr,
                lamb=0.0,
                batch=batch_size,
                update_grid=False,
                singularity_avoiding=True,
                log=max(1, finetune_steps // 5),
            )
            if collect_timing:
                timing_fit.append({"stage": "prune_round", "round": int(rd), "seconds": float(time.perf_counter() - t_fit)})

        should_eval = (rd % prune_eval_interval == 0)
        if np.isfinite(n_after) and np.isfinite(effective_target) and n_after <= effective_target * 1.3:
            should_eval = True
        if rd == len(thresholds) - 1:
            should_eval = True

        if should_eval:
            acc_now = model_acc_ds(work, dataset)
            last_acc = float(acc_now)
        else:
            acc_now = float(last_acc)

        trace.append({"round": rd, "threshold": float(th), "edges_before": n_before, "edges_after": n_after, "acc": float(acc_now)})
        if collect_timing:
            timing_prune_rounds.append(
                {
                    "round": int(rd),
                    "threshold": float(th),
                    "edges_before": float(n_before),
                    "edges_after": float(n_after),
                    "attr_n_sample": int(attr_n_sample) if prune_attr_sample_adaptive else 2048,
                    "eval_skipped": bool(not should_eval),
                    "seconds": float(time.perf_counter() - t_round),
                }
            )

        if acc_now < baseline_acc * 0.6:
            work.load_state_dict(snap_prune_state)
            break

    n_edge_now = get_n_edge(work)
    compact_state = None
    finetune_dataset = dataset
    effective_inputs = list(range(int(work.width_in[0])))

    if np.isfinite(n_edge_now) and n_edge_now > 0:
        try:
            compact_state = compact_inputs_for_symbolic(work, dataset)
            if compact_state is not None:
                work = compact_state["model"]
                finetune_dataset = compact_state["dataset"]
                effective_inputs = compact_state["active_inputs"]
                if verbose:
                    print(f"[symbolize_pipeline] 输入压缩: {int(dataset['train_input'].shape[1])} -> {len(effective_inputs)}")
        except Exception:
            compact_state = None
            finetune_dataset = dataset

        t_pre = time.perf_counter()
        safe_fit(
            work,
            finetune_dataset,
            opt="Adam",
            steps=100,
            lr=0.005,
            lamb=0.0,
            batch=batch_size,
            update_grid=False,
            singularity_avoiding=True,
            log=10,
        )
        if collect_timing:
            timing_fit.append({"stage": "pre_symbolic", "seconds": float(time.perf_counter() - t_pre)})

        t_sym = time.perf_counter()
        sym_result = fast_symbolic(
            work,
            finetune_dataset,
            lib=lib,
            weight_simple=weight_simple,
            lib_hidden=lib_hidden or LIB_HIDDEN,
            lib_output=lib_output or LIB_OUTPUT,
            layerwise_finetune_steps=layerwise_finetune_steps,
            batch_size=batch_size,
            parallel_mode=parallel_mode,
            parallel_workers=parallel_workers,
            parallel_min_tasks=parallel_min_tasks,
            verbose=verbose,
        )
        sym_stats = {
            "total": sym_result["active"],
            "fixed": sym_result["fixed"],
            "low_r2": sym_result["low_r2"],
            "r2_records": sym_result["r2_records"],
            "layer_times": sym_result.get("layer_times", []),
            "parallel_workers": sym_result.get("parallel_workers", 1),
        }
        if collect_timing:
            timing_symbolic_layers.clear()
            timing_symbolic_layers.extend(sym_result.get("layer_times", []))
            timing["symbolic_total_seconds"] = float(time.perf_counter() - t_sym)

        t_heavy = time.perf_counter()
        _heavy_finetune(
            work,
            finetune_dataset,
            total_steps=affine_finetune_steps,
            batch_size=batch_size,
            verbose=verbose,
            lr_schedule=affine_finetune_lr_schedule,
            early_stop_patience=heavy_ft_early_stop_patience,
            early_stop_min_delta=heavy_ft_early_stop_min_delta,
        )
        if collect_timing:
            timing_fit.append({"stage": "post_symbolic_affine", "seconds": float(time.perf_counter() - t_heavy)})

        if compact_state is not None:
            work.input_id = compact_state["original_input_id"]
    else:
        sym_stats = {"total": 0, "fixed": 0, "low_r2": 0, "r2_records": []}

    formulas = None
    if hasattr(work, "symbolic_formula"):
        try:
            formulas = work.symbolic_formula()
        except Exception:
            formulas = None

    valid = collect_valid_formulas(formulas)
    final_n_edge_raw = get_n_edge(work)
    final_n_edge = _count_effective_edges(work)
    return {
        "model": work,
        "formulas": formulas,
        "valid_expressions": valid,
        "trace": pd.DataFrame(trace) if trace else pd.DataFrame(),
        "sym_stats": sym_stats,
        "final_n_edge": final_n_edge,
        "final_n_edge_raw": final_n_edge_raw,
        "final_acc": float(model_acc_ds(work, dataset)),
        "effective_target_edges": effective_target,
        "input_n_edge": n_edge_input,
        "effective_input_indices": effective_inputs,
        "effective_input_dim": len(effective_inputs),
        "timing": timing,
    }


def symbolize_pipeline_report(model, dataset, **kwargs):
    """@brief symbolize_pipeline 的结构化报告版本。

    参数与 symbolize_pipeline 完全一致。
    @return SymbolizeResult 结构化结果对象。
    """
    from symkan.core.types import SymbolizeResult

    result = symbolize_pipeline(model, dataset, **kwargs)
    return SymbolizeResult(
        model=result.get("model"),
        formulas=result.get("formulas"),
        valid_expressions=result.get("valid_expressions", []),
        trace=result.get("trace"),
        sym_stats=result.get("sym_stats", {}),
        final_n_edge=result.get("final_n_edge", 0),
        final_n_edge_raw=result.get("final_n_edge_raw", 0),
        final_acc=result.get("final_acc", 0.0),
        effective_target_edges=result.get("effective_target_edges", 0),
        input_n_edge=result.get("input_n_edge", 0),
        effective_input_indices=result.get("effective_input_indices", []),
        effective_input_dim=result.get("effective_input_dim", 0),
        timing=result.get("timing", {}),
    )
