# Documentation Governance Reinforcement Specification

## 1. Objective

Add a durable documentation-governance layer for `symkan-experiments` so that entry docs, execution docs, evidence docs, and release docs stay synchronized through explicit role boundaries and maintenance rules.

## 2. Audience

The primary readers are:

1. Maintainers who need a stable process for keeping docs synchronized with code and experiment outputs.
2. Contributors who need to know which document to update for which kind of change.
3. Agentic tooling that must route documentation edits without re-discovering the repo-wide conventions each time.

## 3. In Scope

1. Add a dedicated governance document for documentation roles, maintenance flow, writing boundaries, and validation requirements.
2. Sync the governance layer into the main navigation and contribution entry points:
   - `README.md`
   - `docs/index.md`
   - `docs/project_map.md`
   - `docs/doc_sync_matrix.md`
   - `docs/engineering_release_checklist.md`
   - `docs/engineering_rerun_report.md`
   - `docs/engineering_version_rerun_note.md`
   - `CONTRIBUTING.md`
   - `ARCHITECTURE.md`
3. Refresh task-tracking files so they match the current governance task instead of the previous design-manuscript task.

## 4. Out of Scope

1. No code-path behavior changes.
2. No benchmark reruns or result rewrites.
3. No large-scale rewriting of unrelated method or report documents.
4. No weakening of the existing backend-compare evidence boundaries.

## 5. Required Writing Properties

1. Tone must remain rigorous, restrained, and operational.
2. The governance layer must be layered:
   - role definition
   - maintenance flow
   - update triggers
   - prohibited patterns
   - validation checklist
3. The new wording must avoid AI-assistant phrasing, tutorial chatter, and second-person filler unless an execution step genuinely requires imperative wording.

## 6. Acceptance Criteria

1. A dedicated governance document exists and matches the current repository doc system.
2. `README.md` and `docs/index.md` both expose the governance entry.
3. `docs/doc_sync_matrix.md`, `docs/engineering_release_checklist.md`, `CONTRIBUTING.md`, and `AGENTS.md` all reference the same governance contract without conflicting rules.
4. Task-tracking files reflect this governance task.
5. Basic doc-consistency checks pass after the edits.
