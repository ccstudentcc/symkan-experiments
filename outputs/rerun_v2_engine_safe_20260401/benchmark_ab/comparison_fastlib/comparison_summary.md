# Benchmark AB Comparison Summary

- baseline: baseline_fastlib
- variants: baseline_icbr_fastlib

## Variant Metrics

| variant | metric | mean | median | std | min | max |
|---|---|---:|---:|---:|---:|---:|
| baseline_fastlib | final_acc | 0.794000 | 0.799700 | 0.010859 | 0.778800 | 0.803500 |
| baseline_fastlib | final_n_edge | 88.333333 | 88.000000 | 0.471405 | 88.000000 | 89.000000 |
| baseline_fastlib | macro_auc | 0.962537 | 0.962713 | 0.000750 | 0.961542 | 0.963354 |
| baseline_fastlib | run_total_wall_time_s | 112.233492 | 111.820887 | 0.844226 | 111.469539 | 113.410049 |
| baseline_fastlib | symbolic_core_seconds | 75.187859 | 75.281426 | 0.151577 | 74.974051 | 75.308100 |
| baseline_fastlib | symbolize_wall_time_s | 110.162969 | 109.800572 | 0.851764 | 109.349303 | 111.339030 |
| baseline_fastlib | validation_mean_r2 | -0.451777 | -0.408898 | 0.061204 | -0.538331 | -0.408101 |
| baseline_icbr_fastlib | final_acc | 0.793233 | 0.799100 | 0.010941 | 0.777900 | 0.802700 |
| baseline_icbr_fastlib | final_n_edge | 88.333333 | 88.000000 | 0.471405 | 88.000000 | 89.000000 |
| baseline_icbr_fastlib | macro_auc | 0.962634 | 0.962794 | 0.000690 | 0.961720 | 0.963386 |
| baseline_icbr_fastlib | run_total_wall_time_s | 69.944645 | 69.531534 | 0.873096 | 69.143506 | 71.158896 |
| baseline_icbr_fastlib | symbolic_core_seconds | 31.990798 | 31.856789 | 0.230444 | 31.800533 | 32.315072 |
| baseline_icbr_fastlib | symbolize_wall_time_s | 67.817348 | 67.364007 | 0.813375 | 67.128468 | 68.959567 |
| baseline_icbr_fastlib | validation_mean_r2 | -0.456489 | -0.422274 | 0.055795 | -0.535173 | -0.412021 |

## Baseline Pairwise Delta

| baseline | variant | metric | mean_delta | median_delta | std_delta | win | lose | tie |
|---|---|---|---:|---:|---:|---:|---:|---:|
| baseline_fastlib | baseline_icbr_fastlib | final_acc | -0.000767 | -0.000800 | 0.000125 | 0 | 3 | 0 |
| baseline_fastlib | baseline_icbr_fastlib | final_n_edge | 0.000000 | 0.000000 | 0.000000 | 0 | 0 | 3 |
| baseline_fastlib | baseline_icbr_fastlib | macro_auc | 0.000097 | 0.000081 | 0.000061 | 3 | 0 | 0 |
| baseline_fastlib | baseline_icbr_fastlib | run_total_wall_time_s | -42.288847 | -42.251153 | 0.303024 | 3 | 0 | 0 |
| baseline_fastlib | baseline_icbr_fastlib | symbolic_core_seconds | -43.197061 | -43.424637 | 0.381985 | 3 | 0 | 0 |
| baseline_fastlib | baseline_icbr_fastlib | symbolize_wall_time_s | -42.345621 | -42.379463 | 0.281407 | 3 | 0 | 0 |
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
| symbolic_core_speedup_vs_baseline | 2.350452 | 2.363120 | 0.021563 | 2.320095 | 2.368140 |
| final_teacher_imitation_mse_shift | 0.000062 | 0.000060 | 0.000006 | 0.000057 | 0.000070 |
| final_target_mse_shift | -0.000023 | -0.000015 | 0.000028 | -0.000061 | 0.000006 |
| final_target_r2_shift | 0.000258 | 0.000162 | 0.000311 | -0.000066 | 0.000678 |
| baseline_formula_export_success_rate | 1.000000 | 1.000000 | 0.000000 | 1.000000 | 1.000000 |
| icbr_formula_export_success_rate | 1.000000 | 1.000000 | 0.000000 | 1.000000 | 1.000000 |

## ICBR Mechanism Breakdown

| metric | mean | median | std | min | max |
|---|---:|---:|---:|---:|---:|
| icbr_candidate_generation_wall_time_s | 1.138059 | 1.145054 | 0.019440 | 1.111536 | 1.157586 |
| icbr_replay_rerank_wall_time_s | 30.739668 | 30.606331 | 0.217230 | 30.566650 | 31.046021 |
| icbr_candidate_share_of_core_time | 0.035573 | 0.035822 | 0.000441 | 0.034953 | 0.035944 |
| icbr_replay_share_of_core_time | 0.960892 | 0.960748 | 0.000218 | 0.960729 | 0.961199 |
| icbr_other_core_seconds | 0.113072 | 0.111465 | 0.007009 | 0.105404 | 0.122346 |
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
