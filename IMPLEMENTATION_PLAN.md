# SymKAN Design Manuscript Rewrite Plan

## Goal

Turn `docs/design.md` into a paper-style SymKAN design manuscript that is consistent with the current repository, current engineering evidence, and current documentation role split.

## Stage 1: Repository and Reference Baseline

- Goal: Re-open the current repo documents, recent commits, and the reference paper-style structure.
- Success criteria:
  - `README.md` and `ARCHITECTURE.md` are reviewed.
  - current `docs/design.md` weaknesses are identified.
  - `ICBR-KAN_design.md` structure is mapped for reuse, not copying.
- Validation:
  - local file inspection only
- Status: Complete

## Stage 2: Evidence and Claim Boundary Mapping

- Goal: Identify which current results can support which parts of the rewritten manuscript.
- Success criteria:
  - ablation evidence is mapped to module-role claims.
  - 2026-04-01 engineering rerun evidence is mapped to backend-only compare claims.
  - supplementary evidence is explicitly separated from paired evidence.
- Validation:
  - local file inspection only
- Status: Complete

## Stage 3: Task Tracking Refresh

- Goal: Update `SPEC.md`, `IMPLEMENTATION_PLAN.md`, and `TASK_STATUS.md` for this rewrite task before editing the main document.
- Success criteria:
  - current objective is the paper-style rewrite of `docs/design.md`.
  - acceptance boundaries and prohibited claim patterns are recorded.
- Validation:
  - manual review of the three task-tracking files
- Status: Complete

## Stage 4: Manuscript Rewrite

- Goal: Replace the existing design-note structure with a paper-style argument flow.
- Planned sections:
  1. Abstract
  2. Design Premises
  3. Constraints from KAN and the current implementation
  4. Baseline workflow semantics
  5. SymKAN redefinition
  6. Formalization
  7. Key design decisions
  8. Pipeline pseudocode
  9. Interface and workflow relation
  10. Experiment design and evidence boundaries
  11. Results and discussion
  12. Risks and conclusion
- Success criteria:
  - the doc uses restrained, academic wording.
  - the doc cites only repository-backed evidence.
  - the doc no longer reads like a runbook or tutorial.
- Validation:
  - manual read-through
- Status: Complete

## Stage 5: Verification and Cleanup

- Goal: Run the smallest meaningful verification for a doc-only rewrite and check for obvious integrity issues.
- Success criteria:
  - relative links and referenced file paths in `docs/design.md` resolve.
  - no malformed diff hunks or whitespace errors remain.
  - task tracking reflects the completed rewrite.
- Validation:
  - `git diff --check`
  - local path/link sanity check
- Status: Complete
