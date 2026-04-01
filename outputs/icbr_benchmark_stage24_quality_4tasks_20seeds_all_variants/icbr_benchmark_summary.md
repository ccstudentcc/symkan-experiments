# ICBR Benchmark Summary

## Run Config

- Profile: quality
- Run mode: full
- Tasks: minimal, poly_cubic, combo, trig_interaction
- Seeds: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20
- Train/Calibration/Test samples per task: 1000/500/500
- Train steps: 200, lr: 0.01, lamb: 0.001
- Teacher cache: mode=readwrite, dir=outputs\teacher_cache_stage24_quality_4tasks_20seeds, version=v1
- ICBR shortlist topk: 3, grid_number: 21, iteration: 2
- Variants: baseline, icbr_full, icbr_no_replay, icbr_no_shared, icbr_refit_commit
- Teacher prune policy: enabled=True, node_th=0.01, edge_th=0.01, prune_iters=1

## Task-Level Aggregate Stats

| task | n | teacher_cache_hit_mean | teacher_mse_mean | teacher_r2_mean | teacher_gate_pass_mean | baseline_symbolic_mean | icbr_symbolic_mean | delta_mean | delta_median | speedup_mean | speedup_median | imitation_mse_shift_mean | target_mse_shift_mean | formula_export_success_mean |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| minimal | 20 | 0.0000 | 5.078931e-04 | 0.998987 | 1.0000 | 1.219296 | 0.105048 | 1.114247 | 1.117195 | 11.6276 | 11.6746 | 1.391148e-05 | 7.024868e-06 | 1.0000 |
| poly_cubic | 20 | 0.0000 | 2.870665e-03 | 0.941767 | 1.0000 | 5.743161 | 0.388451 | 5.354710 | 5.490280 | 14.5642 | 14.8595 | -1.039194e-04 | -1.159023e-04 | 1.0000 |
| combo | 20 | 0.0000 | 8.390552e-03 | 0.985574 | 1.0000 | 6.897983 | 0.456061 | 6.441922 | 6.562301 | 15.1362 | 15.1535 | -2.774328e-05 | -1.361565e-04 | 1.0000 |
| trig_interaction | 20 | 0.0000 | 8.631814e-03 | 0.988115 | 1.0000 | 16.688776 | 1.132597 | 15.556178 | 15.323735 | 14.7317 | 14.7379 | -4.595893e-04 | -7.299085e-04 | 1.0000 |

## Statistical Significance (by task)

| task | metric | favorable_direction | n_total | n_finite | n_effective | improved | worsened | ties | p_value_two_sided | mean_delta_ci95 |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| minimal | symbolic_wall_time_delta_s | positive | 20 | 20 | 20 | 20 | 0 | 0 | 0.000002 | [1.107867e+00, 1.119952e+00] |
| minimal | imitation_mse_shift | negative | 20 | 20 | 20 | 2 | 18 | 0 | 0.000402 | [8.356827e-06, 1.947088e-05] |
| poly_cubic | symbolic_wall_time_delta_s | positive | 20 | 20 | 20 | 20 | 0 | 0 | 0.000002 | [4.683256e+00, 6.010212e+00] |
| poly_cubic | imitation_mse_shift | negative | 20 | 20 | 20 | 11 | 9 | 0 | 0.823803 | [-3.010438e-04, 4.725553e-05] |
| combo | symbolic_wall_time_delta_s | positive | 20 | 20 | 20 | 20 | 0 | 0 | 0.000002 | [6.235119e+00, 6.596354e+00] |
| combo | imitation_mse_shift | negative | 20 | 20 | 20 | 13 | 7 | 0 | 0.263176 | [-6.961073e-05, 2.074580e-05] |
| trig_interaction | symbolic_wall_time_delta_s | positive | 20 | 20 | 20 | 20 | 0 | 0 | 0.000002 | [1.502422e+01, 1.608152e+01] |
| trig_interaction | imitation_mse_shift | negative | 20 | 20 | 20 | 14 | 6 | 0 | 0.115318 | [-7.701807e-04, -1.628405e-04] |

## Variant Ablation Aggregate Stats (Stage 15)

| task | variant | n | teacher_gate_pass_mean | formula_export_success_mean | symbolic_mean_s | speedup_mean_x | imitation_mse_shift_mean | target_mse_shift_mean | replay_rank_inversion_mean | refit_drift_l2_mean |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| minimal | baseline | 20 | 1.0000 | 1.0000 | 1.219296 | 1.0000 | 0.000000e+00 | 0.000000e+00 | nan | nan |
| minimal | icbr_full | 20 | 1.0000 | 1.0000 | 0.105048 | 11.6276 | 1.391148e-05 | 7.024868e-06 | 0.000000 | nan |
| minimal | icbr_no_replay | 20 | 1.0000 | 1.0000 | 0.100349 | 12.1856 | 1.391148e-05 | 7.024868e-06 | nan | nan |
| minimal | icbr_no_shared | 20 | 1.0000 | 1.0000 | 0.101425 | 12.0326 | 1.391148e-05 | 7.024868e-06 | 0.000000 | nan |
| minimal | icbr_refit_commit | 20 | 1.0000 | 1.0000 | 0.135738 | 8.9943 | 1.903386e-02 | 1.948194e-02 | 0.000000 | 1.950134e+00 |
| poly_cubic | baseline | 20 | 1.0000 | 1.0000 | 5.743161 | 1.0000 | 0.000000e+00 | 0.000000e+00 | nan | nan |
| poly_cubic | icbr_full | 20 | 1.0000 | 1.0000 | 0.388451 | 14.5642 | -1.039194e-04 | -1.159023e-04 | 0.553333 | nan |
| poly_cubic | icbr_no_replay | 20 | 1.0000 | 1.0000 | 0.333060 | 16.9584 | 4.250734e-05 | 4.026131e-05 | nan | nan |
| poly_cubic | icbr_no_shared | 20 | 1.0000 | 1.0000 | 0.535711 | 10.8344 | -1.035082e-04 | -1.153811e-04 | 0.561667 | nan |
| poly_cubic | icbr_refit_commit | 20 | 1.0000 | 1.0000 | 0.582179 | 9.7410 | 1.219295e-02 | 1.261811e-02 | 0.521667 | 4.739820e+00 |
| combo | baseline | 20 | 1.0000 | 1.0000 | 6.897983 | 1.0000 | 0.000000e+00 | 0.000000e+00 | nan | nan |
| combo | icbr_full | 20 | 1.0000 | 1.0000 | 0.456061 | 15.1362 | -2.774328e-05 | -1.361565e-04 | 0.336667 | nan |
| combo | icbr_no_replay | 20 | 1.0000 | 1.0000 | 0.378083 | 18.2518 | 1.949559e-05 | 8.551049e-05 | nan | nan |
| combo | icbr_no_shared | 20 | 1.0000 | 1.0000 | 0.644345 | 10.7139 | -2.694676e-05 | -1.355031e-04 | 0.345000 | nan |
| combo | icbr_refit_commit | 20 | 1.0000 | 1.0000 | 0.682046 | 10.1245 | 1.399077e-02 | 1.500616e-02 | 0.466667 | 3.544982e+00 |
| trig_interaction | baseline | 20 | 1.0000 | 1.0000 | 16.688776 | 1.0000 | 0.000000e+00 | 0.000000e+00 | nan | nan |
| trig_interaction | icbr_full | 20 | 1.0000 | 1.0000 | 1.132597 | 14.7317 | -4.595893e-04 | -7.299085e-04 | 0.528368 | nan |
| trig_interaction | icbr_no_replay | 20 | 1.0000 | 1.0000 | 0.744015 | 22.4371 | 9.781019e-05 | -8.900927e-05 | nan | nan |
| trig_interaction | icbr_no_shared | 20 | 1.0000 | 1.0000 | 1.759505 | 9.4838 | -4.594159e-04 | -7.295497e-04 | 0.528368 | nan |
| trig_interaction | icbr_refit_commit | 20 | 1.0000 | 1.0000 | 1.696152 | 9.8378 | 8.051497e-02 | 8.201710e-02 | 0.671037 | 4.752520e+00 |

## Critique Evidence Summary (Q1/Q2/Q3)

| task | n | q1_candidate_ratio_mean | q1_symbolic_ratio_mean | q2_imitation_mse_gain_mean | q2_target_mse_gain_mean | q2_rank_inversion_mean | q3_imitation_mse_gain_mean | q3_target_mse_gain_mean | q3_refit_drift_mean |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| __overall__ | 80 | 1.431582 | 1.320987 | 1.877663e-04 | 2.546825e-04 | 0.354592 | 3.096456e-02 | 3.190565e-02 | 3.746864e+00 |
| minimal | 20 | 0.965093 | 0.966400 | 0.000000e+00 | 0.000000e+00 | 0.000000 | 1.901995e-02 | 1.947492e-02 | 1.950134e+00 |
| poly_cubic | 20 | 1.417020 | 1.350093 | 1.464267e-04 | 1.561636e-04 | 0.553333 | 1.229687e-02 | 1.273401e-02 | 4.739820e+00 |
| combo | 20 | 1.500390 | 1.413965 | 4.723887e-05 | 2.216670e-04 | 0.336667 | 1.401852e-02 | 1.514232e-02 | 3.544982e+00 |
| trig_interaction | 20 | 1.843824 | 1.553490 | 5.573995e-04 | 6.408993e-04 | 0.528368 | 8.102597e-02 | 8.281691e-02 | 4.752520e+00 |

## Per-Run Performance Details

| task | seed | cache_hit | cache_status | teacher_mse | teacher_r2 | teacher_gate | candidate_s | replay_s | baseline_symbolic_s | icbr_symbolic_s | speedup_x | baseline_imitation_mse | icbr_imitation_mse | imitation_mse_shift | baseline_target_mse | icbr_target_mse | target_mse_shift | formula_export_success |
|---|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| minimal | 1 | False | miss_write | 8.743851e-04 | 0.998206 | True | 0.105260 | 0.002863 | 1.198966 | 0.110320 | 10.8681 | 8.651124e-04 | 8.931800e-04 | 2.806762e-05 | 2.033810e-05 | 2.650214e-05 | 6.164035e-06 | True |
| minimal | 2 | False | miss_write | 4.454271e-04 | 0.999066 | True | 0.099086 | 0.002618 | 1.224861 | 0.103817 | 11.7983 | 4.459639e-04 | 4.509982e-04 | 5.034293e-06 | 5.400889e-06 | 1.739394e-05 | 1.199305e-05 | True |
| minimal | 3 | False | miss_write | 8.999310e-05 | 0.999821 | True | 0.098441 | 0.002607 | 1.200131 | 0.103233 | 11.6254 | 8.897683e-05 | 9.978139e-05 | 1.080456e-05 | 8.734393e-07 | 1.274425e-05 | 1.187081e-05 | True |
| minimal | 4 | False | miss_write | 3.156056e-04 | 0.999357 | True | 0.103684 | 0.002637 | 1.231714 | 0.108309 | 11.3723 | 3.126764e-04 | 3.353381e-04 | 2.266167e-05 | 1.967273e-06 | 1.423975e-05 | 1.227248e-05 | True |
| minimal | 5 | False | miss_write | 7.842554e-04 | 0.998382 | True | 0.096162 | 0.002740 | 1.236593 | 0.100934 | 12.2515 | 7.884009e-04 | 7.820104e-04 | -6.390561e-06 | 2.620356e-05 | 1.689293e-05 | -9.310630e-06 | True |
| minimal | 6 | False | miss_write | 2.575211e-04 | 0.999498 | True | 0.103608 | 0.002629 | 1.223184 | 0.108212 | 11.3035 | 2.540812e-04 | 2.694232e-04 | 1.534194e-05 | 6.173823e-06 | 1.685989e-05 | 1.068606e-05 | True |
| minimal | 7 | False | miss_write | 1.084304e-03 | 0.997919 | True | 0.098746 | 0.002619 | 1.218713 | 0.103363 | 11.7906 | 1.080227e-03 | 1.062239e-03 | -1.798780e-05 | 2.205574e-05 | 2.558113e-05 | 3.525389e-06 | True |
| minimal | 8 | False | miss_write | 2.498816e-04 | 0.999496 | True | 0.110676 | 0.002640 | 1.234536 | 0.115370 | 10.7007 | 2.476941e-04 | 2.699748e-04 | 2.228079e-05 | 2.654781e-06 | 1.454544e-05 | 1.189066e-05 | True |
| minimal | 9 | False | miss_write | 8.732524e-04 | 0.998289 | True | 0.113442 | 0.002611 | 1.255786 | 0.118241 | 10.6206 | 8.165146e-04 | 8.594946e-04 | 4.298001e-05 | 5.528919e-05 | 5.556205e-05 | 2.728557e-07 | True |
| minimal | 10 | False | miss_write | 2.689827e-04 | 0.999441 | True | 0.095366 | 0.002767 | 1.222482 | 0.100199 | 12.2006 | 2.720421e-04 | 2.776679e-04 | 5.625741e-06 | 5.031826e-06 | 1.661923e-05 | 1.158740e-05 | True |
| minimal | 11 | False | miss_write | 2.540758e-04 | 0.999481 | True | 0.099812 | 0.002720 | 1.216809 | 0.104645 | 11.6279 | 2.510936e-04 | 2.719873e-04 | 2.089370e-05 | 3.685107e-06 | 1.636118e-05 | 1.267607e-05 | True |
| minimal | 12 | False | miss_write | 2.983879e-04 | 0.999431 | True | 0.101055 | 0.002621 | 1.239222 | 0.105723 | 11.7213 | 2.921855e-04 | 3.148438e-04 | 2.265832e-05 | 6.395329e-06 | 1.388013e-05 | 7.484797e-06 | True |
| minimal | 13 | False | miss_write | 1.131251e-03 | 0.997874 | True | 0.096485 | 0.002814 | 1.220810 | 0.101358 | 12.0446 | 1.112435e-03 | 1.140263e-03 | 2.782769e-05 | 5.101213e-05 | 3.254159e-05 | -1.847054e-05 | True |
| minimal | 14 | False | miss_write | 1.098518e-03 | 0.997705 | True | 0.094784 | 0.002686 | 1.218649 | 0.099608 | 12.2345 | 1.126850e-03 | 1.132243e-03 | 5.392823e-06 | 1.039167e-05 | 1.740533e-05 | 7.013662e-06 | True |
| minimal | 15 | False | miss_write | 1.993349e-04 | 0.999569 | True | 0.096849 | 0.002775 | 1.228192 | 0.101798 | 12.0650 | 2.002611e-04 | 2.127218e-04 | 1.246063e-05 | 8.791900e-06 | 2.020927e-05 | 1.141737e-05 | True |
| minimal | 16 | False | miss_write | 1.390117e-04 | 0.999729 | True | 0.101292 | 0.002792 | 1.207107 | 0.106293 | 11.3564 | 1.361733e-04 | 1.508087e-04 | 1.463541e-05 | 2.556577e-06 | 1.592912e-05 | 1.337254e-05 | True |
| minimal | 17 | False | miss_write | 6.548367e-04 | 0.998752 | True | 0.099389 | 0.002602 | 1.206930 | 0.103951 | 11.6106 | 6.396074e-04 | 6.599530e-04 | 2.034561e-05 | 7.359743e-06 | 1.639747e-05 | 9.037731e-06 | True |
| minimal | 18 | False | miss_write | 3.753367e-04 | 0.999236 | True | 0.099058 | 0.002606 | 1.203784 | 0.103653 | 11.6136 | 3.752202e-04 | 3.876555e-04 | 1.243534e-05 | 3.641841e-06 | 1.546769e-05 | 1.182585e-05 | True |
| minimal | 19 | False | miss_write | 5.628284e-04 | 0.998878 | True | 0.097741 | 0.002751 | 1.206658 | 0.102544 | 11.7673 | 5.489082e-04 | 5.599498e-04 | 1.104164e-05 | 1.779611e-05 | 2.919518e-05 | 1.139908e-05 | True |
| minimal | 20 | False | miss_write | 2.006718e-04 | 0.999602 | True | 0.094803 | 0.002626 | 1.190789 | 0.099399 | 11.9799 | 2.055852e-04 | 2.077053e-04 | 2.120098e-06 | 1.010590e-05 | 1.389460e-05 | 3.788696e-06 | True |
| poly_cubic | 1 | False | miss_write | 1.954135e-04 | 0.996108 | True | 0.370006 | 0.055272 | 7.217138 | 0.447250 | 16.1367 | 3.012797e-03 | 3.108975e-03 | 9.617792e-05 | 3.553136e-03 | 3.613444e-03 | 6.030733e-05 | True |
| poly_cubic | 2 | False | miss_write | 9.988295e-03 | 0.802038 | True | 0.248529 | 0.020264 | 3.601010 | 0.278538 | 12.9282 | 3.550545e-03 | 3.555752e-03 | 5.207025e-06 | 1.346319e-02 | 1.347599e-02 | 1.279265e-05 | True |
| poly_cubic | 3 | False | miss_write | 2.058470e-03 | 0.957582 | True | 0.355390 | 0.055546 | 7.202921 | 0.433208 | 16.6269 | 2.740473e-03 | 2.915679e-03 | 1.752058e-04 | 5.030414e-03 | 5.242732e-03 | 2.123178e-04 | True |
| poly_cubic | 4 | False | miss_write | 1.918766e-03 | 0.958798 | True | 0.369150 | 0.046667 | 5.967133 | 0.434941 | 13.7194 | 3.691457e-03 | 3.688520e-03 | -2.937159e-06 | 6.437576e-03 | 6.446765e-03 | 9.188894e-06 | True |
| poly_cubic | 5 | False | miss_write | 1.582267e-03 | 0.968798 | True | 0.364985 | 0.054693 | 6.994663 | 0.441602 | 15.8393 | 4.018206e-03 | 3.996735e-03 | -2.147118e-05 | 5.792339e-03 | 5.770161e-03 | -2.217805e-05 | True |
| poly_cubic | 6 | False | miss_write | 3.574073e-03 | 0.930599 | True | 0.321266 | 0.047655 | 5.832213 | 0.388397 | 15.0161 | 3.257953e-03 | 3.248244e-03 | -9.709736e-06 | 7.168230e-03 | 7.153893e-03 | -1.433678e-05 | True |
| poly_cubic | 7 | False | miss_write | 1.627519e-03 | 0.967116 | True | 0.340385 | 0.046672 | 5.972541 | 0.406216 | 14.7029 | 2.820241e-03 | 2.833377e-03 | 1.313654e-05 | 4.572959e-03 | 4.584263e-03 | 1.130439e-05 | True |
| poly_cubic | 8 | False | miss_write | 1.444682e-03 | 0.969527 | True | 0.375653 | 0.056621 | 7.009473 | 0.455183 | 15.3992 | 3.600230e-03 | 3.737836e-03 | 1.376059e-04 | 5.160966e-03 | 5.276306e-03 | 1.153392e-04 | True |
| poly_cubic | 9 | False | miss_write | 2.067646e-03 | 0.953545 | True | 0.386187 | 0.055419 | 6.981454 | 0.464161 | 15.0410 | 3.285242e-03 | 2.076293e-03 | -1.208949e-03 | 5.381184e-03 | 4.153348e-03 | -1.227837e-03 | True |
| poly_cubic | 10 | False | miss_write | 1.177968e-03 | 0.976271 | True | 0.338226 | 0.049765 | 5.855235 | 0.406867 | 14.3910 | 3.889414e-03 | 3.881449e-03 | -7.965835e-06 | 5.142717e-03 | 5.126194e-03 | -1.652259e-05 | True |
| poly_cubic | 11 | False | miss_write | 8.367911e-04 | 0.983070 | True | 0.374688 | 0.054314 | 7.018119 | 0.450995 | 15.5614 | 3.302921e-03 | 3.730261e-03 | 4.273395e-04 | 4.505047e-03 | 4.866564e-03 | 3.615175e-04 | True |
| poly_cubic | 12 | False | miss_write | 6.100412e-03 | 0.880727 | True | 0.231297 | 0.021052 | 3.535641 | 0.262092 | 13.4901 | 3.071663e-03 | 3.064179e-03 | -7.483410e-06 | 9.946868e-03 | 9.916162e-03 | -3.070571e-05 | True |
| poly_cubic | 13 | False | miss_write | 7.577989e-03 | 0.842454 | True | 0.244452 | 0.020171 | 3.525821 | 0.274227 | 12.8573 | 3.651513e-03 | 3.647726e-03 | -3.786990e-06 | 1.114659e-02 | 1.113335e-02 | -1.324806e-05 | True |
| poly_cubic | 14 | False | miss_write | 2.188497e-03 | 0.953776 | True | 0.341531 | 0.048321 | 5.821839 | 0.409497 | 14.2170 | 3.680541e-03 | 3.687987e-03 | 7.445691e-06 | 6.471628e-03 | 6.480814e-03 | 9.186100e-06 | True |
| poly_cubic | 15 | False | miss_write | 3.704652e-03 | 0.925246 | True | 0.245604 | 0.019450 | 3.505418 | 0.274577 | 12.7666 | 4.075334e-03 | 4.077540e-03 | 2.205372e-06 | 7.283895e-03 | 7.291895e-03 | 8.000061e-06 | True |
| poly_cubic | 16 | False | miss_write | 3.211160e-04 | 0.992603 | True | 0.357598 | 0.055774 | 7.049525 | 0.435815 | 16.1755 | 3.350282e-03 | 2.859496e-03 | -4.907863e-04 | 4.044123e-03 | 3.535331e-03 | -5.087920e-04 | True |
| poly_cubic | 17 | False | miss_write | 1.642527e-03 | 0.963773 | True | 0.481462 | 0.061184 | 9.055270 | 0.566173 | 15.9938 | 3.441227e-03 | 2.255762e-03 | -1.185465e-03 | 5.401885e-03 | 4.127136e-03 | -1.274749e-03 | True |
| poly_cubic | 18 | False | miss_write | 4.583246e-03 | 0.906188 | True | 0.300493 | 0.036269 | 5.479171 | 0.352978 | 15.5227 | 3.505956e-03 | 3.519538e-03 | 1.358124e-05 | 8.282366e-03 | 8.281240e-03 | -1.125969e-06 | True |
| poly_cubic | 19 | False | miss_write | 3.605059e-03 | 0.929806 | True | 0.285652 | 0.023471 | 3.608716 | 0.319447 | 11.2968 | 3.664979e-03 | 3.664258e-03 | -7.201452e-07 | 6.908047e-03 | 6.917068e-03 | 9.021256e-06 | True |
| poly_cubic | 20 | False | miss_write | 1.217910e-03 | 0.977311 | True | 0.237035 | 0.020149 | 3.629915 | 0.266861 | 13.6023 | 3.644018e-03 | 3.627000e-03 | -1.701782e-05 | 5.072953e-03 | 5.055427e-03 | -1.752609e-05 | True |
| combo | 1 | False | miss_write | 1.120128e-04 | 0.999801 | True | 0.388256 | 0.057259 | 7.260437 | 0.470061 | 15.4457 | 1.575066e-04 | 2.129885e-04 | 5.548191e-05 | 9.581597e-05 | 1.611466e-04 | 6.533064e-05 | True |
| combo | 2 | False | miss_write | 1.314176e-04 | 0.999765 | True | 0.404897 | 0.056362 | 7.156276 | 0.483469 | 14.8019 | 3.276161e-04 | 2.743214e-04 | -5.329461e-05 | 2.476792e-04 | 1.747216e-04 | -7.295769e-05 | True |
| combo | 3 | False | miss_write | 1.039162e-04 | 0.999813 | True | 0.372812 | 0.054882 | 7.242601 | 0.449882 | 16.0989 | 3.951316e-04 | 3.704526e-04 | -2.467909e-05 | 3.943909e-04 | 3.603154e-04 | -3.407549e-05 | True |
| combo | 4 | False | miss_write | 2.614565e-04 | 0.999526 | True | 0.433907 | 0.057884 | 7.072984 | 0.514499 | 13.7473 | 2.859471e-04 | 3.161757e-04 | 3.022858e-05 | 1.512262e-04 | 1.875380e-04 | 3.631183e-05 | True |
| combo | 5 | False | miss_write | 7.334883e-02 | 0.872105 | True | 0.325792 | 0.046482 | 5.857722 | 0.391959 | 14.9447 | 2.588509e-03 | 2.891312e-03 | 3.028028e-04 | 6.948139e-02 | 7.016528e-02 | 6.838962e-04 | True |
| combo | 6 | False | miss_write | 1.931976e-04 | 0.999663 | True | 0.408124 | 0.056677 | 7.031725 | 0.487170 | 14.4338 | 4.006958e-04 | 3.930925e-04 | -7.603376e-06 | 2.410274e-04 | 2.678412e-04 | 2.681380e-05 | True |
| combo | 7 | False | miss_write | 9.501844e-05 | 0.999847 | True | 0.367901 | 0.054716 | 7.036956 | 0.445136 | 15.8085 | 1.823987e-04 | 1.571475e-04 | -2.525124e-05 | 1.233137e-04 | 1.109143e-04 | -1.239941e-05 | True |
| combo | 8 | False | miss_write | 2.851223e-04 | 0.999498 | True | 0.385563 | 0.054556 | 6.986491 | 0.461824 | 15.1280 | 6.286203e-04 | 5.843451e-04 | -4.427519e-05 | 5.532047e-04 | 4.054306e-04 | -1.477741e-04 | True |
| combo | 9 | False | miss_write | 2.056647e-04 | 0.999643 | True | 0.399310 | 0.055246 | 7.011967 | 0.476523 | 14.7149 | 4.922721e-04 | 5.064688e-04 | 1.419662e-05 | 3.628996e-04 | 3.774865e-04 | 1.458690e-05 | True |
| combo | 10 | False | miss_write | 5.109108e-04 | 0.999153 | True | 0.341654 | 0.045057 | 5.915945 | 0.405885 | 14.5754 | 8.057309e-04 | 5.858886e-04 | -2.198422e-04 | 4.331748e-04 | 2.708456e-04 | -1.623292e-04 | True |
| combo | 11 | False | miss_write | 9.046971e-02 | 0.846260 | True | 0.345730 | 0.047761 | 5.973919 | 0.412919 | 14.4676 | 9.243375e-04 | 8.245591e-04 | -9.977841e-05 | 9.382130e-02 | 9.129374e-02 | -2.527565e-03 | True |
| combo | 12 | False | miss_write | 1.145521e-04 | 0.999809 | True | 0.381678 | 0.055696 | 6.981194 | 0.459927 | 15.1789 | 9.230289e-05 | 1.275011e-04 | 3.519817e-05 | 2.829833e-05 | 7.120007e-05 | 4.290174e-05 | True |
| combo | 13 | False | miss_write | 1.883648e-04 | 0.999693 | True | 0.382406 | 0.055215 | 7.056927 | 0.460066 | 15.3389 | 4.421494e-04 | 4.035065e-04 | -3.864293e-05 | 3.109726e-04 | 2.636155e-04 | -4.735703e-05 | True |
| combo | 14 | False | miss_write | 2.919541e-04 | 0.999473 | True | 0.376276 | 0.057188 | 7.131790 | 0.456392 | 15.6265 | 4.338077e-03 | 4.379413e-03 | 4.133629e-05 | 4.314376e-03 | 4.333870e-03 | 1.949398e-05 | True |
| combo | 15 | False | miss_write | 6.479074e-04 | 0.998847 | True | 0.386150 | 0.056315 | 7.031092 | 0.464976 | 15.1214 | 9.143051e-04 | 8.021651e-04 | -1.121400e-04 | 5.599701e-04 | 4.290225e-04 | -1.309476e-04 | True |
| combo | 16 | False | miss_write | 2.204299e-04 | 0.999646 | True | 0.372579 | 0.055643 | 7.074986 | 0.449960 | 15.7236 | 8.970798e-04 | 7.872159e-04 | -1.098639e-04 | 7.336377e-04 | 6.176241e-04 | -1.160136e-04 | True |
| combo | 17 | False | miss_write | 1.832366e-04 | 0.999693 | True | 0.370131 | 0.055731 | 7.018786 | 0.448230 | 15.6589 | 6.151200e-04 | 5.431079e-04 | -7.201207e-05 | 5.963268e-04 | 5.076180e-04 | -8.870888e-05 | True |
| combo | 18 | False | miss_write | 1.917077e-04 | 0.999670 | True | 0.369395 | 0.056009 | 7.141539 | 0.447984 | 15.9415 | 7.364269e-04 | 5.994271e-04 | -1.369998e-04 | 6.222578e-04 | 4.594193e-04 | -1.628386e-04 | True |
| combo | 19 | False | miss_write | 8.476962e-05 | 0.999856 | True | 0.405674 | 0.057472 | 6.982343 | 0.486251 | 14.3596 | 3.147855e-04 | 2.211468e-04 | -9.363872e-05 | 2.982836e-04 | 1.907786e-04 | -1.075050e-04 | True |
| combo | 20 | False | miss_write | 1.708706e-04 | 0.999717 | True | 0.369596 | 0.055952 | 6.993968 | 0.448106 | 15.6078 | 3.973580e-04 | 4.012697e-04 | 3.911700e-06 | 3.970659e-04 | 3.950715e-04 | -1.994456e-06 | True |
| trig_interaction | 1 | False | miss_write | 2.199448e-03 | 0.997009 | True | 0.801271 | 0.335287 | 18.534567 | 1.208718 | 15.3341 | 3.036956e-03 | 2.072520e-03 | -9.644357e-04 | 5.261504e-03 | 4.232149e-03 | -1.029355e-03 | True |
| trig_interaction | 2 | False | miss_write | 1.979663e-02 | 0.972177 | True | 0.735142 | 0.308935 | 16.368483 | 1.112492 | 14.7134 | 1.853709e-03 | 1.409377e-03 | -4.443323e-04 | 2.300273e-02 | 2.114112e-02 | -1.861604e-03 | True |
| trig_interaction | 3 | False | miss_write | 8.604269e-03 | 0.988900 | True | 0.741325 | 0.289633 | 15.287524 | 1.094302 | 13.9701 | 1.218114e-03 | 1.296523e-03 | 7.840991e-05 | 1.074634e-02 | 1.009823e-02 | -6.481083e-04 | True |
| trig_interaction | 4 | False | miss_write | 2.289809e-02 | 0.969829 | True | 0.685911 | 0.292739 | 15.128243 | 1.041940 | 14.5193 | 3.237507e-03 | 3.236993e-03 | -5.140901e-07 | 2.585588e-02 | 2.564781e-02 | -2.080724e-04 | True |
| trig_interaction | 5 | False | miss_write | 7.897707e-03 | 0.989082 | True | 0.735167 | 0.314009 | 16.475425 | 1.116034 | 14.7625 | 3.291332e-03 | 3.051930e-03 | -2.394016e-04 | 1.241291e-02 | 1.012703e-02 | -2.285881e-03 | True |
| trig_interaction | 6 | False | miss_write | 1.063532e-03 | 0.998652 | True | 0.805427 | 0.358438 | 18.642878 | 1.241668 | 15.0144 | 5.184736e-03 | 3.495793e-03 | -1.688943e-03 | 6.641119e-03 | 4.746199e-03 | -1.894920e-03 | True |
| trig_interaction | 7 | False | miss_write | 8.580280e-04 | 0.998824 | True | 0.787058 | 0.333914 | 17.467440 | 1.194778 | 14.6198 | 3.714190e-03 | 2.489957e-03 | -1.224233e-03 | 4.476866e-03 | 3.278197e-03 | -1.198669e-03 | True |
| trig_interaction | 8 | False | miss_write | 1.366993e-02 | 0.981801 | True | 0.729407 | 0.319853 | 16.378050 | 1.120203 | 14.6206 | 3.874717e-03 | 3.826925e-03 | -4.779175e-05 | 1.542735e-02 | 1.517176e-02 | -2.555940e-04 | True |
| trig_interaction | 9 | False | miss_write | 3.709822e-03 | 0.994756 | True | 0.691674 | 0.296032 | 15.562042 | 1.052611 | 14.7842 | 5.692142e-03 | 5.231661e-03 | -4.604808e-04 | 9.361290e-03 | 8.426717e-03 | -9.345729e-04 | True |
| trig_interaction | 10 | False | miss_write | 4.390491e-02 | 0.935235 | True | 0.739174 | 0.311085 | 16.707435 | 1.119709 | 14.9212 | 3.636261e-03 | 3.221682e-03 | -4.145794e-04 | 4.974522e-02 | 4.882984e-02 | -9.153783e-04 | True |
| trig_interaction | 11 | False | miss_write | 1.817124e-03 | 0.997571 | True | 0.753817 | 0.312229 | 16.427088 | 1.136625 | 14.4525 | 4.614309e-03 | 4.175215e-03 | -4.390939e-04 | 5.387733e-03 | 4.738392e-03 | -6.493409e-04 | True |
| trig_interaction | 12 | False | miss_write | 8.239121e-03 | 0.989670 | True | 0.772646 | 0.313055 | 16.493111 | 1.151919 | 14.3179 | 4.059907e-03 | 4.126425e-03 | 6.651832e-05 | 1.412252e-02 | 1.368957e-02 | -4.329551e-04 | True |
| trig_interaction | 13 | False | miss_write | 1.870870e-03 | 0.997525 | True | 0.823578 | 0.353481 | 18.737831 | 1.254437 | 14.9372 | 3.638195e-03 | 3.453286e-03 | -1.849090e-04 | 5.011617e-03 | 4.799435e-03 | -2.121818e-04 | True |
| trig_interaction | 14 | False | miss_write | 8.184940e-03 | 0.988844 | True | 0.779618 | 0.333668 | 17.542913 | 1.186237 | 14.7887 | 3.658795e-03 | 3.696546e-03 | 3.775163e-05 | 1.044684e-02 | 1.065250e-02 | 2.056602e-04 | True |
| trig_interaction | 15 | False | miss_write | 3.093117e-03 | 0.995512 | True | 0.763810 | 0.314208 | 16.275541 | 1.145188 | 14.2121 | 3.937670e-03 | 4.019482e-03 | 8.181157e-05 | 6.200766e-03 | 8.087819e-03 | 1.887053e-03 | True |
| trig_interaction | 16 | False | miss_write | 7.732280e-03 | 0.989535 | True | 0.759638 | 0.311559 | 16.444544 | 1.138267 | 14.4470 | 2.544113e-03 | 1.663279e-03 | -8.808346e-04 | 9.057995e-03 | 8.032554e-03 | -1.025441e-03 | True |
| trig_interaction | 17 | False | miss_write | 1.024746e-02 | 0.986696 | True | 0.683305 | 0.289319 | 15.210839 | 1.036044 | 14.6816 | 4.988997e-03 | 5.496401e-03 | 5.074036e-04 | 1.451974e-02 | 1.515793e-02 | 6.381879e-04 | True |
| trig_interaction | 18 | False | miss_write | 1.727680e-03 | 0.997576 | True | 0.703710 | 0.314767 | 16.843672 | 1.086249 | 15.5063 | 3.963911e-03 | 2.352803e-03 | -1.611109e-03 | 5.841968e-03 | 4.056174e-03 | -1.785793e-03 | True |
| trig_interaction | 19 | False | miss_write | 3.354001e-03 | 0.995467 | True | 0.841323 | 0.361206 | 19.202439 | 1.280123 | 15.0005 | 3.198225e-03 | 1.317998e-03 | -1.880227e-03 | 7.500532e-03 | 4.911054e-03 | -2.589477e-03 | True |
| trig_interaction | 20 | False | miss_write | 1.767333e-03 | 0.997637 | True | 0.643474 | 0.239089 | 14.045448 | 0.934407 | 15.0314 | 2.759116e-03 | 3.276320e-03 | 5.172037e-04 | 2.579492e-03 | 3.177765e-03 | 5.982725e-04 | True |

## Formula Comparison

### task=minimal seed=1

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=8.743851e-04, r2=0.998206
- Variant formula overview:
  - baseline: symbolic_s=1.198966e+00, imitation_mse=8.651124e-04, target_mse=2.033810e-05, formula_export_success=True
  - icbr_full: symbolic_s=1.103202e-01, imitation_mse=8.931800e-04, target_mse=2.650214e-05, formula_export_success=True
  - icbr_no_replay: symbolic_s=1.130798e-01, imitation_mse=8.931800e-04, target_mse=2.650214e-05, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.050750e-01, imitation_mse=8.931800e-04, target_mse=2.650214e-05, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.372616e-01, imitation_mse=2.038690e-02, target_mse=1.975754e-02, formula_export_success=True
- baseline formula (display, rounded):
  - `-0.993758*cos(3.13624*x_1 + 1.57232) - 0.000259615`
- icbr_full formula (display, rounded):
  - `0.996028*sin(3.15*x_1 + 2.38419e-7) - 0.000142003`
- icbr_no_replay formula (display, rounded):
  - `0.996028*sin(3.15*x_1 + 2.38419e-7) - 0.000142003`
- icbr_no_shared formula (display, rounded):
  - `0.996028*sin(3.15*x_1 + 2.38419e-7) - 0.000142003`
- icbr_refit_commit formula (display, rounded):
  - `0.00973569 - 0.888735*sin(2.85188*x_1 + 3.0198)`

### task=minimal seed=2

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=4.454271e-04, r2=0.999066
- Variant formula overview:
  - baseline: symbolic_s=1.224861e+00, imitation_mse=4.459639e-04, target_mse=5.400889e-06, formula_export_success=True
  - icbr_full: symbolic_s=1.038166e-01, imitation_mse=4.509982e-04, target_mse=1.739394e-05, formula_export_success=True
  - icbr_no_replay: symbolic_s=9.752930e-02, imitation_mse=4.509982e-04, target_mse=1.739394e-05, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.017147e-01, imitation_mse=4.509982e-04, target_mse=1.739394e-05, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.429471e-01, imitation_mse=1.719164e-02, target_mse=1.709766e-02, formula_export_success=True
- baseline formula (display, rounded):
  - `0.997261*cos(3.1392*x_1 - 1.57) + 0.00117608`
- icbr_full formula (display, rounded):
  - `0.999143*sin(3.15*x_1 + 2.38419e-7) + 0.00132781`
- icbr_no_replay formula (display, rounded):
  - `0.999143*sin(3.15*x_1 + 2.38419e-7) + 0.00132781`
- icbr_no_shared formula (display, rounded):
  - `0.999143*sin(3.15*x_1 + 2.38419e-7) + 0.00132781`
- icbr_refit_commit formula (display, rounded):
  - `0.883129*sin(2.84992*x_1 - 0.0984799) + 0.00318842`

### task=minimal seed=3

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=8.999310e-05, r2=0.999821
- Variant formula overview:
  - baseline: symbolic_s=1.200131e+00, imitation_mse=8.897683e-05, target_mse=8.734393e-07, formula_export_success=True
  - icbr_full: symbolic_s=1.032335e-01, imitation_mse=9.978139e-05, target_mse=1.274425e-05, formula_export_success=True
  - icbr_no_replay: symbolic_s=1.020686e-01, imitation_mse=9.978139e-05, target_mse=1.274425e-05, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.010425e-01, imitation_mse=9.978139e-05, target_mse=1.274425e-05, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.395115e-01, imitation_mse=1.859385e-02, target_mse=1.865615e-02, formula_export_success=True
- baseline formula (display, rounded):
  - `0.99892*sin(3.1412*x_1 - 0.000800001) - 5.11669e-5`
- icbr_full formula (display, rounded):
  - `1.00012*sin(3.15*x_1 + 2.38419e-7) - 9.6608e-5`
- icbr_no_replay formula (display, rounded):
  - `1.00012*sin(3.15*x_1 + 2.38419e-7) - 9.6608e-5`
- icbr_no_shared formula (display, rounded):
  - `1.00012*sin(3.15*x_1 + 2.38419e-7) - 9.6608e-5`
- icbr_refit_commit formula (display, rounded):
  - `0.020175 - 0.902809*sin(2.8606*x_1 + 3.014)`

### task=minimal seed=4

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=3.156056e-04, r2=0.999357
- Variant formula overview:
  - baseline: symbolic_s=1.231714e+00, imitation_mse=3.126764e-04, target_mse=1.967273e-06, formula_export_success=True
  - icbr_full: symbolic_s=1.083087e-01, imitation_mse=3.353381e-04, target_mse=1.423975e-05, formula_export_success=True
  - icbr_no_replay: symbolic_s=1.097159e-01, imitation_mse=3.353381e-04, target_mse=1.423975e-05, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.048859e-01, imitation_mse=3.353381e-04, target_mse=1.423975e-05, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.439826e-01, imitation_mse=1.657048e-02, target_mse=1.653554e-02, formula_export_success=True
- baseline formula (display, rounded):
  - `0.000485245 - 0.998297*cos(3.14232*x_1 + 1.57024)`
- icbr_full formula (display, rounded):
  - `0.99943*sin(3.15*x_1 + 2.38419e-7) + 0.000417477`
- icbr_no_replay formula (display, rounded):
  - `0.99943*sin(3.15*x_1 + 2.38419e-7) + 0.000417477`
- icbr_no_shared formula (display, rounded):
  - `0.99943*sin(3.15*x_1 + 2.38419e-7) + 0.000417477`
- icbr_refit_commit formula (display, rounded):
  - `0.909871*sin(2.863*x_1 + 0.11856) - 0.0122013`

### task=minimal seed=5

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=7.842554e-04, r2=0.998382
- Variant formula overview:
  - baseline: symbolic_s=1.236593e+00, imitation_mse=7.884009e-04, target_mse=2.620356e-05, formula_export_success=True
  - icbr_full: symbolic_s=1.009341e-01, imitation_mse=7.820104e-04, target_mse=1.689293e-05, formula_export_success=True
  - icbr_no_replay: symbolic_s=9.335680e-02, imitation_mse=7.820104e-04, target_mse=1.689293e-05, formula_export_success=True
  - icbr_no_shared: symbolic_s=9.678980e-02, imitation_mse=7.820104e-04, target_mse=1.689293e-05, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.363480e-01, imitation_mse=1.582992e-02, target_mse=1.530204e-02, formula_export_success=True
- baseline formula (display, rounded):
  - `0.999795*cos(3.15192*x_1 - 1.57304) - 0.00135056`
- icbr_full formula (display, rounded):
  - `0.999451*sin(3.15*x_1 + 2.38419e-7) - 0.00152688`
- icbr_no_replay formula (display, rounded):
  - `0.999451*sin(3.15*x_1 + 2.38419e-7) - 0.00152688`
- icbr_no_shared formula (display, rounded):
  - `0.999451*sin(3.15*x_1 + 2.38419e-7) - 0.00152688`
- icbr_refit_commit formula (display, rounded):
  - `0.923776*sin(2.87668*x_1 - 0.10744) + 0.0167808`

### task=minimal seed=6

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=2.575211e-04, r2=0.999498
- Variant formula overview:
  - baseline: symbolic_s=1.223184e+00, imitation_mse=2.540812e-04, target_mse=6.173823e-06, formula_export_success=True
  - icbr_full: symbolic_s=1.082124e-01, imitation_mse=2.694232e-04, target_mse=1.685989e-05, formula_export_success=True
  - icbr_no_replay: symbolic_s=9.956120e-02, imitation_mse=2.694232e-04, target_mse=1.685989e-05, formula_export_success=True
  - icbr_no_shared: symbolic_s=9.820150e-02, imitation_mse=2.694232e-04, target_mse=1.685989e-05, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.353457e-01, imitation_mse=2.230188e-02, target_mse=2.260991e-02, formula_export_success=True
- baseline formula (display, rounded):
  - `0.996952*sin(3.13752*x_1 + 0.000560001) - 0.000318352`
- icbr_full formula (display, rounded):
  - `0.998849*sin(3.15*x_1 + 2.38419e-7) - 0.000179172`
- icbr_no_replay formula (display, rounded):
  - `0.998849*sin(3.15*x_1 + 2.38419e-7) - 0.000179172`
- icbr_no_shared formula (display, rounded):
  - `0.998849*sin(3.15*x_1 + 2.38419e-7) - 0.000179172`
- icbr_refit_commit formula (display, rounded):
  - `-0.893975*sin(2.80552*x_1 - 3.0076) - 0.0134534`

### task=minimal seed=7

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.084304e-03, r2=0.997918
- Variant formula overview:
  - baseline: symbolic_s=1.218713e+00, imitation_mse=1.080227e-03, target_mse=2.205574e-05, formula_export_success=True
  - icbr_full: symbolic_s=1.033628e-01, imitation_mse=1.062239e-03, target_mse=2.558113e-05, formula_export_success=True
  - icbr_no_replay: symbolic_s=1.024296e-01, imitation_mse=1.062239e-03, target_mse=2.558113e-05, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.017731e-01, imitation_mse=1.062239e-03, target_mse=2.558113e-05, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.327901e-01, imitation_mse=1.841462e-02, target_mse=1.801110e-02, formula_export_success=True
- baseline formula (display, rounded):
  - `0.993939*cos(3.13576*x_1 - 1.57216) - 0.00136257`
- icbr_full formula (display, rounded):
  - `0.996418*sin(3.15*x_1 + 2.38419e-7) - 0.00119891`
- icbr_no_replay formula (display, rounded):
  - `0.996418*sin(3.15*x_1 + 2.38419e-7) - 0.00119891`
- icbr_no_shared formula (display, rounded):
  - `0.996418*sin(3.15*x_1 + 2.38419e-7) - 0.00119891`
- icbr_refit_commit formula (display, rounded):
  - `-0.892462*sin(2.84116*x_1 - 3.02152) - 0.00972488`

### task=minimal seed=8

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=2.498816e-04, r2=0.999496
- Variant formula overview:
  - baseline: symbolic_s=1.234536e+00, imitation_mse=2.476941e-04, target_mse=2.654781e-06, formula_export_success=True
  - icbr_full: symbolic_s=1.153701e-01, imitation_mse=2.699748e-04, target_mse=1.454544e-05, formula_export_success=True
  - icbr_no_replay: symbolic_s=1.071184e-01, imitation_mse=2.699748e-04, target_mse=1.454544e-05, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.067664e-01, imitation_mse=2.699748e-04, target_mse=1.454544e-05, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.483864e-01, imitation_mse=2.316974e-02, target_mse=2.326304e-02, formula_export_success=True
- baseline formula (display, rounded):
  - `0.998843*sin(3.1388*x_1 - 0.00016) + 0.000838894`
- icbr_full formula (display, rounded):
  - `1.00083*sin(3.15*x_1 + 2.38419e-7) + 0.00041559`
- icbr_no_replay formula (display, rounded):
  - `1.00083*sin(3.15*x_1 + 2.38419e-7) + 0.00041559`
- icbr_no_shared formula (display, rounded):
  - `1.00083*sin(3.15*x_1 + 2.38419e-7) + 0.00041559`
- icbr_refit_commit formula (display, rounded):
  - `0.87561*sin(2.83784*x_1 + 0.11636) + 0.0100477`

### task=minimal seed=9

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=8.732524e-04, r2=0.998289
- Variant formula overview:
  - baseline: symbolic_s=1.255786e+00, imitation_mse=8.165146e-04, target_mse=5.528919e-05, formula_export_success=True
  - icbr_full: symbolic_s=1.182407e-01, imitation_mse=8.594946e-04, target_mse=5.556205e-05, formula_export_success=True
  - icbr_no_replay: symbolic_s=1.088125e-01, imitation_mse=8.594946e-04, target_mse=5.556205e-05, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.085447e-01, imitation_mse=8.594946e-04, target_mse=5.556205e-05, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.418209e-01, imitation_mse=2.078271e-02, target_mse=2.142971e-02, formula_export_success=True
- baseline formula (display, rounded):
  - `0.00277771 - 0.990314*cos(3.13336*x_1 + 1.57144)`
- icbr_full formula (display, rounded):
  - `0.99272*sin(3.15*x_1 + 2.38419e-7) + 0.00244584`
- icbr_no_replay formula (display, rounded):
  - `0.99272*sin(3.15*x_1 + 2.38419e-7) + 0.00244584`
- icbr_no_shared formula (display, rounded):
  - `0.99272*sin(3.15*x_1 + 2.38419e-7) + 0.00244584`
- icbr_refit_commit formula (display, rounded):
  - `0.019953 - 0.898864*sin(2.80648*x_1 + 3.02088)`

### task=minimal seed=10

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=2.689827e-04, r2=0.999441
- Variant formula overview:
  - baseline: symbolic_s=1.222482e+00, imitation_mse=2.720421e-04, target_mse=5.031826e-06, formula_export_success=True
  - icbr_full: symbolic_s=1.001987e-01, imitation_mse=2.776679e-04, target_mse=1.661923e-05, formula_export_success=True
  - icbr_no_replay: symbolic_s=9.397330e-02, imitation_mse=2.776679e-04, target_mse=1.661923e-05, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.012139e-01, imitation_mse=2.776679e-04, target_mse=1.661923e-05, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.296808e-01, imitation_mse=1.734126e-02, target_mse=1.716720e-02, formula_export_success=True
- baseline formula (display, rounded):
  - `0.997424*cos(3.1416*x_1 - 1.57256) - 5.80436e-5`
- icbr_full formula (display, rounded):
  - `0.998568*sin(3.15*x_1 + 2.38419e-7) - 1.85654e-5`
- icbr_no_replay formula (display, rounded):
  - `0.998568*sin(3.15*x_1 + 2.38419e-7) - 1.85654e-5`
- icbr_no_shared formula (display, rounded):
  - `0.998568*sin(3.15*x_1 + 2.38419e-7) - 1.85654e-5`
- icbr_refit_commit formula (display, rounded):
  - `0.910428*sin(2.84424*x_1 + 0.10036) - 0.0150808`

### task=minimal seed=11

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=2.540758e-04, r2=0.999481
- Variant formula overview:
  - baseline: symbolic_s=1.216809e+00, imitation_mse=2.510936e-04, target_mse=3.685107e-06, formula_export_success=True
  - icbr_full: symbolic_s=1.046453e-01, imitation_mse=2.719873e-04, target_mse=1.636118e-05, formula_export_success=True
  - icbr_no_replay: symbolic_s=9.932210e-02, imitation_mse=2.719873e-04, target_mse=1.636118e-05, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.009011e-01, imitation_mse=2.719873e-04, target_mse=1.636118e-05, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.333011e-01, imitation_mse=1.770365e-02, target_mse=1.803434e-02, formula_export_success=True
- baseline formula (display, rounded):
  - `0.997388*sin(3.14216*x_1 + 0.00016) + 0.000264724`
- icbr_full formula (display, rounded):
  - `0.998644*sin(3.15*x_1 + 2.38419e-7) + 0.000306909`
- icbr_no_replay formula (display, rounded):
  - `0.998644*sin(3.15*x_1 + 2.38419e-7) + 0.000306909`
- icbr_no_shared formula (display, rounded):
  - `0.998644*sin(3.15*x_1 + 2.38419e-7) + 0.000306909`
- icbr_refit_commit formula (display, rounded):
  - `0.902646*sin(2.86852*x_1 - 0.11048) + 0.0130719`

### task=minimal seed=12

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=2.983879e-04, r2=0.999431
- Variant formula overview:
  - baseline: symbolic_s=1.239222e+00, imitation_mse=2.921855e-04, target_mse=6.395329e-06, formula_export_success=True
  - icbr_full: symbolic_s=1.057235e-01, imitation_mse=3.148438e-04, target_mse=1.388013e-05, formula_export_success=True
  - icbr_no_replay: symbolic_s=1.006635e-01, imitation_mse=3.148438e-04, target_mse=1.388013e-05, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.017660e-01, imitation_mse=3.148438e-04, target_mse=1.388013e-05, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.305013e-01, imitation_mse=1.894519e-02, target_mse=1.912633e-02, formula_export_success=True
- baseline formula (display, rounded):
  - `0.997395*sin(3.13664*x_1 + 0.000800001) - 0.000248477`
- icbr_full formula (display, rounded):
  - `0.999476*sin(3.15*x_1 + 2.38419e-7) - 0.000429177`
- icbr_no_replay formula (display, rounded):
  - `0.999476*sin(3.15*x_1 + 2.38419e-7) - 0.000429177`
- icbr_no_shared formula (display, rounded):
  - `0.999476*sin(3.15*x_1 + 2.38419e-7) - 0.000429177`
- icbr_refit_commit formula (display, rounded):
  - `0.898709*sin(2.8346*x_1 - 0.1076) + 0.0152973`

### task=minimal seed=13

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.131251e-03, r2=0.997874
- Variant formula overview:
  - baseline: symbolic_s=1.220810e+00, imitation_mse=1.112435e-03, target_mse=5.101213e-05, formula_export_success=True
  - icbr_full: symbolic_s=1.013576e-01, imitation_mse=1.140263e-03, target_mse=3.254159e-05, formula_export_success=True
  - icbr_no_replay: symbolic_s=9.564800e-02, imitation_mse=1.140263e-03, target_mse=3.254159e-05, formula_export_success=True
  - icbr_no_shared: symbolic_s=9.557540e-02, imitation_mse=1.140263e-03, target_mse=3.254159e-05, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.333723e-01, imitation_mse=2.120992e-02, target_mse=2.151055e-02, formula_export_success=True
- baseline formula (display, rounded):
  - `0.00124284 - 0.992042*cos(3.13328*x_1 + 1.57616)`
- icbr_full formula (display, rounded):
  - `0.995064*sin(3.15*x_1 + 2.38419e-7) + 0.000991726`
- icbr_no_replay formula (display, rounded):
  - `0.995064*sin(3.15*x_1 + 2.38419e-7) + 0.000991726`
- icbr_no_shared formula (display, rounded):
  - `0.995064*sin(3.15*x_1 + 2.38419e-7) + 0.000991726`
- icbr_refit_commit formula (display, rounded):
  - `-0.888709*sin(2.86076*x_1 - 2.99604) - 0.00317415`

### task=minimal seed=14

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.098518e-03, r2=0.997705
- Variant formula overview:
  - baseline: symbolic_s=1.218649e+00, imitation_mse=1.126850e-03, target_mse=1.039167e-05, formula_export_success=True
  - icbr_full: symbolic_s=9.960760e-02, imitation_mse=1.132243e-03, target_mse=1.740533e-05, formula_export_success=True
  - icbr_no_replay: symbolic_s=9.645330e-02, imitation_mse=1.132243e-03, target_mse=1.740533e-05, formula_export_success=True
  - icbr_no_shared: symbolic_s=9.908160e-02, imitation_mse=1.132243e-03, target_mse=1.740533e-05, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.289763e-01, imitation_mse=2.578853e-02, target_mse=2.444836e-02, formula_export_success=True
- baseline formula (display, rounded):
  - `0.996905*sin(3.13848*x_1 - 0.00248001) - 0.00116213`
- icbr_full formula (display, rounded):
  - `0.998856*sin(3.15*x_1 + 2.38419e-7) - 0.000845939`
- icbr_no_replay formula (display, rounded):
  - `0.998856*sin(3.15*x_1 + 2.38419e-7) - 0.000845939`
- icbr_no_shared formula (display, rounded):
  - `0.998856*sin(3.15*x_1 + 2.38419e-7) - 0.000845939`
- icbr_refit_commit formula (display, rounded):
  - `0.00153646 - 0.888417*sin(2.83808*x_1 + 3.00364)`

### task=minimal seed=15

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.993349e-04, r2=0.999569
- Variant formula overview:
  - baseline: symbolic_s=1.228192e+00, imitation_mse=2.002611e-04, target_mse=8.791900e-06, formula_export_success=True
  - icbr_full: symbolic_s=1.017977e-01, imitation_mse=2.127218e-04, target_mse=2.020927e-05, formula_export_success=True
  - icbr_no_replay: symbolic_s=9.897900e-02, imitation_mse=2.127218e-04, target_mse=2.020927e-05, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.040512e-01, imitation_mse=2.127218e-04, target_mse=2.020927e-05, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.298653e-01, imitation_mse=1.405391e-02, target_mse=1.418643e-02, formula_export_success=True
- baseline formula (display, rounded):
  - `0.997565*sin(3.14544*x_1 + 0.000640001) + 0.00107871`
- icbr_full formula (display, rounded):
  - `0.998296*sin(3.15*x_1 + 2.38419e-7) + 0.00102238`
- icbr_no_replay formula (display, rounded):
  - `0.998296*sin(3.15*x_1 + 2.38419e-7) + 0.00102238`
- icbr_no_shared formula (display, rounded):
  - `0.998296*sin(3.15*x_1 + 2.38419e-7) + 0.00102238`
- icbr_refit_commit formula (display, rounded):
  - `0.918361*sin(2.92004*x_1 + 0.11212) - 0.00317479`

### task=minimal seed=16

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.390117e-04, r2=0.999729
- Variant formula overview:
  - baseline: symbolic_s=1.207107e+00, imitation_mse=1.361733e-04, target_mse=2.556577e-06, formula_export_success=True
  - icbr_full: symbolic_s=1.062929e-01, imitation_mse=1.508087e-04, target_mse=1.592912e-05, formula_export_success=True
  - icbr_no_replay: symbolic_s=9.740360e-02, imitation_mse=1.508087e-04, target_mse=1.592912e-05, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.034878e-01, imitation_mse=1.508087e-04, target_mse=1.592912e-05, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.316132e-01, imitation_mse=1.982435e-02, target_mse=1.993657e-02, formula_export_success=True
- baseline formula (display, rounded):
  - `0.000305517 - 0.997929*cos(3.142*x_1 + 1.57048)`
- icbr_full formula (display, rounded):
  - `0.99903*sin(3.15*x_1 + 2.38419e-7) + 0.000205202`
- icbr_no_replay formula (display, rounded):
  - `0.99903*sin(3.15*x_1 + 2.38419e-7) + 0.000205202`
- icbr_no_shared formula (display, rounded):
  - `0.99903*sin(3.15*x_1 + 2.38419e-7) + 0.000205202`
- icbr_refit_commit formula (display, rounded):
  - `0.909011*sin(2.8136*x_1 - 0.1086) + 0.0151498`

### task=minimal seed=17

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=6.548367e-04, r2=0.998752
- Variant formula overview:
  - baseline: symbolic_s=1.206930e+00, imitation_mse=6.396074e-04, target_mse=7.359743e-06, formula_export_success=True
  - icbr_full: symbolic_s=1.039510e-01, imitation_mse=6.599530e-04, target_mse=1.639747e-05, formula_export_success=True
  - icbr_no_replay: symbolic_s=9.449470e-02, imitation_mse=6.599530e-04, target_mse=1.639747e-05, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.006970e-01, imitation_mse=6.599530e-04, target_mse=1.639747e-05, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.344289e-01, imitation_mse=1.983366e-02, target_mse=2.049430e-02, formula_export_success=True
- baseline formula (display, rounded):
  - `0.997709*sin(3.14472*x_1 - 0.00192) + 0.000900567`
- icbr_full formula (display, rounded):
  - `0.998637*sin(3.15*x_1 + 2.38419e-7) + 0.000955356`
- icbr_no_replay formula (display, rounded):
  - `0.998637*sin(3.15*x_1 + 2.38419e-7) + 0.000955356`
- icbr_no_shared formula (display, rounded):
  - `0.998637*sin(3.15*x_1 + 2.38419e-7) + 0.000955356`
- icbr_refit_commit formula (display, rounded):
  - `0.00815454 - 0.896323*sin(2.8558*x_1 + 3.0084)`

### task=minimal seed=18

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=3.753367e-04, r2=0.999236
- Variant formula overview:
  - baseline: symbolic_s=1.203784e+00, imitation_mse=3.752202e-04, target_mse=3.641841e-06, formula_export_success=True
  - icbr_full: symbolic_s=1.036529e-01, imitation_mse=3.876555e-04, target_mse=1.546769e-05, formula_export_success=True
  - icbr_no_replay: symbolic_s=1.001353e-01, imitation_mse=3.876555e-04, target_mse=1.546769e-05, formula_export_success=True
  - icbr_no_shared: symbolic_s=9.883430e-02, imitation_mse=3.876555e-04, target_mse=1.546769e-05, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.374769e-01, imitation_mse=2.124007e-02, target_mse=2.111817e-02, formula_export_success=True
- baseline formula (display, rounded):
  - `0.99841*sin(3.14168*x_1 - 0.002) - 0.00064992`
- icbr_full formula (display, rounded):
  - `0.99973*sin(3.15*x_1 + 2.38419e-7) - 0.00049017`
- icbr_no_replay formula (display, rounded):
  - `0.99973*sin(3.15*x_1 + 2.38419e-7) - 0.00049017`
- icbr_no_shared formula (display, rounded):
  - `0.99973*sin(3.15*x_1 + 2.38419e-7) - 0.00049017`
- icbr_refit_commit formula (display, rounded):
  - `0.00500529 - 0.892946*sin(2.85052*x_1 + 3.00268)`

### task=minimal seed=19

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=5.628284e-04, r2=0.998878
- Variant formula overview:
  - baseline: symbolic_s=1.206658e+00, imitation_mse=5.489082e-04, target_mse=1.779611e-05, formula_export_success=True
  - icbr_full: symbolic_s=1.025437e-01, imitation_mse=5.599498e-04, target_mse=2.919518e-05, formula_export_success=True
  - icbr_no_replay: symbolic_s=1.038029e-01, imitation_mse=5.599498e-04, target_mse=2.919518e-05, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.019208e-01, imitation_mse=5.599498e-04, target_mse=2.919518e-05, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.348425e-01, imitation_mse=2.155355e-02, target_mse=2.130570e-02, formula_export_success=True
- baseline formula (display, rounded):
  - `0.994749*sin(3.14384*x_1 - 0.00144) - 7.40718e-5`
- icbr_full formula (display, rounded):
  - `0.995766*sin(3.15*x_1 + 2.38419e-7) + 4.00338e-5`
- icbr_no_replay formula (display, rounded):
  - `0.995766*sin(3.15*x_1 + 2.38419e-7) + 4.00338e-5`
- icbr_no_shared formula (display, rounded):
  - `0.995766*sin(3.15*x_1 + 2.38419e-7) + 4.00338e-5`
- icbr_refit_commit formula (display, rounded):
  - `0.894555*sin(2.82104*x_1 + 0.10488) - 0.0170108`

### task=minimal seed=20

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=2.006718e-04, r2=0.999602
- Variant formula overview:
  - baseline: symbolic_s=1.190789e+00, imitation_mse=2.055852e-04, target_mse=1.010590e-05, formula_export_success=True
  - icbr_full: symbolic_s=9.939880e-02, imitation_mse=2.077053e-04, target_mse=1.389460e-05, formula_export_success=True
  - icbr_no_replay: symbolic_s=9.243700e-02, imitation_mse=2.077053e-04, target_mse=1.389460e-05, formula_export_success=True
  - icbr_no_shared: symbolic_s=9.618500e-02, imitation_mse=2.077053e-04, target_mse=1.389460e-05, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.323013e-01, imitation_mse=2.000145e-02, target_mse=1.991596e-02, formula_export_success=True
- baseline formula (display, rounded):
  - `7.21291e-5 - 0.99929*cos(3.14704*x_1 + 1.57336)`
- icbr_full formula (display, rounded):
  - `0.999836*sin(3.15*x_1 + 2.38419e-7) - 3.69325e-5`
- icbr_no_replay formula (display, rounded):
  - `0.999836*sin(3.15*x_1 + 2.38419e-7) - 3.69325e-5`
- icbr_no_shared formula (display, rounded):
  - `0.999836*sin(3.15*x_1 + 2.38419e-7) - 3.69325e-5`
- icbr_refit_commit formula (display, rounded):
  - `0.000383466 - 0.905403*sin(2.84752*x_1 - 3.006)`

### task=poly_cubic seed=1

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.954135e-04, r2=0.996108
- Variant formula overview:
  - baseline: symbolic_s=7.217138e+00, imitation_mse=3.012797e-03, target_mse=3.553136e-03, formula_export_success=True
  - icbr_full: symbolic_s=4.472502e-01, imitation_mse=3.108975e-03, target_mse=3.613444e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=4.415493e-01, imitation_mse=3.115875e-03, target_mse=3.612901e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=6.578014e-01, imitation_mse=3.108974e-03, target_mse=3.613444e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=6.858875e-01, imitation_mse=1.505659e-02, target_mse=1.558922e-02, formula_export_success=True
- baseline formula (display, rounded):
  - `2.00004*atan(0.222923*(0.0217391 - x_2)**2 + 0.0809479*cos(4.74168*x_1 + 1.57632) - 0.223787) + 0.0226163 + 0.411866/(-0.15238*(-x_2 - 0.0506929)**2 + 0.00850057*cos(8.2412*x_1 + 1.5948) + 1)**2`
- icbr_full formula (display, rounded):
  - `0.247357*exp(-0.0582963*(0.0123456 - x_1)**5 + 0.502696*(-x_2 - 0.0507614)**2) - 1.98173*tanh(0.0813639*sin(4.75*x_1 + 2.38419e-7) + 0.481762*sin(1.0*x_2 + 1.55) - 0.270694) + 0.156401`
- icbr_no_replay formula (display, rounded):
  - `0.247357*exp(-0.0582963*(0.0123456 - x_1)**5 + 0.502696*(-x_2 - 0.0507614)**2) - 1.44345*cos(-0.308369*(0.0217391 - x_2)**2 + 0.111875*sin(4.75*x_1 + 2.38419e-7) + 5.0131) + 0.174657`
- icbr_no_shared formula (display, rounded):
  - `0.247357*exp(-0.0582963*(0.0123456 - x_1)**5 + 0.502696*(-x_2 - 0.0507614)**2) - 1.98173*tanh(0.0813639*sin(4.75*x_1 + 2.38419e-7) + 0.481762*sin(1.0*x_2 + 1.55) - 0.270694) + 0.156401`
- icbr_refit_commit formula (display, rounded):
  - `0.167757*(0.00827147*(0.0200002 - x_1)**5 - 0.182148*(-x_2 - 0.0576346)**2 - 1)**4 + 1.36418*sin(0.322568*(0.0303317 - x_2)**2 + 3.08197*sin(0.042*x_1 + 0.59968) - 2.02483) + 0.215885`

### task=poly_cubic seed=2

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=9.988295e-03, r2=0.802038
- Variant formula overview:
  - baseline: symbolic_s=3.601010e+00, imitation_mse=3.550545e-03, target_mse=1.346319e-02, formula_export_success=True
  - icbr_full: symbolic_s=2.785383e-01, imitation_mse=3.555752e-03, target_mse=1.347599e-02, formula_export_success=True
  - icbr_no_replay: symbolic_s=2.404378e-01, imitation_mse=3.560719e-03, target_mse=1.348289e-02, formula_export_success=True
  - icbr_no_shared: symbolic_s=3.198727e-01, imitation_mse=3.555752e-03, target_mse=1.347599e-02, formula_export_success=True
  - icbr_refit_commit: symbolic_s=4.033799e-01, imitation_mse=1.479899e-02, target_mse=2.497926e-02, formula_export_success=True
- baseline formula (display, rounded):
  - `0.0816851 - 1.87524*tan(0.0860173*cos(4.76304*x_1 - 1.58784) + 0.553778*cos(1.116*x_2 - 0.000800001) - 0.456432)`
- icbr_full formula (display, rounded):
  - `2.20127*tan(0.0732691*cos(4.775*x_1 + 1.55) + 1.38801 - 1.44634*exp(-0.2025*(-x_2 - 5.29819e-7)**2)) + 0.0273696`
- icbr_no_replay formula (display, rounded):
  - `1.3537*asin(0.119062*cos(4.775*x_1 + 1.55) - 0.787926*cos(1.1*x_2 + 2.38419e-7) + 0.643037) + 0.0956466`
- icbr_no_shared formula (display, rounded):
  - `2.20127*tan(0.0732691*cos(4.775*x_1 + 1.55) + 1.38801 - 1.44634*exp(-0.2025*(-x_2 - 5.29819e-7)**2)) + 0.0273696`
- icbr_refit_commit formula (display, rounded):
  - `0.0291716 - 2.1447*tan(1.91753*cos(0.0579999*x_1 + 0.70014) - 6.84434 + 5.43521*exp(-0.0518745*x_2**2))`

### task=poly_cubic seed=3

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=2.058470e-03, r2=0.957582
- Variant formula overview:
  - baseline: symbolic_s=7.202921e+00, imitation_mse=2.740473e-03, target_mse=5.030414e-03, formula_export_success=True
  - icbr_full: symbolic_s=4.332083e-01, imitation_mse=2.915679e-03, target_mse=5.242732e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=3.835316e-01, imitation_mse=2.916030e-03, target_mse=5.243354e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=6.539933e-01, imitation_mse=2.915679e-03, target_mse=5.242732e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=6.938892e-01, imitation_mse=1.505449e-02, target_mse=1.781256e-02, formula_export_success=True
- baseline formula (display, rounded):
  - `0.246249*exp(0.347278*(0.046781 - x_2)**2 + 0.035043*cos(8.0336*x_1 + 4.8008)) - 0.761397*asin(0.189385*cos(4.76528*x_1 - 1.57016) + 1.73716*cos(0.87504*x_2 + 0.00824) - 1.38546) - 0.0156121`
- icbr_full formula (display, rounded):
  - `0.249762*exp(0.342969*(0.0468749 - x_2)**2 + 0.00313135*tan(1.55*x_1 + 2.38419e-7)) - 0.76054*acos(0.630979*(-x_2 - 0.01)**2 - 0.189597*sin(4.775*x_1 + 2.38419e-7) - 0.340916) + 1.16919`
- icbr_no_replay formula (display, rounded):
  - `-0.188517*(-0.0904857*(0.0468749 - x_2)**2 - 0.000826145*tan(1.55*x_1 + 2.38419e-7) - 1)**5 - 0.76054*asin(-0.630979*(-x_2 - 0.01)**2 + 0.189597*sin(4.775*x_1 + 2.38419e-7) + 0.340915) + 0.0357985`
- icbr_no_shared formula (display, rounded):
  - `0.249762*exp(0.342969*(0.0468749 - x_2)**2 + 0.00313135*tan(1.55*x_1 + 2.38419e-7)) - 0.76054*acos(0.630979*(-x_2 - 0.01)**2 - 0.189597*sin(4.775*x_1 + 2.38419e-7) - 0.340916) + 1.16919`
- icbr_refit_commit formula (display, rounded):
  - `0.248842*exp(0.33633*(0.0575641 - x_2)**2 + 0.00120701*tan(0.21616*x_1 + 4.488)) + 0.726618*asin(0.657588*(0.000192629 - x_2)**2 + 5.36852*cos(0.0659999*x_1 - 2.59982) + 4.23443) - 0.0288331`

### task=poly_cubic seed=4

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.918766e-03, r2=0.958798
- Variant formula overview:
  - baseline: symbolic_s=5.967133e+00, imitation_mse=3.691457e-03, target_mse=6.437576e-03, formula_export_success=True
  - icbr_full: symbolic_s=4.349407e-01, imitation_mse=3.688520e-03, target_mse=6.446765e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=3.305805e-01, imitation_mse=3.697942e-03, target_mse=6.452423e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=5.415441e-01, imitation_mse=3.688519e-03, target_mse=6.446765e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=6.342684e-01, imitation_mse=1.489727e-02, target_mse=1.769833e-02, formula_export_success=True
- baseline formula (display, rounded):
  - `0.187736*exp(0.0834636*exp(-34.9442*(-x_2 - 0.997144)**2)) - 1.2833*tan(0.115393*cos(4.72968*x_1 - 1.58008) + 0.838351*cos(1.07672*x_2 + 0.00152) + 5.58464) - 0.0516233`
- icbr_full formula (display, rounded):
  - `0.143234*(1 - 0.0475474*tanh(5.0*x_2 + 5.0))**3 + 1.32439*atanh(0.432828*(-x_2 - 5.54462e-8)**2 + 0.111641*cos(4.75*x_1 + 1.55) - 0.135118) + 0.017083`
- icbr_no_replay formula (display, rounded):
  - `0.13913*(1 + 0.0358154*exp(-23.5225*(-0.927835*x_2 - 1)**2))**4 - 1.32407*tan(0.111739*sin(4.75*x_1 + 2.38419e-7) + 0.781735*cos(1.1*x_2 + 2.38419e-7) - 3.79226) - 0.0096226`
- icbr_no_shared formula (display, rounded):
  - `0.143234*(1 - 0.0475474*tanh(5.0*x_2 + 5.0))**3 + 1.32439*atanh(0.432828*(-x_2 - 5.74503e-8)**2 + 0.111641*cos(4.75*x_1 + 1.55) - 0.135118) + 0.017083`
- icbr_refit_commit formula (display, rounded):
  - `0.121908*(1 + 0.350154*exp(-16.7907*(-0.667467*x_2 - 1)**2))**3 + 1.26825*atanh(-5.49234*cos(0.4078*x_2) + 2.96671*cos(0.03504*x_1 + 4.85604) + 4.92471) + 0.0228563`

### task=poly_cubic seed=5

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.582267e-03, r2=0.968798
- Variant formula overview:
  - baseline: symbolic_s=6.994663e+00, imitation_mse=4.018206e-03, target_mse=5.792339e-03, formula_export_success=True
  - icbr_full: symbolic_s=4.416019e-01, imitation_mse=3.996735e-03, target_mse=5.770161e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=3.886877e-01, imitation_mse=4.027128e-03, target_mse=5.804169e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=6.502419e-01, imitation_mse=3.996735e-03, target_mse=5.770160e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=7.221533e-01, imitation_mse=1.266645e-02, target_mse=1.435585e-02, formula_export_success=True
- baseline formula (display, rounded):
  - `-1.91962*tan(-0.0640953*sin(4.77488*x_1 - 9.39504) + 1.02614*cos(0.75128*x_2 + 0.00152) + 5.43581) - 0.0868926*asin(-0.596698*(0.0228776 - x_2)**2 + 0.232319*cos(4.45128*x_1 - 1.58648) + 0.149935) + 0.320378`
- icbr_full formula (display, rounded):
  - `-1.9119*atanh(-0.279763*(-x_2 - 5.4186e-8)**2 + 0.0644405*cos(4.775*x_1 - 1.55) + 0.163056) + 0.130193*atanh(0.155311*cos(4.45*x_1 + 1.55) - 6.5824*cos(0.35*x_2 + 2.38419e-7) + 6.50807) + 0.287056`
- icbr_no_replay formula (display, rounded):
  - `0.112627*tan(0.458291*(0.0249999 - x_2)**2 + 0.178607*cos(4.45*x_1 + 1.55) + 3.02956) - 1.32216*asin(0.0930807*cos(4.775*x_1 - 1.55) + 1.49526*cos(0.75*x_2 + 2.38419e-7) - 1.25259) + 0.297511`
- icbr_no_shared formula (display, rounded):
  - `-1.9119*atanh(-0.279763*(-x_2 - 5.4186e-8)**2 + 0.0644405*cos(4.775*x_1 - 1.55) + 0.163056) + 0.130193*atanh(0.155311*cos(4.45*x_1 + 1.55) - 6.5824*cos(0.35*x_2 - 2.38419e-7) + 6.50808) + 0.287056`
- icbr_refit_commit formula (display, rounded):
  - `-1.43535*asin(1.99439*sin(0.0446*x_1 - 2.70256) + 3.88956*cos(0.44084*x_2 + 4.00001e-5) - 2.82198) + 0.0966979*asin(0.136365*cos(3.56368*x_1 + 1.29096) - 2.97605*cos(0.61008*x_2 + 4.00001e-5) + 2.87873) + 0.296102`

### task=poly_cubic seed=6

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=3.574073e-03, r2=0.930599
- Variant formula overview:
  - baseline: symbolic_s=5.832213e+00, imitation_mse=3.257953e-03, target_mse=7.168230e-03, formula_export_success=True
  - icbr_full: symbolic_s=3.883972e-01, imitation_mse=3.248244e-03, target_mse=7.153893e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=3.172620e-01, imitation_mse=3.254458e-03, target_mse=7.158458e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=5.396523e-01, imitation_mse=3.248244e-03, target_mse=7.153893e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=6.136893e-01, imitation_mse=1.593216e-02, target_mse=1.868952e-02, formula_export_success=True
- baseline formula (display, rounded):
  - `0.235781*(0.437979*cos(1.45232*x_2 + 9.40112) + 1)**(3/2) - 1.11617*atanh(-0.412494*(-x_2 - 0.00255965)**2 + 0.143102*cos(4.74592*x_1 - 1.59512) + 0.169654) + 0.0408959`
- icbr_full formula (display, rounded):
  - `0.177466*cos(0.767641*sin(1.5*x_2 + 1.55) + 1.48786) + 1.22393*atanh(0.37816*(-x_2 - 5.60985e-8)**2 + 0.131062*cos(4.75*x_1 + 1.55) - 0.14352) + 0.2375`
- icbr_no_replay formula (display, rounded):
  - `0.227506*(1 - 0.424701*sin(1.5*x_2 + 1.55))**(3/2) + 0.812421*asin(0.56724*(-x_2 - 5.60985e-8)**2 + 0.196593*cos(4.75*x_1 + 1.55) - 0.24028) + 0.0465889`
- icbr_no_shared formula (display, rounded):
  - `0.177466*cos(0.767641*sin(1.5*x_2 + 1.55) + 1.48786) + 1.22393*atanh(0.37816*(-x_2 - 5.60985e-8)**2 + 0.131062*cos(4.75*x_1 + 1.55) - 0.14352) + 0.2375`
- icbr_refit_commit formula (display, rounded):
  - `0.164185*sin(1.29238*cos(1.15832*x_2 + 4.00001e-5) + 2.52858) + 1.47544*atanh(0.314985*(9.19551e-5 - x_2)**2 + 3.49007*cos(0.0659999*x_1 + 3.6) + 3.01223) + 0.220909`

### task=poly_cubic seed=7

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.627519e-03, r2=0.967116
- Variant formula overview:
  - baseline: symbolic_s=5.972541e+00, imitation_mse=2.820241e-03, target_mse=4.572959e-03, formula_export_success=True
  - icbr_full: symbolic_s=4.062157e-01, imitation_mse=2.833377e-03, target_mse=4.584263e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=3.484510e-01, imitation_mse=2.833377e-03, target_mse=4.584263e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=5.544006e-01, imitation_mse=2.833378e-03, target_mse=4.584260e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=6.377737e-01, imitation_mse=1.608998e-02, target_mse=1.780642e-02, formula_export_success=True
- baseline formula (display, rounded):
  - `1.33352*asin(0.120708*cos(4.77248*x_1 + 1.58144) - 0.479975*cos(1.42032*x_2 + 0.00255999) + 0.453537) + 0.331853 - 0.338103*exp(-0.0928024*(0.0328308 - x_2)**4)`
- icbr_full formula (display, rounded):
  - `-1.40147*asin(0.114676*cos(4.775*x_1 - 1.55) + 0.467391*cos(1.4*x_2 + 2.38419e-7) - 0.46667) + 0.291992 - 0.332672*exp(-0.0943304*(0.0333333 - x_2)**4)`
- icbr_no_replay formula (display, rounded):
  - `-1.40147*asin(0.114676*cos(4.775*x_1 - 1.55) + 0.467391*cos(1.4*x_2 + 2.38419e-7) - 0.46667) + 0.291992 - 0.332672*exp(-0.0943304*(0.0333333 - x_2)**4)`
- icbr_no_shared formula (display, rounded):
  - `0.269201*(0.0233106*(0.0333333 - x_2)**4 - 1)**5 - 1.40147*asin(0.114676*cos(4.775*x_1 - 1.55) + 0.467391*cos(1.4*x_2 + 2.38419e-7) - 0.46667) + 0.228521`
- icbr_refit_commit formula (display, rounded):
  - `-1.67669*atanh(0.310144*sin(1.60484*x_2 + 1.59164) + 3.15354*cos(0.0719999*x_1 + 0.40042) - 3.1722) + 0.364128 - 0.339825*exp(-0.0427866*(0.203617 - x_2)**4)`

### task=poly_cubic seed=8

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.444682e-03, r2=0.969527
- Variant formula overview:
  - baseline: symbolic_s=7.009473e+00, imitation_mse=3.600230e-03, target_mse=5.160966e-03, formula_export_success=True
  - icbr_full: symbolic_s=4.551828e-01, imitation_mse=3.737836e-03, target_mse=5.276306e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=4.129292e-01, imitation_mse=3.746619e-03, target_mse=5.271637e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=6.791772e-01, imitation_mse=3.737836e-03, target_mse=5.276306e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=6.404753e-01, imitation_mse=1.674070e-02, target_mse=2.005192e-02, formula_export_success=True
- baseline formula (display, rounded):
  - `0.336716*tanh(0.0263641*cos(7.57792*x_1 + 4.59896) - 1.92483*cos(1.048*x_2 - 0.00376001) + 1.2107) + 0.61418*asin(0.263327*cos(4.77984*x_1 + 7.80352) - 0.55952*cos(1.38488*x_2 + 0.00624) + 0.254096) + 0.37381`
- icbr_full formula (display, rounded):
  - `-0.754872*tan(0.212536*sin(4.775*x_1 - 0.0499997) - 4.30924 + 1.41373*exp(-0.3025*(-x_2 - 4.33488e-7)**2)) - 0.366987*atan(1.79912*cos(1.05*x_2 + 2.38419e-7) - 1.04939 + 0.865707*exp(-25.0*(-0.7*x_1 - 1)**2)) + 0.404255`
- icbr_no_replay formula (display, rounded):
  - `0.269616*sin(2.39883*cos(1.05*x_2 + 2.38419e-7) + 1.66748 + 1.15428*exp(-25.0*(-0.7*x_1 - 1)**2)) + 0.615953*acos(0.261583*sin(4.775*x_1 - 0.0499997) + 0.580364*cos(1.35*x_2 + 2.38419e-7) - 0.251468) - 0.567116`
- icbr_no_shared formula (display, rounded):
  - `-0.754872*tan(0.212536*sin(4.775*x_1 - 0.0499997) - 4.30924 + 1.41373*exp(-0.3025*(-x_2 - 4.33488e-7)**2)) - 0.366987*atan(1.79912*cos(1.05*x_2 + 2.38419e-7) - 1.04939 + 0.865707*exp(-25.0*(-0.7*x_1 - 1)**2)) + 0.404255`
- icbr_refit_commit formula (display, rounded):
  - `0.747961*tan(7.44907*sin(0.0939999*x_1 + 4.998) + 11.0205 - 1.01409*exp(-0.45153*(-x_2 - 0.012977)**2)) - 0.372045*atan(-0.907042*(6.38319e-5 - x_2)**2 + 0.744591 + 0.604584*exp(-25.0*(-0.72*x_1 - 1)**2)) + 0.406253`

### task=poly_cubic seed=9

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=2.067646e-03, r2=0.953546
- Variant formula overview:
  - baseline: symbolic_s=6.981454e+00, imitation_mse=3.285242e-03, target_mse=5.381184e-03, formula_export_success=True
  - icbr_full: symbolic_s=4.641607e-01, imitation_mse=2.076293e-03, target_mse=4.153348e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=3.874073e-01, imitation_mse=3.288213e-03, target_mse=5.384484e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=6.439174e-01, imitation_mse=2.076293e-03, target_mse=4.153348e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=6.609438e-01, imitation_mse=1.581541e-02, target_mse=1.789388e-02, formula_export_success=True
- baseline formula (display, rounded):
  - `0.427749*cos(-2.60477*cos(0.78464*x_2) + 0.0920644*cos(4.552*x_1 - 4.78472) + 0.341154) - 0.533461*acos(0.221488*cos(4.79048*x_1 + 1.5824) - 1.93719*cos(0.74976*x_2 - 0.00112) + 1.55852) + 1.28226`
- icbr_full formula (display, rounded):
  - `-0.542981*tanh(0.154059*(-x_1 - 0.02)**5 - 4.66521 + 5.18821*exp(-0.1225*(x_2 - 6.81196e-7)**2)) - 0.638892*asin(0.184439*sin(4.8*x_1 + 2.38419e-7) - 3.34836 + 3.7474*exp(-0.1225*(x_2 - 6.81196e-7)**2)) + 0.483799`
- icbr_no_replay formula (display, rounded):
  - `-0.461183*cos(0.0862122*cos(4.55*x_1 + 1.5) - 2.35016*cos(0.8*x_2 + 2.38419e-7) + 3.21946) - 0.708255*atanh(0.165926*cos(4.8*x_1 - 1.55) + 1.45211*cos(0.75*x_2 - 2.38419e-7) - 1.16269) + 0.472379`
- icbr_no_shared formula (display, rounded):
  - `-0.542981*tanh(0.154059*(-x_1 - 0.02)**5 - 4.66521 + 5.18821*exp(-0.1225*(x_2 - 6.81196e-7)**2)) - 0.638892*asin(0.184439*sin(4.8*x_1 - 2.38419e-7) - 3.34836 + 3.7474*exp(-0.1225*(x_2 - 6.81196e-7)**2)) + 0.483799`
- icbr_refit_commit formula (display, rounded):
  - `-0.428507*sin(2.4819*sin(0.12416*x_1 + 1.85232) - 15.3493 + 13.6661*exp(-0.0574656*(-x_2 - 0.000166862)**2)) - 0.814013*tan(3.6758*sin(0.042*x_1 + 2.60064) - 6.95239 + 5.35625*exp(-0.0656794*(-x_2 - 0.00015608)**2)) + 0.484638`

### task=poly_cubic seed=10

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.177968e-03, r2=0.976271
- Variant formula overview:
  - baseline: symbolic_s=5.855235e+00, imitation_mse=3.889414e-03, target_mse=5.142717e-03, formula_export_success=True
  - icbr_full: symbolic_s=4.068666e-01, imitation_mse=3.881449e-03, target_mse=5.126194e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=3.304032e-01, imitation_mse=3.876603e-03, target_mse=5.130812e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=5.367314e-01, imitation_mse=3.881449e-03, target_mse=5.126194e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=5.722438e-01, imitation_mse=1.525092e-02, target_mse=1.594125e-02, formula_export_success=True
- baseline formula (display, rounded):
  - `-2.26605*tan(0.0684452*cos(4.74064*x_1 - 1.58024) + 0.719184*cos(0.86744*x_2 + 0.00152) + 2.51427) + 0.166832 + 0.0125312/(0.124274*(0.0783167 - x_2)**4 - 1)**4`
- icbr_full formula (display, rounded):
  - `-2.08806*tan(0.0741385*sin(4.75*x_1 + 2.38419e-7) + 0.810251*cos(0.85*x_2 + 2.38419e-7) - 3.84861) + 0.170627 + 0.0280308/(0.286044*tanh(5.0*x_2 + 4.7) + 1)**2`
- icbr_no_replay formula (display, rounded):
  - `-1.79471*asin(0.086495*sin(4.75*x_1 + 2.38419e-7) + 0.945292*cos(0.85*x_2 + 2.38419e-7) - 0.831712) + 0.160859 - 0.0136826/(0.152379*(0.0777778 - x_2)**4 - 1)**3`
- icbr_no_shared formula (display, rounded):
  - `-2.08806*tan(0.0741385*sin(4.75*x_1 + 2.38419e-7) + 0.810251*cos(0.85*x_2 + 2.38419e-7) - 3.84861) + 0.170627 + 0.0280308/(0.286044*tanh(5.0*x_2 + 4.7) + 1)**2`
- icbr_refit_commit formula (display, rounded):
  - `-2.05208*tan(3.99781*sin(0.0733999*x_1 - 4.47724) + 3.54618*cos(0.40172*x_2) - 7.32599) + 0.172342 + 0.0280172/(-0.28663*tanh(4.99932*x_2 + 4.7) - 1)**2`

### task=poly_cubic seed=11

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=8.367911e-04, r2=0.983070
- Variant formula overview:
  - baseline: symbolic_s=7.018119e+00, imitation_mse=3.302921e-03, target_mse=4.505047e-03, formula_export_success=True
  - icbr_full: symbolic_s=4.509948e-01, imitation_mse=3.730261e-03, target_mse=4.866564e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=3.546652e-01, imitation_mse=3.730203e-03, target_mse=4.921853e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=6.390084e-01, imitation_mse=3.730260e-03, target_mse=4.866567e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=7.440323e-01, imitation_mse=1.519459e-02, target_mse=1.630470e-02, formula_export_success=True
- baseline formula (display, rounded):
  - `-1.25484*(-0.00468601*(0.0420483 - x_2)**4 - 0.00126049*sin(8.24152*x_1 - 6.18976) + 1)**5 - 1.10882*tan(0.126901*sin(4.75528*x_1 + 0.0052) + 0.719494*cos(1.2496*x_2 + 0.00215999) + 2.61823) + 1.44743`
- icbr_full formula (display, rounded):
  - `-0.961037*(-0.0101984*(0.0421052 - x_2)**4 + 0.00295501*sin(4.25*x_1 - 0.0999997) + 1)**3 - 0.884356*asin(-0.633527*(-x_2 - 6.81196e-8)**2 + 0.159943*sin(4.75*x_1 + 2.38419e-7) + 0.230502) + 1.1458`
- icbr_no_replay formula (display, rounded):
  - `-1.13258*(0.00648838*(0.0421052 - x_2)**4 - 0.00188003*sin(4.25*x_1 - 0.0999997) - 1)**4 - 0.884356*asin(0.159943*sin(4.75*x_1 + 2.38419e-7) + 0.905238*cos(1.25*x_2 + 2.38419e-7) - 0.667652) + 1.31734`
- icbr_no_shared formula (display, rounded):
  - `1.15155*(0.00510666*(0.0421052 - x_2)**4 - 0.00147967*sin(4.25*x_1 - 0.0999997) - 1)**5 + 0.884356*acos(-0.633527*(-x_2 - 6.81196e-8)**2 + 0.159943*sin(4.75*x_1 + 2.38419e-7) + 0.230502) - 0.052829`
- icbr_refit_commit formula (display, rounded):
  - `-0.936961*(-0.00654363*(0.025461 - x_2)**4 + 0.029364*sin(0.13996*x_1 + 2.043) + 1)**4 + 0.791418*asin(0.703848*(1.5125e-9 - x_2)**2 - 4.32545*sin(0.0376*x_1 + 2.9118) + 0.705121) + 1.24245`

### task=poly_cubic seed=12

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=6.100412e-03, r2=0.880727
- Variant formula overview:
  - baseline: symbolic_s=3.535641e+00, imitation_mse=3.071663e-03, target_mse=9.946868e-03, formula_export_success=True
  - icbr_full: symbolic_s=2.620917e-01, imitation_mse=3.064179e-03, target_mse=9.916162e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=2.412291e-01, imitation_mse=3.067917e-03, target_mse=9.933157e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=3.149136e-01, imitation_mse=3.064179e-03, target_mse=9.916162e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=3.998962e-01, imitation_mse=1.626979e-02, target_mse=2.142191e-02, formula_export_success=True
- baseline formula (display, rounded):
  - `1.49986*tan(0.104518*sin(4.72984*x_1 + 9.40432) - 1.62516*cos(0.70528*x_2 + 0.00024) + 7.76407) + 0.139705`
- icbr_full formula (display, rounded):
  - `1.4583*tan(0.107116*cos(4.75*x_1 + 1.55) + 4.45886 - 4.62535*exp(-0.09*(-x_2 - 7.94729e-7)**2)) + 0.166858`
- icbr_no_replay formula (display, rounded):
  - `1.11787*asin(0.140074*cos(4.75*x_1 + 1.55) - 2.21467*cos(0.7*x_2 + 2.38419e-7) + 2.02789) + 0.131707`
- icbr_no_shared formula (display, rounded):
  - `1.4583*tan(0.107116*cos(4.75*x_1 + 1.55) + 4.45886 - 4.62535*exp(-0.09*(-x_2 - 7.94729e-7)**2)) + 0.166858`
- icbr_refit_commit formula (display, rounded):
  - `0.166043 - 1.44596*tan(3.29498*cos(0.0719999*x_1 + 2.69974) - 4.75001 + 7.89333*exp(-0.0523127*x_2**2))`

### task=poly_cubic seed=13

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=7.577989e-03, r2=0.842454
- Variant formula overview:
  - baseline: symbolic_s=3.525821e+00, imitation_mse=3.651513e-03, target_mse=1.114659e-02, formula_export_success=True
  - icbr_full: symbolic_s=2.742272e-01, imitation_mse=3.647726e-03, target_mse=1.113335e-02, formula_export_success=True
  - icbr_no_replay: symbolic_s=2.596963e-01, imitation_mse=3.650249e-03, target_mse=1.114579e-02, formula_export_success=True
  - icbr_no_shared: symbolic_s=3.262717e-01, imitation_mse=3.647726e-03, target_mse=1.113335e-02, formula_export_success=True
  - icbr_refit_commit: symbolic_s=4.334909e-01, imitation_mse=1.691642e-02, target_mse=2.460065e-02, formula_export_success=True
- baseline formula (display, rounded):
  - `0.123462 - 1.63053*tan(-0.100415*sin(4.73968*x_1 + 9.41264) + 1.44316*cos(0.7196*x_2 - 0.000400001) + 1.82473)`
- icbr_full formula (display, rounded):
  - `1.75132*atanh(0.335695*(-x_2 - 4.96705e-8)**2 + 0.0934899*cos(4.75*x_1 + 1.55) - 0.0992855) + 0.093342`
- icbr_no_replay formula (display, rounded):
  - `1.21234*asin(0.135041*cos(4.75*x_1 + 1.55) - 2.04892*cos(0.7*x_2 - 2.38419e-7) + 1.87599) + 0.127506`
- icbr_no_shared formula (display, rounded):
  - `1.75132*atanh(0.335695*(-x_2 - 4.96705e-8)**2 + 0.0934899*cos(4.75*x_1 + 1.55) - 0.0992855) + 0.093342`
- icbr_refit_commit formula (display, rounded):
  - `1.97627*atanh(0.297951*(2.92544e-5 - x_2)**2 + 2.14603*cos(0.0579999*x_1 + 3.80018) + 1.61434) + 0.074241`

### task=poly_cubic seed=14

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=2.188497e-03, r2=0.953776
- Variant formula overview:
  - baseline: symbolic_s=5.821839e+00, imitation_mse=3.680541e-03, target_mse=6.471628e-03, formula_export_success=True
  - icbr_full: symbolic_s=4.094972e-01, imitation_mse=3.687987e-03, target_mse=6.480814e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=3.278783e-01, imitation_mse=3.688036e-03, target_mse=6.470732e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=5.396947e-01, imitation_mse=3.688016e-03, target_mse=6.480893e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=5.705308e-01, imitation_mse=1.574044e-02, target_mse=1.693141e-02, formula_export_success=True
- baseline formula (display, rounded):
  - `-0.0237246*(-0.447424*(0.00241629 - x_2)**4 - 1)**3 + 1.42255*tan(0.111044*cos(4.7444*x_1 + 1.5892) - 0.399292*cos(1.50456*x_2 + 0.00271999) + 9.69736) + 0.107858`
- icbr_full formula (display, rounded):
  - `-0.0310468*(-0.20635*(-x_2 - 5.96046e-8)**4 - 1)**5 - 1.6013*tan(0.0988275*cos(4.75*x_1 - 1.55) + 0.357451*cos(1.5*x_2 + 2.38419e-7) - 0.266521) + 0.0649256`
- icbr_no_replay formula (display, rounded):
  - `-0.0236327*(-0.448486*(-x_2 - 5.96046e-8)**4 - 1)**3 - 1.03467*asin(0.152733*cos(4.75*x_1 - 1.55) + 0.552424*cos(1.5*x_2 + 2.38419e-7) - 0.361897) + 0.125003`
- icbr_no_shared formula (display, rounded):
  - `-0.0308869*(-0.207161*(-x_2 - 5.96046e-8)**4 - 1)**5 - 1.6013*tan(0.0988275*cos(4.75*x_1 - 1.55) + 0.357451*cos(1.5*x_2 + 2.38419e-7) - 0.266521) + 0.0650872`
- icbr_refit_commit formula (display, rounded):
  - `-0.0214427*(-0.393945*(0.0412518 - x_2)**2 - 1)**3 + 1.61846*tan(2.52435*cos(0.0639999*x_1 - 0.6002) + 0.263513*cos(1.80016*x_2 - 3.12) - 1.90164) + 0.069873`

### task=poly_cubic seed=15

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=3.704652e-03, r2=0.925246
- Variant formula overview:
  - baseline: symbolic_s=3.505418e+00, imitation_mse=4.075334e-03, target_mse=7.283895e-03, formula_export_success=True
  - icbr_full: symbolic_s=2.745768e-01, imitation_mse=4.077540e-03, target_mse=7.291895e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=2.416193e-01, imitation_mse=4.081270e-03, target_mse=7.293209e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=3.060510e-01, imitation_mse=4.077540e-03, target_mse=7.291895e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=4.037102e-01, imitation_mse=1.468261e-02, target_mse=1.835653e-02, formula_export_success=True
- baseline formula (display, rounded):
  - `0.0637337 - 1.75657*tan(0.083854*cos(4.7112*x_1 - 1.59296) + 1.03034*cos(0.82392*x_2 + 0.000320001) - 10.3886)`
- icbr_full formula (display, rounded):
  - `1.36705*asin(0.108083*cos(4.7*x_1 + 1.55) - 1.25018*cos(0.85*x_2 + 2.38419e-7) + 1.16728) + 0.0597679`
- icbr_no_replay formula (display, rounded):
  - `1.66614*tan(0.0884319*cos(4.7*x_1 + 1.55) - 1.02288*cos(0.85*x_2 + 2.38419e-7) + 0.945959) + 0.0750131`
- icbr_no_shared formula (display, rounded):
  - `1.36705*asin(0.108083*cos(4.7*x_1 + 1.55) - 1.25018*cos(0.85*x_2 + 2.38419e-7) + 1.16728) + 0.0597679`
- icbr_refit_commit formula (display, rounded):
  - `1.32012*asin(-5.46236*cos(0.40576*x_2) + 5.78762*cos(0.10668*x_1 - 2.98632) + 11.0692) + 0.0691959`

### task=poly_cubic seed=16

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=3.211160e-04, r2=0.992603
- Variant formula overview:
  - baseline: symbolic_s=7.049525e+00, imitation_mse=3.350282e-03, target_mse=4.044123e-03, formula_export_success=True
  - icbr_full: symbolic_s=4.358147e-01, imitation_mse=2.859496e-03, target_mse=3.535331e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=3.794080e-01, imitation_mse=3.350994e-03, target_mse=4.040902e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=6.720254e-01, imitation_mse=2.867690e-03, target_mse=3.545674e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=7.035886e-01, imitation_mse=1.521240e-02, target_mse=1.595138e-02, formula_export_success=True
- baseline formula (display, rounded):
  - `0.111321*(0.517644*(0.0897336 - x_2)**4 - 0.0393693*cos(4.1876*x_1 - 7.98304) + 1)**(3/2) + 0.91788*asin(0.156001*cos(4.75256*x_1 + 1.58808) + 10.0488 - 10.3417*exp(-0.0524959*(-x_2 - 0.0171089)**2)) + 0.159219`
- icbr_full formula (display, rounded):
  - `-0.583832*(0.242676*sin(0.85*x_2 + 1.5) - 0.00074592*tan(1.55*x_1 + 2.38419e-7) - 1)**3 - 1.31058*atanh(-0.372034*(-x_2 - 0.02)**2 + 0.10952*cos(4.75*x_1 - 1.55) + 0.194903) - 0.0066527`
- icbr_no_replay formula (display, rounded):
  - `0.111063*(0.51833*(x_2 - 0.09)**4 + 0.0394274*cos(4.2*x_1 + 1.45) + 1)**(3/2) + 0.932622*acos(-0.520847*(-x_2 - 0.02)**2 + 0.153328*cos(4.75*x_1 - 1.55) + 0.312864) - 1.28028`
- icbr_no_shared formula (display, rounded):
  - `-0.583832*(0.242676*sin(0.85*x_2 + 1.5) - 0.00074592*tan(1.55*x_1 + 2.38419e-7) - 1)**3 - 1.31058*atanh(-0.372389*(-x_2 - 0.0166667)**2 + 0.10952*cos(4.75*x_1 - 1.55) + 0.195098) - 0.00665204`
- icbr_refit_commit formula (display, rounded):
  - `0.319202*(-0.654184*sin(0.90232*x_2 - 4.78768) - 0.150444*cos(0.18576*x_1 + 2.62768) + 1)**(3/2) - 1.32245*atanh(-0.369098*(0.000171962 - x_2)**2 + 2.89508*cos(0.038*x_1 + 2.0984) + 1.64871) + 0.141856`

### task=poly_cubic seed=17

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.642527e-03, r2=0.963773
- Variant formula overview:
  - baseline: symbolic_s=9.055270e+00, imitation_mse=3.441227e-03, target_mse=5.401885e-03, formula_export_success=True
  - icbr_full: symbolic_s=5.661735e-01, imitation_mse=2.255762e-03, target_mse=4.127136e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=4.440185e-01, imitation_mse=3.427599e-03, target_mse=5.404033e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=9.644809e-01, imitation_mse=2.255762e-03, target_mse=4.127136e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=8.040920e-01, imitation_mse=1.646763e-02, target_mse=1.848858e-02, formula_export_success=True
- baseline formula (display, rounded):
  - `0.766695*cos(-0.168163*cos(4.7416*x_1 + 1.576) + 1.33955*cos(0.91976*x_2 + 0.0052) + 0.698873) - 0.309692*tan(-0.106536*cos(4.64464*x_1 + 1.58192) + 8.89804*cos(0.376*x_2 - 0.00408001) + 0.916117) + 0.431126`
- icbr_full formula (display, rounded):
  - `-0.743093*sin(0.172637*cos(4.75*x_1 - 1.55) - 3.20685 + 3.66103*exp(-0.16*(x_2 - 5.96046e-7)**2)) + 0.328512*tan(0.586144*(0.0107526 - x_2)**2 - 0.208653*(0.0416666 - x_1)**5 + 2.76086) + 0.419754`
- icbr_no_replay formula (display, rounded):
  - `0.328512*tan(0.586144*(0.0107526 - x_2)**2 - 0.100157*sin(4.65*x_1 + 2.38419e-7) + 2.74972) + 1.7659 - 2.09991*exp(-1.03453*(-0.0707037*sin(4.75*x_1 + 2.38419e-7) - 0.530248*cos(0.95*x_2 + 2.38419e-7) + 1)**2)`
- icbr_no_shared formula (display, rounded):
  - `-0.743093*sin(0.172637*cos(4.75*x_1 - 1.55) - 3.20685 + 3.66103*exp(-0.16*(x_2 - 5.96046e-7)**2)) + 0.328512*tan(0.586144*(0.0107526 - x_2)**2 - 0.208653*(0.0416666 - x_1)**5 + 2.76086) + 0.419754`
- icbr_refit_commit formula (display, rounded):
  - `0.740928*cos(4.0862*cos(0.04044*x_1 + 1.78876) - 14.3917 + 11.0097*exp(-0.0510759*(-x_2 - 0.0100885)**2)) - 0.304688*asin(-0.630618*(1.01693e-5 - x_2)**2 + 3.47232*sin(0.15336*x_1 - 1.75728) + 3.90994) + 0.448884`

### task=poly_cubic seed=18

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=4.583246e-03, r2=0.906188
- Variant formula overview:
  - baseline: symbolic_s=5.479171e+00, imitation_mse=3.505956e-03, target_mse=8.282366e-03, formula_export_success=True
  - icbr_full: symbolic_s=3.529784e-01, imitation_mse=3.519538e-03, target_mse=8.281240e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=3.310982e-01, imitation_mse=3.499334e-03, target_mse=8.265232e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=5.348365e-01, imitation_mse=3.519538e-03, target_mse=8.281241e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=5.390586e-01, imitation_mse=1.885842e-02, target_mse=3.104780e-02, formula_export_success=True
- baseline formula (display, rounded):
  - `0.177889 - 1.05992*asin(0.150382*cos(4.72888*x_1 - 1.57632) + 1.76288*cos(0.80912*x_2 + 0.00024) - 1.53327)`
- icbr_full formula (display, rounded):
  - `0.163312 - 1.40923*tan(-0.413749*(-x_2 - 7.11697e-8)**2 + 0.112676*sin(4.75*x_1 + 2.38419e-7) + 0.160518)`
- icbr_no_replay formula (display, rounded):
  - `0.16997 - 1.54249*atanh(0.103286*sin(4.75*x_1 + 2.38419e-7) + 1.23998*cos(0.8*x_2 + 2.38419e-7) - 1.08694)`
- icbr_no_shared formula (display, rounded):
  - `0.163312 - 1.40923*tan(-0.413749*(-x_2 - 7.11697e-8)**2 + 0.112676*sin(4.75*x_1 + 2.38419e-7) + 0.160519)`
- icbr_refit_commit formula (display, rounded):
  - `0.123656 - 0.998534*asin(-0.583139*(1.51809e-9 - x_2)**2 + 6.36009*sin(0.0719999*x_1 - 1.90002) + 6.25995)`

### task=poly_cubic seed=19

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=3.605059e-03, r2=0.929806
- Variant formula overview:
  - baseline: symbolic_s=3.608716e+00, imitation_mse=3.664979e-03, target_mse=6.908047e-03, formula_export_success=True
  - icbr_full: symbolic_s=3.194471e-01, imitation_mse=3.664258e-03, target_mse=6.917068e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=2.410028e-01, imitation_mse=3.664678e-03, target_mse=6.916997e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=3.170106e-01, imitation_mse=3.664258e-03, target_mse=6.917068e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=3.902909e-01, imitation_mse=1.559536e-02, target_mse=1.999627e-02, formula_export_success=True
- baseline formula (display, rounded):
  - `0.143462 - 1.35552*tan(-0.115589*cos(4.72936*x_1 + 1.57912) + 1.9612*cos(0.67184*x_2 + 8.00001e-5) + 1.32662)`
- icbr_full formula (display, rounded):
  - `0.143115 - 1.41802*tan(0.110474*sin(4.75*x_1 + 2.38419e-7) - 4.59855 + 4.73837*exp(-0.09*(x_2 - 7.94729e-7)**2))`
- icbr_no_replay formula (display, rounded):
  - `0.143105 - 1.41749*atanh(0.110474*sin(4.75*x_1 + 2.38419e-7) + 1.73498*cos(0.7*x_2 + 2.38419e-7) - 1.59529)`
- icbr_no_shared formula (display, rounded):
  - `0.143115 - 1.41802*tan(0.110474*sin(4.75*x_1 + 2.38419e-7) - 4.59855 + 4.73837*exp(-0.09*(x_2 - 7.94729e-7)**2))`
- icbr_refit_commit formula (display, rounded):
  - `1.4877*tan(2.63716*sin(0.0659999*x_1 - 0.99974) + 12.6837 - 7.44359*exp(-0.0538239*(0.000172414 - x_2)**2)) + 0.12601`

### task=poly_cubic seed=20

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.217910e-03, r2=0.977311
- Variant formula overview:
  - baseline: symbolic_s=3.629915e+00, imitation_mse=3.644018e-03, target_mse=5.072953e-03, formula_export_success=True
  - icbr_full: symbolic_s=2.668608e-01, imitation_mse=3.627000e-03, target_mse=5.055427e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=2.593421e-01, imitation_mse=3.627895e-03, target_mse=5.054052e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=3.225870e-01, imitation_mse=3.627000e-03, target_mse=5.055427e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=3.901895e-01, imitation_mse=1.587339e-02, target_mse=1.921080e-02, formula_export_success=True
- baseline formula (display, rounded):
  - `0.140387 - 1.4086*asin(0.109631*cos(4.71376*x_1 - 1.6056) + 2.24224*cos(0.61848*x_2 - 0.00016) - 2.122)`
- icbr_full formula (display, rounded):
  - `1.56804*asin(0.0986806*cos(4.7*x_1 + 1.55) + 6.07333 - 6.17051*exp(-0.0625*(-x_2 - 9.53674e-7)**2)) + 0.122497`
- icbr_no_replay formula (display, rounded):
  - `1.95642*tan(0.0789445*cos(4.7*x_1 + 1.55) - 1.71252*cos(0.6*x_2 - 2.38419e-7) + 1.6248) + 0.142226`
- icbr_no_shared formula (display, rounded):
  - `1.56804*asin(0.0986806*cos(4.7*x_1 + 1.55) + 6.07333 - 6.17051*exp(-0.0625*(-x_2 - 9.53674e-7)**2)) + 0.122497`
- icbr_refit_commit formula (display, rounded):
  - `0.128626 - 2.14209*atanh(3.39059*cos(0.405*x_2) + 1.87474*cos(0.0679999*x_1 + 0.50024) - 4.95242)`

### task=combo seed=1

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.120128e-04, r2=0.999801
- Variant formula overview:
  - baseline: symbolic_s=7.260437e+00, imitation_mse=1.575066e-04, target_mse=9.581597e-05, formula_export_success=True
  - icbr_full: symbolic_s=4.700611e-01, imitation_mse=2.129885e-04, target_mse=1.611466e-04, formula_export_success=True
  - icbr_no_replay: symbolic_s=3.825425e-01, imitation_mse=2.158085e-04, target_mse=1.622538e-04, formula_export_success=True
  - icbr_no_shared: symbolic_s=6.547572e-01, imitation_mse=2.129885e-04, target_mse=1.611466e-04, formula_export_success=True
  - icbr_refit_commit: symbolic_s=6.739038e-01, imitation_mse=1.604577e-02, target_mse=1.599642e-02, formula_export_success=True
- baseline formula (display, rounded):
  - `1.5773*tan(0.233108*(0.0609914 - x_2)**2 + 0.279291*sin(3.07144*x_1 - 0.00696) + 9.16002) - 3.01592*atan(0.184408*cos(3.20392*x_1 + 1.5732) - 0.404724 + 0.674348*exp(-0.359999*(-x_2 - 0.04)**2)) + 1.21935`
- icbr_full formula (display, rounded):
  - `1.71285*atanh(0.214306*(0.0609137 - x_2)**2 + 0.2558*sin(3.05*x_1 + 2.38419e-7) - 0.266649) + 6.87602 - 8.19722*exp(-0.338859*(-0.139695*sin(3.2*x_1 + 2.38419e-7) - 0.148643*sin(1.6*x_2 - 1.5) - 1)**2)`
- icbr_no_replay formula (display, rounded):
  - `1.54271*tan(0.238118*(0.0609137 - x_2)**2 + 0.284222*sin(3.05*x_1 + 2.38419e-7) + 2.87595) + 2.92217*tanh(0.189744*sin(3.2*x_1 + 2.38419e-7) + 0.201898*sin(1.6*x_2 - 1.5) - 0.0583956) + 1.15892`
- icbr_no_shared formula (display, rounded):
  - `1.71285*atanh(0.214306*(0.0609137 - x_2)**2 + 0.2558*sin(3.05*x_1 + 2.38419e-7) - 0.266649) + 6.87602 - 8.19722*exp(-0.338859*(-0.139695*sin(3.2*x_1 + 2.38419e-7) - 0.148643*sin(1.6*x_2 - 1.5) - 1)**2)`
- icbr_refit_commit formula (display, rounded):
  - `1.52583*tan(-0.33988*sin(1.25304*x_2 - 4.80416) + 0.260783*cos(2.80184*x_1 + 4.61064) + 0.0790962) - 4.11501*tanh(0.12123*sin(2.84396*x_1 - 3.01884) - 0.121349*sin(1.80184*x_2 + 4.804) + 0.191697) + 1.64183`

### task=combo seed=2

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.314176e-04, r2=0.999765
- Variant formula overview:
  - baseline: symbolic_s=7.156276e+00, imitation_mse=3.276161e-04, target_mse=2.476792e-04, formula_export_success=True
  - icbr_full: symbolic_s=4.834693e-01, imitation_mse=2.743214e-04, target_mse=1.747216e-04, formula_export_success=True
  - icbr_no_replay: symbolic_s=3.967248e-01, imitation_mse=3.399679e-04, target_mse=2.538977e-04, formula_export_success=True
  - icbr_no_shared: symbolic_s=6.514257e-01, imitation_mse=2.743216e-04, target_mse=1.747217e-04, formula_export_success=True
  - icbr_refit_commit: symbolic_s=6.895888e-01, imitation_mse=1.270236e-02, target_mse=1.243210e-02, formula_export_success=True
- baseline formula (display, rounded):
  - `1.80553*asin(0.337806*sin(1.75456*x_2 - 1.58792) - 0.25832*cos(3.23432*x_1 + 1.5828) + 0.256186) + 1.07197*atan(0.266784*(-x_2 - 0.00031797)**4 + 0.532407*cos(3.07344*x_1 - 1.5836) + 0.0983992) + 0.0664676`
- icbr_full formula (display, rounded):
  - `-0.934625*cos(-0.30159*(-x_2 - 4.86569e-8)**4 + 0.599126*cos(3.05*x_1 + 1.55) + 4.56851) + 1.9595*asin(0.238802*cos(3.25*x_1 - 1.55) + 0.810058 - 0.856848*exp(-0.5625*(-x_2 - 3.17891e-7)**2)) - 0.0191927`
- icbr_no_replay formula (display, rounded):
  - `1.14223*tanh(0.24914*(-x_2 - 4.86569e-8)**4 - 0.49493*cos(3.05*x_1 + 1.55) + 0.0934084) + 1.9595*asin(-0.299568*sin(1.8*x_2 + 1.55) + 0.238802*cos(3.25*x_1 - 1.55) + 0.25211) + 0.00841437`
- icbr_no_shared formula (display, rounded):
  - `-0.934625*cos(-0.30159*(-x_2 - 5.96046e-8)**4 + 0.599126*cos(3.05*x_1 + 1.55) + 4.56851) + 1.9595*asin(0.238802*cos(3.25*x_1 - 1.55) + 0.810058 - 0.856848*exp(-0.5625*(-x_2 - 3.17891e-7)**2)) - 0.0191927`
- icbr_refit_commit formula (display, rounded):
  - `-1.79569*asin(0.227962*cos(2.94284*x_1 + 1.70996) + 0.340483*cos(1.7496*x_2 - 8.00001e-5) - 0.250866) - 1.34406 + 2.29772*exp(-0.427337*(0.193309*(-x_2 - 0.0203158)**2 + 0.391821*cos(2.8054*x_1 + 4.59544) - 1)**2)`

### task=combo seed=3

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.039162e-04, r2=0.999813
- Variant formula overview:
  - baseline: symbolic_s=7.242601e+00, imitation_mse=3.951316e-04, target_mse=3.943909e-04, formula_export_success=True
  - icbr_full: symbolic_s=4.498822e-01, imitation_mse=3.704526e-04, target_mse=3.603154e-04, formula_export_success=True
  - icbr_no_replay: symbolic_s=3.856168e-01, imitation_mse=4.423131e-04, target_mse=4.472812e-04, formula_export_success=True
  - icbr_no_shared: symbolic_s=7.058822e-01, imitation_mse=3.704526e-04, target_mse=3.603154e-04, formula_export_success=True
  - icbr_refit_commit: symbolic_s=7.255334e-01, imitation_mse=1.146703e-02, target_mse=1.148244e-02, formula_export_success=True
- baseline formula (display, rounded):
  - `1.19211*tan(0.407649*(-x_2 - 0.0051755)**2 + 0.306781*cos(3.63704*x_1 - 1.38904) + 6.03685) - 1.00539 + 2.61688*exp(-0.334809*(0.525516*cos(2.80256*x_1 - 7.98392) - 0.439876*cos(1.4712*x_2 - 0.00744) - 1)**2)`
- icbr_full formula (display, rounded):
  - `-1.57192*atan(0.432463*cos(2.8*x_1 + 1.45) + 0.350902*cos(1.5*x_2 + 2.38419e-7) - 0.202968) - 1.18961*atanh(0.307771*sin(3.65*x_1 - 2.95) + 9.13466*cos(0.3*x_2 + 2.38419e-7) - 8.90774) + 0.508921`
- icbr_no_replay formula (display, rounded):
  - `1.26324*tan(0.384965*(-x_2 - 0.01)**2 - 0.289666*sin(3.65*x_1 - 2.95) + 2.88363) - 1.07258 + 2.74162*exp(-0.337973*(0.495925*cos(2.8*x_1 + 1.45) + 0.402396*cos(1.5*x_2 + 2.38419e-7) + 1)**2)`
- icbr_no_shared formula (display, rounded):
  - `-1.57192*atan(0.432463*cos(2.8*x_1 + 1.45) + 0.350902*cos(1.5*x_2 + 2.38419e-7) - 0.202968) - 1.18961*atanh(0.307771*sin(3.65*x_1 - 2.95) + 9.13466*cos(0.3*x_2 + 2.38419e-7) - 8.90774) + 0.508921`
- icbr_refit_commit formula (display, rounded):
  - `0.871492*asin(0.362537*sin(3.26292*x_1 + 0.30924) - 3.60015*cos(0.56308*x_2) + 3.28488) + 2.1362 - 2.73863*exp(-0.7005*(0.335436*sin(2.6486*x_1 - 0.18556) + 0.249414*sin(1.60496*x_2 - 1.59168) + 1)**2)`

### task=combo seed=4

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=2.614565e-04, r2=0.999526
- Variant formula overview:
  - baseline: symbolic_s=7.072984e+00, imitation_mse=2.859471e-04, target_mse=1.512262e-04, formula_export_success=True
  - icbr_full: symbolic_s=5.144985e-01, imitation_mse=3.161757e-04, target_mse=1.875380e-04, formula_export_success=True
  - icbr_no_replay: symbolic_s=3.849054e-01, imitation_mse=3.161757e-04, target_mse=1.875380e-04, formula_export_success=True
  - icbr_no_shared: symbolic_s=6.585580e-01, imitation_mse=3.225664e-04, target_mse=1.890226e-04, formula_export_success=True
  - icbr_refit_commit: symbolic_s=7.256630e-01, imitation_mse=1.635681e-02, target_mse=1.634706e-02, formula_export_success=True
- baseline formula (display, rounded):
  - `1.02068*asin(-0.511333*cos(3.23648*x_1 + 1.608) + 0.53922*cos(1.44576*x_2 - 9.41232) + 0.297181) + 1.46889 - 1.75225*exp(-33.1933*(0.0557791*cos(3.02392*x_1 + 7.80136) + 0.895207*cos(0.36008*x_2 - 0.00376001) - 1)**2)`
- icbr_full formula (display, rounded):
  - `1.03525*asin(0.506737*sin(3.25*x_1 + 0.0500002) + 0.475216*sin(1.55*x_2 - 1.55) + 0.249314) + 1.44449 - 1.77115*exp(-0.38436*(-0.526309*(0.0142856 - x_2)**2 - 0.509934*sin(3.0*x_1 - 0.0499997) - 1)**2)`
- icbr_no_replay formula (display, rounded):
  - `1.03525*asin(0.506737*sin(3.25*x_1 + 0.0500002) + 0.475216*sin(1.55*x_2 - 1.55) + 0.249314) + 1.44449 - 1.77115*exp(-0.38436*(-0.526309*(0.0142856 - x_2)**2 - 0.509934*sin(3.0*x_1 - 0.0499997) - 1)**2)`
- icbr_no_shared formula (display, rounded):
  - `1.03525*acos(-0.506737*sin(3.25*x_1 + 0.0500002) - 0.475216*sin(1.55*x_2 - 1.55) - 0.249314) - 0.181676 - 1.77115*exp(-0.384198*(-0.527609*(0.0103092 - x_2)**2 - 0.510042*sin(3.0*x_1 - 0.0499997) - 1)**2)`
- icbr_refit_commit formula (display, rounded):
  - `-1.05678*asin(0.444643*cos(2.91168*x_1 + 1.70908) - 1.27707 + 1.50999*exp(-0.361201*(6.65559e-5 - x_2)**2)) - 0.766032 + 1.97011*exp(-4.01654*(0.129595*sin(2.75228*x_1 - 3.1052) + cos(0.54476*x_2 - 4.00001e-5) - 0.591363)**2)`

### task=combo seed=5

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=7.334883e-02, r2=0.872105
- Variant formula overview:
  - baseline: symbolic_s=5.857722e+00, imitation_mse=2.588509e-03, target_mse=6.948139e-02, formula_export_success=True
  - icbr_full: symbolic_s=3.919587e-01, imitation_mse=2.891312e-03, target_mse=7.016528e-02, formula_export_success=True
  - icbr_no_replay: symbolic_s=3.265316e-01, imitation_mse=2.904917e-03, target_mse=7.016235e-02, formula_export_success=True
  - icbr_no_shared: symbolic_s=5.519208e-01, imitation_mse=2.891312e-03, target_mse=7.016528e-02, formula_export_success=True
  - icbr_refit_commit: symbolic_s=5.681637e-01, imitation_mse=8.738559e-03, target_mse=8.422472e-02, formula_export_success=True
- baseline formula (display, rounded):
  - `-3.59261*sin(0.146544*cos(3.23368*x_1 + 7.78928) + 0.943589*cos(0.786*x_2 + 0.000480001) - 7.05472) + 0.68137*tanh(0.217258*Abs(9.99994*x_1 + 5.4) - 1.25387) + 0.397765`
- icbr_full formula (display, rounded):
  - `0.698872*tanh(0.464595*Abs(4.45*x_1 + 2.4) - 1.20035) - 4.76532*tanh(0.110848*cos(3.25*x_1 + 1.5) + 0.68858*cos(0.8*x_2 - 2.38419e-7) - 0.557548) + 0.404086`
- icbr_no_replay formula (display, rounded):
  - `-3.80653*cos(0.13856*cos(3.25*x_1 + 1.5) + 0.860726*cos(0.8*x_2 - 2.38419e-7) - 2.25943) + 0.698872*tanh(0.464595*Abs(4.45*x_1 + 2.4) - 1.20035) + 0.435486`
- icbr_no_shared formula (display, rounded):
  - `0.698872*tanh(0.464595*Abs(4.45*x_1 + 2.4) - 1.20035) - 4.76532*tanh(0.110848*cos(3.25*x_1 + 1.5) + 0.68858*cos(0.8*x_2 - 2.38419e-7) - 0.557548) + 0.404086`
- icbr_refit_commit formula (display, rounded):
  - `0.626532*cos(0.449278*Abs(4.7756*x_1 + 2.58844) + 3.4084) - 4.82826*tanh(0.0977531*cos(2.89948*x_1 + 1.61444) - 4.86864 + 5.00114*exp(-0.0423042*x_2**2)) + 0.443032`

### task=combo seed=6

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.931976e-04, r2=0.999663
- Variant formula overview:
  - baseline: symbolic_s=7.031725e+00, imitation_mse=4.006958e-04, target_mse=2.410274e-04, formula_export_success=True
  - icbr_full: symbolic_s=4.871704e-01, imitation_mse=3.930925e-04, target_mse=2.678412e-04, formula_export_success=True
  - icbr_no_replay: symbolic_s=4.120557e-01, imitation_mse=3.947682e-04, target_mse=2.716619e-04, formula_export_success=True
  - icbr_no_shared: symbolic_s=7.009664e-01, imitation_mse=3.930925e-04, target_mse=2.678412e-04, formula_export_success=True
  - icbr_refit_commit: symbolic_s=6.686155e-01, imitation_mse=1.414214e-02, target_mse=1.394419e-02, formula_export_success=True
- baseline formula (display, rounded):
  - `2.27649*tan(0.252275*cos(2.98064*x_1 - 1.57392) + 3.27699 - 0.290431*exp(-1.77039*(-x_2 - 0.00709476)**2)) + 0.936046*atan(0.515557*(-x_2 - 0.00841224)**4 + 0.472844*cos(3.35272*x_1 - 1.58256) - 0.200202) + 0.526273`
- icbr_full formula (display, rounded):
  - `2.23346*tan(0.257347*sin(3.0*x_1 + 2.38419e-7) + 0.12342*sin(2.8*x_2 - 1.55) + 3.0998) - 1.02991*tanh(-0.463778*(-x_2 - 0.0111112)**4 + 0.426342*cos(3.35*x_1 + 1.55) + 0.195669) + 0.562276`
- icbr_no_replay formula (display, rounded):
  - `2.23346*tan(0.257347*sin(3.0*x_1 + 2.38419e-7) + 0.12342*sin(2.8*x_2 - 1.55) + 3.0998) - 0.976549*atan(-0.491059*(-x_2 - 0.0111112)**4 + 0.451421*cos(3.35*x_1 + 1.55) + 0.207179) + 0.562191`
- icbr_no_shared formula (display, rounded):
  - `2.23346*tan(0.257347*sin(3.0*x_1 + 2.38419e-7) + 0.12342*sin(2.8*x_2 - 1.55) + 3.0998) - 1.02991*tanh(-0.463778*(-x_2 - 0.0111112)**4 + 0.426342*cos(3.35*x_1 + 1.55) + 0.195669) + 0.562276`
- icbr_refit_commit formula (display, rounded):
  - `-2.30586*tan(-0.230808*sin(2.732*x_1 - 0.11472) + 0.120072*sin(2.79984*x_2 - 4.71236) + 0.0121895) - 0.973229*atan(-0.453672*(0.00218407 - x_2)**4 + 0.392181*sin(3.02164*x_1 + 3.30464) + 0.166538) + 0.470204`

### task=combo seed=7

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=9.501844e-05, r2=0.999847
- Variant formula overview:
  - baseline: symbolic_s=7.036956e+00, imitation_mse=1.823987e-04, target_mse=1.233137e-04, formula_export_success=True
  - icbr_full: symbolic_s=4.451364e-01, imitation_mse=1.571475e-04, target_mse=1.109143e-04, formula_export_success=True
  - icbr_no_replay: symbolic_s=3.749654e-01, imitation_mse=2.201095e-04, target_mse=1.650265e-04, formula_export_success=True
  - icbr_no_shared: symbolic_s=6.488006e-01, imitation_mse=1.571475e-04, target_mse=1.109143e-04, formula_export_success=True
  - icbr_refit_commit: symbolic_s=7.180980e-01, imitation_mse=1.442039e-02, target_mse=1.429344e-02, formula_export_success=True
- baseline formula (display, rounded):
  - `1.4741*asin(0.34792*sin(2.96952*x_1 + 0.00872) + 0.28651*cos(2.11104*x_2 + 9.40808) + 0.174294) - 1.05811 + 2.09644*exp(-0.527851*(0.264315*(0.00483999 - x_2)**4 + 0.381845*cos(3.3288*x_1 - 1.58224) - 1)**2)`
- icbr_full formula (display, rounded):
  - `1.35234*acos(-0.375891*sin(2.95*x_1 + 2.38419e-7) + 0.30335*sin(2.15*x_2 + 1.55) - 0.16767) - 3.25679 + 2.21206*exp(-0.507578*(0.254342*(-x_2 - 5.155e-8)**4 + 0.369088*sin(3.35*x_1 + 2.38419e-7) - 1)**2)`
- icbr_no_replay formula (display, rounded):
  - `1.35234*asin(0.375891*sin(2.95*x_1 + 2.38419e-7) - 0.30335*sin(2.15*x_2 + 1.55) + 0.16767) - 1.13253 + 2.21206*exp(-0.508386*(0.25414*(-x_2 - 5.155e-8)**4 - 0.368781*cos(3.35*x_1 + 1.55) - 1)**2)`
- icbr_no_shared formula (display, rounded):
  - `1.35234*acos(-0.375891*sin(2.95*x_1 + 2.38419e-7) + 0.30335*sin(2.15*x_2 + 1.55) - 0.16767) - 3.25679 + 2.21206*exp(-0.507578*(0.254342*(-x_2 - 5.155e-8)**4 + 0.369088*sin(3.35*x_1 + 2.38419e-7) - 1)**2)`
- icbr_refit_commit formula (display, rounded):
  - `-0.874536*cos(0.372782*(-x_2 - 0.00245067)**4 - 0.498615*sin(3.0214*x_1 - 3.01428) + 1.57145) + 2.22006*atanh(0.211897*sin(2.66392*x_1 - 0.0880399) + 0.198223*sin(2.05244*x_2 + 4.71232) + 0.12962) + 0.175847`

### task=combo seed=8

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=2.851223e-04, r2=0.999498
- Variant formula overview:
  - baseline: symbolic_s=6.986491e+00, imitation_mse=6.286203e-04, target_mse=5.532047e-04, formula_export_success=True
  - icbr_full: symbolic_s=4.618243e-01, imitation_mse=5.843451e-04, target_mse=4.054306e-04, formula_export_success=True
  - icbr_no_replay: symbolic_s=3.888309e-01, imitation_mse=6.423699e-04, target_mse=5.745645e-04, formula_export_success=True
  - icbr_no_shared: symbolic_s=6.452158e-01, imitation_mse=5.836560e-04, target_mse=4.048318e-04, formula_export_success=True
  - icbr_refit_commit: symbolic_s=7.026817e-01, imitation_mse=2.090624e-02, target_mse=2.144920e-02, formula_export_success=True
- baseline formula (display, rounded):
  - `-0.324821*cos(0.405571*(0.00623441 - x_2)**4 - 0.710044*cos(4.16728*x_1 + 1.38984) + 1.41645) + 0.230633*Abs(3.57678*cos(2.8488*x_1 - 7.80928) - 4.39318*cos(1.41992*x_2 + 0.000640001) + 7.72422) - 0.732118`
- icbr_full formula (display, rounded):
  - `12.8418*tan(0.0636886*sin(2.85*x_1 + 0.0500002) - 0.0801493*cos(1.4*x_2 + 2.38419e-7) + 3.12877) + 0.816357 + 0.715612*exp(-0.660314*(-0.266127*(-x_2 - 7.45058e-8)**4 + 0.46679*sin(4.15*x_1 + 2.95) + 1)**2)`
- icbr_no_replay formula (display, rounded):
  - `0.275583*Abs(2.99336*sin(2.85*x_1 + 0.0500002) - 3.76702*cos(1.4*x_2 + 2.38419e-7) + 6.55203) - 1.15224 + 0.715612*exp(-0.660314*(-0.266127*(-x_2 - 7.45058e-8)**4 + 0.46679*sin(4.15*x_1 + 2.95) + 1)**2)`
- icbr_no_shared formula (display, rounded):
  - `-12.8258*atanh(-0.0636886*sin(2.85*x_1 + 0.0500002) + 0.0801493*cos(1.4*x_2 + 2.38419e-7) + 0.0212336) + 0.923935 + 0.715612*exp(-0.660413*(-0.265705*(x_2 - 0.01)**4 + 0.466755*sin(4.15*x_1 + 2.95) + 1)**2)`
- icbr_refit_commit formula (display, rounded):
  - `-0.352295*Abs(2.18397*sin(2.63876*x_1 + 0.11172) + 45.2572 - 49.6788*exp(-0.0514926*(x_2 + 0.000176274)**2)) + 1.1497 + 0.763338*exp(-0.714182*(-0.292019*sin(3.47984*x_1 - 0.40636) + cos(0.65592*x_2 + 8.00001e-5) - 0.0519038)**2)`

### task=combo seed=9

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=2.056647e-04, r2=0.999644
- Variant formula overview:
  - baseline: symbolic_s=7.011967e+00, imitation_mse=4.922721e-04, target_mse=3.628996e-04, formula_export_success=True
  - icbr_full: symbolic_s=4.765229e-01, imitation_mse=5.064688e-04, target_mse=3.774865e-04, formula_export_success=True
  - icbr_no_replay: symbolic_s=3.941214e-01, imitation_mse=5.108187e-04, target_mse=3.812175e-04, formula_export_success=True
  - icbr_no_shared: symbolic_s=6.545884e-01, imitation_mse=5.064688e-04, target_mse=3.774865e-04, formula_export_success=True
  - icbr_refit_commit: symbolic_s=6.967237e-01, imitation_mse=2.194179e-02, target_mse=2.225103e-02, formula_export_success=True
- baseline formula (display, rounded):
  - `3.11612*tan(0.056756*(0.0308286 - x_2)**2 + 0.0968357*sin(3.0052*x_1 + 0.00263999) - 3.96588) + 1.84709*atan(0.218704*cos(3.3784*x_1 - 1.59496) + 0.559191 - 0.96978*exp(-0.456111*(-x_2 - 0.013267)**2)) + 4.10384`
- icbr_full formula (display, rounded):
  - `8.49867 + 2.84453*exp(-0.547749*(0.351569*sin(1.6*x_2 - 1.55) - 0.223702*cos(3.4*x_1 + 1.55) - 1)**2) - 9.52973/sqrt(0.0806149*(0.0307691 - x_2)**2 + 0.13745*sin(3.0*x_1 + 2.38419e-7) + 1)`
- icbr_no_replay formula (display, rounded):
  - `3.13577*log(0.56805*(0.0307691 - x_2)**2 + 0.96854*sin(3.0*x_1 + 2.38419e-7) + 4.64647) - 2.15535*tanh(-0.297367*sin(1.6*x_2 - 1.55) + 0.189213*cos(3.4*x_1 + 1.55) + 0.110115) - 3.96799`
- icbr_no_shared formula (display, rounded):
  - `8.49867 + 2.84453*exp(-0.547749*(0.351569*sin(1.6*x_2 - 1.55) - 0.223702*cos(3.4*x_1 + 1.55) - 1)**2) - 9.52973/sqrt(0.0806149*(0.0307692 - x_2)**2 + 0.13745*sin(3.0*x_1 + 2.38419e-7) + 1)`
- icbr_refit_commit formula (display, rounded):
  - `13.1287 - 4.37336*exp(-0.351827*(0.248776*sin(1.75348*x_2 - 4.71236) + 0.156542*cos(3.01256*x_1 + 1.71824) - 1)**2) - 9.53292/sqrt(0.0791958*(0.0489794 - x_2)**2 + 0.126537*sin(2.74336*x_1 + 0.10104) + 1)`

### task=combo seed=10

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=5.109108e-04, r2=0.999153
- Variant formula overview:
  - baseline: symbolic_s=5.915945e+00, imitation_mse=8.057309e-04, target_mse=4.331748e-04, formula_export_success=True
  - icbr_full: symbolic_s=4.058846e-01, imitation_mse=5.858886e-04, target_mse=2.708456e-04, formula_export_success=True
  - icbr_no_replay: symbolic_s=3.335947e-01, imitation_mse=6.015590e-04, target_mse=2.825860e-04, formula_export_success=True
  - icbr_no_shared: symbolic_s=5.608393e-01, imitation_mse=5.858886e-04, target_mse=2.708456e-04, formula_export_success=True
  - icbr_refit_commit: symbolic_s=5.861545e-01, imitation_mse=1.520202e-02, target_mse=1.479717e-02, formula_export_success=True
- baseline formula (display, rounded):
  - `18.3716*(-0.0251243*cos(3.3268*x_1 + 1.5828) - 0.0824821*cos(0.98312*x_2 + 0.00144) + 1)**(3/2) - 0.448637*sin(0.191456 - 3.78599*exp(-0.568154*(-x_1 - 0.573763)**2)) - 16.2659`
- icbr_full formula (display, rounded):
  - `17.2867*(0.0267944*cos(3.35*x_1 - 1.55) - 0.0850181*cos(1.0*x_2 + 2.38419e-7) + 1)**(3/2) - 0.456949*cos(4.67583 - 3.53941*exp(-0.64*(-x_1 - 0.5625)**2)) - 15.2587`
- icbr_no_replay formula (display, rounded):
  - `25.0348*(-0.0138848*cos(3.35*x_1 - 1.55) + 0.0440564*cos(1.0*x_2 + 2.38419e-7) - 1)**2 - 0.447421*sin(6.26909 - 3.5956*exp(-0.64*(-x_1 - 0.5625)**2)) - 22.9959`
- icbr_no_shared formula (display, rounded):
  - `17.2867*(0.0267944*cos(3.35*x_1 - 1.55) - 0.0850181*cos(1.0*x_2 + 2.38419e-7) + 1)**(3/2) - 0.456949*cos(4.67583 - 3.53941*exp(-0.64*(-x_1 - 0.5625)**2)) - 15.2587`
- icbr_refit_commit formula (display, rounded):
  - `-15.1254*(-0.0214646*(1.4967e-9 - x_2)**2 - 0.0128715*cos(2.98876*x_1 - 1.41292) - 1)**3 - 15.9837 + 1.18341*exp(-3.14098*(0.501329 - exp(-0.499396*(-x_1 - 0.583178)**2))**2)`

### task=combo seed=11

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=9.046971e-02, r2=0.846260
- Variant formula overview:
  - baseline: symbolic_s=5.973919e+00, imitation_mse=9.243375e-04, target_mse=9.382130e-02, formula_export_success=True
  - icbr_full: symbolic_s=4.129185e-01, imitation_mse=8.245591e-04, target_mse=9.129374e-02, formula_export_success=True
  - icbr_no_replay: symbolic_s=3.328040e-01, imitation_mse=1.030428e-03, target_mse=9.477782e-02, formula_export_success=True
  - icbr_no_shared: symbolic_s=5.442392e-01, imitation_mse=8.245591e-04, target_mse=9.129374e-02, formula_export_success=True
  - icbr_refit_commit: symbolic_s=5.892809e-01, imitation_mse=5.887970e-03, target_mse=1.080406e-01, formula_export_success=True
- baseline formula (display, rounded):
  - `-0.0854885*(sin(3.31712*x_1 - 0.00368001) - 0.196208)**2 + 6.72203 - 9.80608*exp(-1.52412*(0.47354*cos(0.64808*x_2) + 0.0689333*cos(3.06992*x_1 + 1.57312) - 1)**2)`
- icbr_full formula (display, rounded):
  - `1.55086*cos(0.139882 - 0.579034*exp(-5.0625*(-x_1 - 0.488889)**2)) - 7.82951 + 11.8319*exp(-0.587496*(-0.128707*(-x_2 - 7.69092e-8)**2 - 0.0915691*sin(3.05*x_1 + 2.38419e-7) + 1)**2)`
- icbr_no_replay formula (display, rounded):
  - `-0.0872832*(sin(3.3*x_1 + 2.38419e-7) - 0.182008)**2 + 4.35457*sin(-0.163768*sin(3.05*x_1 + 2.38419e-7) + 1.12225*cos(0.65*x_2 + 2.38419e-7) + 2.13354) + 0.79169`
- icbr_no_shared formula (display, rounded):
  - `1.55086*cos(0.139882 - 0.579034*exp(-5.0625*(-x_1 - 0.488889)**2)) - 7.82951 + 11.8319*exp(-0.587496*(-0.128707*(-x_2 - 7.69092e-8)**2 - 0.0915691*sin(3.05*x_1 + 2.38419e-7) + 1)**2)`
- icbr_refit_commit formula (display, rounded):
  - `0.678517*cos(0.214245 - 0.885034*exp(-5.0643*(-x_1 - 0.488855)**2)) + 7.57289 - 12.1478*exp(-0.422122*(-0.147873*(-x_2 - 1.09904e-5)**2 - 0.097716*sin(2.80948*x_1 + 0.0947199) - 1)**2)`

### task=combo seed=12

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.145521e-04, r2=0.999809
- Variant formula overview:
  - baseline: symbolic_s=6.981194e+00, imitation_mse=9.230289e-05, target_mse=2.829833e-05, formula_export_success=True
  - icbr_full: symbolic_s=4.599275e-01, imitation_mse=1.275011e-04, target_mse=7.120007e-05, formula_export_success=True
  - icbr_no_replay: symbolic_s=3.702863e-01, imitation_mse=1.275011e-04, target_mse=7.120007e-05, formula_export_success=True
  - icbr_no_shared: symbolic_s=6.567847e-01, imitation_mse=1.275011e-04, target_mse=7.120007e-05, formula_export_success=True
  - icbr_refit_commit: symbolic_s=7.485238e-01, imitation_mse=1.303878e-02, target_mse=1.324740e-02, formula_export_success=True
- baseline formula (display, rounded):
  - `-1.6006*tan(0.313186*cos(3.11976*x_1 + 1.59496) + 0.690738*cos(0.92912*x_2 + 0.000480001) - 10.1606) + 1.62905*atan(0.335225*(-x_2 - 0.000895578)**2 + 0.306807*cos(3.158*x_1 - 1.59496) + 0.0844375) - 0.206143`
- icbr_full formula (display, rounded):
  - `1.60976*tan(0.31095*cos(3.1*x_1 - 1.55) - 0.659955*cos(0.95*x_2 + 2.38419e-7) + 0.701268) + 1.41965 - 2.67709*exp(-0.590904*(0.309153*(-x_2 - 5.01934e-8)**2 - 0.282644*cos(3.15*x_1 + 1.55) + 1)**2)`
- icbr_no_replay formula (display, rounded):
  - `1.60976*tan(0.31095*cos(3.1*x_1 - 1.55) - 0.659955*cos(0.95*x_2 + 2.38419e-7) + 0.701268) + 1.41965 - 2.67709*exp(-0.590904*(0.309153*(-x_2 - 5.01934e-8)**2 - 0.282644*cos(3.15*x_1 + 1.55) + 1)**2)`
- icbr_no_shared formula (display, rounded):
  - `1.60976*tan(0.31095*cos(3.1*x_1 - 1.55) - 0.659955*cos(0.95*x_2 + 2.38419e-7) + 0.701268) + 1.41965 - 2.67709*exp(-0.590904*(0.309153*(-x_2 - 5.01934e-8)**2 - 0.282644*cos(3.15*x_1 + 1.55) + 1)**2)`
- icbr_refit_commit formula (display, rounded):
  - `1.75042*tanh(0.258243*cos(2.88604*x_1 - 1.69844) + 3.98715 - 3.89391*exp(-0.0828748*x_2**2)) - 1.77843*atanh(0.253171*cos(2.82064*x_1 + 1.70712) - 4.59312 + 4.53127*exp(-0.0570444*x_2**2)) - 0.268409`

### task=combo seed=13

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.883648e-04, r2=0.999693
- Variant formula overview:
  - baseline: symbolic_s=7.056927e+00, imitation_mse=4.421494e-04, target_mse=3.109726e-04, formula_export_success=True
  - icbr_full: symbolic_s=4.600664e-01, imitation_mse=4.035065e-04, target_mse=2.636155e-04, formula_export_success=True
  - icbr_no_replay: symbolic_s=4.154956e-01, imitation_mse=4.128863e-04, target_mse=2.749820e-04, formula_export_success=True
  - icbr_no_shared: symbolic_s=6.439385e-01, imitation_mse=4.035065e-04, target_mse=2.636155e-04, formula_export_success=True
  - icbr_refit_commit: symbolic_s=6.779415e-01, imitation_mse=1.621562e-02, target_mse=1.621162e-02, formula_export_success=True
- baseline formula (display, rounded):
  - `-1.21761*acos(0.38992*(0.00553776 - x_2)**2 - 0.380887*cos(3.40272*x_1 + 1.59592) - 0.336238) + 4.60943 - 3.26695*exp(-0.859307*(0.205625*sin(2.87736*x_1 + 9.39544) - 1 + 0.355796*exp(-0.742354*(-x_2 - 0.00334261)**2))**2)`
- icbr_full formula (display, rounded):
  - `1.4427*sin(0.372099*cos(2.9*x_1 + 1.55) - 3.54117 + 0.654615*exp(-0.7225*(-x_2 - 2.80492e-7)**2)) + 1.71061*atanh(0.277087*(-x_2 - 5.54462e-8)**2 + 0.271024*cos(3.4*x_1 - 1.55) - 0.248603) + 0.789339`
- icbr_no_replay formula (display, rounded):
  - `1.25663*asin(0.377846*(-x_2 - 5.54462e-8)**2 + 0.369578*cos(3.4*x_1 - 1.55) - 0.33446) + 2.62125 - 3.12905*exp(-0.893493*(0.211967*cos(2.9*x_1 + 1.55) - 1 + 0.372902*exp(-0.7225*(-x_2 - 2.80492e-7)**2))**2)`
- icbr_no_shared formula (display, rounded):
  - `1.4427*sin(0.372099*cos(2.9*x_1 + 1.55) - 3.54117 + 0.654615*exp(-0.7225*(-x_2 - 2.80492e-7)**2)) + 1.71061*atanh(0.277087*(-x_2 - 5.54462e-8)**2 + 0.271024*cos(3.4*x_1 - 1.55) - 0.248603) + 0.789339`
- icbr_refit_commit formula (display, rounded):
  - `1.43127*cos(-0.350303*cos(2.6314*x_1 + 4.60744) + 1.19121 + 0.629974*exp(-0.767516*(-x_2 - 0.01041)**2)) + 1.27863*acos(-0.371106*(0.000100325 - x_2)**2 - 0.310086*cos(3.07144*x_1 - 1.4008) + 0.337637) - 1.21347`

### task=combo seed=14

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=2.919541e-04, r2=0.999473
- Variant formula overview:
  - baseline: symbolic_s=7.131790e+00, imitation_mse=4.338077e-03, target_mse=4.314376e-03, formula_export_success=True
  - icbr_full: symbolic_s=4.563922e-01, imitation_mse=4.379413e-03, target_mse=4.333870e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=3.851439e-01, imitation_mse=4.299003e-03, target_mse=4.275463e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=6.451651e-01, imitation_mse=4.379413e-03, target_mse=4.333870e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=6.821879e-01, imitation_mse=1.182392e-02, target_mse=1.187212e-02, formula_export_success=True
- baseline formula (display, rounded):
  - `-4.72653*atan(0.132244*cos(3.41128*x_1 + 1.60776) - 1.98956 + 2.4147*exp(-0.0835902*(-x_2 - 0.00304373)**2)) + 0.861984*atan(0.325192*cos(1.40976*x_2 + 9.40048) + 1.55984 - 1.47851*exp(-2.59983*(-x_1 - 0.530935)**2)) + 1.536`
- icbr_full formula (display, rounded):
  - `-0.473407*(-0.188503*(0.0199999 - x_2)**2 + 0.544229 + exp(-2.56*(-x_1 - 0.53125)**2))**2 + 5.57753*tanh(0.113649*cos(3.4*x_1 - 1.55) + 1.50563 - 1.93843*exp(-0.09*(x_2 - 7.94729e-7)**2)) + 2.82085`
- icbr_no_replay formula (display, rounded):
  - `5.57753*tanh(0.11383*sin(3.4*x_1 + 0.0500002) - 0.709767*cos(0.7*x_2 + 2.38419e-7) + 0.277221) - 0.880423*atan(0.28854*sin(1.5*x_2 + 1.55) - 1.52797 + 1.45754*exp(-2.56*(-x_1 - 0.53125)**2)) + 1.89187`
- icbr_no_shared formula (display, rounded):
  - `-0.473407*(-0.188503*(0.0199999 - x_2)**2 + 0.544229 + exp(-2.56*(-x_1 - 0.53125)**2))**2 + 5.57753*tanh(0.113649*cos(3.4*x_1 - 1.55) + 1.50563 - 1.93843*exp(-0.09*(x_2 - 7.94729e-7)**2)) + 2.82085`
- icbr_refit_commit formula (display, rounded):
  - `-0.472933*(-0.188016*(0.0256126 - x_2)**2 + 0.524931 + exp(-2.28215*(-x_1 - 0.53131)**2))**2 - 13.4574*tanh(-0.0968466*(-x_2 - 5.65308e-5)**2 + 0.0586816*sin(3.11912*x_1 + 3.30972) + 0.74889) + 9.0808`

### task=combo seed=15

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=6.479074e-04, r2=0.998847
- Variant formula overview:
  - baseline: symbolic_s=7.031092e+00, imitation_mse=9.143051e-04, target_mse=5.599701e-04, formula_export_success=True
  - icbr_full: symbolic_s=4.649757e-01, imitation_mse=8.021651e-04, target_mse=4.290225e-04, formula_export_success=True
  - icbr_no_replay: symbolic_s=3.774250e-01, imitation_mse=8.535494e-04, target_mse=4.807302e-04, formula_export_success=True
  - icbr_no_shared: symbolic_s=6.420404e-01, imitation_mse=8.021651e-04, target_mse=4.290225e-04, formula_export_success=True
  - icbr_refit_commit: symbolic_s=6.997017e-01, imitation_mse=2.176586e-02, target_mse=2.175470e-02, formula_export_success=True
- baseline formula (display, rounded):
  - `1.86607*tan(0.269956*(0.00884719 - x_2)**2 + 0.43947*cos(2.9404*x_1 - 1.56848) - 0.101812) - 0.712358*asin(0.187393*cos(4.0376*x_1 - 4.80488) - 7.46305 + 8.00244*exp(-0.0696959*(-x_2 - 0.0145454)**2)) + 0.621467`
- icbr_full formula (display, rounded):
  - `2.0411*tan(0.249024*(0.011111 - x_2)**2 + 0.406155*sin(2.95*x_1 + 2.38419e-7) + 3.05061) - 0.977292*atanh(-0.394271*(-x_2 - 0.0142858)**2 + 0.136095*cos(4.05*x_1 + 1.5) + 0.396508) + 0.620165`
- icbr_no_replay formula (display, rounded):
  - `2.0411*tan(0.249024*(0.011111 - x_2)**2 + 0.406155*sin(2.95*x_1 + 2.38419e-7) + 3.05061) - 0.730685*asin(-0.525695*(-x_2 - 0.0142858)**2 + 0.181749*sin(4.05*x_1 + 3.05) + 0.54608) + 0.631994`
- icbr_no_shared formula (display, rounded):
  - `2.0411*tan(0.249024*(0.011111 - x_2)**2 + 0.406155*sin(2.95*x_1 + 2.38419e-7) + 3.05061) - 0.977292*atanh(-0.394271*(-x_2 - 0.0142858)**2 + 0.136095*cos(4.05*x_1 + 1.5) + 0.396508) + 0.620165`
- icbr_refit_commit formula (display, rounded):
  - `-1.99983*atanh(-0.253217*(3.71292e-5 - x_2)**2 + 0.386762*sin(2.66276*x_1 - 3.20216) + 0.0763109) + 0.97404*atanh(-2.67511*cos(0.54984*x_2) + 0.101027*cos(3.43504*x_1 + 4.79508) + 2.28398) + 0.596157`

### task=combo seed=16

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=2.204299e-04, r2=0.999646
- Variant formula overview:
  - baseline: symbolic_s=7.074986e+00, imitation_mse=8.970798e-04, target_mse=7.336377e-04, formula_export_success=True
  - icbr_full: symbolic_s=4.499601e-01, imitation_mse=7.872159e-04, target_mse=6.176241e-04, formula_export_success=True
  - icbr_no_replay: symbolic_s=3.829299e-01, imitation_mse=8.476292e-04, target_mse=6.917704e-04, formula_export_success=True
  - icbr_no_shared: symbolic_s=6.556421e-01, imitation_mse=7.974445e-04, target_mse=6.298075e-04, formula_export_success=True
  - icbr_refit_commit: symbolic_s=7.172018e-01, imitation_mse=1.270912e-02, target_mse=1.259209e-02, formula_export_success=True
- baseline formula (display, rounded):
  - `1.14811*atanh(0.405915*sin(3.4572*x_1 + 6.39072) - 10.8887*cos(0.28432*x_2 + 0.00399999) + 10.5746) + 1.75528 - 1.85344*exp(-0.584794*(-0.286322*sin(1.91048*x_2 - 1.5952) - 0.45355*cos(2.78832*x_1 + 4.58432) - 1)**2)`
- icbr_full formula (display, rounded):
  - `1.04795*tan(0.47608*(-x_2 - 0.0125)**2 + 0.44102*cos(3.45*x_1 - 1.45) - 3.474) - 1.04865*tanh(0.337688*sin(1.9*x_2 + 1.55) + 0.53101*cos(2.8*x_1 + 1.45) - 0.0368016) + 0.672316`
- icbr_no_replay formula (display, rounded):
  - `1.12149*atanh(0.446325*(-x_2 - 0.0125)**2 + 0.413457*cos(3.45*x_1 - 1.45) - 0.316251) + 1.78601 - 1.90695*exp(-0.581737*(-0.279628*sin(1.9*x_2 + 1.55) - 0.439711*cos(2.8*x_1 + 1.45) + 1)**2)`
- icbr_no_shared formula (display, rounded):
  - `1.04795*tan(0.475941*(-x_2 - 0.0140846)**2 + 0.44102*cos(3.45*x_1 - 1.45) - 3.4739) - 1.04865*tanh(0.337688*sin(1.9*x_2 + 1.55) + 0.53101*cos(2.8*x_1 + 1.45) - 0.0368016) + 0.672316`
- icbr_refit_commit formula (display, rounded):
  - `-0.949377*asin(0.438104*cos(3.12564*x_1 + 1.81024) + 4.8837*cos(0.47208*x_2 + 4.00001e-5) - 4.47091) - 0.333558 + 1.76619*exp(-0.50125*(0.316986*sin(1.9554*x_2 - 4.71244) + 0.506752*cos(2.65084*x_1 - 4.89848) + 1)**2)`

### task=combo seed=17

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.832366e-04, r2=0.999693
- Variant formula overview:
  - baseline: symbolic_s=7.018786e+00, imitation_mse=6.151200e-04, target_mse=5.963268e-04, formula_export_success=True
  - icbr_full: symbolic_s=4.482297e-01, imitation_mse=5.431079e-04, target_mse=5.076180e-04, formula_export_success=True
  - icbr_no_replay: symbolic_s=3.761996e-01, imitation_mse=5.840736e-04, target_mse=5.459391e-04, formula_export_success=True
  - icbr_no_shared: symbolic_s=7.031591e-01, imitation_mse=5.431079e-04, target_mse=5.076181e-04, formula_export_success=True
  - icbr_refit_commit: symbolic_s=7.087282e-01, imitation_mse=1.390771e-02, target_mse=1.433066e-02, formula_export_success=True
- baseline formula (display, rounded):
  - `-1.43197*tan(0.266866*cos(3.57168*x_1 + 7.98792) + 0.336077*cos(1.7112*x_2 - 0.00432001) - 6.41779) + 1.84219 - 2.45844*exp(-0.46501*(0.304755*(-x_2 - 0.00227313)**2 + 0.459694*sin(2.83864*x_1 - 6.38512) + 1)**2)`
- icbr_full formula (display, rounded):
  - `1.13189*asin(0.339143*cos(3.55*x_1 - 1.45) - 0.432564*cos(1.7*x_2 + 2.38419e-7) + 0.189954) + 1.88789 - 2.56522*exp(-0.467265*(0.28981*(-x_2 - 8.22133e-8)**2 - 0.438013*sin(2.85*x_1 + 3.05) + 1)**2)`
- icbr_no_replay formula (display, rounded):
  - `-1.40345*tan(0.271223*sin(3.55*x_1 - 3.0) + 0.346051*cos(1.7*x_2 + 2.38419e-7) - 3.2826) + 1.90495 - 2.56522*exp(-0.467265*(0.28981*(-x_2 - 8.22133e-8)**2 - 0.438013*sin(2.85*x_1 + 3.05) + 1)**2)`
- icbr_no_shared formula (display, rounded):
  - `1.13189*asin(0.339143*cos(3.55*x_1 - 1.45) - 0.432564*cos(1.7*x_2 + 2.38419e-7) + 0.189954) + 1.88789 - 2.56522*exp(-0.467265*(0.28981*(-x_2 - 8.51495e-8)**2 - 0.438013*sin(2.85*x_1 + 3.05) + 1)**2)`
- icbr_refit_commit formula (display, rounded):
  - `1.12945*asin(0.287695*sin(3.20692*x_1 + 0.27928) + 0.364429*cos(1.9*x_2 + 3.12) + 0.11491) - 1.26885 + 2.70934*exp(-0.551188*(0.251784*(-x_2 - 2.54308e-5)**2 + 0.363004*sin(2.64408*x_1 - 0.18888) - 1)**2)`

### task=combo seed=18

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.917077e-04, r2=0.999670
- Variant formula overview:
  - baseline: symbolic_s=7.141539e+00, imitation_mse=7.364269e-04, target_mse=6.222578e-04, formula_export_success=True
  - icbr_full: symbolic_s=4.479842e-01, imitation_mse=5.994271e-04, target_mse=4.594193e-04, formula_export_success=True
  - icbr_no_replay: symbolic_s=3.764794e-01, imitation_mse=7.774571e-04, target_mse=6.709796e-04, formula_export_success=True
  - icbr_no_shared: symbolic_s=6.477404e-01, imitation_mse=5.994271e-04, target_mse=4.594193e-04, formula_export_success=True
  - icbr_refit_commit: symbolic_s=7.153691e-01, imitation_mse=1.642475e-02, target_mse=1.640903e-02, formula_export_success=True
- baseline formula (display, rounded):
  - `2.04091*tan(0.132838*cos(3.44008*x_1 - 1.5844) + 9.90601 - 0.32219*exp(-1.18079*(-x_2 - 0.0658175)**2)) + 2.95873*atan(0.167913*(0.0697393 - x_2)**2 - 0.24987*cos(3.02528*x_1 + 1.57408) + 0.091361) - 0.621795`
- icbr_full formula (display, rounded):
  - `2.3497*cos(0.211066*(0.07 - x_2)**2 + 0.312866*sin(3.0*x_1 + 2.38419e-7) + 4.84835) + 2.32707*asin(0.109346*sin(3.45*x_1 + 2.38419e-7) + 0.723235 - 0.314864*exp(-0.9025*(-x_2 - 0.0526318)**2)) - 1.31731`
- icbr_no_replay formula (display, rounded):
  - `3.24067*tanh(0.153503*(0.07 - x_2)**2 + 0.227539*sin(3.0*x_1 + 2.38419e-7) + 0.107894) - 2.07817*atanh(0.125587*sin(2.4*x_2 - 4.55) + 0.131108*cos(3.45*x_1 + 1.55) - 0.273328) - 0.680745`
- icbr_no_shared formula (display, rounded):
  - `2.3497*cos(0.211066*(x_2 - 0.07)**2 + 0.312866*sin(3.0*x_1 + 2.38419e-7) + 4.84835) + 2.32707*asin(0.109346*sin(3.45*x_1 + 2.38419e-7) + 0.723235 - 0.314864*exp(-0.9025*(-x_2 - 0.0526318)**2)) - 1.31731`
- icbr_refit_commit formula (display, rounded):
  - `3.13625*tanh(0.151734*(0.0615459 - x_2)**2 + 0.214593*sin(2.74796*x_1 - 0.0977599) + 0.0972573) + 2.26553*acos(0.0961315*sin(3.05272*x_1 + 3.304) - 0.66127 + 0.270829*exp(-1.21*(-x_2 - 0.0527272)**2)) - 4.79054`

### task=combo seed=19

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=8.476962e-05, r2=0.999856
- Variant formula overview:
  - baseline: symbolic_s=6.982343e+00, imitation_mse=3.147855e-04, target_mse=2.982836e-04, formula_export_success=True
  - icbr_full: symbolic_s=4.862506e-01, imitation_mse=2.211468e-04, target_mse=1.907786e-04, formula_export_success=True
  - icbr_no_replay: symbolic_s=3.911837e-01, imitation_mse=3.570108e-04, target_mse=3.476196e-04, formula_export_success=True
  - icbr_no_shared: symbolic_s=6.516222e-01, imitation_mse=2.211468e-04, target_mse=1.907786e-04, formula_export_success=True
  - icbr_refit_commit: symbolic_s=6.794405e-01, imitation_mse=1.859284e-02, target_mse=1.875773e-02, formula_export_success=True
- baseline formula (display, rounded):
  - `0.896378*atan(0.690133*(0.00300677 - x_2)**2 + 0.618425*cos(3.14904*x_1 - 1.59992) - 0.808323) - 1.25746*atan(0.596864*cos(3.15192*x_1 + 1.5904) + 2.95069*cos(0.61224*x_2 + 0.00104) - 3.23831) + 0.264022`
- icbr_full formula (display, rounded):
  - `2.38417*tanh(0.324532*(-x_2 - 5.96046e-8)**2 + 0.359991*cos(3.15*x_1 - 1.55) + 0.513731) - 0.913046*atan(-0.675808*(-x_2 - 5.29819e-8)**2 + 0.60529*cos(3.15*x_1 + 1.55) + 0.800306) - 0.497596`
- icbr_no_replay formula (display, rounded):
  - `-0.913046*atan(-0.675808*(-x_2 - 5.29819e-8)**2 + 0.60529*cos(3.15*x_1 + 1.55) + 0.800306) + 1.20229*atan(0.623984*cos(3.15*x_1 - 1.55) - 3.20819*cos(0.6*x_2 + 2.38419e-7) + 3.48043) + 0.304364`
- icbr_no_shared formula (display, rounded):
  - `2.38417*tanh(0.324532*(-x_2 - 5.96046e-8)**2 + 0.359991*cos(3.15*x_1 - 1.55) + 0.513731) - 0.913046*atan(-0.675808*(-x_2 - 5.29819e-8)**2 + 0.60529*cos(3.15*x_1 + 1.55) + 0.800306) - 0.497596`
- icbr_refit_commit formula (display, rounded):
  - `1.35735*atan(0.488859*(-x_2 - 0.000183273)**2 + 0.394342*cos(2.86824*x_1 + 4.79656) - 0.859963) + 2.22242 - 5.3386*exp(-1.4516*(0.16521*(-x_2 - 0.000303136)**2 - 0.166319*sin(2.873*x_1 - 3.01692) + 1)**2)`

### task=combo seed=20

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.708706e-04, r2=0.999717
- Variant formula overview:
  - baseline: symbolic_s=6.993968e+00, imitation_mse=3.973580e-04, target_mse=3.970659e-04, formula_export_success=True
  - icbr_full: symbolic_s=4.481062e-01, imitation_mse=4.012697e-04, target_mse=3.950715e-04, formula_export_success=True
  - icbr_no_replay: symbolic_s=3.738255e-01, imitation_mse=4.479366e-04, target_mse=4.519469e-04, formula_export_success=True
  - icbr_no_shared: symbolic_s=6.636052e-01, imitation_mse=4.012697e-04, target_mse=3.950715e-04, formula_export_success=True
  - icbr_refit_commit: symbolic_s=6.674259e-01, imitation_mse=1.346217e-02, target_mse=1.345607e-02, formula_export_success=True
- baseline formula (display, rounded):
  - `-0.760387*tan(0.515752*cos(3.22192*x_1 + 1.6016) - 0.549159 + 0.79641*exp(-0.933002*(0.00712275 - x_2)**2)) - 0.602351 + 1.85001*exp(-0.880816*(0.421183*(-x_2 - 0.00442262)**2 - 0.422286*sin(3.08832*x_1 + 9.40704) - 1)**2)`
- icbr_full formula (display, rounded):
  - `0.771009*tan(0.508674*cos(3.2*x_1 - 1.55) - 0.308047*cos(2.15*x_2 + 2.38419e-7) + 3.21103) - 0.597899 + 1.82622*exp(-0.880351*(-0.428053*(-x_2 - 4.79233e-8)**2 + 0.430035*cos(3.1*x_1 + 1.55) + 1)**2)`
- icbr_no_replay formula (display, rounded):
  - `0.771009*tan(-0.298673*sin(2.2*x_2 + 1.55) + 0.508674*cos(3.2*x_1 - 1.55) + 3.201) - 0.597899 + 1.82622*exp(-0.880351*(-0.428053*(-x_2 - 4.79233e-8)**2 + 0.430035*cos(3.1*x_1 + 1.55) + 1)**2)`
- icbr_no_shared formula (display, rounded):
  - `0.771009*tan(0.508674*cos(3.2*x_1 - 1.55) - 0.308047*cos(2.15*x_2 + 2.38419e-7) + 3.21103) - 0.597899 + 1.82622*exp(-0.880351*(-0.428053*(-x_2 - 4.79233e-8)**2 + 0.430035*cos(3.1*x_1 + 1.55) + 1)**2)`
- icbr_refit_commit formula (display, rounded):
  - `0.848883*cos(0.728712*(7.03067e-5 - x_2)**2 + 0.675413*cos(2.82524*x_1 + 4.6074) - 1.90736) - 1.12968*tan(0.330262*sin(2.89752*x_1 + 3.29816) + 0.22188*sin(2.15308*x_2 - 4.71228) + 3.10531) + 0.4718`

### task=trig_interaction seed=1

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=2.199448e-03, r2=0.997009
- Variant formula overview:
  - baseline: symbolic_s=1.853457e+01, imitation_mse=3.036956e-03, target_mse=5.261504e-03, formula_export_success=True
  - icbr_full: symbolic_s=1.208718e+00, imitation_mse=2.072520e-03, target_mse=4.232149e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=7.959738e-01, imitation_mse=2.908568e-03, target_mse=5.000852e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.954480e+00, imitation_mse=2.072517e-03, target_mse=4.232141e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.775486e+00, imitation_mse=7.767259e-02, target_mse=7.937106e-02, formula_export_success=True
- baseline formula (display, rounded):
  - `-0.931138*atan(0.275526*cos(3.3608*x_1 + 7.78976) + 0.639957 - 1.15355*exp(-2.39308*(-x_2 - 0.00418886)**2)) + 0.410127*atan(0.397729*cos(4.04904*x_1 - 1.77344) - 0.161132*cos(2.54024*x_3 + 5.63224) - 1.27886 + 0.529288*exp(-1.96011*(0.0342847 - x_2)**2)) + 0.00333947 - 1.51574*exp(-1.77241*(-0.583214*atan(0.79256*x_3 - 0.70824) + 0.0233858 - 0.03198*exp(-6.76*(-x_2 - 0.0476923)**2) - exp(-0.978042*(0.5652 - x_1)**2))**2) + 1.75317*exp(-1.4024*(0.0423792*(0.0267339 - x_2)**4 + 0.478335*atan(1.13136*x_3 - 0.82536) - 0.0856049 + exp(-1.24724*(-x_1 - 0.556375)**2))**2)`
- icbr_full formula (display, rounded):
  - `-1.50103 + 1.67515*exp(-1.55334*(-0.493369*atan(1.1*x_3 - 0.85) - 0.341749 + 0.421428*exp(-0.09*(x_2 - 7.94729e-7)**2) - exp(-1.21*(-x_1 - 0.545455)**2))**2) - 1.58459*exp(-0.402015*(-exp(0.6*x_3) + 0.0314722*sin(4.1*x_2 - 1.45) + 0.339273*Abs(3.95*x_1 - 2.25) - 0.449066)**2) + 1.78002*exp(-1.21136*(0.149964*cos(3.35*x_1 + 1.5) + 1 - 0.628136*exp(-2.4025*(-x_2 - 1.53818e-7)**2))**2) + 0.28547/(-0.0581954*cos(4.05*x_1 + 4.5) + 0.0330067*cos(2.9*x_2 + 3.05) - 0.0238281*cos(2.5*x_3 + 2.5) + 1)**5`
- icbr_no_replay formula (display, rounded):
  - `-0.930936*atan(0.501347*sin(3.15*x_2 - 1.55) + 0.275088*cos(3.35*x_1 + 1.5) - 0.00733132) + 0.420415*atan(0.39208*cos(4.05*x_1 + 4.5) + 0.160537*cos(2.5*x_3 + 2.5) - 1.28361 + 0.522167*exp(-1.96*(0.0357141 - x_2)**2)) + 0.17083 - 1.58459*exp(-1.93261*(-tanh(0.5*x_3 - 0.8) - 0.301628 - 0.0290661*exp(-6.5025*(-x_2 - 0.0392158)**2) - 0.926828*exp(-0.9025*(0.578947 - x_1)**2))**2) + 1.67515*exp(-1.55334*(-0.0415244*(0.0299999 - x_2)**4 - 0.493369*atan(1.1*x_3 - 0.85) + 0.0759437 - exp(-1.21*(-x_1 - 0.545455)**2))**2)`
- icbr_no_shared formula (display, rounded):
  - `-1.50102 + 1.67515*exp(-1.55334*(0.493369*atan(1.1*x_3 - 0.85) + 0.341749 - 0.421428*exp(-0.09*(x_2 - 7.94729e-7)**2) + exp(-1.21*(x_1 + 0.545455)**2))**2) - 1.58459*exp(-0.402015*(-exp(0.6*x_3) + 0.0314722*sin(4.1*x_2 - 1.45) + 0.339273*Abs(3.95*x_1 - 2.25) - 0.449066)**2) + 1.78002*exp(-1.21136*(0.149964*cos(3.35*x_1 + 1.5) + 1 - 0.628136*exp(-2.4025*(-x_2 - 1.53818e-7)**2))**2) + 0.28547/(-0.0581954*cos(4.05*x_1 + 4.5) + 0.0330067*cos(2.9*x_2 + 3.05) - 0.0238281*cos(2.5*x_3 + 2.5) + 1)**5`
- icbr_refit_commit formula (display, rounded):
  - `21.2772*sin(0.174492*exp(0.59912*x_3) - 0.0156314*cos(1.30002*x_2 + 3.114) - 0.0538333*Abs(4.00208*x_1 - 2.54204) + 4.78921) - 0.816753*cos(-4.27708*sin(0.8*x_2 - 4.704) + 0.214049*cos(2.56324*x_1 - 4.80336) + 2.24507) + 0.383387*atan(0.268255*(0.193854 - x_3)**2 - 8.1086*sin(0.15844*x_1 + 1.43948) + 1.4648 + 5.7342*exp(-0.0853574*(0.0476451 - x_2)**2)) - 14.277 + 35.7488*exp(-0.031762*(0.220382*(-0.859695*x_3 - 1)**2 + 0.615293 - exp(-1.72975*(0.819799 - x_1)**2) - 0.202664*exp(-0.227109*(0.000251805 - x_2)**2))**2)`

### task=trig_interaction seed=2

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.979663e-02, r2=0.972177
- Variant formula overview:
  - baseline: symbolic_s=1.636848e+01, imitation_mse=1.853709e-03, target_mse=2.300273e-02, formula_export_success=True
  - icbr_full: symbolic_s=1.112492e+00, imitation_mse=1.409377e-03, target_mse=2.114112e-02, formula_export_success=True
  - icbr_no_replay: symbolic_s=7.240387e-01, imitation_mse=1.648381e-03, target_mse=2.158880e-02, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.733553e+00, imitation_mse=1.408856e-03, target_mse=2.114398e-02, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.659011e+00, imitation_mse=1.036508e-01, target_mse=9.743717e-02, formula_export_success=True
- baseline formula (display, rounded):
  - `-4.28366*exp(0.0780634*sin(3.30696*x_1 - 3.39928) - 0.0208572*atan(3.32144*x_3 - 2.7428) - 0.122423*exp(-1.65915*(-x_2 - 0.0637848)**2)) + 0.365742*sin(0.782791*sin(3.8392*x_1 + 9.01056) + 9.54848 + 1.59891*exp(-0.559623*(1 - 0.957545*x_3)**2)) - 2.29558*tan(0.170304*sin(3.24232*x_1 - 9.60536) + 0.341509*cos(0.89992*x_3 + 6.7492) - 3.32737 - 0.286109*exp(-2.88049*(0.0361065 - x_2)**2)) - 1.86035 + 6.45837*exp(-0.313423*(-0.86108*atan(0.62584*x_3 - 0.18936) + 0.177149 - exp(-1.13789*(-x_1 - 0.718989)**2))**2)`
- icbr_full formula (display, rounded):
  - `-2.64022*(0.0393944*sin(3.3*x_1 - 3.4) - 0.0264245*sin(2.65*x_2 - 4.55) - 0.0104174*atan(3.35*x_3 - 2.75) + 1)**3 - 13.6324*sqrt(-0.0468455*sin(3.3*x_2 + 1.45) - 0.0621598*cos(3.25*x_1 + 4.55) + 0.13535*cos(0.85*x_3 + 0.45) + 1) - 2.4878*sin(0.590318*cos(1.9*x_1 + 1.45) - 2.19962 + 1.77084*exp(-0.722499*(1 - 0.529412*x_3)**2)) + 0.351725*cos(-0.762326*sin(1.3*x_3 + 0.0500002) + 0.80457*cos(3.85*x_1 - 2.0) + 3.71012) + 15.2495`
- icbr_no_replay formula (display, rounded):
  - `3.1851*(-0.0195869*sin(3.3*x_1 - 3.4) + 0.0131383*sin(2.65*x_2 - 4.55) + 0.00517951*atan(3.35*x_3 - 2.75) - 1)**5 + 0.351725*cos(0.806607*sin(3.85*x_1 - 3.55) + 0.762432*cos(1.3*x_3 - 1.55) - 3.69613) - 2.4573*tan(0.159695*sin(3.25*x_1 + 2.95) + 0.348052*cos(0.85*x_3 + 0.45) - 0.205439 - 0.267659*exp(-2.89*(0.0294116 - x_2)**2)) - 1.94674 + 5.71296*exp(-0.711079*(0.332824*sin(1.9*x_1 + 3.05) - 0.350804 + exp(-0.722499*(1 - 0.529412*x_3)**2))**2)`
- icbr_no_shared formula (display, rounded):
  - `-2.64022*(0.0393944*sin(3.3*x_1 - 3.4) - 0.0264245*sin(2.65*x_2 - 4.55) - 0.0104174*atan(3.35*x_3 - 2.75) + 1)**3 - 13.809*sqrt(-0.0462165*sin(3.3*x_2 + 1.45) - 0.0613251*cos(3.25*x_1 + 4.55) + 0.133533*cos(0.85*x_3 + 0.45) + 1) - 2.4878*sin(0.590318*cos(1.9*x_1 + 1.45) - 2.19962 + 1.77084*exp(-0.722499*(1 - 0.529412*x_3)**2)) + 0.351725*cos(-0.762326*sin(1.3*x_3 + 0.0500002) + 0.80457*cos(3.85*x_1 - 2.0) + 3.71012) + 15.4259`
- icbr_refit_commit formula (display, rounded):
  - `-15.7585*sqrt(-0.0335081*sin(2.56004*x_1 - 0.0959599) + 0.939071*sin(0.41396*x_2 + 4.69804) - 0.759985*sin(0.27696*x_3 + 4.88128) + 1) - 11.5522*(-0.295894*sin(0.41792*x_2 + 1.596) + 0.0132882*cos(2.53116*x_1 + 1.406) + 1 - 0.0625522*exp(-4.55088*(1 - 0.363928*x_3)**2))**4 - 0.266617*tanh(0.59575*sin(2.47468*x_1 - 3.40604) + 1.2245*sin(1.24036*x_3 - 0.00016) + 1.20652) + 16.1422 + 1.88332*exp(-15.472*(-sin(0.2272*x_3 - 0.7178) - 0.166212*cos(1.7316*x_1 + 1.5022) - 0.729125)**2)`

### task=trig_interaction seed=3

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=8.604269e-03, r2=0.988900
- Variant formula overview:
  - baseline: symbolic_s=1.528752e+01, imitation_mse=1.218114e-03, target_mse=1.074634e-02, formula_export_success=True
  - icbr_full: symbolic_s=1.094302e+00, imitation_mse=1.296523e-03, target_mse=1.009823e-02, formula_export_success=True
  - icbr_no_replay: symbolic_s=7.168285e-01, imitation_mse=1.316618e-03, target_mse=1.038506e-02, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.663432e+00, imitation_mse=1.296523e-03, target_mse=1.009823e-02, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.594225e+00, imitation_mse=3.647404e-02, target_mse=4.081279e-02, formula_export_success=True
- baseline formula (display, rounded):
  - `1.51347*cos(0.213171*cos(3.30464*x_1 - 1.5948) + 0.0153588*cos(3.73208*x_3 + 5.60776) + 4.37823 + 0.61538*exp(-2.69774*(-x_2 - 0.00316594)**2)) - 0.29718*tanh(0.222541*cos(4.14184*x_1 + 1.7952) + 0.645955 - 1.0467*exp(-1.09914*(0.040061 - x_2)**2)) + 1.36364 + 1.21982*exp(-1.02298*(tan(0.14432*x_3 - 8.43808) - 0.0956264*Abs(9.98904*x_1 + 6.0) - 0.449061)**2) - 2.67631*exp(-0.343454*(0.723086*sin(2.01208*x_1 - 9.00024) - 0.981669*atan(0.884*x_3 - 1.00008) - 1)**2)`
- icbr_full formula (display, rounded):
  - `1.00043*sin(0.976991*cos(2.0*x_1 + 2.0) - 3.87477*tanh(0.5*x_3 - 1.2) + 1.17697) - 1.52429*cos(0.271074*sin(3.25*x_2 - 1.55) + 0.211495*cos(3.3*x_1 + 1.55) + 0.0152919*cos(3.75*x_3 + 2.45) + 4.72213) + 0.00865224 + 1.24234*exp(-1.16838*(tan(0.25*x_3 + 3.85) - 0.182299*Abs(4.825*x_1 + 2.9) + 0.118408)**2) - 0.558722*exp(-0.510473*(0.190545*sin(4.15*x_1 - 2.9) + 0.357135*cos(2.3*x_2 + 3.05) - 1)**2)`
- icbr_no_replay formula (display, rounded):
  - `0.224724*cos(-0.292952*cos(4.15*x_1 - 4.5) + 3.86774 + 1.37071*exp(-1.1025*(0.0476188 - x_2)**2)) - 0.527479 + 3.55326*exp(-0.767529*(0.00870157*sin(3.75*x_3 + 0.9) - 0.120704*cos(3.3*x_1 + 1.55) - 1 + 0.347574*exp(-2.7225*(-x_2 - 1.44496e-7)**2))**2) + 1.24234*exp(-20.1143*(-0.0439363*Abs(4.825*x_1 + 2.9) + 0.755994*atan(0.5*x_3 - 1.6) + 1)**2) - 2.94776*exp(-2.492*(-0.252142*cos(2.0*x_1 + 2.0) + tanh(0.5*x_3 - 1.2) + 0.912743)**2)`
- icbr_no_shared formula (display, rounded):
  - `1.00043*sin(0.976991*cos(2.0*x_1 + 2.0) - 3.87477*tanh(0.5*x_3 - 1.2) + 1.17697) - 1.52429*cos(0.271074*sin(3.25*x_2 - 1.55) + 0.211495*cos(3.3*x_1 + 1.55) + 0.0152919*cos(3.75*x_3 + 2.45) + 4.72213) + 0.00865224 + 1.24234*exp(-1.16838*(tan(0.25*x_3 + 3.85) - 0.182299*Abs(4.825*x_1 + 2.9) + 0.118408)**2) - 0.558722*exp(-0.510473*(-0.190545*sin(4.15*x_1 - 2.9) - 0.357135*cos(2.3*x_2 + 3.05) + 1)**2)`
- icbr_refit_commit formula (display, rounded):
  - `-0.648166*sin(-1.03761*exp(0.80624*x_3) + 0.472186*Abs(4.5616*x_1 - 2.58092) + 0.476201) + 0.239606*cos(7.37054*sin(0.2244*x_1 - 1.51632) + 6.72202*sin(0.522*x_2 - 1.59792) + 15.1256) + 1.97764*tanh(1.58693*sin(0.8*x_2 - 4.704) + 0.121352*cos(2.6122*x_1 - 1.59816) - 1.55525 + 0.131837*exp(-0.198987*(-x_3 - 0.0312051)**2)) - 0.262248*Abs(-0.930426*Abs(2.8692*x_1 + 1.94696) + 18.6909*atan(0.71192*x_3 - 2.86324) + 26.3171) + 0.591847`

### task=trig_interaction seed=4

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=2.289809e-02, r2=0.969829
- Variant formula overview:
  - baseline: symbolic_s=1.512824e+01, imitation_mse=3.237507e-03, target_mse=2.585588e-02, formula_export_success=True
  - icbr_full: symbolic_s=1.041940e+00, imitation_mse=3.236993e-03, target_mse=2.564781e-02, formula_export_success=True
  - icbr_no_replay: symbolic_s=6.836445e-01, imitation_mse=3.443655e-03, target_mse=2.624240e-02, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.572867e+00, imitation_mse=3.236993e-03, target_mse=2.564781e-02, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.531419e+00, imitation_mse=9.055908e-02, target_mse=1.274508e-01, formula_export_success=True
- baseline formula (display, rounded):
  - `-0.477311*cos(2.24449*tan(0.52248*x_3 + 9.62248) - 1.21097*atan(2.45088*x_1 + 0.59208) + 2.88174) + 1.46514*tan(0.086696*(-x_3 - 0.0768071)**2 + 0.25855*sin(2.91048*x_1 + 6.18952) + 0.211433*cos(3.0808*x_2 - 0.00328001) + 3.26625) - 0.671593*atan(0.49765*sin(3.31704*x_1 - 3.1924) + 0.281353*cos(3.28144*x_2 - 9.38712) - 0.296233) - 1.25301 + 1.15939*exp(-3.21251*(-0.350865*cos(0.85984*x_3 - 7.43688) + 0.385114 - exp(-1.35099*(-x_1 - 0.480418)**2))**2)`
- icbr_full formula (display, rounded):
  - `0.592677*sin(-0.550727*sin(3.3*x_1 - 0.0499997) + 0.312912*sin(3.25*x_2 - 1.55) + 2.79866) + 0.520331*sin(-1.24696*sin(0.85*x_3 + 3.55) + 0.167848 + 3.55792*exp(-1.3225*(x_1 + 0.478261)**2)) - 0.485264*cos(1.19452*atan(2.45*x_1 + 0.6) - 2.58998*atanh(0.45*x_3 + 0.2) + 3.47411) + 1.44256*atanh(0.0877467*(x_3 + 0.0769231)**2 - 0.261189*cos(2.9*x_1 + 1.5) + 0.213353*cos(3.1*x_2 + 2.38419e-7) + 0.117321) - 0.632655`
- icbr_no_replay formula (display, rounded):
  - `-0.592677*sin(0.550727*sin(3.3*x_1 - 0.0499997) + 0.311634*cos(3.3*x_2 + 0.0500002) - 2.79433) - 0.485264*cos(-2.091*tan(0.55*x_3 - 2.95) + 1.19452*atan(2.45*x_1 + 0.6) + 3.35888) + 1.4497*tan(0.0877467*(x_3 + 0.0769231)**2 - 0.26133*sin(2.9*x_1 + 3.05) + 0.213353*cos(3.1*x_2 + 2.38419e-7) + 0.117914) - 1.26829 + 1.16764*exp(-3.1647*(0.353362*cos(0.85*x_3 + 2.0) + 0.395444 - exp(-1.3225*(x_1 + 0.478261)**2))**2)`
- icbr_no_shared formula (display, rounded):
  - `0.592677*sin(-0.550727*sin(3.3*x_1 - 0.0499997) + 0.312912*sin(3.25*x_2 - 1.55) + 2.79866) + 0.520331*sin(-1.24696*sin(0.85*x_3 + 3.55) + 0.167848 + 3.55792*exp(-1.3225*(x_1 + 0.478261)**2)) - 0.485264*cos(1.19452*atan(2.45*x_1 + 0.6) - 2.58998*atanh(0.45*x_3 + 0.2) + 3.47411) + 1.44256*atanh(0.0877467*(x_3 + 0.0769231)**2 - 0.261189*cos(2.9*x_1 + 1.5) + 0.213353*cos(3.1*x_2 + 2.38419e-7) + 0.117321) - 0.632655`
- icbr_refit_commit formula (display, rounded):
  - `-6.18161*(-0.229852*atan(1.62504*x_1 + 0.34124) + atanh(0.12492*x_3 + 0.61) - 0.689093)**2 - 8.93265*sqrt(0.0428605*sin(2.19192*x_1 - 3.21152) - 0.794147*cos(0.46904*x_2 + 0.00592) + 1 + 0.0362647*exp(-0.49*(-x_3 - 0.0799999)**2)) - 1.99043*sin(0.156473*cos(2.19792*x_1 - 1.60804) - 0.344439*cos(1.3*x_2 + 3.116) + 3.65546) + 0.546412*sin(1.04566*atan(0.7984*x_3 + 0.35) + 3.39086 - 2.29874*exp(-2.09728*(0.819749 - x_1)**2)) + 3.39468`

### task=trig_interaction seed=5

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=7.897707e-03, r2=0.989082
- Variant formula overview:
  - baseline: symbolic_s=1.647543e+01, imitation_mse=3.291332e-03, target_mse=1.241291e-02, formula_export_success=True
  - icbr_full: symbolic_s=1.116034e+00, imitation_mse=3.051930e-03, target_mse=1.012703e-02, formula_export_success=True
  - icbr_no_replay: symbolic_s=7.395176e-01, imitation_mse=3.590774e-03, target_mse=1.325338e-02, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.804504e+00, imitation_mse=3.051930e-03, target_mse=1.012702e-02, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.717972e+00, imitation_mse=9.239562e-02, target_mse=1.186043e-01, formula_export_success=True
- baseline formula (display, rounded):
  - `-0.41672*sin(0.135894*Abs(7.4072*x_3 - 6.2408) + 11.266 - 3.8631*exp(-1.45907*(-x_1 - 0.470693)**2)) + 0.100466*Abs(0.298644*(x_3 + 0.0462926)**2 + 5.19369*sin(2.67136*x_1 - 6.40224) - 2.68387*cos(2.81544*x_2 + 3.0108) + 7.16421) - 1.35757 - 2.19577*exp(-1.18541*(0.123177*sin(3.84128*x_1 + 9.1948) + 0.297128*sin(0.66792*x_3 + 7.97264) + 0.121025*cos(3.32136*x_2 + 9.59032) - 1)**2) + 2.05121*exp(-0.379953*((-0.309677*x_3 - 1)**2 - 0.610984*atan(2.7896*x_1 + 0.57888) - 0.924924)**2)`
- icbr_full formula (display, rounded):
  - `0.760795*sin(0.98786*(0.6*x_3 + 1)**(3/2) - 0.405595 + 2.02326*exp(-1.5625*(-x_1 - 0.84)**2)) - 0.417131*cos(-0.616621*Abs(4.875*x_1 + 2.35) + 1.2247*atan(0.9*x_3 + 0.0500002) + 6.10887) - 0.955723*cos(0.259819*sin(3.3*x_2 - 4.55) + 0.273044*sin(1.05*x_3 + 4.9) + 0.263986*cos(3.85*x_1 + 4.5) - 4.3562) + 0.887389*Abs(0.587886*sin(2.65*x_1 + 3.0) + 0.300633*cos(2.85*x_2 + 3.0) - 0.904608 + 0.082507*exp(-0.49*(x_3 + 0.0714282)**2)) - 1.37733`
- icbr_no_replay formula (display, rounded):
  - `0.760795*sin(1.42062*(-0.31*x_3 - 1)**2 - 0.861476*atan(2.85*x_1 + 0.6) + 0.262973) - 0.417131*cos(-0.285611*Abs(3.5*x_3 - 2.95) + 2.75505 + 3.92903*exp(-1.3225*(x_1 + 0.478261)**2)) + 0.887389*Abs(0.0338599*(-x_3 - 0.0444445)**2 + 0.305289*sin(2.8*x_2 + 1.45) - 0.586887*cos(2.65*x_1 + 1.45) + 0.813064) + 1.3304*atan(-0.189888*sin(3.85*x_1 + 2.9) + 0.18707*sin(3.3*x_2 - 4.55) + 0.325578*cos(0.8*x_3 - 3.0) + 0.404531) - 1.40213`
- icbr_no_shared formula (display, rounded):
  - `0.760795*sin(0.98786*(0.6*x_3 + 1)**(3/2) - 0.405595 + 2.02326*exp(-1.5625*(-x_1 - 0.84)**2)) - 0.417131*cos(-0.616621*Abs(4.875*x_1 + 2.35) + 1.2247*atan(0.9*x_3 + 0.0500002) + 6.10887) - 0.955723*cos(0.259819*sin(3.3*x_2 - 4.55) + 0.273044*sin(1.05*x_3 + 4.9) + 0.263986*cos(3.85*x_1 + 4.5) - 4.3562) + 0.887389*Abs(0.587886*sin(2.65*x_1 + 3.0) + 0.300633*cos(2.85*x_2 + 3.0) - 0.904608 + 0.082507*exp(-0.49*(x_3 + 0.0714282)**2)) - 1.37733`
- icbr_refit_commit formula (display, rounded):
  - `1.1343*cos(0.137274*cos(2.42624*x_1 - 4.9092) - 0.0259628*Abs(3.73892*x_3 + 0.90816) + 8.87733 - 7.62072*exp(-0.0676831*(-x_2 - 0.0304428)**2)) + 0.449975*Abs(0.077122*(x_3 - 1.50506e-9)**4 - 1.1094*sin(2.39564*x_1 - 3.20772) - 2.77643*cos(1.00002*x_2 + 3.106) + 2.33215) - 2.67324 - 0.778229*exp(-0.252752*(-0.722338*Abs(4.51592*x_1 + 2.61008) - 0.243695*Abs(4.99244*x_3 - 4.58088) + 1)**2) + 1.01318*exp(-3.57714*(0.389911*(0.602813*x_3 + 1)**(3/2) + 0.209181 - exp(-0.694889*(0.723464 - x_1)**2))**2)`

### task=trig_interaction seed=6

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.063532e-03, r2=0.998652
- Variant formula overview:
  - baseline: symbolic_s=1.864288e+01, imitation_mse=5.184736e-03, target_mse=6.641119e-03, formula_export_success=True
  - icbr_full: symbolic_s=1.241668e+00, imitation_mse=3.495793e-03, target_mse=4.746199e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=8.046693e-01, imitation_mse=6.133396e-03, target_mse=7.419022e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.963405e+00, imitation_mse=3.499322e-03, target_mse=4.751226e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.880608e+00, imitation_mse=1.078258e-01, target_mse=1.099510e-01, formula_export_success=True
- baseline formula (display, rounded):
  - `-1.08225*(0.0733413*(-x_2 - 0.00847096)**2 + 0.610908*cos(0.67808*x_3 - 2.1264) - 0.176071 + exp(-0.970619*(-x_1 - 0.785627)**2))**2 + 2.9667*sin(0.186544*cos(4.68216*x_1 - 8.18744) + 0.967472*atan(0.62376*x_3 - 1.0216) + 1.68472 + 0.231689*exp(-2.21867*(0.00870079 - x_2)**2)) + 0.697502*atan(0.278553*(-x_3 - 0.113458)**2 + 0.633415*cos(3.17816*x_1 - 1.79168) - 1.46662 + 1.43526*exp(-2.13113*(-x_2 - 0.00783647)**2)) - 4.41936 + 2.80815*exp(-0.738879*(-0.0537176*cos(3.1524*x_2 - 9.4088) - 0.517555*atan(0.80864*x_3 + 0.58304) + 0.473359 - exp(-0.950703*(-x_1 - 0.648507)**2))**2)`
- icbr_full formula (display, rounded):
  - `-1.1223*(0.0787009*(-x_2 - 0.0111112)**4 - 0.852253 + exp(-0.9025*(-x_1 - 0.789474)**2) + 0.944004*exp(-1.0*(1 - 0.5*x_3)**2))**2 - 0.401437*(-0.844327*sin(1.9*x_1 - 3.45) - 0.101677*sin(3.15*x_2 - 1.55) - atan(0.8*x_3 + 0.6) - 0.174082)**2 - 2.69261*(-0.129935*sin(4.7*x_1 - 3.45) - 1 + 0.161114*exp(-2.25*(-x_2 - 1.58946e-7)**2) + 0.523551/(1 - 0.195122*x_3)**2)**2 + 0.707316*atan(0.273567*(-x_3 - 0.113402)**2 - 0.623786*sin(3.2*x_1 + 2.9) - 1.45707 + 1.41648*exp(-2.1025*(-x_2 - 1.64427e-7)**2)) + 1.32949`
- icbr_no_replay formula (display, rounded):
  - `-1.1223*(0.0719772*(-x_2 - 0.01)**2 - 0.577866*sin(0.7*x_3 + 2.6) - 0.214173 + exp(-0.9025*(-x_1 - 0.789474)**2))**2 + 3.32927*cos(0.462794*exp(0.6*x_3) - 0.174739*sin(4.7*x_1 - 3.45) + 0.093606*sin(3.05*x_2 + 1.55) - 0.95619) - 1.04721*cos(0.886824*sin(1.9*x_1 - 3.45) + 0.106795*sin(3.15*x_2 - 1.55) + 1.05033*atan(0.8*x_3 + 0.6) - 3.03039) + 0.707316*atan(0.273567*(-x_3 - 0.113402)**2 - 0.603249*sin(3.0*x_2 - 1.55) + 0.623922*cos(3.2*x_1 + 4.5) - 0.653283) - 3.01941`
- icbr_no_shared formula (display, rounded):
  - `-1.1223*(0.0787009*(-x_2 - 0.0111112)**4 - 0.852253 + exp(-0.9025*(-x_1 - 0.789474)**2) + 0.944004*exp(-1.0*(1 - 0.5*x_3)**2))**2 - 0.401437*(-0.844327*sin(1.9*x_1 - 3.45) - 0.101677*sin(3.15*x_2 - 1.55) - atan(0.8*x_3 + 0.6) - 0.174082)**2 - 2.69362*(-0.130006*sin(4.7*x_1 - 3.45) - 1 + 0.161203*exp(-2.25*(-x_2 - 1.58946e-7)**2) + 0.52384/(1 - 0.195122*x_3)**2)**2 + 0.707316*atan(0.273567*(x_3 + 0.113402)**2 - 0.623786*sin(3.2*x_1 + 2.9) - 1.45707 + 1.41648*exp(-2.1025*(-x_2 - 1.64427e-7)**2)) + 1.32905`
- icbr_refit_commit formula (display, rounded):
  - `4.5979*sin(0.338566*sin(1.68332*x_1 - 3.41664) - 0.164074*sin(1.1*x_2 - 4.712) + 1.62425*cos(0.29864*x_3 - 0.49) + 0.607262) + 1.1085*tanh(36.6066*sin(0.14804*x_1 - 1.61344) - 0.140937*Abs(3.19812*x_2 - 0.02796) + 35.8703 + 1.47528/(1 - 0.196062*x_3)**2) - 0.728243*atan(0.456997*cos(2.09536*x_1 - 4.899) + 20.5626 + 0.756083*exp(-0.36*(-x_3 - 0.113333)**2) - 21.2076*exp(-0.0611473*(-x_2 - 0.00016176)**2)) - 4.96803 + 0.722326*exp(-3.0505*(-0.725735*sin(0.43088*x_2 - 4.70384) + 0.585372*atan(0.69996*x_3 - 0.45052) + 0.473836 + exp(-0.862669*(-x_1 - 0.856718)**2))**2)`

### task=trig_interaction seed=7

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=8.580280e-04, r2=0.998824
- Variant formula overview:
  - baseline: symbolic_s=1.746744e+01, imitation_mse=3.714190e-03, target_mse=4.476866e-03, formula_export_success=True
  - icbr_full: symbolic_s=1.194778e+00, imitation_mse=2.489957e-03, target_mse=3.278197e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=8.277106e-01, imitation_mse=3.651947e-03, target_mse=4.424701e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.840633e+00, imitation_mse=2.489957e-03, target_mse=3.278197e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.792433e+00, imitation_mse=9.667935e-02, target_mse=9.955832e-02, formula_export_success=True
- baseline formula (display, rounded):
  - `1.90405*cos(3.09636*tan(0.14912*x_1 - 6.9348) + 12.7269 - 1.69292*exp(-0.63936*(-0.70055*x_3 - 1)**2)) - 0.819219*atan(0.404789*(0.0321225 - x_3)**2 + 0.85466*sin(3.08592*x_1 - 3.01552) + 1.15465 - 1.01562*exp(-2.71063*(0.000291546 - x_2)**2)) + 0.466352*atan(0.603559*sin(3.62128*x_1 - 5.78656) - 0.355625*cos(2.78928*x_2 + 9.39744) - 0.0511708*Abs(5.1624*x_3 - 3.56976) + 0.59065) + 0.620051*atan(0.388891*sin(3.11048*x_2 + 1.58928) + 1.09265*cos(2.62192*x_1 - 1.60432) - 0.292373*tanh(4.85008*x_3 - 2.77696) + 0.875335) + 1.47404`
- icbr_full formula (display, rounded):
  - `2.53341*sin(0.817798*atan(0.85*x_3 + 0.1) + 12.8103 - 8.14235/sqrt(0.153846*x_1 + 1)) - 0.810407*atan(0.407844*(0.032258 - x_3)**2 + 1.81388 - 1.02214*exp(-2.7225*(-x_2 - 1.44496e-7)**2) - 1.62508*exp(-4.0*(0.475 - x_1)**2)) + 0.607164*atan(1.11682*sin(2.6*x_1 - 0.0499997) + 0.399221*cos(3.1*x_2 + 2.38419e-7) + 1.18112 - 0.598913*exp(-6.25*(0.92 - x_3)**2)) + 0.457549*atan(0.361238*sin(2.8*x_2 + 1.55) + 0.612589*cos(3.6*x_1 - 1.05) - 0.0572727*Abs(4.7*x_3 - 3.25) + 0.589046) + 2.11289`
- icbr_no_replay formula (display, rounded):
  - `2.53341*sin(2.72827*log(1.1*x_1 + 4.8) + 1.24527 - 1.46794*exp(-0.64*(-0.6875*x_3 - 1)**2)) - 0.810407*atan(0.407844*(0.032258 - x_3)**2 - 0.8632*cos(3.1*x_1 - 1.45) + 1.14703 - 1.02214*exp(-2.7225*(-x_2 - 1.44496e-7)**2)) + 0.457549*atan(0.613968*sin(3.6*x_1 + 0.5) + 0.361238*sin(2.8*x_2 + 1.55) - 0.0572727*Abs(4.7*x_3 - 3.25) + 0.587319) - 0.607164*atan(0.39929*sin(3.1*x_2 - 1.55) + 1.11667*cos(2.6*x_1 + 1.55) + 0.298745*tanh(4.9*x_3 - 2.8) - 0.875732) + 2.11289`
- icbr_no_shared formula (display, rounded):
  - `2.53341*sin(0.817798*atan(0.85*x_3 + 0.1) + 12.8103 - 8.14235/sqrt(0.153846*x_1 + 1)) - 0.810407*atan(0.407844*(0.032258 - x_3)**2 + 1.81388 - 1.02214*exp(-2.7225*(-x_2 - 1.44496e-7)**2) - 1.62508*exp(-4.0*(0.475 - x_1)**2)) + 0.607164*atan(1.11682*sin(2.6*x_1 - 0.0499997) + 0.399221*cos(3.1*x_2 + 2.38419e-7) + 1.18112 - 0.598913*exp(-6.25*(0.92 - x_3)**2)) + 0.457549*atan(0.361238*sin(2.8*x_2 + 1.55) + 0.612589*cos(3.6*x_1 - 1.05) - 0.0572727*Abs(4.7*x_3 - 3.25) + 0.589046) + 2.11289`
- icbr_refit_commit formula (display, rounded):
  - `-9.48543*(0.0112617*(-x_3 - 0.640492)**4 + 0.111977*sin(2.16796*x_1 + 3.11188) - 0.88389*cos(0.46336*x_2) + 1)**2 - 0.514253*cos(2.84681*cos(0.70204*x_1 + 3.0128) + 13.1392 - 13.4109*exp(-0.0501401*(0.0101822 - x_2)**2) + 0.574773/sqrt(0.591636*x_3 + 1)) + 5.05668 - 4.51442*exp(-6.37638*(-0.0337705*(0.00278746 - x_3)**2 - 0.0614107*sin(2.1476*x_1 + 3.2066) + cos(0.42532*x_2) - 0.842194)**2) - 1.24925*exp(-33.8058*(0.624123*log(1.1088*x_1 + 4.82688) + 0.200711*atan(0.78532*x_3 + 0.12276) - 1)**2)`

### task=trig_interaction seed=8

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.366993e-02, r2=0.981801
- Variant formula overview:
  - baseline: symbolic_s=1.637805e+01, imitation_mse=3.874717e-03, target_mse=1.542735e-02, formula_export_success=True
  - icbr_full: symbolic_s=1.120203e+00, imitation_mse=3.826925e-03, target_mse=1.517176e-02, formula_export_success=True
  - icbr_no_replay: symbolic_s=7.317924e-01, imitation_mse=3.852918e-03, target_mse=1.531208e-02, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.736457e+00, imitation_mse=3.826925e-03, target_mse=1.517176e-02, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.729074e+00, imitation_mse=1.000417e-01, target_mse=1.168602e-01, formula_export_success=True
- baseline formula (display, rounded):
  - `0.427989*cos(2.76929*sqrt(1 - 0.885331*x_1) + 1.06041*tanh(2.0396*x_3 + 0.81872) + 3.83751) + 0.907366*tan(0.113697*(-x_3 - 0.366451)**2 - 0.446841*cos(2.88256*x_1 + 7.61848) + 0.167318*cos(3.60784*x_2 - 6.2092) - 9.45055) - 3.87173 + 3.17349*exp(-0.720473*(0.0414443*(0.0494237 - x_3)**4 - 0.235405*sin(3.25664*x_1 - 3.38656) - 1 + 0.349802*exp(-2.09995*(0.00132495 - x_2)**2))**2) + 1.8422*exp(-0.496715*(0.0723376*Abs(9.99994*x_1 + 8.8) - 0.571927*atan(1.70784*x_3 - 1.11296) - 1)**2)`
- icbr_full formula (display, rounded):
  - `-0.435466*cos(2.72578*sqrt(1 - 0.885057*x_1) + 1.04972*tanh(2.0*x_3 + 0.8) + 0.739075) - 0.864521*cos(0.244081*Abs(4.15*x_1 + 3.65) - 0.799065*atan(1.7*x_3 - 1.1) + 1.74312) + 0.953961*tan(0.108927*(-x_3 - 0.366667)**2 - 0.16035*sin(3.6*x_2 - 1.5) + 0.428534*cos(2.9*x_1 + 4.5) - 3.16615) + 1.83643*tanh(0.188214*sin(3.0*x_2 + 1.55) - 0.296978*cos(3.25*x_1 - 4.95) - 0.452041*cos(0.45*x_3 - 2.38419e-7) + 0.513607) - 1.03256`
- icbr_no_replay formula (display, rounded):
  - `-0.435466*cos(2.72578*sqrt(1 - 0.885057*x_1) + 1.04972*tanh(2.0*x_3 + 0.8) + 0.739075) - 0.953961*tan(-0.108927*(-x_3 - 0.366667)**2 + 0.429709*sin(2.9*x_1 + 2.9) + 0.16035*sin(3.6*x_2 - 1.5) + 3.16563) - 3.83422 + 3.19275*exp(-0.732715*(0.0407442*(0.05 - x_3)**4 - 0.231294*cos(3.25*x_1 - 4.95) - 1 + 0.344006*exp(-2.1025*(-x_2 - 1.64427e-7)**2))**2) + 1.80595*exp(-0.503581*(-0.175486*Abs(4.15*x_1 + 3.65) + 0.574502*atan(1.7*x_3 - 1.1) + 1)**2)`
- icbr_no_shared formula (display, rounded):
  - `-0.435466*cos(2.72578*sqrt(1 - 0.885057*x_1) + 1.04972*tanh(2.0*x_3 + 0.8) + 0.739075) - 0.864521*cos(0.244081*Abs(4.15*x_1 + 3.65) - 0.799065*atan(1.7*x_3 - 1.1) + 1.74312) + 0.953961*tan(0.108927*(-x_3 - 0.366667)**2 - 0.16035*sin(3.6*x_2 - 1.5) + 0.428534*cos(2.9*x_1 + 4.5) - 3.16615) + 1.83643*tanh(0.188214*sin(3.0*x_2 + 1.55) - 0.296978*cos(3.25*x_1 - 4.95) - 0.452041*cos(0.45*x_3 - 2.38419e-7) + 0.513607) - 1.03256`
- icbr_refit_commit formula (display, rounded):
  - `-26.5098*sqrt(-0.00590085*(-x_3 - 0.443712)**2 + 0.0234639*cos(2.10628*x_1 - 4.892) + 1 - 0.348051*exp(-0.0688327*(0.0301875 - x_2)**2)) - 0.334856*sin(3.52604*sqrt(1 - 0.869924*x_1) + 1.32712*tanh(1.99336*x_3 + 0.79756) - 4.6755) + 0.398016*sin(-1.04517*Abs(1.67*x_1 + 3.4) + 4.13028 + 12.9639*exp(-2.87954*(1 - 0.268086*x_3)**2)) + 1.83328*tanh(0.0480632*(0.0200003 - x_3)**4 - 0.255979*sin(2.11488*x_1 - 3.81428) + 1.3958*sin(0.80002*x_2 - 4.704) - 1.10023) + 21.1077`

### task=trig_interaction seed=9

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=3.709822e-03, r2=0.994756
- Variant formula overview:
  - baseline: symbolic_s=1.556204e+01, imitation_mse=5.692142e-03, target_mse=9.361290e-03, formula_export_success=True
  - icbr_full: symbolic_s=1.052611e+00, imitation_mse=5.231661e-03, target_mse=8.426717e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=7.206855e-01, imitation_mse=5.980869e-03, target_mse=1.007589e-02, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.655016e+00, imitation_mse=5.231661e-03, target_mse=8.426717e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.587565e+00, imitation_mse=7.173591e-02, target_mse=7.417633e-02, formula_export_success=True
- baseline formula (display, rounded):
  - `0.284378*(sin(0.97448*x_3 + 6.20592) + 0.505694*tan(0.7688*x_1 - 3.62216) + 0.52422)**2 - 0.634611*sin(0.724465*tan(0.62584*x_3 + 3.5824) + 3.42616 + 1.86792*exp(-1.21952*(-x_1 - 0.708707)**2)) + 0.517218*cos(3.86477*atan(0.21408*x_3 + 0.48848) - 8.96928 + 3.02438*exp(-1.12326*(-x_1 - 0.514493)**2)) + 0.219336*Abs(-2.71752*sin(3.10032*x_1 + 9.4076) + 2.26257*cos(3.1548*x_2 + 0.00399999) + 0.611566*atan(2.08648*x_3 + 1.0604) + 4.99381) - 1.88152`
- icbr_full formula (display, rounded):
  - `-2.9452*(-1 + 0.549299*exp(-1.3225*(-x_1 - 0.695652)**2) + 0.72478/sqrt(1 - 0.482759*x_3))**2 + 0.727265*sin(0.964074*sin(0.95*x_3 + 3.05) - 2.7698*atan(2.3*x_1 + 3.5) + 1.74108) + 0.510938*cos(-3.26636*(1 - 0.0414508*x_3)**5 + 2.30978 + 3.07429*exp(-1.1025*(x_1 + 0.52381)**2)) - 6.30378*tanh(0.0792947*sin(3.15*x_2 - 1.55) + 0.0951019*cos(3.1*x_1 + 1.55) - 0.218199*tanh(0.55*x_3 + 1.5) + 0.214606) + 0.768699`
- icbr_no_replay formula (display, rounded):
  - `0.272641*(-cos(1.0*x_3 + 1.5) + 0.509954*tan(0.75*x_1 - 3.65) + 0.546211)**2 + 0.51969*sin(-2.65742*(1 - 0.0829016*x_3)**3 + 3.31077 + 2.99931*exp(-1.1025*(x_1 + 0.52381)**2)) - 0.602467*sin(0.783502*tan(0.6*x_3 + 0.45) - 2.88533 + 1.89985*exp(-1.3225*(-x_1 - 0.695652)**2)) + 0.358207*Abs(-1.66428*cos(3.1*x_1 + 1.55) + 1.3862*cos(3.15*x_2 + 2.38419e-7) + 0.37867*atan(2.05*x_3 + 1.05) + 3.04878) - 1.85006`
- icbr_no_shared formula (display, rounded):
  - `-2.9452*(-1 + 0.549299*exp(-1.3225*(-x_1 - 0.695652)**2) + 0.72478/sqrt(1 - 0.482759*x_3))**2 + 0.727265*sin(0.964074*sin(0.95*x_3 + 3.05) - 2.7698*atan(2.3*x_1 + 3.5) + 1.74108) + 0.510938*cos(-3.26636*(1 - 0.0414508*x_3)**5 + 2.30978 + 3.07429*exp(-1.1025*(x_1 + 0.52381)**2)) - 6.30378*tanh(0.0792947*sin(3.15*x_2 - 1.55) + 0.0951019*cos(3.1*x_1 + 1.55) - 0.218199*tanh(0.55*x_3 + 1.5) + 0.214606) + 0.768699`
- icbr_refit_commit formula (display, rounded):
  - `-0.299714*sin(-2.32157*atanh(0.22*x_3 + 0.69996) + 4.84602 + 3.31524*exp(-1.01091*(0.801162 - x_1)**2)) - 0.246335*cos(-7.74231*atan(2.85864*x_1 + 4.59148) + 7.01951 + 5.01832*exp(-0.494659*(-0.615197*x_3 - 1)**2)) - 0.149863*Abs(7.86418*(0.0419725*x_3 - 1)**5 - 1.23003*Abs(3.90656*x_1 + 2.3406) + 13.866) + 0.605658*Abs(3.40158*sin(1.1*x_2 - 4.712) + 0.829537*cos(2.15612*x_1 - 1.61324) - 0.304572 - 0.235006*exp(-0.9506*x_3)) - 0.813185`

### task=trig_interaction seed=10

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=4.390491e-02, r2=0.935235
- Variant formula overview:
  - baseline: symbolic_s=1.670743e+01, imitation_mse=3.636261e-03, target_mse=4.974522e-02, formula_export_success=True
  - icbr_full: symbolic_s=1.119709e+00, imitation_mse=3.221682e-03, target_mse=4.882984e-02, formula_export_success=True
  - icbr_no_replay: symbolic_s=7.400151e-01, imitation_mse=3.800195e-03, target_mse=4.745243e-02, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.749547e+00, imitation_mse=3.221682e-03, target_mse=4.882984e-02, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.660884e+00, imitation_mse=9.172502e-02, target_mse=1.527550e-01, formula_export_success=True
- baseline formula (display, rounded):
  - `-0.528935*cos(-1.43263*(0.53192*x_3 + 1)**(3/2) + 1.13318*atan(2.04952*x_1 + 0.62736) + 10.3364) + 0.806176*tan(0.0911126*(-x_3 - 0.176611)**4 + 0.24795*sin(2.79568*x_1 + 6.21144) - 5.90345 + 0.256737*exp(-2.40374*(0.00815273 - x_2)**2)) - 1.63743*atan(0.232713*sin(3.38552*x_1 + 2.9852) + 0.035171*cos(2.00504*x_3 + 6.994) - 0.011215 - 0.537168*exp(-2.73572*(-x_2 - 0.0052237)**2)) - 2.08779 + 1.31718*exp(-2.36337*(-0.378682*tanh(0.78784*x_3 + 0.30304) + 0.336489 - exp(-1.3343*(-x_1 - 0.496502)**2))**2)`
- icbr_full formula (display, rounded):
  - `0.565425*sin(0.882423*cos(1.05*x_3 + 5.0) - 5.81148 + 3.2618*exp(-1.21*(-x_1 - 0.5)**2)) - 0.53618*cos(4.07126*sin(0.35*x_3 - 0.65) - 1.1489*atan(1.95*x_1 + 0.6) + 6.13292) + 0.801205*tan(0.102452*(-x_3 - 0.189474)**2 + 0.255844*sin(2.8*x_1 - 0.0499997) + 3.47975 + 0.26485*exp(-2.4025*(-x_2 - 1.53818e-7)**2)) + 0.40318 - 3.10183*exp(-0.565375*(0.0338551*(-x_3 - 0.375)**2 - 0.193871*sin(3.4*x_1 + 3.0) + 1 + 0.447336*exp(-2.7225*(-x_2 - 1.44496e-7)**2))**2)`
- icbr_no_replay formula (display, rounded):
  - `-0.528762*sin(-1.42534*(0.535354*x_3 + 1)**(3/2) + 1.16464*atan(1.95*x_1 + 0.6) + 5.61711) + 0.801205*tan(0.0940517*(-x_3 - 0.176471)**4 + 0.115114*sin(3.15*x_2 + 1.55) - 0.255944*cos(2.8*x_1 + 1.5) + 3.64185) + 1.83831*tanh(-0.0314465*sin(2.0*x_3 - 4.0) + 0.208234*cos(3.4*x_1 + 4.55) + 0.0446348 + 0.480511*exp(-2.7225*(-x_2 - 1.44496e-7)**2)) - 2.11179 + 1.30593*exp(-2.53756*(-0.363653*tanh(0.8*x_3 + 0.3) + 0.35766 - exp(-1.21*(-x_1 - 0.5)**2))**2)`
- icbr_no_shared formula (display, rounded):
  - `0.565425*sin(0.882423*cos(1.05*x_3 + 5.0) - 5.81148 + 3.2618*exp(-1.21*(-x_1 - 0.5)**2)) - 0.53618*cos(4.07126*sin(0.35*x_3 - 0.65) - 1.1489*atan(1.95*x_1 + 0.6) + 6.13292) + 0.801205*tan(0.102452*(-x_3 - 0.189474)**2 + 0.255844*sin(2.8*x_1 - 0.0499997) + 3.47975 + 0.26485*exp(-2.4025*(-x_2 - 1.53818e-7)**2)) + 0.40318 - 3.10183*exp(-0.565375*(0.0338551*(-x_3 - 0.375)**2 - 0.193871*sin(3.4*x_1 + 3.0) + 1 + 0.447336*exp(-2.7225*(-x_2 - 1.44496e-7)**2))**2)`
- icbr_refit_commit formula (display, rounded):
  - `0.418194*sin(6.01652*sin(0.3114*x_3 + 2.41396) + 2.42212*atan(0.93948*x_1 + 0.4932) - 3.5294) + 0.642432*sin(0.757454*atan(0.95028*x_3 + 0.25956) + 3.35795 - 2.1117*exp(-1.73059*(0.863172 - x_1)**2)) + 4.12302*sin(0.0833737*cos(2.58696*x_1 + 1.492) + 8.73761 + 0.297281*exp(-0.0719097*(-x_3 - 0.373061)**2) - 6.73741*exp(-0.0416812*x_2**2)) - 4.91195 + 4.70203/(-0.131721*(-x_3 - 0.329257)**2 - 0.873971*sin(1.10002*x_2 - 4.712) + 0.437295*cos(2.17472*x_1 + 1.51188) + 3.56504)`

### task=trig_interaction seed=11

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.817124e-03, r2=0.997571
- Variant formula overview:
  - baseline: symbolic_s=1.642709e+01, imitation_mse=4.614309e-03, target_mse=5.387733e-03, formula_export_success=True
  - icbr_full: symbolic_s=1.136625e+00, imitation_mse=4.175215e-03, target_mse=4.738392e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=7.117721e-01, imitation_mse=4.350398e-03, target_mse=5.132723e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.778766e+00, imitation_mse=4.175215e-03, target_mse=4.738394e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.598389e+00, imitation_mse=7.260990e-02, target_mse=7.703864e-02, formula_export_success=True
- baseline formula (display, rounded):
  - `0.500515*sin(-2.61442*tan(0.22192*x_3 - 9.03848) + 0.225875*Abs(10.0*x_1 + 5.0) + 6.48949) - 0.810517*cos(-1.6911*tan(0.556*x_1 - 6.41408) + 1.30156*atan(0.79216*x_3 + 0.392) + 8.74036) + 2.93201*cos(0.0470862*(0.0568437 - x_3)**4 + 0.154606*cos(3.412*x_1 - 1.78808) + 0.170256*cos(3.18384*x_2 + 0.01184) + 5.04384) + 0.381547*tanh(0.710674*tanh(3.20032*x_3 - 1.712) - 2.15305 + 2.61317*exp(-1.67485*(0.588737 - x_1)**2) + 0.329258*exp(-2.5083*(0.0439965 - x_2)**2)) - 1.50621`
- icbr_full formula (display, rounded):
  - `2.93745*sin(0.0426193*(0.0444444 - x_3)**2 - 0.169073*sin(3.2*x_2 - 1.55) + 0.153705*cos(3.4*x_1 + 4.5) + 0.320344) - 0.980229*cos(-1.30417*(0.191489*x_3 - 1)**3 + 1.88911*atanh(0.45*x_1 - 0.15) + 2.11159) - 0.506601*cos(2.37733*tan(0.25*x_3 - 2.8) - 0.560521*Abs(4.0*x_1 + 2.0) + 4.69486) - 0.379248*tanh(1.23465*cos(2.3*x_1 - 4.55) - 0.733963*tanh(3.0*x_3 - 1.65) + 0.809203 - 0.334108*exp(-2.4025*(0.0322579 - x_2)**2)) - 1.67229`
- icbr_no_replay formula (display, rounded):
  - `-0.505688*sin(-2.37733*tan(0.25*x_3 - 2.8) + 0.560521*Abs(4.0*x_1 + 2.0) + 3.15514) + 2.93745*sin(0.0469868*(0.0555556 - x_3)**4 - 0.169073*sin(3.2*x_2 - 1.55) + 0.153705*cos(3.4*x_1 + 4.5) + 0.325128) - 0.980229*cos(1.52078*tan(0.55*x_1 + 3.0) - 1.15424*atan(0.8*x_3 + 0.4) + 3.77679) - 0.379248*tanh(1.23465*cos(2.3*x_1 - 4.55) - 0.733963*tanh(3.0*x_3 - 1.65) + 0.809203 - 0.334108*exp(-2.4025*(0.0322579 - x_2)**2)) - 1.67107`
- icbr_no_shared formula (display, rounded):
  - `2.93745*sin(0.0426193*(0.0444444 - x_3)**2 - 0.169073*sin(3.2*x_2 - 1.55) + 0.153705*cos(3.4*x_1 + 4.5) + 0.320344) - 0.980229*cos(-1.30417*(0.191489*x_3 - 1)**3 + 1.88911*atanh(0.45*x_1 - 0.15) + 2.11159) - 0.506601*cos(2.37733*tan(0.25*x_3 - 2.8) - 0.448417*Abs(5.0*x_1 + 2.5) + 4.69486) - 0.379248*tanh(1.23465*cos(2.3*x_1 - 4.55) - 0.733963*tanh(3.0*x_3 - 1.65) + 0.809203 - 0.334108*exp(-2.4025*(0.0322579 - x_2)**2)) - 1.67229`
- icbr_refit_commit formula (display, rounded):
  - `-0.362398*cos(2.61483*(1 - 0.192163*x_3)**3 + 7.86566*tan(0.17808*x_1 + 2.6436) - 1.4696) - 0.471978*cos(-3.08596*tan(0.19568*x_3 + 0.41116) + 1.5801*Abs(1.3118*x_1 + 0.80724) + 2.00094) + 0.467792*cos(0.81176*cos(2.06296*x_1 - 4.5924) + 0.0532854*Abs(4.08164*x_2 - 0.19848) + 2.57469 - 3.56258*exp(-3.55926*(1 - 0.424552*x_3)**2)) + 4.00418 - 10.9274*exp(-10.9656*(-0.0132254*cos(2.16084*x_1 + 0.91276) - 0.652499 - 0.0275658*exp(-0.171959*(-x_3 - 0.00028938)**2) + exp(-0.0423042*(-x_2 - 0.00991831)**2))**2)`

### task=trig_interaction seed=12

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=8.239121e-03, r2=0.989670
- Variant formula overview:
  - baseline: symbolic_s=1.649311e+01, imitation_mse=4.059907e-03, target_mse=1.412252e-02, formula_export_success=True
  - icbr_full: symbolic_s=1.151919e+00, imitation_mse=4.126425e-03, target_mse=1.368957e-02, formula_export_success=True
  - icbr_no_replay: symbolic_s=7.273380e-01, imitation_mse=4.140490e-03, target_mse=1.402936e-02, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.734807e+00, imitation_mse=4.126425e-03, target_mse=1.368957e-02, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.737734e+00, imitation_mse=8.194225e-02, target_mse=9.114729e-02, formula_export_success=True
- baseline formula (display, rounded):
  - `0.394628*sin(-8.1793 + 4.53384*exp(-1.66926*(-x_1 - 0.387121)**2) + 3.90857*exp(-0.571898*(1 - 0.442822*x_3)**2)) + 0.929454*sin(0.826106*tanh(4.20024*x_1 + 0.3) - 1.17512*atanh(0.444*x_3 + 0.3284) + 1.74742) + 0.446036*tanh(1.03928*cos(2.72416*x_1 + 4.78792) + 0.496654*tan(0.58952*x_3 + 0.6064) - 1.55133 + 0.557596*exp(-3.74779*(0.0239266 - x_2)**2)) - 1.84359*atan(0.201226*cos(3.28392*x_1 + 7.79584) + 0.26071*cos(3.16632*x_2 - 9.4096) - 0.319794 + 0.0505735*exp(-2.00483*(-x_3 - 0.714504)**2)) - 0.927001`
- icbr_full formula (display, rounded):
  - `0.930896*sin(0.815995*tanh(4.5*x_1 + 0.3) - 1.1279*asin(0.45*x_3 + 0.5) + 1.94094) + 0.394224*cos(1.84446*sin(0.6*x_3 + 3.05) + 1.06115 - 4.48812*exp(-1.69*(-x_1 - 0.384615)**2)) - 0.812258*cos(0.565662*sin(2.7*x_1 - 3.05) + 0.374472 - 0.303936*exp(-3.8025*(0.0256409 - x_2)**2) - 0.785427/sqrt(1 - 0.623377*x_3)) + 1.31975 - 3.26462*exp(-0.915793*(-0.18216*sin(3.15*x_2 - 1.55) - 0.140548*cos(3.3*x_1 + 1.5) + 1 - 0.0353318*exp(-1.96*(-x_3 - 0.714286)**2))**2)`
- icbr_no_replay formula (display, rounded):
  - `0.930896*sin(-0.95593*tan(0.55*x_3 + 3.45) + 0.815995*tanh(4.5*x_1 + 0.3) + 1.65637) + 0.394224*cos(-3.34669 + 3.71795*exp(-0.5625*(0.466667*x_3 - 1)**2) + 4.48812*exp(-1.69*(-x_1 - 0.384615)**2)) + 2.00772*tanh(0.185004*sin(3.3*x_1 - 0.0499997) - 0.239692*sin(3.15*x_2 - 1.55) + 0.309694 - 0.0464908*exp(-1.96*(-x_3 - 0.714286)**2)) + 0.466281*tanh(0.975235*cos(2.7*x_1 - 1.5) + 0.469059*tan(0.6*x_3 - 2.55) - 1.48376 + 0.524027*exp(-3.8025*(0.0256409 - x_2)**2)) - 0.950283`
- icbr_no_shared formula (display, rounded):
  - `0.930896*sin(0.815995*tanh(4.5*x_1 + 0.3) - 1.1279*asin(0.45*x_3 + 0.5) + 1.94094) + 0.394224*cos(1.84446*sin(0.6*x_3 + 3.05) + 1.06115 - 4.48812*exp(-1.69*(-x_1 - 0.384615)**2)) - 0.812258*cos(0.565662*sin(2.7*x_1 - 3.05) + 0.374472 - 0.303936*exp(-3.8025*(0.0256409 - x_2)**2) - 0.785427/sqrt(1 - 0.623377*x_3)) + 1.31975 - 3.26462*exp(-0.915793*(-0.18216*sin(3.15*x_2 - 1.55) - 0.140548*cos(3.3*x_1 + 1.5) + 1 - 0.0353318*exp(-1.96*(-x_3 - 0.714286)**2))**2)`
- icbr_refit_commit formula (display, rounded):
  - `-0.460375*sin(-2.85273*atanh(0.25168*x_3 + 0.53764) + 4.50642 + 3.22498*exp(-1.71746*(0.604676 - x_1)**2)) + 0.867474*sin(0.288436*log(3.84436 - 3.13652*x_3) + 0.513967*sin(2.17752*x_1 - 3.0998) + 7.076 - 3.38449*exp(-0.0912765*(0.0328346 - x_2)**2)) - 0.360519*cos(-1.43365*sin(0.603*x_3 - 0.0922799) + 0.744577*Abs(3.52336*x_1 + 1.46848) + 0.0125535) - 4.13183*tanh(0.0772753*cos(2.59868*x_1 - 4.6988) - 0.012829*tanh(2.64488*x_3 + 0.29804) + 6.74619 - 7.35666*exp(-0.0416649*x_2**2)) - 1.42286`

### task=trig_interaction seed=13

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.870870e-03, r2=0.997525
- Variant formula overview:
  - baseline: symbolic_s=1.873783e+01, imitation_mse=3.638195e-03, target_mse=5.011617e-03, formula_export_success=True
  - icbr_full: symbolic_s=1.254437e+00, imitation_mse=3.453286e-03, target_mse=4.799435e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=8.778802e-01, imitation_mse=3.794630e-03, target_mse=5.136981e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.958067e+00, imitation_mse=3.453286e-03, target_mse=4.799435e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.893807e+00, imitation_mse=8.226382e-02, target_mse=8.696847e-02, formula_export_success=True
- baseline formula (display, rounded):
  - `-0.252906*cos(0.49091*(-x_2 - 0.0435735)**3 + 0.217586*(-x_3 - 0.0485467)**4 + 0.428079*sin(3.92208*x_1 - 6.80504) - 10.8817) - 1.11955*cos(0.0417043*cos(3.09992*x_2 - 3.19192) + 0.913137*tan(0.8548*x_1 + 9.57024) + 1.98309 + 2.09662*exp(-0.681483*(-0.706173*x_3 - 1)**2)) - 0.724152*tanh(0.35618*(-x_3 - 0.236406)**3 + 0.719923*sin(2.66056*x_1 + 9.3952) + 0.24621*cos(3.60112*x_2 - 3.20152) + 0.918317) - 1.7671*atan(0.152303*atan(3.29496*x_3 + 2.1652) - 0.616658 + 0.923421*exp(-3.08185*(-x_1 - 0.487969)**2) - 0.620296*exp(-2.4466*(0.0164689 - x_2)**2)) - 1.06007`
- icbr_full formula (display, rounded):
  - `1.08647*sin(0.939477*tan(0.85*x_1 - 3.0) - 1.19165*atan(0.9*x_3 + 0.15) + 1.70672 - 0.0946934*exp(-2.56*(-x_2 - 1.49012e-7)**2)) - 0.249071*cos(0.498298*(-x_2 - 0.0434783)**3 + 0.435098*sin(3.95*x_1 - 0.5) + 2.82859 - 1.17348*exp(-0.16*(x_3 + 0.124999)**2)) - 0.536951*atan(0.490211*(-x_3 - 0.235955)**3 + 0.988282*cos(2.65*x_1 + 1.55) - 0.338471*cos(3.6*x_2 - 0.0499997) + 1.12071) + 0.83969 - 3.56959*exp(-1.31473*(0.0786858*atan(3.25*x_3 + 2.15) - 1 + 0.472545*exp(-3.0625*(-x_1 - 0.485714)**2) - 0.318857*exp(-2.4025*(0.0322579 - x_2)**2))**2)`
- icbr_no_replay formula (display, rounded):
  - `-1.08647*sin(0.042453*cos(3.1*x_2 - 0.0499997) - 0.939477*tan(0.85*x_1 - 3.0) + 1.19165*atan(0.9*x_3 + 0.15) - 1.65606) - 0.249071*cos(0.498298*(-x_2 - 0.0434783)**3 + 0.220191*(x_3 + 0.05)**4 - 0.434407*cos(3.9*x_1 + 1.05) + 1.67123) - 0.721596*tanh(0.356517*(-x_3 - 0.235955)**3 + 0.71875*cos(2.65*x_1 + 1.55) - 0.24616*cos(3.6*x_2 - 0.0499997) + 0.91506) + 2.0037*tanh(0.238256*cos(3.15*x_2 - 0.0499997) - 0.135334*atan(3.25*x_3 + 2.15) + 0.875264 - 0.812742*exp(-3.0625*(-x_1 - 0.485714)**2)) - 1.08137`
- icbr_no_shared formula (display, rounded):
  - `1.08647*sin(0.939477*tan(0.85*x_1 - 3.0) - 1.19165*atan(0.9*x_3 + 0.15) + 1.70672 - 0.0946934*exp(-2.56*(-x_2 - 1.49012e-7)**2)) - 0.249071*cos(0.498298*(-x_2 - 0.0434783)**3 + 0.435098*sin(3.95*x_1 - 0.5) + 2.82859 - 1.17348*exp(-0.16*(x_3 + 0.124999)**2)) - 0.536951*atan(0.490211*(-x_3 - 0.235955)**3 + 0.988282*cos(2.65*x_1 + 1.55) - 0.338471*cos(3.6*x_2 - 0.0499997) + 1.12071) + 0.83969 - 3.56959*exp(-1.31473*(0.0786858*atan(3.25*x_3 + 2.15) - 1 + 0.472545*exp(-3.0625*(-x_1 - 0.485714)**2) - 0.318857*exp(-2.4025*(0.0322579 - x_2)**2))**2)`
- icbr_refit_commit formula (display, rounded):
  - `-1.83562*sin(0.0360736*(1 - 0.777418*x_3)**4 + 0.397461*sin(2.13672*x_1 - 0.10868) - 2.53351*sin(0.70006*x_2 - 1.596) + 1.27386) - 8.68588*sin(-0.0454822*(-x_3 - 0.470263)**3 + 0.850955*cos(0.54416*x_2 - 0.00576) + 0.791671 + 0.304296*exp(-1.54117*(0.710272 - x_1)**2)) + 6.90187 + 1.26093*exp(-3.21246*(0.126553*sin(0.86764*x_2 - 1.60012) + 0.78003*tan(0.42864*x_1 + 0.4708) - 0.783287 + exp(-0.663052*(-0.701233*x_3 - 1)**2))**2) - 0.461822*exp(-233.088*(-0.00436939*(-0.790672*x_2 - 1)**3 + 0.932899*sin(0.20026*x_1 + 1.52) - 0.0158935*cos(1.00068*x_3 - 3.01632) - 1)**2)`

### task=trig_interaction seed=14

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=8.184940e-03, r2=0.988844
- Variant formula overview:
  - baseline: symbolic_s=1.754291e+01, imitation_mse=3.658795e-03, target_mse=1.044684e-02, formula_export_success=True
  - icbr_full: symbolic_s=1.186237e+00, imitation_mse=3.696546e-03, target_mse=1.065250e-02, formula_export_success=True
  - icbr_no_replay: symbolic_s=7.776587e-01, imitation_mse=3.855315e-03, target_mse=1.069354e-02, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.803200e+00, imitation_mse=3.696537e-03, target_mse=1.065250e-02, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.752020e+00, imitation_mse=6.474165e-02, target_mse=7.572677e-02, formula_export_success=True
- baseline formula (display, rounded):
  - `2.02998*atan(0.189163*cos(3.21392*x_1 + 4.78344) - 0.184487 + 0.568509*exp(-2.04398*(0.0492977 - x_2)**2)) - 0.3841 - 1.24568*exp(-2.56722*(0.0775958*Abs(9.46784*x_1 - 5.658) - 0.483092*atan(0.862*x_3 - 0.72184) - 1 + 0.0333154*exp(-22.8193*(0.526025 - x_2)**2))**2) + 1.02783*exp(-3.01715*(-0.029204*tan(0.6268*x_2 - 0.00624) + 0.368846*atan(1.07224*x_3 - 0.4748) - 0.269472 + exp(-1.15778*(-x_1 - 0.577695)**2))**2) + 0.273522*exp(-1.21831*(-0.392982*cos(2.69096*x_1 + 1.41112) - 0.772565*atan(3.542*x_2 - 2.28392) - 1 - 0.501622*exp(-12.1383*(1 - 0.976315*x_3)**2))**2)`
- icbr_full formula (display, rounded):
  - `0.121916*tanh(0.456521*(-x_3 - 0.278689)**5 + 0.881538*tanh(3.85*x_1 - 0.2) + 2.04058 - 4.88785*exp(-3.0625*(1 - 0.857143*x_2)**2)) + 2.13497*atan(0.178702*cos(3.2*x_1 - 1.5) - 0.233155*cos(2.9*x_2 + 3.0) + 0.126888) - 0.25736 + 1.02914*exp(-3.08345*(0.0274813*tan(0.65*x_2 + 2.38419e-7) - 0.365587*atan(1.05*x_3 - 0.45) + 0.288172 - exp(-1.1025*(-x_1 - 0.571429)**2))**2) - 1.24121*exp(-0.378651*(0.819254*(-0.171429*x_3 - 1)**5 + 0.0276421*sin(5.0*x_2 - 1.05) + 0.417212*Abs(4.6*x_1 - 2.75) - 1)**2)`
- icbr_no_replay formula (display, rounded):
  - `2.13497*atan(0.178702*cos(3.2*x_1 - 1.5) - 0.233155*cos(2.9*x_2 + 3.0) + 0.126888) - 0.398161 - 1.24121*exp(-3.64177*(-0.647115*tanh(0.6*x_3 - 0.75) + 0.13453*Abs(4.6*x_1 - 2.75) - 1 + 0.0280109*exp(-22.5625*(0.526316 - x_2)**2))**2) + 1.02914*exp(-3.08345*(0.0274813*tan(0.65*x_2 + 2.38419e-7) - 0.365587*atan(1.05*x_3 - 0.45) + 0.288172 - exp(-1.1025*(-x_1 - 0.571429)**2))**2) + 0.275453*exp(-1.18111*(0.390723*cos(2.7*x_1 + 4.55) - 0.769737*atan(3.55*x_2 - 2.3) - 1 - 0.502946*exp(-11.9025*(1 - 0.971014*x_3)**2))**2)`
- icbr_no_shared formula (display, rounded):
  - `0.121916*tanh(0.456915*(-x_3 - 0.278481)**5 + 0.881538*tanh(3.85*x_1 - 0.2) + 2.04055 - 4.88785*exp(-3.0625*(1 - 0.857143*x_2)**2)) + 2.13497*atan(0.178702*cos(3.2*x_1 - 1.5) - 0.233155*cos(2.9*x_2 + 3.0) + 0.126888) - 0.25736 + 1.02914*exp(-3.08345*(0.0274813*tan(0.65*x_2 - 2.38419e-7) - 0.365587*atan(1.05*x_3 - 0.45) + 0.288172 - exp(-1.1025*(-x_1 - 0.571429)**2))**2) - 1.24121*exp(-0.378651*(0.819254*(-0.171429*x_3 - 1)**5 + 0.0276421*sin(5.0*x_2 - 1.05) + 0.417212*Abs(4.6*x_1 - 2.75) - 1)**2)`
- icbr_refit_commit formula (display, rounded):
  - `-1.49136*cos(0.202406*cos(2.16444*x_1 + 1.62132) + 2.88805*cos(0.71604*x_2 + 3.10424) + 0.898608) + 0.242718*Abs(0.564027*cos(0.41856*x_2 + 0.10208) - 10.4017*tanh(0.416*x_3 - 1.2001) + 0.711129*Abs(4.56088*x_1 - 3.1732) - 12.6309) - 24.9055 + 24.1674*exp(-0.0412206*(-0.0914333*tan(0.25288*x_2 - 3.10488) - 0.177432*Abs(4.36316*x_1 + 2.842) + 0.537146*atan(0.84356*x_3 - 0.4788) + 1)**2) + 0.2724*exp(-124.481*(0.0156537*(-x_3 - 0.271535)**5 - 0.0315726 - exp(-3.89226*(1 - 0.330846*x_2)**2) + 0.066273*exp(-1.68974*(0.723133 - x_1)**2))**2)`

### task=trig_interaction seed=15

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=3.093117e-03, r2=0.995512
- Variant formula overview:
  - baseline: symbolic_s=1.627554e+01, imitation_mse=3.937670e-03, target_mse=6.200766e-03, formula_export_success=True
  - icbr_full: symbolic_s=1.145188e+00, imitation_mse=4.019482e-03, target_mse=8.087819e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=7.294350e-01, imitation_mse=4.121100e-03, target_mse=6.266429e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.714822e+00, imitation_mse=4.020891e-03, target_mse=8.088623e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.740583e+00, imitation_mse=9.133089e-02, target_mse=8.917523e-02, formula_export_success=True
- baseline formula (display, rounded):
  - `-0.157329*sin(1.0788*tan(0.96232*x_3 - 6.1968) - 8.85878 + 2.0219*exp(-6.8774*(-0.949666*x_1 - 1)**2)) + 0.912056*sin(0.168899*(-x_2 - 0.000905484)**2 + 1.23951*tan(0.308*x_3 - 5.66832) - 0.870591*tanh(4.20004*x_1 + 0.308) + 7.09654) - 1.40833*sin(0.118625*(-x_3 - 0.274206)**2 + 0.391042*sin(3.05352*x_1 - 6.39024) - 3.90687 + 0.850421*exp(-2.37752*(-x_2 - 0.000207534)**2)) - 0.433316*cos(3.95001*sqrt(0.422916*x_3 + 1) + 3.33384 + 4.99429*exp(-1.30837*(-x_1 - 0.389215)**2)) - 0.344923`
- icbr_full formula (display, rounded):
  - `-0.434495*sin(-3.89269*sqrt(0.426667*x_3 + 1) + 0.824875*Abs(4.7*x_1 + 1.85) + 5.3183) + 1.12652*sin(1.30466*sqrt(1 - 0.77*x_3) - 0.148843*(-x_2 - 5.96046e-8)**2 + 0.771899*tanh(4.05*x_1 + 0.3) + 0.159446) + 0.173774*cos(1.19725*asin(0.9*x_3 + 0.1) - 0.95653 + 1.90268*exp(-6.76*(-0.942308*x_1 - 1)**2)) + 1.45727*cos(0.114521*(-x_3 - 0.274194)**2 - 0.377694*cos(3.05*x_1 + 1.45) + 0.35542*cos(3.15*x_2 + 2.38419e-7) - 1.86975) - 0.557`
- icbr_no_replay formula (display, rounded):
  - `0.434495*sin(3.89269*sqrt(0.426667*x_3 + 1) - 10.7054 + 4.93908*exp(-1.3225*(x_1 + 0.391304)**2)) + 1.3797*sin(0.121257*(-x_3 - 0.274194)**2 - 0.399911*cos(3.05*x_1 + 1.45) - 0.767986 + 0.866225*exp(-2.4025*(-x_2 - 1.53818e-7)**2)) - 0.949987*cos(0.164791*(-x_2 - 5.96046e-8)**2 + 1.13993*tan(0.35*x_3 + 3.7) - 0.854602*tanh(4.05*x_1 + 0.3) + 2.54424) - 0.625085 + 0.383981*exp(-0.905044*(0.53753*tan(0.95*x_3 - 3.05) - 0.496116 + exp(-6.76*(-0.942308*x_1 - 1)**2))**2)`
- icbr_no_shared formula (display, rounded):
  - `-0.434495*sin(-3.89269*sqrt(0.426667*x_3 + 1) + 0.824875*Abs(4.7*x_1 + 1.85) + 5.3183) + 1.12652*sin(1.30257*sqrt(1 - 0.771084*x_3) - 0.148843*(-x_2 - 8.08199e-8)**2 + 0.771899*tanh(4.05*x_1 + 0.3) + 0.161599) + 0.173774*cos(1.19725*asin(0.9*x_3 + 0.1) - 0.95653 + 1.90268*exp(-6.76*(-0.942308*x_1 - 1)**2)) + 1.45727*cos(0.114521*(-x_3 - 0.274194)**2 - 0.377694*cos(3.05*x_1 + 1.45) + 0.35542*cos(3.15*x_2 + 2.38419e-7) - 1.86975) - 0.557`
- icbr_refit_commit formula (display, rounded):
  - `-2.38588*(0.578295*sqrt(1 - 0.769732*x_3) - 0.0623783*(-x_2 - 0.00127209)**2 - 1 + 0.790844*exp(-1.71673*(0.596715 - x_1)**2))**2 - 2.40724*cos(-1.13218*sqrt(0.419381*x_3 + 1) + 0.326921*Abs(2.79528*x_1 + 1.4504) + 3.40777) - 3.47871 + 3.22913*exp(-2.18445*(-0.535474*sin(1.1*x_2 - 4.712) + sin(0.25196*x_3 - 4.61524) + 0.118255*cos(2.22156*x_1 - 4.79336) + 0.0332758)**2) + 0.226964*exp(-8.20407*(0.501108*tanh(2.28224*x_1 + 2.13332) - atanh(0.233*x_3 + 0.54556) + 0.367217)**2)`

### task=trig_interaction seed=16

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=7.732280e-03, r2=0.989535
- Variant formula overview:
  - baseline: symbolic_s=1.644454e+01, imitation_mse=2.544113e-03, target_mse=9.057995e-03, formula_export_success=True
  - icbr_full: symbolic_s=1.138267e+00, imitation_mse=1.663279e-03, target_mse=8.032554e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=7.049075e-01, imitation_mse=3.090470e-03, target_mse=9.337440e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.724828e+00, imitation_mse=1.663279e-03, target_mse=8.032554e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.645742e+00, imitation_mse=8.294655e-02, target_mse=8.175211e-02, formula_export_success=True
- baseline formula (display, rounded):
  - `-0.565364*sin(-2.73952*sqrt(1 - 0.537683*x_3) + 8.85773 + 3.42493*exp(-0.766675*(0.545637 - x_1)**2)) + 1.26186*sin(0.208024*sin(3.40096*x_1 + 6.2104) - 0.0113403*cos(3.30248*x_3 + 2.78096) - 0.342096 + 0.897856*exp(-2.61197*(-x_2 - 0.000792002)**2)) - 1.35931 + 0.897617*exp(-2.65762*(0.0392626*sin(1.74448*x_2 + 7.78872) + 0.545957 - exp(-1.20631*(-x_1 - 0.445334)**2) - 0.465688*exp(-0.620566*(0.633492 - x_3)**2))**2) + 1.08832*exp(-1.74449*(-0.462697*atan(1.44568*x_3 - 1.306) + 0.0512479 - exp(-1.04874*(-x_1 - 0.686665)**2))**2)`
- icbr_full formula (display, rounded):
  - `-2.66157*(0.0630025*cos(3.4*x_1 + 1.5) - 0.120459*cos(3.2*x_2 + 2.38419e-7) + 1 - 0.00712128*exp(-4.0*(0.125 - x_3)**2))**(3/2) + 0.440096*sin(0.430695*Abs(4.55*x_1 + 3.05) + 0.346337 - 18.2136*exp(-3.61*(1 - 0.210526*x_3)**2)) + 0.390024*sin(0.156078*(0.0399999 - x_2)**2 + 0.644805*cos(1.65*x_3 - 1.05) - 5.72645 + 3.26836*exp(-1.21*(x_1 + 0.454545)**2)) + 0.565953*cos(2.75439*atanh(0.2*x_3 + 0.5) + 0.0148429 + 3.31463*exp(-0.81*(0.555556 - x_1)**2)) + 2.61918`
- icbr_no_replay formula (display, rounded):
  - `1.25398*sin(0.209377*cos(3.4*x_1 + 1.5) + 0.011416*cos(3.3*x_3 - 3.5) + 3.49417 - 0.908706*exp(-2.56*(-x_2 - 1.49012e-7)**2)) + 0.565953*cos(-2.74407*sqrt(1 - 0.536842*x_3) + 4.27146 + 3.31463*exp(-0.81*(0.555556 - x_1)**2)) - 1.28879 + 0.871382*exp(-2.8647*(0.0377495*sin(1.8*x_2 + 1.5) - 0.195642*sin(1.65*x_3 + 0.5) + 0.273496 - exp(-1.21*(x_1 + 0.454545)**2))**2) + 1.05513*exp(-1.90626*(-0.454608*atan(1.45*x_3 - 1.3) + 0.0692244 - exp(-(-1.0*x_1 - 0.7)**2))**2)`
- icbr_no_shared formula (display, rounded):
  - `-2.66157*(0.0630025*cos(3.4*x_1 + 1.5) - 0.120459*cos(3.2*x_2 + 2.38419e-7) + 1 - 0.00712128*exp(-4.0*(0.125 - x_3)**2))**(3/2) + 0.440096*sin(0.430695*Abs(4.55*x_1 + 3.05) + 0.346337 - 18.2136*exp(-3.61*(1 - 0.210526*x_3)**2)) + 0.390024*sin(0.156078*(0.0399999 - x_2)**2 + 0.644805*cos(1.65*x_3 - 1.05) - 5.72645 + 3.26836*exp(-1.21*(x_1 + 0.454545)**2)) + 0.565953*cos(2.75439*atanh(0.2*x_3 + 0.5) + 0.0148429 + 3.31463*exp(-0.81*(0.555556 - x_1)**2)) + 2.61918`
- icbr_refit_commit formula (display, rounded):
  - `0.425083*sin(0.122569*(0.0209911 - x_2)**2 + 0.542092*cos(1.5234*x_3 - 1.09168) + 3.44448 - 2.18789*exp(-2.21593*(0.859949 - x_1)**2)) + 11.5068*cos(0.242548*sin(1.4096*x_1 + 0.60916) + 0.329391*tan(0.246*x_3 + 0.5003) + 3.01922) - 0.215649*Abs(-0.913553*Abs(2.93868*x_1 + 2.22868) + 1.84909 + 39.4191*exp(-3.9928*(0.188009*x_3 - 1)**2)) + 15.2895 - 10.2889*exp(-12.9178*(-0.00678558*cos(2.59516*x_1 - 1.61552) + 0.71551 - 0.00534657*exp(-0.228828*(0.0417259 - x_3)**2) - exp(-0.039888*(0.010014 - x_2)**2))**2)`

### task=trig_interaction seed=17

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.024746e-02, r2=0.986696
- Variant formula overview:
  - baseline: symbolic_s=1.521084e+01, imitation_mse=4.988997e-03, target_mse=1.451974e-02, formula_export_success=True
  - icbr_full: symbolic_s=1.036044e+00, imitation_mse=5.496401e-03, target_mse=1.515793e-02, formula_export_success=True
  - icbr_no_replay: symbolic_s=6.572466e-01, imitation_mse=5.450842e-03, target_mse=1.588085e-02, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.627134e+00, imitation_mse=5.496399e-03, target_mse=1.515791e-02, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.627796e+00, imitation_mse=1.080165e-01, target_mse=1.192906e-01, formula_export_success=True
- baseline formula (display, rounded):
  - `-1.42034*(-tan(0.4064*x_3 - 9.39992) + 0.426655*atan(2.32936*x_1 + 0.38392) - 0.146128)**2 - 1.54089*atan(0.21051*sin(3.10376*x_1 - 9.6076) + 0.456949 - 0.312899*exp(-2.20392*(0.0521636 - x_2)**2)) + 4.14541*atan(0.0907226*cos(3.4096*x_1 + 4.40824) + 0.486307 - 0.2853*exp(-0.2383*(-x_3 - 0.390855)**2) + 0.206045*exp(-2.16184*(-x_2 - 0.0297622)**2)) - 1.15356 + 0.874643*exp(-4.00803*(-0.312598*atan(0.84744*x_3 + 0.03672) + 0.304817 - exp(-1.43482*(-x_1 - 0.481734)**2))**2)`
- icbr_full formula (display, rounded):
  - `0.721546*(0.250156*cos(3.1*x_1 + 4.55) + 1 + 0.367625*exp(-2.25*(0.0666665 - x_2)**2))**(3/2) - 1.31132*(0.851271*asin(0.5*x_3 + 0.0500002) - 0.419214 + exp(-1.21*(-x_1 - 0.863636)**2))**2 - 4.77493*tanh(0.0799465*sin(3.4*x_1 - 3.45) + 0.0775297*cos(3.05*x_2 - 3.05) - 0.105528*cos(1.05*x_3 + 3.55) - 0.444853) - 2.79284 + 0.860404*exp(-4.14184*(-0.109903 + 0.672925*exp(-0.562499*(0.6*x_3 + 1)**2) - exp(-1.5625*(x_1 + 0.48)**2))**2)`
- icbr_no_replay formula (display, rounded):
  - `-0.950265*(asin(0.5*x_3 + 0.0500002) - 0.520062*atan(2.35*x_1 + 0.4) + 0.161767)**2 - 0.396599*cos(1.2199*atan(0.85*x_3 + 0.0500002) + 2.03292 + 3.83772*exp(-1.5625*(x_1 + 0.48)**2)) + 4.77493*tanh(-0.0799465*sin(3.4*x_1 - 3.45) + 0.0839776*sin(1.2*x_3 - 1.1) + 0.322988 + 0.179153*exp(-2.25*(-x_2 - 0.0333335)**2)) - 2.49636 + 2.49474*exp(-1.05162*(-0.147039*sin(3.1*x_1 + 2.95) - 1 + 0.216129*exp(-2.25*(0.0666665 - x_2)**2))**2)`
- icbr_no_shared formula (display, rounded):
  - `0.721546*(0.250156*cos(3.1*x_1 + 4.55) + 1 + 0.367625*exp(-2.25*(0.0666665 - x_2)**2))**(3/2) - 1.31132*(0.851271*asin(0.5*x_3 + 0.0500002) - 0.419214 + exp(-1.21*(-x_1 - 0.863636)**2))**2 - 4.77493*tanh(0.0799465*sin(3.4*x_1 - 3.45) + 0.0775297*cos(3.05*x_2 - 3.05) - 0.105528*cos(1.05*x_3 + 3.55) - 0.444853) - 2.79284 + 0.860404*exp(-4.14184*(-0.109903 + 0.672925*exp(-0.5625*(-0.6*x_3 - 1)**2) - exp(-1.5625*(-x_1 - 0.48)**2))**2)`
- icbr_refit_commit formula (display, rounded):
  - `-2.89739*tanh(0.104133*sin(2.15876*x_1 + 3.00956) + 0.68582 - 0.306282*exp(-0.81*(0.0599999 - x_2)**2)) - 6.47414*tanh(0.0534933*sin(2.23072*x_1 - 3.88556) - 1.5694*sin(0.42888*x_2 - 4.69804) - 0.0366094*tanh(2.40014*x_3 - 1.364) + 1.02069) - 1.88107 + 0.940009*exp(-53.9914*(-atanh(0.10024*x_3 + 0.0817599) + 0.186285 - 0.252122*exp(-0.801813*(-0.996114*x_1 - 1)**2))**2) - 0.701509*exp(-0.610494*(cos(0.86792*x_3 + 1.61536) + 0.737755*Abs(3.06276*x_1 + 1.8764) + 0.0554733)**2)`

### task=trig_interaction seed=18

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.727680e-03, r2=0.997576
- Variant formula overview:
  - baseline: symbolic_s=1.684367e+01, imitation_mse=3.963911e-03, target_mse=5.841968e-03, formula_export_success=True
  - icbr_full: symbolic_s=1.086249e+00, imitation_mse=2.352803e-03, target_mse=4.056174e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=7.014816e-01, imitation_mse=4.179232e-03, target_mse=5.822138e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.724706e+00, imitation_mse=2.352803e-03, target_mse=4.056173e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.669165e+00, imitation_mse=5.216579e-02, target_mse=5.660880e-02, formula_export_success=True
- baseline formula (display, rounded):
  - `-0.836825*sin(-0.0482731*cos(4.46184*x_2 + 3.18472) + 0.699191*tan(0.71688*x_3 + 3.46872) + 6.22052 + 2.88596*exp(-0.880895*(0.588391 - x_1)**2)) - 0.238397*cos(1.1157*asin(0.7876*x_3 + 0.14528) - 18.0213 + 10.1592*exp(-0.16*(-x_1 - 0.63)**2)) + 0.257222*cos(0.910234*atan(1.12336*x_3 - 0.60368) + 4.54859 + 3.8196*exp(-0.517248*(-x_1 - 0.561401)**2)) + 1.86103*atan(0.0337788*(-x_3 - 0.181548)**5 + 0.226361*cos(3.00056*x_1 + 4.79056) - 0.194393 + 0.647933*exp(-2.32672*(-x_2 - 0.000209787)**2)) - 0.0507699`
- icbr_full formula (display, rounded):
  - `-0.251532*cos(4.07192*cos(0.85*x_1 - 2.6) - 1.03244*asin(0.8*x_3 + 0.15) + 5.74224) - 0.25261*cos(0.493923*Abs(4.0*x_1 + 2.15) - 10.1862 + 5.56174*exp(-0.09*(-0.833333*x_3 - 1)**2)) - 0.794057*cos(0.703344*tan(0.75*x_3 + 0.3) - 1.70744 + 3.0022*exp(-0.9025*(x_1 - 0.578947)**2) + 0.0977089*exp(-8.41*(0.0344827 - x_2)**2)) + 1.71366 - 3.078*exp(-0.350825*(-0.0403783*(-x_3 - 0.181818)**5 + 0.271016*sin(3.0*x_1 - 3.05) - 1 - 0.766985*exp(-2.4025*(-x_2 - 1.53818e-7)**2))**2)`
- icbr_no_replay formula (display, rounded):
  - `-0.858056*sin(0.0475094*cos(4.45*x_2 + 0.0500002) + 0.66427*tan(0.75*x_3 + 0.3) - 6.29041 + 2.83541*exp(-0.9025*(x_1 - 0.578947)**2)) - 0.25261*cos(0.905789*atan(1.15*x_3 - 0.6) + 1.26709 + 3.97714*exp(-0.489999*(x_1 + 0.571429)**2)) + 1.91088*atan(0.0328849*(-x_3 - 0.181818)**5 + 0.220516*cos(3.0*x_1 - 1.5) - 0.166563 + 0.624648*exp(-2.4025*(-x_2 - 1.53818e-7)**2)) - 0.403803 + 0.594361*exp(-4.57083*(-sin(0.8*x_1 - 1.05) + 0.231798*asin(0.8*x_3 + 0.15) - 0.668296)**2)`
- icbr_no_shared formula (display, rounded):
  - `-0.251532*cos(4.07192*cos(0.85*x_1 - 2.6) - 1.03244*asin(0.8*x_3 + 0.15) + 5.74224) - 0.25261*cos(0.493923*Abs(4.0*x_1 + 2.15) - 10.1862 + 5.56174*exp(-0.09*(-0.833333*x_3 - 1)**2)) - 0.794057*cos(0.703344*tan(0.75*x_3 + 0.3) - 1.70744 + 3.0022*exp(-0.9025*(x_1 - 0.578947)**2) + 0.0977089*exp(-8.41*(0.0344827 - x_2)**2)) + 1.71366 - 3.078*exp(-0.350825*(-0.0403783*(x_3 + 0.181818)**5 - 0.271016*sin(3.0*x_1 - 3.05) + 1 + 0.766985*exp(-2.4025*(-x_2 - 1.53818e-7)**2))**2)`
- icbr_refit_commit formula (display, rounded):
  - `-1.482*sin(0.0299892*(-x_3 - 0.258256)**5 + 0.245303*sin(2.15268*x_1 + 0.0905199) + 11.6501*cos(0.37388*x_2) - 14.3275) - 0.591212*cos(0.340551*sin(0.82972*x_2 + 4.7002) - 0.923421*tan(0.71668*x_3 - 2.8136) - 1.30993 + 3.15899*exp(-1.51457*(-x_1 - 0.89661)**2)) - 0.21385*Abs(49.0051*cos(0.19932*x_1 + 3.29508) - 3.44263*tan(0.12236*x_3 + 3.90508) + 50.8752) - 9.42115 + 9.61748*exp(-0.0559212*(-0.286217*Abs(2.48912*x_1 + 1.45216) + 0.428653*atan(0.94472*x_3 - 0.65128) + 1)**2)`

### task=trig_interaction seed=19

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=3.354001e-03, r2=0.995467
- Variant formula overview:
  - baseline: symbolic_s=1.920244e+01, imitation_mse=3.198225e-03, target_mse=7.500532e-03, formula_export_success=True
  - icbr_full: symbolic_s=1.280123e+00, imitation_mse=1.317998e-03, target_mse=4.911054e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=8.117198e-01, imitation_mse=1.541177e-03, target_mse=5.245027e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.985252e+00, imitation_mse=1.317065e-03, target_mse=4.909575e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.906662e+00, imitation_mse=9.435110e-02, target_mse=1.046610e-01, formula_export_success=True
- baseline formula (display, rounded):
  - `-0.776596*cos(1.04484*tanh(1.22216*x_3 - 1.03592) + 6.17809 + 1.61322*exp(-1.84829*(0.514888 - x_1)**2) + 0.498156*exp(-2.29292*(0.0036454 - x_2)**2)) - 0.840001*tan(0.309333*cos(2.47976*x_1 - 4.59856) - 0.180184*cos(2.05504*x_2 + 0.00455999) + 0.380722*atanh(0.4636*x_3 + 0.42208) - 9.30219) - 3.60133*atan(0.28383*cos(4.122*x_1 + 1.40496) - 3.22395 + 2.20686*exp(-0.129312*(-0.922803*x_3 - 1)**2) - 0.585558*exp(-3.39237*(-x_2 - 0.00208487)**2)) - 4.38097 + 1.9344*exp(-1.89603*(-0.0370274*cos(3.58216*x_2 + 3.19992) - atan(0.35376*x_3 + 0.17008) + 0.410018 - 0.722604*exp(-0.773696*(-x_1 - 0.669668)**2))**2)`
- icbr_full formula (display, rounded):
  - `-0.886254*exp(-0.766206*sin(0.75*x_3 - 0.75) - 0.25907*cos(4.1*x_1 + 4.55) - 0.533111*exp(-3.4225*(-x_2 - 1.28875e-7)**2)) + 0.752746*cos(-4.31706 + 0.514933*exp(-2.25*(-x_2 - 1.58946e-7)**2) + 1.65702*exp(-1.8225*(x_1 - 0.518519)**2) + 1.78768*exp(-2.1025*(1 - 0.586207*x_3)**2)) + 0.746546*cos(3.3038*(1 - 0.211111*x_3)**(3/2) - 0.114906*sin(3.6*x_2 - 1.5) + 0.338604*Abs(4.1*x_1 + 2.6) - 4.97136) + 0.861091*tan(0.441866*sqrt(1 - 0.958763*x_3) + 0.297534*cos(2.5*x_1 - 1.45) + 0.173518*cos(2.05*x_2 + 2.38419e-7) + 2.37408) + 1.58666`
- icbr_no_replay formula (display, rounded):
  - `-0.819274*sin(1.03992*tanh(1.2*x_3 - 1.05) - 4.77802 + 0.481712*exp(-2.25*(-x_2 - 1.58946e-7)**2) + 1.55012*exp(-1.8225*(x_1 - 0.518519)**2)) + 0.746546*cos(0.114913*cos(3.6*x_2 + 0.0500002) + 0.338604*Abs(4.1*x_1 + 2.6) - 4.7794 + 6.40963*exp(-0.7225*(-0.235294*x_3 - 1)**2)) + 0.861091*tan(0.441866*sqrt(1 - 0.958763*x_3) + 0.297534*cos(2.5*x_1 - 1.45) + 0.173518*cos(2.05*x_2 + 2.38419e-7) + 2.37408) + 2.05163 + 1.28355/(-0.176807*sin(0.75*x_3 - 0.75) - 0.0597818*cos(4.1*x_1 + 4.55) - 1 - 0.123018*exp(-3.4225*(-x_2 - 1.28875e-7)**2))**3`
- icbr_no_shared formula (display, rounded):
  - `-0.886254*exp(-0.766206*sin(0.75*x_3 - 0.75) - 0.25907*cos(4.1*x_1 + 4.55) - 0.533111*exp(-3.4225*(-x_2 - 1.28875e-7)**2)) + 0.752746*cos(-4.31706 + 0.514933*exp(-2.25*(-x_2 - 1.58946e-7)**2) + 1.65702*exp(-1.8225*(x_1 - 0.518519)**2) + 1.78768*exp(-2.1025*(1 - 0.586207*x_3)**2)) + 0.746546*cos(3.3038*(1 - 0.211111*x_3)**(3/2) - 0.114906*sin(3.6*x_2 - 1.5) + 0.338604*Abs(4.1*x_1 + 2.6) - 4.97136) + 0.861091*tan(0.442479*sqrt(1 - 0.957895*x_3) + 0.297534*cos(2.5*x_1 - 1.45) + 0.173518*cos(2.05*x_2 + 2.38419e-7) + 2.37343) + 1.58666`
- icbr_refit_commit formula (display, rounded):
  - `-1278.43*exp(-0.278787*(x_3 + 0.999802)**(3/2) - 0.111542*sin(2.39732*x_1 - 0.0971199) - 6.93815*cos(0.40364*x_2 + 0.00404)) + 1.36237*log(1.36106*sqrt(1 - 0.98119*x_3) - 0.93426*cos(2.14196*x_1 + 1.70172) - 0.195095*Abs(4.498*x_2 + 4.00001e-5) + 3.61505) + 0.243939*Abs(0.538523*(0.500231*x_3 + 1)**4 - 0.267385*Abs(3.86492*x_2 - 0.01592) + 1.82034 - 3.08297*exp(-2.05223*(x_1 + 0.746245)**2)) - 2.14993 + 1.34718*exp(-15.3614*(0.523226*(1 - 0.212272*x_3)**(3/2) + 0.221911*cos(0.61512*x_2 + 0.00608) + 0.050471*Abs(4.07672*x_1 + 2.96024) - 1)**2)`

### task=trig_interaction seed=20

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.767333e-03, r2=0.997637
- Variant formula overview:
  - baseline: symbolic_s=1.404545e+01, imitation_mse=2.759116e-03, target_mse=2.579492e-03, formula_export_success=True
  - icbr_full: symbolic_s=9.344066e-01, imitation_mse=3.276320e-03, target_mse=3.177765e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=6.959784e-01, imitation_mse=3.208132e-03, target_mse=3.121142e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.464618e+00, imitation_mse=3.276320e-03, target_mse=3.177764e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.422459e+00, imitation_mse=nan, target_mse=nan, formula_export_success=True
- baseline formula (display, rounded):
  - `-6.00886*(-0.554619*log(7.93128 - 3.25904*x_3) - 0.0286525*cos(2.3992*x_2 + 3.18864) - 0.110111*tan(1.18168*x_1 - 3.21456) + 1)**2 + 1.57603*cos(1.61692*sin(0.4312*x_3 - 2.20768) - 0.167537*cos(2.83592*x_2 - 9.39584) + 7.66877 - 1.31951*exp(-2.20653*(-x_1 - 0.55321)**2)) + 2.04337*atan(0.406511*sin(3.04296*x_1 - 0.19672) + 0.296546*sin(1.188*x_3 - 1.59648) - 0.562264 + 0.503971*exp(-2.58463*(0.00582205 - x_2)**2)) - 0.00563684`
- icbr_full formula (display, rounded):
  - `-112.574*(0.0267025*tan(1.15*x_1 + 3.05) + 0.296054 - 0.0173896*exp(-1.1025*(-x_2 - 2.27065e-7)**2) - 1/(4.0 - 0.85*x_3))**2 - 1.84487*cos(0.25439*(1 - x_3)**(3/2) - 0.580234*sin(2.55*x_1 + 3.0) + 0.151479*cos(2.85*x_2 + 0.0500002) - 3.89879) - 2.509 + 4.12451*exp(-1.38413*(0.203813*sin(3.05*x_1 + 2.95) + 0.0986579*cos(1.5*x_3 - 0.0499997) + 1 - 0.253437*exp(-2.56*(-x_2 - 1.49012e-7)**2))**2)`
- icbr_no_replay formula (display, rounded):
  - `-3.31606*(0.748683*log(5.0 - 2.05*x_3) - 0.0385696*cos(2.4*x_2 + 0.0500002) + 0.155583*tan(1.15*x_1 + 3.05) - 1)**2 + 1.4093*sin(0.685731*sin(2.55*x_1 + 3.0) + 0.178866*sin(2.85*x_2 - 1.55) - 1.60966*sin(0.45*x_3 + 4.05) + 0.886183) + 2.00003*atan(0.194658*(0.0166666 - x_3)**2 - 0.419623*sin(3.05*x_1 + 2.95) + 0.22989*sin(3.2*x_2 + 1.55) - 0.597494) + 0.161583`
- icbr_no_shared formula (display, rounded):
  - `-112.574*(0.0267025*tan(1.15*x_1 + 3.05) + 0.296054 - 0.0173896*exp(-1.1025*(-x_2 - 2.27065e-7)**2) - 1/(4.0 - 0.85*x_3))**2 - 1.84487*cos(0.25439*(1 - x_3)**(3/2) - 0.580234*sin(2.55*x_1 + 3.0) + 0.151479*cos(2.85*x_2 + 0.0500002) - 3.89879) - 2.509 + 4.12451*exp(-1.38413*(0.203813*sin(3.05*x_1 + 2.95) + 0.0986579*cos(1.5*x_3 - 0.0499997) + 1 - 0.253437*exp(-2.56*(-x_2 - 1.49012e-7)**2))**2)`
- icbr_refit_commit formula (display, rounded):
  - `-17.478*sin(0.0727043*(0.997492 - x_3)**(3/2) + 0.160182*sin(2.2524*x_1 - 0.0943599) - 0.0185146*Abs(4.99993*x_2 + 0.0999999) + 4.52286) + 21.0851*cos(0.136077*(1 - 0.300928*x_1)**3 + 0.345769*tan(0.166*x_3 + 0.89972) - 0.00706446*Abs(4.99692*x_2 + 0.0999999) - 0.680032) - 39.2223 + 4.02068*exp(-31.3663*(0.0189799*(0.0260231 - x_3)**2 - 0.038049*sin(2.14304*x_1 + 3.00124) + 0.821036*cos(0.36792*x_2 - 0.00408) - 1)**2)`

## Visualization Summary

- `icbr_benchmark_symbolic_time_errorbar.png`
- `icbr_benchmark_speedup_boxplot.png`
- `icbr_benchmark_mse_shift_boxplot.png`
- `icbr_benchmark_variant_overview.png`
- `icbr_benchmark_q123_evidence_by_task.png`
## Visualization Design Guide

- `Point + 95% CI`: 适合论文里的主结论图；正值偏态指标优先用几何均值与 log 轴，不用柱面积暗示额外量感。
- `Violin + Box + Points`: 适合 speedup / imitation_mse_shift 这类分布图；当前固定 KDE 带宽规则为 `Silverman`。
- `Task-Row Two-Panel Grid`: 适合 variant overview；每个 task 一行，左列 `SymbolicTime`，右列合并 `ImitationMSE + TargetMSE`，两列都显式标尺度。
- `Q1/Q2/Q3`: 三个 panel 都用相对 `icbr_full` 的 ratio 值，并在 log 轴上展示 `几何均值 + 95% CI`，1 表示与 full 持平。
- `Recommended Combo`: A=point+95%CI（正值偏态指标用几何均值），B=violin+box+points（分布），C=task-row two-panel grid（多指标 overview）。

## Extensibility Notes

- 任务可扩展：在任务解析层新增 task token 或 task spec，即可复用统一导出与统计管线。
- 统计可扩展：新增 benchmark 指标后，可自动进入 task stats（count/mean/median/std/min/max）。
- 显著性可扩展：可在 `_SIGNIFICANCE_DIRECTIONS` 增加需要方向性判断的 delta 指标。
- 门禁可扩展：可在 `_TaskSpec` 中为单任务覆盖 teacher MSE/R2 阈值。
