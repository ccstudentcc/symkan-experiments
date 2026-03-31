from __future__ import annotations

import math

import torch

from kan.MultKAN import MultKAN
from kan.icbr import benchmark_icbr_vs_baseline, benchmark_symbolic_variants


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
    assert math.isfinite(metrics["baseline_imitation_mse"])
    assert math.isfinite(metrics["icbr_imitation_mse"])
    assert math.isfinite(metrics["imitation_mse_shift"])
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
    assert isinstance(metrics["formula_export_success"], bool)
    assert isinstance(metrics["baseline_formula_export_success"], bool)
    assert isinstance(metrics["icbr_formula_export_success"], bool)
    assert isinstance(metrics["baseline_formula_raw"], list)
    assert isinstance(metrics["baseline_formula_display"], list)
    assert isinstance(metrics["icbr_formula_raw"], list)
    assert isinstance(metrics["icbr_formula_display"], list)


def test_benchmark_symbolic_variants_reports_challenge_evidence() -> None:
    torch.manual_seed(0)
    model = MultKAN(width=[1, 1], grid=5, k=3, auto_save=False)
    calibration_input = torch.linspace(-1.0, 1.0, steps=24).unsqueeze(1)
    calibration_target = torch.sin(torch.pi * calibration_input)

    bundle = benchmark_symbolic_variants(
        model,
        calibration_split=calibration_input,
        calibration_target=calibration_target,
        lib=["x", "x^2"],
        topk=2,
        a_range=(-2.0, 2.0),
        b_range=(-2.0, 2.0),
        grid_number=11,
        iteration=1,
        variants=["baseline", "icbr_full", "icbr_no_replay", "icbr_no_shared", "icbr_refit_commit"],
    )

    assert bundle["variants_requested"] == [
        "baseline",
        "icbr_full",
        "icbr_no_replay",
        "icbr_no_shared",
        "icbr_refit_commit",
    ]
    assert "challenge_evidence" in bundle
    assert "shared_tensor" in bundle["challenge_evidence"]
    assert "contextual_replay" in bundle["challenge_evidence"]
    assert "explicit_commit" in bundle["challenge_evidence"]
    assert "icbr_no_replay" in bundle["variants"]
    assert "icbr_no_shared" in bundle["variants"]
    assert "icbr_refit_commit" in bundle["variants"]
    assert "imitation_mse_gain_full_vs_no_replay" in bundle["challenge_evidence"]["contextual_replay"]
    assert "imitation_mse_gain_explicit_vs_refit" in bundle["challenge_evidence"]["explicit_commit"]


def test_benchmark_symbolic_variants_evaluates_targets_on_evaluation_split() -> None:
    torch.manual_seed(0)
    model = MultKAN(width=[1, 1], grid=5, k=3, auto_save=False)
    calibration_input = torch.linspace(-1.0, 1.0, steps=24).unsqueeze(1)
    calibration_target = torch.sin(torch.pi * calibration_input)
    evaluation_input = torch.linspace(-1.5, 1.5, steps=24).unsqueeze(1)
    evaluation_target = torch.cos(torch.pi * evaluation_input)

    bundle = benchmark_symbolic_variants(
        model,
        calibration_split=calibration_input,
        calibration_target=calibration_target,
        evaluation_split=evaluation_input,
        evaluation_target=evaluation_target,
        lib=["x", "x^2"],
        topk=2,
        a_range=(-2.0, 2.0),
        b_range=(-2.0, 2.0),
        grid_number=11,
        iteration=1,
        variants=["baseline", "icbr_full"],
    )

    teacher_target_mse = float(bundle["teacher_target_mse"])
    assert math.isfinite(teacher_target_mse)

    with torch.no_grad():
        teacher_prediction = model(evaluation_input)
        if isinstance(teacher_prediction, tuple):
            teacher_prediction = teacher_prediction[0]
        teacher_prediction = teacher_prediction.detach()
    expected_teacher_target_mse = float(torch.mean((teacher_prediction - evaluation_target).pow(2)).item())
    assert math.isclose(teacher_target_mse, expected_teacher_target_mse, rel_tol=1e-6, abs_tol=1e-6)
