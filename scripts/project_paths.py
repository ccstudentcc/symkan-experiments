from __future__ import annotations

from pathlib import Path


DEFAULT_BENCHMARK_RUNS_DIR = "outputs/benchmark_runs"
DEFAULT_BENCHMARK_AB_DIR = "outputs/benchmark_ab"
DEFAULT_BENCHMARK_ABLATION_DIR = "outputs/benchmark_ablation"

LEGACY_BENCHMARK_RUNS_DIR = "benchmark_runs"
LEGACY_BENCHMARK_AB_DIR = "benchmark_ab"
LEGACY_BENCHMARK_ABLATION_DIR = "benchmark_ablation"


def resolve_preferred_dir(raw: str, repo_root: Path, default_dir: str, legacy_dir: str) -> Path:
    candidate = Path(raw)
    if candidate.is_absolute():
        return candidate.resolve()

    if raw != default_dir:
        return (repo_root / candidate).resolve()

    preferred = (repo_root / default_dir).resolve()
    legacy = (repo_root / legacy_dir).resolve()
    if preferred.exists() or not legacy.exists():
        return preferred
    return legacy
