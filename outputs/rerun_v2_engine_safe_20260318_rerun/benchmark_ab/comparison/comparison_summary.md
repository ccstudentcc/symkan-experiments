# Benchmark AB Comparison Summary

- baseline: baseline
- variants: adaptive, adaptive_auto

## Variant Metrics

| variant | metric | mean | median | std | min | max |
|---|---|---:|---:|---:|---:|---:|
| adaptive | final_acc | 0.742533 | 0.758400 | 0.025247 | 0.706900 | 0.762300 |
| adaptive | final_n_edge | 86.000000 | 88.000000 | 3.559026 | 81.000000 | 89.000000 |
| adaptive | macro_auc | 0.945706 | 0.949055 | 0.005695 | 0.937688 | 0.950375 |
| adaptive | run_total_wall_time_s | 209.552334 | 253.291445 | 63.807734 | 119.328496 | 256.037062 |
| adaptive | symbolic_core_seconds | 47.499191 | 33.166994 | 20.641635 | 32.641286 | 76.689293 |
| adaptive | symbolize_wall_time_s | 104.127099 | 63.394783 | 59.782909 | 60.332107 | 188.654406 |
| adaptive | validation_mean_r2 | -0.646339 | -0.535531 | 0.183572 | -0.905063 | -0.498423 |
| adaptive_auto | final_acc | 0.751467 | 0.762300 | 0.017632 | 0.726600 | 0.765500 |
| adaptive_auto | final_n_edge | 89.000000 | 89.000000 | 0.816497 | 88.000000 | 90.000000 |
| adaptive_auto | macro_auc | 0.946249 | 0.949055 | 0.004944 | 0.939300 | 0.950392 |
| adaptive_auto | run_total_wall_time_s | 130.715215 | 127.277306 | 11.246623 | 118.985549 | 145.882790 |
| adaptive_auto | symbolic_core_seconds | 33.259280 | 33.409406 | 0.521054 | 32.559443 | 33.808991 |
| adaptive_auto | symbolize_wall_time_s | 74.526931 | 77.228590 | 10.984734 | 59.927616 | 86.424587 |
| adaptive_auto | validation_mean_r2 | -0.552361 | -0.498423 | 0.149342 | -0.756171 | -0.402489 |
| baseline | final_acc | 0.777433 | 0.769700 | 0.013937 | 0.765600 | 0.797000 |
| baseline | final_n_edge | 88.666667 | 88.000000 | 0.942809 | 88.000000 | 90.000000 |
| baseline | macro_auc | 0.956107 | 0.956221 | 0.002493 | 0.952997 | 0.959101 |
| baseline | run_total_wall_time_s | 153.470521 | 151.746348 | 8.425588 | 144.122015 | 164.543201 |
| baseline | symbolic_core_seconds | 33.867724 | 34.268971 | 0.689998 | 32.896778 | 34.437422 |
| baseline | symbolize_wall_time_s | 88.751556 | 86.297721 | 8.737565 | 79.490309 | 100.466638 |
| baseline | validation_mean_r2 | -0.672284 | -0.735966 | 0.091875 | -0.738525 | -0.542361 |

## Baseline Pairwise Delta

| baseline | variant | metric | mean_delta | median_delta | std_delta | win | lose | tie |
|---|---|---|---:|---:|---:|---:|---:|---:|
| baseline | adaptive | final_acc | -0.034900 | -0.011300 | 0.039169 | 0 | 3 | 0 |
| baseline | adaptive | final_n_edge | -2.666667 | -2.000000 | 3.299832 | 2 | 1 | 0 |
| baseline | adaptive | macro_auc | -0.010401 | -0.007167 | 0.008005 | 0 | 3 | 0 |
| baseline | adaptive | run_total_wall_time_s | 56.081813 | 104.290714 | 71.655142 | 1 | 2 | 0 |
| baseline | adaptive | symbolic_core_seconds | 13.631467 | -1.101977 | 21.328964 | 2 | 1 | 0 |
| baseline | adaptive | symbolize_wall_time_s | 15.375543 | -25.965615 | 66.473338 | 2 | 1 | 0 |
| baseline | adaptive | validation_mean_r2 | 0.025945 | 0.006830 | 0.165518 | 2 | 1 | 0 |
| baseline | adaptive_auto | final_acc | -0.025967 | -0.004200 | 0.031421 | 0 | 3 | 0 |
| baseline | adaptive_auto | final_n_edge | 0.333333 | 1.000000 | 1.699673 | 1 | 2 | 0 |
| baseline | adaptive_auto | macro_auc | -0.009858 | -0.007167 | 0.007273 | 0 | 3 | 0 |
| baseline | adaptive_auto | run_total_wall_time_s | -22.755306 | -32.760799 | 17.432779 | 2 | 1 | 0 |
| baseline | adaptive_auto | symbolic_core_seconds | -0.608444 | -0.459981 | 0.981591 | 2 | 1 | 0 |
| baseline | adaptive_auto | symbolize_wall_time_s | -14.224624 | -23.238047 | 15.016143 | 2 | 1 | 0 |
| baseline | adaptive_auto | validation_mean_r2 | 0.119923 | 0.139872 | 0.105131 | 2 | 1 | 0 |

## Symbolize Trace Rhythm

| variant | rounds_mean | effective_rounds_mean | total_edges_removed_mean | mean_drop_ratio_mean | max_drop_ratio_mean |
|---|---:|---:|---:|---:|---:|
| adaptive | 0.6667 | 0.6667 | 14.6667 | 0.203953 | 0.203953 |
| adaptive_auto | 3.3333 | 2.6667 | 9.0000 | 0.019431 | 0.033532 |
| baseline | 10.6667 | 6.6667 | 23.3333 | 0.027671 | 0.088960 |

## Auto Conclusion

- Highest mean final_acc: baseline
- Most stable final_acc (lowest std): baseline
- Highest mean macro_auc: baseline
- Fastest symbolic_core_seconds: adaptive_auto
- Fastest symbolize_wall_time_s: adaptive_auto

- Pairwise note vs baseline:
  - adaptive on final_acc: win=0, lose=3, median_delta=-0.011300, mean_delta=-0.034900
  - adaptive on macro_auc: win=0, lose=3, median_delta=-0.007167, mean_delta=-0.010401
  - adaptive_auto on final_acc: win=0, lose=3, median_delta=-0.004200, mean_delta=-0.025967
  - adaptive_auto on macro_auc: win=0, lose=3, median_delta=-0.007167, mean_delta=-0.009858
