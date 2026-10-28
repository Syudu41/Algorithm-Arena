"""Stable insertion sort with an immutable, replayable hole/key trace.

Comparisons count value comparisons only (not index-boundary checks). A shift
moves one existing value one slot right. A placement reinserts the held key,
including keys that return to their original slot: exactly n-1 placements.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Iterable, Sequence, Union

from .validation import validate_values


@dataclass(frozen=True)
class SelectKey:
    index: int
    value: int


@dataclass(frozen=True)
class Compare:
    left_index: int
    gap: int
    left: int
    key: int
    shift: bool


@dataclass(frozen=True)
class Shift:
    source: int
    target: int
    value: int


@dataclass(frozen=True)
class InsertKey:
    index: int
    value: int


@dataclass(frozen=True)
class PassComplete:
    sorted_until: int  # inclusive; prefix is ordered, not permanently fixed


@dataclass(frozen=True)
class Complete:
    values: tuple[int, ...]
    comparisons: int
    shifts: int
    placements: int


Event = Union[SelectKey, Compare, Shift, InsertKey, PassComplete, Complete]


@dataclass(frozen=True)
class Trace:
    initial: tuple[int, ...]
    final: tuple[int, ...]
    events: tuple[Event, ...]
    comparisons: int
    shifts: int
    placements: int

    def to_dict(self) -> dict:
        return {'algorithm': 'insertion', 'initial': list(self.initial),
                'final': list(self.final), 'comparisons': self.comparisons,
                'shifts': self.shifts, 'placements': self.placements,
                'events': [{'type': type(e).__name__, **asdict(e)} for e in self.events]}


def insertion_trace(values: Sequence[int]) -> Trace:
    a = validate_values(list(values))
    initial = tuple(a)
    events: list[Event] = []
    comparisons = shifts = placements = 0
    for i in range(1, len(a)):
        key = a[i]
        events.append(SelectKey(i, key))
        j = i - 1
        while j >= 0:
            shift = a[j] > key
            events.append(Compare(j, j + 1, a[j], key, shift))
            comparisons += 1
            if not shift:
                break
            events.append(Shift(j, j + 1, a[j]))
            a[j + 1] = a[j]
            shifts += 1
            j -= 1
        a[j + 1] = key
        placements += 1
        events.append(InsertKey(j + 1, key))
        events.append(PassComplete(i))
    final = tuple(a)
    events.append(Complete(final, comparisons, shifts, placements))
    return Trace(initial, final, tuple(events), comparisons, shifts, placements)


def replay(values: Sequence[int], events: Iterable[Event]) -> tuple[int, ...]:
    """Rebuild using only key/shift/insert events, validating the hole semantics."""
    a = list(values)
    key = None
    gap = None
    for ev in events:
        if isinstance(ev, SelectKey):
            if key is not None or a[ev.index] != ev.value:
                raise ValueError('invalid key selection')
            key, gap = a[ev.index], ev.index
            a[gap] = None
        elif isinstance(ev, Compare):
            if key != ev.key or gap != ev.gap or a[ev.left_index] != ev.left:
                raise ValueError('comparison disagrees with trace state')
        elif isinstance(ev, Shift):
            if key is None or ev.target != gap or a[ev.source] != ev.value:
                raise ValueError('shift must fill the current gap')
            a[ev.target], a[ev.source] = a[ev.source], None
            gap = ev.source
        elif isinstance(ev, InsertKey):
            if key != ev.value or gap != ev.index:
                raise ValueError('placement must fill the current gap')
            a[ev.index], key, gap = key, None, None
        elif isinstance(ev, PassComplete):
            if key is not None or a[:ev.sorted_until + 1] != sorted(a[:ev.sorted_until + 1]):
                raise ValueError('prefix is not ordered')
    if key is not None or None in a:
        raise ValueError('trace leaves an unfilled gap')
    return tuple(a)
