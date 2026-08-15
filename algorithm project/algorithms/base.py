"""Shared types and protocol for sorting algorithms."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Generator, List, Optional, Protocol, Set, Tuple


@dataclass
class SortState:
    """
    One frame of the sort animation.

    Attributes:
        values: Current array snapshot (copy for safe rendering).
        compare: Indices currently being compared (highlight).
        swap: Indices that were just swapped (highlight).
        pivot: Pivot index for quicksort (optional).
        sorted_indices: Indices known to be in final position.
        comparisons: Running total of key comparisons so far.
    """

    values: List[float]
    compare: Optional[Tuple[int, int]] = None
    swap: Optional[Tuple[int, int]] = None
    pivot: Optional[int] = None
    sorted_indices: Set[int] = field(default_factory=set)
    comparisons: int = 0


class SortingAlgorithm(Protocol):
    """Protocol: each algorithm exposes a display name and a step generator."""

    name: str

    def steps(self, values: List[float]) -> Generator[SortState, None, None]:
        ...
