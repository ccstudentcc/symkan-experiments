# Task Status

## Current Objective

Keep the repaired ICBR integration documented and interpretable: baseline remains the default symbolic backend, while `baseline` vs `baseline_icbr` is now treated as a backend-only compare with shared numeric and shared symbolic-prep semantics.

## Current Status

- Repository exploration and bug triage complete.
- Opt-in ICBR symbolic backend is wired into `symkan`.
- ICBR no longer converts pruned/off edges into active symbolic zero edges.
- Effective-edge counting now ignores symbolic zero placeholders.
- `scripts.symkanbenchmark` now:
  - applies explicit phase-local reseeding for numeric training,
  - caches pre-symbolic numeric state under the benchmark root,
  - reuses that cache across baseline and baseline_icbr runs,
  - caches the shared symbolic-prep boundary under `_symbolic_prep_cache/`,
  - restores the prepared symbolic state for backend-only reruns,
  - marks cache-hit runs with `numeric_cache_hit`,
  - marks shared-prep cache reuse with `symbolic_prep_cache_hit`,
  - separates cached numeric and cached symbolic-prep reference time from current symbolization-only runtime.
- `symkan.symbolic.pipeline` is now split into:
  - shared pre-backend preparation,
  - backend-specific symbolic completion,
  - preserved public entrypoints for the original call sites.
- `scripts.benchmark_ab_compare` now emits additional baseline/icbr-only summaries without changing the generic compare outputs.
- Requested reruns completed for seeds `42,52,62` under:
  - `outputs/rerun_v2_engine_safe_20260401/benchmark_ab/baseline`
  - `outputs/rerun_v2_engine_safe_20260401/benchmark_ab/baseline_icbr`
- Compare artifacts regenerated under:
  - `outputs/rerun_v2_engine_safe_20260401/benchmark_ab/comparison`

## Key Decisions

- Keep the existing symbolic pipeline entrypoint and dispatch internally by backend.
- Treat `(numeric=0, symbolic=0)` as the correct terminal state for pruned edges in ICBR.
- Exclude `symbolize` config from the numeric-cache key so backend-only benchmark variants share one numeric training result.
- Move the benchmark cache boundary forward from numeric-stage end to the shared symbolic-prep boundary, so backend-only comparisons never rerun prune/input-compaction/pre-symbolic-fit.
- Do not attribute cached numeric-stage wall-time or cached symbolic-prep wall-time to current symbolization-only runs; expose them separately via `cached_stage_total_seconds_ref` and `cached_symbolic_prep_seconds_ref`.
- Keep the new compare-only ICBR indicators gated to the exact `baseline` vs `baseline_icbr` scenario so generic A/B workflows are untouched.

## Validation Snapshot

- Tests passed:
  - `tests/test_icbr_regressions.py`
  - `tests/test_symbolic_pipeline_regressions.py`
  - `tests/test_benchmark_metrics_export.py`
  - `tests/test_app_config.py`
  - `tests/test_benchmark_ab_compare.py`
- Regenerated benchmark observations:
  - For seeds `42,52,62`, baseline and baseline_icbr now have identical:
    - `base_acc`
    - `enhanced_acc`
    - `enhanced_n_edge`
    - `selected_stage`
    - `selected_score`
    - `pre_symbolic_n_edge`
  - `trace_summary.csv` now reports identical `Symbolize Trace Rhythm` for baseline and baseline_icbr.
  - `baseline_icbr_shared_check.csv` reports `shared_symbolic_prep_aligned=True` for all three seeds.
  - `baseline_icbr` has `numeric_cache_hit=True` and `symbolic_prep_cache_hit=True` for all three seeds.
  - `baseline_icbr` final edge counts are now `88,89,88` instead of exploding into the full dense graph.
  - `baseline_icbr_primary_effect.csv` reports:
    - mean `symbolic_core_speedup_vs_baseline = 2.174967`
    - mean `final_teacher_imitation_mse_shift = -0.006009`
    - mean `final_target_mse_shift = -0.008364`
    - mean `final_target_r2_shift = 0.092972`

## Residual Risks

- `symbolize_wall_time_s` is still a wall-clock measure that includes export overhead, so the compare conclusion for baseline/icbr should prefer `symbolic_core_seconds` and the new specialized summary tables.
- The symbolic-prep cache key intentionally excludes backend-only settings; if future workflows introduce additional shared-prep toggles, they must be added to `_symbolic_prep_cache_key`.
- Historical CSVs generated before this repair do not contain the new `final_teacher_imitation_mse` / `final_target_*` / `symbolic_prep_*` columns and should not be mixed into the new comparison set.

## Next Step

Current follow-up is documentation-oriented rather than implementation-oriented:

1. Keep `ARCHITECTURE.md`、`SPEC.md` and the `docs/` corpus aligned with the `2026-04-01` compare outputs.
2. If future backend variants are added, extend the compare-only reporting path without polluting the generic benchmark compare contract.
