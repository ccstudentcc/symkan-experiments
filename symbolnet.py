"""
Compatibility entrypoint.

The canonical implementation lives in `scripts/symbolnet.py`, but we keep this
shim so commands like `python symbolnet.py ...` keep working.
"""

from scripts.symbolnet import main


if __name__ == "__main__":
    main()

