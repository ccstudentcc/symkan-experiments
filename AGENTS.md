# Project Rules

- When `benchmark_ab_compare.py` changes compare semantics or output files, also sync `docs/symkanbenchmark_usage.md`, `docs/full_experiment_runbook.md`, `docs/engineering_rerun_report.md`, `docs/engineering_version_rerun_note.md`, and `docs/engineering_release_checklist.md`.
- Treat any single baseline-backend vs icbr-backend compare as valid backend-only evidence only when `baseline_icbr_shared_check.csv` reports `shared_symbolic_prep_aligned=True` and `trace_summary.csv` shows identical trace rhythm.
- Treat `baseline_icbr_fulllib`-style single-variant reruns as supplementary evidence only; without a paired baseline compare and `baseline_icbr_shared_check.csv`, do not describe them as backend-only compare evidence.
- If a library-only benchmark variant should reuse existing numeric/shared-prep caches, keep the change inside `symbolize.lib` / `symbolize.lib_hidden` / `symbolize.lib_output`; changing non-`symbolize` sections will fork the numeric cache key.
- Treat `outputs/**/_numeric_cache/` and `outputs/**/_symbolic_prep_cache/` as runtime-only caches; ignore them in git and do not stage them as benchmark deliverables.
