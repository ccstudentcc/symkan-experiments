from __future__ import annotations

import math

import torch

from kan.MultKAN import MultKAN
from kan.icbr import benchmark_icbr_vs_baseline


def test_icbr_benchmark_smoke_reports_core_metrics() -> None:
    torch.manual_seed(0)
    model = MultKAN(width=[1, 1], grid=5, k=3, auto_save=False)
    calibration_input = torch.linspace(-1.0, 1.0, steps=32).unsqueeze(1)
    calibration_target = torch.sin(torch.pi * calibration_input)

    metrics = benchmark_icbr_vs_baseline(
        model,
        calibration_split=calibration_input,
        calibration_target=calibration_target,
        lib=["x", "x^2"],
        topk=2,
        a_range=(-2.0, 2.0),
        b_range=(-2.0, 2.0),
        grid_number=17,
        iteration=1,
    )

    assert math.isfinite(metrics["candidate_generation_wall_time_s"])
    assert math.isfinite(metrics["replay_rerank_wall_time_s"])
    assert math.isfinite(metrics["symbolic_wall_time_s"])
    assert math.isfinite(metrics["baseline_symbolic_wall_time_s"])
    assert math.isfinite(metrics["symbolic_wall_time_delta_s"])
    assert math.isfinite(metrics["symbolic_speedup_vs_baseline"])
    assert math.isfinite(metrics["replay_imitation_gap"])
    assert math.isfinite(metrics["final_mse_loss_shift"])
    assert math.isfinite(metrics["teacher_target_mse"])
    assert math.isfinite(metrics["teacher_target_r2"])
    assert math.isfinite(metrics["baseline_target_mse"])
    assert math.isfinite(metrics["baseline_target_r2"])
    assert math.isfinite(metrics["icbr_target_mse"])
    assert math.isfinite(metrics["icbr_target_r2"])
    assert math.isfinite(metrics["symbolic_target_mse_shift"])
    assert math.isfinite(metrics["symbolic_target_r2_shift"])
    assert metrics["candidate_generation_wall_time_s"] >= 0.0
    assert metrics["replay_rerank_wall_time_s"] >= 0.0
    assert metrics["symbolic_wall_time_s"] >= 0.0
    assert metrics["baseline_symbolic_wall_time_s"] >= 0.0
    assert math.isfinite(metrics["symbolic_wall_time_delta_s"])
    assert metrics["symbolic_speedup_vs_baseline"] >= 0.0
    assert isinstance(metrics["formula_validation_result"], bool)
    assert isinstance(metrics["baseline_formula_validation_result"], bool)
    assert isinstance(metrics["icbr_formula_validation_result"], bool)
    assert isinstance(metrics["baseline_formula_raw"], list)
    assert isinstance(metrics["baseline_formula_display"], list)
    assert isinstance(metrics["icbr_formula_raw"], list)
    assert isinstance(metrics["icbr_formula_display"], list)
