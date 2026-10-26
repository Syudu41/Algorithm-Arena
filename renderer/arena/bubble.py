"""Deterministic Bubble Sort that records an immutable, replayable trace.

The Manim scenes never sort anything themselves: they only animate the
events produced here, so the video cannot disagree with the algorithm.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Iterable, Sequence, Union


@dataclass(frozen=True)
class Compare:
    i: int
    j: int
    left: int
    right: int
    swap: bool  # True when left > right, i.e. a Swap event follows


@dataclass(frozen=True)
class Swap:
    i: int
    j: int


@dataclass(frozen=True)
class PassComplete:
    number: int        # 1-based pass number
    sorted_from: int   # indices >= sorted_from are in their final place
    early_exit: bool   # pass made no swaps, so the whole array is sorted


@dataclass(frozen=True)
class Complete:
    values: tuple[int, ...]
    comparisons: int
    swaps: int


Event = Union[Compare, Swap, PassComplete, Complete]


@dataclass(frozen=True)
class Trace:
    initial: tuple[int, ...]
    events: tuple[Event, ...]
    final: tuple[int, ...]
    comparisons: int
    swaps: int

    def to_dict(self) -> dict:
        return {
            "algorithm": "bubble",
            "initial": list(self.initial),
            "final": list(self.final),
            "comparisons": self.comparisons,
            "swaps": self.swaps,
            "events": [{"type": type(e).__name__, **asdict(e)} for e in self.events],
        }


def bubble_trace(values: Sequence[int]) -> Trace:
    """Bubble Sort with early exit: O(n^2) worst/average, O(n) best case."""
    a = list(values)
    n = len(a)
    events: list[Event] = []
    comparisons = swaps = 0
    for p in range(n - 1):
        swapped = False
        for i in range(n - 1 - p):
            j = i + 1
            needs_swap = a[i] > a[j]
            events.append(Compare(i, j, a[i], a[j], needs_swap))
            comparisons += 1
            if needs_swap:
                a[i], a[j] = a[j], a[i]
                events.append(Swap(i, j))
                swaps += 1
                swapped = True
        last_pass = p == n - 2
        early_exit = not swapped and not last_pass
        sorted_from = 0 if (early_exit or last_pass) else n - 1 - p
        events.append(PassComplete(p + 1, sorted_from, early_exit))
        if early_exit:
            break
    final = tuple(a)
    events.append(Complete(final, comparisons, swaps))
    return Trace(tuple(values), tuple(events), final, comparisons, swaps)


def replay(values: Sequence[int], events: Iterable[Event]) -> tuple[int, ...]:
    """Rebuild the end state from the trace alone (used by tests)."""
    a = list(values)
    for ev in events:
        if isinstance(ev, Swap):
            a[ev.i], a[ev.j] = a[ev.j], a[ev.i]
    return tuple(a)
