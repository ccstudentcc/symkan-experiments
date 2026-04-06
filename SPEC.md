# SymKAN Manuscript and Slide Companion Specification

## 1. Objective

Add a paper-oriented companion manuscript under `docs/` that preserves `docs/design.md`, upgrade it with formal citations, and add a companion Beamer slide source pack under `docs/slides/`.

## 2. Audience

The primary readers are:

1. Authors who need a manuscript-style summary for papers, theses, or defense writing.
2. Maintainers who must keep the new manuscript aligned with the repo's design, report, and governance layers.
3. Readers who need a reusable slide deck for research talks or thesis-defense sections without weakening evidence boundaries.
4. Agentic tooling that needs an explicit role split between design docs, runbooks, dated reports, manuscript-style synthesis, and slide sources.

## 3. In Scope

1. Add a new core doc, `docs/symkan_manuscript.md`, as a paper-style main narrative.
2. Keep `docs/design.md` in place and preserve its role as the design-boundary document.
3. Add formal external citations to the manuscript and keep repo-internal dated reports as internal evidence rather than pretending they are external references.
4. Add `docs/slides/` with Beamer sources that align with the manuscript's claim boundaries.
5. Sync the new manuscript and slide layer into the doc-governance and navigation chain:
   - `docs/documentation_governance.md`
   - `docs/index.md`
   - `docs/project_map.md`
   - `README.md`
   - `CONTRIBUTING.md`
   - `docs/engineering_release_checklist.md`
   - `AGENTS.md`
6. Refresh task-tracking files so they describe the expanded manuscript-and-slides task rather than the earlier governance-only task.

## 4. Out of Scope

1. No benchmark reruns.
2. No code-path behavior changes.
3. No weakening of the current backend-compare evidence boundaries.
4. No conversion of `docs/design.md` into a runbook or dated report.
5. No invention of new experimental claims beyond maintained docs and existing outputs.
6. No fabricated references or unverified bibliographic metadata.

## 5. Required Writing Properties

1. The new manuscript must read as a restrained, paper-style narrative rather than a tutorial.
2. It must define SymKAN as an engineering pipeline for post-training KAN symbolization, not as a new numeric trainer or generic symbolic regression system.
3. The manuscript should follow a scientific-writing style more closely: continuous prose, explicit section roles, and a clear separation between results and interpretation.
4. Results and discussion must respect the maintained evidence hierarchy:
   - `2026-03-18` overall rerun for engineering baseline and strategy tradeoffs
   - ablation and LayerwiseFT reports for module roles
   - `2026-04-01` layered/FAST_LIB paired compare for backend-only evidence
   - `baseline_icbr_fulllib` only as supplementary single-arm evidence
5. External references should support KAN background, symbolic regression context, post-hoc symbolic modeling, and reproducibility or benchmark methodology, while repo-internal reports remain separate evidence anchors.
6. The Beamer deck should function as a talk-ready compression of the manuscript rather than a runbook or result dump.

## 6. Acceptance Criteria

1. `docs/symkan_manuscript.md` exists, presents a paper-style main narrative distinct from `docs/design.md`, and contains verified external references plus a references section.
2. `docs/slides/` exists and contains a Beamer-based companion deck aligned with the manuscript's evidence hierarchy.
3. The synced doc-system entry points expose the manuscript and slide layer without blurring document roles.
4. `AGENTS.md` reflects any newly discovered core-doc routing rule needed to prevent future misses.
5. `SPEC.md`, `IMPLEMENTATION_PLAN.md`, and `TASK_STATUS.md` all reflect the expanded manuscript-and-slides task.
6. Basic doc-consistency checks pass after the edits.
