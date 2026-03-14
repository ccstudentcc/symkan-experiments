# Benchmark AB Comparison Summary

- baseline: baseline
- variants: adaptive, adaptive_auto

## Variant Metrics

| variant | metric | mean | median | std | min | max |
|---|---|---:|---:|---:|---:|---:|
| adaptive | export_wall_time_s | 75.719917 | 84.373186 | 12.882869 | 57.508284 | 85.278281 |
| adaptive | final_acc | 0.767767 | 0.764500 | 0.011742 | 0.755300 | 0.783500 |
| adaptive | final_n_edge | 85.333333 | 86.000000 | 2.494438 | 82.000000 | 88.000000 |
| adaptive | macro_auc | 0.948570 | 0.947740 | 0.002104 | 0.946510 | 0.951460 |
| adaptive | symbolic_total_seconds | 31.052998 | 31.112219 | 0.979082 | 29.825359 | 32.221415 |
| adaptive | validation_mean_r2 | -0.536085 | -0.514063 | 0.106147 | -0.675693 | -0.418499 |
| adaptive_auto | export_wall_time_s | 72.576891 | 67.904416 | 14.624108 | 57.465413 | 92.360845 |
| adaptive_auto | final_acc | 0.749100 | 0.745100 | 0.018588 | 0.728600 | 0.773600 |
| adaptive_auto | final_n_edge | 85.333333 | 88.000000 | 5.249339 | 78.000000 | 90.000000 |
| adaptive_auto | macro_auc | 0.943012 | 0.941397 | 0.004377 | 0.938644 | 0.948995 |
| adaptive_auto | symbolic_total_seconds | 30.883783 | 30.766319 | 1.755247 | 28.795194 | 33.089837 |
| adaptive_auto | validation_mean_r2 | -0.613704 | -0.593238 | 0.030555 | -0.656897 | -0.590979 |
| baseline | export_wall_time_s | 73.168666 | 74.430487 | 2.058069 | 70.266340 | 74.809172 |
| baseline | final_acc | 0.780733 | 0.780500 | 0.001034 | 0.779600 | 0.782100 |
| baseline | final_n_edge | 89.666667 | 90.000000 | 0.471405 | 89.000000 | 90.000000 |
| baseline | macro_auc | 0.954847 | 0.956314 | 0.002288 | 0.951616 | 0.956611 |
| baseline | symbolic_total_seconds | 33.267782 | 33.199039 | 0.365845 | 32.858059 | 33.746248 |
| baseline | validation_mean_r2 | -0.613534 | -0.618877 | 0.027055 | -0.643673 | -0.578052 |

## Baseline Pairwise Delta

| baseline | variant | metric | mean_delta | median_delta | std_delta | win | lose | tie |
|---|---|---|---:|---:|---:|---:|---:|---:|
| baseline | adaptive | export_wall_time_s | 2.551251 | 9.564014 | 13.948274 | 2 | 1 | 0 |
| baseline | adaptive | final_acc | -0.012967 | -0.016000 | 0.010709 | 1 | 2 | 0 |
| baseline | adaptive | final_n_edge | -4.333333 | -3.000000 | 2.624669 | 0 | 3 | 0 |
| baseline | adaptive | macro_auc | -0.006277 | -0.005106 | 0.001837 | 0 | 3 | 0 |
| baseline | adaptive | symbolic_total_seconds | -2.214784 | -1.745840 | 1.246497 | 0 | 3 | 0 |
| baseline | adaptive | validation_mean_r2 | 0.077448 | 0.063988 | 0.095353 | 2 | 1 | 0 |
| baseline | adaptive_auto | export_wall_time_s | -0.591775 | -6.904756 | 13.316488 | 1 | 2 | 0 |
| baseline | adaptive_auto | final_acc | -0.031633 | -0.037000 | 0.018399 | 0 | 3 | 0 |
| baseline | adaptive_auto | final_n_edge | -4.333333 | -1.000000 | 5.436502 | 0 | 2 | 1 |
| baseline | adaptive_auto | macro_auc | -0.011835 | -0.014917 | 0.006633 | 0 | 3 | 0 |
| baseline | adaptive_auto | symbolic_total_seconds | -2.383999 | -2.432720 | 2.116163 | 1 | 2 | 0 |
| baseline | adaptive_auto | validation_mean_r2 | -0.000171 | 0.027898 | 0.056387 | 2 | 1 | 0 |

## Symbolize Trace Rhythm

| variant | rounds_mean | effective_rounds_mean | total_edges_removed_mean | mean_drop_ratio_mean | max_drop_ratio_mean |
|---|---:|---:|---:|---:|---:|
| adaptive | 1.0000 | 1.0000 | 16.3333 | 0.158815 | 0.158815 |
| adaptive_auto | 3.6667 | 3.3333 | 12.6667 | 0.027287 | 0.100226 |
| baseline | 6.6667 | 5.3333 | 26.3333 | 0.035203 | 0.128140 |

## Auto Conclusion

- Highest mean final_acc: baseline
- Most stable final_acc (lowest std): baseline
- Highest mean macro_auc: baseline
- Fastest symbolic_total_seconds: adaptive_auto
- Fastest export_wall_time_s: adaptive_auto

- Pairwise note vs baseline:
  - adaptive on final_acc: win=1, lose=2, median_delta=-0.016000, mean_delta=-0.012967
  - adaptive on macro_auc: win=0, lose=3, median_delta=-0.005106, mean_delta=-0.006277
  - adaptive_auto on final_acc: win=0, lose=3, median_delta=-0.037000, mean_delta=-0.031633
  - adaptive_auto on macro_auc: win=0, lose=3, median_delta=-0.014917, mean_delta=-0.011835
