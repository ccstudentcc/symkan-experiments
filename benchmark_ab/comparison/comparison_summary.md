# Benchmark AB Comparison Summary

- baseline: baseline
- variants: adaptive, adaptive_auto

## Variant Metrics

| variant | metric | mean | median | std | min | max |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| adaptive | export_wall_time_s | 94.478758 | 92.841081 | 12.924166 | 79.532457 | 111.062736 |
| adaptive | final_acc | 0.754033 | 0.755300 | 0.017741 | 0.731700 | 0.775100 |
| adaptive | final_n_edge | 86.666667 | 88.000000 | 3.399346 | 82.000000 | 90.000000 |
| adaptive | macro_auc | 0.948044 | 0.945523 | 0.004009 | 0.944907 | 0.953703 |
| adaptive | symbolic_total_seconds | 47.597252 | 48.883779 | 3.153120 | 43.256437 | 50.651539 |
| adaptive | validation_mean_r2 | -0.500101 | -0.445721 | 0.108979 | -0.652178 | -0.402405 |
| adaptive_auto | export_wall_time_s | 99.135381 | 100.927199 | 10.636341 | 85.305421 | 111.173523 |
| adaptive_auto | final_acc | 0.755133 | 0.761300 | 0.011211 | 0.739400 | 0.764700 |
| adaptive_auto | final_n_edge | 88.000000 | 89.000000 | 2.160247 | 85.000000 | 90.000000 |
| adaptive_auto | macro_auc | 0.948704 | 0.949400 | 0.001021 | 0.947260 | 0.949451 |
| adaptive_auto | symbolic_total_seconds | 48.588935 | 49.012122 | 1.581085 | 46.475913 | 50.278769 |
| adaptive_auto | validation_mean_r2 | -0.480890 | -0.456150 | 0.064658 | -0.569496 | -0.417024 |
| baseline | export_wall_time_s | 124.242818 | 123.768612 | 2.330939 | 121.654809 | 127.305033 |
| baseline | final_acc | 0.732233 | 0.768600 | 0.060337 | 0.647200 | 0.780900 |
| baseline | final_n_edge | 89.000000 | 89.000000 | 0.816497 | 88.000000 | 90.000000 |
| baseline | macro_auc | 0.946050 | 0.953607 | 0.013748 | 0.926757 | 0.957786 |
| baseline | symbolic_total_seconds | 48.609857 | 48.354937 | 1.989065 | 46.311244 | 51.163390 |
| baseline | validation_mean_r2 | -0.587365 | -0.580844 | 0.125301 | -0.743982 | -0.437267 |

## Baseline Pairwise Delta

| baseline | variant | metric | mean_delta | median_delta | std_delta | win | lose | tie |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| baseline | adaptive | export_wall_time_s | -29.764060 | -28.813728 | 11.448184 | 0 | 3 | 0 |
| baseline | adaptive | final_acc | 0.021800 | -0.013300 | 0.076442 | 1 | 2 | 0 |
| baseline | adaptive | final_n_edge | -2.333333 | -2.000000 | 3.681787 | 1 | 2 | 0 |
| baseline | adaptive | macro_auc | 0.001994 | -0.008084 | 0.017752 | 1 | 2 | 0 |
| baseline | adaptive | symbolic_total_seconds | -1.012605 | 0.528843 | 5.117344 | 2 | 1 | 0 |
| baseline | adaptive | validation_mean_r2 | 0.087263 | 0.178439 | 0.219197 | 2 | 1 | 0 |
| baseline | adaptive_auto | export_wall_time_s | -25.107437 | -20.727610 | 9.628539 | 0 | 3 | 0 |
| baseline | adaptive_auto | final_acc | 0.022900 | -0.019600 | 0.067007 | 1 | 2 | 0 |
| baseline | adaptive_auto | final_n_edge | -1.000000 | 0.000000 | 2.943920 | 1 | 1 | 1 |
| baseline | adaptive_auto | macro_auc | 0.002654 | -0.006347 | 0.014158 | 1 | 2 | 0 |
| baseline | adaptive_auto | symbolic_total_seconds | -0.020922 | 0.657185 | 3.565776 | 2 | 1 | 0 |
| baseline | adaptive_auto | validation_mean_r2 | 0.106475 | 0.163820 | 0.176218 | 2 | 1 | 0 |

## Symbolize Trace Rhythm

| variant | rounds_mean | effective_rounds_mean | total_edges_removed_mean | mean_drop_ratio_mean | max_drop_ratio_mean |
| --- | ---: | ---: | ---: | ---: | ---: |
| adaptive | 1.0000 | 1.0000 | 15.6667 |  |  |
| adaptive_auto | 4.3333 | 3.0000 | 9.3333 | 0.023743 | 0.058969 |
| baseline | 16.6667 | 9.3333 | 30.6667 |  |  |

## Auto Conclusion

- Highest mean final_acc: adaptive_auto
- Most stable final_acc (lowest std): adaptive_auto
- Highest mean macro_auc: adaptive_auto
- Fastest symbolic_total_seconds: adaptive
- Fastest export_wall_time_s: adaptive

- Pairwise note vs baseline:
  - adaptive on final_acc: win=1, lose=2, median_delta=-0.013300, mean_delta=0.021800
  - adaptive on macro_auc: win=1, lose=2, median_delta=-0.008084, mean_delta=0.001994
  - adaptive_auto on final_acc: win=1, lose=2, median_delta=-0.019600, mean_delta=0.022900
  - adaptive_auto on macro_auc: win=1, lose=2, median_delta=-0.006347, mean_delta=0.002654
