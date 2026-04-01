# Benchmark AB Comparison Summary

- baseline: baseline
- variants: baseline_icbr

## Variant Metrics

| variant | metric | mean | median | std | min | max |
|---|---|---:|---:|---:|---:|---:|
| baseline | final_acc | 0.777767 | 0.779300 | 0.005257 | 0.770700 | 0.783300 |
| baseline | final_n_edge | 88.333333 | 88.000000 | 0.471405 | 88.000000 | 89.000000 |
| baseline | macro_auc | 0.951587 | 0.950857 | 0.001771 | 0.949877 | 0.954027 |
| baseline | run_total_wall_time_s | 149.814120 | 104.360397 | 78.448441 | 84.895639 | 260.186325 |
| baseline | symbolic_core_seconds | 56.559906 | 36.992289 | 27.738354 | 36.899604 | 95.787826 |
| baseline | symbolize_wall_time_s | 128.000426 | 98.021996 | 63.589353 | 69.563631 | 216.415651 |
| baseline | validation_mean_r2 | -0.482755 | -0.479511 | 0.016588 | -0.504498 | -0.464255 |
| baseline_icbr | final_acc | 0.788667 | 0.790700 | 0.009540 | 0.776100 | 0.799200 |
| baseline_icbr | final_n_edge | 88.333333 | 88.000000 | 0.471405 | 88.000000 | 89.000000 |
| baseline_icbr | macro_auc | 0.961440 | 0.961336 | 0.000695 | 0.960645 | 0.962338 |
| baseline_icbr | run_total_wall_time_s | 73.080290 | 70.895760 | 6.755389 | 66.118129 | 82.226982 |
| baseline_icbr | symbolic_core_seconds | 22.861778 | 21.150914 | 2.508906 | 21.025254 | 26.409164 |
| baseline_icbr | symbolize_wall_time_s | 70.118805 | 68.017761 | 6.818590 | 63.018931 | 79.319723 |
| baseline_icbr | validation_mean_r2 | -0.409281 | -0.366264 | 0.068989 | -0.506627 | -0.354950 |

## Baseline Pairwise Delta

| baseline | variant | metric | mean_delta | median_delta | std_delta | win | lose | tie |
|---|---|---|---:|---:|---:|---:|---:|---:|
| baseline | baseline_icbr | final_acc | 0.010900 | 0.011400 | 0.004301 | 3 | 0 | 0 |
| baseline | baseline_icbr | final_n_edge | 0.000000 | 0.000000 | 0.000000 | 0 | 0 | 3 |
| baseline | baseline_icbr | macro_auc | 0.009853 | 0.009789 | 0.001286 | 3 | 0 | 0 |
| baseline | baseline_icbr | run_total_wall_time_s | -76.733830 | -33.464638 | 71.827948 | 3 | 0 | 0 |
| baseline | baseline_icbr | symbolic_core_seconds | -33.698129 | -15.967035 | 25.230104 | 3 | 0 | 0 |
| baseline | baseline_icbr | symbolize_wall_time_s | -57.881621 | -30.004235 | 56.825858 | 3 | 0 | 0 |
| baseline | baseline_icbr | validation_mean_r2 | 0.073474 | 0.097991 | 0.054549 | 2 | 1 | 0 |

## Shared Numeric Stage Check

| stage_seed | shared_numeric_aligned | trace_aligned | shared_symbolic_prep_aligned | baseline_numeric_cache_hit | icbr_numeric_cache_hit | baseline_symbolic_prep_cache_hit | icbr_symbolic_prep_cache_hit |
|---:|---|---|---|---|---|---|---|
| 42 | True | True | True | True | True | False | True |
| 52 | True | True | True | True | True | False | True |
| 62 | True | True | True | True | True | False | True |

## Primary ICBR Effect

| metric | mean | median | std | min | max |
|---|---:|---:|---:|---:|---:|
| symbolic_core_speedup_vs_baseline | 2.377025 | 1.759422 | 0.883934 | 1.744587 | 3.627068 |
| final_teacher_imitation_mse_shift | -0.006009 | -0.006910 | 0.001299 | -0.006946 | -0.004172 |
| final_target_mse_shift | -0.008364 | -0.008328 | 0.000504 | -0.008998 | -0.007767 |
| final_target_r2_shift | 0.092972 | 0.092567 | 0.005597 | 0.086328 | 0.100020 |
| baseline_formula_export_success_rate | 1.000000 | 1.000000 | 0.000000 | 1.000000 | 1.000000 |
| icbr_formula_export_success_rate | 1.000000 | 1.000000 | 0.000000 | 1.000000 | 1.000000 |

## ICBR Mechanism Breakdown

| metric | mean | median | std | min | max |
|---|---:|---:|---:|---:|---:|
| icbr_candidate_generation_wall_time_s | 0.381959 | 0.337081 | 0.078951 | 0.315857 | 0.492938 |
| icbr_replay_rerank_wall_time_s | 22.344875 | 20.723840 | 2.403518 | 20.568012 | 25.742772 |
| icbr_candidate_share_of_core_time | 0.016544 | 0.016032 | 0.001566 | 0.014934 | 0.018665 |
| icbr_replay_share_of_core_time | 0.977609 | 0.978253 | 0.002108 | 0.974767 | 0.979808 |
| icbr_other_core_seconds | 0.134944 | 0.120161 | 0.027474 | 0.111217 | 0.173454 |
| icbr_replay_rank_inversion_rate | 0.113253 | 0.101124 | 0.051747 | 0.056818 | 0.181818 |

## Symbolize Trace Rhythm

| variant | rounds_mean | effective_rounds_mean | total_edges_removed_mean | mean_drop_ratio_mean | max_drop_ratio_mean |
|---|---:|---:|---:|---:|---:|
| baseline | 5.0000 | 3.6667 | 15.3333 | 0.033881 | 0.080582 |
| baseline_icbr | 5.0000 | 3.6667 | 15.3333 | 0.033881 | 0.080582 |

## Auto Conclusion

- Highest mean final_acc: baseline_icbr
- Most stable final_acc (lowest std): baseline
- Highest mean macro_auc: baseline_icbr
- Fastest symbolic_core_seconds: baseline_icbr
- Fastest symbolize_wall_time_s: baseline_icbr

- Pairwise note vs baseline:
  - baseline_icbr on final_acc: win=3, lose=0, median_delta=0.011400, mean_delta=0.010900
  - baseline_icbr on macro_auc: win=3, lose=0, median_delta=0.009789, mean_delta=0.009853
