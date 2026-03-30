# ICBR Benchmark Summary

## Run Config

- Profile: quality
- Tasks: minimal, combo, poly_cubic, trig_interaction
- Seeds: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9
- Train/Test samples per task: 1000/500
- Train steps: 200, lr: 0.01, lamb: 0.001
- Teacher cache: mode=readwrite, dir=outputs\teacher_cache_stage20_quality_10seeds, version=stage20_v1
- ICBR shortlist topk: 3, grid_number: 21, iteration: 2
- Variants: baseline, icbr_full, icbr_no_replay, icbr_no_shared, icbr_refit_commit
- Teacher prune policy: enabled=True, node_th=0.01, edge_th=0.01

## Task-Level Aggregate Stats

| task | n | teacher_cache_hit_mean | teacher_mse_mean | teacher_r2_mean | teacher_gate_pass_mean | baseline_symbolic_mean | icbr_symbolic_mean | delta_mean | delta_median | speedup_mean | speedup_median | mse_shift_mean | target_mse_shift_mean | formula_pass_mean |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| minimal | 10 | 0.0000 | 8.098159e-04 | 0.998352 | 1.0000 | 1.625279 | 0.184004 | 1.441274 | 1.435825 | 8.9421 | 8.6840 | 3.175871e-05 | 3.897287e-06 | 1.0000 |
| combo | 10 | 0.0000 | 1.002603e-04 | 0.999828 | 1.0000 | 9.810976 | 0.655021 | 9.155955 | 9.056827 | 14.9893 | 15.1019 | 1.705845e-05 | 3.000943e-05 | 1.0000 |
| poly_cubic | 10 | 0.0000 | 3.051873e-04 | 0.993830 | 1.0000 | 11.614028 | 1.079258 | 10.534770 | 8.800530 | 12.3000 | 13.5866 | 9.861425e-05 | 8.781510e-05 | 1.0000 |
| trig_interaction | 10 | 0.0000 | 4.589565e-03 | 0.993708 | 1.0000 | 26.910920 | 2.224929 | 24.685992 | 20.153096 | 13.5365 | 14.4099 | -4.661277e-04 | -2.979883e-04 | 1.0000 |

## Statistical Significance (by task)

| task | metric | favorable_direction | n_total | n_finite | n_effective | improved | worsened | ties | p_value_two_sided | mean_delta_ci95 |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| minimal | symbolic_wall_time_delta_s | positive | 10 | 10 | 10 | 10 | 0 | 0 | 0.001953 | [1.414627e+00, 1.469695e+00] |
| minimal | final_mse_loss_shift | negative | 10 | 10 | 10 | 0 | 10 | 0 | 0.001953 | [1.952595e-05, 4.296377e-05] |
| combo | symbolic_wall_time_delta_s | positive | 10 | 10 | 10 | 10 | 0 | 0 | 0.001953 | [8.893874e+00, 9.432597e+00] |
| combo | final_mse_loss_shift | negative | 10 | 10 | 10 | 2 | 8 | 0 | 0.109375 | [-3.181105e-05, 5.059731e-05] |
| poly_cubic | symbolic_wall_time_delta_s | positive | 10 | 10 | 10 | 10 | 0 | 0 | 0.001953 | [8.452945e+00, 1.335747e+01] |
| poly_cubic | final_mse_loss_shift | negative | 10 | 10 | 10 | 2 | 8 | 0 | 0.109375 | [3.925103e-05, 1.535140e-04] |
| trig_interaction | symbolic_wall_time_delta_s | positive | 10 | 10 | 10 | 10 | 0 | 0 | 0.001953 | [1.918877e+01, 3.173477e+01] |
| trig_interaction | final_mse_loss_shift | negative | 10 | 10 | 10 | 7 | 3 | 0 | 0.343750 | [-1.128604e-03, 8.508130e-05] |

## Variant Ablation Aggregate Stats (Stage 15)

| task | variant | n | teacher_gate_pass_mean | formula_pass_mean | symbolic_mean_s | speedup_mean_x | mse_shift_mean | target_mse_shift_mean | replay_rank_inversion_mean | refit_drift_l2_mean |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| minimal | baseline | 10 | 1.0000 | 1.0000 | 1.625279 | 1.0000 | 0.000000e+00 | 0.000000e+00 | nan | nan |
| minimal | icbr_full | 10 | 1.0000 | 1.0000 | 0.184004 | 8.9421 | 3.175871e-05 | 3.897287e-06 | 0.000000 | nan |
| minimal | icbr_no_replay | 10 | 1.0000 | 1.0000 | 0.170557 | 9.6233 | 3.175871e-05 | 3.897287e-06 | nan | nan |
| minimal | icbr_no_shared | 10 | 1.0000 | 1.0000 | 0.178552 | 9.2114 | 3.175871e-05 | 3.897287e-06 | 0.000000 | nan |
| minimal | icbr_refit_commit | 10 | 1.0000 | 1.0000 | 0.216280 | 7.5536 | 1.924665e-02 | 2.011526e-02 | 0.000000 | 2.943549e+00 |
| combo | baseline | 10 | 1.0000 | 1.0000 | 9.810976 | 1.0000 | 0.000000e+00 | 0.000000e+00 | nan | nan |
| combo | icbr_full | 10 | 1.0000 | 1.0000 | 0.655021 | 14.9893 | 1.705845e-05 | 3.000943e-05 | 0.333333 | nan |
| combo | icbr_no_replay | 10 | 1.0000 | 1.0000 | 0.545449 | 18.0078 | 5.626224e-05 | 5.726014e-05 | nan | nan |
| combo | icbr_no_shared | 10 | 1.0000 | 1.0000 | 1.059644 | 9.2883 | 1.713075e-05 | 2.997316e-05 | 0.333333 | nan |
| combo | icbr_refit_commit | 10 | 1.0000 | 1.0000 | 0.924942 | 10.6067 | 1.723460e-02 | 1.735054e-02 | 0.533333 | 3.256235e+00 |
| poly_cubic | baseline | 10 | 1.0000 | 1.0000 | 11.614028 | 1.0000 | 0.000000e+00 | 0.000000e+00 | nan | nan |
| poly_cubic | icbr_full | 10 | 1.0000 | 1.0000 | 1.079258 | 12.3000 | 9.861425e-05 | 8.781510e-05 | 0.323333 | nan |
| poly_cubic | icbr_no_replay | 10 | 1.0000 | 1.0000 | 0.873986 | 15.3243 | 1.313106e-04 | 1.242738e-04 | nan | nan |
| poly_cubic | icbr_no_shared | 10 | 1.0000 | 1.0000 | 1.718278 | 8.0103 | 9.945093e-05 | 8.903120e-05 | 0.356667 | nan |
| poly_cubic | icbr_refit_commit | 10 | 1.0000 | 1.0000 | 1.467487 | 9.0052 | 1.220168e-02 | 1.223885e-02 | 0.353333 | 3.618784e+00 |
| trig_interaction | baseline | 10 | 1.0000 | 1.0000 | 26.910920 | 1.0000 | 0.000000e+00 | 0.000000e+00 | nan | nan |
| trig_interaction | icbr_full | 10 | 1.0000 | 1.0000 | 2.224929 | 13.5365 | -4.661277e-04 | -2.979883e-04 | 0.389693 | nan |
| trig_interaction | icbr_no_replay | 10 | 1.0000 | 1.0000 | 1.110716 | 25.9918 | 4.317174e-04 | 6.702650e-04 | nan | nan |
| trig_interaction | icbr_no_shared | 10 | 1.0000 | 1.0000 | 3.279569 | 8.6914 | -4.661275e-04 | -2.979878e-04 | 0.389693 | nan |
| trig_interaction | icbr_refit_commit | 10 | 1.0000 | 1.0000 | 2.464224 | 11.6211 | 7.100865e-02 | 7.152430e-02 | 0.729918 | 4.958391e+00 |

## Critique Evidence Summary (Q1/Q2/Q3)

| task | n | q1_candidate_ratio_mean | q1_symbolic_ratio_mean | q2_mse_gain_mean | q2_target_mse_gain_mean | q2_rank_inversion_mean | q3_mse_gain_mean | q3_target_mse_gain_mean | q3_refit_drift_mean |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| __overall__ | 40 | 1.635848 | 1.463054 | 2.424363e-04 | 2.579907e-04 | 0.261590 | 3.000257e-02 | 3.035130e-02 | 3.694240e+00 |
| minimal | 10 | 0.985991 | 0.981008 | 0.000000e+00 | 0.000000e+00 | 0.000000 | 1.921489e-02 | 2.011136e-02 | 2.943549e+00 |
| combo | 10 | 1.738955 | 1.618086 | 3.920379e-05 | 2.725071e-05 | 0.333333 | 1.721754e-02 | 1.732053e-02 | 3.256235e+00 |
| poly_cubic | 10 | 1.678152 | 1.555770 | 3.269636e-05 | 3.645869e-05 | 0.323333 | 1.210306e-02 | 1.215104e-02 | 3.618784e+00 |
| trig_interaction | 10 | 2.140293 | 1.697352 | 8.978451e-04 | 9.682533e-04 | 0.389693 | 7.147478e-02 | 7.182228e-02 | 4.958391e+00 |

## Per-Run Performance Details

| task | seed | cache_hit | cache_status | teacher_mse | teacher_r2 | teacher_gate | candidate_s | replay_s | baseline_symbolic_s | icbr_symbolic_s | speedup_x | baseline_mse | icbr_mse | mse_shift | baseline_target_mse | icbr_target_mse | target_mse_shift | formula_ok |
|---|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| minimal | 0 | False | miss_write | 7.140631e-04 | 0.998546 | True | 0.151803 | 0.003731 | 1.664009 | 0.158988 | 10.4662 | 6.738640e-04 | 7.110225e-04 | 3.715855e-05 | 3.997566e-05 | 4.658283e-05 | 6.607163e-06 | True |
| minimal | 1 | False | miss_write | 8.472571e-04 | 0.998228 | True | 0.200686 | 0.003588 | 1.575490 | 0.207575 | 7.5900 | 8.272767e-04 | 8.611805e-04 | 3.390381e-05 | 2.000065e-05 | 2.642836e-05 | 6.427712e-06 | True |
| minimal | 2 | False | miss_write | 8.897363e-04 | 0.998102 | True | 0.199385 | 0.008733 | 1.656883 | 0.212772 | 7.7871 | 8.777932e-04 | 9.106709e-04 | 3.287772e-05 | 1.170462e-05 | 2.066297e-05 | 8.958346e-06 | True |
| minimal | 3 | False | miss_write | 8.938517e-04 | 0.998168 | True | 0.198264 | 0.003833 | 1.667700 | 0.205224 | 8.1263 | 8.711359e-04 | 8.931401e-04 | 2.200424e-05 | 2.343172e-05 | 3.357764e-05 | 1.014591e-05 | True |
| minimal | 4 | False | miss_write | 8.039999e-04 | 0.998426 | True | 0.192713 | 0.003293 | 1.624758 | 0.198908 | 8.1684 | 7.802049e-04 | 7.815711e-04 | 1.366192e-06 | 2.350566e-05 | 2.772263e-05 | 4.216965e-06 | True |
| minimal | 5 | False | miss_write | 6.951384e-04 | 0.998602 | True | 0.182352 | 0.004199 | 1.569501 | 0.190986 | 8.2179 | 6.761598e-04 | 6.782483e-04 | 2.088491e-06 | 1.846787e-05 | 1.239563e-05 | -6.072242e-06 | True |
| minimal | 6 | False | miss_write | 9.082666e-04 | 0.998199 | True | 0.156419 | 0.003572 | 1.590257 | 0.162717 | 9.7731 | 8.761874e-04 | 9.386521e-04 | 6.246474e-05 | 3.263336e-05 | 2.713455e-05 | -5.498812e-06 | True |
| minimal | 7 | False | miss_write | 7.509136e-04 | 0.998474 | True | 0.166890 | 0.003491 | 1.583035 | 0.173009 | 9.1500 | 7.390500e-04 | 7.693761e-04 | 3.032613e-05 | 1.227604e-05 | 2.217430e-05 | 9.898258e-06 | True |
| minimal | 8 | False | miss_write | 7.315540e-04 | 0.998472 | True | 0.155518 | 0.003955 | 1.669808 | 0.162555 | 10.2722 | 7.024428e-04 | 7.544573e-04 | 5.201454e-05 | 2.986476e-05 | 2.967538e-05 | -1.893804e-07 | True |
| minimal | 9 | False | miss_write | 8.633781e-04 | 0.998301 | True | 0.155250 | 0.007579 | 1.651345 | 0.167309 | 9.8700 | 8.173095e-04 | 8.606922e-04 | 4.338264e-05 | 4.509741e-05 | 4.957636e-05 | 4.478949e-06 | True |
| combo | 0 | False | miss_write | 1.062618e-04 | 0.999810 | True | 0.532529 | 0.073910 | 9.746189 | 0.638249 | 15.2702 | 2.134673e-04 | 2.525566e-04 | 3.908922e-05 | 1.343192e-04 | 1.810024e-04 | 4.668317e-05 | True |
| combo | 1 | False | miss_write | 7.166402e-05 | 0.999878 | True | 0.580554 | 0.079061 | 10.358659 | 0.690458 | 15.0026 | 5.449355e-04 | 3.662005e-04 | -1.787349e-04 | 4.408066e-04 | 3.836268e-04 | -5.717977e-05 | True |
| combo | 2 | False | miss_write | 8.699964e-05 | 0.999841 | True | 0.594646 | 0.087948 | 10.064131 | 0.715408 | 14.0677 | 2.553519e-04 | 2.614930e-04 | 6.141083e-06 | 2.459572e-04 | 2.564753e-04 | 1.051807e-05 | True |
| combo | 3 | False | miss_write | 9.052406e-05 | 0.999845 | True | 0.571386 | 0.079576 | 10.666615 | 0.682027 | 15.6396 | 2.491768e-04 | 3.052760e-04 | 5.609920e-05 | 2.224195e-04 | 2.882323e-04 | 6.581272e-05 | True |
| combo | 4 | False | miss_write | 1.302049e-04 | 0.999789 | True | 0.560233 | 0.074912 | 10.090951 | 0.663828 | 15.2011 | 1.663515e-04 | 2.012437e-04 | 3.489217e-05 | 1.095197e-04 | 1.394438e-04 | 2.992409e-05 | True |
| combo | 5 | False | miss_write | 1.022317e-04 | 0.999821 | True | 0.529971 | 0.074724 | 9.489996 | 0.632737 | 14.9983 | 6.498059e-04 | 6.380159e-04 | -1.179002e-05 | 6.688031e-04 | 6.626506e-04 | -6.152492e-06 | True |
| combo | 6 | False | miss_write | 1.030744e-04 | 0.999829 | True | 0.517871 | 0.076195 | 9.629048 | 0.623334 | 15.4477 | 2.358071e-04 | 2.935517e-04 | 5.774465e-05 | 1.739951e-04 | 2.405649e-04 | 6.656980e-05 | True |
| combo | 7 | False | miss_write | 7.618102e-05 | 0.999877 | True | 0.540913 | 0.064359 | 9.152879 | 0.633202 | 14.4549 | 4.156933e-04 | 4.706676e-04 | 5.497431e-05 | 4.005709e-04 | 4.553410e-04 | 5.477006e-05 | True |
| combo | 8 | False | miss_write | 1.047293e-04 | 0.999814 | True | 0.536502 | 0.089590 | 9.414873 | 0.660660 | 14.2507 | 2.780099e-04 | 3.251485e-04 | 4.713860e-05 | 2.174367e-04 | 2.618766e-04 | 4.443993e-05 | True |
| combo | 9 | False | miss_write | 1.307318e-04 | 0.999779 | True | 0.504712 | 0.074937 | 9.496416 | 0.610304 | 15.5601 | 1.650454e-04 | 2.300756e-04 | 6.503024e-05 | 1.381129e-04 | 1.828216e-04 | 4.470872e-05 | True |
| poly_cubic | 0 | False | miss_write | 1.971898e-04 | 0.995779 | True | 0.540941 | 0.080695 | 9.917086 | 0.653315 | 15.1796 | 3.803124e-03 | 3.879537e-03 | 7.641269e-05 | 4.211702e-03 | 4.270816e-03 | 5.911337e-05 | True |
| poly_cubic | 1 | False | miss_write | 2.208959e-04 | 0.995792 | True | 0.567262 | 0.080985 | 9.424726 | 0.681455 | 13.8303 | 3.619018e-03 | 3.684551e-03 | 6.553275e-05 | 4.105555e-03 | 4.160145e-03 | 5.459040e-05 | True |
| poly_cubic | 2 | False | miss_write | 4.400568e-04 | 0.990960 | True | 0.495375 | 0.067605 | 8.016963 | 0.591358 | 13.5569 | 3.441125e-03 | 3.429093e-03 | -1.203222e-05 | 4.254771e-03 | 4.243753e-03 | -1.101848e-05 | True |
| poly_cubic | 3 | False | miss_write | 4.574338e-04 | 0.990719 | True | 0.548865 | 0.064584 | 8.740330 | 0.641898 | 13.6164 | 3.516602e-03 | 3.535074e-03 | 1.847278e-05 | 4.417833e-03 | 4.433027e-03 | 1.519360e-05 | True |
| poly_cubic | 4 | False | miss_write | 1.944016e-04 | 0.995768 | True | 0.577583 | 0.077310 | 9.302384 | 0.686769 | 13.5451 | 2.939998e-03 | 3.132538e-03 | 1.925405e-04 | 3.326834e-03 | 3.516562e-03 | 1.897283e-04 | True |
| poly_cubic | 5 | False | miss_write | 2.636946e-04 | 0.994283 | True | 0.566706 | 0.083638 | 9.540594 | 0.682805 | 13.9726 | 2.717470e-03 | 2.916327e-03 | 1.988572e-04 | 3.094506e-03 | 3.280004e-03 | 1.854976e-04 | True |
| poly_cubic | 6 | False | miss_write | 5.207168e-04 | 0.989974 | True | 0.465844 | 0.077998 | 8.045399 | 0.576071 | 13.9660 | 3.798469e-03 | 3.745944e-03 | -5.252473e-05 | 5.035236e-03 | 4.953411e-03 | -8.182554e-05 | True |
| poly_cubic | 7 | False | miss_write | 2.268898e-04 | 0.995016 | True | 1.635384 | 0.302492 | 12.342967 | 2.056138 | 6.0030 | 3.262920e-03 | 3.446057e-03 | 1.831367e-04 | 3.761967e-03 | 3.942226e-03 | 1.802586e-04 | True |
| poly_cubic | 8 | False | miss_write | 2.437145e-04 | 0.995473 | True | 1.711056 | 0.295845 | 20.334490 | 2.124323 | 9.5722 | 3.883438e-03 | 3.974629e-03 | 9.119092e-05 | 4.386742e-03 | 4.456935e-03 | 7.019285e-05 | True |
| poly_cubic | 9 | False | miss_write | 2.868795e-04 | 0.994538 | True | 1.718483 | 0.268609 | 20.475340 | 2.098444 | 9.7574 | 3.489609e-03 | 3.714165e-03 | 2.245561e-04 | 4.075463e-03 | 4.291883e-03 | 2.164203e-04 | True |
| trig_interaction | 0 | False | miss_write | 3.960060e-03 | 0.994748 | True | 2.978829 | 1.571306 | 47.203868 | 4.889191 | 9.6547 | 3.841724e-03 | 3.736263e-03 | -1.054611e-04 | 8.799501e-03 | 8.564282e-03 | -2.352186e-04 | True |
| trig_interaction | 1 | False | miss_write | 1.170746e-03 | 0.998113 | True | 3.217385 | 2.162502 | 54.066647 | 5.836482 | 9.2636 | 8.269406e-03 | 6.691324e-03 | -1.578082e-03 | 8.301958e-03 | 6.753302e-03 | -1.548657e-03 | True |
| trig_interaction | 2 | False | miss_write | 6.734044e-03 | 0.989837 | True | 0.931165 | 0.418099 | 21.217748 | 1.440100 | 14.7335 | 5.097379e-03 | 4.159365e-03 | -9.380132e-04 | 1.171224e-02 | 1.025989e-02 | -1.452344e-03 | True |
| trig_interaction | 3 | False | miss_write | 2.789838e-03 | 0.996177 | True | 0.963484 | 0.458070 | 22.045023 | 1.516479 | 14.5370 | 2.029721e-03 | 2.408870e-03 | 3.791489e-04 | 4.028204e-03 | 4.625835e-03 | 5.976316e-04 | True |
| trig_interaction | 4 | False | miss_write | 4.315572e-03 | 0.994118 | True | 0.901278 | 0.380173 | 19.437058 | 1.367030 | 14.2185 | 2.755608e-03 | 2.831550e-03 | 7.594260e-05 | 5.385057e-03 | 5.937985e-03 | 5.529285e-04 | True |
| trig_interaction | 5 | False | miss_write | 1.623086e-03 | 0.997863 | True | 1.016365 | 0.464782 | 23.858401 | 1.579819 | 15.1020 | 5.803085e-03 | 2.993516e-03 | -2.809569e-03 | 6.947897e-03 | 4.214177e-03 | -2.733720e-03 | True |
| trig_interaction | 6 | False | miss_write | 1.032247e-02 | 0.986609 | True | 0.986328 | 0.468904 | 22.405188 | 1.557397 | 14.3863 | 3.565518e-03 | 4.115772e-03 | 5.502540e-04 | 1.413354e-02 | 1.604347e-02 | 1.909934e-03 | True |
| trig_interaction | 7 | False | miss_write | 5.634789e-03 | 0.992089 | True | 0.792571 | 0.381088 | 17.994015 | 1.254319 | 14.3456 | 1.490185e-03 | 1.418521e-03 | -7.166411e-05 | 7.506786e-03 | 7.668084e-03 | 1.612976e-04 | True |
| trig_interaction | 8 | False | miss_write | 3.710345e-03 | 0.994873 | True | 0.860994 | 0.395770 | 19.738405 | 1.343619 | 14.6905 | 2.656533e-03 | 2.540433e-03 | -1.161005e-04 | 6.333319e-03 | 6.398233e-03 | 6.491318e-05 | True |
| trig_interaction | 9 | False | miss_write | 5.634702e-03 | 0.992655 | True | 0.959605 | 0.415904 | 21.142850 | 1.464849 | 14.4335 | 2.291829e-03 | 2.244096e-03 | -4.773284e-05 | 8.298097e-03 | 8.001450e-03 | -2.966477e-04 | True |

## Formula Comparison

### task=minimal seed=0

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics: mse=7.140631e-04, r2=0.998546
- Variant formula overview:
  - baseline: symbolic_s=1.664009e+00, mse=6.738640e-04, target_mse=3.997566e-05, formula_ok=True
  - icbr_full: symbolic_s=1.589881e-01, mse=7.110225e-04, target_mse=4.658283e-05, formula_ok=True
  - icbr_no_replay: symbolic_s=1.743429e-01, mse=7.110225e-04, target_mse=4.658283e-05, formula_ok=True
  - icbr_no_shared: symbolic_s=1.770157e-01, mse=7.110225e-04, target_mse=4.658283e-05, formula_ok=True
  - icbr_refit_commit: symbolic_s=2.118476e-01, mse=2.109121e-02, target_mse=2.180224e-02, formula_ok=True
- baseline formula (display, rounded):
  - `0.99273*sin(3.13696*x_1 - 0.00288001) - 0.0037792`
- icbr_full formula (display, rounded):
  - `0.995071*sin(3.15*x_1 + 2.38419e-7) - 0.00368373`
- icbr_no_replay formula (display, rounded):
  - `0.995071*sin(3.15*x_1 + 2.38419e-7) - 0.00368373`
- icbr_no_shared formula (display, rounded):
  - `0.995071*sin(3.15*x_1 + 2.38419e-7) - 0.00368373`
- icbr_refit_commit formula (display, rounded):
  - `0.0020642 - 0.887012*sin(2.86052*x_1 + 2.98728)`

### task=minimal seed=1

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics: mse=8.472571e-04, r2=0.998228
- Variant formula overview:
  - baseline: symbolic_s=1.575490e+00, mse=8.272767e-04, target_mse=2.000065e-05, formula_ok=True
  - icbr_full: symbolic_s=2.075751e-01, mse=8.611805e-04, target_mse=2.642836e-05, formula_ok=True
  - icbr_no_replay: symbolic_s=1.948572e-01, mse=8.611805e-04, target_mse=2.642836e-05, formula_ok=True
  - icbr_no_shared: symbolic_s=1.674739e-01, mse=8.611805e-04, target_mse=2.642836e-05, formula_ok=True
  - icbr_refit_commit: symbolic_s=2.048908e-01, mse=1.918056e-02, target_mse=1.917513e-02, formula_ok=True
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
- Teacher target metrics: mse=8.897363e-04, r2=0.998102
- Variant formula overview:
  - baseline: symbolic_s=1.656883e+00, mse=8.777932e-04, target_mse=1.170462e-05, formula_ok=True
  - icbr_full: symbolic_s=2.127718e-01, mse=9.106709e-04, target_mse=2.066297e-05, formula_ok=True
  - icbr_no_replay: symbolic_s=1.897696e-01, mse=9.106709e-04, target_mse=2.066297e-05, formula_ok=True
  - icbr_no_shared: symbolic_s=1.801698e-01, mse=9.106709e-04, target_mse=2.066297e-05, formula_ok=True
  - icbr_refit_commit: symbolic_s=2.515581e-01, mse=1.912194e-02, target_mse=1.890385e-02, formula_ok=True
- baseline formula (display, rounded):
  - `0.00175362 - 0.996562*cos(3.1372*x_1 + 1.57232)`
- icbr_full formula (display, rounded):
  - `0.998783*sin(3.15*x_1 + 2.38419e-7) + 0.00193121`
- icbr_no_replay formula (display, rounded):
  - `0.998783*sin(3.15*x_1 + 2.38419e-7) + 0.00193121`
- icbr_no_shared formula (display, rounded):
  - `0.998783*sin(3.15*x_1 + 2.38419e-7) + 0.00193121`
- icbr_refit_commit formula (display, rounded):
  - `0.884366*sin(2.84976*x_1 - 0.0981599) + 0.00382307`

### task=minimal seed=3

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics: mse=8.938517e-04, r2=0.998168
- Variant formula overview:
  - baseline: symbolic_s=1.667700e+00, mse=8.711359e-04, target_mse=2.343172e-05, formula_ok=True
  - icbr_full: symbolic_s=2.052236e-01, mse=8.931401e-04, target_mse=3.357764e-05, formula_ok=True
  - icbr_no_replay: symbolic_s=1.930735e-01, mse=8.931401e-04, target_mse=3.357764e-05, formula_ok=True
  - icbr_no_shared: symbolic_s=2.171752e-01, mse=8.931401e-04, target_mse=3.357764e-05, formula_ok=True
  - icbr_refit_commit: symbolic_s=2.410580e-01, mse=1.930612e-02, target_mse=1.925699e-02, formula_ok=True
- baseline formula (display, rounded):
  - `0.994851*cos(3.13816*x_1 - 1.57144) - 0.00299206`
- icbr_full formula (display, rounded):
  - `0.996451*sin(3.15*x_1 + 2.38419e-7) - 0.00303188`
- icbr_no_replay formula (display, rounded):
  - `0.996451*sin(3.15*x_1 + 2.38419e-7) - 0.00303188`
- icbr_no_shared formula (display, rounded):
  - `0.996451*sin(3.15*x_1 + 2.38419e-7) - 0.00303188`
- icbr_refit_commit formula (display, rounded):
  - `0.0171289 - 0.901929*sin(2.86028*x_1 + 3.01384)`

### task=minimal seed=4

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics: mse=8.039999e-04, r2=0.998426
- Variant formula overview:
  - baseline: symbolic_s=1.624758e+00, mse=7.802049e-04, target_mse=2.350566e-05, formula_ok=True
  - icbr_full: symbolic_s=1.989080e-01, mse=7.815711e-04, target_mse=2.772263e-05, formula_ok=True
  - icbr_no_replay: symbolic_s=1.561154e-01, mse=7.815711e-04, target_mse=2.772263e-05, formula_ok=True
  - icbr_no_shared: symbolic_s=1.667716e-01, mse=7.815711e-04, target_mse=2.772263e-05, formula_ok=True
  - icbr_refit_commit: symbolic_s=2.146954e-01, mse=1.697818e-02, target_mse=1.635773e-02, formula_ok=True
- baseline formula (display, rounded):
  - `-0.995812*cos(3.14792*x_1 + 1.56968) - 0.00174834`
- icbr_full formula (display, rounded):
  - `0.996128*sin(3.15*x_1 + 2.38419e-7) - 0.00179093`
- icbr_no_replay formula (display, rounded):
  - `0.996128*sin(3.15*x_1 + 2.38419e-7) - 0.00179093`
- icbr_no_shared formula (display, rounded):
  - `0.996128*sin(3.15*x_1 + 2.38419e-7) - 0.00179093`
- icbr_refit_commit formula (display, rounded):
  - `0.0126343 - 0.908002*sin(2.87116*x_1 + 3.01572)`

### task=minimal seed=5

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics: mse=6.951384e-04, r2=0.998602
- Variant formula overview:
  - baseline: symbolic_s=1.569501e+00, mse=6.761598e-04, target_mse=1.846787e-05, formula_ok=True
  - icbr_full: symbolic_s=1.909857e-01, mse=6.782483e-04, target_mse=1.239563e-05, formula_ok=True
  - icbr_no_replay: symbolic_s=1.488593e-01, mse=6.782483e-04, target_mse=1.239563e-05, formula_ok=True
  - icbr_no_shared: symbolic_s=1.522449e-01, mse=6.782483e-04, target_mse=1.239563e-05, formula_ok=True
  - icbr_refit_commit: symbolic_s=1.918304e-01, mse=1.462230e-02, target_mse=1.357301e-02, formula_ok=True
- baseline formula (display, rounded):
  - `-1.0003*cos(3.15128*x_1 + 1.56888) - 0.00114839`
- icbr_full formula (display, rounded):
  - `1.00005*sin(3.15*x_1 + 2.38419e-7) - 0.00130564`
- icbr_no_replay formula (display, rounded):
  - `1.00005*sin(3.15*x_1 + 2.38419e-7) - 0.00130564`
- icbr_no_shared formula (display, rounded):
  - `1.00005*sin(3.15*x_1 + 2.38419e-7) - 0.00130564`
- icbr_refit_commit formula (display, rounded):
  - `0.924051*sin(2.87668*x_1 - 0.10732) + 0.0169701`

### task=minimal seed=6

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics: mse=9.082666e-04, r2=0.998199
- Variant formula overview:
  - baseline: symbolic_s=1.590257e+00, mse=8.761874e-04, target_mse=3.263336e-05, formula_ok=True
  - icbr_full: symbolic_s=1.627173e-01, mse=9.386521e-04, target_mse=2.713455e-05, formula_ok=True
  - icbr_no_replay: symbolic_s=1.504624e-01, mse=9.386521e-04, target_mse=2.713455e-05, formula_ok=True
  - icbr_no_shared: symbolic_s=1.889663e-01, mse=9.386521e-04, target_mse=2.713455e-05, formula_ok=True
  - icbr_refit_commit: symbolic_s=2.151444e-01, mse=2.335219e-02, target_mse=2.423368e-02, formula_ok=True
- baseline formula (display, rounded):
  - `-0.993571*cos(3.132*x_1 + 1.57304) - 0.000823403`
- icbr_full formula (display, rounded):
  - `0.996284*sin(3.15*x_1 + 2.38419e-7) - 0.000665273`
- icbr_no_replay formula (display, rounded):
  - `0.996284*sin(3.15*x_1 + 2.38419e-7) - 0.000665273`
- icbr_no_shared formula (display, rounded):
  - `0.996284*sin(3.15*x_1 + 2.38419e-7) - 0.000665273`
- icbr_refit_commit formula (display, rounded):
  - `-0.891787*sin(2.80552*x_1 - 3.0078) - 0.0138932`

### task=minimal seed=7

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics: mse=7.509136e-04, r2=0.998474
- Variant formula overview:
  - baseline: symbolic_s=1.583035e+00, mse=7.390500e-04, target_mse=1.227604e-05, formula_ok=True
  - icbr_full: symbolic_s=1.730090e-01, mse=7.693761e-04, target_mse=2.217430e-05, formula_ok=True
  - icbr_no_replay: symbolic_s=1.821014e-01, mse=7.693761e-04, target_mse=2.217430e-05, formula_ok=True
  - icbr_no_shared: symbolic_s=2.101386e-01, mse=7.693761e-04, target_mse=2.217430e-05, formula_ok=True
  - icbr_refit_commit: symbolic_s=2.210585e-01, mse=2.034030e-02, target_mse=2.026269e-02, formula_ok=True
- baseline formula (display, rounded):
  - `0.995472*cos(3.13744*x_1 - 1.57192) - 0.001136`
- icbr_full formula (display, rounded):
  - `0.997666*sin(3.15*x_1 + 2.38419e-7) - 0.000993971`
- icbr_no_replay formula (display, rounded):
  - `0.997666*sin(3.15*x_1 + 2.38419e-7) - 0.000993971`
- icbr_no_shared formula (display, rounded):
  - `0.997666*sin(3.15*x_1 + 2.38419e-7) - 0.000993971`
- icbr_refit_commit formula (display, rounded):
  - `-0.893728*sin(2.8406*x_1 - 3.02152) - 0.0095598`

### task=minimal seed=8

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics: mse=7.315540e-04, r2=0.998472
- Variant formula overview:
  - baseline: symbolic_s=1.669808e+00, mse=7.024428e-04, target_mse=2.986476e-05, formula_ok=True
  - icbr_full: symbolic_s=1.625553e-01, mse=7.544573e-04, target_mse=2.967538e-05, formula_ok=True
  - icbr_no_replay: symbolic_s=1.571993e-01, mse=7.544573e-04, target_mse=2.967538e-05, formula_ok=True
  - icbr_no_shared: symbolic_s=1.571701e-01, mse=7.544573e-04, target_mse=2.967538e-05, formula_ok=True
  - icbr_refit_commit: symbolic_s=2.001335e-01, mse=2.418231e-02, target_mse=2.508470e-02, formula_ok=True
- baseline formula (display, rounded):
  - `6.8929e-5 - 0.993013*cos(3.13456*x_1 + 1.57384)`
- icbr_full formula (display, rounded):
  - `0.995953*sin(3.15*x_1 + 2.38419e-7) - 0.000672042`
- icbr_no_replay formula (display, rounded):
  - `0.995953*sin(3.15*x_1 + 2.38419e-7) - 0.000672042`
- icbr_no_shared formula (display, rounded):
  - `0.995953*sin(3.15*x_1 + 2.38419e-7) - 0.000672042`
- icbr_refit_commit formula (display, rounded):
  - `0.00725783 - 0.873158*sin(2.84396*x_1 + 3.2968)`

### task=minimal seed=9

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics: mse=8.633781e-04, r2=0.998301
- Variant formula overview:
  - baseline: symbolic_s=1.651345e+00, mse=8.173095e-04, target_mse=4.509741e-05, formula_ok=True
  - icbr_full: symbolic_s=1.673094e-01, mse=8.606922e-04, target_mse=4.957636e-05, formula_ok=True
  - icbr_no_replay: symbolic_s=1.587935e-01, mse=8.606922e-04, target_mse=4.957636e-05, formula_ok=True
  - icbr_no_shared: symbolic_s=1.683934e-01, mse=8.606922e-04, target_mse=4.957636e-05, formula_ok=True
  - icbr_refit_commit: symbolic_s=2.105813e-01, mse=2.213277e-02, target_mse=2.275954e-02, formula_ok=True
- baseline formula (display, rounded):
  - `0.991148*sin(3.1348*x_1 + 0.000800001) + 0.00237748`
- icbr_full formula (display, rounded):
  - `0.993361*sin(3.15*x_1 + 2.38419e-7) + 0.00207416`
- icbr_no_replay formula (display, rounded):
  - `0.993361*sin(3.15*x_1 + 2.38419e-7) + 0.00207416`
- icbr_no_shared formula (display, rounded):
  - `0.993361*sin(3.15*x_1 + 2.38419e-7) + 0.00207416`
- icbr_refit_commit formula (display, rounded):
  - `0.0196009 - 0.899563*sin(2.8064*x_1 + 3.02088)`

### task=combo seed=0

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics: mse=1.062618e-04, r2=0.999810
- Variant formula overview:
  - baseline: symbolic_s=9.746189e+00, mse=2.134673e-04, target_mse=1.343192e-04, formula_ok=True
  - icbr_full: symbolic_s=6.382493e-01, mse=2.525566e-04, target_mse=1.810024e-04, formula_ok=True
  - icbr_no_replay: symbolic_s=5.623751e-01, mse=2.532688e-04, target_mse=1.835680e-04, formula_ok=True
  - icbr_no_shared: symbolic_s=1.032088e+00, mse=2.525560e-04, target_mse=1.810027e-04, formula_ok=True
  - icbr_refit_commit: symbolic_s=9.152121e-01, mse=2.306796e-02, target_mse=2.302083e-02, formula_ok=True
- baseline formula (display, rounded):
  - `21.7247*(-0.0126544*sin(3.18976*x_1 + 0.01152) + 0.0159854*cos(1.5036*x_2 + 6.39656) - 1)**2 + 1.51214*asin(0.216099*(0.143021 - x_2)**2 + 0.293675*cos(3.0852*x_1 - 1.58576) - 0.192755) - 20.7568`
- icbr_full formula (display, rounded):
  - `-31.3629*(-0.00600714*cos(3.2*x_1 - 1.55) - 1 + 0.0204798*exp(-0.4225*(-x_2 - 0.0769234)**2))**3 - 2.23782*tan(-0.145852*(x_2 - 0.142857)**2 + 0.198618*cos(3.1*x_1 + 1.55) + 0.153539) - 29.1434`
- icbr_no_replay formula (display, rounded):
  - `-31.3629*(-0.00600714*cos(3.2*x_1 - 1.55) - 1 + 0.0204798*exp(-0.4225*(-x_2 - 0.0769234)**2))**3 - 1.42563*asin(-0.229196*(x_2 - 0.142857)**2 + 0.312114*cos(3.1*x_1 + 1.55) + 0.184132) - 29.226`
- icbr_no_shared formula (display, rounded):
  - `31.3629*(0.00600714*cos(3.2*x_1 - 1.55) + 1 - 0.0204798*exp(-0.4225*(-x_2 - 0.0769234)**2))**3 - 2.23782*tan(-0.145852*(x_2 - 0.142857)**2 + 0.198618*cos(3.1*x_1 + 1.55) + 0.153539) - 29.1434`
- icbr_refit_commit formula (display, rounded):
  - `16.3952*(0.0197629*cos(2.8606*x_1 - 1.72484) + 1 - 0.0464859*exp(-0.81*(-x_2 - 0.0822221)**2))**(3/2) - 2.18754*tan(0.182424*sin(2.81104*x_1 + 3.0088) + 0.699394*cos(0.6666*x_2 - 0.0940399) - 0.54597) - 14.9469`

### task=combo seed=1

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics: mse=7.166402e-05, r2=0.999878
- Variant formula overview:
  - baseline: symbolic_s=1.035866e+01, mse=5.449355e-04, target_mse=4.408066e-04, formula_ok=True
  - icbr_full: symbolic_s=6.904579e-01, mse=3.662005e-04, target_mse=3.836268e-04, formula_ok=True
  - icbr_no_replay: symbolic_s=5.722635e-01, mse=6.096711e-04, target_mse=5.238181e-04, formula_ok=True
  - icbr_no_shared: symbolic_s=1.141839e+00, mse=3.662005e-04, target_mse=3.836268e-04, formula_ok=True
  - icbr_refit_commit: symbolic_s=9.769113e-01, mse=2.139043e-02, target_mse=2.171545e-02, formula_ok=True
- baseline formula (display, rounded):
  - `3.27465*cos(-0.0866122*(0.086219 - x_2)**4 + 0.149532*cos(3.11904*x_1 + 1.57488) + 7.53244) + 5.29898*acos(-0.100087*sin(3.16192*x_1 - 0.00432001) - 0.411964 + 0.306603*exp(-0.571536*(-x_2 - 0.0467725)**2)) - 9.9053`
- icbr_full formula (display, rounded):
  - `23.7435*(-0.00570886*sin(3.15*x_1 + 2.38419e-7) - 0.00593762*cos(1.85*x_2 - 3.05) - 1)**4 - 3.51963*cos(0.0766841*(x_2 - 0.131579)**2 + 0.139514*sin(3.1*x_1 + 2.38419e-7) - 4.38079) - 24.3513`
- icbr_no_replay formula (display, rounded):
  - `-4.87671*acos(0.108954*sin(3.15*x_1 + 2.38419e-7) + 0.11332*cos(1.85*x_2 - 3.05) + 0.185078) + 3.42913*atan(0.0811392*(x_2 - 0.0860215)**4 + 0.139514*sin(3.1*x_1 + 2.38419e-7) + 0.178607) + 6.71507`
- icbr_no_shared formula (display, rounded):
  - `23.7435*(-0.00570886*sin(3.15*x_1 + 2.38419e-7) - 0.00593762*cos(1.85*x_2 - 3.05) - 1)**4 - 3.51963*cos(0.0766841*(x_2 - 0.131579)**2 + 0.139514*sin(3.1*x_1 + 2.38419e-7) - 4.38079) - 24.3513`
- icbr_refit_commit formula (display, rounded):
  - `23.5423*(0.0051912*sin(2.84388*x_1 - 3.01844) - 1 + 0.0106714*exp(-1.21*(-x_2 - 0.0581818)**2))**4 - 3.0914*cos(-0.140423*sin(2.7944*x_1 + 0.10332) + 0.49451*sin(0.60076*x_2 - 4.7898) + 3.93152) - 23.481`

### task=combo seed=2

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics: mse=8.699964e-05, r2=0.999841
- Variant formula overview:
  - baseline: symbolic_s=1.006413e+01, mse=2.553519e-04, target_mse=2.459572e-04, formula_ok=True
  - icbr_full: symbolic_s=7.154082e-01, mse=2.614930e-04, target_mse=2.564753e-04, formula_ok=True
  - icbr_no_replay: symbolic_s=5.645399e-01, mse=3.277135e-04, target_mse=3.124520e-04, formula_ok=True
  - icbr_no_shared: symbolic_s=1.034548e+00, mse=2.614930e-04, target_mse=2.564753e-04, formula_ok=True
  - icbr_refit_commit: symbolic_s=9.264958e-01, mse=1.485424e-02, target_mse=1.484148e-02, formula_ok=True
- baseline formula (display, rounded):
  - `-281.396*(0.00066894*sin(3.18384*x_1 - 9.39392) - 0.000781474*cos(1.63264*x_2 - 2.99656) + 1)**3 + 2.81567*acos(-0.0994283*(0.212468 - x_2)**2 - 0.153328*cos(3.08752*x_1 - 1.60912) + 0.0291618) + 277.682`
- icbr_full formula (display, rounded):
  - `0.566782*cos(3.2*x_1 - 1.55) + 0.682073*cos(1.6*x_2 - 3.0) - 3.91334*tan(-0.0715268*(0.2125 - x_2)**2 + 0.110551*cos(3.1*x_1 + 1.55) + 0.0373908) + 0.795906`
- icbr_no_replay formula (display, rounded):
  - `0.566782*cos(3.2*x_1 - 1.55) + 0.682073*cos(1.6*x_2 - 3.0) - 3.1312*acos(0.0894085*(0.2125 - x_2)**2 + 0.138168*sin(3.1*x_1 - 0.0499997) + 0.00328546) + 5.55693`
- icbr_no_shared formula (display, rounded):
  - `0.566782*cos(3.2*x_1 - 1.55) + 0.682073*cos(1.6*x_2 - 3.0) - 3.91334*tan(-0.0715268*(0.2125 - x_2)**2 + 0.110551*cos(3.1*x_1 + 1.55) + 0.0373908) + 0.795906`
- icbr_refit_commit formula (display, rounded):
  - `0.501698*cos(2.90284*x_1 - 1.41252) - 0.968867*cos(1.29996*x_2 + 0.108) + 3.76398*tan(0.102933*sin(2.80484*x_1 - 0.1172) - 0.165605*cos(0.99936*x_2 - 0.20836) + 0.128645) + 1.06947`

### task=combo seed=3

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics: mse=9.052406e-05, r2=0.999845
- Variant formula overview:
  - baseline: symbolic_s=1.066661e+01, mse=2.491768e-04, target_mse=2.224195e-04, formula_ok=True
  - icbr_full: symbolic_s=6.820269e-01, mse=3.052760e-04, target_mse=2.882323e-04, formula_ok=True
  - icbr_no_replay: symbolic_s=5.429325e-01, mse=3.418499e-04, target_mse=3.252746e-04, formula_ok=True
  - icbr_no_shared: symbolic_s=1.296792e+00, mse=3.052760e-04, target_mse=2.882323e-04, formula_ok=True
  - icbr_refit_commit: symbolic_s=9.961573e-01, mse=1.562561e-02, target_mse=1.576841e-02, formula_ok=True
- baseline formula (display, rounded):
  - `1.60973*acos(-0.165261*(0.127387 - x_2)**2 + 0.269875*sin(3.10744*x_1 + 9.41232) + 0.0990161) + 4.10577*acos(-0.135643*sin(3.16648*x_1 + 0.00984) - 0.391378 + 0.420023*exp(-0.518399*(-x_2 - 0.0512222)**2)) - 8.71637`
- icbr_full formula (display, rounded):
  - `3.98706*acos(-0.139223*sin(3.15*x_1 + 2.38419e-7) - 0.147688*cos(1.75*x_2 - 3.05) - 0.127577) + 2.20639*atanh(0.120688*(0.126761 - x_2)**2 + 0.196737*sin(3.1*x_1 + 2.38419e-7) - 0.0543156) - 6.08037`
- icbr_no_replay formula (display, rounded):
  - `1.71607*acos(-0.15517*(0.126761 - x_2)**2 + 0.252868*cos(3.1*x_1 + 1.55) + 0.119499) + 3.98706*asin(0.139223*sin(3.15*x_1 + 2.38419e-7) + 0.147688*cos(1.75*x_2 - 3.05) + 0.127577) - 2.42577`
- icbr_no_shared formula (display, rounded):
  - `3.98706*acos(-0.139223*sin(3.15*x_1 + 2.38419e-7) - 0.147688*cos(1.75*x_2 - 3.05) - 0.127577) + 2.20639*atanh(0.120688*(0.126761 - x_2)**2 + 0.196737*sin(3.1*x_1 + 2.38419e-7) - 0.0543156) - 6.08037`
- icbr_refit_commit formula (display, rounded):
  - `-1.53762*acos(0.172197*(0.129168 - x_2)**2 + 0.25624*cos(2.81024*x_1 + 4.60476) - 0.0736255) - 4.4627*asin(0.112517*sin(2.85188*x_1 - 3.00996) + 0.112587*sin(1.94504*x_2 - 4.59772) - 0.0920508) + 2.60017`

### task=combo seed=4

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics: mse=1.302049e-04, r2=0.999789
- Variant formula overview:
  - baseline: symbolic_s=1.009095e+01, mse=1.663515e-04, target_mse=1.095197e-04, formula_ok=True
  - icbr_full: symbolic_s=6.638284e-01, mse=2.012437e-04, target_mse=1.394438e-04, formula_ok=True
  - icbr_no_replay: symbolic_s=5.222157e-01, mse=2.012437e-04, target_mse=1.394438e-04, formula_ok=True
  - icbr_no_shared: symbolic_s=1.057883e+00, mse=2.012437e-04, target_mse=1.394438e-04, formula_ok=True
  - icbr_refit_commit: symbolic_s=9.292957e-01, mse=1.291576e-02, target_mse=1.284017e-02, formula_ok=True
- baseline formula (display, rounded):
  - `-1.02081*acos(0.292349*(0.0959583 - x_2)**2 + 0.412969*cos(3.06624*x_1 - 1.59904) - 0.238143) - 5.14512*atan(0.111434*cos(3.19392*x_1 + 1.58936) - 0.236223 + 0.428209*exp(-0.369275*(-x_2 - 0.0467351)**2)) + 2.82012`
- icbr_full formula (display, rounded):
  - `4.10755*cos(0.178053*sin(1.5*x_2 - 1.5) + 0.140036*cos(3.2*x_1 - 1.55) + 4.61431) - 1.45836*atanh(-0.204683*(0.0957447 - x_2)**2 + 0.288364*cos(3.05*x_1 + 1.55) + 0.180012) + 1.37994`
- icbr_no_replay formula (display, rounded):
  - `4.10755*cos(0.178053*sin(1.5*x_2 - 1.5) + 0.140036*cos(3.2*x_1 - 1.55) + 4.61431) - 1.45836*atanh(-0.204683*(0.0957447 - x_2)**2 + 0.288364*cos(3.05*x_1 + 1.55) + 0.180012) + 1.37994`
- icbr_no_shared formula (display, rounded):
  - `4.10755*cos(0.178053*sin(1.5*x_2 - 1.5) + 0.140036*cos(3.2*x_1 - 1.55) + 4.61431) - 1.45836*atanh(-0.204683*(0.0957447 - x_2)**2 + 0.288364*cos(3.05*x_1 + 1.55) + 0.180012) + 1.37994`
- icbr_refit_commit formula (display, rounded):
  - `-4.82106*cos(-0.145427*(-x_2 - 0.0447782)**2 + 0.108545*cos(2.91128*x_1 + 1.7092) + 5.00372) - 1.21852*acos(-0.319956*sin(2.76696*x_1 + 3.01332) - 0.52881*cos(1.00216*x_2 - 0.0918799) + 0.271129) + 3.62129`

### task=combo seed=5

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics: mse=1.022317e-04, r2=0.999821
- Variant formula overview:
  - baseline: symbolic_s=9.489996e+00, mse=6.498059e-04, target_mse=6.688031e-04, formula_ok=True
  - icbr_full: symbolic_s=6.327370e-01, mse=6.380159e-04, target_mse=6.626506e-04, formula_ok=True
  - icbr_no_replay: symbolic_s=5.759907e-01, mse=6.660214e-04, target_mse=6.882849e-04, formula_ok=True
  - icbr_no_shared: symbolic_s=9.845489e-01, mse=6.380159e-04, target_mse=6.626506e-04, formula_ok=True
  - icbr_refit_commit: symbolic_s=8.793964e-01, mse=1.271808e-02, target_mse=1.276061e-02, formula_ok=True
- baseline formula (display, rounded):
  - `-1.17282*atan(-0.139644*(0.215017 - x_2)**2 + 0.359693*sin(3.11464*x_1 + 9.38912) + 0.0754018) - 3.40528*atanh(0.171366*cos(3.16432*x_1 + 1.59712) - 0.341059 + 0.44572*exp(-0.7396*(-x_2 - 0.0455814)**2)) + 0.410104`
- icbr_full formula (display, rounded):
  - `2.55344*acos(-0.228557*cos(3.15*x_1 - 1.55) - 0.226583*cos(1.95*x_2 - 3.05) - 0.101064) - 4.81718 + 1.98729*exp(-0.599234*(0.124135*(0.215054 - x_2)**2 - 0.318914*cos(3.1*x_1 + 1.55) - 1)**2)`
- icbr_no_replay formula (display, rounded):
  - `3.39838*atanh(0.171418*cos(3.15*x_1 - 1.55) + 0.169937*cos(1.95*x_2 - 3.05) + 0.0632975) - 0.762902 + 1.98729*exp(-0.598033*(0.12426*(0.215054 - x_2)**2 + 0.319692*sin(3.1*x_1 - 0.0499997) - 1)**2)`
- icbr_no_shared formula (display, rounded):
  - `2.55344*acos(-0.228557*cos(3.15*x_1 - 1.55) - 0.226583*cos(1.95*x_2 - 3.05) - 0.101064) - 4.81718 + 1.98729*exp(-0.599234*(0.124135*(0.215054 - x_2)**2 - 0.318914*cos(3.1*x_1 + 1.55) - 1)**2)`
- icbr_refit_commit formula (display, rounded):
  - `2.55379*acos(0.208415*cos(2.86804*x_1 - 4.6086) - 0.297839 + 0.431886*exp(-1.21*(-x_2 - 0.0527272)**2)) - 1.12656*atan(-0.160492*(0.12041 - x_2)**4 + 0.349904*sin(2.82988*x_1 + 3.00972) + 0.0352639) - 3.6601`

### task=combo seed=6

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics: mse=1.030744e-04, r2=0.999829
- Variant formula overview:
  - baseline: symbolic_s=9.629048e+00, mse=2.358071e-04, target_mse=1.739951e-04, formula_ok=True
  - icbr_full: symbolic_s=6.233337e-01, mse=2.935517e-04, target_mse=2.405649e-04, formula_ok=True
  - icbr_no_replay: symbolic_s=5.305837e-01, mse=2.964392e-04, target_mse=2.407034e-04, formula_ok=True
  - icbr_no_shared: symbolic_s=1.019464e+00, mse=2.942752e-04, target_mse=2.402019e-04, formula_ok=True
  - icbr_refit_commit: symbolic_s=9.363653e-01, mse=2.246771e-02, target_mse=2.255411e-02, formula_ok=True
- baseline formula (display, rounded):
  - `19.8098*(0.00710678*(0.205738 - x_2)**2 + 0.0111287*cos(3.07944*x_1 - 1.598) + 1)**2 + 3.8752*asin(-0.142892*sin(3.1908*x_1 - 9.40416) + 0.184556*cos(1.5476*x_2 - 3.00808) + 0.0931507) - 19.4849`
- icbr_full formula (display, rounded):
  - `14.8807*(0.0902827*sin(0.55*x_2 + 4.6) - 0.0207747*cos(3.1*x_1 + 1.55) + 1)**(3/2) + 5.04964*atanh(0.109728*cos(3.2*x_1 - 1.55) + 0.133944*cos(1.6*x_2 - 3.0) + 0.0722943) - 12.6316`
- icbr_no_replay formula (display, rounded):
  - `19.045*(0.00737482*(0.206897 - x_2)**2 - 0.011611*cos(3.1*x_1 + 1.55) + 1)**2 + 5.04964*atanh(0.109728*cos(3.2*x_1 - 1.55) + 0.133944*cos(1.6*x_2 - 3.0) + 0.0722943) - 18.7637`
- icbr_no_shared formula (display, rounded):
  - `14.8807*(0.0902827*sin(0.55*x_2 + 4.6) - 0.0207747*cos(3.1*x_1 + 1.55) + 1)**(3/2) + 6.75005*tan(0.0822963*cos(3.2*x_1 - 1.55) + 0.100458*cos(1.6*x_2 - 3.0) + 3.19172) - 12.6039`
- icbr_refit_commit formula (display, rounded):
  - `21.5108*(0.00939533*sin(2.8004*x_1 + 0.0947999) - 0.0145787*cos(0.99968*x_2 - 0.20844) + 1)**2 + 4.67829*atanh(0.104956*cos(2.8554*x_1 - 1.41564) + 0.176258 - 0.264119*exp(-0.81*(-x_2 - 0.0888888)**2)) - 20.5329`

### task=combo seed=7

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics: mse=7.618102e-05, r2=0.999877
- Variant formula overview:
  - baseline: symbolic_s=9.152879e+00, mse=4.156933e-04, target_mse=4.005709e-04, formula_ok=True
  - icbr_full: symbolic_s=6.332018e-01, mse=4.706676e-04, target_mse=4.553410e-04, formula_ok=True
  - icbr_no_replay: symbolic_s=5.183510e-01, mse=4.817897e-04, target_mse=4.621422e-04, formula_ok=True
  - icbr_no_shared: symbolic_s=9.992570e-01, mse=4.706676e-04, target_mse=4.553410e-04, formula_ok=True
  - icbr_refit_commit: symbolic_s=8.838657e-01, mse=1.795800e-02, target_mse=1.794523e-02, formula_ok=True
- baseline formula (display, rounded):
  - `3.41442*asin(0.174005*sin(1.78904*x_2 - 1.41216) - 0.16312*cos(3.16992*x_1 + 1.5816) + 0.0689995) - 2.5169*atan(-0.099045*(0.244418 - x_2)**2 + 0.176164*sin(3.10864*x_1 + 9.4108) + 0.0927017) + 0.551541`
- icbr_full formula (display, rounded):
  - `5.01997*tan(-0.117234*sin(1.8*x_2 - 4.55) + 0.110625*cos(3.15*x_1 - 1.55) + 3.19265) - 2.72276*atan(0.617802*sin(0.55*x_2 - 4.85) + 0.162532*cos(3.1*x_1 + 1.55) - 0.516523) + 0.566009`
- icbr_no_replay formula (display, rounded):
  - `-1.81516*sin(-0.137284*(0.244444 - x_2)**2 + 0.243798*cos(3.1*x_1 + 1.55) + 0.126542) + 5.01897*atanh(-0.117234*sin(1.8*x_2 - 4.55) + 0.110625*cos(3.15*x_1 - 1.55) + 0.0426485) + 0.563735`
- icbr_no_shared formula (display, rounded):
  - `5.01997*tan(-0.117234*sin(1.8*x_2 - 4.55) + 0.110625*cos(3.15*x_1 - 1.55) + 3.19265) - 2.72276*atan(0.617802*sin(0.55*x_2 - 4.85) + 0.162532*cos(3.1*x_1 + 1.55) - 0.516523) + 0.566009`
- icbr_refit_commit formula (display, rounded):
  - `2.73229*tanh(0.0928347*(0.235065 - x_2)**2 + 0.145864*cos(2.83632*x_1 + 4.79448) - 0.0999837) - 3.80613*asin(0.131334*cos(2.8914*x_1 + 1.71092) + 0.264103*cos(1.3*x_2 + 0.108) - 0.178622) + 0.559623`

### task=combo seed=8

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics: mse=1.047293e-04, r2=0.999814
- Variant formula overview:
  - baseline: symbolic_s=9.414873e+00, mse=2.780099e-04, target_mse=2.174367e-04, formula_ok=True
  - icbr_full: symbolic_s=6.606596e-01, mse=3.251485e-04, target_mse=2.618766e-04, formula_ok=True
  - icbr_no_replay: symbolic_s=5.092320e-01, mse=3.269182e-04, target_mse=2.634657e-04, formula_ok=True
  - icbr_no_shared: symbolic_s=1.015972e+00, mse=3.251485e-04, target_mse=2.618766e-04, formula_ok=True
  - icbr_refit_commit: symbolic_s=9.192562e-01, mse=1.836349e-02, target_mse=1.849983e-02, formula_ok=True
- baseline formula (display, rounded):
  - `-2.58275*acos(0.118044*(0.159859 - x_2)**2 - 0.171895*sin(3.10704*x_1 + 9.40424) - 0.11758) + 3.16879*acos(0.172994*sin(3.16736*x_1 - 9.40936) - 0.466453 + 0.553307*exp(-0.479417*(-x_2 - 0.0744078)**2)) - 0.362209`
- icbr_full formula (display, rounded):
  - `3.27988*asin(0.166601*cos(3.15*x_1 - 1.55) + 0.453917 - 0.526747*exp(-0.49*(-x_2 - 0.0714288)**2)) - 3.95405*atanh(0.778622*sin(0.45*x_2 + 1.5) + 0.112176*cos(3.1*x_1 + 1.55) - 0.693474) + 0.553664`
- icbr_no_replay formula (display, rounded):
  - `-3.95421*tan(-0.077114*(0.16 - x_2)**2 + 0.112176*cos(3.1*x_1 + 1.55) + 0.0849198) + 3.27988*acos(-0.166601*cos(3.15*x_1 - 1.55) - 0.453917 + 0.526747*exp(-0.49*(-x_2 - 0.0714288)**2)) - 4.59836`
- icbr_no_shared formula (display, rounded):
  - `3.27988*asin(0.166601*cos(3.15*x_1 - 1.55) + 0.453917 - 0.526747*exp(-0.49*(-x_2 - 0.0714288)**2)) - 3.95405*atanh(0.778622*sin(0.45*x_2 + 1.5) + 0.112176*cos(3.1*x_1 + 1.55) - 0.693474) + 0.553664`
- icbr_refit_commit formula (display, rounded):
  - `-3.41783*acos(-0.210329*sin(1.49788*x_2 - 4.59176) + 0.140068*cos(2.84408*x_1 - 1.4156) + 0.146499) + 3.96061*atanh(0.100402*cos(2.79872*x_1 - 1.70496) - 0.475245*cos(0.57448*x_2 - 0.0956799) + 0.404608) + 5.8628`

### task=combo seed=9

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics: mse=1.307318e-04, r2=0.999779
- Variant formula overview:
  - baseline: symbolic_s=9.496416e+00, mse=1.650454e-04, target_mse=1.381129e-04, formula_ok=True
  - icbr_full: symbolic_s=6.103045e-01, mse=2.300756e-04, target_mse=1.828216e-04, formula_ok=True
  - icbr_no_replay: symbolic_s=5.560072e-01, mse=2.313517e-04, target_mse=1.853896e-04, formula_ok=True
  - icbr_no_shared: symbolic_s=1.014044e+00, mse=2.300756e-04, target_mse=1.828216e-04, formula_ok=True
  - icbr_refit_commit: symbolic_s=8.864634e-01, mse=1.615833e-02, target_mse=1.631125e-02, formula_ok=True
- baseline formula (display, rounded):
  - `-4.89442*tan(0.113953*cos(3.17736*x_1 + 1.58128) + 0.146319*cos(1.49208*x_2 - 6.2084) + 6.07262) - 1.27928*asin(-0.227878*(0.107402 - x_2)**2 + 0.327281*sin(3.08344*x_1 + 9.40864) + 0.234126) - 0.0203771`
- icbr_full formula (display, rounded):
  - `6.44865*tan(0.114721*sin(1.45*x_2 - 1.5) + 0.0853378*cos(3.2*x_1 - 1.55) + 0.2543) - 1.34768*asin(-0.216501*(x_2 - 0.107527)**2 + 0.311829*cos(3.1*x_1 + 1.55) + 0.235894) - 0.593817`
- icbr_no_replay formula (display, rounded):
  - `-1.34768*asin(-0.216501*(x_2 - 0.107527)**2 + 0.311829*cos(3.1*x_1 + 1.55) + 0.235894) + 3.90951*asin(0.191202*sin(1.45*x_2 - 1.5) + 0.14223*cos(3.2*x_1 - 1.55) + 0.323834) - 0.207379`
- icbr_no_shared formula (display, rounded):
  - `6.44865*tan(0.114721*sin(1.45*x_2 - 1.5) + 0.0853378*cos(3.2*x_1 - 1.55) + 0.2543) - 1.34768*asin(-0.216501*(x_2 - 0.107527)**2 + 0.311829*cos(3.1*x_1 + 1.55) + 0.235894) - 0.593817`
- icbr_refit_commit formula (display, rounded):
  - `-6.28551*tan(0.0776342*cos(2.84512*x_1 + 1.71404) - 0.27181 + 0.14075*exp(-1.21*(-x_2 - 0.0618181)**2)) + 1.64239*atanh(0.458299*sin(0.904*x_2 + 4.60848) + 0.233038*cos(2.80596*x_1 - 1.69172) + 0.29074) - 0.581214`

### task=poly_cubic seed=0

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics: mse=1.971898e-04, r2=0.995779
- Variant formula overview:
  - baseline: symbolic_s=9.917086e+00, mse=3.803124e-03, target_mse=4.211702e-03, formula_ok=True
  - icbr_full: symbolic_s=6.533152e-01, mse=3.879537e-03, target_mse=4.270816e-03, formula_ok=True
  - icbr_no_replay: symbolic_s=5.335668e-01, mse=4.012137e-03, target_mse=4.417135e-03, formula_ok=True
  - icbr_no_shared: symbolic_s=1.063304e+00, mse=3.882675e-03, target_mse=4.275353e-03, formula_ok=True
  - icbr_refit_commit: symbolic_s=9.445244e-01, mse=1.650953e-02, target_mse=1.686238e-02, formula_ok=True
- baseline formula (display, rounded):
  - `-0.271577*sqrt(-0.536605*(-x_2 - 0.00611641)**2 - 0.021878*sin(7.67864*x_1 + 6.40864) + 1) - 1.56573*tan(0.106323*cos(4.7596*x_1 - 7.8104) + 0.637719*cos(1.04096*x_2 - 0.00288001) + 5.76407) + 0.440439`
- icbr_full formula (display, rounded):
  - `-0.272411*sqrt(-0.53581*(-x_2 - 0.0111112)**2 - 0.00131848*tan(1.55*x_1 + 2.38419e-7) + 1) - 1.18704*acos(0.423278*(-x_2 - 5.4186e-8)**2 - 0.140625*sin(4.75*x_1 + 0.0500002) - 0.141471) + 2.29081`
- icbr_no_replay formula (display, rounded):
  - `-0.271807*sqrt(-0.538195*(-x_2 - 0.0111112)**2 + 1 + 0.0276186*exp(-25.0*(0.6 - x_1)**2)) - 1.50684*tan(0.110491*sin(4.75*x_1 + 0.0500002) + 0.713688*cos(1.0*x_2 + 2.38419e-7) - 3.72889) + 0.44612`
- icbr_no_shared formula (display, rounded):
  - `-0.272332*sqrt(-0.533885*(-x_2 - 7.45058e-8)**2 - 0.00131925*tan(1.55*x_1 + 2.38419e-7) + 1) - 1.18704*acos(0.423278*(-x_2 - 5.4186e-8)**2 - 0.140625*sin(4.75*x_1 + 0.0500002) - 0.141471) + 2.29081`
- icbr_refit_commit formula (display, rounded):
  - `-0.639174*sqrt(-7.82814e-5*tan(0.2142*x_1 + 4.48996) - 0.829098 + exp(-0.0970945*(0.00012837 - x_2)**2)) - 1.62508*tan(5.47572*sin(0.0860799*x_1 - 1.7738) + 3.19994*cos(0.44252*x_2 - 4.00001e-5) + 5.39765) + 0.418957`

### task=poly_cubic seed=1

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics: mse=2.208959e-04, r2=0.995792
- Variant formula overview:
  - baseline: symbolic_s=9.424726e+00, mse=3.619018e-03, target_mse=4.105555e-03, formula_ok=True
  - icbr_full: symbolic_s=6.814555e-01, mse=3.684551e-03, target_mse=4.160145e-03, formula_ok=True
  - icbr_no_replay: symbolic_s=5.563087e-01, mse=3.761740e-03, target_mse=4.228259e-03, formula_ok=True
  - icbr_no_shared: symbolic_s=1.013293e+00, mse=3.684551e-03, target_mse=4.160145e-03, formula_ok=True
  - icbr_refit_commit: symbolic_s=8.876101e-01, mse=1.558530e-02, target_mse=1.606065e-02, formula_ok=True
- baseline formula (display, rounded):
  - `0.225479*tan(0.335726*(-x_2 - 0.0366861)**2 + 0.0116048*cos(7.75128*x_1 + 4.79464) - 2.70072) - 1.5692*tan(-0.103908*cos(4.72656*x_1 + 1.57856) + 1.03837*cos(0.78024*x_2 - 0.00776) + 2.20907) + 0.0499582`
- icbr_full formula (display, rounded):
  - `-0.30932*sqrt(-0.605193*(-x_2 - 0.0365854)**2 - 0.00132426*tan(1.55*x_1 + 2.38419e-7) + 1) - 1.45684*tan(0.11137*sin(4.75*x_1 + 2.38419e-7) + 0.950806*cos(0.85*x_2 + 2.38419e-7) - 3.97071) + 0.477135`
- icbr_no_replay formula (display, rounded):
  - `0.222844*tan(0.357062*(-x_2 - 0.0365854)**2 + 0.000781312*tan(1.55*x_1 + 2.38419e-7) + 3.53405) - 1.14772*asin(-0.412621*(0.0142856 - x_2)**2 + 0.141743*sin(4.75*x_1 + 2.38419e-7) + 0.135867) + 0.0563234`
- icbr_no_shared formula (display, rounded):
  - `-0.30932*sqrt(-0.605193*(-x_2 - 0.0365854)**2 - 0.00132426*tan(1.55*x_1 + 2.38419e-7) + 1) - 1.45684*tan(0.11137*sin(4.75*x_1 + 2.38419e-7) + 0.950806*cos(0.85*x_2 + 2.38419e-7) - 3.97071) + 0.477135`
- icbr_refit_commit formula (display, rounded):
  - `-0.309683*sqrt(-0.605218*(-x_2 - 0.0205421)**2 - 0.000730641*tan(0.502*x_1 - 4.19946) + 1) + 1.44671*tan(0.328301*(-x_2 - 0.00027301)**2 + 2.88232*sin(0.04256*x_1 + 0.6) - 1.74714) + 0.480583`

### task=poly_cubic seed=2

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics: mse=4.400568e-04, r2=0.990960
- Variant formula overview:
  - baseline: symbolic_s=8.016963e+00, mse=3.441125e-03, target_mse=4.254771e-03, formula_ok=True
  - icbr_full: symbolic_s=5.913577e-01, mse=3.429093e-03, target_mse=4.243753e-03, formula_ok=True
  - icbr_no_replay: symbolic_s=4.869574e-01, mse=3.432392e-03, target_mse=4.245607e-03, formula_ok=True
  - icbr_no_shared: symbolic_s=8.514359e-01, mse=3.429093e-03, target_mse=4.243753e-03, formula_ok=True
  - icbr_refit_commit: symbolic_s=7.779231e-01, mse=1.498576e-02, target_mse=1.605278e-02, formula_ok=True
- baseline formula (display, rounded):
  - `-0.22455*sqrt(1 - 0.556473*(-x_2 - 0.00309781)**2) + 1.39592*tan(0.115336*sin(4.77136*x_1 + 9.40848) - 0.836353*cos(0.96848*x_2 - 0.002) + 6.99107) + 0.388651`
- icbr_full formula (display, rounded):
  - `0.14053*tan(11.2944 - 11.1009*exp(-0.04*(-x_2 - 1.19209e-6)**2)) + 1.1222*asin(0.143859*cos(4.775*x_1 + 1.55) + 2.91362 - 3.06131*exp(-0.16*(x_2 - 5.96046e-7)**2)) + 0.122191`
- icbr_no_replay formula (display, rounded):
  - `0.14053*tan(0.436486*(-x_2 - 5.09986e-8)**2 + 0.19428) + 1.39867*tan(0.115087*cos(4.775*x_1 + 1.55) - 0.865794*cos(0.95*x_2 + 2.38419e-7) + 3.87775) + 0.138677`
- icbr_no_shared formula (display, rounded):
  - `0.14053*tan(11.2944 - 11.1009*exp(-0.04*(-x_2 - 1.19209e-6)**2)) + 1.1222*asin(0.143859*cos(4.775*x_1 + 1.55) + 2.91362 - 3.06131*exp(-0.16*(x_2 - 5.96046e-7)**2)) + 0.122191`
- icbr_refit_commit formula (display, rounded):
  - `0.0257176*tan(0.0130919*(-x_2 - 3.38124e-5)**2 + 1.49671) - 1.51188*tan(-0.339102*(-x_2 - 4.1008e-5)**2 + 2.71006*cos(0.0579999*x_1 + 0.7001) + 1.17433) - 0.195794`

### task=poly_cubic seed=3

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics: mse=4.574338e-04, r2=0.990719
- Variant formula overview:
  - baseline: symbolic_s=8.740330e+00, mse=3.516602e-03, target_mse=4.417833e-03, formula_ok=True
  - icbr_full: symbolic_s=6.418984e-01, mse=3.535074e-03, target_mse=4.433027e-03, formula_ok=True
  - icbr_no_replay: symbolic_s=4.966022e-01, mse=3.535473e-03, target_mse=4.432084e-03, formula_ok=True
  - icbr_no_shared: symbolic_s=9.280013e-01, mse=3.535074e-03, target_mse=4.433027e-03, formula_ok=True
  - icbr_refit_commit: symbolic_s=8.326006e-01, mse=1.551155e-02, target_mse=1.634423e-02, formula_ok=True
- baseline formula (display, rounded):
  - `0.154867*tan(0.494412*(-x_2 - 0.0330213)**2 + 9.64692) - 1.28142*tan(0.119088*cos(4.7368*x_1 - 1.57416) + 0.923274*cos(0.93376*x_2 - 0.00792) - 7.06445) + 0.131769`
- icbr_full formula (display, rounded):
  - `-0.243733*sqrt(1 - 0.650991*(-x_2 - 0.0329671)**2) + 1.35622*tan(0.357811*(0.0142856 - x_2)**2 - 0.112632*sin(4.75*x_1 + 2.38419e-7) + 3.01526) + 0.402063`
- icbr_no_replay formula (display, rounded):
  - `0.14767*tan(0.534356*(-x_2 - 0.0329671)**2 + 0.167665) - 1.35556*atanh(-0.357811*(0.0142856 - x_2)**2 + 0.112632*sin(4.75*x_1 + 2.38419e-7) + 0.134737) + 0.144898`
- icbr_no_shared formula (display, rounded):
  - `-0.243733*sqrt(1 - 0.650991*(-x_2 - 0.0329671)**2) + 1.35622*tan(0.357811*(0.0142856 - x_2)**2 - 0.112632*sin(4.75*x_1 + 2.38419e-7) + 3.01526) + 0.402063`
- icbr_refit_commit formula (display, rounded):
  - `-0.243698*sqrt(0.0066203 - cos(1.19982*x_2 - 3.094)) - 0.97258*acos(3.92805*sin(0.0539999*x_1 + 0.79994) - 1.14406*cos(0.96588*x_2 - 8.00001e-5) - 1.86006) + 1.93116`

### task=poly_cubic seed=4

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics: mse=1.944016e-04, r2=0.995768
- Variant formula overview:
  - baseline: symbolic_s=9.302384e+00, mse=2.939998e-03, target_mse=3.326834e-03, formula_ok=True
  - icbr_full: symbolic_s=6.867690e-01, mse=3.132538e-03, target_mse=3.516562e-03, formula_ok=True
  - icbr_no_replay: symbolic_s=5.325472e-01, mse=3.139105e-03, target_mse=3.520627e-03, formula_ok=True
  - icbr_no_shared: symbolic_s=1.136285e+00, mse=3.132745e-03, target_mse=3.516829e-03, formula_ok=True
  - icbr_refit_commit: symbolic_s=9.348640e-01, mse=1.490212e-02, target_mse=1.535861e-02, formula_ok=True
- baseline formula (display, rounded):
  - `-0.0731405*tan(-0.0373744*(-x_2 - 0.0331653)**2 + 0.00124971*cos(7.66768*x_1 + 7.9844) + 8.0291) - 1.33773*tan(0.111003*sin(4.75008*x_1 - 0.0072) + 0.970916*cos(0.87984*x_2 - 0.00864) - 7.13281) - 0.260404`
- icbr_full formula (display, rounded):
  - `-1.34504*tan(-0.35399*(0.010204 - x_2)**2 + 0.110475*sin(4.75*x_1 + 2.38419e-7) + 0.130745) - 0.237869*tan(0.581723*cos(1.0*x_2 + 0.0500002) - 4.28751 + 0.0123083*exp(-25.0*(0.6 - x_1)**2)) + 0.0189052`
- icbr_no_replay formula (display, rounded):
  - `-1.34504*tan(-0.35399*(0.010204 - x_2)**2 + 0.110475*sin(4.75*x_1 + 2.38419e-7) + 0.130745) + 0.237869*tan(0.275011*(-x_2 - 0.0333334)**2 + 3.70686 - 0.0123083*exp(-25.0*(0.6 - x_1)**2)) + 0.0189052`
- icbr_no_shared formula (display, rounded):
  - `-0.237869*tan(0.581723*cos(1.0*x_2 + 0.0500002) - 4.28751 + 0.0123083*exp(-25.0*(x_1 - 0.6)**2)) - 1.34465*atanh(-0.353989*(0.0101522 - x_2)**2 + 0.110475*sin(4.75*x_1 - 2.38419e-7) + 0.130745) + 0.0188963`
- icbr_refit_commit formula (display, rounded):
  - `0.0317888*tan(-0.070228*sin(0.69994*x_2 + 1.606) + 1.56343 + 0.00523963*exp(-25.0*(1 - 0.76*x_1)**2)) + 1.46106*atanh(2.49765*sin(0.03628*x_1 + 0.12272) - 0.501113*sin(1.20018*x_2 - 4.712) + 0.0898185) - 0.264664`

### task=poly_cubic seed=5

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics: mse=2.636946e-04, r2=0.994283
- Variant formula overview:
  - baseline: symbolic_s=9.540594e+00, mse=2.717470e-03, target_mse=3.094506e-03, formula_ok=True
  - icbr_full: symbolic_s=6.828050e-01, mse=2.916327e-03, target_mse=3.280004e-03, formula_ok=True
  - icbr_no_replay: symbolic_s=5.344355e-01, mse=2.916328e-03, target_mse=3.280004e-03, formula_ok=True
  - icbr_no_shared: symbolic_s=1.029028e+00, mse=2.916011e-03, target_mse=3.279468e-03, formula_ok=True
  - icbr_refit_commit: symbolic_s=9.587676e-01, mse=1.419974e-02, target_mse=1.467779e-02, formula_ok=True
- baseline formula (display, rounded):
  - `0.212296*tan(0.385517*(-x_2 - 0.031872)**2 + 0.014512*cos(7.82272*x_1 - 1.4052) + 0.331957) + 1.04086*asin(0.13842*sin(4.75864*x_1 - 9.39896) - 1.01618*cos(0.98056*x_2 - 0.00784) + 0.801167) + 0.140141`
- icbr_full formula (display, rounded):
  - `0.221622*tan(0.350159*(-x_2 - 0.0317461)**2 + 3.54026 - 0.0203347*exp(-25.0*(0.59 - x_1)**2)) - 1.07279*acos(0.442583*(0.011111 - x_2)**2 - 0.134583*cos(4.75*x_1 - 1.55) - 0.193613) + 1.79289`
- icbr_no_replay formula (display, rounded):
  - `0.221622*tan(0.350159*(-x_2 - 0.0317461)**2 + 3.54026 - 0.0203347*exp(-25.0*(0.59 - x_1)**2)) - 1.07279*asin(-0.442583*(0.011111 - x_2)**2 + 0.134583*cos(4.75*x_1 - 1.55) + 0.193612) + 0.107758`
- icbr_no_shared formula (display, rounded):
  - `-0.238226*log(-1.14762*(x_2 + 0.0319148)**2 + 3.04579 + 0.0666527*exp(-25.0*(0.59 - x_1)**2)) - 1.07279*acos(0.442583*(0.011111 - x_2)**2 - 0.134583*cos(4.75*x_1 - 1.55) - 0.193613) + 2.15167`
- icbr_refit_commit formula (display, rounded):
  - `-0.306373*sqrt(-0.587245*(-x_2 - 0.0487753)**2 + 1 - 0.181999*exp(-25.0*(1 - 0.78*x_1)**2)) - 1.43961*atanh(-0.328923*(-x_2 - 1.37832e-5)**2 + 2.32402*cos(0.042*x_1 + 1.99998) + 1.09603) + 0.492208`

### task=poly_cubic seed=6

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics: mse=5.207168e-04, r2=0.989974
- Variant formula overview:
  - baseline: symbolic_s=8.045399e+00, mse=3.798469e-03, target_mse=5.035236e-03, formula_ok=True
  - icbr_full: symbolic_s=5.760708e-01, mse=3.745944e-03, target_mse=4.953411e-03, formula_ok=True
  - icbr_no_replay: symbolic_s=4.652636e-01, mse=3.843470e-03, target_mse=5.087434e-03, formula_ok=True
  - icbr_no_shared: symbolic_s=8.421079e-01, mse=3.745944e-03, target_mse=4.953411e-03, formula_ok=True
  - icbr_refit_commit: symbolic_s=8.480290e-01, mse=1.675225e-02, target_mse=1.800607e-02, formula_ok=True
- baseline formula (display, rounded):
  - `-1.4981*acos(-0.109401*cos(4.74992*x_1 - 1.59064) + 5.2014 - 5.27878*exp(-0.0633427*(0.0162111 - x_2)**2)) + 2.25127 + 0.205693/(1 - 0.181329*(-x_2 - 0.0570374)**2)**2`
- icbr_full formula (display, rounded):
  - `1.47846*acos(-0.110838*cos(4.75*x_1 + 1.55) + 0.865898*cos(0.9*x_2 + 2.38419e-7) - 0.784572) - 2.42488 + 0.209226/(0.179171*(x_2 + 0.0555556)**2 - 1)**2`
- icbr_no_replay formula (display, rounded):
  - `1.47846*asin(0.329033*(0.0199999 - x_2)**2 + 0.110838*cos(4.75*x_1 + 1.55) - 0.0794008) - 0.102529 + 0.209226/(0.179171*(x_2 + 0.0555556)**2 - 1)**2`
- icbr_no_shared formula (display, rounded):
  - `1.47846*acos(-0.110838*cos(4.75*x_1 + 1.55) + 0.865898*cos(0.9*x_2 + 2.38419e-7) - 0.784572) - 2.42488 + 0.209226/(0.179171*(-x_2 - 0.0555556)**2 - 1)**2`
- icbr_refit_commit formula (display, rounded):
  - `1.42061*asin(0.344449*(0.000121818 - x_2)**2 + 3.58612*cos(0.0679999*x_1 + 3.60002) + 3.10573) - 0.0590194 + 0.304988/(1 - 0.239858*sin(1.5*x_2 + 4.804))**2`

### task=poly_cubic seed=7

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics: mse=2.268898e-04, r2=0.995016
- Variant formula overview:
  - baseline: symbolic_s=1.234297e+01, mse=3.262920e-03, target_mse=3.761967e-03, formula_ok=True
  - icbr_full: symbolic_s=2.056138e+00, mse=3.446057e-03, target_mse=3.942226e-03, formula_ok=True
  - icbr_no_replay: symbolic_s=1.704573e+00, mse=3.446057e-03, target_mse=3.942226e-03, formula_ok=True
  - icbr_no_shared: symbolic_s=3.660325e+00, mse=3.446057e-03, target_mse=3.942226e-03, formula_ok=True
  - icbr_refit_commit: symbolic_s=2.790158e+00, mse=1.559319e-02, target_mse=1.603835e-02, formula_ok=True
- baseline formula (display, rounded):
  - `0.0401577*tan(0.0253453*(-x_2 - 0.0252374)**2 - 0.000928825*cos(7.73912*x_1 - 4.58616) + 4.59206) + 1.14547*asin(0.140207*cos(4.77816*x_1 + 1.5888) - 1.01517*cos(0.956*x_2 - 0.00552001) + 0.827878) - 0.124731`
- icbr_full formula (display, rounded):
  - `0.1026*tan(0.0687222*(-x_2 - 0.0253165)**2 + 4.39192 - 0.00344821*exp(-25.0*(0.6 - x_1)**2)) - 1.62475*atanh(0.0989322*cos(4.775*x_1 - 1.55) + 0.601791*cos(1.05*x_2 + 2.38419e-7) - 0.470658) - 0.103446`
- icbr_no_replay formula (display, rounded):
  - `0.1026*tan(0.0687222*(-x_2 - 0.0253165)**2 + 4.39192 - 0.00344821*exp(-25.0*(0.6 - x_1)**2)) - 1.62475*atanh(0.0989322*cos(4.775*x_1 - 1.55) + 0.601791*cos(1.05*x_2 + 2.38419e-7) - 0.470658) - 0.103446`
- icbr_no_shared formula (display, rounded):
  - `0.1026*tan(0.0687222*(-x_2 - 0.0253165)**2 + 4.39192 - 0.00344821*exp(-25.0*(0.6 - x_1)**2)) - 1.62475*atanh(0.0989322*cos(4.775*x_1 - 1.55) + 0.601791*cos(1.05*x_2 + 2.38419e-7) - 0.470658) - 0.103446`
- icbr_refit_commit formula (display, rounded):
  - `0.072376*tan(0.0468336*x_2**2 + 4.49125 + 0.0168166*exp(-25.0*(1 - 0.76*x_1)**2)) + 1.57999*atanh(5.1465*cos(0.0838399*x_1 + 3.36112) + 8.74603 - 3.87072*exp(-0.0841695*(0.0126844 - x_2)**2)) - 0.104261`

### task=poly_cubic seed=8

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics: mse=2.437145e-04, r2=0.995473
- Variant formula overview:
  - baseline: symbolic_s=2.033449e+01, mse=3.883438e-03, target_mse=4.386742e-03, formula_ok=True
  - icbr_full: symbolic_s=2.124323e+00, mse=3.974629e-03, target_mse=4.456935e-03, formula_ok=True
  - icbr_no_replay: symbolic_s=1.709258e+00, mse=3.982884e-03, target_mse=4.465010e-03, formula_ok=True
  - icbr_no_shared: symbolic_s=3.311191e+00, mse=3.974629e-03, target_mse=4.456935e-03, formula_ok=True
  - icbr_refit_commit: symbolic_s=2.821496e+00, mse=1.629138e-02, target_mse=1.675938e-02, formula_ok=True
- baseline formula (display, rounded):
  - `0.956525*asin(-0.172713*cos(4.7616*x_1 - 1.59432) + 1.06125*cos(1.00016*x_2 + 9.412) + 0.848976) - 0.016334 + 0.214517/(-0.132798*(-x_2 - 0.0495675)**2 + 0.00521835*cos(7.73592*x_1 + 7.99912) + 1)**3`
- icbr_full formula (display, rounded):
  - `0.109774*tan(0.0803522*(x_2 + 0.05)**2 + 0.000190827*tan(1.55*x_1 + 2.38419e-7) + 4.38793) + 1.44504*atanh(0.114879*cos(4.75*x_1 + 1.55) - 0.6434*cos(1.05*x_2 + 2.38419e-7) + 0.511356) - 0.141749`
- icbr_no_replay formula (display, rounded):
  - `0.109774*tan(0.0803522*(x_2 + 0.05)**2 + 0.000190827*tan(1.55*x_1 + 2.38419e-7) + 4.38793) - 0.991685*acos(0.4775*(0.0124999 - x_2)**2 + 0.167097*cos(4.75*x_1 + 1.55) - 0.192775) + 1.42055`
- icbr_no_shared formula (display, rounded):
  - `0.109774*tan(0.0803522*(x_2 + 0.05)**2 + 0.000190827*tan(1.55*x_1 + 2.38419e-7) + 4.38793) + 1.44504*atanh(0.114879*cos(4.75*x_1 + 1.55) - 0.6434*cos(1.05*x_2 + 2.38419e-7) + 0.511356) - 0.141749`
- icbr_refit_commit formula (display, rounded):
  - `-0.108547*tan(0.0925284*cos(1.50456*x_2 + 0.0918799) - 8.74792e-5*tan(0.304*x_1 + 4.39992) + 1.82468) + 1.13814*asin(0.556925*sin(1.30002*x_2 + 4.712) - 7.38841*cos(0.0777599*x_1 + 0.24288) + 7.53539) - 0.116834`

### task=poly_cubic seed=9

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics: mse=2.868795e-04, r2=0.994538
- Variant formula overview:
  - baseline: symbolic_s=2.047534e+01, mse=3.489609e-03, target_mse=4.075463e-03, formula_ok=True
  - icbr_full: symbolic_s=2.098444e+00, mse=3.714165e-03, target_mse=4.291883e-03, formula_ok=True
  - icbr_no_replay: symbolic_s=1.720350e+00, mse=3.715293e-03, target_mse=4.294963e-03, formula_ok=True
  - icbr_no_shared: symbolic_s=3.347805e+00, mse=3.719504e-03, target_mse=4.299776e-03, formula_ok=True
  - icbr_refit_commit: symbolic_s=2.878897e+00, mse=1.615773e-02, target_mse=1.689890e-02, formula_ok=True
- baseline formula (display, rounded):
  - `-0.0522339*tan(-0.0377594*(-x_2 - 0.0300216)**2 + 0.00144032*sin(7.81576*x_1 - 2.9896) + 4.87614) - 1.12495*asin(0.139898*cos(4.75008*x_1 - 1.58128) + 0.990633*cos(0.97152*x_2 - 0.00808) - 0.794508) - 0.103426`
- icbr_full formula (display, rounded):
  - `-1.14616*asin(-0.428427*(0.00999994 - x_2)**2 + 0.137344*sin(4.75*x_1 + 2.38419e-7) + 0.189618) - 0.0195876 + 0.232782/(0.159626*(-x_2 - 0.03)**2 - 1 - 0.00847097*exp(-25.0*(0.59 - x_1)**2))**2`
- icbr_no_replay formula (display, rounded):
  - `1.14616*asin(0.428427*(0.00999994 - x_2)**2 + 0.137417*cos(4.75*x_1 + 1.55) - 0.189003) - 0.0195876 + 0.232782/(0.159626*(-x_2 - 0.03)**2 - 1 - 0.00847097*exp(-25.0*(0.59 - x_1)**2))**2`
- icbr_no_shared formula (display, rounded):
  - `-1.14616*asin(-0.427747*(0.0142856 - x_2)**2 + 0.137344*sin(4.75*x_1 + 2.38419e-7) + 0.189475) - 0.0195876 + 0.232782/(0.159626*(-x_2 - 0.03)**2 - 1 - 0.00847097*exp(-25.0*(x_1 - 0.59)**2))**2`
- icbr_refit_commit formula (display, rounded):
  - `1.53617*atanh(0.319982*(-x_2 - 7.061e-5)**2 + 2.72246*cos(0.03992*x_1 - 2.1) + 1.23766) - 0.0343101 + 0.236778/(-0.154589*(-x_2 - 0.0486505)**2 + 1 - 0.013029*exp(-25.0*(1 - 0.92*x_1)**2))**2`

### task=trig_interaction seed=0

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics: mse=3.960060e-03, r2=0.994748
- Variant formula overview:
  - baseline: symbolic_s=4.720387e+01, mse=3.841724e-03, target_mse=8.799501e-03, formula_ok=True
  - icbr_full: symbolic_s=4.889191e+00, mse=3.736263e-03, target_mse=8.564282e-03, formula_ok=True
  - icbr_no_replay: symbolic_s=2.941514e+00, mse=3.773011e-03, target_mse=8.527163e-03, formula_ok=True
  - icbr_no_shared: symbolic_s=8.613142e+00, mse=3.736263e-03, target_mse=8.564282e-03, formula_ok=True
  - icbr_refit_commit: symbolic_s=6.507333e+00, mse=1.064527e-01, target_mse=1.092256e-01, formula_ok=True
- baseline formula (display, rounded):
  - `1.15662*sin(0.237991*cos(3.78512*x_1 - 8.00544) + 0.422881*cos(3.12304*x_2 - 0.000320001) - 0.0236924*tanh(3.81648*x_3 - 1.79056) + 6.26388) + 0.432285*cos(1.19945*sin(2.55528*x_1 - 9.41056) + 0.865454*atan(1.97728*x_3 - 1.59904) - 5.31194) + 0.342727 - 1.38998*exp(-2.75347*(-atan(0.41312*x_3 - 0.87888) - 0.47423 - 0.857093*exp(-1.66802*(0.536484 - x_1)**2) - 0.063391*exp(-0.958206*(0.0333442 - x_2)**2))**2) + 0.680915*exp(-2.41755*(0.683322*sin(2.30584*x_1 + 8.97536) - 0.21072 + exp(-0.611023*(1 - 0.814144*x_3)**2))**2)`
- icbr_full formula (display, rounded):
  - `1.15638*cos(0.0309413*(-x_3 - 0.273973)**3 - 0.23822*sin(3.8*x_1 + 3.0) + 0.424732*cos(3.1*x_2 + 2.38419e-7) - 1.57867) - 0.451349 - 1.40685*exp(-9.69065*(0.0215594*(0.032258 - x_2)**2 - atan(0.45*x_3 - 1.65) - 0.932964 - 0.446479*exp(-1.69*(0.538462 - x_1)**2))**2) + 1.24025*exp(-0.243538*(-cos(2.55*x_1 - 1.55) + 0.71139*atan(2.0*x_3 - 1.6) + 0.806166)**2) + 0.686772*exp(-2.28473*(-0.693876*sin(2.3*x_1 - 3.6) + 0.205462 - exp(-0.64*(1 - 0.8125*x_3)**2))**2)`
- icbr_no_replay formula (display, rounded):
  - `-0.428481*cos(1.20906*cos(2.55*x_1 - 1.55) - 0.860117*atan(2.0*x_3 - 1.6) + 2.17779) - 1.1713 - 1.40685*exp(-9.69065*(-0.0131785*sin(2.15*x_2 + 1.5) - atan(0.45*x_3 - 1.65) - 0.920592 - 0.446479*exp(-1.69*(0.538462 - x_1)**2))**2) + 2.55784*exp(-0.530765*(0.17311*sin(3.8*x_1 + 3.0) - 0.308644*cos(3.1*x_2 + 2.38419e-7) + 0.0169375*tanh(4.0*x_3 - 1.85) + 1)**2) + 0.686772*exp(-1.10001*(-sin(2.3*x_1 - 3.6) + 0.660829*cos(1.2*x_3 + 1.5) - 0.517822)**2)`
- icbr_no_shared formula (display, rounded):
  - `1.15638*cos(0.0309413*(-x_3 - 0.273973)**3 - 0.23822*sin(3.8*x_1 + 3.0) + 0.424732*cos(3.1*x_2 + 2.38419e-7) - 1.57867) - 0.451349 - 1.40685*exp(-9.69065*(0.0215594*(0.032258 - x_2)**2 - atan(0.45*x_3 - 1.65) - 0.932964 - 0.446479*exp(-1.69*(x_1 - 0.538462)**2))**2) + 1.24025*exp(-0.243538*(-cos(2.55*x_1 - 1.55) + 0.71139*atan(2.0*x_3 - 1.6) + 0.806166)**2) + 0.686772*exp(-2.28473*(-0.693876*sin(2.3*x_1 - 3.6) + 0.205462 - exp(-0.64*(1 - 0.8125*x_3)**2))**2)`
- icbr_refit_commit formula (display, rounded):
  - `-1.13477*cos(0.1345*sin(2.35208*x_1 + 2.99572) + 0.0334484*atan(2.92972*x_3 - 2.36972) + 33.9613 - 29.5719*exp(-0.0345959*(-x_2 - 0.0111828)**2)) - 0.219419*Abs(0.340715*(-0.58255*x_3 - 1)**4 + 1.55226 - 3.50712*exp(-1.49368*(0.695162 - x_1)**2)) + 0.354986*Abs(0.660635*Abs(3.26668*x_1 - 2.24416) + 0.0512697*Abs(3.0958*x_2 - 0.10032) - 11.8777*atan(0.59612*x_3 - 2.6582) - 17.3665) - 0.0644156 - 0.538792*exp(-4.99947*(0.350156 - 0.843632*exp(-0.50854*(-0.813271*x_3 - 1)**2) - exp(-2.49349*(0.799174 - x_1)**2))**2)`

### task=trig_interaction seed=1

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics: mse=1.170746e-03, r2=0.998113
- Variant formula overview:
  - baseline: symbolic_s=5.406665e+01, mse=8.269406e-03, target_mse=8.301958e-03, formula_ok=True
  - icbr_full: symbolic_s=5.836482e+00, mse=6.691324e-03, target_mse=6.753302e-03, formula_ok=True
  - icbr_no_replay: symbolic_s=9.222282e-01, mse=8.591769e-03, target_mse=8.738704e-03, formula_ok=True
  - icbr_no_shared: symbolic_s=2.997664e+00, mse=6.691324e-03, target_mse=6.753302e-03, formula_ok=True
  - icbr_refit_commit: symbolic_s=2.172332e+00, mse=7.377906e-02, target_mse=7.484721e-02, formula_ok=True
- baseline formula (display, rounded):
  - `-0.480719*sin(-1.29193*cos(2.33616*x_1 + 8.2196) + 0.146559*cos(3.99856*x_2 + 6.20976) + 0.598691*tan(0.91192*x_3 - 2.95968) + 8.22444) + 0.509575*sin(1.15765*cos(2.45544*x_1 + 7.8016) - 0.120965*cos(1.996*x_2 - 6.39272) + 1.16007*atan(1.222*x_3 - 0.88472) + 2.55528) + 0.501071 + 0.908862*exp(-5.1303*(-0.233051*cos(1.49248*x_3 + 1.77408) - 0.147441 + exp(-1.84308*(-x_1 - 0.398409)**2) - 0.0932319*exp(-1.54694*(0.0521 - x_2)**2))**2) - 1.91077*exp(-0.448194*(0.288001*sin(3.54792*x_1 + 9.78552) + 0.0932117*cos(1.97072*x_3 - 4.58992) - 0.690374 - exp(-2.57205*(-x_2 - 0.00663441)**2))**2)`
- icbr_full formula (display, rounded):
  - `-0.265369*(0.149981*(0.0379746 - x_2)**2 + 0.969021*cos(2.45*x_1 + 1.5) + atan(1.2*x_3 - 0.9) + 0.746054)**2 + 0.443991*sin(-0.89595*cos(1.5*x_3 - 4.5) + 0.0633626*Abs(5.0*x_2 - 0.3) + 0.640062 + 3.83853*exp(-1.8225*(-x_1 - 0.407407)**2)) - 1.12464*atan(0.280942*sin(3.55*x_1 + 3.5) + 0.430265*sin(3.2*x_2 - 1.55) - 0.266847 + 0.190815*exp(-1.21*(-x_3 - 0.818182)**2)) + 0.929212 - 1.14923*exp(-1.74264*(0.0528703*sin(4.0*x_2 + 1.5) + 0.21896*tan(0.9*x_3 - 2.95) - 0.387537 + exp(-1.5625*(0.52 - x_1)**2))**2)`
- icbr_no_replay formula (display, rounded):
  - `-0.488919*cos(-1.27452*sin(2.35*x_1 + 3.5) + 0.144757*sin(4.0*x_2 + 1.5) + 0.599505*tan(0.9*x_3 - 2.95) + 0.359568) - 0.519378*cos(1.14065*sin(2.45*x_1 - 0.0499997) - 0.133258*cos(1.85*x_2 + 3.05) - 1.17733*atan(1.2*x_3 - 0.9) + 2.11839) + 0.467659 + 0.915032*exp(-4.89309*(-0.23341*cos(1.5*x_3 - 4.5) - 0.146495 + exp(-1.8225*(-x_1 - 0.407407)**2) - 0.0971232*exp(-1.44*(0.0416664 - x_2)**2))**2) - 1.84362*exp(-0.672063*(-0.244784*sin(3.55*x_1 + 3.5) - 0.37489*sin(3.2*x_2 - 1.55) + 0.0794033*cos(1.95*x_3 - 1.45) + 1)**2)`
- icbr_no_shared formula (display, rounded):
  - `-0.265369*(0.149981*(0.0379746 - x_2)**2 + 0.969021*cos(2.45*x_1 + 1.5) + atan(1.2*x_3 - 0.9) + 0.746054)**2 + 0.443991*sin(-0.89595*cos(1.5*x_3 - 4.5) + 0.0633626*Abs(5.0*x_2 - 0.3) + 0.640062 + 3.83853*exp(-1.8225*(-x_1 - 0.407407)**2)) - 1.12464*atan(0.280942*sin(3.55*x_1 + 3.5) + 0.430265*sin(3.2*x_2 - 1.55) - 0.266847 + 0.190815*exp(-1.21*(-x_3 - 0.818182)**2)) + 0.929212 - 1.14923*exp(-1.74264*(0.0528703*sin(4.0*x_2 + 1.5) + 0.21896*tan(0.9*x_3 - 2.95) - 0.387537 + exp(-1.5625*(0.52 - x_1)**2))**2)`
- icbr_refit_commit formula (display, rounded):
  - `0.34706*sin(0.229452*(0.0551204 - x_2)**2 + 0.61816*(-0.933205*x_3 - 1)**2 - 3.6331 - 3.23852*exp(-1.49876*(0.70032 - x_1)**2)) - 0.426004*cos(0.248056*(0.0410647 - x_2)**2 + 0.762235*sin(1.434*x_3 + 0.21388) + 5.57614 - 2.63418*exp(-2.77089*(0.781713 - x_1)**2)) + 0.927845*cos(0.2256*sin(2.30052*x_1 + 0.30532) + 3.83336*sin(0.80026*x_2 - 4.704) + 0.104643*atan(2.106*x_3 + 0.19988) - 4.88738) + 0.247797*Abs(1.86811*sqrt(1 - 0.937035*x_3) + 2.03358*sin(0.63876*x_2 + 4.69792) + 0.518631*Abs(4.99948*x_1 - 3.098) - 2.5932) - 0.54745`

### task=trig_interaction seed=2

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics: mse=6.734044e-03, r2=0.989837
- Variant formula overview:
  - baseline: symbolic_s=2.121775e+01, mse=5.097379e-03, target_mse=1.171224e-02, formula_ok=True
  - icbr_full: symbolic_s=1.440100e+00, mse=4.159365e-03, target_mse=1.025989e-02, formula_ok=True
  - icbr_no_replay: symbolic_s=9.321032e-01, mse=6.161980e-03, target_mse=1.370093e-02, formula_ok=True
  - icbr_no_shared: symbolic_s=2.742598e+00, mse=4.159365e-03, target_mse=1.025989e-02, formula_ok=True
  - icbr_refit_commit: symbolic_s=2.052544e+00, mse=5.959955e-02, target_mse=6.852099e-02, formula_ok=True
- baseline formula (display, rounded):
  - `0.403438*atan(0.672081 - 2.01297*exp(-2.99013*(-x_1 - 0.363359)**2) - 1.29681*exp(-0.734654*(0.550214 - x_3)**2) + 1.09893*exp(-1.0886*(0.0351173 - x_2)**2)) - 0.987629*atan(0.221159*cos(3.42576*x_1 + 1.60888) - 0.0684918*atan(2.6504*x_3 + 1.04) + 0.331475 - 0.956274*exp(-2.88375*(-x_2 - 0.00885664)**2)) - 0.316604 - 1.21147*exp(-2.07398*(-0.0211089*cos(4.2916*x_2 - 6.20448) - 0.313627*atan(1.21168*x_3 - 0.5216) + 0.219131 - exp(-1.11936*(0.549111 - x_1)**2))**2) + 1.47798*exp(-1.97761*(0.60228*atan(0.79776*x_3 - 0.77832) - 0.0351355 + exp(-1.28251*(-x_1 - 0.606103)**2))**2)`
- icbr_full formula (display, rounded):
  - `0.843557*sin(0.493945*sin(3.3*x_2 - 1.55) - 0.25514*cos(3.45*x_1 - 1.55) - 0.341696*cos(0.6*x_3 - 0.55) + 3.16926) + 0.511679*cos(0.0637093*sin(4.3*x_2 - 1.5) + 0.443314*Abs(4.8*x_1 - 2.7) - 0.945345*atan(1.2*x_3 - 0.5) + 0.538995) - 1.5201 + 0.831118*exp(-1.17986*(-0.217358*sin(2.3*x_2 + 1.5) - 0.0972223*Abs(4.0*x_3 - 2.2) + 0.741175 + exp(-3.0625*(-x_1 - 0.371429)**2))**2) + 1.50807*exp(-0.403083*(0.754967*(0.169492*x_3 + 1)**5 + cos(2.05*x_1 - 4.975) - 0.555803)**2)`
- icbr_no_replay formula (display, rounded):
  - `0.511679*cos(0.0637093*sin(4.3*x_2 - 1.5) - 0.945345*atan(1.2*x_3 - 0.5) + 3.73452 - 2.95435*exp(-1.21*(x_1 - 0.545455)**2)) + 0.941694*atan(0.23146*sin(3.4*x_1 + 0.0500002) - 0.450993*sin(3.3*x_2 - 1.55) + 0.0721081*atan(2.65*x_3 + 1.05) + 0.161589) + 0.404086*atan(0.437218*sin(2.3*x_2 + 1.5) - 0.545049*cos(1.8*x_3 - 1.0) + 0.554062 - 2.01151*exp(-3.0625*(-x_1 - 0.371429)**2)) - 1.01595 + 1.50807*exp(-2.84255*(0.376568*cos(2.05*x_1 - 4.975) + tanh(0.5*x_3 - 0.9) + 0.790437)**2)`
- icbr_no_shared formula (display, rounded):
  - `0.843557*sin(0.493945*sin(3.3*x_2 - 1.55) - 0.25514*cos(3.45*x_1 - 1.55) - 0.341696*cos(0.6*x_3 - 0.55) + 3.16926) + 0.511679*cos(0.0637093*sin(4.3*x_2 - 1.5) + 0.443314*Abs(4.8*x_1 - 2.7) - 0.945345*atan(1.2*x_3 - 0.5) + 0.538995) - 1.5201 + 0.831118*exp(-1.17986*(-0.217358*sin(2.3*x_2 + 1.5) - 0.0972223*Abs(4.0*x_3 - 2.2) + 0.741175 + exp(-3.0625*(-x_1 - 0.371429)**2))**2) + 1.50807*exp(-0.403083*(0.754967*(0.169492*x_3 + 1)**5 + cos(2.05*x_1 - 4.975) - 0.555803)**2)`
- icbr_refit_commit formula (display, rounded):
  - `0.421115*sin(0.523162*sin(1.48264*x_3 + 0.59824) + 7.52638 - 1.43654*exp(-3.02927*(0.725731 - x_1)**2) - 10.2128*exp(-0.0665639*(0.0316279 - x_2)**2)) + 0.849334*sin(0.169524*cos(2.59012*x_1 + 1.62032) + 0.333897*cos(0.60744*x_3 - 3.69732) + 24.4333 - 27.9156*exp(-0.0406586*(-x_2 - 0.010117)**2)) - 0.218354*Abs(-2.10877*(-0.169509*x_3 - 1)**5 - 1.05824*Abs(3.69108*x_1 + 2.66476) + 1.703) + 0.488557*Abs(0.152571*cos(1.10004*x_2 - 3.108) + 0.312148*Abs(4.56248*x_1 - 2.9392) - 0.84124*atan(0.98928*x_3 - 0.54716) - 1.90427) - 0.0585735`

### task=trig_interaction seed=3

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics: mse=2.789838e-03, r2=0.996177
- Variant formula overview:
  - baseline: symbolic_s=2.204502e+01, mse=2.029721e-03, target_mse=4.028204e-03, formula_ok=True
  - icbr_full: symbolic_s=1.516479e+00, mse=2.408870e-03, target_mse=4.625835e-03, formula_ok=True
  - icbr_no_replay: symbolic_s=9.368098e-01, mse=2.552712e-03, target_mse=4.878518e-03, formula_ok=True
  - icbr_no_shared: symbolic_s=2.781665e+00, mse=2.408870e-03, target_mse=4.625835e-03, formula_ok=True
  - icbr_refit_commit: symbolic_s=2.081531e+00, mse=5.832446e-02, target_mse=6.129974e-02, formula_ok=True
- baseline formula (display, rounded):
  - `0.345705*sin(0.225067*sin(2.58544*x_2 + 1.5984) + 0.798027*sin(1.82048*x_3 + 6.78432) + 3.92581 + 3.21786*exp(-1.18775*(0.411069 - x_1)**2)) - 1.366*atan(0.370868*sin(3.0276*x_2 - 1.57256) - 0.222666*cos(3.50416*x_1 - 1.99712) + 0.254765*atan(0.5112*x_3 + 0.19848) + 0.196755) + 0.489243 + 1.18063*exp(-2.60063*(-0.0756451*cos(1.32184*x_2 - 0.00496001) - 0.500902*acos(0.558159*x_3 + 0.13304) + 0.426915 + exp(-1.38957*(-x_1 - 0.555616)**2))**2) - 1.26442*exp(-1.34412*(0.537782 - 0.632713*exp(-2.49589*(1 - 0.876038*x_3)**2) - exp(-1.43981*(0.560037 - x_1)**2))**2)`
- icbr_full formula (display, rounded):
  - `0.926362*(0.202672*(1 - 0.322034*x_3)**(3/2) + 0.180485*cos(3.5*x_1 - 2.0) + 0.299416*cos(3.05*x_2 + 2.38419e-7) + 1)**(3/2) - 0.512052*cos(0.192433*(-x_2 - 4.89064e-8)**2 - 1.67621*acos(0.55*x_3 + 0.15) + 4.26513 + 3.32794*exp(-1.3225*(-x_1 - 0.565217)**2)) - 0.346335*cos(0.78299*cos(1.85*x_3 + 2.05) + 1.08597 - 0.549623*exp(-1.44*(-x_2 - 1.98682e-7)**2) - 3.18862*exp(-1.21*(0.409091 - x_1)**2)) - 0.45575 - 1.20434*exp(-1.40637*(-0.516746 + exp(-1.5625*(x_1 - 0.56)**2) + 0.647776*exp(-2.56*(1 - 0.875*x_3)**2))**2)`
- icbr_no_replay formula (display, rounded):
  - `-0.345847*sin(-0.222934*sin(2.6*x_2 - 1.55) + 0.798147*sin(1.8*x_3 + 0.5) + 0.819656 + 3.18862*exp(-1.21*(0.409091 - x_1)**2)) - 0.905382 + 1.16226*exp(-2.76879*(-0.0723946*cos(1.35*x_2 + 2.38419e-7) + 0.503678*asin(0.55*x_3 + 0.15) - 0.384422 + exp(-1.3225*(-x_1 - 0.565217)**2))**2) + 2.19756*exp(-1.05196*(-0.157231*cos(3.5*x_1 - 2.0) - 0.26084*cos(3.05*x_2 + 2.38419e-7) + 1 - 0.305709*exp(-0.722499*(0.411765*x_3 + 1)**2))**2) - 1.20434*exp(-1.40637*(-0.516746 + exp(-1.5625*(x_1 - 0.56)**2) + 0.647776*exp(-2.56*(1 - 0.875*x_3)**2))**2)`
- icbr_no_shared formula (display, rounded):
  - `0.926362*(0.202672*(1 - 0.322034*x_3)**(3/2) + 0.180485*cos(3.5*x_1 - 2.0) + 0.299416*cos(3.05*x_2 + 2.38419e-7) + 1)**(3/2) - 0.512052*cos(0.192433*(-x_2 - 4.89064e-8)**2 - 1.67621*acos(0.55*x_3 + 0.15) + 4.26513 + 3.32794*exp(-1.3225*(-x_1 - 0.565217)**2)) - 0.346335*cos(0.78299*cos(1.85*x_3 + 2.05) + 1.08597 - 0.549623*exp(-1.44*(-x_2 - 1.98682e-7)**2) - 3.18862*exp(-1.21*(0.409091 - x_1)**2)) - 0.45575 - 1.20434*exp(-1.40637*(-0.516746 + exp(-1.5625*(x_1 - 0.56)**2) + 0.647776*exp(-2.56*(1 - 0.875*x_3)**2))**2)`
- icbr_refit_commit formula (display, rounded):
  - `-0.345963*cos(0.788887*cos(1.57572*x_3 - 4.20728) + 0.478739*Abs(3.92556*x_1 - 2.059) + 0.083049*Abs(4.99762*x_2 + 0.0979999) - 2.7643) + 0.331081*Abs(0.764996*(x_3 + 0.536901)**2 - 0.644764*Abs(2.80552*x_1 - 1.90312) + 1.3967) - 5.61113 + 3.5704*exp(-7.82311*(-0.83206*sqrt(1 - 0.171527*x_3) - 0.133017*Abs(1.23968*x_1 + 0.82728) + 0.00279505*Abs(4.99999*x_2 + 0.0999999) + 1)**2) + 5.94403*exp(-22.7817*(-0.0155953*(1 - 0.323812*x_3)**(3/2) - 0.783753*cos(0.36796*x_2) + 0.00999842*cos(2.326*x_1 - 4.992) + 1)**2)`

### task=trig_interaction seed=4

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics: mse=4.315572e-03, r2=0.994118
- Variant formula overview:
  - baseline: symbolic_s=1.943706e+01, mse=2.755608e-03, target_mse=5.385057e-03, formula_ok=True
  - icbr_full: symbolic_s=1.367030e+00, mse=2.831550e-03, target_mse=5.937985e-03, formula_ok=True
  - icbr_no_replay: symbolic_s=8.515103e-01, mse=3.039960e-03, target_mse=5.652036e-03, formula_ok=True
  - icbr_no_shared: symbolic_s=2.395608e+00, mse=2.831551e-03, target_mse=5.937984e-03, formula_ok=True
  - icbr_refit_commit: symbolic_s=1.841818e+00, mse=6.580822e-02, target_mse=7.681624e-02, formula_ok=True
- baseline formula (display, rounded):
  - `1.22263*atan(0.165462*sin(2.95224*x_2 - 4.78984) - 0.163445*cos(3.3344*x_1 + 7.7936) + 0.128418) - 2.10775 + 3.29088*exp(-0.532138*(0.150694*sin(3.2364*x_2 - 7.80584) - 0.137897*cos(3.41296*x_1 - 8.00008) + 1 + 0.0277291*exp(-(0.13088 - 1.0*x_3)**2))**2) - 1.86196*exp(-2.26762*(-atan(0.768*x_3 - 1.60048) - 0.751401 - 0.667733*exp(-0.89537*(0.597565 - x_1)**2))**2) + 1.91206*exp(-1.97759*(-0.062998*Abs(7.33888*x_1 + 4.6924) + 0.679252*atan(0.73448*x_3 - 0.94) + 1)**2)`
- icbr_full formula (display, rounded):
  - `1.6366*sin(0.0221547*(0.116279 - x_3)**2 - 0.172871*sin(3.4*x_1 + 3.0) + 0.188839*cos(3.25*x_2 + 0.0500002) - 0.0933768) + 0.760263*cos(8.64426*tanh(0.4*x_3 - 1.35) - 0.331091*Abs(4.3*x_1 + 2.75) + 9.06977) - 1.16241*atan(0.171995*cos(3.35*x_1 + 1.5) + 0.110163 - 0.403075*exp(-2.1025*(0.0344826 - x_2)**2)) + 1.17238 - 1.93623*exp(-3.38709*(atan(0.85*x_3 - 2.0) + 0.883953 + 0.544951*exp(-0.81*(x_1 - 0.611111)**2))**2)`
- icbr_no_replay formula (display, rounded):
  - `0.787614*sin(8.43342*tanh(0.4*x_3 - 1.35) - 0.323016*Abs(4.3*x_1 + 2.75) + 10.4108) - 1.4887*cos(0.190158*sin(3.4*x_1 + 3.0) + 0.0152257*sin(2.2*x_3 - 5.0) - 0.207723*cos(3.25*x_2 + 0.0500002) - 1.51612) + 1.16241*atan(0.172083*sin(3.35*x_1 - 0.0499997) + 0.173892*sin(2.95*x_2 + 1.5) + 0.115181) + 1.09106 - 1.93623*exp(-3.38709*(atan(0.85*x_3 - 2.0) + 0.883953 + 0.544951*exp(-0.81*(x_1 - 0.611111)**2))**2)`
- icbr_no_shared formula (display, rounded):
  - `1.6366*sin(0.0221547*(0.116279 - x_3)**2 - 0.172871*sin(3.4*x_1 + 3.0) + 0.188839*cos(3.25*x_2 + 0.0500002) - 0.0933773) + 0.760263*cos(8.64426*tanh(0.4*x_3 - 1.35) - 0.331091*Abs(4.3*x_1 + 2.75) + 9.06977) - 1.16241*atan(0.171995*cos(3.35*x_1 + 1.5) + 0.110163 - 0.403075*exp(-2.1025*(0.0344826 - x_2)**2)) + 1.17238 - 1.93623*exp(-3.38709*(atan(0.85*x_3 - 2.0) + 0.883953 + 0.544951*exp(-0.81*(x_1 - 0.611111)**2))**2)`
- icbr_refit_commit formula (display, rounded):
  - `9.15377*sin(0.245657*exp(0.68864*x_3) - 0.0798601*Abs(3.87184*x_1 - 2.65004) + 4.83555) + 1.81255*tanh(0.0200934*(0.116279 - x_3)**2 + 0.114731*sin(2.6084*x_1 - 0.0852799) + 4.56451*cos(0.41988*x_2 + 0.00604) - 4.47196) - 0.27151*Abs(2.03033*exp(0.699*x_3) - 0.838878*Abs(2.7884*x_1 + 1.9626) + 0.972364) + 1.60651*atan(0.093666*cos(2.62172*x_1 - 1.6068) - 4.9998 + 5.26856*exp(-0.0549995*(0.0252431 - x_2)**2)) + 9.11572`

### task=trig_interaction seed=5

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics: mse=1.623086e-03, r2=0.997863
- Variant formula overview:
  - baseline: symbolic_s=2.385840e+01, mse=5.803085e-03, target_mse=6.947897e-03, formula_ok=True
  - icbr_full: symbolic_s=1.579819e+00, mse=2.993516e-03, target_mse=4.214177e-03, formula_ok=True
  - icbr_no_replay: symbolic_s=1.009645e+00, mse=6.674105e-03, target_mse=7.714660e-03, formula_ok=True
  - icbr_no_shared: symbolic_s=3.012055e+00, mse=2.993516e-03, target_mse=4.214176e-03, formula_ok=True
  - icbr_refit_commit: symbolic_s=2.244129e+00, mse=6.890123e-02, target_mse=6.748471e-02, formula_ok=True
- baseline formula (display, rounded):
  - `-0.614702*sin(0.326733*cos(1.39352*x_2 + 0.00319999) - 1.22604*tan(0.49008*x_3 - 5.72104) + 13.2936 - 3.2117*exp(-(-1.0*x_1 - 0.656)**2)) - 0.541862*sin(1.23498*atan(0.86376*x_3 - 0.56288) - 5.82389 + 3.48443*exp(-0.638018*(0.570884 - x_1)**2) + 0.357813*exp(-2.5467*(0.00125327 - x_2)**2)) + 0.493301*tan(0.404433*sin(3.34368*x_1 - 6.59712) - 0.0540245*sin(2.6328*x_3 + 7.1716) - 0.318616*cos(3.17944*x_2 - 9.4088) + 0.0796841) - 0.553512*atan(0.643046*sin(2.97792*x_2 - 1.5864) + 1.42641*atan(0.224*x_3 + 0.17456) - 0.652568 + 1.37025*exp(-3.58087*(-x_1 - 0.34844)**2)) - 0.0890025`
- icbr_full formula (display, rounded):
  - `-0.610319*sin(0.260443*sin(1.6*x_2 - 1.55) - 1.45927*cos(1.9*x_1 + 4.45) - 3.89169 + 8.59152/(3.5 - 1.25*x_3)) + 0.545814*sin(5.60738*cos(0.3*x_3 - 2.65) - 0.437834*Abs(4.55*x_1 - 2.5) + 5.43582 + 0.354922*exp(-2.56*(-x_2 - 1.49012e-7)**2)) - 0.483003*tan(0.0553822*sin(2.6*x_3 + 0.9) + 0.411445*cos(3.35*x_1 - 5.0) - 0.325673*cos(3.15*x_2 + 2.38419e-7) - 3.2149) + 0.558126*atan(3.41459*(0.0222222*x_3 - 1)**4 + 0.632125*sin(3.0*x_2 + 1.55) - 2.9935 - 1.35748*exp(-3.4225*(-x_1 - 0.351351)**2)) - 0.0761196`
- icbr_no_replay formula (display, rounded):
  - `0.610319*sin(1.45927*cos(1.9*x_1 + 4.45) + 0.326708*cos(1.4*x_2 + 2.38419e-7) - 1.22729*tan(0.5*x_3 + 0.55) + 2.11216) + 0.545814*sin(1.17227*atan(0.9*x_3 - 0.55) - 2.73965 + 0.354922*exp(-2.56*(-x_2 - 1.49012e-7)**2) + 3.47903*exp(-0.64*(x_1 - 0.5625)**2)) - 0.483003*tan(0.411638*sin(3.35*x_1 - 3.45) + 0.323164*sin(3.2*x_2 - 1.55) - 0.0547254*cos(2.65*x_3 + 2.45) - 3.21904) + 0.558126*atan(0.632125*sin(3.0*x_2 + 1.55) - 1.58907*atan(0.2*x_3 + 0.2) + 0.734319 - 1.35748*exp(-3.4225*(-x_1 - 0.351351)**2)) - 0.0761196`
- icbr_no_shared formula (display, rounded):
  - `-0.610319*sin(0.260443*sin(1.6*x_2 - 1.55) - 1.45927*cos(1.9*x_1 + 4.45) - 3.89169 + 8.59152/(3.5 - 1.25*x_3)) + 0.545814*sin(5.60738*cos(0.3*x_3 - 2.65) - 0.437834*Abs(4.55*x_1 - 2.5) + 5.43582 + 0.354922*exp(-2.56*(-x_2 - 1.49012e-7)**2)) - 0.483003*tan(0.0553822*sin(2.6*x_3 + 0.9) + 0.411445*cos(3.35*x_1 - 5.0) - 0.325673*cos(3.15*x_2 + 2.38419e-7) - 3.2149) + 0.558126*atan(3.41459*(0.0222222*x_3 - 1)**4 + 0.632125*sin(3.0*x_2 + 1.55) - 2.9935 - 1.35748*exp(-3.4225*(-x_1 - 0.351351)**2)) - 0.0761196`
- icbr_refit_commit formula (display, rounded):
  - `-5.75153*sqrt(-0.0239463*sin(2.25052*x_1 - 0.70624) - 0.0279123*cos(0.70004*x_3 + 3.01868) + 1 - 0.933642*exp(-0.0506249*x_2**2)) - 12.6612*sin(-0.320643*Abs(1.1094*x_1 + 0.80772) + 0.0110717*Abs(4.38984*x_2 + 0.04352) + 4.55185 + 0.584495/(1.35784 - 0.48512*x_3)) - 0.548872*cos(2.87889*sin(1.00002*x_2 + 4.712) + 1.88154*tanh(0.16156*x_3 + 0.20824) + 1.09065 - 1.08529*exp(-3.18951*(0.689169 - x_1)**2)) - 10.7196 + 0.977752*exp(-15.1097*(cos(0.31196*x_3 + 0.50796) + 0.3936*Abs(0.89716*x_1 - 0.56092) - 0.21005 - 0.604447*exp(-0.118336*(0.0102326 - x_2)**2))**2)`

### task=trig_interaction seed=6

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics: mse=1.032247e-02, r2=0.986609
- Variant formula overview:
  - baseline: symbolic_s=2.240519e+01, mse=3.565518e-03, target_mse=1.413354e-02, formula_ok=True
  - icbr_full: symbolic_s=1.557397e+00, mse=4.115772e-03, target_mse=1.604347e-02, formula_ok=True
  - icbr_no_replay: symbolic_s=9.579400e-01, mse=4.480192e-03, target_mse=1.574279e-02, formula_ok=True
  - icbr_no_shared: symbolic_s=2.799119e+00, mse=4.115773e-03, target_mse=1.604348e-02, formula_ok=True
  - icbr_refit_commit: symbolic_s=2.100547e+00, mse=7.765187e-02, target_mse=8.713644e-02, formula_ok=True
- baseline formula (display, rounded):
  - `0.77835*tanh(0.460213*sin(2.84232*x_1 - 6.20104) - 1.1278 + 1.57326*exp(-2.16937*(-x_2 - 0.00325892)**2)) - 0.284532*tanh(1.50696*sin(1.89424*x_2 - 1.59336) + 1.30556*tanh(2.6*x_3 - 2.064) - 4.41329 + 6.17426*exp(-2.24137*(-x_1 - 0.586032)**2)) + 0.417337 + 0.984575*exp(-4.0338*(0.115699*cos(1.21096*x_2 - 9.41184) + 0.443511*atan(0.72288*x_3 - 0.44768) - 0.126774 + exp(-1.3734*(-x_1 - 0.450338)**2))**2) - 1.34455*exp(-1.68623*(0.072747*(0.0486808 - x_2)**2 - 0.49008*atan(0.80464*x_3 - 0.35128) + 0.179531 - exp(-1.33393*(0.531066 - x_1)**2))**2)`
- icbr_full formula (display, rounded):
  - `-0.566038*sin(-0.197143*(0.05 - x_2)**2 + 1.33578*atan(0.8*x_3 - 0.35) + 1.06332 + 2.73529*exp(-1.3225*(x_1 - 0.521739)**2)) - 0.665608*cos(0.52021*cos(2.85*x_1 - 1.5) - 6.01763 + 1.79556*exp(-2.1025*(-x_2 - 1.64427e-7)**2)) - 0.108448 + 1.01611*exp(-3.41833*(0.551001*tanh(0.6*x_3 - 0.45) + 0.169403 - 0.344598*exp(-0.25*(x_2 - 4.76837e-7)**2) + exp(-1.44*(-x_1 - 0.458333)**2))**2) - 0.60691*exp(-3.10758*(0.916205*sin(2.45*x_1 + 3.05) - 0.452596*sin(1.9*x_2 + 1.55) + 0.378481*tanh(2.7*x_3 - 2.1) - 1)**2)`
- icbr_no_replay formula (display, rounded):
  - `-0.665608*cos(0.52021*cos(2.85*x_1 - 1.5) - 6.01763 + 1.79556*exp(-2.1025*(-x_2 - 1.64427e-7)**2)) + 0.655412 - 0.60691*exp(-10.7131*(-0.243761*sin(1.9*x_2 + 1.55) + 0.203843*tanh(2.7*x_3 - 2.1) - 0.995856 + exp(-2.4025*(-x_1 - 0.580645)**2))**2) + 1.01611*exp(-3.41833*(0.0813074*sin(1.5*x_2 - 1.55) + 0.465958*atan(0.7*x_3 - 0.45) - 0.129295 + exp(-1.44*(-x_1 - 0.458333)**2))**2) - 1.33793*exp(-1.69656*(-0.0720738*(0.05 - x_2)**2 + 0.488349*atan(0.8*x_3 - 0.35) - 0.179752 + exp(-1.3225*(x_1 - 0.521739)**2))**2)`
- icbr_no_shared formula (display, rounded):
  - `-0.566038*sin(-0.197143*(0.05 - x_2)**2 + 1.33578*atan(0.8*x_3 - 0.35) + 1.06332 + 2.73529*exp(-1.3225*(x_1 - 0.521739)**2)) - 0.665608*cos(0.52021*cos(2.85*x_1 - 1.5) - 6.01763 + 1.79556*exp(-2.1025*(-x_2 - 1.64427e-7)**2)) - 0.108448 + 1.01611*exp(-3.41833*(0.551001*tanh(0.6*x_3 - 0.45) + 0.169403 - 0.344598*exp(-0.25*(x_2 - 4.76837e-7)**2) + exp(-1.44*(x_1 + 0.458333)**2))**2) - 0.60691*exp(-3.10758*(0.916205*sin(2.45*x_1 + 3.05) - 0.452596*sin(1.9*x_2 + 1.55) + 0.378481*tanh(2.7*x_3 - 2.1) - 1)**2)`
- icbr_refit_commit formula (display, rounded):
  - `-16.8624*sin(0.199547*sin(0.75336*x_3 + 2.68524) + 0.0620718*Abs(4.08964*x_1 - 2.66036) - 4.56133 - 0.516693*exp(-0.0520204*(0.052087 - x_2)**2)) - 3.85686*cos(-0.556168*tanh(0.51668*x_3 - 0.4712) + 2.40568 + 0.726448*exp(-2.33833*(0.821889 - x_1)**2) + 0.0664281*exp(-2.07936*(0.01043 - x_2)**2)) - 1.25326*tanh(0.235255*cos(2.14264*x_1 + 1.60348) + 19.5339 - 19.5532*exp(-0.0447406*x_2**2)) - 0.269819*atan(0.719749*sin(2.90112*x_2 + 4.71188) + 0.818931*atan(3.9532*x_3 - 3.29624) + 0.502711 - 4.93023*exp(-1.4673*(0.705841 - x_1)**2)) + 13.1003`

### task=trig_interaction seed=7

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics: mse=5.634789e-03, r2=0.992089
- Variant formula overview:
  - baseline: symbolic_s=1.799402e+01, mse=1.490185e-03, target_mse=7.506786e-03, formula_ok=True
  - icbr_full: symbolic_s=1.254319e+00, mse=1.418521e-03, target_mse=7.668084e-03, formula_ok=True
  - icbr_no_replay: symbolic_s=7.943443e-01, mse=1.458059e-03, target_mse=7.777133e-03, formula_ok=True
  - icbr_no_shared: symbolic_s=2.295058e+00, mse=1.418521e-03, target_mse=7.668084e-03, formula_ok=True
  - icbr_refit_commit: symbolic_s=1.741520e+00, mse=1.193234e-01, target_mse=1.239552e-01, formula_ok=True
- baseline formula (display, rounded):
  - `0.340308*cos(-5.49852 + 2.20627*exp(-0.476762*(0.746843 - x_3)**2) + 3.93482*exp(-1.59466*(0.434273 - x_1)**2)) - 0.475844*cos(1.20435*atan(1.7432*x_3 - 1.44312) - 0.105687 + 2.80987*exp(-1.88568*(0.615904 - x_1)**2)) + 1.27561 - 3.19174*exp(-0.256304*(0.176496*cos(3.76304*x_1 + 1.57664) - 1 - 0.823148*exp(-2.55463*(0.000350369 - x_2)**2))**2) + 1.17592*exp(-2.28781*(-0.86377*sqrt(1 - 0.646039*x_3) + 0.624257 + exp(-1.63328*(-x_1 - 0.536401)**2))**2)`
- icbr_full formula (display, rounded):
  - `-0.340384*sin(0.914873*sin(1.45*x_3 + 0.45) + 0.499578 + 3.95235*exp(-1.5625*(0.44 - x_1)**2)) - 0.485858*sin(1.18348*atan(1.75*x_3 - 1.45) - 4.8074 + 2.75838*exp(-1.96*(0.607143 - x_1)**2)) + 1.42161 - 3.44063*exp(-0.275985*(-0.157195*cos(3.75*x_1 - 1.55) - 1 - 0.732957*exp(-2.56*(-x_2 - 1.49012e-7)**2))**2) + 1.18126*exp(-2.23909*(-0.869087*sqrt(1 - 0.646342*x_3) + 0.637468 + exp(-1.69*(-x_1 - 0.538462)**2))**2)`
- icbr_no_replay formula (display, rounded):
  - `-0.340384*sin(0.914873*sin(1.45*x_3 + 0.45) + 0.499578 + 3.95235*exp(-1.5625*(0.44 - x_1)**2)) - 0.485858*sin(1.18348*atan(1.75*x_3 - 1.45) - 4.8074 + 2.75838*exp(-1.96*(0.607143 - x_1)**2)) + 1.42161 + 1.18126*exp(-6.7286*(0.853139*asin(0.1*x_3 + 0.85) - 1 + 0.576864*exp(-1.69*(-x_1 - 0.538462)**2))**2) - 3.44063*exp(-0.275638*(-0.157297*sin(3.75*x_1 + 2.38419e-7) - 1 - 0.733418*exp(-2.56*(-x_2 - 1.49012e-7)**2))**2)`
- icbr_no_shared formula (display, rounded):
  - `-0.340384*sin(0.914873*sin(1.45*x_3 + 0.45) + 0.499578 + 3.95235*exp(-1.5625*(0.44 - x_1)**2)) - 0.485858*sin(1.18348*atan(1.75*x_3 - 1.45) - 4.8074 + 2.75838*exp(-1.96*(0.607143 - x_1)**2)) + 1.42161 - 3.44063*exp(-0.275985*(-0.157195*cos(3.75*x_1 - 1.55) - 1 - 0.732957*exp(-2.56*(-x_2 - 1.49012e-7)**2))**2) + 1.18126*exp(-2.23909*(-0.869087*sqrt(1 - 0.646342*x_3) + 0.637468 + exp(-1.69*(x_1 + 0.538462)**2))**2)`
- icbr_refit_commit formula (display, rounded):
  - `-1.45202*sin(1.7204*sin(1.00004*x_2 - 4.712) + 0.0939264*cos(2.40548*x_1 + 4.694) + 1.71204) + 5.17728*cos(0.0911573*(-0.387689*x_3 - 1)**5 + 2.86957 + 0.669572*exp(-1.54058*(-x_1 - 0.689526)**2)) + 0.330241*cos(0.703843*Abs(2.7906*x_1 - 1.6958) - 0.664858*atan(1.70208*x_3 + 0.55052) + 0.480397) + 5.26079 - 0.929283*exp(-3.18642*(-0.981169*log(3.19552 - 1.098*x_3) - 0.162145*Abs(4.96056*x_1 + 3.3304) + 1)**2)`

### task=trig_interaction seed=8

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics: mse=3.710345e-03, r2=0.994873
- Variant formula overview:
  - baseline: symbolic_s=1.973840e+01, mse=2.656533e-03, target_mse=6.333319e-03, formula_ok=True
  - icbr_full: symbolic_s=1.343619e+00, mse=2.540433e-03, target_mse=6.398233e-03, formula_ok=True
  - icbr_no_replay: symbolic_s=8.407777e-01, mse=2.963724e-03, target_mse=6.898958e-03, formula_ok=True
  - icbr_no_shared: symbolic_s=2.463688e+00, mse=2.540433e-03, target_mse=6.398233e-03, formula_ok=True
  - icbr_refit_commit: symbolic_s=1.907070e+00, mse=7.022427e-02, target_mse=7.185498e-02, formula_ok=True
- baseline formula (display, rounded):
  - `-0.875385*sin(0.274301*sin(3.7168*x_1 - 6.39264) + 2.3582 + 1.3081*exp(-2.37974*(0.00217809 - x_2)**2)) - 0.333188*cos(-1.15032*cos(2.58416*x_1 + 1.60776) + 0.269972 + 0.942376*exp(-7.89385*(1 - 0.980325*x_3)**2)) - 0.38817 + 1.57416*exp(-1.91109*(0.0830289*cos(1.0044*x_2 + 9.40464) + 0.437969*atan(0.85456*x_3 - 0.39496) - 0.108315 + exp(-1.37828*(-x_1 - 0.55816)**2))**2) - 0.912932*exp(-3.6592*(-0.291781*atan(1.28992*x_3 - 0.38584) + 0.319013 - exp(-0.910879*(0.519782 - x_1)**2))**2)`
- icbr_full formula (display, rounded):
  - `0.6607*cos(0.118441*cos(1.5*x_2 - 0.0499997) - 1.2889*atan(0.85*x_3 - 0.4) + 0.466454 - 2.93735*exp(-1.3225*(-x_1 - 0.565217)**2)) + 0.240545*tanh(2.18154*sin(2.6*x_1 + 0.0500002) - 2.17004 + 1.77584*exp(-7.84*(1 - 0.982143*x_3)**2)) + 1.59082 - 0.929634*exp(-3.4568*(0.291517*atan(1.3*x_3 - 0.4) - 0.317585 + exp(-0.9025*(x_1 - 0.526316)**2))**2) - 1.88039*exp(-0.510626*(0.210394*cos(3.7*x_1 + 1.45) - 0.436951 - exp(-2.4025*(-x_2 - 1.53818e-7)**2))**2)`
- icbr_no_replay formula (display, rounded):
  - `-0.340611*cos(1.1344*sin(2.6*x_1 + 0.0500002) + 0.261579 + 0.923436*exp(-7.84*(1 - 0.982143*x_3)**2)) + 0.805186 + 1.50869*exp(-2.0622*(0.0387563*(0.0209424 - x_2)**2 + 0.438798*atan(0.85*x_3 - 0.4) - 0.189998 + exp(-1.3225*(-x_1 - 0.565217)**2))**2) - 0.929634*exp(-3.4568*(0.291517*atan(1.3*x_3 - 0.4) - 0.317585 + exp(-0.9025*(x_1 - 0.526316)**2))**2) - 1.88039*exp(-0.510626*(0.210394*cos(3.7*x_1 + 1.45) - 0.436951 - exp(-2.4025*(-x_2 - 1.53818e-7)**2))**2)`
- icbr_no_shared formula (display, rounded):
  - `0.6607*cos(0.118441*cos(1.5*x_2 - 0.0499997) - 1.2889*atan(0.85*x_3 - 0.4) + 0.466454 - 2.93735*exp(-1.3225*(-x_1 - 0.565217)**2)) + 0.240545*tanh(2.18154*sin(2.6*x_1 + 0.0500002) - 2.17004 + 1.77584*exp(-7.84*(1 - 0.982143*x_3)**2)) + 1.59082 - 0.929634*exp(-3.4568*(0.291517*atan(1.3*x_3 - 0.4) - 0.317585 + exp(-0.9025*(x_1 - 0.526316)**2))**2) - 1.88039*exp(-0.510626*(0.210394*cos(3.7*x_1 + 1.45) - 0.436951 - exp(-2.4025*(-x_2 - 1.53818e-7)**2))**2)`
- icbr_refit_commit formula (display, rounded):
  - `0.921041*cos(2.21604*sin(1.1*x_2 + 4.712) + 0.145573*cos(2.3778*x_1 + 1.51772) + 3.37264) + 21.0305*cos(0.179491*sin(0.80296*x_3 - 0.4898) - 0.083049*Abs(3.09176*x_1 + 2.09464) + 0.00303754*Abs(4.98164*x_2 + 0.00016) + 0.357768) + 8.34455 - 24.5023*exp(-0.0301194*(-0.442396*tanh(1.03036*x_3 - 0.30888) + 0.264122*Abs(2.88324*x_1 - 1.75076) - 1)**2) - 4.89729*exp(-0.11948*(0.068671*(-x_3 - 0.494608)**5 - 0.658839 + exp(-1.49456*(-x_1 - 0.70268)**2))**2)`

### task=trig_interaction seed=9

- Task source: synthetic_formula
- Target formula: `None`
- Teacher cache: hit=False, mode=readwrite, status=miss_write
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics: mse=5.634702e-03, r2=0.992655
- Variant formula overview:
  - baseline: symbolic_s=2.114285e+01, mse=2.291829e-03, target_mse=8.298097e-03, formula_ok=True
  - icbr_full: symbolic_s=1.464849e+00, mse=2.244096e-03, target_mse=8.001450e-03, formula_ok=True
  - icbr_no_replay: symbolic_s=9.202890e-01, mse=2.422648e-03, target_mse=8.518361e-03, formula_ok=True
  - icbr_no_shared: symbolic_s=2.695093e+00, mse=2.244096e-03, target_mse=8.001450e-03, formula_ok=True
  - icbr_refit_commit: symbolic_s=1.993415e+00, mse=4.782280e-02, target_mse=5.554846e-02, formula_ok=True
- baseline formula (display, rounded):
  - `0.757538*atan(0.543263*sin(2.96456*x_2 + 1.60584) - 0.610547*cos(2.75152*x_1 + 1.58568) + 0.603117 - 0.251946*exp(-11.2037*(1 - 0.995961*x_3)**2)) + 0.548072*atan(0.0975099*sin(3.94504*x_3 - 8.79) - 0.760464*cos(2.7164*x_1 + 1.58296) - 1.46229 + 1.32485*exp(-2.68383*(0.0178728 - x_2)**2)) + 0.261186 + 0.871719*exp(-2.94135*(-0.0744691*Abs(9.95544*x_1 + 5.28312) + 0.683707*atan(0.602*x_3 - 0.562) + 1)**2) - 1.21792*exp(-2.45961*(0.392418*(-0.239845*x_3 - 1)**3 + 0.895403 - exp(-0.87131*(0.557936 - x_1)**2))**2)`
- icbr_full formula (display, rounded):
  - `1.55937*tanh(0.322131*sin(2.75*x_1 + 2.38419e-7) - 0.287331*sin(2.95*x_2 - 1.55) + 0.683626 - 0.131933*exp(-11.2225*(1 - x_3)**2)) + 0.556457*atan(0.0960718*sin(3.95*x_3 - 2.5) + 0.748063*cos(2.7*x_1 - 1.55) + 0.579717*cos(3.25*x_2 - 0.0499997) - 0.747473) - 0.265064 + 0.846275*exp(-16.0354*(-0.848877*sin(0.3*x_3 + 2.15) - 0.0673499*Abs(4.9*x_1 + 2.6) + 1)**2) - 1.18168*exp(-2.76437*(0.427274*(0.15942*x_3 + 1)**4 - 0.948307 + exp(-0.81*(x_1 - 0.555556)**2))**2)`
- icbr_no_replay formula (display, rounded):
  - `0.556457*atan(0.0960718*sin(3.95*x_3 - 2.5) + 0.748063*cos(2.7*x_1 - 1.55) - 1.45022 + 1.29899*exp(-2.7225*(0.0303029 - x_2)**2)) + 0.745867*atan(0.62225*cos(2.75*x_1 - 1.55) + 0.555817*cos(2.95*x_2 + 0.0500002) + 0.60324 - 0.25507*exp(-11.2225*(1 - x_3)**2)) + 0.265233 + 0.846275*exp(-4.38231*(0.830914*tanh(0.45*x_3 - 0.6) - 0.128833*Abs(4.9*x_1 + 2.6) + 1)**2) - 1.18168*exp(-2.76437*(0.381272*(0.23913*x_3 + 1)**3 - 0.902338 + exp(-0.81*(x_1 - 0.555556)**2))**2)`
- icbr_no_shared formula (display, rounded):
  - `1.55937*tanh(0.322131*sin(2.75*x_1 + 2.38419e-7) - 0.287331*sin(2.95*x_2 - 1.55) + 0.683626 - 0.131933*exp(-11.2225*(1 - x_3)**2)) + 0.556457*atan(0.0960718*sin(3.95*x_3 - 2.5) + 0.748063*cos(2.7*x_1 - 1.55) + 0.579717*cos(3.25*x_2 - 0.0499997) - 0.747473) - 0.265064 + 0.846275*exp(-16.0354*(-0.848877*sin(0.3*x_3 + 2.15) - 0.0673499*Abs(4.9*x_1 + 2.6) + 1)**2) - 1.18168*exp(-2.76437*(0.427274*(0.15942*x_3 + 1)**4 - 0.948307 + exp(-0.81*(x_1 - 0.555556)**2))**2)`
- icbr_refit_commit formula (display, rounded):
  - `116.617*(-0.0208624*sin(0.69704*x_3 - 1.60388) + 0.0216617*cos(2.1606*x_1 - 4.7068) + 0.917139 - exp(-0.0407716*(0.030309 - x_2)**2))**2 + 7.72316*cos(-0.29726*(-0.159406*x_3 - 1)**4 + 0.0965376*Abs(4.18948*x_1 - 2.65912) + 3.05021) - 0.996756*atan(0.442339*sin(2.15788*x_1 + 3.19448) + 22.2158 - 23.2081*exp(-0.0407232*(-x_2 - 0.0202181)**2) + 2.35621*exp(-8.12683*(1 - 0.467609*x_3)**2)) - 0.725612 + 7.54121*exp(-2.25384*(-0.922096*sin(0.21404*x_3 - 4.26924) - 0.0404685*Abs(4.43296*x_1 + 2.71916) + 1)**2)`

## Visualization Summary

- `icbr_benchmark_symbolic_time_errorbar.png`
- `icbr_benchmark_speedup_boxplot.png`
- `icbr_benchmark_mse_shift_boxplot.png`
- `icbr_benchmark_variant_overview.png`
- `icbr_benchmark_q123_evidence_by_task.png`
## Visualization Design Guide

- `Violin + Scatter (vertical)`: 适合按 task 看变体的 seed 分布与离散度（密度 + 个体点）。
- `Grouped Bar + 95% CI`: 适合论文/汇报中的均值对比与不确定性表达（推荐用于 variant 对比主图）。
- `Boxplot`: 适合强调中位数、IQR 与离群点，做稳健性补充。
- `Recommended Combo`: A=分组柱状+95%CI（主结论），B=小提琴+散点（分布），C=箱线图（稳健性）。

## Extensibility Notes

- 任务可扩展：在任务解析层新增 task token 或 task spec，即可复用统一导出与统计管线。
- 统计可扩展：新增 benchmark 指标后，可自动进入 task stats（count/mean/median/std/min/max）。
- 显著性可扩展：可在 `_SIGNIFICANCE_DIRECTIONS` 增加需要方向性判断的 delta 指标。
- 门禁可扩展：可在 `_TaskSpec` 中为单任务覆盖 teacher MSE/R2 阈值。
