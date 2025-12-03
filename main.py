from __future__ import annotations

import sys
from pathlib import Path


def _bootstrap_src() -> None:
    """Ensure the src directory is importable when running the CLI directly."""
    root = Path(__file__).resolve().parent
    src = root / "src"
    if src.exists() and str(src) not in sys.path:
        sys.path.insert(0, str(src))


def main() -> int:
    _bootstrap_src()
    from testgap.cli import main as cli_main

    return cli_main()


if __name__ == "__main__":
    raise SystemExit(main())
