# Task Status

## Current Objective

Keep the repaired ICBR integration documented and interpretable across both the minimal layered-library compare and the wider `FAST_LIB` compare: baseline remains the default symbolic backend, while single baseline-backend vs icbr-backend pairs are treated as backend-only compares with shared numeric and shared symbolic-prep semantics.

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
  - `outputs/rerun_v2_engine_safe_20260401/benchmark_ab/baseline_fastlib`
  - `outputs/rerun_v2_engine_safe_20260401/benchmark_ab/baseline_icbr_fastlib`
  - `outputs/rerun_v2_engine_safe_20260401/benchmark_ab/baseline_icbr_fulllib`
- Compare artifacts regenerated under:
  - `outputs/rerun_v2_engine_safe_20260401/benchmark_ab/comparison`
  - `outputs/rerun_v2_engine_safe_20260401/benchmark_ab/comparison_fastlib`

## Key Decisions

- Keep the existing symbolic pipeline entrypoint and dispatch internally by backend.
- Treat `(numeric=0, symbolic=0)` as the correct terminal state for pruned edges in ICBR.
- Exclude `symbolize` config from the numeric-cache key so backend-only benchmark variants share one numeric training result.
- Keep library-only compare deltas inside `symbolize.lib` / `symbolize.lib_hidden` / `symbolize.lib_output` so widened-library variants still reuse the same numeric cache.
- Move the benchmark cache boundary forward from numeric-stage end to the shared symbolic-prep boundary, so backend-only comparisons never rerun prune/input-compaction/pre-symbolic-fit.
- Do not attribute cached numeric-stage wall-time or cached symbolic-prep wall-time to current symbolization-only runs; expose them separately via `cached_stage_total_seconds_ref` and `cached_symbolic_prep_seconds_ref`.
- Keep the new compare-only ICBR indicators gated to a single baseline-backend vs icbr-backend pair so generic A/B workflows are untouched.

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
    - mean `symbolic_core_speedup_vs_baseline = 1.751763`
    - mean `final_teacher_imitation_mse_shift = -0.006330`
    - mean `final_target_mse_shift = -0.008691`
    - mean `final_target_r2_shift = 0.096602`
  - `comparison/baseline_icbr_mechanism_summary.csv` now reports candidate generation at about `1.7539%` of core time and replay rerank at about `97.6469%`.
  - For seeds `42,52,62`, `baseline_fastlib` and `baseline_icbr_fastlib` also have identical:
    - `base_acc`
    - `enhanced_acc`
    - `enhanced_n_edge`
    - `selected_stage`
    - `selected_score`
    - `pre_symbolic_n_edge`
  - `comparison_fastlib/trace_summary.csv` reports identical `Symbolize Trace Rhythm` for `baseline_fastlib` and `baseline_icbr_fastlib`.
  - `comparison_fastlib/baseline_icbr_shared_check.csv` reports `shared_symbolic_prep_aligned=True` for all three seeds.
  - Both fastlib variants have `numeric_cache_hit=True` and `symbolic_prep_cache_hit=True` for all three seeds.
  - `comparison_fastlib/baseline_icbr_primary_effect.csv` reports:
    - mean `symbolic_core_speedup_vs_baseline = 2.350452`
    - mean `final_teacher_imitation_mse_shift = 0.000062`
    - mean `final_target_mse_shift = -0.000023`
    - mean `final_target_r2_shift = 0.000258`
  - `comparison_fastlib/baseline_icbr_mechanism_summary.csv` now reports candidate generation at about `3.5573%` of core time and replay rerank at about `96.0892%`.
  - `baseline_icbr_fulllib` is now available as a supplementary single-arm slice:
    - `baseline_fulllib` was intentionally skipped because the full-library baseline path is too slow for this rerun.
    - mean `final_acc = 0.795433`
    - mean `macro_auc = 0.963225`
    - mean `final_target_r2 = 0.601003`
    - mean `symbolic_core_seconds = 35.218785`

## Residual Risks

- `symbolize_wall_time_s` is still a wall-clock measure that includes export overhead, so the compare conclusion for baseline/icbr should prefer `symbolic_core_seconds` and the new specialized summary tables.
- The symbolic-prep cache key intentionally excludes backend-only settings; if future workflows introduce additional shared-prep toggles, they must be added to `_symbolic_prep_cache_key`.
- The FAST_LIB slice improves speed much more strongly than the layered-library slice, but quality deltas are near-zero and mixed in sign; this should be reported as a speed-focused result, not a broad quality-improvement claim.
- `baseline_icbr_fulllib` can demonstrate that ICBR keeps the full-library path runnable and can bring single-arm gains, but it is not paired backend-only evidence because no `baseline_fulllib` compare was generated.
- Historical CSVs generated before this repair do not contain the new `final_teacher_imitation_mse` / `final_target_*` / `symbolic_prep_*` columns and should not be mixed into the new comparison set.

## Next Step

Current follow-up is documentation-oriented rather than implementation-oriented:

1. Keep `ARCHITECTURE.md`、`SPEC.md` and the `docs/` corpus aligned with both `comparison/` and `comparison_fastlib/`.
2. Keep `docs/engineering_rerun_report.md` as the stable rerun index and add future experimental prose to date-stamped `docs/engineering_rerun_report_YYYYMMDD.md` files instead of overwriting older reports.
3. If future backend variants are added, extend the compare-only reporting path without polluting the generic benchmark compare contract.
