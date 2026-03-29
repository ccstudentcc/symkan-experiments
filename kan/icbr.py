from __future__ import annotations

import copy
from time import perf_counter
from typing import Iterable, Mapping

import numpy as np
import sympy
import torch
from sklearn.linear_model import LinearRegression

from .utils import SYMBOLIC_LIB


def _clone_model_memory(source_model):
    from .MultKAN import MultKAN

    cloned = MultKAN(
        width=copy.deepcopy(source_model.width),
        grid=source_model.grid,
        k=source_model.k,
        mult_arity=copy.deepcopy(source_model.mult_arity),
        noise_scale=0.0,
        base_fun=source_model.base_fun_name,
        symbolic_enabled=source_model.symbolic_enabled,
        affine_trainable=source_model.affine_trainable,
        grid_eps=source_model.grid_eps,
        grid_range=copy.deepcopy(source_model.grid_range),
        sp_trainable=source_model.sp_trainable,
        sb_trainable=source_model.sb_trainable,
        save_act=source_model.save_act,
        auto_save=False,
        first_init=False,
        ckpt_path=source_model.ckpt_path,
        state_id=source_model.state_id,
        round=source_model.round,
        device=source_model.device,
        numeric_basis=getattr(source_model, "numeric_basis", "bspline"),
    )
    cloned.load_state_dict(source_model.state_dict())
    cloned.input_id = source_model.input_id.detach().clone()
    if source_model.cache_data is None:
        cloned.cache_data = None
    else:
        cloned.cache_data = source_model.cache_data.detach().clone()
    cloned.auto_save = False

    for layer_idx in range(len(source_model.symbolic_fun)):
        out_dim = source_model.symbolic_fun[layer_idx].out_dim
        in_dim = source_model.symbolic_fun[layer_idx].in_dim
        for output_idx in range(out_dim):
            for input_idx in range(in_dim):
                cloned.symbolic_fun[layer_idx].funs[output_idx][input_idx] = source_model.symbolic_fun[layer_idx].funs[
                    output_idx
                ][input_idx]
                cloned.symbolic_fun[layer_idx].funs_sympy[output_idx][input_idx] = source_model.symbolic_fun[
                    layer_idx
                ].funs_sympy[output_idx][input_idx]
                cloned.symbolic_fun[layer_idx].funs_avoid_singularity[output_idx][input_idx] = source_model.symbolic_fun[
                    layer_idx
                ].funs_avoid_singularity[output_idx][input_idx]
                cloned.symbolic_fun[layer_idx].funs_name[output_idx][input_idx] = source_model.symbolic_fun[layer_idx].funs_name[
                    output_idx
                ][input_idx]

    cloned.acts = None
    return cloned


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


def _snapshot_symbolic_edge_state(work_model, layer_idx: int, input_idx: int, output_idx: int) -> dict[str, object]:
    symbolic_layer = work_model.symbolic_fun[layer_idx]
    return {
        "fun": symbolic_layer.funs[output_idx][input_idx],
        "fun_sympy": symbolic_layer.funs_sympy[output_idx][input_idx],
        "fun_avoid_singularity": symbolic_layer.funs_avoid_singularity[output_idx][input_idx],
        "fun_name": symbolic_layer.funs_name[output_idx][input_idx],
        "affine": symbolic_layer.affine.data[output_idx, input_idx].detach().clone(),
        "numeric_mask": work_model.act_fun[layer_idx].mask.data[input_idx][output_idx].detach().clone(),
        "symbolic_mask": symbolic_layer.mask.data[output_idx][input_idx].detach().clone(),
    }


def _restore_symbolic_edge_state(
    work_model,
    layer_idx: int,
    input_idx: int,
    output_idx: int,
    snapshot: dict[str, object],
) -> None:
    symbolic_layer = work_model.symbolic_fun[layer_idx]
    symbolic_layer.funs[output_idx][input_idx] = snapshot["fun"]
    symbolic_layer.funs_sympy[output_idx][input_idx] = snapshot["fun_sympy"]
    symbolic_layer.funs_avoid_singularity[output_idx][input_idx] = snapshot["fun_avoid_singularity"]
    symbolic_layer.funs_name[output_idx][input_idx] = snapshot["fun_name"]
    symbolic_layer.affine.data[output_idx, input_idx] = snapshot["affine"]
    work_model.act_fun[layer_idx].mask.data[input_idx][output_idx] = snapshot["numeric_mask"]
    symbolic_layer.mask.data[output_idx][input_idx] = snapshot["symbolic_mask"]


def _apply_symbolic_candidate_state(
    work_model,
    layer_idx: int,
    input_idx: int,
    output_idx: int,
    candidate: Mapping[str, object],
) -> None:
    fun_name = str(candidate["fun_name"])
    if fun_name not in SYMBOLIC_LIB:
        raise KeyError(f"Unknown symbolic function: {fun_name}")

    symbolic_layer = work_model.symbolic_fun[layer_idx]
    if "params" in candidate:
        params = torch.as_tensor(
            candidate["params"],
            dtype=symbolic_layer.affine.dtype,
            device=symbolic_layer.affine.device,
        )
    elif fun_name == "0":
        params = torch.tensor([1.0, 0.0, 1.0, 0.0], dtype=symbolic_layer.affine.dtype, device=symbolic_layer.affine.device)
    else:
        raise KeyError("candidate must include 'params' unless committing the zero function")

    if params.shape != (4,):
        raise ValueError("candidate['params'] must contain exactly 4 values: (a, b, c, d)")

    symbolic_layer.funs[output_idx][input_idx] = SYMBOLIC_LIB[fun_name][0]
    symbolic_layer.funs_sympy[output_idx][input_idx] = SYMBOLIC_LIB[fun_name][1]
    symbolic_layer.funs_avoid_singularity[output_idx][input_idx] = SYMBOLIC_LIB[fun_name][3]
    symbolic_layer.funs_name[output_idx][input_idx] = fun_name
    symbolic_layer.affine.data[output_idx, input_idx] = params
    work_model.act_fun[layer_idx].mask.data[input_idx][output_idx] = 0.0
    symbolic_layer.mask.data[output_idx][input_idx] = 1.0


def _extract_calibration_input(calibration_split: Mapping[str, torch.Tensor] | torch.Tensor) -> torch.Tensor:
    if isinstance(calibration_split, torch.Tensor):
        return calibration_split

    if "val_input" in calibration_split:
        return calibration_split["val_input"]
    if "test_input" in calibration_split:
        return calibration_split["test_input"]
    if "train_input" in calibration_split:
        return calibration_split["train_input"]
    raise KeyError("calibration_split must provide one of val_input/test_input/train_input")


def replay_rerank_edge_candidates(
    work_model,
    teacher_model,
    calibration_split: Mapping[str, torch.Tensor] | torch.Tensor,
    *,
    layer_idx: int,
    input_idx: int,
    output_idx: int,
    shortlist: list[Mapping[str, object]],
    singularity_avoiding: bool = False,
    y_th: float = 10.0,
) -> dict[str, object]:
    """
    Replay shortlisted symbolic candidates on ``work_model`` and rank by imitation loss.

    The target edge state is always restored after replay. This helper does not call
    ``log_history``/checkpoint primitives and is designed for in-memory evaluation only.
    """

    if not shortlist:
        raise ValueError("shortlist must not be empty")

    calibration_input = _extract_calibration_input(calibration_split)
    state_id_before = getattr(work_model, "state_id", None)
    teacher_state_id_before = getattr(teacher_model, "state_id", None)
    edge_snapshot = _snapshot_symbolic_edge_state(work_model, layer_idx, input_idx, output_idx)

    with torch.no_grad():
        teacher_output = teacher_model(calibration_input, singularity_avoiding=singularity_avoiding, y_th=y_th)
        if isinstance(teacher_output, tuple):
            teacher_output = teacher_output[0]
        teacher_output = teacher_output.detach()

    ranking: list[dict[str, object]] = []
    replay_start = perf_counter()
    try:
        for candidate_index, candidate in enumerate(shortlist):
            _apply_symbolic_candidate_state(work_model, layer_idx, input_idx, output_idx, candidate)

            with torch.no_grad():
                work_output = work_model(calibration_input, singularity_avoiding=singularity_avoiding, y_th=y_th)
                if isinstance(work_output, tuple):
                    work_output = work_output[0]
                work_output = work_output.detach()

            replay_loss = torch.mean((work_output - teacher_output).pow(2)).item()
            ranking.append(
                {
                    "candidate_index": candidate_index,
                    "fun_name": str(candidate["fun_name"]),
                    "params": torch.as_tensor(candidate["params"]).detach().clone(),
                    "local_r2": float(candidate.get("r2", float("nan"))),
                    "complexity": float(candidate.get("complexity", float("nan"))),
                    "replay_score": float(replay_loss),
                }
            )
            _restore_symbolic_edge_state(work_model, layer_idx, input_idx, output_idx, edge_snapshot)
    finally:
        _restore_symbolic_edge_state(work_model, layer_idx, input_idx, output_idx, edge_snapshot)

    if state_id_before is not None and getattr(work_model, "state_id", None) != state_id_before:
        raise RuntimeError("replay evaluator changed work_model.state_id")
    if teacher_state_id_before is not None and getattr(teacher_model, "state_id", None) != teacher_state_id_before:
        raise RuntimeError("replay evaluator changed teacher_model.state_id")

    ranking.sort(key=lambda item: item["replay_score"])
    return {
        "edge": {"layer_idx": layer_idx, "input_idx": input_idx, "output_idx": output_idx},
        "ranked_candidates": ranking,
        "best_candidate": copy.deepcopy(ranking[0]),
        "score_name": "squared_imitation_loss",
        "replay_rerank_wall_time_s": perf_counter() - replay_start,
    }


def commit_symbolic_candidate(
    work_model,
    *,
    layer_idx: int,
    input_idx: int,
    output_idx: int,
    candidate: Mapping[str, object],
) -> None:
    """
    Commit an externally selected symbolic candidate directly to model symbolic state.

    This helper writes ``funs/funs_sympy/funs_avoid_singularity/funs_name/affine`` and
    switches masks to symbolic mode without re-fitting via ``fix_symbolic``.
    """

    _apply_symbolic_candidate_state(work_model, layer_idx, input_idx, output_idx, candidate)


def _set_teacher_numeric_mode(teacher_model) -> None:
    for layer_idx in range(len(teacher_model.symbolic_fun)):
        teacher_model.symbolic_fun[layer_idx].mask.data.zero_()


def _ensure_fully_symbolic_completion(work_model) -> None:
    for layer_idx in range(len(work_model.width_in) - 1):
        numeric_mask = work_model.act_fun[layer_idx].mask
        symbolic_mask = work_model.symbolic_fun[layer_idx].mask
        fully_symbolic = torch.logical_and(numeric_mask == 0, symbolic_mask.T == 1)
        if not bool(torch.all(fully_symbolic).item()):
            raise RuntimeError(
                f"Layer {layer_idx} is not fully symbolic; exporter should not be considered complete."
            )


def _build_edge_shortlist(
    teacher_acts_layer: torch.Tensor,
    teacher_edge_targets_layer: torch.Tensor,
    *,
    input_idx: int,
    output_idx: int,
    lib_names: list[str],
    topk: int,
    a_range: tuple[float, float],
    b_range: tuple[float, float],
    grid_number: int,
    iteration: int,
) -> list[dict[str, object]]:
    candidates: list[dict[str, object]] = []
    for fun_name in lib_names:
        result = generate_layer_candidates(
            teacher_acts_layer,
            teacher_edge_targets_layer,
            lib=[fun_name],
            edge_indices=[(input_idx, output_idx)],
            a_range=a_range,
            b_range=b_range,
            grid_number=grid_number,
            iteration=iteration,
        )
        candidates.append(result["candidates"][0])

    candidates.sort(key=lambda item: (-float(item["r2"]), float(item["complexity"])))
    topk = max(1, min(topk, len(candidates)))
    return candidates[:topk]


def _run_auto_symbolic_icbr_with_models(
    teacher_model,
    work_model,
    calibration_input: torch.Tensor,
    *,
    lib_names: list[str],
    topk: int,
    a_range: tuple[float, float],
    b_range: tuple[float, float],
    grid_number: int,
    iteration: int,
    verbose: int,
    collect_metrics: bool = False,
):
    if teacher_model is work_model:
        raise ValueError("teacher_model and work_model must be different objects")

    _set_teacher_numeric_mode(teacher_model)
    teacher_model.auto_save = False
    work_model.auto_save = False

    candidate_generation_wall_time_s = 0.0
    replay_rerank_wall_time_s = 0.0
    symbolic_start = perf_counter()

    with torch.no_grad():
        teacher_model(calibration_input)

    depth = len(work_model.width_in) - 1
    for layer_idx in range(depth):
        teacher_acts_layer = teacher_model.acts[layer_idx]
        teacher_edge_targets_layer = teacher_model.spline_postacts[layer_idx]

        for input_idx in range(work_model.width_in[layer_idx]):
            for output_idx in range(work_model.width_out[layer_idx + 1]):
                symbolic_mask = float(work_model.symbolic_fun[layer_idx].mask[output_idx, input_idx].item())
                numeric_mask = float(work_model.act_fun[layer_idx].mask[input_idx][output_idx].item())

                if symbolic_mask > 0.0 and numeric_mask == 0.0:
                    if verbose >= 2:
                        print(f"skip ({layer_idx},{input_idx},{output_idx}) already symbolic")
                    continue

                if symbolic_mask == 0.0 and numeric_mask == 0.0:
                    commit_symbolic_candidate(
                        work_model,
                        layer_idx=layer_idx,
                        input_idx=input_idx,
                        output_idx=output_idx,
                        candidate={"fun_name": "0"},
                    )
                    if verbose >= 1:
                        print(f"commit ({layer_idx},{input_idx},{output_idx}) as 0")
                    continue

                candidate_start = perf_counter()
                shortlist = _build_edge_shortlist(
                    teacher_acts_layer,
                    teacher_edge_targets_layer,
                    input_idx=input_idx,
                    output_idx=output_idx,
                    lib_names=lib_names,
                    topk=topk,
                    a_range=a_range,
                    b_range=b_range,
                    grid_number=grid_number,
                    iteration=iteration,
                )
                candidate_generation_wall_time_s += perf_counter() - candidate_start
                rerank = replay_rerank_edge_candidates(
                    work_model,
                    teacher_model,
                    calibration_input,
                    layer_idx=layer_idx,
                    input_idx=input_idx,
                    output_idx=output_idx,
                    shortlist=shortlist,
                )
                replay_rerank_wall_time_s += float(rerank["replay_rerank_wall_time_s"])
                best = rerank["best_candidate"]
                commit_symbolic_candidate(
                    work_model,
                    layer_idx=layer_idx,
                    input_idx=input_idx,
                    output_idx=output_idx,
                    candidate=best,
                )
                if verbose >= 1:
                    print(
                        f"commit ({layer_idx},{input_idx},{output_idx}) "
                        f"{best['fun_name']} replay_score={best['replay_score']:.6e}"
                    )

    _ensure_fully_symbolic_completion(work_model)
    symbolic_wall_time_s = perf_counter() - symbolic_start
    if collect_metrics:
        return work_model, {
            "candidate_generation_wall_time_s": candidate_generation_wall_time_s,
            "replay_rerank_wall_time_s": replay_rerank_wall_time_s,
            "symbolic_wall_time_s": symbolic_wall_time_s,
        }
    return work_model


def auto_symbolic_icbr(
    model,
    *,
    calibration_split: Mapping[str, torch.Tensor] | torch.Tensor | None = None,
    lib: Iterable[str] | Mapping[str, tuple] | None = None,
    topk: int = 5,
    a_range: tuple[float, float] = (-10.0, 10.0),
    b_range: tuple[float, float] = (-10.0, 10.0),
    grid_number: int = 101,
    iteration: int = 3,
    verbose: int = 1,
):
    """
    Run Phase I ICBR symbolic fitting on a cloned work model.

    Returns a new work model and keeps the input model unchanged.
    """

    if calibration_split is None:
        if getattr(model, "cache_data", None) is None:
            raise ValueError("calibration_split is required when model.cache_data is empty")
        calibration_input = model.cache_data
    else:
        calibration_input = _extract_calibration_input(calibration_split)

    symbolic_lib = _resolve_symbolic_lib(lib)
    lib_names = list(symbolic_lib.keys())
    if not lib_names:
        raise ValueError("symbolic library must not be empty")

    teacher_model = _clone_model_memory(model)
    work_model = _clone_model_memory(model)
    return _run_auto_symbolic_icbr_with_models(
        teacher_model,
        work_model,
        calibration_input,
        lib_names=lib_names,
        topk=topk,
        a_range=a_range,
        b_range=b_range,
        grid_number=grid_number,
        iteration=iteration,
        verbose=verbose,
    )


def _round_sympy_expr(expr, significant_digits: int = 6):
    rounded = expr
    for atom in sympy.preorder_traversal(expr):
        if isinstance(atom, sympy.Float):
            rounded_value = f"{float(atom):.{significant_digits}g}"
            rounded = rounded.subs(atom, sympy.Float(rounded_value))
    return rounded


def _formula_export_details(
    model,
    *,
    input_dim: int,
    significant_digits: int = 6,
) -> dict[str, object]:
    try:
        formulas, _ = model.symbolic_formula(var=[f"x_{idx + 1}" for idx in range(input_dim)])
    except Exception as exc:
        return {
            "ok": False,
            "raw": [],
            "display": [],
            "error": f"{type(exc).__name__}: {exc}",
        }

    raw = [str(expr) for expr in formulas]
    display = [str(_round_sympy_expr(expr, significant_digits=significant_digits)) for expr in formulas]
    return {"ok": True, "raw": raw, "display": display, "error": None}


def benchmark_icbr_vs_baseline(
    model,
    *,
    calibration_split: Mapping[str, torch.Tensor] | torch.Tensor,
    lib: Iterable[str] | Mapping[str, tuple] | None = None,
    topk: int = 5,
    a_range: tuple[float, float] = (-10.0, 10.0),
    b_range: tuple[float, float] = (-10.0, 10.0),
    grid_number: int = 101,
    iteration: int = 3,
    formula_significant_digits: int = 6,
) -> dict[str, object]:
    calibration_input = _extract_calibration_input(calibration_split)
    input_dim = int(calibration_input.shape[1])
    symbolic_lib = _resolve_symbolic_lib(lib)
    lib_names = list(symbolic_lib.keys())
    if not lib_names:
        raise ValueError("symbolic library must not be empty")

    teacher_numeric = _clone_model_memory(model)
    _set_teacher_numeric_mode(teacher_numeric)
    teacher_numeric.auto_save = False
    with torch.no_grad():
        teacher_output = teacher_numeric(calibration_input).detach()

    baseline_model = _clone_model_memory(model)
    baseline_model.auto_save = False
    with torch.no_grad():
        baseline_model(calibration_input)
    baseline_start = perf_counter()
    baseline_model.auto_symbolic(lib=lib_names, verbose=0, weight_simple=0.0, r2_threshold=0.0)
    baseline_symbolic_wall_time_s = perf_counter() - baseline_start
    with torch.no_grad():
        baseline_output = baseline_model(calibration_input).detach()
    baseline_mse = torch.mean((baseline_output - teacher_output).pow(2)).item()
    baseline_formula = _formula_export_details(
        baseline_model,
        input_dim=input_dim,
        significant_digits=formula_significant_digits,
    )
    baseline_formula_ok = bool(baseline_formula["ok"]) and len(baseline_formula["raw"]) == int(baseline_output.shape[1])

    teacher_model = _clone_model_memory(model)
    work_model = _clone_model_memory(model)
    work_model, icbr_timing = _run_auto_symbolic_icbr_with_models(
        teacher_model,
        work_model,
        calibration_input,
        lib_names=lib_names,
        topk=topk,
        a_range=a_range,
        b_range=b_range,
        grid_number=grid_number,
        iteration=iteration,
        verbose=0,
        collect_metrics=True,
    )
    with torch.no_grad():
        icbr_output = work_model(calibration_input).detach()
    icbr_mse = torch.mean((icbr_output - teacher_output).pow(2)).item()
    icbr_formula = _formula_export_details(
        work_model,
        input_dim=input_dim,
        significant_digits=formula_significant_digits,
    )
    icbr_formula_ok = bool(icbr_formula["ok"]) and len(icbr_formula["raw"]) == int(icbr_output.shape[1])

    icbr_symbolic_wall_time_s = float(icbr_timing["symbolic_wall_time_s"])
    baseline_symbolic_wall_time_s_f = float(baseline_symbolic_wall_time_s)
    symbolic_speedup_vs_baseline = baseline_symbolic_wall_time_s_f / max(icbr_symbolic_wall_time_s, 1e-12)
    symbolic_wall_time_delta_s = baseline_symbolic_wall_time_s_f - icbr_symbolic_wall_time_s

    return {
        "candidate_generation_wall_time_s": float(icbr_timing["candidate_generation_wall_time_s"]),
        "replay_rerank_wall_time_s": float(icbr_timing["replay_rerank_wall_time_s"]),
        "symbolic_wall_time_s": icbr_symbolic_wall_time_s,
        "baseline_symbolic_wall_time_s": baseline_symbolic_wall_time_s_f,
        "symbolic_wall_time_delta_s": float(symbolic_wall_time_delta_s),
        "symbolic_speedup_vs_baseline": float(symbolic_speedup_vs_baseline),
        "replay_imitation_gap": float(icbr_mse),
        "final_mse_loss_shift": float(icbr_mse - baseline_mse),
        "formula_validation_result": bool(icbr_formula_ok and baseline_formula_ok),
        "baseline_formula_validation_result": bool(baseline_formula_ok),
        "icbr_formula_validation_result": bool(icbr_formula_ok),
        "baseline_formula_raw": baseline_formula["raw"],
        "baseline_formula_display": baseline_formula["display"],
        "icbr_formula_raw": icbr_formula["raw"],
        "icbr_formula_display": icbr_formula["display"],
        "baseline_formula_error": baseline_formula["error"],
        "icbr_formula_error": icbr_formula["error"],
        "baseline_mse": float(baseline_mse),
        "icbr_mse": float(icbr_mse),
    }


__all__ = [
    "auto_symbolic_icbr",
    "benchmark_icbr_vs_baseline",
    "commit_symbolic_candidate",
    "generate_layer_candidates",
    "replay_rerank_edge_candidates",
]
