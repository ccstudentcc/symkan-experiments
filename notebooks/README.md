# Notebooks

This directory contains interactive research notebooks.

- `kan.ipynb`: the main exploratory and paper-oriented SymKAN experiment notebook.

The notebook resolves the repository root for imports and data loading.

- Runtime model artifacts are still created inside `notebooks/model/`.
- Structured CSV outputs are written to `outputs/notebooks/`.

For notebook-oriented demos, prefer direct function calls and `symkan.config.AppConfig` over YAML files.
YAML remains the recommended path for repeatable CLI and CI-style runs.
