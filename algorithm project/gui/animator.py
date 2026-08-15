"""Drive step-by-step sort animation on the Tk event loop."""

from __future__ import annotations

import time
from typing import Any, Callable, Generator, Optional, TypeVar

T = TypeVar("T")


class AnimationController:
    """
    Schedule repeated callbacks to consume a generator.

    Supports pause/resume and cancellation without blocking the UI thread.
    """

    def __init__(self, root) -> None:
        self._root = root
        self._after_id: Optional[str] = None
        self._gen: Optional[Generator[T, None, None]] = None
        self._paused = False
        self._delay_ms = 30
        self._on_step: Optional[Callable[[T], None]] = None
        self._on_complete: Optional[Callable[[], None]] = None

    @property
    def is_running(self) -> bool:
        return self._gen is not None

    @property
    def paused(self) -> bool:
        return self._paused

    def set_delay_ms(self, delay_ms: int) -> None:
        self._delay_ms = max(0, int(delay_ms))

    def pause(self) -> None:
        self._paused = True

    def resume(self) -> None:
        if not self._paused or self._gen is None:
            return
        self._paused = False
        self._schedule_next()

    def cancel(self) -> None:
        if self._after_id is not None:
            self._root.after_cancel(self._after_id)
            self._after_id = None
        self._gen = None
        self._paused = False
        self._on_step = None
        self._on_complete = None

    def start(
        self,
        gen: Generator[T, None, None],
        on_step: Callable[[T], None],
        on_complete: Optional[Callable[[], None]] = None,
    ) -> None:
        self.cancel()
        self._gen = gen
        self._on_step = on_step
        self._on_complete = on_complete
        self._paused = False
        self._schedule_next()

    def _schedule_next(self) -> None:
        if self._gen is None:
            return
        self._after_id = self._root.after(self._delay_ms, self._tick)

    def _tick(self) -> None:
        self._after_id = None
        if self._gen is None or self._on_step is None:
            return
        if self._paused:
            return

        try:
            state = next(self._gen)
        except StopIteration:
            self._finish()
            return

        self._on_step(state)
        self._schedule_next()

    def _finish(self) -> None:
        complete = self._on_complete
        self._gen = None
        self._on_step = None
        self._on_complete = None
        self._paused = False
        if complete:
            complete()


def measure_sort(
    gen_factory: Callable[[], Generator[Any, None, None]],
) -> tuple[float, Any]:
    """
    Consume a fresh generator and return (elapsed_ms, last_yielded_value).

    Used for timing and final comparison counts without UI delays.
    """
    gen = gen_factory()
    t0 = time.perf_counter()
    last = None
    for item in gen:
        last = item
    t1 = time.perf_counter()
    return (t1 - t0) * 1000.0, last
