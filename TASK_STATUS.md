# Task Status

## Current Objective

Reinforce the documentation governance layer so that the repository's entry docs, sync rules, contribution workflow, release checklist, and agent routing all point to the same document-system contract.

## Current Status

- `README.md`, `ARCHITECTURE.md`, and the last 10 commits have been reviewed.
- `docs/index.md`, `docs/project_map.md`, `docs/doc_sync_matrix.md`, `docs/engineering_release_checklist.md`, `docs/engineering_rerun_report.md`, `CONTRIBUTING.md`, and `AGENTS.md` have been reviewed as the current governance surface.
- Existing task-tracking files were confirmed to be stale because they still described the earlier `docs/design.md` manuscript rewrite.
- Two bounded read-only subagents have been dispatched:
  - one for documentation topology and routing gaps
  - one for tone, structure, and maintenance-flow weaknesses
- The subagent findings have been integrated into the final edits:
  - duplicated navigation in `README.md` has been compressed into stable entry points
  - `docs/project_map.md` now routes to conclusions instead of restating them
  - governance and task-tracking entry points are exposed in `docs/index.md`, `README.md`, and `ARCHITECTURE.md`
- `docs/documentation_governance.md` has been added as the governance-layer contract.
- `README.md`, `docs/index.md`, `docs/project_map.md`, `docs/doc_sync_matrix.md`, `docs/engineering_release_checklist.md`, `CONTRIBUTING.md`, and `AGENTS.md` have been updated to expose or enforce the new governance layer.
- `ARCHITECTURE.md`, `docs/engineering_rerun_report.md`, and `docs/engineering_version_rerun_note.md` have been tightened so routing, stable-link rules, and report-writing language match the governance layer.
- `SPEC.md`, `IMPLEMENTATION_PLAN.md`, and `TASK_STATUS.md` have been rewritten for this governance task.
- Validation is complete:
  - `git diff --check` passed
  - fixed-string scans found no `````bash``, `````sh``, or `````shell`` code blocks in `README.md`, `docs/`, `CONTRIBUTING.md`, or `ARCHITECTURE.md`
  - no direct `python scripts.*` / `python symkanbenchmark.py` / `python ablation_runner.py` command-form regressions were found in `README.md` or `docs/`
  - governance and task-tracking cross-links were confirmed with targeted `rg` checks

## Key Decisions

1. Use a dedicated governance document instead of embedding more rules into `docs/index.md` or `doc_sync_matrix.md` alone.
2. Keep the role split explicit:
   - entry docs define where to look
   - method docs define design and usage semantics
   - report docs define dated evidence
   - governance docs define maintenance rules
3. Preserve the stable-index vs dated-body pattern for engineering rerun reports.
4. Keep `doc_sync_matrix.md` as the impacted-file SSOT, while `documentation_governance.md` defines the higher-level document-system contract.
5. Mirror governance rules into `AGENTS.md` only where they help future routing and prevent repeated discovery work.

## Residual Risks

1. Some older topic documents may still contain tutorial-like phrasing that this pass does not rewrite.
2. Future contributors may update topic documents without revisiting the governance layer unless the new entry points are used consistently.
3. The working tree now contains a doc-only governance change set that still requires explicit user direction for staging, commit, or push.

## Next Step

The governance-layer reinforcement task is complete. The next optional step is a scoped commit if this doc-only change set should be recorded now.
