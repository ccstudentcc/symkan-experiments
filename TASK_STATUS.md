# Task Status

## Current Objective

Rewrite `docs/design.md` into a paper-style SymKAN design manuscript that matches the current repository structure, the current engineering evidence, and the current documentation role split.

## Current Status

- `README.md`, `ARCHITECTURE.md`, and the last 10 commits have been reviewed.
- The current `docs/design.md` has been identified as a design-note style document rather than a thesis-style manuscript.
- The reference structure from `..\\ICBR-KAN\\ICBR-KAN_design.md` has been analyzed.
- Current evidence sources have been mapped:
  - `docs/ablation_report.md`
  - `docs/layerwiseft_improved_report.md`
  - `docs/engineering_rerun_report_20260401.md`
  - `outputs/rerun_v2_engine_safe_20260401/benchmark_ab/comparison/*`
  - `outputs/rerun_v2_engine_safe_20260401/benchmark_ab/comparison_fastlib/*`
- Task-tracking files are being refreshed for this document rewrite.
- `SPEC.md`, `IMPLEMENTATION_PLAN.md`, and `TASK_STATUS.md` have been updated for this rewrite task.
- `docs/design.md` has been rewritten into a paper-style manuscript with explicit evidence and claim boundaries.
- `docs/engineering_rerun_report.md` has been synced so the stable rerun index now points readers to the new dated `2026-03-18` overall rerun body.
- `README.md`, `docs/index.md`, `docs/project_map.md`, `docs/engineering_version_rerun_note.md`, `docs/full_experiment_runbook.md`, `docs/engineering_release_checklist.md`, and `ARCHITECTURE.md` have been reviewed and selectively updated where the new experiment-line split changed navigation or wording.
- `AGENTS.md` now includes a routing rule for future `docs/design.md` experiment-section rewrites, reducing repeated document-discovery work.
- `git diff --check` has passed.
- Relative links referenced from `docs/design.md` have been sanity-checked successfully.

## Key Decisions

1. Use the paper-style section order from `ICBR-KAN_design.md`, but adapt it from a single-algorithm narrative to an engineering-pipeline narrative.
2. Keep SymKAN's primary object as a reproducible pipeline:
   - configuration normalization
   - stagewise preparation
   - symbolic completion
   - validation
   - structured export and compare
3. Preserve the repository's live behavior boundaries:
   - `baseline` is still the default backend.
   - `icbr` is still opt-in.
   - backend-only fairness begins only after shared numeric and shared symbolic-prep alignment.
4. Use ablation evidence for module-role claims and backend compare evidence for ICBR-specific claims.
5. Treat `baseline_icbr_fulllib` as supplementary single-arm evidence only.

## Residual Risks

1. The rewritten document could drift into runbook language unless section roles stay strict.
2. The document could overclaim quality improvements if layered and FAST_LIB evidence are not separated carefully.
3. The full-library supplementary slice could be misread as paired backend-only evidence if not explicitly fenced.
4. `formula_export_success_rate` could be overstated unless the export-vs-recovery boundary is stated plainly.

## Next Step

The current rewrite-and-sync task is complete. The next optional step is a second editorial pass if a stricter thesis voice or a shorter conference-paper variant is needed.
