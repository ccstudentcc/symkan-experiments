from __future__ import annotations

import argparse
import os
import json
import math
import time
from contextlib import contextmanager, redirect_stderr, redirect_stdout
from pathlib import Path
from typing import Any, Dict, List

import numpy as np
import pandas as pd
import torch
from scipy.special import softmax as scipy_softmax

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
from symkan.tuning import stagewise_train

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


def load_data(args: argparse.Namespace, repo_root: Path) -> Dict[str, Any]:
    x_train = np.load(resolve_path(args.x_train, repo_root)).astype(np.float32)
    x_test = np.load(resolve_path(args.x_test, repo_root)).astype(np.float32)
    y_train_raw = np.load(resolve_path(args.y_train, repo_root))
    y_test_raw = np.load(resolve_path(args.y_test, repo_root))

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


def run_eval_benchmarks(context: Dict[str, Any], args: argparse.Namespace, output_dir: Path) -> Dict[str, Any]:
    enhanced_model = context["enhanced_model"]
    export_model = context["export_model"]
    export_formulas = context["export_formulas"]
    dataset_enhanced = context["dataset_enhanced"]

    x_np = dataset_enhanced["test_input"].detach().cpu().numpy()
    y_np = np.argmax(dataset_enhanced["test_label"].detach().cpu().numpy(), axis=1)

    bench_rows = [
        benchmark_callable("legacy_numpy_path", lambda: model_acc(enhanced_model, x_np, y_np), repeat=args.bench_repeat, warmup=args.bench_warmup),
        benchmark_callable(
            "fast_tensor_path",
            lambda: model_acc_ds_fast(enhanced_model, dataset_enhanced),
            repeat=args.bench_repeat,
            warmup=args.bench_warmup,
        ),
        benchmark_callable(
            "model_acc_ds_current",
            lambda: model_acc_ds(enhanced_model, dataset_enhanced),
            repeat=args.bench_repeat,
            warmup=args.bench_warmup,
        ),
    ]

    if export_formulas is not None:
        bench_rows.append(
            benchmark_callable(
                "validate_formula_first",
                lambda: validate_formula_numerically(export_model, export_formulas, dataset_enhanced, n_sample=args.validate_n_sample),
                repeat=1,
                warmup=0,
            )
        )
        bench_rows.append(
            benchmark_callable(
                "validate_formula_cached",
                lambda: validate_formula_numerically(export_model, export_formulas, dataset_enhanced, n_sample=args.validate_n_sample),
                repeat=1,
                warmup=0,
            )
        )

    benchmark_df = pd.DataFrame([{k: v for k, v in row.items() if k != "last_output"} for row in bench_rows])
    benchmark_df.to_csv(output_dir / "benchmark_single_round.csv", index=False, encoding="utf-8-sig")

    all_round_rows: List[Dict[str, Any]] = []
    for round_id in range(1, args.eval_rounds + 1):
        round_rows = [
            benchmark_callable("legacy_numpy_path", lambda: model_acc(enhanced_model, x_np, y_np), repeat=args.bench_repeat, warmup=args.bench_warmup),
            benchmark_callable(
                "fast_tensor_path",
                lambda: model_acc_ds_fast(enhanced_model, dataset_enhanced),
                repeat=args.bench_repeat,
                warmup=args.bench_warmup,
            ),
            benchmark_callable(
                "model_acc_ds_current",
                lambda: model_acc_ds(enhanced_model, dataset_enhanced),
                repeat=args.bench_repeat,
                warmup=args.bench_warmup,
            ),
        ]

        if export_formulas is not None:
            if eval_metrics_module is not None and hasattr(eval_metrics_module, "_LAMBDA_CACHE"):
                eval_metrics_module._LAMBDA_CACHE.clear()
            round_rows.append(
                benchmark_callable(
                    "validate_formula_first",
                    lambda: validate_formula_numerically(export_model, export_formulas, dataset_enhanced, n_sample=args.validate_n_sample),
                    repeat=1,
                    warmup=0,
                )
            )
            round_rows.append(
                benchmark_callable(
                    "validate_formula_cached",
                    lambda: validate_formula_numerically(export_model, export_formulas, dataset_enhanced, n_sample=args.validate_n_sample),
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


def run_parallel_benchmark(context: Dict[str, Any], args: argparse.Namespace, output_dir: Path) -> pd.DataFrame:
    enhanced_model = context["enhanced_model"]
    dataset_enhanced = context["dataset_enhanced"]
    batch_size = context["batch_size"]
    library_cfg = context["library_cfg"]
    silent = bool(args.quiet)

    edge_now = int(get_n_edge(enhanced_model))
    target_quick = max(args.parallel_target_min, min(args.parallel_target_max, edge_now))
    rows: List[Dict[str, Any]] = []

    for cfg in resolve_parallel_modes(args.parallel_modes):
        t0 = time.perf_counter()
        with maybe_silent(silent):
            out = symbolize_pipeline(
                enhanced_model,
                dataset_enhanced,
                target_edges=target_quick,
                max_prune_rounds=args.parallel_max_prune_rounds,
                lib=library_cfg["lib"],
                lib_hidden=library_cfg["lib_hidden"],
                lib_output=library_cfg["lib_output"],
                weight_simple=args.weight_simple,
                finetune_steps=args.parallel_finetune_steps,
                finetune_lr=args.finetune_lr,
                layerwise_finetune_steps=args.parallel_layerwise_finetune_steps,
                affine_finetune_steps=args.parallel_affine_finetune_steps,
                batch_size=batch_size,
                prune_eval_interval=args.parallel_prune_eval_interval,
                prune_attr_sample_adaptive=args.parallel_prune_attr_sample_adaptive,
                prune_attr_sample_min=args.parallel_prune_attr_sample_min,
                prune_attr_sample_max=args.parallel_prune_attr_sample_max,
                heavy_ft_early_stop_patience=args.parallel_heavy_ft_patience,
                heavy_ft_early_stop_min_delta=args.parallel_heavy_ft_min_delta,
                collect_timing=True,
                verbose=False,
                parallel_mode=cfg["parallel_mode"],
                parallel_workers=cfg["parallel_workers"],
                parallel_min_tasks=args.parallel_min_tasks,
            )
        wall_time = time.perf_counter() - t0
        timing = out.get("timing", {})
        symbolic_time = timing.get("symbolic_total_seconds", float("nan"))
        rows.append(
            {
                "mode": cfg["name"],
                "parallel_mode": cfg["parallel_mode"],
                "parallel_workers_effective": out.get("sym_stats", {}).get("parallel_workers"),
                "target_edges": int(target_quick),
                "wall_time_s": float(wall_time),
                "symbolic_time_s": float(symbolic_time) if symbolic_time == symbolic_time else float("nan"),
                "final_acc": float(out.get("final_acc", float("nan"))),
                "final_n_edge": int(out.get("final_n_edge", -1)),
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
    args: argparse.Namespace,
    repo_root: Path,
    run_index: int,
    total_runs: int,
    stage_seed: int,
) -> Dict[str, Any]:
    run_dir = ensure_dir(Path(args.output_dir) / f"run_{run_index:02d}_seed{stage_seed}")

    set_global_seed(args.global_seed)
    device = str(resolve_device(args.device))
    set_device(device)
    batch_size = int(args.batch_size) if args.batch_size and args.batch_size > 0 else int(default_batch_size())
    library_cfg = resolve_library(args.lib_preset)
    data = load_data(args, repo_root)
    silent = bool(args.quiet)

    dataset_full = build_dataset(data["X_train"], data["Y_train"], data["X_test"], data["Y_test"])
    inner_dim = int(args.inner_dim)
    width_base = [data["input_dim"], inner_dim, data["n_classes"]]

    base_model = KAN(
        width=width_base,
        grid=args.grid,
        k=args.k,
        seed=args.baseline_seed,
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
            steps=args.baseline_steps,
            lr=args.baseline_lr,
            lamb=args.baseline_lamb,
            batch=batch_size,
            update_grid=True,
            singularity_avoiding=True,
            log=args.baseline_log,
        )
    base_acc = float(model_acc(base_model, data["X_test"], data["y_test"]))

    feature_score = safe_attribute(base_model, dataset_full)
    top_k = min(int(args.top_k), data["input_dim"])
    keep_idx = np.sort(np.argsort(-feature_score)[:top_k])
    x_train_sel = data["X_train"][:, keep_idx]
    x_test_sel = data["X_test"][:, keep_idx]
    dataset_enhanced = build_dataset(x_train_sel, data["Y_train"], x_test_sel, data["Y_test"])

    with maybe_silent(silent):
        enhanced_model, enhanced_res = stagewise_train(
            dataset_enhanced,
            width=[int(x_train_sel.shape[1]), inner_dim, data["n_classes"]],
            grid=args.grid,
            k=args.k,
            seed=stage_seed,
            lamb_schedule=tuple(args.stage_lamb_schedule),
            lr_schedule=tuple(args.stage_lr_schedule),
            steps_per_stage=args.steps_per_stage,
            batch_size=batch_size,
            prune_start_stage=args.prune_start_stage,
            target_edges=args.stage_target_edges,
            prune_edge_threshold_init=args.prune_edge_threshold_init,
            prune_edge_threshold_step=args.prune_edge_threshold_step,
            prune_acc_drop_tol=args.prune_acc_drop_tol,
            post_prune_ft_steps=args.post_prune_ft_steps,
            sym_target_edges=args.sym_target_edges,
            acc_weight=args.acc_weight,
            use_validation=args.use_validation,
            validation_ratio=args.validation_ratio,
            validation_seed=args.validation_seed if args.validation_seed is not None else args.global_seed,
            adaptive_threshold=args.adaptive_threshold,
            threshold_base_step=args.threshold_base_step,
            threshold_min=args.threshold_min,
            threshold_max=args.threshold_max,
            success_boost=args.success_boost,
            failure_penalty=args.failure_penalty,
            min_gain_threshold=args.stage_min_gain_threshold,
            max_prune_attempts=args.stage_max_prune_attempts,
            adaptive_lamb=args.adaptive_lamb,
            min_lamb_ratio=args.min_lamb_ratio,
            max_lamb_ratio=args.max_lamb_ratio,
            adaptive_ft=args.adaptive_ft,
            min_ft_ratio=args.min_ft_ratio,
            verbose=(args.verbose and not silent),
        )
    enhanced_acc = float(model_acc_ds(enhanced_model, dataset_enhanced))
    stage_df = pd.DataFrame(enhanced_res.get("stage_logs", []))
    save_stage_logs(stage_df, csv_path=str(run_dir / "kan_stage_logs.csv"))

    export_t0 = time.perf_counter()
    with maybe_silent(silent):
        export_result = symbolize_pipeline(
            enhanced_model,
            dataset_enhanced,
            target_edges=args.symbolic_target_edges,
            max_prune_rounds=args.max_prune_rounds,
            lib=library_cfg["lib"],
            lib_hidden=library_cfg["lib_hidden"],
            lib_output=library_cfg["lib_output"],
            weight_simple=args.weight_simple,
            finetune_steps=args.finetune_steps,
            finetune_lr=args.finetune_lr,
            layerwise_finetune_steps=args.layerwise_finetune_steps,
            affine_finetune_steps=args.affine_finetune_steps,
            affine_finetune_lr_schedule=list(args.affine_lr_schedule),
            parallel_mode=args.parallel_mode,
            parallel_workers=args.parallel_workers,
            parallel_min_tasks=args.parallel_min_tasks,
            prune_eval_interval=args.prune_eval_interval,
            prune_attr_sample_adaptive=args.prune_attr_sample_adaptive,
            prune_attr_sample_min=args.prune_attr_sample_min,
            prune_attr_sample_max=args.prune_attr_sample_max,
            heavy_ft_early_stop_patience=args.heavy_ft_early_stop_patience,
            heavy_ft_early_stop_min_delta=args.heavy_ft_early_stop_min_delta,
            collect_timing=True,
            batch_size=batch_size,
            verbose=(args.verbose and not silent),
        )
    export_wall_time = float(time.perf_counter() - export_t0)

    export_model = export_result["model"]
    export_formulas = export_result["formulas"]
    valid_exprs = export_result["valid_expressions"]
    trace_df = export_result["trace"]
    trace_df.to_csv(run_dir / "symbolize_trace.csv", index=False, encoding="utf-8-sig")

    val_df = validate_formula_numerically(
        export_model,
        export_formulas,
        dataset_enhanced,
        n_sample=args.validate_n_sample,
    )
    if val_df is not None:
        val_df.to_csv(run_dir / "formula_validation.csv", index=False, encoding="utf-8-sig")

    logits_sym = model_logits(export_model, x_test_sel)
    y_prob_sym = scipy_softmax(logits_sym, axis=1)
    roc_data = compute_multiclass_roc_auc(dataset_enhanced["test_label"].detach().cpu().numpy(), y_prob_sym)
    auc_macro = float(np.mean([roc_data[class_idx]["auc"] for class_idx in range(data["n_classes"])]))

    summary_df = build_formula_summary(export_formulas, valid_exprs, roc_data, data["n_classes"])
    save_symbolic_summary(summary_df, csv_path=str(run_dir / "kan_symbolic_summary.csv"))

    roc_rows = [
        {"class": class_idx, "auc": float(roc_data[class_idx]["auc"])} for class_idx in range(data["n_classes"])
    ]
    pd.DataFrame(roc_rows).to_csv(run_dir / "roc_auc_summary.csv", index=False, encoding="utf-8-sig")

    if args.save_bundle:
        save_export_bundle(
            {
                "config": {
                    "stage_seed": stage_seed,
                    "lib_preset": args.lib_preset,
                    "device": get_device(),
                    "tasks": resolve_tasks(args.tasks),
                },
                "baseline_result": base_res,
                "stagewise_result": enhanced_res,
                "symbolize_result": export_result,
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
        "lib_preset": args.lib_preset,
        "base_acc": base_acc,
        "base_n_edge": int(get_n_edge(base_model)),
        "selected_input_dim": int(len(keep_idx)),
        "enhanced_acc": enhanced_acc,
        "enhanced_n_edge": int(get_n_edge(enhanced_model)),
        "selected_stage": enhanced_res.get("selected_stage"),
        "selected_score": float(enhanced_res.get("selected_score", float("nan"))),
        "final_acc": float(export_result.get("final_acc", float("nan"))),
        "final_n_edge": int(export_result.get("final_n_edge", -1)),
        "effective_target_edges": int(export_result.get("effective_target_edges", -1)),
        "effective_input_dim": int(export_result.get("effective_input_dim", -1)),
        "valid_expression_count": int(len(valid_exprs)),
        "macro_auc": auc_macro,
        "validation_mean_r2": float(val_df["r2"].mean()) if val_df is not None and len(val_df) > 0 else float("nan"),
        "validation_negative_r2_count": int((val_df["r2"] < 0).sum()) if val_df is not None and len(val_df) > 0 else 0,
        "symbolic_total_seconds": float(export_result.get("timing", {}).get("symbolic_total_seconds", float("nan"))),
        "export_wall_time_s": export_wall_time,
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
        },
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Notebook-aligned symkan benchmark runner.")
    parser.add_argument("--tasks", default="all", help="full,eval-bench,parallel-bench 或 all")
    parser.add_argument("--output-dir", default="benchmark_runs", help="输出目录")
    parser.add_argument("--device", default="auto", help="auto/cpu/cuda/cuda:0")
    parser.add_argument("--batch-size", type=int, default=0, help="0 表示使用 default_batch_size()")
    parser.add_argument("--global-seed", type=int, default=123)
    parser.add_argument("--baseline-seed", type=int, default=123)
    parser.add_argument("--stagewise-seeds", default="42", help="逗号分隔的 stagewise 种子列表")
    parser.add_argument("--lib-preset", choices=["layered", "fast", "expressive", "full"], default="layered")
    parser.add_argument("--save-bundle", action="store_true", help="额外导出 pkl bundle")
    parser.add_argument("--verbose", action="store_true", help="打印 stagewise 与 symbolize 详细日志")
    parser.add_argument("--quiet", action="store_true", help="静默运行，屏蔽训练与符号化过程输出")

    parser.add_argument("--x-train", default="X_train.npy")
    parser.add_argument("--x-test", default="X_test.npy")
    parser.add_argument("--y-train", default="Y_train_cat.npy")
    parser.add_argument("--y-test", default="Y_test_cat.npy")

    parser.add_argument("--inner-dim", type=int, default=16)
    parser.add_argument("--grid", type=int, default=5)
    parser.add_argument("--k", type=int, default=3)

    parser.add_argument("--baseline-steps", type=int, default=150)
    parser.add_argument("--baseline-lr", type=float, default=0.02)
    parser.add_argument("--baseline-lamb", type=float, default=1e-4)
    parser.add_argument("--baseline-log", type=int, default=12)
    parser.add_argument("--top-k", type=int, default=120)

    parser.add_argument(
        "--stage-lamb-schedule",
        type=parse_csv_floats,
        default=[0.0, 0.0, 2e-5, 5e-5, 1e-4, 2e-4, 3e-4, 5e-4, 7e-4, 1e-3],
    )
    parser.add_argument(
        "--stage-lr-schedule",
        type=parse_csv_floats,
        default=[0.02, 0.015, 0.012, 0.01, 0.008, 0.006, 0.005, 0.004, 0.003, 0.002],
    )
    parser.add_argument("--steps-per-stage", type=int, default=60)
    parser.add_argument("--prune-start-stage", type=int, default=3)
    parser.add_argument("--stage-target-edges", type=int, default=120)
    parser.add_argument("--prune-edge-threshold-init", type=float, default=0.003)
    parser.add_argument("--prune-edge-threshold-step", type=float, default=0.003)
    parser.add_argument("--prune-acc-drop-tol", type=float, default=0.04)
    parser.add_argument("--post-prune-ft-steps", type=int, default=50)
    parser.add_argument("--sym-target-edges", type=int, default=50)
    parser.add_argument("--acc-weight", type=float, default=0.5)

    parser.add_argument("--symbolic-target-edges", type=int, default=90)
    parser.add_argument("--max-prune-rounds", type=int, default=30)
    parser.add_argument("--weight-simple", type=float, default=0.10)
    parser.add_argument("--finetune-steps", type=int, default=50)
    parser.add_argument("--finetune-lr", type=float, default=0.0005)
    parser.add_argument("--layerwise-finetune-steps", type=int, default=120)
    parser.add_argument("--affine-finetune-steps", type=int, default=200)
    parser.add_argument("--affine-lr-schedule", type=parse_csv_floats, default=[0.003, 0.001, 0.0005, 0.0002])
    parser.add_argument("--parallel-mode", default="auto")
    parser.add_argument("--parallel-workers", type=int, default=None)
    parser.add_argument("--parallel-min-tasks", type=int, default=16)
    parser.add_argument("--prune-eval-interval", type=int, default=2)
    parser.add_argument("--prune-attr-sample-adaptive", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--prune-attr-sample-min", type=int, default=768)
    parser.add_argument("--prune-attr-sample-max", type=int, default=2048)
    parser.add_argument("--heavy-ft-early-stop-patience", type=int, default=2)
    parser.add_argument("--heavy-ft-early-stop-min-delta", type=float, default=5e-4)
    parser.add_argument("--validate-n-sample", type=int, default=500)

    parser.add_argument("--bench-repeat", type=int, default=3)
    parser.add_argument("--bench-warmup", type=int, default=1)
    parser.add_argument("--eval-rounds", type=int, default=3)

    parser.add_argument("--parallel-modes", default=",".join(DEFAULT_PARALLEL_MODES))
    parser.add_argument("--parallel-target-min", type=int, default=40)
    parser.add_argument("--parallel-target-max", type=int, default=80)
    parser.add_argument("--parallel-max-prune-rounds", type=int, default=8)
    parser.add_argument("--parallel-finetune-steps", type=int, default=20)
    parser.add_argument("--parallel-layerwise-finetune-steps", type=int, default=40)
    parser.add_argument("--parallel-affine-finetune-steps", type=int, default=0)
    parser.add_argument("--parallel-prune-eval-interval", type=int, default=2)
    parser.add_argument("--parallel-prune-attr-sample-adaptive", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--parallel-prune-attr-sample-min", type=int, default=512)
    parser.add_argument("--parallel-prune-attr-sample-max", type=int, default=1536)
    parser.add_argument("--parallel-heavy-ft-patience", type=int, default=1)
    parser.add_argument("--parallel-heavy-ft-min-delta", type=float, default=5e-4)

    # ---- adaptive pruning (stagewise_train) ----
    parser.add_argument("--use-validation", action=argparse.BooleanOptionalAction, default=False,
                        help="启用验证集驱动的剪枝接受判断")
    parser.add_argument("--validation-ratio", type=float, default=0.15,
                        help="切出验证集的比例（use-validation 开启时生效）")
    parser.add_argument("--validation-seed", type=int, default=None,
                        help="验证集切分随机种子；不传则跟随 global-seed")
    parser.add_argument("--adaptive-threshold", action=argparse.BooleanOptionalAction, default=False,
                        help="根据最近剪枝成败自动调整阈值")
    parser.add_argument("--threshold-base-step", type=float, default=0.005)
    parser.add_argument("--threshold-min", type=float, default=0.001)
    parser.add_argument("--threshold-max", type=float, default=0.1)
    parser.add_argument("--success-boost", type=float, default=0.5)
    parser.add_argument("--failure-penalty", type=float, default=0.3)
    parser.add_argument("--stage-min-gain-threshold", type=int, default=3,
                        help="最近剪枝平均收益低于该值时停止当阶段剪枝")
    parser.add_argument("--stage-max-prune-attempts", type=int, default=20,
                        help="单阶段最多剪枝尝试次数（仅 adaptive-threshold 模式有效）")
    parser.add_argument("--adaptive-lamb", action=argparse.BooleanOptionalAction, default=False,
                        help="按当前稀疏进度调整 lamb")
    parser.add_argument("--min-lamb-ratio", type=float, default=0.3)
    parser.add_argument("--max-lamb-ratio", type=float, default=1.5)
    parser.add_argument("--adaptive-ft", action=argparse.BooleanOptionalAction, default=False,
                        help="按当前稀疏进度缩放剪枝后恢复步数")
    parser.add_argument("--min-ft-ratio", type=float, default=0.3)
    return parser


def normalize_numeric_args(args: argparse.Namespace) -> None:
    args.stage_lamb_schedule = [float(item) for item in args.stage_lamb_schedule]
    args.stage_lr_schedule = [float(item) for item in args.stage_lr_schedule]
    args.affine_lr_schedule = [float(item) for item in args.affine_lr_schedule]


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    normalize_numeric_args(args)

    if args.quiet:
        args.verbose = False

    tasks = resolve_tasks(args.tasks)
    stagewise_seeds = parse_csv_ints(args.stagewise_seeds)
    repo_root = Path(__file__).resolve().parent
    ensure_dir(Path(args.output_dir))

    run_metrics: List[Dict[str, Any]] = []
    eval_summaries: List[pd.DataFrame] = []
    parallel_summaries: List[pd.DataFrame] = []

    for run_index, stage_seed in enumerate(stagewise_seeds, start=1):
        result = run_single_experiment(args, repo_root, run_index, len(stagewise_seeds), stage_seed)
        run_dir = result["run_dir"]
        run_metrics.append(result["metrics"])
        context = result["context"]

        if "eval-bench" in tasks:
            eval_result = run_eval_benchmarks(context, args, run_dir)
            summary = eval_result["multi_round_summary"].copy()
            summary.insert(0, "run_index", run_index)
            summary.insert(1, "stage_seed", stage_seed)
            eval_summaries.append(summary)

        if "parallel-bench" in tasks:
            parallel_df = run_parallel_benchmark(context, args, run_dir).copy()
            parallel_df.insert(0, "run_index", run_index)
            parallel_df.insert(1, "stage_seed", stage_seed)
            parallel_summaries.append(parallel_df)

    run_metrics_df = pd.DataFrame(run_metrics)
    run_metrics_df.to_csv(Path(args.output_dir) / "symkanbenchmark_runs.csv", index=False, encoding="utf-8-sig")

    if eval_summaries:
        pd.concat(eval_summaries, ignore_index=True).to_csv(
            Path(args.output_dir) / "symkanbenchmark_eval_runs.csv",
            index=False,
            encoding="utf-8-sig",
        )

    if parallel_summaries:
        pd.concat(parallel_summaries, ignore_index=True).to_csv(
            Path(args.output_dir) / "symkanbenchmark_parallel_runs.csv",
            index=False,
            encoding="utf-8-sig",
        )

    print(f"completed {len(stagewise_seeds)} run(s)")
    print(f"output_dir = {Path(args.output_dir).resolve()}")


if __name__ == "__main__":
    main()