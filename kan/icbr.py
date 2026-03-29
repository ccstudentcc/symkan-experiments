from __future__ import annotations

from time import perf_counter
from typing import Iterable, Mapping

import numpy as np
import torch
from sklearn.linear_model import LinearRegression

from .utils import SYMBOLIC_LIB


def _resolve_symbolic_lib(
    lib: Iterable[str] | Mapping[str, tuple] | None,
) -> dict[str, tuple]:
    if lib is None:
        return dict(SYMBOLIC_LIB)

    if isinstance(lib, Mapping):
        return dict(lib)

    resolved: dict[str, tuple] = {}
    for name in lib:
        if name not in SYMBOLIC_LIB:
            raise KeyError(f"Unknown symbolic function: {name}")
        resolved[name] = SYMBOLIC_LIB[name]
    return resolved


def _build_edge_batch(
    teacher_acts: torch.Tensor,
    teacher_edge_targets: torch.Tensor,
    edge_indices: list[tuple[int, int]] | None,
) -> tuple[torch.Tensor, torch.Tensor, list[tuple[int, int]]]:
    if teacher_acts.ndim != 2:
        raise ValueError("teacher_acts must have shape [batch, in_dim]")
    if teacher_edge_targets.ndim != 3:
        raise ValueError("teacher_edge_targets must have shape [batch, out_dim, in_dim]")
    if teacher_acts.shape[0] != teacher_edge_targets.shape[0]:
        raise ValueError("teacher_acts and teacher_edge_targets must share batch dimension")
    if teacher_acts.shape[1] != teacher_edge_targets.shape[2]:
        raise ValueError("teacher_acts in_dim must match teacher_edge_targets in_dim")

    out_dim = int(teacher_edge_targets.shape[1])
    in_dim = int(teacher_edge_targets.shape[2])

    if edge_indices is None:
        selected_edges = [(i, j) for j in range(out_dim) for i in range(in_dim)]
    else:
        selected_edges = list(edge_indices)
        for i, j in selected_edges:
            if i < 0 or i >= in_dim:
                raise IndexError(f"edge i={i} out of range [0, {in_dim})")
            if j < 0 or j >= out_dim:
                raise IndexError(f"edge j={j} out of range [0, {out_dim})")

    if not selected_edges:
        raise ValueError("edge_indices must not be empty")

    x_batch = torch.stack([teacher_acts[:, i] for i, _ in selected_edges], dim=1)
    y_batch = torch.stack([teacher_edge_targets[:, j, i] for i, j in selected_edges], dim=1)
    return x_batch, y_batch, selected_edges


def _batched_fit_params_for_function(
    x_batch: torch.Tensor,
    y_batch: torch.Tensor,
    fun,
    *,
    a_range: tuple[float, float],
    b_range: tuple[float, float],
    grid_number: int,
    iteration: int,
    device: str | torch.device | None = None,
) -> dict[str, torch.Tensor]:
    if x_batch.shape != y_batch.shape:
        raise ValueError("x_batch and y_batch must have the same shape [batch, edge]")
    if grid_number < 2:
        raise ValueError("grid_number must be at least 2")
    if iteration < 1:
        raise ValueError("iteration must be at least 1")

    if device is None:
        work_device = x_batch.device
    else:
        work_device = torch.device(device)

    x = x_batch.to(work_device)
    y = y_batch.to(work_device)
    dtype = x.dtype
    edge_count = x.shape[1]

    a_low = torch.full((edge_count,), float(a_range[0]), dtype=dtype, device=work_device)
    a_high = torch.full((edge_count,), float(a_range[1]), dtype=dtype, device=work_device)
    b_low = torch.full((edge_count,), float(b_range[0]), dtype=dtype, device=work_device)
    b_high = torch.full((edge_count,), float(b_range[1]), dtype=dtype, device=work_device)

    boundary_hit = torch.zeros(edge_count, dtype=torch.bool, device=work_device)
    nan_to_num_trigger = torch.zeros(edge_count, dtype=torch.bool, device=work_device)
    top1_top2_margin = torch.zeros(edge_count, dtype=dtype, device=work_device)

    grid_steps = torch.linspace(0.0, 1.0, steps=grid_number, device=work_device, dtype=dtype)
    y_mean = torch.mean(y, dim=0, keepdim=True)
    y_centered = y - y_mean
    y_centered_ss = torch.sum(y_centered.pow(2), dim=0).clamp_min(1e-4)

    for _ in range(iteration):
        a_values = a_low[:, None] + (a_high - a_low)[:, None] * grid_steps[None, :]
        b_values = b_low[:, None] + (b_high - b_low)[:, None] * grid_steps[None, :]

        u = x[:, :, None, None] * a_values[None, :, :, None] + b_values[None, :, None, :]
        post_fun = fun(u)

        post_mean = torch.mean(post_fun, dim=0, keepdim=True)
        centered_post = post_fun - post_mean

        numerator = torch.sum(centered_post * y_centered[:, :, None, None], dim=0).pow(2)
        denominator = (
            torch.sum(centered_post.pow(2), dim=0) * y_centered_ss[:, None, None]
        ) + 1e-4
        r2_raw = numerator / denominator

        invalid_r2 = ~torch.isfinite(r2_raw)
        nan_to_num_trigger |= invalid_r2.reshape(edge_count, -1).any(dim=1)
        r2 = torch.nan_to_num(r2_raw)
        r2_flat = r2.reshape(edge_count, -1)

        best_flat = torch.argmax(r2_flat, dim=1)
        a_id = torch.div(best_flat, grid_number, rounding_mode="floor")
        b_id = best_flat % grid_number

        at_boundary = (a_id == 0) | (a_id == grid_number - 1) | (b_id == 0) | (b_id == grid_number - 1)
        boundary_hit |= at_boundary

        if grid_number * grid_number > 1:
            top2 = torch.topk(r2_flat, k=2, dim=1).values
            top1_top2_margin = top2[:, 0] - top2[:, 1]
        else:
            top1_top2_margin = torch.zeros(edge_count, dtype=dtype, device=work_device)

        a_id_minus = (a_id - 1).clamp(min=0)
        a_id_plus = (a_id + 1).clamp(max=grid_number - 1)
        b_id_minus = (b_id - 1).clamp(min=0)
        b_id_plus = (b_id + 1).clamp(max=grid_number - 1)

        a_low_inner = a_values.gather(1, a_id_minus[:, None]).squeeze(1)
        a_high_inner = a_values.gather(1, a_id_plus[:, None]).squeeze(1)
        b_low_inner = b_values.gather(1, b_id_minus[:, None]).squeeze(1)
        b_high_inner = b_values.gather(1, b_id_plus[:, None]).squeeze(1)

        a_low = torch.where(
            a_id == 0,
            a_values[:, 0],
            torch.where(a_id == grid_number - 1, a_values[:, -2], a_low_inner),
        )
        a_high = torch.where(
            a_id == 0,
            a_values[:, 1],
            torch.where(a_id == grid_number - 1, a_values[:, -1], a_high_inner),
        )
        b_low = torch.where(
            b_id == 0,
            b_values[:, 0],
            torch.where(b_id == grid_number - 1, b_values[:, -2], b_low_inner),
        )
        b_high = torch.where(
            b_id == 0,
            b_values[:, 1],
            torch.where(b_id == grid_number - 1, b_values[:, -1], b_high_inner),
        )

    a_best = a_values.gather(1, a_id[:, None]).squeeze(1)
    b_best = b_values.gather(1, b_id[:, None]).squeeze(1)
    best_r2 = r2_flat.gather(1, best_flat[:, None]).squeeze(1)

    post_fun_best = fun(a_best[None, :] * x + b_best[None, :])
    invalid_post_fun = ~torch.isfinite(post_fun_best)
    nan_to_num_trigger |= invalid_post_fun.any(dim=0)
    post_fun_best = torch.nan_to_num(post_fun_best)

    c_best = torch.empty(edge_count, dtype=dtype, device=work_device)
    d_best = torch.empty(edge_count, dtype=dtype, device=work_device)

    for edge_id in range(edge_count):
        reg = LinearRegression().fit(
            post_fun_best[:, edge_id : edge_id + 1].detach().cpu().numpy(),
            y[:, edge_id].detach().cpu().numpy(),
        )
        coef = float(np.asarray(reg.coef_).reshape(-1)[0])
        intercept = float(np.asarray(reg.intercept_).reshape(-1)[0])
        c_best[edge_id] = coef
        d_best[edge_id] = intercept

    params = torch.stack([a_best, b_best, c_best, d_best], dim=1)
    return {
        "params": params,
        "r2": best_r2,
        "boundary_hit": boundary_hit,
        "nan_to_num_trigger": nan_to_num_trigger,
        "top1_top2_margin": top1_top2_margin,
    }


def generate_layer_candidates(
    teacher_acts: torch.Tensor,
    teacher_edge_targets: torch.Tensor,
    *,
    lib: Iterable[str] | Mapping[str, tuple] | None = None,
    edge_indices: list[tuple[int, int]] | None = None,
    a_range: tuple[float, float] = (-10.0, 10.0),
    b_range: tuple[float, float] = (-10.0, 10.0),
    grid_number: int = 101,
    iteration: int = 3,
    device: str | torch.device | None = None,
) -> dict[str, object]:
    """
    Generate per-edge symbolic candidates from teacher caches without touching model state.

    Parameters are compatible with ``fit_params`` for each candidate function.
    """

    start_time = perf_counter()
    symbolic_lib = _resolve_symbolic_lib(lib)
    x_batch, y_batch, selected_edges = _build_edge_batch(teacher_acts, teacher_edge_targets, edge_indices)

    best_candidates: list[dict[str, object] | None] = [None] * len(selected_edges)

    for fun_name, content in symbolic_lib.items():
        if len(content) < 3:
            raise ValueError(f"Invalid symbolic library entry for {fun_name}")
        fun = content[0]
        complexity = float(content[2])

        fit_result = _batched_fit_params_for_function(
            x_batch,
            y_batch,
            fun,
            a_range=a_range,
            b_range=b_range,
            grid_number=grid_number,
            iteration=iteration,
            device=device,
        )

        for edge_id, (i, j) in enumerate(selected_edges):
            r2_value = float(fit_result["r2"][edge_id].item())
            current = best_candidates[edge_id]
            should_replace = current is None
            if current is not None:
                best_r2 = float(current["r2"])
                best_complexity = float(current["complexity"])
                should_replace = (r2_value > best_r2) or (
                    abs(r2_value - best_r2) <= 1e-12 and complexity < best_complexity
                )
            if should_replace:
                best_candidates[edge_id] = {
                    "i": i,
                    "j": j,
                    "fun_name": fun_name,
                    "params": fit_result["params"][edge_id].detach().cpu(),
                    "r2": r2_value,
                    "complexity": complexity,
                    "diagnostics": {
                        "boundary_hit": bool(fit_result["boundary_hit"][edge_id].item()),
                        "nan_to_num_trigger": bool(fit_result["nan_to_num_trigger"][edge_id].item()),
                        "top1_top2_margin": float(fit_result["top1_top2_margin"][edge_id].item()),
                    },
                }

    if any(candidate is None for candidate in best_candidates):
        raise RuntimeError("Failed to build candidates for all edges")

    elapsed = perf_counter() - start_time
    return {
        "candidates": best_candidates,
        "candidate_generation_wall_time_s": elapsed,
        "edge_count": len(selected_edges),
    }


__all__ = ["generate_layer_candidates"]
