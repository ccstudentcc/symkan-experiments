from __future__ import annotations

import ast
import argparse
from contextlib import contextmanager, redirect_stderr, redirect_stdout
import csv
import hashlib
import json
import math
import os
import random
import statistics
import time
import warnings
from dataclasses import dataclass, replace
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Union

import numpy as np
import torch

from kan.MultKAN import MultKAN
from kan.icbr import benchmark_symbolic_variants
from kan.utils import create_dataset


@contextmanager
def _suppress_console_output(enabled: bool):
    if not enabled:
        yield
        return
    with open(os.devnull, "w", encoding="utf-8") as sink:
        with redirect_stdout(sink), redirect_stderr(sink):
            yield


_NUMERIC_METRICS = [
    "teacher_test_mse",
    "teacher_test_r2",
    "candidate_generation_wall_time_s",
    "replay_rerank_wall_time_s",
    "symbolic_wall_time_s",
    "baseline_symbolic_wall_time_s",
    "symbolic_wall_time_delta_s",
    "symbolic_speedup_vs_baseline",
    "replay_imitation_gap",
    "final_mse_loss_shift",
    "baseline_mse",
    "icbr_mse",
    "teacher_target_mse",
    "teacher_target_r2",
    "baseline_target_mse",
    "baseline_target_r2",
    "icbr_target_mse",
    "icbr_target_r2",
    "symbolic_target_mse_shift",
    "symbolic_target_r2_shift",
]

_BOOLEAN_METRICS = [
    "teacher_cache_hit",
    "teacher_quality_gate_pass",
    "formula_validation_result",
    "baseline_formula_validation_result",
    "icbr_formula_validation_result",
]

_SIGNIFICANCE_DIRECTIONS = {
    "symbolic_wall_time_delta_s": "positive",
    "final_mse_loss_shift": "negative",
}

_CHALLENGE_EVIDENCE_METRICS = [
    "shared_tensor_candidate_time_ratio_no_shared_vs_full",
    "shared_tensor_symbolic_time_ratio_no_shared_vs_full",
    "contextual_replay_mse_gain_full_vs_no_replay",
    "contextual_replay_target_mse_gain_full_vs_no_replay",
    "contextual_replay_rank_inversion_rate_full",
    "explicit_commit_mse_gain_explicit_vs_refit",
    "explicit_commit_target_mse_gain_explicit_vs_refit",
    "explicit_commit_refit_commit_param_drift_l2_mean",
]

_VARIANT_NUMERIC_METRICS = [
    "candidate_generation_wall_time_s",
    "replay_rerank_wall_time_s",
    "symbolic_wall_time_s",
    "mse",
    "target_mse",
    "target_r2",
    "baseline_symbolic_wall_time_s",
    "baseline_mse",
    "baseline_target_mse",
    "baseline_target_r2",
    "symbolic_wall_time_delta_s",
    "symbolic_speedup_vs_baseline",
    "final_mse_loss_shift",
    "symbolic_target_mse_shift",
    "symbolic_target_r2_shift",
    "replay_rank_inversion_count",
    "replay_rank_inversion_total",
    "replay_rank_inversion_rate",
    "commit_param_drift_l2_mean",
    "commit_param_drift_l2_max",
]

_VARIANT_BOOLEAN_METRICS = [
    "formula_validation_result",
    "teacher_quality_gate_pass",
]

_BENCHMARK_PROFILES: dict[str, dict[str, float | int]] = {
    "quick": {
        "train_num": 64,
        "test_num": 64,
        "train_steps": 20,
        "lr": 1e-2,
        "lamb": 1e-3,
    },
    "quality": {
        "train_num": 1000,
        "test_num": 500,
        "train_steps": 200,
        "lr": 1e-2,
        "lamb": 1e-3,
    },
    "feynman_reference": {
        "train_num": 2000,
        "test_num": 1000,
        "train_steps": 200,
        "lr": 1e-2,
        "lamb": 1e-2,
    },
}

_TEACHER_CACHE_MODES = {"readwrite", "readonly", "refresh", "off"}
_BENCHMARK_VARIANTS = (
    "baseline",
    "icbr_full",
    "icbr_no_replay",
    "icbr_no_shared",
    "icbr_refit_commit",
)
_FEYNMAN_VARIANTS = (
    "Feynman_without_units",
    "Feynman_with_units",
    "bonus_without_units",
    "bonus_with_units",
)
_FEYNMAN_FIT_OPTS = ("Adam", "LBFGS")
_FEYNMAN_PAPER10_DATASETS = [
    "feynman_I_9_18",
    "feynman_I_10_7",
    "feynman_I_12_1",
    "feynman_I_12_4",
    "feynman_I_13_4",
    "feynman_I_34_1",
    "feynman_II_6_15a",
    "feynman_II_6_15b",
    "feynman_II_21_32",
    "feynman_II_34_29a",
]

_WidthToken = Union[int, list[int]]


@dataclass(frozen=True)
class _VisualizationStyle:
    font_family: str = "DejaVu Sans"
    base_font_size: float = 10.5
    title_font_size: float = 12.5
    tick_font_size: float = 9.5
    annotation_font_size: float = 8.8
    grid_color: str = "#D8DEE6"
    grid_alpha: float = 0.85
    grid_linewidth: float = 0.8
    spine_color: str = "#5D6773"
    text_color: str = "#1C2733"
    figure_facecolor: str = "#FAFBFC"
    axes_facecolor: str = "#FFFFFF"
    note_facecolor: str = "#F7F3EA"
    note_edgecolor: str = "#D3C7B4"
    legend_facecolor: str = "#FFFFFF"
    legend_edgecolor: str = "#D8DEE6"
    baseline_color: str = "#7A8796"
    icbr_color: str = "#1F4E79"
    accent_green: str = "#2E8B57"
    accent_red: str = "#C65D4B"
    accent_gold: str = "#C69214"
    violin_fill: str = "#A9C3E2"
    violin_edge: str = "#3E648C"
    point_color: str = "#173B5E"
    kde_bandwidth_rule: str = "silverman"
    ci_multiplier: float = 1.96


_VISUALIZATION_STYLE = _VisualizationStyle()

_REPLOT_ROW_METRICS = {
    "baseline_symbolic_wall_time_s",
    "symbolic_wall_time_s",
    "symbolic_speedup_vs_baseline",
    "final_mse_loss_shift",
    "shared_tensor_symbolic_time_ratio_no_shared_vs_full",
    "contextual_replay_mse_gain_full_vs_no_replay",
    "explicit_commit_mse_gain_explicit_vs_refit",
}

_REPLOT_VARIANT_METRICS = {
    "symbolic_wall_time_s",
    "mse",
    "target_mse",
}


@dataclass(frozen=True)
class _TaskSpec:
    name: str
    n_var: int
    width: list[_WidthToken]
    target_fn: Callable[[torch.Tensor], torch.Tensor] | None
    lib: list[str] | None
    icbr_topk: int | None = None
    teacher_max_test_mse: float | None = None
    teacher_min_test_r2: float | None = None
    ranges: list[list[float]] | list[float] | None = None
    dataset_kind: str = "synthetic"
    dataset_path: str | None = None
    dataset_variant: str | None = None
    dataset_split_strategy: str = "random"
    dataset_split_seed: int | None = None
    dataset_filename: str | None = None
    dataset_total_rows: int | None = None
    dataset_total_columns: int | None = None
    target_formula: str | None = None
    equation_metadata: dict[str, str] | None = None
    teacher_grid: int = 5
    teacher_k: int = 3
    teacher_fit_opt: str = "Adam"
    teacher_post_train_prune: bool = False
    teacher_prune_node_th: float = 1e-2
    teacher_prune_edge_th: float = 3e-2
    teacher_prune_iters: int = 1
    teacher_post_prune_steps: int = 0
    teacher_post_prune_lr: float = 1e-3
    teacher_post_prune_lamb: float = 1e-2
    teacher_post_prune_early_stop: bool = False
    teacher_post_prune_eval_every: int = 5
    teacher_post_prune_min_delta: float = 1e-6
    teacher_post_prune_patience: int = 2


def _task_specs() -> dict[str, _TaskSpec]:
    return {
        "minimal": _TaskSpec(
            name="minimal",
            n_var=1,
            width=[1, 1],
            target_fn=lambda x: torch.sin(torch.pi * x[:, [0]]),
            lib=None,
            ranges=[-1, 1],
        ),
        "combo": _TaskSpec(
            name="combo",
            n_var=2,
            width=[2, 2, 1],
            target_fn=lambda x: torch.sin(torch.pi * x[:, [0]]) + x[:, [1]] ** 2,
            lib=None,
            ranges=[-1, 1],
        ),
        "poly_cubic": _TaskSpec(
            name="poly_cubic",
            n_var=2,
            width=[2, 3, 1],
            target_fn=lambda x: 0.8 * x[:, [0]] ** 3 - 0.4 * x[:, [0]] + 0.6 * x[:, [1]] ** 2,
            lib=None,
            ranges=[-1, 1],
        ),
        "trig_interaction": _TaskSpec(
            name="trig_interaction",
            n_var=3,
            width=[3, 4, 1],
            target_fn=lambda x: torch.sin(torch.pi * x[:, [0]])
            + 0.5 * torch.cos(torch.pi * x[:, [1]])
            + x[:, [0]] * x[:, [2]],
            lib=None,
            icbr_topk=5,
            ranges=[-1, 1],
        ),
    }


def _normalize_width_token(value: object) -> _WidthToken:
    if isinstance(value, (int, np.integer)):
        normalized = int(value)
        if normalized <= 0:
            raise ValueError("Width values must be positive.")
        return normalized
    if isinstance(value, tuple):
        value = list(value)
    if isinstance(value, list):
        if len(value) != 2:
            raise ValueError("Multiplication-aware width entries must have exactly two integers: [num_sum, num_mult].")
        normalized_pair = [_normalize_width_token(item) for item in value]
        if not all(isinstance(item, int) for item in normalized_pair):
            raise ValueError("Nested width entries cannot contain further nested structures.")
        return [int(normalized_pair[0]), int(normalized_pair[1])]
    raise ValueError("Width entries must be integers or two-integer lists like [5,2].")


def _serialize_width_tokens(width_tokens: list[_WidthToken]) -> _WidthToken | list[_WidthToken]:
    serialized = [list(token) if isinstance(token, list) else int(token) for token in width_tokens]
    if len(serialized) == 1:
        single = serialized[0]
        return list(single) if isinstance(single, list) else int(single)
    return serialized


def _tasks_request_feynman_defaults(tasks: list[str]) -> bool:
    feynman_tokens = {"feynman_paper10", "feynman_random"}
    return any(task.startswith("feynman_") or task in feynman_tokens for task in tasks)


def _seed_everything(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


def _resolve_dataset_split_seed(spec: _TaskSpec, *, benchmark_seed: int) -> int | None:
    if spec.dataset_kind != "feynman_file":
        return None
    if spec.dataset_split_seed is not None:
        return int(spec.dataset_split_seed)
    return int(benchmark_seed)


def _parse_width_mid(text: str) -> list[_WidthToken]:
    raw_text = text.strip()
    if not raw_text:
        raise ValueError("feynman_width_mid must contain at least one width entry.")

    if raw_text.startswith("[") and raw_text.endswith("]"):
        parsed = ast.literal_eval(raw_text)
        if isinstance(parsed, tuple):
            parsed = list(parsed)
        if isinstance(parsed, list):
            if all(isinstance(item, (int, np.integer)) for item in parsed):
                if len(parsed) == 2:
                    return [_normalize_width_token(parsed)]
                return [_normalize_width_token(item) for item in parsed]
            return [_normalize_width_token(item) for item in parsed]
        return [_normalize_width_token(parsed)]

    values = [chunk.strip() for chunk in raw_text.split(",") if chunk.strip()]
    if not values:
        raise ValueError("feynman_width_mid must contain at least one integer.")
    return [_normalize_width_token(int(value)) for value in values]


def _feynman_cli_to_filename(ds_name: str) -> str:
    if ds_name.lower().startswith("feynman_"):
        ds_name = ds_name[len("feynman_") :]
    parts = ds_name.split("_")
    return ".".join(parts)


def _feynman_filename_to_cli(filename: str) -> str:
    return "feynman_" + filename.replace(".", "_")


def _list_local_feynman_dataset_names(
    feynman_root: Path,
    variant: str,
) -> list[str]:
    base_dir = feynman_root / variant
    if not base_dir.is_dir():
        return []
    names: list[str] = []
    for fp in sorted(base_dir.iterdir()):
        if not fp.is_file() or fp.name.startswith("."):
            continue
        names.append(_feynman_filename_to_cli(fp.name))
    return names


def _load_feynman_equations_map(
    equations_csv_path: Path | None,
) -> tuple[dict[str, str], dict[str, dict[str, str]], list[str]]:
    if equations_csv_path is None or not equations_csv_path.is_file():
        return {}, {}, []
    with equations_csv_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            return {}, {}, []
        raw_fieldnames = list(reader.fieldnames)
        fieldnames = [name.lstrip("\ufeff").strip() for name in raw_fieldnames]
        clean_to_raw = {clean: raw for clean, raw in zip(fieldnames, raw_fieldnames)}
        lower_to_name = {name.lower(): name for name in fieldnames}
        name_col = fieldnames[0]
        for candidate in ("filename", "name", "equation", "id"):
            if candidate in lower_to_name:
                name_col = lower_to_name[candidate]
                break
        formula_col = fieldnames[-1]
        for candidate in ("formula", "feynman", "tex", "equation", "rhs", "lhs", "target", "output"):
            if candidate in lower_to_name:
                formula_col = lower_to_name[candidate]
                break
        mapping: dict[str, str] = {}
        metadata_map: dict[str, dict[str, str]] = {}
        for row in reader:
            key = str(row.get(clean_to_raw[name_col], "")).strip()
            value = str(row.get(clean_to_raw[formula_col], "")).strip()
            if key and key.lower() != "nan":
                mapping[key] = value
                normalized_row: dict[str, str] = {}
                for field in fieldnames:
                    field_value = str(row.get(clean_to_raw[field], "")).strip()
                    if field_value and field_value.lower() != "nan":
                        normalized_row[field] = field_value
                metadata_map[key] = normalized_row
        return mapping, metadata_map, fieldnames


def _load_local_feynman_dataset_as_kan(
    *,
    dataset_path: Path,
    split_seed: int,
    train_num: int,
    test_num: int,
    split_strategy: str,
) -> dict[str, torch.Tensor]:
    if not dataset_path.is_file():
        raise FileNotFoundError(f"Feynman dataset file not found: {dataset_path}")
    data = np.loadtxt(dataset_path)
    if data.ndim == 1:
        data = data.reshape(-1, 1)
    if data.shape[1] < 2:
        raise ValueError(f"Dataset must contain at least one feature and one label column: {dataset_path}")

    x_np = data[:, :-1].astype(np.float32)
    y_np = data[:, -1:].astype(np.float32)
    total = int(x_np.shape[0])
    n_tr = int(min(train_num, total))
    n_te = int(min(test_num, max(0, total - n_tr)))

    if split_strategy == "linspace":
        tr_idx = np.unique(np.round(np.linspace(0, total - 1, n_tr)).astype(int))
        te_all = np.unique(np.round(np.linspace(0, total - 1, n_tr + n_te)).astype(int))
        te_idx = te_all[~np.isin(te_all, tr_idx)][:n_te]
    elif split_strategy == "random":
        rng = np.random.RandomState(split_seed)
        perm = rng.permutation(total)
        tr_idx = perm[:n_tr]
        te_idx = perm[n_tr : n_tr + n_te] if n_te > 0 else np.array([], dtype=int)
    else:  # pragma: no cover - argparse constrains this
        raise ValueError(f"Unknown feynman split strategy: {split_strategy}")

    train_input = torch.from_numpy(x_np[tr_idx]).to(device="cpu", dtype=torch.float32)
    train_label = torch.from_numpy(y_np[tr_idx]).to(device="cpu", dtype=torch.float32)
    if n_te > 0:
        test_input = torch.from_numpy(x_np[te_idx]).to(device="cpu", dtype=torch.float32)
        test_label = torch.from_numpy(y_np[te_idx]).to(device="cpu", dtype=torch.float32)
    else:
        test_input = torch.empty((0, x_np.shape[1]), dtype=torch.float32, device="cpu")
        test_label = torch.empty((0, 1), dtype=torch.float32, device="cpu")

    return {
        "train_input": train_input,
        "train_label": train_label,
        "test_input": test_input,
        "test_label": test_label,
    }


def _expand_feynman_task_tokens(
    tasks: list[str],
    *,
    feynman_root: Path,
    feynman_variant: str,
    feynman_max_datasets: int,
    feynman_dataset_select_seed: int,
) -> list[str]:
    expanded: list[str] = []
    for task in tasks:
        if task == "feynman_paper10":
            expanded.extend(_FEYNMAN_PAPER10_DATASETS)
            continue
        if task == "feynman_random":
            available = _list_local_feynman_dataset_names(feynman_root, feynman_variant)
            if not available:
                raise RuntimeError(
                    f"No Feynman datasets found in {(feynman_root / feynman_variant)} for token 'feynman_random'."
                )
            rng = np.random.RandomState(feynman_dataset_select_seed)
            shuffled = list(available)
            rng.shuffle(shuffled)
            expanded.extend(shuffled[: int(feynman_max_datasets)])
            continue
        expanded.append(task)

    deduped: list[str] = []
    seen: set[str] = set()
    for task in expanded:
        if task in seen:
            continue
        seen.add(task)
        deduped.append(task)
    return deduped


def _build_feynman_task_spec(
    *,
    task_name: str,
    feynman_root: Path,
    feynman_variant: str,
    feynman_width_mid: list[_WidthToken],
    feynman_split_strategy: str,
    feynman_split_strategy_seed: int | None,
    feynman_post_prune_steps: int | None,
    feynman_post_prune_lr: float | None,
    feynman_post_prune_lamb: float | None,
    feynman_post_prune_eval_every: int | None,
    feynman_post_prune_min_delta: float | None,
    feynman_post_prune_patience: int | None,
    prune_iters: int,
    feynman_fit_opt: str | None,
    equations_map: dict[str, str],
    equations_metadata_map: dict[str, dict[str, str]],
) -> _TaskSpec:
    filename = _feynman_cli_to_filename(task_name)
    dataset_path = (feynman_root / feynman_variant / filename).resolve()
    if not dataset_path.is_file():
        raise FileNotFoundError(
            f"Feynman task '{task_name}' requires file '{dataset_path}', but it does not exist."
        )
    raw = np.loadtxt(dataset_path)
    if raw.ndim == 1:
        raw = raw.reshape(-1, 1)
    if raw.shape[1] < 2:
        raise ValueError(f"Invalid Feynman dataset columns (<2): {dataset_path}")
    if feynman_post_prune_steps is not None and int(feynman_post_prune_steps) < 0:
        raise ValueError("feynman_post_prune_steps must be >= 0 when provided.")
    if feynman_post_prune_eval_every is not None and int(feynman_post_prune_eval_every) <= 0:
        raise ValueError("feynman_post_prune_eval_every must be > 0 when provided.")
    if feynman_post_prune_patience is not None and int(feynman_post_prune_patience) <= 0:
        raise ValueError("feynman_post_prune_patience must be > 0 when provided.")
    if int(prune_iters) < 0:
        raise ValueError("prune_iters must be >= 0.")
    if feynman_fit_opt is not None and feynman_fit_opt not in _FEYNMAN_FIT_OPTS:
        raise ValueError(
            f"Unsupported feynman_fit_opt: {feynman_fit_opt}. Expected one of {list(_FEYNMAN_FIT_OPTS)}"
        )
    n_var = int(raw.shape[1] - 1)
    width = [n_var, *feynman_width_mid, 1]
    fit_opt = str(feynman_fit_opt) if feynman_fit_opt is not None else "Adam"

    post_prune_steps = int(feynman_post_prune_steps) if feynman_post_prune_steps is not None else 100
    post_prune_lr = float(feynman_post_prune_lr) if feynman_post_prune_lr is not None else 1e-3
    post_prune_lamb = float(feynman_post_prune_lamb) if feynman_post_prune_lamb is not None else 1e-3
    post_prune_eval_every = (
        int(feynman_post_prune_eval_every) if feynman_post_prune_eval_every is not None else 5
    )
    post_prune_min_delta = (
        float(feynman_post_prune_min_delta) if feynman_post_prune_min_delta is not None else 1e-6
    )
    post_prune_patience = int(feynman_post_prune_patience) if feynman_post_prune_patience is not None else 3

    return _TaskSpec(
        name=task_name,
        n_var=n_var,
        width=width,
        target_fn=None,
        lib=None,
        dataset_kind="feynman_file",
        dataset_path=str(dataset_path),
        dataset_variant=feynman_variant,
        dataset_split_strategy=feynman_split_strategy,
        dataset_split_seed=(int(feynman_split_strategy_seed) if feynman_split_strategy_seed is not None else None),
        dataset_filename=filename,
        dataset_total_rows=int(raw.shape[0]),
        dataset_total_columns=int(raw.shape[1]),
        target_formula=equations_map.get(filename),
        equation_metadata=dict(equations_metadata_map.get(filename, {})),
        teacher_max_test_mse=0.1,
        teacher_min_test_r2=None,
        teacher_grid=20,
        teacher_k=3,
        teacher_fit_opt=fit_opt,
        teacher_post_train_prune=True,
        teacher_prune_node_th=1e-2,
        teacher_prune_edge_th=1e-2,
        teacher_prune_iters=int(prune_iters),
        teacher_post_prune_steps=post_prune_steps,
        teacher_post_prune_lr=post_prune_lr,
        teacher_post_prune_lamb=post_prune_lamb,
        teacher_post_prune_early_stop=True,
        teacher_post_prune_eval_every=post_prune_eval_every,
        teacher_post_prune_min_delta=post_prune_min_delta,
        teacher_post_prune_patience=post_prune_patience,
    )


def _resolve_task_specs(
    *,
    tasks: list[str],
    feynman_root: Path,
    feynman_variant: str,
    feynman_width_mid: list[_WidthToken],
    feynman_split_strategy: str,
    feynman_split_strategy_seed: int | None,
    feynman_post_prune_steps: int | None,
    feynman_post_prune_lr: float | None,
    feynman_post_prune_lamb: float | None,
    feynman_post_prune_eval_every: int | None,
    feynman_post_prune_min_delta: float | None,
    feynman_post_prune_patience: int | None,
    prune_iters: int,
    feynman_fit_opt: str | None,
    feynman_max_datasets: int,
    feynman_dataset_select_seed: int,
    feynman_equations_csv: Path | None,
) -> tuple[list[str], dict[str, _TaskSpec], dict[str, str], dict[str, object]]:
    requested_tasks = _expand_feynman_task_tokens(
        tasks,
        feynman_root=feynman_root,
        feynman_variant=feynman_variant,
        feynman_max_datasets=feynman_max_datasets,
        feynman_dataset_select_seed=feynman_dataset_select_seed,
    )
    base_specs = _task_specs()

    needs_feynman = any(task.startswith("feynman_") for task in requested_tasks)
    if needs_feynman:
        if feynman_equations_csv is None:
            auto_path = feynman_root / "FeynmanEquations.csv"
            feynman_equations_csv = auto_path if auto_path.is_file() else None
        equations_map, equations_metadata_map, equations_metadata_columns = _load_feynman_equations_map(
            feynman_equations_csv
        )
    else:
        equations_map = {}
        equations_metadata_map = {}
        equations_metadata_columns = []

    resolved_specs: dict[str, _TaskSpec] = {}
    for task in requested_tasks:
        if task in base_specs:
            resolved_specs[task] = base_specs[task]
            continue
        if task.startswith("feynman_"):
            resolved_specs[task] = _build_feynman_task_spec(
                task_name=task,
                feynman_root=feynman_root,
                feynman_variant=feynman_variant,
                feynman_width_mid=feynman_width_mid,
                feynman_split_strategy=feynman_split_strategy,
                feynman_split_strategy_seed=feynman_split_strategy_seed,
                feynman_post_prune_steps=feynman_post_prune_steps,
                feynman_post_prune_lr=feynman_post_prune_lr,
                feynman_post_prune_lamb=feynman_post_prune_lamb,
                feynman_post_prune_eval_every=feynman_post_prune_eval_every,
                feynman_post_prune_min_delta=feynman_post_prune_min_delta,
                feynman_post_prune_patience=feynman_post_prune_patience,
                prune_iters=prune_iters,
                feynman_fit_opt=feynman_fit_opt,
                equations_map=equations_map,
                equations_metadata_map=equations_metadata_map,
            )
            continue
        raise ValueError(f"Unknown benchmark task: {task}")

    feynman_task_metadata: dict[str, dict[str, object]] = {}
    for task_name, spec in resolved_specs.items():
        if spec.dataset_kind != "feynman_file":
            continue
        feynman_task_metadata[task_name] = {
            "filename": spec.dataset_filename,
            "dataset_path": spec.dataset_path,
            "total_rows": spec.dataset_total_rows,
            "total_columns": spec.dataset_total_columns,
            "n_var": spec.n_var,
            "target_formula": spec.target_formula,
            "equation_metadata": dict(spec.equation_metadata or {}),
        }

    feynman_config: dict[str, object] = {
        "enabled": bool(needs_feynman),
        "root": str(feynman_root),
        "variant": feynman_variant,
        "equations_csv": str(feynman_equations_csv) if feynman_equations_csv is not None else None,
        "equations_metadata_columns": equations_metadata_columns,
        "split_strategy": feynman_split_strategy,
        "split_strategy_seed": (
            int(feynman_split_strategy_seed) if feynman_split_strategy_seed is not None else None
        ),
        "split_strategy_seed_policy": (
            "explicit_override" if feynman_split_strategy_seed is not None else "follow_benchmark_seed"
        ),
        "post_prune_overrides": {
            "steps": feynman_post_prune_steps,
            "lr": feynman_post_prune_lr,
            "lamb": feynman_post_prune_lamb,
            "eval_every": feynman_post_prune_eval_every,
            "min_delta": feynman_post_prune_min_delta,
            "patience": feynman_post_prune_patience,
        },
        "prune_iters": int(prune_iters),
        "fit_opt_override": feynman_fit_opt,
        "width_mid": _serialize_width_tokens(feynman_width_mid),
        "max_datasets": int(feynman_max_datasets),
        "dataset_select_seed": int(feynman_dataset_select_seed),
        "paper10_datasets": list(_FEYNMAN_PAPER10_DATASETS),
        "task_metadata": feynman_task_metadata,
    }
    return requested_tasks, resolved_specs, equations_map, feynman_config


def _build_teacher_dataset(
    spec: _TaskSpec,
    *,
    seed: int,
    train_num: int,
    test_num: int,
) -> dict[str, torch.Tensor]:
    _seed_everything(seed)
    if spec.dataset_kind == "feynman_file":
        if spec.dataset_path is None:
            raise ValueError(f"Feynman task '{spec.name}' is missing dataset_path.")
        return _load_local_feynman_dataset_as_kan(
            dataset_path=Path(spec.dataset_path),
            split_seed=int(_resolve_dataset_split_seed(spec, benchmark_seed=seed)),
            train_num=train_num,
            test_num=test_num,
            split_strategy=spec.dataset_split_strategy,
        )
    if spec.target_fn is None:
        raise ValueError(f"Synthetic task '{spec.name}' is missing target_fn.")
    return create_dataset(
        spec.target_fn,
        n_var=spec.n_var,
        ranges=spec.ranges if spec.ranges is not None else [-1, 1],
        train_num=train_num,
        test_num=test_num,
        seed=seed,
        device="cpu",
    )


def _build_teacher_model(spec: _TaskSpec, *, seed: int) -> MultKAN:
    return MultKAN(
        width=spec.width,
        grid=int(spec.teacher_grid),
        k=int(spec.teacher_k),
        seed=int(seed),
        auto_save=False,
        device="cpu",
    )


def _train_teacher_model(
    spec: _TaskSpec,
    dataset: dict[str, torch.Tensor],
    *,
    seed: int,
    train_steps: int,
    lr: float,
    lamb: float,
    quiet: bool = False,
) -> MultKAN:
    _seed_everything(seed)
    model = _build_teacher_model(spec, seed=seed)
    with _suppress_console_output(quiet):
        model.fit(
            dataset,
            opt=spec.teacher_fit_opt,
            steps=train_steps,
            lr=lr,
            update_grid=False,
            batch=-1,
            lamb=lamb,
            log=max(train_steps + 1, 999999),
        )

    def _prune_teacher_once(node_th: float, edge_th: float) -> MultKAN:
        with _suppress_console_output(quiet):
            pruned = model.prune_node(threshold=node_th, log_history=False)
            # prune_node creates a derived model with auto_save=True by default;
            # disable it to avoid benchmark-side checkpoint noise and side effects.
            pruned.auto_save = False
            pruned.forward(pruned.cache_data)
            pruned.attribute()
            pruned.prune_edge(threshold=edge_th, log_history=False)
        pruned.auto_save = False
        return pruned

    def _refit_teacher_once(post_prune_steps: int, post_prune_lr: float, post_prune_lamb: float) -> None:
        if post_prune_steps <= 0:
            return
        if bool(spec.teacher_post_prune_early_stop):
            eval_every = max(1, int(spec.teacher_post_prune_eval_every))
            patience = max(1, int(spec.teacher_post_prune_patience))
            min_delta = float(spec.teacher_post_prune_min_delta)
            remaining_steps = post_prune_steps
            prev_train_mse: float | None = None
            stable_checks = 0
            while remaining_steps > 0:
                chunk_steps = min(eval_every, remaining_steps)
                with _suppress_console_output(quiet):
                    model.fit(
                        dataset,
                        opt=spec.teacher_fit_opt,
                        steps=chunk_steps,
                        lr=post_prune_lr,
                        update_grid=False,
                        batch=-1,
                        lamb=post_prune_lamb,
                        log=max(chunk_steps + 1, 999999),
                    )
                remaining_steps -= chunk_steps
                with torch.no_grad():
                    train_pred = model(dataset["train_input"])
                    train_mse = float(
                        torch.mean((train_pred - dataset["train_label"]).pow(2)).item()
                    )
                if prev_train_mse is not None:
                    if abs(prev_train_mse - train_mse) <= min_delta:
                        stable_checks += 1
                    else:
                        stable_checks = 0
                prev_train_mse = train_mse
                if stable_checks >= patience:
                    break
        else:
            with _suppress_console_output(quiet):
                model.fit(
                    dataset,
                    opt=spec.teacher_fit_opt,
                    steps=post_prune_steps,
                    lr=post_prune_lr,
                    update_grid=False,
                    batch=-1,
                    lamb=post_prune_lamb,
                    log=max(post_prune_steps + 1, 999999),
                )

    if spec.teacher_post_train_prune:
        prune_iters = max(0, int(spec.teacher_prune_iters))
        post_prune_steps = int(spec.teacher_post_prune_steps)
        post_prune_lr = float(spec.teacher_post_prune_lr)
        post_prune_lamb = float(spec.teacher_post_prune_lamb)
        for _ in range(prune_iters):
            try:
                model = _prune_teacher_once(
                    float(spec.teacher_prune_node_th),
                    float(spec.teacher_prune_edge_th),
                )
            except Exception as prune_exc:
                warnings.warn(
                    f"Teacher prune failed for task={spec.name} with configured thresholds; "
                    f"falling back to no-threshold prune. error={prune_exc!r}",
                    RuntimeWarning,
                )
                try:
                    model = _prune_teacher_once(0.0, 0.0)
                except Exception as prune_fallback_exc:
                    warnings.warn(
                        f"Fallback prune also failed for task={spec.name}; keep current teacher model for refit. "
                        f"error={prune_fallback_exc!r}",
                        RuntimeWarning,
                    )
            # Keep benchmark loops side-effect free: disable checkpoint auto-save throughout tuning.
            model.auto_save = False
            _refit_teacher_once(post_prune_steps, post_prune_lr, post_prune_lamb)
    return model


def _build_teacher_cache_identity(
    *,
    spec: _TaskSpec,
    seed: int,
    train_num: int,
    test_num: int,
    train_steps: int,
    lr: float,
    lamb: float,
    profile_name: str,
    cache_version: str,
) -> tuple[str, dict[str, object]]:
    payload: dict[str, object] = {
        "task": spec.name,
        "seed": int(seed),
        "n_var": int(spec.n_var),
        "width": list(spec.width),
        "dataset_kind": spec.dataset_kind,
        "dataset_path": spec.dataset_path,
        "dataset_variant": spec.dataset_variant,
        "dataset_split_strategy": spec.dataset_split_strategy,
        "dataset_split_seed": _resolve_dataset_split_seed(spec, benchmark_seed=seed),
        "teacher_grid": int(spec.teacher_grid),
        "teacher_k": int(spec.teacher_k),
        "teacher_fit_opt": spec.teacher_fit_opt,
        "teacher_post_train_prune": bool(spec.teacher_post_train_prune),
        "teacher_prune_node_th": float(spec.teacher_prune_node_th),
        "teacher_prune_edge_th": float(spec.teacher_prune_edge_th),
        "teacher_prune_iters": int(spec.teacher_prune_iters),
        "teacher_post_prune_steps": int(spec.teacher_post_prune_steps),
        "teacher_post_prune_lr": float(spec.teacher_post_prune_lr),
        "teacher_post_prune_lamb": float(spec.teacher_post_prune_lamb),
        "teacher_post_prune_early_stop": bool(spec.teacher_post_prune_early_stop),
        "teacher_post_prune_eval_every": int(spec.teacher_post_prune_eval_every),
        "teacher_post_prune_min_delta": float(spec.teacher_post_prune_min_delta),
        "teacher_post_prune_patience": int(spec.teacher_post_prune_patience),
        "train_num": int(train_num),
        "test_num": int(test_num),
        "train_steps": int(train_steps),
        "lr": float(lr),
        "lamb": float(lamb),
        "profile": profile_name,
        "cache_version": cache_version,
    }
    serialized = json.dumps(payload, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    digest = hashlib.sha256(serialized.encode("utf-8")).hexdigest()[:16]
    return f"{spec.name}_seed{seed}_{digest}", payload


def _acquire_lock(lock_path: Path, *, timeout_s: float = 120.0) -> bool:
    start = time.perf_counter()
    while True:
        try:
            fd = os.open(str(lock_path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.close(fd)
            return True
        except FileExistsError:
            if (time.perf_counter() - start) >= timeout_s:
                return False
            time.sleep(0.1)


def _release_lock(lock_path: Path) -> None:
    try:
        lock_path.unlink()
    except FileNotFoundError:
        pass


def _write_json_atomic(path: Path, payload: dict[str, object]) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    tmp.replace(path)


def _write_torch_state_atomic(path: Path, state_dict: dict[str, torch.Tensor]) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    torch.save(state_dict, tmp)
    tmp.replace(path)


def _resolve_teacher_model_with_cache(
    *,
    spec: _TaskSpec,
    seed: int,
    train_num: int,
    test_num: int,
    train_steps: int,
    lr: float,
    lamb: float,
    profile_name: str,
    cache_dir: Path,
    cache_mode: str,
    cache_version: str,
    quiet: bool = False,
    lock_timeout_s: float = 120.0,
) -> tuple[MultKAN, dict[str, torch.Tensor], dict[str, object]]:
    if cache_mode not in _TEACHER_CACHE_MODES:
        raise ValueError(f"Unsupported teacher cache mode: {cache_mode}")

    dataset = _build_teacher_dataset(
        spec,
        seed=seed,
        train_num=train_num,
        test_num=test_num,
    )
    cache_key, cache_payload = _build_teacher_cache_identity(
        spec=spec,
        seed=seed,
        train_num=train_num,
        test_num=test_num,
        train_steps=train_steps,
        lr=lr,
        lamb=lamb,
        profile_name=profile_name,
        cache_version=cache_version,
    )

    cache_root = cache_dir / cache_key
    state_path = cache_root / "teacher_state.pt"
    meta_path = cache_root / "teacher_meta.json"
    lock_path = cache_root / "teacher_cache.lock"

    def _train() -> MultKAN:
        return _train_teacher_model(
            spec,
            dataset,
            seed=seed,
            train_steps=train_steps,
            lr=lr,
            lamb=lamb,
            quiet=quiet,
        )

    if cache_mode in {"readwrite", "readonly"} and state_path.exists() and meta_path.exists():
        try:
            model = _build_teacher_model(spec, seed=seed)
            state = torch.load(state_path, map_location="cpu")
            model.load_state_dict(state)
            return model, dataset, {
                "teacher_cache_hit": True,
                "teacher_cache_key": cache_key,
                "teacher_cache_path": str(cache_root),
                "teacher_cache_mode": cache_mode,
                "teacher_cache_status": "hit",
            }
        except Exception as exc:
            cache_load_error = f"{type(exc).__name__}: {exc}"
        else:  # pragma: no cover
            cache_load_error = ""
    else:
        cache_load_error = ""

    if cache_mode == "off":
        model = _train()
        return model, dataset, {
            "teacher_cache_hit": False,
            "teacher_cache_key": cache_key,
            "teacher_cache_path": str(cache_root),
            "teacher_cache_mode": cache_mode,
            "teacher_cache_status": "off_no_cache",
        }

    if cache_mode == "readonly":
        model = _train()
        status = "readonly_miss_no_write"
        if cache_load_error:
            status = f"readonly_load_error_no_write ({cache_load_error})"
        return model, dataset, {
            "teacher_cache_hit": False,
            "teacher_cache_key": cache_key,
            "teacher_cache_path": str(cache_root),
            "teacher_cache_mode": cache_mode,
            "teacher_cache_status": status,
        }

    model = _train()
    cache_root.mkdir(parents=True, exist_ok=True)
    lock_acquired = _acquire_lock(lock_path, timeout_s=lock_timeout_s)
    if lock_acquired:
        try:
            state_dict = {key: value.detach().cpu() for key, value in model.state_dict().items()}
            _write_torch_state_atomic(state_path, state_dict)
            _write_json_atomic(
                meta_path,
                {
                    "cache_key": cache_key,
                    "cache_payload": cache_payload,
                    "cache_mode_written_by": cache_mode,
                    "generated_at_utc": datetime.now(timezone.utc).isoformat(),
                },
            )
            status = "refresh_write" if cache_mode == "refresh" else "miss_write"
            if cache_load_error:
                status = f"{status}_after_load_error"
        finally:
            _release_lock(lock_path)
    else:
        status = "write_skipped_lock_timeout"
        if cache_load_error:
            status = f"{status}_after_load_error"

    return model, dataset, {
        "teacher_cache_hit": False,
        "teacher_cache_key": cache_key,
        "teacher_cache_path": str(cache_root),
        "teacher_cache_mode": cache_mode,
        "teacher_cache_status": status,
    }


def _serialize_formula_list(formulas: list[str]) -> str:
    return " || ".join(formulas)


def _deserialize_formula_list(serialized: object) -> list[str]:
    text = str(serialized).strip()
    if not text:
        return []
    return [item.strip() for item in text.split(" || ") if item.strip()]


def _parse_bool_text(value: object) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes"}


def _parse_float_text(value: object) -> float:
    text = str(value).strip()
    if not text:
        return float("nan")
    try:
        return float(text)
    except ValueError:
        return float("nan")


def _load_rows_for_replot(rows_csv: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    with rows_csv.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for raw in reader:
            row: dict[str, object] = {"task": str(raw.get("task", "")).strip()}
            for metric_name in _REPLOT_ROW_METRICS:
                row[metric_name] = _parse_float_text(raw.get(metric_name, ""))
            rows.append(row)
    return rows


def _load_variant_rows_for_replot(variant_rows_csv: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    with variant_rows_csv.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for raw in reader:
            row: dict[str, object] = {
                "task": str(raw.get("task", "")).strip(),
                "seed": _parse_float_text(raw.get("seed", "")),
                "variant": str(raw.get("variant", "")).strip(),
            }
            for metric_name in _REPLOT_VARIANT_METRICS:
                row[metric_name] = _parse_float_text(raw.get(metric_name, ""))
            rows.append(row)
    return rows


def _rewrite_visualization_summary_markdown(
    *,
    summary_md_path: Path,
    visualization: dict[str, object],
    output_dir: Path,
) -> None:
    if not summary_md_path.exists():
        return
    text = summary_md_path.read_text(encoding="utf-8")
    start_marker = "## Visualization Summary"
    end_marker = "## Visualization Design Guide"
    if start_marker not in text or end_marker not in text:
        return

    section_lines = [start_marker, ""]
    if bool(visualization.get("enabled")):
        for path in list(visualization.get("files", [])):
            rel = str(Path(path).relative_to(output_dir))
            section_lines.append(f"- `{rel}`")
    else:
        section_lines.append(f"- Visualization disabled: {visualization.get('error')}")
    section_lines.append("")
    replacement = "\n".join(section_lines)

    prefix, tail = text.split(start_marker, maxsplit=1)
    _, suffix = tail.split(end_marker, maxsplit=1)
    summary_md_path.write_text(prefix + replacement + end_marker + suffix, encoding="utf-8")


def _replot_visualizations_from_artifacts(
    *,
    summary_json_path: Path,
    rows_csv: Path,
    variant_rows_csv: Path,
    output_dir: Path,
) -> dict[str, object]:
    summary = json.loads(summary_json_path.read_text(encoding="utf-8"))
    rows = _load_rows_for_replot(rows_csv)
    variant_rows = _load_variant_rows_for_replot(variant_rows_csv)

    tasks = list(summary.get("config", {}).get("tasks", []))
    if not tasks:
        tasks = sorted({str(row["task"]) for row in rows if str(row["task"])})
    variants = list(summary.get("config", {}).get("variants", []))
    if not variants:
        variants = sorted({str(row["variant"]) for row in variant_rows if str(row["variant"])})
    by_task_rows = {task: [row for row in rows if str(row["task"]) == task] for task in tasks}

    visualization = _generate_visualizations(
        output_dir=output_dir,
        tasks=tasks,
        by_task_rows=by_task_rows,
        variant_rows=variant_rows,
        variants=variants,
    )
    summary.setdefault("artifacts", {})["visualizations"] = visualization
    summary.setdefault("metadata", {})["last_replot_utc"] = datetime.now(timezone.utc).isoformat()
    summary_json_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    _rewrite_visualization_summary_markdown(
        summary_md_path=output_dir / "icbr_benchmark_summary.md",
        visualization=visualization,
        output_dir=output_dir,
    )
    return {
        "summary": summary,
        "visualization": visualization,
        "output_dir": str(output_dir),
    }


def _compute_target_mse_and_r2(prediction: torch.Tensor, target: torch.Tensor) -> tuple[float, float]:
    mse = float(torch.mean((prediction - target).pow(2)).item())
    target_centered = target - torch.mean(target, dim=0, keepdim=True)
    ss_tot = float(torch.sum(target_centered.pow(2)).item())
    if ss_tot <= 1e-12:
        return mse, float("nan")
    ss_res = float(torch.sum((prediction - target).pow(2)).item())
    r2 = 1.0 - (ss_res / ss_tot)
    return mse, float(r2)


def _build_teacher_quality_gate_result(
    *,
    teacher_test_mse: float,
    teacher_test_r2: float,
    max_test_mse: float | None,
    min_test_r2: float | None,
) -> tuple[bool, str]:
    gate_failures: list[str] = []
    if max_test_mse is not None and (not math.isfinite(teacher_test_mse) or teacher_test_mse > max_test_mse):
        gate_failures.append(f"teacher_test_mse={teacher_test_mse:.6g} > {max_test_mse:.6g}")
    if min_test_r2 is not None and (not math.isfinite(teacher_test_r2) or teacher_test_r2 < min_test_r2):
        gate_failures.append(f"teacher_test_r2={teacher_test_r2:.6g} < {min_test_r2:.6g}")
    if gate_failures:
        return False, "; ".join(gate_failures)
    return True, ""


def _build_skipped_symbolic_metrics(*, reason: str) -> dict[str, object]:
    nan_metrics = {
        "candidate_generation_wall_time_s": float("nan"),
        "replay_rerank_wall_time_s": float("nan"),
        "symbolic_wall_time_s": float("nan"),
        "baseline_symbolic_wall_time_s": float("nan"),
        "symbolic_wall_time_delta_s": float("nan"),
        "symbolic_speedup_vs_baseline": float("nan"),
        "replay_imitation_gap": float("nan"),
        "final_mse_loss_shift": float("nan"),
        "baseline_mse": float("nan"),
        "icbr_mse": float("nan"),
        "teacher_target_mse": float("nan"),
        "teacher_target_r2": float("nan"),
        "baseline_target_mse": float("nan"),
        "baseline_target_r2": float("nan"),
        "icbr_target_mse": float("nan"),
        "icbr_target_r2": float("nan"),
        "symbolic_target_mse_shift": float("nan"),
        "symbolic_target_r2_shift": float("nan"),
    }
    return {
        **nan_metrics,
        "formula_validation_result": False,
        "baseline_formula_validation_result": False,
        "icbr_formula_validation_result": False,
        "baseline_formula_raw": [],
        "baseline_formula_display": [],
        "icbr_formula_raw": [],
        "icbr_formula_display": [],
        "baseline_formula_error": f"skipped_by_teacher_quality_gate: {reason}",
        "icbr_formula_error": f"skipped_by_teacher_quality_gate: {reason}",
    }


def _build_legacy_metrics_from_variant_bundle(bundle: dict[str, object]) -> dict[str, object]:
    baseline = bundle["baseline"]
    variants = bundle["variants"]
    comparisons = bundle["comparisons_vs_baseline"]
    icbr = variants["icbr_full"]
    cmp = comparisons["icbr_full"]
    return {
        "candidate_generation_wall_time_s": float(icbr["candidate_generation_wall_time_s"]),
        "replay_rerank_wall_time_s": float(icbr["replay_rerank_wall_time_s"]),
        "symbolic_wall_time_s": float(icbr["symbolic_wall_time_s"]),
        "baseline_symbolic_wall_time_s": float(baseline["symbolic_wall_time_s"]),
        "symbolic_wall_time_delta_s": float(cmp["symbolic_wall_time_delta_s"]),
        "symbolic_speedup_vs_baseline": float(cmp["symbolic_speedup_vs_baseline"]),
        "replay_imitation_gap": float(cmp["replay_imitation_gap"]),
        "final_mse_loss_shift": float(cmp["final_mse_loss_shift"]),
        "formula_validation_result": bool(cmp["formula_validation_result"]),
        "baseline_formula_validation_result": bool(baseline["formula_validation_result"]),
        "icbr_formula_validation_result": bool(icbr["formula_validation_result"]),
        "baseline_formula_raw": list(baseline["formula_raw"]),
        "baseline_formula_display": list(baseline["formula_display"]),
        "icbr_formula_raw": list(icbr["formula_raw"]),
        "icbr_formula_display": list(icbr["formula_display"]),
        "baseline_formula_error": baseline["formula_error"],
        "icbr_formula_error": icbr["formula_error"],
        "baseline_mse": float(baseline["mse"]),
        "icbr_mse": float(icbr["mse"]),
        "teacher_target_mse": float(bundle["teacher_target_mse"]),
        "teacher_target_r2": float(bundle["teacher_target_r2"]),
        "baseline_target_mse": float(baseline["target_mse"]),
        "baseline_target_r2": float(baseline["target_r2"]),
        "icbr_target_mse": float(icbr["target_mse"]),
        "icbr_target_r2": float(icbr["target_r2"]),
        "symbolic_target_mse_shift": float(cmp["symbolic_target_mse_shift"]),
        "symbolic_target_r2_shift": float(cmp["symbolic_target_r2_shift"]),
    }


def _build_variant_rows_for_task_seed(
    *,
    task: str,
    seed: int,
    variant_bundle: dict[str, object],
    variants_requested: list[str],
    teacher_quality_gate_pass: bool,
    teacher_quality_gate_reason: str,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    baseline = variant_bundle["baseline"]
    variants = variant_bundle["variants"]
    comparisons = variant_bundle["comparisons_vs_baseline"]
    baseline_row = {
        "task": task,
        "seed": seed,
        "variant": "baseline",
        "variant_requested": bool("baseline" in variants_requested),
        "candidate_mode": "baseline",
        "rerank_mode": "baseline",
        "commit_mode": "baseline",
        "teacher_quality_gate_pass": bool(teacher_quality_gate_pass),
        "teacher_quality_gate_reason": teacher_quality_gate_reason,
        "candidate_generation_wall_time_s": float("nan"),
        "replay_rerank_wall_time_s": float("nan"),
        "symbolic_wall_time_s": float(baseline["symbolic_wall_time_s"]),
        "mse": float(baseline["mse"]),
        "target_mse": float(baseline["target_mse"]),
        "target_r2": float(baseline["target_r2"]),
        "formula_validation_result": bool(baseline["formula_validation_result"]),
        "formula_raw": list(baseline["formula_raw"]),
        "formula_display": list(baseline["formula_display"]),
        "formula_error": baseline["formula_error"],
        "replay_rank_inversion_count": float("nan"),
        "replay_rank_inversion_total": float("nan"),
        "replay_rank_inversion_rate": float("nan"),
        "commit_param_drift_l2_mean": float("nan"),
        "commit_param_drift_l2_max": float("nan"),
        "baseline_symbolic_wall_time_s": float(baseline["symbolic_wall_time_s"]),
        "baseline_mse": float(baseline["mse"]),
        "baseline_target_mse": float(baseline["target_mse"]),
        "baseline_target_r2": float(baseline["target_r2"]),
        "symbolic_wall_time_delta_s": 0.0,
        "symbolic_speedup_vs_baseline": 1.0,
        "final_mse_loss_shift": 0.0,
        "symbolic_target_mse_shift": 0.0,
        "symbolic_target_r2_shift": 0.0,
    }
    rows.append(baseline_row)
    for variant_name, variant in variants.items():
        cmp = comparisons.get(variant_name, {})
        rows.append(
            {
                "task": task,
                "seed": seed,
                "variant": variant_name,
                "variant_requested": bool(variant_name in variants_requested),
                "candidate_mode": variant.get("candidate_mode"),
                "rerank_mode": variant.get("rerank_mode"),
                "commit_mode": variant.get("commit_mode"),
                "teacher_quality_gate_pass": bool(teacher_quality_gate_pass),
                "teacher_quality_gate_reason": teacher_quality_gate_reason,
                "candidate_generation_wall_time_s": float(variant["candidate_generation_wall_time_s"]),
                "replay_rerank_wall_time_s": float(variant["replay_rerank_wall_time_s"]),
                "symbolic_wall_time_s": float(variant["symbolic_wall_time_s"]),
                "mse": float(variant["mse"]),
                "target_mse": float(variant["target_mse"]),
                "target_r2": float(variant["target_r2"]),
                "formula_validation_result": bool(variant["formula_validation_result"]),
                "formula_raw": list(variant["formula_raw"]),
                "formula_display": list(variant["formula_display"]),
                "formula_error": variant["formula_error"],
                "replay_rank_inversion_count": int(variant["replay_rank_inversion_count"]),
                "replay_rank_inversion_total": int(variant["replay_rank_inversion_total"]),
                "replay_rank_inversion_rate": float(variant["replay_rank_inversion_rate"]),
                "commit_param_drift_l2_mean": float(variant["commit_param_drift_l2_mean"]),
                "commit_param_drift_l2_max": float(variant["commit_param_drift_l2_max"]),
                "baseline_symbolic_wall_time_s": float(baseline["symbolic_wall_time_s"]),
                "baseline_mse": float(baseline["mse"]),
                "baseline_target_mse": float(baseline["target_mse"]),
                "baseline_target_r2": float(baseline["target_r2"]),
                "symbolic_wall_time_delta_s": float(cmp.get("symbolic_wall_time_delta_s", float("nan"))),
                "symbolic_speedup_vs_baseline": float(cmp.get("symbolic_speedup_vs_baseline", float("nan"))),
                "final_mse_loss_shift": float(cmp.get("final_mse_loss_shift", float("nan"))),
                "symbolic_target_mse_shift": float(cmp.get("symbolic_target_mse_shift", float("nan"))),
                "symbolic_target_r2_shift": float(cmp.get("symbolic_target_r2_shift", float("nan"))),
            }
        )
    return rows


def _build_skipped_variant_rows_for_task_seed(
    *,
    task: str,
    seed: int,
    variants_requested: list[str],
    reason: str,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for variant_name in variants_requested:
        rows.append(
            {
                "task": task,
                "seed": seed,
                "variant": variant_name,
                "variant_requested": True,
                "candidate_mode": "skipped_by_teacher_quality_gate",
                "rerank_mode": "skipped_by_teacher_quality_gate",
                "commit_mode": "skipped_by_teacher_quality_gate",
                "teacher_quality_gate_pass": False,
                "teacher_quality_gate_reason": reason,
                "candidate_generation_wall_time_s": float("nan"),
                "replay_rerank_wall_time_s": float("nan"),
                "symbolic_wall_time_s": float("nan"),
                "mse": float("nan"),
                "target_mse": float("nan"),
                "target_r2": float("nan"),
                "formula_validation_result": False,
                "formula_raw": [],
                "formula_display": [],
                "formula_error": f"skipped_by_teacher_quality_gate: {reason}",
                "replay_rank_inversion_count": float("nan"),
                "replay_rank_inversion_total": float("nan"),
                "replay_rank_inversion_rate": float("nan"),
                "commit_param_drift_l2_mean": float("nan"),
                "commit_param_drift_l2_max": float("nan"),
                "baseline_symbolic_wall_time_s": float("nan"),
                "baseline_mse": float("nan"),
                "baseline_target_mse": float("nan"),
                "baseline_target_r2": float("nan"),
                "symbolic_wall_time_delta_s": float("nan"),
                "symbolic_speedup_vs_baseline": float("nan"),
                "final_mse_loss_shift": float("nan"),
                "symbolic_target_mse_shift": float("nan"),
                "symbolic_target_r2_shift": float("nan"),
            }
        )
    return rows


def _build_variant_metric_stats(rows: list[dict[str, object]]) -> dict[str, dict[str, float]]:
    stats: dict[str, dict[str, float]] = {}
    for metric in _VARIANT_NUMERIC_METRICS:
        values: list[float] = []
        for row in rows:
            value = float(row[metric])
            if math.isfinite(value):
                values.append(value)
        stats[metric] = _describe(values)
    for metric in _VARIANT_BOOLEAN_METRICS:
        values = [1.0 if bool(row[metric]) else 0.0 for row in rows]
        stats[metric] = _describe(values)
    return stats


def _build_challenge_evidence_stats(rows: list[dict[str, object]]) -> dict[str, dict[str, float]]:
    stats: dict[str, dict[str, float]] = {}
    for metric in _CHALLENGE_EVIDENCE_METRICS:
        values: list[float] = []
        for row in rows:
            value = float(row[metric])
            if math.isfinite(value):
                values.append(value)
        stats[metric] = _describe(values)
    return stats

def _describe(values: list[float]) -> dict[str, float]:
    if not values:
        return {
            "count": 0.0,
            "mean": float("nan"),
            "median": float("nan"),
            "std": float("nan"),
            "min": float("nan"),
            "max": float("nan"),
        }
    return {
        "count": float(len(values)),
        "mean": float(statistics.mean(values)),
        "median": float(statistics.median(values)),
        "std": float(statistics.stdev(values)) if len(values) > 1 else 0.0,
        "min": float(min(values)),
        "max": float(max(values)),
    }


def _bootstrap_mean_ci(
    values: list[float],
    *,
    iterations: int = 2000,
    alpha: float = 0.05,
    seed: int = 0,
) -> tuple[float, float]:
    if not values:
        return float("nan"), float("nan")

    rng = random.Random(seed)
    n = len(values)
    bootstrap_means: list[float] = []
    for _ in range(iterations):
        sample = [values[rng.randrange(n)] for _ in range(n)]
        bootstrap_means.append(float(statistics.mean(sample)))
    bootstrap_means.sort()

    lower_idx = int((alpha / 2.0) * (iterations - 1))
    upper_idx = int((1.0 - alpha / 2.0) * (iterations - 1))
    return bootstrap_means[lower_idx], bootstrap_means[upper_idx]


def _sign_test_pvalue_two_sided(successes: int, total: int) -> float:
    if total <= 0:
        return float("nan")
    tail_count = sum(math.comb(total, k) for k in range(0, min(successes, total - successes) + 1))
    return float(min(1.0, 2.0 * tail_count / (2**total)))


def _build_metric_stats(rows: list[dict[str, object]]) -> dict[str, dict[str, float]]:
    stats: dict[str, dict[str, float]] = {}
    for metric in _NUMERIC_METRICS:
        values = []
        for row in rows:
            value = float(row[metric])
            if math.isfinite(value):
                values.append(value)
        stats[metric] = _describe(values)
    for metric in _BOOLEAN_METRICS:
        values = [1.0 if bool(row[metric]) else 0.0 for row in rows]
        stats[metric] = _describe(values)
    return stats


def _build_significance(
    rows: list[dict[str, object]],
    *,
    task_label: str,
) -> dict[str, dict[str, float | int | str | list[float]]]:
    by_metric: dict[str, dict[str, float | int | str | list[float]]] = {}
    for metric_name, favorable_direction in _SIGNIFICANCE_DIRECTIONS.items():
        deltas = []
        for row in rows:
            value = float(row[metric_name])
            if math.isfinite(value):
                deltas.append(value)
        effective = [value for value in deltas if abs(value) > 1e-12]
        tie_count = len(deltas) - len(effective)

        if favorable_direction == "positive":
            improved_count = sum(1 for value in effective if value > 0.0)
        else:
            improved_count = sum(1 for value in effective if value < 0.0)
        worsened_count = len(effective) - improved_count

        ci_seed = sum(ord(ch) for ch in f"{task_label}:{metric_name}") + len(deltas) * 97
        ci_low, ci_high = _bootstrap_mean_ci(deltas, seed=ci_seed)
        p_value = _sign_test_pvalue_two_sided(improved_count, len(effective))

        by_metric[metric_name] = {
            "favorable_direction": favorable_direction,
            "sample_count": len(rows),
            "finite_count": len(deltas),
            "effective_count": len(effective),
            "tie_count": tie_count,
            "improved_count": improved_count,
            "worsened_count": worsened_count,
            "delta_stats": _describe(deltas),
            "mean_delta_ci95": [float(ci_low), float(ci_high)],
            "sign_test_pvalue_two_sided": float(p_value),
        }
    return by_metric


def _build_task_stats_rows(
    *,
    tasks: list[str],
    rows: list[dict[str, object]],
    by_task_metrics: dict[str, dict[str, dict[str, float]]],
    overall_metrics: dict[str, dict[str, float]],
) -> list[dict[str, object]]:
    stats_rows: list[dict[str, object]] = []
    for metric_name, metric_stats in overall_metrics.items():
        stats_rows.append(
            {
                "scope": "overall",
                "task": "__all__",
                "metric": metric_name,
                **metric_stats,
            }
        )
    for task in tasks:
        task_rows = [row for row in rows if row["task"] == task]
        for metric_name, metric_stats in by_task_metrics[task].items():
            stats_rows.append(
                {
                    "scope": "task",
                    "task": task,
                    "metric": metric_name,
                    "seed_count": len(task_rows),
                    **metric_stats,
                }
            )
    return stats_rows


def _build_significance_rows(
    *,
    tasks: list[str],
    by_task_significance: dict[str, dict[str, dict[str, float | int | str | list[float]]]],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for task in tasks:
        task_sig = by_task_significance[task]
        for metric_name, item in task_sig.items():
            ci = item["mean_delta_ci95"]
            rows.append(
                {
                    "task": task,
                    "metric": metric_name,
                    "favorable_direction": item["favorable_direction"],
                    "sample_count": item["sample_count"],
                    "finite_count": item["finite_count"],
                    "effective_count": item["effective_count"],
                    "tie_count": item["tie_count"],
                    "improved_count": item["improved_count"],
                    "worsened_count": item["worsened_count"],
                    "mean_delta": item["delta_stats"]["mean"],
                    "median_delta": item["delta_stats"]["median"],
                    "std_delta": item["delta_stats"]["std"],
                    "min_delta": item["delta_stats"]["min"],
                    "max_delta": item["delta_stats"]["max"],
                    "mean_delta_ci95_low": ci[0],
                    "mean_delta_ci95_high": ci[1],
                    "sign_test_pvalue_two_sided": item["sign_test_pvalue_two_sided"],
                }
            )
    return rows


def _write_task_stats_csv(
    path: Path,
    stats_rows: list[dict[str, object]],
) -> None:
    fieldnames = [
        "scope",
        "task",
        "metric",
        "seed_count",
        "count",
        "mean",
        "median",
        "std",
        "min",
        "max",
    ]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in stats_rows:
            writer.writerow({name: row.get(name, "") for name in fieldnames})


def _write_significance_csv(
    path: Path,
    significance_rows: list[dict[str, object]],
) -> None:
    if not significance_rows:
        return
    fieldnames = list(significance_rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(significance_rows)


def _generate_visualizations(
    *,
    output_dir: Path,
    tasks: list[str],
    by_task_rows: dict[str, list[dict[str, object]]],
    variant_rows: list[dict[str, object]],
    variants: list[str],
) -> dict[str, object]:
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from matplotlib import ticker
    except Exception as exc:  # pragma: no cover - depends on local matplotlib availability
        return {"enabled": False, "error": f"{type(exc).__name__}: {exc}", "files": []}

    style = _VISUALIZATION_STYLE
    created_files: list[str] = []
    plot_metadata: dict[str, dict[str, object]] = {}
    warnings_list: list[str] = []

    rc_params = {
        "font.family": style.font_family,
        "font.size": style.base_font_size,
        "axes.titlesize": style.title_font_size,
        "axes.labelsize": style.base_font_size,
        "xtick.labelsize": style.tick_font_size,
        "ytick.labelsize": style.tick_font_size,
        "axes.edgecolor": style.spine_color,
        "axes.labelcolor": style.text_color,
        "axes.facecolor": style.axes_facecolor,
        "figure.facecolor": style.figure_facecolor,
        "text.color": style.text_color,
        "xtick.color": style.text_color,
        "ytick.color": style.text_color,
        "grid.color": style.grid_color,
        "grid.alpha": style.grid_alpha,
        "grid.linewidth": style.grid_linewidth,
        "legend.frameon": True,
        "legend.fancybox": False,
    }

    with plt.rc_context(rc=rc_params):
        def _finite_metric_values(task: str, metric: str) -> list[float]:
            values: list[float] = []
            for row in by_task_rows.get(task, []):
                value = float(row.get(metric, float("nan")))
                if math.isfinite(value):
                    values.append(value)
            return values

        def _safe_mean_ci95(values: list[float]) -> tuple[float, float]:
            if not values:
                return float("nan"), float("nan")
            if len(values) == 1:
                return float(values[0]), 0.0
            mean = float(statistics.mean(values))
            std = float(statistics.stdev(values))
            ci95 = style.ci_multiplier * std / math.sqrt(len(values))
            return mean, float(ci95)

        def _safe_log_metric_ci95(values: list[float], *, log_base: float = math.e) -> tuple[float, float, float]:
            positive_values = [value for value in values if math.isfinite(value) and value > 0.0]
            if not positive_values:
                return float("nan"), float("nan"), float("nan")
            if len(positive_values) == 1:
                value = float(positive_values[0])
                return value, value, value
            logs = [math.log(value, log_base) for value in positive_values]
            mean_log = float(statistics.mean(logs))
            std_log = float(statistics.stdev(logs))
            ci95_log = style.ci_multiplier * std_log / math.sqrt(len(logs))
            center = log_base ** mean_log
            low = log_base ** (mean_log - ci95_log)
            high = log_base ** (mean_log + ci95_log)
            return float(center), float(low), float(high)

        def _safe_log2_ratio_ci95(values: list[float]) -> tuple[float, float]:
            positive_values = [value for value in values if math.isfinite(value) and value > 0.0]
            if not positive_values:
                return float("nan"), float("nan")
            log_values = [math.log(value, 2.0) for value in positive_values]
            return _safe_mean_ci95(log_values)

        def _canonical_scale_name(scale: str) -> str:
            if scale.startswith("symlog"):
                return "symlog"
            return scale

        def _badge_scale_name(scale: str) -> str:
            canonical = _canonical_scale_name(scale)
            if canonical in {"log", "symlog"}:
                return "log"
            return canonical

        def _format_scale_badge(scale: str) -> str:
            return f"scale={_badge_scale_name(scale)}"

        def _format_scale_suffix(scale: str) -> str:
            canonical = _canonical_scale_name(scale)
            if canonical == "log2_ratio":
                return "log2-ratio scale"
            return f"{canonical} scale"

        def _with_scale_ylabel(base_label: str, scale: str) -> str:
            return f"{base_label} ({_format_scale_suffix(scale)})"

        def _apply_axes_style(ax, *, title: str, ylabel: str) -> None:
            ax.set_title(title, pad=10.0)
            ax.set_ylabel(ylabel)
            ax.grid(axis="y", linestyle="-", alpha=style.grid_alpha)
            ax.set_axisbelow(True)
            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)
            ax.spines["left"].set_color(style.spine_color)
            ax.spines["bottom"].set_color(style.spine_color)

        def _style_legend_frame(legend) -> None:
            if legend is None:
                return
            legend.get_frame().set_facecolor(style.legend_facecolor)
            legend.get_frame().set_edgecolor(style.legend_edgecolor)
            legend.get_frame().set_alpha(0.95)

        def _style_legend(
            ax,
            *,
            loc: str = "best",
            bbox_to_anchor: tuple[float, float] | None = None,
            ncol: int = 1,
        ) -> None:
            legend = ax.legend(loc=loc, bbox_to_anchor=bbox_to_anchor, ncol=ncol, borderaxespad=0.0)
            if legend is None:
                return
            _style_legend_frame(legend)

        def _add_axis_scale_badge(ax, scale: str) -> None:
            ax.set_title(
                _format_scale_badge(scale),
                loc="left",
                pad=10.0,
                fontsize=style.annotation_font_size,
                color=style.text_color,
            )

        def _maybe_add_axis_scale_badge(ax, scale: str) -> None:
            if _canonical_scale_name(scale) == "linear":
                return
            _add_axis_scale_badge(ax, scale)

        def _build_note_lines(*, summary_line: str, measure_line: str, extra_line: str | None = None) -> list[str]:
            lines = [f"Stats: {summary_line}", f"Measure: {measure_line}"]
            if extra_line:
                lines.append(extra_line)
            return lines

        def _add_figure_note(fig, lines: list[str]) -> None:
            fig.text(
                0.015,
                0.02,
                "\n".join(lines),
                ha="left",
                va="bottom",
                fontsize=style.annotation_font_size,
                bbox={
                    "boxstyle": "round,pad=0.35",
                    "facecolor": style.note_facecolor,
                    "edgecolor": style.note_edgecolor,
                    "alpha": 0.96,
                },
            )

        def _apply_value_axis(ax, values: list[float], *, floor: float | None = None) -> None:
            finite_values = [value for value in values if math.isfinite(value)]
            if not finite_values:
                return
            current_floor = min(finite_values) if floor is None else min(floor, min(finite_values))
            current_ceiling = max(finite_values)
            if ax.get_yscale() == "log":
                positive_values = [value for value in finite_values if value > 0.0]
                if not positive_values:
                    return
                lower = min(positive_values)
                upper = max(positive_values)
                span_ratio = max(upper / max(lower, 1e-12), 1.0001)
                ax.set_ylim(lower / (span_ratio ** 0.08), upper * (span_ratio ** 0.10))
                return
            if current_floor == current_ceiling:
                padding = max(abs(current_floor) * 0.15, 1e-6)
                ax.set_ylim(current_floor - padding, current_ceiling + padding)
                return
            span = current_ceiling - current_floor
            ax.set_ylim(current_floor - span * 0.12, current_ceiling + span * 0.18)

        def _apply_time_axis(ax, values: list[float]) -> str:
            positive = [value for value in values if math.isfinite(value) and value > 0.0]
            if not positive:
                return "linear"
            spread_ratio = max(positive) / max(min(positive), 1e-12)
            if len(positive) >= 2 and spread_ratio >= 6.0:
                ax.set_yscale("log")
                ax.set_ylim(min(positive) / 1.25, max(positive) * 1.35)
                return "log"
            _apply_value_axis(ax, positive)
            return "linear"

        def _apply_log_tick_mathtext(ax) -> None:
            ax.yaxis.set_major_locator(ticker.LogLocator(base=10.0))
            ax.yaxis.set_major_formatter(ticker.LogFormatterMathtext(base=10.0))
            ax.yaxis.set_minor_locator(ticker.LogLocator(base=10.0, subs=np.arange(2, 10) * 0.1))
            ax.yaxis.set_minor_formatter(ticker.NullFormatter())

        def _thin_y_major_ticks(
            ax,
            ticks: list[float],
            *,
            preferred_ticks: list[float] | None = None,
            min_pixel_gap: float = 26.0,
        ) -> list[float]:
            visible_min, visible_max = sorted(ax.get_ylim())
            visible_ticks = [
                float(tick)
                for tick in ticks
                if math.isfinite(tick) and visible_min * 0.999 <= tick <= visible_max * 1.001
            ]
            if len(visible_ticks) <= 1:
                return visible_ticks
            ax.figure.canvas.draw()
            preferred_keys = {round(float(tick), 12) for tick in (preferred_ticks or [])}
            positions = {
                tick: float(ax.transData.transform((0.0, tick))[1])
                for tick in visible_ticks
            }
            ordered_ticks = sorted(visible_ticks, key=lambda tick: positions[tick])
            kept_ticks: list[float] = [ordered_ticks[0]]
            for idx, tick in enumerate(ordered_ticks[1:], start=1):
                is_last = idx == len(ordered_ticks) - 1
                is_preferred = round(tick, 12) in preferred_keys
                gap = positions[tick] - positions[kept_ticks[-1]]
                if gap >= min_pixel_gap:
                    kept_ticks.append(tick)
                    continue
                if is_preferred and round(kept_ticks[-1], 12) not in preferred_keys:
                    kept_ticks[-1] = tick
                    continue
                if is_last and round(kept_ticks[-1], 12) not in preferred_keys:
                    kept_ticks[-1] = tick
            if round(ordered_ticks[-1], 12) not in {round(tick, 12) for tick in kept_ticks}:
                if len(kept_ticks) >= 2:
                    previous_tick = kept_ticks[-2]
                    if positions[ordered_ticks[-1]] - positions[previous_tick] >= min_pixel_gap:
                        kept_ticks[-1] = ordered_ticks[-1]
                else:
                    kept_ticks.append(ordered_ticks[-1])
            return sorted({float(round(tick, 12)) for tick in kept_ticks})

        def _format_ratio_tick(value: float, _position: float | None = None) -> str:
            if not math.isfinite(value) or value <= 0.0:
                return ""
            if math.isclose(value, 1.0, rel_tol=1e-9, abs_tol=1e-12):
                return "1"
            if math.isclose(value, round(value), rel_tol=1e-9, abs_tol=1e-12):
                return str(int(round(value)))
            if 1e-3 <= value <= 1e4:
                return f"{value:.4g}"
            if value >= 10.0 or value < 0.1:
                return f"{value:.0e}".replace("e+0", "e").replace("e+", "e").replace("e-0", "e-")
            return f"{value:.3g}"

        def _build_ratio_ticks(lower: float, upper: float, *, baseline: float = 1.0) -> list[float]:
            if not math.isfinite(lower) or not math.isfinite(upper) or lower <= 0.0 or upper <= 0.0:
                return []
            if lower >= upper:
                return [lower]

            span_ratio = upper / lower
            ticks: list[float] = []
            if span_ratio <= 3.5:
                if lower < baseline < upper:
                    lower_mid = math.sqrt(lower * baseline)
                    upper_mid = math.sqrt(baseline * upper)
                    ticks = [lower, lower_mid, baseline, upper_mid, upper]
                else:
                    ticks = list(np.geomspace(lower, upper, num=5))
            else:
                min_exp = int(math.floor(math.log10(lower))) - 1
                max_exp = int(math.ceil(math.log10(upper))) + 1
                preferred = (1.0, 2.0, 5.0)
                for exp in range(min_exp, max_exp + 1):
                    scale = 10.0**exp
                    for mult in preferred:
                        candidate = mult * scale
                        if lower * 0.999 <= candidate <= upper * 1.001:
                            ticks.append(candidate)
                if lower < baseline < upper:
                    ticks.append(baseline)
                if not ticks:
                    ticks = list(np.geomspace(lower, upper, num=5))

            deduped = sorted(
                {
                    float(round(tick, 12))
                    for tick in ticks
                    if math.isfinite(tick) and lower * 0.999 <= tick <= upper * 1.001 and tick > 0.0
                }
            )
            return deduped

        def _apply_ratio_axis(
            ax,
            values: list[float],
            *,
            baseline: float = 1.0,
            include_baseline_in_limits: bool = True,
        ) -> str:
            positive = [value for value in values if math.isfinite(value) and value > 0.0]
            if not positive:
                return "linear"
            ax.set_yscale("log")
            limit_values = positive + [baseline] if include_baseline_in_limits else positive
            lower_raw = min(limit_values)
            upper_raw = max(limit_values)
            span_ratio = max(upper_raw / max(lower_raw, 1e-12), 1.0001)
            lower = lower_raw / (span_ratio ** 0.025)
            upper = upper_raw * (span_ratio ** 0.035)
            ax.set_ylim(lower, upper)
            ratio_ticks = _build_ratio_ticks(lower, upper, baseline=baseline)
            if ratio_ticks:
                ratio_ticks = _thin_y_major_ticks(ax, ratio_ticks, preferred_ticks=[baseline])
                ax.yaxis.set_major_locator(ticker.FixedLocator(ratio_ticks))
                ax.yaxis.set_major_formatter(ticker.FuncFormatter(_format_ratio_tick))
                ax.yaxis.set_minor_locator(ticker.NullLocator())
            else:
                _apply_log_tick_mathtext(ax)
            return "log"

        def _apply_symlog_axis(ax, values: list[float]) -> str:
            finite_nonzero = [value for value in values if math.isfinite(value) and abs(value) > 0.0]
            if len(finite_nonzero) < 2:
                return "linear"
            spread_ratio = max(abs(value) for value in finite_nonzero) / max(min(abs(value) for value in finite_nonzero), 1e-12)
            if spread_ratio < 20.0:
                return "linear"
            linthresh = max(float(np.quantile(np.abs(finite_nonzero), 0.35)), 1e-6)
            ax.set_yscale("symlog", linthresh=linthresh)
            return f"symlog(linthresh={linthresh:.1e})"

        def _maybe_use_scientific_ticks(ax, values: list[float]) -> None:
            if ax.get_yscale() != "linear":
                return
            finite_values = [value for value in values if math.isfinite(value)]
            if not finite_values:
                return
            max_abs = max(abs(value) for value in finite_values)
            if 0.0 < max_abs < 1e-2 or max_abs >= 1e3:
                formatter = ticker.ScalarFormatter(useMathText=True)
                formatter.set_powerlimits((-2, 2))
                ax.yaxis.set_major_formatter(formatter)

        def _plot_point_ci(
            *,
            ax,
            labels: list[str],
            series: list[dict[str, object]],
            title: str,
            ylabel: str,
            baseline_line: float | None = None,
        ) -> list[float]:
            x_positions = np.arange(len(labels), dtype=float)
            all_values: list[float] = []
            for item in series:
                offset = float(item.get("offset", 0.0))
                means = list(item["means"])
                finite_positions = [idx for idx, value in enumerate(means) if math.isfinite(value)]
                if not finite_positions:
                    continue
                x_values = [x_positions[idx] + offset for idx in finite_positions]
                y_values = [means[idx] for idx in finite_positions]
                all_values.extend(y_values)
                if "ci95s" in item:
                    ci95s = list(item["ci95s"])
                    y_errors = [ci95s[idx] for idx in finite_positions]
                    all_values.extend(value - error for value, error in zip(y_values, y_errors))
                    all_values.extend(value + error for value, error in zip(y_values, y_errors))
                else:
                    lows = [list(item["lows"])[idx] for idx in finite_positions]
                    highs = [list(item["highs"])[idx] for idx in finite_positions]
                    y_errors = np.array(
                        [
                            [value - low for value, low in zip(y_values, lows)],
                            [high - value for value, high in zip(y_values, highs)],
                        ]
                    )
                    all_values.extend(lows)
                    all_values.extend(highs)
                ax.errorbar(
                    x_values,
                    y_values,
                    yerr=y_errors,
                    fmt="o",
                    linestyle="none",
                    capsize=4,
                    markersize=6,
                    markeredgewidth=1.1,
                    markeredgecolor=str(item["color"]),
                    color=str(item["color"]),
                    ecolor=str(item["color"]),
                    elinewidth=1.3,
                    label=str(item["label"]),
                )
            if baseline_line is not None:
                ax.axhline(
                    baseline_line,
                    linestyle="--",
                    linewidth=1.2,
                    color=style.baseline_color,
                    alpha=0.9,
                )
            ax.set_xticks(x_positions)
            ax.set_xticklabels(labels, rotation=20, ha="right")
            _apply_axes_style(ax, title=title, ylabel=ylabel)
            return all_values

        def _plot_violin_scatter_box(
            *,
            ax,
            data: list[list[float]],
            labels: list[str],
            title: str,
            ylabel: str,
            baseline: float | None = None,
            rng_seed: int = 0,
        ) -> list[float]:
            positions = np.arange(1, len(labels) + 1, dtype=float)
            violin = ax.violinplot(
                data,
                positions=positions,
                widths=0.82,
                showmeans=False,
                showmedians=False,
                showextrema=False,
                bw_method=style.kde_bandwidth_rule,
            )
            for body in violin["bodies"]:
                body.set_facecolor(style.violin_fill)
                body.set_edgecolor(style.violin_edge)
                body.set_alpha(0.42)

            box = ax.boxplot(
                data,
                positions=positions,
                widths=0.20,
                patch_artist=True,
                showfliers=False,
                medianprops={"color": style.text_color, "linewidth": 1.4},
                whiskerprops={"color": style.violin_edge, "linewidth": 1.0},
                capprops={"color": style.violin_edge, "linewidth": 1.0},
            )
            for patch in box["boxes"]:
                patch.set_facecolor(style.violin_edge)
                patch.set_alpha(0.28)
                patch.set_edgecolor(style.violin_edge)

            flattened: list[float] = []
            rng = np.random.default_rng(rng_seed)
            for idx, values in enumerate(data, start=1):
                flattened.extend(values)
                jitter = rng.normal(0.0, 0.045, size=len(values))
                ax.scatter(
                    np.full(len(values), idx, dtype=float) + jitter,
                    values,
                    s=18,
                    color=style.point_color,
                    alpha=0.82,
                    linewidths=0.0,
                    zorder=3,
                )

            if baseline is not None:
                ax.axhline(
                    baseline,
                    linestyle="--",
                    linewidth=1.2,
                    color=style.baseline_color,
                    alpha=0.9,
                )
            ax.set_xticks(positions)
            ax.set_xticklabels(labels, rotation=20, ha="right")
            _apply_axes_style(ax, title=title, ylabel=ylabel)
            _apply_value_axis(ax, flattened, floor=baseline if baseline is not None else None)
            return flattened

        def _finite_variant_metric_values(metric: str, variant_name: str, task_name: str) -> list[float]:
            values: list[float] = []
            for row in variant_rows:
                if str(row.get("task")) != task_name or str(row.get("variant")) != variant_name:
                    continue
                value = float(row.get(metric, float("nan")))
                if math.isfinite(value):
                    values.append(value)
            return values

        def _finite_variant_log2_ratio_values(
            *,
            task_name: str,
            numerator_variant: str,
            denominator_variant: str,
            metric: str,
        ) -> list[float]:
            numerator_by_seed: dict[int, float] = {}
            denominator_by_seed: dict[int, float] = {}
            for row in variant_rows:
                if str(row.get("task")) != task_name:
                    continue
                raw_seed = row.get("seed")
                try:
                    seed = int(raw_seed)
                except (TypeError, ValueError):
                    continue
                variant_name = str(row.get("variant"))
                value = float(row.get(metric, float("nan")))
                if not math.isfinite(value) or value <= 0.0:
                    continue
                if variant_name == numerator_variant:
                    numerator_by_seed[seed] = value
                elif variant_name == denominator_variant:
                    denominator_by_seed[seed] = value
            shared_seeds = sorted(set(numerator_by_seed).intersection(denominator_by_seed))
            ratios: list[float] = []
            for seed in shared_seeds:
                denominator = denominator_by_seed[seed]
                numerator = numerator_by_seed[seed]
                if denominator <= 0.0 or numerator <= 0.0:
                    continue
                ratios.append(numerator / denominator)
            return ratios

        fig, ax = plt.subplots(figsize=(10.8, 5.8))
        baseline_center, baseline_low, baseline_high = [], [], []
        icbr_center, icbr_low, icbr_high = [], [], []
        for task_name in tasks:
            base_center, base_low, base_high_value = _safe_log_metric_ci95(
                _finite_metric_values(task_name, "baseline_symbolic_wall_time_s")
            )
            icbr_value, icbr_low_value, icbr_high_value = _safe_log_metric_ci95(
                _finite_metric_values(task_name, "symbolic_wall_time_s")
            )
            baseline_center.append(base_center)
            baseline_low.append(base_low)
            baseline_high.append(base_high_value)
            icbr_center.append(icbr_value)
            icbr_low.append(icbr_low_value)
            icbr_high.append(icbr_high_value)
        if any(math.isfinite(value) for value in baseline_center + icbr_center):
            all_values = _plot_point_ci(
                ax=ax,
                labels=tasks,
                series=[
                    {
                        "label": "Baseline geometric mean ± 95% CI",
                        "means": baseline_center,
                        "lows": baseline_low,
                        "highs": baseline_high,
                        "offset": -0.12,
                        "color": style.baseline_color,
                    },
                    {
                        "label": "ICBR geometric mean ± 95% CI",
                        "means": icbr_center,
                        "lows": icbr_low,
                        "highs": icbr_high,
                        "offset": 0.12,
                        "color": style.icbr_color,
                    },
                ],
                title="Symbolic Wall Time by Task",
                ylabel="Symbolic Wall Time (s)",
            )
            time_scale = _apply_time_axis(ax, all_values)
            ax.set_ylabel("Symbolic Wall Time (s)")
            _maybe_add_axis_scale_badge(ax, time_scale)
            _maybe_use_scientific_ticks(ax, all_values)
            handles, labels = ax.get_legend_handles_labels()
            legend = fig.legend(
                handles,
                labels,
                loc="upper center",
                bbox_to_anchor=(0.5, 0.99),
                ncol=2,
                frameon=True,
            )
            _style_legend_frame(legend)
            _add_figure_note(
                fig,
                _build_note_lines(
                    summary_line="point=geometric mean; whisker=95% CI on log-scale estimate",
                    measure_line="task-level symbolic wall time",
                    extra_line=f"Scale: {time_scale}; strictly positive timing metrics summarized in multiplicative space",
                ),
            )
            fig.tight_layout(rect=(0.0, 0.08, 1.0, 0.90))
            time_plot = output_dir / "icbr_benchmark_symbolic_time_errorbar.png"
            fig.savefig(time_plot, dpi=160)
            created_files.append(str(time_plot))
            plot_metadata["symbolic_time_errorbar"] = {
                "path": str(time_plot),
                "chart_type": "point_ci95",
                "y_scale": time_scale,
                "y_label": "Symbolic Wall Time (s)",
                "scale_label_placement": "title_band_left",
                "legend_placement": "figure_top_outside",
                "stat_note": "point=geometric mean; whisker=95% CI on log-scale estimate",
                "design_reason": "Timing metrics are strictly positive and right-skewed, so geometric mean on a log axis is more stable for paper comparison.",
            }
        else:
            warnings_list.append(
                "Insufficient finite symbolic timing metrics for plot generation (likely skipped by teacher quality gate)."
            )
        plt.close(fig)

        fig, ax = plt.subplots(figsize=(10.8, 5.8))
        speedup_data = [_finite_metric_values(task_name, "symbolic_speedup_vs_baseline") for task_name in tasks]
        if all(len(values) > 0 for values in speedup_data):
            speedup_values = _plot_violin_scatter_box(
                ax=ax,
                data=speedup_data,
                labels=tasks,
                title="ICBR Speedup vs Baseline",
                ylabel="Speedup Ratio (×)",
                baseline=1.0,
                rng_seed=7,
            )
            speedup_scale = _apply_ratio_axis(
                ax,
                speedup_values,
                baseline=1.0,
                include_baseline_in_limits=False,
            )
            ax.set_ylabel("Speedup Ratio (×)")
            _maybe_add_axis_scale_badge(ax, speedup_scale)
            _maybe_use_scientific_ticks(ax, speedup_values)
            _add_figure_note(
                fig,
                _build_note_lines(
                    summary_line=f"violin KDE bw={style.kde_bandwidth_rule}; box=median/IQR; dots=seed rows",
                    measure_line="per-task speedup distribution vs baseline",
                    extra_line="Reference: dashed line at 1x means parity with baseline symbolic time; log axis keeps multiplicative gaps symmetric",
                ),
            )
            fig.tight_layout(rect=(0.0, 0.08, 1.0, 1.0))
            speedup_plot = output_dir / "icbr_benchmark_speedup_boxplot.png"
            fig.savefig(speedup_plot, dpi=160)
            created_files.append(str(speedup_plot))
            plot_metadata["speedup_boxplot"] = {
                "path": str(speedup_plot),
                "chart_type": "violin_box_points",
                "y_scale": speedup_scale,
                "y_label": "Speedup Ratio (×)",
                "scale_label_placement": "title_band_left",
                "kde_bandwidth_rule": style.kde_bandwidth_rule,
                "stat_note": "violin=density; box=median/IQR; points=seed rows",
                "design_reason": "Speedup is multiplicative by definition, so a log axis with 1x as the neutral reference preserves ratio semantics.",
            }
        else:
            warnings_list.append(
                "Insufficient finite symbolic speedup metrics for plot generation (likely skipped by teacher quality gate)."
            )
        plt.close(fig)

        fig, ax = plt.subplots(figsize=(10.8, 5.8))
        mse_shift_data = [_finite_metric_values(task_name, "final_mse_loss_shift") for task_name in tasks]
        if all(len(values) > 0 for values in mse_shift_data):
            mse_values = _plot_violin_scatter_box(
                ax=ax,
                data=mse_shift_data,
                labels=tasks,
                title="Imitation MSE Shift by Task",
                ylabel="ICBR MSE - baseline MSE",
                baseline=0.0,
                rng_seed=11,
            )
            mse_scale = _apply_symlog_axis(ax, mse_values)
            ax.set_ylabel("ICBR MSE - Baseline MSE")
            _maybe_add_axis_scale_badge(ax, mse_scale)
            _maybe_use_scientific_ticks(ax, mse_values)
            _add_figure_note(
                fig,
                _build_note_lines(
                    summary_line=f"violin KDE bw={style.kde_bandwidth_rule}; box=median/IQR; dots=seed rows",
                    measure_line="per-task imitation-MSE delta distribution",
                    extra_line=f"Reference: dashed line at 0 means no change vs baseline; scale={mse_scale}",
                ),
            )
            fig.tight_layout(rect=(0.0, 0.08, 1.0, 1.0))
            mse_plot = output_dir / "icbr_benchmark_mse_shift_boxplot.png"
            fig.savefig(mse_plot, dpi=160)
            created_files.append(str(mse_plot))
            plot_metadata["mse_shift_boxplot"] = {
                "path": str(mse_plot),
                "chart_type": "violin_box_points",
                "y_scale": mse_scale,
                "y_label": "ICBR MSE - Baseline MSE",
                "scale_label_placement": "title_band_left",
                "kde_bandwidth_rule": style.kde_bandwidth_rule,
                "stat_note": "violin=density; box=median/IQR; points=seed rows",
                "design_reason": "Most tasks cluster near zero while long-tail tasks can dominate, so a zero-centered robust scale is needed.",
            }
        else:
            warnings_list.append("Insufficient finite mse shift metrics for plot generation (likely skipped by teacher quality gate).")
        plt.close(fig)

        variant_metrics = [
            ("symbolic_wall_time_s", "SymbolicTime", "Symbolic Wall Time (s)", style.icbr_color),
            ("merged_mse", "MSEs", "MSE", style.accent_green),
        ]
        fig, axes = plt.subplots(
            nrows=len(tasks),
            ncols=2,
            figsize=(11.6, max(7.6, 3.5 * len(tasks))),
            squeeze=False,
        )
        has_variant_data = False
        time_scale_by_task: dict[str, str] = {}
        mse_scale_by_task: dict[str, str] = {}
        variant_mse_legend_handles = None
        variant_mse_legend_labels = None
        for row_idx, task_name in enumerate(tasks):
            for col_idx, (metric_name, metric_title, ylabel, color) in enumerate(variant_metrics):
                axis = axes[row_idx][col_idx]
                if metric_name == "symbolic_wall_time_s":
                    centers: list[float] = []
                    lows: list[float] = []
                    highs: list[float] = []
                    for variant_name in variants:
                        center, low, high = _safe_log_metric_ci95(
                            _finite_variant_metric_values(metric_name, variant_name, task_name)
                        )
                        centers.append(center)
                        lows.append(low)
                        highs.append(high)
                    if any(math.isfinite(value) for value in centers):
                        has_variant_data = True
                        all_values = _plot_point_ci(
                            ax=axis,
                            labels=variants,
                            series=[
                                {
                                    "label": "SymbolicTime geometric mean ± 95% CI",
                                    "means": centers,
                                    "lows": lows,
                                    "highs": highs,
                                    "offset": 0.0,
                                    "color": color,
                                }
                            ],
                            title=f"{task_name} | {metric_title}",
                            ylabel=ylabel,
                        )
                        time_scale_by_task[task_name] = _apply_time_axis(axis, all_values)
                        _maybe_add_axis_scale_badge(axis, time_scale_by_task[task_name])
                        axis.set_ylabel("Symbolic Wall Time (s)")
                        _maybe_use_scientific_ticks(axis, all_values)
                    else:
                        _apply_axes_style(axis, title=f"{task_name} | {metric_title}", ylabel="Symbolic Wall Time (s)")
                        axis.set_xticks(np.arange(len(variants), dtype=float))
                        axis.set_xticklabels(variants, rotation=20, ha="right")
                    continue

                mse_center: list[float] = []
                mse_low: list[float] = []
                mse_high: list[float] = []
                target_center: list[float] = []
                target_low: list[float] = []
                target_high: list[float] = []
                for variant_name in variants:
                    center, low, high = _safe_log_metric_ci95(
                        _finite_variant_metric_values("mse", variant_name, task_name)
                    )
                    mse_center.append(center)
                    mse_low.append(low)
                    mse_high.append(high)
                    center, low, high = _safe_log_metric_ci95(
                        _finite_variant_metric_values("target_mse", variant_name, task_name)
                    )
                    target_center.append(center)
                    target_low.append(low)
                    target_high.append(high)
                if any(math.isfinite(value) for value in mse_center + target_center):
                    has_variant_data = True
                    all_values = _plot_point_ci(
                        ax=axis,
                        labels=variants,
                        series=[
                            {
                                "label": "ImitationMSE geometric mean ± 95% CI",
                                "means": mse_center,
                                "lows": mse_low,
                                "highs": mse_high,
                                "offset": -0.10,
                                "color": style.accent_green,
                            },
                            {
                                "label": "TargetMSE geometric mean ± 95% CI",
                                "means": target_center,
                                "lows": target_low,
                                "highs": target_high,
                                "offset": 0.10,
                                "color": style.accent_red,
                            }
                        ],
                        title=f"{task_name} | {metric_title}",
                        ylabel=ylabel,
                    )
                    axis.set_yscale("log")
                    mse_scale_by_task[task_name] = "log"
                    _apply_value_axis(axis, all_values)
                    _apply_log_tick_mathtext(axis)
                    _maybe_add_axis_scale_badge(axis, mse_scale_by_task[task_name])
                    axis.set_ylabel("MSE")
                    if variant_mse_legend_handles is None or variant_mse_legend_labels is None:
                        variant_mse_legend_handles, variant_mse_legend_labels = axis.get_legend_handles_labels()
                    _maybe_use_scientific_ticks(axis, all_values)
                else:
                    _apply_axes_style(axis, title=f"{task_name} | {metric_title}", ylabel="MSE")
                    axis.set_xticks(np.arange(len(variants), dtype=float))
                    axis.set_xticklabels(variants, rotation=20, ha="right")
        if has_variant_data:
            if variant_mse_legend_handles and variant_mse_legend_labels:
                legend = fig.legend(
                    variant_mse_legend_handles,
                    variant_mse_legend_labels,
                    loc="upper center",
                    bbox_to_anchor=(0.5, 0.992),
                    ncol=2,
                    frameon=True,
                )
                _style_legend_frame(legend)
            _add_figure_note(
                fig,
                _build_note_lines(
                    summary_line="point=geometric mean; whisker=95% CI on log-scale estimate",
                    measure_line="one task per row; left=SymbolicTime, right=ImitationMSE + TargetMSE",
                    extra_line="Both columns show scale labels; positive skewed metrics are summarized in multiplicative space",
                ),
            )
            fig.tight_layout(rect=(0.0, 0.07, 1.0, 0.95))
            variant_plot = output_dir / "icbr_benchmark_variant_overview.png"
            fig.savefig(variant_plot, dpi=160)
            created_files.append(str(variant_plot))
            plot_metadata["variant_overview"] = {
                "path": str(variant_plot),
                "chart_type": "task_row_two_panel_point_ci95",
                "layout": "one task per row; two columns = SymbolicTime / merged MSEs",
                "time_scale_by_task": time_scale_by_task,
                "mse_scale_by_task": mse_scale_by_task,
                "time_y_label_by_task": {
                    task_name: "Symbolic Wall Time (s)"
                    for task_name, scale in time_scale_by_task.items()
                },
                "mse_y_label": "MSE",
                "scale_label_placement": "title_band_left",
                "legend_placement": "figure_top_outside",
                "stat_note": "point=geometric mean; whisker=95% CI on log-scale estimate",
                "design_reason": "Symbolic time and MSE-family metrics are positive and skewed, so merged log-scale small multiples communicate variant gaps more cleanly.",
            }
        else:
            warnings_list.append("Insufficient finite variant metrics for variant-overview visualization.")
        plt.close(fig)

        challenge_plot_specs = [
            (
                "shared_tensor_symbolic_time_ratio_no_shared_vs_full",
                "Q1 Shared-Tensor Evidence",
                "Symbolic Wall Time Ratio\n(icbr_no_shared / icbr_full, ×)",
                1.0,
                style.accent_gold,
                "log",
            ),
            (
                "contextual_replay_mse_ratio_no_replay_vs_full",
                "Q2 Contextual-Replay Evidence",
                "Imitation MSE Ratio\n(icbr_no_replay / icbr_full, ×)",
                1.0,
                style.accent_green,
                "log",
            ),
            (
                "explicit_commit_mse_ratio_refit_vs_full",
                "Q3 Explicit-Commit Evidence",
                "Imitation MSE Ratio\n(icbr_refit_commit / icbr_full, ×)",
                1.0,
                style.accent_red,
                "log",
            ),
        ]
        fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(10.8, 11.4), squeeze=False)
        has_challenge_data = False
        challenge_scale_map: dict[str, str] = {}
        for axis, (metric_name, title, ylabel, baseline_line, color, metric_scale) in zip(axes.flatten(), challenge_plot_specs):
            means: list[float] = []
            lows: list[float] = []
            highs: list[float] = []
            for task_name in tasks:
                if metric_name == "contextual_replay_mse_ratio_no_replay_vs_full":
                    ratio_values = _finite_variant_log2_ratio_values(
                        task_name=task_name,
                        numerator_variant="icbr_no_replay",
                        denominator_variant="icbr_full",
                        metric="mse",
                    )
                    mean, low, high = _safe_log_metric_ci95(ratio_values)
                elif metric_name == "explicit_commit_mse_ratio_refit_vs_full":
                    ratio_values = _finite_variant_log2_ratio_values(
                        task_name=task_name,
                        numerator_variant="icbr_refit_commit",
                        denominator_variant="icbr_full",
                        metric="mse",
                    )
                    mean, low, high = _safe_log_metric_ci95(ratio_values)
                elif metric_scale == "log":
                    mean, low, high = _safe_log_metric_ci95(_finite_metric_values(task_name, metric_name))
                else:
                    mean, ci95 = _safe_mean_ci95(_finite_metric_values(task_name, metric_name))
                    low = mean - ci95 if math.isfinite(mean) and math.isfinite(ci95) else float("nan")
                    high = mean + ci95 if math.isfinite(mean) and math.isfinite(ci95) else float("nan")
                means.append(mean)
                lows.append(low)
                highs.append(high)
            if any(math.isfinite(value) for value in means):
                has_challenge_data = True
                all_values = _plot_point_ci(
                    ax=axis,
                    labels=tasks,
                    series=[
                        {
                            "label": "Geometric mean ± 95% CI",
                            "means": means,
                            "lows": lows,
                            "highs": highs,
                            "offset": 0.0,
                            "color": color,
                        }
                    ],
                    title=title,
                    ylabel=ylabel,
                    baseline_line=baseline_line,
                )
                axis.set_ylabel(ylabel)
                challenge_scale_map[metric_name] = _apply_ratio_axis(axis, all_values, baseline=baseline_line)
                _maybe_add_axis_scale_badge(axis, challenge_scale_map[metric_name])
                _maybe_use_scientific_ticks(axis, all_values)
            else:
                _apply_axes_style(axis, title=title, ylabel=ylabel)
                axis.set_xticks(np.arange(len(tasks), dtype=float))
                axis.set_xticklabels(tasks, rotation=20, ha="right")
                axis.axhline(
                    baseline_line,
                    linestyle="--",
                    linewidth=1.2,
                    color=style.baseline_color,
                    alpha=0.9,
                )
        if has_challenge_data:
            _add_figure_note(
                fig,
                _build_note_lines(
                    summary_line="Q1/Q2/Q3 all use geometric mean ± 95% CI on ratio values",
                    measure_line="task-wise primary challenge evidence against the icbr_full reference",
                    extra_line="All three panels are ratio-type on a log axis, so 1x means parity with full and larger values mean the ablated variant is higher than full",
                ),
            )
            fig.tight_layout(rect=(0.0, 0.07, 1.0, 1.0))
            challenge_plot = output_dir / "icbr_benchmark_q123_evidence_by_task.png"
            fig.savefig(challenge_plot, dpi=160)
            created_files.append(str(challenge_plot))
            plot_metadata["q123_evidence_by_task"] = {
                "path": str(challenge_plot),
                "chart_type": "point_ci95",
                "scale_by_panel": challenge_scale_map,
                "y_label_by_panel": {
                    "shared_tensor_symbolic_time_ratio_no_shared_vs_full": "Symbolic Wall Time Ratio\n(icbr_no_shared / icbr_full, ×)",
                    "contextual_replay_mse_ratio_no_replay_vs_full": "Imitation MSE Ratio\n(icbr_no_replay / icbr_full, ×)",
                    "explicit_commit_mse_ratio_refit_vs_full": "Imitation MSE Ratio\n(icbr_refit_commit / icbr_full, ×)",
                },
                "scale_label_placement": "title_band_left",
                "stat_note": "Q1/Q2/Q3=geometric mean ratio ± 95% CI; dashed lines=neutral reference at 1x",
                "design_reason": "All three challenge panels are multiplicative comparisons against icbr_full, so ratio values on a log axis preserve the original metric semantics.",
            }
        else:
            warnings_list.append("Insufficient finite Q1/Q2/Q3 evidence metrics for challenge-evidence visualization.")
        plt.close(fig)

    if created_files:
        return {
            "enabled": True,
            "error": "; ".join(warnings_list) if warnings_list else None,
            "files": created_files,
            "plots": plot_metadata,
        }
    error_message = "; ".join(warnings_list) if warnings_list else "No visualization files were created."
    return {"enabled": False, "error": error_message, "files": [], "plots": plot_metadata}


def run_benchmark(
    *,
    tasks: list[str],
    seeds: list[int],
    output_dir: Path,
    train_num: int,
    test_num: int,
    train_steps: int,
    lr: float,
    lamb: float,
    topk: int,
    grid_number: int,
    iteration: int,
    teacher_max_test_mse: float,
    teacher_min_test_r2: float,
    teacher_cache_dir: Path = Path("outputs/teacher_cache"),
    teacher_cache_mode: str = "readwrite",
    teacher_cache_version: str = "v1",
    profile_name: str = "custom",
    profile_defaults: dict[str, float | int] | None = None,
    profile_overrides: dict[str, bool] | None = None,
    feynman_root: Path = Path("datasets"),
    feynman_variant: str = "Feynman_with_units",
    feynman_equations_csv: Path | None = None,
    feynman_split_strategy: str = "random",
    feynman_split_strategy_seed: int | None = None,
    feynman_post_prune_steps: int | None = None,
    feynman_post_prune_lr: float | None = None,
    feynman_post_prune_lamb: float | None = None,
    feynman_post_prune_eval_every: int | None = None,
    feynman_post_prune_min_delta: float | None = None,
    feynman_post_prune_patience: int | None = None,
    feynman_fit_opt: str | None = None,
    feynman_width_mid: list[_WidthToken] | None = None,
    prune_iters: int | None = None,
    feynman_max_datasets: int = 10,
    feynman_dataset_select_seed: int = 1,
    variants: list[str] | None = None,
    enable_teacher_prune: bool | None = None,
    teacher_prune_node_th: float = 1e-2,
    teacher_prune_edge_th: float = 1e-2,
    make_plots: bool,
    quiet: bool,
) -> dict[str, object]:
    if feynman_variant not in _FEYNMAN_VARIANTS:
        raise ValueError(f"Unsupported feynman variant: {feynman_variant}")
    if feynman_split_strategy not in {"random", "linspace"}:
        raise ValueError(f"Unsupported feynman split strategy: {feynman_split_strategy}")
    if feynman_split_strategy_seed is not None and int(feynman_split_strategy_seed) < 0:
        raise ValueError("feynman_split_strategy_seed must be >= 0.")
    if prune_iters is not None and int(prune_iters) < 0:
        raise ValueError("prune_iters must be >= 0.")
    if feynman_fit_opt is not None and feynman_fit_opt not in _FEYNMAN_FIT_OPTS:
        raise ValueError(f"Unsupported feynman_fit_opt: {feynman_fit_opt}")
    if feynman_width_mid is None:
        feynman_width_mid = [[5, 2]]
    if prune_iters is None:
        prune_iters = 3 if _tasks_request_feynman_defaults(tasks) or profile_name == "feynman_reference" else 1

    resolved_tasks, specs, _equations_map, feynman_config = _resolve_task_specs(
        tasks=tasks,
        feynman_root=feynman_root,
        feynman_variant=feynman_variant,
        feynman_width_mid=feynman_width_mid,
        feynman_split_strategy=feynman_split_strategy,
        feynman_split_strategy_seed=(
            int(feynman_split_strategy_seed) if feynman_split_strategy_seed is not None else None
        ),
        feynman_post_prune_steps=feynman_post_prune_steps,
        feynman_post_prune_lr=feynman_post_prune_lr,
        feynman_post_prune_lamb=feynman_post_prune_lamb,
        feynman_post_prune_eval_every=feynman_post_prune_eval_every,
        feynman_post_prune_min_delta=feynman_post_prune_min_delta,
        feynman_post_prune_patience=feynman_post_prune_patience,
        prune_iters=int(prune_iters),
        feynman_fit_opt=feynman_fit_opt,
        feynman_max_datasets=feynman_max_datasets,
        feynman_dataset_select_seed=feynman_dataset_select_seed,
        feynman_equations_csv=feynman_equations_csv,
    )
    effective_variants = _normalize_variants(",".join(variants) if variants is not None else None)
    effective_enable_teacher_prune = bool(enable_teacher_prune) if enable_teacher_prune is not None else (profile_name == "quality")
    for task_name in resolved_tasks:
        spec = specs[task_name]
        if spec.dataset_kind == "feynman_file":
            continue
        if not effective_enable_teacher_prune:
            continue
        specs[task_name] = replace(
            spec,
            teacher_post_train_prune=True,
            teacher_prune_node_th=float(teacher_prune_node_th),
            teacher_prune_edge_th=float(teacher_prune_edge_th),
            teacher_prune_iters=int(prune_iters),
        )
    feynman_config["benchmark_variants"] = list(effective_variants)

    output_dir.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, object]] = []
    variant_rows: list[dict[str, object]] = []

    for task_name in resolved_tasks:
        spec = specs[task_name]
        for seed in seeds:
            effective_topk = int(spec.icbr_topk) if spec.icbr_topk is not None else int(topk)
            effective_teacher_max_test_mse = (
                float(spec.teacher_max_test_mse)
                if spec.teacher_max_test_mse is not None
                else float(teacher_max_test_mse)
            )
            effective_teacher_min_test_r2 = (
                float(spec.teacher_min_test_r2)
                if spec.teacher_min_test_r2 is not None
                else (
                    None
                    if spec.dataset_kind == "feynman_file" and spec.teacher_min_test_r2 is None
                    else float(teacher_min_test_r2)
                )
            )
            model, dataset, cache_info = _resolve_teacher_model_with_cache(
                spec=spec,
                seed=seed,
                train_num=train_num,
                test_num=test_num,
                train_steps=train_steps,
                lr=lr,
                lamb=lamb,
                profile_name=profile_name,
                cache_dir=teacher_cache_dir,
                cache_mode=teacher_cache_mode,
                cache_version=teacher_cache_version,
                quiet=quiet,
            )
            with torch.no_grad():
                teacher_test_pred = model(dataset["test_input"])
                if isinstance(teacher_test_pred, tuple):
                    teacher_test_pred = teacher_test_pred[0]
                teacher_test_pred = teacher_test_pred.detach()
            teacher_test_mse, teacher_test_r2 = _compute_target_mse_and_r2(
                teacher_test_pred,
                dataset["test_label"],
            )
            teacher_quality_gate_pass, teacher_quality_gate_reason = _build_teacher_quality_gate_result(
                teacher_test_mse=teacher_test_mse,
                teacher_test_r2=teacher_test_r2,
                max_test_mse=effective_teacher_max_test_mse,
                min_test_r2=effective_teacher_min_test_r2,
            )

            if teacher_quality_gate_pass:
                with _suppress_console_output(quiet):
                    variant_bundle = benchmark_symbolic_variants(
                        model,
                        calibration_split={
                            "test_input": dataset["test_input"],
                            "test_label": dataset["test_label"],
                        },
                        calibration_target=dataset["test_label"],
                        lib=spec.lib,
                        topk=effective_topk,
                        a_range=(-5.0, 5.0),
                        b_range=(-5.0, 5.0),
                        grid_number=grid_number,
                        iteration=iteration,
                        variants=effective_variants,
                    )
                metrics = _build_legacy_metrics_from_variant_bundle(variant_bundle)
                variant_rows.extend(
                    _build_variant_rows_for_task_seed(
                        task=task_name,
                        seed=seed,
                        variant_bundle=variant_bundle,
                        variants_requested=effective_variants,
                        teacher_quality_gate_pass=teacher_quality_gate_pass,
                        teacher_quality_gate_reason=teacher_quality_gate_reason,
                    )
                )
                challenge_evidence = dict(variant_bundle.get("challenge_evidence", {}))
            else:
                metrics = _build_skipped_symbolic_metrics(reason=teacher_quality_gate_reason)
                variant_rows.extend(
                    _build_skipped_variant_rows_for_task_seed(
                        task=task_name,
                        seed=seed,
                        variants_requested=effective_variants,
                        reason=teacher_quality_gate_reason,
                    )
                )
                challenge_evidence = {
                    "shared_tensor": {
                        "candidate_time_ratio_no_shared_vs_full": float("nan"),
                        "symbolic_time_ratio_no_shared_vs_full": float("nan"),
                    },
                    "contextual_replay": {
                        "mse_gain_full_vs_no_replay": float("nan"),
                        "target_mse_gain_full_vs_no_replay": float("nan"),
                        "replay_rank_inversion_rate_full": float("nan"),
                    },
                    "explicit_commit": {
                        "mse_gain_explicit_vs_refit": float("nan"),
                        "target_mse_gain_explicit_vs_refit": float("nan"),
                        "refit_commit_param_drift_l2_mean": float("nan"),
                    },
                }
            row = {
                "task": task_name,
                "seed": seed,
                "task_kind": spec.dataset_kind,
                "task_source": "feynman_file" if spec.dataset_kind == "feynman_file" else "synthetic_formula",
                "target_formula": spec.target_formula,
                "feynman_dataset_filename": spec.dataset_filename,
                "feynman_dataset_rows": spec.dataset_total_rows,
                "feynman_dataset_columns": spec.dataset_total_columns,
                "feynman_split_seed": _resolve_dataset_split_seed(spec, benchmark_seed=seed),
                "feynman_equation_metadata": dict(spec.equation_metadata or {}),
                "n_var": spec.n_var,
                "width": list(spec.width),
                "lib": list(spec.lib) if spec.lib is not None else ["__FULL_SYMBOLIC_LIB__"],
                "icbr_topk_used": effective_topk,
                "teacher_test_mse": teacher_test_mse,
                "teacher_test_r2": teacher_test_r2,
                "teacher_max_test_mse_threshold": effective_teacher_max_test_mse,
                "teacher_min_test_r2_threshold": effective_teacher_min_test_r2,
                "teacher_quality_gate_pass": teacher_quality_gate_pass,
                "teacher_quality_gate_reason": teacher_quality_gate_reason,
                "teacher_cache_hit": bool(cache_info["teacher_cache_hit"]),
                "teacher_cache_key": str(cache_info["teacher_cache_key"]),
                "teacher_cache_path": str(cache_info["teacher_cache_path"]),
                "teacher_cache_mode": str(cache_info["teacher_cache_mode"]),
                "teacher_cache_status": str(cache_info["teacher_cache_status"]),
                "shared_tensor_candidate_time_ratio_no_shared_vs_full": float(
                    challenge_evidence["shared_tensor"]["candidate_time_ratio_no_shared_vs_full"]
                ),
                "shared_tensor_symbolic_time_ratio_no_shared_vs_full": float(
                    challenge_evidence["shared_tensor"]["symbolic_time_ratio_no_shared_vs_full"]
                ),
                "contextual_replay_mse_gain_full_vs_no_replay": float(
                    challenge_evidence["contextual_replay"]["mse_gain_full_vs_no_replay"]
                ),
                "contextual_replay_target_mse_gain_full_vs_no_replay": float(
                    challenge_evidence["contextual_replay"]["target_mse_gain_full_vs_no_replay"]
                ),
                "contextual_replay_rank_inversion_rate_full": float(
                    challenge_evidence["contextual_replay"]["replay_rank_inversion_rate_full"]
                ),
                "explicit_commit_mse_gain_explicit_vs_refit": float(
                    challenge_evidence["explicit_commit"]["mse_gain_explicit_vs_refit"]
                ),
                "explicit_commit_target_mse_gain_explicit_vs_refit": float(
                    challenge_evidence["explicit_commit"]["target_mse_gain_explicit_vs_refit"]
                ),
                "explicit_commit_refit_commit_param_drift_l2_mean": float(
                    challenge_evidence["explicit_commit"]["refit_commit_param_drift_l2_mean"]
                ),
                **metrics,
            }
            rows.append(row)
            if not quiet:
                if teacher_quality_gate_pass:
                    print(
                        f"[icbr-benchmark] task={task_name} seed={seed} "
                        f"cache_hit={bool(cache_info['teacher_cache_hit'])} "
                        f"teacher_mse={teacher_test_mse:.6e} teacher_r2={teacher_test_r2:.4f} "
                        f"icbr_symbolic={metrics['symbolic_wall_time_s']:.4f}s "
                        f"baseline_symbolic={metrics['baseline_symbolic_wall_time_s']:.4f}s "
                        f"speedup={metrics['symbolic_speedup_vs_baseline']:.2f}x "
                        f"mse_shift={metrics['final_mse_loss_shift']:.6e} "
                        f"target_mse_shift={metrics['symbolic_target_mse_shift']:.6e}"
                    )
                else:
                    print(
                        f"[icbr-benchmark] task={task_name} seed={seed} "
                        f"cache_hit={bool(cache_info['teacher_cache_hit'])} "
                        f"teacher_mse={teacher_test_mse:.6e} teacher_r2={teacher_test_r2:.4f} "
                        f"skipped_symbolic_by_gate reason={teacher_quality_gate_reason}"
                    )

    rows_csv = output_dir / "icbr_benchmark_rows.csv"
    row_fieldnames = [
        "task",
        "seed",
        "task_kind",
        "task_source",
        "target_formula",
        "feynman_dataset_filename",
        "feynman_dataset_rows",
        "feynman_dataset_columns",
        "feynman_split_seed",
        "feynman_equation_metadata",
        "n_var",
        "width",
        "lib",
        "icbr_topk_used",
        "teacher_test_mse",
        "teacher_test_r2",
        "teacher_max_test_mse_threshold",
        "teacher_min_test_r2_threshold",
        "teacher_quality_gate_pass",
        "teacher_quality_gate_reason",
        "teacher_cache_hit",
        "teacher_cache_key",
        "teacher_cache_path",
        "teacher_cache_mode",
        "teacher_cache_status",
        "shared_tensor_candidate_time_ratio_no_shared_vs_full",
        "shared_tensor_symbolic_time_ratio_no_shared_vs_full",
        "contextual_replay_mse_gain_full_vs_no_replay",
        "contextual_replay_target_mse_gain_full_vs_no_replay",
        "contextual_replay_rank_inversion_rate_full",
        "explicit_commit_mse_gain_explicit_vs_refit",
        "explicit_commit_target_mse_gain_explicit_vs_refit",
        "explicit_commit_refit_commit_param_drift_l2_mean",
        "candidate_generation_wall_time_s",
        "replay_rerank_wall_time_s",
        "symbolic_wall_time_s",
        "baseline_symbolic_wall_time_s",
        "symbolic_wall_time_delta_s",
        "symbolic_speedup_vs_baseline",
        "replay_imitation_gap",
        "final_mse_loss_shift",
        "baseline_mse",
        "icbr_mse",
        "teacher_target_mse",
        "teacher_target_r2",
        "baseline_target_mse",
        "baseline_target_r2",
        "icbr_target_mse",
        "icbr_target_r2",
        "symbolic_target_mse_shift",
        "symbolic_target_r2_shift",
        "formula_validation_result",
        "baseline_formula_validation_result",
        "icbr_formula_validation_result",
        "baseline_formula_error",
        "icbr_formula_error",
        "baseline_formula_raw",
        "baseline_formula_display",
        "icbr_formula_raw",
        "icbr_formula_display",
    ]
    with rows_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=row_fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    "task": row["task"],
                    "seed": row["seed"],
                    "task_kind": row["task_kind"],
                    "task_source": row["task_source"],
                    "target_formula": row["target_formula"],
                    "feynman_dataset_filename": row["feynman_dataset_filename"],
                    "feynman_dataset_rows": row["feynman_dataset_rows"],
                    "feynman_dataset_columns": row["feynman_dataset_columns"],
                    "feynman_split_seed": row["feynman_split_seed"],
                    "feynman_equation_metadata": json.dumps(row["feynman_equation_metadata"], ensure_ascii=False),
                    "n_var": row["n_var"],
                    "width": json.dumps(row["width"], ensure_ascii=False),
                    "lib": json.dumps(row["lib"], ensure_ascii=False),
                    "icbr_topk_used": row["icbr_topk_used"],
                    "teacher_test_mse": row["teacher_test_mse"],
                    "teacher_test_r2": row["teacher_test_r2"],
                    "teacher_max_test_mse_threshold": row["teacher_max_test_mse_threshold"],
                    "teacher_min_test_r2_threshold": row["teacher_min_test_r2_threshold"],
                    "teacher_quality_gate_pass": row["teacher_quality_gate_pass"],
                    "teacher_quality_gate_reason": row["teacher_quality_gate_reason"],
                    "teacher_cache_hit": row["teacher_cache_hit"],
                    "teacher_cache_key": row["teacher_cache_key"],
                    "teacher_cache_path": row["teacher_cache_path"],
                    "teacher_cache_mode": row["teacher_cache_mode"],
                    "teacher_cache_status": row["teacher_cache_status"],
                    "shared_tensor_candidate_time_ratio_no_shared_vs_full": row[
                        "shared_tensor_candidate_time_ratio_no_shared_vs_full"
                    ],
                    "shared_tensor_symbolic_time_ratio_no_shared_vs_full": row[
                        "shared_tensor_symbolic_time_ratio_no_shared_vs_full"
                    ],
                    "contextual_replay_mse_gain_full_vs_no_replay": row[
                        "contextual_replay_mse_gain_full_vs_no_replay"
                    ],
                    "contextual_replay_target_mse_gain_full_vs_no_replay": row[
                        "contextual_replay_target_mse_gain_full_vs_no_replay"
                    ],
                    "contextual_replay_rank_inversion_rate_full": row[
                        "contextual_replay_rank_inversion_rate_full"
                    ],
                    "explicit_commit_mse_gain_explicit_vs_refit": row[
                        "explicit_commit_mse_gain_explicit_vs_refit"
                    ],
                    "explicit_commit_target_mse_gain_explicit_vs_refit": row[
                        "explicit_commit_target_mse_gain_explicit_vs_refit"
                    ],
                    "explicit_commit_refit_commit_param_drift_l2_mean": row[
                        "explicit_commit_refit_commit_param_drift_l2_mean"
                    ],
                    "candidate_generation_wall_time_s": row["candidate_generation_wall_time_s"],
                    "replay_rerank_wall_time_s": row["replay_rerank_wall_time_s"],
                    "symbolic_wall_time_s": row["symbolic_wall_time_s"],
                    "baseline_symbolic_wall_time_s": row["baseline_symbolic_wall_time_s"],
                    "symbolic_wall_time_delta_s": row["symbolic_wall_time_delta_s"],
                    "symbolic_speedup_vs_baseline": row["symbolic_speedup_vs_baseline"],
                    "replay_imitation_gap": row["replay_imitation_gap"],
                    "final_mse_loss_shift": row["final_mse_loss_shift"],
                    "baseline_mse": row["baseline_mse"],
                    "icbr_mse": row["icbr_mse"],
                    "teacher_target_mse": row["teacher_target_mse"],
                    "teacher_target_r2": row["teacher_target_r2"],
                    "baseline_target_mse": row["baseline_target_mse"],
                    "baseline_target_r2": row["baseline_target_r2"],
                    "icbr_target_mse": row["icbr_target_mse"],
                    "icbr_target_r2": row["icbr_target_r2"],
                    "symbolic_target_mse_shift": row["symbolic_target_mse_shift"],
                    "symbolic_target_r2_shift": row["symbolic_target_r2_shift"],
                    "formula_validation_result": row["formula_validation_result"],
                    "baseline_formula_validation_result": row["baseline_formula_validation_result"],
                    "icbr_formula_validation_result": row["icbr_formula_validation_result"],
                    "baseline_formula_error": row["baseline_formula_error"],
                    "icbr_formula_error": row["icbr_formula_error"],
                    "baseline_formula_raw": _serialize_formula_list(row["baseline_formula_raw"]),
                    "baseline_formula_display": _serialize_formula_list(row["baseline_formula_display"]),
                    "icbr_formula_raw": _serialize_formula_list(row["icbr_formula_raw"]),
                    "icbr_formula_display": _serialize_formula_list(row["icbr_formula_display"]),
                }
            )

    variant_rows_csv = output_dir / "icbr_benchmark_variant_rows.csv"
    variant_row_fieldnames = [
        "task",
        "seed",
        "variant",
        "variant_requested",
        "candidate_mode",
        "rerank_mode",
        "commit_mode",
        "teacher_quality_gate_pass",
        "teacher_quality_gate_reason",
        "candidate_generation_wall_time_s",
        "replay_rerank_wall_time_s",
        "symbolic_wall_time_s",
        "mse",
        "target_mse",
        "target_r2",
        "formula_validation_result",
        "formula_error",
        "formula_raw",
        "formula_display",
        "replay_rank_inversion_count",
        "replay_rank_inversion_total",
        "replay_rank_inversion_rate",
        "commit_param_drift_l2_mean",
        "commit_param_drift_l2_max",
        "baseline_symbolic_wall_time_s",
        "baseline_mse",
        "baseline_target_mse",
        "baseline_target_r2",
        "symbolic_wall_time_delta_s",
        "symbolic_speedup_vs_baseline",
        "final_mse_loss_shift",
        "symbolic_target_mse_shift",
        "symbolic_target_r2_shift",
    ]
    with variant_rows_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=variant_row_fieldnames)
        writer.writeheader()
        for row in variant_rows:
            serialized_row = {name: row.get(name, "") for name in variant_row_fieldnames}
            serialized_row["formula_raw"] = _serialize_formula_list(list(row.get("formula_raw", [])))
            serialized_row["formula_display"] = _serialize_formula_list(list(row.get("formula_display", [])))
            writer.writerow(serialized_row)

    by_task_rows = {task_name: [row for row in rows if row["task"] == task_name] for task_name in resolved_tasks}
    by_task_metrics = {task_name: _build_metric_stats(task_rows) for task_name, task_rows in by_task_rows.items()}
    overall_metrics = _build_metric_stats(rows)
    challenge_evidence_overall = _build_challenge_evidence_stats(rows)
    challenge_evidence_by_task = {
        task_name: _build_challenge_evidence_stats(task_rows)
        for task_name, task_rows in by_task_rows.items()
    }
    by_task_significance = {
        task_name: _build_significance(task_rows, task_label=task_name) for task_name, task_rows in by_task_rows.items()
    }
    overall_significance = _build_significance(rows, task_label="__overall__")

    variant_by_task = {task_name: [row for row in variant_rows if row["task"] == task_name] for task_name in resolved_tasks}
    variant_overall_rows_by_variant = {
        variant_name: [row for row in variant_rows if row["variant"] == variant_name]
        for variant_name in effective_variants
    }
    variant_by_task_rows_by_variant = {
        task_name: {
            variant_name: [row for row in variant_by_task[task_name] if row["variant"] == variant_name]
            for variant_name in effective_variants
        }
        for task_name in resolved_tasks
    }
    variant_overall_stats = {
        variant_name: {
            "row_count": len(variant_overall_rows_by_variant[variant_name]),
            "metrics": _build_variant_metric_stats(variant_overall_rows_by_variant[variant_name]),
        }
        for variant_name in effective_variants
    }
    variant_task_stats = {
        task_name: {
            variant_name: {
                "row_count": len(variant_by_task_rows_by_variant[task_name][variant_name]),
                "metrics": _build_variant_metric_stats(variant_by_task_rows_by_variant[task_name][variant_name]),
            }
            for variant_name in effective_variants
        }
        for task_name in resolved_tasks
    }

    task_stats_rows = _build_task_stats_rows(
        tasks=resolved_tasks,
        rows=rows,
        by_task_metrics=by_task_metrics,
        overall_metrics=overall_metrics,
    )
    task_stats_csv = output_dir / "icbr_benchmark_task_stats.csv"
    _write_task_stats_csv(task_stats_csv, task_stats_rows)

    significance_rows = _build_significance_rows(tasks=resolved_tasks, by_task_significance=by_task_significance)
    significance_csv = output_dir / "icbr_benchmark_significance.csv"
    _write_significance_csv(significance_csv, significance_rows)

    visualization = {"enabled": False, "error": "Disabled by --no-plots", "files": []}
    if make_plots:
        visualization = _generate_visualizations(
            output_dir=output_dir,
            tasks=resolved_tasks,
            by_task_rows=by_task_rows,
            variant_rows=variant_rows,
            variants=list(effective_variants),
        )

    summary = {
        "metadata": {
            "generated_at_utc": datetime.now(timezone.utc).isoformat(),
            "benchmark_name": "icbr_phase1_cpu_extended_validation",
            "report_version": "2.0",
        },
        "config": {
            "tasks": resolved_tasks,
            "seeds": seeds,
            "profile": {
                "name": profile_name,
                "defaults": profile_defaults if profile_defaults is not None else {},
                "overrides": profile_overrides if profile_overrides is not None else {},
            },
            "train_num": train_num,
            "test_num": test_num,
            "train_steps": train_steps,
            "lr": lr,
            "lamb": lamb,
            "topk": topk,
            "grid_number": grid_number,
            "iteration": iteration,
            "variants": list(effective_variants),
            "teacher_prune_policy": {
                "enabled": bool(effective_enable_teacher_prune),
                "default_rule": "enabled_by_default_when_profile_is_quality",
                "node_th": float(teacher_prune_node_th),
                "edge_th": float(teacher_prune_edge_th),
                "prune_iters": int(prune_iters),
            },
            "teacher_quality_gate": {
                "enabled": True,
                "teacher_max_test_mse_default": float(teacher_max_test_mse),
                "teacher_min_test_r2_default": float(teacher_min_test_r2),
                "task_overrides": {
                    task_name: {
                        "teacher_max_test_mse": (
                            float(specs[task_name].teacher_max_test_mse)
                            if specs[task_name].teacher_max_test_mse is not None
                            else float(teacher_max_test_mse)
                        ),
                        "teacher_min_test_r2": (
                            float(specs[task_name].teacher_min_test_r2)
                            if specs[task_name].teacher_min_test_r2 is not None
                            else (
                                None
                                if specs[task_name].dataset_kind == "feynman_file"
                                and specs[task_name].teacher_min_test_r2 is None
                                else float(teacher_min_test_r2)
                            )
                        ),
                    }
                    for task_name in resolved_tasks
                },
                "policy": "skip_symbolic_comparison_when_teacher_quality_fails; null threshold means that metric is not required",
            },
            "teacher_training": {
                task_name: {
                    "grid": int(specs[task_name].teacher_grid),
                    "k": int(specs[task_name].teacher_k),
                    "opt": specs[task_name].teacher_fit_opt,
                    "post_train_prune": bool(specs[task_name].teacher_post_train_prune),
                    "prune_node_th": float(specs[task_name].teacher_prune_node_th),
                    "prune_edge_th": float(specs[task_name].teacher_prune_edge_th),
                    "prune_iters": int(specs[task_name].teacher_prune_iters),
                    "post_prune_steps": int(specs[task_name].teacher_post_prune_steps),
                    "post_prune_lr": float(specs[task_name].teacher_post_prune_lr),
                    "post_prune_lamb": float(specs[task_name].teacher_post_prune_lamb),
                    "post_prune_early_stop": bool(specs[task_name].teacher_post_prune_early_stop),
                    "post_prune_eval_every": int(specs[task_name].teacher_post_prune_eval_every),
                    "post_prune_min_delta": float(specs[task_name].teacher_post_prune_min_delta),
                    "post_prune_patience": int(specs[task_name].teacher_post_prune_patience),
                }
                for task_name in resolved_tasks
            },
            "feynman": feynman_config,
            "teacher_cache": {
                "dir": str(teacher_cache_dir),
                "mode": teacher_cache_mode,
                "version": teacher_cache_version,
                "modes_supported": sorted(_TEACHER_CACHE_MODES),
            },
            "output_dir": str(output_dir),
            "plots_enabled": make_plots,
            "task_topk_overrides": {
                task_name: int(specs[task_name].icbr_topk)
                for task_name in resolved_tasks
                if specs[task_name].icbr_topk is not None
            },
            "task_lib_mode": {
                task_name: ("full_symbolic_lib" if specs[task_name].lib is None else "task_subset")
                for task_name in resolved_tasks
            },
        },
        "rows": rows,
        "aggregates": {
            "overall": {
                "row_count": len(rows),
                "metrics": overall_metrics,
                "significance": overall_significance,
            },
            "by_task": {
                task_name: {
                    "row_count": len(by_task_rows[task_name]),
                    "metrics": by_task_metrics[task_name],
                    "significance": by_task_significance[task_name],
                }
                for task_name in resolved_tasks
            },
            "challenge_evidence": {
                "overall": challenge_evidence_overall,
                "by_task": challenge_evidence_by_task,
            },
            "variant_ablation": {
                "overall": variant_overall_stats,
                "by_task": variant_task_stats,
            },
        },
        "artifacts": {
            "rows_csv": str(rows_csv),
            "variant_rows_csv": str(variant_rows_csv),
            "task_stats_csv": str(task_stats_csv),
            "significance_csv": str(significance_csv),
            "visualizations": visualization,
        },
        "notes": {
            "field_guide": {
                "symbolic_wall_time_delta_s": "baseline_symbolic_wall_time_s - icbr_symbolic_wall_time_s",
                "final_mse_loss_shift": "icbr_mse - baseline_mse; negative means ICBR has lower MSE",
                "teacher_test_mse": "Teacher numeric model MSE against real test labels before symbolic fitting.",
                "teacher_test_r2": "Teacher numeric model R2 against real test labels before symbolic fitting.",
                "teacher_cache_hit": "Whether teacher model was loaded from persistent cache.",
                "symbolic_target_mse_shift": "icbr_target_mse - baseline_target_mse; negative means ICBR is closer to real targets.",
                "symbolic_target_r2_shift": "icbr_target_r2 - baseline_target_r2; positive means ICBR has higher target R2.",
                "shared_tensor_candidate_time_ratio_no_shared_vs_full": "Q1 evidence: icbr_no_shared candidate time / icbr_full candidate time; >1 suggests shared tensor helps.",
                "shared_tensor_symbolic_time_ratio_no_shared_vs_full": "Q1 evidence: icbr_no_shared total symbolic time / icbr_full total symbolic time.",
                "contextual_replay_mse_gain_full_vs_no_replay": "Q2 evidence: icbr_no_replay mse - icbr_full mse; >0 suggests replay rerank improves imitation error.",
                "contextual_replay_rank_inversion_rate_full": "Q2 evidence: fraction of edges where replay-selected candidate differs from local top-1 in icbr_full.",
                "explicit_commit_mse_gain_explicit_vs_refit": "Q3 evidence: icbr_refit_commit mse - icbr_full mse; >0 suggests explicit commit avoids refit drift.",
                "explicit_commit_refit_commit_param_drift_l2_mean": "Q3 evidence: mean L2 drift between selected params and refit params under icbr_refit_commit.",
                "stats_schema": "Each metric includes count | mean | median | std | min | max",
            },
            "significance_guide": {
                "sign_test_pvalue_two_sided": "Two-sided sign test p-value on non-tie seeds.",
                "mean_delta_ci95": "Bootstrap 95% CI of mean delta across seeds.",
            },
            "variant_ablation_guide": {
                "baseline": "MultKAN.auto_symbolic() baseline.",
                "icbr_full": "ICBR with shared candidate evaluation + replay rerank + explicit commit.",
                "icbr_no_replay": "ICBR with local-r2 rerank (replay disabled).",
                "icbr_no_shared": "ICBR with per-edge serial candidate generation (shared batching disabled).",
                "icbr_refit_commit": "ICBR with refit commit path (explicit commit disabled).",
            },
            "visualization_design_guide": {
                "point_ci95": {
                    "best_for": "Paper-style center-and-uncertainty comparison without bar-area distortion.",
                    "recommended_when": "Need log-scale compatible estimates or task-level evidence summaries.",
                    "example_metrics": [
                        "symbolic_wall_time_s",
                        "variant_overview_symbolic_wall_time_s",
                        "q1/q2/q3 evidence",
                    ],
                },
                "violin_box_points": {
                    "best_for": "Seed-level distribution comparison with density, median/IQR, and raw samples together.",
                    "recommended_when": "Need one chart to expose multimodality, spread, and small-sample dispersion.",
                    "example_metrics": ["symbolic_speedup_vs_baseline", "final_mse_loss_shift"],
                },
                "variant_grid": {
                    "best_for": "Task-by-task variant comparison without mixing units on one axis.",
                    "recommended_when": "Need each task on its own row, symbolic time on one panel, and merged MSE-family metrics on another.",
                    "example_metrics": ["symbolic_wall_time_s", "mse + target_mse"],
                },
                "combo_layout": {
                    "best_for": "Decision-ready report combining uncertainty views and distribution views under one visual language.",
                    "recommended_panels": [
                        "Panel A: point + 95% CI (geometric mean for positive skewed metrics)",
                        "Panel B: violin + box + points (distribution)",
                        "Panel C: task-row small multiples with merged MSE panel",
                    ],
                },
            },
            "teacher_quality_gate": {
                "pass_rule": "teacher_test_mse <= threshold_mse AND teacher_test_r2 >= threshold_r2 when the corresponding threshold is set; null threshold disables that check",
                "failure_policy": "Skip baseline/ICBR symbolic comparison for that row and keep explicit gate reason.",
            },
            "teacher_cache": {
                "cache_key_rule": "hash(task, seed, width, dataset_kind, dataset_path, dataset_variant, dataset_split_strategy, dataset_split_seed, teacher_grid, teacher_k, teacher_fit_opt, teacher_post_train_prune, teacher_prune_node_th, teacher_prune_edge_th, teacher_prune_iters, teacher_post_prune_steps, teacher_post_prune_lr, teacher_post_prune_lamb, teacher_post_prune_early_stop, teacher_post_prune_eval_every, teacher_post_prune_min_delta, teacher_post_prune_patience, train_num, test_num, train_steps, lr, lamb, profile, cache_version)",
                "modes": {
                    "readwrite": "Read cache when available; train+write on miss.",
                    "readonly": "Read cache only; train without writing on miss.",
                    "refresh": "Ignore old cache and retrain, then overwrite cache.",
                    "off": "Disable cache and always train.",
                },
            },
            "teacher_training": {
                "feynman_reference_policy": "For feynman_file tasks: train(opt=Adam by default; override via --feynman-fit-opt) -> repeat prune(node_th=1e-2, edge_th=1e-2) + refit(steps=100, lr=1e-3, lamb=1e-3, early_stop_check_every=5) for prune_iters rounds (default 3) -> cache.",
            },
            "extensibility": [
                "Add new tasks in the resolver layer (core task specs or feynman token expansion).",
                "Rows-level details are preserved for error bars and downstream statistical tests.",
                "Task stats CSV and significance CSV can be consumed by external plotting/report tools.",
                "Teacher cache key version can be bumped with --teacher-cache-version for compatibility control.",
            ],
        },
    }
    summary_json_path = output_dir / "icbr_benchmark_summary.json"
    summary_json_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    md_lines: list[str] = [
        "# ICBR Benchmark Summary",
        "",
        "## Run Config",
        "",
        f"- Profile: {summary['config']['profile']['name']}",
        f"- Tasks: {', '.join(resolved_tasks)}",
        f"- Seeds: {', '.join(str(seed) for seed in seeds)}",
        f"- Train/Test samples per task: {train_num}/{test_num}",
        f"- Train steps: {train_steps}, lr: {lr}, lamb: {lamb}",
        f"- Teacher cache: mode={teacher_cache_mode}, dir={teacher_cache_dir}, version={teacher_cache_version}",
        f"- ICBR shortlist topk: {topk}, grid_number: {grid_number}, iteration: {iteration}",
        f"- Variants: {', '.join(summary['config']['variants'])}",
        f"- Teacher prune policy: enabled={summary['config']['teacher_prune_policy']['enabled']}, "
        f"node_th={summary['config']['teacher_prune_policy']['node_th']}, "
        f"edge_th={summary['config']['teacher_prune_policy']['edge_th']}, "
        f"prune_iters={summary['config']['teacher_prune_policy']['prune_iters']}",
    ]
    if bool(summary["config"]["feynman"]["enabled"]):
        md_lines.append(
            f"- Feynman data: root={summary['config']['feynman']['root']}, "
            f"variant={summary['config']['feynman']['variant']}, "
            f"split={summary['config']['feynman']['split_strategy']}, "
            f"split_seed={summary['config']['feynman']['split_strategy_seed'] if summary['config']['feynman']['split_strategy_seed'] is not None else 'per-benchmark-seed'}, "
            f"select_seed={summary['config']['feynman']['dataset_select_seed']}, "
            f"width_mid={summary['config']['feynman']['width_mid']}, "
            f"prune_iters={summary['config']['feynman']['prune_iters']}"
        )
    md_lines.extend(
        [
        "",
        "## Task-Level Aggregate Stats",
        "",
        "| task | n | teacher_cache_hit_mean | teacher_mse_mean | teacher_r2_mean | teacher_gate_pass_mean | baseline_symbolic_mean | icbr_symbolic_mean | delta_mean | delta_median | speedup_mean | speedup_median | mse_shift_mean | target_mse_shift_mean | formula_pass_mean |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for task_name in resolved_tasks:
        task_item = summary["aggregates"]["by_task"][task_name]
        metrics = task_item["metrics"]
        md_lines.append(
            "| "
            + f"{task_name} | "
            + f"{task_item['row_count']} | "
            + f"{metrics['teacher_cache_hit']['mean']:.4f} | "
            + f"{metrics['teacher_test_mse']['mean']:.6e} | "
            + f"{metrics['teacher_test_r2']['mean']:.6f} | "
            + f"{metrics['teacher_quality_gate_pass']['mean']:.4f} | "
            + f"{metrics['baseline_symbolic_wall_time_s']['mean']:.6f} | "
            + f"{metrics['symbolic_wall_time_s']['mean']:.6f} | "
            + f"{metrics['symbolic_wall_time_delta_s']['mean']:.6f} | "
            + f"{metrics['symbolic_wall_time_delta_s']['median']:.6f} | "
            + f"{metrics['symbolic_speedup_vs_baseline']['mean']:.4f} | "
            + f"{metrics['symbolic_speedup_vs_baseline']['median']:.4f} | "
            + f"{metrics['final_mse_loss_shift']['mean']:.6e} | "
            + f"{metrics['symbolic_target_mse_shift']['mean']:.6e} | "
            + f"{metrics['formula_validation_result']['mean']:.4f} |"
        )
    md_lines.append("")

    md_lines.extend(
        [
            "## Statistical Significance (by task)",
            "",
            "| task | metric | favorable_direction | n_total | n_finite | n_effective | improved | worsened | ties | p_value_two_sided | mean_delta_ci95 |",
            "|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|",
        ]
    )
    for task_name in resolved_tasks:
        sig_item = summary["aggregates"]["by_task"][task_name]["significance"]
        for metric_name in ["symbolic_wall_time_delta_s", "final_mse_loss_shift"]:
            metric_sig = sig_item[metric_name]
            ci = metric_sig["mean_delta_ci95"]
            md_lines.append(
                "| "
                + f"{task_name} | "
                + f"{metric_name} | "
                + f"{metric_sig['favorable_direction']} | "
                + f"{metric_sig['sample_count']} | "
                + f"{metric_sig['finite_count']} | "
                + f"{metric_sig['effective_count']} | "
                + f"{metric_sig['improved_count']} | "
                + f"{metric_sig['worsened_count']} | "
                + f"{metric_sig['tie_count']} | "
                + f"{metric_sig['sign_test_pvalue_two_sided']:.6f} | "
                + f"[{float(ci[0]):.6e}, {float(ci[1]):.6e}] |"
            )
    md_lines.append("")

    md_lines.extend(
        [
            "## Variant Ablation Aggregate Stats (Stage 15)",
            "",
            "| task | variant | n | teacher_gate_pass_mean | formula_pass_mean | symbolic_mean_s | speedup_mean_x | mse_shift_mean | target_mse_shift_mean | replay_rank_inversion_mean | refit_drift_l2_mean |",
            "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for task_name in resolved_tasks:
        task_variants = summary["aggregates"]["variant_ablation"]["by_task"][task_name]
        for variant_name in summary["config"]["variants"]:
            variant_item = task_variants[variant_name]
            metrics = variant_item["metrics"]
            md_lines.append(
                "| "
                + f"{task_name} | "
                + f"{variant_name} | "
                + f"{variant_item['row_count']} | "
                + f"{metrics['teacher_quality_gate_pass']['mean']:.4f} | "
                + f"{metrics['formula_validation_result']['mean']:.4f} | "
                + f"{metrics['symbolic_wall_time_s']['mean']:.6f} | "
                + f"{metrics['symbolic_speedup_vs_baseline']['mean']:.4f} | "
                + f"{metrics['final_mse_loss_shift']['mean']:.6e} | "
                + f"{metrics['symbolic_target_mse_shift']['mean']:.6e} | "
                + f"{metrics['replay_rank_inversion_rate']['mean']:.6f} | "
                + f"{metrics['commit_param_drift_l2_mean']['mean']:.6e} |"
            )
    md_lines.append("")

    md_lines.extend(
        [
            "## Critique Evidence Summary (Q1/Q2/Q3)",
            "",
            "| task | n | q1_candidate_ratio_mean | q1_symbolic_ratio_mean | q2_mse_gain_mean | q2_target_mse_gain_mean | q2_rank_inversion_mean | q3_mse_gain_mean | q3_target_mse_gain_mean | q3_refit_drift_mean |",
            "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
        ]
    )
    overall_evidence = summary["aggregates"]["challenge_evidence"]["overall"]
    md_lines.append(
        "| __overall__ | "
        + f"{int(overall_evidence['shared_tensor_candidate_time_ratio_no_shared_vs_full']['count'])} | "
        + f"{overall_evidence['shared_tensor_candidate_time_ratio_no_shared_vs_full']['mean']:.6f} | "
        + f"{overall_evidence['shared_tensor_symbolic_time_ratio_no_shared_vs_full']['mean']:.6f} | "
        + f"{overall_evidence['contextual_replay_mse_gain_full_vs_no_replay']['mean']:.6e} | "
        + f"{overall_evidence['contextual_replay_target_mse_gain_full_vs_no_replay']['mean']:.6e} | "
        + f"{overall_evidence['contextual_replay_rank_inversion_rate_full']['mean']:.6f} | "
        + f"{overall_evidence['explicit_commit_mse_gain_explicit_vs_refit']['mean']:.6e} | "
        + f"{overall_evidence['explicit_commit_target_mse_gain_explicit_vs_refit']['mean']:.6e} | "
        + f"{overall_evidence['explicit_commit_refit_commit_param_drift_l2_mean']['mean']:.6e} |"
    )
    for task_name in resolved_tasks:
        task_evidence = summary["aggregates"]["challenge_evidence"]["by_task"][task_name]
        md_lines.append(
            "| "
            + f"{task_name} | "
            + f"{int(task_evidence['shared_tensor_candidate_time_ratio_no_shared_vs_full']['count'])} | "
            + f"{task_evidence['shared_tensor_candidate_time_ratio_no_shared_vs_full']['mean']:.6f} | "
            + f"{task_evidence['shared_tensor_symbolic_time_ratio_no_shared_vs_full']['mean']:.6f} | "
            + f"{task_evidence['contextual_replay_mse_gain_full_vs_no_replay']['mean']:.6e} | "
            + f"{task_evidence['contextual_replay_target_mse_gain_full_vs_no_replay']['mean']:.6e} | "
            + f"{task_evidence['contextual_replay_rank_inversion_rate_full']['mean']:.6f} | "
            + f"{task_evidence['explicit_commit_mse_gain_explicit_vs_refit']['mean']:.6e} | "
            + f"{task_evidence['explicit_commit_target_mse_gain_explicit_vs_refit']['mean']:.6e} | "
            + f"{task_evidence['explicit_commit_refit_commit_param_drift_l2_mean']['mean']:.6e} |"
        )
    md_lines.append("")

    md_lines.extend(
        [
            "## Per-Run Performance Details",
            "",
            "| task | seed | cache_hit | cache_status | teacher_mse | teacher_r2 | teacher_gate | candidate_s | replay_s | baseline_symbolic_s | icbr_symbolic_s | speedup_x | baseline_mse | icbr_mse | mse_shift | baseline_target_mse | icbr_target_mse | target_mse_shift | formula_ok |",
            "|---|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for row in rows:
        md_lines.append(
            "| "
            + f"{row['task']} | {row['seed']} | "
            + f"{bool(row['teacher_cache_hit'])} | "
            + f"{row['teacher_cache_status']} | "
            + f"{float(row['teacher_test_mse']):.6e} | "
            + f"{float(row['teacher_test_r2']):.6f} | "
            + f"{bool(row['teacher_quality_gate_pass'])} | "
            + f"{float(row['candidate_generation_wall_time_s']):.6f} | "
            + f"{float(row['replay_rerank_wall_time_s']):.6f} | "
            + f"{float(row['baseline_symbolic_wall_time_s']):.6f} | "
            + f"{float(row['symbolic_wall_time_s']):.6f} | "
            + f"{float(row['symbolic_speedup_vs_baseline']):.4f} | "
            + f"{float(row['baseline_mse']):.6e} | "
            + f"{float(row['icbr_mse']):.6e} | "
            + f"{float(row['final_mse_loss_shift']):.6e} | "
            + f"{float(row['baseline_target_mse']):.6e} | "
            + f"{float(row['icbr_target_mse']):.6e} | "
            + f"{float(row['symbolic_target_mse_shift']):.6e} | "
            + f"{bool(row['formula_validation_result'])} |"
        )
    md_lines.append("")

    if bool(summary["config"]["feynman"]["enabled"]):
        md_lines.extend(["## Feynman Dataset Metadata", ""])
        for task_name in resolved_tasks:
            spec = specs[task_name]
            if spec.dataset_kind != "feynman_file":
                continue
            md_lines.append(f"### {task_name}")
            md_lines.append("")
            md_lines.append(f"- Dataset file: `{spec.dataset_filename}`")
            md_lines.append(f"- Dataset path: `{spec.dataset_path}`")
            md_lines.append(
                f"- Raw data shape: rows={spec.dataset_total_rows}, columns={spec.dataset_total_columns}, n_var={spec.n_var}"
            )
            md_lines.append(
                f"- Split setting: strategy={spec.dataset_split_strategy}, split_seed={row['feynman_split_seed']}, train_num={train_num}, test_num={test_num}"
            )
            md_lines.append(f"- Target formula: `{spec.target_formula}`")
            metadata = dict(spec.equation_metadata or {})
            if metadata:
                md_lines.append("- Equation metadata (from FeynmanEquations.csv):")
                for key, value in metadata.items():
                    md_lines.append(f"  - {key}: `{value}`")
            md_lines.append("")

    variant_rows_by_task_seed: dict[tuple[str, int], dict[str, dict[str, object]]] = {}
    for variant_row in variant_rows:
        key = (str(variant_row["task"]), int(variant_row["seed"]))
        variant_rows_by_task_seed.setdefault(key, {})[str(variant_row["variant"])] = variant_row

    def _fmt_float(value: object) -> str:
        number = float(value)
        if math.isfinite(number):
            return f"{number:.6e}"
        return "nan"

    md_lines.append("## Formula Comparison")
    md_lines.append("")
    for row in rows:
        task_name = str(row["task"])
        seed = int(row["seed"])
        variant_map = variant_rows_by_task_seed.get((task_name, seed), {})
        md_lines.append(f"### task={row['task']} seed={row['seed']}")
        md_lines.append("")
        md_lines.append(f"- Task source: {row['task_source']}")
        md_lines.append(f"- Target formula: `{row['target_formula']}`")
        md_lines.append(
            f"- Teacher cache: hit={bool(row['teacher_cache_hit'])}, "
            f"mode={row['teacher_cache_mode']}, status={row['teacher_cache_status']}"
        )
        md_lines.append(
            f"- Teacher quality gate: pass={bool(row['teacher_quality_gate_pass'])}; "
            f"reason=`{row['teacher_quality_gate_reason']}`"
        )
        md_lines.append(
            f"- Teacher target metrics: mse={float(row['teacher_target_mse']):.6e}, "
            f"r2={float(row['teacher_target_r2']):.6f}"
        )
        md_lines.append("- Variant formula overview:")
        for variant_name in summary["config"]["variants"]:
            variant = variant_map.get(str(variant_name))
            if variant is None:
                md_lines.append(f"  - {variant_name}: missing")
                continue
            md_lines.append(
                f"  - {variant_name}: symbolic_s={_fmt_float(variant['symbolic_wall_time_s'])}, "
                f"mse={_fmt_float(variant['mse'])}, "
                f"target_mse={_fmt_float(variant['target_mse'])}, "
                f"formula_ok={bool(variant['formula_validation_result'])}"
            )
        for variant_name in summary["config"]["variants"]:
            variant = variant_map.get(str(variant_name))
            if variant is None:
                continue
            display_formulas = list(variant.get("formula_display", []))
            formula_error = variant.get("formula_error")

            md_lines.append(f"- {variant_name} formula (display, rounded):")
            if display_formulas:
                for expr in display_formulas:
                    md_lines.append(f"  - `{expr}`")
            else:
                md_lines.append("  - `<none>`")

            if formula_error:
                md_lines.append(f"- {variant_name} formula export error: {formula_error}")
        md_lines.append("")

    md_lines.extend(["## Visualization Summary", ""])
    if visualization["enabled"]:
        for path in visualization["files"]:
            rel = str(Path(path).relative_to(output_dir))
            md_lines.append(f"- `{rel}`")
    else:
        md_lines.append(f"- Visualization disabled: {visualization['error']}")
    md_lines.append("")

    md_lines.extend(
        [
            "## Visualization Design Guide",
            "",
            "- `Point + 95% CI`: 适合论文里的主结论图；正值偏态指标优先用几何均值与 log 轴，不用柱面积暗示额外量感。",
            "- `Violin + Box + Points`: 适合 speedup / mse shift 这类分布图；当前固定 KDE 带宽规则为 `Silverman`。",
            "- `Task-Row Two-Panel Grid`: 适合 variant overview；每个 task 一行，左列 `SymbolicTime`，右列合并 `ImitationMSE + TargetMSE`，两列都显式标尺度。",
            "- `Q1/Q2/Q3`: 三个 panel 都用相对 `icbr_full` 的 ratio 值，并在 log 轴上展示 `几何均值 + 95% CI`，1 表示与 full 持平。",
            "- `Recommended Combo`: A=point+95%CI（正值偏态指标用几何均值），B=violin+box+points（分布），C=task-row two-panel grid（多指标 overview）。",
        ]
    )
    md_lines.append("")

    md_lines.extend(
        [
            "## Extensibility Notes",
            "",
            "- 任务可扩展：在任务解析层新增 task token 或 task spec，即可复用统一导出与统计管线。",
            "- 统计可扩展：新增 benchmark 指标后，可自动进入 task stats（count/mean/median/std/min/max）。",
            "- 显著性可扩展：可在 `_SIGNIFICANCE_DIRECTIONS` 增加需要方向性判断的 delta 指标。",
            "- 门禁可扩展：可在 `_TaskSpec` 中为单任务覆盖 teacher MSE/R2 阈值。",
        ]
    )
    (output_dir / "icbr_benchmark_summary.md").write_text("\n".join(md_lines) + "\n", encoding="utf-8")

    return {
        "rows": rows,
        "variant_rows": variant_rows,
        "summary": summary,
        "output_dir": str(output_dir),
    }


def _parse_int_list(text: str) -> list[int]:
    values = [item.strip() for item in text.split(",") if item.strip()]
    if not values:
        raise ValueError("Expected at least one integer value.")
    return [int(item) for item in values]


def _parse_str_list(text: str) -> list[str]:
    values = [item.strip() for item in text.split(",") if item.strip()]
    if not values:
        raise ValueError("Expected at least one task.")
    return values


def _normalize_variants(variants_raw: str | None) -> list[str]:
    if variants_raw is None:
        return ["baseline", "icbr_full"]
    parsed = _parse_str_list(variants_raw)
    deduped: list[str] = []
    seen: set[str] = set()
    for variant in parsed:
        if variant not in _BENCHMARK_VARIANTS:
            raise ValueError(f"Unknown benchmark variant: {variant}")
        if variant in seen:
            continue
        seen.add(variant)
        deduped.append(variant)
    if "baseline" not in seen:
        deduped.insert(0, "baseline")
    if "icbr_full" not in seen:
        deduped.append("icbr_full")
    return deduped


def _resolve_default_tasks_and_seeds(
    *,
    profile: str,
    tasks_raw: str | None,
    seeds_raw: str | None,
) -> tuple[list[str], list[int]]:
    if tasks_raw is None:
        if profile == "feynman_reference":
            tasks = ["feynman_paper10"]
        else:
            tasks = ["minimal", "combo", "poly_cubic", "trig_interaction"]
    else:
        tasks = _parse_str_list(tasks_raw)

    if seeds_raw is None:
        if profile == "feynman_reference":
            seeds = [1]
        else:
            seeds = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    else:
        seeds = _parse_int_list(seeds_raw)

    return tasks, seeds


def _resolve_training_config(
    *,
    profile: str,
    train_num: int | None,
    test_num: int | None,
    train_steps: int | None,
    lr: float | None,
    lamb: float | None,
) -> tuple[dict[str, float | int], dict[str, bool]]:
    if profile not in _BENCHMARK_PROFILES:
        raise ValueError(f"Unknown benchmark profile: {profile}")

    profile_defaults = _BENCHMARK_PROFILES[profile]
    resolved = {
        "train_num": int(profile_defaults["train_num"]) if train_num is None else int(train_num),
        "test_num": int(profile_defaults["test_num"]) if test_num is None else int(test_num),
        "train_steps": int(profile_defaults["train_steps"]) if train_steps is None else int(train_steps),
        "lr": float(profile_defaults["lr"]) if lr is None else float(lr),
        "lamb": float(profile_defaults["lamb"]) if lamb is None else float(lamb),
    }
    overridden = {
        "train_num": train_num is not None,
        "test_num": test_num is not None,
        "train_steps": train_steps is not None,
        "lr": lr is not None,
        "lamb": lamb is not None,
    }
    return resolved, overridden


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Run CPU benchmark for ICBR Phase I with extended multi-seed reporting.")
    parser.add_argument(
        "--profile",
        default="quick",
        choices=sorted(_BENCHMARK_PROFILES.keys()),
        help=(
            "Benchmark run profile: quick for smoke, quality for teacher-convergence verification, "
            "feynman_reference for README-style Feynman defaults."
        ),
    )
    parser.add_argument(
        "--tasks",
        default=None,
        help=(
            "Comma-separated tasks. "
            "Supports core tasks (minimal,combo,poly_cubic,trig_interaction), "
            "explicit feynman task names (e.g. feynman_I_10_7), "
            "and feynman task tokens (feynman_paper10, feynman_random)."
        ),
    )
    parser.add_argument(
        "--feynman-datasets",
        default="",
        help="Optional comma-separated explicit feynman datasets to append (e.g. feynman_I_10_7,feynman_II_6_15a).",
    )
    parser.add_argument(
        "--feynman-root",
        default="datasets",
        help="Root directory containing Feynman variants and optionally FeynmanEquations.csv.",
    )
    parser.add_argument(
        "--feynman-variant",
        default="Feynman_with_units",
        choices=list(_FEYNMAN_VARIANTS),
        help="Feynman dataset variant subdirectory.",
    )
    parser.add_argument(
        "--feynman-equations-csv",
        default=None,
        help="Optional FeynmanEquations.csv path. Defaults to <feynman_root>/FeynmanEquations.csv if present.",
    )
    parser.add_argument(
        "--feynman-max-datasets",
        type=int,
        default=10,
        help="Max datasets for feynman_random token.",
    )
    parser.add_argument(
        "--feynman-dataset-select-seed",
        type=int,
        default=1,
        help="Random selection seed for feynman_random token.",
    )
    parser.add_argument(
        "--feynman-split-strategy",
        default="random",
        choices=["random", "linspace"],
        help="Train/test split strategy for local Feynman files.",
    )
    parser.add_argument(
        "--feynman-split-strategy-seed",
        type=int,
        default=None,
        help=(
            "Random seed used by Feynman random split strategy. "
            "If omitted, each benchmark seed drives its own split."
        ),
    )
    parser.add_argument(
        "--feynman-width-mid",
        default="[5,2]",
        help=(
            "Hidden width spec inserted between input/output for feynman tasks. "
            "Examples: [5,2] -> width=[n_var,[5,2],1]; 5,3 -> width=[n_var,5,3,1]; "
            "[[5,2],3] -> width=[n_var,[5,2],3,1]."
        ),
    )
    parser.add_argument(
        "--feynman-post-prune-steps",
        type=int,
        default=None,
        help="Optional override for Feynman post-prune refit steps.",
    )
    parser.add_argument(
        "--feynman-post-prune-lr",
        type=float,
        default=None,
        help="Optional override for Feynman post-prune refit learning rate.",
    )
    parser.add_argument(
        "--feynman-post-prune-lamb",
        type=float,
        default=None,
        help="Optional override for Feynman post-prune refit lamb.",
    )
    parser.add_argument(
        "--feynman-post-prune-eval-every",
        type=int,
        default=None,
        help="Optional override for Feynman post-prune early-stop eval cadence.",
    )
    parser.add_argument(
        "--feynman-post-prune-min-delta",
        type=float,
        default=None,
        help="Optional override for Feynman post-prune early-stop min delta.",
    )
    parser.add_argument(
        "--feynman-post-prune-patience",
        type=int,
        default=None,
        help="Optional override for Feynman post-prune early-stop patience.",
    )
    parser.add_argument(
        "--feynman-fit-opt",
        default=None,
        choices=list(_FEYNMAN_FIT_OPTS),
        help="Optional override for Feynman teacher optimizer (Adam or LBFGS).",
    )
    parser.add_argument(
        "--prune-iters",
        type=int,
        default=None,
        help=(
            "Number of prune+refit rounds for teacher tuning. "
            "Defaults to 3 for Feynman tasks / feynman_reference, otherwise 1."
        ),
    )
    parser.add_argument(
        "--seeds",
        default=None,
        help="Comma-separated integer seeds. If omitted, profile-dependent defaults are used.",
    )
    parser.add_argument("--output-dir", default="outputs/icbr_benchmark_extended", help="Output directory")
    parser.add_argument(
        "--replot-only",
        action="store_true",
        help="Rebuild visualization PNGs from existing summary/rows/variant_rows without rerunning experiments.",
    )
    parser.add_argument(
        "--replot-summary-json",
        default=None,
        help="Existing summary JSON path for --replot-only. Defaults to <output-dir>/icbr_benchmark_summary.json.",
    )
    parser.add_argument(
        "--replot-rows-csv",
        default=None,
        help="Existing rows CSV path for --replot-only. Defaults to summary sibling icbr_benchmark_rows.csv.",
    )
    parser.add_argument(
        "--replot-variant-rows-csv",
        default=None,
        help="Existing variant rows CSV path for --replot-only. Defaults to summary sibling icbr_benchmark_variant_rows.csv.",
    )
    parser.add_argument("--train-num", type=int, default=None, help="Training sample count per task")
    parser.add_argument("--test-num", type=int, default=None, help="Test/calibration sample count per task")
    parser.add_argument("--train-steps", type=int, default=None, help="Teacher training steps")
    parser.add_argument("--lr", type=float, default=None, help="Teacher training learning rate")
    parser.add_argument("--lamb", type=float, default=None, help="Teacher sparsity regularization lambda")
    parser.add_argument("--topk", type=int, default=3, help="Replay shortlist size")
    parser.add_argument("--grid-number", type=int, default=21, help="Grid size for (a,b) search")
    parser.add_argument("--iteration", type=int, default=2, help="Zoom iterations for (a,b) search")
    parser.add_argument(
        "--variants",
        default=None,
        help=(
            "Comma-separated benchmark variants. Supported: "
            "baseline,icbr_full,icbr_no_replay,icbr_no_shared,icbr_refit_commit. "
            "baseline/icbr_full will be auto-included if omitted."
        ),
    )
    prune_group = parser.add_mutually_exclusive_group()
    prune_group.add_argument(
        "--enable-teacher-prune",
        action="store_true",
        help="Force-enable post-train prune for synthetic teacher tasks.",
    )
    prune_group.add_argument(
        "--disable-teacher-prune",
        action="store_true",
        help="Force-disable post-train prune for synthetic teacher tasks.",
    )
    parser.add_argument(
        "--teacher-prune-node-th",
        type=float,
        default=1e-2,
        help="Synthetic teacher prune node threshold when prune is enabled.",
    )
    parser.add_argument(
        "--teacher-prune-edge-th",
        type=float,
        default=1e-2,
        help="Synthetic teacher prune edge threshold when prune is enabled.",
    )
    parser.add_argument(
        "--teacher-max-test-mse",
        type=float,
        default=0.10,
        help="Default teacher quality gate: max allowed teacher test MSE before symbolic fitting.",
    )
    parser.add_argument(
        "--teacher-min-test-r2",
        type=float,
        default=0.75,
        help="Default teacher quality gate: min required teacher test R2 before symbolic fitting.",
    )
    parser.add_argument(
        "--teacher-cache-dir",
        default="outputs/teacher_cache",
        help="Persistent teacher cache directory used across benchmark runs.",
    )
    parser.add_argument(
        "--teacher-cache-mode",
        default="readwrite",
        choices=sorted(_TEACHER_CACHE_MODES),
        help="Teacher cache mode: readwrite, readonly, refresh, off.",
    )
    parser.add_argument(
        "--teacher-cache-version",
        default="v1",
        help="Teacher cache key version suffix for compatibility control.",
    )
    parser.add_argument("--no-plots", action="store_true", help="Disable plot generation")
    parser.add_argument("--quiet", action="store_true", help="Disable per-run progress prints")
    cli_tokens = list(argv) if argv is not None else list(os.sys.argv[1:])
    args = parser.parse_args(argv)

    if args.replot_only:
        if args.no_plots:
            raise ValueError("--replot-only cannot be combined with --no-plots.")
        summary_json_path = Path(args.replot_summary_json) if args.replot_summary_json else Path(args.output_dir) / "icbr_benchmark_summary.json"
        output_dir = Path(args.output_dir) if "--output-dir" in cli_tokens else summary_json_path.parent
        rows_csv = Path(args.replot_rows_csv) if args.replot_rows_csv else summary_json_path.with_name("icbr_benchmark_rows.csv")
        variant_rows_csv = (
            Path(args.replot_variant_rows_csv)
            if args.replot_variant_rows_csv
            else summary_json_path.with_name("icbr_benchmark_variant_rows.csv")
        )
        result = _replot_visualizations_from_artifacts(
            summary_json_path=summary_json_path,
            rows_csv=rows_csv,
            variant_rows_csv=variant_rows_csv,
            output_dir=output_dir,
        )
        if not args.quiet:
            visualization = result["visualization"]
            print(
                f"[icbr-benchmark] replot_only={bool(visualization.get('enabled'))} "
                f"files={len(list(visualization.get('files', [])))} output_dir={output_dir}"
            )
        return

    tasks, seeds = _resolve_default_tasks_and_seeds(
        profile=args.profile,
        tasks_raw=args.tasks,
        seeds_raw=args.seeds,
    )
    if args.feynman_datasets.strip():
        tasks.extend(_parse_str_list(args.feynman_datasets))
    output_dir = Path(args.output_dir)
    teacher_cache_dir = Path(args.teacher_cache_dir)
    feynman_root = Path(args.feynman_root)
    feynman_equations_csv = Path(args.feynman_equations_csv) if args.feynman_equations_csv else None
    feynman_width_mid = _parse_width_mid(args.feynman_width_mid)
    resolved_training, profile_overrides = _resolve_training_config(
        profile=args.profile,
        train_num=args.train_num,
        test_num=args.test_num,
        train_steps=args.train_steps,
        lr=args.lr,
        lamb=args.lamb,
    )
    variants = _normalize_variants(args.variants)
    enable_teacher_prune: bool | None = None
    if args.enable_teacher_prune:
        enable_teacher_prune = True
    elif args.disable_teacher_prune:
        enable_teacher_prune = False

    run_benchmark(
        tasks=tasks,
        seeds=seeds,
        output_dir=output_dir,
        train_num=int(resolved_training["train_num"]),
        test_num=int(resolved_training["test_num"]),
        train_steps=int(resolved_training["train_steps"]),
        lr=float(resolved_training["lr"]),
        lamb=float(resolved_training["lamb"]),
        topk=args.topk,
        grid_number=args.grid_number,
        iteration=args.iteration,
        teacher_max_test_mse=args.teacher_max_test_mse,
        teacher_min_test_r2=args.teacher_min_test_r2,
        teacher_cache_dir=teacher_cache_dir,
        teacher_cache_mode=args.teacher_cache_mode,
        teacher_cache_version=args.teacher_cache_version,
        profile_name=args.profile,
        profile_defaults=dict(_BENCHMARK_PROFILES[args.profile]),
        profile_overrides=profile_overrides,
        feynman_root=feynman_root,
        feynman_variant=args.feynman_variant,
        feynman_equations_csv=feynman_equations_csv,
        feynman_split_strategy=args.feynman_split_strategy,
        feynman_split_strategy_seed=args.feynman_split_strategy_seed,
        feynman_post_prune_steps=args.feynman_post_prune_steps,
        feynman_post_prune_lr=args.feynman_post_prune_lr,
        feynman_post_prune_lamb=args.feynman_post_prune_lamb,
        feynman_post_prune_eval_every=args.feynman_post_prune_eval_every,
        feynman_post_prune_min_delta=args.feynman_post_prune_min_delta,
        feynman_post_prune_patience=args.feynman_post_prune_patience,
        feynman_fit_opt=args.feynman_fit_opt,
        feynman_width_mid=feynman_width_mid,
        prune_iters=args.prune_iters,
        feynman_max_datasets=args.feynman_max_datasets,
        feynman_dataset_select_seed=args.feynman_dataset_select_seed,
        variants=variants,
        enable_teacher_prune=enable_teacher_prune,
        teacher_prune_node_th=args.teacher_prune_node_th,
        teacher_prune_edge_th=args.teacher_prune_edge_th,
        make_plots=not args.no_plots,
        quiet=args.quiet,
    )


if __name__ == "__main__":
    main()
