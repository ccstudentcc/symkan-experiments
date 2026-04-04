# Project Rules

- When `benchmark_ab_compare.py` changes compare semantics or output files, also sync `docs/symkanbenchmark_usage.md`, `docs/full_experiment_runbook.md`, `docs/engineering_rerun_report.md`, `docs/engineering_version_rerun_note.md`, and `docs/engineering_release_checklist.md`.
- Keep `docs/engineering_rerun_report.md` as the stable rerun index; new engineering reruns must create or update a date-stamped `docs/engineering_rerun_report_YYYYMMDD.md` body instead of overwriting older reports.
- For `docs/design.md` experiment-section rewrites, read `docs/ablation_report.md`, `docs/layerwiseft_improved_report.md`, `docs/engineering_rerun_report_20260318.md`, and `docs/engineering_rerun_report_20260401.md` first; include `docs/engineering_rerun_report_20260327.md` only when historical compare lines are discussed.
- Documentation in this repo should use a rigorous engineering style: concise, precise, and free of AI-assistant phrasing, tutorial chatter, or conversational filler.
- When adding or revising docs, prefer stable operational wording over second-person guidance; keep commands and contracts explicit, but keep the prose restrained.
- Treat any single baseline-backend vs icbr-backend compare as valid backend-only evidence only when `baseline_icbr_shared_check.csv` reports `shared_symbolic_prep_aligned=True` and `trace_summary.csv` shows identical trace rhythm.
- Treat `baseline_icbr_fulllib`-style single-variant reruns as supplementary evidence only; without a paired baseline compare and `baseline_icbr_shared_check.csv`, do not describe them as backend-only compare evidence.
- If a library-only benchmark variant should reuse existing numeric/shared-prep caches, keep the change inside `symbolize.lib` / `symbolize.lib_hidden` / `symbolize.lib_output`; changing non-`symbolize` sections will fork the numeric cache key.
- Treat `outputs/**/_numeric_cache/` and `outputs/**/_symbolic_prep_cache/` as runtime-only caches; ignore them in git and do not stage them as benchmark deliverables.
- For documentation-system changes, read `docs/documentation_governance.md` before editing `README.md` or `docs/index.md`; treat it as the layer-role contract, and use `docs/doc_sync_matrix.md` as the impacted-file SSOT.
- When adding, removing, or re-scoping a core document, also sync `docs/documentation_governance.md`, `docs/index.md`, `README.md`, `CONTRIBUTING.md`, and `docs/engineering_release_checklist.md`.
