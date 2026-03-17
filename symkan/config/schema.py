from __future__ import annotations

from typing import Any, Dict, Optional


DEFAULT_CONFIG: Dict[str, Any] = {
    "tasks": "all",
    "output_dir": "outputs/benchmark_runs",
    "device": "auto",
    "batch_size": 0,
    "global_seed": 123,
    "baseline_seed": 123,
    "stagewise_seeds": "42",
    "lib_preset": "layered",
    "save_bundle": False,
    "verbose": False,
    "quiet": False,
    "x_train": "data/X_train.npy",
    "x_test": "data/X_test.npy",
    "y_train": "data/Y_train_cat.npy",
    "y_test": "data/Y_test_cat.npy",
    "auto_fetch_mnist": True,
    "mnist_classes": list(range(10)),
    "inner_dim": 16,
    "grid": 5,
    "k": 3,
    "baseline_steps": 150,
    "baseline_lr": 0.02,
    "baseline_lamb": 1e-4,
    "baseline_log": 12,
    "top_k": 120,
    "stage_lamb_schedule": [0.0, 0.0, 2e-5, 5e-5, 1e-4, 2e-4, 3e-4, 5e-4, 7e-4, 1e-3],
    "stage_lr_schedule": [0.02, 0.015, 0.012, 0.01, 0.008, 0.006, 0.005, 0.004, 0.003, 0.002],
    "steps_per_stage": 60,
    "prune_start_stage": 3,
    "stage_target_edges": 120,
    "prune_edge_threshold_init": 0.003,
    "prune_edge_threshold_step": 0.003,
    "prune_acc_drop_tol": 0.04,
    "post_prune_ft_steps": 50,
    "sym_target_edges": 50,
    "acc_weight": 0.5,
    "disable_stagewise_train": False,
    "e2e_steps": 0,
    "e2e_lr": 0.0,
    "e2e_lamb": -1.0,
    "prune_collapse_floor": 0.6,
    "use_validation": False,
    "validation_ratio": 0.15,
    "validation_seed": None,
    "adaptive_threshold": False,
    "threshold_base_step": 0.005,
    "threshold_min": 0.001,
    "threshold_max": 0.1,
    "success_boost": 0.5,
    "failure_penalty": 0.3,
    "stage_min_gain_threshold": 3,
    "stage_max_prune_attempts": 20,
    "adaptive_lamb": False,
    "min_lamb_ratio": 0.3,
    "max_lamb_ratio": 1.5,
    "adaptive_ft": False,
    "min_ft_ratio": 0.3,
    "stage_early_stop": False,
    "stage_early_stop_patience": 2,
    "stage_early_stop_min_acc_gain": 0.002,
    "stage_early_stop_edge_buffer": 0,
    "symbolic_target_edges": 90,
    "max_prune_rounds": 30,
    "weight_simple": 0.10,
    "finetune_steps": 50,
    "finetune_lr": 0.0005,
    "layerwise_finetune_steps": 60,
    "layerwise_finetune_lr": 0.005,
    "layerwise_finetune_lamb": 1e-5,
    "layerwise_use_validation": True,
    "layerwise_validation_ratio": 0.15,
    "layerwise_validation_seed": None,
    "layerwise_early_stop_patience": 2,
    "layerwise_early_stop_min_delta": 1e-3,
    "layerwise_eval_interval": 20,
    "layerwise_validation_n_sample": 300,
    "affine_finetune_steps": 200,
    "affine_lr_schedule": [0.003, 0.001, 0.0005, 0.0002],
    "parallel_mode": "auto",
    "parallel_workers": None,
    "parallel_min_tasks": 16,
    "prune_eval_interval": 2,
    "prune_attr_sample_adaptive": True,
    "prune_attr_sample_min": 768,
    "prune_attr_sample_max": 2048,
    "heavy_ft_early_stop_patience": 2,
    "heavy_ft_early_stop_min_delta": 5e-4,
    "validate_n_sample": 500,
    "bench_repeat": 3,
    "bench_warmup": 1,
    "eval_rounds": 3,
    "parallel_modes": "auto,off,thread4",
    "parallel_target_min": 40,
    "parallel_target_max": 80,
    "parallel_max_prune_rounds": 8,
    "parallel_finetune_steps": 20,
    "parallel_layerwise_finetune_steps": 20,
    "parallel_affine_finetune_steps": 0,
    "parallel_prune_eval_interval": 2,
    "parallel_prune_attr_sample_adaptive": True,
    "parallel_prune_attr_sample_min": 512,
    "parallel_prune_attr_sample_max": 1536,
    "parallel_heavy_ft_patience": 1,
    "parallel_heavy_ft_min_delta": 5e-4,
    "input_compaction": True,
    "symbolic_prune_threshold_start": 0.02,
    "symbolic_prune_threshold_end": 0.03,
    "symbolic_prune_max_drop_ratio": 1.0,
    "symbolic_prune_threshold_backoff": 0.7,
    "symbolic_prune_adaptive_threshold": True,
    "symbolic_prune_adaptive_step": 0.0,
    "symbolic_prune_adaptive_acc_drop_tol": 0.02,
    "symbolic_prune_adaptive_min_edges_gain": 1,
    "symbolic_prune_adaptive_low_gain_patience": 4,
}

SECTION_FIELD_MAP: Dict[str, set[str]] = {
    "runtime": {
        "tasks", "output_dir", "device", "batch_size", "global_seed", "baseline_seed",
        "stagewise_seeds", "lib_preset", "save_bundle", "verbose", "quiet",
    },
    "data": {
        "x_train", "x_test", "y_train", "y_test", "auto_fetch_mnist", "mnist_classes",
    },
    "model": {
        "inner_dim", "grid", "k", "baseline_steps", "baseline_lr", "baseline_lamb", "baseline_log", "top_k",
    },
    "stagewise": {
        "stage_lamb_schedule", "stage_lr_schedule", "steps_per_stage", "prune_start_stage", "stage_target_edges",
        "prune_edge_threshold_init", "prune_edge_threshold_step", "prune_acc_drop_tol", "post_prune_ft_steps",
        "sym_target_edges", "acc_weight", "disable_stagewise_train", "e2e_steps", "e2e_lr", "e2e_lamb",
        "prune_collapse_floor", "use_validation", "validation_ratio", "validation_seed", "adaptive_threshold",
        "threshold_base_step", "threshold_min", "threshold_max", "success_boost", "failure_penalty",
        "stage_min_gain_threshold", "stage_max_prune_attempts", "adaptive_lamb", "min_lamb_ratio",
        "max_lamb_ratio", "adaptive_ft", "min_ft_ratio", "stage_early_stop", "stage_early_stop_patience",
        "stage_early_stop_min_acc_gain", "stage_early_stop_edge_buffer", "lamb_schedule", "lr_schedule",
    },
    "symbolic": {
        "symbolic_target_edges", "max_prune_rounds", "weight_simple", "finetune_steps", "finetune_lr",
        "layerwise_finetune_steps", "layerwise_finetune_lr", "layerwise_finetune_lamb", "layerwise_use_validation",
        "layerwise_validation_ratio", "layerwise_validation_seed", "layerwise_early_stop_patience",
        "layerwise_early_stop_min_delta", "layerwise_eval_interval", "layerwise_validation_n_sample",
        "affine_finetune_steps", "affine_lr_schedule", "parallel_mode", "parallel_workers", "parallel_min_tasks",
        "prune_eval_interval", "prune_attr_sample_adaptive", "prune_attr_sample_min", "prune_attr_sample_max",
        "heavy_ft_early_stop_patience", "heavy_ft_early_stop_min_delta", "validate_n_sample", "input_compaction",
        "symbolic_prune_threshold_start", "symbolic_prune_threshold_end", "symbolic_prune_max_drop_ratio",
        "symbolic_prune_threshold_backoff", "symbolic_prune_adaptive_threshold", "symbolic_prune_adaptive_step",
        "symbolic_prune_adaptive_acc_drop_tol", "symbolic_prune_adaptive_min_edges_gain",
        "symbolic_prune_adaptive_low_gain_patience",
    },
    "benchmarking": {
        "bench_repeat", "bench_warmup", "eval_rounds", "parallel_modes", "parallel_target_min", "parallel_target_max",
        "parallel_max_prune_rounds", "parallel_finetune_steps", "parallel_layerwise_finetune_steps",
        "parallel_affine_finetune_steps", "parallel_prune_eval_interval", "parallel_prune_attr_sample_adaptive",
        "parallel_prune_attr_sample_min", "parallel_prune_attr_sample_max", "parallel_heavy_ft_patience",
        "parallel_heavy_ft_min_delta",
    },
}


try:
    from pydantic import BaseModel, ConfigDict, Field, field_validator
except ImportError:  # pragma: no cover - depends on environment
    PYDANTIC_AVAILABLE = False
else:
    PYDANTIC_AVAILABLE = True


if PYDANTIC_AVAILABLE:
    class BenchmarkConfigModel(BaseModel):
        model_config = ConfigDict(extra="forbid")

        tasks: str = DEFAULT_CONFIG["tasks"]
        output_dir: str = DEFAULT_CONFIG["output_dir"]
        device: str = DEFAULT_CONFIG["device"]
        batch_size: int = DEFAULT_CONFIG["batch_size"]
        global_seed: int = DEFAULT_CONFIG["global_seed"]
        baseline_seed: int = DEFAULT_CONFIG["baseline_seed"]
        stagewise_seeds: str = DEFAULT_CONFIG["stagewise_seeds"]
        lib_preset: str = DEFAULT_CONFIG["lib_preset"]
        save_bundle: bool = DEFAULT_CONFIG["save_bundle"]
        verbose: bool = DEFAULT_CONFIG["verbose"]
        quiet: bool = DEFAULT_CONFIG["quiet"]
        x_train: str = DEFAULT_CONFIG["x_train"]
        x_test: str = DEFAULT_CONFIG["x_test"]
        y_train: str = DEFAULT_CONFIG["y_train"]
        y_test: str = DEFAULT_CONFIG["y_test"]
        auto_fetch_mnist: bool = DEFAULT_CONFIG["auto_fetch_mnist"]
        mnist_classes: list[int] = Field(default_factory=lambda: list(DEFAULT_CONFIG["mnist_classes"]))
        inner_dim: int = DEFAULT_CONFIG["inner_dim"]
        grid: int = DEFAULT_CONFIG["grid"]
        k: int = DEFAULT_CONFIG["k"]
        baseline_steps: int = DEFAULT_CONFIG["baseline_steps"]
        baseline_lr: float = DEFAULT_CONFIG["baseline_lr"]
        baseline_lamb: float = DEFAULT_CONFIG["baseline_lamb"]
        baseline_log: int = DEFAULT_CONFIG["baseline_log"]
        top_k: int = DEFAULT_CONFIG["top_k"]
        stage_lamb_schedule: list[float] = Field(default_factory=lambda: list(DEFAULT_CONFIG["stage_lamb_schedule"]))
        stage_lr_schedule: list[float] = Field(default_factory=lambda: list(DEFAULT_CONFIG["stage_lr_schedule"]))
        steps_per_stage: int = DEFAULT_CONFIG["steps_per_stage"]
        prune_start_stage: int = DEFAULT_CONFIG["prune_start_stage"]
        stage_target_edges: int = DEFAULT_CONFIG["stage_target_edges"]
        prune_edge_threshold_init: float = DEFAULT_CONFIG["prune_edge_threshold_init"]
        prune_edge_threshold_step: float = DEFAULT_CONFIG["prune_edge_threshold_step"]
        prune_acc_drop_tol: float = DEFAULT_CONFIG["prune_acc_drop_tol"]
        post_prune_ft_steps: int = DEFAULT_CONFIG["post_prune_ft_steps"]
        sym_target_edges: int = DEFAULT_CONFIG["sym_target_edges"]
        acc_weight: float = DEFAULT_CONFIG["acc_weight"]
        disable_stagewise_train: bool = DEFAULT_CONFIG["disable_stagewise_train"]
        e2e_steps: int = DEFAULT_CONFIG["e2e_steps"]
        e2e_lr: float = DEFAULT_CONFIG["e2e_lr"]
        e2e_lamb: float = DEFAULT_CONFIG["e2e_lamb"]
        prune_collapse_floor: float = DEFAULT_CONFIG["prune_collapse_floor"]
        use_validation: bool = DEFAULT_CONFIG["use_validation"]
        validation_ratio: float = DEFAULT_CONFIG["validation_ratio"]
        validation_seed: Optional[int] = DEFAULT_CONFIG["validation_seed"]
        adaptive_threshold: bool = DEFAULT_CONFIG["adaptive_threshold"]
        threshold_base_step: float = DEFAULT_CONFIG["threshold_base_step"]
        threshold_min: float = DEFAULT_CONFIG["threshold_min"]
        threshold_max: float = DEFAULT_CONFIG["threshold_max"]
        success_boost: float = DEFAULT_CONFIG["success_boost"]
        failure_penalty: float = DEFAULT_CONFIG["failure_penalty"]
        stage_min_gain_threshold: int = DEFAULT_CONFIG["stage_min_gain_threshold"]
        stage_max_prune_attempts: int = DEFAULT_CONFIG["stage_max_prune_attempts"]
        adaptive_lamb: bool = DEFAULT_CONFIG["adaptive_lamb"]
        min_lamb_ratio: float = DEFAULT_CONFIG["min_lamb_ratio"]
        max_lamb_ratio: float = DEFAULT_CONFIG["max_lamb_ratio"]
        adaptive_ft: bool = DEFAULT_CONFIG["adaptive_ft"]
        min_ft_ratio: float = DEFAULT_CONFIG["min_ft_ratio"]
        stage_early_stop: bool = DEFAULT_CONFIG["stage_early_stop"]
        stage_early_stop_patience: int = DEFAULT_CONFIG["stage_early_stop_patience"]
        stage_early_stop_min_acc_gain: float = DEFAULT_CONFIG["stage_early_stop_min_acc_gain"]
        stage_early_stop_edge_buffer: int = DEFAULT_CONFIG["stage_early_stop_edge_buffer"]
        symbolic_target_edges: int = DEFAULT_CONFIG["symbolic_target_edges"]
        max_prune_rounds: int = DEFAULT_CONFIG["max_prune_rounds"]
        weight_simple: float = DEFAULT_CONFIG["weight_simple"]
        finetune_steps: int = DEFAULT_CONFIG["finetune_steps"]
        finetune_lr: float = DEFAULT_CONFIG["finetune_lr"]
        layerwise_finetune_steps: int = DEFAULT_CONFIG["layerwise_finetune_steps"]
        layerwise_finetune_lr: float = DEFAULT_CONFIG["layerwise_finetune_lr"]
        layerwise_finetune_lamb: float = DEFAULT_CONFIG["layerwise_finetune_lamb"]
        layerwise_use_validation: bool = DEFAULT_CONFIG["layerwise_use_validation"]
        layerwise_validation_ratio: float = DEFAULT_CONFIG["layerwise_validation_ratio"]
        layerwise_validation_seed: Optional[int] = DEFAULT_CONFIG["layerwise_validation_seed"]
        layerwise_early_stop_patience: int = DEFAULT_CONFIG["layerwise_early_stop_patience"]
        layerwise_early_stop_min_delta: float = DEFAULT_CONFIG["layerwise_early_stop_min_delta"]
        layerwise_eval_interval: int = DEFAULT_CONFIG["layerwise_eval_interval"]
        layerwise_validation_n_sample: int = DEFAULT_CONFIG["layerwise_validation_n_sample"]
        affine_finetune_steps: int = DEFAULT_CONFIG["affine_finetune_steps"]
        affine_lr_schedule: list[float] = Field(default_factory=lambda: list(DEFAULT_CONFIG["affine_lr_schedule"]))
        parallel_mode: str = DEFAULT_CONFIG["parallel_mode"]
        parallel_workers: Optional[int] = DEFAULT_CONFIG["parallel_workers"]
        parallel_min_tasks: int = DEFAULT_CONFIG["parallel_min_tasks"]
        prune_eval_interval: int = DEFAULT_CONFIG["prune_eval_interval"]
        prune_attr_sample_adaptive: bool = DEFAULT_CONFIG["prune_attr_sample_adaptive"]
        prune_attr_sample_min: int = DEFAULT_CONFIG["prune_attr_sample_min"]
        prune_attr_sample_max: int = DEFAULT_CONFIG["prune_attr_sample_max"]
        heavy_ft_early_stop_patience: int = DEFAULT_CONFIG["heavy_ft_early_stop_patience"]
        heavy_ft_early_stop_min_delta: float = DEFAULT_CONFIG["heavy_ft_early_stop_min_delta"]
        validate_n_sample: int = DEFAULT_CONFIG["validate_n_sample"]
        bench_repeat: int = DEFAULT_CONFIG["bench_repeat"]
        bench_warmup: int = DEFAULT_CONFIG["bench_warmup"]
        eval_rounds: int = DEFAULT_CONFIG["eval_rounds"]
        parallel_modes: str = DEFAULT_CONFIG["parallel_modes"]
        parallel_target_min: int = DEFAULT_CONFIG["parallel_target_min"]
        parallel_target_max: int = DEFAULT_CONFIG["parallel_target_max"]
        parallel_max_prune_rounds: int = DEFAULT_CONFIG["parallel_max_prune_rounds"]
        parallel_finetune_steps: int = DEFAULT_CONFIG["parallel_finetune_steps"]
        parallel_layerwise_finetune_steps: int = DEFAULT_CONFIG["parallel_layerwise_finetune_steps"]
        parallel_affine_finetune_steps: int = DEFAULT_CONFIG["parallel_affine_finetune_steps"]
        parallel_prune_eval_interval: int = DEFAULT_CONFIG["parallel_prune_eval_interval"]
        parallel_prune_attr_sample_adaptive: bool = DEFAULT_CONFIG["parallel_prune_attr_sample_adaptive"]
        parallel_prune_attr_sample_min: int = DEFAULT_CONFIG["parallel_prune_attr_sample_min"]
        parallel_prune_attr_sample_max: int = DEFAULT_CONFIG["parallel_prune_attr_sample_max"]
        parallel_heavy_ft_patience: int = DEFAULT_CONFIG["parallel_heavy_ft_patience"]
        parallel_heavy_ft_min_delta: float = DEFAULT_CONFIG["parallel_heavy_ft_min_delta"]
        input_compaction: bool = DEFAULT_CONFIG["input_compaction"]
        symbolic_prune_threshold_start: float = DEFAULT_CONFIG["symbolic_prune_threshold_start"]
        symbolic_prune_threshold_end: float = DEFAULT_CONFIG["symbolic_prune_threshold_end"]
        symbolic_prune_max_drop_ratio: float = DEFAULT_CONFIG["symbolic_prune_max_drop_ratio"]
        symbolic_prune_threshold_backoff: float = DEFAULT_CONFIG["symbolic_prune_threshold_backoff"]
        symbolic_prune_adaptive_threshold: bool = DEFAULT_CONFIG["symbolic_prune_adaptive_threshold"]
        symbolic_prune_adaptive_step: float = DEFAULT_CONFIG["symbolic_prune_adaptive_step"]
        symbolic_prune_adaptive_acc_drop_tol: float = DEFAULT_CONFIG["symbolic_prune_adaptive_acc_drop_tol"]
        symbolic_prune_adaptive_min_edges_gain: int = DEFAULT_CONFIG["symbolic_prune_adaptive_min_edges_gain"]
        symbolic_prune_adaptive_low_gain_patience: int = DEFAULT_CONFIG["symbolic_prune_adaptive_low_gain_patience"]

        @field_validator("lib_preset")
        @classmethod
        def validate_lib_preset(cls, value: str) -> str:
            allowed = {"layered", "fast", "expressive", "full"}
            if value not in allowed:
                raise ValueError(f"lib_preset must be one of {sorted(allowed)}")
            return value
