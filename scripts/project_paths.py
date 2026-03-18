from __future__ import annotations

import re
from pathlib import Path


DEFAULT_BENCHMARK_RUNS_DIR = "outputs/benchmark_runs"
DEFAULT_BENCHMARK_AB_DIR = "outputs/benchmark_ab"
DEFAULT_BENCHMARK_ABLATION_DIR = "outputs/benchmark_ablation"

LEGACY_BENCHMARK_RUNS_DIR = "benchmark_runs"
LEGACY_BENCHMARK_AB_DIR = "benchmark_ab"
LEGACY_BENCHMARK_ABLATION_DIR = "benchmark_ablation"
_SAFE_CHILD_NAME = re.compile(r"^[A-Za-z0-9_.-]+$")


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


def validate_child_name(raw: str, kind: str = "name") -> str:
    candidate = raw.strip()
    if not candidate or not _SAFE_CHILD_NAME.fullmatch(candidate):
        raise ValueError(f"invalid {kind}: {raw!r}")
    return candidate


def resolve_named_child(root: Path, raw: str, kind: str = "name") -> Path:
    root_resolved = root.resolve()
    child_name = validate_child_name(raw, kind=kind)
    child = (root_resolved / child_name).resolve()
    try:
        child.relative_to(root_resolved)
    except ValueError as exc:
        raise ValueError(f"{kind} escapes root: {raw!r}") from exc
    return child
