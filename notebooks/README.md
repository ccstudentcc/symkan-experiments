# Notebooks

This directory contains interactive research notebooks.

- `kan.ipynb`: the main exploratory and paper-oriented SymKAN experiment notebook.

The notebook resolves the repository root for imports and data loading.

- Runtime model artifacts are still created inside `notebooks/model/`.
- Structured CSV outputs are written to `outputs/notebooks/`.
- Flat notebook kwargs are normalized by `symkan.config.notebook` into the canonical `AppConfig` shape before entering the current runtime.
- `symkan.notebook_compat` remains a thin execution bridge for notebook-style calls.
- Canonical `symkan` parameter names are the preferred public interface; legacy aliases are retained only as compatibility fallback.

Current rerun status:

- `kan.ipynb` was rerun on `2026-03-19`.
- The latest structured outputs include:
  - `outputs/notebooks/kan_symbolic_summary.csv`
  - `outputs/notebooks/benchmark_multi_round_raw.csv`
  - `outputs/notebooks/benchmark_multi_round_summary_cn.csv`
  - `outputs/notebooks/benchmark_multi_round_summary_en.csv`
  - `outputs/notebooks/benchmark_symbolic_parallel_quick.csv`

For notebook-oriented demos, prefer direct function calls and `symkan.config.AppConfig` over YAML files.
YAML remains the recommended path for repeatable CLI and CI-style runs.
