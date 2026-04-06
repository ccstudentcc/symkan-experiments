# SymKAN Beamer Companion Deck

This directory contains a Beamer source pack that mirrors the claim boundary of
`docs/symkan_manuscript.md`.

## Files

- `symkan_manuscript_companion.tex`: main Beamer deck
- `symkan_slide_style.tex`: local theme, colors, and helper macros
- `symkan_slide_data.tex`: inline tables for charts and reported values
- `references.bib`: manuscript-aligned external bibliography for future slide-level citation reuse

## Scope Contract

- The deck is a companion to the manuscript, not an independent evidence source.
- All quantitative values are copied from `docs/symkan_manuscript.md`.
- The deck does not introduce new experimental claims, new output parsing, or
  new fairness statements beyond the manuscript.
- `baseline_icbr_fulllib` is kept as supplementary one-sided evidence only.

## Build

Preferred:

```powershell
# 运行目录：仓库根目录（symkan-experiments/）
Push-Location docs/slides
latexmk -pdf symkan_manuscript_companion.tex
Pop-Location
```

Fallback:

```powershell
# 运行目录：仓库根目录（symkan-experiments/）
Push-Location docs/slides
pdflatex symkan_manuscript_companion.tex
bibtex symkan_manuscript_companion
pdflatex symkan_manuscript_companion.tex
pdflatex symkan_manuscript_companion.tex
Pop-Location
```

The deck uses BibTeX via `natbib` so page-level citations and the closing
references frame are rendered directly from `references.bib`. `latexmk` is the
preferred path because it resolves the bibliography pass automatically.

## Editing Notes

- Update chart values in `symkan_slide_data.tex`.
- Update narrative framing in `symkan_manuscript_companion.tex`.
- Keep `references.bib` aligned with the manuscript references section.
- Use slide-level `\citep{...}` calls when external context is introduced; do
  not leave `references.bib` disconnected from the deck source.
- Keep the wording conservative: backend-only claims require shared-state
  alignment and must stay tied to the dated source family already named in the
  manuscript.
