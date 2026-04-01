# Benchmark AB Comparison Summary

- baseline: baseline_fastlib
- variants: baseline_icbr_fastlib

## Variant Metrics

| variant | metric | mean | median | std | min | max |
|---|---|---:|---:|---:|---:|---:|
| baseline_fastlib | final_acc | 0.794000 | 0.799700 | 0.010859 | 0.778800 | 0.803500 |
| baseline_fastlib | final_n_edge | 88.333333 | 88.000000 | 0.471405 | 88.000000 | 89.000000 |
| baseline_fastlib | macro_auc | 0.962537 | 0.962713 | 0.000750 | 0.961542 | 0.963354 |
| baseline_fastlib | run_total_wall_time_s | 334.638446 | 261.478977 | 167.154150 | 176.547860 | 565.888502 |
| baseline_fastlib | symbolic_core_seconds | 211.949580 | 161.017811 | 95.381006 | 129.245365 | 345.585565 |
| baseline_fastlib | symbolize_wall_time_s | 328.139783 | 251.685354 | 168.287164 | 171.182740 | 561.551255 |
| baseline_fastlib | validation_mean_r2 | -0.451777 | -0.408898 | 0.061204 | -0.538331 | -0.408101 |
| baseline_icbr_fastlib | final_acc | 0.793233 | 0.799100 | 0.010941 | 0.777900 | 0.802700 |
| baseline_icbr_fastlib | final_n_edge | 88.333333 | 88.000000 | 0.471405 | 88.000000 | 89.000000 |
| baseline_icbr_fastlib | macro_auc | 0.962634 | 0.962794 | 0.000690 | 0.961720 | 0.963386 |
| baseline_icbr_fastlib | run_total_wall_time_s | 76.947981 | 76.821946 | 1.051730 | 75.727530 | 78.294467 |
| baseline_icbr_fastlib | symbolic_core_seconds | 34.899150 | 34.991668 | 0.261437 | 34.542884 | 35.162897 |
| baseline_icbr_fastlib | symbolize_wall_time_s | 74.484392 | 74.378946 | 1.135263 | 73.149710 | 75.924521 |
| baseline_icbr_fastlib | validation_mean_r2 | -0.456489 | -0.422274 | 0.055795 | -0.535173 | -0.412021 |

## Baseline Pairwise Delta

| baseline | variant | metric | mean_delta | median_delta | std_delta | win | lose | tie |
|---|---|---|---:|---:|---:|---:|---:|---:|
| baseline_fastlib | baseline_icbr_fastlib | final_acc | -0.000767 | -0.000800 | 0.000125 | 0 | 3 | 0 |
| baseline_fastlib | baseline_icbr_fastlib | final_n_edge | 0.000000 | 0.000000 | 0.000000 | 0 | 0 | 3 |
| baseline_fastlib | baseline_icbr_fastlib | macro_auc | 0.000097 | 0.000081 | 0.000061 | 3 | 0 | 0 |
| baseline_fastlib | baseline_icbr_fastlib | run_total_wall_time_s | -257.690465 | -183.184510 | 167.875424 | 3 | 0 | 0 |
| baseline_fastlib | baseline_icbr_fastlib | symbolic_core_seconds | -177.050431 | -125.854914 | 95.621133 | 3 | 0 | 0 |
| baseline_fastlib | baseline_icbr_fastlib | symbolize_wall_time_s | -253.655391 | -175.760834 | 169.091437 | 3 | 0 | 0 |
| baseline_fastlib | baseline_icbr_fastlib | validation_mean_r2 | -0.004712 | -0.003920 | 0.006773 | 1 | 2 | 0 |

## Shared Numeric Stage Check

| stage_seed | shared_numeric_aligned | trace_aligned | shared_symbolic_prep_aligned | baseline_numeric_cache_hit | icbr_numeric_cache_hit | baseline_symbolic_prep_cache_hit | icbr_symbolic_prep_cache_hit |
|---:|---|---|---|---|---|---|---|
| 42 | True | True | True | True | True | True | True |
| 52 | True | True | True | True | True | True | True |
| 62 | True | True | True | True | True | True | True |

## Primary ICBR Effect

| metric | mean | median | std | min | max |
|---|---:|---:|---:|---:|---:|
| symbolic_core_speedup_vs_baseline | 6.092446 | 4.579196 | 2.789792 | 3.693604 | 10.004537 |
| final_teacher_imitation_mse_shift | 0.000062 | 0.000060 | 0.000006 | 0.000057 | 0.000070 |
| final_target_mse_shift | -0.000023 | -0.000015 | 0.000028 | -0.000061 | 0.000006 |
| final_target_r2_shift | 0.000258 | 0.000162 | 0.000311 | -0.000066 | 0.000678 |
| baseline_formula_export_success_rate | 1.000000 | 1.000000 | 0.000000 | 1.000000 | 1.000000 |
| icbr_formula_export_success_rate | 1.000000 | 1.000000 | 0.000000 | 1.000000 | 1.000000 |

## ICBR Mechanism Breakdown

| metric | mean | median | std | min | max |
|---|---:|---:|---:|---:|---:|
| icbr_candidate_generation_wall_time_s | 1.192465 | 1.220830 | 0.045347 | 1.128471 | 1.228094 |
| icbr_replay_rerank_wall_time_s | 33.592179 | 33.632677 | 0.217455 | 33.307923 | 33.835937 |
| icbr_candidate_share_of_core_time | 0.034162 | 0.034719 | 0.001067 | 0.032669 | 0.035097 |
| icbr_replay_share_of_core_time | 0.962558 | 0.962263 | 0.001277 | 0.961162 | 0.964248 |
| icbr_other_core_seconds | 0.114505 | 0.106490 | 0.011592 | 0.106129 | 0.130897 |
| icbr_replay_rank_inversion_rate | 0.252852 | 0.247191 | 0.014482 | 0.238636 | 0.272727 |

## Symbolize Trace Rhythm

| variant | rounds_mean | effective_rounds_mean | total_edges_removed_mean | mean_drop_ratio_mean | max_drop_ratio_mean |
|---|---:|---:|---:|---:|---:|
| baseline_fastlib | 5.0000 | 3.6667 | 15.3333 | 0.033881 | 0.080582 |
| baseline_icbr_fastlib | 5.0000 | 3.6667 | 15.3333 | 0.033881 | 0.080582 |

## Auto Conclusion

- Highest mean final_acc: baseline_fastlib
- Most stable final_acc (lowest std): baseline_fastlib
- Highest mean macro_auc: baseline_icbr_fastlib
- Fastest symbolic_core_seconds: baseline_icbr_fastlib
- Fastest symbolize_wall_time_s: baseline_icbr_fastlib

- Pairwise note vs baseline:
  - baseline_icbr_fastlib on final_acc: win=0, lose=3, median_delta=-0.000800, mean_delta=-0.000767
  - baseline_icbr_fastlib on macro_auc: win=3, lose=0, median_delta=0.000081, mean_delta=0.000097
