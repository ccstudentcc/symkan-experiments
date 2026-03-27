# Benchmark AB Comparison Summary

- baseline: baseline
- variants: radial_bf

## Variant Metrics

| variant | metric | mean | median | std | min | max |
|---|---|---:|---:|---:|---:|---:|
| baseline | final_acc | 0.777433 | 0.769700 | 0.013937 | 0.765600 | 0.797000 |
| baseline | final_n_edge | 88.666667 | 88.000000 | 0.942809 | 88.000000 | 90.000000 |
| baseline | macro_auc | 0.956107 | 0.956221 | 0.002493 | 0.952997 | 0.959101 |
| baseline | run_total_wall_time_s | 201.644621 | 208.579634 | 18.250213 | 176.647260 | 219.706968 |
| baseline | symbolic_core_seconds | 44.329937 | 45.755389 | 2.050448 | 41.430303 | 45.804120 |
| baseline | symbolize_wall_time_s | 118.647711 | 119.778940 | 14.898043 | 99.862114 | 136.302080 |
| baseline | validation_mean_r2 | -0.549509 | -0.570796 | 0.088075 | -0.645148 | -0.432584 |
| radial_bf | final_acc | 0.765400 | 0.769000 | 0.005666 | 0.757400 | 0.769800 |
| radial_bf | final_n_edge | 89.000000 | 89.000000 | 0.816497 | 88.000000 | 90.000000 |
| radial_bf | macro_auc | 0.953788 | 0.955118 | 0.004489 | 0.947747 | 0.958498 |
| radial_bf | run_total_wall_time_s | 136.664280 | 135.823769 | 1.666350 | 135.177904 | 138.991166 |
| radial_bf | symbolic_core_seconds | 40.865443 | 41.088505 | 0.586093 | 40.062580 | 41.445243 |
| radial_bf | symbolize_wall_time_s | 76.367098 | 76.820645 | 1.832915 | 73.930102 | 78.350548 |
| radial_bf | validation_mean_r2 | -0.746382 | -0.457732 | 0.410943 | -1.327538 | -0.453876 |

## Baseline Pairwise Delta

| baseline | variant | metric | mean_delta | median_delta | std_delta | win | lose | tie |
|---|---|---|---:|---:|---:|---:|---:|---:|
| baseline | radial_bf | final_acc | -0.012033 | -0.008200 | 0.011153 | 0 | 3 | 0 |
| baseline | radial_bf | final_n_edge | 0.333333 | 1.000000 | 1.699673 | 1 | 2 | 0 |
| baseline | radial_bf | macro_auc | -0.002319 | -0.001104 | 0.006935 | 1 | 2 | 0 |
| baseline | radial_bf | run_total_wall_time_s | -64.980341 | -69.588468 | 18.137813 | 3 | 0 | 0 |
| baseline | radial_bf | symbolic_core_seconds | -3.464494 | -4.310146 | 2.284097 | 3 | 0 | 0 |
| baseline | radial_bf | symbolize_wall_time_s | -42.280613 | -41.428392 | 16.067917 | 3 | 0 | 0 |
| baseline | radial_bf | validation_mean_r2 | -0.196873 | -0.025148 | 0.405627 | 1 | 2 | 0 |

## Symbolize Trace Rhythm

| variant | rounds_mean | effective_rounds_mean | total_edges_removed_mean | mean_drop_ratio_mean | max_drop_ratio_mean |
|---|---:|---:|---:|---:|---:|
| baseline | 10.6667 | 6.6667 | 23.3333 | 0.027671 | 0.088960 |
| radial_bf | 3.0000 | 2.6667 | 15.0000 | 0.044928 | 0.108470 |

## Auto Conclusion

- Highest mean final_acc: baseline
- Most stable final_acc (lowest std): radial_bf
- Highest mean macro_auc: baseline
- Fastest symbolic_core_seconds: radial_bf
- Fastest symbolize_wall_time_s: radial_bf

- Pairwise note vs baseline:
  - radial_bf on final_acc: win=0, lose=3, median_delta=-0.008200, mean_delta=-0.012033
  - radial_bf on macro_auc: win=1, lose=2, median_delta=-0.001104, mean_delta=-0.002319
