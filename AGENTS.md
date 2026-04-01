# Project Rules

- When `benchmark_ab_compare.py` changes compare semantics or output files, also sync `docs/symkanbenchmark_usage.md`, `docs/full_experiment_runbook.md`, `docs/engineering_rerun_report.md`, `docs/engineering_version_rerun_note.md`, and `docs/engineering_release_checklist.md`.
- Treat `baseline` vs `baseline_icbr` as a valid backend-only compare only when `baseline_icbr_shared_check.csv` reports `shared_symbolic_prep_aligned=True` and `trace_summary.csv` shows identical trace rhythm.
