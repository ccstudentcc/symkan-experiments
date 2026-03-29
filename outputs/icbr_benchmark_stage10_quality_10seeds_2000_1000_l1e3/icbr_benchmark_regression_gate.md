# ICBR Benchmark Regression Gate

- Source summary: `outputs\icbr_benchmark_stage10_quality_10seeds_2000_1000_l1e3\icbr_benchmark_summary.json`
- Generated at UTC: 2026-03-29T06:27:19.016579+00:00
- Overall status: **PASS**
- Checks: 25, Failed: 0

## Check Details

| scope | task | metric | stat | op | threshold | value | status |
|---|---|---|---|---|---:|---:|---|
| overall | __all__ | teacher_quality_gate_pass | mean | >= | 0.95 | 1 | pass |
| overall | __all__ | formula_validation_result | mean | >= | 0.95 | 1 | pass |
| overall | __all__ | symbolic_speedup_vs_baseline | median | >= | 1.1 | 13.579 | pass |
| overall | __all__ | final_mse_loss_shift | mean | <= | 0.0005 | -7.79329e-05 | pass |
| overall | __all__ | symbolic_target_mse_shift | mean | <= | 0.0005 | -7.62255e-05 | pass |
| task | minimal | teacher_quality_gate_pass | mean | >= | 0.95 | 1 | pass |
| task | minimal | formula_validation_result | mean | >= | 0.95 | 1 | pass |
| task | minimal | symbolic_speedup_vs_baseline | median | >= | 1.1 | 15.8948 | pass |
| task | minimal | final_mse_loss_shift | mean | <= | 0.0005 | 8.96631e-05 | pass |
| task | minimal | symbolic_target_mse_shift | mean | <= | 0.0005 | 2.58993e-05 | pass |
| task | combo | teacher_quality_gate_pass | mean | >= | 0.95 | 1 | pass |
| task | combo | formula_validation_result | mean | >= | 0.95 | 1 | pass |
| task | combo | symbolic_speedup_vs_baseline | median | >= | 1.1 | 14.0662 | pass |
| task | combo | final_mse_loss_shift | mean | <= | 0.0005 | -0.000141865 | pass |
| task | combo | symbolic_target_mse_shift | mean | <= | 0.0005 | -4.31698e-05 | pass |
| task | poly_cubic | teacher_quality_gate_pass | mean | >= | 0.95 | 1 | pass |
| task | poly_cubic | formula_validation_result | mean | >= | 0.95 | 1 | pass |
| task | poly_cubic | symbolic_speedup_vs_baseline | median | >= | 1.1 | 13.515 | pass |
| task | poly_cubic | final_mse_loss_shift | mean | <= | 0.0005 | -1.37453e-05 | pass |
| task | poly_cubic | symbolic_target_mse_shift | mean | <= | 0.0005 | -1.25285e-05 | pass |
| task | trig_interaction | teacher_quality_gate_pass | mean | >= | 0.95 | 1 | pass |
| task | trig_interaction | formula_validation_result | mean | >= | 0.95 | 1 | pass |
| task | trig_interaction | symbolic_speedup_vs_baseline | median | >= | 1.1 | 12.33 | pass |
| task | trig_interaction | final_mse_loss_shift | mean | <= | 0.0005 | -0.000245785 | pass |
| task | trig_interaction | symbolic_target_mse_shift | mean | <= | 0.0005 | -0.000275103 | pass |

