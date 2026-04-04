# SymKAN Design Manuscript Rewrite Specification

## 1. Objective

Rewrite `docs/design.md` into a paper-style SymKAN design manuscript grounded in the current `symkan-experiments` repository state. The rewritten document should explain the pipeline as a rigorous engineering method for symbolic KAN experimentation rather than as a command guide or a changelog.

## 2. Audience

The primary readers are:

1. Thesis or paper readers who need a coherent method narrative.
2. Maintainers who need the design rationale behind current defaults and compare semantics.
3. Reviewers who need to understand which claims are supported by ablation evidence and which claims are supported by backend-only compare evidence.

## 3. In Scope

1. Reframe SymKAN as a pipeline with clear objects, stages, interfaces, and evidence boundaries.
2. Preserve the repository's actual boundaries:
   - `pykan` training semantics are not rewritten.
   - `baseline` remains the default symbolic backend.
   - `icbr` remains an opt-in backend-only symbolic completion path.
3. Ground module-role claims in:
   - `docs/ablation_report.md`
   - `docs/layerwiseft_improved_report.md`
4. Ground backend-compare claims in:
   - `docs/engineering_rerun_report_20260401.md`
   - `outputs/rerun_v2_engine_safe_20260401/benchmark_ab/comparison/`
   - `outputs/rerun_v2_engine_safe_20260401/benchmark_ab/comparison_fastlib/`
5. State explicit evidence boundaries for:
   - layered paired compare
   - FAST_LIB paired compare
   - `baseline_icbr_fulllib` supplementary single-arm slice

## 4. Out of Scope

1. No code-path behavior changes.
2. No benchmark reruns.
3. No new experiment results.
4. No claims of statistical significance beyond the existing `n=3` engineering evidence.
5. No conversion of the design document into a runbook, tutorial, or release note.

## 5. Required Writing Properties

1. Tone must be rigorous, restrained, and thesis-friendly.
2. The document must avoid AI-assistant phrasing, motivational filler, and conversational guidance.
3. The structure should follow a paper-like flow:
   - abstract
   - premises
   - constraints
   - baseline semantics
   - method redefinition
   - formalization
   - design decisions
   - experiment design
   - results
   - risks
   - conclusion
4. Each major section must answer a distinct design question instead of repeating usage guidance already covered elsewhere.

## 6. Claim Boundaries

1. Module-role conclusions must come from the ablation reports, not from the backend compare.
2. Backend-only fairness claims require:
   - `shared_numeric_aligned=True`
   - `trace_aligned=True`
   - `shared_symbolic_prep_aligned=True`
3. `baseline_icbr_fulllib` must be described as supplementary single-arm evidence only.
4. `formula_export_success_rate=1.0` must not be described as proof of true closed-form recovery.
5. Speed conclusions should prioritize `symbolic_core_seconds` over `symbolize_wall_time_s` when discussing backend effects.

## 7. Acceptance Criteria

1. `docs/design.md` reads as a coherent paper-style manuscript rather than a design memo.
2. The new structure is visibly closer to `ICBR-KAN_design.md` in argument flow, while staying specific to `symkan-experiments`.
3. The document clearly separates:
   - pipeline design rationale
   - experiment evidence
   - result interpretation boundaries
4. Relative links referenced in the rewritten document resolve within the repository.
5. Task-tracking files are updated to reflect this rewrite task.
