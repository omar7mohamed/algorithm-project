"""Main Tkinter application for the sorting visualizer."""

from __future__ import annotations

import random
import tkinter as tk
from copy import copy
from tkinter import messagebox, ttk
from typing import List

from algorithms import BubbleSort, MergeSort, QuickSort
from algorithms.base import SortState, SortingAlgorithm
from gui.animator import AnimationController, measure_sort
from utils.stats import AlgorithmResult, SortStats, complexity_table
from utils.validation import ValidationError, parse_number_list


class SortingVisualizerApp:
    """Root window wiring controls, chart, and animation."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        root.title("Sorting Algorithms Visualizer and Comparator")
        root.minsize(960, 640)

        self._data: List[float] = []
        self._dark = tk.BooleanVar(value=False)
        self._speed = tk.IntVar(value=40)
        self._anim = AnimationController(root)
        self._algorithms = {
            "bubble": BubbleSort(),
            "merge": MergeSort(),
            "quick": QuickSort(),
        }
        self._complexity = complexity_table()

        self._build_ui()
        self._apply_theme()
        self._generate_random(silent=True)

    # ------------------------------------------------------------------ UI
    def _build_ui(self) -> None:
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        top = ttk.Frame(self.root, padding=8)
        top.grid(row=0, column=0, sticky="ew")
        top.columnconfigure(1, weight=1)

        ttk.Label(top, text="Numbers (comma or space separated):").grid(
            row=0, column=0, sticky="w"
        )
        self.input_var = tk.StringVar()
        self.entry = ttk.Entry(top, textvariable=self.input_var, width=60)
        self.entry.grid(row=0, column=1, sticky="ew", padx=(6, 6))

        ttk.Button(top, text="Random", command=self._on_random).grid(
            row=0, column=2, padx=(0, 4)
        )
        ttk.Button(top, text="Load", command=self._on_load).grid(row=0, column=3)

        ctrl = ttk.Frame(self.root, padding=(8, 0))
        ctrl.grid(row=1, column=0, sticky="nsew")
        ctrl.columnconfigure(0, weight=3)
        ctrl.columnconfigure(1, weight=1)

        left = ttk.Frame(ctrl)
        left.grid(row=0, column=0, sticky="nsew")
        left.rowconfigure(1, weight=1)
        left.columnconfigure(0, weight=1)

        btn_row = ttk.Frame(left)
        btn_row.grid(row=0, column=0, sticky="ew", pady=(0, 6))
        for i, (key, label) in enumerate(
            [
                ("bubble", "Bubble Sort"),
                ("merge", "Merge Sort"),
                ("quick", "Quick Sort"),
            ]
        ):
            ttk.Button(
                btn_row,
                text=label,
                command=lambda k=key: self._run_single(k),
            ).grid(row=0, column=i, padx=4, sticky="ew")
            btn_row.columnconfigure(i, weight=1)

        ttk.Button(btn_row, text="Run All", command=self._run_all).grid(
            row=0, column=3, padx=(12, 4), sticky="ew"
        )
        btn_row.columnconfigure(3, weight=1)

        chart_frame = ttk.Frame(left, padding=(0, 0, 0, 4))
        chart_frame.grid(row=1, column=0, sticky="nsew")
        chart_frame.rowconfigure(0, weight=1)
        chart_frame.columnconfigure(0, weight=1)

        # Import chart only after the Tk root exists (see run_app). Loading
        # FigureCanvasTkAgg before tk.Tk() can break or headless-exit on Windows.
        from visualization.chart import SortChart

        self.chart = SortChart(chart_frame, dark=self._dark.get())
        self.chart.widget.grid(row=0, column=0, sticky="nsew")

        speed_row = ttk.Frame(left)
        speed_row.grid(row=2, column=0, sticky="ew", pady=(4, 0))
        ttk.Label(speed_row, text="Animation delay (ms):").pack(side=tk.LEFT)
        self.speed_scale = ttk.Scale(
            speed_row,
            from_=0,
            to=400,
            variable=self._speed,
            orient=tk.HORIZONTAL,
            command=self._on_speed_change,
        )
        self.speed_scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=8)
        self.speed_label = ttk.Label(speed_row, text="")
        self.speed_label.pack(side=tk.LEFT)
        self._refresh_speed_label()

        bottom = ttk.Frame(left)
        bottom.grid(row=3, column=0, sticky="ew", pady=(8, 0))
        ttk.Button(bottom, text="Pause", command=self._on_pause).pack(
            side=tk.LEFT, padx=(0, 4)
        )
        ttk.Button(bottom, text="Resume", command=self._on_resume).pack(
            side=tk.LEFT, padx=(0, 4)
        )
        ttk.Button(bottom, text="Reset", command=self._on_reset).pack(
            side=tk.LEFT, padx=(0, 4)
        )
        self.dark_check = ttk.Checkbutton(
            bottom,
            text="Dark mode",
            variable=self._dark,
            command=self._on_toggle_dark,
        )
        self.dark_check.pack(side=tk.RIGHT)

        right = ttk.LabelFrame(ctrl, text="Results", padding=8)
        right.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
        right.rowconfigure(0, weight=1)
        right.columnconfigure(0, weight=1)

        self.results_text = tk.Text(
            right,
            width=36,
            height=24,
            wrap="word",
            state=tk.DISABLED,
            font=("Consolas", 10),
        )
        self.results_text.grid(row=0, column=0, sticky="nsew")
        scroll = ttk.Scrollbar(
            right, orient=tk.VERTICAL, command=self.results_text.yview
        )
        scroll.grid(row=0, column=1, sticky="ns")
        self.results_text.configure(yscrollcommand=scroll.set)

        self._set_results_text(
            "Welcome.\n\n"
            "Enter numbers or click Random, then choose an algorithm.\n"
            "Run All compares time and comparisons on the same data.\n"
        )

    def _refresh_speed_label(self) -> None:
        self.speed_label.configure(text=f"{int(self._speed.get())} ms")

    def _on_speed_change(self, _value: str) -> None:
        delay = int(float(_value))
        self._anim.set_delay_ms(delay)
        self._refresh_speed_label()

    def _apply_theme(self) -> None:
        style = ttk.Style()
        if self._dark.get():
            style.theme_use("clam")
            bg = "#1e1e1e"
            fg = "#e0e0e0"
            self.root.configure(background=bg)
            style.configure(".", background=bg, foreground=fg)
            style.configure("TFrame", background=bg)
            style.configure("TLabel", background=bg, foreground=fg)
            style.configure("TLabelframe", background=bg, foreground=fg)
            style.configure("TLabelframe.Label", background=bg, foreground=fg)
            style.configure("TButton", padding=6)
            style.configure("TScale", background=bg)
            self.results_text.configure(
                background="#252526",
                foreground="#d4d4d4",
                insertbackground="#d4d4d4",
                highlightthickness=0,
            )
        else:
            try:
                style.theme_use("vista")
            except tk.TclError:
                style.theme_use("default")
            self.root.configure(background="#f0f0f0")
            style.configure("TFrame", background="#f0f0f0")
            style.configure("TLabel", background="#f0f0f0")
            style.configure("TLabelframe", background="#f0f0f0")
            style.configure("TLabelframe.Label", background="#f0f0f0")
            self.results_text.configure(
                background="#ffffff",
                foreground="#222222",
                insertbackground="#222222",
                highlightthickness=0,
            )
        self.chart.set_dark(self._dark.get())

    def _on_toggle_dark(self) -> None:
        self._apply_theme()

    # ----------------------------------------------------------- data input
    def _generate_random(self, *, silent: bool = False) -> None:
        count = random.randint(18, 28)
        self._data = [random.randint(8, 99) for _ in range(count)]
        self.input_var.set(", ".join(str(int(x)) for x in self._data))
        self.chart.reset_colors(self._data)
        if not silent:
            self._set_results_text("Generated a new random array.\n")

    def _on_random(self) -> None:
        self._anim.cancel()
        self._generate_random(silent=False)

    def _on_load(self) -> None:
        self._anim.cancel()
        try:
            self._data = parse_number_list(self.input_var.get())
        except ValidationError as exc:
            messagebox.showerror("Invalid input", str(exc))
            return
        if len(self._data) > 120:
            messagebox.showwarning(
                "Large input",
                "Visualization may be slow for more than ~120 elements. "
                "Consider a smaller set.",
            )
        self.chart.reset_colors(self._data)
        self._set_results_text(f"Loaded {len(self._data)} values.\n")

    def _ensure_data(self) -> bool:
        if not self._data:
            messagebox.showinfo("No data", "Load numbers first.")
            return False
        return True

    # -------------------------------------------------------------- animation
    def _on_pause(self) -> None:
        self._anim.pause()

    def _on_resume(self) -> None:
        self._anim.resume()

    def _on_reset(self) -> None:
        self._anim.cancel()
        if self._data:
            self.chart.reset_colors(self._data)
        self._set_results_text("Animation reset. Data unchanged.\n")

    def _algorithm_for(self, key: str) -> SortingAlgorithm:
        return self._algorithms[key]

    def _run_single(self, key: str) -> None:
        if not self._ensure_data():
            return
        alg = self._algorithm_for(key)
        self._start_measured_animation(alg)

    def _run_all(self) -> None:
        if not self._ensure_data():
            return
        self._anim.cancel()

        stats = SortStats()
        base = copy(self._data)
        sequence: List[SortingAlgorithm] = []

        for key in ("bubble", "merge", "quick"):
            alg = self._algorithm_for(key)
            ms, last = measure_sort(lambda a=alg, b=copy(base): a.steps(b))
            comps = last.comparisons if isinstance(last, SortState) else 0
            cplx = self._complexity[alg.name]
            stats.results.append(
                AlgorithmResult(
                    name=alg.name,
                    time_ms=ms,
                    comparisons=comps,
                    complexity_best=cplx["best"],
                    complexity_avg=cplx["avg"],
                    complexity_worst=cplx["worst"],
                )
            )
            sequence.append(alg)

        self._set_results_text(stats.as_text())

        fastest = stats.fastest()
        fastest_name = fastest.name if fastest else ""
        self._play_animation_sequence(sequence, 0, fastest_name)

    def _start_measured_animation(self, alg: SortingAlgorithm) -> None:
        self._anim.cancel()
        base = copy(self._data)
        ms, last = measure_sort(lambda: alg.steps(copy(base)))
        comps = last.comparisons if isinstance(last, SortState) else 0
        cplx = self._complexity[alg.name]
        result = AlgorithmResult(
            name=alg.name,
            time_ms=ms,
            comparisons=comps,
            complexity_best=cplx["best"],
            complexity_avg=cplx["avg"],
            complexity_worst=cplx["worst"],
        )
        text = SortStats([result]).as_text()
        self._set_results_text(text)

        self._anim.set_delay_ms(int(self._speed.get()))
        self.chart.reset_colors(self._data)

        def on_step(state: SortState) -> None:
            self.chart.update_state(state)

        self._anim.start(alg.steps(copy(self._data)), on_step=on_step)

    def _play_animation_sequence(
        self,
        algorithms: List[SortingAlgorithm],
        index: int,
        fastest_name: str,
    ) -> None:
        """Play algorithm visualizations back-to-back after Run All."""
        if index >= len(algorithms):
            suffix = (
                f"\nAll visualizations finished.\nFastest (by time): {fastest_name}\n"
                if fastest_name
                else "\nAll visualizations finished.\n"
            )
            self._append_results(suffix)
            return

        alg = algorithms[index]

        def gen_factory():
            return alg.steps(copy(self._data))

        def on_step(state: SortState) -> None:
            self.chart.update_state(state)

        def on_complete() -> None:
            self._play_animation_sequence(algorithms, index + 1, fastest_name)

        def kickoff() -> None:
            self.chart.reset_colors(self._data)
            self._anim.set_delay_ms(int(self._speed.get()))
            self._anim.start(
                gen_factory(),
                on_step=on_step,
                on_complete=on_complete,
            )

        delay_ms = 0 if index == 0 else 400
        if delay_ms:
            self.root.after(delay_ms, kickoff)
        else:
            kickoff()

    # --------------------------------------------------------------- results IO
    def _set_results_text(self, content: str) -> None:
        self.results_text.configure(state=tk.NORMAL)
        self.results_text.delete("1.0", tk.END)
        self.results_text.insert(tk.END, content)
        self.results_text.configure(state=tk.DISABLED)

    def _append_results(self, content: str) -> None:
        self.results_text.configure(state=tk.NORMAL)
        self.results_text.insert(tk.END, content)
        self.results_text.configure(state=tk.DISABLED)


def run_app() -> None:
    """
    Start the GUI event loop.

    Tk root must exist before matplotlib's TkAgg canvas backend is loaded,
    otherwise the window may never appear or the process can exit immediately.
    """
    import matplotlib

    matplotlib.use("TkAgg")

    root = tk.Tk()
    app = SortingVisualizerApp(root)

    root.update_idletasks()
    root.deiconify()
    root.lift()
    try:
        root.attributes("-topmost", True)
    except tk.TclError:
        pass

    def _unset_topmost() -> None:
        try:
            root.attributes("-topmost", False)
        except tk.TclError:
            pass

    root.after(150, _unset_topmost)
    root.mainloop()
