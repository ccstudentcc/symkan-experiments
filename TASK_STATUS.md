# Task Status

## Current Objective

Upgrade `docs/symkan_manuscript.md` into a citation-backed paper-style manuscript, add a companion Beamer deck under `docs/slides/`, and synchronize the doc system around both artifacts while keeping `docs/design.md` intact.

## Current Status

- `README.md`, `ARCHITECTURE.md`, the last 10 commits, and the key SymKAN design/report docs have been reviewed.
- The initial manuscript companion and its first-round doc-system sync have already been added.
- A second bounded subagent round has been completed for:
  - scientific-writing compliance review
  - citation-placement review
  - Beamer deck planning
- Those review-only subagents have been closed after their outputs were integrated.
- `docs/symkan_manuscript.md` has been rewritten toward a stricter scientific-writing style and now includes formal external references plus a references section.
- `docs/slides/` now contains the Beamer companion deck, local style/data files, a slide-level `references.bib`, and a README with root-level build commands.
- The Beamer deck now renders page-level external citations plus a closing references frame from `references.bib` via BibTeX.
- `README.md`, `docs/index.md`, `docs/project_map.md`, `docs/documentation_governance.md`, `docs/doc_sync_matrix.md`, `CONTRIBUTING.md`, `docs/engineering_release_checklist.md`, and `AGENTS.md` have been synchronized for the new slide layer and revised manuscript role.
- `.gitignore` now ignores LaTeX intermediates and the compiled deck PDF under `docs/slides/`, and `AGENTS.md` now records that only Beamer sources belong in git by default.
- `SPEC.md`, `IMPLEMENTATION_PLAN.md`, and `TASK_STATUS.md` have been refreshed to reflect the expanded manuscript-and-slides scope.
- Validation is complete:
  - `git diff --check` passed with no patch-format errors; only CRLF normalization warnings were emitted.
  - targeted `rg` checks confirmed the revised manuscript and `docs/slides/` are wired into the required entry points.
  - `pdflatex` was run twice against `docs/slides/symkan_manuscript_companion.tex`, producing a smoke-check PDF under `tmp/slides_compile_check/`.
  - `git status --short` shows a scoped doc-only worktree with the manuscript, slides, and synchronized governance/navigation files.

## Key Decisions

1. Keep `docs/design.md` as the design-boundary document and add a separate manuscript companion instead of rewriting the existing design doc again.
2. Keep the new manuscript inside the current governance structure rather than inventing a new document category.
3. Treat the new manuscript as a synthesis surface: it may reorganize maintained evidence, but it must not invent stronger claims than the underlying dated reports support.
4. Use numbered external citations for academic positioning, but keep repo-internal dated reports and compare artifacts as internal evidence rather than formal literature.
5. Move presentation planning out of the manuscript body and into the new `docs/slides/` layer so the manuscript stays closer to a paper-style narrative.
6. Extend `AGENTS.md` so future core-doc changes must also sync `docs/project_map.md`.

## Residual Risks

1. The Beamer deck now compiles, but the compile log still reports overfull box and overflow warnings, so a later typography pass may still be desirable.
2. Future result updates must continue propagating into both the manuscript and `docs/slides/`, otherwise the two layers can drift.
3. The working tree contains a coordinated doc-only change set that still requires explicit user direction for staging, commit, or push.

## Next Step

The expanded manuscript-and-slides task is complete. The next optional step is staging, committing, or doing a dedicated slide-layout polish pass based on the current TeX warnings.
