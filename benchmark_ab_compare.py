"""
Compatibility entrypoint.

The canonical implementation lives in `scripts/benchmark_ab_compare.py`, but we keep this
shim so existing docs/commands like `python benchmark_ab_compare.py ...` keep working.
"""

from scripts.benchmark_ab_compare import main


if __name__ == "__main__":
    main()
