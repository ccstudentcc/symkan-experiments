from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import random
import statistics
import time
import warnings
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

import numpy as np
import torch

from kan.MultKAN import MultKAN
from kan.icbr import benchmark_icbr_vs_baseline
from kan.utils import create_dataset


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

_BENCHMARK_PROFILES: dict[str, dict[str, float | int]] = {
    "quick": {
        "train_num": 64,
        "test_num": 64,
        "train_steps": 20,
        "lr": 0.05,
        "lamb": 1e-3,
    },
    "quality": {
        "train_num": 1000,
        "test_num": 500,
        "train_steps": 80,
        "lr": 0.03,
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
_FEYNMAN_VARIANTS = (
    "Feynman_without_units",
    "Feynman_with_units",
    "bonus_without_units",
    "bonus_with_units",
)
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


@dataclass(frozen=True)
class _TaskSpec:
    name: str
    n_var: int
    width: list[int]
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


def _parse_width_mid(text: str) -> list[int]:
    values = [chunk.strip() for chunk in text.split(",") if chunk.strip()]
    if not values:
        raise ValueError("feynman_width_mid must contain at least one integer.")
    parsed = [int(value) for value in values]
    if any(value <= 0 for value in parsed):
        raise ValueError("feynman_width_mid values must be positive.")
    return parsed


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
    feynman_width_mid: list[int],
    feynman_split_strategy: str,
    feynman_split_strategy_seed: int,
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
    n_var = int(raw.shape[1] - 1)
    width = [n_var, *feynman_width_mid, 1]
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
        dataset_split_seed=int(feynman_split_strategy_seed),
        dataset_filename=filename,
        dataset_total_rows=int(raw.shape[0]),
        dataset_total_columns=int(raw.shape[1]),
        target_formula=equations_map.get(filename),
        equation_metadata=dict(equations_metadata_map.get(filename, {})),
        teacher_grid=20,
        teacher_k=3,
        teacher_fit_opt="Adam",
        teacher_post_train_prune=True,
        teacher_prune_node_th=1e-2,
        teacher_prune_edge_th=1e-2,
        teacher_post_prune_steps=100,
        teacher_post_prune_lr=1e-3,
        teacher_post_prune_lamb=1e-2,
        teacher_post_prune_early_stop=True,
        teacher_post_prune_eval_every=5,
        teacher_post_prune_min_delta=1e-6,
        teacher_post_prune_patience=2,
    )


def _resolve_task_specs(
    *,
    tasks: list[str],
    feynman_root: Path,
    feynman_variant: str,
    feynman_width_mid: list[int],
    feynman_split_strategy: str,
    feynman_split_strategy_seed: int,
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
        "split_strategy_seed": int(feynman_split_strategy_seed),
        "width_mid": feynman_width_mid,
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
    torch.manual_seed(seed)
    if spec.dataset_kind == "feynman_file":
        if spec.dataset_path is None:
            raise ValueError(f"Feynman task '{spec.name}' is missing dataset_path.")
        return _load_local_feynman_dataset_as_kan(
            dataset_path=Path(spec.dataset_path),
            split_seed=int(spec.dataset_split_seed) if spec.dataset_split_seed is not None else int(seed),
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


def _build_teacher_model(spec: _TaskSpec) -> MultKAN:
    return MultKAN(
        width=spec.width,
        grid=int(spec.teacher_grid),
        k=int(spec.teacher_k),
        auto_save=False,
        device="cpu",
    )


def _train_teacher_model(
    spec: _TaskSpec,
    dataset: dict[str, torch.Tensor],
    *,
    train_steps: int,
    lr: float,
    lamb: float,
) -> MultKAN:
    model = _build_teacher_model(spec)
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
    if spec.teacher_post_train_prune:
        try:
            model = model.prune(
                node_th=float(spec.teacher_prune_node_th),
                edge_th=float(spec.teacher_prune_edge_th),
            )
        except Exception as prune_exc:
            warnings.warn(
                f"Teacher prune failed for task={spec.name} with configured thresholds; "
                f"falling back to no-threshold prune. error={prune_exc!r}",
                RuntimeWarning,
            )
            try:
                model = model.prune(node_th=0.0, edge_th=0.0)
            except Exception as prune_fallback_exc:
                warnings.warn(
                    f"Fallback prune also failed for task={spec.name}; keep unpruned teacher model. "
                    f"error={prune_fallback_exc!r}",
                    RuntimeWarning,
                )
        post_prune_steps = int(spec.teacher_post_prune_steps)
        if post_prune_steps > 0:
            post_prune_lr = float(spec.teacher_post_prune_lr)
            post_prune_lamb = float(spec.teacher_post_prune_lamb)
            if bool(spec.teacher_post_prune_early_stop):
                eval_every = max(1, int(spec.teacher_post_prune_eval_every))
                patience = max(1, int(spec.teacher_post_prune_patience))
                min_delta = float(spec.teacher_post_prune_min_delta)
                remaining_steps = post_prune_steps
                prev_train_mse: float | None = None
                stable_checks = 0
                while remaining_steps > 0:
                    chunk_steps = min(eval_every, remaining_steps)
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
        "dataset_split_seed": (
            int(spec.dataset_split_seed) if spec.dataset_split_seed is not None else None
        ),
        "teacher_grid": int(spec.teacher_grid),
        "teacher_k": int(spec.teacher_k),
        "teacher_fit_opt": spec.teacher_fit_opt,
        "teacher_post_train_prune": bool(spec.teacher_post_train_prune),
        "teacher_prune_node_th": float(spec.teacher_prune_node_th),
        "teacher_prune_edge_th": float(spec.teacher_prune_edge_th),
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
            train_steps=train_steps,
            lr=lr,
            lamb=lamb,
        )

    if cache_mode in {"readwrite", "readonly"} and state_path.exists() and meta_path.exists():
        try:
            model = _build_teacher_model(spec)
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
    max_test_mse: float,
    min_test_r2: float,
) -> tuple[bool, str]:
    gate_failures: list[str] = []
    if not math.isfinite(teacher_test_mse) or teacher_test_mse > max_test_mse:
        gate_failures.append(f"teacher_test_mse={teacher_test_mse:.6g} > {max_test_mse:.6g}")
    if not math.isfinite(teacher_test_r2) or teacher_test_r2 < min_test_r2:
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
) -> dict[str, object]:
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception as exc:  # pragma: no cover - depends on local matplotlib availability
        return {"enabled": False, "error": f"{type(exc).__name__}: {exc}", "files": []}

    created_files: list[str] = []

    def _finite_metric_values(task: str, metric: str) -> list[float]:
        values: list[float] = []
        for row in by_task_rows[task]:
            value = float(row[metric])
            if math.isfinite(value):
                values.append(value)
        return values

    def _safe_mean_std(values: list[float]) -> tuple[float, float]:
        if not values:
            return float("nan"), float("nan")
        if len(values) == 1:
            return float(values[0]), 0.0
        return float(statistics.mean(values)), float(statistics.stdev(values))

    fig, ax = plt.subplots(figsize=(10, 4.5))
    x_positions = list(range(len(tasks)))
    baseline_mean, baseline_std, icbr_mean, icbr_std = [], [], [], []
    for task in tasks:
        base_mean, base_std = _safe_mean_std(_finite_metric_values(task, "baseline_symbolic_wall_time_s"))
        icbr_m, icbr_s = _safe_mean_std(_finite_metric_values(task, "symbolic_wall_time_s"))
        baseline_mean.append(base_mean)
        baseline_std.append(base_std)
        icbr_mean.append(icbr_m)
        icbr_std.append(icbr_s)
    if not all(math.isfinite(value) for value in (baseline_mean + baseline_std + icbr_mean + icbr_std)):
        plt.close(fig)
        return {
            "enabled": False,
            "error": "Insufficient finite symbolic timing metrics for plot generation (likely skipped by teacher quality gate).",
            "files": created_files,
        }
    bar_width = 0.36
    ax.bar(
        [x - bar_width / 2.0 for x in x_positions],
        baseline_mean,
        width=bar_width,
        yerr=baseline_std,
        capsize=4,
        label="Baseline symbolic time",
    )
    ax.bar(
        [x + bar_width / 2.0 for x in x_positions],
        icbr_mean,
        width=bar_width,
        yerr=icbr_std,
        capsize=4,
        label="ICBR symbolic time",
    )
    ax.set_xticks(x_positions)
    ax.set_xticklabels(tasks, rotation=20)
    ax.set_ylabel("seconds")
    ax.set_title("Symbolic Wall Time by Task (mean ± std)")
    ax.legend()
    time_plot = output_dir / "icbr_benchmark_symbolic_time_errorbar.png"
    fig.tight_layout()
    fig.savefig(time_plot, dpi=160)
    plt.close(fig)
    created_files.append(str(time_plot))

    fig, ax = plt.subplots(figsize=(10, 4.5))
    speedup_data = [_finite_metric_values(task, "symbolic_speedup_vs_baseline") for task in tasks]
    if any(len(values) == 0 for values in speedup_data):
        plt.close(fig)
        return {
            "enabled": False,
            "error": "Insufficient finite symbolic metrics for plot generation (likely skipped by teacher quality gate).",
            "files": created_files,
        }
    ax.boxplot(speedup_data, labels=tasks, showmeans=True)
    ax.set_ylabel("speedup x")
    ax.set_title("ICBR Speedup vs Baseline (seed distribution)")
    ax.grid(axis="y", alpha=0.3)
    speedup_plot = output_dir / "icbr_benchmark_speedup_boxplot.png"
    fig.tight_layout()
    fig.savefig(speedup_plot, dpi=160)
    plt.close(fig)
    created_files.append(str(speedup_plot))

    fig, ax = plt.subplots(figsize=(10, 4.5))
    mse_shift_data = [_finite_metric_values(task, "final_mse_loss_shift") for task in tasks]
    if any(len(values) == 0 for values in mse_shift_data):
        plt.close(fig)
        return {
            "enabled": False,
            "error": "Insufficient finite mse shift metrics for plot generation (likely skipped by teacher quality gate).",
            "files": created_files,
        }
    ax.boxplot(mse_shift_data, labels=tasks, showmeans=True)
    ax.axhline(0.0, linestyle="--", linewidth=1.0, color="black", alpha=0.7)
    ax.set_ylabel("icbr_mse - baseline_mse")
    ax.set_title("MSE Shift by Task (seed distribution)")
    ax.grid(axis="y", alpha=0.3)
    mse_plot = output_dir / "icbr_benchmark_mse_shift_boxplot.png"
    fig.tight_layout()
    fig.savefig(mse_plot, dpi=160)
    plt.close(fig)
    created_files.append(str(mse_plot))

    return {"enabled": True, "error": None, "files": created_files}


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
    feynman_split_strategy_seed: int = 1,
    feynman_width_mid: list[int] | None = None,
    feynman_max_datasets: int = 10,
    feynman_dataset_select_seed: int = 1,
    make_plots: bool,
    quiet: bool,
) -> dict[str, object]:
    if feynman_variant not in _FEYNMAN_VARIANTS:
        raise ValueError(f"Unsupported feynman variant: {feynman_variant}")
    if feynman_split_strategy not in {"random", "linspace"}:
        raise ValueError(f"Unsupported feynman split strategy: {feynman_split_strategy}")
    if int(feynman_split_strategy_seed) < 0:
        raise ValueError("feynman_split_strategy_seed must be >= 0.")
    if feynman_width_mid is None:
        feynman_width_mid = [5, 2]

    resolved_tasks, specs, _equations_map, feynman_config = _resolve_task_specs(
        tasks=tasks,
        feynman_root=feynman_root,
        feynman_variant=feynman_variant,
        feynman_width_mid=feynman_width_mid,
        feynman_split_strategy=feynman_split_strategy,
        feynman_split_strategy_seed=int(feynman_split_strategy_seed),
        feynman_max_datasets=feynman_max_datasets,
        feynman_dataset_select_seed=feynman_dataset_select_seed,
        feynman_equations_csv=feynman_equations_csv,
    )

    output_dir.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, object]] = []

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
                else float(teacher_min_test_r2)
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
                metrics = benchmark_icbr_vs_baseline(
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
                )
            else:
                metrics = _build_skipped_symbolic_metrics(reason=teacher_quality_gate_reason)
            row = {
                "task": task_name,
                "seed": seed,
                "task_kind": spec.dataset_kind,
                "task_source": "feynman_file" if spec.dataset_kind == "feynman_file" else "synthetic_formula",
                "target_formula": spec.target_formula,
                "feynman_dataset_filename": spec.dataset_filename,
                "feynman_dataset_rows": spec.dataset_total_rows,
                "feynman_dataset_columns": spec.dataset_total_columns,
                "feynman_split_seed": spec.dataset_split_seed,
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

    by_task_rows = {task_name: [row for row in rows if row["task"] == task_name] for task_name in resolved_tasks}
    by_task_metrics = {task_name: _build_metric_stats(task_rows) for task_name, task_rows in by_task_rows.items()}
    overall_metrics = _build_metric_stats(rows)
    by_task_significance = {
        task_name: _build_significance(task_rows, task_label=task_name) for task_name, task_rows in by_task_rows.items()
    }
    overall_significance = _build_significance(rows, task_label="__overall__")

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
        visualization = _generate_visualizations(output_dir=output_dir, tasks=resolved_tasks, by_task_rows=by_task_rows)

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
                            else float(teacher_min_test_r2)
                        ),
                    }
                    for task_name in resolved_tasks
                },
                "policy": "skip_symbolic_comparison_when_teacher_quality_fails",
            },
            "teacher_training": {
                task_name: {
                    "grid": int(specs[task_name].teacher_grid),
                    "k": int(specs[task_name].teacher_k),
                    "opt": specs[task_name].teacher_fit_opt,
                    "post_train_prune": bool(specs[task_name].teacher_post_train_prune),
                    "prune_node_th": float(specs[task_name].teacher_prune_node_th),
                    "prune_edge_th": float(specs[task_name].teacher_prune_edge_th),
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
        },
        "artifacts": {
            "rows_csv": str(rows_csv),
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
                "stats_schema": "Each metric includes count | mean | median | std | min | max",
            },
            "significance_guide": {
                "sign_test_pvalue_two_sided": "Two-sided sign test p-value on non-tie seeds.",
                "mean_delta_ci95": "Bootstrap 95% CI of mean delta across seeds.",
            },
            "teacher_quality_gate": {
                "pass_rule": "teacher_test_mse <= threshold_mse AND teacher_test_r2 >= threshold_r2",
                "failure_policy": "Skip baseline/ICBR symbolic comparison for that row and keep explicit gate reason.",
            },
            "teacher_cache": {
                "cache_key_rule": "hash(task, seed, width, dataset_kind, dataset_path, dataset_variant, dataset_split_strategy, dataset_split_seed, teacher_grid, teacher_k, teacher_fit_opt, teacher_post_train_prune, teacher_prune_node_th, teacher_prune_edge_th, teacher_post_prune_steps, teacher_post_prune_lr, teacher_post_prune_lamb, teacher_post_prune_early_stop, teacher_post_prune_eval_every, teacher_post_prune_min_delta, teacher_post_prune_patience, train_num, test_num, train_steps, lr, lamb, profile, cache_version)",
                "modes": {
                    "readwrite": "Read cache when available; train+write on miss.",
                    "readonly": "Read cache only; train without writing on miss.",
                    "refresh": "Ignore old cache and retrain, then overwrite cache.",
                    "off": "Disable cache and always train.",
                },
            },
            "teacher_training": {
                "feynman_reference_policy": "For feynman_file tasks: train -> prune(node_th=1e-2, edge_th=1e-2) -> refit(steps=100, lr=1e-3, lamb=1e-2, early_stop_check_every=5) -> cache.",
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
    ]
    if bool(summary["config"]["feynman"]["enabled"]):
        md_lines.append(
            f"- Feynman data: root={summary['config']['feynman']['root']}, "
            f"variant={summary['config']['feynman']['variant']}, "
            f"split={summary['config']['feynman']['split_strategy']}, "
            f"split_seed={summary['config']['feynman']['split_strategy_seed']}, "
            f"select_seed={summary['config']['feynman']['dataset_select_seed']}, "
            f"width_mid={summary['config']['feynman']['width_mid']}"
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
                f"- Split setting: strategy={spec.dataset_split_strategy}, split_seed={spec.dataset_split_seed}, train_num={train_num}, test_num={test_num}"
            )
            md_lines.append(f"- Target formula: `{spec.target_formula}`")
            metadata = dict(spec.equation_metadata or {})
            if metadata:
                md_lines.append("- Equation metadata (from FeynmanEquations.csv):")
                for key, value in metadata.items():
                    md_lines.append(f"  - {key}: `{value}`")
            md_lines.append("")

    md_lines.append("## Formula Comparison")
    md_lines.append("")
    for row in rows:
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
        md_lines.append("- Baseline formula (display, rounded):")
        for expr in row["baseline_formula_display"]:
            md_lines.append(f"  - `{expr}`")
        md_lines.append("- ICBR formula (display, rounded):")
        for expr in row["icbr_formula_display"]:
            md_lines.append(f"  - `{expr}`")
        md_lines.append("- Baseline formula (raw):")
        for expr in row["baseline_formula_raw"]:
            md_lines.append(f"  - `{expr}`")
        md_lines.append("- ICBR formula (raw):")
        for expr in row["icbr_formula_raw"]:
            md_lines.append(f"  - `{expr}`")
        if row["baseline_formula_error"] or row["icbr_formula_error"]:
            md_lines.append(f"- Formula export error baseline={row['baseline_formula_error']}, icbr={row['icbr_formula_error']}")
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
            "## Extensibility Notes",
            "",
            "- 任务可扩展：在任务解析层新增 task token 或 task spec，即可复用统一导出与统计管线。",
            "- 统计可扩展：新增 benchmark 指标后，可自动进入 task stats（count/mean/median/std/min/max）。",
            "- 显著性可扩展：可在 `_SIGNIFICANCE_DIRECTIONS` 增加需要方向性判断的 delta 指标。",
            "- 门禁可扩展：可在 `_TaskSpec` 中为单任务覆盖 teacher MSE/R2 阈值。",
        ]
    )
    (output_dir / "icbr_benchmark_summary.md").write_text("\n".join(md_lines) + "\n", encoding="utf-8")

    return {"rows": rows, "summary": summary, "output_dir": str(output_dir)}


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
        default=1,
        help="Random seed used by feynman random split strategy.",
    )
    parser.add_argument(
        "--feynman-width-mid",
        default="5,2",
        help="Comma-separated hidden widths used for feynman tasks, e.g. 5,2 -> width=[n_var,5,2,1].",
    )
    parser.add_argument(
        "--seeds",
        default=None,
        help="Comma-separated integer seeds. If omitted, profile-dependent defaults are used.",
    )
    parser.add_argument("--output-dir", default="outputs/icbr_benchmark_extended", help="Output directory")
    parser.add_argument("--train-num", type=int, default=None, help="Training sample count per task")
    parser.add_argument("--test-num", type=int, default=None, help="Test/calibration sample count per task")
    parser.add_argument("--train-steps", type=int, default=None, help="Teacher training steps")
    parser.add_argument("--lr", type=float, default=None, help="Teacher training learning rate")
    parser.add_argument("--lamb", type=float, default=None, help="Teacher sparsity regularization lambda")
    parser.add_argument("--topk", type=int, default=3, help="Replay shortlist size")
    parser.add_argument("--grid-number", type=int, default=21, help="Grid size for (a,b) search")
    parser.add_argument("--iteration", type=int, default=2, help="Zoom iterations for (a,b) search")
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
    args = parser.parse_args(argv)

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
        feynman_width_mid=feynman_width_mid,
        feynman_max_datasets=args.feynman_max_datasets,
        feynman_dataset_select_seed=args.feynman_dataset_select_seed,
        make_plots=not args.no_plots,
        quiet=args.quiet,
    )


if __name__ == "__main__":
    main()
