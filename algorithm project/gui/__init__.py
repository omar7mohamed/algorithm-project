"""Tkinter GUI for the sorting visualizer."""

from __future__ import annotations

__all__ = ["run_app"]


def __getattr__(name: str):
    if name == "run_app":
        from gui.app import run_app

        return run_app
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
