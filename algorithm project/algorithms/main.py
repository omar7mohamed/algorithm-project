"""Run the app from the algorithms package: ``python -m algorithms.main`` (from project root)."""

from __future__ import annotations

import sys
from pathlib import Path

# Support ``python algorithms/main.py`` so imports resolve to project root.
_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from gui.app import run_app


class Main:
    """Application entry: call ``run()`` to start the GUI."""

    def run(self) -> None:
        run_app()


if __name__ == "__main__":
    Main().run()
