"""Timing and comparison statistics for sorting runs."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class AlgorithmResult:
    """Outcome of running one algorithm on a dataset."""

    name: str
    time_ms: float
    comparisons: int
    complexity_best: str
    complexity_avg: str
    complexity_worst: str


@dataclass
class SortStats:
    """Aggregate results when comparing multiple algorithms."""

    results: List[AlgorithmResult] = field(default_factory=list)

    def fastest(self) -> Optional[AlgorithmResult]:
        """Return the result with the smallest elapsed time, if any."""
        if not self.results:
            return None
        return min(self.results, key=lambda r: r.time_ms)

    def as_text(self) -> str:
        """Human-readable summary for the results panel."""
        if not self.results:
            return "No runs yet."

        lines: List[str] = []
        for r in self.results:
            lines.append(
                f"{r.name}\n"
                f"  Time: {r.time_ms:.3f} ms\n"
                f"  Comparisons: {r.comparisons}\n"
                f"  Complexity: best {r.complexity_best}, "
                f"avg {r.complexity_avg}, worst {r.complexity_worst}\n"
            )

        fastest = self.fastest()
        if fastest and len(self.results) > 1:
            lines.append(f"Fastest (by time): {fastest.name}\n")

        return "\n".join(lines)


def complexity_table() -> Dict[str, Dict[str, str]]:
    """Big-O strings keyed by algorithm name."""
    return {
        "Bubble Sort": {
            "best": "O(n)",
            "avg": "O(n²)",
            "worst": "O(n²)",
        },
        "Merge Sort": {
            "best": "O(n log n)",
            "avg": "O(n log n)",
            "worst": "O(n log n)",
        },
        "Quick Sort": {
            "best": "O(n log n)",
            "avg": "O(n log n)",
            "worst": "O(n²)",
        },
    }
