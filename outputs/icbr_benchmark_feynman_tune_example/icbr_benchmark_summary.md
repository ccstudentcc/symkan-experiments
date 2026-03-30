# ICBR Benchmark Summary

## Run Config

- Profile: feynman_reference
- Tasks: feynman_I_12_4
- Seeds: 1
- Train/Test samples per task: 2000/1000
- Train steps: 200, lr: 0.01, lamb: 0.01
- Teacher cache: mode=off, dir=outputs\teacher_cache_feynman_tune, version=feynman_tune_v1
- ICBR shortlist topk: 3, grid_number: 21, iteration: 2
- Variants: baseline, icbr_full
- Teacher prune policy: enabled=False, node_th=0.01, edge_th=0.01, prune_iters=3
- Feynman data: root=datasets, variant=Feynman_with_units, split=random, split_seed=1, select_seed=1, width_mid=[5, 2], prune_iters=3

## Task-Level Aggregate Stats

| task | n | teacher_cache_hit_mean | teacher_mse_mean | teacher_r2_mean | teacher_gate_pass_mean | baseline_symbolic_mean | icbr_symbolic_mean | delta_mean | delta_median | speedup_mean | speedup_median | mse_shift_mean | target_mse_shift_mean | formula_pass_mean |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| feynman_I_12_4 | 1 | 0.0000 | 6.969286e-04 | 0.004922 | 1.0000 | 49.902263 | 2.559894 | 47.342369 | 47.342369 | 19.4939 | 19.4939 | 4.557146e-10 | 2.512825e-07 | 1.0000 |

## Statistical Significance (by task)

| task | metric | favorable_direction | n_total | n_finite | n_effective | improved | worsened | ties | p_value_two_sided | mean_delta_ci95 |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| feynman_I_12_4 | symbolic_wall_time_delta_s | positive | 1 | 1 | 1 | 1 | 0 | 0 | 1.000000 | [4.734237e+01, 4.734237e+01] |
| feynman_I_12_4 | final_mse_loss_shift | negative | 1 | 1 | 1 | 0 | 1 | 0 | 1.000000 | [4.557146e-10, 4.557146e-10] |

## Variant Ablation Aggregate Stats (Stage 15)

| task | variant | n | teacher_gate_pass_mean | formula_pass_mean | symbolic_mean_s | speedup_mean_x | mse_shift_mean | target_mse_shift_mean | replay_rank_inversion_mean | refit_drift_l2_mean |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| feynman_I_12_4 | baseline | 1 | 1.0000 | 1.0000 | 49.902263 | 1.0000 | 0.000000e+00 | 0.000000e+00 | nan | nan |
| feynman_I_12_4 | icbr_full | 1 | 1.0000 | 1.0000 | 2.559894 | 19.4939 | 4.557146e-10 | 2.512825e-07 | 0.285714 | nan |

## Critique Evidence Summary (Q1/Q2/Q3)

| task | n | q1_candidate_ratio_mean | q1_symbolic_ratio_mean | q2_mse_gain_mean | q2_target_mse_gain_mean | q2_rank_inversion_mean | q3_mse_gain_mean | q3_target_mse_gain_mean | q3_refit_drift_mean |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| __overall__ | 0 | nan | nan | nan | nan | 0.285714 | nan | nan | nan |
| feynman_I_12_4 | 0 | nan | nan | nan | nan | 0.285714 | nan | nan | nan |

## Per-Run Performance Details

| task | seed | cache_hit | cache_status | teacher_mse | teacher_r2 | teacher_gate | candidate_s | replay_s | baseline_symbolic_s | icbr_symbolic_s | speedup_x | baseline_mse | icbr_mse | mse_shift | baseline_target_mse | icbr_target_mse | target_mse_shift | formula_ok |
|---|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| feynman_I_12_4 | 1 | False | off_no_cache | 6.969286e-04 | 0.004922 | True | 1.662975 | 0.659607 | 49.902263 | 2.559894 | 19.4939 | 8.623404e-09 | 9.079119e-09 | 4.557146e-10 | 6.962453e-04 | 6.964966e-04 | 2.512825e-07 | True |

## Feynman Dataset Metadata

### feynman_I_12_4

- Dataset file: `I.12.4`
- Dataset path: `D:\chenpeng\Documents\学习\数学\毕业论文\symkan-experiments\datasets\Feynman_with_units\I.12.4`
- Raw data shape: rows=1000000, columns=4, n_var=3
- Split setting: strategy=random, split_seed=1, train_num=2000, test_num=1000
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

## Formula Comparison

### task=feynman_I_12_4 seed=1

- Task source: feynman_file
- Target formula: `q1*r/(4*pi*epsilon*r**3)`
- Teacher cache: hit=False, mode=off, status=off_no_cache
- Teacher quality gate: pass=True; reason=``
- Teacher target metrics: mse=6.969286e-04, r2=0.004922
- Variant formula overview:
  - baseline: symbolic_s=4.990226e+01, mse=8.623404e-09, target_mse=6.962453e-04, formula_ok=True
  - icbr_full: symbolic_s=2.559894e+00, mse=9.079119e-09, target_mse=6.964966e-04, formula_ok=True
- baseline formula (display, rounded):
  - `0.00721625*(-0.102014*(-0.0195549 - 0.159809*exp(-99.0941*(1 - 0.944287*x_1)**2))*(0.0911951*Abs(1.8448*x_2 - 3.27752) + 0.224965) + 1)**5 - 0.000325024*cos(0.155064*Abs(4.46208*x_1 - 8.30696) + 1.1058 - 0.397637*exp(-99.9988*(1 - 0.900005*x_2)**2)) - 0.000112807*Abs(0.399533*Abs(2.22024*x_3 - 4.0368) - 0.0680893 + 0.754851*exp(-98.8434*(0.90686*x_2 - 1)**2)) + 0.0120428 + 4.19122e-11/(-(-0.0685058*Abs(3.32*x_1 - 5.59968) + 0.0244012*Abs(3.4704*x_3 - 6.33064) - 0.178828)*(-0.0193187*Abs(3.76208*x_1 - 7.13176) - 0.0973871 + 0.0246343*exp(-98.6049*(1 - 0.88862*x_2)**2)) - 0.0713222)**5`
- icbr_full formula (display, rounded):
  - `-0.000571597*(-0.091787*Abs(2.55*x_1 - 4.75) + 0.0541972*sign(3.5 - 2.95*x_2) + 1)**2 - 0.000234119*tanh(0.161283*Abs(2.75*x_3 - 5.0) + 0.157367*sign(3.9 - 3.3*x_2) - 0.674213) + 0.0151373 - 4.2239e-11/((-0.0302845*Abs(2.4*x_1 - 4.55) + 0.00874211*sign(3.5 - 2.9*x_2) - 0.0883942)*(-0.0770928*Abs(2.95*x_1 - 4.975) + 0.0635112 - 0.228716*exp(-1.69*(1 - 0.5*x_3)**2)) + 0.0714286)**5 - 0.00431315/(-0.166667*(0.0686367*Abs(2.45*x_2 - 4.35) + 0.224955)*(-0.0603097*sign(3.9 - 3.35*x_1) - 0.0803577) - 1)**5`

## Visualization Summary

- `icbr_benchmark_symbolic_time_errorbar.png`
- `icbr_benchmark_speedup_boxplot.png`
- `icbr_benchmark_mse_shift_boxplot.png`
- `icbr_benchmark_variant_overview.png`

## Visualization Design Guide

- `Point + 95% CI`: 适合论文里的主结论图；正值偏态指标优先用几何均值与 log 轴，不用柱面积暗示额外量感。
- `Violin + Box + Points`: 适合 speedup / mse shift 这类分布图；当前固定 KDE 带宽规则为 `Silverman`。
- `Task-Row Two-Panel Grid`: 适合 variant overview；每个 task 一行，左列 `SymbolicTime`，右列合并 `ImitationMSE + TargetMSE`，两列都显式标尺度。
- `Q1/Q2/Q3`: 三个 panel 都用相对 `icbr_full` 的 ratio 值，并在 log 轴上展示 `几何均值 + 95% CI`，1 表示与 full 持平。
- `Recommended Combo`: A=point+95%CI（正值偏态指标用几何均值），B=violin+box+points（分布），C=task-row two-panel grid（多指标 overview）。

## Extensibility Notes

- 任务可扩展：在任务解析层新增 task token 或 task spec，即可复用统一导出与统计管线。
- 统计可扩展：新增 benchmark 指标后，可自动进入 task stats（count/mean/median/std/min/max）。
- 显著性可扩展：可在 `_SIGNIFICANCE_DIRECTIONS` 增加需要方向性判断的 delta 指标。
- 门禁可扩展：可在 `_TaskSpec` 中为单任务覆盖 teacher MSE/R2 阈值。
