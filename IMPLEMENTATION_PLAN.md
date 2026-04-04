# Documentation Governance Reinforcement Plan

## Goal

Add a governance layer for the documentation system and propagate it through the repository's navigation, sync, contribution, release, and agent-facing entry points.

## Stage 1: Baseline Review

- Goal: Re-open the current repo-level documentation system and identify where governance is already partially encoded.
- Success criteria:
  - `README.md`, `ARCHITECTURE.md`, and the last 10 commits are reviewed.
  - `docs/index.md`, `docs/project_map.md`, `docs/doc_sync_matrix.md`, `docs/engineering_release_checklist.md`, `CONTRIBUTING.md`, and `AGENTS.md` are reviewed.
  - the current task-tracking files are re-opened and confirmed to be stale for this task.
- Validation:
  - local file inspection only
- Status: Complete

## Stage 2: Parallel Audit

- Goal: Use bounded subagents to audit topology gaps and style/maintenance weaknesses without overlapping writes.
- Success criteria:
  - one audit covers document layers, routing, and missing governance hooks.
  - one audit covers tone, structure, and maintenance-flow weaknesses.
  - both audits return concrete parent-edit targets.
- Validation:
  - subagent read-only reports
- Status: Complete

## Stage 3: Governance Layer Draft

- Goal: Add or update the files that define the documentation governance contract.
- Planned files:
  1. `docs/documentation_governance.md`
  2. `README.md`
  3. `docs/index.md`
  4. `docs/project_map.md`
  5. `docs/doc_sync_matrix.md`
  6. `docs/engineering_release_checklist.md`
  7. `docs/engineering_rerun_report.md`
  8. `docs/engineering_version_rerun_note.md`
  9. `CONTRIBUTING.md`
  10. `ARCHITECTURE.md`
- Success criteria:
  - the new governance doc defines roles, flow, writing boundaries, prohibited patterns, and validation.
  - each synced entry point points to the governance layer where appropriate.
- Validation:
  - manual review of edited files
- Status: Complete

## Stage 4: Task Tracking Refresh

- Goal: Rewrite `SPEC.md`, `IMPLEMENTATION_PLAN.md`, and `TASK_STATUS.md` so they describe the current governance task.
- Success criteria:
  - the previous design-manuscript task is no longer shown as the current objective.
  - current scope, risks, and acceptance criteria are recorded.
- Validation:
  - manual review of the three task-tracking files
- Status: Complete

## Stage 5: Verification and Cleanup

- Goal: Run the smallest meaningful checks for a doc-governance-only change set and integrate the audit feedback.
- Success criteria:
  - edited files have no diff-format or whitespace issues.
  - navigation, command-style, and core link expectations are checked.
  - task tracking is updated to final status.
- Validation:
  - `git diff --check`
  - targeted `rg` checks
- Status: Complete
