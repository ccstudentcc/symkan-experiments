# ICBR Integration Repair Plan

## Goal

Integrate ICBR into `symkan` as an opt-in symbolic backend, keep baseline symbolic fitting as the default, and make the benchmark A/B workflow compare baseline vs ICBR from the same numeric KAN semantics without polluting symbolization-only runtime metrics.

## Constraints

- Default `symkan` behavior must remain baseline-compatible.
- `ICBR-KAN/` is reference-only and does not require validation here.
- Benchmark outputs for this task must land under `outputs/rerun_v2_engine_safe_20260401`.
- Requested benchmark seeds are `42,52,62`.
- Validation must use `C:\Users\chenpeng\miniconda3\envs\kan\python.exe`.

## Stage 1: Backend Wiring

- Goal: Add the smallest stable config/CLI surface to select symbolic backend.
- Success criteria:
  - `SymbolizeConfig` accepts `symbolic_backend`.
  - `scripts.symkanbenchmark` can pass the backend from YAML and CLI.
  - `configs/benchmark_ab/baseline_icbr.yaml` exists and only changes symbolic backend.
- Validation:
  - `pytest tests/test_app_config.py`
- Status: Complete

## Stage 2: ICBR Symbolic Semantics Repair

- Goal: Prevent ICBR from reactivating pruned edges or counting zero placeholder edges as effective symbolic complexity.
- Success criteria:
  - Pruned/off edges remain `(numeric=0, symbolic=0)` in the ICBR loop.
  - ICBR completion only requires no active numeric edges to remain.
  - Effective-edge counting excludes symbolic zero placeholders.
- Validation:
  - `pytest tests/test_icbr_regressions.py`
  - `pytest tests/test_symbolic_pipeline_regressions.py`
- Status: Complete

## Stage 3: Numeric Path Alignment and Cache Reuse

- Goal: Ensure baseline and baseline_icbr reuse the same numeric KAN semantics and avoid retraining when only symbolic backend changes.
- Success criteria:
  - Numeric-phase seeding is explicit and phase-local.
  - Benchmark numeric cache key excludes `symbolize` config, so baseline and baseline_icbr share the same cached numeric state.
  - Cache-hit runs mark `numeric_cache_hit=True` and do not reuse numeric-stage wall-time as current-run wall-time.
- Validation:
  - `pytest tests/test_benchmark_metrics_export.py`
- Status: Complete

## Stage 4: Shared Symbolic-Prep Cache Repair

- Goal: Move the cache boundary from numeric-stage end to the shared symbolic-prep boundary so `baseline` and `baseline_icbr` reuse identical prune/input-compaction/pre-symbolic-fit state.
- Success criteria:
  - `symkan.symbolic.pipeline` is split into a shared preparation step and a backend-specific completion step without breaking the public `symbolize_pipeline()` entrypoint.
  - `scripts.symkanbenchmark` persists shared symbolic-prep bundles under `_symbolic_prep_cache/`.
  - `baseline_icbr` restores the prepared state instead of rerunning prune rounds, so `symbolize_trace.csv` aligns with `baseline`.
  - Symbolization-only timing excludes shared prep and instead records it as a reference metric.
- Validation:
  - `pytest tests/test_symbolic_pipeline_regressions.py`
  - `pytest tests/test_benchmark_metrics_export.py`
- Status: Complete

## Stage 5: Compare-Only ICBR Summary

- Goal: Add a `baseline` vs `baseline_icbr` specialized compare layer inspired by `scripts/icbr_benchmark.py`, without changing the generic compare workflow.
- Success criteria:
  - Generic outputs (`variant_summary.csv`, `pairwise_delta_summary.csv`, `seedwise_delta.csv`, `trace_summary.csv`, `comparison_summary.md`) continue to generate unchanged for ordinary A/B workflows.
  - When the compare pair is exactly `baseline` vs `baseline_icbr`, the script additionally emits:
    - `baseline_icbr_shared_check.csv`
    - `baseline_icbr_primary_effect.csv`
    - `baseline_icbr_mechanism_summary.csv`
  - The markdown summary adds dedicated sections for shared-state checks, primary ICBR effects, and ICBR mechanism breakdown.
- Validation:
  - `pytest tests/test_benchmark_ab_compare.py`
- Status: Complete

## Stage 6: Benchmark Rerun and Compare

- Goal: Regenerate requested A/B outputs and confirm semantic cleanliness under the repaired cache boundary and compare semantics.
- Success criteria:
  - `base_acc`, `enhanced_acc`, `enhanced_n_edge`, `selected_stage`, and `pre_symbolic_n_edge` match between baseline and baseline_icbr for each seed.
  - `trace_summary.csv` shows identical `Symbolize Trace Rhythm` for `baseline` and `baseline_icbr`.
  - `baseline_icbr_shared_check.csv` reports `shared_symbolic_prep_aligned=True` for all requested seeds.
  - `baseline_icbr_primary_effect.csv` and `baseline_icbr_mechanism_summary.csv` are generated successfully.
- Validation:
  - `python -m scripts.symkanbenchmark --tasks full --stagewise-seeds 42,52,62 --config configs/benchmark_ab/baseline.yaml --output-dir outputs/rerun_v2_engine_safe_20260401/benchmark_ab/baseline --quiet`
  - `python -m scripts.symkanbenchmark --tasks full --stagewise-seeds 42,52,62 --config configs/benchmark_ab/baseline_icbr.yaml --output-dir outputs/rerun_v2_engine_safe_20260401/benchmark_ab/baseline_icbr --quiet`
  - `python -m scripts.benchmark_ab_compare --root outputs/rerun_v2_engine_safe_20260401/benchmark_ab --baseline baseline --variants baseline_icbr --output outputs/rerun_v2_engine_safe_20260401/benchmark_ab/comparison`
- Status: Complete

## Validation Evidence

- `C:\Users\chenpeng\miniconda3\envs\kan\python.exe -m pytest tests\test_icbr_regressions.py tests\test_symbolic_pipeline_regressions.py tests\test_benchmark_metrics_export.py tests\test_app_config.py tests\test_benchmark_ab_compare.py`
- `C:\Users\chenpeng\miniconda3\envs\kan\python.exe -m scripts.symkanbenchmark --tasks full --stagewise-seeds 42,52,62 --config configs/benchmark_ab/baseline.yaml --output-dir outputs/rerun_v2_engine_safe_20260401/benchmark_ab/baseline --quiet`
- `C:\Users\chenpeng\miniconda3\envs\kan\python.exe -m scripts.symkanbenchmark --tasks full --stagewise-seeds 42,52,62 --config configs/benchmark_ab/baseline_icbr.yaml --output-dir outputs/rerun_v2_engine_safe_20260401/benchmark_ab/baseline_icbr --quiet`
- `C:\Users\chenpeng\miniconda3\envs\kan\python.exe -m scripts.benchmark_ab_compare --root outputs/rerun_v2_engine_safe_20260401/benchmark_ab --baseline baseline --variants baseline_icbr --output outputs/rerun_v2_engine_safe_20260401/benchmark_ab/comparison`

## Observed Evidence (2026-04-01)

1. `baseline_icbr_shared_check.csv` reports `shared_numeric_aligned=True`、`trace_aligned=True` 与 `shared_symbolic_prep_aligned=True` for seeds `42/52/62`。
2. `trace_summary.csv` shows identical `Symbolize Trace Rhythm` for `baseline` and `baseline_icbr`。
3. `baseline_icbr_primary_effect.csv` reports:
   - `symbolic_core_speedup_vs_baseline = 1.751763`
   - `final_teacher_imitation_mse_shift = -0.006330`
   - `final_target_mse_shift = -0.008691`
   - `final_target_r2_shift = 0.096602`
4. `baseline_icbr_mechanism_summary.csv` shows candidate generation is about `1.7539%` of core time, while replay rerank rises to about `97.6469%` after teacher-output reuse.

## Generated Artifacts

The final comparison set under `outputs/rerun_v2_engine_safe_20260401/benchmark_ab/comparison/` now contains:

- `variant_summary.csv`
- `pairwise_delta_summary.csv`
- `seedwise_delta.csv`
- `trace_seedwise.csv`
- `trace_summary.csv`
- `comparison_summary.md`
- `baseline_icbr_shared_check.csv`
- `baseline_icbr_primary_effect.csv`
- `baseline_icbr_mechanism_summary.csv`

## Notes

- `scripts.symkanbenchmark` now caches pre-symbolic numeric state under the benchmark root sibling `_numeric_cache/`, keyed by the non-symbolic config plus `stage_seed`, `batch_size`, and resolved device.
- It also caches the shared symbolic-prep boundary under `_symbolic_prep_cache/`, keyed by the numeric-cache identity plus prune/input-compaction/pre-symbolic-fit settings only.
- Cache-hit runs keep reference timings in `cached_stage_total_seconds_ref` and `cached_symbolic_prep_seconds_ref` so symbolization-only runtime metrics are not polluted by shared training/prep cost.
- On the regenerated `2026-04-01` benchmark slice, baseline and baseline_icbr now share identical pre-symbolic metrics and identical `Symbolize Trace Rhythm` for all requested seeds.
- Current conclusion phrasing should prefer the specialized compare tables over the generic markdown auto-conclusion, because the specialized tables encode the fairness boundary explicitly.

## Stage 7: FAST_LIB Backend Compare Follow-Up

- Goal: Re-run the backend-only compare under a wider symbolic library while still reusing the existing numeric/shared-prep cache boundary.
- Success criteria:
  - `configs/benchmark_ab/baseline_fastlib.yaml` and `configs/benchmark_ab/baseline_icbr_fastlib.yaml` keep non-`symbolize` sections identical to `baseline.yaml`.
  - FAST_LIB overrides are encoded inside `symbolize.lib`, so the rerun continues to hit the existing `_numeric_cache/` and `_symbolic_prep_cache/`.
  - `scripts.benchmark_ab_compare` emits the specialized `baseline_icbr_*` summaries for the new single baseline-backend vs icbr-backend pair.
  - `comparison_fastlib/baseline_icbr_shared_check.csv` reports `shared_symbolic_prep_aligned=True` for all requested seeds.
- Validation:
  - `C:\Users\chenpeng\miniconda3\envs\kan\python.exe -m pytest tests\test_app_config.py tests\test_benchmark_ab_compare.py`
  - `C:\Users\chenpeng\miniconda3\envs\kan\python.exe -m scripts.symkanbenchmark --tasks full --stagewise-seeds 42,52,62 --config configs/benchmark_ab/baseline_fastlib.yaml --output-dir outputs/rerun_v2_engine_safe_20260401/benchmark_ab/baseline_fastlib --quiet`
  - `C:\Users\chenpeng\miniconda3\envs\kan\python.exe -m scripts.symkanbenchmark --tasks full --stagewise-seeds 42,52,62 --config configs/benchmark_ab/baseline_icbr_fastlib.yaml --output-dir outputs/rerun_v2_engine_safe_20260401/benchmark_ab/baseline_icbr_fastlib --quiet`
  - `C:\Users\chenpeng\miniconda3\envs\kan\python.exe -m scripts.benchmark_ab_compare --root outputs/rerun_v2_engine_safe_20260401/benchmark_ab --baseline baseline_fastlib --variants baseline_icbr_fastlib --output outputs/rerun_v2_engine_safe_20260401/benchmark_ab/comparison_fastlib`
- Status: Complete

## Observed Evidence (FAST_LIB, 2026-04-01)

1. `comparison_fastlib/baseline_icbr_shared_check.csv` reports `shared_numeric_aligned=True`、`trace_aligned=True` 与 `shared_symbolic_prep_aligned=True` for seeds `42/52/62`.
2. Both `baseline_fastlib` and `baseline_icbr_fastlib` report `numeric_cache_hit=True` and `symbolic_prep_cache_hit=True` for all requested seeds.
3. `comparison_fastlib/baseline_icbr_primary_effect.csv` reports:
   - `symbolic_core_speedup_vs_baseline = 2.350452`
   - `final_teacher_imitation_mse_shift = 0.000062`
   - `final_target_mse_shift = -0.000023`
   - `final_target_r2_shift = 0.000258`
4. `comparison_fastlib/baseline_icbr_mechanism_summary.csv` shows replay rerank still dominates the remaining ICBR core time even after widening the candidate library, now at about `96.0892%` of core time.

## Stage 8: Full-Library ICBR Supplement

- Goal: Add a single-arm supplementary slice that shows ICBR can still keep the full symbolic library path runnable when the paired baseline full-library path is too slow to include in the rerun.
- Success criteria:
  - `baseline_fulllib` is explicitly treated as intentionally skipped for cost reasons rather than forgotten evidence.
  - `baseline_icbr_fulllib` is documented as supplementary single-arm evidence, not as paired backend-only compare proof.
  - The docs record both the single-arm quality gains vs `baseline_icbr_fastlib` and the remaining acceptable ICBR runtime profile.
- Validation:
  - `C:\Users\chenpeng\miniconda3\envs\kan\python.exe -m scripts.symkanbenchmark --tasks full --stagewise-seeds 42,52,62 --config configs/benchmark_ab/baseline_icbr_fulllib.yaml --output-dir outputs/rerun_v2_engine_safe_20260401/benchmark_ab/baseline_icbr_fulllib --quiet`
- Status: Complete

## Observed Evidence (Full-Library ICBR Supplement, 2026-04-01)

1. `baseline_fulllib` was intentionally not regenerated because the full-library baseline path is too slow for this rerun.
2. `baseline_icbr_fulllib/symkanbenchmark_runs.csv` reports:
   - `final_acc = 0.795433`
   - `macro_auc = 0.963225`
   - `final_target_r2 = 0.601003`
   - `symbolic_core_seconds = 35.218785`
3. Relative to `baseline_icbr_fastlib`, the full-library ICBR slice keeps the path runnable while improving single-arm quality:
   - `final_acc +0.002200`
   - `macro_auc +0.000592`
   - `final_target_r2 +0.004067`
   - `symbolic_core_seconds +3.227987`
