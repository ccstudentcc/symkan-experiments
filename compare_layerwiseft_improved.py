"""
Compatibility entrypoint.

The canonical implementation lives in `scripts/compare_layerwiseft_improved.py`, but we keep this
shim so existing docs/commands like `python compare_layerwiseft_improved.py ...` keep working.
"""

from scripts.compare_layerwiseft_improved import main


if __name__ == "__main__":
    main()
