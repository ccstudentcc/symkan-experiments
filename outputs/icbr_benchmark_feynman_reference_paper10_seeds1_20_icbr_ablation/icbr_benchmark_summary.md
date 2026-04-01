# ICBR Benchmark Summary

## Run Config

- Profile: feynman_reference
- Run mode: full
- Tasks: feynman_I_9_18, feynman_I_10_7, feynman_I_12_1, feynman_I_12_4, feynman_I_6_2a, feynman_I_34_1, feynman_II_6_15a, feynman_II_6_15b, feynman_II_21_32, feynman_II_34_29a
- Seeds: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20
- Train/Calibration/Test samples per task: 2000/1000/1000
- Train steps: 200, lr: 0.01, lamb: 0.01
- Teacher cache: mode=readonly, dir=outputs\teacher_cache_feynman_reference_paper10_seeds1_20, version=stage24_feynman_reference_paper10_seeds1_20_v1
- ICBR shortlist topk: 3, grid_number: 21, iteration: 2
- Variants: icbr_full, icbr_no_replay, icbr_no_shared, icbr_refit_commit
- Teacher prune policy: enabled=False, node_th=0.01, edge_th=0.01, prune_iters=3
- Feynman data: root=datasets, variant=Feynman_with_units, split=random, split_seed=per-benchmark-seed, select_seed=1, width_mid=[5, 2], prune_iters=3

## Task-Level Aggregate Stats

| task | n | teacher_cache_hit_mean | teacher_mse_mean | teacher_r2_mean | teacher_gate_pass_mean | baseline_symbolic_mean | icbr_symbolic_mean | delta_mean | delta_median | speedup_mean | speedup_median | imitation_mse_shift_mean | target_mse_shift_mean | formula_export_success_mean |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| feynman_I_9_18 | 20 | 1.0000 | 1.434354e-02 | 0.054338 | 1.0000 | nan | 0.968160 | nan | nan | nan | nan | nan | nan | 1.0000 |
| feynman_I_10_7 | 20 | 1.0000 | 6.207134e-03 | 0.995763 | 1.0000 | nan | 2.895988 | nan | nan | nan | nan | nan | nan | 1.0000 |
| feynman_I_12_1 | 20 | 1.0000 | 2.977085e-02 | 0.998782 | 0.9500 | nan | 2.682568 | nan | nan | nan | nan | nan | nan | 0.9500 |
| feynman_I_12_4 | 20 | 1.0000 | 9.069696e-04 | -0.330897 | 1.0000 | nan | 0.912785 | nan | nan | nan | nan | nan | nan | 1.0000 |
| feynman_I_6_2a | 20 | 1.0000 | 6.128534e-03 | -0.224731 | 1.0000 | nan | 0.237950 | nan | nan | nan | nan | nan | nan | 1.0000 |
| feynman_I_34_1 | 20 | 1.0000 | 2.289391e-02 | 0.992881 | 1.0000 | nan | 3.335848 | nan | nan | nan | nan | nan | nan | 1.0000 |
| feynman_II_6_15a | 20 | 1.0000 | 1.330638e-02 | 0.898912 | 1.0000 | nan | 0.971247 | nan | nan | nan | nan | nan | nan | 1.0000 |
| feynman_II_6_15b | 20 | 1.0000 | 9.358341e-04 | -0.074641 | 1.0000 | nan | 0.327013 | nan | nan | nan | nan | nan | nan | 1.0000 |
| feynman_II_21_32 | 20 | 1.0000 | 2.353139e-03 | -0.050908 | 1.0000 | nan | 1.224305 | nan | nan | nan | nan | nan | nan | 1.0000 |
| feynman_II_34_29a | 20 | 1.0000 | 2.523925e-03 | 0.949847 | 1.0000 | nan | 0.966706 | nan | nan | nan | nan | nan | nan | 1.0000 |

## Statistical Significance (by task)

| task | metric | favorable_direction | n_total | n_finite | n_effective | improved | worsened | ties | p_value_two_sided | mean_delta_ci95 |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| feynman_I_9_18 | symbolic_wall_time_delta_s | positive | 20 | 0 | 0 | 0 | 0 | 0 | nan | [nan, nan] |
| feynman_I_9_18 | imitation_mse_shift | negative | 20 | 0 | 0 | 0 | 0 | 0 | nan | [nan, nan] |
| feynman_I_10_7 | symbolic_wall_time_delta_s | positive | 20 | 0 | 0 | 0 | 0 | 0 | nan | [nan, nan] |
| feynman_I_10_7 | imitation_mse_shift | negative | 20 | 0 | 0 | 0 | 0 | 0 | nan | [nan, nan] |
| feynman_I_12_1 | symbolic_wall_time_delta_s | positive | 20 | 0 | 0 | 0 | 0 | 0 | nan | [nan, nan] |
| feynman_I_12_1 | imitation_mse_shift | negative | 20 | 0 | 0 | 0 | 0 | 0 | nan | [nan, nan] |
| feynman_I_12_4 | symbolic_wall_time_delta_s | positive | 20 | 0 | 0 | 0 | 0 | 0 | nan | [nan, nan] |
| feynman_I_12_4 | imitation_mse_shift | negative | 20 | 0 | 0 | 0 | 0 | 0 | nan | [nan, nan] |
| feynman_I_6_2a | symbolic_wall_time_delta_s | positive | 20 | 0 | 0 | 0 | 0 | 0 | nan | [nan, nan] |
| feynman_I_6_2a | imitation_mse_shift | negative | 20 | 0 | 0 | 0 | 0 | 0 | nan | [nan, nan] |
| feynman_I_34_1 | symbolic_wall_time_delta_s | positive | 20 | 0 | 0 | 0 | 0 | 0 | nan | [nan, nan] |
| feynman_I_34_1 | imitation_mse_shift | negative | 20 | 0 | 0 | 0 | 0 | 0 | nan | [nan, nan] |
| feynman_II_6_15a | symbolic_wall_time_delta_s | positive | 20 | 0 | 0 | 0 | 0 | 0 | nan | [nan, nan] |
| feynman_II_6_15a | imitation_mse_shift | negative | 20 | 0 | 0 | 0 | 0 | 0 | nan | [nan, nan] |
| feynman_II_6_15b | symbolic_wall_time_delta_s | positive | 20 | 0 | 0 | 0 | 0 | 0 | nan | [nan, nan] |
| feynman_II_6_15b | imitation_mse_shift | negative | 20 | 0 | 0 | 0 | 0 | 0 | nan | [nan, nan] |
| feynman_II_21_32 | symbolic_wall_time_delta_s | positive | 20 | 0 | 0 | 0 | 0 | 0 | nan | [nan, nan] |
| feynman_II_21_32 | imitation_mse_shift | negative | 20 | 0 | 0 | 0 | 0 | 0 | nan | [nan, nan] |
| feynman_II_34_29a | symbolic_wall_time_delta_s | positive | 20 | 0 | 0 | 0 | 0 | 0 | nan | [nan, nan] |
| feynman_II_34_29a | imitation_mse_shift | negative | 20 | 0 | 0 | 0 | 0 | 0 | nan | [nan, nan] |

## Variant Ablation Aggregate Stats (Stage 15)

| task | variant | n | teacher_gate_pass_mean | formula_export_success_mean | symbolic_mean_s | speedup_mean_x | imitation_mse_shift_mean | target_mse_shift_mean | replay_rank_inversion_mean | refit_drift_l2_mean |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| feynman_I_9_18 | icbr_full | 20 | 1.0000 | 1.0000 | 0.968160 | nan | nan | nan | 0.229957 | nan |
| feynman_I_9_18 | icbr_no_replay | 20 | 1.0000 | 1.0000 | 0.689077 | nan | nan | nan | nan | nan |
| feynman_I_9_18 | icbr_no_shared | 20 | 1.0000 | 1.0000 | 1.275075 | nan | nan | nan | 0.241645 | nan |
| feynman_I_9_18 | icbr_refit_commit | 20 | 1.0000 | 1.0000 | 1.642133 | nan | nan | nan | 0.216323 | 1.744097e+00 |
| feynman_I_10_7 | icbr_full | 20 | 1.0000 | 1.0000 | 2.895988 | nan | nan | nan | 0.532798 | nan |
| feynman_I_10_7 | icbr_no_replay | 20 | 1.0000 | 1.0000 | 1.874595 | nan | nan | nan | nan | nan |
| feynman_I_10_7 | icbr_no_shared | 20 | 1.0000 | 1.0000 | 4.223814 | nan | nan | nan | 0.512534 | nan |
| feynman_I_10_7 | icbr_refit_commit | 20 | 1.0000 | 1.0000 | 5.358576 | nan | nan | nan | 0.539151 | 1.484242e+01 |
| feynman_I_12_1 | icbr_full | 20 | 0.9500 | 0.9500 | 2.682568 | nan | nan | nan | 0.455297 | nan |
| feynman_I_12_1 | icbr_no_replay | 20 | 0.9500 | 0.9500 | 1.768385 | nan | nan | nan | nan | nan |
| feynman_I_12_1 | icbr_no_shared | 20 | 0.9500 | 0.9500 | 3.965919 | nan | nan | nan | 0.446174 | nan |
| feynman_I_12_1 | icbr_refit_commit | 20 | 0.9500 | 0.9500 | 4.737719 | nan | nan | nan | 0.485147 | 1.266772e+01 |
| feynman_I_12_4 | icbr_full | 20 | 1.0000 | 1.0000 | 0.912785 | nan | nan | nan | 0.384811 | nan |
| feynman_I_12_4 | icbr_no_replay | 20 | 1.0000 | 1.0000 | 0.672160 | nan | nan | nan | nan | nan |
| feynman_I_12_4 | icbr_no_shared | 20 | 1.0000 | 1.0000 | 1.233151 | nan | nan | nan | 0.393583 | nan |
| feynman_I_12_4 | icbr_refit_commit | 20 | 1.0000 | 1.0000 | 1.546741 | nan | nan | nan | 0.453455 | 2.932771e+00 |
| feynman_I_6_2a | icbr_full | 20 | 1.0000 | 1.0000 | 0.237950 | nan | nan | nan | 0.296667 | nan |
| feynman_I_6_2a | icbr_no_replay | 20 | 1.0000 | 1.0000 | 0.221079 | nan | nan | nan | nan | nan |
| feynman_I_6_2a | icbr_no_shared | 20 | 1.0000 | 1.0000 | 0.247179 | nan | nan | nan | 0.296667 | nan |
| feynman_I_6_2a | icbr_refit_commit | 20 | 1.0000 | 1.0000 | 0.391683 | nan | nan | nan | 0.330000 | 3.019073e+00 |
| feynman_I_34_1 | icbr_full | 20 | 1.0000 | 1.0000 | 3.335848 | nan | nan | nan | 0.510442 | nan |
| feynman_I_34_1 | icbr_no_replay | 20 | 1.0000 | 1.0000 | 2.131929 | nan | nan | nan | nan | nan |
| feynman_I_34_1 | icbr_no_shared | 20 | 1.0000 | 1.0000 | 4.947857 | nan | nan | nan | 0.516587 | nan |
| feynman_I_34_1 | icbr_refit_commit | 20 | 1.0000 | 1.0000 | 6.075297 | nan | nan | nan | 0.536960 | 1.547089e+01 |
| feynman_II_6_15a | icbr_full | 20 | 1.0000 | 1.0000 | 0.971247 | nan | nan | nan | 0.343525 | nan |
| feynman_II_6_15a | icbr_no_replay | 20 | 1.0000 | 1.0000 | 0.774910 | nan | nan | nan | nan | nan |
| feynman_II_6_15a | icbr_no_shared | 20 | 1.0000 | 1.0000 | 1.378717 | nan | nan | nan | 0.349080 | nan |
| feynman_II_6_15a | icbr_refit_commit | 20 | 1.0000 | 1.0000 | 1.704460 | nan | nan | nan | 0.374064 | 4.957933e+00 |
| feynman_II_6_15b | icbr_full | 20 | 1.0000 | 1.0000 | 0.327013 | nan | nan | nan | 0.406173 | nan |
| feynman_II_6_15b | icbr_no_replay | 20 | 1.0000 | 1.0000 | 0.248877 | nan | nan | nan | nan | nan |
| feynman_II_6_15b | icbr_no_shared | 20 | 1.0000 | 1.0000 | 0.403914 | nan | nan | nan | 0.406173 | nan |
| feynman_II_6_15b | icbr_refit_commit | 20 | 1.0000 | 1.0000 | 0.559634 | nan | nan | nan | 0.464815 | 2.002894e+00 |
| feynman_II_21_32 | icbr_full | 20 | 1.0000 | 1.0000 | 1.224305 | nan | nan | nan | 0.341692 | nan |
| feynman_II_21_32 | icbr_no_replay | 20 | 1.0000 | 1.0000 | 0.824308 | nan | nan | nan | nan | nan |
| feynman_II_21_32 | icbr_no_shared | 20 | 1.0000 | 1.0000 | 1.708871 | nan | nan | nan | 0.337153 | nan |
| feynman_II_21_32 | icbr_refit_commit | 20 | 1.0000 | 1.0000 | 2.093813 | nan | nan | nan | 0.377634 | 4.693955e+00 |
| feynman_II_34_29a | icbr_full | 20 | 1.0000 | 1.0000 | 0.966706 | nan | nan | nan | 0.383515 | nan |
| feynman_II_34_29a | icbr_no_replay | 20 | 1.0000 | 1.0000 | 0.759923 | nan | nan | nan | nan | nan |
| feynman_II_34_29a | icbr_no_shared | 20 | 1.0000 | 1.0000 | 1.301272 | nan | nan | nan | 0.369030 | nan |
| feynman_II_34_29a | icbr_refit_commit | 20 | 1.0000 | 1.0000 | 1.779952 | nan | nan | nan | 0.357108 | 2.083976e+00 |

## Critique Evidence Summary (Q1/Q2/Q3)

| task | n | q1_candidate_ratio_mean | q1_symbolic_ratio_mean | q2_imitation_mse_gain_mean | q2_target_mse_gain_mean | q2_rank_inversion_mean | q3_imitation_mse_gain_mean | q3_target_mse_gain_mean | q3_refit_drift_mean |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| __overall__ | 199 | 1.343141 | 1.295932 | 1.009572e-02 | 1.058437e-02 | 0.390127 | 1.076520e-02 | 1.073953e-02 | 6.812217e+00 |
| feynman_I_9_18 | 20 | 1.351033 | 1.228955 | 3.178100e-08 | 7.079681e-07 | 0.229957 | 4.357936e-07 | 2.514361e-06 | 1.744097e+00 |
| feynman_I_10_7 | 20 | 1.704277 | 1.457429 | 6.871279e-04 | 6.357850e-04 | 0.532798 | 4.321613e-04 | 3.551870e-04 | 1.484242e+01 |
| feynman_I_12_1 | 19 | 1.714456 | 1.475155 | 1.068458e-01 | 1.096358e-01 | 0.455297 | 1.387751e-01 | 1.430248e-01 | 1.266772e+01 |
| feynman_I_12_4 | 20 | 1.294202 | 1.240570 | 2.989111e-09 | -1.239343e-07 | 0.384811 | 4.803087e-09 | 1.076260e-07 | 2.932771e+00 |
| feynman_I_6_2a | 20 | 0.763738 | 0.984012 | 5.410277e-07 | 9.740834e-07 | 0.296667 | 7.942114e-06 | 9.299432e-06 | 3.019073e+00 |
| feynman_I_34_1 | 20 | 1.755688 | 1.483258 | 2.742841e-03 | 5.278775e-03 | 0.510442 | 4.892615e-03 | 2.991535e-03 | 1.547089e+01 |
| feynman_II_6_15a | 20 | 1.552556 | 1.420277 | -2.350287e-05 | -1.277892e-04 | 0.343525 | 2.267610e-03 | 1.019839e-03 | 4.957933e+00 |
| feynman_II_6_15b | 20 | 0.575331 | 1.086951 | 2.402042e-10 | -7.587078e-08 | 0.406173 | 1.565042e-09 | 5.079384e-09 | 2.002894e+00 |
| feynman_II_21_32 | 20 | 1.286401 | 1.259820 | 1.201628e-06 | 3.045937e-06 | 0.341692 | 1.132181e-05 | -1.120157e-05 | 4.693955e+00 |
| feynman_II_34_29a | 20 | 1.452290 | 1.331852 | 1.058586e-05 | 5.643545e-05 | 0.383515 | 2.768742e-04 | 4.748629e-05 | 2.083976e+00 |

## Per-Run Performance Details

| task | seed | cache_hit | cache_status | teacher_mse | teacher_r2 | teacher_gate | candidate_s | replay_s | baseline_symbolic_s | icbr_symbolic_s | speedup_x | baseline_imitation_mse | icbr_imitation_mse | imitation_mse_shift | baseline_target_mse | icbr_target_mse | target_mse_shift | formula_export_success |
|---|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| feynman_I_9_18 | 1 | True | hit | 1.630265e-02 | -0.003680 | True | 0.824190 | 0.320311 | nan | 1.258657 | nan | nan | 1.114276e-08 | nan | nan | 1.630319e-02 | nan | True |
| feynman_I_9_18 | 2 | True | hit | 1.497844e-02 | 0.000232 | True | 1.395445 | 0.686530 | nan | 2.323648 | nan | nan | 8.799262e-09 | nan | nan | 1.498076e-02 | nan | True |
| feynman_I_9_18 | 3 | True | hit | 1.347480e-02 | -0.000924 | True | 0.285046 | 0.037119 | nan | 0.342061 | nan | nan | 1.153306e-08 | nan | nan | 1.347650e-02 | nan | True |
| feynman_I_9_18 | 4 | True | hit | 1.371062e-02 | 0.000294 | True | 0.759420 | 0.285538 | nan | 1.151719 | nan | nan | 1.835985e-08 | nan | nan | 1.370914e-02 | nan | True |
| feynman_I_9_18 | 5 | True | hit | 1.844272e-02 | -0.313000 | True | 0.797533 | 0.176903 | nan | 1.040506 | nan | nan | 3.111923e-11 | nan | nan | 1.844273e-02 | nan | True |
| feynman_I_9_18 | 6 | True | hit | 1.477381e-02 | 0.000836 | True | 0.286473 | 0.036290 | nan | 0.346058 | nan | nan | 1.723541e-08 | nan | nan | 1.477232e-02 | nan | True |
| feynman_I_9_18 | 7 | True | hit | 1.719902e-02 | -0.000011 | True | 0.589960 | 0.196794 | nan | 0.866521 | nan | nan | 1.289530e-08 | nan | nan | 1.719774e-02 | nan | True |
| feynman_I_9_18 | 8 | True | hit | 1.898704e-02 | -0.085501 | True | 0.263680 | 0.037747 | nan | 0.321564 | nan | nan | 1.571844e-09 | nan | nan | 1.898681e-02 | nan | True |
| feynman_I_9_18 | 9 | True | hit | 1.678944e-02 | -0.000845 | True | 0.780641 | 0.310398 | nan | 1.205051 | nan | nan | 1.348650e-08 | nan | nan | 1.679214e-02 | nan | True |
| feynman_I_9_18 | 10 | True | hit | 1.557820e-02 | -0.001530 | True | 0.271416 | 0.035503 | nan | 0.326864 | nan | nan | 5.759627e-09 | nan | nan | 1.557777e-02 | nan | True |
| feynman_I_9_18 | 11 | True | hit | 1.698013e-02 | 0.000495 | True | 1.231186 | 0.551308 | nan | 1.983035 | nan | nan | 2.056279e-08 | nan | nan | 1.698070e-02 | nan | True |
| feynman_I_9_18 | 12 | True | hit | 1.457448e-02 | 0.000613 | True | 0.640104 | 0.229389 | nan | 0.956721 | nan | nan | 1.056017e-08 | nan | nan | 1.457146e-02 | nan | True |
| feynman_I_9_18 | 13 | True | hit | 5.796647e-03 | 0.616056 | True | 1.161896 | 0.480813 | nan | 1.814029 | nan | nan | 3.987592e-05 | nan | nan | 5.712926e-03 | nan | True |
| feynman_I_9_18 | 14 | True | hit | 1.483851e-02 | -0.001558 | True | 0.273705 | 0.040448 | nan | 0.335585 | nan | nan | 6.065010e-09 | nan | nan | 1.483736e-02 | nan | True |
| feynman_I_9_18 | 15 | True | hit | 6.399109e-03 | 0.607449 | True | 0.649679 | 0.140379 | nan | 0.844593 | nan | nan | 3.747870e-05 | nan | nan | 6.328515e-03 | nan | True |
| feynman_I_9_18 | 16 | True | hit | 1.450734e-02 | -0.000488 | True | 0.592910 | 0.210157 | nan | 0.884706 | nan | nan | 1.874476e-08 | nan | nan | 1.450795e-02 | nan | True |
| feynman_I_9_18 | 17 | True | hit | 1.367797e-02 | 0.000793 | True | 0.937104 | 0.381327 | nan | 1.463040 | nan | nan | 3.154301e-08 | nan | nan | 1.368139e-02 | nan | True |
| feynman_I_9_18 | 18 | True | hit | 1.623747e-02 | -0.008441 | True | 0.505756 | 0.148707 | nan | 0.714668 | nan | nan | 3.213075e-08 | nan | nan | 1.623518e-02 | nan | True |
| feynman_I_9_18 | 19 | True | hit | 9.563173e-03 | 0.289152 | True | 0.560721 | 0.198419 | nan | 0.840103 | nan | nan | 2.026287e-05 | nan | nan | 9.533228e-03 | nan | True |
| feynman_I_9_18 | 20 | True | hit | 1.405925e-02 | -0.013190 | True | 0.282082 | 0.041743 | nan | 0.344077 | nan | nan | 1.631059e-07 | nan | nan | 1.405848e-02 | nan | True |
| feynman_I_10_7 | 1 | True | hit | 3.003362e-03 | 0.997856 | True | 2.206059 | 0.989927 | nan | 3.536571 | nan | nan | 4.101141e-03 | nan | nan | 5.559786e-03 | nan | True |
| feynman_I_10_7 | 2 | True | hit | 6.079824e-03 | 0.995837 | True | 1.975545 | 0.837923 | nan | 3.104909 | nan | nan | 1.440883e-03 | nan | nan | 5.164017e-03 | nan | True |
| feynman_I_10_7 | 3 | True | hit | 3.509219e-03 | 0.997671 | True | 1.616713 | 0.622251 | nan | 2.456937 | nan | nan | 7.892341e-04 | nan | nan | 3.667539e-03 | nan | True |
| feynman_I_10_7 | 4 | True | hit | 4.864902e-03 | 0.996456 | True | 1.844344 | 0.717996 | nan | 2.812079 | nan | nan | 3.662106e-03 | nan | nan | 6.503371e-03 | nan | True |
| feynman_I_10_7 | 5 | True | hit | 4.616702e-03 | 0.996805 | True | 1.555000 | 0.591792 | nan | 2.356293 | nan | nan | 1.023818e-02 | nan | nan | 1.108889e-02 | nan | True |
| feynman_I_10_7 | 6 | True | hit | 1.170843e-02 | 0.991804 | True | 1.695504 | 0.666083 | nan | 2.593963 | nan | nan | 5.567632e-03 | nan | nan | 1.290675e-02 | nan | True |
| feynman_I_10_7 | 7 | True | hit | 7.841146e-03 | 0.994580 | True | 1.998480 | 0.798290 | nan | 3.084140 | nan | nan | 3.686062e-03 | nan | nan | 6.871138e-03 | nan | True |
| feynman_I_10_7 | 8 | True | hit | 4.293375e-03 | 0.996983 | True | 2.232642 | 0.954123 | nan | 3.515893 | nan | nan | 8.862158e-03 | nan | nan | 1.263677e-02 | nan | True |
| feynman_I_10_7 | 9 | True | hit | 2.179883e-03 | 0.998635 | True | 1.997335 | 0.837779 | nan | 3.123830 | nan | nan | 8.051416e-04 | nan | nan | 2.265056e-03 | nan | True |
| feynman_I_10_7 | 10 | True | hit | 5.516047e-03 | 0.996187 | True | 1.827409 | 0.745748 | nan | 2.832239 | nan | nan | 6.163856e-03 | nan | nan | 9.195032e-03 | nan | True |
| feynman_I_10_7 | 11 | True | hit | 5.087778e-03 | 0.996679 | True | 1.224878 | 0.411149 | nan | 1.780140 | nan | nan | 9.817193e-04 | nan | nan | 4.817777e-03 | nan | True |
| feynman_I_10_7 | 12 | True | hit | 2.541073e-03 | 0.998257 | True | 2.127175 | 0.921910 | nan | 3.362797 | nan | nan | 1.313240e-03 | nan | nan | 2.954144e-03 | nan | True |
| feynman_I_10_7 | 13 | True | hit | 1.100221e-02 | 0.992481 | True | 1.573295 | 0.566584 | nan | 2.344634 | nan | nan | 3.905891e-03 | nan | nan | 1.038419e-02 | nan | True |
| feynman_I_10_7 | 14 | True | hit | 7.272445e-03 | 0.994964 | True | 1.688843 | 0.649759 | nan | 2.572386 | nan | nan | 2.608390e-03 | nan | nan | 7.784284e-03 | nan | True |
| feynman_I_10_7 | 15 | True | hit | 3.860933e-03 | 0.997343 | True | 1.546046 | 0.597217 | nan | 2.353506 | nan | nan | 6.067846e-04 | nan | nan | 4.059847e-03 | nan | True |
| feynman_I_10_7 | 16 | True | hit | 1.727486e-02 | 0.988392 | True | 2.232201 | 0.879940 | nan | 3.415790 | nan | nan | 6.055890e-03 | nan | nan | 1.734900e-02 | nan | True |
| feynman_I_10_7 | 17 | True | hit | 5.949637e-03 | 0.996164 | True | 2.353586 | 0.992690 | nan | 3.691060 | nan | nan | 8.149193e-03 | nan | nan | 1.314933e-02 | nan | True |
| feynman_I_10_7 | 18 | True | hit | 9.737878e-03 | 0.993581 | True | 2.073518 | 0.810413 | nan | 3.165185 | nan | nan | 4.383460e-03 | nan | nan | 8.271948e-03 | nan | True |
| feynman_I_10_7 | 19 | True | hit | 4.861716e-03 | 0.996651 | True | 2.281723 | 0.985339 | nan | 3.601777 | nan | nan | 2.055234e-03 | nan | nan | 5.672069e-03 | nan | True |
| feynman_I_10_7 | 20 | True | hit | 2.941273e-03 | 0.997939 | True | 1.470297 | 0.549279 | nan | 2.215626 | nan | nan | 8.918055e-04 | nan | nan | 3.066737e-03 | nan | True |
| feynman_I_12_1 | 1 | True | hit | 2.104911e-03 | 0.999916 | True | 1.522981 | 0.557293 | nan | 2.273242 | nan | nan | 3.066562e-02 | nan | nan | 3.033241e-02 | nan | True |
| feynman_I_12_1 | 2 | True | hit | 2.802466e-02 | 0.998943 | True | 1.734177 | 0.680859 | nan | 2.648083 | nan | nan | 1.815900e-01 | nan | nan | 2.011948e-01 | nan | True |
| feynman_I_12_1 | 3 | True | hit | 3.628120e-03 | 0.999860 | True | 1.706769 | 0.607732 | nan | 2.529936 | nan | nan | 1.294834e-02 | nan | nan | 1.267620e-02 | nan | True |
| feynman_I_12_1 | 4 | True | hit | 3.009059e-01 | 0.987139 | False | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | False |
| feynman_I_12_1 | 5 | True | hit | 2.414070e-02 | 0.999077 | True | 2.018614 | 0.769808 | nan | 3.058801 | nan | nan | 7.712198e-01 | nan | nan | 8.325033e-01 | nan | True |
| feynman_I_12_1 | 6 | True | hit | 6.698473e-03 | 0.999732 | True | 1.538460 | 0.562020 | nan | 2.298317 | nan | nan | 2.234508e-02 | nan | nan | 2.765743e-02 | nan | True |
| feynman_I_12_1 | 7 | True | hit | 2.975251e-02 | 0.998820 | True | 2.001315 | 0.753977 | nan | 3.018938 | nan | nan | 6.107330e-02 | nan | nan | 8.171619e-02 | nan | True |
| feynman_I_12_1 | 8 | True | hit | 1.698283e-02 | 0.999360 | True | 1.695409 | 0.615261 | nan | 2.524306 | nan | nan | 5.606720e-01 | nan | nan | 5.548102e-01 | nan | True |
| feynman_I_12_1 | 9 | True | hit | 6.134526e-03 | 0.999762 | True | 1.795514 | 0.696699 | nan | 2.738086 | nan | nan | 2.172768e-02 | nan | nan | 1.439277e-02 | nan | True |
| feynman_I_12_1 | 10 | True | hit | 3.732413e-02 | 0.998505 | True | 1.977709 | 0.817392 | nan | 3.085215 | nan | nan | 1.213208e+00 | nan | nan | 1.257170e+00 | nan | True |
| feynman_I_12_1 | 11 | True | hit | 4.830737e-03 | 0.999805 | True | 1.602877 | 0.582820 | nan | 2.392004 | nan | nan | 1.469392e-02 | nan | nan | 1.550554e-02 | nan | True |
| feynman_I_12_1 | 12 | True | hit | 1.246034e-02 | 0.999492 | True | 1.555681 | 0.555385 | nan | 2.311707 | nan | nan | 2.658220e-02 | nan | nan | 2.791931e-02 | nan | True |
| feynman_I_12_1 | 13 | True | hit | 1.496255e-02 | 0.999343 | True | 1.951747 | 0.766992 | nan | 2.980844 | nan | nan | 1.673985e-01 | nan | nan | 1.666720e-01 | nan | True |
| feynman_I_12_1 | 14 | True | hit | 8.608292e-03 | 0.999668 | True | 1.871276 | 0.743363 | nan | 2.868540 | nan | nan | 2.781707e-02 | nan | nan | 2.639337e-02 | nan | True |
| feynman_I_12_1 | 15 | True | hit | 2.635321e-02 | 0.998976 | True | 1.917805 | 0.721610 | nan | 2.891053 | nan | nan | 8.041531e-01 | nan | nan | 8.364451e-01 | nan | True |
| feynman_I_12_1 | 16 | True | hit | 1.986190e-02 | 0.999265 | True | 1.969199 | 0.794491 | nan | 3.040909 | nan | nan | nan | nan | nan | nan | nan | True |
| feynman_I_12_1 | 17 | True | hit | 1.136978e-02 | 0.999540 | True | 2.033170 | 0.759340 | nan | 3.060072 | nan | nan | 2.555362e-02 | nan | nan | 3.149015e-02 | nan | True |
| feynman_I_12_1 | 18 | True | hit | 5.351551e-03 | 0.999787 | True | 1.161406 | 0.385102 | nan | 1.685718 | nan | nan | 5.138262e-03 | nan | nan | 8.630076e-03 | nan | True |
| feynman_I_12_1 | 19 | True | hit | 8.175789e-03 | 0.999671 | True | 1.730443 | 0.605043 | nan | 2.551794 | nan | nan | 1.834862e-02 | nan | nan | 2.585209e-02 | nan | True |
| feynman_I_12_1 | 20 | True | hit | 2.774611e-02 | 0.998981 | True | 1.948682 | 0.793859 | nan | 3.011225 | nan | nan | 3.739345e-01 | nan | nan | 3.784853e-01 | nan | True |
| feynman_I_12_4 | 1 | True | hit | 7.618417e-04 | -0.000199 | True | 1.314619 | 0.500314 | nan | 1.992265 | nan | nan | 2.994029e-09 | nan | nan | 7.628362e-04 | nan | True |
| feynman_I_12_4 | 2 | True | hit | 1.093586e-03 | -0.513327 | True | 0.000002 | 0.000000 | nan | 0.009604 | nan | nan | 0.000000e+00 | nan | nan | 1.093586e-03 | nan | True |
| feynman_I_12_4 | 3 | True | hit | 6.317526e-04 | -0.000872 | True | 0.137219 | 0.014669 | nan | 0.162493 | nan | nan | 0.000000e+00 | nan | nan | 6.317526e-04 | nan | True |
| feynman_I_12_4 | 4 | True | hit | 7.571742e-04 | -0.002349 | True | 0.599126 | 0.157445 | nan | 0.822402 | nan | nan | 2.735728e-15 | nan | nan | 7.571742e-04 | nan | True |
| feynman_I_12_4 | 5 | True | hit | 4.494367e-03 | -5.492441 | True | 0.524651 | 0.082113 | nan | 0.642554 | nan | nan | 1.089298e-11 | nan | nan | 4.494326e-03 | nan | True |
| feynman_I_12_4 | 6 | True | hit | 5.981217e-04 | -0.000014 | True | 0.671886 | 0.175493 | nan | 0.916019 | nan | nan | 3.067762e-09 | nan | nan | 5.988560e-04 | nan | True |
| feynman_I_12_4 | 7 | True | hit | 6.042366e-04 | -0.001834 | True | 0.295373 | 0.027242 | nan | 0.338146 | nan | nan | 7.098141e-17 | nan | nan | 6.042366e-04 | nan | True |
| feynman_I_12_4 | 8 | True | hit | 5.404748e-04 | 0.000827 | True | 1.052186 | 0.358681 | nan | 1.540235 | nan | nan | 6.674118e-07 | nan | nan | 5.413584e-04 | nan | True |
| feynman_I_12_4 | 9 | True | hit | 6.036269e-04 | -0.005880 | True | 0.941005 | 0.316997 | nan | 1.378139 | nan | nan | 6.092929e-08 | nan | nan | 6.038004e-04 | nan | True |
| feynman_I_12_4 | 10 | True | hit | 6.541178e-04 | 0.001329 | True | 0.770561 | 0.207607 | nan | 1.056995 | nan | nan | 2.897517e-08 | nan | nan | 6.532336e-04 | nan | True |
| feynman_I_12_4 | 11 | True | hit | 8.037632e-04 | -0.000112 | True | 0.274879 | 0.027784 | nan | 0.318144 | nan | nan | 2.967952e-13 | nan | nan | 8.037648e-04 | nan | True |
| feynman_I_12_4 | 12 | True | hit | 7.019500e-04 | 0.001951 | True | 1.031248 | 0.366521 | nan | 1.536184 | nan | nan | 2.900351e-08 | nan | nan | 7.017696e-04 | nan | True |
| feynman_I_12_4 | 13 | True | hit | 5.430167e-04 | -0.009126 | True | 0.287511 | 0.029234 | nan | 0.332308 | nan | nan | 3.363434e-14 | nan | nan | 5.430165e-04 | nan | True |
| feynman_I_12_4 | 14 | True | hit | 4.482468e-04 | -0.018556 | True | 0.532225 | 0.118894 | nan | 0.696493 | nan | nan | 1.525921e-12 | nan | nan | 4.482435e-04 | nan | True |
| feynman_I_12_4 | 15 | True | hit | 7.240190e-04 | -0.004617 | True | 0.461050 | 0.100685 | nan | 0.604844 | nan | nan | 1.704978e-07 | nan | nan | 7.214854e-04 | nan | True |
| feynman_I_12_4 | 16 | True | hit | 8.866242e-04 | 0.028178 | True | 1.710272 | 0.696351 | nan | 2.647660 | nan | nan | 7.467645e-07 | nan | nan | 9.076842e-04 | nan | True |
| feynman_I_12_4 | 17 | True | hit | 5.651012e-04 | -0.000211 | True | 0.500535 | 0.117470 | nan | 0.665405 | nan | nan | 1.564516e-12 | nan | nan | 5.651045e-04 | nan | True |
| feynman_I_12_4 | 18 | True | hit | 1.103953e-03 | -0.597388 | True | 0.485280 | 0.085604 | nan | 0.607000 | nan | nan | 5.478545e-10 | nan | nan | 1.103716e-03 | nan | True |
| feynman_I_12_4 | 19 | True | hit | 9.144658e-04 | 0.000489 | True | 0.979576 | 0.291428 | nan | 1.381528 | nan | nan | 1.090538e-07 | nan | nan | 9.151176e-04 | nan | True |
| feynman_I_12_4 | 20 | True | hit | 7.089532e-04 | -0.003783 | True | 0.468249 | 0.096184 | nan | 0.607279 | nan | nan | 4.262328e-12 | nan | nan | 7.089493e-04 | nan | True |
| feynman_I_6_2a | 1 | True | hit | 4.749580e-03 | -0.005976 | True | 0.271882 | 0.014091 | nan | 0.293618 | nan | nan | 1.959322e-15 | nan | nan | 4.749581e-03 | nan | True |
| feynman_I_6_2a | 2 | True | hit | 5.435676e-03 | -0.130923 | True | 0.276062 | 0.014014 | nan | 0.298047 | nan | nan | 1.006278e-06 | nan | nan | 5.404796e-03 | nan | True |
| feynman_I_6_2a | 3 | True | hit | 1.337722e-03 | 0.710607 | True | 0.270884 | 0.014438 | nan | 0.296658 | nan | nan | 2.251322e-05 | nan | nan | 1.247119e-03 | nan | True |
| feynman_I_6_2a | 4 | True | hit | 2.493406e-03 | 0.493235 | True | 0.272577 | 0.014388 | nan | 0.294685 | nan | nan | 2.809519e-05 | nan | nan | 2.317316e-03 | nan | True |
| feynman_I_6_2a | 5 | True | hit | 5.043435e-03 | -0.054326 | True | 0.136153 | 0.006905 | nan | 0.147937 | nan | nan | 0.000000e+00 | nan | nan | 5.043435e-03 | nan | True |
| feynman_I_6_2a | 6 | True | hit | 1.584985e-02 | -2.152354 | True | 0.272957 | 0.014547 | nan | 0.295407 | nan | nan | 9.093685e-06 | nan | nan | 1.588012e-02 | nan | True |
| feynman_I_6_2a | 7 | True | hit | 1.069810e-02 | -1.196477 | True | 0.000002 | 0.000000 | nan | 0.006011 | nan | nan | 0.000000e+00 | nan | nan | 1.069810e-02 | nan | True |
| feynman_I_6_2a | 8 | True | hit | 2.772667e-03 | 0.429632 | True | 0.440186 | 0.061361 | nan | 0.528044 | nan | nan | 1.279101e-04 | nan | nan | 3.575761e-03 | nan | True |
| feynman_I_6_2a | 9 | True | hit | 1.222142e-02 | -1.290458 | True | 0.000002 | 0.000000 | nan | 0.006449 | nan | nan | 0.000000e+00 | nan | nan | 1.222142e-02 | nan | True |
| feynman_I_6_2a | 10 | True | hit | 1.593146e-04 | 0.967640 | True | 0.277085 | 0.013469 | nan | 0.297956 | nan | nan | 5.448458e-05 | nan | nan | 1.077841e-04 | nan | True |
| feynman_I_6_2a | 11 | True | hit | 1.198883e-02 | -1.321450 | True | 0.000001 | 0.000000 | nan | 0.002887 | nan | nan | 0.000000e+00 | nan | nan | 1.198883e-02 | nan | True |
| feynman_I_6_2a | 12 | True | hit | 2.492909e-04 | 0.949017 | True | 0.295930 | 0.013923 | nan | 0.318336 | nan | nan | 2.432517e-05 | nan | nan | 2.678768e-04 | nan | True |
| feynman_I_6_2a | 13 | True | hit | 2.807868e-04 | 0.938131 | True | 0.272868 | 0.013527 | nan | 0.293948 | nan | nan | 3.316826e-05 | nan | nan | 2.077396e-04 | nan | True |
| feynman_I_6_2a | 14 | True | hit | 2.367586e-04 | 0.948221 | True | 0.509822 | 0.078158 | nan | 0.618981 | nan | nan | 4.590224e-05 | nan | nan | 1.680815e-04 | nan | True |
| feynman_I_6_2a | 15 | True | hit | 1.124615e-02 | -1.256123 | True | 0.000001 | 0.000000 | nan | 0.005752 | nan | nan | 0.000000e+00 | nan | nan | 1.124615e-02 | nan | True |
| feynman_I_6_2a | 16 | True | hit | 6.682832e-03 | -0.352419 | True | 0.274077 | 0.014092 | nan | 0.295753 | nan | nan | 1.979324e-06 | nan | nan | 6.628862e-03 | nan | True |
| feynman_I_6_2a | 17 | True | hit | 1.123139e-02 | -1.241356 | True | 0.000001 | 0.000000 | nan | 0.002564 | nan | nan | 0.000000e+00 | nan | nan | 1.123139e-02 | nan | True |
| feynman_I_6_2a | 18 | True | hit | 2.225641e-03 | 0.555444 | True | 0.277352 | 0.014023 | nan | 0.299114 | nan | nan | 3.106413e-05 | nan | nan | 2.074329e-03 | nan | True |
| feynman_I_6_2a | 19 | True | hit | 4.883552e-03 | -0.000667 | True | 0.283377 | 0.013836 | nan | 0.305450 | nan | nan | 1.811718e-15 | nan | nan | 4.883551e-03 | nan | True |
| feynman_I_6_2a | 20 | True | hit | 1.278427e-02 | -1.484015 | True | 0.139539 | 0.006974 | nan | 0.151407 | nan | nan | 0.000000e+00 | nan | nan | 1.278427e-02 | nan | True |
| feynman_I_34_1 | 1 | True | hit | 2.049711e-02 | 0.993958 | True | 2.154112 | 0.957089 | nan | 3.437626 | nan | nan | 6.661199e-03 | nan | nan | 1.914949e-02 | nan | True |
| feynman_I_34_1 | 2 | True | hit | 1.240291e-02 | 0.995901 | True | 2.259085 | 0.965688 | nan | 3.564617 | nan | nan | nan | nan | nan | nan | nan | True |
| feynman_I_34_1 | 3 | True | hit | 7.803584e-03 | 0.997296 | True | 2.280266 | 0.994095 | nan | 3.612540 | nan | nan | 8.735810e-03 | nan | nan | 1.277007e-02 | nan | True |
| feynman_I_34_1 | 4 | True | hit | 9.617497e-03 | 0.996991 | True | 2.180589 | 0.991651 | nan | 3.526530 | nan | nan | 3.133173e-02 | nan | nan | 3.040851e-02 | nan | True |
| feynman_I_34_1 | 5 | True | hit | 3.206039e-02 | 0.989316 | True | 2.173282 | 0.952898 | nan | 3.450422 | nan | nan | 8.257429e-03 | nan | nan | 3.638929e-02 | nan | True |
| feynman_I_34_1 | 6 | True | hit | 2.283802e-02 | 0.992602 | True | 2.204799 | 0.899688 | nan | 3.415725 | nan | nan | 4.325967e-02 | nan | nan | 4.931849e-02 | nan | True |
| feynman_I_34_1 | 7 | True | hit | 2.506424e-02 | 0.991728 | True | 1.629491 | 0.630826 | nan | 2.490776 | nan | nan | 9.486181e-03 | nan | nan | 2.348139e-02 | nan | True |
| feynman_I_34_1 | 8 | True | hit | 2.053738e-02 | 0.994004 | True | 2.331407 | 1.010252 | nan | 3.690839 | nan | nan | 9.981794e-03 | nan | nan | 1.863173e-02 | nan | True |
| feynman_I_34_1 | 9 | True | hit | 1.957853e-02 | 0.993839 | True | 2.321503 | 0.990891 | nan | 3.651372 | nan | nan | 8.233731e-03 | nan | nan | 1.544530e-02 | nan | True |
| feynman_I_34_1 | 10 | True | hit | 1.119535e-02 | 0.996269 | True | 2.089105 | 0.870737 | nan | 3.268496 | nan | nan | 3.028617e-02 | nan | nan | 3.918470e-02 | nan | True |
| feynman_I_34_1 | 11 | True | hit | 2.325557e-02 | 0.993461 | True | 2.291225 | 0.911865 | nan | 3.525921 | nan | nan | 1.331795e-02 | nan | nan | 2.580416e-02 | nan | True |
| feynman_I_34_1 | 12 | True | hit | 2.463624e-02 | 0.992108 | True | 2.141717 | 0.855056 | nan | 3.293169 | nan | nan | 2.083176e-02 | nan | nan | 3.339599e-02 | nan | True |
| feynman_I_34_1 | 13 | True | hit | 2.830283e-02 | 0.990871 | True | 1.975757 | 0.820110 | nan | 3.072203 | nan | nan | 1.736820e-02 | nan | nan | 2.102674e-02 | nan | True |
| feynman_I_34_1 | 14 | True | hit | 3.044471e-02 | 0.990929 | True | 1.904997 | 0.746005 | nan | 2.907365 | nan | nan | 4.479099e-02 | nan | nan | 6.196485e-02 | nan | True |
| feynman_I_34_1 | 15 | True | hit | 5.435445e-02 | 0.983432 | True | 1.692588 | 0.743018 | nan | 2.699599 | nan | nan | 8.594024e-03 | nan | nan | 4.446702e-02 | nan | True |
| feynman_I_34_1 | 16 | True | hit | 4.391044e-02 | 0.987287 | True | 2.096157 | 0.824208 | nan | 3.214648 | nan | nan | 2.063552e-02 | nan | nan | 4.057738e-02 | nan | True |
| feynman_I_34_1 | 17 | True | hit | 1.968483e-02 | 0.993354 | True | 2.374073 | 1.066800 | nan | 3.800079 | nan | nan | 1.579683e-02 | nan | nan | 2.669173e-02 | nan | True |
| feynman_I_34_1 | 18 | True | hit | 2.223324e-02 | 0.993207 | True | 1.817105 | 0.734729 | nan | 2.812961 | nan | nan | 9.411777e-03 | nan | nan | 2.260610e-02 | nan | True |
| feynman_I_34_1 | 19 | True | hit | 1.441680e-02 | 0.995479 | True | 2.406183 | 1.058375 | nan | 3.828243 | nan | nan | 1.381758e-02 | nan | nan | 1.578507e-02 | nan | True |
| feynman_I_34_1 | 20 | True | hit | 1.504405e-02 | 0.995579 | True | 2.197082 | 0.934873 | nan | 3.453827 | nan | nan | 1.683268e-02 | nan | nan | 2.023239e-02 | nan | True |
| feynman_II_6_15a | 1 | True | hit | 6.369051e-03 | 0.945345 | True | 0.636324 | 0.115632 | nan | 0.798720 | nan | nan | 3.117603e-03 | nan | nan | 4.205469e-03 | nan | True |
| feynman_II_6_15a | 2 | True | hit | 1.113541e-02 | 0.912134 | True | 0.900286 | 0.218359 | nan | 1.200092 | nan | nan | 4.612273e-03 | nan | nan | 1.348995e-02 | nan | True |
| feynman_II_6_15a | 3 | True | hit | 9.527929e-03 | 0.915886 | True | 0.632189 | 0.124587 | nan | 0.805954 | nan | nan | 2.332101e-03 | nan | nan | 8.595952e-03 | nan | True |
| feynman_II_6_15a | 4 | True | hit | 2.637712e-02 | 0.782050 | True | 0.628769 | 0.122924 | nan | 0.798958 | nan | nan | 1.591181e-03 | nan | nan | 2.509389e-02 | nan | True |
| feynman_II_6_15a | 5 | True | hit | 4.778140e-03 | 0.965069 | True | 0.965058 | 0.340966 | nan | 1.430657 | nan | nan | 2.402755e-03 | nan | nan | 2.948069e-03 | nan | True |
| feynman_II_6_15a | 6 | True | hit | 1.341172e-02 | 0.863253 | True | 0.636273 | 0.118775 | nan | 0.802041 | nan | nan | 2.566695e-03 | nan | nan | 1.302010e-02 | nan | True |
| feynman_II_6_15a | 7 | True | hit | 4.955336e-03 | 0.954187 | True | 0.651365 | 0.142715 | nan | 0.851949 | nan | nan | 2.451396e-03 | nan | nan | 4.124199e-03 | nan | True |
| feynman_II_6_15a | 8 | True | hit | 1.257570e-02 | 0.924930 | True | 0.798683 | 0.242248 | nan | 1.133054 | nan | nan | 2.776601e-03 | nan | nan | 1.352338e-02 | nan | True |
| feynman_II_6_15a | 9 | True | hit | 1.993361e-03 | 0.985958 | True | 0.637880 | 0.125988 | nan | 0.812268 | nan | nan | 1.530436e-03 | nan | nan | 3.248615e-03 | nan | True |
| feynman_II_6_15a | 10 | True | hit | 1.486348e-02 | 0.879280 | True | 0.637801 | 0.121651 | nan | 0.806681 | nan | nan | 2.609615e-03 | nan | nan | 1.560747e-02 | nan | True |
| feynman_II_6_15a | 11 | True | hit | 3.687255e-03 | 0.973415 | True | 0.626355 | 0.117853 | nan | 0.792195 | nan | nan | 2.613873e-03 | nan | nan | 3.701681e-03 | nan | True |
| feynman_II_6_15a | 12 | True | hit | 7.151763e-03 | 0.953419 | True | 0.737585 | 0.163907 | nan | 0.964155 | nan | nan | 3.247613e-03 | nan | nan | 9.306940e-03 | nan | True |
| feynman_II_6_15a | 13 | True | hit | 1.672021e-02 | 0.891533 | True | 0.773407 | 0.179325 | nan | 1.021718 | nan | nan | 3.411409e-03 | nan | nan | 1.473744e-02 | nan | True |
| feynman_II_6_15a | 14 | True | hit | 1.746401e-02 | 0.863890 | True | 0.612446 | 0.118231 | nan | 0.778436 | nan | nan | 3.166891e-03 | nan | nan | 1.258425e-02 | nan | True |
| feynman_II_6_15a | 15 | True | hit | 1.296408e-02 | 0.918742 | True | 0.845164 | 0.196540 | nan | 1.117308 | nan | nan | 3.510766e-03 | nan | nan | 1.304162e-02 | nan | True |
| feynman_II_6_15a | 16 | True | hit | 4.659444e-02 | 0.644485 | True | 0.869331 | 0.206557 | nan | 1.154887 | nan | nan | 6.591200e-03 | nan | nan | 4.431628e-02 | nan | True |
| feynman_II_6_15a | 17 | True | hit | 1.638500e-02 | 0.910131 | True | 0.934252 | 0.226841 | nan | 1.248999 | nan | nan | 3.050191e-03 | nan | nan | 1.531200e-02 | nan | True |
| feynman_II_6_15a | 18 | True | hit | 7.634224e-03 | 0.958082 | True | 0.643466 | 0.129667 | nan | 0.823635 | nan | nan | 2.901497e-03 | nan | nan | 7.073708e-03 | nan | True |
| feynman_II_6_15a | 19 | True | hit | 7.792956e-03 | 0.940272 | True | 0.945320 | 0.221484 | nan | 1.251087 | nan | nan | 2.462572e-03 | nan | nan | 5.380500e-03 | nan | True |
| feynman_II_6_15a | 20 | True | hit | 2.374646e-02 | 0.796181 | True | 0.653966 | 0.128681 | nan | 0.832150 | nan | nan | 4.789907e-03 | nan | nan | 2.124733e-02 | nan | True |
| feynman_II_6_15b | 1 | True | hit | 9.840300e-04 | -0.000356 | True | 0.780133 | 0.251051 | nan | 1.123231 | nan | nan | 1.520482e-15 | nan | nan | 9.840296e-04 | nan | True |
| feynman_II_6_15b | 2 | True | hit | 8.323397e-04 | -0.000965 | True | 0.862822 | 0.306354 | nan | 1.281856 | nan | nan | 1.888183e-07 | nan | nan | 8.322987e-04 | nan | True |
| feynman_II_6_15b | 3 | True | hit | 1.071363e-03 | -0.143456 | True | 0.000001 | 0.000000 | nan | 0.005940 | nan | nan | 0.000000e+00 | nan | nan | 1.071363e-03 | nan | True |
| feynman_II_6_15b | 4 | True | hit | 9.244844e-04 | -0.113510 | True | 0.000002 | 0.000000 | nan | 0.010962 | nan | nan | 0.000000e+00 | nan | nan | 9.244844e-04 | nan | True |
| feynman_II_6_15b | 5 | True | hit | 7.740369e-04 | -0.108638 | True | 0.000001 | 0.000000 | nan | 0.005926 | nan | nan | 0.000000e+00 | nan | nan | 7.740369e-04 | nan | True |
| feynman_II_6_15b | 6 | True | hit | 9.548308e-04 | -0.113994 | True | 0.000001 | 0.000000 | nan | 0.007942 | nan | nan | 0.000000e+00 | nan | nan | 9.548308e-04 | nan | True |
| feynman_II_6_15b | 7 | True | hit | 8.986164e-04 | -0.102587 | True | 0.000002 | 0.000000 | nan | 0.010104 | nan | nan | 0.000000e+00 | nan | nan | 8.986164e-04 | nan | True |
| feynman_II_6_15b | 8 | True | hit | 1.064811e-03 | -0.000941 | True | 0.589995 | 0.131965 | nan | 0.776118 | nan | nan | 3.252846e-09 | nan | nan | 1.064098e-03 | nan | True |
| feynman_II_6_15b | 9 | True | hit | 8.612588e-04 | -0.112901 | True | 0.000001 | 0.000000 | nan | 0.007053 | nan | nan | 0.000000e+00 | nan | nan | 8.612588e-04 | nan | True |
| feynman_II_6_15b | 10 | True | hit | 8.909228e-04 | -0.000565 | True | 0.447436 | 0.066535 | nan | 0.542862 | nan | nan | 5.223306e-10 | nan | nan | 8.908281e-04 | nan | True |
| feynman_II_6_15b | 11 | True | hit | 9.960495e-04 | -0.002393 | True | 0.512389 | 0.130192 | nan | 0.693210 | nan | nan | 3.718850e-08 | nan | nan | 9.952792e-04 | nan | True |
| feynman_II_6_15b | 12 | True | hit | 1.033659e-03 | -0.143498 | True | 0.000002 | 0.000000 | nan | 0.005446 | nan | nan | 0.000000e+00 | nan | nan | 1.033659e-03 | nan | True |
| feynman_II_6_15b | 13 | True | hit | 8.972737e-04 | -0.052753 | True | 0.421660 | 0.100287 | nan | 0.565675 | nan | nan | 1.092550e-17 | nan | nan | 8.972737e-04 | nan | True |
| feynman_II_6_15b | 14 | True | hit | 1.032210e-03 | -0.117410 | True | 0.300260 | 0.036978 | nan | 0.355494 | nan | nan | 3.142819e-07 | nan | nan | 1.032610e-03 | nan | True |
| feynman_II_6_15b | 15 | True | hit | 8.955402e-04 | -0.002009 | True | 0.565221 | 0.153847 | nan | 0.787290 | nan | nan | 9.327588e-12 | nan | nan | 8.955455e-04 | nan | True |
| feynman_II_6_15b | 16 | True | hit | 9.430442e-04 | -0.130366 | True | 0.000002 | 0.000000 | nan | 0.012887 | nan | nan | 0.000000e+00 | nan | nan | 9.430442e-04 | nan | True |
| feynman_II_6_15b | 17 | True | hit | 8.237726e-04 | -0.105382 | True | 0.000002 | 0.000000 | nan | 0.014450 | nan | nan | 0.000000e+00 | nan | nan | 8.237726e-04 | nan | True |
| feynman_II_6_15b | 18 | True | hit | 9.097869e-04 | -0.037539 | True | 0.263586 | 0.032627 | nan | 0.313564 | nan | nan | 1.074257e-08 | nan | nan | 9.074827e-04 | nan | True |
| feynman_II_6_15b | 19 | True | hit | 9.247026e-04 | -0.081507 | True | 0.000002 | 0.000000 | nan | 0.006205 | nan | nan | 0.000000e+00 | nan | nan | 9.247026e-04 | nan | True |
| feynman_II_6_15b | 20 | True | hit | 1.003951e-03 | -0.122048 | True | 0.000002 | 0.000000 | nan | 0.014048 | nan | nan | 0.000000e+00 | nan | nan | 1.003951e-03 | nan | True |
| feynman_II_21_32 | 1 | True | hit | 1.493103e-03 | 0.379566 | True | 0.831156 | 0.263091 | nan | 1.195281 | nan | nan | 6.726975e-06 | nan | nan | 1.496096e-03 | nan | True |
| feynman_II_21_32 | 2 | True | hit | 7.359342e-04 | 0.708554 | True | 2.035026 | 1.022305 | nan | 3.424450 | nan | nan | 1.752526e-04 | nan | nan | 6.899062e-04 | nan | True |
| feynman_II_21_32 | 3 | True | hit | 2.384550e-03 | -0.001780 | True | 0.269085 | 0.033773 | nan | 0.321398 | nan | nan | 4.135581e-17 | nan | nan | 2.384550e-03 | nan | True |
| feynman_II_21_32 | 4 | True | hit | 2.135467e-03 | 0.000713 | True | 0.709610 | 0.201306 | nan | 0.990277 | nan | nan | 2.209316e-09 | nan | nan | 2.135136e-03 | nan | True |
| feynman_II_21_32 | 5 | True | hit | 8.132804e-04 | 0.668205 | True | 2.624597 | 1.376298 | nan | 4.458530 | nan | nan | 1.836436e-04 | nan | nan | 7.758312e-04 | nan | True |
| feynman_II_21_32 | 6 | True | hit | 5.235733e-03 | -1.204739 | True | 0.000002 | 0.000000 | nan | 0.006389 | nan | nan | 0.000000e+00 | nan | nan | 5.235733e-03 | nan | True |
| feynman_II_21_32 | 7 | True | hit | 1.722905e-03 | 0.082550 | True | 2.252587 | 0.971928 | nan | 3.562629 | nan | nan | 2.115646e-04 | nan | nan | 1.815683e-03 | nan | True |
| feynman_II_21_32 | 8 | True | hit | 2.475399e-03 | -0.000443 | True | 0.769591 | 0.235557 | nan | 1.091965 | nan | nan | 3.162406e-09 | nan | nan | 2.475600e-03 | nan | True |
| feynman_II_21_32 | 9 | True | hit | 2.159873e-03 | -0.003155 | True | 0.978486 | 0.328140 | nan | 1.426632 | nan | nan | 9.523992e-06 | nan | nan | 2.157943e-03 | nan | True |
| feynman_II_21_32 | 10 | True | hit | 2.284898e-03 | -0.027954 | True | 0.519673 | 0.131010 | nan | 0.703897 | nan | nan | 1.176797e-06 | nan | nan | 2.281094e-03 | nan | True |
| feynman_II_21_32 | 11 | True | hit | 4.712855e-03 | -1.276523 | True | 0.370985 | 0.051077 | nan | 0.449153 | nan | nan | 1.089830e-04 | nan | nan | 4.618037e-03 | nan | True |
| feynman_II_21_32 | 12 | True | hit | 2.257648e-03 | -0.000939 | True | 0.479002 | 0.109429 | nan | 0.632841 | nan | nan | 6.348505e-08 | nan | nan | 2.257725e-03 | nan | True |
| feynman_II_21_32 | 13 | True | hit | 6.905866e-04 | 0.637997 | True | 0.876934 | 0.267469 | nan | 1.241026 | nan | nan | 6.111238e-05 | nan | nan | 6.752167e-04 | nan | True |
| feynman_II_21_32 | 14 | True | hit | 2.054393e-03 | 0.174886 | True | 1.125923 | 0.330072 | nan | 1.586524 | nan | nan | 7.835014e-05 | nan | nan | 1.956586e-03 | nan | True |
| feynman_II_21_32 | 15 | True | hit | 2.103222e-03 | -0.000619 | True | 0.451943 | 0.074765 | nan | 0.556334 | nan | nan | 3.858509e-13 | nan | nan | 2.103239e-03 | nan | True |
| feynman_II_21_32 | 16 | True | hit | 2.318854e-03 | -0.001445 | True | 0.561878 | 0.148323 | nan | 0.771039 | nan | nan | 3.454889e-15 | nan | nan | 2.318854e-03 | nan | True |
| feynman_II_21_32 | 17 | True | hit | 1.835415e-03 | -0.000313 | True | 0.514127 | 0.126859 | nan | 0.693556 | nan | nan | 7.725140e-15 | nan | nan | 1.835414e-03 | nan | True |
| feynman_II_21_32 | 18 | True | hit | 2.063831e-03 | -0.002537 | True | 0.276599 | 0.038355 | nan | 0.335623 | nan | nan | 2.466222e-16 | nan | nan | 2.063831e-03 | nan | True |
| feynman_II_21_32 | 19 | True | hit | 5.374732e-03 | -1.146653 | True | 0.000001 | 0.000000 | nan | 0.004625 | nan | nan | 0.000000e+00 | nan | nan | 5.374732e-03 | nan | True |
| feynman_II_21_32 | 20 | True | hit | 2.210110e-03 | -0.003531 | True | 0.727033 | 0.224332 | nan | 1.033927 | nan | nan | 6.402131e-08 | nan | nan | 2.211104e-03 | nan | True |
| feynman_II_34_29a | 1 | True | hit | 3.283374e-03 | 0.938800 | True | 0.586391 | 0.100543 | nan | 0.728100 | nan | nan | 1.012601e-03 | nan | nan | 2.202557e-03 | nan | True |
| feynman_II_34_29a | 2 | True | hit | 8.221035e-03 | 0.824023 | True | 0.558177 | 0.101350 | nan | 0.701030 | nan | nan | 3.955179e-04 | nan | nan | 8.117501e-03 | nan | True |
| feynman_II_34_29a | 3 | True | hit | 1.796857e-03 | 0.964477 | True | 0.438797 | 0.058288 | nan | 0.522652 | nan | nan | 3.452672e-04 | nan | nan | 1.343956e-03 | nan | True |
| feynman_II_34_29a | 4 | True | hit | 7.587199e-03 | 0.834555 | True | 0.486825 | 0.083699 | nan | 0.604453 | nan | nan | 9.639600e-04 | nan | nan | 6.588182e-03 | nan | True |
| feynman_II_34_29a | 5 | True | hit | 7.392028e-04 | 0.987189 | True | 0.720125 | 0.195168 | nan | 0.988204 | nan | nan | 2.260667e-04 | nan | nan | 6.927077e-04 | nan | True |
| feynman_II_34_29a | 6 | True | hit | 2.476792e-03 | 0.953876 | True | 0.839170 | 0.226768 | nan | 1.151434 | nan | nan | 5.088653e-04 | nan | nan | 1.649910e-03 | nan | True |
| feynman_II_34_29a | 7 | True | hit | 1.849228e-03 | 0.964085 | True | 0.437075 | 0.057974 | nan | 0.521346 | nan | nan | 3.269258e-04 | nan | nan | 1.339610e-03 | nan | True |
| feynman_II_34_29a | 8 | True | hit | 1.291595e-03 | 0.974205 | True | 1.086155 | 0.337669 | nan | 1.548221 | nan | nan | 4.904304e-04 | nan | nan | 1.265619e-03 | nan | True |
| feynman_II_34_29a | 9 | True | hit | 8.267267e-04 | 0.980500 | True | 0.802486 | 0.219510 | nan | 1.103543 | nan | nan | 2.927550e-04 | nan | nan | 8.580095e-04 | nan | True |
| feynman_II_34_29a | 10 | True | hit | 2.886099e-03 | 0.946847 | True | 0.832779 | 0.225911 | nan | 1.143011 | nan | nan | 4.749817e-04 | nan | nan | 1.942512e-03 | nan | True |
| feynman_II_34_29a | 11 | True | hit | 2.058228e-03 | 0.958682 | True | 0.442550 | 0.061586 | nan | 0.532742 | nan | nan | 4.314002e-04 | nan | nan | 1.530446e-03 | nan | True |
| feynman_II_34_29a | 12 | True | hit | 1.087793e-03 | 0.979554 | True | 0.958344 | 0.305027 | nan | 1.377733 | nan | nan | 1.735118e-04 | nan | nan | 9.183690e-04 | nan | True |
| feynman_II_34_29a | 13 | True | hit | 1.373389e-03 | 0.977742 | True | 0.637723 | 0.170490 | nan | 0.873619 | nan | nan | 1.902845e-04 | nan | nan | 1.060870e-03 | nan | True |
| feynman_II_34_29a | 14 | True | hit | 2.658555e-03 | 0.948101 | True | 0.637622 | 0.171254 | nan | 0.875524 | nan | nan | 9.152153e-04 | nan | nan | 3.775060e-03 | nan | True |
| feynman_II_34_29a | 15 | True | hit | 2.851010e-03 | 0.947507 | True | 0.562097 | 0.100809 | nan | 0.706438 | nan | nan | 7.056124e-04 | nan | nan | 1.759438e-03 | nan | True |
| feynman_II_34_29a | 16 | True | hit | 6.639074e-04 | 0.987324 | True | 1.243713 | 0.390441 | nan | 1.775478 | nan | nan | 1.680916e-04 | nan | nan | 5.053207e-04 | nan | True |
| feynman_II_34_29a | 17 | True | hit | 1.950528e-03 | 0.965082 | True | 0.712071 | 0.201443 | nan | 0.988950 | nan | nan | 3.893392e-04 | nan | nan | 1.730093e-03 | nan | True |
| feynman_II_34_29a | 18 | True | hit | 1.232347e-03 | 0.978397 | True | 1.012266 | 0.314439 | nan | 1.443062 | nan | nan | 6.048803e-04 | nan | nan | 1.348723e-03 | nan | True |
| feynman_II_34_29a | 19 | True | hit | 3.165730e-03 | 0.935921 | True | 0.646751 | 0.119555 | nan | 0.814271 | nan | nan | 7.988914e-04 | nan | nan | 2.393458e-03 | nan | True |
| feynman_II_34_29a | 20 | True | hit | 2.478911e-03 | 0.950068 | True | 0.688491 | 0.178210 | nan | 0.934309 | nan | nan | 8.107352e-04 | nan | nan | 3.292388e-03 | nan | True |

## Feynman Dataset Metadata

### feynman_I_9_18

- Dataset file: `I.9.18`
- Dataset path: `D:\chenpeng\Documents\学习\数学\毕业论文\symkan-experiments\datasets\Feynman_with_units\I.9.18`
- Raw data shape: rows=1000000, columns=10, n_var=9
- Split setting: strategy=random, split_seed=20, train_num=2000, calibration_num=1000, test_num=1000
- Target formula: `G*m1*m2/((x2-x1)**2+(y2-y1)**2+(z2-z1)**2)`
- Equation metadata (from FeynmanEquations.csv):
  - Filename: `I.9.18`
  - Number: `5`
  - Output: `F`
  - Formula: `G*m1*m2/((x2-x1)**2+(y2-y1)**2+(z2-z1)**2)`
  - # variables: `9`
  - v1_name: `m1`
  - v1_low: `1`
  - v1_high: `2`
  - v2_name: `m2`
  - v2_low: `1`
  - v2_high: `2`
  - v3_name: `G`
  - v3_low: `1`
  - v3_high: `2`
  - v4_name: `x1`
  - v4_low: `3`
  - v4_high: `4`
  - v5_name: `x2`
  - v5_low: `1`
  - v5_high: `2`
  - v6_name: `y1`
  - v6_low: `3`
  - v6_high: `4`
  - v7_name: `y2`
  - v7_low: `1`
  - v7_high: `2`
  - v8_name: `z1`
  - v8_low: `3`
  - v8_high: `4`
  - v9_name: `z2`
  - v9_low: `1`
  - v9_high: `2`

### feynman_I_10_7

- Dataset file: `I.10.7`
- Dataset path: `D:\chenpeng\Documents\学习\数学\毕业论文\symkan-experiments\datasets\Feynman_with_units\I.10.7`
- Raw data shape: rows=1000000, columns=4, n_var=3
- Split setting: strategy=random, split_seed=20, train_num=2000, calibration_num=1000, test_num=1000
- Target formula: `m_0/sqrt(1-v**2/c**2)`
- Equation metadata (from FeynmanEquations.csv):
  - Filename: `I.10.7`
  - Number: `6`
  - Output: `m`
  - Formula: `m_0/sqrt(1-v**2/c**2)`
  - # variables: `3`
  - v1_name: `m_0`
  - v1_low: `1`
  - v1_high: `5`
  - v2_name: `v`
  - v2_low: `1`
  - v2_high: `2`
  - v3_name: `c`
  - v3_low: `3`
  - v3_high: `10`

### feynman_I_12_1

- Dataset file: `I.12.1`
- Dataset path: `D:\chenpeng\Documents\学习\数学\毕业论文\symkan-experiments\datasets\Feynman_with_units\I.12.1`
- Raw data shape: rows=1000000, columns=3, n_var=2
- Split setting: strategy=random, split_seed=20, train_num=2000, calibration_num=1000, test_num=1000
- Target formula: `mu*Nn`
- Equation metadata (from FeynmanEquations.csv):
  - Filename: `I.12.1`
  - Number: `8`
  - Output: `F`
  - Formula: `mu*Nn`
  - # variables: `2`
  - v1_name: `mu`
  - v1_low: `1`
  - v1_high: `5`
  - v2_name: `Nn`
  - v2_low: `1`
  - v2_high: `5`

### feynman_I_12_4

- Dataset file: `I.12.4`
- Dataset path: `D:\chenpeng\Documents\学习\数学\毕业论文\symkan-experiments\datasets\Feynman_with_units\I.12.4`
- Raw data shape: rows=1000000, columns=4, n_var=3
- Split setting: strategy=random, split_seed=20, train_num=2000, calibration_num=1000, test_num=1000
- Target formula: `q1*r/(4*pi*epsilon*r**3)`
- Equation metadata (from FeynmanEquations.csv):
  - Filename: `I.12.4`
  - Number: `11`
  - Output: `Ef`
  - Formula: `q1*r/(4*pi*epsilon*r**3)`
  - # variables: `3`
  - v1_name: `q1`
  - v1_low: `1`
  - v1_high: `5`
  - v2_name: `epsilon`
  - v2_low: `1`
  - v2_high: `5`
  - v3_name: `r`
  - v3_low: `1`
  - v3_high: `5`

### feynman_I_6_2a

- Dataset file: `I.6.2a`
- Dataset path: `D:\chenpeng\Documents\学习\数学\毕业论文\symkan-experiments\datasets\Feynman_with_units\I.6.2a`
- Raw data shape: rows=1000000, columns=2, n_var=1
- Split setting: strategy=random, split_seed=20, train_num=2000, calibration_num=1000, test_num=1000
- Target formula: `exp(-theta**2/2)/sqrt(2*pi)`
- Equation metadata (from FeynmanEquations.csv):
  - Filename: `I.6.2a`
  - Number: `1`
  - Output: `f`
  - Formula: `exp(-theta**2/2)/sqrt(2*pi)`
  - # variables: `1`
  - v1_name: `theta`
  - v1_low: `1`
  - v1_high: `3`

### feynman_I_34_1

- Dataset file: `I.34.1`
- Dataset path: `D:\chenpeng\Documents\学习\数学\毕业论文\symkan-experiments\datasets\Feynman_with_units\I.34.1`
- Raw data shape: rows=1000000, columns=4, n_var=3
- Split setting: strategy=random, split_seed=20, train_num=2000, calibration_num=1000, test_num=1000
- Target formula: `omega_0/(1-v/c)`
- Equation metadata (from FeynmanEquations.csv):
  - Filename: `I.34.1`
  - Number: `35`
  - Output: `omega`
  - Formula: `omega_0/(1-v/c)`
  - # variables: `3`
  - v1_name: `c`
  - v1_low: `3`
  - v1_high: `10`
  - v2_name: `v`
  - v2_low: `1`
  - v2_high: `2`
  - v3_name: `omega_0`
  - v3_low: `1`
  - v3_high: `5`

### feynman_II_6_15a

- Dataset file: `II.6.15a`
- Dataset path: `D:\chenpeng\Documents\学习\数学\毕业论文\symkan-experiments\datasets\Feynman_with_units\II.6.15a`
- Raw data shape: rows=1000000, columns=7, n_var=6
- Split setting: strategy=random, split_seed=20, train_num=2000, calibration_num=1000, test_num=1000
- Target formula: `p_d/(4*pi*epsilon)*3*z/r**5*sqrt(x**2+y**2)`
- Equation metadata (from FeynmanEquations.csv):
  - Filename: `II.6.15a`
  - Number: `56`
  - Output: `Ef`
  - Formula: `p_d/(4*pi*epsilon)*3*z/r**5*sqrt(x**2+y**2)`
  - # variables: `6`
  - v1_name: `epsilon`
  - v1_low: `1`
  - v1_high: `3`
  - v2_name: `p_d`
  - v2_low: `1`
  - v2_high: `3`
  - v3_name: `r`
  - v3_low: `1`
  - v3_high: `3`
  - v4_name: `x`
  - v4_low: `1`
  - v4_high: `3`
  - v5_name: `y`
  - v5_low: `1`
  - v5_high: `3`
  - v6_name: `z`
  - v6_low: `1`
  - v6_high: `3`

### feynman_II_6_15b

- Dataset file: `II.6.15b`
- Dataset path: `D:\chenpeng\Documents\学习\数学\毕业论文\symkan-experiments\datasets\Feynman_with_units\II.6.15b`
- Raw data shape: rows=1000000, columns=5, n_var=4
- Split setting: strategy=random, split_seed=20, train_num=2000, calibration_num=1000, test_num=1000
- Target formula: `p_d/(4*pi*epsilon)*3*cos(theta)*sin(theta)/r**3`
- Equation metadata (from FeynmanEquations.csv):
  - Filename: `II.6.15b`
  - Number: `57`
  - Output: `Ef`
  - Formula: `p_d/(4*pi*epsilon)*3*cos(theta)*sin(theta)/r**3`
  - # variables: `4`
  - v1_name: `epsilon`
  - v1_low: `1`
  - v1_high: `3`
  - v2_name: `p_d`
  - v2_low: `1`
  - v2_high: `3`
  - v3_name: `theta`
  - v3_low: `1`
  - v3_high: `3`
  - v4_name: `r`
  - v4_low: `1`
  - v4_high: `3`

### feynman_II_21_32

- Dataset file: `II.21.32`
- Dataset path: `D:\chenpeng\Documents\学习\数学\毕业论文\symkan-experiments\datasets\Feynman_with_units\II.21.32`
- Raw data shape: rows=1000000, columns=6, n_var=5
- Split setting: strategy=random, split_seed=20, train_num=2000, calibration_num=1000, test_num=1000
- Target formula: `q/(4*pi*epsilon*r*(1-v/c))`
- Equation metadata (from FeynmanEquations.csv):
  - Filename: `II.21.32`
  - Number: `71`
  - Output: `Volt`
  - Formula: `q/(4*pi*epsilon*r*(1-v/c))`
  - # variables: `5`
  - v1_name: `q`
  - v1_low: `1`
  - v1_high: `5`
  - v2_name: `epsilon`
  - v2_low: `1`
  - v2_high: `5`
  - v3_name: `r`
  - v3_low: `1`
  - v3_high: `5`
  - v4_name: `v`
  - v4_low: `1`
  - v4_high: `2`
  - v5_name: `c`
  - v5_low: `3`
  - v5_high: `10`

### feynman_II_34_29a

- Dataset file: `II.34.29a`
- Dataset path: `D:\chenpeng\Documents\学习\数学\毕业论文\symkan-experiments\datasets\Feynman_with_units\II.34.29a`
- Raw data shape: rows=1000000, columns=4, n_var=3
- Split setting: strategy=random, split_seed=20, train_num=2000, calibration_num=1000, test_num=1000
- Target formula: `q*h/(4*pi*m)`
- Equation metadata (from FeynmanEquations.csv):
  - Filename: `II.34.29a`
  - Number: `78`
  - Output: `mom`
  - Formula: `q*h/(4*pi*m)`
  - # variables: `3`
  - v1_name: `q`
  - v1_low: `1`
  - v1_high: `5`
  - v2_name: `h`
  - v2_low: `1`
  - v2_high: `5`
  - v3_name: `m`
  - v3_low: `1`
  - v3_high: `5`

## Formula Comparison

### task=feynman_I_9_18 seed=1

- Task source: feynman_file
- Target formula: `G*m1*m2/((x2-x1)**2+(y2-y1)**2+(z2-z1)**2)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.630265e-02, r2=-0.003680
- Variant formula overview:
  - icbr_full: symbolic_s=1.258657e+00, imitation_mse=1.114276e-08, target_mse=1.630319e-02, formula_export_success=True
  - icbr_no_replay: symbolic_s=8.702691e-01, imitation_mse=1.113813e-08, target_mse=1.630319e-02, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.643095e+00, imitation_mse=1.114277e-08, target_mse=1.630319e-02, formula_export_success=True
  - icbr_refit_commit: symbolic_s=2.202329e+00, imitation_mse=1.989224e-08, target_mse=1.630353e-02, formula_export_success=True
- icbr_full formula (display, rounded):
  - `-0.00135625*Abs(-4.95*(1.65342 - 1.72992*(1 - 0.0603015*x_8)**(3/2))*(-2.29201*(1 - 0.0529101*x_6)**(3/2) + 2.20844 - 1.17074e-10/(0.969697 - x_7)**5) + 1.0) + 0.282502 - 9.80403e-13/(-0.702111*(1 - 0.0609137*x_4)**(3/2) - 0.630501*(1 - 0.06*x_8)**(3/2) + 1)**5 + 2.39187e-10/(0.593981 - (1 - 0.06*x_8)**(3/2))**5`
- icbr_no_replay formula (display, rounded):
  - `-0.00135625*Abs(-4.95*(1.65342 - 1.72992*(1 - 0.0603015*x_8)**(3/2))*(-2.29201*(1 - 0.0529101*x_6)**(3/2) + 2.20844 - 1.17074e-10/(0.969697 - x_7)**5) + 1.0) + 0.282502 - 9.80403e-13/(-0.702111*(1 - 0.0609137*x_4)**(3/2) - 0.630501*(1 - 0.06*x_8)**(3/2) + 1)**5 + 9.51279e-12/(0.782713 - exp(-0.05*x_8))**5`
- icbr_no_shared formula (display, rounded):
  - `-0.00135625*Abs(4.95*(1.72992*(1 - 0.0603015*x_8)**(3/2) - 1.65342)*(-2.29201*(1 - 0.0529101*x_6)**(3/2) + 2.20844 + 1.17074e-10/(x_7 - 0.969697)**5) + 1.0) + 0.282502 - 9.80403e-13/(-0.702111*(1 - 0.0609137*x_4)**(3/2) - 0.630501*(1 - 0.06*x_8)**(3/2) + 1)**5 + 2.39187e-10/(0.593981 - (1 - 0.06*x_8)**(3/2))**5`
- icbr_refit_commit formula (display, rounded):
  - `-0.000938846*Abs(5.0*(4.21761 - 4.29558*exp(-0.0368*x_8))*(2.39274*(1 - 0.0504131*x_6)**(3/2) - 2.31074 + 4.56334e-6/(0.319846*x_7 - 1)**5) - 4.3) + 0.287397 - 4.60928e-12/(-0.652534*(1 - 0.0644951*x_4)**(3/2) - 0.664038*(1 - 0.0550024*x_8)**(3/2) + 1)**5 + 4.61782e-11/(0.72993*(0.0481875*x_8 + 1)**(3/2) - 1)**5`

### task=feynman_I_9_18 seed=2

- Task source: feynman_file
- Target formula: `G*m1*m2/((x2-x1)**2+(y2-y1)**2+(z2-z1)**2)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.497844e-02, r2=0.000232
- Variant formula overview:
  - icbr_full: symbolic_s=2.323648e+00, imitation_mse=8.799262e-09, target_mse=1.498076e-02, formula_export_success=True
  - icbr_no_replay: symbolic_s=1.374273e+00, imitation_mse=1.058538e-08, target_mse=1.498118e-02, formula_export_success=True
  - icbr_no_shared: symbolic_s=3.386191e+00, imitation_mse=8.799964e-09, target_mse=1.498076e-02, formula_export_success=True
  - icbr_refit_commit: symbolic_s=3.855404e+00, imitation_mse=1.189628e-08, target_mse=1.498088e-02, formula_export_success=True
- icbr_full formula (display, rounded):
  - `-0.00131224*Abs(4.0*(0.0481536*x_8 - 0.0157981)*(0.0132734*(0.01*x_6 + 1)**5 + 0.016794*Abs(3.25*x_1 - 4.35) + 0.064105*Abs(2.75*x_7 - 3.65) + 5.31021 - 0.00468843*exp(-25.0*(0.69*x_2 - 1)**2) - 5.24016*exp(-0.05*x_4)) - 0.55) + 0.287906 - 1.60988e-6/(-cos(0.4*x_4 + 3.4) - 0.425616)**5 + 5.96845e-14/((1 - 0.052356*x_8)**(3/2) - 0.784211)**5 + 7.92742e-13/((1 - 0.06*x_8)**(3/2) - 0.75958)**5 + 4.26328e-10/(0.776028 - (1 - 0.0540541*x_8)**(3/2))**3 - 4.63564e-13/(0.758583 - (1 - 0.0603015*x_6)**(3/2))**5`
- icbr_no_replay formula (display, rounded):
  - `-6.49061e-5*sign(-3.15*(-1.11542 + 1.14667*exp(-0.05*x_8))*(-3.04156*(1 - 0.0534759*x_4)**(3/2) + 0.0171729*(-0.01*x_6 - 1)**4 + 0.016794*Abs(3.25*x_1 - 4.35) + 0.064105*Abs(2.75*x_7 - 3.65) + 3.13617 - 0.00468843*exp(-25.0*(1 - 0.69*x_2)**2)) - 0.5) + 0.287794 + 5.96845e-14/((1 - 0.052356*x_8)**(3/2) - 0.784211)**5 + 7.92742e-13/((1 - 0.06*x_8)**(3/2) - 0.75958)**5 - 5.35201e-10/((1 - 0.06*x_4)**(3/2) - 0.805584)**5 - 1.805e-14/(0.869688 - exp(-0.05*x_6))**5 + 7.81465e-13/(0.783917 - (1 - 0.0540541*x_8)**(3/2))**5`
- icbr_no_shared formula (display, rounded):
  - `-0.00131224*Abs(4.0*(0.0481536*x_8 - 0.0157982)*(0.0132734*(0.01*x_6 + 1)**5 + 0.016794*Abs(3.25*x_1 - 4.35) + 0.064105*Abs(2.75*x_7 - 3.65) + 5.31021 - 0.00468843*exp(-25.0*(0.69*x_2 - 1)**2) - 5.24016*exp(-0.05*x_4)) - 0.55) + 0.287906 + 1.60988e-6/(cos(0.4*x_4 + 3.4) + 0.425616)**5 + 5.96845e-14/((1 - 0.052356*x_8)**(3/2) - 0.784211)**5 + 7.92742e-13/((1 - 0.06*x_8)**(3/2) - 0.75958)**5 + 4.51715e-10/(0.771286 - (1 - 0.0552486*x_8)**(3/2))**3 - 4.63564e-13/(0.758583 - (1 - 0.0603015*x_6)**(3/2))**5`
- icbr_refit_commit formula (display, rounded):
  - `-0.000588923*Abs(-5.0*(-3.22334 + 3.24379*exp(-0.01568*x_8))*(-0.00925974*(1 - 0.0230083*x_6)**5 + 0.023199*Abs(2.35264*x_1 - 3.1724) + 0.04808*Abs(3.66076*x_7 - 4.89012) + 8.19034 - 0.00663822*exp(-10.24*(1 - 0.6798*x_2)**2) - 8.06644*exp(-0.03032*x_4)) + 1.2) + 0.288961 - 1.84577e-13/(0.823974*(0.0496546*x_6 + 1)**(3/2) - 1)**5 + 6.40613e-13/((1 - 0.0572227*x_8)**(3/2) - 0.770294)**5 + 3.97691e-10/(0.781469 - (1 - 0.0526854*x_8)**(3/2))**3 - 1.08403e-13/(0.768975 - (1 - 0.0564925*x_8)**(3/2))**5 + 5.57159e-6/(0.580566 - cos(0.50004*x_4 - 0.10804))**5`

### task=feynman_I_9_18 seed=3

- Task source: feynman_file
- Target formula: `G*m1*m2/((x2-x1)**2+(y2-y1)**2+(z2-z1)**2)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.347480e-02, r2=-0.000924
- Variant formula overview:
  - icbr_full: symbolic_s=3.420608e-01, imitation_mse=1.153306e-08, target_mse=1.347650e-02, formula_export_success=True
  - icbr_no_replay: symbolic_s=2.629646e-01, imitation_mse=1.153306e-08, target_mse=1.347650e-02, formula_export_success=True
  - icbr_no_shared: symbolic_s=3.167217e-01, imitation_mse=1.153306e-08, target_mse=1.347650e-02, formula_export_success=True
  - icbr_refit_commit: symbolic_s=5.179271e-01, imitation_mse=1.364365e-08, target_mse=1.347537e-02, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0.289076 - 0.000106536*sign(14.1038*(1 - 0.0537634*x_8)**(3/2) - 10.2694)`
- icbr_no_replay formula (display, rounded):
  - `0.289076 - 0.000106536*sign(14.1038*(1 - 0.0537634*x_8)**(3/2) - 10.2694)`
- icbr_no_shared formula (display, rounded):
  - `0.289076 - 0.000106536*sign(14.1038*(1 - 0.0537634*x_8)**(3/2) - 10.2694)`
- icbr_refit_commit formula (display, rounded):
  - `0.289088 - 8.72304e-5*sign(12.8767*(1 - 0.0514166*x_8)**(3/2) - 9.44874)`

### task=feynman_I_9_18 seed=4

- Task source: feynman_file
- Target formula: `G*m1*m2/((x2-x1)**2+(y2-y1)**2+(z2-z1)**2)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.371062e-02, r2=0.000294
- Variant formula overview:
  - icbr_full: symbolic_s=1.151719e+00, imitation_mse=1.835985e-08, target_mse=1.370914e-02, formula_export_success=True
  - icbr_no_replay: symbolic_s=8.132023e-01, imitation_mse=1.838193e-08, target_mse=1.370924e-02, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.464671e+00, imitation_mse=1.834736e-08, target_mse=1.370928e-02, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.914287e+00, imitation_mse=2.544611e-08, target_mse=1.371018e-02, formula_export_success=True
- icbr_full formula (display, rounded):
  - `-8.85865e-5*sign(15.4505 - 18.2993*exp(-0.05*x_8)) + 0.000112516*sign(3.18335*sin(0.35*x_6 + 2.0) + 0.0342977 - 0.00408986*exp(-25.0*(1 - 0.47*x_3)**2) + 6.84205e-10/(0.973545 - x_1)**5) + 0.285282 - 1.74576e-5/(0.224394*Abs(2.55*x_5 - 3.6) + 1)**4`
- icbr_no_replay formula (display, rounded):
  - `-8.85865e-5*sign(7.56614 - 10.3217*(1 - 0.0552486*x_8)**(3/2)) + 0.000112516*sign(13.8378*(1 - 0.06*x_6)**(3/2) - 0.0132178*sign(4.8 - 4.75*x_1) + 0.0029415*sign(4.85 - 4.45*x_3) - 9.95964) + 0.28528 - 4.63381e-6/(1 - 0.206937*exp(-24.7506*(1 - 0.703518*x_5)**2))**5`
- icbr_no_shared formula (display, rounded):
  - `8.85865e-5*sign(-14.8049 + 17.5328*exp(-0.05*x_8)) + 0.000112516*sign(3.18335*sin(0.35*x_6 + 2.0) + 0.0342977 - 0.00408986*exp(-25.0*(1 - 0.47*x_3)**2) - 6.84205e-10/(x_1 - 0.973545)**5) + 0.285282 - 1.74576e-5/(0.224394*Abs(2.55*x_5 - 3.6) + 1)**4`
- icbr_refit_commit formula (display, rounded):
  - `-6.21015e-5*sign(26.9755 - 29.8902*exp(-0.02988*x_8)) + 6.72332e-5*sign(2.79429*sin(0.40928*x_6 + 1.782) + 0.150239 - 0.00384769*exp(-25.0*(1 - 0.48*x_3)**2) + 3.32493e-8/(0.933969 - x_1)**5) + 0.285231 - 2.0436e-5/(0.114714*Abs(3.366*x_5 - 4.79996) + 1)**4`

### task=feynman_I_9_18 seed=5

- Task source: feynman_file
- Target formula: `G*m1*m2/((x2-x1)**2+(y2-y1)**2+(z2-z1)**2)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.844272e-02, r2=-0.313000
- Variant formula overview:
  - icbr_full: symbolic_s=1.040506e+00, imitation_mse=3.111923e-11, target_mse=1.844273e-02, formula_export_success=True
  - icbr_no_replay: symbolic_s=8.014863e-01, imitation_mse=3.090452e-11, target_mse=1.844276e-02, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.445986e+00, imitation_mse=3.111923e-11, target_mse=1.844273e-02, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.744780e+00, imitation_mse=6.221264e-11, target_mse=1.844281e-02, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0.215041 - 2.68718e-7/(0.000180893*sign(3.35 - 2.85*x_1) + 0.00018958*sign(3.65 - 3.1*x_3) + 0.000104511*sign(3.8 - 3.25*x_5) + 1 + 0.000294907*exp(-25.0*(1 - 0.995*x_9)**2) - 0.471063*exp(-0.05*x_8) - 0.0130737*exp(-0.1*x_6) - 0.546394*exp(-0.05*x_4) + 0.00855107/(x_7 + 0.999994)**2)**4`
- icbr_no_replay formula (display, rounded):
  - `0.215041 - 3.0764e-7/(0.021479*(-0.01*x_6 - 1)**4 + 0.000187115*sign(3.35 - 2.85*x_1) + 0.000108106*sign(3.8 - 3.25*x_5) + 1 + 0.00030505*exp(-25.0*(1 - 0.995*x_9)**2) + 0.000493587*exp(-25.0*(1 - x_3)**2) - 0.487266*exp(-0.05*x_8) - 0.565188*exp(-0.05*x_4) + 0.00884519/(x_7 + 0.999994)**2)**4`
- icbr_no_shared formula (display, rounded):
  - `0.215041 - 2.68718e-7/(0.000180893*sign(3.35 - 2.85*x_1) + 0.00018958*sign(3.65 - 3.1*x_3) + 0.000104511*sign(3.8 - 3.25*x_5) + 1 + 0.000294907*exp(-25.0*(1 - 0.995*x_9)**2) - 0.471063*exp(-0.05*x_8) - 0.0130737*exp(-0.1*x_6) - 0.546394*exp(-0.05*x_4) + 0.00855107/(x_7 + 0.999994)**2)**4`
- icbr_refit_commit formula (display, rounded):
  - `0.21513 - 1.47653e-7/(0.56156*exp(0.028*x_4) + 0.448608*exp(0.03*x_8) + 6.68573e-5*sign(4.39808 - 3.79*x_5) + 0.000123032*sign(4.99812 - 4.288*x_1) - 1 + 0.00018643*exp(-24.01*(1 - 0.952653*x_9)**2) + 0.000304836*exp(-24.9998*(1 - 0.960004*x_3)**2) - 0.00700881*exp(-0.2*x_6) + 0.00593066/(-x_7 - 0.932022)**2)**4`

### task=feynman_I_9_18 seed=6

- Task source: feynman_file
- Target formula: `G*m1*m2/((x2-x1)**2+(y2-y1)**2+(z2-z1)**2)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.477381e-02, r2=0.000836
- Variant formula overview:
  - icbr_full: symbolic_s=3.460585e-01, imitation_mse=1.723541e-08, target_mse=1.477232e-02, formula_export_success=True
  - icbr_no_replay: symbolic_s=2.981116e-01, imitation_mse=1.723541e-08, target_mse=1.477232e-02, formula_export_success=True
  - icbr_no_shared: symbolic_s=3.213128e-01, imitation_mse=1.723541e-08, target_mse=1.477232e-02, formula_export_success=True
  - icbr_refit_commit: symbolic_s=5.114308e-01, imitation_mse=2.380401e-08, target_mse=1.477661e-02, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0.000305417*sign(14.4329*(1 - 0.0515464*x_6)**(3/2) - 10.7155) + 0.285209`
- icbr_no_replay formula (display, rounded):
  - `0.000305417*sign(14.4329*(1 - 0.0515464*x_6)**(3/2) - 10.7155) + 0.285209`
- icbr_no_shared formula (display, rounded):
  - `0.000305417*sign(14.4329*(1 - 0.0515464*x_6)**(3/2) - 10.7155) + 0.285209`
- icbr_refit_commit formula (display, rounded):
  - `0.000251336*sign(9.71542*(1 - 0.0501117*x_6)**(3/2) - 7.24161) + 0.285171`

### task=feynman_I_9_18 seed=7

- Task source: feynman_file
- Target formula: `G*m1*m2/((x2-x1)**2+(y2-y1)**2+(z2-z1)**2)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.719902e-02, r2=-0.000011
- Variant formula overview:
  - icbr_full: symbolic_s=8.665213e-01, imitation_mse=1.289530e-08, target_mse=1.719774e-02, formula_export_success=True
  - icbr_no_replay: symbolic_s=5.983377e-01, imitation_mse=1.289530e-08, target_mse=1.719774e-02, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.083384e+00, imitation_mse=1.289529e-08, target_mse=1.719774e-02, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.595010e+00, imitation_mse=1.340038e-08, target_mse=1.720171e-02, formula_export_success=True
- icbr_full formula (display, rounded):
  - `6.03259e-5*sign(11.4848*(1 - 0.0543478*x_8)**(3/2) - 8.54331) + 0.28758 + 6.05296e-14/((1 - 0.0540541*x_6)**(3/2) - 0.776814)**5 - 1.92152e-10/(-0.805281 + exp(-0.05*x_4))**3`
- icbr_no_replay formula (display, rounded):
  - `6.03259e-5*sign(11.4848*(1 - 0.0543478*x_8)**(3/2) - 8.54331) + 0.28758 + 6.05296e-14/((1 - 0.0540541*x_6)**(3/2) - 0.776814)**5 - 1.92152e-10/(-0.805281 + exp(-0.05*x_4))**3`
- icbr_no_shared formula (display, rounded):
  - `6.03259e-5*sign(11.9259*(1 - 0.0520833*x_8)**(3/2) - 8.9926) + 0.28758 - 6.05296e-14/(0.776814 - (1 - 0.0540541*x_6)**(3/2))**5 - 1.92152e-10/(-0.805281 + exp(-0.05*x_4))**3`
- icbr_refit_commit formula (display, rounded):
  - `-0.00012352*sign(8.35284*(1 - 0.057795*x_8)**(3/2) - 6.25907) + 0.287438 + 1.51137e-11/(0.899908*exp(0.025*x_4) - 1)**3 + 5.17796e-14/((1 - 0.051629*x_6)**(3/2) - 0.786577)**5`

### task=feynman_I_9_18 seed=8

- Task source: feynman_file
- Target formula: `G*m1*m2/((x2-x1)**2+(y2-y1)**2+(z2-z1)**2)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.898704e-02, r2=-0.085501
- Variant formula overview:
  - icbr_full: symbolic_s=3.215636e-01, imitation_mse=1.571844e-09, target_mse=1.898681e-02, formula_export_success=True
  - icbr_no_replay: symbolic_s=2.850749e-01, imitation_mse=1.571844e-09, target_mse=1.898681e-02, formula_export_success=True
  - icbr_no_shared: symbolic_s=3.206392e-01, imitation_mse=1.571844e-09, target_mse=1.898681e-02, formula_export_success=True
  - icbr_refit_commit: symbolic_s=5.248640e-01, imitation_mse=1.343240e-08, target_mse=1.898917e-02, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0.256701 - 0.00205147*Abs(4.32633*(1 - 0.06*x_8)**(3/2) - 3.03635)`
- icbr_no_replay formula (display, rounded):
  - `0.256701 - 0.00205147*Abs(4.32633*(1 - 0.06*x_8)**(3/2) - 3.03635)`
- icbr_no_shared formula (display, rounded):
  - `0.256701 - 0.00205147*Abs(4.32633*(1 - 0.06*x_8)**(3/2) - 3.03635)`
- icbr_refit_commit formula (display, rounded):
  - `0.000379441*Abs(5.23163*(1 - 0.0623469*x_8)**(3/2) - 7.88954) + 0.254903`

### task=feynman_I_9_18 seed=9

- Task source: feynman_file
- Target formula: `G*m1*m2/((x2-x1)**2+(y2-y1)**2+(z2-z1)**2)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.678944e-02, r2=-0.000845
- Variant formula overview:
  - icbr_full: symbolic_s=1.205051e+00, imitation_mse=1.348650e-08, target_mse=1.679214e-02, formula_export_success=True
  - icbr_no_replay: symbolic_s=8.644460e-01, imitation_mse=1.697795e-08, target_mse=1.678242e-02, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.636893e+00, imitation_mse=1.348690e-08, target_mse=1.679214e-02, formula_export_success=True
  - icbr_refit_commit: symbolic_s=2.206333e+00, imitation_mse=1.397220e-08, target_mse=1.678995e-02, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0.000314147*sign(-4.83613*(1 - 0.0606061*x_4)**(3/2) - 3.34016*(1 - 0.0603015*x_6)**(3/2) - 2.97515*(1 - 0.0606061*x_8)**(3/2) + 8.10611) + 0.284377 - 8.92625e-8/(-0.218937*x_4 - 0.0364108*(-0.01*x_8 - 1)**4 + 1)**3 + 2.61185e-13/((1 - 0.0612245*x_4)**(3/2) - 0.751116)**5`
- icbr_no_replay formula (display, rounded):
  - `-0.000929348*Abs(4.81183*(1 - 0.0606061*x_4)**(3/2) - 13.5706 + 5.6902*exp(-0.05*x_8) + 6.36146*exp(-0.05*x_6)) + 0.284803 - 2.00946e-12/(-0.00698648*(-0.01*x_8 - 1)**4 - 0.784191 + exp(-0.05*x_4))**5 + 2.61185e-13/((1 - 0.0612245*x_4)**(3/2) - 0.751116)**5`
- icbr_no_shared formula (display, rounded):
  - `0.000314147*sign(-4.81498*(1 - 0.0609137*x_4)**(3/2) - 3.35469*(1 - 0.06*x_6)**(3/2) - 2.98816*(1 - 0.0603015*x_8)**(3/2) + 8.11265) + 0.284377 - 8.92625e-8/(-0.218937*x_4 - 0.0364108*(-0.01*x_8 - 1)**4 + 1)**3 + 2.55501e-13/((1 - 0.0609137*x_4)**(3/2) - 0.752322)**5`
- icbr_refit_commit formula (display, rounded):
  - `0.000256744*sign(-4.8387*(1 - 0.0609202*x_4)**(3/2) + 3.17465*(0.0520575*x_6 + 1)**(3/2) + 2.63077*(0.0559243*x_8 + 1)**(3/2) - 3.82988) + 0.284427 + 2.57715e-9/(-0.00486347*(1 - 0.0400038*x_8)**4 + 0.718564*(0.0569339*x_4 + 1)**(3/2) - 1)**3 + 5.54726e-14/((1 - 0.0569684*x_4)**(3/2) - 0.764621)**5`

### task=feynman_I_9_18 seed=10

- Task source: feynman_file
- Target formula: `G*m1*m2/((x2-x1)**2+(y2-y1)**2+(z2-z1)**2)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.557820e-02, r2=-0.001530
- Variant formula overview:
  - icbr_full: symbolic_s=3.268644e-01, imitation_mse=5.759627e-09, target_mse=1.557777e-02, formula_export_success=True
  - icbr_no_replay: symbolic_s=2.832027e-01, imitation_mse=5.759627e-09, target_mse=1.557777e-02, formula_export_success=True
  - icbr_no_shared: symbolic_s=3.212547e-01, imitation_mse=5.759627e-09, target_mse=1.557777e-02, formula_export_success=True
  - icbr_refit_commit: symbolic_s=5.770105e-01, imitation_mse=5.754276e-09, target_mse=1.557774e-02, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0.285617 - 2.3449e-12/(0.758246 - (1 - 0.0609137*x_8)**(3/2))**5`
- icbr_no_replay formula (display, rounded):
  - `0.285617 - 2.3449e-12/(0.758246 - (1 - 0.0609137*x_8)**(3/2))**5`
- icbr_no_shared formula (display, rounded):
  - `0.285617 - 2.3449e-12/(0.758246 - (1 - 0.0609137*x_8)**(3/2))**5`
- icbr_refit_commit formula (display, rounded):
  - `0.285617 + 2.67916e-12/((1 - 0.062318*x_8)**(3/2) - 0.753113)**5`

### task=feynman_I_9_18 seed=11

- Task source: feynman_file
- Target formula: `G*m1*m2/((x2-x1)**2+(y2-y1)**2+(z2-z1)**2)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.698013e-02, r2=0.000495
- Variant formula overview:
  - icbr_full: symbolic_s=1.983035e+00, imitation_mse=2.056279e-08, target_mse=1.698070e-02, formula_export_success=True
  - icbr_no_replay: symbolic_s=1.270194e+00, imitation_mse=2.067775e-08, target_mse=1.698065e-02, formula_export_success=True
  - icbr_no_shared: symbolic_s=2.816552e+00, imitation_mse=2.056274e-08, target_mse=1.698070e-02, formula_export_success=True
  - icbr_refit_commit: symbolic_s=3.441088e+00, imitation_mse=2.835657e-08, target_mse=1.698251e-02, formula_export_success=True
- icbr_full formula (display, rounded):
  - `-0.000486817*Abs(17.346 - 20.454*exp(-0.05*x_8)) - 0.00150903*Abs(0.0847634*Abs(2.65*x_1 - 3.55) + 14.7782 - 17.3254*exp(-0.05*x_8) + 1.28997e-9/(x_5 - 0.97)**5) + 8.09274e-5*sign(-0.153943*x_8 - 0.00925042*Abs(2.55*x_9 - 3.55) - 3.42735 + 4.73553*exp(-0.05*x_4)) + 0.286703 - 3.51129e-13/(-(-0.00742049 + 0.00799106*exp(-0.1*x_8))*(0.00183352 - 0.00870971*exp(-0.1*x_8) - 4.63173e-9/(0.977778 - x_9)**4 - 4.66802e-9/(0.977778 - x_5)**4) + 0.0324324)**5`
- icbr_no_replay formula (display, rounded):
  - `-0.000486817*Abs(11.5911*(1 - 0.0549451*x_8)**(3/2) - 8.58898) - 0.00150903*Abs(-10.151*(1 - 0.0529101*x_8)**(3/2) + 0.0847634*Abs(2.65*x_1 - 3.55) + 7.69998 + 1.28997e-9/(x_5 - 0.97)**5) + 8.09274e-5*sign(-0.00925042*Abs(2.55*x_9 - 3.55) - 7.04563 + 3.66803*exp(-0.05*x_8) + 4.73553*exp(-0.05*x_4)) + 0.286703 - 3.51129e-13/(-(0.0127827 - 0.0126959*(0.01*x_8 + 1)**4)*(0.0138377*(0.01*x_8 + 1)**4 - 0.0201856 + 4.55785e-10/(0.97 - x_9)**5 + 4.98988e-10/(0.969388 - x_5)**5) + 0.0324324)**5`
- icbr_no_shared formula (display, rounded):
  - `-0.000486817*Abs(17.346 - 20.454*exp(-0.05*x_8)) - 0.00150903*Abs(0.0847634*Abs(2.65*x_1 - 3.55) + 14.7782 - 17.3254*exp(-0.05*x_8) + 1.28997e-9/(x_5 - 0.97)**5) + 8.09274e-5*sign(-0.153943*x_8 - 0.00925042*Abs(2.55*x_9 - 3.55) - 3.42735 + 4.73553*exp(-0.05*x_4)) + 0.286703 - 3.51129e-13/(-(-0.00742049 + 0.00799106*exp(-0.1*x_8))*(0.00183352 - 0.00870971*exp(-0.1*x_8) - 4.63173e-9/(x_9 - 0.977778)**4 - 4.66802e-9/(x_5 - 0.977778)**4) + 0.0324324)**5`
- icbr_refit_commit formula (display, rounded):
  - `-0.000296701*Abs(27.0018 - 29.9043*exp(-0.03264*x_8)) + 0.00112389*Abs(0.0757116*Abs(3.7*x_1 - 4.99997) + 28.9603 - 32.857*exp(-0.03056*x_8) - 5.16567e-5/(0.332651*x_5 - 1)**5) + 6.1233e-5*sign(-1.56048*(0.0634059*x_8 + 1)**(3/2) - 17.9871*exp(0.01132*x_4) - 0.00704851*Abs(3.566*x_9 - 4.9996) + 20.8295) + 0.285672 - 1.88385e-14/(-(-0.00460524 + 0.00566578*exp(-0.2*x_8))*(-0.00707262*(1 - 0.0304101*x_8)**4 - 0.00586797*sign(4.94342 - 4.908*x_9) - 0.00572752 - 4.8935e-9/(0.977395 - x_5)**4) + 0.0200009)**5`

### task=feynman_I_9_18 seed=12

- Task source: feynman_file
- Target formula: `G*m1*m2/((x2-x1)**2+(y2-y1)**2+(z2-z1)**2)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.457448e-02, r2=0.000613
- Variant formula overview:
  - icbr_full: symbolic_s=9.567213e-01, imitation_mse=1.056017e-08, target_mse=1.457146e-02, formula_export_success=True
  - icbr_no_replay: symbolic_s=7.001868e-01, imitation_mse=1.056017e-08, target_mse=1.457146e-02, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.253068e+00, imitation_mse=1.055999e-08, target_mse=1.457146e-02, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.697525e+00, imitation_mse=1.562739e-08, target_mse=1.457320e-02, formula_export_success=True
- icbr_full formula (display, rounded):
  - `-0.000479197*Abs(-4.95*(2.48821 - 2.58549*(1 - 0.0534759*x_6)**(3/2))*(2.64961*(1 - 0.0546448*x_4)**(3/2) - 2.54701) - 1.6) - 5.87121e-5*sign(2.49907 - 3.5552*(1 - 0.06*x_8)**(3/2)) - 7.5452e-5*sign(5.36376 - 7.54742*(1 - 0.0603015*x_4)**(3/2)) + 0.289283`
- icbr_no_replay formula (display, rounded):
  - `-0.000479197*Abs(-4.95*(2.48821 - 2.58549*(1 - 0.0534759*x_6)**(3/2))*(2.64961*(1 - 0.0546448*x_4)**(3/2) - 2.54701) - 1.6) - 7.5452e-5*sign(5.36376 - 7.54742*(1 - 0.0603015*x_4)**(3/2)) - 5.87121e-5*sign(5.69047 - 6.77534*exp(-0.05*x_8)) + 0.289283`
- icbr_no_shared formula (display, rounded):
  - `-0.000479197*Abs(-4.95*(2.48821 - 2.58549*(1 - 0.0534759*x_6)**(3/2))*(2.61132*(1 - 0.0555556*x_4)**(3/2) - 2.50795) - 1.6) - 5.87121e-5*sign(2.49907 - 3.5552*(1 - 0.06*x_8)**(3/2)) - 7.5452e-5*sign(5.39745 - 7.58028*(1 - 0.06*x_4)**(3/2)) + 0.289283`
- icbr_refit_commit formula (display, rounded):
  - `-0.000324714*Abs(-5.0*(2.46838 - 2.56602*(1 - 0.053935*x_6)**(3/2))*(2.74037*(1 - 0.052603*x_4)**(3/2) - 2.63948) - 1.4) - 5.69635e-5*sign(3.36864 - 4.70606*(1 - 0.0575751*x_4)**(3/2)) - 4.01595e-5*sign(2.92258*(0.0475216*x_8 + 1)**(3/2) - 3.68333) + 0.289285`

### task=feynman_I_9_18 seed=13

- Task source: feynman_file
- Target formula: `G*m1*m2/((x2-x1)**2+(y2-y1)**2+(z2-z1)**2)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=5.796647e-03, r2=0.616056
- Variant formula overview:
  - icbr_full: symbolic_s=1.814029e+00, imitation_mse=3.987592e-05, target_mse=5.712926e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=1.208456e+00, imitation_mse=4.043082e-05, target_mse=5.710848e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=2.587222e+00, imitation_mse=3.987581e-05, target_mse=5.712928e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=2.976791e+00, imitation_mse=4.169521e-05, target_mse=5.702948e-03, formula_export_success=True
- icbr_full formula (display, rounded):
  - `-0.0993476*cos(0.253676*sin(2.95*x_5 - 1.9) + 0.63567*cos(2.15*x_2 - 2.15) - 0.185482*Abs(3.65*x_9 - 4.6) - 7.1681) + 0.205131*atan(0.902868*(-0.166667*x_1 - 1)**4 + 0.762213*sin(0.45*x_8 + 1.65) + 0.256115*cos(1.95*x_9 - 4.925) + 0.276696*tan(1.45*x_2 + 0.55) + 0.209504*tan(1.0*x_5 - 5.0) - 8.6857 + 7.68139*exp(-0.05*x_4)) + 0.406778 + 0.0260308*exp(-24.5025*((3.39157 - 3.52515*(1 - 0.0537634*x_6)**(3/2))*(3.23492*(1 - 0.0537634*x_6)**(3/2) - 3.11234) + 0.414141)**2)`
- icbr_no_replay formula (display, rounded):
  - `-0.0993476*cos(-0.245763*cos(3.05*x_5 - 3.6) + 0.649493*tanh(2.2*x_2 - 3.7) + 0.185482*Abs(3.65*x_9 - 4.6) + 7.09755) + 0.205131*atan(4.03102*(1 - 0.06*x_4)**(3/2) + 4.23267*(1 - 0.0603015*x_8)**(3/2) + 1.61078*exp(0.4*x_1) + 0.276696*tan(1.45*x_2 + 0.55) + 0.209504*tan(1.0*x_5 - 5.0) - 9.12129 + 0.478717*exp(-8.1225*(1 - 0.438597*x_9)**2)) + 0.406778 + 0.0260308*exp(-24.5025*((3.39157 - 3.52515*(1 - 0.0537634*x_6)**(3/2))*(3.23492*(1 - 0.0537634*x_6)**(3/2) - 3.11234) + 0.414141)**2)`
- icbr_no_shared formula (display, rounded):
  - `-0.0993476*cos(0.253676*sin(2.95*x_5 - 1.9) + 0.63567*cos(2.15*x_2 - 2.15) - 0.185482*Abs(3.65*x_9 - 4.6) - 7.1681) + 0.205131*atan(0.902868*(-0.166667*x_1 - 1)**4 + 0.762213*sin(0.45*x_8 + 1.65) + 0.256115*cos(1.95*x_9 - 4.925) + 0.276696*tan(1.45*x_2 + 0.55) + 0.209504*tan(1.0*x_5 - 5.0) - 8.6857 + 7.68139*exp(-0.05*x_4)) + 0.406778 + 0.0260308*exp(-24.5025*((3.39157 - 3.52515*(1 - 0.0537634*x_6)**(3/2))*(3.18882*(1 - 0.0546448*x_6)**(3/2) - 3.06534) + 0.414141)**2)`
- icbr_refit_commit formula (display, rounded):
  - `-0.0980866*cos(0.286101*sin(2.56248*x_5 - 1.35736) + 0.636255*cos(2.15304*x_2 + 4.1292) - 0.18916*Abs(3.51772*x_9 - 4.42164) - 0.930318) + 0.18551*atan(4.76633*(1 - 0.0602033*x_8)**(3/2) + 1.01023*(-0.167183*x_1 - 1)**4 + 0.286992*cos(1.95708*x_9 + 1.3488) + 0.301889*tan(0.60014*x_2 + 1.272) + 0.272188*tan(0.78396*x_5 + 4.62048) - 15.5858 + 11.4241*exp(-0.036*x_4)) + 0.39513 + 0.0345704*exp(-10.8916*(-(2.45765 - 2.61816*(1 - 0.0761706*x_6)**(3/2))*(2.4025*(1 - 0.0761747*x_6)**(3/2) - 2.2552) - 0.316644)**2)`

### task=feynman_I_9_18 seed=14

- Task source: feynman_file
- Target formula: `G*m1*m2/((x2-x1)**2+(y2-y1)**2+(z2-z1)**2)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.483851e-02, r2=-0.001558
- Variant formula overview:
  - icbr_full: symbolic_s=3.355855e-01, imitation_mse=6.065010e-09, target_mse=1.483736e-02, formula_export_success=True
  - icbr_no_replay: symbolic_s=3.450535e-01, imitation_mse=6.065010e-09, target_mse=1.483736e-02, formula_export_success=True
  - icbr_no_shared: symbolic_s=3.347319e-01, imitation_mse=6.065010e-09, target_mse=1.483736e-02, formula_export_success=True
  - icbr_refit_commit: symbolic_s=5.872885e-01, imitation_mse=6.028190e-09, target_mse=1.483720e-02, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0.283195 + 7.22158e-13/((1 - 0.06*x_6)**(3/2) - 0.758764)**5`
- icbr_no_replay formula (display, rounded):
  - `0.283195 + 7.22158e-13/((1 - 0.06*x_6)**(3/2) - 0.758764)**5`
- icbr_no_shared formula (display, rounded):
  - `0.283195 + 7.22158e-13/((1 - 0.06*x_6)**(3/2) - 0.758764)**5`
- icbr_refit_commit formula (display, rounded):
  - `0.283194 + 3.44309e-13/((1 - 0.0560533*x_6)**(3/2) - 0.772562)**5`

### task=feynman_I_9_18 seed=15

- Task source: feynman_file
- Target formula: `G*m1*m2/((x2-x1)**2+(y2-y1)**2+(z2-z1)**2)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=6.399109e-03, r2=0.607449
- Variant formula overview:
  - icbr_full: symbolic_s=8.445926e-01, imitation_mse=3.747870e-05, target_mse=6.328515e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=7.026374e-01, imitation_mse=3.747975e-05, target_mse=6.329609e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.107279e+00, imitation_mse=3.745150e-05, target_mse=6.328339e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.416219e+00, imitation_mse=4.347821e-05, target_mse=6.370828e-03, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0.246525*atan(7.67337*(1 - 0.0609137*x_6)**(3/2) + 0.391256*tan(1.55*x_2 + 0.5) + 0.102102*tan(0.5*x_7 - 5.0) + 0.804*asin(1.15*x_3 - 1.7) - 25.5232 + 7.91652*exp(-0.05*x_8) + 15.9367*exp(-0.05*x_4)) + 0.387046`
- icbr_no_replay formula (display, rounded):
  - `0.246525*atan(8.2896*(1 - 0.0606061*x_4)**(3/2) + 7.67337*(1 - 0.0609137*x_6)**(3/2) + 4.13614*(1 - 0.0603015*x_8)**(3/2) + 0.391256*tan(1.55*x_2 + 0.5) + 0.804*asin(1.15*x_3 - 1.7) + 0.719403*atan(3.5*x_7 - 2.3) - 15.2937) + 0.387046`
- icbr_no_shared formula (display, rounded):
  - `0.246525*atan(7.63971*(1 - 0.0612245*x_6)**(3/2) + 0.391256*tan(1.55*x_2 + 0.5) + 1.08655*tan(0.85*x_3 - 1.25) + 0.102102*tan(0.5*x_7 - 5.0) - 25.4962 + 7.91652*exp(-0.05*x_8) + 15.9367*exp(-0.05*x_4)) + 0.387046`
- icbr_refit_commit formula (display, rounded):
  - `0.245241*atan(7.80773*(1 - 0.0590406*x_6)**(3/2) - 24.5799*exp(0.0128*x_8) + 0.533014*tan(0.768*x_2 - 1.87172) + 0.0871855*tan(0.398*x_7 - 4.93224) + 0.792333*asin(1.1548*x_3 - 1.69764) + 2.82888 + 20.0761*exp(-0.03764*x_4)) + 0.381679`

### task=feynman_I_9_18 seed=16

- Task source: feynman_file
- Target formula: `G*m1*m2/((x2-x1)**2+(y2-y1)**2+(z2-z1)**2)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.450734e-02, r2=-0.000488
- Variant formula overview:
  - icbr_full: symbolic_s=8.847062e-01, imitation_mse=1.874476e-08, target_mse=1.450795e-02, formula_export_success=True
  - icbr_no_replay: symbolic_s=5.800601e-01, imitation_mse=1.874476e-08, target_mse=1.450795e-02, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.061787e+00, imitation_mse=1.874476e-08, target_mse=1.450795e-02, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.449819e+00, imitation_mse=2.595744e-08, target_mse=1.450956e-02, formula_export_success=True
- icbr_full formula (display, rounded):
  - `-0.000460812*Abs(13.1836*(1 - 0.0529101*x_8)**(3/2) - 9.89446) - 9.5663e-5*sign(7.37216 - 10.0011*(1 - 0.0537634*x_4)**(3/2)) + 0.284456 - 7.26844e-13/(0.758485 - (1 - 0.0603015*x_8)**(3/2))**5`
- icbr_no_replay formula (display, rounded):
  - `-0.000460812*Abs(13.1836*(1 - 0.0529101*x_8)**(3/2) - 9.89446) - 9.5663e-5*sign(7.37216 - 10.0011*(1 - 0.0537634*x_4)**(3/2)) + 0.284456 - 7.26844e-13/(0.758485 - (1 - 0.0603015*x_8)**(3/2))**5`
- icbr_no_shared formula (display, rounded):
  - `-0.000460812*Abs(13.1836*(1 - 0.0529101*x_8)**(3/2) - 9.89446) - 9.5663e-5*sign(7.75963 - 10.3817*(1 - 0.0515464*x_4)**(3/2)) + 0.284456 - 7.26844e-13/(0.758485 - (1 - 0.0603015*x_8)**(3/2))**5`
- icbr_refit_commit formula (display, rounded):
  - `0.000225574*Abs(12.2054*(1 - 0.0577534*x_8)**(3/2) - 8.29644) - 6.73211e-5*sign(7.10768 - 9.97565*(1 - 0.0581767*x_4)**(3/2)) + 0.284223 - 4.97936e-13/(0.766147 - (1 - 0.0581155*x_8)**(3/2))**5`

### task=feynman_I_9_18 seed=17

- Task source: feynman_file
- Target formula: `G*m1*m2/((x2-x1)**2+(y2-y1)**2+(z2-z1)**2)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.367797e-02, r2=0.000793
- Variant formula overview:
  - icbr_full: symbolic_s=1.463040e+00, imitation_mse=3.154301e-08, target_mse=1.368139e-02, formula_export_success=True
  - icbr_no_replay: symbolic_s=9.914019e-01, imitation_mse=3.153900e-08, target_mse=1.368138e-02, formula_export_success=True
  - icbr_no_shared: symbolic_s=2.051713e+00, imitation_mse=3.140891e-08, target_mse=1.368120e-02, formula_export_success=True
  - icbr_refit_commit: symbolic_s=2.510625e+00, imitation_mse=4.700711e-08, target_mse=1.368397e-02, formula_export_success=True
- icbr_full formula (display, rounded):
  - `-0.000263097*Abs(-5.0*(3.64922 - 3.79295*(1 - 0.0537634*x_6)**(3/2))*(3.18335*(1 - 0.0537634*x_6)**(3/2) - 3.06272) - 2.65) + 0.000206958*sign(-4.975*(2.83096*(1 - 0.0515464*x_8)**(3/2) - 2.73112 - 0.000864932*exp(-25.0*(1 - 0.48*x_7)**2))*(0.644431*(1 - 0.06*x_4)**(3/2) + 1.47853*(1 - 0.0603015*x_6)**(3/2) - 2.03063 + 0.000725941*exp(-25.0*(1 - 0.81*x_7)**2)) + 1.5) + 0.283103 + 6.09452e-11/((1 - 0.06*x_4)**(3/2) - 0.609883)**5`
- icbr_no_replay formula (display, rounded):
  - `-0.000263097*Abs(-5.0*(3.64922 - 3.79295*(1 - 0.0537634*x_6)**(3/2))*(3.18335*(1 - 0.0537634*x_6)**(3/2) - 3.06272) - 2.65) + 0.000206958*sign(-4.975*(2.83096*(1 - 0.0515464*x_8)**(3/2) - 2.73112 - 0.000864932*exp(-25.0*(1 - 0.48*x_7)**2))*(1.47853*(1 - 0.0603015*x_6)**(3/2) - 2.60904 + 0.000725941*exp(-25.0*(1 - 0.81*x_7)**2) + 1.22804*exp(-0.05*x_4)) + 1.5) + 0.283103 + 2.42523e-12/(-0.79105 + exp(-0.05*x_4))**5`
- icbr_no_shared formula (display, rounded):
  - `-0.000263097*Abs(-5.0*(3.59411 - 3.73889*(1 - 0.0546448*x_6)**(3/2))*(2.89164*(1 - 0.06*x_6)**(3/2) - 2.76466) - 2.65) + 0.000206958*sign(-4.975*(2.83096*(1 - 0.0515464*x_8)**(3/2) - 2.73112 - 0.000864932*exp(-25.0*(1 - 0.48*x_7)**2))*(0.644431*(1 - 0.06*x_4)**(3/2) + 1.47853*(1 - 0.0603015*x_6)**(3/2) - 2.03063 + 0.000725941*exp(-25.0*(1 - 0.81*x_7)**2)) + 1.5) - 3.78693e-5*sign(2.18238*(1 - 0.06*x_4)**(3/2) - 1.48655) + 0.283147`
- icbr_refit_commit formula (display, rounded):
  - `0.000229353*Abs(-5.0*(2.65607 - 2.82818*(1 - 0.075798*x_6)**(3/2))*(3.41657*(1 - 0.049655*x_6)**(3/2) - 3.29998) - 3.76) - 3.77168e-5*sign(3.37619 - 2.61922*(0.0482786*x_4 + 1)**(3/2)) + 0.000137992*sign(-4.89892*(2.91577*(1 - 0.0498687*x_8)**(3/2) - 2.81734 - 0.000934378*exp(-24.9998*(1 - 0.470002*x_7)**2))*(1.47573*(1 - 0.0604332*x_6)**(3/2) - 0.587933*(0.0536364*x_4 + 1)**(3/2) - 0.81423 + 0.000737102*exp(-11.2204*(1 - 0.794022*x_7)**2)) + 1.538) + 0.282756`

### task=feynman_I_9_18 seed=18

- Task source: feynman_file
- Target formula: `G*m1*m2/((x2-x1)**2+(y2-y1)**2+(z2-z1)**2)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.623747e-02, r2=-0.008441
- Variant formula overview:
  - icbr_full: symbolic_s=7.146676e-01, imitation_mse=3.213075e-08, target_mse=1.623518e-02, formula_export_success=True
  - icbr_no_replay: symbolic_s=5.821932e-01, imitation_mse=3.188691e-08, target_mse=1.623530e-02, formula_export_success=True
  - icbr_no_shared: symbolic_s=8.865114e-01, imitation_mse=3.213079e-08, target_mse=1.623518e-02, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.179773e+00, imitation_mse=1.824051e-07, target_mse=1.623303e-02, formula_export_success=True
- icbr_full formula (display, rounded):
  - `-0.0175262*Abs(2.24068*(1 - 0.0603015*x_8)**(3/2) - 1.59162) + 0.280815 + 4.52942e-5/(-0.539685*x_8 + 0.000840212*tan(2.4*x_1 + 2.5) + 1)**5`
- icbr_no_replay formula (display, rounded):
  - `-0.0175262*Abs(3.62154 - 4.28851*exp(-0.05*x_8)) + 0.280815 + 1.28927e-10/(6.53505e-5*tan(2.4*x_1 + 2.5) - 0.908683 + exp(-0.05*x_8))**5`
- icbr_no_shared formula (display, rounded):
  - `-0.0175262*Abs(2.24068*(1 - 0.0603015*x_8)**(3/2) - 1.59162) + 0.280815 + 4.52942e-5/(-0.539685*x_8 + 0.000840212*tan(2.4*x_1 + 2.5) + 1)**5`
- icbr_refit_commit formula (display, rounded):
  - `-0.00774659*Abs(2.50023*(0.0520687*x_8 + 1)**(3/2) - 3.15449) + 0.280507 + 7.74795e-10/(-0.945506*exp(0.02244*x_8) + 1.08474e-6*tan(0.022*x_1 + 1.55348) + 1)**3`

### task=feynman_I_9_18 seed=19

- Task source: feynman_file
- Target formula: `G*m1*m2/((x2-x1)**2+(y2-y1)**2+(z2-z1)**2)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=9.563173e-03, r2=0.289152
- Variant formula overview:
  - icbr_full: symbolic_s=8.401027e-01, imitation_mse=2.026287e-05, target_mse=9.533228e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=6.317916e-01, imitation_mse=2.033739e-05, target_mse=9.557467e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.075926e+00, imitation_mse=2.026285e-05, target_mse=9.533231e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.366246e+00, imitation_mse=2.089901e-05, target_mse=9.530096e-03, formula_export_success=True
- icbr_full formula (display, rounded):
  - `-0.00154892*Abs(4.9*(0.432778*sin(0.35*x_4 + 2.0) - 0.441582)*(0.449109*sin(0.35*x_8 + 2.0) - 0.458259) - 1.05) + 0.243176*atan(0.193093*tan(1.5*x_1 - 2.55) + 0.146865*tan(1.25*x_3 + 3.75) + 0.290195) + 0.270921`
- icbr_no_replay formula (display, rounded):
  - `-0.00154892*Abs(4.9*(1.87313*(1 - 0.0603015*x_4)**(3/2) - 1.79031)*(2.13903*(1 - 0.0540541*x_8)**(3/2) - 2.0574) - 1.05) + 0.00922589 + 0.407945*exp(-0.213318*(-0.292652*tan(1.5*x_1 - 2.55) - 0.222589*tan(1.25*x_3 + 3.75) + 1)**2)`
- icbr_no_shared formula (display, rounded):
  - `-0.00154892*Abs(-4.9*(0.458259 - 0.449109*sin(0.35*x_8 + 2.0))*(0.379183*cos(0.4*x_4 + 3.4) + 0.444497) + 1.05) + 0.243176*atan(0.193093*tan(1.5*x_1 - 2.55) + 0.146865*tan(1.25*x_3 + 3.75) + 0.290195) + 0.270921`
- icbr_refit_commit formula (display, rounded):
  - `-0.000846996*Abs(-5.0*(0.470281 - 0.368097*sin(0.4272*x_8 + 1.71544))*(0.316145*sin(0.47964*x_4 - 1.61788) + 0.45841) + 0.9) + 0.0263733 + 0.406754*exp(-0.183403*(-0.395605*tan(1.13736*x_1 - 2.13752) - 0.211686*tan(0.807*x_3 + 0.99484) + 1)**2)`

### task=feynman_I_9_18 seed=20

- Task source: feynman_file
- Target formula: `G*m1*m2/((x2-x1)**2+(y2-y1)**2+(z2-z1)**2)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.405925e-02, r2=-0.013190
- Variant formula overview:
  - icbr_full: symbolic_s=3.440770e-01, imitation_mse=1.631059e-07, target_mse=1.405848e-02, formula_export_success=True
  - icbr_no_replay: symbolic_s=3.182006e-01, imitation_mse=1.631059e-07, target_mse=1.405848e-02, formula_export_success=True
  - icbr_no_shared: symbolic_s=3.865689e-01, imitation_mse=1.631059e-07, target_mse=1.405848e-02, formula_export_success=True
  - icbr_refit_commit: symbolic_s=5.679063e-01, imitation_mse=1.977766e-07, target_mse=1.406528e-02, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0.275869 - 0.0117666*Abs(12.0677*(1 - 0.0540541*x_8)**(3/2) - 8.95715)`
- icbr_no_replay formula (display, rounded):
  - `0.275869 - 0.0117666*Abs(12.0677*(1 - 0.0540541*x_8)**(3/2) - 8.95715)`
- icbr_no_shared formula (display, rounded):
  - `0.275869 - 0.0117666*Abs(12.0677*(1 - 0.0540541*x_8)**(3/2) - 8.95715)`
- icbr_refit_commit formula (display, rounded):
  - `0.275671 - 0.0116141*Abs(12.0046*(1 - 0.0517994*x_8)**(3/2) - 9.02218)`

### task=feynman_I_10_7 seed=1

- Task source: feynman_file
- Target formula: `m_0/sqrt(1-v**2/c**2)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=3.003362e-03, r2=0.997856
- Variant formula overview:
  - icbr_full: symbolic_s=3.536571e+00, imitation_mse=4.101141e-03, target_mse=5.559786e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=2.215975e+00, imitation_mse=8.363572e-03, target_mse=1.094056e-02, formula_export_success=True
  - icbr_no_shared: symbolic_s=5.060371e+00, imitation_mse=4.113351e-03, target_mse=5.569391e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=6.495559e+00, imitation_mse=4.493448e-03, target_mse=5.258390e-03, formula_export_success=True
- icbr_full formula (display, rounded):
  - `-2.3546*(0.00843127*cos(3.15*x_2 - 3.7) - 0.0108659*atanh(0.4*x_1 - 1.4) - 0.482381*atanh(0.0499997*x_3 - 0.4) + 1)**(3/2) + 32.8705*log(0.05*(-0.129508*Abs(4.35*x_1 - 4.775) - 3.09643*atanh(0.0499997*x_3 - 0.4) - 1.62509)*(0.14323*cos(2.9*x_2 - 3.35) - 1.68312*acos(0.0499997*x_3 - 0.5) - 2.03292*atanh(0.3*x_1 - 1.0) + 1.04154) + 4.6) + 1.07379*sin(-0.135775*Abs(2.75*x_1 - 4.675) + 1.11429*acos(0.0499997*x_3 - 0.5) + 0.313811) - 0.166632*Abs(-4.0*(-0.0962471*cos(0.6*x_1 + 2.75) - 0.139934*cos(3.85*x_2 - 4.825) - 2.8062*acos(0.0499997*x_3 - 0.5) + 6.24219)*(0.0459954*tan(1.8*x_2 + 3.5) - 0.0330211*tanh(0.6*x_1 - 2.0) + 1.17371*atanh(0.0499997*x_3 - 0.4) + 0.536778) + 1.35) + 0.0356301*Abs(1.91347*asin(0.3*x_1 - 1.3) + 26.3967*atanh(0.0499997*x_3 - 0.4) + 8.45686) - 0.0705194*atanh(1.78768*atanh(0.0499997*x_3 - 0.4) - 0.537574) - 47.5123 + 0.048612/(atanh(0.0499997*x_3 - 0.4) + 0.448382 + 0.138948/(x_1 - 0.2)**5)**2`
- icbr_no_replay formula (display, rounded):
  - `-0.640625*(-0.121849*Abs(2.75*x_1 - 4.675) - asin(0.0499997*x_3 - 0.5) + 0.436625)**2 - 2.18685*(0.00885711*cos(3.15*x_2 - 3.7) - 0.503173*asin(0.0499997*x_3 - 0.5) - 0.0114147*atanh(0.4*x_1 - 1.4) + 1)**(3/2) + 0.0207164*tan(7.10031*acos(0.0499997*x_3 - 0.5) - 18.5156) + 0.0704236*Abs(-4.85*(-0.129508*Abs(4.35*x_1 - 4.775) - 3.09643*atanh(0.0499997*x_3 - 0.4) - 1.62509)*(0.14323*cos(2.9*x_2 - 3.35) - 1.68312*acos(0.0499997*x_3 - 0.5) - 1.50935*asin(0.4*x_1 - 1.35) + 1.01145) - 0.45) - 0.166632*Abs(4.0*(0.00971978*Abs(1.75*x_1 - 2.65) + 1.16543*acos(0.0499997*x_3 - 0.5) - 0.0496089*asin(1.8*x_2 - 2.8) - 2.51624)*(0.019658*Abs(2.65*x_1 - 3.7) - 0.111489*Abs(3.9*x_2 - 4.9) + 2.8062*acos(0.0499997*x_3 - 0.5) - 6.16565) - 1.35) + 0.0356301*Abs(26.2106*asin(0.0499997*x_3 - 0.5) + 1.36624*atanh(0.4*x_1 - 1.35) + 10.505) - 0.841846*atan(-11.3551*acos(0.0499997*x_3 - 0.5) + 21.9697 + 4.0941*exp(-25.0*(1 - 0.995*x_1)**2)) + 5.04499`
- icbr_no_shared formula (display, rounded):
  - `-2.3546*(0.00843127*cos(3.15*x_2 - 3.7) - 0.0108659*atanh(0.4*x_1 - 1.4) - 0.482381*atanh(0.0499997*x_3 - 0.4) + 1)**(3/2) + 32.8705*log(0.05*(-0.137404*Abs(4.1*x_1 - 4.5) - 3.09643*atanh(0.0499997*x_3 - 0.4) - 1.62502)*(0.14323*cos(2.9*x_2 - 3.35) - 1.68312*acos(0.0499997*x_3 - 0.5) - 2.03292*atanh(0.3*x_1 - 1.0) + 1.04154) + 4.6) + 1.07379*sin(-0.135775*Abs(2.75*x_1 - 4.675) + 1.11429*acos(0.0499997*x_3 - 0.5) + 0.313811) - 0.196223*Abs(-3.4*(-0.0962471*cos(0.6*x_1 + 2.75) - 0.139934*cos(3.85*x_2 - 4.825) - 2.8062*acos(0.0499997*x_3 - 0.5) + 6.24219)*(0.0459954*tan(1.8*x_2 + 3.5) - 0.0330211*tanh(0.6*x_1 - 2.0) + 1.17371*atanh(0.0499997*x_3 - 0.4) + 0.536778) + 1.15) + 0.0356301*Abs(1.91347*asin(0.3*x_1 - 1.3) + 26.3967*atanh(0.0499997*x_3 - 0.4) + 8.45686) - 0.0705194*atanh(1.78768*atanh(0.0499997*x_3 - 0.4) - 0.537574) - 47.5124 + 0.048612/(atanh(0.0499997*x_3 - 0.4) + 0.448382 + 0.138948/(x_1 - 0.2)**5)**2`
- icbr_refit_commit formula (display, rounded):
  - `-14.9001*(0.00217234*cos(3.76496*x_2 - 4.54632) - 0.00437789*atanh(0.102*x_1 - 1.1) - atanh(0.004*x_3 - 0.68864) - 0.498609)**(3/2) + 18.5891*log(0.0999999*(-0.129865*Abs(4.322*x_1 + 4.58448) - 17.8805*atanh(0.00599999*x_3 - 0.60026) - 11.535)*(0.156729*cos(2.55292*x_2 - 2.83756) + 1.1472*asin(0.0736799*x_3 - 0.60116) - 2.03037*atanh(0.30032*x_1 - 1.00084) - 1.76856) + 4.99935) - 1.07503*sin(0.214595*Abs(1.74484*x_1 - 3.07724) + 0.718765*acos(0.60028 - 0.0779999*x_3) - 3.30927) - 0.1431*Abs(4.5476*(0.0961666*cos(0.60064*x_1 - 0.39304) - 0.139843*cos(3.853*x_2 - 4.82876) + 1.905*acos(0.60036 - 0.0739999*x_3) - 1.42391)*(0.0459488*tan(1.80128*x_2 + 3.49824) - 0.0329645*tanh(0.60152*x_1 - 2.00436) + 0.791181*acos(0.60012 - 0.0739999*x_3) - 0.699547) - 1.51104) + 0.0400698*Abs(1.686*asin(0.30048*x_1 - 1.30056) + 14.8186*asin(0.0785599*x_3 - 0.60272) + 7.44716) - 0.0621545*atanh(21.7774*atanh(0.00436*x_3 - 0.63688) + 14.93) - 27.2744 + 0.00145473/(atanh(0.00599999*x_3 - 0.6) + 0.698915 - 0.0240309/(0.200154 - x_1)**5)**2`

### task=feynman_I_10_7 seed=2

- Task source: feynman_file
- Target formula: `m_0/sqrt(1-v**2/c**2)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=6.079824e-03, r2=0.995837
- Variant formula overview:
  - icbr_full: symbolic_s=3.104909e+00, imitation_mse=1.440883e-03, target_mse=5.164017e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=2.003438e+00, imitation_mse=1.821697e-03, target_mse=5.325709e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=4.517369e+00, imitation_mse=1.440846e-03, target_mse=5.164017e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=5.732709e+00, imitation_mse=nan, target_mse=nan, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0.142893*(16.5116*sqrt(0.0301508*x_1 + 1) + 10.5883*atanh(0.0499997*x_3 - 0.4) - 12.3893)*(0.0631642*cos(4.2*x_2 - 2.25) + 4.16264*atanh(0.0499997*x_3 - 0.4) - 1.70732 + 9.36177*exp(-(0.1*x_1 - 1.0)**2)) - 1.03226*sin(5.01904*sqrt(0.123457*x_1 + 1) - 4.47795*acos(0.0499997*x_3 - 0.5) + 0.253813) + 0.313878*cos(-0.038179*Abs(3.2*x_1 - 4.9) + 8.82959*atanh(0.0499997*x_3 - 0.4) + 7.82672) - 0.154051*Abs(29.275*asin(0.0499997*x_3 - 0.5) - 0.197895*sign(3.4*x_2 - 3.95) + 30.3981 - 27.2477*exp(-(0.1*x_1 - 1.0)**2)) + 0.759279 + 1.11648*exp(-120.505*(-0.00381206*Abs(2.9*x_1 - 3.5) - 0.478288*acos(0.0499997*x_3 - 0.5) + 1)**2) + 0.167283*exp(-64.2743*(1 - 0.509591*acos(0.0499997*x_3 - 0.5))**2) + 0.574173/(-2.0*(-7.76937*asin(0.0499997*x_3 - 0.5) - 3.89797)*(0.224638*acos(0.4*x_1 - 1.4) - 4.86569*acos(0.0499997*x_3 - 0.5) + 9.42873) - 0.0500002)`
- icbr_no_replay formula (display, rounded):
  - `9.26125*(-0.00797022*Abs(2.9*x_1 - 3.5) + asin(0.0499997*x_3 - 0.5) + 0.116483)**2 + 0.142893*(10.5144*asin(0.0499997*x_3 - 0.5) + 2.22503 + 5.61969*exp(-0.64*(0.0625*x_1 - 1)**2))*(0.0570476*Abs(3.65*x_2 - 4.65) + 4.13359*asin(0.0499997*x_3 - 0.5) - 1.37109 + 9.36177*exp(-(0.1*x_1 - 1.0)**2)) - 1.03226*sin(-0.845232*acos(0.3*x_1 - 1.0) + 4.47795*asin(0.0499997*x_3 - 0.5) + 0.505999) + 0.313878*cos(-0.038179*Abs(3.2*x_1 - 4.9) + 8.76798*asin(0.0499997*x_3 - 0.5) + 8.70698) - 0.154051*Abs(29.275*asin(0.0499997*x_3 - 0.5) - 0.197895*sign(3.4*x_2 - 3.95) + 30.3981 - 27.2477*exp(-(0.1*x_1 - 1.0)**2)) + 0.754247 + 0.167283*exp(-16.6909*(asin(0.0499997*x_3 - 0.5) + 0.391563)**2) + 0.574173/(-2.0*(7.76937*acos(0.0499997*x_3 - 0.5) - 16.1021)*(-0.224638*asin(0.4*x_1 - 1.4) + 4.86569*asin(0.0499997*x_3 - 0.5) + 2.13857) - 0.0500002)`
- icbr_no_shared formula (display, rounded):
  - `0.142893*(16.432*sqrt(0.030303*x_1 + 1) + 10.5883*atanh(0.0499997*x_3 - 0.4) - 12.3098)*(0.0631642*cos(4.2*x_2 - 2.25) + 4.16264*atanh(0.0499997*x_3 - 0.4) - 1.70732 + 9.36177*exp(-(0.1*x_1 - 1.0)**2)) - 1.03226*sin(5.01904*sqrt(0.123457*x_1 + 1) - 4.47795*acos(0.0499997*x_3 - 0.5) + 0.253813) + 0.313878*cos(-0.038179*Abs(3.2*x_1 - 4.9) + 8.82959*atanh(0.0499997*x_3 - 0.4) + 7.82672) - 0.154051*Abs(29.275*asin(0.0499997*x_3 - 0.5) - 0.197895*sign(3.4*x_2 - 3.95) + 30.3981 - 27.2477*exp(-(0.1*x_1 - 1.0)**2)) + 0.759279 + 1.11648*exp(-120.505*(-0.00381206*Abs(2.9*x_1 - 3.5) - 0.478288*acos(0.0499997*x_3 - 0.5) + 1)**2) + 0.167283*exp(-16.6909*(-asin(0.0499997*x_3 - 0.5) - 0.391563)**2) + 0.574173/(-2.0*(-7.76937*asin(0.0499997*x_3 - 0.5) - 3.89797)*(-4.86569*acos(0.0499997*x_3 - 0.5) - 0.224638*asin(0.4*x_1 - 1.4) + 9.78159) - 0.0500002)`
- icbr_refit_commit formula (display, rounded):
  - `3.62993*(-0.00788593*Abs(4.5*x_1 - 4.99919) + asin(0.0779999*x_3 - 0.60064) - 0.00769319)**2 + 0.142841*(85.8947*atanh(0.00392*x_3 - 0.63496) + 62.5232 + 3.70033*exp(-0.81036*(1 - 0.0844256*x_1)**2))*(-0.0631556*cos(4.20092*x_2 + 0.89036) + 31.7566*atanh(0.0042*x_3 - 0.63284) + 17.9128 + 12.9213*exp(-0.810108*(1 - 0.0799946*x_1)**2)) + 9.90737*sin(1.55623*sqrt(0.122276*x_1 + 1) + 0.880479*acos(0.60336 - 0.0787199*x_3) - 1.58718) + 0.518646*sin(0.0395769*Abs(1.9146*x_1 - 2.62216) - 3.69283*acos(0.60544 - 0.0780799*x_3) + 0.0522417) - 0.241118*Abs(12.006*asin(0.0779999*x_3 - 0.60128) - 0.113681*sign(4.096*x_2 - 4.59866) + 24.3282 - 25.2611*exp(-0.810108*(0.0755504*x_1 - 1)**2)) + 1.35824*atan(4.99989*(-5.00376*asin(0.0781599*x_3 - 0.60104) - 2.996)*(3.14173*acos(0.60016 - 0.0779599*x_3) + 0.212792*acos(0.42244*x_1 - 1.42784) - 3.68159) + 0.4) - 5.69377 + 0.190348*exp(-4.9969*(asin(0.0779999*x_3 - 0.60128) + 0.498497)**2)`

### task=feynman_I_10_7 seed=3

- Task source: feynman_file
- Target formula: `m_0/sqrt(1-v**2/c**2)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=3.509219e-03, r2=0.997671
- Variant formula overview:
  - icbr_full: symbolic_s=2.456937e+00, imitation_mse=7.892341e-04, target_mse=3.667539e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=1.630510e+00, imitation_mse=1.372017e-03, target_mse=4.059964e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=3.665313e+00, imitation_mse=7.891933e-04, target_mse=3.666760e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=4.633160e+00, imitation_mse=1.546791e-03, target_mse=4.458473e-03, formula_export_success=True
- icbr_full formula (display, rounded):
  - `-0.723644*sin(-7.26358*sqrt(0.06*x_1 + 1) + 3.74152*asin(0.0499997*x_3 - 0.5) + 8.986) + 0.258381*tan(3.6543*acos(0.0499997*x_3 - 0.5) - 5.33622 + 3.5187*exp(-(0.1*x_1 - 1.0)**2)) + 4.74312*asin(2.79088*log(0.1*x_1 + 4.6) + 0.0139097*Abs(3.95*x_2 - 4.95) + 1.17465*asin(0.0499997*x_3 - 0.5) - 4.34428) + 1.00536*atan(10.5179*log(0.15*x_1 + 4.5) + 1.23679*acos(0.0499997*x_3 - 0.5) - 19.7928) + 5.1925 - 1.88519*exp(-9.06466*(0.368401*atanh(0.0499997*x_3 - 0.4) + 0.33597 - exp(-(0.1*x_1 - 1.0)**2))**2) - 1.01046/(3.25*(-5.84132*atanh(0.0499997*x_3 - 0.4) - 2.32766)*(2.78069*(1 - 0.655172*x_2)**2 + 2.38906*atanh(0.0499997*x_3 - 0.4) + 1.30314) - 0.45)`
- icbr_no_replay formula (display, rounded):
  - `0.727514*cos(7.26358*sqrt(0.06*x_1 + 1) + 3.74152*acos(0.0499997*x_3 - 0.5) - 10.1632) + 0.258381*tan(0.0662337*Abs(4.5*x_1 - 4.925) + 3.6543*acos(0.0499997*x_3 - 0.5) - 3.74982) + 0.206606*atan(1.65*(5.80039*acos(0.0499997*x_3 - 0.5) - 12.0212)*(-2.37232*acos(0.0499997*x_3 - 0.5) + 0.123806*sign(3.7 - 3.2*x_2) + 5.44925) + 1.2) + 1.00536*atan(9.41869*sqrt(0.0748663*x_1 + 1) + 1.23679*acos(0.0499997*x_3 - 0.5) - 13.3935) + 0.852282*atan(2.20279*acos(0.0499997*x_3 - 0.5) - 7.25433 + 6.02152*exp(-(0.1*x_1 - 1.0)**2)) + 9.47686*atanh(1.39544*log(0.1*x_1 + 4.6) + 0.00695484*Abs(3.95*x_2 - 4.95) + 0.587322*asin(0.0499997*x_3 - 0.5) - 2.22213) + 5.00339`
- icbr_no_shared formula (display, rounded):
  - `-0.723644*sin(-7.26358*sqrt(0.06*x_1 + 1) + 3.74152*asin(0.0499997*x_3 - 0.5) + 8.986) + 0.258381*tan(-3.6543*asin(0.0499997*x_3 - 0.5) + 0.403935 + 3.5187*exp(-(0.1*x_1 - 1.0)**2)) + 4.74312*asin(2.79088*log(0.1*x_1 + 4.6) + 0.0139097*Abs(3.95*x_2 - 4.95) + 1.17465*asin(0.0499997*x_3 - 0.5) - 4.34428) + 1.00536*atan(9.69374*sqrt(0.0725389*x_1 + 1) + 1.23679*acos(0.0499997*x_3 - 0.5) - 13.6674) + 5.1925 - 1.88519*exp(-9.06466*(0.368401*atanh(0.0499997*x_3 - 0.4) + 0.33597 - exp(-(0.1*x_1 - 1.0)**2))**2) - 1.01046/(3.25*(-5.84132*atanh(0.0499997*x_3 - 0.4) - 2.32766)*(2.78069*(1 - 0.655172*x_2)**2 + 2.38906*atanh(0.0499997*x_3 - 0.4) + 1.30314) - 0.45)`
- icbr_refit_commit formula (display, rounded):
  - `-0.465821*tan(18.1639*atanh(0.00408*x_3 - 0.65692) + 15.723 + 1.36002*exp(-0.0361455*(-0.927625*x_1 - 1)**2)) - 0.894725*tanh(-6.39805*sqrt(0.0559087*x_1 + 1) + 23.3358*atanh(0.00416*x_3 - 0.64572) + 24.1496) + 4.65048*asin(3.05833*log(0.0943999*x_1 + 4.68796) + 0.0137199*Abs(4.0*x_2 - 5.0) + 0.772922*asin(0.0779999*x_3 - 0.60048) - 4.94785) + 3.61025 - 1.88446*exp(-17.281*(-0.153844*atanh(0.0859999*x_3 - 0.60024) - 0.41199 + exp(-0.810288*(1 - 0.0799857*x_1)**2))**2) + 0.0138941/(0.582036*sqrt(0.0734056*x_1 + 1) - 0.0435673*atanh(0.0859999*x_3 - 0.6006) - 1)**4 + 0.883256/(-2.84196*(-44.1527*atanh(0.00416*x_3 - 0.64228) - 33.5603)*(2.77536*(1 - 0.65473*x_2)**2 + 13.8019*atanh(0.00599999*x_3 - 0.60006) + 9.88006) + 0.39268)`

### task=feynman_I_10_7 seed=4

- Task source: feynman_file
- Target formula: `m_0/sqrt(1-v**2/c**2)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=4.864902e-03, r2=0.996456
- Variant formula overview:
  - icbr_full: symbolic_s=2.812079e+00, imitation_mse=3.662106e-03, target_mse=6.503371e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=1.841369e+00, imitation_mse=6.017652e-03, target_mse=7.831263e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=4.200687e+00, imitation_mse=3.663599e-03, target_mse=6.501676e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=5.142023e+00, imitation_mse=5.555634e-03, target_mse=8.007919e-03, formula_export_success=True
- icbr_full formula (display, rounded):
  - `23.2446*sqrt(-0.00819644*cos(3.05*x_2 - 3.5) + 0.193178*tan(0.05*x_3 - 3.55) + 0.0518888*asin(0.4*x_1 - 1.35) + 1) + 1.01414*tanh(0.4*(-2.49543*tan(0.05*x_3 - 3.55) + 1.05571*asin(0.3*x_1 - 1.05) + 0.0152372)*(0.996426*sin(0.95*x_1 + 3.1) + 0.289527*sin(2.05*x_2 - 3.6) - 9.81291*acos(0.0499997*x_3 - 0.5) + 23.2953) - 1.2) - 0.124362*Abs(-3.55*(12.7159 - 6.13547*acos(0.0499997*x_3 - 0.5))*(1.29427*cos(0.35*x_1 + 0.45) + 0.0753214*Abs(3.8*x_2 - 4.9) + 2.12137*asin(0.0499997*x_3 - 0.5) + 0.0837952) - 2.7) - 1.7295*acos(-0.27358*acos(0.35*x_1 - 1.2) + 1.06929*atanh(0.0499997*x_3 - 0.4) + 0.466336) - 16.0366 + 0.176217*exp(-495.704*(-0.00456101*Abs(2.75*x_1 - 4.55) + 0.550715*acos(0.0499997*x_3 - 0.5) - 1)**2) + 1.61974*exp(-106.69*(tan(0.05*x_3 - 3.55) + 0.359062)**2)`
- icbr_no_replay formula (display, rounded):
  - `-7.09403*(0.00894862*cos(3.05*x_2 - 3.5) - 0.210906*tan(0.05*x_3 - 3.55) - 0.0566506*asin(0.4*x_1 - 1.35) + 1)**(3/2) + 0.826409*cos(0.7*(6.17095*tan(0.05*x_3 - 3.55) + 2.51447)*(2.13363*tan(0.05*x_3 - 3.55) - 0.161917*Abs(2.7*x_1 - 3.25) + 0.0753214*Abs(3.8*x_2 - 4.9) + 0.763014) + 0.6) + 1.01414*tanh(0.4*(-2.49543*tan(0.05*x_3 - 3.55) + 1.05571*asin(0.3*x_1 - 1.05) + 0.0152372)*(9.86964*tan(0.05*x_3 - 3.55) + 0.280513*tanh(2.2*x_2 - 3.7) + 0.26374*Abs(2.8*x_1 - 4.7) + 5.71485) - 1.2) + 1.7295*asin(1.06796*tan(0.05*x_3 - 3.55) + 0.27358*asin(0.35*x_1 - 1.2) + 0.0456129) + 10.6046 + 0.176217*exp(-152.084*(-tan(0.05*x_3 - 3.55) - 0.00823436*Abs(2.75*x_1 - 4.55) - 0.152243)**2) + 1.61974*exp(-106.69*(tan(0.05*x_3 - 3.55) + 0.359062)**2)`
- icbr_no_shared formula (display, rounded):
  - `22.9322*sqrt(-0.00830632*cos(3.05*x_2 - 3.5) + 0.195768*tan(0.05*x_3 - 3.55) + 0.0525845*asin(0.4*x_1 - 1.35) + 1) + 1.01414*tanh(0.4*(-2.49543*tan(0.05*x_3 - 3.55) + 1.05571*asin(0.3*x_1 - 1.05) + 0.0152372)*(0.996426*sin(0.95*x_1 + 3.1) + 0.289527*sin(2.05*x_2 - 3.6) - 9.81291*acos(0.0499997*x_3 - 0.5) + 23.2953) - 1.2) - 0.124362*Abs(-3.55*(12.7159 - 6.13547*acos(0.0499997*x_3 - 0.5))*(1.29427*cos(0.35*x_1 + 0.45) + 0.0753214*Abs(3.8*x_2 - 4.9) + 2.12137*asin(0.0499997*x_3 - 0.5) + 0.0837952) - 2.7) - 1.7295*acos(-0.27358*acos(0.35*x_1 - 1.2) + 1.06929*atanh(0.0499997*x_3 - 0.4) + 0.466336) - 15.7242 + 0.176217*exp(-495.704*(-0.00456101*Abs(2.75*x_1 - 4.55) + 0.550715*acos(0.0499997*x_3 - 0.5) - 1)**2) + 1.61974*exp(-106.69*(tan(0.05*x_3 - 3.55) + 0.359062)**2)`
- icbr_refit_commit formula (display, rounded):
  - `-4.16274*(0.0183427*cos(2.0442*x_2 - 2.15056) - 0.084827*asin(0.38288*x_1 - 1.27732) - 0.922901*asin(0.014*x_3 - 0.6) + 1)**(3/2) + 1.48038*tanh(0.26636*(-11.8395*tan(0.00767999*x_3 - 0.60824) + 0.845947*acos(1.22188 - 0.36616*x_1) - 8.55334)*(0.992311*cos(0.942*x_1 - 4.7) + 0.313331*tanh(1.94784*x_2 - 3.35396) - 34.4272*acos(0.01224*x_3 - 0.61728) + 79.7456) - 1.12444) - 0.097608*Abs(4.52332*(22.2243*acos(0.6164 - 0.01184*x_3) - 20.248)*(1.32698*cos(0.34*x_1 + 0.50122) + 0.0823583*Abs(3.44496*x_2 - 4.45916) + 1.44003*asin(0.0739999*x_3 - 0.60006) - 0.0926182) + 3.43972) + 2.45517*atanh(0.174029*acos(1.27696 - 0.38284*x_1) + 5.4807*atanh(0.00452*x_3 - 0.6206) + 3.4065) + 12.4795 - 0.169737*exp(-82.4464*(-0.00781027*Abs(2.55948*x_1 - 4.29996) - 0.603118*acos(0.60036 - 0.0739999*x_3) + 1)**2) + 4.41664*exp(-1338.96*(tan(0.00771999*x_3 - 0.6012) + 0.690738)**2)`

### task=feynman_I_10_7 seed=5

- Task source: feynman_file
- Target formula: `m_0/sqrt(1-v**2/c**2)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=4.616702e-03, r2=0.996805
- Variant formula overview:
  - icbr_full: symbolic_s=2.356293e+00, imitation_mse=1.023818e-02, target_mse=1.108889e-02, formula_export_success=True
  - icbr_no_replay: symbolic_s=1.534770e+00, imitation_mse=1.063867e-02, target_mse=1.136355e-02, formula_export_success=True
  - icbr_no_shared: symbolic_s=3.481089e+00, imitation_mse=1.024358e-02, target_mse=1.109373e-02, formula_export_success=True
  - icbr_refit_commit: symbolic_s=4.402580e+00, imitation_mse=9.780407e-03, target_mse=1.083841e-02, formula_export_success=True
- icbr_full formula (display, rounded):
  - `29.3451*sqrt(0.0230799*asin(0.4*x_1 - 1.4) + 0.179118*asin(0.0499997*x_3 - 0.5) + 1) - 0.291445*Abs(1.45412*sin(0.35*x_1 - 1.1) + 13.2014*acos(0.0499997*x_3 - 0.5) - 23.8952) - 0.688141*atan(-0.687121*asin(0.4*x_1 - 1.4) + 3.94487*atanh(0.0499997*x_3 - 0.4) + 0.67578) - 0.974918*atanh(0.75*(0.531358*sin(0.5*x_1 + 1.5) - 0.718291)*(0.0890044*Abs(2.85*x_1 - 4.25) + 0.284912) + 0.9) - 6.75262*atanh(0.0136293*sin(1.75*x_2 + 0.2) + 0.0637404*acos(0.45*x_1 - 1.45) + 0.415159*acos(0.0499997*x_3 - 0.5) - 0.63288) - 23.1108 + 1.10855*exp(-132.245*(atanh(0.0499997*x_3 - 0.4) + 0.725293 - 0.697866*exp(-0.64*(0.0625*x_1 - 1)**2))**2)`
- icbr_no_replay formula (display, rounded):
  - `1.40906*sqrt(-(0.0890044*Abs(2.85*x_1 - 4.25) + 0.284912)*(-0.0672524*Abs(3.65*x_1 - 4.7) - 0.229592) - 0.0200001) + 29.3451*sqrt(0.0230799*asin(0.4*x_1 - 1.4) + 0.179118*asin(0.0499997*x_3 - 0.5) + 1) - 0.541163*tanh(22.493*asin(0.0499997*x_3 - 0.5) + 16.9688 - 15.8074*exp(-0.64*(0.0625*x_1 - 1)**2)) - 0.291445*Abs(-0.171378*Abs(2.85*x_1 - 3.3) + 13.2942*atanh(0.0499997*x_3 - 0.4) + 2.80268) - 0.688141*atan(-0.687121*asin(0.4*x_1 - 1.4) + 3.91733*asin(0.0499997*x_3 - 0.5) + 1.06908) - 6.75262*atanh(0.0136293*sin(1.75*x_2 + 0.2) - 0.0637404*asin(0.45*x_1 - 1.45) - 0.415159*asin(0.0499997*x_3 - 0.5) + 0.119373) - 24.106`
- icbr_no_shared formula (display, rounded):
  - `29.3451*sqrt(0.0230799*asin(0.4*x_1 - 1.4) + 0.179118*asin(0.0499997*x_3 - 0.5) + 1) - 0.291445*Abs(1.45412*sin(0.35*x_1 - 1.1) + 13.2014*acos(0.0499997*x_3 - 0.5) - 23.8952) - 0.688141*atan(-0.687121*asin(0.4*x_1 - 1.4) + 3.94487*atanh(0.0499997*x_3 - 0.4) + 0.67578) - 0.974918*atanh(0.75*(0.531358*sin(0.5*x_1 + 1.5) - 0.718291)*(0.107877*Abs(2.35*x_1 - 3.5) + 0.28481) + 0.9) - 6.75262*atanh(0.0136293*sin(1.75*x_2 + 0.2) + 0.0637404*acos(0.45*x_1 - 1.45) + 0.415159*acos(0.0499997*x_3 - 0.5) - 0.63288) - 23.1108 + 1.10855*exp(-132.245*(atanh(0.0499997*x_3 - 0.4) + 0.725293 - 0.697866*exp(-0.64*(0.0625*x_1 - 1)**2))**2)`
- icbr_refit_commit formula (display, rounded):
  - `48.1356*sqrt(0.0102504*asin(0.41636*x_1 - 1.41644) + 0.64935*atanh(0.00416*x_3 - 0.62496) + 1) - 0.324781*Abs(1.27549*sin(0.34*x_1 + 2.1005) + 7.6683*asin(0.0739999*x_3 - 0.60024) + 1.7243) - 0.759994*atan(-0.583868*asin(0.41628*x_1 - 1.4164) + 26.8932*atanh(0.00408*x_3 - 0.64008) + 19.6193) - 0.971995*atanh(0.75356*(-0.530792*cos(0.5006*x_1 - 3.2134) - 0.717848)*(0.0763669*Abs(3.1474*x_1 - 4.2658) + 0.281193) + 0.90024) + 13.5*atanh(0.00617892*sin(1.7012*x_2 + 3.40796) + 0.03501*acos(1.27152 - 0.38072*x_1) + 1.43419*atanh(0.00416*x_3 - 0.62804) + 0.55331) - 25.7608 + 1.10844*exp(-8113.68*(atanh(0.00416*x_3 - 0.62344) + 0.748881 - 0.0572528*exp(-0.810144*(1 - 0.0866589*x_1)**2))**2)`

### task=feynman_I_10_7 seed=6

- Task source: feynman_file
- Target formula: `m_0/sqrt(1-v**2/c**2)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.170843e-02, r2=0.991804
- Variant formula overview:
  - icbr_full: symbolic_s=2.593963e+00, imitation_mse=5.567632e-03, target_mse=1.290675e-02, formula_export_success=True
  - icbr_no_replay: symbolic_s=1.734883e+00, imitation_mse=6.347841e-03, target_mse=1.376156e-02, formula_export_success=True
  - icbr_no_shared: symbolic_s=3.834011e+00, imitation_mse=5.570253e-03, target_mse=1.291595e-02, formula_export_success=True
  - icbr_refit_commit: symbolic_s=4.907115e+00, imitation_mse=7.630490e-03, target_mse=1.371557e-02, formula_export_success=True
- icbr_full formula (display, rounded):
  - `-13.2683*(0.229325*acos(0.3*x_1 - 1.05) - atanh(0.0499997*x_3 - 0.4) - 0.440743)**2 + 0.283721*(-0.00975062*Abs(3.0*x_1 - 4.925) - 11.8842*acos(0.0499997*x_3 - 0.5) + 25.2945 - 0.265911*exp(-13.69*(1 - 0.743243*x_2)**2))*(0.153795*Abs(3.35*x_2 - 4.45) + 13.4906*asin(0.0499997*x_3 - 0.5) - 0.0165093*sign(4.0 - 3.45*x_1) + 7.21932) + 0.415412*tanh(0.109274*Abs(1.85*x_1 - 2.85) + 16.6896*acos(0.0499997*x_3 - 0.5) - 30.3033) - 10.2202*asin(0.0499997*(-0.431634*acos(0.35*x_1 - 1.2) - 12.5939*acos(0.0499997*x_3 - 0.5) + 27.2703)*(-0.141359*Abs(3.3*x_1 - 3.8) - 7.7916*acos(0.0499997*x_3 - 0.5) + 16.4499 - 0.253405*exp(-17.2225*(1 - 0.73494*x_2)**2)) - 0.65) - 5.28198 + 0.850927*exp(-1002.71*(1 - 0.512979*acos(0.0499997*x_3 - 0.5))**2)`
- icbr_no_replay formula (display, rounded):
  - `-13.0816*(-0.230956*asin(0.3*x_1 - 1.05) - asin(0.0499997*x_3 - 0.5) - 0.181474)**2 + 0.283721*(-0.00975062*Abs(3.0*x_1 - 4.925) + 0.161962*Abs(2.85*x_2 - 3.8) + 11.8842*asin(0.0499997*x_3 - 0.5) + 6.34391)*(0.153795*Abs(3.35*x_2 - 4.45) + 13.4906*asin(0.0499997*x_3 - 0.5) + 7.23615 - 0.0439283*exp(-25.0*(0.965 - x_1)**2)) - 0.418847*tanh(28.3553*asin(0.0499997*x_3 - 0.5) + 9.2266) - 0.415412*tanh(-0.109274*Abs(1.85*x_1 - 2.85) + 16.6896*asin(0.0499997*x_3 - 0.5) + 4.08746) + 10.2202*acos(0.0499997*(0.431634*asin(0.35*x_1 - 1.2) + 12.5939*asin(0.0499997*x_3 - 0.5) + 6.80983)*(-0.141359*Abs(3.3*x_1 - 3.8) + 7.7916*asin(0.0499997*x_3 - 0.5) + 4.21089 - 0.253405*exp(-17.2225*(1 - 0.73494*x_2)**2)) - 0.65) - 20.917`
- icbr_no_shared formula (display, rounded):
  - `-13.2683*(0.229325*acos(0.3*x_1 - 1.05) - atanh(0.0499997*x_3 - 0.4) - 0.440743)**2 + 0.283721*(-0.00975062*Abs(3.0*x_1 - 4.925) - 11.8842*acos(0.0499997*x_3 - 0.5) + 25.2945 - 0.265911*exp(-13.69*(1 - 0.743243*x_2)**2))*(0.153795*Abs(3.35*x_2 - 4.45) + 13.4906*asin(0.0499997*x_3 - 0.5) - 0.0165093*sign(4.0 - 3.45*x_1) + 7.21932) - 0.415412*tanh(-0.109274*Abs(1.85*x_1 - 2.85) + 16.6896*asin(0.0499997*x_3 - 0.5) + 4.08746) - 10.2202*asin(0.0499997*(-0.431634*acos(0.35*x_1 - 1.2) - 12.5939*acos(0.0499997*x_3 - 0.5) + 27.2703)*(-0.129599*Abs(3.6*x_1 - 4.15) - 7.7916*acos(0.0499997*x_3 - 0.5) + 16.4495 - 0.253405*exp(-17.2225*(1 - 0.73494*x_2)**2)) - 0.65) - 5.28198 + 0.850927*exp(-1002.71*(1 - 0.512979*acos(0.0499997*x_3 - 0.5))**2)`
- icbr_refit_commit formula (display, rounded):
  - `-13.9976*(-acos(0.78088 - 0.0557999*x_1) - 0.625408*asin(0.0779999*x_3 - 0.60002) + 0.879624)**2 + 0.283585*(-0.011956*Abs(2.42108*x_1 - 4.03712) + 90.2202*atanh(0.0042*x_3 - 0.639) + 68.7717 - 0.291575*exp(-10.24*(1 - 0.740625*x_2)**2))*(0.147264*Abs(3.55552*x_2 - 4.77572) + 109.402*atanh(0.00388*x_3 - 0.64364) - 0.0141815*sign(4.8989 - 4.192*x_1) + 83.8838) - 0.432299*tanh(-0.259506*sin(0.84*x_1 + 3.5) + 9.35459*asin(0.0784399*x_3 - 0.60384) + 1.61147) + 127.966*acos(0.002*(8.12765*acos(0.60122 - 0.0779999*x_3) - 0.39156*acos(0.3814*x_1 - 1.2738) - 6.80646)*(1.42659*cos(0.34*x_1 + 0.50032) + 0.155939*Abs(3.0672*x_2 - 4.19164) + 5.02836*acos(0.60134 - 0.0779999*x_3) - 5.78112) - 0.9) - 342.44 + 6.03663*exp(-3581.97*(atanh(0.00404*x_3 - 0.64644) + 0.772246)**2)`

### task=feynman_I_10_7 seed=7

- Task source: feynman_file
- Target formula: `m_0/sqrt(1-v**2/c**2)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=7.841146e-03, r2=0.994580
- Variant formula overview:
  - icbr_full: symbolic_s=3.084140e+00, imitation_mse=3.686062e-03, target_mse=6.871138e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=2.043592e+00, imitation_mse=3.739056e-03, target_mse=6.854551e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=4.489735e+00, imitation_mse=3.686063e-03, target_mse=6.871141e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=5.589179e+00, imitation_mse=3.986723e-03, target_mse=6.932694e-03, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0.207488*(-3.72271*asin(0.3*x_1 - 1.05) - 3.84725*asin(0.0499997*x_3 - 0.5) - 5.58348)*(-0.13182*Abs(3.1*x_2 - 4.0) + 3.78973*acos(0.0499997*x_3 - 0.5) - 0.429922*asin(0.4*x_1 - 1.35) - 8.79574) + 0.452976*cos(-0.0643867*tan(0.45*x_1 - 5.0) + 10.0174*tan(0.05*x_3 - 3.55) + 7.70558) - 0.352531*tanh(82.9242*(1 - 0.653061*x_2)**4 + 13.1586*tan(0.05*x_3 - 3.55) - 1.61432*atanh(0.4*x_1 - 1.35) + 2.10043) - 0.030266*atan(5.86545*tan(0.05*x_3 - 3.55) + 0.889813) + 0.5799 + 1.4625*exp(-147.465*(tan(0.05*x_3 - 3.55) - 0.00927684*Abs(3.3*x_1 - 4.8) + 0.382236)**2) + 0.75216*exp(-4.84*((1.62837*cos(0.3*x_1 - 2.5) - 0.135696*asin(0.8*x_2 - 1.5) - 4.5164*asin(0.0499997*x_3 - 0.5) - 1.13552)*(0.229336*tan(0.05*x_3 - 3.55) - 0.256706*atanh(0.2*x_1 - 1.2) + 0.256165 - 0.227899*exp(-24.7506*(1 - 0.713568*x_2)**2)) - 0.25)**2)`
- icbr_no_replay formula (display, rounded):
  - `0.207488*(-3.86936*tan(0.05*x_3 - 3.55) - 3.72271*asin(0.3*x_1 - 1.05) - 5.22989)*(-3.81151*tan(0.05*x_3 - 3.55) - 0.13182*Abs(3.1*x_2 - 4.0) - 0.429922*asin(0.4*x_1 - 1.35) - 2.49455) + 0.452976*cos(-0.0643867*tan(0.45*x_1 - 5.0) + 10.0174*tan(0.05*x_3 - 3.55) + 7.70558) - 0.352531*tanh(82.9242*(1 - 0.653061*x_2)**4 + 13.1586*tan(0.05*x_3 - 3.55) - 1.61432*atanh(0.4*x_1 - 1.35) + 2.10043) + 0.547785 + 1.4625*exp(-147.465*(tan(0.05*x_3 - 3.55) - 0.00927684*Abs(3.3*x_1 - 4.8) + 0.382236)**2) + 0.0526655*exp(-15.2905*(tan(0.05*x_3 - 3.55) + 0.330718)**2) + 0.75216*exp(-4.84*((-0.108085*tan(1.0*x_2 + 1.5) - 4.54235*tan(0.05*x_3 - 3.55) - 4.15689 + 5.58064*exp(-(0.1*x_1 - 1.0)**2))*(-0.114085*acos(0.0999997*x_3 - 0.75) - 0.256706*atanh(0.2*x_1 - 1.2) + 0.427674 - 0.227899*exp(-24.7506*(1 - 0.713568*x_2)**2)) - 0.25)**2)`
- icbr_no_shared formula (display, rounded):
  - `0.207488*(-3.72271*asin(0.3*x_1 - 1.05) - 3.84725*asin(0.0499997*x_3 - 0.5) - 5.58348)*(-0.13182*Abs(3.1*x_2 - 4.0) + 3.78973*acos(0.0499997*x_3 - 0.5) - 0.429922*asin(0.4*x_1 - 1.35) - 8.79574) + 0.452976*cos(-0.0643867*tan(0.45*x_1 - 5.0) + 10.0174*tan(0.05*x_3 - 3.55) + 7.70558) - 0.352531*tanh(82.9242*(1 - 0.653061*x_2)**4 + 13.1586*tan(0.05*x_3 - 3.55) - 1.61432*atanh(0.4*x_1 - 1.35) + 2.10043) - 0.030266*atan(5.86545*tan(0.05*x_3 - 3.55) + 0.889813) + 0.5799 + 1.4625*exp(-147.465*(tan(0.05*x_3 - 3.55) - 0.00927684*Abs(3.3*x_1 - 4.8) + 0.382236)**2) + 0.75216*exp(-4.84*((1.62837*cos(0.3*x_1 - 2.5) + 0.135696*acos(0.8*x_2 - 1.5) - 4.5164*asin(0.0499997*x_3 - 0.5) - 1.34867)*(0.229336*tan(0.05*x_3 - 3.55) - 0.256706*atanh(0.2*x_1 - 1.2) + 0.256165 - 0.227899*exp(-24.7506*(1 - 0.713568*x_2)**2)) - 0.25)**2)`
- icbr_refit_commit formula (display, rounded):
  - `0.207492*(-2.99639*asin(0.36468*x_1 - 1.21712) - 12.0458*asin(0.014*x_3 - 0.60016) - 11.1553)*(-0.149718*Abs(2.71316*x_2 - 3.5172) - 11.867*acos(0.6 - 0.014*x_3) - 0.57866*atanh(0.30044*x_1 - 1.00132) + 10.1339) + 0.449833*cos(-0.060498*tan(0.55288*x_1 - 1.96624) + 47.0598*tan(0.00771999*x_3 - 0.60684) + 29.9117) - 0.355938*tanh(73.1723*(1 - 0.660222*x_2)**4 + 59.352*tan(0.00755999*x_3 - 0.60528) - 2.09059*atanh(0.27384*x_1 - 1.17824) + 37.2324) - 0.0290639*atan(31.6752*tan(0.00623999*x_3 - 0.68872) + 24.3767) + 0.577175 + 1.36327*exp(-4141.63*(tan(0.00615999*x_3 - 0.6964) - 0.00169297*Abs(3.34568*x_1 - 4.32912) + 0.827415)**2) + 0.764434*exp(-4.41*(-(1.4583*cos(0.338*x_1 + 3.70034) - 0.134089*asin(0.81004*x_2 - 1.51188) - 14.1362*asin(0.014*x_3 - 0.60064) - 7.94736)*(0.137438*asin(0.0833999*x_3 - 0.63708) - 0.294378*atanh(0.0679999*x_1 - 1.06668) + 0.130898 - 0.29926*exp(-11.2888*(1 - 0.698084*x_2)**2)) + 0.269524)**2)`

### task=feynman_I_10_7 seed=8

- Task source: feynman_file
- Target formula: `m_0/sqrt(1-v**2/c**2)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=4.293375e-03, r2=0.996983
- Variant formula overview:
  - icbr_full: symbolic_s=3.515893e+00, imitation_mse=8.862158e-03, target_mse=1.263677e-02, formula_export_success=True
  - icbr_no_replay: symbolic_s=2.218053e+00, imitation_mse=9.267394e-03, target_mse=1.305322e-02, formula_export_success=True
  - icbr_no_shared: symbolic_s=5.040005e+00, imitation_mse=8.862819e-03, target_mse=1.263793e-02, formula_export_success=True
  - icbr_refit_commit: symbolic_s=6.495455e+00, imitation_mse=nan, target_mse=nan, formula_export_success=True
- icbr_full formula (display, rounded):
  - `-5.71453*(-0.0615286*Abs(3.85*x_1 - 4.825) + atanh(0.0499997*x_3 - 0.4) + 0.602806)**4 + 11.8729*sqrt(-0.0382202*acos(0.4*x_1 - 1.4) - 0.208194*acos(0.0499997*x_3 - 0.5) + 1) + 9.94468*sin(0.05*(-0.136093*cos(1.0*x_1 + 4.55) - 0.327768*cos(3.15*x_2 - 3.7) - 5.797*acos(0.0499997*x_3 - 0.5) + 13.5155)*(0.243258*Abs(3.8*x_1 - 4.9) + 0.045882*Abs(3.05*x_2 - 4.15) + 5.03794*acos(0.0499997*x_3 - 0.5) - 9.44957) + 4.95) + 0.0645806*cos(13.1957*atanh(0.0499997*x_3 - 0.4) + 2.10807) - 0.384475*atan(40.9401*atanh(0.0499997*x_3 - 0.4) + 15.6085 - 8.2263*exp(-(0.1*x_1 - 1.0)**2)) + 4.84686*atanh(0.00333572*Abs(3.95*x_2 - 4.975) - 0.618432*acos(0.0499997*x_3 - 0.5) + 0.0453086*atanh(0.4*x_1 - 1.35) + 0.908559) + 4.4339 + 0.906843*exp(-1.8*(-1.46987*cos(0.3*x_1 - 2.5) + 7.74936*atanh(0.0499997*x_3 - 0.4) + 1.91387)*(-0.432243*sin(0.35*x_1 - 1.1) + 2.86567*atanh(0.0499997*x_3 - 0.4) + 1.11664 - 0.148262*exp(-12.25*(1 - 0.757143*x_2)**2)))`
- icbr_no_replay formula (display, rounded):
  - `-5.55446*(-0.0619671*Abs(3.85*x_1 - 4.825) + asin(0.0499997*x_3 - 0.5) + 0.707482)**4 - 2.56131*(-0.0751938*asin(0.4*x_1 - 1.4) - 0.409598*asin(0.0499997*x_3 - 0.5) + 1)**(3/2) + 3.17418*cos(0.1*(-0.327768*cos(3.15*x_2 - 3.7) + 0.0362481*Abs(2.85*x_1 - 4.8) - 5.797*acos(0.0499997*x_3 - 0.5) + 13.3487)*(0.243258*Abs(3.8*x_1 - 4.9) - 5.03794*asin(0.0499997*x_3 - 0.5) - 1.45393 - 0.0770867*exp(-15.21*(1 - 0.730769*x_2)**2)) + 3.5) - 6.54277*tanh(0.95*(-0.0969627*Abs(4.4*x_1 - 4.825) + 7.69452*asin(0.0499997*x_3 - 0.5) + 3.53965)*(-0.047654*Abs(3.05*x_1 - 3.55) + 0.0683166*Abs(3.6*x_2 - 4.7) + 2.84539*asin(0.0499997*x_3 - 0.5) + 1.53205) + 1.3) - 0.0305753*Abs(19.6535*asin(0.0499997*x_3 - 0.5) + 5.33492) - 2.46325*acos(0.00667146*Abs(3.95*x_2 - 4.975) + 1.23687*asin(0.0499997*x_3 - 0.5) + 0.0906174*atanh(0.4*x_1 - 1.35) + 0.0742613) - 0.384475*atan(-0.156698*Abs(4.45*x_1 - 4.925) + 40.6504*asin(0.0499997*x_3 - 0.5) + 15.9732) + 19.5878`
- icbr_no_shared formula (display, rounded):
  - `-5.71453*(-0.0615286*Abs(3.85*x_1 - 4.825) + atanh(0.0499997*x_3 - 0.4) + 0.602806)**4 + 11.9112*sqrt(-0.0381318*acos(0.4*x_1 - 1.4) - 0.207713*acos(0.0499997*x_3 - 0.5) + 1) + 9.94468*sin(0.05*(-0.136093*cos(1.0*x_1 + 4.55) - 0.327768*cos(3.15*x_2 - 3.7) + 5.797*asin(0.0499997*x_3 - 0.5) + 4.40956)*(0.243258*Abs(3.8*x_1 - 4.9) + 0.045882*Abs(3.05*x_2 - 4.15) + 5.03794*acos(0.0499997*x_3 - 0.5) - 9.44957) + 4.95) + 0.0645806*cos(13.1957*atanh(0.0499997*x_3 - 0.4) + 2.10807) - 0.384475*atan(40.9401*atanh(0.0499997*x_3 - 0.4) + 15.6085 - 8.2263*exp(-(0.1*x_1 - 1.0)**2)) + 4.84686*atanh(0.00333572*Abs(3.95*x_2 - 4.975) - 0.618432*acos(0.0499997*x_3 - 0.5) + 0.0453086*atanh(0.4*x_1 - 1.35) + 0.908559) + 4.39718 + 0.906842*exp(-1.8*(-1.46987*cos(0.3*x_1 - 2.5) + 7.74936*atanh(0.0499997*x_3 - 0.4) + 1.91387)*(-0.432243*sin(0.35*x_1 - 1.1) + 2.86567*atanh(0.0499997*x_3 - 0.4) + 1.11664 - 0.148262*exp(-12.25*(1 - 0.757143*x_2)**2)))`
- icbr_refit_commit formula (display, rounded):
  - `-1341.11*(-0.027242*Abs(1.935*x_1 - 2.24168) + atanh(0.00799999*x_3 - 0.60004) + 0.754928)**4 + 10.2286*sqrt(acos(0.6246 - 0.01204*x_3) + 0.0504797*acos(1.41196 - 0.41108*x_1) - 0.287623) - 5.88334*sin(0.0659999*(-0.392799*cos(2.5004*x_2 + 3.49552) + 0.0391509*Abs(2.631*x_1 - 4.555) + 3.74139*asin(0.0779999*x_3 - 0.60064) + 3.6388)*(0.302294*Abs(3.00452*x_1 - 3.60776) - 3.25153*acos(0.60052 - 0.0779999*x_3) + 4.20446 - 0.0852249*exp(-11.0822*(1 - 0.727774*x_2)**2)) - 4.4) - 0.0645872*cos(101.306*atanh(0.0042*x_3 - 0.62944) + 74.8171) - 0.371746*atan(287.864*atanh(0.00408*x_3 - 0.64036) + 219.812 - 11.953*exp(-0.810144*(1 - 0.0688827*x_1)**2)) - 3.60762*atanh(0.00583283*sin(3.80144*x_2 - 3.2018) - 2.84324*acos(0.61064 - 0.0128*x_3) + 0.086673*acos(0.29972*x_1 - 1.29972) + 2.83829) - 0.10731 + 77.676*exp(-4.45936*(-0.193075*(-1.47586*cos(0.29868*x_1 - 2.4952) + 59.4544*atanh(0.00408*x_3 - 0.644) + 44.1948)*(0.448522*sin(0.336*x_1 - 4.19946) - 0.0688429*cos(4.89924*x_2 - 0.2074) + 21.0678*atanh(0.0042*x_3 - 0.65152) + 16.2445) - 1)**2)`

### task=feynman_I_10_7 seed=9

- Task source: feynman_file
- Target formula: `m_0/sqrt(1-v**2/c**2)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=2.179883e-03, r2=0.998635
- Variant formula overview:
  - icbr_full: symbolic_s=3.123830e+00, imitation_mse=8.051416e-04, target_mse=2.265056e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=1.961768e+00, imitation_mse=1.411834e-03, target_mse=2.747877e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=4.546105e+00, imitation_mse=8.051415e-04, target_mse=2.265056e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=5.527673e+00, imitation_mse=7.998159e-04, target_mse=2.186103e-03, formula_export_success=True
- icbr_full formula (display, rounded):
  - `-0.309828*tan(1.6*(0.688859 - 0.313615*exp(-4.0*(1 - 0.825*x_2)**2))*(0.826284*cos(0.4*x_1 + 0.3) - 0.192248*cos(2.0*x_2 - 4.975) + 1.92949*atanh(0.0499997*x_3 - 0.4) - 0.609769) - 2.5) + 0.413995*tan(2.0*(0.30251*cos(0.45*x_1 + 0.15) + 1.65914*asin(0.0499997*x_3 - 0.5) + 0.473422)*(-0.948618*asin(0.0499997*x_3 - 0.5) - 0.199969*atan(1.15*x_2 - 2.05) - 0.793976) - 2.95) + 0.0876581*Abs(4.17912*sqrt(0.13924*x_1 + 1) + 1.30558*sin(0.55*x_2 + 2.4) + 14.0411*atanh(0.0499997*x_3 - 0.4) - 2.83401) - 9.87939*acos(0.012076*cos(4.7*x_2 + 3.25) + 0.0893986*asin(0.35*x_1 - 1.2) + 0.323458*atanh(0.0499997*x_3 - 0.4) - 0.315904) - 1.62265*atan(-0.495249*cos(0.55*x_1 + 2.9) + 2.7029*asin(0.0499997*x_3 - 0.5) + 1.17766) + 24.0467 - 1.51063*exp(-1.93057*(-0.336844*acos(0.45*x_1 - 1.45) - 0.421248*atanh(0.0499997*x_3 - 0.4) + 1 + 0.156844*exp(-15.21*(1 - 0.74359*x_2)**2))**2)`
- icbr_no_replay formula (display, rounded):
  - `-0.309828*tan(1.6*(0.0939571*Abs(4.0*x_2 - 4.925) + 0.347089)*(-0.110273*Abs(2.85*x_1 - 3.45) - 1.9159*acos(0.0499997*x_3 - 0.5) + 2.98196 + 0.411218*exp(-1.21*(1.0 - x_2)**2)) - 2.5) + 0.413995*tan(2.0*(-0.032382*Abs(3.95*x_1 - 4.9) + 1.65914*asin(0.0499997*x_3 - 0.5) + 0.71876)*(-0.948618*asin(0.0499997*x_3 - 0.5) - 0.199969*atan(1.15*x_2 - 2.05) - 0.793976) - 2.95) + 0.0876581*Abs(0.780109*asin(0.3*x_1 - 1.0) + 13.9421*asin(0.0499997*x_3 - 0.5) + 2.30685 + 2.10844*exp(-0.16*(x_2 + 0.374999)**2)) - 1.62265*atan(-0.0937055*Abs(2.65*x_1 - 3.55) + 2.7029*asin(0.0499997*x_3 - 0.5) + 1.66155) + 10.1127*atanh(0.013277*Abs(3.2*x_2 - 4.15) - 0.0893986*acos(0.35*x_1 - 1.2) + 0.321178*asin(0.0499997*x_3 - 0.5) - 0.00790152) + 7.04606 - 1.51063*exp(-0.337768*(acos(0.0499997*x_3 - 0.5) + 0.805309*asin(0.45*x_1 - 1.45) - 0.545406 + 0.374974*exp(-15.21*(1 - 0.74359*x_2)**2))**2)`
- icbr_no_shared formula (display, rounded):
  - `-0.309828*tan(1.6*(0.688859 - 0.313615*exp(-4.0*(1 - 0.825*x_2)**2))*(0.826284*cos(0.4*x_1 + 0.3) - 0.192248*cos(2.0*x_2 - 4.975) + 1.92949*atanh(0.0499997*x_3 - 0.4) - 0.609769) - 2.5) + 0.413995*tan(2.0*(0.30251*cos(0.45*x_1 + 0.15) + 1.65914*asin(0.0499997*x_3 - 0.5) + 0.473422)*(-0.948618*asin(0.0499997*x_3 - 0.5) - 0.199969*atan(1.15*x_2 - 2.05) - 0.793976) - 2.95) + 0.0876581*Abs(4.17912*sqrt(0.13924*x_1 + 1) + 1.30558*sin(0.55*x_2 + 2.4) + 14.0411*atanh(0.0499997*x_3 - 0.4) - 2.83401) - 9.87939*acos(0.012076*cos(4.7*x_2 + 3.25) + 0.0893986*asin(0.35*x_1 - 1.2) + 0.323458*atanh(0.0499997*x_3 - 0.4) - 0.315904) - 1.62265*atan(-0.495249*cos(0.55*x_1 + 2.9) + 2.7029*asin(0.0499997*x_3 - 0.5) + 1.17766) + 24.0467 - 1.51063*exp(-1.93057*(-0.336844*acos(0.45*x_1 - 1.45) - 0.421248*atanh(0.0499997*x_3 - 0.4) + 1 + 0.156844*exp(-15.21*(1 - 0.74359*x_2)**2))**2)`
- icbr_refit_commit formula (display, rounded):
  - `-0.427908*tan(1.2318*(0.700838 - 0.324879*exp(-3.61*(1 - 0.829474*x_2)**2))*(0.821716*cos(0.40252*x_1 + 0.2932) - 0.192612*cos(1.99572*x_2 + 1.31424) + 1.23656*asin(0.0779999*x_3 - 0.6) - 0.638909) + 0.52352) + 0.502432*tan(1.6638*(-0.33418*cos(0.40184*x_1 + 3.4078) + 1.06817*asin(0.0781999*x_3 - 0.6002) + 0.268587)*(-0.612203*asin(0.0779999*x_3 - 0.60084) - 0.21978*atan(1.04528*x_2 - 1.903) - 0.69299) + 0.0947599) + 0.0881987*Abs(4.08868*sqrt(0.13874*x_1 + 1) + 102.513*atanh(0.00416*x_3 - 0.64712) + 68.9133 + 2.68875*exp(-0.092416*(x_2 + 0.964605)**2)) - 10.4402*acos(-0.0113427*cos(4.69936*x_2 + 0.10924) + 0.075991*asin(0.3824*x_1 - 1.276) + 1.87635*atanh(0.00555999*x_3 - 0.60284) + 0.843724) - 2.08381*atan(0.44134*cos(0.536*x_1 - 0.2) + 1.51835*asin(0.0782799*x_3 - 0.60204) + 0.978046) + 25.8583 - 1.52926*exp(-0.246971*(-0.749831*acos(0.60056 - 0.0771199*x_3) + acos(1.3946 - 0.42276*x_1) + 0.906728 + 0.484331*exp(-10.24*(1 - 0.740625*x_2)**2))**2)`

### task=feynman_I_10_7 seed=10

- Task source: feynman_file
- Target formula: `m_0/sqrt(1-v**2/c**2)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=5.516047e-03, r2=0.996187
- Variant formula overview:
  - icbr_full: symbolic_s=2.832239e+00, imitation_mse=6.163856e-03, target_mse=9.195032e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=1.835882e+00, imitation_mse=7.901560e-03, target_mse=1.083836e-02, formula_export_success=True
  - icbr_no_shared: symbolic_s=4.054782e+00, imitation_mse=6.162418e-03, target_mse=9.194367e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=5.017873e+00, imitation_mse=5.106436e-03, target_mse=9.371921e-03, formula_export_success=True
- icbr_full formula (display, rounded):
  - `36.921*(-0.127724*cos(0.35*x_1 + 0.5) - atanh(0.0499997*x_3 - 0.4) - 0.0248107)**3 - 1.83538*(0.818619*sin(0.35*x_1 - 1.1) - atanh(0.0499997*x_3 - 0.4) - 0.283026 - 0.047449*exp(-5.0625*(1 - 0.8*x_2)**2))**2 - 4.33404*sin(0.1*(-0.210916*Abs(3.15*x_1 - 4.65) + 5.32502*atanh(0.0500002*x_3 - 0.4) + 1.38193)*(1.00187*sin(0.55*x_1 - 5.0) - 7.53681*atanh(0.0499997*x_3 - 0.4) - 4.64967 + 0.485361*exp(-25.0*(0.995 - x_2)**2)) - 4.35) - 4.11288*asin(1.29748*(1 - 0.032967*x_1)**(3/2) + 1.1955*acos(0.0499997*x_3 - 0.5) - 3.04898) + 8.53716 - 0.744168*exp(-3.2653*(0.0252938*Abs(2.85*x_1 - 4.8) + atanh(0.0499997*x_3 - 0.4) - 0.201526)**2) - 0.445145*exp(-20.25*(-(0.0953008*Abs(2.7*x_1 - 4.25) + 0.307692)*(-7.76662*(1 - 0.040201*x_1)**(3/2) - 2.71323*asin(0.0499997*x_3 - 0.5) + 6.20654) - 0.288889)**2)`
- icbr_no_replay formula (display, rounded):
  - `36.921*(0.00972206*Abs(4.4*x_1 - 4.9) - atanh(0.0499997*x_3 - 0.4) - 0.108089)**3 - 1.83538*(0.11062*Abs(2.5*x_1 - 3.05) + 0.015812*Abs(3.9*x_2 - 4.925) - atanh(0.0499997*x_3 - 0.4) - 0.867822)**2 + 0.266106*sin(0.110233*Abs(2.85*x_1 - 4.8) + 4.35809*atanh(0.0499997*x_3 - 0.4) - 2.41356) + 0.254272*tanh(5.0*(0.0953008*Abs(2.7*x_1 - 4.25) + 0.307692)*(18.2962*sqrt(0.0515464*x_1 + 1) - 2.71323*asin(0.0499997*x_3 - 0.5) - 19.8585) + 0.6) + 1.20696*tanh(0.3*(-0.210916*Abs(3.15*x_1 - 4.65) + 5.32502*atanh(0.0500002*x_3 - 0.4) + 1.38193)*(-0.187817*Abs(2.75*x_1 - 4.1) - 7.53681*atanh(0.0499997*x_3 - 0.4) - 3.67438 + 0.485361*exp(-25.0*(0.995 - x_2)**2)) - 1.2) + 4.11288*asin(-1.29748*(1 - 0.032967*x_1)**(3/2) + 1.2041*atanh(0.0499997*x_3 - 0.4) + 1.05109) + 4.74241`
- icbr_no_shared formula (display, rounded):
  - `36.921*(-0.127724*cos(0.35*x_1 + 0.5) - atanh(0.0499997*x_3 - 0.4) - 0.0248107)**3 - 1.83538*(0.818619*sin(0.35*x_1 - 1.1) - atanh(0.0499997*x_3 - 0.4) - 0.283026 - 0.047449*exp(-5.0625*(1 - 0.8*x_2)**2))**2 - 4.33404*sin(0.1*(-0.210916*Abs(3.15*x_1 - 4.65) + 5.32502*atanh(0.0500002*x_3 - 0.4) + 1.38193)*(1.00187*sin(0.55*x_1 - 5.0) - 7.53681*atanh(0.0499997*x_3 - 0.4) - 4.64967 + 0.485361*exp(-25.0*(0.995 - x_2)**2)) - 4.35) - 4.11288*asin(1.29748*(1 - 0.032967*x_1)**(3/2) + 1.1955*acos(0.0499997*x_3 - 0.5) - 3.04898) + 8.53716 - 0.744168*exp(-3.2653*(0.0261913*Abs(2.75*x_1 - 4.625) + atanh(0.0499997*x_3 - 0.4) - 0.201555)**2) - 0.445145*exp(-20.25*(-(0.0953008*Abs(2.7*x_1 - 4.25) + 0.307692)*(-7.76662*(1 - 0.040201*x_1)**(3/2) - 2.71323*asin(0.0499997*x_3 - 0.5) + 6.20654) - 0.288889)**2)`
- icbr_refit_commit formula (display, rounded):
  - `1119.23*(0.0385031*cos(0.3364*x_1 - 2.59968) - 0.956186*acos(0.60684 - 0.01312*x_3) + 1)**3 + 0.274216*cos(0.117499*Abs(2.59028*x_1 - 4.57892) + 22.8862*atanh(0.00627999*x_3 - 0.607) + 16.6869) + 3.40049*cos(0.892577*cos(0.34048*x_1 + 0.50008) + 4.70231*atanh(0.00799999*x_3 - 0.6) + 3.11614 + 0.0534793*exp(-4.41*(1 - 0.801905*x_2)**2)) + 1.50518*tanh(0.23088*(-0.203819*Abs(3.1642*x_1 - 4.38584) + 30.7573*atanh(0.00599999*x_3 - 0.60002) + 20.5093)*(-0.184333*Abs(2.67036*x_1 - 3.49392) + 30.768*acos(0.00987999*x_3 - 0.66736) - 71.3277 + 1.50465*exp(-6.30371*(0.608511 - x_2)**2)) - 1.12096) - 5.68362*asin(0.914497*(1 - 0.0334219*x_1)**(3/2) + 2.9532*acos(0.0124*x_3 - 0.61944) - 6.86607) + 2.19126 + 0.470493*exp(-2.64674*(-(0.0952139*Abs(2.7094*x_1 - 4.41176) + 0.316617)*(18.0967*sqrt(0.0521555*x_1 + 1) - 1.73266*asin(0.0788399*x_3 - 0.60448) - 19.3414) + 0.537347)**2)`

### task=feynman_I_10_7 seed=11

- Task source: feynman_file
- Target formula: `m_0/sqrt(1-v**2/c**2)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=5.087778e-03, r2=0.996679
- Variant formula overview:
  - icbr_full: symbolic_s=1.780140e+00, imitation_mse=9.817193e-04, target_mse=4.817777e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=1.266399e+00, imitation_mse=1.113611e-03, target_mse=4.978377e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=2.554350e+00, imitation_mse=9.818914e-04, target_mse=4.817719e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=3.373611e+00, imitation_mse=1.703715e-03, target_mse=6.565762e-03, formula_export_success=True
- icbr_full formula (display, rounded):
  - `2.87407*sin(0.0603124*Abs(3.6*x_2 - 4.5) - 1.08649*acos(0.3*x_1 - 1.05) - 0.863866*atanh(0.0499997*x_3 - 0.4) + 1.63423) - 2.44003*acos(0.0499997*(4.55477*log(0.15*x_1 + 4.5) - 0.0872673*Abs(2.6*x_2 - 3.15) - 5.06*acos(0.0499997*x_3 - 0.5) + 3.36455)*(0.347865*cos(0.3*x_1 - 2.5) + 0.133719*Abs(2.8*x_2 - 3.8) + 5.30627*atanh(0.0499997*x_3 - 0.4) + 2.71965) - 0.55) + 0.442417*atanh(0.9*(0.0661197*Abs(3.25*x_2 - 4.25) + 0.198753)*(0.496976*cos(0.7*x_1 - 3.9) - 10.4807*atanh(0.0499997*x_3 - 0.4) - 3.27997) + 1.0) + 7.86098`
- icbr_no_replay formula (display, rounded):
  - `2.86713*cos(0.0603124*Abs(3.6*x_2 - 4.5) + 0.857863*acos(0.0499997*x_3 - 0.5) + 1.08649*asin(0.3*x_1 - 1.05) - 3.05607) + 2.44003*asin(0.0499997*(4.15815*sqrt(0.0732984*x_1 + 1) - 0.0872673*Abs(2.6*x_2 - 3.15) - 5.06*acos(0.0499997*x_3 - 0.5) + 6.05675)*(5.2694*asin(0.0499997*x_3 - 0.5) + 2.7171 + 1.19263*exp(-(0.1*x_1 - 1.0)**2) - 0.200722*exp(-18.49*(1 - 0.732558*x_2)**2)) - 0.55) + 0.442417*atanh(0.9*(0.0661197*Abs(3.25*x_2 - 4.25) + 0.198753)*(0.112456*Abs(2.7*x_1 - 4.0) + 10.4079*acos(0.0499997*x_3 - 0.5) - 21.2318) + 1.0) + 3.97285`
- icbr_no_shared formula (display, rounded):
  - `2.87407*sin(0.0603124*Abs(3.6*x_2 - 4.5) - 1.08649*acos(0.3*x_1 - 1.05) - 0.863866*atanh(0.0499997*x_3 - 0.4) + 1.63423) + 2.44003*asin(0.0499997*(4.23756*sqrt(0.0717949*x_1 + 1) - 0.0872673*Abs(2.6*x_2 - 3.15) - 5.06*acos(0.0499997*x_3 - 0.5) + 5.97766)*(0.347865*cos(0.3*x_1 - 2.5) + 0.133719*Abs(2.8*x_2 - 3.8) + 5.30627*atanh(0.0499997*x_3 - 0.4) + 2.71965) - 0.55) + 0.442417*atanh(0.9*(0.0661197*Abs(3.25*x_2 - 4.25) + 0.198753)*(0.496976*cos(0.7*x_1 - 3.9) - 10.4807*atanh(0.0499997*x_3 - 0.4) - 3.27997) + 1.0) + 4.02818`
- icbr_refit_commit formula (display, rounded):
  - `2.42391*cos(0.0769872*Abs(3.3486*x_2 - 4.16076) + 7.37119*acos(0.79934 - 0.042*x_1) - 6.04913*atanh(0.00603999*x_3 - 0.60028) - 5.45923) + 1.85857*acos(-0.0669999*(0.100681*x_1 + 0.143631*Abs(2.65456*x_2 - 3.63888) + 3.39755*asin(0.0780399*x_3 - 0.60408) + 2.33853)*(4.1631*sqrt(0.0732029*x_1 + 1) - 0.0775627*Abs(2.87312*x_2 - 3.46944) + 16.2653*asin(0.0136*x_3 - 0.60144) + 5.97532) + 0.5492) + 0.613368*atanh(0.59962*(0.056384*Abs(3.8*x_2 - 4.99999) + 0.199597)*(-0.589644*sin(0.544*x_1 + 1.30016) - 79.2175*atanh(0.00432*x_3 - 0.6236) - 56.8296) + 0.918) + 0.581643`

### task=feynman_I_10_7 seed=12

- Task source: feynman_file
- Target formula: `m_0/sqrt(1-v**2/c**2)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=2.541073e-03, r2=0.998257
- Variant formula overview:
  - icbr_full: symbolic_s=3.362797e+00, imitation_mse=1.313240e-03, target_mse=2.954144e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=2.098541e+00, imitation_mse=1.315362e-03, target_mse=2.936352e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=4.933812e+00, imitation_mse=1.305111e-03, target_mse=2.932072e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=6.493615e+00, imitation_mse=2.768495e-03, target_mse=3.871694e-03, formula_export_success=True
- icbr_full formula (display, rounded):
  - `36.134*(0.804019*sqrt(0.0714286*x_1 + 1) + 0.110046*acos(0.0499997*x_3 - 0.5) - 1)**(3/2) + 13.2143*sqrt(log(0.15*x_1 + 4.8) + 0.192964*atanh(0.0499997*x_3 - 0.4) - 0.836743) + 0.0908697*tanh(15.0699*acos(0.0499997*x_3 - 0.5) - 27.2324) + 0.0339833*Abs(3.6*(81.3891*sqrt(0.0111111*x_1 + 1) + 4.15448*atanh(0.0499997*x_3 - 0.4) - 79.8963)*(5.82665*atanh(0.0499997*x_3 - 0.4) + 1.25468 + 0.581717*exp(-1.5625*(0.96*x_2 - 1)**2)) - 1.85) + 0.372664*acos(-0.104727*Abs(2.7*x_1 - 3.25) + 2.16422*asin(0.0499997*x_3 - 0.5) + 0.994162) - 0.726152*atanh(0.2*(0.213859*tanh(2.1*x_2 - 3.5) + 4.00617*acos(0.0499997*x_3 - 0.5) + 0.147998*atanh(0.4*x_1 - 1.35) - 7.55484)*(-0.0648565*Abs(3.1*x_1 - 4.05) - 8.47073*asin(0.0499997*x_3 - 0.5) - 5.16585 + 0.396836*exp(-1.5625*(1 - 0.96*x_2)**2)) - 0.8) + 6.71419*atanh(0.770787*sqrt(0.0918367*x_1 + 1) + 0.0096015*Abs(2.55*x_2 - 3.1) + 0.298096*atanh(0.0499997*x_3 - 0.4) - 1.09642) - 9.02859`
- icbr_no_replay formula (display, rounded):
  - `-12.649*(-0.5215*sqrt(0.07*x_1 + 1) - 0.111306*asin(0.0499997*x_3 - 0.5) + 1)**(3/2) + 27.1822*(0.972047*sqrt(0.0714286*x_1 + 1) - 0.133044*asin(0.0499997*x_3 - 0.5) - 1)**(3/2) - 0.0908697*tanh(15.0699*asin(0.0499997*x_3 - 0.5) + 3.56066) + 0.0339833*Abs(3.6*(4.12482*asin(0.0499997*x_3 - 0.5) + 0.0221286 + 5.27188*exp(-(0.1*x_1 - 1.0)**2))*(5.78505*asin(0.0499997*x_3 - 0.5) + 1.83534 + 0.581717*exp(-1.5625*(0.96*x_2 - 1)**2)) - 1.85) - 0.372664*asin(-0.104727*Abs(2.7*x_1 - 3.25) + 2.16422*asin(0.0499997*x_3 - 0.5) + 0.994163) - 0.726152*atanh(0.2*(0.193072*sin(2.25*x_2 - 3.8) - 4.00617*asin(0.0499997*x_3 - 0.5) + 0.147998*atanh(0.4*x_1 - 1.35) - 1.25299)*(-0.0648565*Abs(3.1*x_1 - 4.05) - 8.47073*asin(0.0499997*x_3 - 0.5) - 5.16585 + 0.396836*exp(-1.5625*(1 - 0.96*x_2)**2)) - 0.8) + 6.71419*atanh(0.770787*sqrt(0.0918367*x_1 + 1) - 0.00895616*cos(3.25*x_2 - 3.85) + 0.295968*asin(0.0499997*x_3 - 0.5) - 1.05574) + 7.19459`
- icbr_no_shared formula (display, rounded):
  - `12.0252*sqrt(sqrt(0.07*x_1 + 1) + 0.21497*atanh(0.0499997*x_3 - 0.4) - 0.254137) + 36.413*(0.804561*sqrt(0.071066*x_1 + 1) + 0.109609*acos(0.0499997*x_3 - 0.5) - 1)**(3/2) + 0.0908697*tanh(15.0699*acos(0.0499997*x_3 - 0.5) - 27.2324) + 0.0843935*Abs(1.45*(81.3891*sqrt(0.0111111*x_1 + 1) + 4.15448*atanh(0.0499997*x_3 - 0.4) - 79.8963)*(5.82665*atanh(0.0499997*x_3 - 0.4) + 1.25468 + 0.581717*exp(-1.5625*(0.96*x_2 - 1)**2)) - 0.75) + 0.372664*acos(-0.104727*Abs(2.7*x_1 - 3.25) - 2.16422*acos(0.0499997*x_3 - 0.5) + 4.39371) - 0.726152*atanh(0.2*(0.213859*tanh(2.1*x_2 - 3.5) + 4.00617*acos(0.0499997*x_3 - 0.5) + 0.147998*atanh(0.4*x_1 - 1.35) - 7.55484)*(-0.0648565*Abs(3.1*x_1 - 4.05) - 8.47073*asin(0.0499997*x_3 - 0.5) - 5.16585 + 0.396836*exp(-1.5625*(1 - 0.96*x_2)**2)) - 0.8) + 6.71419*atanh(0.756706*sqrt(0.09375*x_1 + 1) + 0.0096015*Abs(2.55*x_2 - 3.1) + 0.298096*atanh(0.0499997*x_3 - 0.4) - 1.08243) - 8.10854`
- icbr_refit_commit formula (display, rounded):
  - `25.9234*(sqrt(0.0716149*x_1 + 1) - 0.0885445*acos(0.60172 - 0.0779999*x_3) - 0.873777)**(3/2) + 15.7308*sqrt(0.711663*log(0.0960399*x_1 + 3.11808) + atanh(0.00428*x_3 - 0.64072) + 0.405395) - 0.109434*tanh(6.82442*acos(0.6004 - 0.0779999*x_3) - 9.23845) + 0.0240118*Abs(4.98408*(32.3501*atanh(0.00392*x_3 - 0.65524) + 21.7629 + 7.68637*exp(-0.810144*(0.0755488*x_1 - 1)**2))*(43.0131*atanh(0.00428*x_3 - 0.64052) + 31.4386 + 0.640903*exp(-1.20987*(0.98369*x_2 - 1)**2)) - 0.182) - 1.15972*atanh(0.1108*(0.213821*tanh(2.10068*x_2 - 3.5012) + 2.60113*acos(0.0775199*x_3 - 0.60096) + 0.198555*atanh(0.3134*x_1 - 1.18152) - 4.86836)*(-0.36798*Abs(0.53504*x_1 - 0.64304) - 33.8674*asin(0.01024*x_3 - 0.6614) - 25.2592 + 0.418098*exp(-1.28904*(1 - 0.987*x_2)**2)) - 0.8018) + 0.470738*atanh(0.0660073*Abs(3.29588*x_1 - 3.69628) + 1.0911*acos(0.0776399*x_3 - 0.60264) - 2.34317) + 8.77864*atanh(0.645819*log(0.0961199*x_1 + 2.42204) + 0.0048686*Abs(3.67324*x_2 - 4.46556) + 1.68453*atanh(0.00408*x_3 - 0.63972) + 0.235339) - 7.62148`

### task=feynman_I_10_7 seed=13

- Task source: feynman_file
- Target formula: `m_0/sqrt(1-v**2/c**2)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.100221e-02, r2=0.992481
- Variant formula overview:
  - icbr_full: symbolic_s=2.344634e+00, imitation_mse=3.905891e-03, target_mse=1.038419e-02, formula_export_success=True
  - icbr_no_replay: symbolic_s=1.553603e+00, imitation_mse=4.406367e-03, target_mse=1.197792e-02, formula_export_success=True
  - icbr_no_shared: symbolic_s=3.378961e+00, imitation_mse=3.905891e-03, target_mse=1.038419e-02, formula_export_success=True
  - icbr_refit_commit: symbolic_s=4.579045e+00, imitation_mse=4.320880e-03, target_mse=1.073183e-02, formula_export_success=True
- icbr_full formula (display, rounded):
  - `26.5516*sqrt(0.01*(1.53591*sqrt(0.169492*x_1 + 1) - 13.0355*acos(0.0499997*x_3 - 0.5) + 25.4093)*(-0.107097*sin(5.0*x_2 + 1.0) - 0.169045*asin(0.0999997*x_3 - 0.75) - 3.35263 + 9.54634*exp(-(0.1*x_1 - 1.0)**2)) + 1) + 2.41154*asin(0.0267978*Abs(3.15*x_2 - 4.2) - 0.163053*acos(0.3*x_1 - 1.05) + 1.05101*asin(0.0499997*x_3 - 0.5) + 0.320218) - 0.476678*atanh(0.189638*acos(0.4*x_1 - 1.4) + 3.85152*atanh(0.0499997*x_3 - 0.4) - 0.118072) - 25.6726 + 4.6613*exp(-4.63572*(0.0263825*sin(3.8*x_2 - 0.95) - 0.242818*asin(0.3*x_1 - 1.05) + atanh(0.0499997*x_3 - 0.4) + 0.652051)**2) + 0.111554*exp(-15.5866*(-atanh(0.0499997*x_3 - 0.4) - 0.284517)**2)`
- icbr_no_replay formula (display, rounded):
  - `0.124961*(0.33518*asin(0.3*x_1 - 1.05) + 13.1292*atanh(0.0499997*x_3 - 0.4) + 5.56146)*(-0.169045*asin(0.0999997*x_3 - 0.75) - 3.26307 + 9.54634*exp(-(0.1*x_1 - 1.0)**2) - 0.210838*exp(-18.9225*(1 - 0.735632*x_2)**2)) + 2.41154*asin(0.0267978*Abs(3.15*x_2 - 4.2) + 0.163053*asin(0.3*x_1 - 1.05) + 1.05101*asin(0.0499997*x_3 - 0.5) + 0.0640962) - 1.75566*atan(0.123074*sin(3.8*x_2 - 0.95) - 1.13274*asin(0.3*x_1 - 1.05) + 4.63169*asin(0.0499997*x_3 - 0.5) + 1.55671) - 0.476678*atanh(-0.189638*asin(0.4*x_1 - 1.4) + 3.82403*asin(0.0499997*x_3 - 0.5) + 0.563642) + 3.02237 + 0.111554*exp(-15.5866*(-atanh(0.0499997*x_3 - 0.4) - 0.284517)**2)`
- icbr_no_shared formula (display, rounded):
  - `26.5516*sqrt(0.01*(1.53591*sqrt(0.169492*x_1 + 1) - 13.0355*acos(0.0499997*x_3 - 0.5) + 25.4093)*(-0.107097*sin(5.0*x_2 + 1.0) - 0.169045*asin(0.0999997*x_3 - 0.75) - 3.35263 + 9.54634*exp(-(0.1*x_1 - 1.0)**2)) + 1) + 2.41154*asin(0.0267978*Abs(3.15*x_2 - 4.2) - 0.163053*acos(0.3*x_1 - 1.05) + 1.05101*asin(0.0499997*x_3 - 0.5) + 0.320218) - 0.476678*atanh(0.189638*acos(0.4*x_1 - 1.4) + 3.85152*atanh(0.0499997*x_3 - 0.4) - 0.118072) - 25.6726 + 4.6613*exp(-4.63572*(0.0263825*sin(3.8*x_2 - 0.95) - 0.242818*asin(0.3*x_1 - 1.05) + atanh(0.0499997*x_3 - 0.4) + 0.652051)**2) + 0.111554*exp(-15.5866*(-atanh(0.0499997*x_3 - 0.4) - 0.284517)**2)`
- icbr_refit_commit formula (display, rounded):
  - `26.5318*sqrt(0.0100079*(1.54534*sqrt(0.168257*x_1 + 1) + 44.3572*acos(0.62152 - 0.0126*x_3) - 41.7617)*(-0.1071*sin(4.99994*x_2 + 1.0) - 0.218042*acos(0.60046 - 0.0779999*x_3) - 5.26527 + 12.8315*exp(-0.81*(1 - 0.0822221*x_1)**2)) + 1) - 0.0620195*tanh(35.9309*atanh(0.00599999*x_3 - 0.60026) + 22.9515) + 3.00765*acos(-0.0190056*Abs(3.55448*x_2 - 4.76684) - 0.624474*acos(0.794 - 0.0506799*x_1) - 0.54083*asin(0.0784399*x_3 - 0.60588) + 0.649798) - 0.593998*atanh(-0.151476*acos(1.42396 - 0.42244*x_1) + 23.3259*atanh(0.00432*x_3 - 0.64884) + 17.0534) - 30.2199 + 4.65645*exp(-286.335*(0.00972368*sin(2.036*x_2 + 4.79998) + 0.0246956*asin(0.36708*x_1 - 1.22304) - atanh(0.00408*x_3 - 0.63168) - 0.782678)**2)`

### task=feynman_I_10_7 seed=14

- Task source: feynman_file
- Target formula: `m_0/sqrt(1-v**2/c**2)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=7.272445e-03, r2=0.994964
- Variant formula overview:
  - icbr_full: symbolic_s=2.572386e+00, imitation_mse=2.608390e-03, target_mse=7.784284e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=1.698867e+00, imitation_mse=3.004002e-03, target_mse=8.719440e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=3.730612e+00, imitation_mse=2.608361e-03, target_mse=7.785153e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=4.868510e+00, imitation_mse=2.885866e-03, target_mse=7.253238e-03, formula_export_success=True
- icbr_full formula (display, rounded):
  - `32.3505*sqrt(0.01*(-41.8772*sqrt(0.0306122*x_1 + 1) - 4.65315*asin(0.0499997*x_3 - 0.5) + 40.1405 - 0.13287*exp(-12.25*(1 - 0.757143*x_2)**2))*(-39.2509*log(0.05*x_1 + 4.925) - 0.126586*Abs(4.0*x_2 - 5.0) - 5.65152*atanh(0.0499997*x_3 - 0.4) + 60.009) + 1) - 12.0536*(-0.163992*asin(0.0499997*x_3 - 0.5) + 1 - 0.516718*exp(-0.64*(0.0625*x_1 - 1)**2))**(3/2) + 1.37*cos(0.152912*atanh(0.45*x_1 - 1.45) - 3.21098*atanh(0.0499997*x_3 - 0.4) + 3.95585) - 0.488474*tanh(6.58725*tan(0.05*x_3 - 0.4) - 0.110514*Abs(4.2*x_1 - 4.55) + 2.63211) - 0.650869*asin(0.5*(4.18286*asin(0.0499997*x_3 - 0.5) + 2.09841)*(-2.28597*(0.01*x_1 + 1)**(3/2) + 0.0942267*cos(3.3*x_2 - 3.95) + 4.07047*asin(0.0499997*x_3 - 0.5) + 3.97882) - 1.0) - 23.2045`
- icbr_no_replay formula (display, rounded):
  - `-7.71035*(0.220893*acos(0.0499997*x_3 - 0.5) + 1 - 0.696008*exp(-0.64*(0.0625*x_1 - 1)**2))**(3/2) + 0.153006*(-71.9177*sqrt(0.010929*x_1 + 1) - 0.126586*Abs(4.0*x_2 - 5.0) + 5.61218*acos(0.0499997*x_3 - 0.5) + 59.962)*(-41.8772*sqrt(0.0306122*x_1 + 1) + 0.0596259*Abs(3.75*x_2 - 4.9) + 4.65315*acos(0.0499997*x_3 - 0.5) + 32.689) + 0.650869*acos(0.5*(8.66883 - 4.18286*acos(0.0499997*x_3 - 0.5))*(-0.0348027*x_1 - 4.07047*acos(0.0499997*x_3 - 0.5) + 7.96344 + 0.219383*exp(-4.0*(1 - 0.825*x_2)**2)) - 1.0) + 9.18371 + 0.859699*exp(-96.2079*(0.00751137*Abs(4.2*x_1 - 4.55) + 0.444555*acos(0.0499997*x_3 - 0.5) - 1)**2) - 2.81685*exp(-6.5246*(0.0207855*tan(0.6*x_1 + 4.35) + 0.686577*acos(0.0499997*x_3 - 0.5) - 1)**2)`
- icbr_no_shared formula (display, rounded):
  - `32.3505*sqrt(0.01*(-42.082*sqrt(0.0304569*x_1 + 1) - 4.65315*asin(0.0499997*x_3 - 0.5) + 40.3451 - 0.13287*exp(-12.25*(1 - 0.757143*x_2)**2))*(-39.2509*log(0.05*x_1 + 4.925) - 0.126586*Abs(4.0*x_2 - 5.0) - 5.65152*atanh(0.0499997*x_3 - 0.4) + 60.009) + 1) - 12.0536*(-0.163992*asin(0.0499997*x_3 - 0.5) + 1 - 0.516718*exp(-0.64*(1 - 0.0625*x_1)**2))**(3/2) + 1.37*cos(0.152912*atanh(0.45*x_1 - 1.45) - 3.21098*atanh(0.0499997*x_3 - 0.4) + 3.95585) - 0.488474*tanh(6.58725*tan(0.05*x_3 - 0.4) - 0.102007*Abs(4.55*x_1 - 4.925) + 2.63246) + 0.650869*acos(0.5*(8.66883 - 4.18286*acos(0.0499997*x_3 - 0.5))*(-2.28597*(0.01*x_1 + 1)**(3/2) + 0.0942267*cos(3.3*x_2 - 3.95) + 4.07047*asin(0.0499997*x_3 - 0.5) + 3.97882) - 1.0) - 24.2269`
- icbr_refit_commit formula (display, rounded):
  - `32.3404*sqrt(0.0100033*(-37.2353*sqrt(0.0214274*x_1 + 1) - 0.136038*Abs(3.65156*x_2 - 4.55388) - 3.62167*acos(0.60026 - 0.0779999*x_3) + 40.4392)*(-32.5065*log(0.0999999*x_1 + 4.9992) + 3.01104*acos(0.0777599*x_3 - 0.60244) + 46.393 - 0.139434*exp(-10.2444*(1 - 0.756089*x_2)**2)) + 1) - 42.1465*(-0.603306*sqrt(0.0330548*x_1 + 1) - 0.0459364*acos(0.6001 - 0.0779999*x_3) + 1)**(3/2) + 1.37041*cos(-0.273408*atanh(0.2492*x_1 - 1.16428) + 22.6985*atanh(0.00452*x_3 - 0.63644) + 11.6754) - 0.678294*acos(-0.48472*(31.1137*atanh(0.00428*x_3 - 0.64036) + 23.5456)*(-1.96211*(0.011623*x_1 + 1)**(3/2) - 0.0929343*cos(3.34932*x_2 - 0.8696) + 30.8862*atanh(0.00404*x_3 - 0.65744) + 25.9001) + 0.97932) - 22.6211 + 0.846494*exp(-587.467*(-tan(0.00623999*x_3 - 0.62168) + 0.00361217*Abs(3.43832*x_1 - 3.64024) - 0.745288)**2)`

### task=feynman_I_10_7 seed=15

- Task source: feynman_file
- Target formula: `m_0/sqrt(1-v**2/c**2)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=3.860933e-03, r2=0.997343
- Variant formula overview:
  - icbr_full: symbolic_s=2.353506e+00, imitation_mse=6.067846e-04, target_mse=4.059847e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=1.508968e+00, imitation_mse=7.518861e-04, target_mse=4.245692e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=3.205773e+00, imitation_mse=6.067136e-04, target_mse=4.059943e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=4.310519e+00, imitation_mse=6.723594e-04, target_mse=4.417954e-03, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0.00528325*Abs(4.25*(6.33783*atanh(0.0499997*x_3 - 0.4) + 2.52567)*(-0.0608092*Abs(2.9*x_1 - 3.45) + 4.13158*atanh(0.0499997*x_3 - 0.4) + 1.4979) - 4.625) - 0.11448*Abs(46.9916*asin(0.0499997*x_3 - 0.5) + 65.4057 - 0.68691*exp(-17.2225*(0.73494*x_2 - 1)**2) - 66.7894*exp(-0.64*(0.0625*x_1 - 1)**2)) + 1.34004*atanh(0.370136*cos(0.3*x_1 - 2.5) - 1.90717*atanh(0.0499997*x_3 - 0.4) + 0.0353427) - 11.8819*atanh(0.993065*(1 - 0.0331492*x_1)**(3/2) + 0.00895373*cos(3.55*x_2 + 1.95) + 0.620661*acos(0.0499997*x_3 - 0.5) - 1.89459) + 4.7454 + 0.146747/sqrt(-(13.4597 - 6.49436*acos(0.0499997*x_3 - 0.5))*(-7.70587*asin(0.0499997*x_3 - 0.5) - 3.86623) - 0.836066)`
- icbr_no_replay formula (display, rounded):
  - `-0.11448*Abs(46.9916*acos(0.0499997*x_3 - 0.5) - 139.22 + 66.7894*exp(-0.64*(0.0625*x_1 - 1)**2) + 0.68691*exp(-17.2225*(1 - 0.73494*x_2)**2)) - 11.8161*acos(-0.993065*(1 - 0.0331492*x_1)**(3/2) + 0.00710464*Abs(3.7*x_2 - 4.575) - 0.620661*acos(0.0499997*x_3 - 0.5) + 1.78347) + 0.962831*asin(0.518191*cos(0.3*x_1 - 2.5) + 2.6512*acos(0.0499997*x_3 - 0.5) - 4.43116) + 24.6054 - 0.0701599*exp(-1.0*(-0.9*(-6.33783*atanh(0.0499997*x_3 - 0.4) - 2.52567)*(0.0608092*Abs(2.9*x_1 - 3.45) + 4.10243*acos(0.0499997*x_3 - 0.5) - 8.35381) + 1)**2) + 0.146747/sqrt(-(13.4597 - 6.49436*acos(0.0499997*x_3 - 0.5))*(-7.76063*atanh(0.0499997*x_3 - 0.4) - 3.09267) - 0.836066)`
- icbr_no_shared formula (display, rounded):
  - `0.00493421*Abs(4.55*(6.33783*atanh(0.0499997*x_3 - 0.4) + 2.52567)*(-0.0839837*Abs(2.1*x_1 - 2.5) + 4.13158*atanh(0.0499997*x_3 - 0.4) + 1.4978) - 4.95) - 0.11448*Abs(46.9916*asin(0.0499997*x_3 - 0.5) + 65.4057 - 0.68691*exp(-17.2225*(0.73494*x_2 - 1)**2) - 66.7894*exp(-0.64*(0.0625*x_1 - 1)**2)) + 1.34004*atanh(0.370136*cos(0.3*x_1 - 2.5) - 1.90717*atanh(0.0499997*x_3 - 0.4) + 0.0353427) - 11.8819*atanh(0.993065*(1 - 0.0331492*x_1)**(3/2) + 0.00895373*cos(3.55*x_2 + 1.95) + 0.620661*acos(0.0499997*x_3 - 0.5) - 1.89459) + 4.74543 + 0.146669/sqrt(-(13.4597 - 6.49436*acos(0.0499997*x_3 - 0.5))*(-7.70587*asin(0.0499997*x_3 - 0.5) - 3.86623) - 0.836364)`
- icbr_refit_commit formula (display, rounded):
  - `-0.0454036*log(-4.49416*(26.6107*acos(0.66708 - 0.00991999*x_3) - 22.4733)*(-26.0229*asin(0.0128*x_3 - 0.612) - 17.0105) - 4.59616) + 0.0103559*Abs(2.26932*(38.7932*atanh(0.00563999*x_3 - 0.60016) + 26.7985)*(-0.0599043*Abs(2.916*x_1 - 3.21448) + 30.3371*atanh(0.00436*x_3 - 0.63428) + 22.51) - 2.88732) - 0.106272*Abs(32.6135*asin(0.0779999*x_3 - 0.6002) + 48.903 - 0.845953*exp(-11.0012*(0.729908*x_2 - 1)**2) - 48.5165*exp(-0.81*(0.0822221*x_1 - 1)**2)) + 1.33836*atanh(0.33212*cos(0.338*x_1 + 3.70038) - 1.22369*asin(0.0779999*x_3 - 0.60122) + 0.0520499) - 164.469*atanh(0.0417113*(1 - 0.0341521*x_1)**(3/2) + 0.000387079*cos(3.54664*x_2 - 4.32872) - 0.183429*atanh(0.0044*x_3 - 0.66824) + 0.46302) + 128.561`

### task=feynman_I_10_7 seed=16

- Task source: feynman_file
- Target formula: `m_0/sqrt(1-v**2/c**2)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.727486e-02, r2=0.988392
- Variant formula overview:
  - icbr_full: symbolic_s=3.415790e+00, imitation_mse=6.055890e-03, target_mse=1.734900e-02, formula_export_success=True
  - icbr_no_replay: symbolic_s=2.206335e+00, imitation_mse=5.864637e-03, target_mse=1.556273e-02, formula_export_success=True
  - icbr_no_shared: symbolic_s=4.989302e+00, imitation_mse=6.054870e-03, target_mse=1.734971e-02, formula_export_success=True
  - icbr_refit_commit: symbolic_s=6.440260e+00, imitation_mse=nan, target_mse=nan, formula_export_success=True
- icbr_full formula (display, rounded):
  - `22.3369*sqrt(-0.0517291*acos(0.4*x_1 - 1.4) + 0.431436*atanh(0.0499997*x_3 - 0.4) + 1 + 0.0492455*exp(-0.09*(-x_2 - 0.833334)**2)) + 1.07672*cos(6.91925*atanh(0.0499997*x_3 - 0.4) + 3.14773 - 0.389766*exp(-16.0*(1 - 0.7125*x_2)**2)) + 1.1917*acos(0.15*(0.255218*sin(2.6*x_2 + 1.9) - 0.112489*Abs(3.15*x_1 - 4.8) + 5.3682*acos(0.0499997*x_3 - 0.5) - 10.7248)*(-0.162706*cos(3.95*x_2 - 4.975) - 0.047762*Abs(2.55*x_1 - 4.7) - 5.57925*asin(0.0499997*x_3 - 0.5) - 2.28797) - 0.9) - 3.612*acos(-0.13404*acos(0.35*x_1 - 1.2) + 0.410944*atanh(0.0499997*x_3 - 0.4) - 0.0728629) - 39.5791 + 9.88235*exp(-0.198684*(-0.0180473*cos(1.6*x_2 - 4.15) - acos(0.0499997*x_3 - 0.5) + 0.151202*asin(0.4*x_1 - 1.4) + 0.448232)**2) + 19.2797/sqrt(-0.12987*(-0.193966*sin(0.35*x_1 - 1.05) - 0.147648*sin(2.65*x_2 + 1.85) - 2.54015*asin(0.0499997*x_3 - 0.5) - 1.92097)*(-0.117166*Abs(2.2*x_1 - 3.5) - 0.0573438*Abs(3.1*x_2 - 4.2) - 2.03352*acos(0.0499997*x_3 - 0.5) + 3.74869) + 1)`
- icbr_no_replay formula (display, rounded):
  - `-6.55173*log(-0.95*(-0.117166*Abs(2.2*x_1 - 3.5) + 2.04801*atanh(0.0499997*x_3 - 0.4) + 0.252888 + 0.0940408*exp(-18.9225*(1 - 0.735632*x_2)**2))*(-0.0228505*Abs(2.85*x_1 - 3.3) + 2.54015*acos(0.0499997*x_3 - 0.5) - 6.01729 + 0.374361*exp(-1.69*(1 - 0.923077*x_2)**2)) + 4.975) - 1.1917*asin(0.15*(-0.047762*Abs(2.55*x_1 - 4.7) + 0.141604*Abs(3.6*x_2 - 4.525) - 5.61903*atanh(0.0499997*x_3 - 0.4) - 1.92928)*(-0.112489*Abs(3.15*x_1 - 4.8) + 5.3682*acos(0.0499997*x_3 - 0.5) - 10.3495 - 0.631898*exp(-1.69*(1 - 0.923077*x_2)**2)) - 0.9) + 8.34343*asin(0.0331201*sin(0.5*x_2 - 3.9) - 0.561435*acos(0.0499997*x_3 - 0.5) + 0.0677959*asin(0.4*x_1 - 1.4) + 0.636621) + 3.69564*atanh(-0.408036*acos(0.0499997*x_3 - 0.5) + 0.13404*asin(0.35*x_1 - 1.2) + 0.548488) + 9.11278 + 9.88235*exp(-0.198684*(-0.018543*sin(1.55*x_2 - 2.5) - acos(0.0499997*x_3 - 0.5) + 0.151202*asin(0.4*x_1 - 1.4) + 0.448202)**2) + 1.49041*exp(-165.137*(0.503784*acos(0.0499997*x_3 - 0.5) - 1 + 0.0285808*exp(-16.0*(1 - 0.7125*x_2)**2))**2)`
- icbr_no_shared formula (display, rounded):
  - `22.3369*sqrt(-0.0517291*acos(0.4*x_1 - 1.4) + 0.431436*atanh(0.0499997*x_3 - 0.4) + 1 + 0.0492455*exp(-0.09*(-x_2 - 0.833334)**2)) + 1.07672*cos(6.91925*atanh(0.0499997*x_3 - 0.4) + 3.14773 - 0.389766*exp(-16.0*(1 - 0.7125*x_2)**2)) + 1.1917*acos(0.15*(0.255218*sin(2.6*x_2 + 1.9) - 0.109002*Abs(3.25*x_1 - 4.95) + 5.3682*acos(0.0499997*x_3 - 0.5) - 10.7248)*(-0.162706*cos(3.95*x_2 - 4.975) - 0.047762*Abs(2.55*x_1 - 4.7) + 5.57925*acos(0.0499997*x_3 - 0.5) - 11.0518) - 0.9) - 3.612*acos(-0.13404*acos(0.35*x_1 - 1.2) + 0.410944*atanh(0.0499997*x_3 - 0.4) - 0.0728629) - 39.5791 + 9.88235*exp(-0.198684*(-0.0180473*cos(1.6*x_2 - 4.15) - acos(0.0499997*x_3 - 0.5) + 0.151202*asin(0.4*x_1 - 1.4) + 0.448232)**2) + 19.2797/sqrt(-0.12987*(-0.193966*sin(0.35*x_1 - 1.05) - 0.147648*sin(2.65*x_2 + 1.85) - 2.54015*asin(0.0499997*x_3 - 0.5) - 1.92097)*(-0.117166*Abs(2.2*x_1 - 3.5) - 0.0573438*Abs(3.1*x_2 - 4.2) - 2.03352*acos(0.0499997*x_3 - 0.5) + 3.74869) + 1)`
- icbr_refit_commit formula (display, rounded):
  - `15.5315*sqrt(0.572942*acos(0.60096 - 0.0784799*x_3) + 0.101587*asin(0.42468*x_1 - 1.42904) + 1 + 0.115552*exp(-0.0905045*(-0.884191*x_2 - 1)**2)) + 1.04362*cos(40.387*atanh(0.00607999*x_3 - 0.60412) + 28.5347 - 0.465906*exp(-11.2078*(1 - 0.70469*x_2)**2)) - 1.45205*acos(-0.12352*(0.246484*sin(2.701*x_2 - 4.51384) - 0.102828*Abs(3.30884*x_1 - 4.81028) - 40.9271*atanh(0.00412*x_3 - 0.646) - 30.9808)*(0.162678*cos(3.95128*x_2 - 1.8352) - 0.0861376*Abs(1.43484*x_1 - 2.76952) - 32.4573*atanh(0.00599999*x_3 - 0.60004) - 21.8997) + 0.83956) - 3.74788*acos(-0.116306*acos(0.38244*x_1 - 1.27668) + 0.249478*asin(0.0790399*x_3 - 0.60612) - 0.124248) - 24.95 - 6.8089*exp(-1.85369*(-0.00986699*cos(1.36112*x_2 - 0.67276) - 0.067125*acos(1.42924 - 0.42488*x_1) + 0.304914*acos(0.0777999*x_3 - 0.60448) - 1)**2) + 19.3116/sqrt(-0.129671*(-0.202337*sin(0.334*x_1 - 0.9993) + 1.72431*acos(0.0739999*x_3 - 0.60086) - 4.60865 + 0.366928*exp(-1.7738*(1 - 0.91987*x_2)**2))*(-0.100075*Abs(2.551*x_1 - 4.11772) - 0.0596546*Abs(3.0324*x_2 - 4.14652) + 11.8187*atanh(0.00599999*x_3 - 0.60062) + 7.6968) + 1)`

### task=feynman_I_10_7 seed=17

- Task source: feynman_file
- Target formula: `m_0/sqrt(1-v**2/c**2)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=5.949637e-03, r2=0.996164
- Variant formula overview:
  - icbr_full: symbolic_s=3.691060e+00, imitation_mse=8.149193e-03, target_mse=1.314933e-02, formula_export_success=True
  - icbr_no_replay: symbolic_s=2.333503e+00, imitation_mse=8.355324e-03, target_mse=1.303849e-02, formula_export_success=True
  - icbr_no_shared: symbolic_s=5.437573e+00, imitation_mse=8.148701e-03, target_mse=1.315001e-02, formula_export_success=True
  - icbr_refit_commit: symbolic_s=6.730699e+00, imitation_mse=7.906892e-03, target_mse=1.294537e-02, formula_export_success=True
- icbr_full formula (display, rounded):
  - `1.21838*sin(6.57078*sqrt(0.102041*x_1 + 1) + 0.0596534*Abs(4.0*x_2 - 5.0) + 0.324235*atanh(0.0499997*x_3 - 0.4) - 1.38152) + 0.683409*tan(0.341095*sin(0.35*x_1 - 1.1) + 0.0241848*Abs(3.8*x_2 - 4.85) - 1.80298*atanh(0.0499997*x_3 - 0.4) - 0.512631) + 0.716396*tanh(0.4*(-0.159656*atan(2.15*x_2 - 3.65) - 12.1994*atanh(0.0499997*x_3 - 0.4) - 5.28379)*(-37.9022*sqrt(0.0324324*x_1 + 1) - 0.129179*sin(1.9*x_2 + 3.0) + 6.85328*atanh(0.0499997*x_3 - 0.4) + 40.5575) - 1.15) - 0.721146*tanh(0.119521*Abs(3.65*x_2 - 4.6) + 1.64847*acos(0.3*x_1 - 1.05) + 4.69889*atanh(0.0499997*x_3 - 0.4) - 2.98524) + 2.45921*asin(0.0999997*(1.43149*cos(0.3*x_1 - 2.5) + 0.0848552*Abs(3.65*x_2 - 4.575) + 0.631781*atanh(0.0499997*x_3 - 0.4) + 1.67806)*(-0.0355952*Abs(3.4*x_1 - 5.0) - 0.0386398*Abs(4.05*x_2 - 5.0) + 8.34048*atanh(0.0499997*x_3 - 0.4) + 3.04755) - 0.65) - 0.0449987*atan(19.4627*atanh(0.0499997*x_3 - 0.4) + 2.75617) + 4.73781 - 0.24554*exp(-247.332*(0.00448486*Abs(2.9*x_1 - 3.8) + 0.540672*acos(0.0499997*x_3 - 0.5) - 1)**2)`
- icbr_no_replay formula (display, rounded):
  - `1.21579*cos(6.57078*sqrt(0.102041*x_1 + 1) + 0.0596534*Abs(4.0*x_2 - 5.0) + 0.321954*asin(0.0499997*x_3 - 0.5) - 2.89921) + 0.683409*tan(0.0369154*Abs(3.1*x_1 - 3.55) + 0.0241848*Abs(3.8*x_2 - 4.85) - 1.7903*asin(0.0499997*x_3 - 0.5) - 0.920812) - 0.721146*tanh(0.119521*Abs(3.65*x_2 - 4.6) + 1.64847*acos(0.3*x_1 - 1.05) - 4.66584*acos(0.0499997*x_3 - 0.5) + 4.8122) + 2.45921*asin(0.0999997*(-0.0355952*Abs(3.4*x_1 - 5.0) - 0.0386398*Abs(4.05*x_2 - 5.0) - 8.2818*acos(0.0499997*x_3 - 0.5) + 16.8879)*(0.0848552*Abs(3.65*x_2 - 4.575) + 0.627337*asin(0.0499997*x_3 - 0.5) - 1.30385 + 4.90806*exp(-(0.1*x_1 - 1.0)**2)) - 0.65) + 3.9354 - 0.24554*exp(-72.3016*(0.00829498*Abs(2.9*x_1 - 3.8) - asin(0.0499997*x_3 - 0.5) - 0.278753)**2) + 0.104479*exp(-70.2626*(asin(0.0499997*x_3 - 0.5) + 0.322772)**2) + 1.30602*exp(-2.25*(0.166667*(-12.1136*asin(0.0499997*x_3 - 0.5) - 0.159656*atan(2.15*x_2 - 3.65) - 6.49979)*(-6.80507*acos(0.0499997*x_3 - 0.5) + 21.1405 - 13.8351*exp(-0.64*(0.0625*x_1 - 1)**2) + 0.281891*exp(-(0.95 - 1.0*x_2)**2)) - 1)**2)`
- icbr_no_shared formula (display, rounded):
  - `1.21838*sin(6.57078*sqrt(0.102041*x_1 + 1) + 0.0596534*Abs(4.0*x_2 - 5.0) + 0.324235*atanh(0.0499997*x_3 - 0.4) - 1.38152) + 0.683409*tan(0.341095*sin(0.35*x_1 - 1.1) + 0.0241848*Abs(3.8*x_2 - 4.85) - 1.80298*atanh(0.0499997*x_3 - 0.4) - 0.512631) + 0.716396*tanh(0.4*(-0.159656*atan(2.15*x_2 - 3.65) - 12.1994*atanh(0.0499997*x_3 - 0.4) - 5.28379)*(-38.6857*sqrt(0.031746*x_1 + 1) - 0.129179*sin(1.9*x_2 + 3.0) + 6.85328*atanh(0.0499997*x_3 - 0.4) + 41.3403) - 1.15) - 0.721146*tanh(0.119521*Abs(3.65*x_2 - 4.6) + 1.64847*acos(0.3*x_1 - 1.05) + 4.69889*atanh(0.0499997*x_3 - 0.4) - 2.98524) + 2.45921*asin(0.0999997*(1.43149*cos(0.3*x_1 - 2.5) + 0.0848552*Abs(3.65*x_2 - 4.575) + 0.631781*atanh(0.0499997*x_3 - 0.4) + 1.67806)*(-0.0355952*Abs(3.4*x_1 - 5.0) - 0.0386398*Abs(4.05*x_2 - 5.0) + 8.34048*atanh(0.0499997*x_3 - 0.4) + 3.04755) - 0.65) - 0.0449987*atan(19.4627*atanh(0.0499997*x_3 - 0.4) + 2.75617) + 4.73781 - 0.24554*exp(-247.332*(0.00448486*Abs(2.9*x_1 - 3.8) + 0.540672*acos(0.0499997*x_3 - 0.5) - 1)**2)`
- icbr_refit_commit formula (display, rounded):
  - `1.01777*log(-0.96273*sin(0.336*x_1 - 4.19964) + 0.068337*Abs(3.60668*x_2 - 4.61104) - 37.0718*atanh(0.00416*x_3 - 0.64216) - 23.2076) + 1.53884*tanh(0.268*(-0.209404*atan(1.578*x_2 - 2.79944) - 94.3712*atanh(0.00416*x_3 - 0.63028) - 70.2832)*(-0.12904*sin(1.90168*x_2 + 2.99828) + 4.43162*acos(0.6 - 0.0772799*x_3) - 0.481247 - 8.89207*exp(-0.810036*(1 - 0.0866646*x_1)**2)) - 1.4) + 1.73926*tanh(0.0744032*Abs(2.16464*x_2 - 2.68104) + 0.653647*acos(0.99892 - 0.29956*x_1) + 0.145123*asin(0.0779999*x_3 - 0.6002) - 1.07419) - 0.750966*tanh(0.172628*Abs(2.29744*x_2 - 2.896) - 7.43054*acos(0.78684 - 0.0498799*x_1) + 32.1553*atanh(0.00416*x_3 - 0.65232) + 29.6726) + 1.80323*asin(0.13624*(5.92938*cos(0.0699999*x_1 + 4.49934) + 0.0874736*Abs(3.50884*x_2 - 4.41052) + 0.40484*asin(0.0779999*x_3 - 0.60146) + 1.64928)*(-0.0342734*Abs(3.36712*x_1 - 4.38788) - 0.0463292*Abs(3.33168*x_2 - 4.11364) + 30.1115*asin(0.01172*x_3 - 0.62392) + 19.8824) - 0.74932) - 0.0449765*atan(149.914*atanh(0.00412*x_3 - 0.64336) + 109.229) + 3.80669 - 0.256156*exp(-44.4127*(0.00692117*Abs(3.986*x_1 - 4.79956) - 0.755501*acos(0.60086 - 0.0779999*x_3) + 1)**2)`

### task=feynman_I_10_7 seed=18

- Task source: feynman_file
- Target formula: `m_0/sqrt(1-v**2/c**2)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=9.737878e-03, r2=0.993581
- Variant formula overview:
  - icbr_full: symbolic_s=3.165185e+00, imitation_mse=4.383460e-03, target_mse=8.271948e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=2.030944e+00, imitation_mse=4.746205e-03, target_mse=8.526148e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=4.916495e+00, imitation_mse=4.383750e-03, target_mse=8.272880e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=5.918292e+00, imitation_mse=nan, target_mse=nan, formula_export_success=True
- icbr_full formula (display, rounded):
  - `15.9334*sqrt(0.0172622*tan(1.15*x_2 + 1.3) + 0.0547206*asin(0.35*x_1 - 1.2) + 0.334468*asin(0.0499997*x_3 - 0.5) + 1) - 2.0689*(acos(0.0499997*x_3 - 0.5) - 0.128085*asin(0.35*x_1 - 1.2) + 0.539801 - 0.00897552*exp(-21.16*(1 - 0.706522*x_2)**2))**(3/2) + 1.75228*sin(0.45*(1.17478*cos(0.35*x_1 + 0.5) + 0.0492526*tanh(1.95*x_2 - 3.45) + 3.23785*atanh(0.0499997*x_3 - 0.4) + 0.350966)*(0.131759*Abs(2.45*x_1 - 3.0) + 0.0655648*Abs(3.65*x_2 - 4.575) + 2.85666*atanh(0.0499997*x_3 - 0.4) + 1.64492) - 4.05) - 0.00774027*tan(7.8997*asin(0.0499997*x_3 - 0.5) + 1.31287) - 0.0851175*tanh(1.61785*acos(0.4*x_1 - 1.4) - 20.9267*acos(0.0499997*x_3 - 0.5) + 33.5997) - 6.89745 + 7.31493/(4.55*(-1.08179*sin(0.35*x_1 - 1.1) + 5.74749*asin(0.0499997*x_3 - 0.5) + 1.86595)*(0.380961*sin(0.5*x_1 + 1.5) + 6.53155*atanh(0.0499997*x_3 - 0.4) + 2.77137 - 0.378117*exp(-1.44*(1 - 0.958333*x_2)**2)) + 4.8)`
- icbr_no_replay formula (display, rounded):
  - `-4.58914*(-0.0199437*tan(1.15*x_2 + 1.3) - 0.0632205*asin(0.35*x_1 - 1.2) - 0.386423*asin(0.0499997*x_3 - 0.5) + 1)**(3/2) - 6.34376*(-0.0606866*asin(0.35*x_1 - 1.2) - 0.4738*asin(0.0499997*x_3 - 0.5) + 1 - 0.0042526*exp(-21.16*(1 - 0.706522*x_2)**2))**(3/2) - 1.78471*cos(0.45*(0.131759*Abs(2.45*x_1 - 3.0) + 0.0655648*Abs(3.65*x_2 - 4.575) + 2.83672*asin(0.0499997*x_3 - 0.5) + 1.92971)*(-0.0924887*Abs(4.25*x_1 - 4.725) + 3.21526*asin(0.0499997*x_3 - 0.5) + 0.0437808*atan(2.25*x_2 - 4.0) + 1.44044) - 2.5) - 0.00774027*tan(7.8997*asin(0.0499997*x_3 - 0.5) + 1.31287) - 0.0851175*tanh(-1.61785*asin(0.4*x_1 - 1.4) + 20.9267*asin(0.0499997*x_3 - 0.5) + 3.26944) - 5.66576*atan(3.7*(-0.169216*Abs(2.15*x_1 - 2.55) + 5.74749*asin(0.0499997*x_3 - 0.5) + 2.57844)*(-0.0578077*Abs(3.05*x_1 - 4.05) + 6.48596*asin(0.0499997*x_3 - 0.5) + 3.76673 - 0.378117*exp(-1.44*(1 - 0.958333*x_2)**2)) + 3.65) + 22.4949`
- icbr_no_shared formula (display, rounded):
  - `16.2762*sqrt(0.0169128*tan(1.15*x_2 + 1.3) + 0.053613*asin(0.35*x_1 - 1.2) + 0.327698*asin(0.0499997*x_3 - 0.5) + 1) - 2.08177*(acos(0.0499997*x_3 - 0.5) - 0.128085*asin(0.35*x_1 - 1.2) + 0.511298 - 0.00897552*exp(-21.16*(1 - 0.706522*x_2)**2))**(3/2) + 1.75228*sin(0.45*(1.17478*cos(0.35*x_1 + 0.5) + 0.0492526*tanh(1.95*x_2 - 3.45) + 3.23785*atanh(0.0499997*x_3 - 0.4) + 0.350966)*(0.131759*Abs(2.45*x_1 - 3.0) + 0.0655648*Abs(3.65*x_2 - 4.575) + 2.85666*atanh(0.0499997*x_3 - 0.4) + 1.64492) - 4.05) - 0.00774027*tan(7.8997*asin(0.0499997*x_3 - 0.5) + 1.31287) - 0.0851175*tanh(1.61785*acos(0.4*x_1 - 1.4) - 20.9267*acos(0.0499997*x_3 - 0.5) + 33.5997) - 7.32969 + 7.31493/(4.55*(-1.08179*sin(0.35*x_1 - 1.1) + 5.74749*asin(0.0499997*x_3 - 0.5) + 1.86595)*(0.380961*sin(0.5*x_1 + 1.5) + 6.53155*atanh(0.0499997*x_3 - 0.4) + 2.77137 - 0.378117*exp(-1.44*(1 - 0.958333*x_2)**2)) + 4.8)`
- icbr_refit_commit formula (display, rounded):
  - `6895450.0*(-atanh(0.00436*x_3 - 0.63876) - 0.708576)**5 - 4.81409*(-0.0340347*tan(0.66728*x_2 + 1.93144) - 0.0555366*asin(0.38312*x_1 - 1.27804) - 0.241774*asin(0.0782799*x_3 - 0.60072) + 1)**(3/2) - 2.78649*(0.525309*acos(0.0787599*x_3 - 0.60244) - 0.100029*asin(0.3678*x_1 - 1.2246) + 1 - 0.00962277*exp(-11.2805*(1 - 0.695222*x_2)**2))**(3/2) - 57.4958*sin(0.0662799*(-1.21906*cos(0.336*x_1 - 2.59958) + 0.0713652*tanh(1.43908*x_2 - 2.80036) + 23.7179*atanh(0.00432*x_3 - 0.64012) + 17.0153)*(0.089173*Abs(3.58172*x_1 - 3.99536) + 0.0625129*Abs(3.71696*x_2 - 4.62528) + 20.9538*atanh(0.00424*x_3 - 0.64832) + 16.6226) - 1.45752) - 0.0916975*tanh(-1.03518*acos(1.42796 - 0.42548*x_1) + 110.963*atanh(0.004*x_3 - 0.64848) + 82.3092) - 42.2484 - 5.34516/(-3.31364*(1.10847*sin(0.34032*x_1 + 2.10068) + 3.66511*asin(0.0789199*x_3 - 0.6062) + 1.22555)*(-0.380104*sin(0.49984*x_1 - 1.6208) + 52.2328*atanh(0.00392*x_3 - 0.64232) + 39.8679 - 0.356193*exp(-1.69255*(1 - 0.943904*x_2)**2)) - 3.5072)`

### task=feynman_I_10_7 seed=19

- Task source: feynman_file
- Target formula: `m_0/sqrt(1-v**2/c**2)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=4.861716e-03, r2=0.996651
- Variant formula overview:
  - icbr_full: symbolic_s=3.601777e+00, imitation_mse=2.055234e-03, target_mse=5.672069e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=2.269449e+00, imitation_mse=2.684528e-03, target_mse=6.254700e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=5.218605e+00, imitation_mse=2.055417e-03, target_mse=5.674767e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=6.621522e+00, imitation_mse=2.270546e-03, target_mse=6.003378e-03, formula_export_success=True
- icbr_full formula (display, rounded):
  - `-1.39695*(0.582421*(1 - 0.04*x_1)**(3/2) - 0.605313*atanh(0.0499997*x_3 - 0.4) + 1)**(3/2) - 0.392749*sin(0.128903*Abs(3.7*x_1 - 4.15) - 0.257637*Abs(3.65*x_2 - 4.575) + 4.44417*acos(0.0499997*x_3 - 0.5) - 10.7601) - 0.0846262*tanh(5.63171*asin(0.0499997*x_3 - 0.5) + 1.12544) + 0.0456311*Abs(3.2*(11.3975*sqrt(0.12987*x_1 + 1) + 0.166284*Abs(3.4*x_2 - 4.4) + 2.59361*acos(0.0499997*x_3 - 0.5) - 16.6262)*(0.605486*cos(0.85*x_1 + 1.9) + 0.129938*Abs(3.55*x_2 - 4.65) + 8.27887*asin(0.0499997*x_3 - 0.5) + 5.78521) + 2.3) + 1.83762*acos(-0.0181135*Abs(3.65*x_2 - 4.55) - 0.143987*asin(0.45*x_1 - 1.45) - 1.08366*atanh(0.0499997*x_3 - 0.4) - 0.046898) + 1.18105 + 4.05098*exp(-44.8245*((1 - 0.65*x_2)**4 - 0.0572864*asin(0.4*x_1 - 1.35) + 0.380403*asin(0.0499997*x_3 - 0.5) + 0.286497)**2) + 0.188677*exp(-2.56*(-(1.52678*sin(0.35*x_1 - 1.05) + 2.90839*atanh(0.0499997*x_3 - 0.4) + 2.5186)*(7.27024*asin(0.0499997*x_3 - 0.5) + 7.80837 - 7.66703*exp(-0.64*(0.0625*x_1 - 1)**2)) - 0.25)**2)`
- icbr_no_replay formula (display, rounded):
  - `-3.70906*(-0.698502*sqrt(0.0526316*x_1 + 1) + 0.31349*acos(0.0499997*x_3 - 0.5) + 1)**(3/2) + 147.214*(-(1 - 0.65*x_2)**4 + 0.0572864*asin(0.4*x_1 - 1.35) - 0.380403*asin(0.0499997*x_3 - 0.5) + 0.0773818)**3 + 0.387799*cos(0.131481*Abs(3.7*x_1 - 4.15) - 0.26279*Abs(3.65*x_2 - 4.575) + 4.53305*acos(0.0499997*x_3 - 0.5) - 9.35427) - 0.078187*tanh(4.35*(0.134596*Abs(3.8*x_1 - 4.3) + 2.88813*asin(0.0499997*x_3 - 0.5) + 1.85137)*(-7.27024*acos(0.0499997*x_3 - 0.5) + 19.2284 - 7.66703*exp(-0.64*(0.0625*x_1 - 1)**2)) - 1.8) + 0.0456311*Abs(3.2*(0.158471*Abs(2.6*x_1 - 4.0) + 0.129938*Abs(3.55*x_2 - 4.65) + 8.33692*atanh(0.0499997*x_3 - 0.4) + 4.23316)*(0.166284*Abs(3.4*x_2 - 4.4) - 2.00182*acos(0.3*x_1 - 1.0) + 2.59361*acos(0.0499997*x_3 - 0.5) + 0.14951) + 2.3) + 1.83762*asin(0.0181135*Abs(3.65*x_2 - 4.55) + 0.143987*asin(0.45*x_1 - 1.45) + 1.07612*asin(0.0499997*x_3 - 0.5) + 0.154944) + 4.09514 + 0.143145*exp(-58.2232*(0.510965*acos(0.0499997*x_3 - 0.5) - 1)**2)`
- icbr_no_shared formula (display, rounded):
  - `-1.46147*(0.560385*(1 - 0.04*x_1)**(3/2) - 0.582412*atanh(0.0499997*x_3 - 0.4) + 1)**(3/2) - 0.392749*sin(0.128903*Abs(3.7*x_1 - 4.15) - 0.257637*Abs(3.65*x_2 - 4.575) + 4.44417*acos(0.0499997*x_3 - 0.5) - 10.7601) - 0.0846262*tanh(5.63171*asin(0.0499997*x_3 - 0.5) + 1.12544) + 0.0456311*Abs(3.2*(11.3975*sqrt(0.12987*x_1 + 1) + 0.166284*Abs(3.4*x_2 - 4.4) + 2.59361*acos(0.0499997*x_3 - 0.5) - 16.6262)*(0.605486*cos(0.85*x_1 + 1.9) + 0.129938*Abs(3.55*x_2 - 4.65) + 8.27887*asin(0.0499997*x_3 - 0.5) + 5.78521) + 2.3) + 1.83762*asin(0.0181135*Abs(3.65*x_2 - 4.55) + 0.143987*asin(0.45*x_1 - 1.45) + 1.08366*atanh(0.0499997*x_3 - 0.4) + 0.0468976) + 4.13542 + 4.05098*exp(-44.8245*((1 - 0.65*x_2)**4 - 0.0572864*asin(0.4*x_1 - 1.35) + 0.380403*asin(0.0499997*x_3 - 0.5) + 0.286497)**2) + 0.188677*exp(-2.56*(-(1.52678*sin(0.35*x_1 - 1.05) + 2.90839*atanh(0.0499997*x_3 - 0.4) + 2.5186)*(7.27024*asin(0.0499997*x_3 - 0.5) + 7.80837 - 7.66703*exp(-0.64*(0.0625*x_1 - 1)**2)) - 0.25)**2)`
- icbr_refit_commit formula (display, rounded):
  - `14.9315*sqrt(-0.110665*(1 - 0.0401848*x_1)**(3/2) + 0.8766*atanh(0.00428*x_3 - 0.6262) + 1) - 0.316415*sin(-0.385656*Abs(1.47388*x_1 - 1.57996) + 0.387152*Abs(2.85676*x_2 - 3.57472) + 3.42899*asin(0.0779999*x_3 - 0.6018) + 6.78534) - 1.94862*tanh(10.1896*(1 - 0.658439*x_2)**4 + 2.60221*acos(0.6007 - 0.0779999*x_3) - 0.644579*asin(0.38404*x_1 - 1.27992) - 2.86507) - 0.476095*Abs(0.30608*(11.5292*sqrt(0.128157*x_1 + 1) + 0.2861*Abs(1.96516*x_2 - 2.55548) + 8.35681*acos(0.01356*x_3 - 0.60204) - 29.8609)*(-0.609928*cos(0.836*x_1 - 1.1999) + 0.184075*Abs(2.51484*x_2 - 3.32128) + 51.2175*atanh(0.00559999*x_3 - 0.60208) + 37.1714) - 4.6968) - 0.0717101*atan(4.46091*asin(0.0782399*x_3 - 0.60276) + 0.577549) + 2.26389*atanh(0.0178815*Abs(2.93752*x_2 - 3.64796) + 0.125621*asin(0.42416*x_1 - 1.39744) + 6.5226*atanh(0.00432*x_3 - 0.63284) + 4.56765) - 2.48717 + 0.1654*exp(-2.24089*(-(1.59203*sin(0.3342*x_1 - 0.99992) + 21.239*atanh(0.00424*x_3 - 0.65048) + 17.7959)*(54.6605*atanh(0.00432*x_3 - 0.6302) + 42.8431 - 5.17934*exp(-0.810468*(1 - 0.0821984*x_1)**2)) - 0.286688)**2)`

### task=feynman_I_10_7 seed=20

- Task source: feynman_file
- Target formula: `m_0/sqrt(1-v**2/c**2)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=2.941273e-03, r2=0.997939
- Variant formula overview:
  - icbr_full: symbolic_s=2.215626e+00, imitation_mse=8.918055e-04, target_mse=3.066737e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=1.505059e+00, imitation_mse=8.873385e-04, target_mse=3.066906e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=3.221333e+00, imitation_mse=8.918055e-04, target_mse=3.066737e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=3.892125e+00, imitation_mse=1.011688e-03, target_mse=3.070208e-03, formula_export_success=True
- icbr_full formula (display, rounded):
  - `-11.8622*(0.217598*cos(0.3*x_1 - 2.5) + asin(0.0499997*x_3 - 0.5) + 0.191944)**2 + 0.557627*sin(6.26901*tan(0.05*x_3 - 3.55) - 1.69552) + 0.119929*tan(0.25*(10.6835 - 5.15483*acos(0.0499997*x_3 - 0.5))*(-4.08447*tan(0.05*x_3 - 3.55) - 1.66433) - 1.6) - 1.20094*acos(-0.955057*tan(0.05*x_3 - 3.55) + 0.0289204*Abs(3.85*x_1 - 4.95) - 0.785215) + 7.3138*atanh(0.0499997*(-8.63671*sqrt(0.0707071*x_1 + 1) + 0.120022*cos(2.05*x_2 + 4.4) - 3.95914*tan(0.05*x_3 - 3.55) + 6.85081)*(-19.0955*sqrt(0.0883978*x_1 + 1) - 1.14975*tan(0.05*x_3 - 3.55) + 19.1382 - 0.0410897*exp(-14.8225*(1 - 0.74026*x_2)**2)) - 0.45) + 7.28555`
- icbr_no_replay formula (display, rounded):
  - `0.557627*sin(6.26901*tan(0.05*x_3 - 3.55) - 1.69552) - 2.08912*sin(3.49325*tan(0.05*x_3 - 3.55) - 2.83149 + 2.59157*exp(-(0.1*x_1 - 1.0)**2)) + 0.119929*tan(0.25*(-4.08447*tan(0.05*x_3 - 3.55) - 1.66433)*(5.1844*tan(0.05*x_3 - 3.55) + 2.11252) - 1.6) + 0.975135*tan(-1.22793*tan(0.05*x_3 - 3.55) + 0.0371834*Abs(3.85*x_1 - 4.95) + 2.48329) + 7.3138*atanh(0.0499997*(-8.63671*sqrt(0.0707071*x_1 + 1) + 0.120022*cos(2.05*x_2 + 4.4) - 3.95914*tan(0.05*x_3 - 3.55) + 6.85081)*(-19.0955*sqrt(0.0883978*x_1 + 1) - 1.14975*tan(0.05*x_3 - 3.55) + 0.0277589*Abs(2.65*x_2 - 3.55) + 19.0945) - 0.45) + 2.97957`
- icbr_no_shared formula (display, rounded):
  - `-11.8622*(0.217598*cos(0.3*x_1 - 2.5) + asin(0.0499997*x_3 - 0.5) + 0.191944)**2 + 0.557627*sin(6.26901*tan(0.05*x_3 - 3.55) - 1.69552) + 0.119929*tan(0.25*(10.6835 - 5.15483*acos(0.0499997*x_3 - 0.5))*(-4.08447*tan(0.05*x_3 - 3.55) - 1.66433) - 1.6) - 1.20094*acos(-0.955057*tan(0.05*x_3 - 3.55) + 0.0289204*Abs(3.85*x_1 - 4.95) - 0.785215) + 7.3138*atanh(0.0499997*(-8.63671*sqrt(0.0707071*x_1 + 1) + 0.120022*cos(2.05*x_2 + 4.4) - 3.95914*tan(0.05*x_3 - 3.55) + 6.85081)*(-19.0955*sqrt(0.0883978*x_1 + 1) - 1.14975*tan(0.05*x_3 - 3.55) + 19.1382 - 0.0410897*exp(-14.8225*(1 - 0.74026*x_2)**2)) - 0.45) + 7.28555`
- icbr_refit_commit formula (display, rounded):
  - `6.19444*sin(7.77254*tan(0.00763999*x_3 - 0.6026) + 9.32134) - 20.4765*cos(-0.682725*cos(0.0999999*x_1 - 4.99925) + 6.64384*atanh(0.00563999*x_3 - 0.60116) + 1.10856) - 1.48759*acos(-3.40394*tan(0.00771999*x_3 - 0.60152) + 0.0205474*Abs(3.9812*x_1 - 4.694) - 2.8524) + 32.6259*atanh(0.00803999*(-8.66669*sqrt(0.0704397*x_1 + 1) - 0.118364*sin(2.07296*x_2 + 2.8084) - 12.325*asin(0.014*x_3 - 0.6002) + 0.62835)*(-18.6583*sqrt(0.0907104*x_1 + 1) - 0.775866*asin(0.0739999*x_3 - 0.60162) + 18.7109 - 0.0448774*exp(-11.0089*(1 - 0.737634*x_2)**2)) - 0.605) + 12.5629 + 1.12628/(-2.07396*(-21.2514*tan(0.00619999*x_3 - 0.68716) - 17.3737)*(23.884*tan(0.00799999*x_3 - 0.60116) + 16.2957) + 0.3126)`

### task=feynman_I_12_1 seed=1

- Task source: feynman_file
- Target formula: `mu*Nn`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=2.104911e-03, r2=0.999916
- Variant formula overview:
  - icbr_full: symbolic_s=2.273242e+00, imitation_mse=3.066562e-02, target_mse=3.033241e-02, formula_export_success=True
  - icbr_no_replay: symbolic_s=1.547225e+00, imitation_mse=3.680226e-02, target_mse=3.612363e-02, formula_export_success=True
  - icbr_no_shared: symbolic_s=3.356429e+00, imitation_mse=3.068605e-02, target_mse=3.036558e-02, formula_export_success=True
  - icbr_refit_commit: symbolic_s=3.997624e+00, imitation_mse=nan, target_mse=nan, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0.527986*(15.8906*sqrt(0.111111*x_1 + 1) + 3.01417*asin(0.35*x_2 - 1.2) - 12.8817)*(1.84863*asin(0.3*x_1 - 1.05) + 0.813602*asin(0.4*x_2 - 1.4) + 2.93342) + 32.3279*sqrt(sqrt(0.0752688*x_2 + 1) - 0.242715 + 0.383182*exp(-(0.1*x_1 - 1.0)**2)) - 14.1071*(0.0487502*Abs(3.7*x_1 - 4.55) + 0.345934*acos(0.3*x_2 - 1.0) - 1)**4 + 1.08788*cos(0.27108*Abs(1.95*x_2 - 3.0) + 5.41426) - 0.901452*cos(-14.4453*sqrt(0.07*x_1 + 1) + 1.25241*acos(0.35*x_2 - 1.2) + 13.5788) - 31.7838 - 1.92982*exp(-10.195*(-0.095644*Abs(2.9*x_1 - 3.95) + 0.0576564*Abs(3.3*x_2 - 4.35) + 1)**2)`
- icbr_no_replay formula (display, rounded):
  - `-0.379346*(0.314324*Abs(1.95*x_2 - 3.0) - 1)**2 - 0.000222728*(-Abs(2.9*x_1 - 3.95) + 0.602823*Abs(3.3*x_2 - 4.35) - 0.138344)**4 + 0.527986*(-2.43659*acos(0.3*x_1 - 1.0) + 3.01417*asin(0.35*x_2 - 1.2) + 9.53476)*(1.84863*asin(0.3*x_1 - 1.05) + 0.813602*asin(0.4*x_2 - 1.4) + 2.93342) + 33.3322*log(2.51801*sqrt(0.0752688*x_2 + 1) + 2.06384 + 0.964855*exp(-(0.1*x_1 - 1.0)**2)) - 0.901452*cos(14.4453*sqrt(0.07*x_1 + 1) + 1.25241*asin(0.35*x_2 - 1.2) - 15.5461) - 53.2974 - 1.56252*exp(-4.45295*(0.140924*Abs(3.7*x_1 - 4.55) - asin(0.3*x_2 - 1.0) + 0.455019)**2)`
- icbr_no_shared formula (display, rounded):
  - `0.527986*(15.8906*sqrt(0.111111*x_1 + 1) + 3.01417*asin(0.35*x_2 - 1.2) - 12.8817)*(1.84863*asin(0.3*x_1 - 1.05) + 0.813602*asin(0.4*x_2 - 1.4) + 2.93342) + 32.2544*sqrt(sqrt(0.0752688*x_2 + 1) - 0.247679 + 0.383182*exp(-(0.1*x_1 - 1.0)**2)) - 0.612548*(0.101332*Abs(3.9*x_1 - 4.8) - 0.757823*asin(0.3*x_2 - 1.0) - 1)**4 + 1.08788*cos(0.27108*Abs(1.95*x_2 - 3.0) + 5.41426) - 0.901452*cos(14.4453*sqrt(0.07*x_1 + 1) + 1.25241*asin(0.35*x_2 - 1.2) - 15.5461) - 31.6303 - 1.92982*exp(-10.195*(-0.095644*Abs(2.9*x_1 - 3.95) + 0.0576564*Abs(3.3*x_2 - 4.35) + 1)**2)`
- icbr_refit_commit formula (display, rounded):
  - `0.527857*(15.8155*sqrt(0.111713*x_1 + 1) + 2.87698*asin(0.36632*x_2 - 1.22132) - 12.9153)*(9.1883*sqrt(0.153818*x_1 + 1) + 0.77339*acos(1.424 - 0.42116*x_2) - 9.71081) + 32.7076*sqrt(sqrt(0.0737737*x_2 + 1) - 0.345239 + 0.519163*exp(-0.811045*(1 - 0.0799484*x_1)**2)) - 267.72*(0.101124*Abs(0.76352*x_1 - 0.87328) - asin(0.03432*x_2 - 0.7852) - 0.960526)**4 - 10.3433*sin(3.76761*sqrt(0.0722301*x_1 + 1) + 0.304206*acos(1.27592 - 0.38216*x_2) - 2.97838) - 1.08194*cos(0.203669*Abs(2.59348*x_2 - 4.09164) - 3.99568) - 22.4836 - 3.55699*exp(-7.38616*(-0.503489*Abs(0.41088*x_1 - 0.51468) + 0.037781*Abs(3.77136*x_2 - 4.65344) + 1)**2)`

### task=feynman_I_12_1 seed=2

- Task source: feynman_file
- Target formula: `mu*Nn`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=2.802466e-02, r2=0.998943
- Variant formula overview:
  - icbr_full: symbolic_s=2.648083e+00, imitation_mse=1.815900e-01, target_mse=2.011948e-01, formula_export_success=True
  - icbr_no_replay: symbolic_s=1.744832e+00, imitation_mse=2.347440e-01, target_mse=2.650733e-01, formula_export_success=True
  - icbr_no_shared: symbolic_s=3.856414e+00, imitation_mse=1.815899e-01, target_mse=2.011947e-01, formula_export_success=True
  - icbr_refit_commit: symbolic_s=4.724439e+00, imitation_mse=2.348877e-01, target_mse=2.588587e-01, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0.0643238*(tan(0.6*x_1 + 4.35) + 0.249684)**2 + 0.464707*tanh(0.211693*tan(0.25*x_1 - 1.8) - 1.1356*atanh(0.45*x_2 - 1.45) + 1.47001) + 0.171184*Abs(4.1*(3.5773*tan(0.3*x_2 - 1.0) + 2.56421*asin(0.05*x_1 - 1.05) + 7.12083)*(-0.835625*acos(0.3*x_2 - 1.3) + 2.09236*atanh(0.3*x_1 - 1.0) + 4.41527) + 1.55) + 0.117126*Abs(61.4211*(1 - 0.032967*x_2)**(3/2) - 55.9324) + 0.159442*Abs(-0.948839*Abs(3.3*x_1 - 3.75) + 0.672211 + 1.17761*exp(-1.5625*(1 - 0.52*x_2)**2)) + 0.414073 - 1.35026*exp(-3.32105*(sin(0.4*x_1 + 1.85) + 0.800249*sign(4.5 - 3.95*x_2) - 0.416307)**2) - 0.471687/(-(-1.11257*atanh(0.4*x_2 - 1.4) - 1.69503)*(-0.0443123*Abs(4.4*x_1 - 4.825) + 1.31524*atanh(0.4*x_2 - 1.4) + 1.84843) + 0.9)**4`
- icbr_no_replay formula (display, rounded):
  - `-0.665837*cos(-0.195469*Abs(3.95*x_1 - 4.95) + 1.62039*sign(4.5 - 3.95*x_2) + 6.68331) - 0.455536*tanh(3.28154*atanh(0.4*x_1 - 1.4) + 5.75998) + 0.171184*Abs(4.1*(1.55622*asin(0.4*x_1 - 1.35) + 0.590917*atanh(0.4*x_2 - 1.35) + 2.87934)*(3.70727*asin(0.3*x_2 - 1.05) + 0.534639*atanh(0.45*x_1 - 1.45) + 4.46976) + 1.55) + 0.159442*Abs(0.948839*Abs(3.3*x_1 - 3.75) + 0.178435*Abs(2.45*x_2 - 4.35) - 1.91582) + 2.08228 - 1.29825*exp(-6.37363*(0.0821749*tan(0.25*x_1 - 1.8) - 0.440817*atanh(0.45*x_2 - 1.45) + 1)**2) - 1.13408*exp(-79.0302*(0.912341 - (1 - 0.032967*x_2)**(3/2))**2) - 0.142145/(-(-0.58406*tan(0.6*x_2 + 4.3) - 1.60031)*(0.691467*tan(0.6*x_2 + 4.3) - 0.0443123*Abs(4.4*x_1 - 4.825) + 1.73698) + 0.446809)**2`
- icbr_no_shared formula (display, rounded):
  - `0.0643238*(tan(0.6*x_1 + 4.35) + 0.249684)**2 + 0.701854*(-3.5773*tan(0.3*x_2 - 1.0) - 2.56421*asin(0.05*x_1 - 1.05) - 7.12083)*(0.835625*acos(0.3*x_2 - 1.3) - 2.09236*atanh(0.3*x_1 - 1.0) - 4.41527) + 0.464707*tanh(0.211693*tan(0.25*x_1 - 1.8) - 1.1356*atanh(0.45*x_2 - 1.45) + 1.47001) + 0.117126*Abs(61.4211*(1 - 0.032967*x_2)**(3/2) - 55.9324) + 0.159442*Abs(-0.948839*Abs(3.3*x_1 - 3.75) + 0.672211 + 1.17761*exp(-1.5625*(1 - 0.52*x_2)**2)) + 0.679408 - 1.35026*exp(-3.32105*(sin(0.4*x_1 + 1.85) + 0.800249*sign(4.5 - 3.95*x_2) - 0.416307)**2) - 0.471687/(-(-1.11257*atanh(0.4*x_2 - 1.4) - 1.69503)*(-0.0443123*Abs(4.4*x_1 - 4.825) + 1.31524*atanh(0.4*x_2 - 1.4) + 1.84843) + 0.9)**4`
- icbr_refit_commit formula (display, rounded):
  - `0.275417*(tan(0.34064*x_1 - 4.56216) + 0.500646)**2 - 0.464707*tanh(-0.0887637*tan(0.11404*x_1 - 4.81828) + 1.61112*atanh(0.00124*x_2 - 1.00124) + 3.97434) + 0.140931*Abs(4.98*(0.833939*acos(1.30088 - 0.3008*x_2) + 2.09011*atanh(0.30028*x_1 - 1.00068) + 1.79)*(2.56635*asin(0.0499199*x_1 - 1.04992) + 2.96526*asin(0.36628*x_2 - 1.21992) + 7.12035) + 4.9985) + 0.146156*Abs(116.6*sqrt(0.0412989*x_2 + 1) - 120.884) + 0.587875*Abs(-0.657367*Abs(1.25868*x_1 - 1.35492) + 0.128283 + 0.339336*exp(-0.990662*(1 - 0.529197*x_2)**2)) - 0.029648 - 1.35014*exp(-3.31741*(-sin(0.4*x_1 + 4.99997) + 0.67579*sign(4.99862 - 4.4*x_2) - 0.521657)**2) - 0.471391/(-(-0.929032*log(1.0*x_2 - 0.908) - 0.887436)*(-0.0822129*Abs(2.36904*x_1 - 2.56068) + 1.75735*atanh(0.21*x_2 - 1.20048) + 2.80408) + 0.899869)**4`

### task=feynman_I_12_1 seed=3

- Task source: feynman_file
- Target formula: `mu*Nn`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=3.628120e-03, r2=0.999860
- Variant formula overview:
  - icbr_full: symbolic_s=2.529936e+00, imitation_mse=1.294834e-02, target_mse=1.267620e-02, formula_export_success=True
  - icbr_no_replay: symbolic_s=1.701540e+00, imitation_mse=1.685602e-02, target_mse=1.698817e-02, formula_export_success=True
  - icbr_no_shared: symbolic_s=3.623401e+00, imitation_mse=1.294525e-02, target_mse=1.267203e-02, formula_export_success=True
  - icbr_refit_commit: symbolic_s=4.435230e+00, imitation_mse=1.152982e-02, target_mse=1.300690e-02, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0.571949*(-26.5652*(1 - 0.0333333*x_2)**(3/2) - 0.107462*acos(0.4*x_1 - 1.3) + 26.3227)*(-0.946102*acos(0.35*x_2 - 1.35) - 1.63494 + 11.2371*exp(-(0.1*x_1 - 1.0)**2)) + 0.291418*sin(5.38921 - 1.53214*exp(-2.89*(1 - 0.470588*x_1)**2)) - 2.78052*cos(0.3*(-6.42134*log(0.2*x_1 + 4.775) + 8.21371 + 5.04897*exp(-(0.1*x_2 - 1.0)**2))*(0.218625*Abs(2.85*x_2 - 3.95) + 2.8533 - 5.69282*exp(-(0.1*x_1 - 1.0)**2)) - 2.3) + 2.18749*cos(0.0104005*Abs(3.25*x_2 - 4.625) - 1.58197 + 9.43215*exp(-0.64*(0.0625*x_1 - 1)**2)) + 0.770716*cos(-0.192038*Abs(3.75*x_2 - 4.3) + 2.73879 + 0.988294*exp(-(0.1*x_1 - 1.0)**2)) - 0.10419*Abs(-25.6847*log(0.15*x_1 + 4.8) + 1.18096*Abs(3.25*x_2 - 4.35) + 40.0831) + 1.5709`
- icbr_no_replay formula (display, rounded):
  - `0.571949*(-26.5652*(1 - 0.0333333*x_2)**(3/2) + 0.107462*asin(0.4*x_1 - 1.3) + 26.1539)*(0.754346*atanh(0.4*x_2 - 1.35) - 3.28902 + 11.2371*exp(-(0.1*x_1 - 1.0)**2)) + 0.770716*cos(0.0188631*Abs(4.45*x_1 - 5.0) - 0.192038*Abs(3.75*x_2 - 4.3) + 3.18619) - 0.10419*Abs(-23.0554*sqrt(0.07*x_1 + 1) + 1.18096*Abs(3.25*x_2 - 4.35) + 22.8527) + 0.212579*Abs(0.101034*Abs(3.25*x_2 - 4.625) - 53.2177 + 91.6266*exp(-0.64*(0.0625*x_1 - 1)**2)) - 3.9471 + 6.50595*exp(-0.1225*(0.428572*(-5.57893*sqrt(0.0972973*x_1 + 1) + 3.75557 + 5.04897*exp(-(0.1*x_2 - 1.0)**2))*(0.218625*Abs(2.85*x_2 - 3.95) + 2.8533 - 5.69282*exp(-(0.1*x_1 - 1.0)**2)) + 1)**2) - 0.424514*exp(-2.34745*(-0.482467 + exp(-2.89*(1 - 0.470588*x_1)**2))**2)`
- icbr_no_shared formula (display, rounded):
  - `0.571948*(-26.5652*(1 - 0.0333333*x_2)**(3/2) - 0.107462*acos(0.4*x_1 - 1.3) + 26.3227)*(-0.946102*acos(0.35*x_2 - 1.35) - 1.63494 + 11.2371*exp(-(0.1*x_1 - 1.0)**2)) + 0.291418*sin(5.38921 - 1.53214*exp(-2.89*(1 - 0.470588*x_1)**2)) - 2.78052*cos(0.3*(-6.42134*log(0.2*x_1 + 4.775) + 8.21371 + 5.04897*exp(-(0.1*x_2 - 1.0)**2))*(0.218625*Abs(2.85*x_2 - 3.95) + 2.8533 - 5.69282*exp(-(0.1*x_1 - 1.0)**2)) - 2.3) + 2.18749*cos(0.0104005*Abs(3.25*x_2 - 4.625) - 1.58197 + 9.43215*exp(-0.64*(0.0625*x_1 - 1)**2)) + 0.770716*cos(-0.192038*Abs(3.75*x_2 - 4.3) + 2.73879 + 0.988294*exp(-(0.1*x_1 - 1.0)**2)) - 0.10419*Abs(-24.1105*sqrt(0.0666667*x_1 + 1) + 1.18096*Abs(3.25*x_2 - 4.35) + 23.904) + 1.5709`
- icbr_refit_commit formula (display, rounded):
  - `0.571835*(-25.8577*(1 - 0.0343012*x_2)**(3/2) + 0.112813*asin(0.38204*x_1 - 1.275) + 25.4478)*(-0.946927*acos(0.34968*x_2 - 1.34956) - 4.45582 + 15.5029*exp(-0.810144*(1 - 0.0799928*x_1)**2)) - 0.29414*sin(0.743946 + 1.59918*exp(-2.19016*(1 - 0.457106*x_1)**2)) - 2.78966*cos(0.3012*(-6.34261*log(0.1966*x_1 + 4.62924) + 0.304115*Abs(1.4038*x_2 - 1.50388) + 10.1624)*(0.19006*Abs(3.21144*x_2 - 4.21956) + 4.17865 - 7.65048*exp(-0.81018*(1 - 0.082213*x_1)**2)) - 2.32312) - 2.25495*cos(0.0117528*Abs(2.7218*x_2 - 3.728) - 2.42427 + 6.15356*exp(-0.810144*(1 - 0.0822148*x_1)**2)) - 0.696414*cos(0.228063*Abs(3.6478*x_2 - 3.95472) + 0.272275 - 1.14479*exp(-1.00368*(1 - 0.100096*x_1)**2)) + 0.156091 + 1.19218*exp(-13.0867*(0.889526*log(0.0978399*x_1 + 3.12656) - 0.0472991*Abs(2.76504*x_2 - 3.48592) - 1)**2)`

### task=feynman_I_12_1 seed=4

- Task source: feynman_file
- Target formula: `mu*Nn`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=False; reason=`teacher_test_mse=0.300906 > 0.1`
- Teacher target metrics (against dataset test_label): mse=nan, r2=nan
- Variant formula overview:
  - icbr_full: symbolic_s=nan, imitation_mse=nan, target_mse=nan, formula_export_success=False
  - icbr_no_replay: symbolic_s=nan, imitation_mse=nan, target_mse=nan, formula_export_success=False
  - icbr_no_shared: symbolic_s=nan, imitation_mse=nan, target_mse=nan, formula_export_success=False
  - icbr_refit_commit: symbolic_s=nan, imitation_mse=nan, target_mse=nan, formula_export_success=False
- icbr_full formula (display, rounded):
  - `<none>`
- icbr_full formula export error: skipped_by_teacher_quality_gate: teacher_test_mse=0.300906 > 0.1
- icbr_no_replay formula (display, rounded):
  - `<none>`
- icbr_no_replay formula export error: skipped_by_teacher_quality_gate: teacher_test_mse=0.300906 > 0.1
- icbr_no_shared formula (display, rounded):
  - `<none>`
- icbr_no_shared formula export error: skipped_by_teacher_quality_gate: teacher_test_mse=0.300906 > 0.1
- icbr_refit_commit formula (display, rounded):
  - `<none>`
- icbr_refit_commit formula export error: skipped_by_teacher_quality_gate: teacher_test_mse=0.300906 > 0.1

### task=feynman_I_12_1 seed=5

- Task source: feynman_file
- Target formula: `mu*Nn`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=2.414070e-02, r2=0.999077
- Variant formula overview:
  - icbr_full: symbolic_s=3.058801e+00, imitation_mse=7.712198e-01, target_mse=8.325033e-01, formula_export_success=True
  - icbr_no_replay: symbolic_s=1.960295e+00, imitation_mse=1.137263e+00, target_mse=1.228027e+00, formula_export_success=True
  - icbr_no_shared: symbolic_s=4.400838e+00, imitation_mse=7.744331e-01, target_mse=8.357081e-01, formula_export_success=True
  - icbr_refit_commit: symbolic_s=5.285629e+00, imitation_mse=9.635945e-01, target_mse=1.037796e+00, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0.722607*sin(1.06364*log(1.5*x_2 - 1.45) + 5.10273 + 24.9997*exp(-25.0*(0.72 - x_1)**2)) + 23.3463*asin(1.88546*sqrt(0.0505051*x_1 + 1) + 0.0143731*Abs(4.5*x_2 - 4.875) - 2.40782) - 10.799*atan(0.85*(0.995687*sqrt(x_2 - 1) - 1.17661 + 0.44586*exp(-1.96*(1 - 0.5*x_1)**2))*(0.0805111*Abs(3.35*x_2 - 4.9) + 1.16476*acos(0.4*x_1 - 1.4) - 3.11518) + 2.0) + 26.3542 + 3.19966*exp(-0.967975*(0.910022*asin(0.35*x_1 - 1.35) - 0.945169 + (0.409091 - x_2)**(-5))**2) - 3.39094*exp(-7.0225*((-0.107473*sin(0.4*x_2 - 1.3) - 0.0917327*sign(3.75 - 3.2*x_1) - 0.269237)*(2.31201*cos(0.3*x_1 - 2.5) - 0.0876135*Abs(2.8*x_2 - 4.35) + 1.55327) - 0.169811)**2) - 1.18412/(0.111355*Abs(3.35*x_2 - 4.825) - 2.00614 - 1.28117/(x_1 - 0.342105)**5) - 0.383517/(5.45345*tanh(4.8*x_1 - 5.0) + 2.3267*sign(4.0 - 3.45*x_2) - 3.77611)`
- icbr_no_replay formula (display, rounded):
  - `23.5641*tan(1.88547*sqrt(0.0505051*x_1 + 1) + 0.0143732*Abs(4.5*x_2 - 4.875) + 0.842165) + 0.231972*tan(0.031985*Abs(3.35*x_2 - 4.825) + 4.14803 - 2.54099*exp(-25.0*(0.98 - x_1)**2)) + 8.85196 - 1.42257*exp(-324.831*(0.0601538*atanh(0.35*x_2 - 1.35) + 0.0767033 + exp(-25.0*(0.72 - x_1)**2))**2) + 3.19966*exp(-167.805*(0.0550623*atanh(0.4*x_1 - 1.35) - 0.0908497 - exp(-18.9225*(0.91954 - x_2)**2))**2) + 1.56551*exp(-129.195*(-0.0801758 - 0.665521*exp(-25.0*(0.99 - x_1)**2) + exp(-25.0*(0.93 - x_2)**2))**2) - 3.39094*exp(-7.0225*((-0.0876135*Abs(2.8*x_2 - 4.35) - 3.36148 + 7.92189*exp(-(0.1*x_1 - 1.0)**2))*(-0.0107474*Abs(3.8*x_2 - 4.7) - 0.0917327*sign(3.75 - 3.2*x_1) - 0.187086) - 0.169811)**2) + 3.69644/(0.166667*(-0.0677704*Abs(2.6*x_1 - 4.95) + 0.708962*atanh(0.4*x_2 - 1.4) + 0.835183)*(0.0805111*Abs(3.35*x_2 - 4.9) - 1.16476*asin(0.4*x_1 - 1.4) - 1.28558) + 1)**3`
- icbr_no_shared formula (display, rounded):
  - `0.722607*sin(1.0476*log(2.0*x_2 - 1.95) + 4.82517 + 24.9997*exp(-25.0*(x_1 - 0.72)**2)) + 23.3463*asin(-0.788915*(1 - 0.04*x_1)**(3/2) + 0.0143731*Abs(4.5*x_2 - 4.875) + 0.26672) - 10.799*atan(0.85*(0.995687*sqrt(x_2 - 1) - 1.17661 + 0.44586*exp(-1.96*(1 - 0.5*x_1)**2))*(0.0817181*Abs(3.3*x_2 - 4.825) - 1.16476*asin(0.4*x_1 - 1.4) - 1.28562) + 2.0) + 26.3542 + 3.19966*exp(-0.967975*(0.910022*asin(0.35*x_1 - 1.35) - 0.945169 + (0.409091 - x_2)**(-5))**2) - 3.39094*exp(-7.0225*((2.31201*cos(0.3*x_1 - 2.5) - 0.0876135*Abs(2.8*x_2 - 4.35) + 1.55327)*(0.0970141*cos(0.45*x_2 + 0.15) - 0.0917327*sign(3.75 - 3.2*x_1) - 0.2656) - 0.169811)**2) - 1.18412/(0.111355*Abs(3.35*x_2 - 4.825) - 2.00614 - 1.28117/(x_1 - 0.342105)**5) - 0.383517/(5.45345*tanh(4.8*x_1 - 5.0) + 2.3267*sign(4.0 - 3.45*x_2) - 3.77611)`
- icbr_refit_commit formula (display, rounded):
  - `-0.721114*sin(1.0723*log(2.938*x_2 - 2.84044) - 5.05444 + 98.7049*exp(-17.0239*(0.557635 - x_1)**2)) + 41.6216*asin(1.02961*sqrt(0.0479351*x_1 + 1) + 0.0888776*Abs(0.37788*x_2 + 1.09176) - 1.74906) - 9.46922*atan(0.77564*(0.995784*sqrt(x_2 - 0.999844) - 1.211 + 0.465787*exp(-1.60357*(1 - 0.49084*x_1)**2))*(0.0999766*Abs(2.62112*x_2 - 3.63232) + 1.11532*acos(0.41908*x_1 - 1.41964) - 2.98236) + 1.72944) + 37.2347 + 392.956*exp(-5.54057*(0.0950816*asin(0.35052*x_1 - 1.3506) - 1 + 0.104227/(0.409589 - x_2)**5)**2) - 3.68451*exp(-5.45185*(-(2.31648*cos(0.29936*x_1 - 2.49664) - 0.119062*Abs(2.062*x_2 - 3.2989) + 1.54254)*(-0.10755*cos(0.39964*x_2 + 3.41424) - 0.069146*sign(4.466 - 3.716*x_1) - 0.248134) + 0.213866)**2) - 1.76635/(0.124388*Abs(2.86972*x_2 - 3.89732) - 2.27124 + 1.2559/(0.342422 - x_1)**5) - 0.389465/(4.97966*tanh(4.8*x_1 - 4.99999) + 2.13087*sign(4.89784 - 4.18612*x_2) - 3.5203)`

### task=feynman_I_12_1 seed=6

- Task source: feynman_file
- Target formula: `mu*Nn`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=6.698473e-03, r2=0.999732
- Variant formula overview:
  - icbr_full: symbolic_s=2.298317e+00, imitation_mse=2.234508e-02, target_mse=2.765743e-02, formula_export_success=True
  - icbr_no_replay: symbolic_s=1.497987e+00, imitation_mse=2.414441e-02, target_mse=3.018217e-02, formula_export_success=True
  - icbr_no_shared: symbolic_s=3.304671e+00, imitation_mse=2.249457e-02, target_mse=2.761970e-02, formula_export_success=True
  - icbr_refit_commit: symbolic_s=4.073362e+00, imitation_mse=nan, target_mse=nan, formula_export_success=True
- icbr_full formula (display, rounded):
  - `-1.82502*(-(-0.19164*log(2.0*x_1 - 1.95) - 0.135636*Abs(1.75*x_2 - 3.05) - 0.359719)*(0.164742*atanh(0.45*x_1 - 1.45) - 0.203567*atanh(0.3*x_2 - 1.3) - 0.0483052) - 0.723077)**4 + 28.1707*(0.00138979*Abs(3.55*x_2 - 4.6) + 0.0203367*asin(0.4*x_1 - 1.4) + 1)**(3/2) + 1.68398*sin(-1.008*sin(0.4*x_1 - 1.25) + 0.285262*Abs(1.85*x_2 - 2.75) + 1.57583) + 0.176111*Abs(3.4*(22.4106*sqrt(0.0913706*x_2 + 1) - 22.8988)*(9.67363*sqrt(0.136986*x_2 + 1) - 27.8658 + 32.8784*exp(-0.64*(0.0625*x_1 - 1)**2)) - 3.45) - 26.7991 - 0.361468*exp(-0.306299*(-0.279291*tan(0.2*x_1 - 1.75) - 1)**2) + 0.615616/(0.101661*Abs(3.15*x_2 - 4.2) + 1.36404)`
- icbr_no_replay formula (display, rounded):
  - `-1.82502*(-(-0.135636*Abs(1.75*x_2 - 3.05) - 0.288442*atanh(0.3*x_1 - 1.3) - 0.735444)*(0.164742*atanh(0.45*x_1 - 1.45) - 0.203567*atanh(0.3*x_2 - 1.3) - 0.0483052) - 0.723077)**4 + 28.1707*(0.00138979*Abs(3.55*x_2 - 4.6) + 0.0203367*asin(0.4*x_1 - 1.4) + 1)**(3/2) + 1.68398*sin(-0.156472*Abs(2.45*x_1 - 3.0) + 0.285262*Abs(1.85*x_2 - 2.75) + 2.30569) + 0.176111*Abs(3.4*(22.4106*sqrt(0.0913706*x_2 + 1) - 22.8988)*(1.77818*asin(0.3*x_2 - 1.0) - 16.2021 + 32.8784*exp(-0.64*(0.0625*x_1 - 1)**2)) - 3.45) - 26.7142 - 0.361468*exp(-0.306299*(-0.279291*tan(0.2*x_1 - 1.75) - 1)**2) + 0.366227/(-0.0451519*Abs(3.15*x_2 - 4.2) - 1)**2`
- icbr_no_shared formula (display, rounded):
  - `-1.82502*(-(-0.184803*log(5.0*x_1 - 4.95) - 0.135636*Abs(1.75*x_2 - 3.05) - 0.201671)*(0.164742*atanh(0.45*x_1 - 1.45) - 0.203567*atanh(0.3*x_2 - 1.3) - 0.0483052) - 0.723077)**4 + 29.5313*(0.00134676*Abs(3.55*x_2 - 4.6) - 0.0197072*acos(0.4*x_1 - 1.4) + 1)**(3/2) + 1.68398*sin(-1.008*sin(0.4*x_1 - 1.25) + 0.285262*Abs(1.85*x_2 - 2.75) + 1.57583) + 0.176111*Abs(3.4*(22.4106*sqrt(0.0913706*x_2 + 1) - 22.8988)*(9.78747*sqrt(0.135135*x_2 + 1) - 27.9783 + 32.8784*exp(-0.64*(0.0625*x_1 - 1)**2)) - 3.45) - 26.7991 - 0.361468*exp(-0.306299*(-0.279291*tan(0.2*x_1 - 1.75) - 1)**2) + 0.615616/(0.101661*Abs(3.15*x_2 - 4.2) + 1.36404)`
- icbr_refit_commit formula (display, rounded):
  - `-2.06022*(-(-0.155769*tan(0.5*x_1 - 4.99998) - 0.128606*Abs(1.87908*x_2 - 3.46192) - 0.686148)*(0.280946*atanh(0.27872*x_1 - 1.1742) - 0.232417*atanh(0.206*x_2 - 1.2) - 0.0323543) - 0.690113)**4 + 142.757*(0.000269102*Abs(3.56884*x_2 - 4.38488) + 0.00382423*asin(0.42116*x_1 - 1.42192) + 1)**(3/2) + 1.79802*cos(0.922773*sin(0.39996*x_1 - 4.39136) + 0.13328*Abs(3.46072*x_2 - 4.67868) + 0.0600362) - 5.98485*Abs(0.0999999*(22.4496*sqrt(0.091193*x_2 + 1) - 22.9376)*(99.9056*sqrt(0.0291072*x_1 + 1) + 9.62614*sqrt(0.137773*x_2 + 1) - 110.445) - 3.58352) - 121.06 + 0.639856*exp(-2.72351*(1 - 0.0816938*tan(0.2*x_1 + 1.38764))**2) + 0.956617/(0.169356*Abs(2.88304*x_2 - 3.57712) + 2.09927)`

### task=feynman_I_12_1 seed=7

- Task source: feynman_file
- Target formula: `mu*Nn`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=2.975251e-02, r2=0.998820
- Variant formula overview:
  - icbr_full: symbolic_s=3.018938e+00, imitation_mse=6.107330e-02, target_mse=8.171619e-02, formula_export_success=True
  - icbr_no_replay: symbolic_s=1.970196e+00, imitation_mse=6.903938e-02, target_mse=8.737220e-02, formula_export_success=True
  - icbr_no_shared: symbolic_s=4.395572e+00, imitation_mse=6.107245e-02, target_mse=8.167890e-02, formula_export_success=True
  - icbr_refit_commit: symbolic_s=5.323933e+00, imitation_mse=6.302927e-02, target_mse=8.644527e-02, formula_export_success=True
- icbr_full formula (display, rounded):
  - `1.32186*(-0.0967742*(15.757*(1 - 0.0333333*x_1)**(3/2) + 36.3094*log(0.15*x_2 + 4.575) - 71.1879)*(-5.80814*log(0.2*x_1 + 5.0) + 0.162338*Abs(2.5*x_2 - 4.05) + 9.95847) - 1)**3 + 0.614856*(-21.6451*sqrt(0.0618557*x_1 + 1) - 1.48412*atanh(0.4*x_2 - 1.35) + 19.8592)*(-4.12943*sqrt(0.142857*x_1 + 1) + 2.06872*acos(0.4*x_2 - 1.35) - 1.68142) + 54.1672*log(0.0290822*x_2 + 2.46869*log(0.1*x_1 + 4.8) + 0.596495) - 0.234875*sin(0.310468*Abs(2.25*x_1 - 3.85) + 1.43845*acos(0.45*x_2 - 1.45) + 0.104303) + 0.122391*Abs(0.564593*Abs(4.4*x_1 - 4.925) - 23.7448 + 38.151*exp(-0.64*(0.0625*x_2 - 1)**2)) - 80.4878 - 0.819817*exp(-2.6548*(0.107686*Abs(2.25*x_1 - 3.1) - sign(4.5 - 3.9*x_2) - 0.749905)**2) + 0.556093*exp(-68.3709*(-0.0503415*Abs(2.15*x_1 - 2.55) - 0.462091*acos(0.3*x_2 - 1.05) + 1)**2)`
- icbr_no_replay formula (display, rounded):
  - `0.423905*cos(-0.261048*Abs(2.25*x_1 - 3.1) + 2.42416*sign(4.5 - 3.9*x_2) + 4.70204) + 0.175723*Abs(3.5*(21.6451*sqrt(0.0618557*x_1 + 1) + 1.48412*atanh(0.4*x_2 - 1.35) - 19.8592)*(-2.06872*acos(0.4*x_2 - 1.35) + 0.779429*asin(0.3*x_1 - 1.05) + 6.73496) - 0.0999997) + 0.175108*Abs(-68.088*(1 - 0.032967*x_1)**(3/2) + 53.5449 + 22.7422*exp(-(0.1*x_2 - 1.0)**2)) - 0.100349*Abs(0.530068*Abs(2.25*x_1 - 3.85) + 2.45589*acos(0.45*x_2 - 1.45) - 7.99753) + 0.122391*Abs(0.564593*Abs(4.4*x_1 - 4.925) - 23.7448 + 38.151*exp(-0.64*(0.0625*x_2 - 1)**2)) - 2.58119*atan(0.35*(15.757*(1 - 0.0333333*x_1)**(3/2) + 31.8725*sqrt(0.0752688*x_2 + 1) - 47.8564)*(-5.12244*sqrt(0.0913706*x_1 + 1) + 0.162338*Abs(2.5*x_2 - 4.05) + 5.7344) - 1.5) - 2.21049 + 0.556093*exp(-14.5991*(-0.108943*Abs(2.15*x_1 - 2.55) + asin(0.3*x_2 - 1.05) + 0.593278)**2)`
- icbr_no_shared formula (display, rounded):
  - `1.32186*(-0.0967742*(15.8396*(1 - 0.0331492*x_1)**(3/2) + 36.3094*log(0.15*x_2 + 4.575) - 71.2709)*(-5.80814*log(0.2*x_1 + 5.0) + 0.162338*Abs(2.5*x_2 - 4.05) + 9.95847) - 1)**3 + 0.614856*(10.0187*(1 - 0.043956*x_1)**(3/2) - 1.48412*atanh(0.4*x_2 - 1.35) - 11.8122)*(-4.12943*sqrt(0.142857*x_1 + 1) + 2.06872*acos(0.4*x_2 - 1.35) - 1.68142) + 54.1672*log(0.0290822*x_2 + 2.46869*log(0.1*x_1 + 4.8) + 0.596495) - 0.234875*sin(0.310468*Abs(2.25*x_1 - 3.85) + 1.43845*acos(0.45*x_2 - 1.45) + 0.104303) + 0.122391*Abs(0.564593*Abs(4.4*x_1 - 4.925) - 23.7448 + 38.151*exp(-0.64*(0.0625*x_2 - 1)**2)) - 80.4878 - 0.819817*exp(-2.6548*(0.107686*Abs(2.25*x_1 - 3.1) - sign(4.5 - 3.9*x_2) - 0.749905)**2) + 0.556093*exp(-68.3709*(-0.0503415*Abs(2.15*x_1 - 2.55) - 0.462091*acos(0.3*x_2 - 1.05) + 1)**2)`
- icbr_refit_commit formula (display, rounded):
  - `1.26096*(-0.100001*(-35.4987*sqrt(0.044825*x_1 + 1) + 36.6329*log(0.0946399*x_2 + 2.91472) - 3.90013)*(-5.14734*sqrt(0.0908767*x_1 + 1) + 0.229372*Abs(1.75412*x_2 - 2.8868) + 5.77149) - 1)**3 + 0.614864*(-20.5747*sqrt(0.0653566*x_1 + 1) - 1.97577*atanh(0.31436*x_2 - 1.18276) + 18.5282)*(-4.10793*sqrt(0.143733*x_1 + 1) + 2.20038*acos(0.38324*x_2 - 1.27828) - 1.86937) + 0.23484*sin(-0.36206*Abs(1.95036*x_1 - 3.48732) + 1.55345*acos(1.39576 - 0.42328*x_2) + 1.51139) + 0.114183*Abs(8.01708*sin(0.34*x_1 + 2.10142) + 9.83692 - 25.7886*exp(-0.81054*(1 - 0.0866377*x_2)**2)) - 2.59377 + 0.71993*exp(-355.164*(-0.00483911*Abs(3.64168*x_1 - 4.02912) - 0.421911*acos(0.042*x_2 - 0.79936) + 1)**2) - 0.8194*exp(-1.97893*(0.284946*Abs(0.97116*x_1 - 1.29964) - sign(4.9982 - 4.392*x_2) - 0.727817)**2) + 8.97666*exp(-49.4219*(-0.00628798*x_2 - 0.547345*log(0.0960399*x_1 + 4.73448) + 1)**2)`

### task=feynman_I_12_1 seed=8

- Task source: feynman_file
- Target formula: `mu*Nn`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.698283e-02, r2=0.999360
- Variant formula overview:
  - icbr_full: symbolic_s=2.524306e+00, imitation_mse=5.606720e-01, target_mse=5.548102e-01, formula_export_success=True
  - icbr_no_replay: symbolic_s=1.660336e+00, imitation_mse=7.485131e-01, target_mse=7.191753e-01, formula_export_success=True
  - icbr_no_shared: symbolic_s=3.748926e+00, imitation_mse=5.607000e-01, target_mse=5.548390e-01, formula_export_success=True
  - icbr_refit_commit: symbolic_s=4.719082e+00, imitation_mse=8.816294e-01, target_mse=8.719426e-01, formula_export_success=True
- icbr_full formula (display, rounded):
  - `-0.873034*sin(1.97839*acos(0.35*x_1 - 1.35) - 4.64239 + 13.4318*exp(-25.0*(0.97 - x_2)**2)) + 0.639414*Abs(4.75*(0.640601*sqrt(x_2 - 1) - 0.302837)*(0.679274*acos(0.25*x_1 - 1.25) - 1.92973 + 1.40612*exp(-25.0*(0.88 - x_2)**2)) + 0.5) + 0.247675*Abs(-6.12327*acos(0.35*x_1 - 1.35) + 8.78019*asin(0.4*x_2 - 1.3) + 28.1389) - 17.0824*acos(-0.165158*acos(0.35*x_1 - 1.2) - 0.175777*acos(0.3*x_2 - 1.0) + 0.385936) + 31.0204 + 5.33544*exp(-2.18654*(0.670576*atanh(0.4*x_1 - 1.4) - 1 + 0.662739/(0.419355 - x_2)**5)**2) + 6.96336*exp(-4.0*(-(0.532048*sqrt(x_2 - 1.0) - 0.560051 + 0.190952*exp(-2.89*(1 - 0.470588*x_1)**2))*(-0.91318*tanh(5.0*x_2 - 5.0) - 0.392497*atanh(0.4*x_1 - 1.4) + 0.378589) - 0.575)**2)`
- icbr_no_replay formula (display, rounded):
  - `0.878758*cos(-1.26812*atanh(0.45*x_1 - 1.45) + 0.496029 + 13.2371*exp(-25.0*(0.97 - x_2)**2)) + 0.639414*Abs(4.75*(0.25595*tan(0.6*x_2 + 4.35) + 0.632456)*(0.430471*atanh(0.4*x_1 - 1.35) + 0.567789 - 1.40612*exp(-25.0*(x_2 - 0.88)**2)) - 0.5) + 0.247675*Abs(8.78019*asin(0.4*x_2 - 1.3) + 4.9102*atanh(0.4*x_1 - 1.35) + 17.4368) - 17.0824*acos(-0.165158*acos(0.35*x_1 - 1.2) + 0.175777*asin(0.3*x_2 - 1.0) + 0.109826) + 31.0121 + 5.33544*exp(-235.674*(0.0645909*atanh(0.4*x_1 - 1.4) - 0.10186 - exp(-19.36*(0.909091 - x_2)**2))**2) + 6.96336*exp(-4.0*(-(0.212908*tan(0.6*x_2 + 4.35) + 0.216871 + 0.190952*exp(-2.89*(1 - 0.470588*x_1)**2))*(-0.392497*atanh(0.4*x_1 - 1.4) - 0.532842 + 0.958683*exp(-23.04*(0.9375 - x_2)**2)) - 0.575)**2)`
- icbr_no_shared formula (display, rounded):
  - `-0.873034*sin(1.97839*acos(0.35*x_1 - 1.35) - 4.64239 + 13.4318*exp(-25.0*(0.97 - x_2)**2)) + 0.639414*Abs(4.75*(0.640601*sqrt(x_2 - 1) - 0.302837)*(0.679274*asin(0.25*x_1 - 1.25) + 0.862731 - 1.40612*exp(-25.0*(x_2 - 0.88)**2)) - 0.5) + 0.254289*Abs(8.55213*acos(1.3 - 0.4*x_2) - 5.96422*acos(0.35*x_1 - 1.35) + 13.9626) - 17.0824*acos(-0.165158*acos(0.35*x_1 - 1.2) + 0.175777*asin(0.3*x_2 - 1.0) + 0.109826) + 31.0232 + 5.33544*exp(-2.18654*(0.670576*atanh(0.4*x_1 - 1.4) - 1 + 0.662739/(0.419355 - x_2)**5)**2) + 6.96336*exp(-4.0*(-(0.532048*sqrt(x_2 - 1) - 0.56005 + 0.190952*exp(-2.89*(1 - 0.470588*x_1)**2))*(-0.91318*tanh(5.0*x_2 - 5.0) - 0.392497*atanh(0.4*x_1 - 1.4) + 0.378589) - 0.575)**2)`
- icbr_refit_commit formula (display, rounded):
  - `0.771086*sin(1.83639*asin(0.35032*x_1 - 1.3504) + 1.42323 - 34.5955*exp(-7.65076*(0.650535 - x_2)**2)) + 0.635386*Abs(-4.63628*(0.640601*sqrt(x_2 - 1) - 0.302837)*(-0.577972*atanh(0.30344*x_1 - 1.184) - 0.673065 - 0.0104529/(0.607813 - x_2)**5) - 0.40576) + 0.910281*Abs(-1.66295*acos(0.34932*x_1 - 1.34932) + 2.49828*asin(0.382*x_2 - 1.27524) + 12.2455) - 54.1554*acos(0.0521098*tan(0.30052*x_1 - 1.00108) + 0.265693*asin(0.042*x_2 - 0.79938) - 0.324357) + 119.751 + 260.16*exp(-3.54524*(0.299054*atanh(0.106*x_1 - 1.10132) - 1 + 0.205207/(0.419101 - x_2)**5)**2) - 7.11361*exp(-3.58284*(-(0.532048*sqrt(x_2 - 1) - 0.579345 + 0.201649*exp(-2.18945*(1 - 0.457153*x_1)**2))*(-0.721197*tanh(4.9*x_2 - 5.0) - 0.550597*atanh(0.104*x_1 - 1.10086) - 0.351843) + 0.203525)**2)`

### task=feynman_I_12_1 seed=9

- Task source: feynman_file
- Target formula: `mu*Nn`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=6.134526e-03, r2=0.999762
- Variant formula overview:
  - icbr_full: symbolic_s=2.738086e+00, imitation_mse=2.172768e-02, target_mse=1.439277e-02, formula_export_success=True
  - icbr_no_replay: symbolic_s=1.815889e+00, imitation_mse=2.204890e-02, target_mse=1.488195e-02, formula_export_success=True
  - icbr_no_shared: symbolic_s=4.082987e+00, imitation_mse=2.172770e-02, target_mse=1.439277e-02, formula_export_success=True
  - icbr_refit_commit: symbolic_s=4.981817e+00, imitation_mse=nan, target_mse=nan, formula_export_success=True
- icbr_full formula (display, rounded):
  - `-0.00032679*(-0.771718*Abs(3.2*x_1 - 4.575) + 0.665681*Abs(2.8*x_2 - 4.45) + 1)**4 + 0.549191*(-1.14358*acos(0.4*x_1 - 1.4) + 1.05317*asin(0.45*x_2 - 1.45) + 4.83724)*(-2.34283*acos(0.35*x_2 - 1.2) + 1.58098*asin(0.45*x_1 - 1.45) + 8.57581) + 0.532399*sin(2.38543*atanh(0.4*x_1 - 1.35) + 1.46467) + 0.462747*sin(21.4058*sqrt(0.0913706*x_1 + 1) + 0.732973*atanh(0.45*x_2 - 1.45) - 19.4677) - 1.2642*sin(-0.611355*acos(0.3*x_2 - 1.0) + 2.42855 + 2.82809*exp(-(0.1*x_1 - 1.0)**2)) + 0.842002*tanh(0.4*(1.58781*asin(0.45*x_2 - 1.45) + 2.25706)*(-1.62565*sin(0.45*x_1 + 1.7) - 0.100558*Abs(2.4*x_2 - 3.75) + 1.67658) - 1.55) + 1.70987 + 1.23449*exp(-0.16487*(0.278176*Abs(2.7*x_1 - 3.8) - 0.275441*Abs(3.65*x_2 - 4.55) + 1)**2)`
- icbr_no_replay formula (display, rounded):
  - `-0.00032679*(-0.771718*Abs(3.2*x_1 - 4.575) + 0.665681*Abs(2.8*x_2 - 4.45) + 1)**4 + 0.549191*(1.14358*asin(0.4*x_1 - 1.4) + 1.05317*asin(0.45*x_2 - 1.45) + 3.04092)*(1.58098*asin(0.45*x_1 - 1.45) + 2.34283*asin(0.35*x_2 - 1.2) + 4.89569) + 0.532399*sin(2.38543*atanh(0.4*x_1 - 1.35) + 1.46467) + 0.462747*sin(21.4058*sqrt(0.0913706*x_1 + 1) + 0.732973*atanh(0.45*x_2 - 1.45) - 19.4677) - 1.26393*cos(0.611355*asin(0.3*x_2 - 1.0) - 0.0817601 + 2.82809*exp(-(0.1*x_1 - 1.0)**2)) + 0.842002*tanh(0.4*(1.58781*asin(0.45*x_2 - 1.45) + 2.25706)*(0.174157*Abs(3.95*x_1 - 4.95) - 0.100558*Abs(2.4*x_2 - 3.75) + 0.334763) - 1.55) + 1.68514 + 1.23449*exp(-0.16487*(0.278176*Abs(2.7*x_1 - 3.8) - 0.275441*Abs(3.65*x_2 - 4.55) + 1)**2)`
- icbr_no_shared formula (display, rounded):
  - `-0.00032679*(-0.771718*Abs(3.2*x_1 - 4.575) + 0.665681*Abs(2.8*x_2 - 4.45) + 1)**4 + 0.532399*sin(2.38543*atanh(0.4*x_1 - 1.35) + 1.46467) + 0.462747*sin(21.4058*sqrt(0.0913706*x_1 + 1) + 0.732973*atanh(0.45*x_2 - 1.45) - 19.4677) - 1.2642*sin(0.611355*asin(0.3*x_2 - 1.0) + 1.46824 + 2.82809*exp(-(0.1*x_1 - 1.0)**2)) + 0.842002*tanh(0.4*(1.58781*asin(0.45*x_2 - 1.45) + 2.25706)*(-1.62565*sin(0.45*x_1 + 1.7) - 0.100558*Abs(2.4*x_2 - 3.75) + 1.67658) - 1.55) + 0.289048*Abs(1.9*(-1.14358*acos(0.4*x_1 - 1.4) + 1.05317*asin(0.45*x_2 - 1.45) + 4.83724)*(-2.34283*acos(0.35*x_2 - 1.2) + 1.58098*asin(0.45*x_1 - 1.45) + 8.57581) + 0.25) + 1.63761 + 1.23449*exp(-0.16487*(0.278176*Abs(2.7*x_1 - 3.8) - 0.275441*Abs(3.65*x_2 - 4.55) + 1)**2)`
- icbr_refit_commit formula (display, rounded):
  - `-0.0617923*(-Abs(1.15116*x_1 - 1.57168) + 0.284262*Abs(3.06908*x_2 - 4.84984) + 0.394587)**2 + 0.549002*(2.22387*acos(1.22544 - 0.36824*x_2) - 1.70369*acos(0.42392*x_1 - 1.39748) + 4.04833)*(1.0929*asin(0.419*x_1 - 1.422) + 1.44383*atanh(0.33*x_2 - 1.1) + 3.04666) + 0.604006*sin(2.30147*atanh(0.32912*x_1 - 1.185) + 1.43707) + 0.460111*cos(21.719*sqrt(0.0901112*x_1 + 1) + 1.20431*atanh(0.31184*x_2 - 1.17792) - 21.1179) + 0.927296*tanh(0.34408*(1.70318*asin(0.4254*x_2 - 1.39968) + 2.31144)*(1.79669*sin(0.4*x_1 + 4.99995) - 0.0742535*Abs(3.2*x_2 - 4.99953) + 1.67573) - 1.3808) + 0.0903294*Abs(45.6867*sqrt(0.133193*x_2 + 1) - 77.7463 + 55.38*exp(-0.810072*(0.0755521*x_1 - 1)**2)) + 0.676047 + 1.27529*exp(-0.17305*(0.316027*Abs(2.18272*x_1 - 2.87444) - 0.24339*Abs(3.83588*x_2 - 4.33484) + 1)**2)`

### task=feynman_I_12_1 seed=10

- Task source: feynman_file
- Target formula: `mu*Nn`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=3.732413e-02, r2=0.998505
- Variant formula overview:
  - icbr_full: symbolic_s=3.085215e+00, imitation_mse=1.213208e+00, target_mse=1.257170e+00, formula_export_success=True
  - icbr_no_replay: symbolic_s=1.986330e+00, imitation_mse=2.050241e+00, target_mse=2.068568e+00, formula_export_success=True
  - icbr_no_shared: symbolic_s=5.280539e+00, imitation_mse=1.213655e+00, target_mse=1.257502e+00, formula_export_success=True
  - icbr_refit_commit: symbolic_s=5.196287e+00, imitation_mse=1.790465e+00, target_mse=1.795568e+00, formula_export_success=True
- icbr_full formula (display, rounded):
  - `92.3183*(-0.848902*(1 - 0.0327869*x_2)**(3/2) + 1 - 0.0382014/(0.706522 - x_1)**2)**3 + 1.41234*sin(4.6*(-0.77255*sin(0.7*x_2 + 4.0) + 0.0304986*Abs(3.4*x_1 - 4.85) - 1.24731)*(0.32823*atanh(0.3*x_1 - 1.0) - 0.14406*sign(3.9 - 3.35*x_2) + 0.111393) + 4.55) + 1.06199*sin(4.75*(-0.315505*cos(0.35*x_1 + 0.5) - 0.0790618 - 1.16349*exp(-25.0*(0.93 - x_2)**2))*(-0.869359*acos(0.35*x_2 - 1.35) + 1.4051 + 0.699139*exp(-2.7225*(1 - 0.484848*x_1)**2)) + 1.55) - 2.02963*atan(0.224467 + 0.801077*exp(-3.24*(1 - 0.472222*x_2)**2) + 0.736853/(0.725806 - x_1)**2) - 2.53829*atan(1.14045*cos(0.35*x_2 + 0.5) - 0.134076*Abs(2.65*x_1 - 5.0) + 1.22049) + 6.8012 + 1.50398*exp(-12.1577*(tanh(5.0*x_2 - 4.5) + 0.480544*sign(4.5 - 3.95*x_1) - 0.678916)**2) + 5.86062*exp(-0.517726*(0.291694*tan(0.65*x_1 - 2.15) + 0.444063*tan(0.6*x_2 - 2.1) - 1)**2)`
- icbr_no_replay formula (display, rounded):
  - `3.07485*tanh(0.356802*tan(0.65*x_1 - 2.15) + 0.54318*tan(0.6*x_2 - 2.1) + 0.131796) + 1.21931*Abs(-4.4*(0.0304986*Abs(3.4*x_1 - 4.85) - 0.139782*Abs(3.35*x_2 - 4.825) - 0.394502)*(0.282252*asin(0.35*x_1 - 1.25) + 0.282575 - 0.42096*exp(-25.0*(0.965 - x_2)**2)) - 2.38419e-7) - 2.02963*atan(0.507775 + 0.801077*exp(-3.24*(1 - 0.472222*x_2)**2) + 7.87676*exp(-25.0*(1 - x_1)**2)) - 2.53829*atan(1.14045*cos(0.35*x_2 + 0.5) - 0.134076*Abs(2.65*x_1 - 5.0) + 1.22049) + 7.65073 + 4.25079*exp(-34.5124*(-(1 - 0.0327869*x_2)**(3/2) + 0.682854 - 0.420498*exp(-25.0*(1 - 0.995*x_1)**2))**2) + 1.50398*exp(-33.2198*(-0.100633 - 0.380831*exp(-25.0*(0.91 - x_2)**2) + exp(-25.0*(0.91 - x_1)**2))**2) + 1.8573*exp(-10.89*(-(0.0331826*Abs(3.2*x_1 - 3.7) - 0.358084*sign(4.5 - 3.9*x_2) - 0.643552)*(0.692191*atanh(0.4*x_2 - 1.35) - 0.115001 + 0.699139*exp(-2.7225*(1 - 0.484848*x_1)**2)) - 0.0151516)**2)`
- icbr_no_shared formula (display, rounded):
  - `88.7082*(-0.846928*(1 - 0.0333333*x_2)**(3/2) + 1 - 0.0387127/(x_1 - 0.706522)**2)**3 + 1.41234*sin(4.6*(-0.77255*sin(0.7*x_2 + 4.0) + 0.0304986*Abs(3.4*x_1 - 4.85) - 1.24731)*(0.32823*atanh(0.3*x_1 - 1.0) - 0.14406*sign(3.9 - 3.35*x_2) + 0.111393) + 4.55) + 1.06199*sin(4.75*(0.0372649*Abs(2.85*x_1 - 3.3) - 0.281447 - 1.16349*exp(-25.0*(0.93 - x_2)**2))*(-0.869359*acos(0.35*x_2 - 1.35) + 1.4051 + 0.699139*exp(-2.7225*(1 - 0.484848*x_1)**2)) + 1.55) - 2.02963*atan(0.224467 + 0.801077*exp(-3.24*(1 - 0.472222*x_2)**2) + 0.736853/(0.725806 - x_1)**2) - 2.53829*atan(1.14045*cos(0.35*x_2 + 0.5) - 0.134076*Abs(2.65*x_1 - 5.0) + 1.22049) + 6.8012 + 1.50398*exp(-12.1577*(tanh(5.0*x_2 - 4.5) + 0.480544*sign(4.5 - 3.95*x_1) - 0.678916)**2) + 5.86062*exp(-0.517726*(0.291694*tan(0.65*x_1 - 2.15) + 0.444063*tan(0.6*x_2 - 2.1) - 1)**2)`
- icbr_refit_commit formula (display, rounded):
  - `-1.41201*sin(4.602*(-0.182443*sin(0.642*x_1 + 1.00082) + 0.82138*sin(0.642*x_2 + 1.00022) - 1.08236)*(0.327275*atanh(0.30076*x_1 - 1.0018) - 0.124324*sign(4.69818 - 3.996*x_2) + 0.12964) + 1.40896) + 1.0678*sin(4.75044*(0.325547*cos(0.338*x_1 + 3.70016) - 0.0854135 - 10.2697*exp(-5.68117*(0.371148 - x_2)**2))*(-0.869407*acos(0.35*x_2 - 1.34996) + 1.2973 + 0.75541*exp(-1.64434*(1 - 0.476886*x_1)**2)) - 4.71256) + 6.26068*tanh(0.13628*tan(0.4*x_1 + 1.21) + 0.0721898*tan(0.10624*x_2 + 1.4796) - 0.056937) - 1.63273*atan(0.340105*sin(1.338*x_2 - 1.39996) + 0.281357 + 0.425888/(0.782886 - x_1)**2) + 8.39258 + 2.35442*exp(-0.643374*(0.96907*tanh(5.0*x_2 - 4.99) + sign(4.59998 - 4.092*x_1) - 0.53199)**2) + 4.50246*exp(-2.26782*(-0.813902*sin(0.20192*x_2 - 3.72564) + 0.129791*Abs(1.20068*x_1 - 2.40524) - 1)**2) + 16.998*exp(-7.38557*(-(1 - 0.0355732*x_2)**(3/2) + 0.308217 - 0.044283/(0.722527 - x_1)**2)**2)`

### task=feynman_I_12_1 seed=11

- Task source: feynman_file
- Target formula: `mu*Nn`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=4.830737e-03, r2=0.999804
- Variant formula overview:
  - icbr_full: symbolic_s=2.392004e+00, imitation_mse=1.469392e-02, target_mse=1.550554e-02, formula_export_success=True
  - icbr_no_replay: symbolic_s=1.593642e+00, imitation_mse=1.553629e-02, target_mse=1.582596e-02, formula_export_success=True
  - icbr_no_shared: symbolic_s=3.568469e+00, imitation_mse=1.467663e-02, target_mse=1.547781e-02, formula_export_success=True
  - icbr_refit_commit: symbolic_s=4.280130e+00, imitation_mse=1.326930e-02, target_mse=1.545338e-02, formula_export_success=True
- icbr_full formula (display, rounded):
  - `149.453*sqrt(0.0100503*(9.44679*sqrt(0.142857*x_1 + 1) + 8.28017*sqrt(0.1*x_2 + 1) - 18.2818)*(10.886*log(0.2*x_2 + 4.95) + 1.27072*asin(0.45*x_1 - 1.45) - 15.8068) + 1) - 0.0827413*(-atanh(0.4*x_2 - 1.35) - 0.702542)**3 + 1.66217*sin(0.148965*Abs(3.2*x_1 - 4.55) - 0.102636*Abs(3.4*x_2 - 4.45) + 1.67297) + 10.6128*cos(0.0572582*Abs(2.15*x_1 - 2.6) - 0.0582932*Abs(2.95*x_2 - 4.0) + 0.183452) + 0.0760292*Abs(-4.9*(8.50641*(1 - 0.0425532*x_1)**(3/2) + 0.658419*acos(0.4*x_2 - 1.4) - 10.1993)*(-14.8229*sqrt(0.172414*x_2 + 1) - 1.64097*tan(0.3*x_1 - 1.0) + 13.9457) + 0.9) - 162.124 + 1.55752*exp(-0.0827016*(1 - 0.268234*Abs(3.15*x_1 - 4.55))**2)`
- icbr_no_replay formula (display, rounded):
  - `149.453*sqrt(0.0100503*(9.42339*sqrt(0.0942408*x_2 + 1) + 1.27072*asin(0.45*x_1 - 1.45) - 7.82281)*(8.28017*sqrt(0.1*x_2 + 1) + 1.80152*asin(0.3*x_1 - 1.0) - 6.81569) + 1) - 0.0827413*(-atanh(0.4*x_2 - 1.35) - 0.702542)**3 - 0.17137*(0.316563*Abs(2.15*x_1 - 2.6) - 0.322285*Abs(2.95*x_2 - 4.0) + 1)**2 - 0.367254*cos(0.231415*Abs(3.15*x_1 - 4.55) + 2.28726) + 2.0957*cos(0.128955*Abs(3.2*x_1 - 4.55) - 0.0888491*Abs(3.4*x_2 - 4.45) + 0.099735) + 0.0760292*Abs(-4.9*(-19.7015*sqrt(0.0555556*x_1 + 1) - 0.658419*asin(0.4*x_2 - 1.4) + 19.0459)*(1.42407*acos(0.35*x_1 - 1.2) + 3.28052*acos(0.3*x_2 - 1.05) - 12.2443) + 0.9) - 150.762`
- icbr_no_shared formula (display, rounded):
  - `150.176*sqrt(0.01*(9.44679*sqrt(0.142857*x_1 + 1) + 8.28017*sqrt(0.1*x_2 + 1) - 18.2818)*(9.68756*sqrt(0.0913706*x_2 + 1) + 1.27072*asin(0.45*x_1 - 1.45) - 8.08536) + 1) - 0.0827413*(-atanh(0.4*x_2 - 1.35) - 0.702542)**3 + 1.66217*sin(0.148965*Abs(3.2*x_1 - 4.55) - 0.102636*Abs(3.4*x_2 - 4.45) + 1.67297) + 10.6128*cos(0.0572582*Abs(2.15*x_1 - 2.6) - 0.0582932*Abs(2.95*x_2 - 4.0) + 0.183452) + 0.08188*Abs(4.55*(8.50641*(1 - 0.0425532*x_1)**(3/2) + 0.658419*acos(0.4*x_2 - 1.4) - 10.1993)*(14.8229*sqrt(0.172414*x_2 + 1) + 1.64097*tan(0.3*x_1 - 1.0) - 13.9457) + 0.95) - 162.838 + 1.55752*exp(-0.0827016*(1 - 0.268234*Abs(3.15*x_1 - 4.55))**2)`
- icbr_refit_commit formula (display, rounded):
  - `77.795*sqrt(0.0200022*(9.38805*sqrt(0.143903*x_1 + 1) + 8.24382*sqrt(0.100497*x_2 + 1) - 18.1877)*(11.0527*log(0.0964399*x_2 + 2.42776) + 1.74359*atanh(0.33*x_1 - 1.1) - 8.12664) + 1) - 0.171081*(-0.38059*atanh(0.25324*x_2 - 1.16908) - 1)**5 - 27.3374*sin(0.0403906*Abs(2.61032*x_1 - 3.61024) - 0.0191127*Abs(4.0292*x_2 - 4.81732) + 4.74386) - 2.64945*cos(-0.0627118*Abs(4.07776*x_1 - 4.57916) + 0.139766*Abs(2.53608*x_2 - 3.24696) + 2.77235) - 3.58182*Abs(-0.10404*(8.40581*(1 - 0.043103*x_1)**(3/2) + 0.626633*acos(0.42172*x_2 - 1.4218) - 10.0101)*(-15.0658*sqrt(0.169095*x_2 + 1) - 1.36026*acos(1.22176 - 0.36612*x_1) + 16.3196) + 2.67444) - 98.1288 + 0.89602*exp(-0.160746*(1 - 0.322763*Abs(2.546*x_1 - 3.52092))**2)`

### task=feynman_I_12_1 seed=12

- Task source: feynman_file
- Target formula: `mu*Nn`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.246034e-02, r2=0.999492
- Variant formula overview:
  - icbr_full: symbolic_s=2.311707e+00, imitation_mse=2.658220e-02, target_mse=2.791931e-02, formula_export_success=True
  - icbr_no_replay: symbolic_s=1.548300e+00, imitation_mse=3.187125e-02, target_mse=3.472744e-02, formula_export_success=True
  - icbr_no_shared: symbolic_s=3.307563e+00, imitation_mse=2.658378e-02, target_mse=2.791979e-02, formula_export_success=True
  - icbr_refit_commit: symbolic_s=4.001796e+00, imitation_mse=4.222786e-02, target_mse=4.183070e-02, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0.751562*(49.7033*sqrt(0.0543478*x_2 + 1) + 0.026857*tan(0.65*x_1 - 2.15) - 50.199)*(25.4297*log(0.2*x_1 + 4.675) + 1.2127*tanh(4.75*x_2 - 5.0) - 40.8276) - 0.789564*cos(8.61586*sqrt(0.0972973*x_1 + 1) + 0.833669*cos(0.3*x_2 - 2.5) - 8.45326) + 0.113395*Abs(40.3701*(1 - 0.0410256*x_1)**(3/2) - 36.6091) + 0.118075*Abs(82.9315*log(0.1*x_2 + 4.525) + 0.853083*asin(0.45*x_1 - 1.45) - 128.604) + 2.09083 - 0.554847*exp(-25.0*((0.214739*tan(0.6*x_2 + 4.35) + 0.53195)*(0.0434848*Abs(3.85*x_1 - 4.825) - 1.9104 + 1.36712*exp(-1.0*(1 - 0.55*x_2)**2)) - 0.01)**2) - 0.305975*exp(-5.24302*(0.216614 - atanh(0.3*x_2 - 1.0))**2)`
- icbr_no_replay formula (display, rounded):
  - `-0.789564*cos(8.61586*sqrt(0.0972973*x_1 + 1) + 0.833669*cos(0.3*x_2 - 2.5) - 8.45326) - 0.137444*tanh(3.77428*asin(0.4*x_2 - 1.35) + 1.07443) + 0.181293*Abs(-4.15*(22.1889*sqrt(0.0989011*x_1 + 1) - 22.598 - 1.38679*exp(-25.0*(0.99 - x_2)**2))*(49.7033*sqrt(0.0543478*x_2 + 1) + 0.026857*tan(0.65*x_1 - 2.15) - 50.199) + 0.15) + 0.113395*Abs(97.3846*sqrt(0.0512821*x_1 + 1) - 101.152) + 0.118075*Abs(82.9315*log(0.1*x_2 + 4.525) + 0.853083*asin(0.45*x_1 - 1.45) - 128.604) + 1.96967 - 0.554847*exp(-25.0*((0.214739*tan(0.6*x_2 + 4.35) + 0.53195)*(0.0434848*Abs(3.85*x_1 - 4.825) - 0.163534*Abs(2.85*x_2 - 4.775) - 0.438665) - 0.01)**2)`
- icbr_no_shared formula (display, rounded):
  - `0.751562*(49.7033*sqrt(0.0543478*x_2 + 1) + 0.026857*tan(0.65*x_1 - 2.15) - 50.199)*(25.4297*log(0.2*x_1 + 4.675) + 1.2127*tanh(4.75*x_2 - 5.0) - 40.8276) - 0.789564*cos(9.963*log(0.2*x_1 + 4.8) + 0.833669*cos(0.3*x_2 - 2.5) - 15.4621) + 0.113395*Abs(40.3701*(1 - 0.0410256*x_1)**(3/2) - 36.6091) + 0.118075*Abs(82.9315*log(0.1*x_2 + 4.525) + 0.853083*asin(0.45*x_1 - 1.45) - 128.604) + 2.09083 - 0.554847*exp(-25.0*((0.214739*tan(0.6*x_2 + 4.35) + 0.53195)*(0.0423834*Abs(3.95*x_1 - 4.95) - 1.91041 + 1.36712*exp(-1.0*(1 - 0.55*x_2)**2)) - 0.01)**2) - 0.305975*exp(-5.24302*(0.216614 - atanh(0.3*x_2 - 1.0))**2)`
- icbr_refit_commit formula (display, rounded):
  - `-0.783773*cos(8.98264*sqrt(0.0940325*x_1 + 1) + 0.75516*cos(0.338*x_2 + 3.70074) - 8.8625) + 0.156644*Abs(4.8*(47.8827*sqrt(0.0565714*x_2 + 1) + 0.0268796*tan(0.436*x_1 - 1.92932) - 48.3632)*(25.4782*log(0.19832*x_1 + 4.64568) + 1.32675*tanh(4.9*x_2 - 5.0) - 40.8654) + 3.6998) + 0.0799128*Abs(55.4109*(1 - 0.0416973*x_1)**(3/2) - 50.1253) + 0.1356*Abs(70.9229*sqrt(0.0429074*x_2 + 1) + 0.768045*asin(0.42304*x_1 - 1.39532) - 73.666) + 0.766783 + 0.309751*exp(-2.91555*(-atanh(0.30024*x_2 - 1.00032) - 0.684625)**2) + 0.591858*exp(-2.84637*(-(0.430625*tan(0.35732*x_2 + 4.83408) + 0.683546)*(0.0620362*Abs(2.65716*x_1 - 3.053) - 1.99555 + 1.42392*exp(-0.788757*(1 - 0.563302*x_2)**2)) - 0.875172)**2)`

### task=feynman_I_12_1 seed=13

- Task source: feynman_file
- Target formula: `mu*Nn`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.496255e-02, r2=0.999343
- Variant formula overview:
  - icbr_full: symbolic_s=2.980844e+00, imitation_mse=1.673985e-01, target_mse=1.666720e-01, formula_export_success=True
  - icbr_no_replay: symbolic_s=1.965258e+00, imitation_mse=3.069894e-01, target_mse=3.266009e-01, formula_export_success=True
  - icbr_no_shared: symbolic_s=4.337451e+00, imitation_mse=1.673985e-01, target_mse=1.666720e-01, formula_export_success=True
  - icbr_refit_commit: symbolic_s=5.417450e+00, imitation_mse=nan, target_mse=nan, formula_export_success=True
- icbr_full formula (display, rounded):
  - `-1.81967*sin(5.0*(-0.885676*cos(0.45*x_1 + 0.0999997) + 0.926635 + 0.108069*exp(-1.21*(1 - 0.545455*x_2)**2))*(-0.227909*asin(0.4*x_2 - 1.4) + 0.107267*sign(3.95 - 3.4*x_1) - 0.142564) + 1.45) - 1.37161*tan(0.35*(0.30583*cos(0.45*x_2 + 0.15) - 2.32436 + 5.04695*exp(-(0.1*x_1 - 1.0)**2))*(0.0438006*Abs(2.8*x_1 - 5.0) - 0.565459*atanh(0.4*x_2 - 1.4) - 0.672411) - 4.1) + 23.3461*atanh(1.15336*sqrt(0.107527*x_1 + 1) + 0.211682*cos(0.3*x_2 - 2.5) - 1.41514) + 7.02301 + 2.94125*exp(-0.161896*(-acos(0.4*x_2 - 1.4) - 0.754044 + 0.97018/(0.575758 - x_1)**3)**2) + 1.50516*exp(-0.486876*(acos(0.4*x_1 - 1.4) - 0.799566*acos(0.35*x_2 - 1.35) + 0.0852955)**2) + 1.77527*exp(-1.49945*(0.303345*tan(0.65*x_1 - 2.15) - 1 - 0.974726/(x_2 - 0.310345)**5)**2) + 2.92906*exp(-1.282*(0.4386*tan(0.6*x_1 - 2.05) + 0.117042*tan(0.25*x_2 - 1.8) - 1)**2)`
- icbr_no_replay formula (display, rounded):
  - `14.9078*(-0.0929044*acos(0.4*x_2 - 1.4) + 0.672756 - exp(-25.0*(0.99 - x_1)**2))**4 - 1.61047*log(4.3*(0.0438006*Abs(2.8*x_1 - 5.0) - 0.565459*atanh(0.4*x_2 - 1.4) - 0.672411)*(-0.0327349*Abs(3.95*x_2 - 4.925) - 2.07696 + 5.04695*exp(-(0.1*x_1 - 1.0)**2)) + 4.8) + 0.654396*sin(-1.42876*asin(0.4*x_1 - 1.4) + 0.909853*atanh(0.4*x_2 - 1.35) + 1.94579) + 2.17571*Abs(-3.5*(0.0947943*Abs(3.95*x_1 - 4.975) - 0.0139631*Abs(2.8*x_2 - 4.775) + 0.290811)*(0.227909*acos(0.4*x_2 - 1.4) + 0.107267*sign(3.95 - 3.4*x_1) - 0.500563) - 0.0500002) + 23.3461*atanh(0.171546*asin(0.3*x_1 - 1.0) - 0.521831 + 0.725484*exp(-(0.1*x_2 - 1.0)**2)) + 10.1151 + 1.77527*exp(-39.1651*(0.0593545*tan(0.65*x_1 - 2.15) - 0.207386 - exp(-25.0*(0.99 - x_2)**2))**2) + 2.92906*exp(-1.64031*(0.387748*tan(0.6*x_1 - 2.05) - 1 - 0.295178/(0.741935 - x_2)**2)**2)`
- icbr_no_shared formula (display, rounded):
  - `-1.81967*sin(5.0*(-0.885676*cos(0.45*x_1 + 0.1) + 0.926635 + 0.108069*exp(-1.21*(1 - 0.545455*x_2)**2))*(-0.227909*asin(0.4*x_2 - 1.4) + 0.107267*sign(3.95 - 3.4*x_1) - 0.142564) + 1.45) - 1.37161*tan(0.35*(0.30583*cos(0.45*x_2 + 0.15) - 2.32436 + 5.04695*exp(-(0.1*x_1 - 1.0)**2))*(0.0438006*Abs(2.8*x_1 - 5.0) - 0.565459*atanh(0.4*x_2 - 1.4) - 0.672411) - 4.1) + 23.3461*atanh(1.15336*sqrt(0.107527*x_1 + 1) + 0.211682*cos(0.3*x_2 - 2.5) - 1.41514) + 7.02301 + 2.94125*exp(-0.161896*(-acos(0.4*x_2 - 1.4) - 0.754044 + 0.97018/(0.575758 - x_1)**3)**2) + 1.50516*exp(-0.486876*(acos(0.4*x_1 - 1.4) - 0.799566*acos(0.35*x_2 - 1.35) + 0.0852955)**2) + 1.77527*exp(-1.49945*(-0.303345*tan(0.65*x_1 - 2.15) + 1 + 0.974726/(x_2 - 0.310345)**5)**2) + 2.92906*exp(-1.282*(0.4386*tan(0.6*x_1 - 2.05) + 0.117042*tan(0.25*x_2 - 1.8) - 1)**2)`
- icbr_refit_commit formula (display, rounded):
  - `1.82741*sin(4.9698*(0.900066*cos(0.44*x_1 + 3.3006) - 0.0171115*Abs(2.30316*x_2 - 4.10368) + 1.02055)*(-0.218254*asin(0.41868*x_2 - 1.41996) + 0.0957656*sign(4.59826 - 3.99*x_1) - 0.141816) - 1.696) - 1.18626*tan(0.25124*(0.315265*cos(0.434*x_2 + 0.20002) - 3.59218 + 6.96253*exp(-0.810144*(1 - 0.0799928*x_1)**2))*(-0.78098*atanh(0.104*x_2 - 1.10142) - 1.05165 - 0.356662*exp(-0.99904*(1 - 0.528654*x_1)**2)) + 2.03736) - 98.0329*atanh(-0.19315*sqrt(0.106169*x_1 + 1) + 0.101813*cos(0.0999999*x_2 - 4.99913) + 0.785026) + 66.4783 + 33.7567*exp(-4.40437*(0.0852938*acos(1.41988 - 0.41856*x_2) - 1 + 0.0864018/(0.575772 - x_1)**3)**2) + 1.50554*exp(-1.81104*(0.54099*acos(1.3748 - 0.38492*x_1) - 0.424884*atanh(0.3334*x_2 - 1.1948) - 1)**2) + 131.769*exp(-4.58403*(0.0719745*tan(0.40392*x_1 + 4.40376) + 0.0197892*tan(0.20408*x_2 + 1.38576) - 1)**2) + 45.8911*exp(-4.08793*(0.0234072*tan(0.2*x_1 - 4.888) - 1 + 0.19665/(0.310531 - x_2)**5)**2)`

### task=feynman_I_12_1 seed=14

- Task source: feynman_file
- Target formula: `mu*Nn`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=8.608292e-03, r2=0.999668
- Variant formula overview:
  - icbr_full: symbolic_s=2.868540e+00, imitation_mse=2.781707e-02, target_mse=2.639337e-02, formula_export_success=True
  - icbr_no_replay: symbolic_s=1.875102e+00, imitation_mse=3.259807e-02, target_mse=3.187469e-02, formula_export_success=True
  - icbr_no_shared: symbolic_s=4.462304e+00, imitation_mse=2.781559e-02, target_mse=2.639221e-02, formula_export_success=True
  - icbr_refit_commit: symbolic_s=5.241102e+00, imitation_mse=3.594432e-02, target_mse=3.525775e-02, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0.767499*(-10.0705*sqrt(0.133333*x_1 + 1) + 0.996466*acos(0.45*x_2 - 1.45) + 7.43733)*(1.22273*acos(0.35*x_1 - 1.2) - 2.25074*atanh(0.3*x_2 - 1.0) - 5.47665) - 0.267716*(-0.218254*Abs(4.0*x_1 - 5.0) + 0.184565*Abs(3.05*x_2 - 3.6) + 1)**2 - 0.748025*sin(2.35*(-0.0795155*Abs(3.05*x_2 - 5.0) + 0.0748225*atanh(0.45*x_1 - 1.45) - 0.187871)*(-0.121371*Abs(3.05*x_2 - 4.15) + 0.174912*atanh(0.45*x_1 - 1.45) - 0.105144) + 3.6) - 0.87847*cos(2.89148*(1 - 0.040201*x_2)**(3/2) - 13.4334*sqrt(0.0725389*x_1 + 1) + 11.038) + 2.65275 - 1.3309*exp(-678.409*(0.981482*sqrt(0.0301508*x_2 + 1) + 0.00710337*atanh(0.4*x_1 - 1.35) - 1)**2) + 0.850906*exp(-2.85723*(0.342854 + exp(-3.61*(1 - 0.473684*x_2)**2) + 0.670364*exp(-2.89*(1 - 0.470588*x_1)**2))**2) - 0.529961*exp(-12.8034*(1 + 0.0873096/(0.481481 - x_2)**5)**2)`
- icbr_no_replay formula (display, rounded):
  - `-0.267716*(-0.218254*Abs(4.0*x_1 - 5.0) + 0.184565*Abs(3.05*x_2 - 3.6) + 1)**2 + 0.172501*Abs(4.45*(1.80854*asin(0.3*x_1 - 1.0) + 0.996466*asin(0.45*x_2 - 1.45) + 3.09005)*(1.22273*asin(0.35*x_1 - 1.2) + 1.67274*asin(0.4*x_2 - 1.35) + 3.58924) - 1.45) + 0.227836*Abs(0.371907*Abs(4.25*x_2 - 4.6) + 0.790525*atanh(0.4*x_1 - 1.35) - 0.561686) + 2.03782 - 2.04392*exp(-45.1138*(-0.215247*(1 - 0.040201*x_2)**(3/2) + sqrt(0.0725389*x_1 + 1) - 0.829128)**2) + 0.850906*exp(-2.85723*(0.342854 + exp(-3.61*(1 - 0.473684*x_2)**2) + 0.670364*exp(-2.89*(1 - 0.470588*x_1)**2))**2) + 1.42327*exp(-1.96*(-(0.0434039*tan(0.6*x_1 + 4.3) - 0.0795155*Abs(3.05*x_2 - 5.0) - 0.182318)*(0.101841*tan(0.6*x_1 + 4.3) - 0.121371*Abs(3.05*x_2 - 4.15) - 0.0919926) + 0.464286)**2) - 0.529961*exp(-57.4031*(0.467052 - exp(-23.04*(0.9375 - x_2)**2))**2)`
- icbr_no_shared formula (display, rounded):
  - `0.767499*(-10.0705*sqrt(0.133333*x_1 + 1) - 0.996466*asin(0.45*x_2 - 1.45) + 9.00258)*(1.22273*acos(0.35*x_1 - 1.2) - 2.25074*atanh(0.3*x_2 - 1.0) - 5.47665) - 0.267716*(-0.218254*Abs(4.0*x_1 - 5.0) + 0.184565*Abs(3.05*x_2 - 3.6) + 1)**2 - 0.748025*sin(2.35*(-0.0795155*Abs(3.05*x_2 - 5.0) + 0.0748225*atanh(0.45*x_1 - 1.45) - 0.187871)*(-0.121371*Abs(3.05*x_2 - 4.15) + 0.174912*atanh(0.45*x_1 - 1.45) - 0.105144) + 3.6) - 0.87847*cos(2.89148*(1 - 0.040201*x_2)**(3/2) - 13.5605*sqrt(0.0717949*x_1 + 1) + 11.1646) + 2.65275 - 1.3309*exp(-672.011*(0.98139*sqrt(0.030303*x_2 + 1) + 0.00713711*atanh(0.4*x_1 - 1.35) - 1)**2) + 0.850906*exp(-2.85723*(0.342854 + exp(-3.61*(1 - 0.473684*x_2)**2) + 0.670364*exp(-2.89*(1 - 0.470588*x_1)**2))**2) - 0.529961*exp(-12.8034*(1 + 0.0873096/(0.481481 - x_2)**5)**2)`
- icbr_refit_commit formula (display, rounded):
  - `0.767436*(-10.0381*sqrt(0.133832*x_1 + 1) - 1.07834*asin(0.42204*x_2 - 1.39456) + 8.92916)*(-1.10821*asin(0.38168*x_1 - 1.27436) - 2.25461*atanh(0.29952*x_2 - 0.9992) - 3.51775) - 0.280449*(-0.213298*Abs(3.90796*x_1 - 4.40996) + 0.122806*Abs(4.41568*x_2 - 4.80332) + 1)**2 - 0.737411*sin(2.4002*(-0.333879*cos(0.938*x_2 - 4.69988) + 0.107014*atanh(0.208*x_1 - 1.20098) - 0.523444)*(-0.0931973*Abs(3.898*x_2 - 4.99914) + 0.256974*atanh(0.21*x_1 - 1.2) + 0.0753452) - 2.71244) + 2.64173 - 1.49301*exp(-525.769*(-0.99891*sqrt(0.0290076*x_2 + 1) + 0.00875256*acos(0.35008*x_1 - 1.35012) + 1)**2) + 1.8763*exp(-59.6338*(0.20405*(1 - 0.0406009*x_2)**(3/2) - 0.962894*sqrt(0.0720328*x_1 + 1) + 1)**2) - 0.961622*exp(-0.994971*(-1 + 0.839348*exp(-2.89*(1 - 0.451765*x_2)**2) + 0.573455*exp(-2.18437*(1 - 0.457387*x_1)**2))**2) - 0.368341*exp(-3.33792*(1 + 0.0960538/(0.481464 - x_2)**5)**2)`

### task=feynman_I_12_1 seed=15

- Task source: feynman_file
- Target formula: `mu*Nn`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=2.635321e-02, r2=0.998976
- Variant formula overview:
  - icbr_full: symbolic_s=2.891053e+00, imitation_mse=8.041531e-01, target_mse=8.364451e-01, formula_export_success=True
  - icbr_no_replay: symbolic_s=1.907354e+00, imitation_mse=1.046853e+00, target_mse=1.116883e+00, formula_export_success=True
  - icbr_no_shared: symbolic_s=4.379223e+00, imitation_mse=8.040316e-01, target_mse=8.363144e-01, formula_export_success=True
  - icbr_refit_commit: symbolic_s=5.174783e+00, imitation_mse=9.888800e-01, target_mse=1.031429e+00, formula_export_success=True
- icbr_full formula (display, rounded):
  - `46.0924*sqrt(-0.610161*(1 - 0.0322581*x_1)**(3/2) + sqrt(0.10989*x_2 + 1) + 0.581516) - 1.36339*log(2.65*(113.322*sqrt(0.0111111*x_1 + 1) - 0.190576*Abs(4.35*x_2 - 4.7) - 114.141)*(-8.53857*sqrt(0.0773481*x_2 + 1) + 1.41681*asin(0.3*x_1 - 1.05) + 10.0818) + 2.15) - 14.0746*acos(2.09153*log(0.15*x_2 + 4.5) - 4.61898 + 1.73402*exp(-0.64*(0.0625*x_1 - 1)**2)) - 0.36416*atan(0.479592*Abs(2.85*x_2 - 4.775) + 4.03681*acos(0.35*x_1 - 1.2) - 7.67866) - 17.9573 + 3.13988*exp(-1.95379*(0.0581245*Abs(2.3*x_1 - 3.2) - 1 - 0.118444/(0.84058 - x_2)**2)**2) + 5.30937*exp(-73.856*(-0.835452 + exp(-0.64*(0.0625*x_1 - 1)**2) + 0.197869/(0.333333 - x_2)**5)**2) + 1.60594*exp(-25.0*(-(0.0473043*Abs(2.65*x_1 - 4.95) + 0.174148)*(-0.160283*tan(0.5*x_2 - 5.0) - 1.28881*tanh(4.75*x_1 - 5.0) + 0.897703) - 0.33)**2)`
- icbr_no_replay formula (display, rounded):
  - `48.875*log(-1.36596*(1 - 0.0322581*x_1)**(3/2) - 0.3393*acos(0.3*x_2 - 1.0) + 6.96231) - 1.12895*tan(0.5*(-8.53857*sqrt(0.0773481*x_2 + 1) + 1.41681*asin(0.3*x_1 - 1.05) + 10.0818)*(-0.190576*Abs(4.35*x_2 - 4.7) - 3.44152 + 7.33736*exp(-(0.1*x_1 - 1.0)**2)) - 0.95) + 0.435895*tanh(-0.479592*Abs(2.85*x_2 - 4.775) + 4.03681*asin(0.35*x_1 - 1.2) + 1.38766) + 14.0746*asin(1.80907*sqrt(0.0777778*x_2 + 1) - 3.28283 + 1.73402*exp(-0.64*(0.0625*x_1 - 1)**2)) - 72.7886 + 3.13988*exp(-1.95379*(0.0581245*Abs(2.3*x_1 - 3.2) - 1 - 0.118444/(0.84058 - x_2)**2)**2) + 5.30937*exp(-126.816*(-0.647206 + 0.763143*exp(-0.64*(0.0625*x_1 - 1)**2) - exp(-25.0*(0.98 - x_2)**2))**2) + 1.60594*exp(-25.0*(-(0.0473043*Abs(2.65*x_1 - 4.95) + 0.174148)*(-0.160283*tan(0.5*x_2 - 5.0) + 0.618513*sign(4.0 - 3.4*x_1) + 0.239581) - 0.33)**2)`
- icbr_no_shared formula (display, rounded):
  - `45.9855*sqrt(-0.619468*(1 - 0.031746*x_1)**(3/2) + sqrt(0.10989*x_2 + 1) + 0.585273) - 1.36261*log(4.625*(113.322*sqrt(0.0111111*x_1 + 1) - 0.190576*Abs(4.35*x_2 - 4.7) - 114.141)*(-8.58141*sqrt(0.0769231*x_2 + 1) + 1.41681*asin(0.3*x_1 - 1.05) + 10.1244) + 3.75) - 14.0746*acos(2.11269*log(0.15*x_2 + 4.55) - 4.67407 + 1.73402*exp(-0.64*(0.0625*x_1 - 1)**2)) - 0.36416*atan(0.479592*Abs(2.85*x_2 - 4.775) + 4.03681*acos(0.35*x_1 - 1.2) - 7.67866) - 16.9655 + 3.13988*exp(-1.95379*(0.0581245*Abs(2.3*x_1 - 3.2) - 1 - 0.118444/(0.84058 - x_2)**2)**2) + 5.30937*exp(-73.856*(-0.835452 + exp(-0.64*(0.0625*x_1 - 1)**2) + 0.197869/(0.333333 - x_2)**5)**2) + 1.60594*exp(-25.0*(-(0.0473043*Abs(2.65*x_1 - 4.95) + 0.174148)*(-0.160283*tan(0.5*x_2 - 5.0) - 1.28881*tanh(4.75*x_1 - 5.0) + 0.897703) - 0.33)**2)`
- icbr_refit_commit formula (display, rounded):
  - `46.2392*sqrt(-0.612349*(1 - 0.0323955*x_1)**(3/2) + sqrt(0.110844*x_2 + 1) + 0.608105) - 1.36397*log(3.637*(104.58*sqrt(0.0120566*x_1 + 1) - 0.294824*Abs(2.8*x_2 - 1.30448) - 104.902)*(6.55446*sqrt(0.167522*x_1 + 1) - 9.04233*sqrt(0.072627*x_2 + 1) + 2.33678) + 2.95216) + 8.53316*acos(-3.453*log(0.0961199*x_2 + 2.90472) + 5.30631 - 1.87289*exp(-0.810288*(1 - 0.0844293*x_1)**2)) - 0.371315*atan(0.500101*Abs(2.74528*x_2 - 4.77744) - 3.64551*acos(1.2776 - 0.38304*x_1) + 4.67558) - 55.0754 + 62.8738*exp(-4.70238*(0.0101123*Abs(3.67192*x_1 - 4.86308) - 1 - 0.0296283/(0.851653 - x_2)**2)**2) + 449.699*exp(-13.9279*(-1 + 0.496685*exp(-0.81*(1 - 0.0888888*x_1)**2) + 0.156572/(0.333312 - x_2)**5)**2) + 3.63324*exp(-9.61124*(-(0.0504023*Abs(2.53688*x_1 - 4.99184) + 0.178074)*(-0.133389*tan(0.2998*x_2 - 4.856) - 1.32279*tanh(4.68*x_1 - 4.89996) + 0.833418) - 0.555035)**2)`

### task=feynman_I_12_1 seed=16

- Task source: feynman_file
- Target formula: `mu*Nn`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.986190e-02, r2=0.999265
- Variant formula overview:
  - icbr_full: symbolic_s=3.040909e+00, imitation_mse=nan, target_mse=nan, formula_export_success=True
  - icbr_no_replay: symbolic_s=1.975614e+00, imitation_mse=nan, target_mse=nan, formula_export_success=True
  - icbr_no_shared: symbolic_s=4.541059e+00, imitation_mse=nan, target_mse=nan, formula_export_success=True
  - icbr_refit_commit: symbolic_s=5.400330e+00, imitation_mse=nan, target_mse=nan, formula_export_success=True
- icbr_full formula (display, rounded):
  - `-2.54912*(0.0330796*tan(0.65*x_2 - 2.15) + 0.229217 - exp(-23.04*(0.9375 - x_1)**2))**3 + 50.7048*log(0.801041*sqrt(0.129412*x_1 + 1) + 0.0518477*Abs(2.3*x_2 - 2.75) + 3.773) - 1.80436*atanh(0.35*(42.0569*sqrt(0.0215054*x_1 + 1) - 21.7627*log(0.2*x_2 + 4.75) - 7.87566)*(0.157763*tan(0.65*x_1 - 2.15) - 0.0354091*Abs(2.95*x_2 - 4.9) + 0.389211) - 0.8) + 15.5237*atanh(0.0160639*Abs(3.05*x_2 - 3.6) - 0.667508 + 0.793073*exp(-(0.1*x_1 - 1.0)**2)) - 74.7354 + 1.00375*exp(-2.12334*(0.500193*asin(0.4*x_1 - 1.4) - 0.72272*sign(5.0 - 4.45*x_2) - 1)**2) + 3.13911*exp(-5.37599*(0.229748*tan(0.5*x_2 + 1.45) - 0.518103 - 1/(x_1 - 0.272727)**5)**2) + 4.42186*exp(-25.0*(-(-0.165874*tan(0.65*x_1 - 2.15) - 0.494951 + 0.615978*exp(-23.04*(0.9375 - x_2)**2))*(-0.158781*tanh(4.7*x_1 - 5.0) - 0.341695 + 1.33738*exp(-(0.1*x_2 - 1.0)**2)) - 0.4)**2)`
- icbr_no_replay formula (display, rounded):
  - `-0.093421*(0.0995885*tan(0.65*x_2 - 2.15) - sign(4.0 - 3.45*x_1) - 0.32139)**3 + 46.8865*sqrt(0.0226335*Abs(2.3*x_2 - 2.75) - 0.0611999*acos(0.3*x_1 - 1.0) + 1) - 15.2346*acos(0.0160639*Abs(3.05*x_2 - 3.6) - 0.817508 + 0.793073*exp(-(0.1*x_1 - 1.0)**2)) - 1.80436*atanh(0.35*(-19.0882*sqrt(0.0967742*x_2 + 1) + 17.5168 + 5.19462*exp(-(0.1*x_1 - 1.0)**2))*(0.157763*tan(0.65*x_1 - 2.15) - 0.0354091*Abs(2.95*x_2 - 4.9) + 0.389211) - 0.8) - 14.2884 + 3.13911*exp(-82.8128*(0.0807525*atanh(0.4*x_2 - 1.35) - 0.14542 - exp(-25.0*(1 - x_1)**2))**2) + 1.00375*exp(-40.8191*(0.114082*asin(0.4*x_1 - 1.4) - 0.0614447 - exp(-23.04*(0.833333 - x_2)**2))**2) + 4.42186*exp(-25.0*(-(-0.165874*tan(0.65*x_1 - 2.15) - 0.494951 + 0.615978*exp(-23.04*(0.9375 - x_2)**2))*(0.0266677*Abs(4.25*x_2 - 4.75) + 0.0829235*sign(4.0 - 3.4*x_1) + 0.189344) - 0.4)**2)`
- icbr_no_shared formula (display, rounded):
  - `2.54972*(-0.0330796*tan(0.65*x_2 - 2.15) - 0.229296 + exp(-23.04*(0.9375 - x_1)**2))**3 + 50.7048*log(0.801041*sqrt(0.129412*x_1 + 1) + 0.0518477*Abs(2.3*x_2 - 2.75) + 3.773) - 1.80436*atanh(0.35*(44.2501*sqrt(0.0204082*x_1 + 1) - 21.7627*log(0.2*x_2 + 4.75) - 10.0681)*(0.157763*tan(0.65*x_1 - 2.15) - 0.0354091*Abs(2.95*x_2 - 4.9) + 0.389211) - 0.8) + 15.5237*atanh(0.0146234*Abs(3.35*x_2 - 3.95) - 0.667552 + 0.793073*exp(-(0.1*x_1 - 1.0)**2)) - 74.7354 + 1.00375*exp(-2.12334*(0.500193*asin(0.4*x_1 - 1.4) - 0.72272*sign(5.0 - 4.45*x_2) - 1)**2) + 3.13911*exp(-5.37599*(0.229748*tan(0.5*x_2 + 1.45) - 0.518103 - 1/(x_1 - 0.272727)**5)**2) + 4.42186*exp(-25.0*(-(-0.165874*tan(0.65*x_1 - 2.15) - 0.494951 + 0.615978*exp(-23.04*(0.9375 - x_2)**2))*(-0.158781*tanh(4.7*x_1 - 5.0) - 0.341695 + 1.33738*exp(-(0.1*x_2 - 1.0)**2)) - 0.4)**2)`
- icbr_refit_commit formula (display, rounded):
  - `-15.3652*(0.0116697*tan(0.434*x_2 - 1.926) - 0.0285686 - exp(-7.54052*(0.619578 - x_1)**2))**3 + 51.6243*log(0.770168*sqrt(0.130119*x_1 + 1) + 0.0282484*Abs(4.04384*x_2 - 4.44444) + 3.72596) - 3.00808*atanh(0.23496*(41.2513*sqrt(0.0219386*x_1 + 1) - 21.7848*log(0.0973999*x_2 + 2.31588) - 22.6854)*(-0.142303*cos(0.942*x_2 - 4.69996) + 0.167163*tan(0.42588*x_1 + 4.3704) + 0.346434) - 0.77468) + 73.6463*atanh(0.00329811*Abs(2.41856*x_2 - 2.62196) - 0.611391 + 0.179443*exp(-0.810324*(1 - 0.0799839*x_1)**2)) - 39.4046 + 1.00056*exp(-1.6267*(-0.514092*asin(0.41852*x_1 - 1.41996) + 0.680384*sign(4.9996 - 4.494*x_2) + 1)**2) + 269.155*exp(-5.53921*(0.112422*tan(0.35544*x_2 + 1.7848) - 1 + 0.314643/(0.272411 - x_1)**5)**2) + 7.39806*exp(-10.1246*(-(-0.164377*tan(0.45412*x_1 - 1.95072) - 0.609361 + 11.8562*exp(-4.21678*(0.164657 - x_2)**2))*(-0.158871*tanh(4.7*x_1 - 4.99946) + 0.940381 - 0.77756*exp(-0.0351487*(-0.947728*x_2 - 1)**2)) - 0.570159)**2)`

### task=feynman_I_12_1 seed=17

- Task source: feynman_file
- Target formula: `mu*Nn`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.136978e-02, r2=0.999540
- Variant formula overview:
  - icbr_full: symbolic_s=3.060072e+00, imitation_mse=2.555362e-02, target_mse=3.149015e-02, formula_export_success=True
  - icbr_no_replay: symbolic_s=1.970076e+00, imitation_mse=3.574005e-02, target_mse=4.311816e-02, formula_export_success=True
  - icbr_no_shared: symbolic_s=4.370145e+00, imitation_mse=2.555421e-02, target_mse=3.148727e-02, formula_export_success=True
  - icbr_refit_commit: symbolic_s=5.300498e+00, imitation_mse=3.141677e-02, target_mse=3.132124e-02, formula_export_success=True
- icbr_full formula (display, rounded):
  - `-68.5674*((1 - 0.0414508*x_1)**(3/2) - 0.156125*cos(0.5*x_2 - 0.0499997) - 0.90251)**4 + 0.685425*(19.6807*sqrt(0.11*x_2 + 1) + 30.0312*log(0.15*x_1 + 4.95) - 68.6544)*(0.553199*atanh(0.35*x_2 - 1.15) - 2.07821 + 7.03159*exp(-(0.1*x_1 - 1.0)**2)) - 1.47688*(-0.204943*tan(0.6*x_2 + 4.35) + 0.0737083*Abs(3.65*x_1 - 4.2) - 1)**2 + 0.191953*(-0.0816723*Abs(3.35*x_2 - 4.775) + sign(4.0 - 3.45*x_1) + 0.297922)**2 - 0.762705*cos(0.147609*Abs(2.9*x_1 - 4.0) - 1.21538*asin(0.3*x_2 - 1.3) + 2.89418) - 8.40978*acos(-0.0653135*cos(0.45*x_1 + 0.1) + 0.18914*cos(0.3*x_2 - 2.5) - 0.368248) + 18.4437 - 2.00352*exp(-2.4025*(-(-0.837396*cos(0.9*x_2 + 1.7) - 0.0858484*Abs(2.35*x_1 - 4.4) - 2.03928)*(0.0786337*Abs(2.6*x_2 - 4.15) - 0.768153*asin(0.2*x_1 - 1.2) - 0.768559) + 1)**2)`
- icbr_no_replay formula (display, rounded):
  - `16.2155*sqrt(0.0114177*Abs(3.5*x_1 - 4.5) + 1 + 0.933162*exp(-(0.1*x_2 - 1.0)**2)) + 0.254218*tanh(-43.7668*sqrt(0.0555556*x_1 + 1) + 0.395923*Abs(3.55*x_2 - 4.6) + 47.418) + 0.171373*Abs(4.0*(29.9238*sqrt(0.0606061*x_1 + 1) + 2.99013*asin(0.3*x_2 - 1.0) - 27.5477)*(1.78312*sin(0.35*x_1 - 1.1) + 0.432797*asin(0.45*x_2 - 1.45) + 2.29612) - 2.35) + 0.162159*Abs(0.224899*Abs(3.35*x_2 - 4.775) + 2.75368*sign(3.45*x_1 - 4.0) - 1.06853) - 19.755 + 1.57433*exp(-0.244104*(-0.170721*Abs(2.9*x_1 - 4.0) + atanh(0.4*x_2 - 1.35) - 0.000243314)**2) - 2.42191*exp(-0.494412*(-0.47395*tan(0.6*x_2 + 4.35) + 0.170458*Abs(3.65*x_1 - 4.2) + 1)**2) - 2.00352*exp(-2.4025*(-(-0.0858484*Abs(2.35*x_1 - 4.4) - 0.239565*Abs(2.5*x_2 - 4.05) - 1.01683)*(0.0786337*Abs(2.6*x_2 - 4.15) - 0.421831*atanh(0.4*x_1 - 1.35) - 0.33196) + 1)**2)`
- icbr_no_shared formula (display, rounded):
  - `-68.5674*((1 - 0.0414508*x_1)**(3/2) - 0.156125*cos(0.5*x_2 - 0.0500002) - 0.90251)**4 + 0.685425*(19.7192*sqrt(0.109756*x_2 + 1) + 30.0312*log(0.15*x_1 + 4.95) - 68.6925)*(0.553199*atanh(0.35*x_2 - 1.15) - 2.07821 + 7.03159*exp(-(0.1*x_1 - 1.0)**2)) - 1.47688*(0.204943*tan(0.6*x_2 + 4.35) - 0.0737083*Abs(3.65*x_1 - 4.2) + 1)**2 + 0.191953*(-0.0816723*Abs(3.35*x_2 - 4.775) + sign(4.0 - 3.45*x_1) + 0.297922)**2 - 0.762705*cos(0.147609*Abs(2.9*x_1 - 4.0) - 1.21538*asin(0.3*x_2 - 1.3) + 2.89418) - 8.40978*acos(-0.0653135*cos(0.45*x_1 + 0.1) + 0.18914*cos(0.3*x_2 - 2.5) - 0.368248) + 18.4437 - 2.00352*exp(-2.4025*(-(-0.837396*cos(0.9*x_2 + 1.7) - 0.0858484*Abs(2.35*x_1 - 4.4) - 2.03928)*(0.0786337*Abs(2.6*x_2 - 4.15) - 0.768153*asin(0.2*x_1 - 1.2) - 0.768559) + 1)**2)`
- icbr_refit_commit formula (display, rounded):
  - `-80.9181*(0.955424*(1 - 0.0416418*x_1)**(3/2) + 0.0288174*Abs(2.37712*x_2 - 2.892) - 1)**4 + 0.685378*(19.9664*sqrt(0.108215*x_2 + 1) + 30.3876*log(0.0959999*x_1 + 3.20892) - 56.335)*(0.595544*atanh(0.33*x_2 - 1.1) - 1.98958 + 6.90843*exp(-1.01212*(1 - 0.101228*x_1)**2)) - 2.16465*(-0.239598*tan(0.3426*x_2 + 4.66136) + 0.0516033*Abs(4.28384*x_1 - 4.69384) - 1)**2 + 0.12386*(-0.0943567*Abs(3.51684*x_2 - 4.72336) + sign(4.79972 - 4.096*x_1) + 0.138069)**2 - 0.122591*Abs(-0.597354*Abs(3.5598*x_1 - 4.57984) + 6.18471*asin(0.30084*x_2 - 1.30084) + 2.17906) + 8.14757*acos(0.0618243*cos(0.50028*x_1 - 0.02192) + 7.33577*cos(0.00799999*x_2 - 4.9981) - 1.53124) - 6.85817 - 1.89495*exp(-2.53154*(-(0.831674*cos(0.89996*x_2 - 1.41272) - 0.0812902*Abs(2.53492*x_1 - 4.9874) - 2.03083)*(0.26963*Abs(0.75288*x_2 - 1.22364) - 0.77105*asin(0.1988*x_1 - 1.19876) - 0.76643) + 0.953491)**2)`

### task=feynman_I_12_1 seed=18

- Task source: feynman_file
- Target formula: `mu*Nn`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=5.351551e-03, r2=0.999787
- Variant formula overview:
  - icbr_full: symbolic_s=1.685718e+00, imitation_mse=5.138262e-03, target_mse=8.630076e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=1.180638e+00, imitation_mse=5.473472e-03, target_mse=8.172597e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=2.389867e+00, imitation_mse=5.137419e-03, target_mse=8.623638e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=2.993440e+00, imitation_mse=nan, target_mse=nan, formula_export_success=True
- icbr_full formula (display, rounded):
  - `122.892*sqrt(0.01*(16.3949*(1 - 0.0326087*x_2)**(3/2) - 30.3037*log(0.15*x_1 + 4.75) + 31.5797)*(-7.13194*sqrt(0.105263*x_1 + 1) + 11.8651 - 8.38056*exp(-0.64*(0.0625*x_2 - 1)**2)) + 1) + 12.009*sin(0.05*(2.22183*acos(0.3*x_2 - 1.05) - 5.67148)*(3.30128*acos(0.3*x_1 - 1.0) - 0.396003*asin(0.4*x_2 - 1.4) - 8.78252) - 0.35) - 8.8174*cos(-0.0602449*Abs(3.25*x_1 - 4.35) + 0.0463836*Abs(3.35*x_2 - 4.4) + 3.30641) - 127.189 + 0.586348*exp(-0.329282*(0.263263*Abs(2.9*x_2 - 3.85) - 1)**2)`
- icbr_no_replay formula (display, rounded):
  - `122.892*sqrt(0.01*(16.3949*(1 - 0.0326087*x_2)**(3/2) - 27.4637*sqrt(0.07*x_1 + 1) + 11.8293)*(-1.04206*asin(0.3*x_1 - 1.0) + 3.58099 - 8.38056*exp(-0.64*(0.0625*x_2 - 1)**2)) + 1) - 0.113827*(-0.371001*Abs(3.25*x_1 - 4.35) + 0.28564*Abs(3.35*x_2 - 4.4) + 1)**2 - 0.211633*sin(0.359439*Abs(2.9*x_2 - 3.85) - 2.93601) + 12.0125*cos(0.05*(-2.22183*asin(0.3*x_2 - 1.05) - 2.18144)*(-3.30128*asin(0.3*x_1 - 1.0) - 0.396003*asin(0.4*x_2 - 1.4) - 3.59688) - 1.9) - 118.243`
- icbr_no_shared formula (display, rounded):
  - `122.892*sqrt(0.01*(16.3949*(1 - 0.0326087*x_2)**(3/2) - 30.4496*log(0.15*x_1 + 4.775) + 31.9663)*(-7.13194*sqrt(0.105263*x_1 + 1) + 11.8651 - 8.38056*exp(-0.64*(0.0625*x_2 - 1)**2)) + 1) + 12.009*sin(0.05*(2.22183*acos(0.3*x_2 - 1.05) - 5.67148)*(3.30128*acos(0.3*x_1 - 1.0) - 0.396003*asin(0.4*x_2 - 1.4) - 8.78252) - 0.35) - 8.8174*cos(-0.0602449*Abs(3.25*x_1 - 4.35) + 0.0463836*Abs(3.35*x_2 - 4.4) + 3.30641) - 127.189 + 0.586348*exp(-0.329282*(0.263263*Abs(2.9*x_2 - 3.85) - 1)**2)`
- icbr_refit_commit formula (display, rounded):
  - `64.0128*sqrt(0.0200005*(16.1368*(1 - 0.0331605*x_2)**(3/2) - 30.9613*log(0.10244*x_1 + 3.32088) + 21.7795)*(-7.18843*sqrt(0.104328*x_1 + 1) + 9.94239 - 5.5199*exp(-0.810108*(1 - 0.0844387*x_2)**2)) + 1) - 0.117846*(-0.405471*Abs(2.83724*x_1 - 3.52204) + 0.25493*Abs(3.58212*x_2 - 4.29828) + 1)**2 + 355.254*sin(0.002*(1.78547*acos(0.36516*x_2 - 1.21848) - 4.87404)*(-21.1082*sqrt(0.113722*x_1 + 1) - 0.379574*asin(0.41828*x_2 - 1.42) + 21.192) - 0.60012) + 136.88 + 0.614674*exp(-0.33707*(0.188328*Abs(3.77824*x_2 - 4.56964) - 1)**2)`

### task=feynman_I_12_1 seed=19

- Task source: feynman_file
- Target formula: `mu*Nn`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=8.175789e-03, r2=0.999671
- Variant formula overview:
  - icbr_full: symbolic_s=2.551794e+00, imitation_mse=1.834862e-02, target_mse=2.585209e-02, formula_export_success=True
  - icbr_no_replay: symbolic_s=1.714815e+00, imitation_mse=2.204658e-02, target_mse=2.540806e-02, formula_export_success=True
  - icbr_no_shared: symbolic_s=3.616384e+00, imitation_mse=1.836823e-02, target_mse=2.583879e-02, formula_export_success=True
  - icbr_refit_commit: symbolic_s=4.203689e+00, imitation_mse=2.841577e-02, target_mse=3.686660e-02, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0.572068*(-17.8306*sqrt(0.1125*x_1 + 1) - 19.9914*log(0.15*x_2 + 4.975) + 50.6725)*(-31.4881*sqrt(0.0666667*x_2 + 1) - 1.0109*asin(0.3*x_1 - 1.0) + 31.0201) - 4.85717*(-0.00727608*Abs(3.65*x_1 - 4.2) - 0.00690326*Abs(4.5*x_2 - 4.875) + 1)**(3/2) - 0.0696562*sin(3.48583*asin(0.35*x_2 - 1.2) + 4.56472) - 0.359682*acos(0.112132*Abs(3.8*x_1 - 4.725) - 0.0361712*Abs(2.95*x_2 - 4.0) - 0.577037) + 6.60093 - 3.20956*exp(-2.78715*(-0.115614*Abs(2.45*x_1 - 3.0) + 0.070616*Abs(3.7*x_2 - 4.2) - 1)**2) - 1.44072*exp(-2.7225*(0.30303*(-2.84188*cos(0.35*x_2 + 0.45) - 0.198012*Abs(2.9*x_1 - 3.95) + 2.15506)*(-0.108927*Abs(3.4*x_1 - 4.9) - 0.0570579*Abs(3.15*x_2 - 4.85) - 0.609793) - 1)**2)`
- icbr_no_replay formula (display, rounded):
  - `-4.40861*(-0.114306*cos(0.3*x_2 - 2.5) - 0.00776161*Abs(3.65*x_1 - 4.2) + 1)**(3/2) + 0.0695187*cos(3.50389*asin(0.35*x_2 - 1.2) + 6.13526) - 0.198107*tan(-0.14951*Abs(3.8*x_1 - 4.725) + 0.0482283*Abs(2.95*x_2 - 4.0) + 3.93605) + 1.90689*Abs(0.3*(-31.4881*sqrt(0.0666667*x_2 + 1) - 1.0109*asin(0.3*x_1 - 1.0) + 31.0201)*(-18.1599*sqrt(0.0666667*x_2 + 1) - 2.76217*asin(0.3*x_1 - 1.0) + 15.8657) + 0.0999997) + 5.85522 - 3.20956*exp(-2.78715*(-0.115614*Abs(2.45*x_1 - 3.0) + 0.070616*Abs(3.7*x_2 - 4.2) - 1)**2) - 1.44072*exp(-2.7225*(0.30303*(-0.198012*Abs(2.9*x_1 - 3.95) + 0.368342*Abs(2.6*x_2 - 3.15) + 0.247254)*(-0.108927*Abs(3.4*x_1 - 4.9) - 0.0570579*Abs(3.15*x_2 - 4.85) - 0.609793) - 1)**2)`
- icbr_no_shared formula (display, rounded):
  - `0.572068*(-17.8662*sqrt(0.112245*x_1 + 1) - 19.9914*log(0.15*x_2 + 4.975) + 50.7078)*(-31.6486*sqrt(0.0662983*x_2 + 1) + 1.0109*acos(0.3*x_1 - 1.0) + 29.5921) + 11.8923*sqrt(0.00907926*Abs(3.6*x_1 - 4.15) + 0.00849411*Abs(4.5*x_2 - 4.875) + 1) - 0.0696562*sin(3.48583*asin(0.35*x_2 - 1.2) + 4.56472) - 0.359682*acos(0.10926*Abs(3.9*x_1 - 4.85) - 0.0361712*Abs(2.95*x_2 - 4.0) - 0.576999) - 10.1487 - 3.20956*exp(-2.78715*(-0.115614*Abs(2.45*x_1 - 3.0) + 0.070616*Abs(3.7*x_2 - 4.2) - 1)**2) - 1.44072*exp(-2.7225*(0.30303*(-2.84188*cos(0.35*x_2 + 0.45) - 0.198012*Abs(2.9*x_1 - 3.95) + 2.15506)*(-0.108927*Abs(3.4*x_1 - 4.9) - 0.0570579*Abs(3.15*x_2 - 4.85) - 0.609793) - 1)**2)`
- icbr_refit_commit formula (display, rounded):
  - `12.1743*sqrt(-0.470514*cos(0.0779999*x_2 + 1.39894) + 0.0126153*Abs(2.46404*x_1 - 2.67224) + 1) - 0.399467*tan(-0.109542*Abs(3.35828*x_1 - 3.86652) + 0.0433851*Abs(2.121*x_2 - 2.72716) + 3.66261) - 5.71863*Abs(0.10004*(17.9528*sqrt(0.111629*x_1 + 1) + 18.2348*sqrt(0.0663684*x_2 + 1) - 36.9556)*(6.32592*sqrt(0.116558*x_1 + 1) + 31.1824*sqrt(0.0673796*x_2 + 1) - 38.1643) - 3.6888) - 0.575002 + 10.9881*exp(-0.0339759*(0.212241*Abs(3.28832*x_1 - 3.69768) - 0.18933*Abs(3.43944*x_2 - 3.74284) - 1)**2) + 0.14331*exp(-8.77742*(0.599792*acos(1.22824 - 0.36912*x_2) - 1)**2) - 4.74198*exp(-3.55624*(-0.149369*(0.726314*sin(0.544*x_1 + 1.3009) - 0.0730923*Abs(2.35904*x_2 - 3.38584) - 1.32536)*(-2.96492*cos(0.334*x_2 + 0.50022) - 0.20777*Abs(2.70676*x_1 - 3.50544) + 2.1689) + 1)**2)`

### task=feynman_I_12_1 seed=20

- Task source: feynman_file
- Target formula: `mu*Nn`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=2.774611e-02, r2=0.998981
- Variant formula overview:
  - icbr_full: symbolic_s=3.011225e+00, imitation_mse=3.739345e-01, target_mse=3.784853e-01, formula_export_success=True
  - icbr_no_replay: symbolic_s=1.983885e+00, imitation_mse=4.255330e-01, target_mse=4.342880e-01, formula_export_success=True
  - icbr_no_shared: symbolic_s=4.330212e+00, imitation_mse=3.739345e-01, target_mse=3.784853e-01, formula_export_success=True
  - icbr_refit_commit: symbolic_s=5.266035e+00, imitation_mse=8.105809e-01, target_mse=8.857067e-01, formula_export_success=True
- icbr_full formula (display, rounded):
  - `3.8908*cos(-0.170011*acos(0.4*x_2 - 1.3) + 0.723082*atanh(0.4*x_1 - 1.4) + 4.59298) - 0.281088*Abs(0.423684*tan(0.7*x_1 - 2.2) - 1.38539*tan(0.55*x_2 + 4.45) + 0.959497) - 0.568464*atan(2.25*(0.152886*Abs(2.5*x_2 - 3.45) - 0.904206*atanh(0.35*x_1 - 1.3) - 0.790013)*(0.143094*Abs(3.35*x_2 - 4.875) - 0.792242*atanh(0.4*x_1 - 1.35) - 0.601408) - 0.95) + 23.7028*atanh(0.258568*cos(0.3*x_2 - 2.5) + 0.0668455*asin(0.4*x_1 - 1.35) - 0.105935) + 9.86613 + 3.85648*exp(-118.827*(tanh(4.925*x_2 - 5.0) - 0.0643834*acos(0.45*x_1 - 1.45) - 0.986143)**2) + 6.11562*exp(-2.79101*(0.299239*tan(0.6*x_2 - 2.1) + 0.222562*atanh(0.45*x_1 - 1.45) - 1)**2) + 2.61479/sqrt((-0.905291*sin(0.35*x_1 - 1.15) + 1.16771*cos(0.55*x_2 + 2.9) + 0.820962)*(-0.390092*sin(0.5*x_2 + 1.5) - 0.896952*atanh(0.3*x_1 - 1.0) - 0.329704) + 1)`
- icbr_no_replay formula (display, rounded):
  - `3.8908*cos(0.45517*tan(0.5*x_1 - 5.0) - 0.170011*acos(0.4*x_2 - 1.3) + 4.66997) - 0.849224*tan(0.65*(0.802452*cos(0.4*x_1 + 0.3) + 0.205367*Abs(2.85*x_2 - 3.8) - 0.291294)*(0.0595491*Abs(3.05*x_2 - 4.05) - 0.573943*asin(0.45*x_1 - 1.45) - 0.654204) - 0.85) - 0.281088*Abs(0.423684*tan(0.7*x_1 - 2.2) - 1.38539*tan(0.55*x_2 + 4.45) + 0.959497) - 23.2098*acos(0.0668455*asin(0.4*x_1 - 1.35) - 0.806085 + 0.886734*exp(-(0.1*x_2 - 1.0)**2)) + 50.7235 + 3.85648*exp(-118.39*(0.0645022*asin(0.45*x_1 - 1.45) - 0.0894055 - exp(-25.0*(0.97 - x_2)**2))**2) + 6.11562*exp(-2.79101*(0.299239*tan(0.6*x_2 - 2.1) + 0.222562*atanh(0.45*x_1 - 1.45) - 1)**2) + 1.29901*exp(-1.1025*((-0.412352*tan(0.6*x_1 + 4.35) + 0.152886*Abs(2.5*x_2 - 3.45) - 0.611722)*(0.143094*Abs(3.35*x_2 - 4.875) - 0.792242*atanh(0.4*x_1 - 1.35) - 0.601408) + 0.285714)**2)`
- icbr_no_shared formula (display, rounded):
  - `3.8908*cos(-0.170011*acos(0.4*x_2 - 1.3) + 0.723082*atanh(0.4*x_1 - 1.4) + 4.59298) - 0.281088*Abs(0.423684*tan(0.7*x_1 - 2.2) - 1.38539*tan(0.55*x_2 + 4.45) + 0.959497) - 0.568464*atan(2.25*(0.152886*Abs(2.5*x_2 - 3.45) - 0.904206*atanh(0.35*x_1 - 1.3) - 0.790013)*(0.143094*Abs(3.35*x_2 - 4.875) - 0.792242*atanh(0.4*x_1 - 1.35) - 0.601408) - 0.95) - 23.7028*atanh(-0.258568*cos(0.3*x_2 - 2.5) + 0.0668455*acos(0.4*x_1 - 1.35) + 0.000934476) + 9.86613 + 3.85648*exp(-140.474*(0.919729*tanh(4.925*x_2 - 5.0) + 0.0592153*asin(0.45*x_1 - 1.45) - 1)**2) + 6.11562*exp(-2.79101*(-0.299239*tan(0.6*x_2 - 2.1) - 0.222562*atanh(0.45*x_1 - 1.45) + 1)**2) + 2.61479/sqrt((-0.905291*sin(0.35*x_1 - 1.15) + 1.16771*cos(0.55*x_2 + 2.9) + 0.820962)*(-0.390092*sin(0.5*x_2 + 1.5) - 0.896952*atanh(0.3*x_1 - 1.0) - 0.329704) + 1)`
- icbr_refit_commit formula (display, rounded):
  - `-4.49578*cos(-0.164005*acos(0.38336*x_2 - 1.27804) + 0.666699*atanh(0.40028*x_1 - 1.40028) + 1.3362) - 0.244205*Abs(0.563012*tan(0.43652*x_1 + 4.3572) - 2.94889*tan(0.34488*x_2 + 4.85568) + 0.58104) - 0.567985*atan(2.2536*(-0.835663*sin(0.642*x_2 + 1.00084) - 0.858906*tan(0.38028*x_1 + 1.75388) + 0.194036)*(-0.709742*cos(0.60044*x_2 - 0.42176) - 0.823083*tan(0.363*x_1 - 1.46196) - 0.157808) - 0.95192) + 80.2397*atanh(0.00392353*Abs(4.676*x_2 - 4.9742) + 0.0175063*acos(1.27444 - 0.38212*x_1) - 0.495119) + 44.5169 + 583.662*exp(-24.5506*(0.45362*tanh(4.8*x_2 - 5.0) + 0.0405237*acos(1.4184 - 0.41844*x_1) - 1)**2) + 147.204*exp(-4.34986*(0.0287183*tan(0.12224*x_2 + 1.46556) + 0.147121*atanh(0.2644*x_1 - 1.18452) - 1)**2) + 2.61618/sqrt(0.999585*(0.750655*sin(0.432*x_1 - 4.49832) - 1.19122*cos(0.536*x_2 - 0.2) + 0.869291)*(-0.391258*sin(0.49996*x_2 - 4.80444) - 0.897116*atanh(0.29992*x_1 - 1.00016) - 0.323035) + 1)`

### task=feynman_I_12_4 seed=1

- Task source: feynman_file
- Target formula: `q1*r/(4*pi*epsilon*r**3)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=7.618417e-04, r2=-0.000199
- Variant formula overview:
  - icbr_full: symbolic_s=1.992265e+00, imitation_mse=2.994029e-09, target_mse=7.628362e-04, formula_export_success=True
  - icbr_no_replay: symbolic_s=1.331509e+00, imitation_mse=3.158076e-09, target_mse=7.628290e-04, formula_export_success=True
  - icbr_no_shared: symbolic_s=2.893313e+00, imitation_mse=2.994019e-09, target_mse=7.628362e-04, formula_export_success=True
  - icbr_refit_commit: symbolic_s=3.407260e+00, imitation_mse=3.163783e-09, target_mse=7.626546e-04, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0.000324212*(-0.704082*(-0.0880234*sign(4.0 - 3.4*x_1) - 0.162386)*(-0.646999 - 0.104529*exp(-3.4225*(1 - 0.459459*x_3)**2) + 0.52478*exp(-1.0*(1 - 0.55*x_1)**2)) + 1)**5 - 0.0014832*(0.002965*sign(3.5 - 2.9*x_2) - 0.034058*sign(3.9 - 3.35*x_1) - 1)**3 - 0.000150063*asin(0.254867*sin(1.3*x_3 + 5.0) - 0.0942179*sign(3.5 - 2.95*x_2) + 0.380296) + 0.0178597 - 2.68834e-5/((1 - 0.07*x_1)**(3/2) + 0.0242119*Abs(2.7*x_3 - 4.2) + 0.649211)**3 - 5.07051e-5/(-(0.0589299*Abs(2.15*x_2 - 4.0) + 0.174171)*(-0.0418686*sign(3.9 - 3.35*x_1) - 0.0567785) - 0.7)**4`
- icbr_no_replay formula (display, rounded):
  - `-0.00328875*(-(-0.014391 - 0.124949*exp(-25.0*(0.96 - x_1)**2))*(0.0589299*Abs(2.15*x_2 - 4.0) + 0.174171) + 0.52)**5 + 0.000693378*(-(-0.0880234*sign(4.0 - 3.4*x_1) - 0.162386)*(-0.102396*Abs(1.8*x_1 - 3.1) - 0.0791413 - 0.104529*exp(-3.4225*(1 - 0.459459*x_3)**2)) + 0.74)**3 - 0.0014832*(0.002965*sign(3.5 - 2.9*x_2) - 0.034058*sign(3.9 - 3.35*x_1) - 1)**3 - 0.000121409*atanh(-0.0931711*sign(3.5 - 2.95*x_2) + 0.169094 + 0.514094*exp(-3.24*(1 - 0.472222*x_3)**2)) + 0.0178104 - 2.64978e-6/(0.0111842*Abs(2.7*x_3 - 4.2) - 0.236621 + exp(-0.05*x_1))**3`
- icbr_no_shared formula (display, rounded):
  - `0.000324212*(-0.704082*(-0.0880234*sign(4.0 - 3.4*x_1) - 0.162386)*(-0.646999 - 0.104529*exp(-3.4225*(1 - 0.459459*x_3)**2) + 0.52478*exp(-1.0*(1 - 0.55*x_1)**2)) + 1)**5 - 0.0014832*(0.002965*sign(3.5 - 2.9*x_2) - 0.034058*sign(3.9 - 3.35*x_1) - 1)**3 + 0.000150063*acos(0.254867*sin(1.3*x_3 + 5.0) - 0.0942179*sign(3.5 - 2.95*x_2) + 0.380296) + 0.017624 - 2.68834e-5/((1 - 0.07*x_1)**(3/2) + 0.0242119*Abs(2.7*x_3 - 4.2) + 0.649211)**3 - 5.07053e-5/((0.0589299*Abs(2.15*x_2 - 4.0) + 0.174171)*(-0.0418686*sign(3.9 - 3.35*x_1) - 0.0567785) + 0.700001)**4`
- icbr_refit_commit formula (display, rounded):
  - `0.000309874*(-0.740067*(-0.0652883*sign(4.9757 - 4.2*x_1) - 0.14055)*(-0.672136 - 0.108472*exp(-2.5921*(1 - 0.444397*x_3)**2) + 0.552138*exp(-0.806476*(1 - 0.555922*x_1)**2)) + 1)**5 + 0.000702469*(0.0603114*sign(4.78116 - 4.121*x_1) - 0.00267472*sign(4.7996 - 4.292*x_2) + 1)**3 - 0.000105606*asin(0.113091*tanh(4.4*x_2 - 4.99952) + 0.411675 + 0.475235*exp(-2.54734*(1 - 0.454374*x_3)**2)) + 0.0186689 + 4.49687e-5/(-0.450571*(1 - 0.0764052*x_1)**(3/2) - 0.060703*tanh(0.618*x_3 - 2.09984) - 1)**3 - 5.03188e-5/(-(0.549232 - 0.347354*exp(-1.37734*(1 - 0.499932*x_2)**2))*(-0.0337653*sign(4.9757 - 4.2*x_1) - 0.048786) - 0.69896)**4`

### task=feynman_I_12_4 seed=2

- Task source: feynman_file
- Target formula: `q1*r/(4*pi*epsilon*r**3)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.093586e-03, r2=-0.513327
- Variant formula overview:
  - icbr_full: symbolic_s=9.603900e-03, imitation_mse=0.000000e+00, target_mse=1.093586e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=9.073600e-03, imitation_mse=0.000000e+00, target_mse=1.093586e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=8.411300e-03, imitation_mse=0.000000e+00, target_mse=1.093586e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=7.456200e-03, imitation_mse=0.000000e+00, target_mse=1.093586e-03, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0`
- icbr_no_replay formula (display, rounded):
  - `0`
- icbr_no_shared formula (display, rounded):
  - `0`
- icbr_refit_commit formula (display, rounded):
  - `0`

### task=feynman_I_12_4 seed=3

- Task source: feynman_file
- Target formula: `q1*r/(4*pi*epsilon*r**3)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=6.317526e-04, r2=-0.000872
- Variant formula overview:
  - icbr_full: symbolic_s=1.624929e-01, imitation_mse=0.000000e+00, target_mse=6.317526e-04, formula_export_success=True
  - icbr_no_replay: symbolic_s=1.325459e-01, imitation_mse=3.469447e-18, target_mse=6.317526e-04, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.599082e-01, imitation_mse=0.000000e+00, target_mse=6.317526e-04, formula_export_success=True
  - icbr_refit_commit: symbolic_s=2.272198e-01, imitation_mse=0.000000e+00, target_mse=6.317526e-04, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0.0188878000000000`
- icbr_no_replay formula (display, rounded):
  - `0.0188878000000000`
- icbr_no_shared formula (display, rounded):
  - `0.0188878000000000`
- icbr_refit_commit formula (display, rounded):
  - `0.0188878000000000`

### task=feynman_I_12_4 seed=4

- Task source: feynman_file
- Target formula: `q1*r/(4*pi*epsilon*r**3)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=7.571742e-04, r2=-0.002349
- Variant formula overview:
  - icbr_full: symbolic_s=8.224023e-01, imitation_mse=2.735728e-15, target_mse=7.571742e-04, formula_export_success=True
  - icbr_no_replay: symbolic_s=6.157222e-01, imitation_mse=4.905285e-15, target_mse=7.571740e-04, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.040488e+00, imitation_mse=2.731954e-15, target_mse=7.571742e-04, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.401606e+00, imitation_mse=1.394110e-14, target_mse=7.571747e-04, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0.0181915 - 1.97469e-5/(0.0204654*x_1 - 1)**5 + 0.000145905/(1 + 0.42619*exp(-0.05*x_1))**5 + 1.79852e-5/(0.802195 + exp(-0.05*x_3))**5`
- icbr_no_replay formula (display, rounded):
  - `0.0181866 + 2.45326e-5/(0.0215938*x_1 - 1)**4 + 2.50523e-5/(1 - 0.0129016*x_1)**5 + 1.79852e-5/(0.802195 + exp(-0.05*x_3))**5`
- icbr_no_shared formula (display, rounded):
  - `0.0181878 - 2.19091e-5/(0.00420012*Abs(4.975*x_1 - 5.0) - 1)**5 + 0.000157818/(1 + 0.770508*exp(-0.05*x_1))**3 - 1.79852e-5/(-0.802195 - exp(-0.05*x_3))**5`
- icbr_refit_commit formula (display, rounded):
  - `0.0181791 - 2.88137e-5/(0.0154903*x_1 - 1)**5 + 6.59075e-5/(1 + 0.363651*exp(-0.0999999*x_1))**3 - 9.0484e-6/(-1 - 0.304246*exp(-0.0619999*x_3))**5`

### task=feynman_I_12_4 seed=5

- Task source: feynman_file
- Target formula: `q1*r/(4*pi*epsilon*r**3)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=4.494367e-03, r2=-5.492441
- Variant formula overview:
  - icbr_full: symbolic_s=6.425542e-01, imitation_mse=1.089298e-11, target_mse=4.494326e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=5.068425e-01, imitation_mse=1.089298e-11, target_mse=4.494326e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=9.258974e-01, imitation_mse=1.089298e-11, target_mse=4.494326e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.050654e+00, imitation_mse=1.394065e-11, target_mse=4.494291e-03, formula_export_success=True
- icbr_full formula (display, rounded):
  - `-5.20283e-7*tan(5.0*(0.0601776*sign(3.85 - 3.3*x_2) + 0.0894599)*(0.00497909*sign(3.5 - 2.9*x_1) - 0.0562628*sign(4.0 - 3.4*x_2) + 0.0893502*sign(4.0 - 3.45*x_3) + 0.0515795) + 1.5) - 0.0417803`
- icbr_no_replay formula (display, rounded):
  - `-5.20283e-7*tan(5.0*(0.0601776*sign(3.85 - 3.3*x_2) + 0.0894599)*(0.00497909*sign(3.5 - 2.9*x_1) - 0.0562628*sign(4.0 - 3.4*x_2) + 0.0893502*sign(4.0 - 3.45*x_3) + 0.0515795) + 1.5) - 0.0417803`
- icbr_no_shared formula (display, rounded):
  - `-5.20283e-7*tan(5.0*(0.0601776*sign(3.85 - 3.3*x_2) + 0.0894599)*(0.00497909*sign(3.5 - 2.9*x_1) - 0.0562628*sign(4.0 - 3.4*x_2) + 0.0893502*sign(4.0 - 3.45*x_3) + 0.0515795) + 1.5) - 0.0417803`
- icbr_refit_commit formula (display, rounded):
  - `6.09477e-11*tan(2.96288*(0.0488547*sign(4.58376 - 3.8078*x_2) + 0.0786115)*(0.0755361*sign(4.73 - 4.046*x_3) + 0.0026497*sign(4.98866 - 4.4*x_1) - 0.045436*sign(4.999 - 4.192*x_2) + 0.0465964) + 1.6) - 0.0417877`

### task=feynman_I_12_4 seed=6

- Task source: feynman_file
- Target formula: `q1*r/(4*pi*epsilon*r**3)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=5.981217e-04, r2=-0.000014
- Variant formula overview:
  - icbr_full: symbolic_s=9.160189e-01, imitation_mse=3.067762e-09, target_mse=5.988560e-04, formula_export_success=True
  - icbr_no_replay: symbolic_s=7.491106e-01, imitation_mse=3.067762e-09, target_mse=5.988560e-04, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.204394e+00, imitation_mse=3.067762e-09, target_mse=5.988560e-04, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.598914e+00, imitation_mse=3.795769e-09, target_mse=5.990295e-04, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0.000281614*Abs(0.106399*Abs(2.35*x_2 - 4.4) + 0.278241*sign(3.2*x_1 - 3.75) + 0.135346*sign(3.35*x_3 - 3.95) - 0.765832) + 0.019532 + 1.5478e-9/(-(0.00542822*sign(3.4 - 2.85*x_3) + 0.00927669)*(-0.115723*sign(4.0 - 3.45*x_1) - 0.226673) + 0.0777778)**4`
- icbr_no_replay formula (display, rounded):
  - `0.000281614*Abs(0.106399*Abs(2.35*x_2 - 4.4) + 0.278241*sign(3.2*x_1 - 3.75) + 0.135346*sign(3.35*x_3 - 3.95) - 0.765832) + 0.0195354 + 2.1571e-10/(-(0.00542822*sign(3.4 - 2.85*x_3) + 0.00927669)*(-0.115723*sign(4.0 - 3.45*x_1) - 0.226673) + 0.0888889)**5`
- icbr_no_shared formula (display, rounded):
  - `0.000281614*Abs(0.106399*Abs(2.35*x_2 - 4.4) + 0.278241*sign(3.2*x_1 - 3.75) + 0.135346*sign(3.35*x_3 - 3.95) - 0.765832) + 0.019532 + 1.5478e-9/(-(0.00542822*sign(3.4 - 2.85*x_3) + 0.00927669)*(-0.115723*sign(4.0 - 3.45*x_1) - 0.226673) + 0.0777778)**4`
- icbr_refit_commit formula (display, rounded):
  - `-0.000388402*(-(-0.11039 - 3.40585*exp(-7.08624*(0.450714 - x_1)**2))*(0.00380397*sign(4.69834 - 3.778*x_3) + 0.00776682) + 1)**5 + 0.000153102*Abs(0.266659*Abs(1.37624*x_2 - 2.72708) - 0.344931*sign(4.7982 - 4.086*x_1) - 0.158661*sign(4.8966 - 4.0928*x_3) - 0.91832) + 0.0199775`

### task=feynman_I_12_4 seed=7

- Task source: feynman_file
- Target formula: `q1*r/(4*pi*epsilon*r**3)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=6.042366e-04, r2=-0.001834
- Variant formula overview:
  - icbr_full: symbolic_s=3.381456e-01, imitation_mse=7.098141e-17, target_mse=6.042366e-04, formula_export_success=True
  - icbr_no_replay: symbolic_s=2.696217e-01, imitation_mse=9.007378e-17, target_mse=6.042366e-04, formula_export_success=True
  - icbr_no_shared: symbolic_s=3.132961e-01, imitation_mse=7.098141e-17, target_mse=6.042366e-04, formula_export_success=True
  - icbr_refit_commit: symbolic_s=5.368817e-01, imitation_mse=1.092702e-16, target_mse=6.042366e-04, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0.0201977 + 2.34795e-5/(1 - 0.00380255*x_1)**5`
- icbr_no_replay formula (display, rounded):
  - `0.0201977 + 3.71029e-5/(1 + 0.0966495*exp(-0.05*x_1))**5`
- icbr_no_shared formula (display, rounded):
  - `0.0201977 + 2.34795e-5/(1 - 0.00380255*x_1)**5`
- icbr_refit_commit formula (display, rounded):
  - `0.0202047 - 1.64184e-5/(0.00529154*x_1 - 1)**5`

### task=feynman_I_12_4 seed=8

- Task source: feynman_file
- Target formula: `q1*r/(4*pi*epsilon*r**3)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=5.404748e-04, r2=0.000827
- Variant formula overview:
  - icbr_full: symbolic_s=1.540235e+00, imitation_mse=6.674118e-07, target_mse=5.413584e-04, formula_export_success=True
  - icbr_no_replay: symbolic_s=1.034624e+00, imitation_mse=6.686903e-07, target_mse=5.410440e-04, formula_export_success=True
  - icbr_no_shared: symbolic_s=2.117468e+00, imitation_mse=6.664672e-07, target_mse=5.416101e-04, formula_export_success=True
  - icbr_refit_commit: symbolic_s=2.608038e+00, imitation_mse=6.743804e-07, target_mse=5.415528e-04, formula_export_success=True
- icbr_full formula (display, rounded):
  - `-0.000241108*(1 - 0.656719*cos(1.05*x_3 + 4.35))**(3/2) - 8.35141e-5*(0.718276*sign(3.45 - 2.95*x_3) + 1)**(3/2) - 0.000688565*sign(-1.60719 + 1.37777*exp(-1.21*(1 - 0.545455*x_3)**2)) + 0.019294 - 1.51556e-5*exp(-25.0*((0.629396 - 0.398882*exp(-1.5625*(1 - 0.52*x_2)**2))*(-0.343815*cos(0.95*x_1 + 4.7) - 0.0634887*Abs(2.95*x_3 - 4.925) + 0.502687) + 0.19)**2) - 8.74976e-8/(-0.621782*cos(0.85*x_1 + 1.85) - 1)**5`
- icbr_no_replay formula (display, rounded):
  - `-8.35141e-5*(0.718276*sign(3.45 - 2.95*x_3) + 1)**(3/2) - 5.3294e-6*sign(-5.0*(0.0677087*Abs(2.25*x_2 - 4.1) + 0.206686)*(0.0885378*Abs(2.85*x_1 - 4.7) - 0.0634887*Abs(2.95*x_3 - 4.925) + 0.0829649) + 0.0499997) + 0.0193424 + 0.000610222*exp(-0.0644084*(0.0977067 - Abs(1.75*x_3 - 3.05))**2) + 1.36475e-5/(-0.671277*Abs(2.65*x_3 - 4.5) - 1)**5 - 9.39312e-5/(-0.665532*Abs(2.6*x_1 - 4.15) - 1)**5`
- icbr_no_shared formula (display, rounded):
  - `-0.000241108*(1 - 0.656719*cos(1.05*x_3 + 4.35))**(3/2) - 0.000242918*Abs(0.458927*sign(2.95*x_3 - 3.45) - 0.486929) + 0.000688565*sign(1.60719 - 1.37777*exp(-1.21*(1 - 0.545455*x_3)**2)) + 0.0193014 - 1.51556e-5*exp(-25.0*((0.629396 - 0.398882*exp(-1.5625*(1 - 0.52*x_2)**2))*(-0.343815*cos(0.95*x_1 + 4.7) - 0.0634887*Abs(2.95*x_3 - 4.925) + 0.502687) + 0.19)**2) - 8.74976e-8/(-0.621782*cos(0.85*x_1 + 1.85) - 1)**5`
- icbr_refit_commit formula (display, rounded):
  - `-0.000884952*(1 - 0.176046*cos(1.038*x_3 - 1.89998))**(3/2) - 0.000592892*(0.0682262*sign(4.89904 - 4.192*x_3) + 1)**(3/2) - 1.84244e-5*sign(-0.959798 + 1.17327*exp(-0.796449*(1 - 0.562279*x_3)**2)) + 0.0211015 + 1.33328e-5*exp(-25.0*(-(0.668738 - 0.425098*exp(-1.21*(1 - 0.512727*x_2)**2))*(0.3525*cos(0.9006*x_1 - 4.6056) - 0.249907*cos(0.99992*x_3 + 1.40864) + 0.209404) + 0.16)**2) - 5.49466e-7/(-0.53277*cos(0.838*x_1 - 4.39992) - 1)**5`

### task=feynman_I_12_4 seed=9

- Task source: feynman_file
- Target formula: `q1*r/(4*pi*epsilon*r**3)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=6.036269e-04, r2=-0.005880
- Variant formula overview:
  - icbr_full: symbolic_s=1.378139e+00, imitation_mse=6.092929e-08, target_mse=6.038004e-04, formula_export_success=True
  - icbr_no_replay: symbolic_s=1.003276e+00, imitation_mse=6.015639e-08, target_mse=6.037077e-04, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.990250e+00, imitation_mse=6.092929e-08, target_mse=6.038004e-04, formula_export_success=True
  - icbr_refit_commit: symbolic_s=2.353505e+00, imitation_mse=5.993275e-08, target_mse=6.036541e-04, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0.000547712*(-0.00898675*sign(3.3 - 2.75*x_2) - 1)**5 - 0.00100557*sign(0.0461897*cos(1.2*x_1 - 2.5) - 0.213476*Abs(2.2*x_2 - 3.85) - 0.183277) + 0.0196137 - 5.92223e-5/((-0.0826221*sign(3.2 - 2.7*x_1) - 0.122825)*(0.0696587*sign(3.7 - 3.2*x_2) + 0.152137) + 0.700001)**5`
- icbr_no_replay formula (display, rounded):
  - `0.000547712*(-0.00898675*sign(3.3 - 2.75*x_2) - 1)**5 - 0.00100557*sign(-0.213476*Abs(2.2*x_2 - 3.85) - 0.226057 + 0.0949024*exp(-2.4025*(1 - 0.483871*x_1)**2)) + 0.0196018 - 2.02868e-5/(-0.458521*Abs(1.95*x_2 - 3.35) - 1 + 0.308427*exp(-2.89*(1 - 0.470588*x_1)**2))**5 - 5.92223e-5/((-0.0826221*sign(3.2 - 2.7*x_1) - 0.122825)*(0.0696587*sign(3.7 - 3.2*x_2) + 0.152137) + 0.700001)**5`
- icbr_no_shared formula (display, rounded):
  - `0.000553261*(-0.00889789*sign(3.3 - 2.75*x_2) - 1)**5 - 0.00100557*sign(0.0461897*cos(1.2*x_1 - 2.5) - 0.213476*Abs(2.2*x_2 - 3.85) - 0.183277) + 0.0196193 - 5.92223e-5/((-0.0826221*sign(3.2 - 2.7*x_1) - 0.122825)*(0.0696587*sign(3.7 - 3.2*x_2) + 0.152137) + 0.700001)**5`
- icbr_refit_commit formula (display, rounded):
  - `-0.000527833*(-(0.0939882 - 0.0245333*sign(4.998 - 1.4266*x_2))*(-0.0642868*sign(4.604 - 3.84796*x_1) - 0.105919) + 0.999996)**5 + 0.000399265*(-0.00853418*sign(4.9966 - 3.89504*x_2) - 1)**5 - 4.07418e-6*sign(0.0482899*cos(1.20008*x_1 - 2.50032) - 0.205526*Abs(2.41276*x_2 - 4.4158) + 0.241129) + 1.16583e-5*sign(-0.0404735*Abs(1.63976*x_1 - 3.38192) - 0.20915*Abs(2.2066*x_2 - 3.9166) + 0.282296) + 0.0206579`

### task=feynman_I_12_4 seed=10

- Task source: feynman_file
- Target formula: `q1*r/(4*pi*epsilon*r**3)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=6.541178e-04, r2=0.001329
- Variant formula overview:
  - icbr_full: symbolic_s=1.056995e+00, imitation_mse=2.897517e-08, target_mse=6.532336e-04, formula_export_success=True
  - icbr_no_replay: symbolic_s=7.622683e-01, imitation_mse=2.967843e-08, target_mse=6.532349e-04, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.388638e+00, imitation_mse=2.897517e-08, target_mse=6.532336e-04, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.844335e+00, imitation_mse=3.861398e-08, target_mse=6.534199e-04, formula_export_success=True
- icbr_full formula (display, rounded):
  - `-0.000169643*(-0.610124*sign(4.0 - 3.4*x_2) + 1 + 1.67488e-5/(1 - 0.876405*x_1)**2)**(3/2) + 0.000161564*sign(-0.354654 + 0.533928*exp(-3.0625*(1 - 0.457143*x_3)**2)) + 0.0185593 - 2.09901e-11/((0.147769*Abs(2.05*x_2 - 3.55) + 0.397362)*(0.000166775*Abs(2.9*x_3 - 4.5) + 0.000578423) + 0.04)**4`
- icbr_no_replay formula (display, rounded):
  - `-0.000253566*(-0.297041*sign(4.0 - 3.4*x_2) + 1 + 8.15419e-6/(1 - 0.876405*x_1)**2)**2 + 0.000161564*sign(-0.354654 + 0.533928*exp(-3.0625*(1 - 0.457143*x_3)**2)) + 0.0186398 - 2.09901e-11/((0.147769*Abs(2.05*x_2 - 3.55) + 0.397362)*(0.000166775*Abs(2.9*x_3 - 4.5) + 0.000578423) + 0.04)**4`
- icbr_no_shared formula (display, rounded):
  - `-0.000169643*(-0.610124*sign(4.0 - 3.4*x_2) + 1 + 1.67488e-5/(1 - 0.876405*x_1)**2)**(3/2) + 0.000161564*sign(-0.354654 + 0.533928*exp(-3.0625*(1 - 0.457143*x_3)**2)) + 0.0185593 - 2.09901e-11/((0.147769*Abs(2.05*x_2 - 3.55) + 0.397362)*(0.000166775*Abs(2.9*x_3 - 4.5) + 0.000578423) + 0.04)**4`
- icbr_refit_commit formula (display, rounded):
  - `0.00114264*(0.0743456*sign(4.99956 - 4.294*x_2) + 1 - 0.0026285/(0.544478 - x_1)**2)**(3/2) + 8.91827e-5*sign(-0.312203 + 0.565701*exp(-2.57859*(1 - 0.443841*x_3)**2)) + 0.017138 - 1.54995e-12/(-(0.120081*Abs(2.538*x_2 - 4.56436) + 0.40714)*(0.000145743*Abs(3.16952*x_3 - 4.4976) + 0.000564582) - 0.0232432)**4`

### task=feynman_I_12_4 seed=11

- Task source: feynman_file
- Target formula: `q1*r/(4*pi*epsilon*r**3)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=8.037632e-04, r2=-0.000112
- Variant formula overview:
  - icbr_full: symbolic_s=3.181438e-01, imitation_mse=2.967952e-13, target_mse=8.037648e-04, formula_export_success=True
  - icbr_no_replay: symbolic_s=2.720873e-01, imitation_mse=2.967952e-13, target_mse=8.037648e-04, formula_export_success=True
  - icbr_no_shared: symbolic_s=3.151769e-01, imitation_mse=2.967952e-13, target_mse=8.037648e-04, formula_export_success=True
  - icbr_refit_commit: symbolic_s=5.565694e-01, imitation_mse=3.078724e-13, target_mse=8.037657e-04, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0.019752 - 4.2583e-6/(0.00796999*Abs(2.8*x_3 - 3.9) - 1)**5`
- icbr_no_replay formula (display, rounded):
  - `0.019752 - 4.2583e-6/(0.00796999*Abs(2.8*x_3 - 3.9) - 1)**5`
- icbr_no_shared formula (display, rounded):
  - `0.019752 - 4.2583e-6/(0.00796999*Abs(2.8*x_3 - 3.9) - 1)**5`
- icbr_refit_commit formula (display, rounded):
  - `0.0197508 - 5.46448e-6/(0.00453584*Abs(3.884*x_3 - 4.89996) - 1)**5`

### task=feynman_I_12_4 seed=12

- Task source: feynman_file
- Target formula: `q1*r/(4*pi*epsilon*r**3)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=7.019500e-04, r2=0.001951
- Variant formula overview:
  - icbr_full: symbolic_s=1.536184e+00, imitation_mse=2.900351e-08, target_mse=7.017696e-04, formula_export_success=True
  - icbr_no_replay: symbolic_s=1.108464e+00, imitation_mse=2.926098e-08, target_mse=7.018021e-04, formula_export_success=True
  - icbr_no_shared: symbolic_s=2.219029e+00, imitation_mse=2.900350e-08, target_mse=7.017696e-04, formula_export_success=True
  - icbr_refit_commit: symbolic_s=2.635295e+00, imitation_mse=4.147761e-08, target_mse=7.032432e-04, formula_export_success=True
- icbr_full formula (display, rounded):
  - `-0.00389422*(1 - 0.00142443*sign(3.1 - 2.6*x_1))**5 + 0.00134455*(-(-0.104934*sign(4.0 - 3.4*x_3) - 0.149255)*(-0.0996744*tanh(5.0*x_2 - 5.0) + 0.0762529 - 0.308889*exp(-23.04*(0.9375 - x_3)**2)) - 0.59)**4 + 0.000109296*(0.0433778*tanh(4.925*x_1 - 5.0) - 1)**5 + 0.000108254*sign(0.268404 - 0.181788*Abs(2.55*x_2 - 4.7)) + 0.000153545*sign(0.409135*sign(3.9 - 3.35*x_3) + 0.213127) + 0.0226523`
- icbr_no_replay formula (display, rounded):
  - `-0.00389422*(1 - 0.00142443*sign(3.1 - 2.6*x_1))**5 - 0.000691519*(-(-0.104934*sign(4.0 - 3.4*x_3) - 0.149255)*(0.0354375*sign(3.85 - 3.3*x_2) - 0.103971*sign(4.5 - 3.95*x_3) - 0.0927096) - 0.75)**5 + 9.58116e-5*(-0.0176159*sign(3.95 - 3.4*x_1) - 1)**5 + 0.000108254*sign(0.268404 - 0.181788*Abs(2.55*x_2 - 4.7)) + 0.000153545*sign(0.409135*sign(3.9 - 3.35*x_3) + 0.213127) + 0.0226512`
- icbr_no_shared formula (display, rounded):
  - `-0.00389422*(1 - 0.00142443*sign(3.1 - 2.6*x_1))**5 + 0.00134455*(-(-0.104934*sign(4.0 - 3.4*x_3) - 0.149255)*(-0.0996744*tanh(5.0*x_2 - 5.0) + 0.0762529 - 0.308889*exp(-23.04*(0.9375 - x_3)**2)) - 0.59)**4 + 0.000108802*(0.0435991*tanh(4.925*x_1 - 5.0) - 1)**5 + 0.000108254*sign(0.268404 - 0.181788*Abs(2.55*x_2 - 4.7)) + 0.000153545*sign(0.409135*sign(3.9 - 3.35*x_3) + 0.213127) + 0.0226518`
- icbr_refit_commit formula (display, rounded):
  - `0.000289603*((-0.0822532*sign(4.9991 - 4.19*x_3) - 0.127311)*(-0.0996707*tanh(4.99986*x_2 - 4.99988) + 0.0765345 - 1.15367*exp(-7.02144*(0.56519 - x_3)**2)) + 1)**4 + 8.14409e-5*(0.0633499*tanh(4.856*x_1 - 4.89954) - 1)**5 + 0.000164672*(0.0242691*sign(4.79836 - 3.89*x_1) + 1)**5 + 7.91095e-5*sign(0.484662 - 0.205741*Abs(1.58668*x_2 - 3.07668)) + 1.06636e-7*sign(0.489054*sign(4.99962 - 4.288*x_3) - 0.456994) + 0.0182546`

### task=feynman_I_12_4 seed=13

- Task source: feynman_file
- Target formula: `q1*r/(4*pi*epsilon*r**3)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=5.430167e-04, r2=-0.009126
- Variant formula overview:
  - icbr_full: symbolic_s=3.323079e-01, imitation_mse=3.363434e-14, target_mse=5.430165e-04, formula_export_success=True
  - icbr_no_replay: symbolic_s=2.856537e-01, imitation_mse=3.375482e-14, target_mse=5.430165e-04, formula_export_success=True
  - icbr_no_shared: symbolic_s=3.425785e-01, imitation_mse=3.363434e-14, target_mse=5.430165e-04, formula_export_success=True
  - icbr_refit_commit: symbolic_s=4.924873e-01, imitation_mse=3.422861e-14, target_mse=5.430164e-04, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0.0197606 - 0.000129465/(0.33496 + exp(-0.05*x_3))**2`
- icbr_no_replay formula (display, rounded):
  - `0.0197454 - 0.000728114/(-1 - 0.886556*exp(-0.05*x_3))**4`
- icbr_no_shared formula (display, rounded):
  - `0.0197606 - 0.000129465/(0.33496 + exp(-0.05*x_3))**2`
- icbr_refit_commit formula (display, rounded):
  - `0.0197591 - 0.0001403/(-0.404588 - exp(-0.0539999*x_3))**2`

### task=feynman_I_12_4 seed=14

- Task source: feynman_file
- Target formula: `q1*r/(4*pi*epsilon*r**3)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=4.482468e-04, r2=-0.018556
- Variant formula overview:
  - icbr_full: symbolic_s=6.964925e-01, imitation_mse=1.525921e-12, target_mse=4.482435e-04, formula_export_success=True
  - icbr_no_replay: symbolic_s=5.306046e-01, imitation_mse=1.545481e-12, target_mse=4.482430e-04, formula_export_success=True
  - icbr_no_shared: symbolic_s=8.785175e-01, imitation_mse=1.518145e-12, target_mse=4.482427e-04, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.238055e+00, imitation_mse=4.482374e-12, target_mse=4.482614e-04, formula_export_success=True
- icbr_full formula (display, rounded):
  - `-0.0199316*(-0.000436228*x_2 - 0.00015864*Abs(2.85*x_3 - 3.45) + 1)**5 + 0.0391873 - 7.87619e-6/(0.0382509*x_3 - 1)**3`
- icbr_no_replay formula (display, rounded):
  - `-0.0199316*(-0.000436228*x_2 - 0.00015864*Abs(2.85*x_3 - 3.45) + 1)**5 + 0.0391899 + 5.45412e-6/(1 - 0.0371182*x_3)**4`
- icbr_no_shared formula (display, rounded):
  - `0.0199315*(0.000436228*x_2 + 0.000161566*Abs(2.8*x_3 - 3.4) - 1)**5 + 0.0391873 + 7.87619e-6/(1 - 0.0382509*x_3)**3`
- icbr_refit_commit formula (display, rounded):
  - `0.0245376*(0.000435883*x_2 + 9.47332e-5*Abs(4.698*x_3 - 4.96728) + 1)**4 - 0.00528421 - 3.90418e-7/(-0.435386*(-0.0108004*x_3 - 1)**3 - 1)**5`

### task=feynman_I_12_4 seed=15

- Task source: feynman_file
- Target formula: `q1*r/(4*pi*epsilon*r**3)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=7.240190e-04, r2=-0.004617
- Variant formula overview:
  - icbr_full: symbolic_s=6.048437e-01, imitation_mse=1.704978e-07, target_mse=7.214854e-04, formula_export_success=True
  - icbr_no_replay: symbolic_s=5.108120e-01, imitation_mse=1.727542e-07, target_mse=7.214493e-04, formula_export_success=True
  - icbr_no_shared: symbolic_s=6.978644e-01, imitation_mse=1.704978e-07, target_mse=7.214854e-04, formula_export_success=True
  - icbr_refit_commit: symbolic_s=9.755553e-01, imitation_mse=1.736078e-07, target_mse=7.212697e-04, formula_export_success=True
- icbr_full formula (display, rounded):
  - `-4.05244e-5*tan(0.259947*Abs(2.9*x_1 - 4.825) + 1.85523) - 0.00122381*sign(0.758987*cos(0.95*x_1 + 4.65) - 1.07106) + 0.0182588`
- icbr_no_replay formula (display, rounded):
  - `-4.05244e-5*tan(0.259947*Abs(2.9*x_1 - 4.825) + 1.85523) + 0.0194921 + 2.85906e-5/(-0.599926*Abs(3.0*x_1 - 4.975) - 1)**5`
- icbr_no_shared formula (display, rounded):
  - `-4.05244e-5*tan(0.259947*Abs(2.9*x_1 - 4.825) + 1.85523) - 0.00122381*sign(0.758987*cos(0.95*x_1 + 4.65) - 1.07106) + 0.0182588`
- icbr_refit_commit formula (display, rounded):
  - `0.0194179 - 5.6276e-7*tan(0.00151754*Abs(2.73852*x_1 - 4.77072) + 4.71544)`

### task=feynman_I_12_4 seed=16

- Task source: feynman_file
- Target formula: `q1*r/(4*pi*epsilon*r**3)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=8.866242e-04, r2=0.028178
- Variant formula overview:
  - icbr_full: symbolic_s=2.647660e+00, imitation_mse=7.467645e-07, target_mse=9.076842e-04, formula_export_success=True
  - icbr_no_replay: symbolic_s=1.736790e+00, imitation_mse=7.817978e-07, target_mse=9.078960e-04, formula_export_success=True
  - icbr_no_shared: symbolic_s=3.913401e+00, imitation_mse=7.477847e-07, target_mse=9.078914e-04, formula_export_success=True
  - icbr_refit_commit: symbolic_s=4.468501e+00, imitation_mse=7.657046e-07, target_mse=9.080615e-04, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0.000397531*sin(0.145936*Abs(2.6*x_2 - 4.7) - 3.56 + 1.03707*exp(-1.96*(1 - 0.5*x_3)**2)) - 0.00100538*cos(0.164404*Abs(2.2*x_2 - 3.35) - 0.191659*Abs(2.25*x_3 - 4.25) + 0.272709) + 0.0196314 + 0.000236501*exp(-4.12633*(0.951188*tanh(5.0*x_2 - 4.6) - 1)**2) + 0.00097077*exp(-21.3906*(-(0.418536*tanh(5.0*x_3 - 5.0) - 0.0598962*Abs(2.55*x_1 - 4.7) + 0.0998299*Abs(3.0*x_2 - 4.4) - 0.343726)*(0.0555594*Abs(2.6*x_2 - 4.1) - 0.0710227*sign(4.0 - 3.4*x_1) + 0.0242832 - 0.258449*exp(-25.0*(0.97 - x_3)**2)) - 0.0216217)**2) + 0.000400622/(0.680935*Abs(2.45*x_3 - 4.0) + 1)**3 - 1.67029e-11/(-(0.0621047*sin(0.6*x_3 + 1.2) + 0.29509*cos(0.45*x_2 + 0.1) - 0.460598)*(-0.0076165*Abs(2.75*x_2 - 4.675) - 0.222377 + 0.123792*exp(-2.89*(1 - 0.470588*x_1)**2)) - 0.02)**5`
- icbr_no_replay formula (display, rounded):
  - `2.46416e-7*(0.857797*Abs(2.2*x_2 - 3.35) - Abs(2.25*x_3 - 4.25) + 0.829978)**4 - 0.000397531*sin(-0.145936*Abs(2.6*x_2 - 4.7) + 0.162584*Abs(2.45*x_3 - 4.55) + 2.48137) + 0.0187639 + 0.000236501*exp(-0.274115*(-0.801239*sign(4.5 - 3.9*x_2) - 1)**2) + 0.00097077*exp(-21.3906*(-(-0.0598962*Abs(2.55*x_1 - 4.7) + 0.0998299*Abs(3.0*x_2 - 4.4) - 0.139885*sign(3.9 - 3.35*x_3) - 0.0671148)*(0.0555594*Abs(2.6*x_2 - 4.1) - 0.0970507*sign(3.9 - 3.35*x_3) - 0.0710227*sign(4.0 - 3.4*x_1) - 0.0736905) - 0.0216217)**2) + 0.00033194/(0.498711*Abs(2.45*x_3 - 4.0) + 1)**5 - 1.67029e-11/(-(-0.0076165*Abs(2.75*x_2 - 4.675) - 0.222377 + 0.123792*exp(-2.89*(1 - 0.470588*x_1)**2))*(-0.0337429*Abs(3.7*x_2 - 4.7) - 0.0117493*Abs(2.85*x_3 - 4.0) - 0.149865) - 0.02)**5`
- icbr_no_shared formula (display, rounded):
  - `0.000397531*sin(0.145936*Abs(2.6*x_2 - 4.7) - 3.56 + 1.03707*exp(-1.96*(1 - 0.5*x_3)**2)) - 0.00100538*cos(0.164404*Abs(2.2*x_2 - 3.35) - 0.191659*Abs(2.25*x_3 - 4.25) + 0.272709) + 0.019638 + 0.00097077*exp(-21.3906*((0.418536*tanh(5.0*x_3 - 5.0) - 0.0598962*Abs(2.55*x_1 - 4.7) + 0.133106*Abs(2.25*x_2 - 3.3) - 0.343726)*(0.0555594*Abs(2.6*x_2 - 4.1) - 0.0710227*sign(4.0 - 3.4*x_1) + 0.0242832 - 0.258449*exp(-25.0*(0.97 - x_3)**2)) + 0.0216216)**2) + 0.000236501*exp(-4.12633*(1 - 0.951188*tanh(5.0*x_2 - 4.6))**2) + 0.000364792/(0.7046*Abs(2.45*x_3 - 4.0) + 1)**3 - 1.67029e-11/(-(0.0621047*sin(0.6*x_3 + 1.2) + 0.29509*cos(0.45*x_2 + 0.1) - 0.460598)*(-0.0076165*Abs(2.75*x_2 - 4.675) - 0.222377 + 0.123792*exp(-2.89*(1 - 0.470588*x_1)**2)) - 0.02)**5`
- icbr_refit_commit formula (display, rounded):
  - `-0.000324492*sin(0.192444*Abs(2.21292*x_2 - 4.2234) - 0.922896 + 1.20799*exp(-1.3924*(1 - 0.499254*x_3)**2)) + 0.00046345*cos(-0.150684*Abs(3.65516*x_2 - 4.97192) + 0.497149*Abs(1.42132*x_3 - 2.818) + 2.74149) - 0.000624555*atan(4.99999*(-0.210602*cos(0.836*x_2 - 1.2) - 0.0563313*sign(4.99046 - 4.2*x_1) + 0.288309 - 0.820605*exp(-7.53217*(0.625605 - x_3)**2))*(0.41899*tanh(4.9999*x_3 - 4.9991) - 0.105483*Abs(1.47172*x_1 - 2.84576) + 0.0784852*Abs(3.6436*x_2 - 4.75456) - 0.364854) - 0.6) + 0.0196691 + 0.00017674*exp(-0.548608*(-0.515092*sign(4.96228 - 4.4*x_2) - 1)**2) + 0.000332546/(0.784233*Abs(2.00956*x_3 - 3.41396) + 1)**3 - 6.76345e-14/(-(0.0621034*sin(0.6*x_3 + 1.2002) - 0.299883*cos(0.44*x_2 + 3.30032) - 0.45377)*(-0.0084009*Abs(2.496*x_2 - 4.39988) - 0.23567 + 0.130211*exp(-2.19727*(1 - 0.457067*x_1)**2)) + 0.00733206)**5`

### task=feynman_I_12_4 seed=17

- Task source: feynman_file
- Target formula: `q1*r/(4*pi*epsilon*r**3)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=5.651012e-04, r2=-0.000211
- Variant formula overview:
  - icbr_full: symbolic_s=6.654054e-01, imitation_mse=1.564516e-12, target_mse=5.651045e-04, formula_export_success=True
  - icbr_no_replay: symbolic_s=5.721208e-01, imitation_mse=1.564112e-12, target_mse=5.651045e-04, formula_export_success=True
  - icbr_no_shared: symbolic_s=8.527747e-01, imitation_mse=1.564516e-12, target_mse=5.651045e-04, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.291725e+00, imitation_mse=nan, target_mse=nan, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0.0185928 - 3.98719e-5/(0.00686704*x_1 + 0.0236999*asin(0.4*x_2 - 1.4) - 1)**5 + 9.81286e-5/(-0.459478*(1 - 0.07*x_1)**(3/2) - 1)**4`
- icbr_no_replay formula (display, rounded):
  - `0.0185928 - 4.82002e-5/(0.00713257*x_1 - 0.0246163*acos(0.4*x_2 - 1.4) - 1)**5 + 0.000100317/(-0.469074 - exp(-0.05*x_1))**4`
- icbr_no_shared formula (display, rounded):
  - `0.0185928 - 3.98719e-5/(0.00686704*x_1 + 0.0236999*asin(0.4*x_2 - 1.4) - 1)**5 + 9.81286e-5/(0.459478*(1 - 0.07*x_1)**(3/2) + 1)**4`
- icbr_refit_commit formula (display, rounded):
  - `0.0185795 + 4.10906e-5/(0.0131793*x_1 + 0.0590703*acos(1.28024 - 0.27824*x_2) - 1)**2 + 8.14137e-5/(-0.323199*(1 - 0.0800106*x_1)**(3/2) - 1)**4`

### task=feynman_I_12_4 seed=18

- Task source: feynman_file
- Target formula: `q1*r/(4*pi*epsilon*r**3)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.103953e-03, r2=-0.597388
- Variant formula overview:
  - icbr_full: symbolic_s=6.069995e-01, imitation_mse=5.478545e-10, target_mse=1.103716e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=5.420448e-01, imitation_mse=5.516104e-10, target_mse=1.103705e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=7.743637e-01, imitation_mse=5.478545e-10, target_mse=1.103716e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.039525e+00, imitation_mse=5.441709e-10, target_mse=1.103777e-03, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0.00690357*((-0.083279*cos(0.35*x_3 + 0.5) - 0.176812 + 0.160314*exp(-2.4025*(1 - 0.483871*x_1)**2))*(0.0528253*Abs(2.45*x_3 - 4.0) + 0.0175868*sign(3.75 - 3.25*x_2) + 0.187085) - 0.19)**3 - 0.000926329`
- icbr_no_replay formula (display, rounded):
  - `-0.00753479*(-(0.0528253*Abs(2.45*x_3 - 4.0) + 0.0175868*sign(3.75 - 3.25*x_2) + 0.187085)*(0.00766089*Abs(3.65*x_3 - 4.2) - 0.230278 + 0.160314*exp(-2.4025*(1 - 0.483871*x_1)**2)) + 0.29)**4 - 0.000920711`
- icbr_no_shared formula (display, rounded):
  - `0.00690357*((-0.083279*cos(0.35*x_3 + 0.5) - 0.176812 + 0.160314*exp(-2.4025*(1 - 0.483871*x_1)**2))*(0.0528253*Abs(2.45*x_3 - 4.0) + 0.0175868*sign(3.75 - 3.25*x_2) + 0.187085) - 0.19)**3 - 0.000926329`
- icbr_refit_commit formula (display, rounded):
  - `-0.000323557*(-(-0.0853722*cos(0.34084*x_3 + 0.50028) - 0.192795 + 0.1701*exp(-1.62257*(1 - 0.480955*x_1)**2))*(0.0640565*Abs(2.03168*x_3 - 3.45524) + 0.0151478*sign(4.59974 - 3.992*x_2) + 0.189588) + 0.999976)**3 - 0.000648048`

### task=feynman_I_12_4 seed=19

- Task source: feynman_file
- Target formula: `q1*r/(4*pi*epsilon*r**3)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=9.144658e-04, r2=0.000489
- Variant formula overview:
  - icbr_full: symbolic_s=1.381528e+00, imitation_mse=1.090538e-07, target_mse=9.151176e-04, formula_export_success=True
  - icbr_no_replay: symbolic_s=1.021652e+00, imitation_mse=1.299117e-07, target_mse=9.128529e-04, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.976269e+00, imitation_mse=1.090538e-07, target_mse=9.151176e-04, formula_export_success=True
  - icbr_refit_commit: symbolic_s=2.191820e+00, imitation_mse=1.492765e-07, target_mse=9.152547e-04, formula_export_success=True
- icbr_full formula (display, rounded):
  - `-0.000152092*cos(1.6*(-0.27475*sin(1.05*x_2 + 2.8) - 0.0885743*sin(1.05*x_3 - 3.55) - 0.805829)*(0.472095*cos(1.0*x_2 + 4.55) + 0.133192*Abs(2.9*x_3 - 4.9) - 0.517946) + 4.0) + 0.00216065*Abs(0.00368428*Abs(2.6*x_1 - 4.15) + 0.0532902*Abs(2.85*x_2 - 4.75) + 0.00449337*Abs(2.25*x_3 - 3.95) - 0.332369) + 0.000682553*sign(-0.626289*sin(1.1*x_2 + 2.65) - 0.894428) + 0.0190022`
- icbr_no_replay formula (display, rounded):
  - `0.000158403*sin(1.55*(-0.100186*Abs(2.1*x_2 - 3.6) - 0.0308981*Abs(2.2*x_3 - 3.9) - 0.364361)*(-0.128369*Abs(2.75*x_2 - 4.575) + 0.133192*Abs(2.9*x_3 - 4.9) + 0.0555703) + 2.4) + 0.00029796*sign(-0.00442114*Abs(2.6*x_1 - 4.15) - 0.0639482*Abs(2.85*x_2 - 4.75) - 0.00539205*Abs(2.25*x_3 - 3.95) + 0.188842) + 0.0187318 - 2.87439e-5/(-0.678058*Abs(2.15*x_2 - 3.75) - 1)**5`
- icbr_no_shared formula (display, rounded):
  - `-0.000152092*cos(1.6*(-0.27475*sin(1.05*x_2 + 2.8) - 0.0885743*sin(1.05*x_3 - 3.55) - 0.805829)*(0.472095*cos(1.0*x_2 + 4.55) + 0.133192*Abs(2.9*x_3 - 4.9) - 0.517946) + 4.0) + 0.00216065*Abs(0.00368428*Abs(2.6*x_1 - 4.15) + 0.0506257*Abs(3.0*x_2 - 5.0) + 0.00449337*Abs(2.25*x_3 - 3.95) - 0.332368) + 0.000682553*sign(-0.626289*sin(1.1*x_2 + 2.65) - 0.894428) + 0.0190022`
- icbr_refit_commit formula (display, rounded):
  - `-0.000119008*cos(2.09388*(0.275442*sin(1.036*x_2 - 0.3) - 0.0883422*sin(1.062*x_3 + 2.7) - 0.806612)*(-0.472019*cos(1.00028*x_2 + 1.408) + 0.172895*Abs(2.21908*x_3 - 3.83008) - 0.504665) - 2.11464) + 0.00100079*Abs(0.0043186*Abs(2.75436*x_1 - 4.4892) + 0.09264*Abs(2.04436*x_2 - 3.50668) + 0.00475764*Abs(2.6512*x_3 - 4.78312) - 0.552545) + 0.0184099`

### task=feynman_I_12_4 seed=20

- Task source: feynman_file
- Target formula: `q1*r/(4*pi*epsilon*r**3)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=7.089532e-04, r2=-0.003783
- Variant formula overview:
  - icbr_full: symbolic_s=6.072789e-01, imitation_mse=4.262328e-12, target_mse=7.089493e-04, formula_export_success=True
  - icbr_no_replay: symbolic_s=4.483705e-01, imitation_mse=4.712470e-12, target_mse=7.089505e-04, formula_export_success=True
  - icbr_no_shared: symbolic_s=6.509835e-01, imitation_mse=4.262328e-12, target_mse=7.089493e-04, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.009427e+00, imitation_mse=4.989878e-12, target_mse=7.089505e-04, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0.0183621 - 1.38627e-5/(-0.03366*sign(3.5 - 2.9*x_1) - 1)**5 - 5.12984e-7/(1 - 0.217205*tanh(3.95*x_1 - 5.0))**5`
- icbr_no_replay formula (display, rounded):
  - `0.0183645 - 1.38627e-5/(-0.03366*sign(3.5 - 2.9*x_1) - 1)**5 - 1.88057e-6/(0.234315*sign(3.35 - 2.75*x_1) + 1)**3`
- icbr_no_shared formula (display, rounded):
  - `0.0183621 - 1.38627e-5/(-0.03366*sign(3.5 - 2.9*x_1) - 1)**5 - 5.12984e-7/(1 - 0.217205*tanh(3.95*x_1 - 5.0))**5`
- icbr_refit_commit formula (display, rounded):
  - `0.0183804 + 1.12094e-6/(0.133833*tanh(3.88*x_1 - 4.8999) - 1)**5 - 2.26109e-6/(1 - 0.189034*sign(4.93 - 3.73*x_1))**3`

### task=feynman_I_6_2a seed=1

- Task source: feynman_file
- Target formula: `exp(-theta**2/2)/sqrt(2*pi)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=4.749580e-03, r2=-0.005976
- Variant formula overview:
  - icbr_full: symbolic_s=2.936178e-01, imitation_mse=1.959322e-15, target_mse=4.749581e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=2.737532e-01, imitation_mse=1.959322e-15, target_mse=4.749581e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=2.786717e-01, imitation_mse=1.959322e-15, target_mse=4.749581e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=5.004855e-01, imitation_mse=3.324840e-15, target_mse=4.749580e-03, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0.0795312 - 2.45525e-6/(1 - 0.266167*exp(-0.15*x_1))**5`
- icbr_no_replay formula (display, rounded):
  - `0.0795312 - 2.45525e-6/(1 - 0.266167*exp(-0.15*x_1))**5`
- icbr_no_shared formula (display, rounded):
  - `0.0795312 - 2.45525e-6/(1 - 0.266167*exp(-0.15*x_1))**5`
- icbr_refit_commit formula (display, rounded):
  - `0.0795615 - 2.9515e-5/(1 - 0.0640144*exp(-0.146*x_1))**5`

### task=feynman_I_6_2a seed=2

- Task source: feynman_file
- Target formula: `exp(-theta**2/2)/sqrt(2*pi)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=5.435676e-03, r2=-0.130923
- Variant formula overview:
  - icbr_full: symbolic_s=2.980469e-01, imitation_mse=1.006278e-06, target_mse=5.404796e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=2.536568e-01, imitation_mse=1.743381e-06, target_mse=5.446990e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=2.921122e-01, imitation_mse=1.006278e-06, target_mse=5.404796e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=5.352638e-01, imitation_mse=1.010681e-06, target_mse=5.404756e-03, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0.0591079 - 0.256652*(0.213635*acos(0.55*x_1 - 1.55) - 1)**4`
- icbr_no_replay formula (display, rounded):
  - `0.0573639 - 0.0270048*(0.221761*tan(1.1*x_1 + 0.8) + 1)**3`
- icbr_no_shared formula (display, rounded):
  - `0.0591079 - 0.256652*(0.213635*acos(0.55*x_1 - 1.55) - 1)**4`
- icbr_refit_commit formula (display, rounded):
  - `0.0591148 - 0.00300299*(-0.65041*acos(1.54876 - 0.54876*x_1) - 1)**4`

### task=feynman_I_6_2a seed=3

- Task source: feynman_file
- Target formula: `exp(-theta**2/2)/sqrt(2*pi)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.337722e-03, r2=0.710607
- Variant formula overview:
  - icbr_full: symbolic_s=2.966582e-01, imitation_mse=2.251322e-05, target_mse=1.247119e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=3.034719e-01, imitation_mse=2.251322e-05, target_mse=1.247119e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=2.814249e-01, imitation_mse=2.251322e-05, target_mse=1.247119e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=4.643473e-01, imitation_mse=4.336668e-05, target_mse=1.214781e-03, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0.0255727 + 0.106684*exp(-0.085186*(Abs(3.9*x_1 - 5.0) + 0.497248)**2)`
- icbr_no_replay formula (display, rounded):
  - `0.0255727 + 0.106684*exp(-0.085186*(Abs(3.9*x_1 - 5.0) + 0.497248)**2)`
- icbr_no_shared formula (display, rounded):
  - `0.0255727 + 0.106684*exp(-0.085186*(Abs(3.9*x_1 - 5.0) + 0.497248)**2)`
- icbr_refit_commit formula (display, rounded):
  - `0.243914 - 0.216727*exp(-0.686339*(1 - 0.152632*Abs(3.85916*x_1 - 4.77052))**2)`

### task=feynman_I_6_2a seed=4

- Task source: feynman_file
- Target formula: `exp(-theta**2/2)/sqrt(2*pi)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=2.493406e-03, r2=0.493235
- Variant formula overview:
  - icbr_full: symbolic_s=2.946854e-01, imitation_mse=2.809519e-05, target_mse=2.317316e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=3.045576e-01, imitation_mse=2.809519e-05, target_mse=2.317316e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=2.809680e-01, imitation_mse=2.809519e-05, target_mse=2.317316e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=4.601355e-01, imitation_mse=3.005590e-05, target_mse=2.294074e-03, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0.1087 - 0.077492*exp(-3.72825*(1 - 0.286784*Abs(2.9*x_1 - 4.0))**2)`
- icbr_no_replay formula (display, rounded):
  - `0.1087 - 0.077492*exp(-3.72825*(1 - 0.286784*Abs(2.9*x_1 - 4.0))**2)`
- icbr_no_shared formula (display, rounded):
  - `0.1087 - 0.077492*exp(-3.72825*(1 - 0.286784*Abs(2.9*x_1 - 4.0))**2)`
- icbr_refit_commit formula (display, rounded):
  - `0.113255 - 0.0806855*exp(-3.09664*(1 - 0.273047*Abs(3.022*x_1 - 4.224))**2)`

### task=feynman_I_6_2a seed=5

- Task source: feynman_file
- Target formula: `exp(-theta**2/2)/sqrt(2*pi)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=5.043435e-03, r2=-0.054326
- Variant formula overview:
  - icbr_full: symbolic_s=1.479368e-01, imitation_mse=0.000000e+00, target_mse=5.043435e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=1.331659e-01, imitation_mse=5.551115e-17, target_mse=5.043435e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.435219e-01, imitation_mse=0.000000e+00, target_mse=5.043435e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=2.109166e-01, imitation_mse=1.387779e-17, target_mse=5.043435e-03, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0.0610657000000000`
- icbr_no_replay formula (display, rounded):
  - `0.0610658000000000`
- icbr_no_shared formula (display, rounded):
  - `0.0610657000000000`
- icbr_refit_commit formula (display, rounded):
  - `0.0610657000000000`

### task=feynman_I_6_2a seed=6

- Task source: feynman_file
- Target formula: `exp(-theta**2/2)/sqrt(2*pi)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.584985e-02, r2=-2.152354
- Variant formula overview:
  - icbr_full: symbolic_s=2.954070e-01, imitation_mse=9.093685e-06, target_mse=1.588012e-02, formula_export_success=True
  - icbr_no_replay: symbolic_s=2.677869e-01, imitation_mse=9.121434e-06, target_mse=1.592247e-02, formula_export_success=True
  - icbr_no_shared: symbolic_s=2.827598e-01, imitation_mse=9.093685e-06, target_mse=1.588012e-02, formula_export_success=True
  - icbr_refit_commit: symbolic_s=4.954427e-01, imitation_mse=1.055672e-05, target_mse=1.578790e-02, formula_export_success=True
- icbr_full formula (display, rounded):
  - `-0.0539885*atan(2.63523*atanh(0.7*x_1 - 1.5) + 0.686008) - 0.0314804`
- icbr_no_replay formula (display, rounded):
  - `-0.0539885*atan(2.18356*asin(0.85*x_1 - 1.85) + 0.759487) - 0.0314804`
- icbr_no_shared formula (display, rounded):
  - `-0.0539885*atan(2.63523*atanh(0.7*x_1 - 1.5) + 0.686008) - 0.0314804`
- icbr_refit_commit formula (display, rounded):
  - `-0.0550557*atan(2.55203*atanh(0.70096*x_1 - 1.5014) + 0.700756) - 0.0299839`

### task=feynman_I_6_2a seed=7

- Task source: feynman_file
- Target formula: `exp(-theta**2/2)/sqrt(2*pi)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.069810e-02, r2=-1.196477
- Variant formula overview:
  - icbr_full: symbolic_s=6.011100e-03, imitation_mse=0.000000e+00, target_mse=1.069810e-02, formula_export_success=True
  - icbr_no_replay: symbolic_s=5.681000e-03, imitation_mse=0.000000e+00, target_mse=1.069810e-02, formula_export_success=True
  - icbr_no_shared: symbolic_s=5.257900e-03, imitation_mse=0.000000e+00, target_mse=1.069810e-02, formula_export_success=True
  - icbr_refit_commit: symbolic_s=8.126000e-03, imitation_mse=0.000000e+00, target_mse=1.069810e-02, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0`
- icbr_no_replay formula (display, rounded):
  - `0`
- icbr_no_shared formula (display, rounded):
  - `0`
- icbr_refit_commit formula (display, rounded):
  - `0`

### task=feynman_I_6_2a seed=8

- Task source: feynman_file
- Target formula: `exp(-theta**2/2)/sqrt(2*pi)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=2.772667e-03, r2=0.429632
- Variant formula overview:
  - icbr_full: symbolic_s=5.280441e-01, imitation_mse=1.279101e-04, target_mse=3.575761e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=4.595286e-01, imitation_mse=1.379552e-04, target_mse=3.509976e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=6.402009e-01, imitation_mse=1.279101e-04, target_mse=3.575761e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=9.094420e-01, imitation_mse=1.696185e-04, target_mse=4.048618e-03, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0.0472188*Abs(-0.954484*sign(3.85 - 3.3*x_1) - 0.663899) + 0.0580405 - 3.25206e-5/(1 - 0.177745*tanh(4.25*x_1 - 5.0))**4`
- icbr_no_replay formula (display, rounded):
  - `0.142541 - 0.082647*exp(-1.00946*(-sign(3.85 - 3.3*x_1) - 0.648412)**2) - 2.19685e-5/(0.162172*sign(3.35 - 2.8*x_1) + 1)**5`
- icbr_no_shared formula (display, rounded):
  - `0.0472188*Abs(-0.954484*sign(3.85 - 3.3*x_1) - 0.663899) + 0.0580405 - 3.25206e-5/(1 - 0.177745*tanh(4.25*x_1 - 5.0))**4`
- icbr_refit_commit formula (display, rounded):
  - `-0.0234474*Abs(0.858333*sign(4.3*x_1 - 4.98914) + 2.35374) + 0.145413 - 3.22586e-5/(0.179644*tanh(4.178*x_1 - 4.89956) - 1)**4`

### task=feynman_I_6_2a seed=9

- Task source: feynman_file
- Target formula: `exp(-theta**2/2)/sqrt(2*pi)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.222142e-02, r2=-1.290458
- Variant formula overview:
  - icbr_full: symbolic_s=6.449400e-03, imitation_mse=0.000000e+00, target_mse=1.222142e-02, formula_export_success=True
  - icbr_no_replay: symbolic_s=7.044100e-03, imitation_mse=0.000000e+00, target_mse=1.222142e-02, formula_export_success=True
  - icbr_no_shared: symbolic_s=6.427700e-03, imitation_mse=0.000000e+00, target_mse=1.222142e-02, formula_export_success=True
  - icbr_refit_commit: symbolic_s=6.563400e-03, imitation_mse=0.000000e+00, target_mse=1.222142e-02, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0`
- icbr_no_replay formula (display, rounded):
  - `0`
- icbr_no_shared formula (display, rounded):
  - `0`
- icbr_refit_commit formula (display, rounded):
  - `0`

### task=feynman_I_6_2a seed=10

- Task source: feynman_file
- Target formula: `exp(-theta**2/2)/sqrt(2*pi)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.593146e-04, r2=0.967640
- Variant formula overview:
  - icbr_full: symbolic_s=2.979563e-01, imitation_mse=5.448458e-05, target_mse=1.077841e-04, formula_export_success=True
  - icbr_no_replay: symbolic_s=2.757896e-01, imitation_mse=5.448458e-05, target_mse=1.077841e-04, formula_export_success=True
  - icbr_no_shared: symbolic_s=2.753281e-01, imitation_mse=5.448458e-05, target_mse=1.077841e-04, formula_export_success=True
  - icbr_refit_commit: symbolic_s=4.415373e-01, imitation_mse=5.575977e-05, target_mse=8.477498e-05, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0.296499*cos(1.05727*cos(0.85*x_1 + 2.8) + 2.84837) + 0.311797`
- icbr_no_replay formula (display, rounded):
  - `0.296499*cos(1.05727*cos(0.85*x_1 + 2.8) + 2.84837) + 0.311797`
- icbr_no_shared formula (display, rounded):
  - `0.296499*cos(1.05727*cos(0.85*x_1 + 2.8) + 2.84837) + 0.311797`
- icbr_refit_commit formula (display, rounded):
  - `1.11537*sin(0.519532*cos(0.83728*x_1 + 2.84468) - 1.72964) + 1.13176`

### task=feynman_I_6_2a seed=11

- Task source: feynman_file
- Target formula: `exp(-theta**2/2)/sqrt(2*pi)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.198883e-02, r2=-1.321450
- Variant formula overview:
  - icbr_full: symbolic_s=2.886700e-03, imitation_mse=0.000000e+00, target_mse=1.198883e-02, formula_export_success=True
  - icbr_no_replay: symbolic_s=2.337500e-03, imitation_mse=0.000000e+00, target_mse=1.198883e-02, formula_export_success=True
  - icbr_no_shared: symbolic_s=2.277800e-03, imitation_mse=0.000000e+00, target_mse=1.198883e-02, formula_export_success=True
  - icbr_refit_commit: symbolic_s=3.355600e-03, imitation_mse=0.000000e+00, target_mse=1.198883e-02, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0`
- icbr_no_replay formula (display, rounded):
  - `0`
- icbr_no_shared formula (display, rounded):
  - `0`
- icbr_refit_commit formula (display, rounded):
  - `0`

### task=feynman_I_6_2a seed=12

- Task source: feynman_file
- Target formula: `exp(-theta**2/2)/sqrt(2*pi)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=2.492909e-04, r2=0.949017
- Variant formula overview:
  - icbr_full: symbolic_s=3.183363e-01, imitation_mse=2.432517e-05, target_mse=2.678768e-04, formula_export_success=True
  - icbr_no_replay: symbolic_s=2.910750e-01, imitation_mse=2.483579e-05, target_mse=2.743665e-04, formula_export_success=True
  - icbr_no_shared: symbolic_s=2.849207e-01, imitation_mse=2.432517e-05, target_mse=2.678768e-04, formula_export_success=True
  - icbr_refit_commit: symbolic_s=4.594819e-01, imitation_mse=1.811269e-05, target_mse=2.427818e-04, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0.395344 - 0.513869*exp(-0.427296*(0.308265*tan(0.95*x_1 + 1.1) - 1)**2)`
- icbr_no_replay formula (display, rounded):
  - `0.0807537 - 0.308995*tanh(0.287866*tan(0.95*x_1 + 1.1) + 0.0661736)`
- icbr_no_shared formula (display, rounded):
  - `0.395344 - 0.513869*exp(-0.427296*(0.308265*tan(0.95*x_1 + 1.1) - 1)**2)`
- icbr_refit_commit formula (display, rounded):
  - `-0.232559 + 0.531278*exp(-0.642606*(0.324165*tan(0.75944*x_1 - 1.73116) + 1)**2)`

### task=feynman_I_6_2a seed=13

- Task source: feynman_file
- Target formula: `exp(-theta**2/2)/sqrt(2*pi)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=2.807868e-04, r2=0.938131
- Variant formula overview:
  - icbr_full: symbolic_s=2.939482e-01, imitation_mse=3.316826e-05, target_mse=2.077396e-04, formula_export_success=True
  - icbr_no_replay: symbolic_s=2.639236e-01, imitation_mse=3.329436e-05, target_mse=2.059388e-04, formula_export_success=True
  - icbr_no_shared: symbolic_s=2.941652e-01, imitation_mse=3.316826e-05, target_mse=2.077396e-04, formula_export_success=True
  - icbr_refit_commit: symbolic_s=4.747522e-01, imitation_mse=7.193917e-05, target_mse=1.913267e-04, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0.0230386 + 0.160578*exp(-3.99066*(sin(0.95*x_1 + 1.05) - 0.900554)**2)`
- icbr_no_replay formula (display, rounded):
  - `0.0230386 + 0.160578*exp(-4.40331*(-cos(0.9*x_1 + 2.7) - 0.885578)**2)`
- icbr_no_shared formula (display, rounded):
  - `0.0230386 + 0.160578*exp(-3.99066*(sin(0.95*x_1 + 1.05) - 0.900554)**2)`
- icbr_refit_commit formula (display, rounded):
  - `0.462192 - 0.447156*exp(-0.470917*(0.223738 - sin(0.8412*x_1 - 1.87568))**2)`

### task=feynman_I_6_2a seed=14

- Task source: feynman_file
- Target formula: `exp(-theta**2/2)/sqrt(2*pi)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=2.367586e-04, r2=0.948221
- Variant formula overview:
  - icbr_full: symbolic_s=6.189813e-01, imitation_mse=4.590224e-05, target_mse=1.680815e-04, formula_export_success=True
  - icbr_no_replay: symbolic_s=5.198232e-01, imitation_mse=4.527609e-05, target_mse=1.641085e-04, formula_export_success=True
  - icbr_no_shared: symbolic_s=7.734070e-01, imitation_mse=4.590224e-05, target_mse=1.680815e-04, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.088111e+00, imitation_mse=8.075561e-05, target_mse=1.520819e-04, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0.0169366 + 0.169747*exp(-3.17311*(-sin(0.9*x_1 + 4.2) - 0.994239)**2) + 0.0050029*exp(-20.25*(-(-0.187633*Abs(2.35*x_1 - 3.45) - 0.452827)*(-0.218071*Abs(3.1*x_1 - 4.525) - 0.691217) + 0.922222)**2)`
- icbr_no_replay formula (display, rounded):
  - `0.0169366 + 0.169747*exp(-3.13758*(-cos(0.9*x_1 + 2.65) - 0.981127)**2) + 0.0050029*exp(-20.25*(-(-0.187633*Abs(2.35*x_1 - 3.45) - 0.452827)*(-0.218071*Abs(3.1*x_1 - 4.525) - 0.691217) + 0.922222)**2)`
- icbr_no_shared formula (display, rounded):
  - `0.0169366 + 0.169747*exp(-3.17311*(-sin(0.9*x_1 + 4.2) - 0.994239)**2) + 0.0050029*exp(-20.25*(-(-0.187633*Abs(2.35*x_1 - 3.45) - 0.452827)*(-0.218071*Abs(3.1*x_1 - 4.525) - 0.691217) + 0.922222)**2)`
- icbr_refit_commit formula (display, rounded):
  - `0.00804964 + 0.212589*exp(-2.25356*(0.785211*sin(0.92916*x_1 + 1.03072) - 1)**2) + 0.00414777*exp(-11.5601*(-(-0.135662*Abs(3.27008*x_1 - 4.89472) - 0.457252)*(-0.205749*Abs(3.299*x_1 - 4.90328) - 0.698347) + 0.894112)**2)`

### task=feynman_I_6_2a seed=15

- Task source: feynman_file
- Target formula: `exp(-theta**2/2)/sqrt(2*pi)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.124615e-02, r2=-1.256123
- Variant formula overview:
  - icbr_full: symbolic_s=5.751700e-03, imitation_mse=0.000000e+00, target_mse=1.124615e-02, formula_export_success=True
  - icbr_no_replay: symbolic_s=5.864000e-03, imitation_mse=0.000000e+00, target_mse=1.124615e-02, formula_export_success=True
  - icbr_no_shared: symbolic_s=5.458500e-03, imitation_mse=0.000000e+00, target_mse=1.124615e-02, formula_export_success=True
  - icbr_refit_commit: symbolic_s=5.181800e-03, imitation_mse=0.000000e+00, target_mse=1.124615e-02, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0`
- icbr_no_replay formula (display, rounded):
  - `0`
- icbr_no_shared formula (display, rounded):
  - `0`
- icbr_refit_commit formula (display, rounded):
  - `0`

### task=feynman_I_6_2a seed=16

- Task source: feynman_file
- Target formula: `exp(-theta**2/2)/sqrt(2*pi)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=6.682832e-03, r2=-0.352419
- Variant formula overview:
  - icbr_full: symbolic_s=2.957526e-01, imitation_mse=1.979324e-06, target_mse=6.628862e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=2.883489e-01, imitation_mse=1.979324e-06, target_mse=6.628862e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=2.855078e-01, imitation_mse=1.979324e-06, target_mse=6.628862e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=5.133143e-01, imitation_mse=2.320359e-06, target_mse=6.559867e-03, formula_export_success=True
- icbr_full formula (display, rounded):
  - `-0.133147*sin(0.237569*atanh(0.9*x_1 - 1.9) - 1.07957) - 0.0911821`
- icbr_no_replay formula (display, rounded):
  - `-0.133147*sin(0.237569*atanh(0.9*x_1 - 1.9) - 1.07957) - 0.0911821`
- icbr_no_shared formula (display, rounded):
  - `-0.133147*sin(0.237569*atanh(0.9*x_1 - 1.9) - 1.07957) - 0.0911821`
- icbr_refit_commit formula (display, rounded):
  - `-0.124934*sin(0.405284*atanh(0.56788*x_1 - 1.46176) - 0.929709) - 0.0822567`

### task=feynman_I_6_2a seed=17

- Task source: feynman_file
- Target formula: `exp(-theta**2/2)/sqrt(2*pi)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.123139e-02, r2=-1.241356
- Variant formula overview:
  - icbr_full: symbolic_s=2.563700e-03, imitation_mse=0.000000e+00, target_mse=1.123139e-02, formula_export_success=True
  - icbr_no_replay: symbolic_s=2.749300e-03, imitation_mse=0.000000e+00, target_mse=1.123139e-02, formula_export_success=True
  - icbr_no_shared: symbolic_s=2.313100e-03, imitation_mse=0.000000e+00, target_mse=1.123139e-02, formula_export_success=True
  - icbr_refit_commit: symbolic_s=2.360700e-03, imitation_mse=0.000000e+00, target_mse=1.123139e-02, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0`
- icbr_no_replay formula (display, rounded):
  - `0`
- icbr_no_shared formula (display, rounded):
  - `0`
- icbr_refit_commit formula (display, rounded):
  - `0`

### task=feynman_I_6_2a seed=18

- Task source: feynman_file
- Target formula: `exp(-theta**2/2)/sqrt(2*pi)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=2.225641e-03, r2=0.555444
- Variant formula overview:
  - icbr_full: symbolic_s=2.991145e-01, imitation_mse=3.106413e-05, target_mse=2.074329e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=2.799520e-01, imitation_mse=3.106413e-05, target_mse=2.074329e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=2.972156e-01, imitation_mse=3.106413e-05, target_mse=2.074329e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=4.610482e-01, imitation_mse=5.488827e-05, target_mse=2.084811e-03, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0.036528 + 0.072795*exp(-0.29095*(0.806126 - Abs(3.85*x_1 - 5.0))**2)`
- icbr_no_replay formula (display, rounded):
  - `0.036528 + 0.072795*exp(-0.29095*(0.806126 - Abs(3.85*x_1 - 5.0))**2)`
- icbr_no_shared formula (display, rounded):
  - `0.036528 + 0.072795*exp(-0.29095*(0.806126 - Abs(3.85*x_1 - 5.0))**2)`
- icbr_refit_commit formula (display, rounded):
  - `0.124075 - 0.0914302*exp(-2.07494*(1 - 0.230135*Abs(3.26696*x_1 - 4.18376))**2)`

### task=feynman_I_6_2a seed=19

- Task source: feynman_file
- Target formula: `exp(-theta**2/2)/sqrt(2*pi)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=4.883552e-03, r2=-0.000667
- Variant formula overview:
  - icbr_full: symbolic_s=3.054496e-01, imitation_mse=1.811718e-15, target_mse=4.883551e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=3.449770e-01, imitation_mse=1.811718e-15, target_mse=4.883551e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=3.632743e-01, imitation_mse=1.811718e-15, target_mse=4.883551e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=5.437438e-01, imitation_mse=4.233391e-15, target_mse=4.883550e-03, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0.0791998 - 9.96196e-5/((1 - 0.021164*x_1)**4 + 0.984689)**5`
- icbr_no_replay formula (display, rounded):
  - `0.0791998 - 9.96196e-5/((1 - 0.021164*x_1)**4 + 0.984689)**5`
- icbr_no_shared formula (display, rounded):
  - `0.0791998 - 9.96196e-5/((1 - 0.021164*x_1)**4 + 0.984689)**5`
- icbr_refit_commit formula (display, rounded):
  - `0.079205 + 2.22126e-5/(-0.220075*(1 - 0.0319017*x_1)**4 - 1)**5`

### task=feynman_I_6_2a seed=20

- Task source: feynman_file
- Target formula: `exp(-theta**2/2)/sqrt(2*pi)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.278427e-02, r2=-1.484015
- Variant formula overview:
  - icbr_full: symbolic_s=1.514066e-01, imitation_mse=0.000000e+00, target_mse=1.278427e-02, formula_export_success=True
  - icbr_no_replay: symbolic_s=1.380920e-01, imitation_mse=0.000000e+00, target_mse=1.278427e-02, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.483653e-01, imitation_mse=0.000000e+00, target_mse=1.278427e-02, formula_export_success=True
  - icbr_refit_commit: symbolic_s=2.500485e-01, imitation_mse=0.000000e+00, target_mse=1.278427e-02, formula_export_success=True
- icbr_full formula (display, rounded):
  - `-0.00657968000000000`
- icbr_no_replay formula (display, rounded):
  - `-0.00657968000000000`
- icbr_no_shared formula (display, rounded):
  - `-0.00657968000000000`
- icbr_refit_commit formula (display, rounded):
  - `-0.00657968000000000`

### task=feynman_I_34_1 seed=1

- Task source: feynman_file
- Target formula: `omega_0/(1-v/c)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=2.049711e-02, r2=0.993958
- Variant formula overview:
  - icbr_full: symbolic_s=3.437626e+00, imitation_mse=6.661199e-03, target_mse=1.914949e-02, formula_export_success=True
  - icbr_no_replay: symbolic_s=2.107759e+00, imitation_mse=7.149546e-03, target_mse=2.162142e-02, formula_export_success=True
  - icbr_no_shared: symbolic_s=5.033178e+00, imitation_mse=6.661447e-03, target_mse=1.915031e-02, formula_export_success=True
  - icbr_refit_commit: symbolic_s=5.842316e+00, imitation_mse=9.725915e-03, target_mse=2.399600e-02, formula_export_success=True
- icbr_full formula (display, rounded):
  - `3.6631*(0.0855615*(1.67793*sin(0.35*x_3 - 1.1) - 0.450021*cos(1.85*x_2 + 4.7) - 2.72073*atanh(0.0499997*x_1 - 0.4) + 1.57014)*(-0.234405*cos(1.85*x_2 + 4.7) - 1.36607*cos(0.35*x_3 + 0.5) - 1.85861*atanh(0.0499997*x_1 - 0.4) + 1.06193) + 1)**(3/2) - 0.520271*(0.166326*Abs(3.4*x_3 - 4.5) - 1)**2 + 0.695661*tanh(0.0618414*Abs(3.45*x_2 - 4.45) + 1.30425*asin(0.3*x_3 - 1.0) - 0.144143) + 0.0491261*Abs(-2.2*(0.0817618*Abs(2.8*x_3 - 4.1) + 7.13221*acos(0.0499997*x_1 - 0.5) - 14.5286)*(6.08998*acos(0.0499997*x_1 - 0.5) - 0.0759746*atanh(0.45*x_3 - 1.45) - 12.7379) + 3.25) + 0.137528*Abs(0.713445*cos(3.9*x_2 - 4.9) + 7.54542*acos(0.35*x_3 - 1.2) - 20.6628) + 2.66534*atan(0.154664*tan(0.65*x_3 - 2.15) + 23.8416*acos(0.0499997*x_1 - 0.5) - 45.6516 + 1.08201/(0.75 - 1.15*x_2)) + 1.17409 + 0.892674*exp(-26.7186*(-0.0598868*sin(2.9*x_2 - 4.875) + 0.533712*acos(0.0499997*x_1 - 0.5) + 0.0307239*asin(0.3*x_3 - 1.1) - 1)**2)`
- icbr_no_replay formula (display, rounded):
  - `-0.520271*(0.166326*Abs(3.4*x_3 - 4.5) - 1)**2 - 0.549932*cos(0.0773017*Abs(3.45*x_2 - 4.45) + 1.63031*asin(0.3*x_3 - 1.0) + 1.40732) + 0.0491261*Abs(2.2*(-0.0817618*Abs(2.8*x_3 - 4.1) + 7.13221*asin(0.0499997*x_1 - 0.5) + 3.32531)*(6.08998*asin(0.0499997*x_1 - 0.5) + 0.0759746*atanh(0.45*x_3 - 1.45) + 3.17181) - 3.25) - 0.61743*Abs(0.304817*sin(2.9*x_2 - 4.875) - 0.0122756*Abs(4.1*x_3 - 4.575) + 2.71653*asin(0.0499997*x_1 - 0.5) + 0.929376) + 2.66534*atan(0.154664*tan(0.65*x_3 - 2.15) - 23.8416*asin(0.0499997*x_1 - 0.5) + 1.41287*atan(3.65*x_2 - 3.7) - 10.7766) - 1.39845 + 5.83121*exp(-0.496815*(0.0225164*Abs(3.9*x_2 - 4.9) + 0.297361*asin(0.35*x_3 - 1.2) - 1)**2) + 12.8522*exp(-(-0.05*(-0.450021*cos(1.85*x_2 + 4.7) + 0.170764*Abs(3.3*x_3 - 3.85) + 2.70166*acos(0.0499997*x_1 - 0.5) - 4.05863)*(-0.234405*cos(1.85*x_2 + 4.7) + 0.102716*Abs(4.45*x_3 - 4.9) - 1.84557*asin(0.0499997*x_1 - 0.5) - 0.0187396) + 1.0)**2)`
- icbr_no_shared formula (display, rounded):
  - `3.6631*(0.0855615*(1.67793*sin(0.35*x_3 - 1.1) - 0.450021*cos(1.85*x_2 + 4.7) - 2.72073*atanh(0.0499997*x_1 - 0.4) + 1.57014)*(-0.234405*cos(1.85*x_2 + 4.7) - 1.36607*cos(0.35*x_3 + 0.5) - 1.85861*atanh(0.0499997*x_1 - 0.4) + 1.06193) + 1)**(3/2) - 0.520271*(0.166326*Abs(3.4*x_3 - 4.5) - 1)**2 + 0.695661*tanh(0.0618414*Abs(3.45*x_2 - 4.45) + 1.30425*asin(0.3*x_3 - 1.0) - 0.144143) + 0.0491261*Abs(-2.2*(0.0789644*Abs(2.9*x_3 - 4.25) + 7.13221*acos(0.0499997*x_1 - 0.5) - 14.5284)*(6.08998*acos(0.0499997*x_1 - 0.5) - 0.0759746*atanh(0.45*x_3 - 1.45) - 12.7379) + 3.25) + 0.119294*Abs(0.822444*cos(3.9*x_2 - 4.9) + 8.6982*acos(0.35*x_3 - 1.2) - 23.8321) + 2.66534*atan(0.154664*tan(0.65*x_3 - 2.15) + 23.8416*acos(0.0499997*x_1 - 0.5) - 45.6516 + 1.08201/(0.75 - 1.15*x_2)) + 1.17268 + 0.892674*exp(-26.7186*(-0.0598868*sin(2.9*x_2 - 4.875) + 0.533712*acos(0.0499997*x_1 - 0.5) + 0.0307239*asin(0.3*x_3 - 1.1) - 1)**2)`
- icbr_refit_commit formula (display, rounded):
  - `4.31591*(0.0736073*(-1.74136*sin(0.336*x_3 - 4.19954) + 0.446941*cos(1.86364*x_2 - 4.74348) + 1.75375*acos(0.0775199*x_1 - 0.60132) - 1.15003)*(0.233171*cos(1.8612*x_2 - 4.74124) + 1.41768*cos(0.336*x_3 - 2.59884) - 1.19107*acos(0.60026 - 0.0779999*x_1) + 2.96083) + 1)**(3/2) - 0.541904*(0.152014*Abs(3.58*x_3 - 4.39946) - 1)**2 + 1.69468*sin(0.0592865*cos(3.90088*x_2 - 4.90084) - 0.564577*acos(1.2806 - 0.38428*x_3) + 3.94787) + 0.695225*tanh(7.90349*sqrt(0.120874*x_3 + 1) + 0.0807295*Abs(2.6272*x_2 - 3.40476) - 9.49697) + 0.0322584*Abs(3.3*(0.11658*sqrt(0.999803*x_3 - 1) + 46.0257*atanh(0.00424*x_1 - 0.63676) + 34.5012)*(-0.401611*cos(0.638*x_3 - 3.69998) + 55.4027*atanh(0.00412*x_1 - 0.63664) + 40.906) - 4.98218) + 5.0767*atan(0.233959*tan(0.42796*x_3 - 1.91932) - 22.9639*acos(0.6005 - 0.0779999*x_1) + 27.3815 + 3.19389/(1.48292 - 2.274*x_2)) + 3.27634 + 2.87045*exp(-0.831883*(-0.22297*sin(2.04044*x_2 - 3.71716) + 0.00540572*Abs(4.844*x_3 + 1.33948) - 0.916292*acos(0.60192 - 0.0779999*x_1) + 1)**2)`

### task=feynman_I_34_1 seed=2

- Task source: feynman_file
- Target formula: `omega_0/(1-v/c)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.240291e-02, r2=0.995901
- Variant formula overview:
  - icbr_full: symbolic_s=3.564617e+00, imitation_mse=nan, target_mse=nan, formula_export_success=True
  - icbr_no_replay: symbolic_s=2.269438e+00, imitation_mse=1.746352e-02, target_mse=2.848002e-02, formula_export_success=True
  - icbr_no_shared: symbolic_s=5.130827e+00, imitation_mse=nan, target_mse=nan, formula_export_success=True
  - icbr_refit_commit: symbolic_s=6.272798e+00, imitation_mse=nan, target_mse=nan, formula_export_success=True
- icbr_full formula (display, rounded):
  - `64.2842*sqrt(0.01*(155.512*sqrt(0.0100503*x_3 + 1) - 0.0633378*sin(2.65*x_2 + 5.0) - 1.81817*tan(0.05*x_1 - 3.55) - 156.326)*(35.8512*sqrt(0.0427807*x_3 + 1) - 8.31371*acos(0.0499997*x_1 - 0.5) - 18.6711 + 1.18235*exp(-3.8025*(1 - 0.358974*x_2)**2)) + 1) - 4.13865*(-0.520785*tan(0.05*x_1 - 3.55) - 0.0075302*Abs(3.4*x_2 - 4.35) + 1)**(3/2) + 25.0799*(-tan(0.05*x_1 - 3.55) + 0.0741889*tan(0.3*x_3 - 1.0) + 0.00819139 - 0.11891*exp(-1.8225*(1 - 0.925926*x_2)**2))**2 + 0.127128*cos(-4.3925*tan(0.05*x_1 - 3.55) + 0.304919*Abs(3.85*x_3 - 4.825) + 4.26978) - 0.589897*cos(5.30351*tan(0.05*x_1 - 3.55) + 0.216395*Abs(3.75*x_3 - 4.65) + 2.43311) + 2.55777*acos(0.2*(2.55584*tan(0.05*x_1 - 3.55) + 0.127059*Abs(2.6*x_3 - 3.65) + 1.38709)*(-0.30834*sin(0.35*x_3 - 1.1) + 5.71648*tan(0.05*x_1 - 3.55) - 0.130512*tan(0.7*x_2 + 1.2) + 1.6548) - 1.05) - 65.1152 + 2.16438e-5/(-tan(0.05*x_1 - 3.55) - 0.303998 - 0.067246/(-x_2 - 3.66798e-7)**2)**4`
- icbr_no_replay formula (display, rounded):
  - `-4.13865*(-0.520785*tan(0.05*x_1 - 3.55) - 0.0075302*Abs(3.4*x_2 - 4.35) + 1)**(3/2) + 25.0799*(-tan(0.05*x_1 - 3.55) - 0.0767737*acos(0.3*x_3 - 1.05) + 0.132726 - 0.11891*exp(-1.8225*(1 - 0.925926*x_2)**2))**2 - 0.136458*sin(-4.04799*tan(0.05*x_1 - 3.55) + 0.281004*Abs(3.85*x_3 - 4.825) + 2.87705) - 0.589897*cos(5.30351*tan(0.05*x_1 - 3.55) + 0.216395*Abs(3.75*x_3 - 4.65) + 2.43311) + 0.0648297*Abs(-4.725*(-15.2286*(1 - 0.0333333*x_3)**(3/2) + 8.36134*tan(0.05*x_1 - 3.55) + 0.595786*atan(1.2*x_2 - 2.05) + 19.2611)*(155.512*sqrt(0.0100503*x_3 + 1) - 1.81817*tan(0.05*x_1 - 3.55) - 156.243 - 0.145635*exp(-2.25*(1 - 0.9*x_2)**2)) + 0.45) - 2.09866*atanh(0.25*(2.55584*tan(0.05*x_1 - 3.55) + 0.127059*Abs(2.6*x_3 - 3.65) + 1.38709)*(-0.30834*sin(0.35*x_3 - 1.1) + 5.71648*tan(0.05*x_1 - 3.55) - 0.34763*atan(2.35*x_2 - 1.95) + 2.16322) - 0.95) + 4.0188 - 0.000119236/(-tan(0.05*x_1 - 3.55) + 0.0387619*atan(2.65*x_2 - 2.7) - 0.349353)**3`
- icbr_no_shared formula (display, rounded):
  - `64.2842*sqrt(0.01*(-15.3085*(1 - 0.0331492*x_3)**(3/2) - 8.31371*acos(0.0499997*x_1 - 0.5) + 32.4938 + 1.18235*exp(-3.8025*(1 - 0.358974*x_2)**2))*(155.512*sqrt(0.0100503*x_3 + 1) - 0.0633378*sin(2.65*x_2 + 5.0) - 1.81817*tan(0.05*x_1 - 3.55) - 156.326) + 1) - 4.13865*(-0.520785*tan(0.05*x_1 - 3.55) - 0.0075302*Abs(3.4*x_2 - 4.35) + 1)**(3/2) + 25.0799*(-tan(0.05*x_1 - 3.55) + 0.0741889*tan(0.3*x_3 - 1.0) + 0.00819139 - 0.11891*exp(-1.8225*(1 - 0.925926*x_2)**2))**2 + 0.127128*cos(-4.3925*tan(0.05*x_1 - 3.55) + 0.304919*Abs(3.85*x_3 - 4.825) + 4.26978) - 0.589897*cos(5.30351*tan(0.05*x_1 - 3.55) + 0.205453*Abs(3.95*x_3 - 4.9) + 2.43336) + 2.55777*acos(0.2*(2.55584*tan(0.05*x_1 - 3.55) + 0.127059*Abs(2.6*x_3 - 3.65) + 1.38709)*(-0.30834*sin(0.35*x_3 - 1.1) + 5.71648*tan(0.05*x_1 - 3.55) - 0.130512*tan(0.7*x_2 + 1.2) + 1.6548) - 1.05) - 65.1152 + 2.16438e-5/(-tan(0.05*x_1 - 3.55) - 0.303998 - 0.067246/(-x_2 - 3.66798e-7)**2)**4`
- icbr_refit_commit formula (display, rounded):
  - `33.5684*sqrt(0.0200015*(-14.723*(1 - 0.0345483*x_3)**(3/2) + 29.6349*acos(0.62092 - 0.012*x_1) - 12.1245 + 1.08393*exp(-4.13764*(1 - 0.375396*x_2)**2))*(79.247*sqrt(0.0200038*x_3 + 1) + 0.0633555*sin(2.64916*x_2 - 4.42368) - 1.2271*asin(0.0739999*x_1 - 0.60002) - 80.0695) + 1) - 19.3091*(-tan(0.00603999*x_1 - 0.69512) - 0.00260549*Abs(3.574*x_2 - 4.5996) - 0.408531)**(3/2) + 557.813*(-tan(0.00775999*x_1 - 0.60316) - 0.0129726*acos(0.36704*x_3 - 1.2232) - 0.577516 - 0.0251142*exp(-1.87427*(1 - 0.920061*x_2)**2))**2 + 0.606098*cos(0.209534*Abs(3.74712*x_3 - 4.23976) + 3.50883*asin(0.0739999*x_1 - 0.60036) + 5.50586) + 0.149685*cos(0.253865*Abs(3.84216*x_3 - 4.25736) - 2.50528*acos(0.6 - 0.0739999*x_1) + 2.15021) + 2.56025*acos(0.19966*(12.148*tan(0.00767999*x_1 - 0.60688) + 0.158846*Abs(2.03868*x_3 - 2.75112) + 8.73496)*(30.2264*tan(0.00599999*x_1 - 0.6968) - 0.0343006*tan(0.12992*x_2 - 4.7688) - 0.0624854*Abs(1.6598*x_3 - 1.96924) + 24.6475) - 1.05) - 34.7216 + 3.36485e-8/(tan(0.00611999*x_1 - 0.68256) + 0.79129 + 0.0121641/(0.0183125 - x_2)**2)**4`

### task=feynman_I_34_1 seed=3

- Task source: feynman_file
- Target formula: `omega_0/(1-v/c)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=7.803584e-03, r2=0.997296
- Variant formula overview:
  - icbr_full: symbolic_s=3.612540e+00, imitation_mse=8.735810e-03, target_mse=1.277007e-02, formula_export_success=True
  - icbr_no_replay: symbolic_s=2.302849e+00, imitation_mse=9.043547e-03, target_mse=1.376309e-02, formula_export_success=True
  - icbr_no_shared: symbolic_s=6.426528e+00, imitation_mse=8.735810e-03, target_mse=1.277007e-02, formula_export_success=True
  - icbr_refit_commit: symbolic_s=6.712995e+00, imitation_mse=1.428507e-02, target_mse=1.848783e-02, formula_export_success=True
- icbr_full formula (display, rounded):
  - `1.61645*sin(0.890382*acos(0.35*x_3 - 1.2) + 3.6633*asin(0.0499997*x_1 - 0.5) - 0.260189*asin(1.1*x_2 - 1.65) - 3.42184) - 0.719217*tan(0.6*(-16.5709*sqrt(0.021978*x_3 + 1) + 0.275361*sin(2.75*x_2 - 4.65) - 2.43403*acos(0.0499997*x_1 - 0.5) + 22.6076)*(-5.08308*sqrt(0.147059*x_3 + 1) - 0.1295*asin(1.6*x_2 - 2.6) + 4.27016*atanh(0.0499997*x_1 - 0.4) + 6.7062) - 4.0) + 12.8643*asin(0.0103202*Abs(3.6*x_2 - 4.525) - 0.470132*acos(0.0499997*x_1 - 0.5) - 0.103253 + 1.12809*exp(-0.64*(0.0625*x_3 - 1)**2)) - 0.0672729*atan(5.97273*atanh(0.0499997*x_1 - 0.4) + 0.879929) - 0.327105*atan(2.43656*cos(0.35*x_3 + 0.5) + 43.2295*asin(0.0499997*x_1 - 0.5) + 14.8099) + 6.92154 + 0.536208*exp(-702.538*(-0.507624*acos(0.0499997*x_1 - 0.5) - 0.0131065*asin(0.45*x_3 - 1.45) + 0.0342165*sign(3.75 - 3.2*x_2) + 1)**2) + 3.74861/((14.7538*acos(0.0499997*x_1 - 0.5) - 30.577)*(-0.0288721*Abs(3.6*x_3 - 4.15) + 8.88211*asin(0.0499997*x_1 - 0.5) + 3.57707 + 0.410729*exp(-2.25*(1 - 0.9*x_2)**2)) - 0.461539)**4`
- icbr_no_replay formula (display, rounded):
  - `-0.719217*tan(0.6*(0.275361*sin(2.75*x_2 - 4.65) + 2.43403*asin(0.0499997*x_1 - 0.5) + 2.95686 - 2.08993*exp(-(0.1*x_3 - 1.0)**2))*(-0.127567*tan(1.55*x_2 - 2.5) + 4.23998*asin(0.0499997*x_1 - 0.5) - 0.983701*asin(0.3*x_3 - 1.05) + 0.883331) - 4.0) + 1.00169*atan(5.0*(-14.7538*asin(0.0499997*x_1 - 0.5) - 7.40171)*(-0.133417*Abs(3.1*x_2 - 3.6) - 0.0288721*Abs(3.6*x_3 - 4.15) - 8.88211*acos(0.0499997*x_1 - 0.5) + 17.9714) + 4.15) - 0.327105*atan(-0.269067*Abs(3.05*x_3 - 3.55) + 43.2295*asin(0.0499997*x_1 - 0.5) + 16.3695) + 12.9665*atanh(0.0103202*Abs(3.6*x_2 - 4.525) + 0.470132*asin(0.0499997*x_1 - 0.5) - 0.741733 + 1.12809*exp(-0.64*(0.0625*x_3 - 1)**2)) + 9.74544 + 0.536208*exp(-181.032*(asin(0.0499997*x_1 - 0.5) - 0.0258192*asin(0.45*x_3 - 1.45) + 0.0674051*sign(3.75 - 3.2*x_2) + 0.399165)**2) - 4.23869*exp(-2.69672*(-0.0710259*acos(1.65 - 1.1*x_2) + 0.243055*acos(0.35*x_3 - 1.2) + asin(0.0499997*x_1 - 0.5) - 0.383655)**2) + 0.117099*exp(-62.3136*(0.500852*acos(0.0499997*x_1 - 0.5) - 1)**2)`
- icbr_no_shared formula (display, rounded):
  - `1.61645*sin(0.890382*acos(0.35*x_3 - 1.2) + 3.6633*asin(0.0499997*x_1 - 0.5) - 0.260189*asin(1.1*x_2 - 1.65) - 3.42184) - 0.719217*tan(0.6*(-16.5709*sqrt(0.021978*x_3 + 1) + 0.275361*sin(2.75*x_2 - 4.65) - 2.43403*acos(0.0499997*x_1 - 0.5) + 22.6076)*(-5.08308*sqrt(0.147059*x_3 + 1) - 0.1295*asin(1.6*x_2 - 2.6) + 4.27016*atanh(0.0499997*x_1 - 0.4) + 6.7062) - 4.0) + 12.8643*asin(0.0103202*Abs(3.6*x_2 - 4.525) - 0.470132*acos(0.0499997*x_1 - 0.5) - 0.103253 + 1.12809*exp(-0.64*(0.0625*x_3 - 1)**2)) - 0.0672729*atan(5.97273*atanh(0.0499997*x_1 - 0.4) + 0.879929) - 0.327105*atan(2.43656*cos(0.35*x_3 + 0.5) + 43.2295*asin(0.0499997*x_1 - 0.5) + 14.8099) + 6.92154 + 0.536208*exp(-702.538*(-0.507624*acos(0.0499997*x_1 - 0.5) - 0.0131065*asin(0.45*x_3 - 1.45) + 0.0342165*sign(3.75 - 3.2*x_2) + 1)**2) + 3.74861/((14.7538*acos(0.0499997*x_1 - 0.5) - 30.577)*(-0.0288721*Abs(3.6*x_3 - 4.15) + 8.88211*asin(0.0499997*x_1 - 0.5) + 3.57707 + 0.410729*exp(-2.25*(1 - 0.9*x_2)**2)) - 0.461539)**4`
- icbr_refit_commit formula (display, rounded):
  - `-1.61464*sin(0.269421*acos(1.5982 - 1.066*x_2) + 0.850462*asin(0.36652*x_3 - 1.22092) - 21.3379*atanh(0.00599999*x_1 - 0.60002) - 17.6067) - 0.829722*tan(0.38012*(-14.9857*sqrt(0.0243846*x_3 + 1) - 0.285536*sin(2.6*x_2 + 4.99999) + 15.4199*atanh(0.00547999*x_1 - 0.60004) + 26.6372)*(-5.06301*sqrt(0.147744*x_3 + 1) - 0.129424*asin(1.60108*x_2 - 2.60108) + 31.2629*atanh(0.00432*x_1 - 0.64032) + 28.6407) - 1.00264) + 45.0292*asin(0.00318378*Abs(2.75208*x_2 - 3.44028) - 0.0739489*acos(0.0775599*x_1 - 0.60088) - 0.545914 + 0.180096*exp(-0.810576*(1 - 0.0844143*x_3)**2)) - 0.0645978*atan(49.8329*atanh(0.00396*x_1 - 0.639) + 36.0087) - 0.327669*atan(2.49644*sin(0.34072*x_3 + 2.10036) + 320.268*atanh(0.00432*x_1 - 0.63788) + 234.197) + 30.5364 + 0.561204*exp(-4340.7*(0.00375195*acos(0.42172*x_3 - 1.39168) + atanh(0.0042*x_1 - 0.64668) + 0.00778261*sign(4.6984 - 3.98864*x_2) + 0.750908)**2) + 3.74885/(-(9.1941 - 9.47324*acos(0.6026 - 0.0783999*x_1))*(0.32085*sin(0.336*x_3 - 4.1992) + 5.73197*asin(0.0779999*x_1 - 0.60142) + 2.36871 + 0.390448*exp(-2.56218*(1 - 0.89337*x_2)**2)) + 0.461559)**4`

### task=feynman_I_34_1 seed=4

- Task source: feynman_file
- Target formula: `omega_0/(1-v/c)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=9.617497e-03, r2=0.996991
- Variant formula overview:
  - icbr_full: symbolic_s=3.526530e+00, imitation_mse=3.133173e-02, target_mse=3.040851e-02, formula_export_success=True
  - icbr_no_replay: symbolic_s=2.181037e+00, imitation_mse=3.516982e-02, target_mse=3.779048e-02, formula_export_success=True
  - icbr_no_shared: symbolic_s=5.181468e+00, imitation_mse=3.133173e-02, target_mse=3.040851e-02, formula_export_success=True
  - icbr_refit_commit: symbolic_s=6.517784e+00, imitation_mse=3.671453e-02, target_mse=3.446344e-02, formula_export_success=True
- icbr_full formula (display, rounded):
  - `82.1813*(-0.028874*tan(0.65*x_3 - 2.15) - 0.0899616*acos(2.0 - 1.05*x_2) + asin(0.0499997*x_1 - 0.5) + 0.0841282)**4 + 59.4924*log(0.087582*atanh(0.0499997*x_1 - 0.4) + 0.103934*atanh(0.3*x_3 - 1.0) + 4.70549 - 0.0394476*exp(-1.44*(1 - 0.958333*x_2)**2)) - 1.55482*sin(6.34549*sqrt(0.1375*x_3 + 1) + 0.0648735*cos(2.3*x_2 + 0.8) - 4.43589) - 91.0724 + 1.43767*exp(-525.159*(-0.030001*cos(1.05*x_3 + 4.35) + 0.0860153*tan(1.25*x_2 + 1.15) - asin(0.0499997*x_1 - 0.5) - 0.415497)**2) + 62.1249*exp(-163.602*(asin(0.0499997*x_1 - 0.5) + 0.521267)**2) + 4.16367*exp(-0.7225*(0.0588235*(0.310616*sin(1.0*x_2 + 4.5) - 1.98171*acos(0.0499997*x_1 - 0.5) - 2.65992*acos(0.3*x_3 - 1.05) + 11.3328)*(-1.18106*acos(0.0499997*x_1 - 0.5) - 0.962695*acos(0.15*x_3 - 1.15) + 0.105627*asin(1.55*x_2 - 2.5) + 5.47553) - 1)**2) + 1.25472*exp(-2.1025*(-(3.13411*atanh(0.0499997*x_1 - 0.4) + 1.24899)*(-1.87498*atanh(0.0499997*x_1 - 0.4) - 0.927592 + 0.0671104*exp(-15.21*(1 - 0.74359*x_2)**2)) - 0.275862)**2)`
- icbr_no_replay formula (display, rounded):
  - `436.692*(-0.0602912*tan(1.0*x_2 - 5.0) - 0.0190176*tan(0.65*x_3 - 2.15) - 0.658642*acos(0.0499997*x_1 - 0.5) + 1)**4 + 46.6956*sqrt(0.0468198*asin(0.0499997*x_1 - 0.5) + 0.0415967*asin(0.4*x_3 - 1.35) + 1 - 0.0212374*exp(-1.44*(1 - 0.958333*x_2)**2)) + 0.216927*cos(1.62949*tan(1.25*x_2 + 1.15) + 0.203153*Abs(2.15*x_3 - 3.75) - 18.9442*asin(0.0499997*x_1 - 0.5) - 8.24724) + 0.183674*Abs(9.39201*asin(0.3*x_3 - 1.05) + 8.42172 - 1.21056*exp(-1.44*(0.958333*x_2 - 1)**2)) - 46.6994 + 62.1249*exp(-163.602*(asin(0.0499997*x_1 - 0.5) + 0.521267)**2) + 4.16367*exp(-0.7225*(0.0588235*(0.310616*sin(1.0*x_2 + 4.5) + 1.98171*asin(0.0499997*x_1 - 0.5) + 2.65992*asin(0.3*x_3 - 1.05) + 4.04169)*(1.18106*asin(0.0499997*x_1 - 0.5) + 0.105627*asin(1.55*x_2 - 2.5) + 0.445052*atanh(0.4*x_3 - 1.35) + 1.41874) - 1)**2) + 1.25472*exp(-2.1025*(-(3.13411*atanh(0.0499997*x_1 - 0.4) + 1.24899)*(-0.0363874*Abs(3.3*x_2 - 4.4) - 1.86179*asin(0.0499997*x_1 - 0.5) - 1.04345) - 0.275862)**2)`
- icbr_no_shared formula (display, rounded):
  - `82.1813*(-0.028874*tan(0.65*x_3 - 2.15) - 0.0899616*acos(2.0 - 1.05*x_2) + asin(0.0499997*x_1 - 0.5) + 0.0841282)**4 + 59.4924*log(0.087582*atanh(0.0499997*x_1 - 0.4) + 0.103934*atanh(0.3*x_3 - 1.0) + 4.70549 - 0.0394476*exp(-1.44*(1 - 0.958333*x_2)**2)) - 1.55482*sin(6.34549*sqrt(0.1375*x_3 + 1) + 0.0648735*cos(2.3*x_2 + 0.8) - 4.43589) - 91.0724 + 1.43767*exp(-525.159*(-0.030001*cos(1.05*x_3 + 4.35) + 0.0860153*tan(1.25*x_2 + 1.15) - asin(0.0499997*x_1 - 0.5) - 0.415497)**2) + 62.1249*exp(-163.602*(asin(0.0499997*x_1 - 0.5) + 0.521267)**2) + 4.16367*exp(-0.7225*(0.0588235*(0.310616*sin(1.0*x_2 + 4.5) - 1.98171*acos(0.0499997*x_1 - 0.5) - 2.65992*acos(0.3*x_3 - 1.05) + 11.3328)*(-1.18106*acos(0.0499997*x_1 - 0.5) - 0.962695*acos(0.15*x_3 - 1.15) + 0.105627*asin(1.55*x_2 - 2.5) + 5.47553) - 1)**2) + 1.25472*exp(-2.1025*(-(3.13411*atanh(0.0499997*x_1 - 0.4) + 1.24899)*(-1.87498*atanh(0.0499997*x_1 - 0.4) - 0.927592 + 0.0671104*exp(-15.21*(1 - 0.74359*x_2)**2)) - 0.275862)**2)`
- icbr_refit_commit formula (display, rounded):
  - `12.534*(-0.0470267*tan(0.42408*x_3 + 4.37116) - 0.163024*acos(1.8 - 0.858*x_2) + asin(0.0779999*x_1 - 0.60038) - 0.0934851)**4 + 50.3612*log(0.667737*atanh(0.00599999*x_1 - 0.60014) + 0.136995*atanh(0.30032*x_3 - 1.00144) + 5.68008 - 0.0491999*exp(-1.69*(1 - 0.943077*x_2)**2)) - 1.55113*sin(6.3883*sqrt(0.136528*x_3 + 1) + 0.0648557*cos(2.30164*x_2 + 0.7984) - 10.7319) - 76.9677 + 1.43759*exp(-218.702*(0.245418*tan(0.68588*x_2 - 1.28036) + 0.0216746*Abs(1.654*x_3 - 2.99918) - asin(0.0779999*x_1 - 0.601) - 0.472447)**2) + 47.7348*exp(-68.7893*(asin(0.0775999*x_1 - 0.603) + 0.625155)**2) - 2.63124*exp(-0.16*(-0.2*(0.31409*sin(0.98592*x_2 + 4.52956) + 2.126*acos(1.22236 - 0.36712*x_3) + 11.5287*atanh(0.00599999*x_1 - 0.60006) + 7.52574)*(0.11399*tan(1.40124*x_2 + 0.9064) + 0.701701*atanh(0.0839999*x_1 - 0.60006) + 0.625566*atanh(0.27552*x_3 - 1.17128) + 1.41464) - 1)**2) - 1.36586*exp(-3.4541*(-0.681402*(18.1046*atanh(0.00599999*x_1 - 0.60006) + 12.4994)*(-0.0524465*Abs(2.31448*x_2 - 3.11868) - 10.8289*atanh(0.00599999*x_1 - 0.60018) - 7.58782) - 1)**2)`

### task=feynman_I_34_1 seed=5

- Task source: feynman_file
- Target formula: `omega_0/(1-v/c)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=3.206039e-02, r2=0.989316
- Variant formula overview:
  - icbr_full: symbolic_s=3.450422e+00, imitation_mse=8.257429e-03, target_mse=3.638929e-02, formula_export_success=True
  - icbr_no_replay: symbolic_s=2.181560e+00, imitation_mse=8.941827e-03, target_mse=3.787763e-02, formula_export_success=True
  - icbr_no_shared: symbolic_s=5.049738e+00, imitation_mse=8.257395e-03, target_mse=3.638923e-02, formula_export_success=True
  - icbr_refit_commit: symbolic_s=6.532055e+00, imitation_mse=9.715377e-03, target_mse=3.808179e-02, formula_export_success=True
- icbr_full formula (display, rounded):
  - `-4.6227*(-0.206824*cos(0.3*x_3 - 2.5) - 0.00507597*Abs(3.8*x_2 - 4.95) + 0.314551*acos(0.0499997*x_1 - 0.5) + 1)**(3/2) + 0.470568*cos(4.45*(0.287668*acos(1.25*x_2 - 2.0) + 1.0531*asin(0.3*x_3 - 1.05) + 1.5336*atanh(0.0499997*x_1 - 0.4) + 0.723072)*(0.297353*acos(0.35*x_3 - 1.2) + 0.526052*asin(0.0499997*x_1 - 0.5) + 0.307932*asin(1.2*x_2 - 2.1) - 0.00863263) - 1.5) - 0.638851*tanh(-25.9771*sqrt(0.0529101*x_3 + 1) + 15.9056*atanh(0.0499997*x_1 - 0.4) + 31.2591) - 4.98252*asin(0.0246501*cos(3.05*x_2 - 3.5) + 0.846776*acos(0.0499997*x_1 - 0.5) - 0.750874 - 1.00763*exp(-(0.1*x_3 - 1.0)**2)) - 2.62478*asin(-0.0420256*Abs(2.8*x_3 - 3.25) + 3.28201*asin(0.0499997*x_1 - 0.5) + 0.551417 + 0.315151*exp(-0.16*(x_2 + 0.374999)**2)) + 0.867513*atan(4.95*(28.7256 - 13.8602*acos(0.0499997*x_1 - 0.5))*(6.61813*acos(0.0499997*x_1 - 0.5) - 12.8364 - 0.747558/(x_2 - 0.1)**2) + 4.55) + 14.7987 + 0.113099*exp(-16.8359*(-atanh(0.0499997*x_1 - 0.4) - 0.288828)**2)`
- icbr_no_replay formula (display, rounded):
  - `-7.98471*(-0.00352595*Abs(3.8*x_2 - 4.95) + 0.218498*acos(0.0499997*x_1 - 0.5) + 1 - 0.49221*exp(-(0.1*x_3 - 1.0)**2))**(3/2) - 0.638851*tanh(11.2994*(1 - 0.040201*x_3)**(3/2) - 15.7922*acos(0.0499997*x_1 - 0.5) + 20.3695) - 4.98252*asin(0.0246501*cos(3.05*x_2 - 3.5) - 0.852852*atanh(0.0499997*x_1 - 0.4) + 0.664231 - 1.00763*exp(-(0.1*x_3 - 1.0)**2)) + 2.62478*asin(0.0420256*Abs(2.8*x_3 - 3.25) + 3.28201*acos(0.0499997*x_1 - 0.5) - 5.70678 - 0.315151*exp(-0.16*(x_2 + 0.374999)**2)) + 0.867513*atan(4.95*(28.7256 - 13.8602*acos(0.0499997*x_1 - 0.5))*(0.475701*atan(3.05*x_2 - 3.25) - 6.66563*atanh(0.0499997*x_1 - 0.4) - 2.58565) + 4.55) + 14.0057 + 0.113099*exp(-16.8359*(-atanh(0.0499997*x_1 - 0.4) - 0.288828)**2) + 1.26408*exp(-3.61*(-(0.277524*tan(1.3*x_2 + 4.15) - 0.526051*acos(0.0499997*x_1 - 0.5) + 0.297353*acos(0.35*x_3 - 1.2) + 0.775966)*(1.0531*asin(0.3*x_3 - 1.05) + 1.5336*atanh(0.0499997*x_1 - 0.4) - 0.263585*atanh(1.3*x_2 - 2.0) + 1.19836) + 0.342105)**2)`
- icbr_no_shared formula (display, rounded):
  - `-4.6227*(-0.206824*cos(0.3*x_3 - 2.5) - 0.00507597*Abs(3.8*x_2 - 4.95) + 0.314551*acos(0.0499997*x_1 - 0.5) + 1)**(3/2) + 0.470568*cos(4.45*(0.287668*acos(1.25*x_2 - 2.0) + 1.0531*asin(0.3*x_3 - 1.05) + 1.5336*atanh(0.0499997*x_1 - 0.4) + 0.723072)*(0.526052*asin(0.0499997*x_1 - 0.5) + 0.307932*asin(1.2*x_2 - 2.1) - 0.297353*asin(0.35*x_3 - 1.2) + 0.458449) - 1.5) - 0.638851*tanh(-25.9771*sqrt(0.0529101*x_3 + 1) + 15.9056*atanh(0.0499997*x_1 - 0.4) + 31.2591) + 2.62478*acos(-0.0420256*Abs(2.8*x_3 - 3.25) + 3.28201*asin(0.0499997*x_1 - 0.5) + 0.551417 + 0.315151*exp(-0.16*(x_2 + 0.374999)**2)) - 4.98252*asin(0.0246501*cos(3.05*x_2 - 3.5) - 0.846776*asin(0.0499997*x_1 - 0.5) + 0.579239 - 1.00763*exp(-(0.1*x_3 - 1.0)**2)) + 0.867513*atan(4.95*(28.7256 - 13.8602*acos(0.0499997*x_1 - 0.5))*(6.61813*acos(0.0499997*x_1 - 0.5) - 12.8364 - 0.747558/(x_2 - 0.1)**2) + 4.55) + 10.6757 + 0.113099*exp(-16.8395*(-tan(0.05*x_1 - 0.4) - 0.288795)**2)`
- icbr_refit_commit formula (display, rounded):
  - `-5.09015*(0.717501*cos(0.0779999*x_3 + 1.4) - 0.00526517*Abs(3.43684*x_2 - 4.51508) + acos(0.0126*x_1 - 0.61816) - 0.614942)**(3/2) + 0.470528*cos(4.44996*(5.12237*sqrt(0.158051*x_3 + 1) - 0.30706*acos(1.8999 - 1.176*x_2) + 8.20837*atanh(0.00639999*x_1 - 0.6096) + 0.449468)*(0.33862*asin(0.0781999*x_1 - 0.6032) + 0.306793*asin(1.20468*x_2 - 2.10544) - 0.33827*atanh(0.30092*x_3 - 1.00184) + 0.407995) + 4.78308) - 0.631449*tanh(10.9379*(1 - 0.0404589*x_3)**(3/2) + 89.4026*atanh(0.00599999*x_1 - 0.60044) + 49.7814) - 2.39043*acos(0.0277222*Abs(4.578*x_3 - 4.88792) - 20.7149*atanh(0.00599999*x_1 - 0.60144) - 13.6515 + 0.387317*exp(-1.43827*(1 - 0.294343*x_2)**2)) + 0.765158*atan(5.0*(19.4141 - 8.94517*acos(0.0779999*x_1 - 0.60178))*(-21.197*acos(0.6064 - 0.0136*x_1) + 20.4773 - 0.746686/(0.100481 - x_2)**2) + 4.8) + 40.3753*atanh(0.00268998*cos(2.83272*x_2 - 0.11556) - 0.110568*cos(0.0775199*x_3 + 1.3962) + 0.054543*acos(0.60212 - 0.0784799*x_1) - 0.531065) + 37.3961 + 0.127006*exp(-413.049*(atanh(0.00599999*x_1 - 0.60064) + 0.678983)**2)`

### task=feynman_I_34_1 seed=6

- Task source: feynman_file
- Target formula: `omega_0/(1-v/c)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=2.283802e-02, r2=0.992602
- Variant formula overview:
  - icbr_full: symbolic_s=3.415725e+00, imitation_mse=4.325967e-02, target_mse=4.931849e-02, formula_export_success=True
  - icbr_no_replay: symbolic_s=2.233256e+00, imitation_mse=4.967053e-02, target_mse=5.277755e-02, formula_export_success=True
  - icbr_no_shared: symbolic_s=4.968095e+00, imitation_mse=4.325966e-02, target_mse=4.931835e-02, formula_export_success=True
  - icbr_refit_commit: symbolic_s=5.691089e+00, imitation_mse=4.331269e-02, target_mse=4.747274e-02, formula_export_success=True
- icbr_full formula (display, rounded):
  - `-0.569193*(0.0171548*sin(5.0*x_2 + 4.05) + 16.6557*acos(0.0499997*x_1 - 0.5) - 34.4451)*(-8.31704*tan(0.05*x_1 - 3.55) - 5.87929 + 5.07255*exp(-(0.1*x_3 - 1.0)**2) + 0.207228*exp(-16.0*(1 - 0.7125*x_2)**2)) + 0.338307*(0.0451339*sin(0.95*x_3 + 3.1) - 14.5012*tan(0.05*x_1 - 3.55) - 0.124024*Abs(3.55*x_2 - 4.65) - 6.2155)*(-0.131636*Abs(3.5*x_2 - 4.55) - 12.8168*asin(0.0499997*x_1 - 0.5) - 0.223417*atanh(0.35*x_3 - 1.15) - 7.10801) + 23.7905*(-0.0678399*cos(1.85*x_2 - 1.5) - tan(0.05*x_1 - 3.55) + 0.0150702*Abs(3.85*x_3 - 4.9) - 0.159893)**2 - 0.987593*tanh(0.384308*sin(0.9*x_3 + 3.3) + 15.8582*tan(0.05*x_1 - 3.55) - 1.33282*tan(0.55*x_2 - 0.65) + 4.06454) - 0.979214*atan(6.73648*tan(0.05*x_1 - 3.55) - 1.33474*atan(0.6*x_2 - 1.4) + 0.694824 + 1.03768*exp(-2.89*(1 - 0.470588*x_3)**2)) - 0.00917765 + 3.3407*exp(-6.76348*(-tan(0.05*x_1 - 3.55) - 0.176767*atanh(0.4*x_3 - 1.35) - 0.177004)**2)`
- icbr_no_replay formula (display, rounded):
  - `-121.518*sqrt(0.01*(-16.7528*tan(0.05*x_1 - 3.55) - 6.73511 - 0.0354213*exp(-16.0*(1 - 0.725*x_2)**2))*(-8.31704*tan(0.05*x_1 - 3.55) - 5.87929 + 5.07255*exp(-(0.1*x_3 - 1.0)**2) + 0.207228*exp(-16.0*(1 - 0.7125*x_2)**2)) + 1) + 23.7905*(0.0680752*sin(1.85*x_2 + 3.2) - tan(0.05*x_1 - 3.55) + 0.0150702*Abs(3.85*x_3 - 4.9) - 0.159135)**2 + 0.338307*(-14.5012*tan(0.05*x_1 - 3.55) - 0.124024*Abs(3.55*x_2 - 4.65) + 0.0117958*Abs(2.8*x_3 - 4.675) - 6.27043)*(-12.8916*tan(0.05*x_1 - 3.55) - 0.131636*Abs(3.5*x_2 - 4.55) - 0.175318*asin(0.45*x_3 - 1.45) - 5.92446) + 1.24513*sin(6.01869*tan(0.05*x_1 - 3.55) + 1.06391*atanh(0.4*x_3 - 1.35) + 8.90819) - 0.987593*tanh(15.8582*tan(0.05*x_1 - 3.55) - 1.33282*tan(0.55*x_2 - 0.65) + 0.105035*Abs(2.6*x_3 - 4.2) + 3.60328) - 0.979214*atan(6.73648*tan(0.05*x_1 - 3.55) - 1.33474*atan(0.6*x_2 - 1.4) + 0.694824 + 1.03768*exp(-2.89*(1 - 0.470588*x_3)**2)) + 123.767`
- icbr_no_shared formula (display, rounded):
  - `-0.569193*(0.0171548*sin(5.0*x_2 + 4.05) - 16.6557*asin(0.0499997*x_1 - 0.5) - 8.28241)*(-8.31704*tan(0.05*x_1 - 3.55) - 5.87929 + 5.07255*exp(-(0.1*x_3 - 1.0)**2) + 0.207228*exp(-16.0*(1 - 0.7125*x_2)**2)) + 0.338307*(0.0451339*sin(0.95*x_3 + 3.1) - 14.5012*tan(0.05*x_1 - 3.55) - 0.124024*Abs(3.55*x_2 - 4.65) - 6.2155)*(-0.131636*Abs(3.5*x_2 - 4.55) - 12.8168*asin(0.0499997*x_1 - 0.5) - 0.223417*atanh(0.35*x_3 - 1.15) - 7.10801) + 23.7905*(-0.0678399*cos(1.85*x_2 - 1.5) - tan(0.05*x_1 - 3.55) + 0.0150702*Abs(3.85*x_3 - 4.9) - 0.159893)**2 - 0.987593*tanh(0.384308*sin(0.9*x_3 + 3.3) + 15.8582*tan(0.05*x_1 - 3.55) - 1.33282*tan(0.55*x_2 - 0.65) + 4.06454) - 0.979214*atan(6.73648*tan(0.05*x_1 - 3.55) - 1.33474*atan(0.6*x_2 - 1.4) + 0.694824 + 1.03768*exp(-2.89*(1 - 0.470588*x_3)**2)) - 0.00917874 + 3.3407*exp(-6.76348*(-tan(0.05*x_1 - 3.55) - 0.176767*atanh(0.4*x_3 - 1.35) - 0.177004)**2)`
- icbr_refit_commit formula (display, rounded):
  - `-0.569193*(0.0170523*cos(4.99987*x_2 + 2.5) - 100.781*tan(0.00591999*x_1 - 0.61472) - 70.8387)*(-48.1114*tan(0.00615999*x_1 - 0.61584) - 37.9114 + 7.39617*exp(-0.810432*(1 - 0.0755353*x_3)**2) + 0.246387*exp(-10.2382*(1 - 0.710062*x_2)**2)) + 0.338121*(-0.045345*sin(0.936*x_3) - 0.141241*Abs(3.13672*x_2 - 4.14696) - 9.3046*acos(0.60064 - 0.0779999*x_1) + 8.74002)*(-0.155997*Abs(2.96348*x_2 - 3.8858) - 43.3905*asin(0.01276*x_1 - 0.6126) - 0.240447*atanh(0.33*x_3 - 1.1) - 29.0802) + 537.451*(-0.0154658*cos(1.69768*x_2 - 1.29988) - tan(0.00767999*x_1 - 0.6058) + 0.00301723*Abs(3.97792*x_3 - 4.6884) - 0.637021)**2 - 1.39636*tanh(0.290567*sin(0.90032*x_3 - 3.01324) + 67.3418*tan(0.00631999*x_1 - 0.61468) - 1.02572*tan(0.53452*x_2 + 2.5278) + 45.9124) - 0.966314*atan(29.3698*tan(0.00775999*x_1 - 0.60456) - 1.74389*atan(0.50224*x_2 - 1.45208) + 17.6488 + 1.00397*exp(-2.22093*(1 - 0.457176*x_3)**2)) - 0.589912 + 4.23806*exp(-115.101*(-tan(0.00763999*x_1 - 0.60056) - 0.0489496*atanh(0.31372*x_3 - 1.18208) - 0.640367)**2)`

### task=feynman_I_34_1 seed=7

- Task source: feynman_file
- Target formula: `omega_0/(1-v/c)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=2.506424e-02, r2=0.991728
- Variant formula overview:
  - icbr_full: symbolic_s=2.490776e+00, imitation_mse=9.486181e-03, target_mse=2.348139e-02, formula_export_success=True
  - icbr_no_replay: symbolic_s=1.645744e+00, imitation_mse=1.100515e-02, target_mse=2.632294e-02, formula_export_success=True
  - icbr_no_shared: symbolic_s=3.700043e+00, imitation_mse=9.486527e-03, target_mse=2.348358e-02, formula_export_success=True
  - icbr_refit_commit: symbolic_s=4.856352e+00, imitation_mse=2.704960e-02, target_mse=2.628380e-02, formula_export_success=True
- icbr_full formula (display, rounded):
  - `-2.29848*(asin(0.0499997*x_1 - 0.5) - 0.12941*atanh(1.25*x_2 - 1.85) - 0.266985*atanh(0.4*x_3 - 1.4) - 0.572122)**3 - 1.91342*tan(0.424639*acos(0.3*x_3 - 1.05) + 3.22529*asin(0.0499997*x_1 - 0.5) - 0.0685314*atan(4.45*x_2 - 5.0) - 0.310705) + 1.04236*atan(4.0*(-0.0886067*sin(0.65*x_3 + 4.1) - 9.39837*acos(0.0499997*x_1 - 0.5) + 19.3261)*(-5.09703*asin(0.0499997*x_1 - 0.5) - 2.08024 + 0.494584/(0.0499997 - 1.0*x_2)**3) + 2.3) + 14.4599*atanh(0.00696441*cos(5.0*x_2 - 4.0) - 0.651976*acos(0.0499997*x_1 - 0.5) + 0.449104 + 0.976981*exp(-0.64*(0.0625*x_3 - 1)**2)) + 4.70526 + 0.609043*exp(-96.5805*(atanh(0.0499997*x_1 - 0.4) + 0.0206507*sign(4.975 - 4.6*x_3) + 0.233656 - 0.0458982*exp(-16.0*(1 - 0.7125*x_2)**2))**2)`
- icbr_no_replay formula (display, rounded):
  - `-2.29848*(asin(0.0499997*x_1 - 0.5) - 0.0847613*asin(1.85*x_2 - 2.8) - 0.266985*atanh(0.4*x_3 - 1.4) - 0.578571)**3 - 1.91342*tan(0.424639*acos(0.3*x_3 - 1.05) + 3.22529*asin(0.0499997*x_1 - 0.5) - 0.390239 + 0.102237*exp(-20.25*(1 - 0.966667*x_2)**2)) + 14.3711*asin(0.651976*asin(0.0499997*x_1 - 0.5) - 0.670411 + 0.976981*exp(-0.64*(0.0625*x_3 - 1)**2) - 0.0125666*exp(-24.5025*(1 - 0.717172*x_2)**2)) + 1.04236*atan(4.0*(-0.0164201*Abs(3.1*x_3 - 4.5) + 9.39837*asin(0.0499997*x_1 - 0.5) + 4.65982)*(-5.09703*asin(0.0499997*x_1 - 0.5) + 0.285352*atan(4.2*x_2 - 4.575) - 2.53321) + 2.3) + 6.14812 + 0.609043*exp(-95.2477*(asin(0.0499997*x_1 - 0.5) + 0.314695 - 0.0462182*exp(-16.0*(1 - 0.7125*x_2)**2) + 0.446495*exp(-23.5225*(0.721649 - x_3)**2))**2)`
- icbr_no_shared formula (display, rounded):
  - `-2.2991*(asin(0.0499997*x_1 - 0.5) - 0.12941*atanh(1.25*x_2 - 1.85) - 0.266985*atanh(0.4*x_3 - 1.4) - 0.572022)**3 - 1.91342*tan(0.424639*acos(0.3*x_3 - 1.05) + 3.22529*asin(0.0499997*x_1 - 0.5) - 0.0685314*atan(4.45*x_2 - 5.0) - 0.310705) + 1.04236*atan(4.0*(-0.0886067*sin(0.65*x_3 + 4.1) - 9.39837*acos(0.0499997*x_1 - 0.5) + 19.3261)*(-5.09703*asin(0.0499997*x_1 - 0.5) - 2.08024 + 0.494584/(0.0499997 - 1.0*x_2)**3) + 2.3) + 14.4599*atanh(0.00696441*cos(5.0*x_2 - 4.0) - 0.651976*acos(0.0499997*x_1 - 0.5) + 0.449104 + 0.976981*exp(-0.64*(0.0625*x_3 - 1)**2)) + 4.70536 + 0.609043*exp(-96.5805*(atanh(0.0499997*x_1 - 0.4) + 0.0206507*sign(4.975 - 4.6*x_3) + 0.233656 - 0.0458982*exp(-16.0*(1 - 0.7125*x_2)**2))**2)`
- icbr_refit_commit formula (display, rounded):
  - `-2.7352*(0.607521*asin(0.0779999*x_1 - 0.60124) - 0.121347*atanh(1.2542*x_2 - 1.85668) - 0.348099*atanh(0.102*x_3 - 1.10002) - 1)**3 + 2.55856*tan(-1.59834*asin(0.0783999*x_1 - 0.60392) + 0.261633*asin(0.3674*x_3 - 1.22332) + 0.0579492*atan(4.6*x_2 - 5.0) + 3.22675) - 169.445*atanh(0.000316592*cos(4.97946*x_2 - 0.8) - 0.235849*atanh(0.00416*x_1 - 0.62052) + 0.542492 - 0.0279711*exp(-0.81018*(1 - 0.0888789*x_3)**2)) + 144.918 - 0.616032*exp(-22.6188*(asin(0.0779999*x_1 - 0.60116) + 0.0269613*sign(4.96242 - 4.6*x_3) + 0.00234844 - 0.0841632*exp(-11.1601*(1 - 0.704767*x_2)**2))**2) + 1.80784/(-(0.0890172*sin(0.642*x_3 + 1.00168) + 6.0668*acos(0.60244 - 0.0779599*x_1) - 6.03868)*(-3.2839*asin(0.0781199*x_1 - 0.6018) - 1.50474 - 1.45938/(-x_2 - 0.269348)**4) + 0.488326)**3`

### task=feynman_I_34_1 seed=8

- Task source: feynman_file
- Target formula: `omega_0/(1-v/c)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=2.053738e-02, r2=0.994004
- Variant formula overview:
  - icbr_full: symbolic_s=3.690839e+00, imitation_mse=9.981794e-03, target_mse=1.863173e-02, formula_export_success=True
  - icbr_no_replay: symbolic_s=2.372836e+00, imitation_mse=1.125523e-02, target_mse=1.988849e-02, formula_export_success=True
  - icbr_no_shared: symbolic_s=5.403990e+00, imitation_mse=9.980661e-03, target_mse=1.863953e-02, formula_export_success=True
  - icbr_refit_commit: symbolic_s=6.912233e+00, imitation_mse=1.035334e-02, target_mse=1.584297e-02, formula_export_success=True
- icbr_full formula (display, rounded):
  - `-0.678128*tan(0.611879*cos(0.4*x_3 + 0.3) - 2.75126*acos(0.0499997*x_1 - 0.5) + 4.94385) + 1.06617*tanh(0.35*(0.220012*tan(1.65*x_2 - 2.7) + 14.873*asin(0.0499997*x_1 - 0.5) + 7.97913)*(0.351808*sin(1.9*x_2 + 3.05) + 4.93241*acos(0.0499997*x_1 - 0.5) - 13.9206 + 8.40882*exp(-0.64*(0.0625*x_3 - 1)**2)) - 1.15) + 8.49565*asin(0.00836633*sin(2.45*x_2 + 2.1) - 0.173648*acos(0.3*x_3 - 1.05) + 0.204217*atanh(0.0499997*x_1 - 0.4) - 0.0488533) - 6.50928*asin(0.00630991*cos(2.8*x_2 + 3.1) + 0.299835*acos(0.0499997*x_1 - 0.5) + 0.149094*acos(0.3*x_3 - 1.05) - 0.424173) + 10.0937 + 0.161818*exp(-137.193*(-0.0133529*Abs(3.15*x_3 - 4.2) - atanh(0.0499997*x_1 - 0.4) - 0.0811425)**2) - 0.000911749/(0.0357785*atan(4.65*x_2 - 5.0) - atanh(0.0499997*x_1 - 0.4) + 0.0137419*atanh(0.4*x_3 - 1.4) - 0.520943)**5 + 0.24774/(-(0.329577*cos(0.65*x_3 + 2.6) - 11.5291*atanh(0.0499997*x_1 - 0.4) - 4.04929)*(3.83096*acos(0.0499997*x_1 - 0.5) + 0.153997*atanh(0.3*x_3 - 1.0) - 7.19166 + 3.31799/(-1.0*x_2 - 0.8)**3) - 0.365854)**2`
- icbr_no_replay formula (display, rounded):
  - `-0.678128*tan(-0.0596799*Abs(3.9*x_3 - 4.825) + 2.77098*atanh(0.0499997*x_1 - 0.4) + 0.797979) + 1.06617*tanh(0.35*(0.220012*tan(1.65*x_2 - 2.7) + 14.873*asin(0.0499997*x_1 - 0.5) + 7.97913)*(0.402278*tanh(1.7*x_2 - 2.85) - 4.93241*asin(0.0499997*x_1 - 0.5) - 6.18881 + 8.40882*exp(-0.64*(0.0625*x_3 - 1)**2)) - 1.15) + 8.49565*asin(0.00826338*cos(2.5*x_2 + 0.45) + 0.202763*asin(0.0499997*x_1 - 0.5) + 0.173648*asin(0.3*x_3 - 1.05) - 0.301319) - 6.66094*atanh(0.00630991*cos(2.8*x_2 + 3.1) - 0.299835*asin(0.0499997*x_1 - 0.5) - 0.149094*asin(0.3*x_3 - 1.05) + 0.131002) + 9.1168 + 0.161818*exp(-135.247*(-0.0134486*Abs(3.15*x_3 - 4.2) - asin(0.0499997*x_1 - 0.5) - 0.182098)**2) - 0.0009449/(-asin(0.0499997*x_1 - 0.5) + 0.036035*atan(4.65*x_2 - 5.0) + 0.0138404*atanh(0.4*x_3 - 1.4) - 0.625051)**5 + 0.24774/(-(0.0856324*Abs(2.2*x_3 - 3.1) - 11.447*asin(0.0499997*x_1 - 0.5) - 5.54486)*(-3.83096*asin(0.0499997*x_1 - 0.5) + 0.116329*asin(0.4*x_3 - 1.3) + 0.341057*atan(2.2*x_2 - 2.25) - 1.72313) - 0.365854)**2`
- icbr_no_shared formula (display, rounded):
  - `-0.678128*tan(0.611879*cos(0.4*x_3 + 0.3) - 2.75126*acos(0.0499997*x_1 - 0.5) + 4.94385) + 1.06617*tanh(0.35*(0.220012*tan(1.65*x_2 - 2.7) + 14.873*asin(0.0499997*x_1 - 0.5) + 7.97913)*(0.351808*sin(1.9*x_2 + 3.05) + 4.93241*acos(0.0499997*x_1 - 0.5) - 13.9206 + 8.40882*exp(-0.64*(0.0625*x_3 - 1)**2)) - 1.15) + 8.49565*asin(0.00836633*sin(2.45*x_2 + 2.1) - 0.173648*acos(0.3*x_3 - 1.05) + 0.204217*atanh(0.0499997*x_1 - 0.4) - 0.0488533) - 6.50928*asin(0.00630991*cos(2.8*x_2 + 3.1) + 0.299835*acos(0.0499997*x_1 - 0.5) + 0.149094*acos(0.3*x_3 - 1.05) - 0.424173) + 10.0936 + 0.161818*exp(-137.193*(-0.0133529*Abs(3.15*x_3 - 4.2) - atanh(0.0499997*x_1 - 0.4) - 0.0811425)**2) + 0.000911749/(-0.0357785*atan(4.65*x_2 - 5.0) + atanh(0.0499997*x_1 - 0.4) - 0.0137419*atanh(0.4*x_3 - 1.4) + 0.520943)**5 + 0.248147/(-(0.329577*cos(0.65*x_3 + 2.6) - 11.5291*atanh(0.0499997*x_1 - 0.4) - 4.04929)*(3.83096*acos(0.0499997*x_1 - 0.5) + 0.153997*atanh(0.3*x_3 - 1.0) - 7.19166 + 3.31799/(-1.0*x_2 - 0.8)**3) - 0.366197)**2`
- icbr_refit_commit formula (display, rounded):
  - `3.1168e-48*exp(0.712798*atan(4.7*x_2 - 4.99999) - 149.089*atanh(0.00412*x_1 - 0.63744) + 0.367043*atanh(0.102*x_3 - 1.10006)) - 1.14685*tan(0.324892*sin(0.3994*x_3 + 1.89348) + 8.4961*atanh(0.00599999*x_1 - 0.60006) + 5.84355) + 6.01122*acos(0.0073894*cos(2.56296*x_2 - 2.84792) - 0.905305*acos(0.78896 - 0.04264*x_3) + 0.211247*acos(0.0779999*x_1 - 0.60432) + 0.749365) - 6.39317*asin(0.0113875*sin(2.44748*x_2 - 1.03796) - 1.31098*acos(0.79036 - 0.04264*x_3) - 0.177993*asin(0.0779999*x_1 - 0.60028) + 1.38953) + 1.09001*atan(0.39556*(0.251758*tan(1.4792*x_2 - 2.4712) + 9.35721*asin(0.0799999*x_1 - 0.612) + 6.23688)*(-0.342892*sin(1.95612*x_2 - 0.1708) - 29.5761*atanh(0.00575999*x_1 - 0.60488) - 22.3633 + 5.53811*exp(-0.810432*(1 - 0.0844218*x_3)**2)) - 1.68956) - 0.117022 + 0.163247*exp(-1598.22*(-0.00179074*Abs(4.03592*x_3 - 4.94592) - atanh(0.00607999*x_1 - 0.60012) - 0.635094)**2) + 0.237998/(-(0.349166*sin(0.6004*x_3 + 4.2988) - 88.6811*atanh(0.00416*x_1 - 0.63324) - 65.5066)*(12.8028*acos(0.013*x_1 - 0.60632) + 0.12178*asin(0.38308*x_3 - 1.27768) - 27.6412 + 3.23043/(-x_2 - 0.78561)**3) - 0.357374)**2`

### task=feynman_I_34_1 seed=9

- Task source: feynman_file
- Target formula: `omega_0/(1-v/c)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.957853e-02, r2=0.993839
- Variant formula overview:
  - icbr_full: symbolic_s=3.651372e+00, imitation_mse=8.233731e-03, target_mse=1.544530e-02, formula_export_success=True
  - icbr_no_replay: symbolic_s=2.274345e+00, imitation_mse=8.449504e-03, target_mse=1.540051e-02, formula_export_success=True
  - icbr_no_shared: symbolic_s=5.206228e+00, imitation_mse=8.238061e-03, target_mse=1.546220e-02, formula_export_success=True
  - icbr_refit_commit: symbolic_s=6.681908e+00, imitation_mse=9.369325e-03, target_mse=1.645638e-02, formula_export_success=True
- icbr_full formula (display, rounded):
  - `-2.09461*sin(0.0956881*sin(1.85*x_2 + 3.25) - 0.899439*acos(0.45*x_3 - 1.45) - 1.64003*atanh(0.0499997*x_1 - 0.4) + 4.29254) - 0.084908*Abs(-5.0*(-2.74236*atanh(0.0499997*x_1 - 0.4) - 1.09292)*(0.423006*cos(0.55*x_3 + 2.9) + 0.899169*acos(0.0499997*x_1 - 0.5) - 0.281997*atanh(1.25*x_2 - 1.95) - 1.70627) + 0.35) - 9.93923*acos(0.0747071*asin(0.4*x_3 - 1.3) + 0.283444*atanh(0.0499997*x_1 - 0.4) - 0.298823 - 0.0514346*exp(-1.69*(1 - 0.923077*x_2)**2)) + 1.40423*atan(0.144444*Abs(3.3*x_3 - 3.85) + 16.2078*acos(0.0499997*x_1 - 0.5) + 0.625762*atan(4.725*x_2 - 5.0) - 32.9086) + 25.507 + 0.211245*exp(-560.873*(-0.0261457*tan(0.55*x_3 + 4.45) + atanh(0.0499997*x_1 - 0.4) + 0.0373668*sign(3.4 - 2.9*x_2) + 0.24827)**2) + 4.76351*exp(-2500.97*(-0.0874109*(1 - 0.193548*x_2)**3 + 0.522017*acos(0.0499997*x_1 - 0.5) + 0.0118571*asin(0.3*x_3 - 1.1) - 1)**2) + 0.174364*exp(-11.9025*(-(-4.96276*atanh(0.0499997*x_1 - 0.4) - 1.97781)*(-0.0950954*cos(4.45*x_2 + 0.5) + 0.574656*atanh(0.0499997*x_1 - 0.4) + 0.645591) - 0.710145)**2)`
- icbr_no_replay formula (display, rounded):
  - `-2.09461*sin(0.0937149*cos(1.9*x_2 + 1.6) - 1.62852*asin(0.0499997*x_1 - 0.5) + 0.899439*asin(0.45*x_3 - 1.45) + 2.71594) - 0.084908*Abs(-5.0*(2.72311*acos(0.0499997*x_1 - 0.5) - 5.64374)*(0.0787274*Abs(2.7*x_3 - 3.6) - 0.899169*asin(0.0499997*x_1 - 0.5) - 0.281997*atanh(1.25*x_2 - 1.95) - 0.709661) + 0.35) + 1.40423*atan(0.144444*Abs(3.3*x_3 - 3.85) + 16.2078*acos(0.0499997*x_1 - 0.5) + 0.625762*atan(4.725*x_2 - 5.0) - 32.9086) - 10.1718*atanh(0.281454*acos(0.0499997*x_1 - 0.5) - 0.0747071*asin(0.4*x_3 - 1.3) - 0.32154 + 0.0514346*exp(-1.69*(1 - 0.923077*x_2)**2)) + 8.40289 + 4.76351*exp(-2676.46*(0.0478551*tanh(0.65*x_2 - 0.5) + 0.504612*acos(0.0499997*x_1 - 0.5) - 0.0114617*acos(0.3*x_3 - 1.1) - 1)**2) + 0.211245*exp(-2041.25*(-0.0137052*tan(0.55*x_3 + 4.45) - 0.520505*acos(0.0499997*x_1 - 0.5) + 0.0195871*sign(3.4 - 2.9*x_2) + 1)**2) + 0.174364*exp(-11.9025*(-(-4.92792*asin(0.0499997*x_1 - 0.5) - 2.47252)*(0.0846641*Abs(3.85*x_2 - 4.95) + 0.570622*asin(0.0499997*x_1 - 0.5) + 0.585002) - 0.710145)**2)`
- icbr_no_shared formula (display, rounded):
  - `-2.09461*sin(0.0956881*sin(1.85*x_2 + 3.25) - 0.899439*acos(0.45*x_3 - 1.45) - 1.64003*atanh(0.0499997*x_1 - 0.4) + 4.29254) - 0.084908*Abs(-5.0*(-2.74236*atanh(0.0499997*x_1 - 0.4) - 1.09292)*(0.423006*cos(0.55*x_3 + 2.9) + 0.899169*acos(0.0499997*x_1 - 0.5) - 0.281997*atanh(1.25*x_2 - 1.95) - 1.70627) + 0.35) - 9.93923*acos(0.0747071*asin(0.4*x_3 - 1.3) + 0.283444*atanh(0.0499997*x_1 - 0.4) - 0.298823 - 0.0514346*exp(-1.69*(1 - 0.923077*x_2)**2)) + 1.40423*atan(0.144444*Abs(3.3*x_3 - 3.85) + 16.2078*acos(0.0499997*x_1 - 0.5) + 0.625762*atan(4.725*x_2 - 5.0) - 32.9086) + 25.507 + 0.211245*exp(-560.873*(-0.0261457*tan(0.55*x_3 + 4.45) + atanh(0.0499997*x_1 - 0.4) + 0.0373668*sign(3.4 - 2.9*x_2) + 0.24827)**2) + 4.76351*exp(-2502.74*(0.0872388*(0.195122*x_2 - 1)**3 + 0.521832*acos(0.0499997*x_1 - 0.5) + 0.0118529*asin(0.3*x_3 - 1.1) - 1)**2) + 0.174364*exp(-11.9025*(-(-4.96276*atanh(0.0499997*x_1 - 0.4) - 1.97781)*(-0.0950954*cos(4.45*x_2 + 0.5) + 0.574656*atanh(0.0499997*x_1 - 0.4) + 0.645591) - 0.710145)**2)`
- icbr_refit_commit formula (display, rounded):
  - `2.133*sin(0.0975265*sin(1.77932*x_2 + 3.32628) + 0.961145*acos(1.38884 - 0.42024*x_3) - 12.0421*atanh(0.00428*x_1 - 0.6322) - 10.055) - 0.107197*Abs(3.99708*(19.5933*atanh(0.00436*x_1 - 0.6482) + 15.088)*(0.43146*cos(0.536*x_3 - 0.19992) + 0.53423*atanh(0.0839999*x_1 - 0.6) + 0.57252*atanh(0.64808*x_2 - 1.131) + 0.232961) - 0.4102) - 10.89*acos(0.164072*asin(0.0779999*x_1 - 0.60004) + 0.071162*asin(0.3804*x_3 - 1.27164) - 0.33205 - 0.0452114*exp(-1.77678*(1 - 0.922128*x_2)**2)) - 1.57286*atan(1.37756*sin(0.34*x_3 + 2.1014) - 57.093*acos(0.01136*x_1 - 0.63504) - 0.613885*atan(4.8*x_2 - 5.0) + 127.409) - 0.0698228*atan(-1.01437*tan(0.36304*x_3 - 1.45808) + 132.306*atanh(0.00599999*x_1 - 0.60048) + 0.697677*sign(4.59978 - 3.89*x_2) + 86.6001) + 27.9706 + 47.2137*exp(-17303.2*(0.0203005*(1 - 0.194031*x_2)**3 - 0.449332*acos(0.01144*x_1 - 0.62904) - 0.00224028*asin(0.36612*x_3 - 1.22032) + 1)**2) + 0.162583*exp(-6.95904*(-(-37.9656*atanh(0.00416*x_1 - 0.63608) - 28.4618)*(0.0950912*cos(4.45088*x_2 + 3.64024) + 0.339022*atanh(0.0839999*x_1 - 0.60016) + 0.620877) - 0.73818)**2)`

### task=feynman_I_34_1 seed=10

- Task source: feynman_file
- Target formula: `omega_0/(1-v/c)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.119535e-02, r2=0.996269
- Variant formula overview:
  - icbr_full: symbolic_s=3.268496e+00, imitation_mse=3.028617e-02, target_mse=3.918470e-02, formula_export_success=True
  - icbr_no_replay: symbolic_s=2.085225e+00, imitation_mse=3.297408e-02, target_mse=4.241406e-02, formula_export_success=True
  - icbr_no_shared: symbolic_s=4.742872e+00, imitation_mse=3.009331e-02, target_mse=3.893796e-02, formula_export_success=True
  - icbr_refit_commit: symbolic_s=6.114745e+00, imitation_mse=3.926150e-02, target_mse=4.591067e-02, formula_export_success=True
- icbr_full formula (display, rounded):
  - `36.2392*sqrt(0.01*(-0.03156*sin(1.35*x_3 + 4.9) - 15.2163*asin(0.0499997*x_1 - 0.5) - 7.56064)*(-1.64655*asin(0.0499997*x_1 - 0.5) + 9.7963 - 19.5677*exp(-0.64*(0.0625*x_3 - 1)**2)) + 1) + 86.834*(-0.624072*acos(0.0499997*x_1 - 0.5) - 0.197016*atan(0.4*x_2 - 0.95) - 0.0677851*atanh(0.3*x_3 - 1.0) + 1)**2 + 0.643655*tanh(16.5482*acos(0.0499997*x_1 - 0.5) - 31.7462) - 0.076572*tanh(4.9587*atanh(0.0499997*x_1 - 0.4) + 0.575927) - 0.128277*atan(5.59821*atanh(0.0499997*x_1 - 0.4) + 0.730754) - 5.96972*atanh(0.0499997*(21.5518*sqrt(0.0444444*x_3 + 1) + 0.0237869*Abs(3.1*x_2 - 4.05) + 7.68042*atanh(0.0499997*x_1 - 0.4) - 18.6223)*(10.9519*asin(0.0499997*x_1 - 0.5) - 0.812327*asin(0.75*x_2 - 1.1) + 7.08312 - 4.21448*exp(-0.64*(0.0625*x_3 - 1)**2)) - 0.65) + 14.0846*atanh(0.00322368*Abs(3.95*x_2 - 4.975) - 0.166105*acos(0.3*x_3 - 1.0) + 0.677391*atanh(0.0499997*x_1 - 0.4) + 0.296206) - 34.9679`
- icbr_no_replay formula (display, rounded):
  - `33.8189*(asin(0.0499997*x_1 - 0.5) - 0.0698958*asin(0.45*x_3 - 1.45) - 0.315694*atan(0.4*x_2 - 0.95) + 0.0353457)**2 + 0.067525*Abs(2.5*(1.64655*asin(0.0499997*x_1 - 0.5) - 9.7963 + 19.5677*exp(-0.64*(0.0625*x_3 - 1)**2))*(15.2163*asin(0.0499997*x_1 - 0.5) + 7.53223 + 0.0647704*exp(-3.24*(0.472222*x_3 - 1)**2)) + 4.8) - 14.0179*acos(0.00322368*Abs(3.95*x_2 - 4.975) + 0.672572*asin(0.0499997*x_1 - 0.5) + 0.166105*asin(0.3*x_3 - 1.0) + 0.00279523) - 6.1819*asin(0.0499997*(21.5518*sqrt(0.0444444*x_3 + 1) + 0.0237869*Abs(3.1*x_2 - 4.05) + 7.62578*asin(0.0499997*x_1 - 0.5) - 17.8569)*(10.9519*asin(0.0499997*x_1 - 0.5) - 0.812327*asin(0.75*x_2 - 1.1) + 7.08312 - 4.21448*exp(-0.64*(0.0625*x_3 - 1)**2)) - 0.7) + 23.2899 + 1.60724*exp(-89.4185*(asin(0.0499997*x_1 - 0.5) + 0.448827)**2) + 0.113697*exp(-16.2268*(-asin(0.0499997*x_1 - 0.5) - 0.389991)**2) + 0.204862*exp(-17.3787*(-asin(0.0499997*x_1 - 0.5) - 0.393757)**2)`
- icbr_no_shared formula (display, rounded):
  - `36.2392*sqrt(0.01*(-0.03156*sin(1.35*x_3 + 4.9) - 15.2163*asin(0.0499997*x_1 - 0.5) - 7.56064)*(-1.64655*asin(0.0499997*x_1 - 0.5) + 9.7963 - 19.5677*exp(-0.64*(0.0625*x_3 - 1)**2)) + 1) + 86.4647*(-0.624289*acos(0.0499997*x_1 - 0.5) - 0.197084*atan(0.4*x_2 - 0.95) - 0.0678086*atanh(0.3*x_3 - 1.0) + 1)**2 + 0.643655*tanh(16.5482*acos(0.0499997*x_1 - 0.5) - 31.7462) - 0.076572*tanh(4.9587*atanh(0.0499997*x_1 - 0.4) + 0.575927) - 0.128277*atan(5.59821*atanh(0.0499997*x_1 - 0.4) + 0.730754) - 5.96972*atanh(0.0499997*(21.5518*sqrt(0.0444444*x_3 + 1) + 0.0237869*Abs(3.1*x_2 - 4.05) + 7.68042*atanh(0.0499997*x_1 - 0.4) - 18.6223)*(10.9519*asin(0.0499997*x_1 - 0.5) - 0.812327*asin(0.75*x_2 - 1.1) + 7.08312 - 4.21448*exp(-0.64*(0.0625*x_3 - 1)**2)) - 0.65) + 14.0846*atanh(0.00322368*Abs(3.95*x_2 - 4.975) - 0.166105*acos(0.3*x_3 - 1.0) + 0.677391*atanh(0.0499997*x_1 - 0.4) + 0.296206) - 34.9673`
- icbr_refit_commit formula (display, rounded):
  - `36.2193*sqrt(0.0100059*(-57.8878*sqrt(0.0299304*x_3 + 1) - 1.05779*asin(0.0783599*x_1 - 0.60296) + 57.5922)*(-52.1159*asin(0.01256*x_1 - 0.61692) - 34.2877 - 0.0664385*exp(-2.4336*(1 - 0.462051*x_3)**2)) + 1) + 49.1549*(0.53657*acos(0.6007 - 0.0779999*x_1) - 0.384636*atan(0.30196*x_2 - 0.94884) - 0.0902956*atanh(0.3*x_3 - 1.00004) - 1)**2 - 0.0804627*tanh(35.2719*atanh(0.0042*x_1 - 0.638) + 25.2546) - 0.125227*atan(45.7578*atanh(0.00396*x_1 - 0.6382) + 32.9082) - 34.3929*atanh(0.004*(22.1753*log(0.0961599*x_3 + 4.45092) + 0.0205728*Abs(3.56864*x_2 - 4.68896) + 59.3459*atanh(0.00412*x_1 - 0.63564) + 11.206)*(-1.36264*tan(0.44868*x_2 - 3.77908) + 76.8097*atanh(0.00416*x_1 - 0.68072) + 64.2022 - 2.70835*exp(-0.810648*(1 - 0.0866319*x_3)**2)) - 0.80018) + 214.274*atanh(0.000136026*Abs(3.94512*x_2 - 4.94788) + 0.0379019*acos(0.77732 - 0.04548*x_3) + 0.0187266*asin(0.0781199*x_1 - 0.60016) - 0.621087) + 75.6773 + 2.99241*exp(-26.9934*(acos(0.60236 - 0.0777599*x_1) - 0.970594)**2)`

### task=feynman_I_34_1 seed=11

- Task source: feynman_file
- Target formula: `omega_0/(1-v/c)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=2.325557e-02, r2=0.993461
- Variant formula overview:
  - icbr_full: symbolic_s=3.525921e+00, imitation_mse=1.331795e-02, target_mse=2.580416e-02, formula_export_success=True
  - icbr_no_replay: symbolic_s=2.278331e+00, imitation_mse=1.593997e-02, target_mse=3.832632e-02, formula_export_success=True
  - icbr_no_shared: symbolic_s=5.213783e+00, imitation_mse=1.331369e-02, target_mse=2.582834e-02, formula_export_success=True
  - icbr_refit_commit: symbolic_s=6.344876e+00, imitation_mse=nan, target_mse=nan, formula_export_success=True
- icbr_full formula (display, rounded):
  - `42.2959*sqrt(0.0111111*(-0.0576469*Abs(3.3*x_2 - 4.4) + 1.23414*acos(0.4*x_3 - 1.3) - 3.65837*asin(0.0499997*x_1 - 0.5) - 5.4771)*(-0.192319*Abs(3.8*x_2 - 4.75) + 1.39975*acos(0.35*x_3 - 1.2) - 1.16354*atanh(0.0499997*x_1 - 0.4) - 4.93143) + 1) - 3.85141*tan(7.80207*(1 - 0.654321*x_2)**4 + 1.41835*tan(0.05*x_1 - 3.55) - 0.013476*Abs(2.8*x_3 - 4.3) - 3.34829) - 2.17257*tanh(5.68857*(1 - 0.297436*x_2)**3 + 54.5145*tan(0.05*x_1 - 3.55) - 0.109562*Abs(3.85*x_3 - 4.8) + 14.7825) + 8.42661*asin(0.00972691*sqrt(x_3 - 1) + 0.760784*tan(0.05*x_1 - 3.55) + 0.0147379*Abs(3.5*x_2 - 4.55) - 0.14725) + 1.54454*atan(0.560852*cos(2.55*x_2 + 0.4) - 9.77279*tan(0.05*x_1 - 3.55) + 1.10316*asin(0.4*x_3 - 1.4) - 2.25768) - 37.2552 + 5.7353*exp(-1.44*(0.291667*(8.50681*tan(0.05*x_1 - 3.55) - 1.73916*atanh(0.35*x_3 - 1.15) + 1.47859)*(-0.0925915*tan(0.55*x_3 - 5.0) - 0.415149*acos(0.8*x_2 - 1.3) + 0.507813*asin(0.0499997*x_1 - 0.5) + 1.13534) + 1)**2)`
- icbr_no_replay formula (display, rounded):
  - `-3.85141*tan(7.80207*(1 - 0.654321*x_2)**4 + 1.41835*tan(0.05*x_1 - 3.55) - 0.013476*Abs(2.8*x_3 - 4.3) - 3.34829) - 2.21683*tanh(0.6*(8.50681*tan(0.05*x_1 - 3.55) - 1.36434*asin(0.45*x_3 - 1.45) + 1.52341)*(0.510776*tan(0.05*x_1 - 3.55) + 0.471384*tan(0.7*x_2 - 4.25) - 0.154413*atanh(0.35*x_3 - 1.35) + 0.392948) + 0.4) + 4.39815*asin(0.0499997*(-3.67972*tan(0.05*x_1 - 3.55) - 0.0576469*Abs(3.3*x_2 - 4.4) - 1.23414*asin(0.4*x_3 - 1.3) - 3.20234)*(-1.16212*tan(0.05*x_1 - 3.55) - 0.192319*Abs(3.8*x_2 - 4.75) - 1.39975*asin(0.35*x_3 - 1.2) - 2.74252) - 0.55) - 1.54454*atan(9.77279*tan(0.05*x_1 - 3.55) + 1.10316*acos(0.4*x_3 - 1.4) - 0.280413 + 1.36736*exp(-1.69*(1 - 0.923077*x_2)**2)) + 8.49708*atanh(0.760784*tan(0.05*x_1 - 3.55) + 0.0147379*Abs(3.5*x_2 - 4.55) + 0.00693214*atanh(0.4*x_3 - 1.4) - 0.0321318) + 6.73591 + 1.81413*exp(-2825.09*(tan(0.05*x_1 - 3.55) - 0.00200978*Abs(3.85*x_3 - 4.8) - 0.0213363*atan(1.85*x_2 - 2.2) + 0.302207)**2)`
- icbr_no_shared formula (display, rounded):
  - `43.4213*sqrt(0.0108108*(-0.0576469*Abs(3.3*x_2 - 4.4) + 1.23414*acos(0.4*x_3 - 1.3) - 3.65837*asin(0.0499997*x_1 - 0.5) - 5.4771)*(-0.192319*Abs(3.8*x_2 - 4.75) + 1.39975*acos(0.35*x_3 - 1.2) - 1.16354*atanh(0.0499997*x_1 - 0.4) - 4.93143) + 1) - 3.85141*tan(7.80207*(1 - 0.654321*x_2)**4 + 1.41835*tan(0.05*x_1 - 3.55) - 0.013476*Abs(2.8*x_3 - 4.3) - 3.34829) - 2.17257*tanh(5.68857*(1 - 0.297436*x_2)**3 + 54.5145*tan(0.05*x_1 - 3.55) - 0.109562*Abs(3.85*x_3 - 4.8) + 14.7825) + 8.42661*asin(0.00972691*sqrt(x_3 - 1) + 0.760784*tan(0.05*x_1 - 3.55) + 0.0147379*Abs(3.5*x_2 - 4.55) - 0.14725) + 1.54454*atan(0.560852*cos(2.55*x_2 + 0.4) - 9.77279*tan(0.05*x_1 - 3.55) + 1.10316*asin(0.4*x_3 - 1.4) - 2.25768) - 38.3797 + 5.7353*exp(-1.44*(-0.291667*(8.50681*tan(0.05*x_1 - 3.55) - 1.73916*atanh(0.35*x_3 - 1.15) + 1.47859)*(-0.0925915*tan(0.55*x_3 - 5.0) + 0.507813*asin(0.0499997*x_1 - 0.5) + 0.415149*asin(0.8*x_2 - 1.3) + 0.483221) - 1)**2)`
- icbr_refit_commit formula (display, rounded):
  - `41.9561*sqrt(0.0112051*(-0.0647393*Abs(2.9532*x_2 - 3.97152) - 13.2075*asin(0.0118*x_1 - 0.62472) - 1.28732*asin(0.38416*x_3 - 1.27976) - 10.6004)*(0.751229*acos(0.0773999*x_1 - 0.60088) - 1.34033*asin(0.36532*x_3 - 1.2196) - 4.48673 + 0.577685*exp(-4.83824*(1 - 0.802873*x_2)**2)) + 1) - 27.4399*tanh(4.45471*(1 - 0.29791*x_2)**3 + 219.507*tan(0.00635999*x_1 - 0.67836) - 0.0805725*Abs(4.04144*x_3 - 4.75076) + 171.989) + 26.5071*asin(0.00270018*sqrt(0.999938*x_3 - 1) + 0.00490031*Abs(2.92916*x_2 - 3.83772) + 0.737038*acos(0.61648 - 0.01224*x_1) - 1.26302) - 1.65687*atan(0.514842*cos(2.6512*x_2 - 2.864) + 43.0292*tan(0.00799999*x_1 - 0.6) + 1.00596*acos(0.41912*x_3 - 1.42192) + 26.2262) - 6.53595*atanh(3.48947*(1 - 0.664239*x_2)**4 + 3.10603*tan(0.00799999*x_1 - 0.60184) - 0.00557322*Abs(3.2*x_3 - 4.99991) + 1.37316) - 1.30371 + 7.50137*exp(-1.69104*(-0.24454*(48.7034*tan(0.00631999*x_1 - 0.60488) - 1.87137*atanh(0.33*x_3 - 1.1) + 31.5281)*(-0.0757098*tan(0.48736*x_3 - 1.8898) - 0.413647*acos(0.80276*x_2 - 1.30456) + 0.34652*asin(0.0735999*x_1 - 0.60044) + 1.0602) - 1)**2)`

### task=feynman_I_34_1 seed=12

- Task source: feynman_file
- Target formula: `omega_0/(1-v/c)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=2.463624e-02, r2=0.992108
- Variant formula overview:
  - icbr_full: symbolic_s=3.293169e+00, imitation_mse=2.083176e-02, target_mse=3.339599e-02, formula_export_success=True
  - icbr_no_replay: symbolic_s=2.110923e+00, imitation_mse=2.728264e-02, target_mse=4.003515e-02, formula_export_success=True
  - icbr_no_shared: symbolic_s=4.835019e+00, imitation_mse=2.083176e-02, target_mse=3.339599e-02, formula_export_success=True
  - icbr_refit_commit: symbolic_s=6.180443e+00, imitation_mse=2.077909e-02, target_mse=3.196098e-02, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0.324372*cos(0.111597*Abs(2.7*x_3 - 4.3) - 13.0751*atanh(0.0499997*x_1 - 0.4) - 9.72703 + 0.807346*exp(-16.0*(1 - 0.7125*x_2)**2)) + 0.658152*tan(0.215742*tanh(1.4*x_2 - 2.4) - 3.34877*asin(0.0499997*x_1 - 0.5) + 0.208704*atanh(0.45*x_3 - 1.45) - 0.0665566) - 40.0065*tanh(10.7395*(1 - 0.602151*x_2)**3 - 9.38809*acos(0.0499997*x_1 - 0.5) - 0.285723*atanh(0.3*x_3 - 1.25) + 19.8491) - 7.3954*acos(0.339345*asin(0.0499997*x_1 - 0.5) + 0.0796194*asin(0.4*x_3 - 1.35) - 0.2687 - 0.0213117*exp(-15.21*(1 - 0.74359*x_2)**2)) - 4.90039*atanh(0.0919104*acos(0.35*x_3 - 1.2) - 0.451068*asin(0.0499997*x_1 - 0.5) - 0.152742 + 0.110442*exp(-1.1025*(1 - 0.666667*x_2)**2)) + 61.1332 - 3.4621*exp(-0.0399999*(0.500001*(0.179701*sin(2.4*x_2 - 0.85) + 3.42199*asin(0.0499997*x_1 - 0.5) - 1.51995*asin(0.4*x_3 - 1.35) - 0.782044)*(-0.711451*sin(0.9*x_3 + 3.3) + 1.87114*acos(0.0499997*x_1 - 0.5) - 7.74247 + 1.37728*exp(-1.1025*(1.0 - x_2)**2)) + 1)**2)`
- icbr_no_replay formula (display, rounded):
  - `0.658152*tan(3.34877*acos(0.0499997*x_1 - 0.5) + 0.189402*atan(1.6*x_2 - 2.7) + 0.208704*atanh(0.45*x_3 - 1.45) - 5.33433) + 1.31843*atan(0.373395*tan(0.55*x_3 + 4.45) + 24.7055*acos(0.0499997*x_1 - 0.5) - 47.5104 - 1.55607*exp(-25.0*(1 - x_2)**2)) + 4.90039*atanh(0.115685*(1 - 0.666667*x_2)**2 - 0.451068*acos(0.0499997*x_1 - 0.5) + 0.0919104*asin(0.35*x_3 - 1.2) + 0.606531) - 7.57014*atanh(0.339345*acos(0.0499997*x_1 - 0.5) - 0.0796194*asin(0.4*x_3 - 1.35) - 0.414341 + 0.0213117*exp(-15.21*(1 - 0.74359*x_2)**2)) + 10.0189 + 0.647188*exp(-362.588*(0.00445919*Abs(2.7*x_3 - 4.3) + 0.518795*acos(0.0499997*x_1 - 0.5) - 1 + 0.0322599*exp(-16.0*(1 - 0.7125*x_2)**2))**2) - 3.4621*exp(-0.0399999*(0.500001*(-0.183909*Abs(2.75*x_3 - 4.45) + 1.87114*acos(0.0499997*x_1 - 0.5) - 6.88899 + 1.37728*exp(-1.1025*(1.0 - x_2)**2))*(-3.42199*acos(0.0499997*x_1 - 0.5) - 1.51995*asin(0.4*x_3 - 1.35) + 4.3041 + 0.470285*exp(-1.1025*(1.0 - x_2)**2)) + 1)**2)`
- icbr_no_shared formula (display, rounded):
  - `0.324372*cos(0.111597*Abs(2.7*x_3 - 4.3) - 13.0751*atanh(0.0499997*x_1 - 0.4) - 9.72703 + 0.807346*exp(-16.0*(1 - 0.7125*x_2)**2)) + 0.658152*tan(0.215742*tanh(1.4*x_2 - 2.4) - 3.34877*asin(0.0499997*x_1 - 0.5) + 0.208704*atanh(0.45*x_3 - 1.45) - 0.0665566) - 40.0065*tanh(10.7395*(1 - 0.602151*x_2)**3 - 9.38809*acos(0.0499997*x_1 - 0.5) - 0.285723*atanh(0.3*x_3 - 1.25) + 19.8491) - 7.3954*acos(0.339345*asin(0.0499997*x_1 - 0.5) + 0.0796194*asin(0.4*x_3 - 1.35) - 0.2687 - 0.0213117*exp(-15.21*(1 - 0.74359*x_2)**2)) - 4.90039*atanh(0.0919104*acos(0.35*x_3 - 1.2) - 0.451068*asin(0.0499997*x_1 - 0.5) - 0.152742 + 0.110442*exp(-1.1025*(1 - 0.666667*x_2)**2)) + 61.1332 - 3.4621*exp(-0.0399999*(0.500001*(0.179701*sin(2.4*x_2 - 0.85) + 3.42199*asin(0.0499997*x_1 - 0.5) - 1.51995*asin(0.4*x_3 - 1.35) - 0.782044)*(-0.711451*sin(0.9*x_3 + 3.3) + 1.87114*acos(0.0499997*x_1 - 0.5) - 7.74247 + 1.37728*exp(-1.1025*(1.0 - x_2)**2)) + 1)**2)`
- icbr_refit_commit formula (display, rounded):
  - `0.632226*(0.190406*(-0.1825*sin(2.35352*x_2 + 2.35816) - 1.42067*acos(1.39752 - 0.42368*x_3) + 2.20845*asin(0.0779999*x_1 - 0.60046) + 1.10314)*(0.711274*cos(0.90036*x_3 - 1.413) - 10.8861*atanh(0.00599999*x_1 - 0.60004) - 9.8961 - 1.18006*exp(-8.41*(1 - 0.436552*x_2)**2)) + 1)**(3/2) + 0.324563*cos(0.114054*Abs(2.6138*x_3 - 4.224) - 92.4879*atanh(0.00436*x_1 - 0.6532) - 70.4341 + 0.946119*exp(-11.1465*(1 - 0.704766*x_2)**2)) + 0.55996*tan(0.11932*tanh(1.43896*x_2 - 2.44424) - 1.23153*asin(0.0779999*x_1 - 0.60018) + 0.209407*atanh(0.2488*x_3 - 1.16048) + 4.04083) + 6.67554*acos(-0.0948095*asin(0.38324*x_3 - 1.27912) - 3.01737*atanh(0.00408*x_1 - 0.63004) - 1.81445 + 0.0268227*exp(-10.2358*(1 - 0.740153*x_2)**2)) + 4.18584*acos(-3.9679*atanh(0.0044*x_1 - 0.61604) - 0.121789*atanh(0.29984*x_3 - 0.99988) - 2.49746 + 0.116703*exp(-1.2167*(1 - 0.666667*x_2)**2)) - 1.14059*atan(28.2634*(1 - 0.602159*x_2)**3 - 0.469261*tan(0.32972*x_3 + 4.68564) - 15.9922*acos(0.0777599*x_1 - 0.60016) + 30.4946) - 10.3704`

### task=feynman_I_34_1 seed=13

- Task source: feynman_file
- Target formula: `omega_0/(1-v/c)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=2.830283e-02, r2=0.990871
- Variant formula overview:
  - icbr_full: symbolic_s=3.072203e+00, imitation_mse=1.736820e-02, target_mse=2.102674e-02, formula_export_success=True
  - icbr_no_replay: symbolic_s=1.981463e+00, imitation_mse=1.953233e-02, target_mse=2.344195e-02, formula_export_success=True
  - icbr_no_shared: symbolic_s=4.492872e+00, imitation_mse=1.736318e-02, target_mse=2.102106e-02, formula_export_success=True
  - icbr_refit_commit: symbolic_s=5.485739e+00, imitation_mse=2.820233e-02, target_mse=2.972704e-02, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0.445935*(-0.129412*(0.731357*cos(0.9*x_3 + 1.7) + 0.708878*tan(1.55*x_2 - 2.5) + 7.47948*atanh(0.0499997*x_1 - 0.4) + 6.00651)*(0.280978*Abs(2.8*x_3 - 3.25) + 4.99801*acos(0.0499997*x_1 - 0.5) + 0.130726*atan(1.3*x_2 - 2.3) - 9.48841) - 1)**2 + 1.65517*cos(0.221233*Abs(2.3*x_3 - 3.7) - 0.722958*acos(0.0499997*x_1 - 0.5) + 0.366936) + 1.59282*tanh(0.644161*tan(0.45*x_2 - 4.95) + 35.2653*acos(0.0499997*x_1 - 0.5) + 0.864658*asin(0.35*x_3 - 1.35) - 66.3359) - 0.430766*tanh(-0.84878*tan(1.25*x_2 - 2.25) + 21.9324*atanh(0.0499997*x_1 - 0.4) + 1.67764*sign(4.4 - 3.75*x_3) + 5.16078) + 0.0950911*Abs(13.2114*asin(0.0499997*x_1 - 0.5) + 10.0142*atanh(0.4*x_3 - 1.35) + 28.6755 - 5.10685*exp(-2.1025*(0.896552*x_2 - 1)**2)) + 1.35795 + 0.0677632*exp(-3.0625*(-0.542857*(-4.28129*atanh(0.0499997*x_1 - 0.4) - 1.70599)*(8.36035*atanh(0.0499997*x_1 - 0.4) + 3.33141) - 1)**2)`
- icbr_no_replay formula (display, rounded):
  - `0.445935*(-0.129412*(0.708878*tan(1.55*x_2 - 2.5) + 0.184424*Abs(2.8*x_3 - 4.5) - 7.42771*acos(0.0499997*x_1 - 0.5) + 17.5359)*(0.280978*Abs(2.8*x_3 - 3.25) + 4.99801*acos(0.0499997*x_1 - 0.5) + 0.130726*atan(1.3*x_2 - 2.3) - 9.48841) - 1)**2 - 0.400482*(0.306011*Abs(2.3*x_3 - 3.7) - acos(0.0499997*x_1 - 0.5) + 0.512066)**2 + 0.430766*tanh(0.84878*tan(1.25*x_2 - 2.25) + 21.7805*acos(0.0499997*x_1 - 0.5) - 1.67764*sign(4.4 - 3.75*x_3) - 41.5606) + 1.59282*tanh(35.2653*acos(0.0499997*x_1 - 0.5) + 2.11206*atan(2.6*x_2 - 2.35) + 0.821575*atanh(0.35*x_3 - 1.25) - 69.8898) + 0.0950911*Abs(13.2114*acos(0.0499997*x_1 - 0.5) - 10.0142*atanh(0.4*x_3 - 1.35) - 49.4279 + 5.10685*exp(-2.1025*(1 - 0.896552*x_2)**2)) + 3.00692 + 0.0677632*exp(-3.0625*(-0.542857*(17.2066 - 8.30248*acos(0.0499997*x_1 - 0.5))*(4.25166*acos(0.0499997*x_1 - 0.5) - 8.8114) - 1)**2)`
- icbr_no_shared formula (display, rounded):
  - `0.445935*(-0.129412*(0.731357*cos(0.9*x_3 + 1.7) + 0.708878*tan(1.55*x_2 - 2.5) + 7.47948*atanh(0.0499997*x_1 - 0.4) + 6.00651)*(0.231413*Abs(3.4*x_3 - 3.95) + 4.99801*acos(0.0499997*x_1 - 0.5) + 0.130726*atan(1.3*x_2 - 2.3) - 9.48775) - 1)**2 + 1.65517*cos(0.221233*Abs(2.3*x_3 - 3.7) - 0.722958*acos(0.0499997*x_1 - 0.5) + 0.366936) + 1.59282*tanh(0.644161*tan(0.45*x_2 - 4.95) + 35.2653*acos(0.0499997*x_1 - 0.5) + 0.864658*asin(0.35*x_3 - 1.35) - 66.3359) - 0.430766*tanh(-0.84878*tan(1.25*x_2 - 2.25) + 21.9324*atanh(0.0499997*x_1 - 0.4) + 1.67764*sign(4.4 - 3.75*x_3) + 5.16078) + 0.0950911*Abs(13.2114*asin(0.0499997*x_1 - 0.5) + 10.0142*atanh(0.4*x_3 - 1.35) + 28.6755 - 5.10685*exp(-2.1025*(0.896552*x_2 - 1)**2)) + 1.35795 + 0.0677632*exp(-3.0625*(-0.542857*(-4.28129*atanh(0.0499997*x_1 - 0.4) - 1.70599)*(8.36035*atanh(0.0499997*x_1 - 0.4) + 3.33141) - 1)**2)`
- icbr_refit_commit formula (display, rounded):
  - `0.55917*(-0.108902*(0.913939*tan(1.24036*x_2 + 1.05008) + 1.67641*Abs(0.30916*x_3 - 0.5158) + 56.2571*atanh(0.00424*x_1 - 0.63564) + 44.3808)*(0.143669*tanh(1.178*x_2 - 2.09862) + 0.175174*Abs(4.46656*x_3 - 4.87076) - 16.861*acos(0.6214 - 0.01272*x_1) + 16.0919) - 1)**2 + 1.40668*cos(0.203392*Abs(2.736*x_3 - 4.56396) + 0.508903*acos(0.60098 - 0.0779999*x_1) + 4.57531) + 9.62053*tanh(0.199237*tan(0.30184*x_2 + 4.55596) + 0.338659*tan(0.37588*x_3 - 1.34112) - 9.92339*acos(0.60224 - 0.0782799*x_1) + 11.3367) - 0.479627*tanh(-0.760473*tan(0.668*x_2 - 4.88084) + 118.411*atanh(0.00424*x_1 - 0.63892) + 1.08232*sign(4.909 - 4.3*x_3) + 86.2545) + 0.133046*Abs(29.5574*asin(0.014*x_1 - 0.60034) + 9.20268*atanh(0.33116*x_3 - 1.19032) + 37.6069 - 3.61657*exp(-2.32587*(0.879639*x_2 - 1)**2)) - 0.020488*sign(-1.236*(64.2664*atanh(0.00412*x_1 - 0.63844) + 48.4336)*(-31.7242*atanh(0.00428*x_1 - 0.63876) - 23.9221) - 5.0) + 9.2459`

### task=feynman_I_34_1 seed=14

- Task source: feynman_file
- Target formula: `omega_0/(1-v/c)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=3.044471e-02, r2=0.990929
- Variant formula overview:
  - icbr_full: symbolic_s=2.907365e+00, imitation_mse=4.479099e-02, target_mse=6.196485e-02, formula_export_success=True
  - icbr_no_replay: symbolic_s=1.966621e+00, imitation_mse=4.572953e-02, target_mse=6.719739e-02, formula_export_success=True
  - icbr_no_shared: symbolic_s=4.268457e+00, imitation_mse=4.479131e-02, target_mse=6.196536e-02, formula_export_success=True
  - icbr_refit_commit: symbolic_s=5.534221e+00, imitation_mse=nan, target_mse=nan, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0.440957*sin(5.31993*atanh(0.0499997*x_1 - 0.4) + 2.03293*atanh(0.4*x_3 - 1.3) + 8.34555) + 0.0897439*Abs(2.85*(36.8925*sqrt(0.04*x_3 + 1) + 9.14371*asin(0.0499997*x_1 - 0.5) - 32.6069)*(30.3113*sqrt(0.0444444*x_3 + 1) + 0.281031*cos(2.8*x_2 + 0.05) + 4.39037*asin(0.0499997*x_1 - 0.5) - 27.4585) + 5.0) + 6.8083*acos(0.0999997*(0.505419*(0.35*x_2 + 1)**(3/2) + 4.90534*(0.010101*x_3 + 1)**(3/2) + 6.21845*acos(0.0499997*x_1 - 0.5) - 18.3828)*(-114.942*sqrt(0.0111111*x_3 + 1) - 0.507787*sin(2.0*x_2 + 2.95) - 3.40729*asin(0.0499997*x_1 - 0.5) + 112.188) - 0.9) - 4.83542*asin(0.891031*acos(0.0499997*x_1 - 0.5) - 0.431024 - 1.42862*exp(-0.64*(0.0625*x_3 - 1)**2) + 0.0240152*exp(-8.1225*(1 - 0.77193*x_2)**2)) - 13.8537 + 1.298*exp(-298.132*(atanh(0.0499997*x_1 - 0.4) + 0.235961 + 0.0472277*exp(-25.0*(1 - 0.995*x_2)**2) - 0.379697*exp(-23.5225*(0.927835 - x_3)**2))**2)`
- icbr_no_replay formula (display, rounded):
  - `0.440957*sin(5.28217*asin(0.0499997*x_1 - 0.5) + 2.17145*asin(0.4*x_3 - 1.4) + 9.11412) + 0.0897439*Abs(-2.85*(15.0144*(1 - 0.0326087*x_3)**(3/2) - 9.14371*asin(0.0499997*x_1 - 0.5) - 19.3026)*(-31.4826*log(0.1*x_3 + 4.675) + 4.39037*acos(0.0499997*x_1 - 0.5) + 38.4213 + 0.666113*exp(-2.25*(1 - 0.9*x_2)**2)) - 5.0) - 6.78024*atanh(0.0999997*(0.0754528*x_3 + 0.505419*(0.35*x_2 + 1)**(3/2) - 6.21845*asin(0.0499997*x_1 - 0.5) - 3.71103)*(0.533332*cos(1.9*x_2 + 4.65) - 0.138302*Abs(4.55*x_3 - 4.925) - 3.40729*asin(0.0499997*x_1 - 0.5) - 3.46312) - 0.75) + 9.50425*atanh(0.00466104*Abs(3.85*x_2 - 4.95) + 0.445514*asin(0.0499997*x_1 - 0.5) - 0.597408 + 0.71431*exp(-0.64*(0.0625*x_3 - 1)**2)) - 1.13777 + 1.298*exp(-293.915*(asin(0.0499997*x_1 - 0.5) + 0.338026 + 0.0475654*exp(-25.0*(1 - 0.995*x_2)**2) - 0.382411*exp(-23.5225*(0.927835 - x_3)**2))**2)`
- icbr_no_shared formula (display, rounded):
  - `0.25577*(-36.8925*sqrt(0.04*x_3 + 1) - 9.14371*asin(0.0499997*x_1 - 0.5) + 32.6069)*(-30.3113*sqrt(0.0444444*x_3 + 1) - 0.281031*cos(2.8*x_2 + 0.05) - 4.39037*asin(0.0499997*x_1 - 0.5) + 27.4585) + 0.440957*sin(5.31993*atanh(0.0499997*x_1 - 0.4) + 2.03293*atanh(0.4*x_3 - 1.3) + 8.34555) + 6.8083*acos(0.0999997*(0.512*(0.346154*x_2 + 1)**(3/2) + 4.90534*(0.010101*x_3 + 1)**(3/2) + 6.21845*acos(0.0499997*x_1 - 0.5) - 18.3897)*(-114.942*sqrt(0.0111111*x_3 + 1) - 0.507787*sin(2.0*x_2 + 2.95) - 3.40729*asin(0.0499997*x_1 - 0.5) + 112.188) - 0.9) - 4.83542*asin(0.891031*acos(0.0499997*x_1 - 0.5) - 0.431024 - 1.42862*exp(-0.64*(0.0625*x_3 - 1)**2) + 0.0240152*exp(-8.1225*(1 - 0.77193*x_2)**2)) - 13.405 + 1.298*exp(-298.132*(atanh(0.0499997*x_1 - 0.4) + 0.235961 + 0.0472277*exp(-25.0*(0.995*x_2 - 1)**2) - 0.379697*exp(-23.5225*(0.927835 - x_3)**2))**2)`
- icbr_refit_commit formula (display, rounded):
  - `0.255654*(-37.7779*sqrt(0.0390109*x_3 + 1) - 5.87978*acos(0.6028 - 0.0782799*x_1) + 43.7835)*(-31.2764*sqrt(0.0429905*x_3 + 1) - 13.7455*acos(0.60014 - 0.014*x_1) + 43.0159 + 0.70893*exp(-1.95994*(1 - 0.905727*x_2)**2)) - 0.42561*sin(3.37043*acos(0.60336 - 0.0787599*x_1) + 2.00688*asin(0.43212*x_3 - 1.43604) - 0.0919071) + 8.47755*acos(-0.00582281*cos(4.45044*x_2 + 3.64104) - 1.70973*acos(0.62228 - 0.01232*x_1) + 2.37613 - 0.547137*exp(-0.810036*(1 - 0.0799981*x_3)**2)) - 8.46259*atanh(0.0799999*(-1.46182*(-0.062439*x_2 - 1)**3 + 4.90149*(0.0101088*x_3 + 1)**(3/2) - 19.4649*acos(0.60044 - 0.014*x_1) + 11.6929)*(-64.6707*sqrt(0.0200025*x_3 + 1) - 0.522646*sin(1.94004*x_2 - 3.25552) - 2.1899*asin(0.0783199*x_1 - 0.603) + 62.31) - 0.70002) - 13.9663 + 1.05209*exp(-73870.0*(0.499051*atanh(0.00436*x_1 - 0.64016) + 0.365457 + 0.00521022*exp(-8.83041*(0.806259 - x_2)**2) - exp(-3.79735*(0.0177966 - x_3)**2))**2)`

### task=feynman_I_34_1 seed=15

- Task source: feynman_file
- Target formula: `omega_0/(1-v/c)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=5.435445e-02, r2=0.983432
- Variant formula overview:
  - icbr_full: symbolic_s=2.699599e+00, imitation_mse=8.594024e-03, target_mse=4.446702e-02, formula_export_success=True
  - icbr_no_replay: symbolic_s=1.725073e+00, imitation_mse=1.045958e-02, target_mse=4.434548e-02, formula_export_success=True
  - icbr_no_shared: symbolic_s=3.936974e+00, imitation_mse=8.594024e-03, target_mse=4.446702e-02, formula_export_success=True
  - icbr_refit_commit: symbolic_s=4.741560e+00, imitation_mse=nan, target_mse=nan, formula_export_success=True
- icbr_full formula (display, rounded):
  - `15.184*(0.01*(1.74314*cos(0.35*x_3 + 0.45) - 0.87456*tan(1.1*x_2 + 4.35) - 3.09491)*(-0.32624*sin(1.8*x_2 + 3.25) + 1.85683*cos(0.45*x_3 + 0.0999997) + 4.1348*atanh(0.0499997*x_1 - 0.4) - 1.38284) + 1)**(3/2) + 0.0388592*cos(7.35115*atanh(0.0499997*x_1 - 0.4) + 2.12944) - 1.43421*tan(0.300326*acos(0.4*x_3 - 1.4) + 2.12896*atanh(0.0499997*x_1 - 0.4) - 4.03639) - 9.21061*tan(0.0939915*acos(0.4*x_3 - 1.4) - 0.559854*atanh(0.0499997*x_1 - 0.4) - 0.152174 + 0.0236979*exp(-4.2025*(1 - 0.829268*x_2)**2)) + 1.51538*tanh(1.08562*tan(1.3*x_2 - 2.25) + 31.5481*acos(0.0499997*x_1 - 0.5) - 60.3074) - 10.9912 + 0.453882*exp(-6.25*(-(-3.66334*atanh(0.0499997*x_1 - 0.4) - 1.45984)*(4.57265*atanh(0.0499997*x_1 - 0.4) + 1.8222) - 0.74)**2)`
- icbr_no_replay formula (display, rounded):
  - `1.43421*tan(0.300326*asin(0.4*x_3 - 1.4) - 2.12896*atanh(0.0499997*x_1 - 0.4) + 3.56464) - 1.51538*tanh(-1.08562*tan(1.3*x_2 - 2.25) + 31.5481*asin(0.0499997*x_1 - 0.5) + 10.7517) + 0.0510327*Abs(4.6*(0.87456*tan(1.1*x_2 + 4.35) + 0.217665*Abs(2.7*x_3 - 3.25) + 1.92043)*(0.32624*sin(1.8*x_2 + 3.25) + 0.211732*Abs(3.7*x_3 - 4.675) + 4.10552*acos(0.0499997*x_1 - 0.5) - 7.04511) + 3.05) + 9.20963*atanh(0.0128474*Abs(2.25*x_2 - 2.75) + 0.555886*asin(0.0499997*x_1 - 0.5) + 0.093991*asin(0.4*x_3 - 1.4) + 0.0345517) + 3.97562 + 0.0835127*exp(-16.4434*(-asin(0.0499997*x_1 - 0.5) - 0.366087)**2) + 0.453882*exp(-6.25*(-(9.40976 - 4.54026*acos(0.0499997*x_1 - 0.5))*(-3.63739*asin(0.0499997*x_1 - 0.5) - 1.82495) - 0.74)**2)`
- icbr_no_shared formula (display, rounded):
  - `15.184*(0.01*(1.74314*cos(0.35*x_3 + 0.45) - 0.87456*tan(1.1*x_2 + 4.35) - 3.09491)*(-0.32624*sin(1.8*x_2 + 3.25) + 1.85683*cos(0.45*x_3 + 0.0999997) + 4.1348*atanh(0.0499997*x_1 - 0.4) - 1.38284) + 1)**(3/2) + 0.0388592*cos(7.35115*atanh(0.0499997*x_1 - 0.4) + 2.12944) - 1.43421*tan(0.300326*acos(0.4*x_3 - 1.4) + 2.12896*atanh(0.0499997*x_1 - 0.4) - 4.03639) - 9.21061*tan(0.0939915*acos(0.4*x_3 - 1.4) - 0.559854*atanh(0.0499997*x_1 - 0.4) - 0.152174 + 0.0236979*exp(-4.2025*(1 - 0.829268*x_2)**2)) + 1.51538*tanh(1.08562*tan(1.3*x_2 - 2.25) + 31.5481*acos(0.0499997*x_1 - 0.5) - 60.3074) - 10.9912 + 0.453882*exp(-6.25*(-(-3.66334*atanh(0.0499997*x_1 - 0.4) - 1.45984)*(4.57265*atanh(0.0499997*x_1 - 0.4) + 1.8222) - 0.74)**2)`
- icbr_refit_commit formula (display, rounded):
  - `0.233758*(1.81806*cos(0.334*x_3 + 0.5002) - 1.27324*tan(0.6552*x_2 + 1.65648) - 3.54485)*(-0.329753*sin(1.772*x_2 + 3.30046) - 1.88522*cos(0.44*x_3 + 3.30022) + 30.762*atanh(0.00416*x_1 - 0.65008) + 20.8051) - 0.0409459*sin(54.119*atanh(0.00396*x_1 - 0.64064) + 38.794) - 1.3439*tan(0.288429*acos(0.41856*x_3 - 1.4196) + 15.5539*atanh(0.00396*x_1 - 0.68084) + 7.9955) + 33.9069*tanh(0.83336*tan(0.89396*x_2 + 1.32912) - 11.7987*acos(0.60056 - 0.0779999*x_1) + 12.7122) - 52.7442*atanh(0.00122355*cos(3.45112*x_2 + 2.14004) - 0.0108486*acos(1.41796 - 0.41696*x_3) - 0.0430552*asin(0.0779999*x_1 - 0.60036) + 0.575983) + 69.6316 + 0.377491*exp(-2.59803*(-(36.485*atanh(0.00384*x_1 - 0.65292) + 28.4062)*(-27.3353*atanh(0.0042*x_1 - 0.64412) - 20.8623) - 0.62021)**2)`

### task=feynman_I_34_1 seed=16

- Task source: feynman_file
- Target formula: `omega_0/(1-v/c)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=4.391044e-02, r2=0.987287
- Variant formula overview:
  - icbr_full: symbolic_s=3.214648e+00, imitation_mse=2.063552e-02, target_mse=4.057738e-02, formula_export_success=True
  - icbr_no_replay: symbolic_s=2.079890e+00, imitation_mse=2.401805e-02, target_mse=4.349615e-02, formula_export_success=True
  - icbr_no_shared: symbolic_s=4.659942e+00, imitation_mse=2.063733e-02, target_mse=4.057841e-02, formula_export_success=True
  - icbr_refit_commit: symbolic_s=5.831883e+00, imitation_mse=2.200801e-02, target_mse=4.155270e-02, formula_export_success=True
- icbr_full formula (display, rounded):
  - `13.273*sqrt(sqrt(0.0437158*x_3 + 1) - 0.127188*acos(0.0499997*x_1 - 0.5) - 0.385746) - 14.7145*(-0.115583*asin(0.0499997*x_1 - 0.5) + 1 - 0.574162*exp(-0.64*(0.0625*x_3 - 1)**2))**(3/2) - 17.8932*(-0.00197767*cos(2.85*x_2 + 3.05) - 0.116581*atanh(0.0499997*x_1 - 0.4) + 1 - 0.621216*exp(-0.64*(0.0625*x_3 - 1)**2))**(3/2) - 0.882412*log(3.35*(-8.41539*asin(0.0499997*x_1 - 0.5) + 0.685057*atan(1.2*x_2 - 2.0) - 3.18045)*(0.126199*Abs(2.9*x_2 - 3.45) - 0.0563974*Abs(3.45*x_3 - 4.4) - 6.76036*atanh(0.0499997*x_1 - 0.4) - 2.55258) + 0.5) + 1.00341*atan(0.388762*tan(1.0*x_2 + 3.95) - 1.72638*acos(0.35*x_3 - 1.2) - 7.16223*atanh(0.0499997*x_1 - 0.4) + 1.47967) + 14.1232 + 1.09929*exp(-17.64*(-(0.052832*Abs(3.1*x_3 - 3.65) - 5.35209*asin(0.0499997*x_1 - 0.5) - 2.54941)*(-7.56822*sqrt(0.071066*x_3 + 1) + 2.07687*acos(0.0499997*x_1 - 0.5) + 3.12448 + 0.100786*exp(-15.6025*(1 - 0.746835*x_2)**2)) + 0.202381)**2)`
- icbr_no_replay formula (display, rounded):
  - `-10.895*(0.141223*acos(0.0499997*x_1 - 0.5) + 1 - 0.701529*exp(-0.64*(0.0625*x_3 - 1)**2))**(3/2) - 12.9601*(0.00242076*sin(2.9*x_2 - 4.875) + 0.143531*acos(0.0499997*x_1 - 0.5) + 1 - 0.770243*exp(-0.64*(0.0625*x_3 - 1)**2))**(3/2) - 0.882412*log(3.35*(0.512334*cos(1.6*x_2 - 4.2) + 8.41539*acos(0.0499997*x_1 - 0.5) - 16.4174)*(0.126199*Abs(2.9*x_2 - 3.45) - 0.0563974*Abs(3.45*x_3 - 4.4) - 6.71281*asin(0.0499997*x_1 - 0.5) - 3.22645) + 0.5) - 3.92331*asin(1.00431*(1 - 0.0333333*x_3)**(3/2) + 0.294649*acos(0.0499997*x_1 - 0.5) - 0.994381) - 0.475377*atan(5.0*(0.052832*Abs(3.1*x_3 - 3.65) + 5.35209*acos(0.0499997*x_1 - 0.5) - 10.9565)*(-7.56822*sqrt(0.071066*x_3 + 1) + 2.07687*acos(0.0499997*x_1 - 0.5) + 3.12448 + 0.100786*exp(-15.6025*(1 - 0.746835*x_2)**2)) - 1.6) + 1.00341*atan(7.11185*acos(0.0499997*x_1 - 0.5) - 1.72638*acos(0.35*x_3 - 1.2) + 1.31862*atan(3.9*x_2 - 3.6) - 12.335) + 25.272`
- icbr_no_shared formula (display, rounded):
  - `13.273*sqrt(sqrt(0.0437158*x_3 + 1) - 0.127188*acos(0.0499997*x_1 - 0.5) - 0.385746) - 14.6747*(-0.116016*asin(0.0499997*x_1 - 0.5) + 1 - 0.576312*exp(-0.64*(0.0625*x_3 - 1)**2))**(3/2) - 17.9356*(-0.00197068*cos(2.85*x_2 + 3.05) - 0.116169*atanh(0.0499997*x_1 - 0.4) + 1 - 0.61902*exp(-0.64*(0.0625*x_3 - 1)**2))**(3/2) - 0.882412*log(3.35*(-8.41539*asin(0.0499997*x_1 - 0.5) + 0.685057*atan(1.2*x_2 - 2.0) - 3.18045)*(0.126199*Abs(2.9*x_2 - 3.45) - 0.0512109*Abs(3.8*x_3 - 4.85) - 6.76036*atanh(0.0499997*x_1 - 0.4) - 2.55269) + 0.5) + 1.00341*atan(0.388762*tan(1.0*x_2 + 3.95) - 1.72638*acos(0.35*x_3 - 1.2) - 7.16223*atanh(0.0499997*x_1 - 0.4) + 1.47967) + 14.1283 + 1.09929*exp(-17.64*(-(0.0585003*Abs(2.8*x_3 - 3.3) - 5.35209*asin(0.0499997*x_1 - 0.5) - 2.54927)*(-7.56822*sqrt(0.071066*x_3 + 1) + 2.07687*acos(0.0499997*x_1 - 0.5) + 3.12448 + 0.100786*exp(-15.6025*(1 - 0.746835*x_2)**2)) + 0.202381)**2)`
- icbr_refit_commit formula (display, rounded):
  - `13.3245*sqrt(sqrt(0.0440403*x_3 + 1) + 0.0813382*acos(0.60444 - 0.0792799*x_1) - 0.718938) - 12.6028*(-0.0809035*asin(0.0779999*x_1 - 0.60006) + 1 - 0.410126*exp(-0.81*(1 - 0.0844443*x_3)**2))**(3/2) - 14.367*(-0.00233052*cos(2.691*x_2 + 3.30612) - 0.0856935*asin(0.0779999*x_1 - 0.60002) + 1 - 0.46926*exp(-0.810612*(1 - 0.0844125*x_3)**2))**(3/2) - 0.865439*log(3.735*(0.684197*atan(1.2014*x_2 - 2.00136) - 66.347*atanh(0.00404*x_1 - 0.63852) - 48.9738)*(0.0936572*Abs(3.83172*x_2 - 4.534) - 0.0535779*Abs(3.57496*x_3 - 4.1894) - 52.6114*atanh(0.00416*x_1 - 0.62712) - 38.5053) + 0.50132) + 1.06823*atan(0.10695*tan(0.20308*x_2 + 4.57136) + 1.52659*asin(0.36804*x_3 - 1.2244) - 54.1709*atanh(0.00384*x_1 - 0.64428) - 39.7372) + 14.8471 + 1.11325*exp(-9.65047*(-(-0.498412*sin(0.34084*x_3 + 2.10028) - 3.45395*asin(0.0779999*x_1 - 0.6011) - 1.62423)*(-8.73338*log(0.0956799*x_3 + 3.13412) + 1.33226*acos(0.0784399*x_1 - 0.60684) + 6.92451 + 0.109071*exp(-11.56*(1 - 0.742941*x_2)**2)) + 0.121486)**2)`

### task=feynman_I_34_1 seed=17

- Task source: feynman_file
- Target formula: `omega_0/(1-v/c)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.968483e-02, r2=0.993354
- Variant formula overview:
  - icbr_full: symbolic_s=3.800079e+00, imitation_mse=1.579683e-02, target_mse=2.669173e-02, formula_export_success=True
  - icbr_no_replay: symbolic_s=2.385637e+00, imitation_mse=1.722890e-02, target_mse=2.702296e-02, formula_export_success=True
  - icbr_no_shared: symbolic_s=5.606648e+00, imitation_mse=1.579542e-02, target_mse=2.668757e-02, formula_export_success=True
  - icbr_refit_commit: symbolic_s=7.056598e+00, imitation_mse=3.144688e-02, target_mse=3.743775e-02, formula_export_success=True
- icbr_full formula (display, rounded):
  - `-4.21121*(-0.0332599*asin(0.4*x_3 - 1.4) - 0.447266*atanh(0.0499997*x_1 - 0.4) + 1 + 0.0421584*exp(-2.1025*(1 - 0.896552*x_2)**2))**(3/2) + 1.75601*tanh(0.35*(0.0678574*tan(0.5*x_2 - 5.0) + 0.142775*Abs(3.7*x_3 - 4.575) - 6.83803*atanh(0.0499997*x_1 - 0.4) - 1.95569)*(1.47561*tan(0.8*x_2 - 4.4) + 0.207557*Abs(2.4*x_3 - 4.3) + 7.63848*atanh(0.0499997*x_1 - 0.4) + 5.19633) - 1.25) + 1.07977*atan(0.319854*tanh(1.4*x_2 - 2.5) - 1.45217*acos(0.35*x_3 - 1.2) - 4.36445*atanh(0.0499997*x_1 - 0.4) + 1.39541) + 6.15038 + 0.832617*exp(-111.587*(0.557801*acos(0.0499997*x_1 - 0.5) + 0.171019*asin(0.4*x_3 - 1.4) - 1)**2) + 0.51293*exp(-107.896*(0.0138516*Abs(2.2*x_3 - 4.1) + atanh(0.0499997*x_1 - 0.4) + 0.146893)**2) + 36.2313*exp(-416.444*(-0.0240241*tan(0.8*x_2 + 4.7) - 0.478632*acos(0.0499997*x_1 - 0.5) + 1)**2) + 8.01966*exp(-(0.05*(-10.7264*sqrt(0.147541*x_3 + 1) - 0.0721223*Abs(3.65*x_2 - 4.75) + 2.09682*atanh(0.0499997*x_1 - 0.4) + 11.7367)*(-0.493747*cos(1.0*x_2 - 3.4) + 0.0885652*Abs(2.5*x_3 - 4.7) - 8.23887*atanh(0.0499997*x_1 - 0.4) - 3.69352) - 1.0)**2)`
- icbr_no_replay formula (display, rounded):
  - `15.756*sqrt(0.351076*asin(0.0499997*x_1 - 0.5) + 0.0262909*asin(0.4*x_3 - 1.4) + 1 - 0.0333249*exp(-2.1025*(1 - 0.896552*x_2)**2)) + 1.75601*tanh(0.35*(0.0678574*tan(0.5*x_2 - 5.0) + 0.142775*Abs(3.7*x_3 - 4.575) - 6.7902*asin(0.0499997*x_1 - 0.5) - 2.63744)*(1.47561*tan(0.8*x_2 - 4.4) + 0.207557*Abs(2.4*x_3 - 4.3) + 7.58504*asin(0.0499997*x_1 - 0.5) + 5.95788) - 1.25) + 0.0722588*Abs(4.65*(0.580868*tanh(0.85*x_2 - 1.5) - 0.0885652*Abs(2.5*x_3 - 4.7) + 8.18124*asin(0.0499997*x_1 - 0.5) + 4.48351)*(0.0721223*Abs(3.65*x_2 - 4.75) - 2.08215*asin(0.0499997*x_1 - 0.5) + 2.08042*asin(0.3*x_3 - 1.05) + 1.25128) + 1.9) - 1.07977*atan(4.33392*asin(0.0499997*x_1 - 0.5) - 1.45217*asin(0.35*x_3 - 1.2) - 0.242241*atan(1.85*x_2 - 3.15) + 1.35558) - 10.7799 + 0.832617*exp(-111.587*(0.557801*acos(0.0499997*x_1 - 0.5) + 0.171019*asin(0.4*x_3 - 1.4) - 1)**2) + 0.51293*exp(-106.392*(0.0139492*Abs(2.2*x_3 - 4.1) + asin(0.0499997*x_1 - 0.5) + 0.248331)**2) + 36.2313*exp(-95.4028*(-0.0501933*tan(0.8*x_2 + 4.7) + asin(0.0499997*x_1 - 0.5) + 0.51849)**2)`
- icbr_no_shared formula (display, rounded):
  - `-4.18278*(-0.0334785*asin(0.4*x_3 - 1.4) - 0.450206*atanh(0.0499997*x_1 - 0.4) + 1 + 0.0424356*exp(-2.1025*(1 - 0.896552*x_2)**2))**(3/2) + 1.75601*tanh(0.35*(0.0678574*tan(0.5*x_2 - 5.0) + 0.142775*Abs(3.7*x_3 - 4.575) - 6.83803*atanh(0.0499997*x_1 - 0.4) - 1.95569)*(1.47561*tan(0.8*x_2 - 4.4) + 0.207557*Abs(2.4*x_3 - 4.3) + 7.63848*atanh(0.0499997*x_1 - 0.4) + 5.19633) - 1.25) + 1.07977*atan(0.319854*tanh(1.4*x_2 - 2.5) - 1.45217*acos(0.35*x_3 - 1.2) - 4.36445*atanh(0.0499997*x_1 - 0.4) + 1.39541) + 6.12193 + 0.832617*exp(-111.587*(0.557801*acos(0.0499997*x_1 - 0.5) + 0.171019*asin(0.4*x_3 - 1.4) - 1)**2) + 0.51293*exp(-107.896*(0.0138516*Abs(2.2*x_3 - 4.1) + atanh(0.0499997*x_1 - 0.4) + 0.146893)**2) + 36.2313*exp(-416.444*(-0.0240241*tan(0.8*x_2 + 4.7) - 0.478632*acos(0.0499997*x_1 - 0.5) + 1)**2) + 8.01966*exp(-(0.05*(-10.7264*sqrt(0.147541*x_3 + 1) - 0.0721223*Abs(3.65*x_2 - 4.75) + 2.09682*atanh(0.0499997*x_1 - 0.4) + 11.7367)*(-0.493747*cos(1.0*x_2 - 3.4) + 0.0885652*Abs(2.5*x_3 - 4.7) - 8.23887*atanh(0.0499997*x_1 - 0.4) - 3.69352) - 1.0)**2)`
- icbr_refit_commit formula (display, rounded):
  - `3.32721*(0.0601746*(-10.8574*sqrt(0.145454*x_3 + 1) - 0.0719563*Abs(3.6226*x_2 - 4.73232) + 12.1124*atanh(0.00599999*x_1 - 0.6001) + 19.3922)*(-0.484616*cos(1.01752*x_2 - 3.4198) + 0.506572*Abs(0.4504*x_3 - 0.89968) - 5.28017*acos(0.60004 - 0.0779999*x_1) + 4.73857) + 1)**(3/2) - 7.33996*(-0.199774*acos(0.60116 - 0.0774799*x_1) - 0.0239506*asin(0.38492*x_3 - 1.37772) + 1 + 0.0318926*exp(-1.69*(1 - 0.910769*x_2)**2))**(3/2) + 3.69552*tanh(0.21664*(0.0444303*tan(0.30056*x_2 - 1.738) + 0.12593*Abs(4.13784*x_3 - 4.74684) - 53.1422*atanh(0.00404*x_1 - 0.6422) - 39.6342)*(1.76286*tan(0.67492*x_2 - 1.08544) + 0.232924*Abs(2.19672*x_3 - 4.19388) + 55.9486*atanh(0.00404*x_1 - 0.67052) + 47.506) - 1.42452) + 1.10941*atan(0.306836*tanh(1.40728*x_2 - 2.50908) + 1.33658*acos(1.22124 - 0.36648*x_3) - 32.2632*atanh(0.00416*x_1 - 0.63528) - 25.4909) + 7.27272 + 0.996759*exp(-341.774*(0.0510247*asin(0.42156*x_3 - 1.42356) - atanh(0.00611999*x_1 - 0.60012) - 0.644073)**2) + 0.510305*exp(-2485.03*(0.00181964*Abs(2.48624*x_3 - 4.88128) + atanh(0.00456*x_1 - 0.64532) + 0.728458)**2) + 109.587*exp(-130.688*(-0.0459641*tan(0.29956*x_2 - 4.46) - 0.448757*acos(0.0773199*x_1 - 0.60024) + 1)**2)`

### task=feynman_I_34_1 seed=18

- Task source: feynman_file
- Target formula: `omega_0/(1-v/c)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=2.223324e-02, r2=0.993207
- Variant formula overview:
  - icbr_full: symbolic_s=2.812961e+00, imitation_mse=9.411777e-03, target_mse=2.260610e-02, formula_export_success=True
  - icbr_no_replay: symbolic_s=1.834624e+00, imitation_mse=2.226523e-02, target_mse=5.059660e-02, formula_export_success=True
  - icbr_no_shared: symbolic_s=4.448654e+00, imitation_mse=9.405413e-03, target_mse=2.261068e-02, formula_export_success=True
  - icbr_refit_commit: symbolic_s=5.340941e+00, imitation_mse=9.014816e-03, target_mse=2.164201e-02, formula_export_success=True
- icbr_full formula (display, rounded):
  - `-18.7994*(-0.0984578*atanh(0.0499997*x_1 - 0.4) + 1 - 0.317275*exp(-(0.1*x_3 - 1.0)**2))**(3/2) - 99.6692*(-0.786536*sqrt(0.0212766*x_3 + 1) + 0.00243367*cos(3.15*x_2 - 3.7) - 0.0180871*asin(0.0499997*x_1 - 0.5) + 1)**(3/2) + 0.302623*sin(1.1*(0.122439*Abs(2.55*x_3 - 3.1) + 0.269913)*(-5.97138*asin(0.0499997*x_1 - 0.5) + 0.759469*atanh(0.3*x_3 - 1.0) - 2.26644) + 0.65) + 2.11164*tanh(1.53474*atan(4.65*x_2 - 5.0) - 7.70088*atanh(0.0499997*x_1 - 0.4) + 0.525196*atanh(0.3*x_3 - 1.3) - 3.72039) - 0.966528*asin(0.193483*sin(0.45*x_3 + 1.65) - 0.0520956*cos(4.6*x_2 + 3.35) + 2.91514*asin(0.0499997*x_1 - 0.5) + 0.33024) + 27.8799 - 1.59027/(3.6*(-5.74698*asin(0.0499997*x_1 - 0.5) - 2.88328)*(0.123431*acos(0.4*x_3 - 1.3) + 5.8314*atanh(0.0499997*x_1 - 0.4) + 1.9769) + 0.55)`
- icbr_no_replay formula (display, rounded):
  - `-14.3855*(0.116868*acos(0.0499997*x_1 - 0.5) + 1 - 0.379241*exp(-(0.1*x_3 - 1.0)**2))**(3/2) - 10.2324*(0.0110999*cos(3.15*x_2 - 3.7) + 0.0824945*acos(0.0499997*x_1 - 0.5) + 1 - 0.438381*exp(-(0.1*x_3 - 1.0)**2))**(3/2) + 2.11164*tanh(0.347463*log(4.775*x_3 - 4.7) + 7.64725*acos(0.0499997*x_1 - 0.5) - 15.6578 - 2.13552*exp(-24.5025*(1 - 0.979798*x_2)**2)) + 0.372808*Abs(0.158499*Abs(3.25*x_2 - 4.25) + 0.0600638*Abs(3.8*x_3 - 4.95) + 8.12074*acos(0.0499997*x_1 - 0.5) - 13.2253) + 1.62887*atan(4.0*(5.74698*acos(0.0499997*x_1 - 0.5) - 11.9106)*(-5.79079*acos(0.0499997*x_1 - 0.5) + 0.123431*acos(0.4*x_3 - 1.3) + 11.6544) + 0.95) + 30.414 - 0.686169*exp(-1.21*(0.5*(0.122439*Abs(2.55*x_3 - 3.1) + 0.269913)*(5.97138*acos(0.0499997*x_1 - 0.5) - 0.564547*acos(0.4*x_3 - 1.35) - 10.7482) + 1)**2)`
- icbr_no_shared formula (display, rounded):
  - `-18.884*(-0.0979593*atanh(0.0499997*x_1 - 0.4) + 1 - 0.315668*exp(-(0.1*x_3 - 1.0)**2))**(3/2) - 105.796*(-0.794874*sqrt(0.020202*x_3 + 1) + 0.00233878*cos(3.15*x_2 - 3.7) - 0.0173819*asin(0.0499997*x_1 - 0.5) + 1)**(3/2) + 0.302623*sin(1.1*(0.122439*Abs(2.55*x_3 - 3.1) + 0.269913)*(-5.97138*asin(0.0499997*x_1 - 0.5) + 0.759469*atanh(0.3*x_3 - 1.0) - 2.26644) + 0.65) + 2.11164*tanh(1.53474*atan(4.65*x_2 - 5.0) - 7.70088*atanh(0.0499997*x_1 - 0.4) + 0.525196*atanh(0.3*x_3 - 1.3) - 3.72039) - 0.966528*asin(0.193483*sin(0.45*x_3 + 1.65) - 0.0520956*cos(4.6*x_2 + 3.35) + 2.91514*asin(0.0499997*x_1 - 0.5) + 0.33024) + 27.9661 - 1.59027/(3.6*(-5.74698*asin(0.0499997*x_1 - 0.5) - 2.88328)*(-0.123431*asin(0.4*x_3 - 1.3) + 5.8314*atanh(0.0499997*x_1 - 0.4) + 2.17078) + 0.55)`
- icbr_refit_commit formula (display, rounded):
  - `-31.1117*(-0.257224*acos(0.62756 - 0.01208*x_1) + 1 - 0.345416*exp(-0.81*(1 - 0.0755555*x_3)**2))**(3/2) - 14.0879*(0.00802215*cos(3.732*x_2 - 4.5015) - 0.0434314*asin(0.0779999*x_1 - 0.60026) + 1 - 0.493481*exp(-0.810108*(1 - 0.0799946*x_3)**2))**(3/2) - 0.289507*sin(1.1498*(0.0783534*Abs(3.94424*x_3 - 4.44404) + 0.250249)*(-18.6848*asin(0.014*x_1 - 0.60102) + 0.759009*atanh(0.30016*x_3 - 1.00036) - 11.2168) - 2.41244) - 3.42468*tanh(4.0883*asin(0.0779999*x_1 - 0.60194) - 1.27331*atan(4.65*x_2 - 4.9981) - 0.435014*atanh(0.30032*x_3 - 1.30032) + 3.39541) - 0.966665*asin(0.19799*sin(0.438*x_3 - 4.5997) + 0.0520718*cos(4.60208*x_2 + 0.20576) + 1.88079*asin(0.0779999*x_1 - 0.60144) - 0.00632263) + 2.28879*atan(4.99967*(-3.70883*asin(0.0779999*x_1 - 0.6002) - 2.21756)*(0.129512*acos(0.38224*x_3 - 1.27592) + 3.73706*asin(0.0779999*x_1 - 0.60032) + 1.87352) + 0.8) + 30.8222`

### task=feynman_I_34_1 seed=19

- Task source: feynman_file
- Target formula: `omega_0/(1-v/c)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.441680e-02, r2=0.995479
- Variant formula overview:
  - icbr_full: symbolic_s=3.828243e+00, imitation_mse=1.381758e-02, target_mse=1.578507e-02, formula_export_success=True
  - icbr_no_replay: symbolic_s=2.438200e+00, imitation_mse=1.684926e-02, target_mse=3.397158e-02, formula_export_success=True
  - icbr_no_shared: symbolic_s=5.562981e+00, imitation_mse=1.381758e-02, target_mse=1.578506e-02, formula_export_success=True
  - icbr_refit_commit: symbolic_s=6.648230e+00, imitation_mse=1.527372e-02, target_mse=1.735632e-02, formula_export_success=True
- icbr_full formula (display, rounded):
  - `-0.325926*(-0.113636*(0.839717*cos(0.85*x_3 + 1.9) + 0.925615*tanh(1.2*x_2 - 2.0) - 8.77877*acos(0.0499997*x_1 - 0.5) + 21.2975)*(-7.88024*tan(0.05*x_1 - 3.55) + 0.33673*tanh(2.35*x_2 - 3.95) + 0.148833*Abs(3.25*x_3 - 4.35) - 1.78971) - 1)**3 - 14.9374*(-0.00874553*cos(1.95*x_2 - 4.95) - 0.140399*tan(0.05*x_1 - 3.55) + 1 - 0.469494*exp(-0.64*(0.0625*x_3 - 1)**2))**(3/2) + 4.26194*log(0.1*(2.83514 - 7.29281*exp(-(0.1*x_3 - 1.0)**2))*(0.440427*cos(1.8*x_2 + 4.8) + 0.0979183*Abs(2.65*x_3 - 3.7) + 5.85337*acos(0.0499997*x_1 - 0.5) - 12.8848) + 4.55) + 0.202354*tan(-2.88179*tan(0.05*x_1 - 3.55) + 0.0526482*Abs(3.75*x_2 - 4.3) + 0.0718309*atanh(0.35*x_3 - 1.35) + 0.545755) - 1.1376*tanh(6.03614*tan(0.05*x_1 - 3.55) + 3.26322 - 5.55115*exp(-(0.1*x_3 - 1.0)**2)) - 6.75326*acos(0.00979462*sin(2.75*x_2 - 4.65) + 0.325688*tan(0.05*x_1 - 3.55) - 0.621217 + 0.4806*exp(-(0.1*x_3 - 1.0)**2)) + 18.0918 + 0.000667499/(-tan(0.05*x_1 - 3.55) + 0.0107598*tan(0.6*x_3 - 2.1) + 0.0402015*atan(4.6*x_2 - 5.0) - 0.453578)**4`
- icbr_no_replay formula (display, rounded):
  - `4.20547*sqrt(0.0444444*(2.83514 - 7.29281*exp(-(0.1*x_3 - 1.0)**2))*(-0.418021*sin(1.9*x_2 + 3.1) - 5.88686*tan(0.05*x_1 - 3.55) + 0.0979183*Abs(2.65*x_3 - 3.7) - 3.13656) + 1) - 14.9465*(-0.0082876*sin(2.05*x_2 - 3.5) - 0.140342*tan(0.05*x_1 - 3.55) + 1 - 0.469302*exp(-0.64*(0.0625*x_3 - 1)**2))**(3/2) + 0.202354*tan(0.0499*log(4.525*x_3 - 4.45) - 2.88179*tan(0.05*x_1 - 3.55) + 0.0526482*Abs(3.75*x_2 - 4.3) + 0.418296) + 1.37637*tanh(0.3*(0.691344*sin(1.6*x_2 - 2.65) + 8.82899*tan(0.05*x_1 - 3.55) + 0.214985*Abs(2.7*x_3 - 4.25) + 5.68986)*(-7.88024*tan(0.05*x_1 - 3.55) + 0.33673*tanh(2.35*x_2 - 3.95) + 0.148833*Abs(3.25*x_3 - 4.35) - 1.78971) - 1.5) - 1.1376*tanh(6.03614*tan(0.05*x_1 - 3.55) + 3.26322 - 5.55115*exp(-(0.1*x_3 - 1.0)**2)) - 6.91236*atanh(0.00958531*cos(2.8*x_2 + 3.15) - 0.325688*tan(0.05*x_1 - 3.55) + 0.471462 - 0.4806*exp(-(0.1*x_3 - 1.0)**2)) + 10.1623 + 0.000336215/(tan(0.05*x_1 - 3.55) - 0.0764693*atan(4.775*x_3 - 5.0) + 0.559824 + 0.0578696*exp(-20.25*(1 - 0.988889*x_2)**2))**5`
- icbr_no_shared formula (display, rounded):
  - `-0.325926*(-0.113636*(0.839717*cos(0.85*x_3 + 1.9) + 0.925615*tanh(1.2*x_2 - 2.0) - 8.77877*acos(0.0499997*x_1 - 0.5) + 21.2975)*(-7.88024*tan(0.05*x_1 - 3.55) + 0.33673*tanh(2.35*x_2 - 3.95) + 0.148833*Abs(3.25*x_3 - 4.35) - 1.78971) - 1)**3 - 14.9374*(-0.00874553*cos(1.95*x_2 - 4.95) - 0.140399*tan(0.05*x_1 - 3.55) + 1 - 0.469494*exp(-0.64*(0.0625*x_3 - 1)**2))**(3/2) + 4.26194*log(0.1*(2.83514 - 7.29281*exp(-(0.1*x_3 - 1.0)**2))*(0.440427*cos(1.8*x_2 + 4.8) + 0.0979183*Abs(2.65*x_3 - 3.7) + 5.85337*acos(0.0499997*x_1 - 0.5) - 12.8848) + 4.55) + 0.202354*tan(-2.88179*tan(0.05*x_1 - 3.55) + 0.0526482*Abs(3.75*x_2 - 4.3) + 0.0718309*atanh(0.35*x_3 - 1.35) + 0.545755) - 1.1376*tanh(6.03614*tan(0.05*x_1 - 3.55) + 3.26322 - 5.55115*exp(-(0.1*x_3 - 1.0)**2)) - 6.75326*acos(0.00979462*sin(2.75*x_2 - 4.65) + 0.325688*tan(0.05*x_1 - 3.55) - 0.621217 + 0.4806*exp(-(0.1*x_3 - 1.0)**2)) + 18.0918 + 0.000667499/(tan(0.05*x_1 - 3.55) - 0.0107598*tan(0.6*x_3 - 2.1) - 0.0402015*atan(4.6*x_2 - 5.0) + 0.453578)**4`
- icbr_refit_commit formula (display, rounded):
  - `-0.326073*(-0.113601*(0.317986*sin(2.39904*x_2 - 4.11088) - 41.1069*tan(0.00627999*x_1 - 0.6774) + 0.147855*Abs(3.19412*x_3 - 3.89312) - 31.527)*(0.922846*tanh(1.20368*x_2 - 2.00464) + 0.279014*Abs(2.06132*x_3 - 3.29496) + 30.3074*acos(0.6104 - 0.01252*x_1) - 25.7324) - 1)**3 - 24.418*(-0.00627343*cos(1.976*x_2 + 1.30028) - 0.360286*acos(0.62248 - 0.01204*x_1) + 1 - 0.22485*exp(-0.810036*(1 - 0.0844425*x_3)**2))**(3/2) + 4.18594*log(0.0989599*(4.55406 - 9.80188*exp(-0.81018*(1 - 0.082213*x_3)**2))*(-0.542138*tanh(1.48*x_2 - 2.49992) + 0.0762073*Abs(3.354*x_3 - 4.5742) - 20.1063*acos(0.61316 - 0.01256*x_1) + 17.6602) + 4.416) - 0.208211*tan(15.8432*tan(0.00767999*x_1 - 0.60656) - 0.0594576*Abs(3.76392*x_2 - 4.27172) - 0.104815*atanh(0.208*x_3 - 1.20048) + 12.2742) - 1.15896*tanh(31.6443*tan(0.00603999*x_1 - 0.69408) + 28.5671 - 8.04278*exp(-0.810144*(1 - 0.0755488*x_3)**2)) + 6.72647*asin(0.00999719*sin(2.6356*x_2 - 4.45552) + 1.09995*acos(0.61656 - 0.01272*x_1) - 1.88068 + 0.665254*exp(-0.810036*(1 - 0.0799981*x_3)**2)) + 7.48527 + 9.35301e-7/(tan(0.00623999*x_1 - 0.67716) - 0.00144572*tan(0.3*x_3 - 1.82) - 0.00816524*atan(4.7*x_2 - 5.0) + 0.809357)**4`

### task=feynman_I_34_1 seed=20

- Task source: feynman_file
- Target formula: `omega_0/(1-v/c)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.504405e-02, r2=0.995579
- Variant formula overview:
  - icbr_full: symbolic_s=3.453827e+00, imitation_mse=1.683268e-02, target_mse=2.023239e-02, formula_export_success=True
  - icbr_no_replay: symbolic_s=2.183773e+00, imitation_mse=1.678028e-02, target_mse=2.133735e-02, formula_export_success=True
  - icbr_no_shared: symbolic_s=5.088845e+00, imitation_mse=1.683755e-02, target_mse=2.023596e-02, formula_export_success=True
  - icbr_refit_commit: symbolic_s=6.207170e+00, imitation_mse=2.269772e-02, target_mse=2.628650e-02, formula_export_success=True
- icbr_full formula (display, rounded):
  - `-5.96056*sqrt(1 - 0.226585*acos(0.0499997*x_1 - 0.5)) + 0.999138*sin(0.24719*Abs(2.1*x_3 - 2.5) + 2.96643*atanh(0.0499997*x_1 - 0.4) + 0.694098 + 0.347311*exp(-2.25*(1 - 0.9*x_2)**2)) - 7.78055*acos(0.0499997*(-0.205513*sin(1.25*x_2 + 4.15) + 1.58846 - 4.96936*exp(-(0.1*x_3 - 1.0)**2))*(-49.1659*sqrt(0.0220994*x_3 + 1) + 11.1322*acos(0.0499997*x_1 - 0.5) + 26.249 - 0.312352*exp(-3.4225*(0.351351*x_2 - 1)**2)) - 0.55) - 1.33619*atan(-1.42005*sin(0.4*x_3 - 1.25) + 25.1135*asin(0.0499997*x_1 - 0.5) + 9.54513) + 21.9654 + 2.91193*exp(-24.8212*(0.220891*tan(0.4*x_2 - 3.85) + 0.0195728*Abs(2.2*x_3 - 2.65) - atanh(0.0499997*x_1 - 0.4) - 0.465906)**2) + 0.977534*exp(-134.616*(-0.539142*acos(0.0499997*x_1 - 0.5) + 1 - 0.0367506*exp(-2.25*(1 - 0.9*x_2)**2))**2) + 1.0978/(-(-0.17801*cos(2.05*x_2 + 4.45) - 8.03937*atanh(0.0499997*x_1 - 0.4) - 2.74958)*(-0.109591*sin(1.8*x_2 + 3.3) + 5.7233*asin(0.0499997*x_1 - 0.5) + 0.133667*sign(4.5 - 3.9*x_3) + 2.88465) + 0.333333)**2`
- icbr_no_replay formula (display, rounded):
  - `1.52489*(1 - 0.377382*atanh(0.0499997*x_1 - 0.4))**(3/2) + 0.999138*sin(0.24719*Abs(2.1*x_3 - 2.5) + 2.94548*asin(0.0499997*x_1 - 0.5) + 0.989783 + 0.347311*exp(-2.25*(1 - 0.9*x_2)**2)) - 7.78055*acos(0.0499997*(-0.205298*cos(1.25*x_2 - 3.7) + 1.58926 - 4.96936*exp(-(0.1*x_3 - 1.0)**2))*(-0.218568*tanh(0.8*x_2 - 1.45) - 11.1322*asin(0.0499997*x_1 - 0.5) - 3.41115 - 6.23465*exp(-(0.1*x_3 - 1.0)**2)) - 0.55) + 0.952615*atan(2.9*(0.181828*sin(2.0*x_2 + 2.95) + 7.98258*acos(0.0499997*x_1 - 0.5) - 16.0878)*(-0.109591*sin(1.8*x_2 + 3.3) + 5.7233*asin(0.0499997*x_1 - 0.5) + 0.133667*sign(4.5 - 3.9*x_3) + 2.88465) + 1.6) - 1.33619*atan(-0.220894*Abs(2.45*x_3 - 3.0) + 25.1135*asin(0.0499997*x_1 - 0.5) + 10.5763) + 17.2099 + 2.91193*exp(-112.113*(0.103935*tan(0.4*x_2 - 3.85) + 0.00920951*Abs(2.2*x_3 - 2.65) + 0.467202*acos(0.0499997*x_1 - 0.5) - 1)**2) + 0.977534*exp(-39.1294*(asin(0.0499997*x_1 - 0.5) + 0.284002 - 0.068165*exp(-2.25*(1 - 0.9*x_2)**2))**2)`
- icbr_no_shared formula (display, rounded):
  - `-5.43048*sqrt(1 - 0.242768*acos(0.0499997*x_1 - 0.5)) + 0.999138*sin(0.24719*Abs(2.1*x_3 - 2.5) + 2.96643*atanh(0.0499997*x_1 - 0.4) + 0.694098 + 0.347311*exp(-2.25*(1 - 0.9*x_2)**2)) - 7.78055*acos(0.0499997*(-0.205513*sin(1.25*x_2 + 4.15) + 1.58846 - 4.96936*exp(-(0.1*x_3 - 1.0)**2))*(-49.4291*sqrt(0.021978*x_3 + 1) + 11.1322*acos(0.0499997*x_1 - 0.5) + 26.5121 - 0.312352*exp(-3.4225*(0.351351*x_2 - 1)**2)) - 0.55) - 1.33619*atan(-1.42005*sin(0.4*x_3 - 1.25) + 25.1135*asin(0.0499997*x_1 - 0.5) + 9.54513) + 21.4534 + 2.91193*exp(-24.8212*(0.220891*tan(0.4*x_2 - 3.85) + 0.0195728*Abs(2.2*x_3 - 2.65) - atanh(0.0499997*x_1 - 0.4) - 0.465906)**2) + 0.977534*exp(-134.616*(-0.539142*acos(0.0499997*x_1 - 0.5) + 1 - 0.0367506*exp(-2.25*(1 - 0.9*x_2)**2))**2) + 1.0978/(-(-0.17801*cos(2.05*x_2 + 4.45) - 8.03937*atanh(0.0499997*x_1 - 0.4) - 2.74958)*(-0.109591*sin(1.8*x_2 + 3.3) + 5.7233*asin(0.0499997*x_1 - 0.5) + 0.133667*sign(4.5 - 3.9*x_3) + 2.88465) + 0.333333)**2`
- icbr_refit_commit formula (display, rounded):
  - `-4.98677*sqrt(acos(0.61276 - 0.01284*x_1) - 0.285465) + 0.569771*cos(56.8055*atanh(0.00599999*x_1 - 0.60066) + 37.0573 - 0.641446*exp(-2.56*(1 - 0.88825*x_2)**2)) - 0.801975*cos(0.13939*Abs(4.2258*x_3 - 4.7278) + 1.95602*atanh(0.0859999*x_1 - 0.60006) + 1.90377 + 0.412988*exp(-1.95978*(1 - 0.914338*x_2)**2)) + 93.3851*asin(0.002*(-0.208884*sin(1.22884*x_2 - 2.10332) + 2.8346 - 6.85613*exp(-0.810504*(1 - 0.079975*x_3)**2))*(-7.20496*asin(0.0777599*x_1 - 0.602) - 0.469834 - 8.37982*exp(-0.81*(1 - 0.0822221*x_3)**2) - 0.344349*exp(-3.18937*(1 - 0.332408*x_2)**2)) - 0.9) - 3.89696*atan(2.56584*sin(0.40248*x_3 + 1.88564) + 156.135*asin(0.01252*x_1 - 0.622) + 100.104) + 122.254 - 8.3472*exp(-152.98*(0.0329682*tan(0.36056*x_2 - 0.6476) + 0.0019379*Abs(2.95048*x_3 - 3.25456) - atanh(0.00416*x_1 - 0.6496) - 0.723611)**2) + 1.05269/(-(0.187202*sin(1.93868*x_2 - 3.25272) - 46.4079*atanh(0.00599999*x_1 - 0.60048) - 31.6101)*(-0.110941*sin(1.7778*x_2 + 3.32692) + 43.3956*atanh(0.00416*x_1 - 0.64424) + 0.111702*sign(4.69946 - 4.09*x_3) + 33.1212) + 0.312707)**2`

### task=feynman_II_6_15a seed=1

- Task source: feynman_file
- Target formula: `p_d/(4*pi*epsilon)*3*z/r**5*sqrt(x**2+y**2)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=6.369051e-03, r2=0.945345
- Variant formula overview:
  - icbr_full: symbolic_s=7.987203e-01, imitation_mse=3.117603e-03, target_mse=4.205469e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=6.950753e-01, imitation_mse=3.135232e-03, target_mse=4.178022e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.082232e+00, imitation_mse=3.117604e-03, target_mse=4.205470e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.522708e+00, imitation_mse=3.896276e-03, target_mse=3.810779e-03, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0.0340729 + 4.62301*exp(-11.5759*(cos(0.6*x_3 + 3.35) - 0.0332316*tan(1.0*x_2 + 0.95) - 0.0162399*tan(0.95*x_4 + 1.1) + 0.0994979*asin(0.6*x_1 - 1.25) - 0.0616283*asin(0.65*x_6 - 1.6) - 0.0281889*atanh(0.65*x_5 - 1.35) + 0.986949)**2)`
- icbr_no_replay formula (display, rounded):
  - `0.0340729 + 4.62301*exp(-11.5759*(cos(0.6*x_3 + 3.35) - 0.0332316*tan(1.0*x_2 + 0.95) - 0.0162399*tan(0.95*x_4 + 1.1) - 0.050999*tan(0.75*x_6 + 4.6) + 0.0994979*asin(0.6*x_1 - 1.25) - 0.0185453*asin(0.95*x_5 - 1.95) + 0.996464)**2)`
- icbr_no_shared formula (display, rounded):
  - `0.0340729 + 4.62301*exp(-15.1297*(0.874707*cos(0.6*x_3 + 3.35) - 0.0290679*tan(1.0*x_2 + 0.95) - 0.0142052*tan(0.95*x_4 + 1.1) - 0.0870315*acos(0.6*x_1 - 1.25) - 0.0539067*asin(0.65*x_6 - 1.6) - 0.024657*atanh(0.65*x_5 - 1.35) + 1)**2)`
- icbr_refit_commit formula (display, rounded):
  - `0.0178992 + 207.966*exp(-11.7118*(0.541164*cos(0.53976*x_3 + 3.42972) - 0.0224283*tan(0.72208*x_2 - 1.81996) - 0.0101754*tan(0.78076*x_4 - 1.77124) + 0.047711*asin(0.60716*x_1 - 1.28188) - 0.0338578*asin(0.568*x_6 - 1.5) - 0.0136751*atanh(0.65164*x_5 - 1.35292) + 1)**2)`

### task=feynman_II_6_15a seed=2

- Task source: feynman_file
- Target formula: `p_d/(4*pi*epsilon)*3*z/r**5*sqrt(x**2+y**2)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.113541e-02, r2=0.912134
- Variant formula overview:
  - icbr_full: symbolic_s=1.200092e+00, imitation_mse=4.612273e-03, target_mse=1.348995e-02, formula_export_success=True
  - icbr_no_replay: symbolic_s=9.448492e-01, imitation_mse=4.162004e-03, target_mse=8.953187e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.775795e+00, imitation_mse=4.612273e-03, target_mse=1.348995e-02, formula_export_success=True
  - icbr_refit_commit: symbolic_s=2.068511e+00, imitation_mse=5.248163e-03, target_mse=1.127344e-02, formula_export_success=True
- icbr_full formula (display, rounded):
  - `-0.0805057 + 2.28102*exp(-2.7225*(0.333333*(0.290298*cos(1.05*x_5 + 2.35) + 0.479899*tanh(0.65*x_2 - 1.5) + 0.198197*Abs(3.35*x_6 - 4.25) + 1.08597 + 0.325224/sqrt(x_3 - 0.880952))*(-0.127574*tan(0.95*x_1 + 1.05) - 0.238492*tan(1.15*x_3 + 3.8) + 0.0415616*Abs(3.2*x_4 - 4.1) + 0.0243158*Abs(3.45*x_5 - 4.4) + 0.813771*atan(0.2*x_2 - 0.55) + 0.134061*atanh(0.6*x_6 - 1.5) - 0.14747) - 1)**2)`
- icbr_no_replay formula (display, rounded):
  - `1.92528*sin(0.55*(-0.346926*sin(0.9*x_2 + 1.1) + 0.290298*cos(1.05*x_5 + 2.35) - 0.099037*tan(1.2*x_3 + 3.65) + 0.198197*Abs(3.35*x_6 - 4.25) + 1.37671)*(-0.648067*sin(0.25*x_2 + 2.45) - 0.127574*tan(0.95*x_1 + 1.05) - 0.238492*tan(1.15*x_3 + 3.8) + 0.080696*tan(0.95*x_6 + 1.05) + 0.0415616*Abs(3.2*x_4 - 4.1) + 0.0243158*Abs(3.45*x_5 - 4.4) - 0.171493) + 5.0) + 1.90245`
- icbr_no_shared formula (display, rounded):
  - `-0.0805057 + 2.28102*exp(-2.7225*(0.333333*(0.290298*cos(1.05*x_5 + 2.35) + 0.479899*tanh(0.65*x_2 - 1.5) + 0.198197*Abs(3.35*x_6 - 4.25) + 1.08597 + 0.325224/sqrt(x_3 - 0.880952))*(-0.127574*tan(0.95*x_1 + 1.05) - 0.238492*tan(1.15*x_3 + 3.8) + 0.0415616*Abs(3.2*x_4 - 4.1) + 0.0243158*Abs(3.45*x_5 - 4.4) + 0.813771*atan(0.2*x_2 - 0.55) + 0.134061*atanh(0.6*x_6 - 1.5) - 0.14747) - 1)**2)`
- icbr_refit_commit formula (display, rounded):
  - `-0.0803938 + 2.27822*exp(-2.72224*(-0.33364*(-0.2924*cos(1.03384*x_5 - 0.73916) + 0.480573*tanh(0.64884*x_2 - 1.49716) + 0.182879*Abs(3.53344*x_6 - 4.34) + 1.07598 + 0.32518/sqrt(x_3 - 0.880989))*(0.186433*sqrt(x_6 - 0.975129) - 0.173661*tan(0.72236*x_1 + 1.38504) - 0.328366*tan(0.68032*x_3 + 4.32692) + 0.0371241*Abs(3.49976*x_4 - 4.39984) + 0.0232707*Abs(3.52728*x_5 - 4.4192) + 0.815376*atan(0.19954*x_2 - 0.548) - 0.615389) + 1)**2)`

### task=feynman_II_6_15a seed=3

- Task source: feynman_file
- Target formula: `p_d/(4*pi*epsilon)*3*z/r**5*sqrt(x**2+y**2)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=9.527929e-03, r2=0.915886
- Variant formula overview:
  - icbr_full: symbolic_s=8.059540e-01, imitation_mse=2.332101e-03, target_mse=8.595952e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=6.961698e-01, imitation_mse=2.232841e-03, target_mse=8.623843e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.320752e+00, imitation_mse=2.332102e-03, target_mse=8.595952e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.368307e+00, imitation_mse=7.045344e-03, target_mse=1.377478e-02, formula_export_success=True
- icbr_full formula (display, rounded):
  - `1.95508*tanh(0.170153*sin(1.75*x_4 - 3.9) - 0.199993*tan(1.0*x_1 + 0.95) - 0.567532*tan(1.1*x_3 + 3.9) + 0.07325*Abs(3.15*x_5 - 4.2) + 0.102544*Abs(3.95*x_6 - 4.85) + 0.69276*asin(0.55*x_2 - 1.1) - 2.65612) + 1.94394`
- icbr_no_replay formula (display, rounded):
  - `1.95508*tanh(-0.199993*tan(1.0*x_1 + 0.95) - 0.567532*tan(1.1*x_3 + 3.9) + 0.0835389*Abs(2.9*x_4 - 3.95) + 0.07325*Abs(3.15*x_5 - 4.2) + 0.102544*Abs(3.95*x_6 - 4.85) + 0.69276*asin(0.55*x_2 - 1.1) - 2.86425) + 1.94394`
- icbr_no_shared formula (display, rounded):
  - `1.95508*tanh(0.170153*sin(1.75*x_4 - 3.9) - 0.199993*tan(1.0*x_1 + 0.95) - 0.567532*tan(1.1*x_3 + 3.9) + 0.0809606*Abs(2.85*x_5 - 3.8) + 0.102544*Abs(3.95*x_6 - 4.85) + 0.69276*asin(0.55*x_2 - 1.1) - 2.65612) + 1.94394`
- icbr_refit_commit formula (display, rounded):
  - `1.98456*tanh(-0.280893*tan(0.70368*x_1 + 4.50516) - 0.943646*tan(0.70964*x_3 + 4.48452) + 0.0723718*Abs(3.21144*x_4 - 4.41296) + 0.0600926*Abs(3.6646*x_5 - 4.8912) + 0.113887*Abs(3.34316*x_6 - 3.9498) + 0.668083*acos(1.09976 - 0.55048*x_2) - 4.20894) + 1.96788`

### task=feynman_II_6_15a seed=4

- Task source: feynman_file
- Target formula: `p_d/(4*pi*epsilon)*3*z/r**5*sqrt(x**2+y**2)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=2.637712e-02, r2=0.782050
- Variant formula overview:
  - icbr_full: symbolic_s=7.989580e-01, imitation_mse=1.591181e-03, target_mse=2.509389e-02, formula_export_success=True
  - icbr_no_replay: symbolic_s=6.827880e-01, imitation_mse=1.591060e-03, target_mse=2.512413e-02, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.173301e+00, imitation_mse=1.591181e-03, target_mse=2.509389e-02, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.448056e+00, imitation_mse=1.762732e-03, target_mse=2.435872e-02, formula_export_success=True
- icbr_full formula (display, rounded):
  - `-0.123276 + 4.35237*exp(-12.3786*(-0.00629744*tan(1.0*x_4 + 3.95) - 0.0164314*tan(1.1*x_6 + 3.9) + 0.0875937*asin(0.5*x_1 - 1.05) + atan(0.3*x_3 - 0.75) - 0.0335724*atanh(0.75*x_2 - 1.7) + 0.721069 + 0.0208276/sqrt(x_5 - 0.704918))**2)`
- icbr_no_replay formula (display, rounded):
  - `-0.123276 + 4.35237*exp(-5.45212*(cos(0.45*x_3 + 3.65) - 0.00948893*tan(1.0*x_4 + 3.95) - 0.0101945*tan(0.85*x_5 + 4.15) - 0.0247587*tan(1.1*x_6 + 3.9) + 0.131985*acos(1.05 - 0.5*x_1) - 0.0505866*atanh(0.75*x_2 - 1.7) + 0.840738)**2)`
- icbr_no_shared formula (display, rounded):
  - `-0.123276 + 4.35237*exp(-12.3786*(-0.00629744*tan(1.0*x_4 + 3.95) - 0.0164314*tan(1.1*x_6 + 3.9) + 0.0875937*asin(0.5*x_1 - 1.05) + atan(0.3*x_3 - 0.75) - 0.0335724*atanh(0.75*x_2 - 1.7) + 0.721069 + 0.0208276/sqrt(x_5 - 0.704918))**2)`
- icbr_refit_commit formula (display, rounded):
  - `-0.123456 + 7.40595*exp(-12.4354*(0.00488695*tan(0.52996*x_4 - 1.92128) + 0.0190536*tan(0.6*x_6 - 4.99999) - 0.083783*asin(0.464*x_1 - 0.9987) - atan(0.266*x_3 - 0.69862) + 0.0394727*atanh(0.53052*x_2 - 1.44236) - 0.742496 - 0.0184185/sqrt(x_5 - 0.705461))**2)`

### task=feynman_II_6_15a seed=5

- Task source: feynman_file
- Target formula: `p_d/(4*pi*epsilon)*3*z/r**5*sqrt(x**2+y**2)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=4.778140e-03, r2=0.965069
- Variant formula overview:
  - icbr_full: symbolic_s=1.430657e+00, imitation_mse=2.402755e-03, target_mse=2.948069e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=1.022564e+00, imitation_mse=2.331429e-03, target_mse=3.266896e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.902047e+00, imitation_mse=2.402328e-03, target_mse=2.947903e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=2.593677e+00, imitation_mse=3.641358e-03, target_mse=6.246276e-03, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0.0785786*(0.947221*(0.0220994*x_4 + 1)**4 - 0.066354*tan(1.15*x_1 + 3.8) + 0.0879125*Abs(2.7*x_2 - 3.3) - atanh(0.7*x_3 - 1.5) + 0.136769*atanh(0.55*x_5 - 1.2) + 0.277773*atanh(0.65*x_6 - 1.5) - 0.727225)**5 - 0.00247774 + 0.0212671/((1.08359 - 1.31022*sin(0.4*x_3 + 2.15))*(-0.142771*Abs(3.25*x_1 - 4.2) - 0.761031 + 0.179071*exp(-8.7025*(1 - 0.59322*x_2)**2)) - 0.181818)**4`
- icbr_no_replay formula (display, rounded):
  - `0.31654*(0.918686*(0.0220994*x_4 + 1)**4 - 0.0643551*tan(1.15*x_1 + 3.8) + 0.146836*tan(0.5*x_5 + 2.0) + 0.200693*tan(0.85*x_6 + 1.3) + 0.0852641*Abs(2.7*x_2 - 3.3) - 0.969875*atanh(0.7*x_3 - 1.5) - 1)**4 - 0.00931611 + 0.0184454/(-(1.16375*cos(0.45*x_3 + 3.65) + 1.02261)*(-0.142771*Abs(3.25*x_1 - 4.2) - 0.761031 + 0.179071*exp(-8.7025*(1 - 0.59322*x_2)**2)) + 0.06)**3`
- icbr_no_shared formula (display, rounded):
  - `0.0785786*(0.964931*(0.0217391*x_4 + 1)**4 - 0.066354*tan(1.15*x_1 + 3.8) + 0.0879125*Abs(2.7*x_2 - 3.3) - atanh(0.7*x_3 - 1.5) + 0.136769*atanh(0.55*x_5 - 1.2) + 0.277773*atanh(0.65*x_6 - 1.5) - 0.7451)**5 - 0.00247774 + 0.0212671/((1.08359 - 1.31022*sin(0.4*x_3 + 2.15))*(-0.142771*Abs(3.25*x_1 - 4.2) - 0.761031 + 0.179071*exp(-8.7025*(1 - 0.59322*x_2)**2)) - 0.181818)**4`
- icbr_refit_commit formula (display, rounded):
  - `0.708988*(-0.514205*(-0.0340432*x_4 - 1)**3 - 0.0546591*tan(0.71316*x_1 + 4.28048) + 0.0387125*Abs(3.77296*x_2 - 4.48568) - atanh(0.468*x_3 - 1.09996) + 0.0962997*atanh(0.49676*x_5 - 1.10548) + 0.173194*atanh(0.668*x_6 - 1.49992) - 0.489726)**5 - 0.00647117 + 0.0212714/(-(1.34101*sin(0.39176*x_3 - 0.99064) + 1.10943)*(-1.72835 + 0.18658*exp(-7.29*(1 - 0.578518*x_2)**2) + 0.896208*exp(-0.655193*(1 - 0.856147*x_1)**2)) + 0.181842)**4`

### task=feynman_II_6_15a seed=6

- Task source: feynman_file
- Target formula: `p_d/(4*pi*epsilon)*3*z/r**5*sqrt(x**2+y**2)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.341172e-02, r2=0.863253
- Variant formula overview:
  - icbr_full: symbolic_s=8.020413e-01, imitation_mse=2.566695e-03, target_mse=1.302010e-02, formula_export_success=True
  - icbr_no_replay: symbolic_s=6.881535e-01, imitation_mse=2.566695e-03, target_mse=1.302010e-02, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.190698e+00, imitation_mse=2.566695e-03, target_mse=1.302010e-02, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.290012e+00, imitation_mse=3.805253e-03, target_mse=1.156834e-02, formula_export_success=True
- icbr_full formula (display, rounded):
  - `1.03033*atan(-0.155452*tan(1.15*x_1 + 3.75) - 0.751247*tan(1.15*x_3 + 3.8) + 0.976536*tanh(0.7*x_6 - 1.6) + 0.176205*Abs(3.65*x_2 - 4.575) + 0.155234*Abs(2.7*x_4 - 3.7) + 0.157233*Abs(2.75*x_5 - 3.85) - 3.70178) + 1.28929`
- icbr_no_replay formula (display, rounded):
  - `1.03033*atan(-0.155452*tan(1.15*x_1 + 3.75) - 0.751247*tan(1.15*x_3 + 3.8) + 0.976536*tanh(0.7*x_6 - 1.6) + 0.176205*Abs(3.65*x_2 - 4.575) + 0.155234*Abs(2.7*x_4 - 3.7) + 0.157233*Abs(2.75*x_5 - 3.85) - 3.70178) + 1.28929`
- icbr_no_shared formula (display, rounded):
  - `1.03033*atan(-0.155452*tan(1.15*x_1 + 3.75) - 0.751247*tan(1.15*x_3 + 3.8) + 0.976536*tanh(0.7*x_6 - 1.6) + 0.176205*Abs(3.65*x_2 - 4.575) + 0.155234*Abs(2.7*x_4 - 3.7) + 0.157233*Abs(2.75*x_5 - 3.85) - 3.70178) + 1.28929`
- icbr_refit_commit formula (display, rounded):
  - `0.970277*atan(-0.167612*tan(1.082*x_1 + 0.7) - 1.04623*tan(0.679*x_3 + 4.33128) + 1.0077*tanh(0.67968*x_6 - 1.57908) + 0.203489*Abs(3.0992*x_2 - 3.80036) + 0.209451*Abs(1.969*x_4 - 2.69544) + 0.189064*Abs(2.26424*x_5 - 3.19032) - 4.23571) + 1.20251`

### task=feynman_II_6_15a seed=7

- Task source: feynman_file
- Target formula: `p_d/(4*pi*epsilon)*3*z/r**5*sqrt(x**2+y**2)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=4.955336e-03, r2=0.954187
- Variant formula overview:
  - icbr_full: symbolic_s=8.519490e-01, imitation_mse=2.451396e-03, target_mse=4.124199e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=6.819357e-01, imitation_mse=2.453999e-03, target_mse=4.139076e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.107951e+00, imitation_mse=2.451496e-03, target_mse=4.124141e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.382025e+00, imitation_mse=5.394679e-03, target_mse=6.691290e-03, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0.01365 + 3.52028*exp(-17.3911*(0.365735*(-0.071066*x_2 - 1)**2 - 0.162238*tan(0.95*x_3 + 1.1) + 0.113724*tanh(0.6*x_6 - 1.35) + 0.0105323*Abs(3.25*x_4 - 4.25) - 0.055214*asin(0.75*x_1 - 1.75) - 1 - 0.0871816*exp(-0.3025*(x_5 - 1)**2))**2)`
- icbr_no_replay formula (display, rounded):
  - `0.01365 + 3.52028*exp(-22.8995*(0.52355*(0.0217391*x_2 + 1)**4 + 0.0743862*cos(0.8*x_6 + 2.9) - 0.141385*tan(0.95*x_3 + 1.1) + 0.00917858*Abs(3.25*x_4 - 4.25) - 0.0481171*acos(1.75 - 0.75*x_1) - 1 - 0.0759757*exp(-0.3025*(x_5 - 1)**2))**2)`
- icbr_no_shared formula (display, rounded):
  - `0.01365 + 3.52028*exp(-17.4648*(0.367045*(-0.0707071*x_2 - 1)**2 - 0.161895*tan(0.95*x_3 + 1.1) + 0.113484*tanh(0.6*x_6 - 1.35) + 0.0105101*Abs(3.25*x_4 - 4.25) - 0.0550974*asin(0.75*x_1 - 1.75) - 1 - 0.0869973*exp(-0.3025*(1 - x_5)**2))**2)`
- icbr_refit_commit formula (display, rounded):
  - `0.001476 + 5.60781*exp(-16.5176*(0.303353*(-0.0718277*x_2 - 1)**2 + 0.0290272*cos(1.19852*x_5 - 4.30184) - 0.186423*tan(0.74344*x_3 + 1.43796) + 0.0993503*tanh(0.574*x_6 - 1.29988) + 0.00729792*Abs(3.84544*x_4 - 4.95328) - 0.0455921*asin(0.76456*x_1 - 1.76388) - 1)**2)`

### task=feynman_II_6_15a seed=8

- Task source: feynman_file
- Target formula: `p_d/(4*pi*epsilon)*3*z/r**5*sqrt(x**2+y**2)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.257570e-02, r2=0.924930
- Variant formula overview:
  - icbr_full: symbolic_s=1.133054e+00, imitation_mse=2.776601e-03, target_mse=1.352338e-02, formula_export_success=True
  - icbr_no_replay: symbolic_s=8.403607e-01, imitation_mse=2.789596e-03, target_mse=1.361106e-02, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.572646e+00, imitation_mse=2.776606e-03, target_mse=1.352341e-02, formula_export_success=True
  - icbr_refit_commit: symbolic_s=2.117269e+00, imitation_mse=3.806030e-03, target_mse=1.376244e-02, formula_export_success=True
- icbr_full formula (display, rounded):
  - `-0.0223349 + 3.93968*exp(-18.3943*(-0.0312409*sin(0.6*x_5 + 4.9) + 0.92854*acos(0.55 - 0.3*x_3) - 0.0466223*acos(1.75 - 0.8*x_2) + 0.057968*acos(0.6*x_6 - 1.5) + 0.0468054*asin(0.9*x_1 - 1.9) - 0.0258658*atanh(0.6*x_4 - 1.3) - 1)**2) + 0.0713069*exp(-2.33691*(0.464049*Abs(3.45*x_3 - 5.0) - 1)**2)`
- icbr_no_replay formula (display, rounded):
  - `-0.0223349 + 3.93968*exp(-15.8593*(-0.0336452*sin(0.6*x_5 + 4.9) - 0.0569473*tan(0.65*x_6 + 4.825) - 0.0502104*acos(1.75 - 0.8*x_2) + 0.0504075*asin(0.9*x_1 - 1.9) + asin(0.3*x_3 - 0.55) - 0.0278565*atanh(0.6*x_4 - 1.3) + 0.601938)**2) + 0.0713069*exp(-2.33691*(0.464049*Abs(3.45*x_3 - 5.0) - 1)**2)`
- icbr_no_shared formula (display, rounded):
  - `-0.0223349 + 3.93968*exp(-74.1782*(-0.015557*sin(0.6*x_5 + 4.9) - 0.0232165*acos(1.75 - 0.8*x_2) - 0.462386*acos(0.3*x_3 - 0.55) + 0.0233077*asin(0.9*x_1 - 1.9) - 0.0288663*asin(0.6*x_6 - 1.5) - 0.0128804*atanh(0.6*x_4 - 1.3) + 1)**2) + 0.0713069*exp(-2.33691*(0.464049*Abs(3.45*x_3 - 5.0) - 1)**2)`
- icbr_refit_commit formula (display, rounded):
  - `-0.054809 + 8.73157*exp(-197.966*(-0.0078823*sin(0.58632*x_5 + 4.91344) - 0.014297*acos(1.49872 - 0.59912*x_6) + 0.0107686*acos(0.84492*x_2 - 1.81652) - 0.5869*acos(0.11644*x_3 - 0.0729199) + 0.0124709*asin(0.84504*x_1 - 1.81748) - 0.00597914*asin(0.65*x_4 - 1.49952) + 1)**2) + 0.0927379*exp(-0.810363*(0.51482*Abs(3.26728*x_3 - 4.85568) - 1)**2)`

### task=feynman_II_6_15a seed=9

- Task source: feynman_file
- Target formula: `p_d/(4*pi*epsilon)*3*z/r**5*sqrt(x**2+y**2)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.993361e-03, r2=0.985958
- Variant formula overview:
  - icbr_full: symbolic_s=8.122683e-01, imitation_mse=1.530436e-03, target_mse=3.248615e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=6.648842e-01, imitation_mse=1.538817e-03, target_mse=3.234914e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.148495e+00, imitation_mse=1.530436e-03, target_mse=3.248615e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.553154e+00, imitation_mse=2.241162e-03, target_mse=4.032212e-03, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0.0278395 + 3.33566*exp(-38.5077*(0.0201858*cos(0.95*x_5 + 2.55) - 0.0390504*tan(0.8*x_1 + 4.55) + 0.00617444*Abs(3.3*x_4 - 3.9) + 0.0759911*acos(1.05 - 0.5*x_6) + 0.284821*acos(0.7*x_3 - 1.5) + 0.0538392*atanh(0.65*x_2 - 1.4) - 1)**2)`
- icbr_no_replay formula (display, rounded):
  - `0.0278395 + 3.33566*exp(-7.33077*(0.0440689*sin(1.0*x_5 + 4.05) + 0.0141513*Abs(3.3*x_4 - 3.9) - 0.652787*asin(0.7*x_3 - 1.5) + 0.174165*asin(0.5*x_6 - 1.05) - 0.114139*atanh(0.65*x_1 - 1.45) + 0.123395*atanh(0.65*x_2 - 1.4) - 1)**2)`
- icbr_no_shared formula (display, rounded):
  - `0.0278395 + 3.33566*exp(-38.5077*(0.0201858*cos(0.95*x_5 + 2.55) - 0.0390504*tan(0.8*x_1 + 4.55) + 0.00740932*Abs(2.75*x_4 - 3.25) + 0.0759911*acos(1.05 - 0.5*x_6) + 0.284821*acos(0.7*x_3 - 1.5) + 0.0538392*atanh(0.65*x_2 - 1.4) - 1)**2)`
- icbr_refit_commit formula (display, rounded):
  - `0.00837295 + 6.57035*exp(-24.6543*(-0.0185185*cos(0.93328*x_5 - 0.54812) - 0.0434714*tan(0.67848*x_1 - 4.6598) + 0.00437531*Abs(4.14932*x_4 - 4.74768) + 0.0745409*acos(0.99764 - 0.4632*x_6) + 0.248065*acos(0.72796*x_3 - 1.51992) + 0.0702804*atanh(0.468*x_2 - 1.09996) - 1)**2)`

### task=feynman_II_6_15a seed=10

- Task source: feynman_file
- Target formula: `p_d/(4*pi*epsilon)*3*z/r**5*sqrt(x**2+y**2)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.486348e-02, r2=0.879280
- Variant formula overview:
  - icbr_full: symbolic_s=8.066814e-01, imitation_mse=2.609615e-03, target_mse=1.560747e-02, formula_export_success=True
  - icbr_no_replay: symbolic_s=6.720922e-01, imitation_mse=2.593428e-03, target_mse=1.564661e-02, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.100314e+00, imitation_mse=2.609616e-03, target_mse=1.560748e-02, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.538582e+00, imitation_mse=2.750423e-03, target_mse=1.604349e-02, formula_export_success=True
- icbr_full formula (display, rounded):
  - `-0.0468158 + 4.34809*exp(-4.38509*(0.0472664*sin(0.5*x_5 - 1.05) + 0.0459155*tan(0.95*x_2 + 1.05) + 0.00848315*tan(1.0*x_4 - 2.45) - 0.661058*asin(0.6*x_3 - 1.25) - 0.132737*atanh(0.6*x_1 - 1.3) + 0.0820605*atanh(0.6*x_6 - 1.5) - 1)**2)`
- icbr_no_replay formula (display, rounded):
  - `-0.0468158 + 4.34809*exp(-1.91628*(0.0694576*tan(0.95*x_2 + 1.05) + 0.0128327*tan(1.0*x_4 - 2.45) + 0.0713494*tan(1.0*x_6 + 1.0) + 0.00833683*Abs(4.25*x_5 - 4.725) - acos(1.25 - 0.6*x_3) - 0.200795*atanh(0.6*x_1 - 1.3) - 0.00727943)**2)`
- icbr_no_shared formula (display, rounded):
  - `-0.0468158 + 4.34809*exp(-1.91628*(0.0715011*sin(0.5*x_5 - 1.05) + 0.0694576*tan(0.95*x_2 + 1.05) + 0.0128327*tan(1.0*x_4 - 2.45) - acos(1.25 - 0.6*x_3) - 0.200795*atanh(0.6*x_1 - 1.3) + 0.124135*atanh(0.6*x_6 - 1.5) + 0.0580706)**2)`
- icbr_refit_commit formula (display, rounded):
  - `-0.0486205 + 4.80047*exp(-2.12024*(-0.0613312*sin(0.53372*x_5 + 2.02944) + 0.0870597*tan(0.7336*x_2 - 1.75196) + 0.00986525*tan(0.6*x_4 + 4.214) - acos(1.1678 - 0.55084*x_3) - 0.2384*atanh(0.468*x_1 - 1.1) + 0.112142*atanh(0.64708*x_6 - 1.51228) + 0.0923116)**2)`

### task=feynman_II_6_15a seed=11

- Task source: feynman_file
- Target formula: `p_d/(4*pi*epsilon)*3*z/r**5*sqrt(x**2+y**2)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=3.687255e-03, r2=0.973415
- Variant formula overview:
  - icbr_full: symbolic_s=7.921955e-01, imitation_mse=2.613873e-03, target_mse=3.701681e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=6.649684e-01, imitation_mse=2.838522e-03, target_mse=3.912618e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.083893e+00, imitation_mse=2.613873e-03, target_mse=3.701681e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.442879e+00, imitation_mse=3.423623e-03, target_mse=3.972668e-03, formula_export_success=True
- icbr_full formula (display, rounded):
  - `16.2152*tanh(-4.79714*cos(0.75*x_3 + 3.05) + 0.202833*cos(0.55*x_5 + 3.45) + 0.156514*tan(1.0*x_2 + 0.95) + 0.170536*tan(1.0*x_6 + 1.0) + 0.147074*asin(0.65*x_4 - 1.45) - 0.455291*atanh(0.55*x_1 - 1.2) - 5.24485) + 16.2466`
- icbr_no_replay formula (display, rounded):
  - `16.2152*tanh(-5.12072*sin(0.7*x_3 + 4.7) + 0.202833*cos(0.55*x_5 + 3.45) + 0.156514*tan(1.0*x_2 + 0.95) + 0.170536*tan(1.0*x_6 + 1.0) - 0.363486*asin(0.7*x_1 - 1.5) + 0.171*atanh(0.55*x_4 - 1.2) - 5.39216) + 16.2466`
- icbr_no_shared formula (display, rounded):
  - `16.2152*tanh(-4.79714*cos(0.75*x_3 + 3.05) + 0.202833*cos(0.55*x_5 + 3.45) + 0.156514*tan(1.0*x_2 + 0.95) + 0.170536*tan(1.0*x_6 + 1.0) + 0.147074*asin(0.65*x_4 - 1.45) - 0.455291*atanh(0.55*x_1 - 1.2) - 5.24485) + 16.2466`
- icbr_refit_commit formula (display, rounded):
  - `145.872*tanh(-5.29745*cos(0.658*x_3 - 3.08756) + 0.178692*cos(0.6102*x_5 - 2.92632) + 0.235006*tan(0.65168*x_2 - 4.85388) + 0.246992*tan(0.72984*x_6 - 4.85376) + 0.143022*asin(0.6514*x_4 - 1.45248) - 0.445218*atanh(0.5484*x_1 - 1.19752) - 6.4543) + 145.904`

### task=feynman_II_6_15a seed=12

- Task source: feynman_file
- Target formula: `p_d/(4*pi*epsilon)*3*z/r**5*sqrt(x**2+y**2)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=7.151763e-03, r2=0.953419
- Variant formula overview:
  - icbr_full: symbolic_s=9.641548e-01, imitation_mse=3.247613e-03, target_mse=9.306940e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=7.442068e-01, imitation_mse=3.077301e-03, target_mse=9.266580e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.299603e+00, imitation_mse=3.247611e-03, target_mse=9.306937e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.653563e+00, imitation_mse=nan, target_mse=nan, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0.0331497 + 0.412494/(-(0.542017*tan(0.35*x_1 - 0.75) + 0.432443*Abs(2.55*x_3 - 3.1) + 1.27979)*(1.67796*sin(0.6*x_3 + 1.8) + 0.0434545*tan(1.0*x_2 + 0.95) + 0.0326331*tanh(0.85*x_4 - 1.9) - 0.0249618*acos(0.85*x_5 - 1.85) + 0.0957196*asin(0.5*x_6 - 1.5) - 1.46049) + 0.126761)**4`
- icbr_no_replay formula (display, rounded):
  - `0.0374401 + 0.92856/(-(0.432443*Abs(2.55*x_3 - 3.1) + 0.423685*asin(0.45*x_1 - 0.95) + 1.27349)*(0.0273452*sin(1.0*x_4 + 4.0) - 1.82578*cos(0.55*x_3 + 3.45) + 0.0434545*tan(1.0*x_2 + 0.95) + 0.0416388*tan(1.05*x_6 + 0.9) + 0.0249618*asin(0.85*x_5 - 1.85) - 1.60079) + 0.310345)**5`
- icbr_no_shared formula (display, rounded):
  - `0.0331497 + 0.412494/(-(0.542017*tan(0.35*x_1 - 0.75) + 0.432443*Abs(2.55*x_3 - 3.1) + 1.27979)*(1.67796*sin(0.6*x_3 + 1.8) + 0.0434545*tan(1.0*x_2 + 0.95) + 0.0326331*tanh(0.85*x_4 - 1.9) - 0.0249618*acos(0.85*x_5 - 1.85) - 0.0957196*acos(0.5*x_6 - 1.5) - 1.31013) + 0.126761)**4`
- icbr_refit_commit formula (display, rounded):
  - `0.0251631 + 0.237023/(-(0.547071*tan(0.34692*x_1 - 3.8856) + 0.644806*Abs(1.681*x_3 - 1.99564) + 1.27053)*(1.64715*sin(0.61148*x_3 + 1.7842) - 0.0262407*sin(1.04072*x_4 + 0.81604) + 0.0647976*tan(0.67664*x_2 + 4.53484) + 0.0236438*acos(1.89388 - 0.89108*x_5) + 0.0955948*asin(0.501*x_6 - 1.501) - 1.5028) - 0.0554219)**3`

### task=feynman_II_6_15a seed=13

- Task source: feynman_file
- Target formula: `p_d/(4*pi*epsilon)*3*z/r**5*sqrt(x**2+y**2)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.672021e-02, r2=0.891533
- Variant formula overview:
  - icbr_full: symbolic_s=1.021718e+00, imitation_mse=3.411409e-03, target_mse=1.473744e-02, formula_export_success=True
  - icbr_no_replay: symbolic_s=8.178265e-01, imitation_mse=3.314594e-03, target_mse=1.486033e-02, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.436326e+00, imitation_mse=3.411408e-03, target_mse=1.473744e-02, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.822846e+00, imitation_mse=4.033037e-03, target_mse=1.510505e-02, formula_export_success=True
- icbr_full formula (display, rounded):
  - `1.298*tanh(0.7*(-0.618022*cos(1.15*x_6 + 2.15) - 0.224877*Abs(3.7*x_2 - 4.75) - 1.95563)*(-0.0830593*sin(1.75*x_5 - 3.9) + 0.101533*tan(0.95*x_1 + 1.05) + 0.208994*tan(1.2*x_3 + 3.7) - 0.0363642*Abs(3.35*x_4 - 4.35) + 0.120932*acos(0.6*x_2 - 1.3) - 0.162858*asin(0.6*x_6 - 1.5) - 0.0712528) - 1.35) + 1.21631`
- icbr_no_replay formula (display, rounded):
  - `1.298*tanh(0.7*(-0.618022*cos(1.15*x_6 + 2.15) - 0.224877*Abs(3.7*x_2 - 4.75) - 1.95563)*(0.101533*tan(0.95*x_1 + 1.05) + 0.208994*tan(1.2*x_3 + 3.7) - 0.148407*tan(0.65*x_6 + 4.825) - 0.0363642*Abs(3.35*x_4 - 4.35) - 0.0530389*Abs(2.25*x_5 - 3.1) - 0.120932*asin(0.6*x_2 - 1.3) + 0.245632) - 1.35) + 1.21631`
- icbr_no_shared formula (display, rounded):
  - `1.298*tanh(0.7*(-0.618022*cos(1.15*x_6 + 2.15) - 0.224877*Abs(3.7*x_2 - 4.75) - 1.95563)*(-0.0830593*sin(1.75*x_5 - 3.9) + 0.101533*tan(0.95*x_1 + 1.05) + 0.208994*tan(1.2*x_3 + 3.7) - 0.0363642*Abs(3.35*x_4 - 4.35) - 0.162858*acos(1.5 - 0.6*x_6) + 0.120932*acos(0.6*x_2 - 1.3) + 0.184564) - 1.35) + 1.21631`
- icbr_refit_commit formula (display, rounded):
  - `1.45823*tanh(0.61572*(-0.581469*cos(1.23852*x_6 - 4.288) - 0.221344*Abs(3.65732*x_2 - 4.54936) - 1.92602)*(-0.0956918*sin(1.44944*x_5 + 2.88032) + 0.14295*tan(0.70288*x_1 - 1.72388) + 0.216543*tan(1.18656*x_3 + 3.73304) - 0.0354765*Abs(3.33956*x_4 - 4.2216) - 0.123864*acos(1.28996 - 0.58544*x_2) - 0.162632*asin(0.60104*x_6 - 1.50092) + 0.322791) - 1.30512) + 1.34601`

### task=feynman_II_6_15a seed=14

- Task source: feynman_file
- Target formula: `p_d/(4*pi*epsilon)*3*z/r**5*sqrt(x**2+y**2)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.746401e-02, r2=0.863890
- Variant formula overview:
  - icbr_full: symbolic_s=7.784355e-01, imitation_mse=3.166891e-03, target_mse=1.258425e-02, formula_export_success=True
  - icbr_no_replay: symbolic_s=6.666676e-01, imitation_mse=3.127204e-03, target_mse=1.266108e-02, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.090874e+00, imitation_mse=3.166891e-03, target_mse=1.258425e-02, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.303898e+00, imitation_mse=1.201004e-02, target_mse=1.991849e-02, formula_export_success=True
- icbr_full formula (display, rounded):
  - `2.26687 - 2.3091*tanh(0.212721*cos(1.45*x_4 + 4.6) + 0.0959782*tan(1.0*x_1 - 2.4) + 0.513052*tan(1.1*x_3 + 3.9) - 0.0967663*Abs(4.05*x_2 - 4.975) - 0.0880859*Abs(2.5*x_5 - 3.45) - 0.104502*Abs(3.95*x_6 - 4.875) + 2.91267)`
- icbr_no_replay formula (display, rounded):
  - `2.3091*tanh(-0.0959782*tan(1.0*x_1 - 2.4) - 0.513052*tan(1.1*x_3 + 3.9) + 0.0967663*Abs(4.05*x_2 - 4.975) + 0.0782482*Abs(3.4*x_4 - 4.45) + 0.0880859*Abs(2.5*x_5 - 3.45) + 0.104502*Abs(3.95*x_6 - 4.875) - 3.15976) + 2.26687`
- icbr_no_shared formula (display, rounded):
  - `2.26687 - 2.3091*tanh(0.212721*cos(1.45*x_4 + 4.6) + 0.0959782*tan(1.0*x_1 - 2.4) + 0.513052*tan(1.1*x_3 + 3.9) - 0.0967663*Abs(4.05*x_2 - 4.975) - 0.0880859*Abs(2.5*x_5 - 3.45) - 0.104502*Abs(3.95*x_6 - 4.875) + 2.91267)`
- icbr_refit_commit formula (display, rounded):
  - `3.31619 - 3.39452*tanh(0.174744*cos(1.451*x_4 - 1.68492) + 0.0673695*tan(0.63616*x_1 + 1.06992) + 0.741553*tan(0.68676*x_3 + 4.51328) - 0.0858879*Abs(3.67032*x_2 - 4.36716) - 0.0606453*Abs(2.93144*x_5 - 4.03752) - 0.124433*Abs(2.65392*x_6 - 3.16504) + 3.03098)`

### task=feynman_II_6_15a seed=15

- Task source: feynman_file
- Target formula: `p_d/(4*pi*epsilon)*3*z/r**5*sqrt(x**2+y**2)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.296408e-02, r2=0.918742
- Variant formula overview:
  - icbr_full: symbolic_s=1.117308e+00, imitation_mse=3.510766e-03, target_mse=1.304162e-02, formula_export_success=True
  - icbr_no_replay: symbolic_s=8.633879e-01, imitation_mse=3.507615e-03, target_mse=1.303251e-02, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.612854e+00, imitation_mse=3.510766e-03, target_mse=1.304162e-02, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.891168e+00, imitation_mse=4.770343e-03, target_mse=1.166458e-02, formula_export_success=True
- icbr_full formula (display, rounded):
  - `1.55479*tanh(0.8*(-0.115672*tan(1.25*x_3 + 3.6) + 0.143325*Abs(3.6*x_5 - 4.65) + 0.205164*Abs(3.7*x_6 - 4.8) + 0.807792)*(0.13738*cos(0.75*x_4 + 3.05) - 0.0811008*tan(1.15*x_1 + 3.8) - 0.254246*tan(1.1*x_3 + 3.9) + 0.0629235*tan(0.9*x_6 + 1.2) + 0.0513297*Abs(4.1*x_2 - 4.6) + 0.0101289*Abs(4.3*x_5 - 4.85) - 0.351662) - 1.35) + 1.45407`
- icbr_no_replay formula (display, rounded):
  - `1.55479*tanh(0.8*(-0.115672*tan(1.25*x_3 + 3.6) + 0.143325*Abs(3.6*x_5 - 4.65) + 0.205164*Abs(3.7*x_6 - 4.8) + 0.807792)*(0.146687*sin(0.7*x_4 + 4.7) - 0.0811008*tan(1.15*x_1 + 3.8) - 0.254246*tan(1.1*x_3 + 3.9) + 0.0513297*Abs(4.1*x_2 - 4.6) + 0.0101289*Abs(4.3*x_5 - 4.85) + 0.0780568*asin(0.8*x_6 - 1.8) - 0.341209) - 1.35) + 1.45407`
- icbr_no_shared formula (display, rounded):
  - `1.55479*tanh(0.8*(-0.115672*tan(1.25*x_3 + 3.6) + 0.143325*Abs(3.6*x_5 - 4.65) + 0.205164*Abs(3.7*x_6 - 4.8) + 0.807792)*(0.13738*cos(0.75*x_4 + 3.05) - 0.0811008*tan(1.15*x_1 + 3.8) - 0.254246*tan(1.1*x_3 + 3.9) + 0.0629235*tan(0.9*x_6 + 1.2) + 0.0513297*Abs(4.1*x_2 - 4.6) + 0.0101289*Abs(4.3*x_5 - 4.85) - 0.351662) - 1.35) + 1.45407`
- icbr_refit_commit formula (display, rounded):
  - `1.52859*tanh(0.79284*(-0.116353*tan(1.0914*x_3 + 0.61084) + 0.20433*Abs(3.63764*x_6 - 4.6474) + 1.85527 - 1.01708*exp(-0.581559*(1 - 0.87637*x_5)**2))*(0.155101*cos(0.66084*x_4 - 3.09332) - 0.102239*tan(0.73224*x_1 - 2.03488) - 0.339182*tan(0.602*x_3 - 4.99996) + 0.0628395*tan(0.90088*x_6 + 1.19856) + 0.0845297*Abs(2.46024*x_2 - 2.662) + 0.00885694*Abs(4.802*x_5 - 4.99628) - 0.655092) - 1.31716) + 1.41961`

### task=feynman_II_6_15a seed=16

- Task source: feynman_file
- Target formula: `p_d/(4*pi*epsilon)*3*z/r**5*sqrt(x**2+y**2)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=4.659444e-02, r2=0.644485
- Variant formula overview:
  - icbr_full: symbolic_s=1.154887e+00, imitation_mse=6.591200e-03, target_mse=4.431628e-02, formula_export_success=True
  - icbr_no_replay: symbolic_s=8.830530e-01, imitation_mse=6.390994e-03, target_mse=4.458779e-02, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.619721e+00, imitation_mse=6.591200e-03, target_mse=4.431628e-02, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.992325e+00, imitation_mse=1.086126e-02, target_mse=4.313460e-02, formula_export_success=True
- icbr_full formula (display, rounded):
  - `1.07032 - 0.967076*atan(3.5*(-0.0485852*Abs(2.8*x_2 - 3.8) - 0.034781*Abs(3.4*x_6 - 4.4) - 0.206315 - 0.172102*exp(-25.0*(1 - 0.995*x_3)**2) - 0.150124*exp(-25.0*(0.965 - x_1)**2))*(-0.0508457*cos(2.2*x_6 - 3.3) + 1.16708 - 0.314733*exp(-3.24*(1 - 0.666667*x_5)**2) - 0.288612*exp(-3.8025*(1 - 0.641026*x_4)**2) + 0.656798*exp(-25.0*(1 - x_3)**2) - 0.0152297*exp(-6.25*(1 - 0.62*x_1)**2)) + 2.85)`
- icbr_no_replay formula (display, rounded):
  - `1.07032 - 0.967076*atan(3.5*(-0.0485852*Abs(2.8*x_2 - 3.8) - 0.034781*Abs(3.4*x_6 - 4.4) - 0.206315 - 0.172102*exp(-25.0*(1 - 0.995*x_3)**2) - 0.150124*exp(-25.0*(0.965 - x_1)**2))*(0.0970713*Abs(2.3*x_4 - 3.5) + 0.0733449*Abs(3.2*x_5 - 4.65) + 0.0250255*Abs(3.25*x_6 - 4.7) + 0.460403 + 0.656798*exp(-25.0*(1 - x_3)**2) - 0.0152297*exp(-6.25*(1 - 0.62*x_1)**2)) + 2.85)`
- icbr_no_shared formula (display, rounded):
  - `1.07032 - 0.967076*atan(3.5*(-0.0485852*Abs(2.8*x_2 - 3.8) - 0.034781*Abs(3.4*x_6 - 4.4) - 0.206315 - 0.150124*exp(-25.0*(x_1 - 0.965)**2) - 0.172102*exp(-25.0*(1 - 0.995*x_3)**2))*(-0.0508457*cos(2.2*x_6 - 3.3) + 1.16708 - 0.314733*exp(-3.24*(1 - 0.666667*x_5)**2) - 0.288612*exp(-3.8025*(1 - 0.641026*x_4)**2) + 0.656798*exp(-25.0*(1 - x_3)**2) - 0.0152297*exp(-6.25*(1 - 0.62*x_1)**2)) + 2.85)`
- icbr_refit_commit formula (display, rounded):
  - `-0.0922289 + 2.09175*exp(-4.80399*(-0.793248*(-0.0440683*Abs(3.06296*x_2 - 4.18644) - 0.0315011*Abs(3.63536*x_6 - 4.5268) - 0.0492513*sign(4.99986 - 4.29*x_1) - 0.253958 - 2.05085*exp(-1.80096*(-x_3 - 0.149538)**2))*(-0.050834*cos(2.20112*x_6 - 3.30172) + 1.19129 + 11.0669*exp(-1.59012*(-x_3 - 0.317209)**2) - 0.33722*exp(-2.52886*(1 - 0.665837*x_5)**2) - 0.294272*exp(-3.68717*(1 - 0.632726*x_4)**2) - 0.0159127*exp(-5.03518*(1 - 0.612018*x_1)**2)) - 1)**2)`

### task=feynman_II_6_15a seed=17

- Task source: feynman_file
- Target formula: `p_d/(4*pi*epsilon)*3*z/r**5*sqrt(x**2+y**2)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.638500e-02, r2=0.910131
- Variant formula overview:
  - icbr_full: symbolic_s=1.248999e+00, imitation_mse=3.050191e-03, target_mse=1.531200e-02, formula_export_success=True
  - icbr_no_replay: symbolic_s=9.598194e-01, imitation_mse=3.021654e-03, target_mse=1.517416e-02, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.800304e+00, imitation_mse=3.050191e-03, target_mse=1.531200e-02, formula_export_success=True
  - icbr_refit_commit: symbolic_s=2.091030e+00, imitation_mse=4.933877e-03, target_mse=1.379120e-02, formula_export_success=True
- icbr_full formula (display, rounded):
  - `1.59789*tanh(0.9*(-0.20356*tan(1.05*x_3 + 0.9) + 0.0885478*Abs(3.8*x_4 - 4.85) + 0.17082*Abs(3.75*x_6 - 4.725) + 0.714288 - 0.166266*exp(-3.8025*(1 - 0.666667*x_5)**2))*(0.118308*sqrt(x_6 - 0.987654) - 0.0750134*tan(1.15*x_1 + 3.8) - 0.209404*tan(1.15*x_3 + 3.8) + 0.0534505*Abs(4.15*x_2 - 4.65) + 0.0372264*Abs(2.65*x_5 - 3.6) - 0.424399 - 0.0509126*exp(-2.7225*(1 - 0.666667*x_4)**2)) - 1.35) + 1.45024`
- icbr_no_replay formula (display, rounded):
  - `1.59789*tanh(0.9*(-0.20356*tan(1.05*x_3 + 0.9) + 0.0885478*Abs(3.8*x_4 - 4.85) + 0.0383786*Abs(3.3*x_5 - 4.75) + 0.17082*Abs(3.75*x_6 - 4.725) + 0.538286)*(-0.0750134*tan(1.15*x_1 + 3.8) - 0.209404*tan(1.15*x_3 + 3.8) + 0.047141*tan(1.0*x_6 + 0.95) + 0.0534505*Abs(4.15*x_2 - 4.65) + 0.0111914*Abs(3.2*x_4 - 4.625) + 0.0372264*Abs(2.65*x_5 - 3.6) - 0.352082) - 1.35) + 1.45024`
- icbr_no_shared formula (display, rounded):
  - `1.59789*tanh(0.9*(-0.20356*tan(1.05*x_3 + 0.9) + 0.0885478*Abs(3.8*x_4 - 4.85) + 0.17082*Abs(3.75*x_6 - 4.725) + 0.714288 - 0.166266*exp(-3.8025*(1 - 0.666667*x_5)**2))*(0.118308*sqrt(x_6 - 0.987654) - 0.0750134*tan(1.15*x_1 + 3.8) - 0.209404*tan(1.15*x_3 + 3.8) + 0.0534505*Abs(4.15*x_2 - 4.65) + 0.0372264*Abs(2.65*x_5 - 3.6) - 0.424399 - 0.0509126*exp(-2.7225*(1 - 0.666667*x_4)**2)) - 1.35) + 1.45024`
- icbr_refit_commit formula (display, rounded):
  - `-0.111644 + 2.71764*exp(-2.80951*(-0.368962*(-0.327297*tan(0.72472*x_3 - 1.73612) + 0.125228*Abs(2.6046*x_4 - 3.20428) + 0.172985*Abs(3.60248*x_6 - 4.409) + 0.650569 - 0.175494*exp(-2.89*(1 - 0.668235*x_5)**2))*(0.0229302*sin(2.1008*x_4 - 4.7014) - 0.101625*tan(0.69104*x_1 + 4.30984) - 0.257077*tan(0.75208*x_3 - 2.06448) + 0.0715086*tan(0.6684*x_6 - 4.87476) + 0.089552*Abs(2.44084*x_2 - 2.53992) + 0.0312838*Abs(3.13972*x_5 - 4.31568) - 0.527965) + 1)**2)`

### task=feynman_II_6_15a seed=18

- Task source: feynman_file
- Target formula: `p_d/(4*pi*epsilon)*3*z/r**5*sqrt(x**2+y**2)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=7.634224e-03, r2=0.958082
- Variant formula overview:
  - icbr_full: symbolic_s=8.236352e-01, imitation_mse=2.901497e-03, target_mse=7.073708e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=6.745109e-01, imitation_mse=2.844366e-03, target_mse=7.036407e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.104358e+00, imitation_mse=2.901497e-03, target_mse=7.073708e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.440737e+00, imitation_mse=7.466258e-03, target_mse=1.135773e-02, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0.0350538*(0.137454*sin(1.5*x_5 + 2.95) - 0.174169*tan(1.05*x_1 + 0.9) - 0.621515*tan(1.05*x_3 + 0.9) + 0.574484*atanh(0.5*x_2 - 1.05) + 0.701741 + exp(-2.4025*(1 - 0.225806*x_6)**2) - 0.343375*exp(-0.49*(1 - 0.928571*x_4)**2))**4 + 0.00444999`
- icbr_no_replay formula (display, rounded):
  - `0.0135086*(-0.221056*tan(1.05*x_1 + 0.9) - 0.788829*tan(1.05*x_3 + 0.9) + 0.844849*tanh(0.45*x_6 - 1.1) + 0.0583975*Abs(3.7*x_4 - 4.7) + 0.0687092*Abs(3.25*x_5 - 4.2) + 0.520056*asin(0.7*x_2 - 1.45) + 1)**4 + 0.00444999`
- icbr_no_shared formula (display, rounded):
  - `0.0350538*(0.137454*sin(1.5*x_5 + 2.95) - 0.174169*tan(1.05*x_1 + 0.9) - 0.621515*tan(1.05*x_3 + 0.9) + 0.574484*atanh(0.5*x_2 - 1.05) + 0.701741 + exp(-2.4025*(1 - 0.225806*x_6)**2) - 0.343375*exp(-0.49*(1 - 0.928571*x_4)**2))**4 + 0.00444999`
- icbr_refit_commit formula (display, rounded):
  - `-0.0138545 + 10.6891*exp(-3.14147*(-0.0437495*sin(1.49872*x_5 - 0.18964) - 0.0889312*tan(0.72588*x_1 - 1.73532) - 0.31041*tan(0.73288*x_3 - 1.75784) + 0.193904*atanh(0.474*x_2 - 0.99966) - 1 - 0.433598*exp(-0.0642521*(-x_6 - 0.291936)**2) - 0.112505*exp(-0.424218*(1 - 0.957625*x_4)**2))**2)`

### task=feynman_II_6_15a seed=19

- Task source: feynman_file
- Target formula: `p_d/(4*pi*epsilon)*3*z/r**5*sqrt(x**2+y**2)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=7.792956e-03, r2=0.940272
- Variant formula overview:
  - icbr_full: symbolic_s=1.251087e+00, imitation_mse=2.462572e-03, target_mse=5.380500e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=9.535215e-01, imitation_mse=2.959260e-03, target_mse=6.426406e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.879739e+00, imitation_mse=2.462572e-03, target_mse=5.380504e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=2.218758e+00, imitation_mse=7.754250e-03, target_mse=7.792068e-03, formula_export_success=True
- icbr_full formula (display, rounded):
  - `-0.058302 + 3.64933*exp(-2.7225*(-0.363636*(0.478191*cos(0.95*x_6 + 2.6) - 0.113266*tan(1.2*x_3 + 3.7) + 2.88185 - 0.438439*exp(-0.3025*(x_5 - 1)**2) - 1.21549*exp(-0.49*(0.928571*x_2 - 1)**2))*(0.883878*(0.0621762*x_4 + 1)**(3/2) + 0.15922*cos(0.75*x_6 + 3.05) - 0.27446*tan(1.05*x_3 + 0.85) + 0.0284585*Abs(2.65*x_5 - 3.55) - 0.154495*acos(1.85 - 0.85*x_1) + 0.10879*asin(0.85*x_2 - 1.85) - 1.11284) + 1)**2)`
- icbr_no_replay formula (display, rounded):
  - `-0.058302 + 3.64933*exp(-2.7225*(-0.363636*(0.480468*sin(0.95*x_6 + 4.15) + 0.152287*Abs(3.95*x_2 - 5.0) - 0.215485*atanh(0.8*x_3 - 1.8) + 1.59945 - 0.438439*exp(-0.3025*(x_5 - 1)**2))*(0.883878*(0.0621762*x_4 + 1)**(3/2) + 0.110687*tan(0.8*x_2 + 4.55) - 0.27446*tan(1.05*x_3 + 0.85) + 0.0284585*Abs(2.65*x_5 - 3.55) + 0.0256592*Abs(4.4*x_6 - 4.85) - 0.154495*acos(1.85 - 0.85*x_1) - 1.23882) + 1)**2)`
- icbr_no_shared formula (display, rounded):
  - `-0.058302 + 3.64933*exp(-2.7225*(-0.363636*(0.478191*cos(0.95*x_6 + 2.6) - 0.113266*tan(1.2*x_3 + 3.7) + 2.88185 - 0.438439*exp(-0.3025*(x_5 - 1)**2) - 1.21549*exp(-0.49*(0.928571*x_2 - 1)**2))*(0.888711*(0.0618557*x_4 + 1)**(3/2) + 0.15922*cos(0.75*x_6 + 3.05) - 0.27446*tan(1.05*x_3 + 0.85) + 0.0284585*Abs(2.65*x_5 - 3.55) - 0.154495*asin(0.85*x_1 - 1.85) + 0.10879*asin(0.85*x_2 - 1.85) - 1.36037) + 1)**2)`
- icbr_refit_commit formula (display, rounded):
  - `11.1643 - 11.173*exp(-0.0399999*(-(0.516394*cos(0.8772*x_6 - 3.58156) - 0.135997*tan(0.85048*x_3 + 0.93272) + 2.83883 - 1.21719*exp(-0.490952*(1 - 0.926757*x_2)**2) - 0.439445*exp(-0.292162*(0.954636 - x_5)**2))*(0.861306*(0.0637183*x_4 + 1)**(3/2) - 0.158627*cos(0.753*x_6 - 0.0964399) - 0.43823*tan(0.69328*x_3 + 4.50292) + 0.0250259*Abs(2.9646*x_5 - 3.9484) - 0.173639*acos(1.73412 - 0.76432*x_1) + 0.108697*asin(0.85064*x_2 - 1.8508) - 1.20849) - 0.66)**2)`

### task=feynman_II_6_15a seed=20

- Task source: feynman_file
- Target formula: `p_d/(4*pi*epsilon)*3*z/r**5*sqrt(x**2+y**2)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=2.374646e-02, r2=0.796181
- Variant formula overview:
  - icbr_full: symbolic_s=8.321497e-01, imitation_mse=4.789907e-03, target_mse=2.124733e-02, formula_export_success=True
  - icbr_no_replay: symbolic_s=6.813623e-01, imitation_mse=4.789907e-03, target_mse=2.124733e-02, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.272433e+00, imitation_mse=4.789907e-03, target_mse=2.124733e-02, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.349696e+00, imitation_mse=6.729443e-03, target_mse=2.233068e-02, formula_export_success=True
- icbr_full formula (display, rounded):
  - `-0.0461915 + 1.84528*exp(-6.9422*(0.125158*tan(1.15*x_3 + 3.8) - 0.0451894*Abs(2.65*x_2 - 3.55) - 0.0324091*Abs(2.6*x_4 - 3.6) - 0.0275025*Abs(3.25*x_5 - 4.6) - 0.0283131*Abs(3.95*x_6 - 4.975) + 1 - 0.110364*exp(-25.0*(1 - 0.98*x_1)**2))**2)`
- icbr_no_replay formula (display, rounded):
  - `-0.0461915 + 1.84528*exp(-6.9422*(0.125158*tan(1.15*x_3 + 3.8) - 0.0451894*Abs(2.65*x_2 - 3.55) - 0.0324091*Abs(2.6*x_4 - 3.6) - 0.0275025*Abs(3.25*x_5 - 4.6) - 0.0283131*Abs(3.95*x_6 - 4.975) + 1 - 0.110364*exp(-25.0*(1 - 0.98*x_1)**2))**2)`
- icbr_no_shared formula (display, rounded):
  - `-0.0461915 + 1.84528*exp(-6.9422*(0.125158*tan(1.15*x_3 + 3.8) - 0.0451894*Abs(2.65*x_2 - 3.55) - 0.0324091*Abs(2.6*x_4 - 3.6) - 0.0275025*Abs(3.25*x_5 - 4.6) - 0.0283131*Abs(3.95*x_6 - 4.975) + 1 - 0.110364*exp(-25.0*(1 - 0.98*x_1)**2))**2)`
- icbr_refit_commit formula (display, rounded):
  - `-0.142408 + 4.72343*exp(-5.52633*(0.0895826*tan(0.77932*x_3 - 2.09552) - 0.0247218*Abs(2.83496*x_2 - 3.747) - 0.0143462*Abs(3.5158*x_4 - 4.93188) - 0.0168167*Abs(3.18908*x_5 - 4.58544) - 0.0196238*Abs(3.34552*x_6 - 4.12952) + 1 - 0.0982394*exp(-8.57834*(0.831813 - x_1)**2))**2)`

### task=feynman_II_6_15b seed=1

- Task source: feynman_file
- Target formula: `p_d/(4*pi*epsilon)*3*cos(theta)*sin(theta)/r**3`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=9.840300e-04, r2=-0.000356
- Variant formula overview:
  - icbr_full: symbolic_s=1.123231e+00, imitation_mse=1.520482e-15, target_mse=9.840296e-04, formula_export_success=True
  - icbr_no_replay: symbolic_s=8.375523e-01, imitation_mse=1.754415e-15, target_mse=9.840297e-04, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.518955e+00, imitation_mse=1.522836e-15, target_mse=9.840296e-04, formula_export_success=True
  - icbr_refit_commit: symbolic_s=2.150504e+00, imitation_mse=nan, target_mse=nan, formula_export_success=True
- icbr_full formula (display, rounded):
  - `-5.21757e-8*tan(0.0512263*(0.01*x_1 + 1)**4 + 1.45817 + 0.0420038*exp(-0.1*x_3)) - 0.00967162 - 4.99119e-5/((0.03*x_3 + 1)**3 - 0.034302*asin(0.85*x_1 - 1.85) + 0.951036)**5 - 6.42725e-5/(0.179959*(-0.01*x_1 - 1)**4 - 1 - 0.225899*exp(-0.05*x_3))**4`
- icbr_no_replay formula (display, rounded):
  - `-0.00967604 - 2.86535e-5/((-0.0201005*x_3 - 1)**4 - 0.0285563*tan(0.85*x_1 + 1.3) + 0.746391)**5 + 6.03862e-5/(0.153406*(-0.01*x_1 - 1)**4 - 1 - 0.192568*exp(-0.05*x_3))**5 - 8.23159e-8/(-0.307311*(1 - 0.0222222*x_3)**4 - 0.354704*(0.01*x_1 + 1)**4 + 1)**3`
- icbr_no_shared formula (display, rounded):
  - `-5.21757e-8*tan(0.0512263*(-0.01*x_1 - 1)**4 + 1.45817 + 0.0420038*exp(-0.1*x_3)) - 0.00967198 - 4.99119e-5/((0.03*x_3 + 1)**3 - 0.034302*asin(0.85*x_1 - 1.85) + 0.951036)**5 - 6.3921e-5/(-0.180998*(-0.01*x_1 - 1)**4 + 1 + 0.227203*exp(-0.05*x_3))**4`
- icbr_refit_commit formula (display, rounded):
  - `-7.14026e-9*tan(0.0366173*(1 - 0.0317781*x_3)**4 + 0.0268455*(-0.0200009*x_1 - 1)**4 - 4.76178) - 0.00969437 - 1.46866e-5/(0.403664*(-0.0196389*x_3 - 1)**4 - 0.010469*asin(0.96616*x_1 - 1.96796) + 1)**5 - 5.30599e-6/(0.119316*(-0.0132019*x_1 - 1)**4 + 0.250519*exp(0.034*x_3) - 1)**4`

### task=feynman_II_6_15b seed=2

- Task source: feynman_file
- Target formula: `p_d/(4*pi*epsilon)*3*cos(theta)*sin(theta)/r**3`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=8.323397e-04, r2=-0.000965
- Variant formula overview:
  - icbr_full: symbolic_s=1.281856e+00, imitation_mse=1.888183e-07, target_mse=8.322987e-04, formula_export_success=True
  - icbr_no_replay: symbolic_s=8.927720e-01, imitation_mse=1.915407e-07, target_mse=8.309010e-04, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.761575e+00, imitation_mse=1.887738e-07, target_mse=8.322989e-04, formula_export_success=True
  - icbr_refit_commit: symbolic_s=2.143621e+00, imitation_mse=2.011217e-07, target_mse=8.323310e-04, formula_export_success=True
- icbr_full formula (display, rounded):
  - `-0.000373584*Abs(0.289176*Abs(2.9*x_2 - 4.25) - 0.0411592) - 0.0101144 + 2.06469e-5/(Abs(2.75*x_4 - 4.1) + 0.71054)**3 - 3.48117e-5/((0.0976062*sin(2.2*x_2 - 1.8) - 0.285189)*(0.0117844*sign(3.1 - 2.6*x_1) - 0.13482 + 0.0855563*exp(-6.76*(1 - 0.615385*x_4)**2)) - 0.700001)**4`
- icbr_no_replay formula (display, rounded):
  - `0.00225898*(-(-0.0476222*Abs(3.35*x_2 - 4.95) - 0.164727)*(0.0117844*sign(3.1 - 2.6*x_1) - 0.13482 + 0.0855563*exp(-6.76*(1 - 0.615385*x_4)**2)) - 0.52)**5 - 0.000373584*Abs(0.289176*Abs(2.9*x_2 - 4.25) - 0.0411592) + 0.00241831*Abs(0.077353*Abs(2.7*x_4 - 4.15) - 0.0817686) - 0.0103594 - 7.95309e-5/(-0.863974*Abs(2.75*x_4 - 4.1) - 1)**5`
- icbr_no_shared formula (display, rounded):
  - `-0.000373584*Abs(0.289176*Abs(2.9*x_2 - 4.25) - 0.0411592) - 0.0101144 + 1.29412e-5/(Abs(2.35*x_4 - 3.5) + 0.608379)**3 - 3.48117e-5/((0.0976062*sin(2.2*x_2 - 1.8) - 0.285189)*(0.0117844*sign(3.1 - 2.6*x_1) - 0.13482 + 0.0855563*exp(-6.76*(1 - 0.615385*x_4)**2)) - 0.700001)**4`
- icbr_refit_commit formula (display, rounded):
  - `-0.000400126*Abs(0.356421*Abs(2.466*x_2 - 3.69976) - 0.227721) + 1.01527e-5*sign(0.0373722 - 0.0566361*Abs(2.83656*x_4 - 4.46284)) - 0.0101406 - 3.45811e-5/(-(0.0975823*sin(2.20108*x_2 - 1.80164) - 0.285145)*(0.00589409*sign(4.3 - 3.49372*x_1) - 0.148963 + 0.0906166*exp(-5.07745*(1 - 0.60469*x_4)**2)) + 0.699115)**4`

### task=feynman_II_6_15b seed=3

- Task source: feynman_file
- Target formula: `p_d/(4*pi*epsilon)*3*cos(theta)*sin(theta)/r**3`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.071363e-03, r2=-0.143456
- Variant formula overview:
  - icbr_full: symbolic_s=5.939900e-03, imitation_mse=0.000000e+00, target_mse=1.071363e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=6.014300e-03, imitation_mse=0.000000e+00, target_mse=1.071363e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=6.659500e-03, imitation_mse=0.000000e+00, target_mse=1.071363e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=6.616000e-03, imitation_mse=0.000000e+00, target_mse=1.071363e-03, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0`
- icbr_no_replay formula (display, rounded):
  - `0`
- icbr_no_shared formula (display, rounded):
  - `0`
- icbr_refit_commit formula (display, rounded):
  - `0`

### task=feynman_II_6_15b seed=4

- Task source: feynman_file
- Target formula: `p_d/(4*pi*epsilon)*3*cos(theta)*sin(theta)/r**3`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=9.244844e-04, r2=-0.113510
- Variant formula overview:
  - icbr_full: symbolic_s=1.096170e-02, imitation_mse=0.000000e+00, target_mse=9.244844e-04, formula_export_success=True
  - icbr_no_replay: symbolic_s=9.870800e-03, imitation_mse=0.000000e+00, target_mse=9.244844e-04, formula_export_success=True
  - icbr_no_shared: symbolic_s=9.178500e-03, imitation_mse=0.000000e+00, target_mse=9.244844e-04, formula_export_success=True
  - icbr_refit_commit: symbolic_s=9.534100e-03, imitation_mse=0.000000e+00, target_mse=9.244844e-04, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0`
- icbr_no_replay formula (display, rounded):
  - `0`
- icbr_no_shared formula (display, rounded):
  - `0`
- icbr_refit_commit formula (display, rounded):
  - `0`

### task=feynman_II_6_15b seed=5

- Task source: feynman_file
- Target formula: `p_d/(4*pi*epsilon)*3*cos(theta)*sin(theta)/r**3`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=7.740369e-04, r2=-0.108638
- Variant formula overview:
  - icbr_full: symbolic_s=5.925600e-03, imitation_mse=0.000000e+00, target_mse=7.740369e-04, formula_export_success=True
  - icbr_no_replay: symbolic_s=6.753200e-03, imitation_mse=0.000000e+00, target_mse=7.740369e-04, formula_export_success=True
  - icbr_no_shared: symbolic_s=6.200200e-03, imitation_mse=0.000000e+00, target_mse=7.740369e-04, formula_export_success=True
  - icbr_refit_commit: symbolic_s=5.480400e-03, imitation_mse=0.000000e+00, target_mse=7.740369e-04, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0`
- icbr_no_replay formula (display, rounded):
  - `0`
- icbr_no_shared formula (display, rounded):
  - `0`
- icbr_refit_commit formula (display, rounded):
  - `0`

### task=feynman_II_6_15b seed=6

- Task source: feynman_file
- Target formula: `p_d/(4*pi*epsilon)*3*cos(theta)*sin(theta)/r**3`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=9.548308e-04, r2=-0.113994
- Variant formula overview:
  - icbr_full: symbolic_s=7.941700e-03, imitation_mse=0.000000e+00, target_mse=9.548308e-04, formula_export_success=True
  - icbr_no_replay: symbolic_s=7.895700e-03, imitation_mse=0.000000e+00, target_mse=9.548308e-04, formula_export_success=True
  - icbr_no_shared: symbolic_s=8.112300e-03, imitation_mse=0.000000e+00, target_mse=9.548308e-04, formula_export_success=True
  - icbr_refit_commit: symbolic_s=7.646700e-03, imitation_mse=0.000000e+00, target_mse=9.548308e-04, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0`
- icbr_no_replay formula (display, rounded):
  - `0`
- icbr_no_shared formula (display, rounded):
  - `0`
- icbr_refit_commit formula (display, rounded):
  - `0`

### task=feynman_II_6_15b seed=7

- Task source: feynman_file
- Target formula: `p_d/(4*pi*epsilon)*3*cos(theta)*sin(theta)/r**3`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=8.986164e-04, r2=-0.102587
- Variant formula overview:
  - icbr_full: symbolic_s=1.010390e-02, imitation_mse=0.000000e+00, target_mse=8.986164e-04, formula_export_success=True
  - icbr_no_replay: symbolic_s=1.027470e-02, imitation_mse=0.000000e+00, target_mse=8.986164e-04, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.148660e-02, imitation_mse=0.000000e+00, target_mse=8.986164e-04, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.125010e-02, imitation_mse=0.000000e+00, target_mse=8.986164e-04, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0`
- icbr_no_replay formula (display, rounded):
  - `0`
- icbr_no_shared formula (display, rounded):
  - `0`
- icbr_refit_commit formula (display, rounded):
  - `0`

### task=feynman_II_6_15b seed=8

- Task source: feynman_file
- Target formula: `p_d/(4*pi*epsilon)*3*cos(theta)*sin(theta)/r**3`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.064811e-03, r2=-0.000941
- Variant formula overview:
  - icbr_full: symbolic_s=7.761182e-01, imitation_mse=3.252846e-09, target_mse=1.064098e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=5.575747e-01, imitation_mse=3.238386e-09, target_mse=1.064101e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=8.397436e-01, imitation_mse=3.252846e-09, target_mse=1.064098e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.265650e+00, imitation_mse=3.552019e-09, target_mse=1.064182e-03, formula_export_success=True
- icbr_full formula (display, rounded):
  - `-0.0148752*(-0.00131313*sign(3.45 - 2.9*x_2) + 1 + 0.00195659*exp(-12.6025*(1 - 0.605634*x_4)**2))**5 + 0.00602061 - 8.03653e-7/(1 - 0.00881444*Abs(4.7*x_2 - 5.0))**5`
- icbr_no_replay formula (display, rounded):
  - `-0.0072863 + 0.00156603/(-0.0118337*sign(3.45 - 2.9*x_2) - 1 + 0.0176324*exp(-12.6025*(1 - 0.605634*x_4)**2))**5 - 8.03653e-7/(1 - 0.00881444*Abs(4.7*x_2 - 5.0))**5`
- icbr_no_shared formula (display, rounded):
  - `-0.0148752*(-0.00131313*sign(3.45 - 2.9*x_2) + 1 + 0.00195659*exp(-12.6025*(1 - 0.605634*x_4)**2))**5 + 0.00602061 - 8.03653e-7/(1 - 0.00881444*Abs(4.7*x_2 - 5.0))**5`
- icbr_refit_commit formula (display, rounded):
  - `0.00814021 - 0.0170046/(-0.00102288*sign(3.19822 - 2.584*x_2) - 1 + 0.00218274*exp(-8.42184*(1 - 0.583259*x_4)**2))**4 - 1.32589e-6/(1 - 0.0083537*Abs(3.98*x_2 - 4.79944))**5`

### task=feynman_II_6_15b seed=9

- Task source: feynman_file
- Target formula: `p_d/(4*pi*epsilon)*3*cos(theta)*sin(theta)/r**3`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=8.612588e-04, r2=-0.112901
- Variant formula overview:
  - icbr_full: symbolic_s=7.052800e-03, imitation_mse=0.000000e+00, target_mse=8.612588e-04, formula_export_success=True
  - icbr_no_replay: symbolic_s=6.710700e-03, imitation_mse=0.000000e+00, target_mse=8.612588e-04, formula_export_success=True
  - icbr_no_shared: symbolic_s=5.454500e-03, imitation_mse=0.000000e+00, target_mse=8.612588e-04, formula_export_success=True
  - icbr_refit_commit: symbolic_s=4.783600e-03, imitation_mse=0.000000e+00, target_mse=8.612588e-04, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0`
- icbr_no_replay formula (display, rounded):
  - `0`
- icbr_no_shared formula (display, rounded):
  - `0`
- icbr_refit_commit formula (display, rounded):
  - `0`

### task=feynman_II_6_15b seed=10

- Task source: feynman_file
- Target formula: `p_d/(4*pi*epsilon)*3*cos(theta)*sin(theta)/r**3`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=8.909228e-04, r2=-0.000565
- Variant formula overview:
  - icbr_full: symbolic_s=5.428615e-01, imitation_mse=5.223306e-10, target_mse=8.908281e-04, formula_export_success=True
  - icbr_no_replay: symbolic_s=4.572104e-01, imitation_mse=5.319392e-10, target_mse=8.908259e-04, formula_export_success=True
  - icbr_no_shared: symbolic_s=6.917387e-01, imitation_mse=5.223306e-10, target_mse=8.908281e-04, formula_export_success=True
  - icbr_refit_commit: symbolic_s=8.892552e-01, imitation_mse=3.150908e-11, target_mse=8.910248e-04, formula_export_success=True
- icbr_full formula (display, rounded):
  - `-0.00892175 + 1.34008e-6/(-0.00104127*sin(2.3*x_2 + 4.3) + 1 + 0.568824*exp(-25.0*(0.89 - x_3)**2) + 3.68782e-8/(0.966667 - x_1)**5)**3`
- icbr_no_replay formula (display, rounded):
  - `-0.00892175 + 9.08948e-7/(0.000456979*Abs(3.3*x_2 - 4.9) + 0.120393*sign(4.4 - 3.85*x_3) + 1 + 3.2402e-8/(0.966667 - x_1)**5)**3`
- icbr_no_shared formula (display, rounded):
  - `-0.00892175 + 1.34008e-6/(-0.00104127*sin(2.3*x_2 + 4.3) + 1 + 0.568824*exp(-25.0*(x_3 - 0.89)**2) - 3.68782e-8/(x_1 - 0.966667)**5)**3`
- icbr_refit_commit formula (display, rounded):
  - `-0.00894552 + 8.96051e-6/(-0.000428194*sin(2.3786*x_2 - 1.95932) + 1 - 0.31856*exp(-1.31469*(1 - 0.492098*x_3)**2) + 6.19734e-9/(0.972118 - x_1)**5)**3`

### task=feynman_II_6_15b seed=11

- Task source: feynman_file
- Target formula: `p_d/(4*pi*epsilon)*3*cos(theta)*sin(theta)/r**3`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=9.960495e-04, r2=-0.002393
- Variant formula overview:
  - icbr_full: symbolic_s=6.932102e-01, imitation_mse=3.718850e-08, target_mse=9.952792e-04, formula_export_success=True
  - icbr_no_replay: symbolic_s=5.212205e-01, imitation_mse=3.831330e-08, target_mse=9.951310e-04, formula_export_success=True
  - icbr_no_shared: symbolic_s=8.738568e-01, imitation_mse=3.718850e-08, target_mse=9.952792e-04, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.216109e+00, imitation_mse=4.021817e-08, target_mse=9.951494e-04, formula_export_success=True
- icbr_full formula (display, rounded):
  - `-0.0108279 + 0.000281193/(-0.00577129*Abs(3.8*x_3 - 4.9) - 0.295265*Abs(3.2*x_4 - 4.9) - 1)**4 - 0.00013759/(0.439376*(0.03*x_4 - 1)**3 - 1)**4`
- icbr_no_replay formula (display, rounded):
  - `-0.0108107 - 0.000213911/(-0.0120815*Abs(3.8*x_3 - 4.9) - 0.6181*Abs(3.2*x_4 - 4.9) - 1)**3 - 0.000150152/(1 - 0.439376*(0.03*x_4 - 1)**3)**5`
- icbr_no_shared formula (display, rounded):
  - `-0.0108279 + 0.000281193/(-0.00577129*Abs(3.8*x_3 - 4.9) - 0.295265*Abs(3.2*x_4 - 4.9) - 1)**4 - 0.00013759/(0.439376*(0.03*x_4 - 1)**3 - 1)**4`
- icbr_refit_commit formula (display, rounded):
  - `-0.0108279 + 0.000276997/(-0.00547177*Abs(3.888*x_3 - 4.8993) - 0.495042*Abs(1.95856*x_4 - 3.09296) - 1)**4 - 9.12656e-6/(-0.273051*(-0.0200031*x_4 - 1)**3 - 1)**4`

### task=feynman_II_6_15b seed=12

- Task source: feynman_file
- Target formula: `p_d/(4*pi*epsilon)*3*cos(theta)*sin(theta)/r**3`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.033659e-03, r2=-0.143498
- Variant formula overview:
  - icbr_full: symbolic_s=5.445900e-03, imitation_mse=0.000000e+00, target_mse=1.033659e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=5.366700e-03, imitation_mse=0.000000e+00, target_mse=1.033659e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=6.584500e-03, imitation_mse=0.000000e+00, target_mse=1.033659e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=7.671900e-03, imitation_mse=0.000000e+00, target_mse=1.033659e-03, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0`
- icbr_no_replay formula (display, rounded):
  - `0`
- icbr_no_shared formula (display, rounded):
  - `0`
- icbr_refit_commit formula (display, rounded):
  - `0`

### task=feynman_II_6_15b seed=13

- Task source: feynman_file
- Target formula: `p_d/(4*pi*epsilon)*3*cos(theta)*sin(theta)/r**3`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=8.972737e-04, r2=-0.052753
- Variant formula overview:
  - icbr_full: symbolic_s=5.656754e-01, imitation_mse=1.092550e-17, target_mse=8.972737e-04, formula_export_success=True
  - icbr_no_replay: symbolic_s=4.598023e-01, imitation_mse=1.092550e-17, target_mse=8.972737e-04, formula_export_success=True
  - icbr_no_shared: symbolic_s=6.910324e-01, imitation_mse=1.092876e-17, target_mse=8.972737e-04, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.006549e+00, imitation_mse=1.019540e-15, target_mse=8.972730e-04, formula_export_success=True
- icbr_full formula (display, rounded):
  - `-0.00331658 - 2.58265e-6/((0.0222222*x_3 - 1)**4 + 0.212364)**4 - 2.94086e-5/(-0.66254*(1 - 0.02*x_3)**5 - 1)**5`
- icbr_no_replay formula (display, rounded):
  - `-0.00331658 - 2.58265e-6/((0.0222222*x_3 - 1)**4 + 0.212364)**4 - 2.94086e-5/(-0.66254*(1 - 0.02*x_3)**5 - 1)**5`
- icbr_no_shared formula (display, rounded):
  - `-0.00331658 - 2.58265e-6/((0.0222222*x_3 - 1)**4 + 0.212364)**4 - 2.94086e-5/(0.66254*(0.02*x_3 - 1)**5 - 1)**5`
- icbr_refit_commit formula (display, rounded):
  - `-0.0033141 - 1.6454e-5/(0.453556*(1 - 0.031637*x_3)**4 + 1)**5 + 1.56135e-6/(-(1 - 0.0408467*x_3)**3 - 0.0329644)**2`

### task=feynman_II_6_15b seed=14

- Task source: feynman_file
- Target formula: `p_d/(4*pi*epsilon)*3*cos(theta)*sin(theta)/r**3`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.032210e-03, r2=-0.117410
- Variant formula overview:
  - icbr_full: symbolic_s=3.554943e-01, imitation_mse=3.142819e-07, target_mse=1.032610e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=2.987323e-01, imitation_mse=3.148398e-07, target_mse=1.032702e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=3.763763e-01, imitation_mse=3.142819e-07, target_mse=1.032610e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=5.309432e-01, imitation_mse=3.278939e-07, target_mse=1.032615e-03, formula_export_success=True
- icbr_full formula (display, rounded):
  - `-0.0217537 - 0.000163137/(-Abs(2.1*x_1 - 3.15) - 0.742405)**3`
- icbr_no_replay formula (display, rounded):
  - `-0.0217471 - 0.000396824/(-0.895162*Abs(2.1*x_1 - 3.15) - 1)**5`
- icbr_no_shared formula (display, rounded):
  - `-0.0217537 - 0.000163137/(-Abs(2.1*x_1 - 3.15) - 0.742405)**3`
- icbr_refit_commit formula (display, rounded):
  - `-0.0217537 - 0.000231498/(-Abs(2.41136*x_1 - 3.7186) - 0.848335)**3`

### task=feynman_II_6_15b seed=15

- Task source: feynman_file
- Target formula: `p_d/(4*pi*epsilon)*3*cos(theta)*sin(theta)/r**3`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=8.955402e-04, r2=-0.002009
- Variant formula overview:
  - icbr_full: symbolic_s=7.872900e-01, imitation_mse=9.327588e-12, target_mse=8.955455e-04, formula_export_success=True
  - icbr_no_replay: symbolic_s=5.679198e-01, imitation_mse=9.497116e-12, target_mse=8.955452e-04, formula_export_success=True
  - icbr_no_shared: symbolic_s=9.077020e-01, imitation_mse=9.327588e-12, target_mse=8.955455e-04, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.364103e+00, imitation_mse=9.402100e-12, target_mse=8.955454e-04, formula_export_success=True
- icbr_full formula (display, rounded):
  - `-0.0096673 + 5.9699e-13/(-(0.07337 - 0.0397138*exp(-9.9225*(1 - 0.587302*x_4)**2))*(0.626402*(1 - 0.488889*x_3)**4 + 0.0229574) - 0.02)**4 + 8.05763e-7/(1 - 1.5441e-8/(0.974619 - x_2)**5)**5`
- icbr_no_replay formula (display, rounded):
  - `-0.00966783 - 1.88732e-14/(-(0.07337 - 0.0397138*exp(-9.9225*(1 - 0.587302*x_4)**2))*(0.0211725*sign(3.3 - 2.8*x_3) + 0.0476236) - 0.0222222)**5 + 1.62115e-6/(1 - 1.5441e-8/(0.974619 - x_2)**5)**4`
- icbr_no_shared formula (display, rounded):
  - `-0.0096673 + 5.9699e-13/(-(0.07337 - 0.0397138*exp(-9.9225*(1 - 0.587302*x_4)**2))*(0.626402*(1 - 0.488889*x_3)**4 + 0.0229574) - 0.02)**4 + 8.05763e-7/(1 - 1.5441e-8/(0.974619 - x_2)**5)**5`
- icbr_refit_commit formula (display, rounded):
  - `-0.00966752 + 5.98424e-13/(-(0.0750579 - 0.0407239*exp(-9.02522*(1 - 0.575421*x_4)**2))*(0.626401*(1 - 0.488893*x_3)**4 + 0.0229573) - 0.0200001)**4 - 1.01814e-6/(-1 + 3.9644e-7/(0.939184 - x_2)**5)**5`

### task=feynman_II_6_15b seed=16

- Task source: feynman_file
- Target formula: `p_d/(4*pi*epsilon)*3*cos(theta)*sin(theta)/r**3`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=9.430442e-04, r2=-0.130366
- Variant formula overview:
  - icbr_full: symbolic_s=1.288700e-02, imitation_mse=0.000000e+00, target_mse=9.430442e-04, formula_export_success=True
  - icbr_no_replay: symbolic_s=1.155700e-02, imitation_mse=0.000000e+00, target_mse=9.430442e-04, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.153910e-02, imitation_mse=0.000000e+00, target_mse=9.430442e-04, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.150920e-02, imitation_mse=0.000000e+00, target_mse=9.430442e-04, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0`
- icbr_no_replay formula (display, rounded):
  - `0`
- icbr_no_shared formula (display, rounded):
  - `0`
- icbr_refit_commit formula (display, rounded):
  - `0`

### task=feynman_II_6_15b seed=17

- Task source: feynman_file
- Target formula: `p_d/(4*pi*epsilon)*3*cos(theta)*sin(theta)/r**3`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=8.237726e-04, r2=-0.105382
- Variant formula overview:
  - icbr_full: symbolic_s=1.444970e-02, imitation_mse=0.000000e+00, target_mse=8.237726e-04, formula_export_success=True
  - icbr_no_replay: symbolic_s=1.483810e-02, imitation_mse=0.000000e+00, target_mse=8.237726e-04, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.456930e-02, imitation_mse=0.000000e+00, target_mse=8.237726e-04, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.593190e-02, imitation_mse=0.000000e+00, target_mse=8.237726e-04, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0`
- icbr_no_replay formula (display, rounded):
  - `0`
- icbr_no_shared formula (display, rounded):
  - `0`
- icbr_refit_commit formula (display, rounded):
  - `0`

### task=feynman_II_6_15b seed=18

- Task source: feynman_file
- Target formula: `p_d/(4*pi*epsilon)*3*cos(theta)*sin(theta)/r**3`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=9.097869e-04, r2=-0.037539
- Variant formula overview:
  - icbr_full: symbolic_s=3.135636e-01, imitation_mse=1.074257e-08, target_mse=9.074827e-04, formula_export_success=True
  - icbr_no_replay: symbolic_s=2.875787e-01, imitation_mse=1.114627e-08, target_mse=9.074197e-04, formula_export_success=True
  - icbr_no_shared: symbolic_s=3.195793e-01, imitation_mse=1.074257e-08, target_mse=9.074827e-04, formula_export_success=True
  - icbr_refit_commit: symbolic_s=5.284915e-01, imitation_mse=1.172495e-08, target_mse=9.073926e-04, formula_export_success=True
- icbr_full formula (display, rounded):
  - `-0.00644062 + 1.79894e-5/(1 - 0.51487*exp(-8.7025*(1 - 0.59322*x_4)**2))**3`
- icbr_no_replay formula (display, rounded):
  - `-0.00642234 + 7.08018e-6/(-1 + 0.514819*exp(-8.7025*(1 - 0.59322*x_4)**2))**4`
- icbr_no_shared formula (display, rounded):
  - `-0.00644062 + 1.79894e-5/(1 - 0.51487*exp(-8.7025*(1 - 0.59322*x_4)**2))**3`
- icbr_refit_commit formula (display, rounded):
  - `-0.00644062 + 1.58915e-5/(1 - 0.517961*exp(-7.28784*(1 - 0.576382*x_4)**2))**3`

### task=feynman_II_6_15b seed=19

- Task source: feynman_file
- Target formula: `p_d/(4*pi*epsilon)*3*cos(theta)*sin(theta)/r**3`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=9.247026e-04, r2=-0.081507
- Variant formula overview:
  - icbr_full: symbolic_s=6.205000e-03, imitation_mse=0.000000e+00, target_mse=9.247026e-04, formula_export_success=True
  - icbr_no_replay: symbolic_s=6.483700e-03, imitation_mse=0.000000e+00, target_mse=9.247026e-04, formula_export_success=True
  - icbr_no_shared: symbolic_s=6.861200e-03, imitation_mse=0.000000e+00, target_mse=9.247026e-04, formula_export_success=True
  - icbr_refit_commit: symbolic_s=6.111400e-03, imitation_mse=0.000000e+00, target_mse=9.247026e-04, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0`
- icbr_no_replay formula (display, rounded):
  - `0`
- icbr_no_shared formula (display, rounded):
  - `0`
- icbr_refit_commit formula (display, rounded):
  - `0`

### task=feynman_II_6_15b seed=20

- Task source: feynman_file
- Target formula: `p_d/(4*pi*epsilon)*3*cos(theta)*sin(theta)/r**3`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.003951e-03, r2=-0.122048
- Variant formula overview:
  - icbr_full: symbolic_s=1.404750e-02, imitation_mse=0.000000e+00, target_mse=1.003951e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=1.140410e-02, imitation_mse=0.000000e+00, target_mse=1.003951e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.107140e-02, imitation_mse=0.000000e+00, target_mse=1.003951e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.091640e-02, imitation_mse=0.000000e+00, target_mse=1.003951e-03, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0`
- icbr_no_replay formula (display, rounded):
  - `0`
- icbr_no_shared formula (display, rounded):
  - `0`
- icbr_refit_commit formula (display, rounded):
  - `0`

### task=feynman_II_21_32 seed=1

- Task source: feynman_file
- Target formula: `q/(4*pi*epsilon*r*(1-v/c))`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.493103e-03, r2=0.379566
- Variant formula overview:
  - icbr_full: symbolic_s=1.195281e+00, imitation_mse=6.726975e-06, target_mse=1.496096e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=8.587104e-01, imitation_mse=6.659655e-06, target_mse=1.509051e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=2.096504e+00, imitation_mse=6.726974e-06, target_mse=1.496096e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=2.248457e+00, imitation_mse=6.985079e-06, target_mse=1.500990e-03, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0.0323129 - 1.82855e-10/(asin(0.0499997*x_5 - 0.5) + 0.454944 - 0.0572828*exp(-3.8025*(1 - 0.461538*x_2)**2))**5 + 0.0102993/((-0.0482399*sin(1.45*x_2 - 4.925) - 3.1617*atanh(0.0499997*x_5 - 0.4) - 1.36817)*(-18.4813*sqrt(0.0222222*x_2 + 1) - 0.0545416*(0.01*x_5 + 1)**2 + 0.0244006*Abs(1.75*x_1 - 3.0) + 18.6696) + 0.5)**3`
- icbr_no_replay formula (display, rounded):
  - `-0.00119382*sign(-6.04513*asin(0.0499997*x_5 - 0.5) - 2.47001 + 0.346282*exp(-3.8025*(1 - 0.461538*x_2)**2)) + 0.0285218 + 0.00899844/(-(-3.13928*asin(0.0499997*x_5 - 0.5) - 0.103826*sign(3.75 - 3.2*x_2) - 1.77674)*(-0.00116174*x_5 + 0.0244006*Abs(1.75*x_1 - 3.0) + 0.972182 - 2.35627*exp(-(1.0 - 0.1*x_2)**2)) - 0.325)**2`
- icbr_no_shared formula (display, rounded):
  - `0.0323129 - 1.82855e-10/(asin(0.0499997*x_5 - 0.5) + 0.454944 - 0.0572828*exp(-3.8025*(1 - 0.461538*x_2)**2))**5 + 0.0102993/((-0.0482399*sin(1.45*x_2 - 4.925) - 3.1617*atanh(0.0499997*x_5 - 0.4) - 1.36817)*(-18.4813*sqrt(0.0222222*x_2 + 1) - 0.0545416*(0.01*x_5 + 1)**2 + 0.0244006*Abs(1.75*x_1 - 3.0) + 18.6696) + 0.5)**3`
- icbr_refit_commit formula (display, rounded):
  - `0.0323295 + 2.12446e-9/(-0.971536*acos(0.60052 - 0.0779999*x_5) + 1 + 0.0892936*exp(-2.9073*(1 - 0.442442*x_2)**2))**5 - 0.0102786/(-(-0.0481897*sin(1.442*x_2 - 4.9) - 22.8382*atanh(0.00432*x_5 - 0.64704) - 17.6503)*(-17.2772*sqrt(0.0238241*x_2 + 1) - 0.0256979*(-0.0200031*x_5 - 1)**2 + 0.0187272*Abs(2.29164*x_1 - 4.08432) + 17.4386) - 0.499731)**3`

### task=feynman_II_21_32 seed=2

- Task source: feynman_file
- Target formula: `q/(4*pi*epsilon*r*(1-v/c))`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=7.359342e-04, r2=0.708554
- Variant formula overview:
  - icbr_full: symbolic_s=3.424450e+00, imitation_mse=1.752526e-04, target_mse=6.899062e-04, formula_export_success=True
  - icbr_no_replay: symbolic_s=1.989883e+00, imitation_mse=2.032042e-04, target_mse=7.048253e-04, formula_export_success=True
  - icbr_no_shared: symbolic_s=5.468410e+00, imitation_mse=1.752526e-04, target_mse=6.899061e-04, formula_export_success=True
  - icbr_refit_commit: symbolic_s=5.496255e+00, imitation_mse=1.900231e-04, target_mse=6.986617e-04, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0.24844*sin(0.0579399*Abs(3.0*x_1 - 4.05) + 0.0176539*Abs(2.45*x_2 - 4.35) - 2.79825*acos(0.0499997*x_5 - 0.5) + 10.7233 - 0.185419*exp(-2.4025*(1 - 0.483871*x_3)**2)) - 0.0404104*Abs(-0.247708*sin(0.5*x_3 - 5.0) + 0.243874*Abs(2.25*x_1 - 3.35) - 0.0826969*Abs(3.3*x_4 - 4.35) + 25.4823*asin(0.0499997*x_5 - 0.5) + 0.118281*sign(3.2*x_2 - 3.75) + 8.28572) + 0.0001526*sign(0.257826*cos(1.4*x_1 - 3.2) - 0.0503119) + 0.352908 - 0.201609*exp(-2.52582*(-0.209584*cos(0.5*x_3 - 0.0500002) - atanh(0.0499997*x_5 - 0.4) - 0.558133 + 0.00517923*exp(-25.0*(1 - 0.93*x_1)**2))**2) + 0.0972032*exp(-1.44*(-(0.0821361*Abs(1.95*x_1 - 3.4) + 1.15497*atanh(0.0499997*x_5 - 0.4) + 0.671772 + 0.00190247/(0.642857 - x_2)**5)*(38.7726*sqrt(0.02*x_2 + 1) - 0.0166462*Abs(2.65*x_1 - 4.8) - 1.33612*asin(0.0499997*x_5 - 0.5) - 39.7541 + 0.0393791*exp(-13.69*(1 - 0.743243*x_4)**2)) - 0.5)**2)`
- icbr_no_replay formula (display, rounded):
  - `0.24844*sin(0.0579399*Abs(3.0*x_1 - 4.05) + 0.0176539*Abs(2.45*x_2 - 4.35) + 2.79825*asin(0.0499997*x_5 - 0.5) + 6.32778 - 0.185419*exp(-2.4025*(1 - 0.483871*x_3)**2)) - 0.0404104*Abs(0.243874*Abs(2.25*x_1 - 3.35) + 0.0418974*Abs(2.75*x_3 - 4.1) - 0.0826969*Abs(3.3*x_4 - 4.35) - 25.4823*acos(0.0499997*x_5 - 0.5) + 0.118281*sign(3.2*x_2 - 3.75) + 48.0588) + 0.0001526*sign(-0.28336 + 0.519554*exp(-3.4225*(1 - 0.459459*x_1)**2)) + 0.352908 - 0.201609*exp(-2.49053*(0.0271865*Abs(3.6*x_3 - 4.65) - asin(0.0499997*x_5 - 0.5) + 0.00272657*sign(3.4 - 2.85*x_1) - 0.850387)**2) + 0.0972032*exp(-1.44*(-(0.0821361*Abs(1.95*x_1 - 3.4) + 1.14687*asin(0.0499997*x_5 - 0.5) + 0.786116 - 0.737058*exp(-18.9225*(0.781609 - x_2)**2))*(-0.0166462*Abs(2.65*x_1 - 4.8) + 0.0900703*Abs(4.2*x_2 - 4.65) - 0.0204534*Abs(3.35*x_4 - 4.45) + 1.33612*acos(0.0499997*x_5 - 0.5) - 2.61124) - 0.5)**2)`
- icbr_no_shared formula (display, rounded):
  - `0.24844*sin(0.0579399*Abs(3.0*x_1 - 4.05) + 0.0176539*Abs(2.45*x_2 - 4.35) - 2.79825*acos(0.0499997*x_5 - 0.5) + 10.7233 - 0.185419*exp(-2.4025*(1 - 0.483871*x_3)**2)) - 0.0404104*Abs(-0.247708*sin(0.5*x_3 - 5.0) + 0.243874*Abs(2.25*x_1 - 3.35) - 0.0826969*Abs(3.3*x_4 - 4.35) + 25.4823*asin(0.0499997*x_5 - 0.5) + 0.118281*sign(3.2*x_2 - 3.75) + 8.28572) + 0.0001526*sign(0.257826*cos(1.4*x_1 - 3.2) - 0.0503119) + 0.352908 - 0.201609*exp(-2.52582*(-0.209584*cos(0.5*x_3 - 0.0499997) - atanh(0.0499997*x_5 - 0.4) - 0.558133 + 0.00517923*exp(-25.0*(1 - 0.93*x_1)**2))**2) + 0.0972032*exp(-1.44*(-(0.0821361*Abs(1.95*x_1 - 3.4) + 1.15497*atanh(0.0499997*x_5 - 0.4) + 0.671772 + 0.00190247/(0.642857 - x_2)**5)*(38.7726*sqrt(0.02*x_2 + 1) - 0.0166462*Abs(2.65*x_1 - 4.8) - 1.33612*asin(0.0499997*x_5 - 0.5) - 39.7541 + 0.0393791*exp(-13.69*(1 - 0.743243*x_4)**2)) - 0.5)**2)`
- icbr_refit_commit formula (display, rounded):
  - `-0.251951*cos(0.0569176*Abs(2.93972*x_1 - 3.75008) + 0.0302014*Abs(1.42232*x_2 - 2.6406) + 9.62069*acos(0.62652 - 0.01216*x_5) - 8.37385 - 0.193818*exp(-1.6384*(1 - 0.477187*x_3)**2)) + 0.000443936*Abs(0.326362*sin(1.40004*x_1 + 1.51228) - 2.24012) - 0.0429648*Abs(-0.230267*sin(0.5*x_3 - 4.99928) + 0.1411*Abs(3.47892*x_1 - 4.77144) + 74.1657*asin(0.014*x_5 - 0.60052) - 0.0374172*sign(0.9158*x_2 - 3.15192) + 43.3522 + 0.159588*exp(-9.72841*(0.751154*x_4 - 1)**2)) + 0.3593 - 0.215393*exp(-116.369*(0.0285576*cos(0.5004*x_3 - 3.21372) - atanh(0.0042*x_5 - 0.65148) + 0.000259607*sign(4.99954 - 3.89*x_1) - 0.800939)**2) + 0.109827*exp(-0.981447*(-(0.0607549*Abs(2.6444*x_1 - 4.77784) + 0.665646*atanh(0.0859999*x_5 - 0.6) + 0.61798 + 0.00190714/(0.642667 - x_2)**5)*(39.6586*sqrt(0.0195407*x_2 + 1) - 0.0214305*Abs(2.09152*x_1 - 3.98524) - 0.0195862*Abs(3.5268*x_4 - 4.73452) + 0.861691*acos(0.0780399*x_5 - 0.60224) - 41.7996) - 0.62664)**2)`

### task=feynman_II_21_32 seed=3

- Task source: feynman_file
- Target formula: `q/(4*pi*epsilon*r*(1-v/c))`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=2.384550e-03, r2=-0.001780
- Variant formula overview:
  - icbr_full: symbolic_s=3.213985e-01, imitation_mse=4.135581e-17, target_mse=2.384550e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=2.734382e-01, imitation_mse=4.135581e-17, target_mse=2.384550e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=3.153601e-01, imitation_mse=4.135581e-17, target_mse=2.384550e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=5.365619e-01, imitation_mse=8.308632e-17, target_mse=2.384550e-03, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0.0524218 - 1.63667e-6/(1 - 0.0255585*x_1)**4`
- icbr_no_replay formula (display, rounded):
  - `0.0524218 - 1.63667e-6/(1 - 0.0255585*x_1)**4`
- icbr_no_shared formula (display, rounded):
  - `0.0524218 - 1.63667e-6/(1 - 0.0255585*x_1)**4`
- icbr_refit_commit formula (display, rounded):
  - `0.0524241 - 3.91939e-6/(0.0130946*x_1 - 1)**4`

### task=feynman_II_21_32 seed=4

- Task source: feynman_file
- Target formula: `q/(4*pi*epsilon*r*(1-v/c))`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=2.135467e-03, r2=0.000713
- Variant formula overview:
  - icbr_full: symbolic_s=9.902772e-01, imitation_mse=2.209316e-09, target_mse=2.135136e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=6.937357e-01, imitation_mse=3.533407e-09, target_mse=2.135185e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.273694e+00, imitation_mse=2.209316e-09, target_mse=2.135136e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.670091e+00, imitation_mse=2.072374e-09, target_mse=2.135136e-03, formula_export_success=True
- icbr_full formula (display, rounded):
  - `7.45934e-8*tan(0.0623858*(-0.01*x_5 - 1)**2 + 1.48768) - 0.000186849*atan(0.657715*tanh(4.65*x_3 - 5.0) + 8.28661*asin(0.0499997*x_5 - 0.5) + 0.318383) + 0.0513064 - 9.03335e-6/(0.295328*acos(0.0999997*x_5 - 0.75) - 1)**5`
- icbr_no_replay formula (display, rounded):
  - `7.45934e-8*tan(0.00132849*x_5 + 1.54983) + 0.000141187*tan(-5.30343*asin(0.0499997*x_5 - 0.5) + 0.236658*sign(3.35 - 2.85*x_3) + 2.2634) + 0.0514011 - 0.000203996/(-0.550883*asin(0.0999997*x_5 - 0.75) - 1)**5`
- icbr_no_shared formula (display, rounded):
  - `7.45934e-8*tan(0.0623858*(0.01*x_5 + 1)**2 + 1.48768) - 0.000186849*atan(0.657715*tanh(4.65*x_3 - 5.0) + 8.28661*asin(0.0499997*x_5 - 0.5) + 0.318383) + 0.0513064 - 9.03335e-6/(0.295328*acos(0.0999997*x_5 - 0.75) - 1)**5`
- icbr_refit_commit formula (display, rounded):
  - `2.82054e-8*tan(0.0197139*(-0.0200001*x_5 - 1)**2 + 4.68067) - 0.000184087*atan(0.673793*tanh(4.58*x_3 - 4.89976) + 5.34787*asin(0.0779999*x_5 - 0.60136) - 0.601199) + 0.0513112 - 0.00120556/(0.13423 - acos(0.60016 - 0.0779999*x_5))**5`

### task=feynman_II_21_32 seed=5

- Task source: feynman_file
- Target formula: `q/(4*pi*epsilon*r*(1-v/c))`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=8.132804e-04, r2=0.668205
- Variant formula overview:
  - icbr_full: symbolic_s=4.458530e+00, imitation_mse=1.836436e-04, target_mse=7.758312e-04, formula_export_success=True
  - icbr_no_replay: symbolic_s=2.636768e+00, imitation_mse=1.863229e-04, target_mse=7.793483e-04, formula_export_success=True
  - icbr_no_shared: symbolic_s=6.465584e+00, imitation_mse=1.836436e-04, target_mse=7.758312e-04, formula_export_success=True
  - icbr_refit_commit: symbolic_s=7.546049e+00, imitation_mse=1.993197e-04, target_mse=7.726257e-04, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0.0736024*sin(0.385692*cos(0.7*x_2 - 3.95) + 0.0553357*Abs(2.85*x_1 - 4.75) + 1.65664) - 0.0938718*atan(0.667477*tan(0.3*x_2 - 1.0) - 0.129008*Abs(2.85*x_1 - 3.75) - 0.450882*acos(0.35*x_3 - 1.2) + 5.19615*atanh(0.0499997*x_5 - 0.4) + 1.10177 + 0.0474798*exp(-12.96*(1 - 0.75*x_4)**2)) + 0.366774*atan(0.038836*Abs(3.4*x_1 - 4.35) + 0.492273*acos(0.35*x_2 - 1.2) - 0.427296*asin(0.3*x_3 - 1.05) - 1.9173*atanh(0.0499997*x_5 - 0.4) - 1.18837 + 0.36867*exp(-1.8225*(1 - 0.925926*x_4)**2)) + 0.481344 - 0.816289*exp(-0.0625*(-(0.0516809*Abs(3.2*x_1 - 3.75) - 0.0604285*Abs(2.7*x_2 - 3.15) - 1.67447*asin(0.0499997*x_5 - 0.5) - 1.34096 + 0.278999*exp(-1.44*(1 - 0.958333*x_4)**2))*(0.24871*cos(0.35*x_1 + 0.5) - 0.0215916*Abs(2.65*x_2 - 3.75) - 0.0636794*Abs(4.5*x_3 - 4.975) - 2.65483*asin(0.0499997*x_5 - 0.5) - 2.17394 + 0.139047*exp(-7.0225*(1 - 0.792453*x_4)**2)) + 0.2)**2) + 2.35994e-6/(-0.01284*(0.01*x_5 + 1)**3 + 0.595697*sin(1.2*x_3 - 0.9) + 1)**3 - 3.79928e-10/(atanh(0.0499997*x_5 - 0.4) + 0.290423)**5 - 1.17506e-5/(-(-1.61643*asin(0.0499997*x_5 - 0.5) - 0.810982)*(0.0220919*Abs(1.8*x_2 - 3.5) + 2.90572*asin(0.0499997*x_5 - 0.5) + 1.51265) + 0.0333331)**3`
- icbr_no_replay formula (display, rounded):
  - `-0.0505035*cos(0.0671934*Abs(2.85*x_1 - 4.75) + 0.0905063*Abs(3.15*x_2 - 4.8) + 2.71992) + 0.433504*tanh(0.032704*Abs(3.4*x_1 - 4.35) + 0.414546*acos(0.35*x_2 - 1.2) + 1.60315*acos(0.0499997*x_5 - 0.5) - 0.359828*asin(0.3*x_3 - 1.05) - 3.62989 + 0.310459*exp(-1.8225*(1 - 0.925926*x_4)**2)) + 0.0938718*atan(0.129008*Abs(2.85*x_1 - 3.75) + 0.025133*Abs(3.25*x_4 - 4.3) + 0.690968*acos(0.3*x_2 - 1.05) + 5.15941*acos(0.0499997*x_5 - 0.5) - 0.450882*asin(0.35*x_3 - 1.2) - 10.1875) + 0.483872 - 0.816289*exp(-0.0625*(-(0.0516809*Abs(3.2*x_1 - 3.75) - 0.0604285*Abs(2.7*x_2 - 3.15) - 1.67447*asin(0.0499997*x_5 - 0.5) - 1.34096 + 0.278999*exp(-1.44*(1 - 0.958333*x_4)**2))*(-0.0232175*Abs(3.6*x_1 - 4.15) - 0.0215916*Abs(2.65*x_2 - 3.75) - 0.0636794*Abs(4.5*x_3 - 4.975) - 0.0512895*Abs(3.9*x_4 - 4.9) + 2.65483*acos(0.0499997*x_5 - 0.5) - 6.0321) + 0.2)**2) + 1.32018e-6/(-0.000360138*x_5 + 0.364242 + exp(-2.25*(1 - 0.5*x_3)**2))**3 - 3.44508e-6/(-(-1.62794*atanh(0.0499997*x_5 - 0.4) - 0.648723)*(2.90572*asin(0.0499997*x_5 - 0.5) + 1.61526 - 0.10069*exp(-2.4025*(1 - 0.483871*x_2)**2)) + 0.133333)**5 - 1.34825e-11/(1 - 0.509251*acos(0.0499997*x_5 - 0.5))**5`
- icbr_no_shared formula (display, rounded):
  - `0.0736024*sin(0.385692*cos(0.7*x_2 - 3.95) + 0.0553357*Abs(2.85*x_1 - 4.75) + 1.65664) - 0.0938718*atan(0.667477*tan(0.3*x_2 - 1.0) - 0.129008*Abs(2.85*x_1 - 3.75) - 0.450882*acos(0.35*x_3 - 1.2) + 5.19615*atanh(0.0499997*x_5 - 0.4) + 1.10177 + 0.0474798*exp(-12.96*(1 - 0.75*x_4)**2)) + 0.366774*atan(0.038836*Abs(3.4*x_1 - 4.35) + 0.492273*acos(0.35*x_2 - 1.2) - 0.427296*asin(0.3*x_3 - 1.05) - 1.9173*atanh(0.0499997*x_5 - 0.4) - 1.18837 + 0.36867*exp(-1.8225*(1 - 0.925926*x_4)**2)) + 0.481344 - 0.816289*exp(-0.0625*(-(0.0516809*Abs(3.2*x_1 - 3.75) - 0.0604285*Abs(2.7*x_2 - 3.15) - 1.67447*asin(0.0499997*x_5 - 0.5) - 1.34096 + 0.278999*exp(-1.44*(1 - 0.958333*x_4)**2))*(0.24871*cos(0.35*x_1 + 0.5) - 0.0215916*Abs(2.65*x_2 - 3.75) - 0.0636794*Abs(4.5*x_3 - 4.975) - 2.65483*asin(0.0499997*x_5 - 0.5) - 2.17394 + 0.139047*exp(-7.0225*(1 - 0.792453*x_4)**2)) + 0.2)**2) + 2.35994e-6/(-0.01284*(0.01*x_5 + 1)**3 + 0.595697*sin(1.2*x_3 - 0.9) + 1)**3 - 3.79928e-10/(atanh(0.0499997*x_5 - 0.4) + 0.290423)**5 - 1.17506e-5/(-(-1.61643*asin(0.0499997*x_5 - 0.5) - 0.810982)*(0.0220919*Abs(1.8*x_2 - 3.5) + 2.90572*asin(0.0499997*x_5 - 0.5) + 1.51265) + 0.0333331)**3`
- icbr_refit_commit formula (display, rounded):
  - `0.068363*sin(0.411164*cos(0.66808*x_2 - 0.70296) - 0.0894562*Abs(1.84492*x_1 - 3.20324) + 1.47472) - 0.103512*atan(0.611188*tan(0.30072*x_2 - 1.002) - 0.104201*Abs(3.18192*x_1 - 3.87804) + 0.37514*acos(1.27508 - 0.38204*x_3) + 35.2886*atanh(0.00432*x_5 - 0.63504) + 24.1481 + 0.0472385*exp(-9.78088*(1 - 0.749201*x_4)**2)) + 0.373063*atan(0.0316217*Abs(4.08464*x_1 - 4.79728) - 0.341769*acos(1.2186 - 0.36512*x_3) + 0.443351*acos(0.38188*x_2 - 1.27488) - 10.4854*atanh(0.00631999*x_5 - 0.6002) - 7.01119 + 0.384823*exp(-1.57784*(1 - 0.939719*x_4)**2)) + 0.41416 - 0.765809*exp(-0.0693795*(-(0.502417*sin(0.342*x_1 - 1.09888) - 0.0503678*Abs(3.21548*x_2 - 3.42116) - 1.08075*asin(0.0779999*x_5 - 0.6004) - 0.807292 + 0.29228*exp(-1.21*(1 - 0.983636*x_4)**2))*(-0.0208075*Abs(3.98944*x_1 - 4.29612) - 0.0150904*Abs(3.702*x_2 - 4.99908) - 0.0912491*Abs(3.13232*x_3 - 3.3364) - 1.71351*asin(0.0779999*x_5 - 0.60032) - 1.70518 + 0.15048*exp(-5.59966*(1 - 0.794435*x_4)**2)) + 0.208504)**2) + 1.68749e-5/(0.00530027*(-0.0104016*x_5 - 1)**3 - 0.263871*Abs(0.82476*x_3 - 1.65576) + 1)**3 - 2.30871e-14/(atanh(0.00424*x_5 - 0.65452) + 0.766359)**5 - 1.17122e-5/(-(1.07311 - 1.10625*acos(0.60116 - 0.0733599*x_5))*(0.0220658*Abs(1.86992*x_2 - 3.838) + 1.81303*asin(0.0806799*x_5 - 0.61268) + 1.16143) + 0.0331485)**3`

### task=feynman_II_21_32 seed=6

- Task source: feynman_file
- Target formula: `q/(4*pi*epsilon*r*(1-v/c))`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=5.235733e-03, r2=-1.204739
- Variant formula overview:
  - icbr_full: symbolic_s=6.389200e-03, imitation_mse=0.000000e+00, target_mse=5.235733e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=6.193300e-03, imitation_mse=0.000000e+00, target_mse=5.235733e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=4.608700e-03, imitation_mse=0.000000e+00, target_mse=5.235733e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=5.306700e-03, imitation_mse=0.000000e+00, target_mse=5.235733e-03, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0`
- icbr_no_replay formula (display, rounded):
  - `0`
- icbr_no_shared formula (display, rounded):
  - `0`
- icbr_refit_commit formula (display, rounded):
  - `0`

### task=feynman_II_21_32 seed=7

- Task source: feynman_file
- Target formula: `q/(4*pi*epsilon*r*(1-v/c))`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.722905e-03, r2=0.082550
- Variant formula overview:
  - icbr_full: symbolic_s=3.562629e+00, imitation_mse=2.115646e-04, target_mse=1.815683e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=2.246965e+00, imitation_mse=2.022355e-04, target_mse=1.852756e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=5.183385e+00, imitation_mse=2.115853e-04, target_mse=1.815730e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=6.391187e+00, imitation_mse=3.750165e-04, target_mse=1.607012e-03, formula_export_success=True
- icbr_full formula (display, rounded):
  - `-0.000658554*exp(1.77674*atanh(0.0499997*x_5 - 0.4)) + 0.0660037*sin(0.0764911*Abs(2.7*x_2 - 4.8) - 7.37648*asin(0.0499997*x_5 - 0.5) - 3.12056 + 1.45325e-5/(1 - 0.887755*x_3)**2) + 0.0876442*Abs(1.0*(0.0878185*Abs(3.9*x_1 - 4.8) + 0.0949377*Abs(2.6*x_2 - 3.65) + 0.0908688*Abs(3.9*x_3 - 4.875) - 3.77865*atanh(0.0499997*x_5 - 0.4) - 0.627991)*(0.00301756*tanh(4.05*x_1 - 5.0) - 0.0160998*Abs(2.3*x_2 - 4.525) + 0.122635*Abs(2.2*x_3 - 3.55) + 7.0481*asin(0.0499997*x_5 - 0.5) + 4.03083 - 0.0840838*exp(-12.96*(1 - 0.75*x_4)**2)) + 0.95) + 2.74431*acos(0.0499997*(6.74861*sqrt(0.0510204*x_1 + 1) - 0.706444*cos(0.35*x_2 + 0.5) + 0.0227124*Abs(2.4*x_3 - 3.3) + 3.94089*asin(0.0499997*x_5 - 0.5) - 4.14516)*(-0.833875*sin(0.45*x_3 + 1.7) + 0.0757917*Abs(3.7*x_1 - 4.575) + 0.681522*atanh(0.0499997*x_5 - 0.4) + 1.99513 - 0.177037*exp(-16.4025*(1 - 0.740741*x_4)**2)) - 0.55) - 7.32373 + 3.03101*exp(-0.4346*(0.012727*Abs(3.65*x_1 - 4.15) - acos(0.0499997*x_5 - 0.5) + 0.66829 + 1.97569e-11/(0.972376 - x_4)**5)**2)`
- icbr_no_replay formula (display, rounded):
  - `0.0660037*sin(0.0764911*Abs(2.7*x_2 - 4.8) + 7.37648*acos(0.0499997*x_5 - 0.5) - 14.7075 + 1.45325e-5/(1 - 0.887755*x_3)**2) + 0.0876442*Abs(1.0*(0.0878185*Abs(3.9*x_1 - 4.8) + 0.0949377*Abs(2.6*x_2 - 3.65) + 0.0908688*Abs(3.9*x_3 - 4.875) - 3.75191*asin(0.0499997*x_5 - 0.5) - 1.00464)*(0.122635*Abs(2.2*x_3 - 3.55) + 0.0432144*Abs(3.3*x_4 - 4.35) - 7.0481*acos(0.0499997*x_5 - 0.5) - 0.0028614*sign(3.45 - 2.85*x_1) + 14.9189 + 0.0912213*exp(-2.4025*(1 - 0.483871*x_2)**2)) + 0.95) - 2.74431*asin(0.0499997*(-2.85066*(1 - 0.04*x_1)**(3/2) + 0.0558115*Abs(4.25*x_2 - 4.8) + 0.0227124*Abs(2.4*x_3 - 3.3) - 3.94089*acos(0.0499997*x_5 - 0.5) + 11.187)*(0.0757917*Abs(3.7*x_1 - 4.575) + 0.102566*Abs(3.45*x_3 - 4.4) - 0.6767*acos(0.0499997*x_5 - 0.5) + 2.44346 - 0.177037*exp(-16.4025*(1 - 0.740741*x_4)**2)) - 0.55) - 3.01298 - 0.0125603*exp(-1.76417*acos(0.0499997*x_5 - 0.5)) + 3.03101*exp(-0.4346*(0.012727*Abs(3.65*x_1 - 4.15) - acos(0.0499997*x_5 - 0.5) + 0.66829 + 1.97569e-11/(0.972376 - x_4)**5)**2)`
- icbr_no_shared formula (display, rounded):
  - `-0.000658554*exp(1.77674*atanh(0.0499997*x_5 - 0.4)) + 0.0660037*sin(0.0764911*Abs(2.7*x_2 - 4.8) - 7.37648*asin(0.0499997*x_5 - 0.5) - 3.12056 + 1.45325e-5/(1 - 0.887755*x_3)**2) + 0.0876442*Abs(1.0*(0.0878185*Abs(3.9*x_1 - 4.8) + 0.0949377*Abs(2.6*x_2 - 3.65) + 0.0908688*Abs(3.9*x_3 - 4.875) - 3.77865*atanh(0.0499997*x_5 - 0.4) - 0.627991)*(0.00301756*tanh(4.05*x_1 - 5.0) - 0.024678*Abs(1.5*x_2 - 2.95) + 0.122635*Abs(2.2*x_3 - 3.55) + 7.0481*asin(0.0499997*x_5 - 0.5) + 4.03083 - 0.0840838*exp(-12.96*(1 - 0.75*x_4)**2)) + 0.95) + 2.74431*acos(0.0499997*(6.84518*sqrt(0.0502513*x_1 + 1) - 0.706444*cos(0.35*x_2 + 0.5) + 0.0227124*Abs(2.4*x_3 - 3.3) + 3.94089*asin(0.0499997*x_5 - 0.5) - 4.24153)*(-0.833875*sin(0.45*x_3 + 1.7) + 0.0757917*Abs(3.7*x_1 - 4.575) + 0.681522*atanh(0.0499997*x_5 - 0.4) + 1.99513 - 0.177037*exp(-16.4025*(1 - 0.740741*x_4)**2)) - 0.55) - 7.32373 + 3.03101*exp(-0.4346*(0.012727*Abs(3.65*x_1 - 4.15) - acos(0.0499997*x_5 - 0.5) + 0.66829 - 1.97569e-11/(x_4 - 0.972376)**5)**2)`
- icbr_refit_commit formula (display, rounded):
  - `-0.206463*exp(9.18006*atanh(0.00663999*x_5 - 0.6082)) - 0.0436744*sin(0.192409*Abs(1.4092*x_2 - 2.62352) + 6.20839*acos(0.0775199*x_5 - 0.60212) - 9.10438 + 0.0082746/(0.626269 - x_3)**2) + 0.0377647*Abs(2.27896*(0.0892179*Abs(3.78892*x_1 - 4.1968) + 0.0679589*Abs(3.55164*x_2 - 4.75732) + 0.108634*Abs(3.21188*x_3 - 3.61032) - 21.8008*atanh(0.00599999*x_5 - 0.60076) - 14.2624)*(0.00305166*tanh(3.98*x_1 - 4.9) - 0.0232087*Abs(1.64012*x_2 - 3.38432) + 0.140248*Abs(1.89932*x_3 - 3.09768) + 0.0437321*Abs(3.30164*x_4 - 4.39792) + 4.5121*acos(0.6034 - 0.0786399*x_5) - 3.96283) + 4.62308) - 1.63918*acos(-0.0839999*(6.75473*sqrt(0.050971*x_1 + 1) + 0.736864*sin(0.334*x_2 - 0.99906) + 0.0203557*Abs(2.62616*x_3 - 3.43416) + 30.2722*atanh(0.00408*x_5 - 0.64684) + 17.1016)*(0.733318*cos(0.40268*x_1 + 3.40508) - 0.858211*cos(0.434*x_3 + 0.20012) + 0.402169*atanh(0.0839999*x_5 - 0.6) + 2.54398 - 0.199223*exp(-11.0195*(1 - 0.735447*x_4)**2)) + 0.7) - 0.627097 + 3.76885*exp(-0.460571*(-0.0078132*Abs(4.59888*x_1 - 4.89556) - 0.501565*asin(0.0779999*x_5 - 0.60088) + 1 - 1.46378e-11/(0.972599 - x_4)**5)**2)`

### task=feynman_II_21_32 seed=8

- Task source: feynman_file
- Target formula: `q/(4*pi*epsilon*r*(1-v/c))`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=2.475399e-03, r2=-0.000443
- Variant formula overview:
  - icbr_full: symbolic_s=1.091965e+00, imitation_mse=3.162406e-09, target_mse=2.475600e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=7.389437e-01, imitation_mse=3.132861e-09, target_mse=2.475617e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.390908e+00, imitation_mse=3.162248e-09, target_mse=2.475600e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.824517e+00, imitation_mse=3.177697e-09, target_mse=2.475210e-03, formula_export_success=True
- icbr_full formula (display, rounded):
  - `-0.000410306*exp(0.169422*sign(3.9 - 3.3*x_1)) + 0.0560348 + 0.000273438*exp(-1.13084*(-0.0219659*(-0.01*x_5 - 1)**3 + 0.445075*sign(3.85 - 3.3*x_2) + 1 - 0.502741*exp(-12.6025*(1 - 0.746479*x_4)**2) - 0.812526*exp(-25.0*(0.88 - x_3)**2))**2)`
- icbr_no_replay formula (display, rounded):
  - `0.0560914 + 0.000273438*exp(-0.746578*(0.000920887*x_5 + 0.348542*Abs(2.95*x_4 - 3.9) + 0.547767*sign(3.85 - 3.3*x_2) + 0.598159 - exp(-25.0*(0.88 - x_3)**2))**2) - 0.000465937/(1 - 0.0370197*sign(3.9 - 3.3*x_1))**4`
- icbr_no_shared formula (display, rounded):
  - `-0.000408092*exp(0.1703*sign(3.9 - 3.3*x_1)) + 0.0560327 + 0.000273438*exp(-1.13084*(-0.0219659*(-0.01*x_5 - 1)**3 + 0.445075*sign(3.85 - 3.3*x_2) + 1 - 0.812526*exp(-25.0*(x_3 - 0.88)**2) - 0.502741*exp(-12.6025*(1 - 0.746479*x_4)**2))**2)`
- icbr_refit_commit formula (display, rounded):
  - `-0.000374052*exp(0.1155*sign(4.89994 - 3.986*x_1)) + 0.0561028 + 0.000225993*exp(-13.2926*(-0.00284115*(-0.0200018*x_5 - 1)**3 + 0.115737*sign(4.79826 - 4.198*x_2) + 0.363277 - 0.154593*exp(-10.1598*(1 - 0.747848*x_4)**2) - exp(-12.4045*(0.624662 - x_3)**2))**2)`

### task=feynman_II_21_32 seed=9

- Task source: feynman_file
- Target formula: `q/(4*pi*epsilon*r*(1-v/c))`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=2.159873e-03, r2=-0.003155
- Variant formula overview:
  - icbr_full: symbolic_s=1.426632e+00, imitation_mse=9.523992e-06, target_mse=2.157943e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=1.062177e+00, imitation_mse=9.535358e-06, target_mse=2.157949e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.933673e+00, imitation_mse=9.523992e-06, target_mse=2.157943e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=2.524450e+00, imitation_mse=1.032918e-05, target_mse=2.153960e-03, formula_export_success=True
- icbr_full formula (display, rounded):
  - `-0.00459152*sign(-0.00901082*Abs(2.25*x_3 - 4.525) - 7.54693*asin(0.0499997*x_5 - 0.5) - 2.70203 + 0.178054*exp(-2.56*(1 - 0.46875*x_1)**2)) + 0.0468445 - 7.2127e-12/(-(-0.0234415*(0.01*x_5 + 1)**2 - 0.00752039*sign(3.3 - 2.75*x_1) + 0.0139133)*(-0.00362944*sign(2.9 - 2.75*x_3) + 0.053941*sign(3.45 - 2.9*x_1) + 0.0775396) + 0.01)**3 - 3.45337e-5/(1 - 0.000769149*tan(0.35*x_2 - 1.95))**5`
- icbr_no_replay formula (display, rounded):
  - `-0.00459152*sign(-7.59097*tan(0.05*x_5 - 3.55) - 2.05801 + 0.0490139*exp(-2.89*(1 - 0.470588*x_3)**2) + 0.178054*exp(-2.56*(1 - 0.46875*x_1)**2)) + 0.0468438 - 2.723e-5/(0.0492829*sign(3.5 - 2.9*x_2) + 1)**5 - 9.34209e-14/((-0.00049917*x_5 - 0.00752039*sign(3.3 - 2.75*x_1) - 0.00943945)*(0.053941*sign(3.45 - 2.9*x_1) + 0.0808525 - 0.000363379/(4.15 - 3.75*x_3)) - 0.010929)**4`
- icbr_no_shared formula (display, rounded):
  - `-0.00459152*sign(-0.00901082*Abs(2.25*x_3 - 4.525) - 7.54693*asin(0.0499997*x_5 - 0.5) - 2.70203 + 0.178054*exp(-2.56*(1 - 0.46875*x_1)**2)) + 0.0468445 - 7.2127e-12/(-(-0.0234415*(-0.01*x_5 - 1)**2 - 0.00752039*sign(3.3 - 2.75*x_1) + 0.0139133)*(-0.00362944*sign(2.9 - 2.75*x_3) + 0.053941*sign(3.45 - 2.9*x_1) + 0.0775396) + 0.01)**3 - 3.45337e-5/(1 - 0.000769149*tan(0.35*x_2 - 1.95))**5`
- icbr_refit_commit formula (display, rounded):
  - `-0.0026474*sign(-0.0160373*Abs(1.51512*x_3 - 3.1278) - 6.09481*asin(0.0739999*x_5 - 0.6004) - 2.41339 + 0.226499*exp(-1.69094*(1 - 0.467809*x_1)**2)) + 0.0486672 + 3.1873e-5/(0.00170645*tan(0.72624*x_2 + 0.784) - 1)**5 - 2.90558e-14/(-(-0.0110483*(-0.0200017*x_5 - 1)**2 - 0.00493272*sign(4.89828 - 3.79*x_1) + 0.00398132)*(-0.00362944*sign(3.89894 - 3.698*x_3) + 0.0408088*sign(4.79802 - 3.89*x_1) + 0.0651727) + 0.0200013)**5`

### task=feynman_II_21_32 seed=10

- Task source: feynman_file
- Target formula: `q/(4*pi*epsilon*r*(1-v/c))`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=2.284898e-03, r2=-0.027954
- Variant formula overview:
  - icbr_full: symbolic_s=7.038971e-01, imitation_mse=1.176797e-06, target_mse=2.281094e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=5.507126e-01, imitation_mse=1.175651e-06, target_mse=2.281103e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=9.050022e-01, imitation_mse=1.176797e-06, target_mse=2.281094e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.421284e+00, imitation_mse=1.261530e-06, target_mse=2.279920e-03, formula_export_success=True
- icbr_full formula (display, rounded):
  - `-17.3976*(-atanh(0.0499997*x_5 - 0.4) - 0.0278509*sign(3.95 - 3.45*x_3) - 0.0742015)**5 + 0.0462899 + 5.74381e-9/(-atanh(0.0499997*x_5 - 0.4) - 0.337295)**5`
- icbr_no_replay formula (display, rounded):
  - `-16.7995*(-asin(0.0499997*x_5 - 0.5) - 0.0280465*sign(3.95 - 3.45*x_3) - 0.175118)**5 + 0.0462899 + 5.94829e-9/(-asin(0.0499997*x_5 - 0.5) - 0.440059)**5`
- icbr_no_shared formula (display, rounded):
  - `-17.3976*(-atanh(0.0499997*x_5 - 0.4) - 0.0278509*sign(3.95 - 3.45*x_3) - 0.0742015)**5 + 0.0462899 + 5.74381e-9/(-atanh(0.0499997*x_5 - 0.4) - 0.337295)**5`
- icbr_refit_commit formula (display, rounded):
  - `-36678.7*(-atanh(0.00643999*x_5 - 0.60208) - 0.00430279*sign(4.9222 - 4.3*x_3) - 0.626666)**5 + 0.0464161 + 6.73509e-8/(-atanh(0.0839999*x_5 - 0.60008) - 0.494091)**5`

### task=feynman_II_21_32 seed=11

- Task source: feynman_file
- Target formula: `q/(4*pi*epsilon*r*(1-v/c))`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=4.712855e-03, r2=-1.276523
- Variant formula overview:
  - icbr_full: symbolic_s=4.491534e-01, imitation_mse=1.089830e-04, target_mse=4.618037e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=3.616818e-01, imitation_mse=1.089830e-04, target_mse=4.618037e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=4.756879e-01, imitation_mse=1.089830e-04, target_mse=4.618037e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=7.112741e-01, imitation_mse=1.134328e-04, target_mse=4.592629e-03, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0.0434579 - 0.0360951*Abs(0.521415*Abs(2.25*x_1 - 3.65) - 2.43293 + 0.152699*exp(-3.4225*(1 - 0.459459*x_2)**2))`
- icbr_no_replay formula (display, rounded):
  - `0.0434579 - 0.0360951*Abs(0.521415*Abs(2.25*x_1 - 3.65) - 2.43293 + 0.152699*exp(-3.4225*(1 - 0.459459*x_2)**2))`
- icbr_no_shared formula (display, rounded):
  - `0.0434579 - 0.0360951*Abs(0.521415*Abs(2.25*x_1 - 3.65) - 2.43293 + 0.152699*exp(-3.4225*(1 - 0.459459*x_2)**2))`
- icbr_refit_commit formula (display, rounded):
  - `0.042662 - 0.0555014*Abs(0.27343*Abs(2.74384*x_1 - 4.5652) - 1.56528 + 0.0997131*exp(-2.89*(1 - 0.448235*x_2)**2))`

### task=feynman_II_21_32 seed=12

- Task source: feynman_file
- Target formula: `q/(4*pi*epsilon*r*(1-v/c))`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=2.257648e-03, r2=-0.000939
- Variant formula overview:
  - icbr_full: symbolic_s=6.328412e-01, imitation_mse=6.348505e-08, target_mse=2.257725e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=4.502209e-01, imitation_mse=6.350512e-08, target_mse=2.257725e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=6.995862e-01, imitation_mse=6.348505e-08, target_mse=2.257725e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.061722e+00, imitation_mse=6.454376e-08, target_mse=2.257638e-03, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0.0532806 - 4.11381e-11/(tan(0.05*x_5 - 3.55) + 0.291756)**5 + 2.99577e-9/(-tan(0.05*x_5 - 3.55) - 0.407424)**4`
- icbr_no_replay formula (display, rounded):
  - `0.0532808 - 1.51897e-8/(-asin(0.0999997*x_5 - 0.75) - 0.751594)**5 - 4.11381e-11/(tan(0.05*x_5 - 3.55) + 0.291756)**5`
- icbr_no_shared formula (display, rounded):
  - `0.0532806 - 4.11381e-11/(tan(0.05*x_5 - 3.55) + 0.291756)**5 + 2.99577e-9/(-tan(0.05*x_5 - 3.55) - 0.407424)**4`
- icbr_refit_commit formula (display, rounded):
  - `0.0532796 + 3.66997e-9/(-tan(0.0839999*x_5 - 0.60012) - 0.505283)**4 - 2.69516e-14/(tan(0.00855999*x_5 - 0.60408) + 0.659328)**5`

### task=feynman_II_21_32 seed=13

- Task source: feynman_file
- Target formula: `q/(4*pi*epsilon*r*(1-v/c))`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=6.905866e-04, r2=0.637997
- Variant formula overview:
  - icbr_full: symbolic_s=1.241026e+00, imitation_mse=6.111238e-05, target_mse=6.752167e-04, formula_export_success=True
  - icbr_no_replay: symbolic_s=9.268294e-01, imitation_mse=6.395550e-05, target_mse=6.675911e-04, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.691303e+00, imitation_mse=6.111350e-05, target_mse=6.752626e-04, formula_export_success=True
  - icbr_refit_commit: symbolic_s=2.269024e+00, imitation_mse=6.334241e-05, target_mse=6.596615e-04, formula_export_success=True
- icbr_full formula (display, rounded):
  - `-0.565227*sin(0.00919203*Abs(3.0*x_1 - 3.55) + 0.00854454*Abs(2.2*x_2 - 4.25) + 0.00740514*Abs(2.75*x_4 - 3.65) + 2.03401*atanh(0.0499997*x_5 - 0.4) + 3.12874) - 0.326028*tan(0.0168032*Abs(3.5*x_2 - 5.0) + 3.14464*asin(0.0499997*x_5 - 0.5) + 0.0480525*atanh(0.4*x_3 - 1.4) + 0.00115571*sign(4.975 - 4.9*x_4) + 3.46433) + 0.0366986`
- icbr_no_replay formula (display, rounded):
  - `-0.565227*sin(0.00919203*Abs(3.0*x_1 - 3.55) + 0.00740514*Abs(2.75*x_4 - 3.65) - 2.01981*acos(0.0499997*x_5 - 0.5) + 6.55226 - 0.0464624*exp(-2.4025*(1 - 0.483871*x_2)**2)) - 0.352359*atanh(0.0236711*tan(0.6*x_3 + 4.3) + 0.015603*Abs(3.5*x_2 - 5.0) + 2.92002*asin(0.0499997*x_5 - 0.5) + 0.00107316*sign(4.975 - 4.9*x_4) + 0.288236) + 0.0337829`
- icbr_no_shared formula (display, rounded):
  - `-0.565227*sin(0.00919203*Abs(3.0*x_1 - 3.55) + 0.00737037*Abs(2.55*x_2 - 4.925) + 0.00740514*Abs(2.75*x_4 - 3.65) + 2.03401*atanh(0.0499997*x_5 - 0.4) + 3.12874) - 0.326028*tan(0.0168032*Abs(3.5*x_2 - 5.0) + 3.14464*asin(0.0499997*x_5 - 0.5) + 0.0480525*atanh(0.4*x_3 - 1.4) + 0.00115571*sign(4.975 - 4.9*x_4) + 3.46433) + 0.0366986`
- icbr_refit_commit formula (display, rounded):
  - `0.582265*sin(0.00776081*Abs(3.42848*x_1 - 3.714) + 0.00767856*Abs(2.43844*x_2 - 4.97052) + 0.00540782*Abs(3.65752*x_4 - 4.888) + 15.3161*atanh(0.00416*x_5 - 0.62916) + 10.4873) - 0.370801*tan(0.0170171*Abs(2.96764*x_2 - 3.9922) + 1.79002*asin(0.0779999*x_5 - 0.6) + 0.0602386*atanh(0.104*x_3 - 1.10062) + 0.00059078*sign(4.99952 - 4.898*x_4) - 3.17769) + 0.0242988`

### task=feynman_II_21_32 seed=14

- Task source: feynman_file
- Target formula: `q/(4*pi*epsilon*r*(1-v/c))`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=2.054393e-03, r2=0.174886
- Variant formula overview:
  - icbr_full: symbolic_s=1.586524e+00, imitation_mse=7.835014e-05, target_mse=1.956586e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=1.042692e+00, imitation_mse=7.829356e-05, target_mse=1.956584e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=2.059006e+00, imitation_mse=7.835014e-05, target_mse=1.956586e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=2.664785e+00, imitation_mse=8.445122e-05, target_mse=1.945611e-03, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0.00155033*Abs(5.0*(-0.0137407*Abs(3.3*x_4 - 4.4) + 5.20474*asin(0.0499997*x_5 - 0.5) + 2.5691)*(4.06503*asin(0.0499997*x_5 - 0.5) + 2.51472 - 0.30185*exp(-2.89*(0.470588*x_3 - 1)**2)) - 4.85) - 0.0115896*Abs(0.484017*Abs(2.15*x_3 - 2.55) + 0.0644835*Abs(3.0*x_4 - 4.05) - 19.7855*acos(0.0499997*x_5 - 0.5) + 37.4569) + 0.0923 - 5.44124e-12/(atanh(0.0499997*x_5 - 0.4) + 0.275153)**5`
- icbr_no_replay formula (display, rounded):
  - `0.00155033*Abs(5.0*(-0.0137407*Abs(3.3*x_4 - 4.4) + 5.24182*atanh(0.0499997*x_5 - 0.4) + 2.04661)*(4.094*atanh(0.0499997*x_5 - 0.4) + 2.10664 - 0.30185*exp(-2.89*(0.470588*x_3 - 1)**2)) - 4.85) - 0.0115896*Abs(0.484017*Abs(2.15*x_3 - 2.55) + 0.0644835*Abs(3.0*x_4 - 4.05) + 19.9265*atanh(0.0499997*x_5 - 0.4) + 4.39168) + 0.0923 - 2.00835e-13/(1 - 0.513269*acos(0.0499997*x_5 - 0.5))**5`
- icbr_no_shared formula (display, rounded):
  - `0.00155033*Abs(5.0*(-0.0137407*Abs(3.3*x_4 - 4.4) + 5.20474*asin(0.0499997*x_5 - 0.5) + 2.5691)*(4.06503*asin(0.0499997*x_5 - 0.5) + 2.51472 - 0.30185*exp(-2.89*(0.470588*x_3 - 1)**2)) - 4.85) - 0.0115896*Abs(0.484017*Abs(2.15*x_3 - 2.55) + 0.0644835*Abs(3.0*x_4 - 4.05) - 19.7855*acos(0.0499997*x_5 - 0.5) + 37.4569) + 0.0923 - 5.44124e-12/(atanh(0.0499997*x_5 - 0.4) + 0.275153)**5`
- icbr_refit_commit formula (display, rounded):
  - `-0.0104857*Abs(0.71216*(13.2454*asin(0.01336*x_5 - 0.6058) + 9.05892 - 0.317505*exp(-2.27744*(0.449321*x_3 - 1)**2))*(16.2955*asin(0.014*x_5 - 0.60006) + 10.3265 + 0.0279263*exp(-10.2399*(0.74188*x_4 - 1)**2)) - 4.27768) - 0.0141632*Abs(0.0409196*cos(4.99406*x_4 + 2.6) + 0.247018*Abs(3.39316*x_3 - 3.695) + 93.5617*atanh(0.00599999*x_5 - 0.60022) + 61.9888) + 0.134179 - 1.97638e-14/(atanh(0.00643999*x_5 - 0.60548) + 0.678703)**5`

### task=feynman_II_21_32 seed=15

- Task source: feynman_file
- Target formula: `q/(4*pi*epsilon*r*(1-v/c))`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=2.103222e-03, r2=-0.000619
- Variant formula overview:
  - icbr_full: symbolic_s=5.563343e-01, imitation_mse=3.858509e-13, target_mse=2.103239e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=4.592627e-01, imitation_mse=3.858509e-13, target_mse=2.103239e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=6.770168e-01, imitation_mse=3.858509e-13, target_mse=2.103239e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=8.824633e-01, imitation_mse=7.571532e-13, target_mse=2.103244e-03, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0.0524806 + 5.31785e-7/(-0.0423411*x_3 + 0.0379371*x_5 + (1 - 0.03*x_2)**2 - 0.126295)**5`
- icbr_no_replay formula (display, rounded):
  - `0.0524806 + 5.31785e-7/(-0.0423411*x_3 + 0.0379371*x_5 + (1 - 0.03*x_2)**2 - 0.126295)**5`
- icbr_no_shared formula (display, rounded):
  - `0.0524806 + 5.31785e-7/(-0.0423411*x_3 + 0.0379371*x_5 + (0.03*x_2 - 1)**2 - 0.126295)**5`
- icbr_refit_commit formula (display, rounded):
  - `0.0524783 - 6.2976e-5/(0.0445612*x_3 - 0.0399274*x_5 - 0.802085*(1 - 0.0408189*x_2)**2 - 1)**5`

### task=feynman_II_21_32 seed=16

- Task source: feynman_file
- Target formula: `q/(4*pi*epsilon*r*(1-v/c))`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=2.318854e-03, r2=-0.001445
- Variant formula overview:
  - icbr_full: symbolic_s=7.710390e-01, imitation_mse=3.454889e-15, target_mse=2.318854e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=5.640275e-01, imitation_mse=3.947162e-15, target_mse=2.318854e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=8.951282e-01, imitation_mse=3.426218e-15, target_mse=2.318854e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.228961e+00, imitation_mse=1.860778e-05, target_mse=2.353682e-03, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0.0514286 - 6.05645e-5/((1 - 0.07*x_3)**(3/2) + 0.830966)**2 - 4.86491e-5/(1 - 0.00394053*x_5)**5`
- icbr_no_replay formula (display, rounded):
  - `0.0514286 - 4.86491e-5/(1 - 0.00394053*x_5)**5 - 1.29231e-5/(-0.152666 + exp(-0.05*x_3))**2`
- icbr_no_shared formula (display, rounded):
  - `0.0514292 - 6.05645e-5/((1 - 0.07*x_3)**(3/2) + 0.830966)**2 + 4.92752e-5/(0.00389725*x_5 - 1)**5`
- icbr_refit_commit formula (display, rounded):
  - `0.047132 - 8.21652e-5/(0.339024*(1 - 0.0800143*x_3)**(3/2) + 1)**2 - 3.70896e-5/(0.00614954*x_5 - 1)**4`

### task=feynman_II_21_32 seed=17

- Task source: feynman_file
- Target formula: `q/(4*pi*epsilon*r*(1-v/c))`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.835415e-03, r2=-0.000313
- Variant formula overview:
  - icbr_full: symbolic_s=6.935559e-01, imitation_mse=7.725140e-15, target_mse=1.835414e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=5.468987e-01, imitation_mse=7.743153e-15, target_mse=1.835414e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=8.939903e-01, imitation_mse=7.727693e-15, target_mse=1.835414e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.208101e+00, imitation_mse=1.175281e-14, target_mse=1.835415e-03, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0.0521538 + 6.54574e-6/(0.0222078*x_3 - 0.0212907*x_5 + 1)**5 - 8.06079e-7/(0.0195382*x_5 - 1)**4`
- icbr_no_replay formula (display, rounded):
  - `0.0521538 + 6.54574e-6/(0.0222078*x_3 - 0.0212907*x_5 + 1)**5 - 7.91616e-7/(1 - 0.0161586*x_5)**5`
- icbr_no_shared formula (display, rounded):
  - `0.0521538 + 5.85855e-6/(-0.0208236*x_5 + 0.00438811*Abs(4.95*x_3 - 5.0) + 1)**5 - 8.06079e-7/(0.0195382*x_5 - 1)**4`
- icbr_refit_commit formula (display, rounded):
  - `0.052152 - 8.30422e-6/(-0.0190009*x_3 + 0.0182163*x_5 - 1)**5 - 8.15586e-7/(0.0194068*x_5 - 1)**4`

### task=feynman_II_21_32 seed=18

- Task source: feynman_file
- Target formula: `q/(4*pi*epsilon*r*(1-v/c))`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=2.063831e-03, r2=-0.002537
- Variant formula overview:
  - icbr_full: symbolic_s=3.356230e-01, imitation_mse=2.466222e-16, target_mse=2.063831e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=2.937608e-01, imitation_mse=3.695932e-16, target_mse=2.063831e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=3.309338e-01, imitation_mse=2.466222e-16, target_mse=2.063831e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=5.123273e-01, imitation_mse=3.423692e-15, target_mse=2.063830e-03, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0.0530883 + 1.77403e-5/(1 - 0.0133938*x_5)**3`
- icbr_no_replay formula (display, rounded):
  - `0.0530913 - 1.47891e-5/(0.00947588*x_5 - 1)**5`
- icbr_no_shared formula (display, rounded):
  - `0.0530883 + 1.77403e-5/(1 - 0.0133938*x_5)**3`
- icbr_refit_commit formula (display, rounded):
  - `0.0530951 - 1.12857e-5/(0.0181853*x_5 - 1)**3`

### task=feynman_II_21_32 seed=19

- Task source: feynman_file
- Target formula: `q/(4*pi*epsilon*r*(1-v/c))`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=5.374732e-03, r2=-1.146653
- Variant formula overview:
  - icbr_full: symbolic_s=4.624700e-03, imitation_mse=0.000000e+00, target_mse=5.374732e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=5.312900e-03, imitation_mse=0.000000e+00, target_mse=5.374732e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=5.517200e-03, imitation_mse=0.000000e+00, target_mse=5.374732e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=5.475000e-03, imitation_mse=0.000000e+00, target_mse=5.374732e-03, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0`
- icbr_no_replay formula (display, rounded):
  - `0`
- icbr_no_shared formula (display, rounded):
  - `0`
- icbr_refit_commit formula (display, rounded):
  - `0`

### task=feynman_II_21_32 seed=20

- Task source: feynman_file
- Target formula: `q/(4*pi*epsilon*r*(1-v/c))`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=2.210110e-03, r2=-0.003531
- Variant formula overview:
  - icbr_full: symbolic_s=1.033927e+00, imitation_mse=6.402131e-08, target_mse=2.211104e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=7.779408e-01, imitation_mse=6.402131e-08, target_mse=2.211104e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.412116e+00, imitation_mse=6.402131e-08, target_mse=2.211104e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.667966e+00, imitation_mse=6.398339e-08, target_mse=2.208040e-03, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0.0181172*(-(-0.0655778*sign(3.0 - 2.55*x_2) + 0.0356826*sign(3.8 - 3.25*x_3) - 0.0436737)*(0.0994569*Abs(2.9*x_3 - 4.775) - 0.109079*sign(3.3 - 2.8*x_2) + 0.0162525 + 0.1205*exp(-3.8025*(1 - 0.461538*x_1)**2)) + 0.28)**4 + 0.000160558*sign(4.35909*tan(0.05*x_5 - 3.55) + 0.826117) + 0.0548359`
- icbr_no_replay formula (display, rounded):
  - `0.0181172*(-(-0.0655778*sign(3.0 - 2.55*x_2) + 0.0356826*sign(3.8 - 3.25*x_3) - 0.0436737)*(0.0994569*Abs(2.9*x_3 - 4.775) - 0.109079*sign(3.3 - 2.8*x_2) + 0.0162525 + 0.1205*exp(-3.8025*(1 - 0.461538*x_1)**2)) + 0.28)**4 + 0.000160558*sign(4.35909*tan(0.05*x_5 - 3.55) + 0.826117) + 0.0548359`
- icbr_no_shared formula (display, rounded):
  - `0.0181172*(-(-0.0655778*sign(3.0 - 2.55*x_2) + 0.0356826*sign(3.8 - 3.25*x_3) - 0.0436737)*(0.0994569*Abs(2.9*x_3 - 4.775) - 0.109079*sign(3.3 - 2.8*x_2) + 0.0162525 + 0.1205*exp(-3.8025*(1 - 0.461538*x_1)**2)) + 0.28)**4 + 0.000160558*sign(4.35909*tan(0.05*x_5 - 3.55) + 0.826117) + 0.0548359`
- icbr_refit_commit formula (display, rounded):
  - `0.00072077*(-(-0.0496442*sign(4.62376 - 3.8438*x_2) + 0.027612*sign(4.99994 - 4.194*x_3) - 0.0360372)*(0.231662*tanh(4.68*x_2 - 4.89984) + 0.102439*Abs(2.79684*x_3 - 4.6976) - 0.104904 + 0.123396*exp(-2.89*(1 - 0.446353*x_1)**2)) + 0.999986)**3 - 0.000278074*sign(27.8404*tan(0.00859999*x_5 - 0.60608) + 18.1844) + 0.054582`

### task=feynman_II_34_29a seed=1

- Task source: feynman_file
- Target formula: `q*h/(4*pi*m)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=3.283374e-03, r2=0.938800
- Variant formula overview:
  - icbr_full: symbolic_s=7.281000e-01, imitation_mse=1.012601e-03, target_mse=2.202557e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=5.828830e-01, imitation_mse=1.012601e-03, target_mse=2.202557e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=9.567596e-01, imitation_mse=1.012601e-03, target_mse=2.202557e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.324910e+00, imitation_mse=1.297657e-03, target_mse=2.111750e-03, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0.958615*atan(0.35*(-0.161707*Abs(2.2*x_1 - 3.1) + 0.751605 - 2.90006*exp(-(0.1*x_2 - 1.0)**2))*(0.401427*acos(0.45*x_1 - 1.45) - 0.488289*asin(0.45*x_2 - 1.45) + 0.650254*atanh(0.4*x_3 - 1.35) - 1.00737) - 1.25) + 0.981045`
- icbr_no_replay formula (display, rounded):
  - `0.958615*atan(0.35*(-0.161707*Abs(2.2*x_1 - 3.1) + 0.751605 - 2.90006*exp(-(0.1*x_2 - 1.0)**2))*(-0.401427*asin(0.45*x_1 - 1.45) - 0.488289*asin(0.45*x_2 - 1.45) + 0.650254*atanh(0.4*x_3 - 1.35) - 0.376811) - 1.25) + 0.981045`
- icbr_no_shared formula (display, rounded):
  - `0.958615*atan(0.35*(-0.161707*Abs(2.2*x_1 - 3.1) + 0.751605 - 2.90006*exp(-(0.1*x_2 - 1.0)**2))*(0.401427*acos(0.45*x_1 - 1.45) - 0.488289*asin(0.45*x_2 - 1.45) + 0.650254*atanh(0.4*x_3 - 1.35) - 1.00737) - 1.25) + 0.981045`
- icbr_refit_commit formula (display, rounded):
  - `0.943656*atan(0.35652*(-0.127518*Abs(2.7234*x_1 - 3.64316) + 1.48681 - 4.00201*exp(-0.810036*(1 - 0.0799981*x_2)**2))*(-0.431627*acos(1.39852 - 0.4246*x_1) - 0.530146*asin(0.42172*x_2 - 1.3916) + 0.895447*atanh(0.28936*x_3 - 1.17692) + 0.466226) - 1.2632) + 0.972905`

### task=feynman_II_34_29a seed=2

- Task source: feynman_file
- Target formula: `q*h/(4*pi*m)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=8.221035e-03, r2=0.824023
- Variant formula overview:
  - icbr_full: symbolic_s=7.010295e-01, imitation_mse=3.955179e-04, target_mse=8.117501e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=6.022967e-01, imitation_mse=3.955179e-04, target_mse=8.117501e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=9.566177e-01, imitation_mse=3.955179e-04, target_mse=8.117501e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.207156e+00, imitation_mse=6.487599e-04, target_mse=7.912716e-03, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0.998087 - 0.228911*Abs(-4.85*(0.153046*Abs(2.65*x_1 - 3.7) + 0.03796*Abs(3.05*x_2 - 4.15) + 0.538776)*(-0.010661*Abs(3.3*x_1 - 4.4) - 0.0166758*Abs(3.8*x_2 - 4.9) + 0.0828303*atanh(0.45*x_3 - 1.45) + 0.0396925) - 4.35)`
- icbr_no_replay formula (display, rounded):
  - `0.998087 - 0.228911*Abs(-4.85*(0.153046*Abs(2.65*x_1 - 3.7) + 0.03796*Abs(3.05*x_2 - 4.15) + 0.538776)*(-0.010661*Abs(3.3*x_1 - 4.4) - 0.0166758*Abs(3.8*x_2 - 4.9) + 0.0828303*atanh(0.45*x_3 - 1.45) + 0.0396925) - 4.35)`
- icbr_no_shared formula (display, rounded):
  - `0.998087 - 0.228911*Abs(-4.85*(0.153046*Abs(2.65*x_1 - 3.7) + 0.03796*Abs(3.05*x_2 - 4.15) + 0.538776)*(-0.010661*Abs(3.3*x_1 - 4.4) - 0.0166758*Abs(3.8*x_2 - 4.9) + 0.0828303*atanh(0.45*x_3 - 1.45) + 0.0396925) - 4.35)`
- icbr_refit_commit formula (display, rounded):
  - `0.993306 - 0.278095*Abs(-3.96744*(0.109992*Abs(3.60972*x_1 - 4.80208) + 0.033929*Abs(3.35212*x_2 - 4.34) + 0.528548)*(-0.0295184*Abs(1.1694*x_1 - 1.46332) - 0.0195424*Abs(3.18216*x_2 - 3.69196) + 0.140097*atanh(0.29484*x_3 - 1.16852) + 0.0804829) - 3.55736)`

### task=feynman_II_34_29a seed=3

- Task source: feynman_file
- Target formula: `q*h/(4*pi*m)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.796857e-03, r2=0.964477
- Variant formula overview:
  - icbr_full: symbolic_s=5.226517e-01, imitation_mse=3.452672e-04, target_mse=1.343956e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=4.370717e-01, imitation_mse=3.460626e-04, target_mse=1.410230e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=6.303793e-01, imitation_mse=3.452672e-04, target_mse=1.343956e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=9.185465e-01, imitation_mse=3.424145e-04, target_mse=1.340488e-03, formula_export_success=True
- icbr_full formula (display, rounded):
  - `1.30239 - 0.995738*atan(0.77194*atanh(0.4*x_3 - 1.3) + 10.1423 - 4.19099*exp(-(0.1*x_2 - 1.0)**2) - 8.52419*exp(-0.64*(0.0625*x_1 - 1)**2))`
- icbr_no_replay formula (display, rounded):
  - `0.995738*atan(0.825501*acos(0.4*x_3 - 1.4) - 11.5297 + 4.19099*exp(-(0.1*x_2 - 1.0)**2) + 8.52419*exp(-0.64*(0.0625*x_1 - 1)**2)) + 1.30239`
- icbr_no_shared formula (display, rounded):
  - `1.30239 - 0.995738*atan(0.77194*atanh(0.4*x_3 - 1.3) + 10.1423 - 4.19099*exp(-(0.1*x_2 - 1.0)**2) - 8.52419*exp(-0.64*(0.0625*x_1 - 1)**2))`
- icbr_refit_commit formula (display, rounded):
  - `1.28897 - 0.987797*atan(0.764316*atanh(0.40028*x_3 - 1.3006) + 8.96902 - 5.44208*exp(-0.81018*(1 - 0.084435*x_2)**2) - 5.5647*exp(-0.810036*(1 - 0.0844425*x_1)**2))`

### task=feynman_II_34_29a seed=4

- Task source: feynman_file
- Target formula: `q*h/(4*pi*m)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=7.587199e-03, r2=0.834555
- Variant formula overview:
  - icbr_full: symbolic_s=6.044526e-01, imitation_mse=9.639600e-04, target_mse=6.588182e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=5.299853e-01, imitation_mse=9.639600e-04, target_mse=6.588182e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=8.789273e-01, imitation_mse=9.639821e-04, target_mse=6.588616e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.004063e+00, imitation_mse=1.332422e-03, target_mse=6.218535e-03, formula_export_success=True
- icbr_full formula (display, rounded):
  - `1.45232*tan(0.4*(0.18333*Abs(3.35*x_1 - 4.5) + 0.607536)*(-0.0846498*tan(0.6*x_3 + 4.35) + 0.0150846*Abs(2.15*x_1 - 2.6) + 0.0288306*Abs(3.8*x_2 - 4.75) - 0.0766385) + 0.15) - 0.189577`
- icbr_no_replay formula (display, rounded):
  - `1.45232*tan(0.4*(0.18333*Abs(3.35*x_1 - 4.5) + 0.607536)*(-0.0846498*tan(0.6*x_3 + 4.35) + 0.0150846*Abs(2.15*x_1 - 2.6) + 0.0288306*Abs(3.8*x_2 - 4.75) - 0.0766385) + 0.15) - 0.189577`
- icbr_no_shared formula (display, rounded):
  - `1.45232*tan(0.4*(0.18333*Abs(3.35*x_1 - 4.5) + 0.607536)*(-0.0846498*tan(0.6*x_3 + 4.35) + 0.0113816*Abs(2.85*x_1 - 3.45) + 0.0288306*Abs(3.8*x_2 - 4.75) - 0.0766136) + 0.15) - 0.189577`
- icbr_refit_commit formula (display, rounded):
  - `1.73207*tan(0.31028*(0.217256*Abs(2.7806*x_1 - 3.57744) + 0.596425)*(-0.170809*tan(0.34912*x_3 + 4.84956) + 0.00847611*Abs(3.78304*x_1 - 4.1926) + 0.0254308*Abs(4.24556*x_2 - 4.84376) - 0.149365) + 0.297) - 0.500347`

### task=feynman_II_34_29a seed=5

- Task source: feynman_file
- Target formula: `q*h/(4*pi*m)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=7.392028e-04, r2=0.987189
- Variant formula overview:
  - icbr_full: symbolic_s=9.882038e-01, imitation_mse=2.260667e-04, target_mse=6.927077e-04, formula_export_success=True
  - icbr_no_replay: symbolic_s=7.805453e-01, imitation_mse=2.564532e-04, target_mse=7.326246e-04, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.316456e+00, imitation_mse=2.260667e-04, target_mse=6.927077e-04, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.825150e+00, imitation_mse=nan, target_mse=nan, formula_export_success=True
- icbr_full formula (display, rounded):
  - `20239.1*exp(-0.85671*acos(0.35*x_2 - 1.35) + 0.72144*asin(0.4*x_1 - 1.4) - 15.4575*exp(-0.64*(0.0625*x_3 - 1)**2)) + 0.918212*tanh(10.8759*sqrt(0.0201005*x_2 + 1) + 4.30698*log(0.15*x_1 + 4.575) + 0.0159711*Abs(2.55*x_3 - 5.0) - 19.5237) + 0.872851`
- icbr_no_replay formula (display, rounded):
  - `0.000101159*exp(6.24133*sqrt(0.0773481*x_1 + 1) + 0.040916*Abs(4.4*x_2 - 4.75) - 0.172201*exp(-2.7225*(1 - 0.484848*x_3)**2)) + 14069.2*exp(-0.72144*acos(0.4*x_1 - 1.4) + 0.685917*atanh(0.4*x_2 - 1.35) - 15.4575*exp(-0.64*(0.0625*x_3 - 1)**2)) - 0.0569323`
- icbr_no_shared formula (display, rounded):
  - `20239.1*exp(-0.85671*acos(0.35*x_2 - 1.35) + 0.72144*asin(0.4*x_1 - 1.4) - 15.4575*exp(-0.64*(0.0625*x_3 - 1)**2)) + 0.918212*tanh(10.8759*sqrt(0.0201005*x_2 + 1) + 4.30698*log(0.15*x_1 + 4.575) + 0.0159711*Abs(2.55*x_3 - 5.0) - 19.5237) + 0.872851`
- icbr_refit_commit formula (display, rounded):
  - `479.467*exp(-0.851305*acos(0.34864*x_2 - 1.34852) + 0.67992*asin(0.42124*x_1 - 1.42332) - 10.0845*exp(-0.810216*(1 - 0.0844331*x_3)**2)) + 0.636931*tanh(4.24114*sqrt(0.071585*x_1 + 1) + 10.2345*sqrt(0.0229827*x_2 + 1) - 16.3321 - 0.114037*exp(-1.96*(1 - 0.4736*x_3)**2)) + 0.594022`

### task=feynman_II_34_29a seed=6

- Task source: feynman_file
- Target formula: `q*h/(4*pi*m)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=2.476792e-03, r2=0.953876
- Variant formula overview:
  - icbr_full: symbolic_s=1.151434e+00, imitation_mse=5.088653e-04, target_mse=1.649910e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=9.008860e-01, imitation_mse=5.308916e-04, target_mse=1.653392e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.493817e+00, imitation_mse=5.088609e-04, target_mse=1.649930e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=2.049336e+00, imitation_mse=6.428840e-04, target_mse=1.743357e-03, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0.745629*atan(0.45*(-0.132499*Abs(2.5*x_1 - 3.5) - 0.0612013*Abs(3.8*x_2 - 4.675) - 0.550546)*(-0.654477*sin(0.35*x_1 - 1.1) + 0.497871*acos(0.45*x_2 - 1.45) + 0.767101*atanh(0.4*x_3 - 1.35) - 0.997425) - 1.25) + 0.806071 + 0.0333923*exp(-0.684781*(0.233178*tan(0.55*x_1 - 2.0) + 0.132983*Abs(3.65*x_2 - 4.525) - 1)**2)`
- icbr_no_replay formula (display, rounded):
  - `0.942838*tanh(0.35*(-0.132499*Abs(2.5*x_1 - 3.5) - 0.0612013*Abs(3.8*x_2 - 4.675) - 0.550546)*(-0.0734208*Abs(3.0*x_1 - 3.55) - 0.497871*asin(0.45*x_2 - 1.45) + 0.767101*atanh(0.4*x_3 - 1.35) + 0.216661) - 1.05) + 0.873462 + 0.0333923*exp(-4.69442*(0.0507902*Abs(3.65*x_2 - 4.525) + 0.412438*atan(4.6*x_1 - 5.0) - 1)**2)`
- icbr_no_shared formula (display, rounded):
  - `0.745629*atan(0.45*(-0.132499*Abs(2.5*x_1 - 3.5) - 0.0612013*Abs(3.8*x_2 - 4.675) - 0.550546)*(-0.654477*sin(0.35*x_1 - 1.1) + 0.497871*acos(0.45*x_2 - 1.45) + 0.767101*atanh(0.4*x_3 - 1.35) - 0.997425) - 1.25) + 0.806071 + 0.0333923*exp(-0.684574*(0.233214*tan(0.55*x_1 - 2.0) + 0.126105*Abs(3.85*x_2 - 4.775) - 1)**2)`
- icbr_refit_commit formula (display, rounded):
  - `0.779856*atan(0.44512*(-0.0983761*Abs(3.26976*x_1 - 4.18828) - 0.0909965*Abs(2.5148*x_2 - 2.80304) - 0.516777)*(-0.0517932*Abs(4.21736*x_1 - 4.61092) - 0.539404*asin(0.42292*x_2 - 1.39384) + 1.01029*atanh(0.32724*x_3 - 1.18152) + 0.297909) - 1.2976) + 0.847578 + 0.0372633*exp(-0.441751*(0.106476*tan(0.204*x_1 - 1.7304) + 0.118527*Abs(4.27356*x_2 - 4.8732) - 1)**2)`

### task=feynman_II_34_29a seed=7

- Task source: feynman_file
- Target formula: `q*h/(4*pi*m)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.849228e-03, r2=0.964085
- Variant formula overview:
  - icbr_full: symbolic_s=5.213460e-01, imitation_mse=3.269258e-04, target_mse=1.339610e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=4.464651e-01, imitation_mse=3.269258e-04, target_mse=1.339610e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=6.241023e-01, imitation_mse=3.269258e-04, target_mse=1.339610e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.050677e+00, imitation_mse=3.308502e-04, target_mse=1.371109e-03, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0.619662*atan(0.981277*acos(0.45*x_3 - 1.45) + 1.01533*asin(0.35*x_1 - 1.3) + 0.861041*asin(0.4*x_2 - 1.4) - 2.72827) + 0.841659`
- icbr_no_replay formula (display, rounded):
  - `0.619662*atan(0.981277*acos(0.45*x_3 - 1.45) + 1.01533*asin(0.35*x_1 - 1.3) + 0.861041*asin(0.4*x_2 - 1.4) - 2.72827) + 0.841659`
- icbr_no_shared formula (display, rounded):
  - `0.619662*atan(0.981277*acos(0.45*x_3 - 1.45) + 1.01533*asin(0.35*x_1 - 1.3) + 0.861041*asin(0.4*x_2 - 1.4) - 2.72827) + 0.841659`
- icbr_refit_commit formula (display, rounded):
  - `0.859846 - 0.642257*atan(1.00542*acos(1.39836 - 0.42444*x_3) - 0.78414*acos(1.41984 - 0.4196*x_2) - 0.876428*asin(0.37864*x_1 - 1.368) + 0.936128)`

### task=feynman_II_34_29a seed=8

- Task source: feynman_file
- Target formula: `q*h/(4*pi*m)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.291595e-03, r2=0.974205
- Variant formula overview:
  - icbr_full: symbolic_s=1.548221e+00, imitation_mse=4.904304e-04, target_mse=1.265619e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=1.151540e+00, imitation_mse=5.284641e-04, target_mse=1.428290e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=2.209938e+00, imitation_mse=4.904304e-04, target_mse=1.265619e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=2.969378e+00, imitation_mse=4.769891e-04, target_mse=1.321096e-03, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0.222263*(-0.118052*Abs(2.9*x_3 - 3.5) + 0.334576*asin(0.4*x_2 - 1.35) + 0.109967*atanh(0.35*x_1 - 1.3) + 1)**3 - 0.00186289*sign(-1.56552*sin(1.05*x_3 + 2.75) - 2.36062) + 1.57494 - 1.54262*exp(-0.0624998*(0.600001*(-0.181958*log(4.625*x_3 - 4.5) - 1.22803*cos(0.4*x_2 + 0.3) + 0.0028897*tan(0.3*x_1 + 4.75) + 1.41163)*(0.04104*tanh(4.35*x_2 - 5.0) + 0.586386*acos(0.45*x_3 - 1.45) - 4.36506 + 6.68165*exp(-(0.1*x_1 - 1.0)**2)) + 1)**2)`
- icbr_no_replay formula (display, rounded):
  - `0.208072*(0.0520109*tan(0.6*x_1 + 4.35) - 0.120677*Abs(2.9*x_3 - 3.5) + 0.342015*asin(0.4*x_2 - 1.35) + 1)**3 + 1.5768 - 1.54262*exp(-0.0624998*(0.600001*(-1.69195*cos(0.35*x_1 + 0.5) - 0.586387*asin(0.45*x_3 - 1.45) - 0.0292725*sign(3.4 - 2.85*x_2) + 0.691247)*(0.207891*Abs(2.25*x_2 - 2.75) - 0.24459*atanh(0.4*x_3 - 1.4) + 0.0596595 - 0.00837208*exp(-25.0*(1 - 0.84*x_1)**2)) + 1)**2)`
- icbr_no_shared formula (display, rounded):
  - `-0.222263*(0.118052*Abs(2.9*x_3 - 3.5) - 0.334576*asin(0.4*x_2 - 1.35) - 0.109967*atanh(0.35*x_1 - 1.3) - 1)**3 - 0.00186289*sign(-1.56552*sin(1.05*x_3 + 2.75) - 2.36062) + 1.57494 - 1.54262*exp(-0.0624998*(0.600001*(-0.181958*log(4.625*x_3 - 4.5) - 1.22803*cos(0.4*x_2 + 0.3) + 0.0028897*tan(0.3*x_1 + 4.75) + 1.41163)*(0.04104*tanh(4.35*x_2 - 5.0) + 0.586386*acos(0.45*x_3 - 1.45) - 4.36506 + 6.68165*exp(-(0.1*x_1 - 1.0)**2)) + 1)**2)`
- icbr_refit_commit formula (display, rounded):
  - `0.0385023*(-0.192426*Abs(2.78532*x_3 - 3.08288) + 0.56616*acos(1.27568 - 0.38236*x_2) + 0.223965*atanh(0.25328*x_1 - 1.16796) + 1)**3 + 1.52485 - 1.47275*exp(-0.0483119*(-0.735032*(1.2244*cos(0.40248*x_2 + 3.40576) + 0.00288841*tan(0.30024*x_1 + 1.60808) - 0.335325*atanh(0.102*x_3 - 1.10012) + 0.674938)*(0.0417484*tanh(4.28*x_2 - 4.89982) - 0.635354*asin(0.4224*x_3 - 1.39344) - 3.46786 + 6.67921*exp(-0.99944*(1 - 0.100068*x_1)**2)) - 1)**2) + 5.30543e-10/(-1 + 0.750086*exp(-0.973774*(1 - 0.532874*x_3)**2))**5`

### task=feynman_II_34_29a seed=9

- Task source: feynman_file
- Target formula: `q*h/(4*pi*m)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=8.267267e-04, r2=0.980500
- Variant formula overview:
  - icbr_full: symbolic_s=1.103543e+00, imitation_mse=2.927550e-04, target_mse=8.580095e-04, formula_export_success=True
  - icbr_no_replay: symbolic_s=9.052058e-01, imitation_mse=2.927550e-04, target_mse=8.580095e-04, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.468250e+00, imitation_mse=2.927550e-04, target_mse=8.580095e-04, formula_export_success=True
  - icbr_refit_commit: symbolic_s=2.106222e+00, imitation_mse=3.485394e-04, target_mse=8.940435e-04, formula_export_success=True
- icbr_full formula (display, rounded):
  - `-0.283138*sin(0.0167599*tan(0.6*x_3 + 4.3) + 9.75143 - 9.25798*exp(-0.64*(0.0625*x_2 - 1)**2) - 4.93578*exp(-0.64*(0.0625*x_1 - 1)**2)) + 0.555618*atan(5.0*(-0.119003*Abs(3.4*x_2 - 4.975) - 0.446589)*(-0.130475*asin(0.4*x_1 - 1.35) + 0.42059*asin(0.3*x_3 - 1.0) - 0.0269518*atanh(0.4*x_2 - 1.4) + 0.179751) - 1.1) + 0.950616`
- icbr_no_replay formula (display, rounded):
  - `-0.283138*sin(0.0167599*tan(0.6*x_3 + 4.3) + 9.75143 - 9.25798*exp(-0.64*(0.0625*x_2 - 1)**2) - 4.93578*exp(-0.64*(0.0625*x_1 - 1)**2)) + 0.555618*atan(5.0*(-0.119003*Abs(3.4*x_2 - 4.975) - 0.446589)*(-0.130475*asin(0.4*x_1 - 1.35) + 0.42059*asin(0.3*x_3 - 1.0) - 0.0269518*atanh(0.4*x_2 - 1.4) + 0.179751) - 1.1) + 0.950616`
- icbr_no_shared formula (display, rounded):
  - `-0.283138*sin(0.0167599*tan(0.6*x_3 + 4.3) + 9.75143 - 9.25798*exp(-0.64*(0.0625*x_2 - 1)**2) - 4.93578*exp(-0.64*(0.0625*x_1 - 1)**2)) + 0.555618*atan(5.0*(-0.119003*Abs(3.4*x_2 - 4.975) - 0.446589)*(-0.130475*asin(0.4*x_1 - 1.35) + 0.42059*asin(0.3*x_3 - 1.0) - 0.0269518*atanh(0.4*x_2 - 1.4) + 0.179751) - 1.1) + 0.950616`
- icbr_refit_commit formula (display, rounded):
  - `0.291789*sin(0.0206291*tan(0.40664*x_3 + 1.39856) + 3.01223 - 5.87222*exp(-0.810468*(1 - 0.08442*x_2)**2) - 3.05476*exp(-0.811153*(1 - 0.086605*x_1)**2)) + 0.550218*atan(4.99999*(-0.164634*Abs(2.38576*x_2 - 3.28232) - 0.438179)*(-0.12201*asin(0.4236*x_1 - 1.39736) + 2.13575*asin(0.0521199*x_3 - 0.69196) - 0.0376162*atanh(0.104*x_2 - 1.10128) + 1.31248) - 1.1) + 0.949024`

### task=feynman_II_34_29a seed=10

- Task source: feynman_file
- Target formula: `q*h/(4*pi*m)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=2.886099e-03, r2=0.946847
- Variant formula overview:
  - icbr_full: symbolic_s=1.143011e+00, imitation_mse=4.749817e-04, target_mse=1.942512e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=8.785956e-01, imitation_mse=4.735856e-04, target_mse=1.987560e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.514264e+00, imitation_mse=4.749627e-04, target_mse=1.942630e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=2.123643e+00, imitation_mse=6.665201e-04, target_mse=2.055696e-03, formula_export_success=True
- icbr_full formula (display, rounded):
  - `-0.846712*cos(0.35*(74.818*sqrt(0.0100503*x_2 + 1) + 0.119669*Abs(2.4*x_1 - 3.35) - 74.6508)*(3.83294*sqrt(0.111111*x_2 + 1) + 0.428058*asin(0.45*x_1 - 1.45) - 0.660401*atanh(0.4*x_3 - 1.35) - 4.26536) + 0.5) + 0.898446 - 1.04038e-10/(-(0.250775 - 0.194219*tanh(5.0*x_2 - 4.95))*(0.10567*Abs(2.8*x_2 - 4.65) + 0.373874) - 0.0131579)**4`
- icbr_no_replay formula (display, rounded):
  - `-0.846712*cos(0.35*(0.370431*x_2 + 0.119669*Abs(2.4*x_1 - 3.35) + 0.174307)*(-0.587705*acos(0.3*x_2 - 1.0) + 0.428058*asin(0.45*x_1 - 1.45) - 0.660401*atanh(0.4*x_3 - 1.35) + 1.1419) + 0.5) + 0.898451 + 1.35284e-11/(-(0.10567*Abs(2.8*x_2 - 4.65) + 0.373874)*(0.066331*sign(4.0 - 3.45*x_2) + 0.123507) - 0.0222223)**5`
- icbr_no_shared formula (display, rounded):
  - `-0.846712*cos(0.35*(74.818*sqrt(0.0100503*x_2 + 1) + 0.10839*Abs(2.65*x_1 - 3.7) - 74.6507)*(3.83294*sqrt(0.111111*x_2 + 1) + 0.428058*asin(0.45*x_1 - 1.45) - 0.660401*atanh(0.4*x_3 - 1.35) - 4.26536) + 0.5) + 0.898451 + 1.35284e-11/(-(0.250775 - 0.194219*tanh(5.0*x_2 - 4.95))*(0.10567*Abs(2.8*x_2 - 4.65) + 0.373874) - 0.0222223)**5`
- icbr_refit_commit formula (display, rounded):
  - `0.865062*cos(0.34804*(58.5349*sqrt(0.012899*x_2 + 1) + 0.105011*Abs(2.6786*x_1 - 3.57504) - 58.3736)*(3.82518*sqrt(0.111368*x_2 + 1) + 0.462723*asin(0.42344*x_1 - 1.39468) - 0.880598*atanh(0.31516*x_3 - 1.18448) - 4.35935) + 3.62456) + 0.921563 + 4.77428e-11/(-(0.254518 - 0.197968*tanh(4.966*x_2 - 4.89932))*(0.114223*Abs(2.56936*x_2 - 4.35112) + 0.383999) - 0.0335452)**5`

### task=feynman_II_34_29a seed=11

- Task source: feynman_file
- Target formula: `q*h/(4*pi*m)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=2.058228e-03, r2=0.958682
- Variant formula overview:
  - icbr_full: symbolic_s=5.327424e-01, imitation_mse=4.314002e-04, target_mse=1.530446e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=4.452935e-01, imitation_mse=4.314002e-04, target_mse=1.530445e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=6.205395e-01, imitation_mse=4.314002e-04, target_mse=1.530446e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=9.779390e-01, imitation_mse=5.130740e-04, target_mse=1.700210e-03, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0.721147 - 0.554169*atan(0.769754*acos(0.4*x_2 - 1.4) - 1.05289*acos(0.4*x_3 - 1.35) - 0.931393*asin(0.35*x_1 - 1.2) + 1.54635)`
- icbr_no_replay formula (display, rounded):
  - `0.554169*atan(0.931393*asin(0.35*x_1 - 1.2) + 0.769754*asin(0.4*x_2 - 1.4) - 1.05289*asin(0.4*x_3 - 1.35) - 1.1016) + 0.721147`
- icbr_no_shared formula (display, rounded):
  - `0.721147 - 0.554169*atan(0.769754*acos(0.4*x_2 - 1.4) - 1.05289*acos(0.4*x_3 - 1.35) - 0.931393*asin(0.35*x_1 - 1.2) + 1.54635)`
- icbr_refit_commit formula (display, rounded):
  - `0.592255*atan(0.744185*acos(1.3764 - 0.38444*x_2) + 1.03712*acos(0.38324*x_3 - 1.27816) + 0.826679*asin(0.36552*x_1 - 1.22052) - 3.87281) + 0.752816`

### task=feynman_II_34_29a seed=12

- Task source: feynman_file
- Target formula: `q*h/(4*pi*m)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.087793e-03, r2=0.979554
- Variant formula overview:
  - icbr_full: symbolic_s=1.377733e+00, imitation_mse=1.735118e-04, target_mse=9.183690e-04, formula_export_success=True
  - icbr_no_replay: symbolic_s=9.951279e-01, imitation_mse=1.732631e-04, target_mse=9.174476e-04, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.820075e+00, imitation_mse=1.735130e-04, target_mse=9.184127e-04, formula_export_success=True
  - icbr_refit_commit: symbolic_s=2.524781e+00, imitation_mse=2.217219e-04, target_mse=1.177550e-03, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0.172828*atan(32.3882*sqrt(0.0306122*x_2 + 1) + 1.19983*acos(1.2 - 0.35*x_1) - 36.3999) + 0.41435*atan(1.38808*asin(0.3*x_1 - 1.05) + 0.954848*asin(0.4*x_2 - 1.4) - 3.24029*asin(0.3*x_3 - 1.0) - 2.21116) + 0.00109207*sign(-3.35*(-0.73795 + 0.465955*exp(-2.4025*(1 - 0.483871*x_3)**2))*(-3.84124*sqrt(0.0666667*x_3 + 1) - 0.0161195*tanh(4.7*x_2 - 5.0) + 3.91612) + 0.1) + 0.809839`
- icbr_no_replay formula (display, rounded):
  - `0.172828*atan(32.3882*sqrt(0.0306122*x_2 + 1) + 1.19983*acos(1.2 - 0.35*x_1) - 36.3999) - 0.41435*atan(0.954848*acos(0.4*x_2 - 1.4) - 3.24029*acos(0.3*x_3 - 1.0) - 1.38808*asin(0.3*x_1 - 1.05) + 5.80113) + 0.808708 - 3.23256e-10/(-(-0.73795 + 0.465955*exp(-2.4025*(1 - 0.483871*x_3)**2))*(-3.84124*sqrt(0.0666667*x_3 + 1) + 0.00888677*sign(3.9 - 3.3*x_2) + 3.90901) - 0.0222223)**5`
- icbr_no_shared formula (display, rounded):
  - `0.172828*atan(32.5465*sqrt(0.0304569*x_2 + 1) + 1.19983*acos(1.2 - 0.35*x_1) - 36.558) + 0.41435*atan(1.38808*asin(0.3*x_1 - 1.05) + 0.954848*asin(0.4*x_2 - 1.4) - 3.24029*asin(0.3*x_3 - 1.0) - 2.21116) + 0.00109207*sign(-3.35*(-0.73795 + 0.465955*exp(-2.4025*(1 - 0.483871*x_3)**2))*(-3.84124*sqrt(0.0666667*x_3 + 1) - 0.0161195*tanh(4.7*x_2 - 5.0) + 3.91612) + 0.1) + 0.809839`
- icbr_refit_commit formula (display, rounded):
  - `-0.179602*atan(-38.7283*sqrt(0.0243341*x_2 + 1) + 1.10392*acos(0.3648*x_1 - 1.21712) + 39.1043) + 0.386539*atan(1.10744*asin(0.36472*x_1 - 1.21768) + 0.88996*asin(0.42648*x_2 - 1.42696) - 16.4688*asin(0.0518399*x_3 - 0.68864) - 11.1492) + 0.771904 + 2.12262e-19/(-(-0.114835*Abs(1.65324*x_3 - 3.40648) - 0.264618)*(1.68828*(1 - 0.0501423*x_3)**(3/2) - 0.016121*tanh(4.7*x_2 - 4.99991) - 1.61393) + 0.0260305)**5`

### task=feynman_II_34_29a seed=13

- Task source: feynman_file
- Target formula: `q*h/(4*pi*m)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.373389e-03, r2=0.977742
- Variant formula overview:
  - icbr_full: symbolic_s=8.736191e-01, imitation_mse=1.902845e-04, target_mse=1.060870e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=6.960472e-01, imitation_mse=2.647204e-04, target_mse=1.347067e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.212391e+00, imitation_mse=2.455009e-04, target_mse=1.164487e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.732292e+00, imitation_mse=1.911834e-04, target_mse=1.086934e-03, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0.0635608*acos(0.0220897*tanh(4.6*x_3 - 5.0) - 0.131824*Abs(3.65*x_2 - 4.625) + 0.928782) - 0.791857*atan(0.776581*acos(0.4*x_2 - 1.4) - 2.29467*acos(0.3*x_3 - 1.0) - 1.39838*asin(0.3*x_1 - 1.3) + 4.23024) + 1.06252`
- icbr_no_replay formula (display, rounded):
  - `0.0635608*asin(0.131824*Abs(3.65*x_2 - 4.625) + 0.0138598*sign(3.45 - 2.9*x_3) - 0.936838) - 0.791857*atan(16.6009*sqrt(0.0989011*x_3 + 1) + 0.776581*acos(0.4*x_2 - 1.4) - 0.994729*atanh(0.4*x_1 - 1.35) - 18.0816) + 1.16236`
- icbr_no_shared formula (display, rounded):
  - `-0.0635608*asin(0.0220897*tanh(4.6*x_3 - 5.0) - 0.131824*Abs(3.65*x_2 - 4.625) + 0.928782) - 0.791857*atan(16.4388*sqrt(0.1*x_3 + 1) + 1.39838*acos(0.3*x_1 - 1.3) + 0.776581*acos(0.4*x_2 - 1.4) - 20.5421) + 1.16236`
- icbr_refit_commit formula (display, rounded):
  - `-0.0620657*asin(0.022551*tanh(4.6*x_3 - 4.99979) - 0.120091*Abs(4.03*x_2 - 4.7174) + 0.949945) + 0.847173*atan(2.24617*acos(0.29984*x_3 - 1.00052) + 1.36848*asin(0.29992*x_1 - 1.29992) + 0.719313*asin(0.4232*x_2 - 1.4254) - 5.47306) + 1.23171`

### task=feynman_II_34_29a seed=14

- Task source: feynman_file
- Target formula: `q*h/(4*pi*m)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=2.658555e-03, r2=0.948101
- Variant formula overview:
  - icbr_full: symbolic_s=8.755238e-01, imitation_mse=9.152153e-04, target_mse=3.775060e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=6.773494e-01, imitation_mse=8.399750e-04, target_mse=3.782905e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.161177e+00, imitation_mse=9.150906e-04, target_mse=3.767809e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.707466e+00, imitation_mse=4.404022e-03, target_mse=5.280242e-03, formula_export_success=True
- icbr_full formula (display, rounded):
  - `-0.0834649*tan(0.124729*Abs(3.35*x_3 - 3.95) - 0.0424161*atanh(0.45*x_1 - 1.45) - 0.0595313*atanh(0.4*x_2 - 1.4) + 1.68975) - 0.569158*acos(-1.0*(0.661771 - 0.689674*cos(0.35*x_2 + 0.45))*(0.66984*cos(0.35*x_1 + 0.5) - 0.608772) - 0.35) + 1.05126`
- icbr_no_replay formula (display, rounded):
  - `-0.560345*atanh(1.0*(-0.0509485*Abs(4.4*x_1 - 4.95) - 0.174557)*(0.089243*Abs(2.6*x_2 - 3.1) + 0.195714) + 0.45) + 0.0179477 + 0.686004/sqrt(-0.252598*tan(0.6*x_2 + 4.3) + Abs(3.35*x_3 - 3.95) - 0.340066*atanh(0.45*x_1 - 1.45) + 0.655326)`
- icbr_no_shared formula (display, rounded):
  - `-0.0834649*tan(0.149221*Abs(2.8*x_3 - 3.3) - 0.0424161*atanh(0.45*x_1 - 1.45) - 0.0595313*atanh(0.4*x_2 - 1.4) + 1.68959) - 0.569158*asin(1.0*(0.661771 - 0.689674*cos(0.35*x_2 + 0.45))*(0.66984*cos(0.35*x_1 + 0.5) - 0.608772) + 0.35) + 0.157225`
- icbr_refit_commit formula (display, rounded):
  - `-0.0834693*tan(0.129904*Abs(3.18956*x_3 - 3.49372) - 0.0730396*atanh(0.27768*x_1 - 1.1738) - 0.0784414*atanh(0.208*x_2 - 1.2) + 1.59681) - 0.758654*atanh(0.74928*(0.662486 - 0.719491*cos(0.334*x_2 + 0.5004))*(-0.0498681*Abs(4.48192*x_1 - 4.78752) - 0.163555) + 0.2674) + 0.161112`

### task=feynman_II_34_29a seed=15

- Task source: feynman_file
- Target formula: `q*h/(4*pi*m)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=2.851010e-03, r2=0.947507
- Variant formula overview:
  - icbr_full: symbolic_s=7.064380e-01, imitation_mse=7.056124e-04, target_mse=1.759438e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=5.987618e-01, imitation_mse=6.881994e-04, target_mse=2.031722e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=9.550205e-01, imitation_mse=7.056124e-04, target_mse=1.759438e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.316425e+00, imitation_mse=8.465182e-04, target_mse=1.887460e-03, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0.983527*atan(0.5*(0.253795*Abs(2.15*x_1 - 3.0) + 0.0554277*Abs(3.45*x_2 - 4.45) + 0.746172)*(0.290631*sqrt(x_1 - 1) + 0.401344*asin(0.4*x_2 - 1.35) - 0.42277*atanh(0.4*x_3 - 1.35) - 0.215793) - 1.4) + 1.09033`
- icbr_no_replay formula (display, rounded):
  - `0.983527*atan(0.5*(0.253795*Abs(2.15*x_1 - 3.0) + 0.0554277*Abs(3.45*x_2 - 4.45) + 0.746172)*(-0.401344*acos(0.4*x_2 - 1.35) + 0.1824*atanh(0.45*x_1 - 1.45) - 0.42277*atanh(0.4*x_3 - 1.35) + 0.835781) - 1.4) + 1.09033`
- icbr_no_shared formula (display, rounded):
  - `0.983527*atan(0.5*(0.253795*Abs(2.15*x_1 - 3.0) + 0.0554277*Abs(3.45*x_2 - 4.45) + 0.746172)*(0.290631*sqrt(x_1 - 1) + 0.401344*asin(0.4*x_2 - 1.35) - 0.42277*atanh(0.4*x_3 - 1.35) - 0.215793) - 1.4) + 1.09033`
- icbr_refit_commit formula (display, rounded):
  - `-0.0552441 + 2.31235*exp(-2.40287*(-0.161381*(0.462651*sin(0.436*x_2 - 1.4) + 0.155264*Abs(3.4478*x_1 - 4.61596) + 1.1063)*(0.439955*acos(1.29928 - 0.36508*x_2) + 0.324394*atanh(0.25504*x_1 - 1.1724) - 0.544125*atanh(0.33312*x_3 - 1.19372) - 0.364557) + 1)**2)`

### task=feynman_II_34_29a seed=16

- Task source: feynman_file
- Target formula: `q*h/(4*pi*m)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=6.639074e-04, r2=0.987324
- Variant formula overview:
  - icbr_full: symbolic_s=1.775478e+00, imitation_mse=1.680916e-04, target_mse=5.053207e-04, formula_export_success=True
  - icbr_no_replay: symbolic_s=1.266400e+00, imitation_mse=2.020571e-04, target_mse=5.637529e-04, formula_export_success=True
  - icbr_no_shared: symbolic_s=2.538002e+00, imitation_mse=1.680915e-04, target_mse=5.053204e-04, formula_export_success=True
  - icbr_refit_commit: symbolic_s=3.097244e+00, imitation_mse=nan, target_mse=nan, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0.0446322*(0.716694*sin(0.5*x_2 + 1.55) - 0.0600715*Abs(3.9*x_3 - 4.9) - 1.15328)*(-0.555983*cos(0.55*x_1 + 2.9) - 0.0764214*Abs(2.8*x_2 - 3.95) - 1.04315) + 0.117925*exp(-0.855747*acos(0.35*x_1 - 1.35) - 0.653621*acos(0.4*x_2 - 1.4) + 1.86043*acos(0.3*x_3 - 1.0)) - 0.00955752*cos(3.0*(0.611546*sin(0.7*x_2 + 4.0) - 0.304393*cos(0.7*x_1 - 4.0) + 0.510998)*(0.0399438*tanh(4.6*x_1 - 5.0) + 0.0800123*Abs(2.95*x_2 - 4.55) - 0.0804773*sign(3.85 - 3.3*x_3) + 0.1074) + 2.05) - 0.04251`
- icbr_no_replay formula (display, rounded):
  - `0.0446322*(-0.105176*Abs(2.65*x_1 - 3.6) - 0.0764214*Abs(2.8*x_2 - 3.95) - 0.505014)*(-0.0947951*Abs(3.5*x_2 - 4.45) - 0.0600715*Abs(3.9*x_3 - 4.9) - 0.517739) + 2.74477*tanh(1.06876*acos(0.3*x_3 - 1.0) + 0.375485*asin(0.4*x_2 - 1.4) + 0.39443*atanh(0.4*x_1 - 1.35) - 3.43849) + 2.70828 + 0.0187509*exp(-3.0625*((-0.0750697*Abs(2.45*x_1 - 3.8) + 0.11764*Abs(3.15*x_2 - 4.55) + 0.185453)*(0.0800123*Abs(2.95*x_2 - 4.55) - 0.0254082*sign(3.15 - 2.65*x_1) - 0.0804773*sign(3.85 - 3.3*x_3) + 0.121668) - 0.342857)**2)`
- icbr_no_shared formula (display, rounded):
  - `0.0446322*(0.716694*sin(0.5*x_2 + 1.55) - 0.0600715*Abs(3.9*x_3 - 4.9) - 1.15328)*(-0.555983*cos(0.55*x_1 + 2.9) - 0.0764214*Abs(2.8*x_2 - 3.95) - 1.04315) + 0.117925*exp(-0.855747*acos(0.35*x_1 - 1.35) - 0.653621*acos(0.4*x_2 - 1.4) + 1.86043*acos(0.3*x_3 - 1.0)) - 0.00955752*cos(3.0*(0.611546*sin(0.7*x_2 + 4.0) - 0.304393*cos(0.7*x_1 - 4.0) + 0.510998)*(0.0399438*tanh(4.6*x_1 - 5.0) + 0.0800123*Abs(2.95*x_2 - 4.55) - 0.0804773*sign(3.85 - 3.3*x_3) + 0.1074) + 2.05) - 0.0425101`
- icbr_refit_commit formula (display, rounded):
  - `0.0446294*(-0.715832*sin(0.50072*x_2 + 4.69016) - 0.0555747*Abs(4.15716*x_3 - 4.86284) - 1.1406)*(-0.376372*sin(0.64*x_2 + 4.20008) + 0.559764*cos(0.54316*x_1 - 0.2) - 1.42984) + 117.776*exp(-8.77492*acos(0.72872 - 0.0548399*x_3) + 0.854009*acos(1.3508 - 0.35084*x_1) + 0.611366*acos(1.43 - 0.42808*x_2)) + 0.00955593*cos(3.00044*(-0.304412*cos(0.69992*x_1 - 3.99972) + 0.10175*Abs(3.5532*x_2 - 4.87536) - 0.169669)*(0.0399593*tanh(4.6*x_1 - 4.99962) + 0.13525*Abs(1.71296*x_2 - 2.61648) - 0.0687149*sign(4.5972 - 3.88752*x_3) + 0.122699) - 1.09164) - 0.0425536`

### task=feynman_II_34_29a seed=17

- Task source: feynman_file
- Target formula: `q*h/(4*pi*m)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.950528e-03, r2=0.965082
- Variant formula overview:
  - icbr_full: symbolic_s=9.889499e-01, imitation_mse=3.893392e-04, target_mse=1.730093e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=7.899756e-01, imitation_mse=4.024927e-04, target_mse=1.737118e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.329505e+00, imitation_mse=3.893392e-04, target_mse=1.730093e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.911617e+00, imitation_mse=5.009522e-04, target_mse=1.808363e-03, formula_export_success=True
- icbr_full formula (display, rounded):
  - `-0.533995*atan(0.63302*acos(0.45*x_1 - 1.45) + 0.958575*acos(0.35*x_2 - 1.2) - 0.964423*acos(0.35*x_3 - 1.2) + 0.0821784) + 0.672374 + 0.269416*exp(-10.89*(-(-0.184895*Abs(2.55*x_3 - 4.65) - 0.641729)*(24.1242*sqrt(0.032967*x_3 + 1) - 0.219171*cos(0.6*x_1 + 2.7) - 24.6368) + 0.333333)**2)`
- icbr_no_replay formula (display, rounded):
  - `0.533995*atan(0.964423*acos(0.35*x_3 - 1.2) + 0.63302*asin(0.45*x_1 - 1.45) + 0.958575*asin(0.35*x_2 - 1.2) - 2.58225) + 0.672374 + 0.269416*exp(-10.89*(-(-0.184895*Abs(2.55*x_3 - 4.65) - 0.641729)*(-0.0363807*Abs(3.25*x_1 - 4.6) - 4.98276 + 8.9456*exp(-0.64*(0.0625*x_3 - 1)**2)) + 0.333333)**2)`
- icbr_no_shared formula (display, rounded):
  - `-0.533995*atan(0.63302*acos(0.45*x_1 - 1.45) + 0.958575*acos(0.35*x_2 - 1.2) - 0.964423*acos(0.35*x_3 - 1.2) + 0.0821784) + 0.672374 + 0.269416*exp(-10.89*(-(-0.184895*Abs(2.55*x_3 - 4.65) - 0.641729)*(24.1242*sqrt(0.032967*x_3 + 1) - 0.219171*cos(0.6*x_1 + 2.7) - 24.6368) + 0.333333)**2)`
- icbr_refit_commit formula (display, rounded):
  - `0.57869*atan(0.831184*acos(1.27584 - 0.3824*x_2) + 0.654388*acos(1.3972 - 0.42432*x_1) + 0.883285*acos(0.36592*x_3 - 1.22092) - 4.81509) + 0.727127 + 0.168069*exp(-25.0*(-(-0.224204*Abs(2.1264*x_3 - 4.05176) - 0.657292)*(24.5687*sqrt(0.0323434*x_3 + 1) - 0.218947*cos(0.6008*x_1 + 2.69808) - 25.0807) + 0.18)**2)`

### task=feynman_II_34_29a seed=18

- Task source: feynman_file
- Target formula: `q*h/(4*pi*m)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=1.232347e-03, r2=0.978397
- Variant formula overview:
  - icbr_full: symbolic_s=1.443062e+00, imitation_mse=6.048803e-04, target_mse=1.348723e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=1.072885e+00, imitation_mse=6.800375e-04, target_mse=1.410383e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.999228e+00, imitation_mse=6.048803e-04, target_mse=1.348723e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=2.564686e+00, imitation_mse=6.707871e-04, target_mse=1.365587e-03, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0.00978026*(-cos(0.55*x_3 + 2.95) + 0.0888356*Abs(2.5*x_2 - 3.5) + 0.175357)**4 - 0.688504*atan(1.75*(14.7391*sqrt(0.03*x_2 + 1) + 5.72956*sqrt(0.0444444*x_3 + 1) - 20.6077)*(11.8169*sqrt(0.0721649*x_3 + 1) + 0.694427*acos(0.35*x_1 - 1.2) + 0.0255356*sign(3.75 - 3.2*x_2) - 13.8433) + 1.0) + 1.6092 - 1.08849*exp(-5.24146*(-0.00914901*Abs(2.75*x_3 - 4.625) + 0.401549 - exp(-0.64*(0.0625*x_2 - 1)**2))**2)`
- icbr_no_replay formula (display, rounded):
  - `-0.688504*atan(1.75*(-2.52295*(1 - 0.0333333*x_3)**(3/2) - 0.238664 + 4.99295*exp(-0.64*(0.0625*x_2 - 1)**2))*(11.8169*sqrt(0.0721649*x_3 + 1) - 0.694427*asin(0.35*x_1 - 1.2) + 0.0255356*sign(3.75 - 3.2*x_2) - 12.7525) + 1.0) + 1.6094 - 1.08849*exp(-5.24146*(-0.00914901*Abs(2.75*x_3 - 4.625) + 0.401549 - exp(-0.64*(0.0625*x_2 - 1)**2))**2) + 0.112318*exp(-2.05475*(0.0916231*Abs(2.5*x_2 - 3.5) - 0.154663*Abs(3.35*x_3 - 4.45) - 1)**2)`
- icbr_no_shared formula (display, rounded):
  - `0.00978026*(-cos(0.55*x_3 + 2.95) + 0.0888356*Abs(2.5*x_2 - 3.5) + 0.175357)**4 - 0.688504*atan(1.75*(14.7391*sqrt(0.03*x_2 + 1) + 5.72956*sqrt(0.0444444*x_3 + 1) - 20.6077)*(11.8169*sqrt(0.0721649*x_3 + 1) + 0.694427*acos(0.35*x_1 - 1.2) + 0.0255356*sign(3.75 - 3.2*x_2) - 13.8433) + 1.0) + 1.6092 - 1.08849*exp(-5.24146*(-0.00914901*Abs(2.75*x_3 - 4.625) + 0.401549 - exp(-0.64*(0.0625*x_2 - 1)**2))**2)`
- icbr_refit_commit formula (display, rounded):
  - `0.0104789*(-cos(0.538*x_3 - 3.29864) + 0.0902867*Abs(2.37416*x_2 - 3.19712) + 0.165518)**4 - 0.889379*atan(1.55964*(14.4188*sqrt(0.0306956*x_2 + 1) + 5.81491*sqrt(0.0437528*x_3 + 1) - 20.3728)*(11.8465*sqrt(0.0719672*x_3 + 1) - 0.659822*acos(1.22356 - 0.36776*x_1) + 0.0211021*sign(4.9786 - 4.3*x_2) - 11.7228) + 1.19632) + 0.632394 + 0.95582*exp(-3.92018*(-0.0137349*Abs(2.46372*x_3 - 4.34388) + 1 - 0.876227*exp(-0.810396*(1 - 0.0844237*x_2)**2))**2)`

### task=feynman_II_34_29a seed=19

- Task source: feynman_file
- Target formula: `q*h/(4*pi*m)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=3.165730e-03, r2=0.935921
- Variant formula overview:
  - icbr_full: symbolic_s=8.142713e-01, imitation_mse=7.988914e-04, target_mse=2.393458e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=6.840955e-01, imitation_mse=8.008740e-04, target_mse=2.487608e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.098556e+00, imitation_mse=7.988914e-04, target_mse=2.393458e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.484284e+00, imitation_mse=7.991727e-04, target_mse=2.075125e-03, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0.689935*atan(0.4*(-6.32414*sqrt(0.114583*x_2 + 1) - 1.17134*acos(0.35*x_3 - 1.2) - 0.74168*asin(0.4*x_1 - 1.35) + 8.69794)*(-0.40968*cos(0.7*x_1 - 3.9) + 0.0503329*tan(0.65*x_3 - 2.15) - 0.0926874*Abs(3.2*x_2 - 4.8) - 0.918676) - 1.4) + 0.786785`
- icbr_no_replay formula (display, rounded):
  - `0.689935*atan(0.4*(0.0503329*tan(0.65*x_3 - 2.15) - 0.108031*Abs(2.3*x_1 - 3.4) - 0.0926874*Abs(3.2*x_2 - 4.8) - 0.460376)*(0.74168*acos(0.4*x_1 - 1.35) + 0.995601*acos(0.3*x_2 - 1.0) + 1.17134*asin(0.35*x_3 - 1.2) - 3.29986) - 1.4) + 0.786785`
- icbr_no_shared formula (display, rounded):
  - `0.689935*atan(0.4*(-6.32414*sqrt(0.114583*x_2 + 1) - 1.17134*acos(0.35*x_3 - 1.2) - 0.74168*asin(0.4*x_1 - 1.35) + 8.69794)*(-0.40968*cos(0.7*x_1 - 3.9) + 0.0503329*tan(0.65*x_3 - 2.15) - 0.0926874*Abs(3.2*x_2 - 4.8) - 0.918676) - 1.4) + 0.786785`
- icbr_refit_commit formula (display, rounded):
  - `0.786277*atan(0.35856*(-6.37849*sqrt(0.113469*x_2 + 1) - 1.05595*acos(0.3834*x_3 - 1.27808) - 0.792965*asin(0.38188*x_1 - 1.27476) + 8.54289)*(-0.487166*cos(0.54*x_1 - 3.39992) + 0.0552444*tan(0.41496*x_3 + 4.38452) - 0.0820026*Abs(3.46228*x_2 - 4.78952) - 0.884676) - 1.37624) + 0.872009`

### task=feynman_II_34_29a seed=20

- Task source: feynman_file
- Target formula: `q*h/(4*pi*m)`
- Teacher cache: hit=True, mode=readonly, status=hit
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics (against dataset test_label): mse=2.478911e-03, r2=0.950068
- Variant formula overview:
  - icbr_full: symbolic_s=9.343091e-01, imitation_mse=8.107352e-04, target_mse=3.292388e-03, formula_export_success=True
  - icbr_no_replay: symbolic_s=7.570585e-01, imitation_mse=8.268140e-04, target_mse=3.317032e-03, formula_export_success=True
  - icbr_no_shared: symbolic_s=1.241430e+00, imitation_mse=8.107352e-04, target_mse=3.292388e-03, formula_export_success=True
  - icbr_refit_commit: symbolic_s=1.703222e+00, imitation_mse=5.804419e-04, target_mse=2.621192e-03, formula_export_success=True
- icbr_full formula (display, rounded):
  - `0.755425*cos(0.55*(9.12817 - 16.8169*exp(-0.64*(0.0625*x_1 - 1)**2))*(0.126878*acos(0.35*x_1 - 1.3) - 0.506324*asin(0.35*x_2 - 1.2) + 0.268919*atanh(0.45*x_3 - 1.45) - 0.502577) + 3.55) - 0.236817*tanh(0.512389*Abs(2.65*x_3 - 3.5) + 0.413709) + 1.05222`
- icbr_no_replay formula (display, rounded):
  - `-0.14485*(0.16081*Abs(2.65*x_3 - 3.5) - 1)**5 + 0.755425*cos(0.55*(9.12817 - 16.8169*exp(-0.64*(0.0625*x_1 - 1)**2))*(-0.506324*acos(1.2 - 0.35*x_2) - 0.120762*atanh(0.35*x_1 - 1.2) + 0.268919*atanh(0.45*x_3 - 1.45) + 0.505264) + 3.55) + 0.817589`
- icbr_no_shared formula (display, rounded):
  - `0.755425*cos(0.55*(9.12817 - 16.8169*exp(-0.64*(0.0625*x_1 - 1)**2))*(0.126878*acos(0.35*x_1 - 1.3) - 0.506324*asin(0.35*x_2 - 1.2) + 0.268919*atanh(0.45*x_3 - 1.45) - 0.502577) + 3.55) - 0.236817*tanh(0.512389*Abs(2.65*x_3 - 3.5) + 0.413709) + 1.05222`
- icbr_refit_commit formula (display, rounded):
  - `-1.2081*cos(0.38316*(5.15552 - 11.0757*exp(-0.810396*(1 - 0.0844237*x_1)**2))*(-0.481198*acos(1.22584 - 0.36768*x_2) - 0.126928*acos(1.29936 - 0.35*x_1) + 0.454226*asin(0.30052*x_3 - 1.30068) + 0.831697) + 0.40184) - 0.199249*tanh(0.422043*Abs(3.33796*x_3 - 4.0492) + 0.192144) + 1.43491`

## Visualization Summary

- `icbr_benchmark_symbolic_time_errorbar.png`
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
