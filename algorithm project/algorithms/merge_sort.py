"""Merge sort (iterative merge passes) with visualization steps."""

from __future__ import annotations

from copy import copy
from typing import Generator, List, Set

from algorithms.base import SortState


class MergeSort:
    name = "Merge Sort"

    def steps(self, values: List[float]) -> Generator[SortState, None, None]:
        arr = copy(values)
        n = len(arr)
        comparisons = 0

        if n <= 1:
            yield SortState(values=copy(arr), sorted_indices=set(range(n)), comparisons=0)
            return

        width = 1
        while width < n:
            for left in range(0, n, 2 * width):
                mid = min(left + width, n)
                right = min(left + 2 * width, n)
                if mid >= right:
                    continue

                i, j = left, mid
                temp: List[float] = []
                while i < mid and j < right:
                    comparisons += 1
                    yield SortState(
                        values=copy(arr),
                        compare=(i, j),
                        sorted_indices=self._sorted_ranges(left, width, n),
                        comparisons=comparisons,
                    )
                    if arr[i] <= arr[j]:
                        temp.append(arr[i])
                        i += 1
                    else:
                        temp.append(arr[j])
                        j += 1
                while i < mid:
                    temp.append(arr[i])
                    i += 1
                while j < right:
                    temp.append(arr[j])
                    j += 1

                for k, val in enumerate(temp):
                    arr[left + k] = val
                    yield SortState(
                        values=copy(arr),
                        swap=(left + k, left + k),
                        sorted_indices=self._sorted_ranges(left, width, n),
                        comparisons=comparisons,
                    )

            width *= 2

        yield SortState(
            values=copy(arr),
            sorted_indices=set(range(n)),
            comparisons=comparisons,
        )

    @staticmethod
    def _sorted_ranges(left: int, width: int, n: int) -> Set[int]:
        """Approximate which positions are stable within current pass."""
        # After a full width pass completes, blocks of size `width` are sorted.
        # For simplicity during merge, highlight the active window.
        end = min(left + 2 * width, n)
        return set(range(left, end))
