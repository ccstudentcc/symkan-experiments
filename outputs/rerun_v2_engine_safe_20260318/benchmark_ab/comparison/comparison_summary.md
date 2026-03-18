# Benchmark AB Comparison Summary

- baseline: baseline
- variants: adaptive, adaptive_auto

## Variant Metrics

| variant | metric | mean | median | std | min | max |
|---|---|---:|---:|---:|---:|---:|
| adaptive | final_acc | 0.749967 | 0.762700 | 0.022086 | 0.718900 | 0.768300 |
| adaptive | final_n_edge | 88.000000 | 88.000000 | 1.632993 | 86.000000 | 90.000000 |
| adaptive | macro_auc | 0.944940 | 0.945277 | 0.005455 | 0.938098 | 0.951447 |
| adaptive | run_total_wall_time_s | 143.788060 | 151.264627 | 13.513479 | 124.818333 | 155.281220 |
| adaptive | symbolic_core_seconds | 35.004028 | 35.607150 | 1.032304 | 33.551095 | 35.853841 |
| adaptive | symbolize_wall_time_s | 82.780346 | 87.979429 | 11.535625 | 66.789273 | 93.572336 |
| adaptive | validation_mean_r2 | -0.669981 | -0.737309 | 0.193930 | -0.866564 | -0.406071 |
| adaptive_auto | final_acc | 0.749567 | 0.762400 | 0.020380 | 0.720800 | 0.765500 |
| adaptive_auto | final_n_edge | 88.666667 | 89.000000 | 0.471405 | 88.000000 | 89.000000 |
| adaptive_auto | macro_auc | 0.946627 | 0.949055 | 0.004413 | 0.940434 | 0.950392 |
| adaptive_auto | run_total_wall_time_s | 133.625230 | 132.789508 | 3.746559 | 129.511951 | 138.574232 |
| adaptive_auto | symbolic_core_seconds | 34.975766 | 34.809615 | 0.619226 | 34.314223 | 35.803460 |
| adaptive_auto | symbolize_wall_time_s | 72.956179 | 73.990267 | 5.940789 | 65.218508 | 79.659763 |
| adaptive_auto | validation_mean_r2 | -0.596773 | -0.535755 | 0.113739 | -0.756171 | -0.498392 |
| baseline | final_acc | 0.782600 | 0.786700 | 0.008626 | 0.770600 | 0.790500 |
| baseline | final_n_edge | 89.000000 | 89.000000 | 0.816497 | 88.000000 | 90.000000 |
| baseline | macro_auc | 0.954790 | 0.954972 | 0.002360 | 0.951813 | 0.957584 |
| baseline | run_total_wall_time_s | 146.168036 | 143.887859 | 8.286837 | 137.352819 | 157.263430 |
| baseline | symbolic_core_seconds | 35.968291 | 36.255474 | 0.797787 | 34.879797 | 36.769602 |
| baseline | symbolize_wall_time_s | 80.304843 | 79.944819 | 6.027378 | 73.109441 | 87.860268 |
| baseline | validation_mean_r2 | -0.605568 | -0.588944 | 0.071852 | -0.700695 | -0.527065 |

## Baseline Pairwise Delta

| baseline | variant | metric | mean_delta | median_delta | std_delta | win | lose | tie |
|---|---|---|---:|---:|---:|---:|---:|---:|
| baseline | adaptive | final_acc | -0.032633 | -0.027800 | 0.014018 | 0 | 3 | 0 |
| baseline | adaptive | final_n_edge | -1.000000 | 0.000000 | 1.414214 | 0 | 1 | 2 |
| baseline | adaptive | macro_auc | -0.009850 | -0.006537 | 0.004970 | 0 | 3 | 0 |
| baseline | adaptive | run_total_wall_time_s | -2.379976 | -1.982210 | 13.467511 | 1 | 2 | 0 |
| baseline | adaptive | symbolic_core_seconds | -0.964263 | -1.162452 | 1.508235 | 1 | 2 | 0 |
| baseline | adaptive | symbolize_wall_time_s | 2.475503 | 5.712068 | 11.668023 | 2 | 1 | 0 |
| baseline | adaptive | validation_mean_r2 | -0.064414 | -0.036614 | 0.163917 | 1 | 2 | 0 |
| baseline | adaptive_auto | final_acc | -0.033033 | -0.025000 | 0.011859 | 0 | 3 | 0 |
| baseline | adaptive_auto | final_n_edge | -0.333333 | 0.000000 | 1.247219 | 1 | 1 | 1 |
| baseline | adaptive_auto | macro_auc | -0.008163 | -0.007192 | 0.004858 | 0 | 3 | 0 |
| baseline | adaptive_auto | run_total_wall_time_s | -12.542806 | -11.098351 | 11.872151 | 1 | 2 | 0 |
| baseline | adaptive_auto | symbolic_core_seconds | -0.992525 | -1.445859 | 1.416243 | 1 | 2 | 0 |
| baseline | adaptive_auto | symbolize_wall_time_s | -7.348663 | -0.285056 | 10.824322 | 1 | 2 | 0 |
| baseline | adaptive_auto | validation_mean_r2 | 0.008795 | -0.008690 | 0.151366 | 1 | 2 | 0 |

## Symbolize Trace Rhythm

| variant | rounds_mean | effective_rounds_mean | total_edges_removed_mean | mean_drop_ratio_mean | max_drop_ratio_mean |
|---|---:|---:|---:|---:|---:|
| adaptive | 0.6667 | 0.6667 | 11.3333 | 0.151404 | 0.151404 |
| adaptive_auto | 4.6667 | 3.6667 | 12.0000 | 0.024399 | 0.053290 |
| baseline | 6.3333 | 5.3333 | 22.6667 | 0.053042 | 0.122991 |

## Auto Conclusion

- Highest mean final_acc: baseline
- Most stable final_acc (lowest std): baseline
- Highest mean macro_auc: baseline
- Fastest symbolic_core_seconds: adaptive_auto
- Fastest symbolize_wall_time_s: adaptive_auto

- Pairwise note vs baseline:
  - adaptive on final_acc: win=0, lose=3, median_delta=-0.027800, mean_delta=-0.032633
  - adaptive on macro_auc: win=0, lose=3, median_delta=-0.006537, mean_delta=-0.009850
  - adaptive_auto on final_acc: win=0, lose=3, median_delta=-0.025000, mean_delta=-0.033033
  - adaptive_auto on macro_auc: win=0, lose=3, median_delta=-0.007192, mean_delta=-0.008163
