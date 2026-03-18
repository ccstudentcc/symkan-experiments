from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize(
    ("module_name", "expected_text"),
    [
        ("scripts.symkanbenchmark", "--tasks"),
        ("scripts.ablation_runner", "--aggregate-only"),
        ("scripts.benchmark_ab_compare", "--baseline"),
        ("scripts.compare_layerwiseft_improved", "--new-variant"),
        ("scripts.analyze_layerwiseft", "--ablation-dir"),
    ],
)
def test_module_help_works_without_site_packages(module_name: str, expected_text: str) -> None:
    result = subprocess.run(
        [sys.executable, "-S", "-m", module_name, "--help"],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert expected_text in result.stdout
