"""In-memory utilities for ICBR symbolic fitting and benchmark ablations.

This module keeps the Phase I ICBR workflow separate from ``MultKAN`` while
staying close to the model's runtime data structures. The public entry points
cover three layers of responsibility:

1. Batched candidate generation from teacher caches without mutating a model.
2. Replay/rerank/commit helpers that manipulate a cloned work model explicitly.
3. Benchmark orchestration that compares baseline symbolic fitting with ICBR
   variants under a shared evaluation protocol.

Most helpers operate on cloned models and are expected to preserve caller-owned
state unless their name explicitly says ``commit``.
"""

from __future__ import annotations

import copy
from time import perf_counter
from typing import Iterable, Mapping, Sequence

import numpy as np
import sympy
import torch
from sklearn.linear_model import LinearRegression

from .utils import SYMBOLIC_LIB

_ICBR_BENCHMARK_VARIANTS = (
    "baseline",
    "icbr_full",
    "icbr_no_replay",
    "icbr_no_shared",
    "icbr_refit_commit",
)


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
    """Extract a dense per-edge regression batch from layer teacher caches."""
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
    """Fit affine-wrapped parameters for one symbolic function over many edges.

    Args:
        x_batch: Edge inputs with shape ``[batch, edge]``.
        y_batch: Teacher edge targets with shape ``[batch, edge]``.
        fun: Torch-callable symbolic primitive from ``SYMBOLIC_LIB``.
        a_range: Search range for the pre-transform scale ``a``.
        b_range: Search range for the pre-transform bias ``b``.
        grid_number: Number of grid points per search axis.
        iteration: Number of coarse-to-fine refinement rounds.
        device: Optional device for the search tensors.

    Returns:
        Diagnostics for each edge, including fitted ``params`` in ``(a, b, c, d)``
        order, local ``r2`` scores, and search-quality indicators.
    """
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
    """Generate the best symbolic candidate for each requested edge.

    Args:
        teacher_acts: Cached layer activations with shape ``[batch, in_dim]``.
        teacher_edge_targets: Cached edge targets with shape
            ``[batch, out_dim, in_dim]``.
        lib: Symbolic library names or mapping to evaluate. ``None`` means the
            full ``SYMBOLIC_LIB``.
        edge_indices: Optional ``(input_idx, output_idx)`` subset. ``None``
            evaluates every edge in the layer cache.
        a_range: Search range for the pre-transform scale ``a``.
        b_range: Search range for the pre-transform bias ``b``.
        grid_number: Number of grid points per search axis.
        iteration: Number of coarse-to-fine refinement rounds.
        device: Optional device for batched fitting.

    Returns:
        A payload with one best candidate per requested edge. Each candidate
        stores the chosen function, fitted ``(a, b, c, d)`` parameters, local
        fit score, complexity, and search diagnostics.

    Raises:
        ValueError: If cache shapes are invalid or the search config is invalid.
        RuntimeError: If any requested edge fails to produce a candidate.

    Notes:
        This function is intentionally side-effect free: it only reads teacher
        caches and never mutates model symbolic state.
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
    """Capture the full symbolic/numeric edge state needed for replay rollback."""
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
    """Restore a previously snapshotted edge state exactly."""
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
    """Write a candidate directly into the symbolic layer and flip edge masks."""
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


def _extract_calibration_target(
    calibration_split: Mapping[str, torch.Tensor] | torch.Tensor,
) -> torch.Tensor | None:
    if isinstance(calibration_split, torch.Tensor):
        return None

    if "val_label" in calibration_split:
        return calibration_split["val_label"]
    if "test_label" in calibration_split:
        return calibration_split["test_label"]
    if "train_label" in calibration_split:
        return calibration_split["train_label"]
    return None


def _mse_to_target(prediction: torch.Tensor, target: torch.Tensor) -> float:
    return float(torch.mean((prediction - target).pow(2)).item())


def _r2_to_target(prediction: torch.Tensor, target: torch.Tensor) -> float:
    target_centered = target - torch.mean(target, dim=0, keepdim=True)
    ss_tot = torch.sum(target_centered.pow(2))
    if float(ss_tot.item()) <= 1e-12:
        return float("nan")
    ss_res = torch.sum((prediction - target).pow(2))
    return float((1.0 - (ss_res / ss_tot)).item())


def replay_rerank_edge_candidates(
    work_model,
    teacher_model,
    calibration_split: Mapping[str, torch.Tensor] | torch.Tensor,
    *,
    layer_idx: int,
    input_idx: int,
    output_idx: int,
    shortlist: list[Mapping[str, object]],
    teacher_output: torch.Tensor | None = None,
    singularity_avoiding: bool = False,
    y_th: float = 10.0,
) -> dict[str, object]:
    """Replay shortlisted candidates and rerank them by contextual imitation loss.

    Args:
        work_model: Mutable cloned model used for temporary replay.
        teacher_model: Numeric teacher model that provides reference outputs.
        calibration_split: Calibration input tensor or split mapping. Only the
            input portion is consumed.
        layer_idx: Layer index of the edge being replayed.
        input_idx: Input index of the edge being replayed.
        output_idx: Output index of the edge being replayed.
        shortlist: Candidate payloads, usually ranked by local edge score.
        teacher_output: Optional precomputed teacher output on
            ``calibration_input``. When provided, replay reuses it instead of
            re-running the teacher forward pass for every edge.
        singularity_avoiding: Forward-pass flag forwarded to both models.
        y_th: Singularity guard threshold forwarded to both models.

    Returns:
        Ranking metadata sorted by replay loss ascending. ``best_candidate`` is a
        deep-copied record that can be committed directly.

    Raises:
        ValueError: If ``shortlist`` is empty.
        RuntimeError: If replay unexpectedly changes ``state_id`` on either model.

    Notes:
        Replay is intentionally transactional. The probed edge state is restored
        after every candidate and again in ``finally`` so callers can treat this
        helper as read-only with respect to persistent model state.
    """

    if not shortlist:
        raise ValueError("shortlist must not be empty")

    calibration_input = _extract_calibration_input(calibration_split)
    state_id_before = getattr(work_model, "state_id", None)
    teacher_state_id_before = getattr(teacher_model, "state_id", None)
    edge_snapshot = _snapshot_symbolic_edge_state(work_model, layer_idx, input_idx, output_idx)

    if teacher_output is None:
        with torch.no_grad():
            teacher_output = teacher_model(calibration_input, singularity_avoiding=singularity_avoiding, y_th=y_th)
            if isinstance(teacher_output, tuple):
                teacher_output = teacher_output[0]
            teacher_output = teacher_output.detach()
    else:
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

            # Evaluate the candidate in the full model context instead of only
            # trusting the edge-local score produced during candidate generation.
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
    """Commit a selected candidate into ``work_model`` without refitting.

    Args:
        work_model: Mutable model whose symbolic edge state will be updated.
        layer_idx: Layer index of the edge to mutate.
        input_idx: Input index of the edge to mutate.
        output_idx: Output index of the edge to mutate.
        candidate: Candidate payload produced by generation or replay. For the
            zero function, ``{"fun_name": "0"}`` is sufficient.

    Notes:
        This is a true stateful write. It updates the symbolic function handles,
        affine parameters, and both numeric/symbolic masks so later forward
        passes and formula export see the committed symbolic edge.
    """

    _apply_symbolic_candidate_state(work_model, layer_idx, input_idx, output_idx, candidate)


def _set_teacher_numeric_mode(teacher_model) -> None:
    for layer_idx in range(len(teacher_model.symbolic_fun)):
        teacher_model.symbolic_fun[layer_idx].mask.data.zero_()


def _ensure_fully_symbolic_completion(work_model) -> None:
    for layer_idx in range(len(work_model.width_in) - 1):
        numeric_mask = work_model.act_fun[layer_idx].mask
        remaining_numeric = torch.as_tensor(numeric_mask) > 0
        if bool(torch.any(remaining_numeric).item()):
            raise RuntimeError(
                f"Layer {layer_idx} still has active numeric edges; exporter should not be considered complete."
            )


def _candidate_rank_key(candidate: Mapping[str, object]) -> tuple[float, float]:
    return (-float(candidate["r2"]), float(candidate["complexity"]))


def _update_edge_topk_shortlist(
    shortlist: list[dict[str, object]],
    *,
    candidate: Mapping[str, object],
    topk: int,
) -> None:
    if topk <= 0:
        raise ValueError("topk must be > 0")
    shortlist.append(dict(candidate))
    shortlist.sort(key=_candidate_rank_key)
    if len(shortlist) > topk:
        del shortlist[topk:]


def _is_edge_active_for_symbolic(work_model, *, layer_idx: int, input_idx: int, output_idx: int) -> bool:
    symbolic_mask = float(work_model.symbolic_fun[layer_idx].mask[output_idx, input_idx].item())
    numeric_mask = float(work_model.act_fun[layer_idx].mask[input_idx][output_idx].item())
    return symbolic_mask == 0.0 and numeric_mask > 0.0


def _collect_active_edges_for_layer(work_model, *, layer_idx: int) -> list[tuple[int, int]]:
    active_edges: list[tuple[int, int]] = []
    for input_idx in range(work_model.width_in[layer_idx]):
        for output_idx in range(work_model.width_out[layer_idx + 1]):
            if _is_edge_active_for_symbolic(
                work_model,
                layer_idx=layer_idx,
                input_idx=input_idx,
                output_idx=output_idx,
            ):
                active_edges.append((input_idx, output_idx))
    return active_edges


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
        _update_edge_topk_shortlist(
            candidates,
            candidate=result["candidates"][0],
            topk=max(1, topk),
        )
    return candidates


def _build_layer_shortlists_shared(
    teacher_acts_layer: torch.Tensor,
    teacher_edge_targets_layer: torch.Tensor,
    *,
    edge_indices: list[tuple[int, int]],
    lib_names: list[str],
    topk: int,
    a_range: tuple[float, float],
    b_range: tuple[float, float],
    grid_number: int,
    iteration: int,
) -> dict[tuple[int, int], list[dict[str, object]]]:
    """Build top-k shortlists for many edges with shared batched evaluation.

    The key invariant is that all ``edge_indices`` share the same teacher cache
    tensors, allowing each library function to be fit once in batched form and
    then split back into per-edge top-k shortlists.
    """
    if not edge_indices:
        return {}
    per_edge_candidates: dict[tuple[int, int], list[dict[str, object]]] = {edge: [] for edge in edge_indices}
    for fun_name in lib_names:
        result = generate_layer_candidates(
            teacher_acts_layer,
            teacher_edge_targets_layer,
            lib=[fun_name],
            edge_indices=edge_indices,
            a_range=a_range,
            b_range=b_range,
            grid_number=grid_number,
            iteration=iteration,
        )
        for edge, candidate in zip(edge_indices, result["candidates"]):
            _update_edge_topk_shortlist(
                per_edge_candidates[edge],
                candidate=candidate,
                topk=topk,
            )
    return per_edge_candidates


def _choose_best_candidate_by_local_score(shortlist: Sequence[Mapping[str, object]]) -> dict[str, object]:
    if not shortlist:
        raise ValueError("shortlist must not be empty")
    ranked = sorted(shortlist, key=lambda item: (-float(item["r2"]), float(item["complexity"])))
    best = dict(ranked[0])
    best["replay_score"] = float("nan")
    return best


def _commit_candidate_by_refit(
    work_model,
    *,
    layer_idx: int,
    input_idx: int,
    output_idx: int,
    candidate: Mapping[str, object],
    a_range: tuple[float, float],
    b_range: tuple[float, float],
) -> float:
    """Commit a candidate through ``fix_symbolic`` and report parameter drift.

    Returns:
        The L2 distance between the candidate parameters selected upstream and
        the affine parameters produced by the refit commit path.
    """
    fun_name = str(candidate["fun_name"])
    if fun_name == "0":
        commit_symbolic_candidate(
            work_model,
            layer_idx=layer_idx,
            input_idx=input_idx,
            output_idx=output_idx,
            candidate={"fun_name": "0"},
        )
        return float("nan")
    before = torch.as_tensor(candidate["params"], dtype=work_model.symbolic_fun[layer_idx].affine.dtype).detach().cpu()
    work_model.fix_symbolic(
        layer_idx,
        input_idx,
        output_idx,
        fun_name,
        fit_params_bool=True,
        a_range=a_range,
        b_range=b_range,
        verbose=False,
        log_history=False,
    )
    after = work_model.symbolic_fun[layer_idx].affine.data[output_idx, input_idx].detach().cpu()
    return float(torch.linalg.vector_norm(after - before).item())


def _resolve_icbr_variant_modes(variant: str) -> tuple[str, str, str]:
    if variant == "icbr_full":
        return ("shared", "replay", "explicit")
    if variant == "icbr_no_replay":
        return ("shared", "local", "explicit")
    if variant == "icbr_no_shared":
        return ("serial", "replay", "explicit")
    if variant == "icbr_refit_commit":
        return ("shared", "replay", "refit")
    raise ValueError(f"Unsupported ICBR variant: {variant}")


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
    candidate_mode: str = "shared",
    rerank_mode: str = "replay",
    commit_mode: str = "explicit",
    collect_metrics: bool = False,
):
    """Run the core ICBR Phase I loop on separate teacher/work model clones.

    Args:
        teacher_model: Clone kept in numeric mode to provide caches and replay
            targets.
        work_model: Clone that will be progressively converted to symbolic mode.
        calibration_input: Input batch used for cache generation and replay.
        lib_names: Ordered symbolic primitive names to consider.
        topk: Number of local candidates retained per edge.
        a_range: Search range for the pre-transform scale ``a``.
        b_range: Search range for the pre-transform bias ``b``.
        grid_number: Number of grid points per search axis.
        iteration: Number of coarse-to-fine refinement rounds.
        verbose: Verbosity level for progress prints.
        candidate_mode: ``"shared"`` batches per-layer shortlist generation,
            while ``"serial"`` rebuilds each edge shortlist independently.
        rerank_mode: ``"replay"`` reranks by imitation loss, while ``"local"``
            trusts edge-local R2 ordering.
        commit_mode: ``"explicit"`` writes the chosen candidate directly, while
            ``"refit"`` recomputes parameters via ``fix_symbolic``.
        collect_metrics: Whether to return timing/ablation metrics alongside the
            mutated ``work_model``.

    Returns:
        Either ``work_model`` alone or ``(work_model, metrics)`` when
        ``collect_metrics`` is true.

    Raises:
        ValueError: If invalid mode names are supplied or both model arguments
            refer to the same object.
        RuntimeError: If active numeric edges remain after conversion.
    """
    if teacher_model is work_model:
        raise ValueError("teacher_model and work_model must be different objects")

    _set_teacher_numeric_mode(teacher_model)
    teacher_model.auto_save = False
    work_model.auto_save = False

    if candidate_mode not in {"shared", "serial"}:
        raise ValueError(f"Unsupported candidate_mode: {candidate_mode}")
    if rerank_mode not in {"replay", "local"}:
        raise ValueError(f"Unsupported rerank_mode: {rerank_mode}")
    if commit_mode not in {"explicit", "refit"}:
        raise ValueError(f"Unsupported commit_mode: {commit_mode}")

    candidate_generation_wall_time_s = 0.0
    replay_rerank_wall_time_s = 0.0
    replay_rank_inversion_count = 0
    replay_rank_inversion_total = 0
    commit_param_drifts: list[float] = []
    symbolic_start = perf_counter()

    with torch.no_grad():
        teacher_output = teacher_model(calibration_input)
        if isinstance(teacher_output, tuple):
            teacher_output = teacher_output[0]
        teacher_output = teacher_output.detach()

    depth = len(work_model.width_in) - 1
    for layer_idx in range(depth):
        teacher_acts_layer = teacher_model.acts[layer_idx]
        teacher_edge_targets_layer = teacher_model.spline_postacts[layer_idx]
        shared_shortlists: dict[tuple[int, int], list[dict[str, object]]] = {}
        if candidate_mode == "shared":
            active_edges = _collect_active_edges_for_layer(work_model, layer_idx=layer_idx)
            candidate_start = perf_counter()
            shared_shortlists = _build_layer_shortlists_shared(
                teacher_acts_layer,
                teacher_edge_targets_layer,
                edge_indices=active_edges,
                lib_names=lib_names,
                topk=topk,
                a_range=a_range,
                b_range=b_range,
                grid_number=grid_number,
                iteration=iteration,
            )
            candidate_generation_wall_time_s += perf_counter() - candidate_start

        for input_idx in range(work_model.width_in[layer_idx]):
            for output_idx in range(work_model.width_out[layer_idx + 1]):
                symbolic_mask = float(work_model.symbolic_fun[layer_idx].mask[output_idx, input_idx].item())
                numeric_mask = float(work_model.act_fun[layer_idx].mask[input_idx][output_idx].item())

                if symbolic_mask > 0.0 and numeric_mask == 0.0:
                    if verbose >= 2:
                        print(f"skip ({layer_idx},{input_idx},{output_idx}) already symbolic")
                    continue

                if symbolic_mask == 0.0 and numeric_mask == 0.0:
                    # Pruned/off edges must stay inactive. Leaving them as
                    # (numeric=0, symbolic=0) preserves the pruned graph and
                    # avoids reactivating zero-value symbolic edges.
                    if verbose >= 2:
                        print(f"skip ({layer_idx},{input_idx},{output_idx}) inactive/pruned")
                    continue

                if not _is_edge_active_for_symbolic(
                    work_model,
                    layer_idx=layer_idx,
                    input_idx=input_idx,
                    output_idx=output_idx,
                ):
                    continue

                if candidate_mode == "shared":
                    shortlist = shared_shortlists[(input_idx, output_idx)]
                else:
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

                if rerank_mode == "replay":
                    rerank = replay_rerank_edge_candidates(
                        work_model,
                        teacher_model,
                        calibration_input,
                        layer_idx=layer_idx,
                        input_idx=input_idx,
                        output_idx=output_idx,
                        shortlist=shortlist,
                        teacher_output=teacher_output,
                    )
                    replay_rerank_wall_time_s += float(rerank["replay_rerank_wall_time_s"])
                    best = rerank["best_candidate"]
                    replay_rank_inversion_total += 1
                    if int(best.get("candidate_index", 0)) != 0:
                        replay_rank_inversion_count += 1
                    best_score_repr = f"replay_score={best['replay_score']:.6e}"
                else:
                    best = _choose_best_candidate_by_local_score(shortlist)
                    best_score_repr = f"local_r2={float(best['r2']):.6e}"

                if commit_mode == "explicit":
                    commit_symbolic_candidate(
                        work_model,
                        layer_idx=layer_idx,
                        input_idx=input_idx,
                        output_idx=output_idx,
                        candidate=best,
                    )
                else:
                    drift_value = _commit_candidate_by_refit(
                        work_model,
                        layer_idx=layer_idx,
                        input_idx=input_idx,
                        output_idx=output_idx,
                        candidate=best,
                        a_range=a_range,
                        b_range=b_range,
                    )
                    if np.isfinite(drift_value):
                        commit_param_drifts.append(float(drift_value))
                if verbose >= 1:
                    print(
                        f"commit ({layer_idx},{input_idx},{output_idx}) "
                        f"{best['fun_name']} {best_score_repr}"
                    )

    _ensure_fully_symbolic_completion(work_model)
    symbolic_wall_time_s = perf_counter() - symbolic_start
    if collect_metrics:
        replay_rank_inversion_rate = (
            float(replay_rank_inversion_count / replay_rank_inversion_total)
            if replay_rank_inversion_total > 0
            else float("nan")
        )
        return work_model, {
            "candidate_mode": candidate_mode,
            "rerank_mode": rerank_mode,
            "commit_mode": commit_mode,
            "candidate_generation_wall_time_s": candidate_generation_wall_time_s,
            "replay_rerank_wall_time_s": replay_rerank_wall_time_s,
            "symbolic_wall_time_s": symbolic_wall_time_s,
            "replay_rank_inversion_count": replay_rank_inversion_count,
            "replay_rank_inversion_total": replay_rank_inversion_total,
            "replay_rank_inversion_rate": replay_rank_inversion_rate,
            "commit_param_drift_l2_mean": float(np.mean(commit_param_drifts)) if commit_param_drifts else float("nan"),
            "commit_param_drift_l2_max": float(np.max(commit_param_drifts)) if commit_param_drifts else float("nan"),
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
    """Run Phase I ICBR symbolic fitting on a cloned work model.

    Args:
        model: Trained numeric ``MultKAN`` teacher to clone.
        calibration_split: Calibration tensor or split mapping. If omitted,
            ``model.cache_data`` is used.
        lib: Symbolic library names or mapping to evaluate.
        topk: Number of local candidates retained per edge before reranking.
        a_range: Search range for the pre-transform scale ``a``.
        b_range: Search range for the pre-transform bias ``b``.
        grid_number: Number of grid points per search axis.
        iteration: Number of coarse-to-fine refinement rounds.
        verbose: Verbosity level for progress prints.

    Returns:
        A new export-complete work model. All active numeric edges are
        converted to symbolic form, while already pruned/inactive edges remain
        inactive. The input ``model`` is left unchanged.

    Raises:
        ValueError: If no calibration input is available or the library is empty.
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


def _clear_model_runtime_caches(model, *, keep_cache_data: bool = False) -> None:
    runtime_attrs = (
        "acts",
        "acts_premult",
        "spline_preacts",
        "spline_postsplines",
        "spline_postacts",
        "acts_scale",
        "acts_scale_spline",
        "subnode_actscale",
        "edge_actscale",
        "symbolic_acts",
        "symbolic_acts_premult",
    )
    for attr_name in runtime_attrs:
        if hasattr(model, attr_name):
            setattr(model, attr_name, None)
    if not keep_cache_data and hasattr(model, "cache_data"):
        model.cache_data = None


def _run_baseline_symbolic_benchmark(
    model,
    *,
    calibration_input: torch.Tensor,
    evaluation_input: torch.Tensor,
    teacher_evaluation_output: torch.Tensor,
    target: torch.Tensor | None,
    input_dim: int,
    lib_names: list[str],
    formula_significant_digits: int,
) -> dict[str, object]:
    """Execute the repository baseline symbolic path under the benchmark protocol."""
    baseline_model = _clone_model_memory(model)
    baseline_model.auto_save = False
    try:
        with torch.no_grad():
            baseline_model(calibration_input)
        baseline_start = perf_counter()
        baseline_model.auto_symbolic(lib=lib_names, verbose=0, weight_simple=0.0, r2_threshold=0.0)
        baseline_symbolic_wall_time_s = perf_counter() - baseline_start
        with torch.no_grad():
            baseline_output = baseline_model(evaluation_input).detach()
        baseline_imitation_mse = torch.mean((baseline_output - teacher_evaluation_output).pow(2)).item()
        if target is not None:
            baseline_target_mse = _mse_to_target(baseline_output, target)
            baseline_target_r2 = _r2_to_target(baseline_output, target)
        else:
            baseline_target_mse = float("nan")
            baseline_target_r2 = float("nan")
        baseline_formula = _formula_export_details(
            baseline_model,
            input_dim=input_dim,
            significant_digits=formula_significant_digits,
        )
        baseline_formula_export_success = bool(baseline_formula["ok"]) and len(baseline_formula["raw"]) == int(
            baseline_output.shape[1]
        )
        return {
            "symbolic_wall_time_s": float(baseline_symbolic_wall_time_s),
            "imitation_mse": float(baseline_imitation_mse),
            "target_mse": float(baseline_target_mse),
            "target_r2": float(baseline_target_r2),
            "formula_export_success": bool(baseline_formula_export_success),
            "formula_raw": baseline_formula["raw"],
            "formula_display": baseline_formula["display"],
            "formula_error": baseline_formula["error"],
        }
    finally:
        _clear_model_runtime_caches(baseline_model)


def _run_variant_symbolic_benchmark(
    model,
    *,
    variant: str,
    calibration_input: torch.Tensor,
    evaluation_input: torch.Tensor,
    teacher_evaluation_output: torch.Tensor,
    target: torch.Tensor | None,
    input_dim: int,
    lib_names: list[str],
    topk: int,
    a_range: tuple[float, float],
    b_range: tuple[float, float],
    grid_number: int,
    iteration: int,
    formula_significant_digits: int,
) -> dict[str, object]:
    """Run one named ICBR ablation variant and collect comparable metrics."""
    candidate_mode, rerank_mode, commit_mode = _resolve_icbr_variant_modes(variant)
    teacher_model = _clone_model_memory(model)
    work_model = _clone_model_memory(model)
    teacher_model.auto_save = False
    work_model.auto_save = False
    try:
        work_model, timing = _run_auto_symbolic_icbr_with_models(
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
            candidate_mode=candidate_mode,
            rerank_mode=rerank_mode,
            commit_mode=commit_mode,
            collect_metrics=True,
        )
        with torch.no_grad():
            variant_output = work_model(evaluation_input).detach()
        variant_imitation_mse = torch.mean((variant_output - teacher_evaluation_output).pow(2)).item()
        if target is not None:
            variant_target_mse = _mse_to_target(variant_output, target)
            variant_target_r2 = _r2_to_target(variant_output, target)
        else:
            variant_target_mse = float("nan")
            variant_target_r2 = float("nan")
        variant_formula = _formula_export_details(
            work_model,
            input_dim=input_dim,
            significant_digits=formula_significant_digits,
        )
        variant_formula_export_success = bool(variant_formula["ok"]) and len(variant_formula["raw"]) == int(
            variant_output.shape[1]
        )
        return {
            "candidate_mode": candidate_mode,
            "rerank_mode": rerank_mode,
            "commit_mode": commit_mode,
            "candidate_generation_wall_time_s": float(timing["candidate_generation_wall_time_s"]),
            "replay_rerank_wall_time_s": float(timing["replay_rerank_wall_time_s"]),
            "symbolic_wall_time_s": float(timing["symbolic_wall_time_s"]),
            "replay_rank_inversion_count": int(timing["replay_rank_inversion_count"]),
            "replay_rank_inversion_total": int(timing["replay_rank_inversion_total"]),
            "replay_rank_inversion_rate": float(timing["replay_rank_inversion_rate"]),
            "commit_param_drift_l2_mean": float(timing["commit_param_drift_l2_mean"]),
            "commit_param_drift_l2_max": float(timing["commit_param_drift_l2_max"]),
            "imitation_mse": float(variant_imitation_mse),
            "target_mse": float(variant_target_mse),
            "target_r2": float(variant_target_r2),
            "formula_export_success": bool(variant_formula_export_success),
            "formula_raw": variant_formula["raw"],
            "formula_display": variant_formula["display"],
            "formula_error": variant_formula["error"],
        }
    finally:
        _clear_model_runtime_caches(teacher_model)
        _clear_model_runtime_caches(work_model)


def _normalize_benchmark_variants(variants: Sequence[str] | None) -> list[str]:
    if variants is None:
        return ["baseline", "icbr_full"]
    normalized: list[str] = []
    seen: set[str] = set()
    for raw in variants:
        name = str(raw).strip()
        if not name:
            continue
        if name not in _ICBR_BENCHMARK_VARIANTS:
            raise ValueError(f"Unknown benchmark variant: {name}")
        if name in seen:
            continue
        seen.add(name)
        normalized.append(name)
    return normalized


def _safe_ratio(numerator: float, denominator: float) -> float:
    if not np.isfinite(numerator) or not np.isfinite(denominator):
        return float("nan")
    if abs(denominator) <= 1e-12:
        return float("nan")
    return float(numerator / denominator)


def benchmark_symbolic_variants(
    model,
    *,
    calibration_split: Mapping[str, torch.Tensor] | torch.Tensor,
    calibration_target: torch.Tensor | None = None,
    evaluation_split: Mapping[str, torch.Tensor] | torch.Tensor | None = None,
    evaluation_target: torch.Tensor | None = None,
    lib: Iterable[str] | Mapping[str, tuple] | None = None,
    topk: int = 5,
    a_range: tuple[float, float] = (-10.0, 10.0),
    b_range: tuple[float, float] = (-10.0, 10.0),
    grid_number: int = 101,
    iteration: int = 3,
    formula_significant_digits: int = 6,
    variants: Sequence[str] | None = None,
) -> dict[str, object]:
    """Benchmark baseline symbolic fitting against one or more ICBR variants.

    Args:
        model: Trained numeric ``MultKAN`` teacher to benchmark from.
        calibration_split: Calibration tensor or split mapping used for symbolic
            fitting and replay.
        calibration_target: Optional calibration target override.
        evaluation_split: Optional evaluation tensor or split mapping. Defaults
            to the calibration input when omitted.
        evaluation_target: Optional evaluation target override.
        lib: Symbolic library names or mapping to evaluate.
        topk: Number of local candidates retained per edge.
        a_range: Search range for the pre-transform scale ``a``.
        b_range: Search range for the pre-transform bias ``b``.
        grid_number: Number of grid points per search axis.
        iteration: Number of coarse-to-fine refinement rounds.
        formula_significant_digits: Significant digits used for display-only
            rounded formulas.
        variants: Requested benchmark variants. ``None`` defaults to
            ``("baseline", "icbr_full")``.

    Returns:
        A benchmark bundle containing teacher quality metrics, optional baseline
        results, per-variant payloads, comparisons against baseline, and grouped
        challenge evidence for the shared-shortlist/replay/commit ablations.

    Raises:
        ValueError: If the symbolic library is empty or evaluation targets do not
            match the model output shape.
    """
    variant_names = _normalize_benchmark_variants(variants)
    calibration_input = _extract_calibration_input(calibration_split)
    if calibration_target is None:
        calibration_target = _extract_calibration_target(calibration_split)
    if evaluation_split is None:
        evaluation_input = calibration_input
    else:
        evaluation_input = _extract_calibration_input(evaluation_split)
    if evaluation_target is None:
        if evaluation_split is None:
            evaluation_target = calibration_target
        else:
            evaluation_target = _extract_calibration_target(evaluation_split)
    input_dim = int(calibration_input.shape[1])
    symbolic_lib = _resolve_symbolic_lib(lib)
    lib_names = list(symbolic_lib.keys())
    if not lib_names:
        raise ValueError("symbolic library must not be empty")

    baseline_requested = "baseline" in variant_names

    teacher_numeric = _clone_model_memory(model)
    _set_teacher_numeric_mode(teacher_numeric)
    teacher_numeric.auto_save = False
    try:
        with torch.no_grad():
            teacher_numeric(calibration_input)
            teacher_evaluation_output = teacher_numeric(evaluation_input).detach()
    finally:
        _clear_model_runtime_caches(teacher_numeric)
        del teacher_numeric

    if evaluation_target is not None:
        target = evaluation_target.to(device=teacher_evaluation_output.device, dtype=teacher_evaluation_output.dtype)
        if target.shape != teacher_evaluation_output.shape:
            raise ValueError(
                "evaluation_target shape must match model output shape; "
                f"got {tuple(target.shape)} vs {tuple(teacher_evaluation_output.shape)}"
            )
        teacher_target_mse = _mse_to_target(teacher_evaluation_output, target)
        teacher_target_r2 = _r2_to_target(teacher_evaluation_output, target)
    else:
        target = None
        teacher_target_mse = float("nan")
        teacher_target_r2 = float("nan")

    baseline_payload: dict[str, object] | None = None
    baseline_formula_export_success = False
    if baseline_requested:
        baseline_payload = _run_baseline_symbolic_benchmark(
            model,
            calibration_input=calibration_input,
            evaluation_input=evaluation_input,
            teacher_evaluation_output=teacher_evaluation_output,
            target=target,
            input_dim=input_dim,
            lib_names=lib_names,
            formula_significant_digits=formula_significant_digits,
        )
        baseline_formula_export_success = bool(baseline_payload["formula_export_success"])

    variant_payloads: dict[str, dict[str, object]] = {}
    comparisons_vs_baseline: dict[str, dict[str, float | bool]] = {}
    for variant in variant_names:
        if variant == "baseline":
            continue
        variant_payloads[variant] = _run_variant_symbolic_benchmark(
            model,
            variant=variant,
            calibration_input=calibration_input,
            evaluation_input=evaluation_input,
            teacher_evaluation_output=teacher_evaluation_output,
            target=target,
            input_dim=input_dim,
            lib_names=lib_names,
            topk=topk,
            a_range=a_range,
            b_range=b_range,
            grid_number=grid_number,
            iteration=iteration,
            formula_significant_digits=formula_significant_digits,
        )
        variant_formula_export_success = bool(variant_payloads[variant]["formula_export_success"])
        variant_imitation_mse = float(variant_payloads[variant]["imitation_mse"])
        variant_target_mse = float(variant_payloads[variant]["target_mse"])
        variant_target_r2 = float(variant_payloads[variant]["target_r2"])
        if baseline_payload is not None:
            comparisons_vs_baseline[variant] = {
                "symbolic_wall_time_delta_s": float(
                    baseline_payload["symbolic_wall_time_s"] - variant_payloads[variant]["symbolic_wall_time_s"]
                ),
                "symbolic_speedup_vs_baseline": float(
                    baseline_payload["symbolic_wall_time_s"]
                    / max(float(variant_payloads[variant]["symbolic_wall_time_s"]), 1e-12)
                ),
                "imitation_mse_shift": float(variant_imitation_mse - baseline_payload["imitation_mse"]),
                "target_mse_shift": float(variant_target_mse - baseline_payload["target_mse"]),
                "target_r2_shift": float(variant_target_r2 - baseline_payload["target_r2"]),
                "formula_export_success": bool(variant_formula_export_success and baseline_formula_export_success),
            }
        else:
            comparisons_vs_baseline[variant] = {
                "symbolic_wall_time_delta_s": float("nan"),
                "symbolic_speedup_vs_baseline": float("nan"),
                "imitation_mse_shift": float("nan"),
                "target_mse_shift": float("nan"),
                "target_r2_shift": float("nan"),
                "formula_export_success": bool(variant_formula_export_success),
            }

    full = variant_payloads.get("icbr_full")
    no_shared = variant_payloads.get("icbr_no_shared")
    no_replay = variant_payloads.get("icbr_no_replay")
    refit_commit = variant_payloads.get("icbr_refit_commit")
    challenge_evidence = {
        "shared_tensor": {
            "candidate_time_ratio_no_shared_vs_full": _safe_ratio(
                float(no_shared["candidate_generation_wall_time_s"]) if no_shared else float("nan"),
                float(full["candidate_generation_wall_time_s"]) if full else float("nan"),
            ),
            "symbolic_time_ratio_no_shared_vs_full": _safe_ratio(
                float(no_shared["symbolic_wall_time_s"]) if no_shared else float("nan"),
                float(full["symbolic_wall_time_s"]) if full else float("nan"),
            ),
        },
        "contextual_replay": {
            "imitation_mse_gain_full_vs_no_replay": (
                float(no_replay["imitation_mse"]) - float(full["imitation_mse"])
                if full is not None and no_replay is not None
                else float("nan")
            ),
            "target_mse_gain_full_vs_no_replay": (
                float(no_replay["target_mse"]) - float(full["target_mse"])
                if full is not None and no_replay is not None
                else float("nan")
            ),
            "replay_rank_inversion_rate_full": float(full["replay_rank_inversion_rate"]) if full else float("nan"),
        },
        "explicit_commit": {
            "imitation_mse_gain_explicit_vs_refit": (
                float(refit_commit["imitation_mse"]) - float(full["imitation_mse"])
                if full is not None and refit_commit is not None
                else float("nan")
            ),
            "target_mse_gain_explicit_vs_refit": (
                float(refit_commit["target_mse"]) - float(full["target_mse"])
                if full is not None and refit_commit is not None
                else float("nan")
            ),
            "refit_commit_param_drift_l2_mean": float(refit_commit["commit_param_drift_l2_mean"])
            if refit_commit
            else float("nan"),
        },
    }
    return {
        "variants_requested": list(variant_names),
        "teacher_target_mse": float(teacher_target_mse),
        "teacher_target_r2": float(teacher_target_r2),
        "baseline": baseline_payload,
        "variants": variant_payloads,
        "comparisons_vs_baseline": comparisons_vs_baseline,
        "challenge_evidence": challenge_evidence,
    }


def benchmark_icbr_vs_baseline(
    model,
    *,
    calibration_split: Mapping[str, torch.Tensor] | torch.Tensor,
    calibration_target: torch.Tensor | None = None,
    evaluation_split: Mapping[str, torch.Tensor] | torch.Tensor | None = None,
    evaluation_target: torch.Tensor | None = None,
    lib: Iterable[str] | Mapping[str, tuple] | None = None,
    topk: int = 5,
    a_range: tuple[float, float] = (-10.0, 10.0),
    b_range: tuple[float, float] = (-10.0, 10.0),
    grid_number: int = 101,
    iteration: int = 3,
    formula_significant_digits: int = 6,
) -> dict[str, object]:
    """Run the common two-way benchmark: baseline symbolic fitting vs ICBR full.

    Args:
        model: Trained numeric ``MultKAN`` teacher to benchmark from.
        calibration_split: Calibration tensor or split mapping.
        calibration_target: Optional calibration target override.
        evaluation_split: Optional evaluation tensor or split mapping.
        evaluation_target: Optional evaluation target override.
        lib: Symbolic library names or mapping to evaluate.
        topk: Number of local candidates retained per edge.
        a_range: Search range for the pre-transform scale ``a``.
        b_range: Search range for the pre-transform bias ``b``.
        grid_number: Number of grid points per search axis.
        iteration: Number of coarse-to-fine refinement rounds.
        formula_significant_digits: Significant digits used for display formulas.

    Returns:
        A flattened summary of timing, imitation/target accuracy, replay metrics,
        commit-drift metrics, and formula export outcomes for baseline vs
        ``icbr_full``.
    """
    bundle = benchmark_symbolic_variants(
        model,
        calibration_split=calibration_split,
        calibration_target=calibration_target,
        evaluation_split=evaluation_split,
        evaluation_target=evaluation_target,
        lib=lib,
        topk=topk,
        a_range=a_range,
        b_range=b_range,
        grid_number=grid_number,
        iteration=iteration,
        formula_significant_digits=formula_significant_digits,
        variants=("baseline", "icbr_full"),
    )
    baseline = bundle["baseline"]
    icbr = bundle["variants"]["icbr_full"]
    cmp = bundle["comparisons_vs_baseline"]["icbr_full"]
    return {
        "candidate_generation_wall_time_s": float(icbr["candidate_generation_wall_time_s"]),
        "replay_rerank_wall_time_s": float(icbr["replay_rerank_wall_time_s"]),
        "symbolic_wall_time_s": float(icbr["symbolic_wall_time_s"]),
        "baseline_symbolic_wall_time_s": float(baseline["symbolic_wall_time_s"]),
        "symbolic_wall_time_delta_s": float(cmp["symbolic_wall_time_delta_s"]),
        "symbolic_speedup_vs_baseline": float(cmp["symbolic_speedup_vs_baseline"]),
        "baseline_imitation_mse": float(baseline["imitation_mse"]),
        "icbr_imitation_mse": float(icbr["imitation_mse"]),
        "imitation_mse_shift": float(cmp["imitation_mse_shift"]),
        "formula_export_success": bool(cmp["formula_export_success"]),
        "baseline_formula_export_success": bool(baseline["formula_export_success"]),
        "icbr_formula_export_success": bool(icbr["formula_export_success"]),
        "baseline_formula_raw": list(baseline["formula_raw"]),
        "baseline_formula_display": list(baseline["formula_display"]),
        "icbr_formula_raw": list(icbr["formula_raw"]),
        "icbr_formula_display": list(icbr["formula_display"]),
        "baseline_formula_error": baseline["formula_error"],
        "icbr_formula_error": icbr["formula_error"],
        "teacher_target_mse": float(bundle["teacher_target_mse"]),
        "teacher_target_r2": float(bundle["teacher_target_r2"]),
        "baseline_target_mse": float(baseline["target_mse"]),
        "baseline_target_r2": float(baseline["target_r2"]),
        "icbr_target_mse": float(icbr["target_mse"]),
        "icbr_target_r2": float(icbr["target_r2"]),
        "symbolic_target_mse_shift": float(cmp["target_mse_shift"]),
        "symbolic_target_r2_shift": float(cmp["target_r2_shift"]),
        "replay_rank_inversion_count": int(icbr["replay_rank_inversion_count"]),
        "replay_rank_inversion_total": int(icbr["replay_rank_inversion_total"]),
        "replay_rank_inversion_rate": float(icbr["replay_rank_inversion_rate"]),
        "commit_param_drift_l2_mean": float(icbr["commit_param_drift_l2_mean"]),
        "commit_param_drift_l2_max": float(icbr["commit_param_drift_l2_max"]),
    }


__all__ = [
    "auto_symbolic_icbr",
    "benchmark_icbr_vs_baseline",
    "benchmark_symbolic_variants",
    "commit_symbolic_candidate",
    "generate_layer_candidates",
    "replay_rerank_edge_candidates",
]
