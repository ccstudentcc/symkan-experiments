"""
Compatibility entrypoint.

The canonical implementation lives in `scripts/ablation_runner.py`, but we keep this
shim so existing docs/commands like `python ablation_runner.py ...` keep working.
"""

from scripts.ablation_runner import main


if __name__ == "__main__":
    main()
