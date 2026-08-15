"""Render sort states as a matplotlib bar chart with color coding."""

from __future__ import annotations

from typing import Iterable, List, Optional, Tuple

from matplotlib.axes import Axes
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from algorithms.base import SortState


class SortChart:
    """
    Embedded matplotlib chart for sorting visualization.

    Colors:
        default: primary bar color
        compare: indices being compared
        swap: indices involved in a swap
        pivot: quicksort pivot
        sorted: indices in final position
    """

    def __init__(
        self,
        parent,
        *,
        dark: bool = False,
        figsize: Tuple[float, float] = (8.0, 4.2),
        dpi: int = 100,
    ) -> None:
        self._dark = dark
        self.figure = Figure(figsize=figsize, dpi=dpi, tight_layout=True)
        self.axes: Axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=parent)
        self._bars = None
        self._apply_theme()
        self.axes.set_xticks([])
        self.axes.set_ylabel("Value")

    @property
    def widget(self):
        return self.canvas.get_tk_widget()

    def set_dark(self, dark: bool) -> None:
        self._dark = dark
        self._apply_theme()
        self.canvas.draw_idle()

    def _apply_theme(self) -> None:
        if self._dark:
            self.figure.patch.set_facecolor("#1e1e1e")
            self.axes.set_facecolor("#252526")
            self.axes.tick_params(colors="#cccccc")
            self.axes.yaxis.label.set_color("#cccccc")
            self.axes.spines["bottom"].set_color("#555555")
            self.axes.spines["top"].set_color("#555555")
            self.axes.spines["left"].set_color("#555555")
            self.axes.spines["right"].set_color("#555555")
        else:
            self.figure.patch.set_facecolor("#f5f5f5")
            self.axes.set_facecolor("#ffffff")
            self.axes.tick_params(colors="#333333")
            self.axes.yaxis.label.set_color("#333333")
            for spine in self.axes.spines.values():
                spine.set_color("#cccccc")

    def _palette(self) -> dict:
        if self._dark:
            return {
                "default": "#4fc3f7",
                "compare": "#ffb74d",
                "swap": "#ef5350",
                "pivot": "#ba68c8",
                "sorted": "#66bb6a",
            }
        return {
            "default": "#1976d2",
            "compare": "#f57c00",
            "swap": "#d32f2f",
            "pivot": "#7b1fa2",
            "sorted": "#388e3c",
        }

    def setup(self, values: List[float]) -> None:
        """Initialize or reset bars for a new array."""
        self.axes.clear()
        self.axes.set_xticks([])
        self.axes.set_ylabel("Value")
        self._apply_theme()

        n = len(values)
        x = list(range(n))
        palette = self._palette()
        self._bars = self.axes.bar(
            x,
            values,
            color=[palette["default"]] * n,
            edgecolor="#888888" if not self._dark else "#666666",
            linewidth=0.5,
        )
        self.axes.set_xlim(-0.5, max(n - 0.5, 0.5))
        ymax = max(values) if values else 1.0
        ymin = min(values) if values else 0.0
        pad = 0.05 * (ymax - ymin if ymax != ymin else 1.0)
        self.axes.set_ylim(ymin - pad, ymax + pad)
        self.canvas.draw_idle()

    def update_state(self, state: SortState) -> None:
        """Update bar heights and colors from a sort state."""
        if self._bars is None:
            self.setup(state.values)
            return

        values = state.values
        palette = self._palette()
        colors: List[str] = [palette["default"]] * len(values)

        for idx in state.sorted_indices:
            if 0 <= idx < len(colors):
                colors[idx] = palette["sorted"]

        if state.pivot is not None and 0 <= state.pivot < len(colors):
            colors[state.pivot] = palette["pivot"]

        if state.compare:
            a, b = state.compare
            for idx in (a, b):
                if 0 <= idx < len(colors):
                    colors[idx] = palette["compare"]

        if state.swap:
            a, b = state.swap
            for idx in (a, b):
                if 0 <= idx < len(colors):
                    colors[idx] = palette["swap"]

        for bar, height, color in zip(self._bars, values, colors):
            bar.set_height(height)
            bar.set_color(color)

        ymax = max(values) if values else 1.0
        ymin = min(values) if values else 0.0
        pad = 0.05 * (ymax - ymin if ymax != ymin else 1.0)
        self.axes.set_ylim(ymin - pad, ymax + pad)
        self.canvas.draw_idle()

    def reset_colors(self, values: Iterable[float]) -> None:
        """Redraw a neutral state (e.g., after reset)."""
        vals = list(values)
        state = SortState(values=vals)
        self.setup(vals)
        self.update_state(state)
