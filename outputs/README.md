# Outputs

This directory stores run-generated artifacts and long-lived experiment archives.

- `outputs/benchmark_runs/`: default output root for `symkanbenchmark.py`.
- `outputs/benchmark_ab/`: archived A/B benchmark comparisons.
- `outputs/benchmark_ablation/`: archived ablation runs and derived analyses.

Scripts now default to these locations. Legacy root-level directories such as `benchmark_runs/`,
`benchmark_ab/`, and `benchmark_ablation/` are still recognized when reading older results.
