# Outputs

This directory stores run-generated artifacts and long-lived experiment archives.

- `outputs/benchmark_runs/`: default output root for `python -m scripts.symkanbenchmark`.
- `outputs/benchmark_ab/`: archived A/B benchmark comparisons.
- `outputs/benchmark_ablation/`: archived ablation runs and derived analyses.
- `outputs/notebooks/`: CSV artifacts exported by `notebooks/kan.ipynb`.
- `outputs/rerun_v2_engine_safe_20260318/`: engineering-version rerun archive using `stagewise.guard_mode=light` and `stagewise.prune_acc_drop_tol=0.08`.
- `outputs/rerun_v2_engine_safe_20260318_rerun/`: latest engineering rerun archive for the same config baseline.

For future engineering reruns, prefer naming as `outputs/rerun_v2_engine_safe_<YYYYMMDD>/` for consistent archival.
If you need a second run on the same day, pass `-OutRoot outputs/rerun_v2_engine_safe_<YYYYMMDD>_rerun`.

Scripts now default to these locations. Legacy root-level directories such as `benchmark_runs/`,
`benchmark_ab/`, and `benchmark_ablation/` are still recognized when reading older results.
