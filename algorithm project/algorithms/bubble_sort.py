"""Bubble sort with step-by-step states for visualization."""

from __future__ import annotations

from copy import copy
from typing import Generator, List, Set

from algorithms.base import SortState


class BubbleSort:
    name = "Bubble Sort"

    def steps(self, values: List[float]) -> Generator[SortState, None, None]:
        arr = copy(values)
        n = len(arr)
        comparisons = 0
        sorted_so_far: Set[int] = set()

        if n <= 1:
            yield SortState(values=copy(arr), sorted_indices=set(range(n)), comparisons=0)
            return

        for i in range(n):
            swapped = False
            for j in range(0, n - i - 1):
                comparisons += 1
                yield SortState(
                    values=copy(arr),
                    compare=(j, j + 1),
                    sorted_indices=set(sorted_so_far),
                    comparisons=comparisons,
                )
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    swapped = True
                    yield SortState(
                        values=copy(arr),
                        swap=(j, j + 1),
                        sorted_indices=set(sorted_so_far),
                        comparisons=comparisons,
                    )
            sorted_so_far.add(n - i - 1)
            if not swapped:
                # Array is fully sorted; mark all indices for the final frame.
                sorted_so_far = set(range(n))
                break

        if len(sorted_so_far) < n:
            sorted_so_far = set(range(n))
        yield SortState(
            values=copy(arr),
            sorted_indices=sorted_so_far,
            comparisons=comparisons,
        )
