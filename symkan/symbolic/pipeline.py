"""symkan 主符号化流水线。

该模块负责将训练后的 KAN 模型推进到符号表达式导出阶段，涵盖渐进剪枝、
输入压缩、逐层符号拟合和末端强化微调。
"""

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
    """执行符号化后的强化微调。

    Args:
        work: 待微调模型。
        dataset: 微调数据集。
        total_steps: 总微调步数。
        batch_size: 批大小。
        verbose: 是否打印日志。
        lr_schedule: 分阶段学习率序列。
        early_stop_patience: 早停耐心值。
        early_stop_min_delta: 判定有效改进的最小精度增量。

    Returns:
        float: 恢复最佳参数后的模型精度。
    """
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
    prune_threshold_start=0.02,
    prune_threshold_end=0.03,
    prune_max_drop_ratio_per_round=1.0,
    prune_threshold_backoff=0.7,
    prune_adaptive_threshold=False,
    prune_adaptive_step=0.0,
    prune_adaptive_acc_drop_tol=0.02,
    prune_adaptive_min_edges_gain=1,
    prune_adaptive_low_gain_patience=4,
    heavy_ft_early_stop_patience=0,
    heavy_ft_early_stop_min_delta=1e-4,
    collect_timing=True,
    verbose=True,
):
    """执行 symkan 主符号化流水线。

    流程依次包含渐进剪枝、可选输入压缩、逐层符号拟合、强化微调和结果导出。

    Args:
        model: 待符号化的 KAN/symkan 模型。
        dataset: 由 ``build_dataset`` 构建的数据字典。
        target_edges: 目标边数。
        max_prune_rounds: 最大剪枝轮数。
        lib: 统一函数库。
        lib_hidden: 隐藏层函数库。
        lib_output: 输出层函数库。
        weight_simple: 函数复杂度偏好权重。
        finetune_steps: 每轮剪枝后的短微调步数。
        finetune_lr: 每轮剪枝后的短微调学习率。
        affine_finetune_steps: 末端强化微调总步数。
        affine_finetune_lr_schedule: 强化微调学习率序列。
        layerwise_finetune_steps: 每层符号化后微调步数。
        batch_size: 批大小；为空时自动使用默认值。
        parallel_mode: 并行模式配置，当前实现会强制回退到串行。
        parallel_workers: 期望 worker 数。
        parallel_min_tasks: 启用并行的最小任务阈值。
        prune_eval_interval: 剪枝评估间隔。
        prune_attr_sample_adaptive: 是否启用归因采样分级。
        prune_attr_sample_min: 归因最小采样数。
        prune_attr_sample_max: 归因最大采样数。
        prune_threshold_start: 渐进剪枝阈值起点。
        prune_threshold_end: 渐进剪枝阈值终点。
        prune_max_drop_ratio_per_round: 单轮允许的最大边数降幅比例。
        prune_threshold_backoff: 超降幅时的阈值回退倍数。
        prune_adaptive_threshold: 是否启用自适应阈值控制。
        prune_adaptive_step: 自适应阈值基础步长；小于等于 0 时自动估计。
        prune_adaptive_acc_drop_tol: 自适应判定中的单轮允许精度回落。
        prune_adaptive_min_edges_gain: 自适应判定中的单轮最小有效剪枝收益。
        prune_adaptive_low_gain_patience: 连续低收益轮数达到该值时提前停止剪枝。
        heavy_ft_early_stop_patience: 强化微调早停耐心轮数。
        heavy_ft_early_stop_min_delta: 早停最小改进阈值。
        collect_timing: 是否收集详细耗时统计。
        verbose: 是否打印详细日志。

    Returns:
        dict: 包含模型、表达式、边数、精度、轨迹、统计与耗时信息。
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
        # 保留旧版的宽松目标边数策略，避免极宽模型在早期轮次直接卡死。
        effective_target = max(target_edges, int(n_edge_input * 0.5))

    thresholds = np.linspace(float(prune_threshold_start), float(prune_threshold_end), max_prune_rounds)
    trace = []
    prune_eval_interval = max(1, int(prune_eval_interval))
    last_acc = float(baseline_acc)
    adaptive_mode = bool(prune_adaptive_threshold)
    th_low = min(float(prune_threshold_start), float(prune_threshold_end))
    th_high = max(float(prune_threshold_start), float(prune_threshold_end))
    adaptive_step = float(prune_adaptive_step)
    if adaptive_step <= 0:
        adaptive_step = max((th_high - th_low) / max(1, max_prune_rounds - 1), 1e-4)
    current_threshold = th_low
    success_count = 0
    failure_count = 0
    low_gain_rounds = 0

    for rd in range(max_prune_rounds):
        th = float(current_threshold if adaptive_mode else thresholds[rd])
        t_round = time.perf_counter()
        n_before = get_n_edge(work)
        if np.isfinite(n_before) and n_before <= effective_target:
            break
        acc_ref = float(last_acc)

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
        drop_ratio = 0.0
        if np.isfinite(n_before) and np.isfinite(n_after) and float(n_before) > 0:
            drop_ratio = max(0.0, (float(n_before) - float(n_after)) / float(n_before))

        if drop_ratio > float(prune_max_drop_ratio_per_round):
            # 单轮剪枝过猛，回滚并用更低阈值重试一次，避免直接塌缩到低边数区。
            work.load_state_dict(snap_prune_state)
            safer_th = max(1e-4, float(th) * float(prune_threshold_backoff))
            try:
                safe_attribute(work, dataset, n_sample=int(attr_n_sample))
                work.prune_edge(threshold=safer_th)
                n_after = get_n_edge(work)
                if np.isfinite(n_before) and np.isfinite(n_after) and float(n_before) > 0:
                    drop_ratio = max(0.0, (float(n_before) - float(n_after)) / float(n_before))
                th = safer_th
            except Exception:
                work.load_state_dict(snap_prune_state)
                break

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
        if adaptive_mode:
            should_eval = True
        if np.isfinite(n_after) and np.isfinite(effective_target) and n_after <= effective_target * 1.3:
            should_eval = True
        if rd == max_prune_rounds - 1:
            should_eval = True

        if should_eval:
            acc_now = model_acc_ds(work, dataset)
            last_acc = float(acc_now)
        else:
            acc_now = float(last_acc)

        edges_removed = 0
        if np.isfinite(n_before) and np.isfinite(n_after):
            edges_removed = max(0, int(round(float(n_before) - float(n_after))))
        acc_drop = float(acc_ref - float(acc_now))

        trace.append(
            {
                "round": rd,
                "threshold": float(th),
                "edges_before": n_before,
                "edges_after": n_after,
                "drop_ratio": float(drop_ratio),
                "edges_removed": int(edges_removed),
                "acc_drop": float(acc_drop),
                "acc": float(acc_now),
            }
        )
        if collect_timing:
            timing_prune_rounds.append(
                {
                    "round": int(rd),
                    "threshold": float(th),
                    "edges_before": float(n_before),
                    "edges_after": float(n_after),
                    "drop_ratio": float(drop_ratio),
                    "edges_removed": int(edges_removed),
                    "acc_drop": float(acc_drop),
                    "attr_n_sample": int(attr_n_sample) if prune_attr_sample_adaptive else 2048,
                    "eval_skipped": bool(not should_eval),
                    "seconds": float(time.perf_counter() - t_round),
                }
            )

        if adaptive_mode:
            no_gain = edges_removed <= 0
            too_much_drop = acc_drop > float(prune_adaptive_acc_drop_tol)
            success = (not no_gain) and (not too_much_drop)

            if no_gain:
                # 没剪掉任何边时，说明阈值过低，应上调而不是下调。
                success_count = 0
                failure_count += 1
                low_gain_rounds += 1
                probe = 1.2 + min(2.5, failure_count * 0.5)
                current_threshold = min(th_high, float(th) + adaptive_step * probe)
            elif success:
                success_count += 1
                failure_count = 0
                if edges_removed <= int(prune_adaptive_min_edges_gain):
                    low_gain_rounds += 1
                else:
                    low_gain_rounds = 0
                boost = 1.0 + min(3.0, success_count * 0.4)
                if edges_removed <= int(prune_adaptive_min_edges_gain):
                    boost *= 1.5
                current_threshold = min(th_high, float(th) + adaptive_step * boost)
            else:
                # 有剪枝但精度掉太多，说明阈值偏高，回退。
                failure_count += 1
                success_count = 0
                low_gain_rounds += 1
                penalty = 0.3 * (1.0 + min(2.0, failure_count * 0.3))
                current_threshold = max(th_low, float(th) - adaptive_step * penalty)

            # 只有在阈值已接近上界时仍持续低收益，才判定为收敛并停止，
            # 否则继续探索阈值空间。
            near_ceiling = current_threshold >= (th_high - max(adaptive_step, 1e-4))
            if near_ceiling and low_gain_rounds >= max(1, int(prune_adaptive_low_gain_patience)):
                break

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
    """返回 ``symbolize_pipeline`` 的结构化报告版本。

    Args:
        model: 待符号化模型。
        dataset: 数据集字典。
        **kwargs: 传递给 ``symbolize_pipeline`` 的其余参数。

    Returns:
        SymbolizeResult: 结构化结果对象。
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
