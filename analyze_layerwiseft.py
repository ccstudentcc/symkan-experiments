"""
Compatibility entrypoint.

The canonical implementation lives in `scripts/analyze_layerwiseft.py`, but we keep this
shim so existing docs/commands like `python analyze_layerwiseft.py ...` keep working.
"""

from scripts.analyze_layerwiseft import main


if __name__ == "__main__":
    main()
