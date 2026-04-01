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
| baseline_icbr | run_total_wall_time_s | 71.447204 | 72.746447 | 2.354010 | 68.143149 | 73.452016 |
| baseline_icbr | symbolic_core_seconds | 26.114427 | 26.208229 | 0.224485 | 25.804865 | 26.330188 |
| baseline_icbr | symbolize_wall_time_s | 68.817573 | 70.056450 | 2.329805 | 65.554109 | 70.842161 |
| baseline_icbr | validation_mean_r2 | -0.409281 | -0.366264 | 0.068989 | -0.506627 | -0.354950 |

## Baseline Pairwise Delta

| baseline | variant | metric | mean_delta | median_delta | std_delta | win | lose | tie |
|---|---|---|---:|---:|---:|---:|---:|---:|
| baseline | baseline_icbr | final_acc | 0.010900 | 0.011400 | 0.004301 | 3 | 0 | 0 |
| baseline | baseline_icbr | final_n_edge | 0.000000 | 0.000000 | 0.000000 | 0 | 0 | 3 |
| baseline | baseline_icbr | macro_auc | 0.009853 | 0.009789 | 0.001286 | 3 | 0 | 0 |
| baseline | baseline_icbr | run_total_wall_time_s | -78.366916 | -31.613950 | 76.867134 | 3 | 0 | 0 |
| baseline | baseline_icbr | symbolic_core_seconds | -30.445479 | -10.784061 | 27.957359 | 3 | 0 | 0 |
| baseline | baseline_icbr | symbolize_wall_time_s | -59.182853 | -27.965546 | 61.865334 | 3 | 0 | 0 |
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
| symbolic_core_speedup_vs_baseline | 2.174967 | 1.411476 | 1.086859 | 1.401418 | 3.712007 |
| final_teacher_imitation_mse_shift | -0.006009 | -0.006910 | 0.001299 | -0.006946 | -0.004172 |
| final_target_mse_shift | -0.008364 | -0.008328 | 0.000504 | -0.008998 | -0.007767 |
| final_target_r2_shift | 0.092972 | 0.092567 | 0.005597 | 0.086328 | 0.100020 |
| baseline_formula_export_success_rate | 1.000000 | 1.000000 | 0.000000 | 1.000000 | 1.000000 |
| icbr_formula_export_success_rate | 1.000000 | 1.000000 | 0.000000 | 1.000000 | 1.000000 |

## ICBR Mechanism Breakdown

| metric | mean | median | std | min | max |
|---|---:|---:|---:|---:|---:|
| icbr_candidate_generation_wall_time_s | 0.349936 | 0.338095 | 0.016835 | 0.337968 | 0.373744 |
| icbr_replay_rerank_wall_time_s | 19.251307 | 19.356854 | 0.189021 | 18.985841 | 19.411226 |
| icbr_candidate_share_of_core_time | 0.013407 | 0.012895 | 0.000762 | 0.012841 | 0.014483 |
| icbr_replay_share_of_core_time | 0.737183 | 0.737223 | 0.001157 | 0.735747 | 0.738579 |
| icbr_other_core_seconds | 6.513185 | 6.513407 | 0.055354 | 6.445280 | 6.580868 |
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
