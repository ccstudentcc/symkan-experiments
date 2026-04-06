# SymKAN Manuscript and Slide Companion Plan

## Goal

Add a manuscript-style companion doc with formal citations, add a companion Beamer slide source pack, and wire both into the repo's documentation system without re-scoping `docs/design.md`.

## Stage 1: Repo and Evidence Review

- Goal: Re-open the current design doc, report docs, governance docs, and recent repo context.
- Success criteria:
  - `README.md`, `ARCHITECTURE.md`, and the last 10 commits are reviewed.
  - `docs/design.md`, `docs/ablation_report.md`, `docs/layerwiseft_improved_report.md`, `docs/engineering_rerun_report_20260318.md`, and `docs/engineering_rerun_report_20260401.md` are reviewed.
  - governance entry points and task-tracking files are re-opened.
- Validation:
  - local file inspection only
- Status: Complete

## Stage 2: Parallel Sidecar Review

- Goal: Use bounded subagents to gather non-overlapping guidance for manuscript structure, presentation narrative, visualization planning, and doc-sync impact.
- Success criteria:
  - academic-writing guidance is collected
  - presentation-story guidance is collected
  - figure/table planning guidance is collected
  - doc-sync impact analysis is collected
- Validation:
  - read-only subagent reports
- Status: Complete

## Stage 3: Manuscript Draft

- Goal: Add `docs/symkan_manuscript.md` as a paper-style narrative that reorganizes current maintained evidence.
- Success criteria:
  - the new manuscript defines SymKAN as a post-training symbolization pipeline
  - the manuscript keeps evidence slices separate
  - the manuscript includes reusable paper/slide display planning without becoming a runbook
- Validation:
  - manual review of the new doc against repo evidence
- Status: Complete

## Stage 4: Manuscript Citation and Scientific-Writing Upgrade

- Goal: Rework the manuscript toward a stricter scientific-writing style and add verified external citations.
- Success criteria:
  - the manuscript drops the prior metadata-heavy opening and reads as continuous academic prose
  - external references are added for KAN background, symbolic regression context, post-hoc symbolic modeling, and reproducibility or benchmark methodology
  - results and discussion are separated more clearly
  - repo-internal evidence remains distinct from external references
- Validation:
  - manual review against the maintained evidence hierarchy
  - metadata spot-checks against live external sources
- Status: Complete

## Stage 5: Slide Source Pack

- Goal: Add `docs/slides/` as a Beamer companion deck aligned with the manuscript.
- Success criteria:
  - `docs/slides/` contains a Beamer main file, local bibliography, and minimal usage notes
  - slide claims match the manuscript's evidence boundaries
  - the deck is organized for a 10-15 minute research presentation rather than an operations walkthrough
- Validation:
  - manual review of slide structure and citations handling
  - optional lightweight tex sanity check if the environment allows it
- Status: Complete

## Stage 6: Doc-System Sync

- Goal: Register the new manuscript and slide layer in the repo's governance, navigation, project-map, contribution, and release-check surfaces.
- Planned files:
  1. `docs/documentation_governance.md`
  2. `docs/index.md`
  3. `docs/project_map.md`
  4. `README.md`
  5. `CONTRIBUTING.md`
  6. `docs/engineering_release_checklist.md`
  7. `AGENTS.md`
- Success criteria:
  - the new manuscript and `docs/slides/` are discoverable from stable entry points
  - `docs/design.md` keeps its existing role
  - project-map sync is explicitly enforced
- Validation:
  - manual diff review
- Status: Complete

## Stage 7: Verification and Closeout

- Goal: Run the smallest meaningful doc-consistency checks and finalize task tracking.
- Success criteria:
  - task-tracking files reflect the expanded task
  - doc diffs have no whitespace or patch-format issues
  - manuscript and slide links are discoverable through the synced entry points
- Validation:
  - `git diff --check`
  - targeted `rg` checks
  - `git status --short`
- Status: Complete
