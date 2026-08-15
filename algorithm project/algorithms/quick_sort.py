"""Quick sort (Lomuto partition) with recursion and visualization."""

from __future__ import annotations

from copy import copy
from typing import Generator, List

from algorithms.base import SortState


class QuickSort:
    name = "Quick Sort"

    def steps(self, values: List[float]) -> Generator[SortState, None, None]:
        arr = copy(values)
        counters = {"comparisons": 0}

        if len(arr) <= 1:
            yield SortState(
                values=copy(arr),
                sorted_indices=set(range(len(arr))),
                comparisons=0,
            )
            return

        yield from self._quicksort(arr, 0, len(arr) - 1, counters)

        yield SortState(
            values=copy(arr),
            sorted_indices=set(range(len(arr))),
            comparisons=counters["comparisons"],
        )

    def _quicksort(
        self,
        arr: List[float],
        low: int,
        high: int,
        counters: dict,
    ) -> Generator[SortState, None, None]:
        if low < high:
            pivot_idx = yield from self._partition(arr, low, high, counters)
            yield from self._quicksort(arr, low, pivot_idx - 1, counters)
            yield from self._quicksort(arr, pivot_idx + 1, high, counters)
        elif low == high:
            yield SortState(
                values=copy(arr),
                sorted_indices={low},
                comparisons=counters["comparisons"],
            )

    def _partition(
        self,
        arr: List[float],
        low: int,
        high: int,
        counters: dict,
    ) -> Generator[SortState, None, int]:
        pivot_val = arr[high]
        i = low - 1

        yield SortState(
            values=copy(arr),
            pivot=high,
            comparisons=counters["comparisons"],
        )

        for j in range(low, high):
            counters["comparisons"] += 1
            yield SortState(
                values=copy(arr),
                pivot=high,
                compare=(j, high),
                comparisons=counters["comparisons"],
            )
            if arr[j] <= pivot_val:
                i += 1
                if i != j:
                    arr[i], arr[j] = arr[j], arr[i]
                    yield SortState(
                        values=copy(arr),
                        pivot=high,
                        swap=(i, j),
                        comparisons=counters["comparisons"],
                    )

        i += 1
        if i != high:
            arr[i], arr[high] = arr[high], arr[i]
            yield SortState(
                values=copy(arr),
                pivot=i,
                swap=(i, high),
                comparisons=counters["comparisons"],
            )

        return i
