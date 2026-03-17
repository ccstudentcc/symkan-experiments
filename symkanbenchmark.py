"""
Compatibility entrypoint.

The canonical implementation lives in `scripts/symkanbenchmark.py`, but we keep this
shim so existing docs/commands like `python symkanbenchmark.py ...` keep working.
"""

from scripts.symkanbenchmark import main


if __name__ == "__main__":
    main()
