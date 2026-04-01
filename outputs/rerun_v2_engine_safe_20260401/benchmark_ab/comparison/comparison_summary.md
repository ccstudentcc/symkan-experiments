# Benchmark AB Comparison Summary

- baseline: baseline
- variants: baseline_icbr

## Variant Metrics

| variant | metric | mean | median | std | min | max |
|---|---|---:|---:|---:|---:|---:|
| baseline | final_acc | 0.777467 | 0.779300 | 0.004949 | 0.770700 | 0.782400 |
| baseline | final_n_edge | 88.333333 | 88.000000 | 0.471405 | 88.000000 | 89.000000 |
| baseline | macro_auc | 0.951264 | 0.950857 | 0.001331 | 0.949877 | 0.953059 |
| baseline | run_total_wall_time_s | 69.864499 | 65.924048 | 6.331691 | 64.871241 | 78.798209 |
| baseline | symbolic_core_seconds | 33.297856 | 33.271347 | 0.054991 | 33.247794 | 33.374427 |
| baseline | symbolize_wall_time_s | 68.013948 | 63.968896 | 6.367529 | 63.068957 | 77.003992 |
| baseline | validation_mean_r2 | -0.486988 | -0.479511 | 0.012425 | -0.504498 | -0.476955 |
| baseline_icbr | final_acc | 0.788667 | 0.790700 | 0.009540 | 0.776100 | 0.799200 |
| baseline_icbr | final_n_edge | 88.333333 | 88.000000 | 0.471405 | 88.000000 | 89.000000 |
| baseline_icbr | macro_auc | 0.961440 | 0.961336 | 0.000695 | 0.960645 | 0.962338 |
| baseline_icbr | run_total_wall_time_s | 62.462939 | 64.152287 | 2.468532 | 58.972503 | 64.264026 |
| baseline_icbr | symbolic_core_seconds | 19.013927 | 18.816274 | 0.321209 | 18.758547 | 19.466960 |
| baseline_icbr | symbolize_wall_time_s | 60.000633 | 61.606118 | 2.364092 | 56.658165 | 61.737617 |
| baseline_icbr | validation_mean_r2 | -0.409281 | -0.366264 | 0.068989 | -0.506627 | -0.354950 |

## Baseline Pairwise Delta

| baseline | variant | metric | mean_delta | median_delta | std_delta | win | lose | tie |
|---|---|---|---:|---:|---:|---:|---:|---:|
| baseline | baseline_icbr | final_acc | 0.011200 | 0.011400 | 0.004656 | 3 | 0 | 0 |
| baseline | baseline_icbr | final_n_edge | 0.000000 | 0.000000 | 0.000000 | 0 | 0 | 3 |
| baseline | baseline_icbr | macro_auc | 0.010176 | 0.009789 | 0.000931 | 3 | 0 | 0 |
| baseline | baseline_icbr | run_total_wall_time_s | -7.401560 | -6.951545 | 5.649013 | 3 | 0 | 0 |
| baseline | baseline_icbr | symbolic_core_seconds | -14.283929 | -14.455073 | 0.361749 | 3 | 0 | 0 |
| baseline | baseline_icbr | symbolize_wall_time_s | -8.013315 | -7.310731 | 5.764088 | 3 | 0 | 0 |
| baseline | baseline_icbr | validation_mean_r2 | 0.077707 | 0.110690 | 0.056737 | 2 | 1 | 0 |

## Shared Numeric Stage Check

| stage_seed | shared_numeric_aligned | trace_aligned | shared_symbolic_prep_aligned | baseline_numeric_cache_hit | icbr_numeric_cache_hit | baseline_symbolic_prep_cache_hit | icbr_symbolic_prep_cache_hit |
|---:|---|---|---|---|---|---|---|
| 42 | True | True | True | True | True | True | True |
| 52 | True | True | True | True | True | True | True |
| 62 | True | True | True | True | True | True | True |

## Primary ICBR Effect

| metric | mean | median | std | min | max |
|---|---:|---:|---:|---:|---:|
| symbolic_core_speedup_vs_baseline | 1.751763 | 1.768222 | 0.031329 | 1.707909 | 1.779158 |
| final_teacher_imitation_mse_shift | -0.006330 | -0.006910 | 0.001579 | -0.007907 | -0.004172 |
| final_target_mse_shift | -0.008691 | -0.008328 | 0.000939 | -0.009978 | -0.007767 |
| final_target_r2_shift | 0.096602 | 0.092567 | 0.010434 | 0.086328 | 0.110912 |
| baseline_formula_export_success_rate | 1.000000 | 1.000000 | 0.000000 | 1.000000 | 1.000000 |
| icbr_formula_export_success_rate | 1.000000 | 1.000000 | 0.000000 | 1.000000 | 1.000000 |

## ICBR Mechanism Breakdown

| metric | mean | median | std | min | max |
|---|---:|---:|---:|---:|---:|
| icbr_candidate_generation_wall_time_s | 0.333292 | 0.326695 | 0.013212 | 0.321451 | 0.351729 |
| icbr_replay_rerank_wall_time_s | 18.566778 | 18.384944 | 0.329835 | 18.285689 | 19.029702 |
| icbr_candidate_share_of_core_time | 0.017539 | 0.017084 | 0.000866 | 0.016782 | 0.018750 |
| icbr_replay_share_of_core_time | 0.976469 | 0.977077 | 0.001201 | 0.974792 | 0.977538 |
| icbr_other_core_seconds | 0.113857 | 0.110563 | 0.005150 | 0.109879 | 0.121129 |
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
  - baseline_icbr on final_acc: win=3, lose=0, median_delta=0.011400, mean_delta=0.011200
  - baseline_icbr on macro_auc: win=3, lose=0, median_delta=0.009789, mean_delta=0.010176
