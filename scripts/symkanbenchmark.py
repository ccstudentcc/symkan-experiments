from __future__ import annotations

import argparse
import os
import json
import math
import time
import warnings
from contextlib import contextmanager, redirect_stderr, redirect_stdout
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd
import torch
from scipy.special import softmax as scipy_softmax
from sklearn.datasets import fetch_openml

from kan import KAN
from symkan.core import (
    build_dataset,
    get_device,
    get_n_edge,
    model_acc,
    model_acc_ds,
    model_acc_ds_fast,
    model_logits,
    safe_fit,
    set_device,
)
from symkan.config import AppConfig, ConfigError, load_config
from symkan.core.runtime import default_batch_size, resolve_device
from symkan.eval import compute_multiclass_roc_auc, validate_formula_numerically
from symkan.io import save_export_bundle, save_stage_logs, save_symbolic_summary
from symkan.pruning import safe_attribute
from symkan.symbolic import (
    EXPRESSIVE_LIB,
    FAST_LIB,
    LIB_HIDDEN,
    LIB_OUTPUT,
    collect_all_formulas,
    format_expr,
    symbolize_pipeline,
)
from symkan.symbolic.pipeline import symbolize_pipeline_report
from symkan.tuning import stagewise_train_report
from scripts.project_paths import (
    DEFAULT_BENCHMARK_RUNS_DIR,
    LEGACY_BENCHMARK_RUNS_DIR,
    resolve_preferred_dir,
)

try:
    import psutil
except Exception:
    psutil = None

try:
    import symkan.eval.metrics as eval_metrics_module
except Exception:
    eval_metrics_module = None


DEFAULT_TASKS = ("full", "eval-bench", "parallel-bench")
DEFAULT_PARALLEL_MODES = ("auto", "off", "thread4")

DEFAULT_DATA_DIR = "data"
DEFAULT_X_TRAIN = str(Path(DEFAULT_DATA_DIR) / "X_train.npy")
DEFAULT_X_TEST = str(Path(DEFAULT_DATA_DIR) / "X_test.npy")
DEFAULT_Y_TRAIN = str(Path(DEFAULT_DATA_DIR) / "Y_train_cat.npy")
DEFAULT_Y_TEST = str(Path(DEFAULT_DATA_DIR) / "Y_test_cat.npy")

LEGACY_X_TRAIN = "X_train.npy"
LEGACY_X_TEST = "X_test.npy"
LEGACY_Y_TRAIN = "Y_train_cat.npy"
LEGACY_Y_TEST = "Y_test_cat.npy"
_MNIST_FALLBACK_EXCEPTIONS = (ImportError, ModuleNotFoundError, OSError, RuntimeError, ValueError)


@dataclass
class BenchmarkRunnerConfig:
    config_path: Optional[str]
    tasks: str
    output_dir: str
    stagewise_seeds: str
    save_bundle: bool
    quiet: bool
    verbose: bool
    bench_repeat: int
    bench_warmup: int
    eval_rounds: int
    parallel_modes: str
    parallel_target_min: int
    parallel_target_max: int
    parallel_max_prune_rounds: int
    parallel_finetune_steps: int
    parallel_layerwise_finetune_steps: int
    parallel_affine_finetune_steps: int
    parallel_prune_eval_interval: int
    parallel_prune_attr_sample_adaptive: bool
    parallel_prune_attr_sample_min: int
    parallel_prune_attr_sample_max: int
    parallel_heavy_ft_patience: int
    parallel_heavy_ft_min_delta: float
    device: Optional[str] = None
    global_seed: Optional[int] = None
    baseline_seed: Optional[int] = None
    batch_size: Optional[int] = None
    lib_preset: Optional[str] = None
    disable_stagewise_train: Optional[bool] = None
    max_prune_rounds: Optional[int] = None
    layerwise_finetune_steps: Optional[int] = None
    layerwise_finetune_lamb: Optional[float] = None
    layerwise_use_validation: Optional[bool] = None
    layerwise_validation_ratio: Optional[float] = None
    layerwise_validation_seed: Optional[int] = None
    layerwise_early_stop_patience: Optional[int] = None
    layerwise_early_stop_min_delta: Optional[float] = None
    layerwise_eval_interval: Optional[int] = None
    layerwise_validation_n_sample: Optional[int] = None
    input_compaction: Optional[bool] = None
    prune_collapse_floor: Optional[float] = None
    symbolic_prune_adaptive_acc_drop_tol: Optional[float] = None
    validate_n_sample: Optional[int] = None


def parse_csv_list(raw: str) -> List[str]:
    return [item.strip() for item in raw.split(",") if item.strip()]


def parse_csv_ints(raw: str) -> List[int]:
    return [int(item) for item in parse_csv_list(raw)]


def parse_csv_floats(raw: str) -> List[float]:
    return [float(item) for item in parse_csv_list(raw)]


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


@contextmanager
def maybe_silent(enabled: bool):
    if not enabled:
        yield
        return
    with open(os.devnull, "w", encoding="utf-8") as sink:
        with redirect_stdout(sink), redirect_stderr(sink):
            yield


def set_global_seed(seed: int) -> None:
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def resolve_path(raw: str, base_dir: Path) -> Path:
    candidate = Path(raw)
    if candidate.is_absolute():
        return candidate
    return (base_dir / candidate).resolve()


def _is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def _validate_autofetch_targets(config: AppConfig, repo_root: Path, missing_files: List[Path]) -> None:
    if not missing_files or config.data.allow_auto_fetch_outside_data_dir:
        return

    data_root = (repo_root / DEFAULT_DATA_DIR).resolve()
    invalid = [str(path) for path in missing_files if not _is_relative_to(path, data_root)]
    if invalid:
        raise ConfigError(
            "auto_fetch_mnist may only create missing files under "
            f"'{data_root}' by default; set data.allow_auto_fetch_outside_data_dir=true "
            f"to opt in for custom targets: {invalid}"
        )


def to_jsonable(value: Any) -> Any:
    if isinstance(value, (np.floating, np.integer)):
        return value.item()
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, pd.DataFrame):
        return value.to_dict(orient="records")
    if isinstance(value, pd.Series):
        return value.to_dict()
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, dict):
        return {str(k): to_jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [to_jsonable(v) for v in value]
    return value


def write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.write_text(json.dumps(to_jsonable(payload), ensure_ascii=False, indent=2), encoding="utf-8")


def _select_classes(x: np.ndarray, y: np.ndarray, classes: List[int]) -> tuple[np.ndarray, np.ndarray]:
    mask = np.zeros_like(y, dtype=bool)
    for cls in classes:
        mask |= y == cls
    return x[mask], y[mask]


def _onehot_from_labels(y: np.ndarray, classes: List[int]) -> np.ndarray:
    class_to_idx = {cls: idx for idx, cls in enumerate(classes)}
    mapped = np.array([class_to_idx[int(v)] for v in y], dtype=np.int64)
    return np.eye(len(classes), dtype=np.float32)[mapped]


def _fetch_mnist_via_keras(classes: List[int]) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    from tensorflow import keras  # type: ignore

    (x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()
    x_train = x_train.reshape(x_train.shape[0], -1).astype(np.float32) / 255.0
    x_test = x_test.reshape(x_test.shape[0], -1).astype(np.float32) / 255.0
    y_train = y_train.astype(np.int64)
    y_test = y_test.astype(np.int64)
    x_train, y_train = _select_classes(x_train, y_train, classes)
    x_test, y_test = _select_classes(x_test, y_test, classes)
    y_train_onehot = _onehot_from_labels(y_train, classes)
    y_test_onehot = _onehot_from_labels(y_test, classes)
    return x_train, x_test, y_train_onehot, y_test_onehot


def _fetch_mnist_via_openml(classes: List[int]) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    mnist = fetch_openml("mnist_784", version=1, as_frame=False)
    x = mnist.data.astype(np.float32) / 255.0
    y = mnist.target.astype(np.int64)
    x_train, x_test = x[:60000], x[60000:]
    y_train, y_test = y[:60000], y[60000:]
    x_train, y_train = _select_classes(x_train, y_train, classes)
    x_test, y_test = _select_classes(x_test, y_test, classes)
    y_train_onehot = _onehot_from_labels(y_train, classes)
    y_test_onehot = _onehot_from_labels(y_test, classes)
    return x_train, x_test, y_train_onehot, y_test_onehot


def _fetch_mnist_with_fallback(classes: List[int]) -> tuple[tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray], str]:
    keras_error_message = ""
    try:
        return _fetch_mnist_via_keras(classes), "tensorflow.keras.datasets.mnist"
    except _MNIST_FALLBACK_EXCEPTIONS as keras_exc:
        keras_error_message = str(keras_exc)
        warnings.warn(
            f"[data] keras MNIST fetch failed ({keras_exc}); falling back to OpenML.",
            category=UserWarning,
            stacklevel=2,
        )

    try:
        return _fetch_mnist_via_openml(classes), "sklearn.fetch_openml(mnist_784)"
    except _MNIST_FALLBACK_EXCEPTIONS as openml_exc:
        raise RuntimeError(
            "automatic MNIST fetch failed via tensorflow.keras.datasets.mnist "
            f"({keras_error_message}) and sklearn.fetch_openml(mnist_784) ({openml_exc})"
        ) from openml_exc


def ensure_numpy_dataset_files(config: AppConfig, repo_root: Path) -> None:
    # Backward-compat: if user kept the old root-level *.npy files and didn't
    # override the new default paths, transparently use the legacy locations.
    legacy_pairs = [
        ("x_train", DEFAULT_X_TRAIN, LEGACY_X_TRAIN),
        ("x_test", DEFAULT_X_TEST, LEGACY_X_TEST),
        ("y_train", DEFAULT_Y_TRAIN, LEGACY_Y_TRAIN),
        ("y_test", DEFAULT_Y_TEST, LEGACY_Y_TEST),
    ]
    for attr, default_raw, legacy_raw in legacy_pairs:
        raw = str(getattr(config.data, attr))
        if raw != default_raw:
            continue
        new_path = resolve_path(default_raw, repo_root)
        if new_path.exists():
            continue
        legacy_path = resolve_path(legacy_raw, repo_root)
        if legacy_path.exists():
            setattr(config.data, attr, legacy_raw)

    x_train_path = resolve_path(config.data.x_train, repo_root)
    x_test_path = resolve_path(config.data.x_test, repo_root)
    y_train_path = resolve_path(config.data.y_train, repo_root)
    y_test_path = resolve_path(config.data.y_test, repo_root)
    expected_files = [x_train_path, x_test_path, y_train_path, y_test_path]
    missing_files = [path for path in expected_files if not path.exists()]
    if not missing_files:
        return
    if not config.data.auto_fetch_mnist:
        raise FileNotFoundError(
            "缺少输入数据文件，且已禁用自动拉取 MNIST: " + ", ".join(str(path) for path in missing_files)
        )

    _validate_autofetch_targets(config, repo_root, missing_files)

    for path in missing_files:
        ensure_dir(path.parent)

    classes = sorted(set(int(v) for v in config.data.mnist_classes))
    if not classes:
        raise ValueError("--mnist-classes 不能为空")

    (x_train, x_test, y_train, y_test), source = _fetch_mnist_with_fallback(classes)

    np.save(x_train_path, x_train.astype(np.float32))
    np.save(x_test_path, x_test.astype(np.float32))
    np.save(y_train_path, y_train.astype(np.float32))
    np.save(y_test_path, y_test.astype(np.float32))
    print(
        "[data] 已自动生成数据文件: "
        f"{x_train_path.name}, {x_test_path.name}, {y_train_path.name}, {y_test_path.name} "
        f"(source={source}, classes={classes})"
    )


def load_data(config: AppConfig, repo_root: Path) -> Dict[str, Any]:
    ensure_numpy_dataset_files(config, repo_root)
    x_train = np.load(resolve_path(config.data.x_train, repo_root)).astype(np.float32)
    x_test = np.load(resolve_path(config.data.x_test, repo_root)).astype(np.float32)
    y_train_raw = np.load(resolve_path(config.data.y_train, repo_root))
    y_test_raw = np.load(resolve_path(config.data.y_test, repo_root))

    if y_train_raw.ndim > 1:
        y_train = np.argmax(y_train_raw, axis=1).astype(np.int64)
        y_test = np.argmax(y_test_raw, axis=1).astype(np.int64)
        n_classes = int(y_train_raw.shape[1])
    else:
        y_train = y_train_raw.astype(np.int64)
        y_test = y_test_raw.astype(np.int64)
        n_classes = int(np.max(y_train) + 1)

    y_train_onehot = np.eye(n_classes, dtype=np.float32)[y_train]
    y_test_onehot = np.eye(n_classes, dtype=np.float32)[y_test]

    return {
        "X_train": x_train,
        "X_test": x_test,
        "y_train": y_train,
        "y_test": y_test,
        "Y_train": y_train_onehot,
        "Y_test": y_test_onehot,
        "input_dim": int(x_train.shape[1]),
        "n_classes": n_classes,
    }


def resolve_tasks(raw: str) -> List[str]:
    tasks = parse_csv_list(raw)
    if not tasks or "all" in tasks:
        return list(DEFAULT_TASKS)
    valid = set(DEFAULT_TASKS)
    unknown = [task for task in tasks if task not in valid]
    if unknown:
        raise ValueError(f"unknown tasks: {unknown}")
    return tasks


def resolve_parallel_modes(raw: str) -> List[Dict[str, Any]]:
    specs: List[Dict[str, Any]] = []
    for name in parse_csv_list(raw):
        if name == "auto":
            specs.append({"name": "auto", "parallel_mode": "auto", "parallel_workers": None})
            continue
        if name == "off":
            specs.append({"name": "off", "parallel_mode": "off", "parallel_workers": 1})
            continue
        if name.startswith("thread"):
            suffix = name.replace("thread", "", 1)
            workers = int(suffix) if suffix else 4
            specs.append({"name": name, "parallel_mode": "thread", "parallel_workers": workers})
            continue
        raise ValueError(f"unknown parallel mode spec: {name}")
    if not specs:
        return resolve_parallel_modes(",".join(DEFAULT_PARALLEL_MODES))
    return specs


def resolve_library(lib_preset: str) -> Dict[str, Any]:
    if lib_preset == "layered":
        return {"lib": None, "lib_hidden": LIB_HIDDEN, "lib_output": LIB_OUTPUT, "label": "layered"}
    if lib_preset == "fast":
        return {"lib": FAST_LIB, "lib_hidden": None, "lib_output": None, "label": "fast"}
    if lib_preset in {"expressive", "full"}:
        return {"lib": EXPRESSIVE_LIB, "lib_hidden": None, "lib_output": None, "label": lib_preset}
    raise ValueError(f"unknown lib preset: {lib_preset}")


def build_runtime_app_config(
    config: AppConfig,
    width: List[int],
    stage_seed: int,
    batch_size: int,
    library_cfg: Dict[str, Any],
) -> AppConfig:
    stage_update = {
        "width": width,
        "grid": config.model.grid,
        "k": config.model.k,
        "seed": stage_seed,
        "batch_size": batch_size,
        "validation_seed": (
            config.stagewise.validation_seed
            if config.stagewise.validation_seed is not None
            else config.runtime.global_seed
        ),
        "verbose": bool(config.runtime.verbose and not config.runtime.quiet),
    }
    symbolize_update = {
        "batch_size": batch_size,
        "layerwise_validation_seed": (
            config.symbolize.layerwise_validation_seed
            if config.symbolize.layerwise_validation_seed is not None
            else config.runtime.global_seed
        ),
        "verbose": bool(config.runtime.verbose and not config.runtime.quiet),
    }
    if config.symbolize.lib is None and config.symbolize.lib_hidden is None and config.symbolize.lib_output is None:
        symbolize_update.update(
            {
                "lib": library_cfg["lib"],
                "lib_hidden": library_cfg["lib_hidden"],
                "lib_output": library_cfg["lib_output"],
            }
        )

    return config.model_copy(
        update={
            "stagewise": config.stagewise.model_copy(update=stage_update),
            "symbolize": config.symbolize.model_copy(update=symbolize_update),
        }
    )


def apply_benchmark_overrides(config: AppConfig, args: BenchmarkRunnerConfig) -> AppConfig:
    runtime_update: dict[str, Any] = {}
    library_update: dict[str, Any] = {}
    workflow_update: dict[str, Any] = {}
    evaluation_update: dict[str, Any] = {}
    symbolize_update: dict[str, Any] = {}

    if args.device is not None:
        runtime_update["device"] = args.device
    if args.global_seed is not None:
        runtime_update["global_seed"] = args.global_seed
    if args.baseline_seed is not None:
        runtime_update["baseline_seed"] = args.baseline_seed
    if args.batch_size is not None:
        runtime_update["batch_size"] = args.batch_size
    runtime_update["quiet"] = args.quiet
    runtime_update["verbose"] = False if args.quiet else args.verbose

    if args.lib_preset is not None:
        library_update["lib_preset"] = args.lib_preset
    if args.disable_stagewise_train is not None:
        workflow_update["disable_stagewise_train"] = args.disable_stagewise_train
    if args.max_prune_rounds is not None:
        symbolize_update["max_prune_rounds"] = args.max_prune_rounds
    if args.layerwise_finetune_steps is not None:
        symbolize_update["layerwise_finetune_steps"] = args.layerwise_finetune_steps
    if args.layerwise_finetune_lamb is not None:
        symbolize_update["layerwise_finetune_lamb"] = args.layerwise_finetune_lamb
    if args.layerwise_use_validation is not None:
        symbolize_update["layerwise_use_validation"] = args.layerwise_use_validation
    if args.layerwise_validation_ratio is not None:
        symbolize_update["layerwise_validation_ratio"] = args.layerwise_validation_ratio
    if args.layerwise_validation_seed is not None:
        symbolize_update["layerwise_validation_seed"] = args.layerwise_validation_seed
    if args.layerwise_early_stop_patience is not None:
        symbolize_update["layerwise_early_stop_patience"] = args.layerwise_early_stop_patience
    if args.layerwise_early_stop_min_delta is not None:
        symbolize_update["layerwise_early_stop_min_delta"] = args.layerwise_early_stop_min_delta
    if args.layerwise_eval_interval is not None:
        symbolize_update["layerwise_eval_interval"] = args.layerwise_eval_interval
    if args.layerwise_validation_n_sample is not None:
        symbolize_update["layerwise_validation_n_sample"] = args.layerwise_validation_n_sample
    if args.input_compaction is not None:
        symbolize_update["enable_input_compaction"] = args.input_compaction
    if args.prune_collapse_floor is not None:
        symbolize_update["prune_collapse_floor"] = args.prune_collapse_floor
    if args.symbolic_prune_adaptive_acc_drop_tol is not None:
        symbolize_update["prune_adaptive_acc_drop_tol"] = args.symbolic_prune_adaptive_acc_drop_tol
    if args.validate_n_sample is not None:
        evaluation_update["validate_n_sample"] = args.validate_n_sample

    updates: dict[str, Any] = {}
    if runtime_update:
        updates["runtime"] = config.runtime.model_copy(update=runtime_update)
    if library_update:
        updates["library"] = config.library.model_copy(update=library_update)
    if workflow_update:
        updates["workflow"] = config.workflow.model_copy(update=workflow_update)
    if evaluation_update:
        updates["evaluation"] = config.evaluation.model_copy(update=evaluation_update)
    if symbolize_update:
        updates["symbolize"] = config.symbolize.model_copy(update=symbolize_update)
    if not updates:
        return config
    return config.model_copy(update=updates)


def load_benchmark_app_config(config_path: Optional[str], args: BenchmarkRunnerConfig) -> AppConfig:
    default_config_path = Path(__file__).resolve().parents[1] / "configs" / "symkanbenchmark.default.yaml"
    base_config = load_config(config_path) if config_path else load_config(default_config_path)
    return apply_benchmark_overrides(base_config, args)


def build_formula_summary(
    formulas: Any,
    valid_exprs: List[Dict[str, Any]],
    roc_data: Dict[int, Dict[str, Any]],
    n_classes: int,
) -> pd.DataFrame:
    all_formulas = collect_all_formulas(formulas)
    valid_idx = {item["index"] for item in valid_exprs}
    rows = []
    for class_idx in range(n_classes):
        formula_info = next((item for item in all_formulas if item["index"] == class_idx), None)
        if formula_info and formula_info["index"] in valid_idx:
            expr_full = formula_info["expr"]
            expr_display = format_expr(expr_full, n_digits=2)
            complexity = int(formula_info["complexity"])
        else:
            expr_full = "N/A (零或常数)"
            expr_display = "N/A"
            complexity = 0
        auc_value = float(roc_data[class_idx]["auc"]) if class_idx in roc_data else math.nan
        rows.append(
            {
                "类别": class_idx,
                "表达式": expr_display,
                "复杂度": complexity,
                "AUC": round(auc_value, 4) if not math.isnan(auc_value) else math.nan,
                "expr_full": expr_full,
            }
        )
    return pd.DataFrame(rows)


def benchmark_callable(name: str, fn, repeat: int = 3, warmup: int = 1) -> Dict[str, Any]:
    for _ in range(max(0, warmup)):
        fn()

    times: List[float] = []
    rss_deltas: List[float] = []
    gpu_peaks: List[float] = []
    last_output = None

    for _ in range(max(1, repeat)):
        if torch.cuda.is_available():
            torch.cuda.reset_peak_memory_stats()
            torch.cuda.synchronize()

        rss_before = rss_mb()
        t0 = time.perf_counter()
        last_output = fn()
        if torch.cuda.is_available():
            torch.cuda.synchronize()
        elapsed = time.perf_counter() - t0
        rss_after = rss_mb()

        times.append(float(elapsed))
        if np.isfinite(rss_before) and np.isfinite(rss_after):
            rss_deltas.append(float(rss_after - rss_before))
        else:
            rss_deltas.append(float("nan"))
        if torch.cuda.is_available():
            gpu_peaks.append(float(torch.cuda.max_memory_allocated() / (1024 ** 2)))
        else:
            gpu_peaks.append(float("nan"))

    return {
        "name": name,
        "time_mean_s": float(np.mean(times)),
        "time_std_s": float(np.std(times)),
        "rss_delta_mean_mb": safe_nanmean(rss_deltas),
        "gpu_peak_mean_mb": safe_nanmean(gpu_peaks),
        "last_output": last_output,
    }


def rss_mb() -> float:
    if psutil is None:
        return float("nan")
    return float(psutil.Process().memory_info().rss / (1024 ** 2))


def safe_nanmean(values: List[float]) -> float:
    arr = np.asarray(values, dtype=float)
    if arr.size == 0 or not np.isfinite(arr).any():
        return float("nan")
    return float(np.nanmean(arr))


def export_multi_round_reports(multi_round_raw: pd.DataFrame, output_dir: Path) -> pd.DataFrame:
    multi_round_summary = (
        multi_round_raw.groupby("name", as_index=False)
        .agg(
            time_mean_s=("time_mean_s", "mean"),
            time_std_s=("time_mean_s", "std"),
            rss_delta_mean_mb=("rss_delta_mean_mb", "mean"),
            gpu_peak_mean_mb=("gpu_peak_mean_mb", "mean"),
        )
    )

    if (multi_round_summary["name"] == "legacy_numpy_path").any():
        legacy_t = float(multi_round_summary.loc[multi_round_summary["name"] == "legacy_numpy_path", "time_mean_s"].iloc[0])
        multi_round_summary["vs_legacy_time_reduction_pct"] = (
            (legacy_t - multi_round_summary["time_mean_s"]) / legacy_t * 100.0
        )

    if (multi_round_summary["name"] == "validate_formula_first").any():
        first_t = float(
            multi_round_summary.loc[multi_round_summary["name"] == "validate_formula_first", "time_mean_s"].iloc[0]
        )
        mask = multi_round_summary["name"].isin(["validate_formula_first", "validate_formula_cached"])
        multi_round_summary.loc[mask, "vs_first_validate_reduction_pct"] = (
            (first_t - multi_round_summary.loc[mask, "time_mean_s"]) / first_t * 100.0
        )

    multi_round_summary = multi_round_summary.sort_values("time_mean_s", ascending=True).reset_index(drop=True)

    raw_csv = output_dir / "benchmark_multi_round_raw.csv"
    cn_csv = output_dir / "benchmark_multi_round_summary_cn.csv"
    en_csv = output_dir / "benchmark_multi_round_summary_en.csv"

    summary_en = multi_round_summary.rename(
        columns={
            "name": "metric_name",
            "time_mean_s": "time_mean_s",
            "time_std_s": "time_std_s",
            "rss_delta_mean_mb": "rss_delta_mean_mb",
            "gpu_peak_mean_mb": "gpu_peak_mean_mb",
            "vs_legacy_time_reduction_pct": "vs_legacy_time_reduction_pct",
            "vs_first_validate_reduction_pct": "vs_first_validate_reduction_pct",
        }
    )
    summary_cn = multi_round_summary.rename(
        columns={
            "name": "指标项",
            "time_mean_s": "平均耗时(秒)",
            "time_std_s": "耗时标准差(秒)",
            "rss_delta_mean_mb": "RSS平均变化(MB)",
            "gpu_peak_mean_mb": "GPU峰值显存均值(MB)",
            "vs_legacy_time_reduction_pct": "相对legacy耗时降幅(%)",
            "vs_first_validate_reduction_pct": "相对首次公式验证降幅(%)",
        }
    )

    name_map_cn = {
        "legacy_numpy_path": "旧评估路径（NumPy往返）",
        "fast_tensor_path": "新评估路径（Tensor快路径）",
        "model_acc_ds_current": "当前默认评估接口",
        "validate_formula_first": "公式验证（首次编译）",
        "validate_formula_cached": "公式验证（缓存复用）",
    }
    summary_cn["指标项"] = summary_cn["指标项"].map(lambda item: name_map_cn.get(item, item))

    for frame in (summary_en, summary_cn):
        for column in frame.columns:
            if getattr(frame[column].dtype, "kind", "") in {"f", "c"}:
                frame[column] = frame[column].round(6)

    multi_round_raw.to_csv(raw_csv, index=False, encoding="utf-8-sig")
    summary_cn.to_csv(cn_csv, index=False, encoding="utf-8-sig")
    summary_en.to_csv(en_csv, index=False, encoding="utf-8-sig")

    return multi_round_summary


def run_eval_benchmarks(context: Dict[str, Any], config: BenchmarkRunnerConfig, output_dir: Path) -> Dict[str, Any]:
    enhanced_model = context["enhanced_model"]
    export_model = context["export_model"]
    export_formulas = context["export_formulas"]
    dataset_enhanced = context["dataset_enhanced"]

    x_np = dataset_enhanced["test_input"].detach().cpu().numpy()
    y_np = np.argmax(dataset_enhanced["test_label"].detach().cpu().numpy(), axis=1)

    bench_rows = [
        benchmark_callable("legacy_numpy_path", lambda: model_acc(enhanced_model, x_np, y_np), repeat=config.bench_repeat, warmup=config.bench_warmup),
        benchmark_callable(
            "fast_tensor_path",
            lambda: model_acc_ds_fast(enhanced_model, dataset_enhanced),
            repeat=config.bench_repeat,
            warmup=config.bench_warmup,
        ),
        benchmark_callable(
            "model_acc_ds_current",
            lambda: model_acc_ds(enhanced_model, dataset_enhanced),
            repeat=config.bench_repeat,
            warmup=config.bench_warmup,
        ),
    ]

    if export_formulas is not None:
        bench_rows.append(
            benchmark_callable(
                "validate_formula_first",
                lambda: validate_formula_numerically(
                    export_model,
                    export_formulas,
                    dataset_enhanced,
                    n_sample=context["app_config"].evaluation.validate_n_sample,
                ),
                repeat=1,
                warmup=0,
            )
        )
        bench_rows.append(
            benchmark_callable(
                "validate_formula_cached",
                lambda: validate_formula_numerically(
                    export_model,
                    export_formulas,
                    dataset_enhanced,
                    n_sample=context["app_config"].evaluation.validate_n_sample,
                ),
                repeat=1,
                warmup=0,
            )
        )

    benchmark_df = pd.DataFrame([{k: v for k, v in row.items() if k != "last_output"} for row in bench_rows])
    benchmark_df.to_csv(output_dir / "benchmark_single_round.csv", index=False, encoding="utf-8-sig")

    all_round_rows: List[Dict[str, Any]] = []
    for round_id in range(1, config.eval_rounds + 1):
        round_rows = [
            benchmark_callable("legacy_numpy_path", lambda: model_acc(enhanced_model, x_np, y_np), repeat=config.bench_repeat, warmup=config.bench_warmup),
            benchmark_callable(
                "fast_tensor_path",
                lambda: model_acc_ds_fast(enhanced_model, dataset_enhanced),
                repeat=config.bench_repeat,
                warmup=config.bench_warmup,
            ),
            benchmark_callable(
                "model_acc_ds_current",
                lambda: model_acc_ds(enhanced_model, dataset_enhanced),
                repeat=config.bench_repeat,
                warmup=config.bench_warmup,
            ),
        ]

        if export_formulas is not None:
            if eval_metrics_module is not None and hasattr(eval_metrics_module, "_LAMBDA_CACHE"):
                eval_metrics_module._LAMBDA_CACHE.clear()
            round_rows.append(
                benchmark_callable(
                    "validate_formula_first",
                    lambda: validate_formula_numerically(
                        export_model,
                        export_formulas,
                        dataset_enhanced,
                        n_sample=context["app_config"].evaluation.validate_n_sample,
                    ),
                    repeat=1,
                    warmup=0,
                )
            )
            round_rows.append(
                benchmark_callable(
                    "validate_formula_cached",
                    lambda: validate_formula_numerically(
                        export_model,
                        export_formulas,
                        dataset_enhanced,
                        n_sample=context["app_config"].evaluation.validate_n_sample,
                    ),
                    repeat=1,
                    warmup=0,
                )
            )

        for row in round_rows:
            clean_row = {k: v for k, v in row.items() if k != "last_output"}
            clean_row["round"] = round_id
            all_round_rows.append(clean_row)

    multi_round_raw = pd.DataFrame(all_round_rows)
    multi_round_summary = export_multi_round_reports(multi_round_raw, output_dir)
    return {
        "single_round": benchmark_df,
        "multi_round_raw": multi_round_raw,
        "multi_round_summary": multi_round_summary,
    }


def run_parallel_benchmark(context: Dict[str, Any], config: BenchmarkRunnerConfig, output_dir: Path) -> pd.DataFrame:
    enhanced_model = context["enhanced_model"]
    dataset_enhanced = context["dataset_enhanced"]
    batch_size = context["batch_size"]
    library_cfg = context["library_cfg"]
    silent = bool(config.quiet)

    edge_now = int(get_n_edge(enhanced_model))
    target_quick = max(config.parallel_target_min, min(config.parallel_target_max, edge_now))
    base_symbolize_config = context["app_config"].symbolize
    rows: List[Dict[str, Any]] = []

    for cfg in resolve_parallel_modes(config.parallel_modes):
        quick_symbolize_config = base_symbolize_config.model_copy(
            update={
                "target_edges": target_quick,
                "max_prune_rounds": config.parallel_max_prune_rounds,
                "finetune_steps": config.parallel_finetune_steps,
                "layerwise_finetune_steps": config.parallel_layerwise_finetune_steps,
                "affine_finetune_steps": config.parallel_affine_finetune_steps,
                "prune_eval_interval": config.parallel_prune_eval_interval,
                "prune_attr_sample_adaptive": config.parallel_prune_attr_sample_adaptive,
                "prune_attr_sample_min": config.parallel_prune_attr_sample_min,
                "prune_attr_sample_max": config.parallel_prune_attr_sample_max,
                "heavy_ft_early_stop_patience": config.parallel_heavy_ft_patience,
                "heavy_ft_early_stop_min_delta": config.parallel_heavy_ft_min_delta,
                "parallel_mode": cfg["parallel_mode"],
                "parallel_workers": cfg["parallel_workers"],
                "verbose": False,
            }
        )
        quick_app_config = context["app_config"].model_copy(
            update={"symbolize": quick_symbolize_config.model_copy(update={"batch_size": batch_size})}
        )
        t0 = time.perf_counter()
        with maybe_silent(silent):
            out = symbolize_pipeline_report(enhanced_model, dataset_enhanced, quick_app_config)
        wall_time = time.perf_counter() - t0
        timing = out.timing
        symbolic_time = timing.get("symbolic_total_seconds", float("nan"))
        rows.append(
            {
                "mode": cfg["name"],
                "parallel_mode": cfg["parallel_mode"],
                "parallel_workers_effective": out.sym_stats.get("parallel_workers"),
                "target_edges": int(target_quick),
                "wall_time_s": float(wall_time),
                "symbolic_time_s": float(symbolic_time) if symbolic_time == symbolic_time else float("nan"),
                "final_acc": float(out.final_acc),
                "final_n_edge": int(out.final_n_edge),
            }
        )

    parallel_df = pd.DataFrame(rows).sort_values("wall_time_s").reset_index(drop=True)
    if (parallel_df["mode"] == "off").any():
        base = float(parallel_df.loc[parallel_df["mode"] == "off", "wall_time_s"].iloc[0])
    else:
        base = float(parallel_df["wall_time_s"].iloc[0])
    parallel_df["vs_off_speedup_x"] = base / parallel_df["wall_time_s"]
    parallel_df.to_csv(output_dir / "benchmark_symbolic_parallel_quick.csv", index=False, encoding="utf-8-sig")
    return parallel_df


def run_single_experiment(
    config: AppConfig,
    runner: BenchmarkRunnerConfig,
    repo_root: Path,
    run_index: int,
    total_runs: int,
    stage_seed: int,
) -> Dict[str, Any]:
    run_dir = ensure_dir(Path(runner.output_dir) / f"run_{run_index:02d}_seed{stage_seed}")

    set_global_seed(config.runtime.global_seed)
    device = str(resolve_device(config.runtime.device))
    set_device(device)
    batch_size = (
        int(config.runtime.batch_size)
        if config.runtime.batch_size and config.runtime.batch_size > 0
        else int(default_batch_size())
    )
    library_cfg = resolve_library(config.library.lib_preset)
    data = load_data(config, repo_root)
    silent = bool(config.runtime.quiet)

    dataset_full = build_dataset(data["X_train"], data["Y_train"], data["X_test"], data["Y_test"])
    inner_dim = int(config.model.inner_dim)
    width_base = [data["input_dim"], inner_dim, data["n_classes"]]

    base_model = KAN(
        width=width_base,
        grid=config.model.grid,
        k=config.model.k,
        seed=config.runtime.baseline_seed,
        auto_save=False,
        symbolic_enabled=True,
        save_act=True,
        device=get_device(),
    )
    with maybe_silent(silent):
        base_res = safe_fit(
            base_model,
            dataset_full,
            opt="Adam",
            steps=config.model.baseline_steps,
            lr=config.model.baseline_lr,
            lamb=config.model.baseline_lamb,
            batch=batch_size,
            update_grid=True,
            singularity_avoiding=True,
            log=config.model.baseline_log,
        )
    base_acc = float(model_acc(base_model, data["X_test"], data["y_test"]))

    feature_score = safe_attribute(base_model, dataset_full)
    top_k = min(int(config.model.top_k), data["input_dim"])
    keep_idx = np.sort(np.argsort(-feature_score)[:top_k])
    x_train_sel = data["X_train"][:, keep_idx]
    x_test_sel = data["X_test"][:, keep_idx]
    dataset_enhanced = build_dataset(x_train_sel, data["Y_train"], x_test_sel, data["Y_test"])
    app_config = build_runtime_app_config(
        config,
        width=[int(x_train_sel.shape[1]), inner_dim, data["n_classes"]],
        stage_seed=stage_seed,
        batch_size=batch_size,
        library_cfg=library_cfg,
    )

    stage_fallback_t0 = time.perf_counter()
    if config.workflow.disable_stagewise_train:
        enhanced_model = KAN(
            width=[int(x_train_sel.shape[1]), inner_dim, data["n_classes"]],
            grid=config.model.grid,
            k=config.model.k,
            seed=stage_seed,
            auto_save=False,
            symbolic_enabled=True,
            save_act=True,
            device=get_device(),
        )
        e2e_steps = (
            int(config.workflow.e2e_steps)
            if int(config.workflow.e2e_steps) > 0
            else int(len(config.stagewise.lr_schedule) * config.stagewise.steps_per_stage)
        )
        e2e_lr = (
            float(config.workflow.e2e_lr)
            if float(config.workflow.e2e_lr) > 0
            else float(np.median(config.stagewise.lr_schedule))
        )
        e2e_lamb = (
            float(config.workflow.e2e_lamb)
            if float(config.workflow.e2e_lamb) >= 0
            else float(np.median(config.stagewise.lamb_schedule))
        )
        with maybe_silent(silent):
            e2e_res = safe_fit(
                enhanced_model,
                dataset_enhanced,
                opt="Adam",
                steps=e2e_steps,
                lr=e2e_lr,
                lamb=e2e_lamb,
                batch=batch_size,
                update_grid=True,
                singularity_avoiding=True,
                log=max(1, e2e_steps // 10),
            )
        stage_total_seconds = float(time.perf_counter() - stage_fallback_t0)
        enhanced_res = {
            "train_loss": list(e2e_res.get("train_loss", [])),
            "test_loss": list(e2e_res.get("test_loss", [])),
            "stage_logs": [
                {
                    "stage": 0,
                    "lamb": float(e2e_lamb),
                    "effective_lamb": float(e2e_lamb),
                    "lr": float(e2e_lr),
                    "acc_before": float("nan"),
                    "acc_after": float(model_acc_ds(enhanced_model, dataset_enhanced)),
                    "edges_before": float("nan"),
                    "edges_after": int(get_n_edge(enhanced_model)),
                    "prune_accepted": False,
                    "prune_attempts": [],
                    "prune_attempt_count": 0,
                    "rollback": "",
                    "prune_th": float("nan"),
                    "sym_score": float("nan"),
                    "train_seconds": float(stage_total_seconds),
                    "prune_seconds": 0.0,
                    "stage_seconds": float(stage_total_seconds),
                }
            ],
            "best_acc": float(model_acc_ds(enhanced_model, dataset_enhanced)),
            "selected_stage": "e2e",
            "selected_edges": int(get_n_edge(enhanced_model)),
            "selected_score": float("nan"),
            "stage_snapshots": [],
            "stage_early_stopped": False,
            "stage_early_stop_reason": "",
            "stage_timings": [
                {
                    "stage": 0,
                    "train_seconds": float(stage_total_seconds),
                    "prune_seconds": 0.0,
                    "stage_seconds": float(stage_total_seconds),
                }
            ],
            "stage_train_total_seconds": float(stage_total_seconds),
            "stage_prune_total_seconds": 0.0,
            "final_finetune_seconds": 0.0,
            "stage_total_seconds": float(stage_total_seconds),
        }
    else:
        with maybe_silent(silent):
            enhanced_model, enhanced_res = stagewise_train_report(dataset_enhanced, app_config)
    stage_result = enhanced_res.to_legacy_dict() if hasattr(enhanced_res, "to_legacy_dict") else enhanced_res
    enhanced_acc = float(model_acc_ds(enhanced_model, dataset_enhanced))
    stage_logs = enhanced_res.stage_logs if hasattr(enhanced_res, "stage_logs") else stage_result.get("stage_logs", [])
    stage_df = pd.DataFrame(stage_logs)
    save_stage_logs(stage_df, csv_path=str(run_dir / "kan_stage_logs.csv"))

    export_t0 = time.perf_counter()
    with maybe_silent(silent):
        export_result = symbolize_pipeline_report(enhanced_model, dataset_enhanced, app_config)
    export_wall_time = float(time.perf_counter() - export_t0)
    symbolize_result = export_result.to_legacy_dict() if hasattr(export_result, "to_legacy_dict") else export_result

    export_model = export_result.model
    export_formulas = export_result.formulas
    valid_exprs = export_result.valid_expressions
    trace_df = export_result.trace
    trace_df.to_csv(run_dir / "symbolize_trace.csv", index=False, encoding="utf-8-sig")

    val_df = validate_formula_numerically(
        export_model,
        export_formulas,
        dataset_enhanced,
        n_sample=config.evaluation.validate_n_sample,
    )
    if val_df is not None:
        val_df.to_csv(run_dir / "formula_validation.csv", index=False, encoding="utf-8-sig")

    logits_sym = model_logits(export_model, x_test_sel)
    y_prob_sym = scipy_softmax(logits_sym, axis=1)
    roc_data = compute_multiclass_roc_auc(dataset_enhanced["test_label"].detach().cpu().numpy(), y_prob_sym)
    auc_macro = float(np.mean([roc_data[class_idx]["auc"] for class_idx in range(data["n_classes"])]))

    summary_df = build_formula_summary(export_formulas, valid_exprs, roc_data, data["n_classes"])
    save_symbolic_summary(summary_df, csv_path=str(run_dir / "kan_symbolic_summary.csv"))
    valid_complexity = summary_df.loc[summary_df["expr_full"] != "N/A (零或常数)", "复杂度"]
    expr_complexity_mean = float(valid_complexity.mean()) if len(valid_complexity) > 0 else float("nan")

    stage_total_seconds = float(stage_result.get("stage_total_seconds", time.perf_counter() - stage_fallback_t0))
    stage_train_total_seconds = float(stage_result.get("stage_train_total_seconds", float("nan")))
    stage_prune_total_seconds = float(stage_result.get("stage_prune_total_seconds", float("nan")))
    stage_final_finetune_seconds = float(stage_result.get("final_finetune_seconds", float("nan")))

    roc_rows = [
        {"class": class_idx, "auc": float(roc_data[class_idx]["auc"])} for class_idx in range(data["n_classes"])
    ]
    pd.DataFrame(roc_rows).to_csv(run_dir / "roc_auc_summary.csv", index=False, encoding="utf-8-sig")

    if runner.save_bundle:
        save_export_bundle(
            {
                "config": {**config.model_dump(), "stage_seed": stage_seed, "device": get_device()},
                "baseline_result": base_res,
                "stagewise_result": stage_result,
                "symbolize_result": symbolize_result,
                "formula_summary": summary_df,
                "validation": val_df,
            },
            path=str(run_dir / "symkanbenchmark_bundle.pkl"),
        )

    metrics = {
        "run_index": run_index,
        "total_runs": total_runs,
        "stage_seed": stage_seed,
        "device": get_device(),
        "batch_size": batch_size,
        "lib_preset": config.library.lib_preset,
        "base_acc": base_acc,
        "base_n_edge": int(get_n_edge(base_model)),
        "selected_input_dim": int(len(keep_idx)),
        "enhanced_acc": enhanced_acc,
        "enhanced_n_edge": int(get_n_edge(enhanced_model)),
        "selected_stage": stage_result.get("selected_stage"),
        "selected_score": float(stage_result.get("selected_score", float("nan"))),
        "final_acc": float(symbolize_result.get("final_acc", float("nan"))),
        "final_n_edge": int(symbolize_result.get("final_n_edge", -1)),
        "effective_target_edges": int(symbolize_result.get("effective_target_edges", -1)),
        "effective_input_dim": int(symbolize_result.get("effective_input_dim", -1)),
        "valid_expression_count": int(len(valid_exprs)),
        "expr_complexity_mean": expr_complexity_mean,
        "macro_auc": auc_macro,
        "validation_mean_r2": float(val_df["r2"].mean()) if val_df is not None and len(val_df) > 0 else float("nan"),
        "validation_negative_r2_count": int((val_df["r2"] < 0).sum()) if val_df is not None and len(val_df) > 0 else 0,
        "stage_total_seconds": stage_total_seconds,
        "stage_train_total_seconds": stage_train_total_seconds,
        "stage_prune_total_seconds": stage_prune_total_seconds,
        "stage_final_finetune_seconds": stage_final_finetune_seconds,
        "symbolic_total_seconds": float(symbolize_result.get("timing", {}).get("symbolic_total_seconds", float("nan"))),
        "export_wall_time_s": export_wall_time,
        "pre_symbolic_n_edge": int(symbolize_result.get("input_n_edge", get_n_edge(enhanced_model))),
        "pre_symbolic_too_dense": int(symbolize_result.get("input_n_edge", get_n_edge(enhanced_model))) > int(config.stagewise.target_edges) * 2,
        "stagewise_enabled": bool(not config.workflow.disable_stagewise_train),
        "input_compaction_enabled": bool(config.symbolize.enable_input_compaction),
        "layerwise_finetune_steps": int(config.symbolize.layerwise_finetune_steps),
        "layerwise_finetune_lr": float(config.symbolize.layerwise_finetune_lr),
        "layerwise_finetune_lamb": float(config.symbolize.layerwise_finetune_lamb),
        "layerwise_use_validation": bool(config.symbolize.layerwise_use_validation),
        "layerwise_validation_ratio": float(config.symbolize.layerwise_validation_ratio),
        "layerwise_validation_seed": (
            config.symbolize.layerwise_validation_seed
            if config.symbolize.layerwise_validation_seed is not None
            else config.runtime.global_seed
        ),
        "layerwise_early_stop_patience": int(config.symbolize.layerwise_early_stop_patience),
        "layerwise_early_stop_min_delta": float(config.symbolize.layerwise_early_stop_min_delta),
        "layerwise_eval_interval": int(config.symbolize.layerwise_eval_interval),
        "layerwise_validation_n_sample": int(config.symbolize.layerwise_validation_n_sample),
        "output_dir": str(run_dir),
    }
    write_json(run_dir / "metrics.json", {"metrics": metrics, "roc": roc_rows})

    return {
        "run_dir": run_dir,
        "metrics": metrics,
        "context": {
            "enhanced_model": enhanced_model,
            "export_model": export_model,
            "export_formulas": export_formulas,
            "dataset_enhanced": dataset_enhanced,
            "batch_size": batch_size,
            "library_cfg": library_cfg,
            "app_config": app_config,
        },
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Notebook-aligned symkan benchmark runner.")
    parser.add_argument("--config", default=None, help="AppConfig YAML 路径；脚本会先 load_config() 再应用显式覆盖")
    parser.add_argument("--tasks", default="all", help="full,eval-bench,parallel-bench 或 all")
    parser.add_argument("--output-dir", default=DEFAULT_BENCHMARK_RUNS_DIR, help="输出目录")
    parser.add_argument("--stagewise-seeds", default="42", help="逗号分隔的 stagewise 种子列表")
    parser.add_argument("--save-bundle", action="store_true", help="额外导出 pkl bundle")
    parser.add_argument("--verbose", action="store_true", help="打印 stagewise 与 symbolize 详细日志")
    parser.add_argument("--quiet", action="store_true", help="静默运行，屏蔽训练与符号化过程输出")
    parser.add_argument("--device", default=None, help="显式覆盖 runtime.device")
    parser.add_argument("--global-seed", type=int, default=None, help="显式覆盖 runtime.global_seed")
    parser.add_argument("--baseline-seed", type=int, default=None, help="显式覆盖 runtime.baseline_seed")
    parser.add_argument("--batch-size", type=int, default=None, help="显式覆盖 runtime.batch_size")
    parser.add_argument("--lib-preset", choices=["layered", "fast", "expressive", "full"], default=None)
    parser.add_argument("--disable-stagewise-train", action=argparse.BooleanOptionalAction, default=None)
    parser.add_argument("--max-prune-rounds", type=int, default=None, help="显式覆盖 symbolize.max_prune_rounds")
    parser.add_argument("--layerwise-finetune-steps", type=int, default=None)
    parser.add_argument("--layerwise-finetune-lamb", type=float, default=None)
    parser.add_argument("--layerwise-use-validation", action=argparse.BooleanOptionalAction, default=None)
    parser.add_argument("--layerwise-validation-ratio", type=float, default=None)
    parser.add_argument("--layerwise-validation-seed", type=int, default=None)
    parser.add_argument("--layerwise-early-stop-patience", type=int, default=None)
    parser.add_argument("--layerwise-early-stop-min-delta", type=float, default=None)
    parser.add_argument("--layerwise-eval-interval", type=int, default=None)
    parser.add_argument("--layerwise-validation-n-sample", type=int, default=None)
    parser.add_argument("--input-compaction", action=argparse.BooleanOptionalAction, default=None)
    parser.add_argument("--prune-collapse-floor", type=float, default=None)
    parser.add_argument("--symbolic-prune-adaptive-acc-drop-tol", type=float, default=None)
    parser.add_argument("--validate-n-sample", type=int, default=None, help="显式覆盖 evaluation.validate_n_sample")

    parser.add_argument("--bench-repeat", type=int, default=3)
    parser.add_argument("--bench-warmup", type=int, default=1)
    parser.add_argument("--eval-rounds", type=int, default=3)

    parser.add_argument("--parallel-modes", default=",".join(DEFAULT_PARALLEL_MODES))
    parser.add_argument("--parallel-target-min", type=int, default=40)
    parser.add_argument("--parallel-target-max", type=int, default=80)
    parser.add_argument("--parallel-max-prune-rounds", type=int, default=8)
    parser.add_argument("--parallel-finetune-steps", type=int, default=20)
    parser.add_argument("--parallel-layerwise-finetune-steps", type=int, default=20)
    parser.add_argument("--parallel-affine-finetune-steps", type=int, default=0)
    parser.add_argument("--parallel-prune-eval-interval", type=int, default=2)
    parser.add_argument("--parallel-prune-attr-sample-adaptive", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--parallel-prune-attr-sample-min", type=int, default=512)
    parser.add_argument("--parallel-prune-attr-sample-max", type=int, default=1536)
    parser.add_argument("--parallel-heavy-ft-patience", type=int, default=1)
    parser.add_argument("--parallel-heavy-ft-min-delta", type=float, default=5e-4)
    return parser


def parse_benchmark_cli_config(argv: Optional[List[str]] = None) -> BenchmarkRunnerConfig:
    parser = build_parser()
    namespace = parser.parse_args(argv)
    values = vars(namespace)
    config = BenchmarkRunnerConfig(config_path=values.pop("config"), **values)
    if config.quiet:
        config.verbose = False
    return config


def run_benchmark(runner: BenchmarkRunnerConfig) -> None:
    tasks = resolve_tasks(runner.tasks)
    stagewise_seeds = parse_csv_ints(runner.stagewise_seeds)
    repo_root = Path(__file__).resolve().parents[1]
    output_dir = resolve_preferred_dir(
        str(runner.output_dir),
        repo_root=repo_root,
        default_dir=DEFAULT_BENCHMARK_RUNS_DIR,
        legacy_dir=LEGACY_BENCHMARK_RUNS_DIR,
    )
    runner.output_dir = str(output_dir)
    ensure_dir(output_dir)
    app_config = load_benchmark_app_config(runner.config_path, runner)

    run_metrics: List[Dict[str, Any]] = []
    eval_summaries: List[pd.DataFrame] = []
    parallel_summaries: List[pd.DataFrame] = []

    for run_index, stage_seed in enumerate(stagewise_seeds, start=1):
        result = run_single_experiment(app_config, runner, repo_root, run_index, len(stagewise_seeds), stage_seed)
        run_dir = result["run_dir"]
        run_metrics.append(result["metrics"])
        context = result["context"]

        if "eval-bench" in tasks:
            eval_result = run_eval_benchmarks(context, runner, run_dir)
            summary = eval_result["multi_round_summary"].copy()
            summary.insert(0, "run_index", run_index)
            summary.insert(1, "stage_seed", stage_seed)
            eval_summaries.append(summary)

        if "parallel-bench" in tasks:
            parallel_df = run_parallel_benchmark(context, runner, run_dir).copy()
            parallel_df.insert(0, "run_index", run_index)
            parallel_df.insert(1, "stage_seed", stage_seed)
            parallel_summaries.append(parallel_df)

    run_metrics_df = pd.DataFrame(run_metrics)
    run_metrics_df.to_csv(output_dir / "symkanbenchmark_runs.csv", index=False, encoding="utf-8-sig")

    if eval_summaries:
        pd.concat(eval_summaries, ignore_index=True).to_csv(
            output_dir / "symkanbenchmark_eval_runs.csv",
            index=False,
            encoding="utf-8-sig",
        )

    if parallel_summaries:
        pd.concat(parallel_summaries, ignore_index=True).to_csv(
            output_dir / "symkanbenchmark_parallel_runs.csv",
            index=False,
            encoding="utf-8-sig",
        )

    print(f"completed {len(stagewise_seeds)} run(s)")
    print(f"output_dir = {output_dir.resolve()}")


def main() -> None:
    config = parse_benchmark_cli_config()
    run_benchmark(config)


if __name__ == "__main__":
    main()
