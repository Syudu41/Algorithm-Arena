"""Stable top-down Merge Sort with immutable, identity-preserving events.

Comparisons count only head-to-head value comparisons. Writes count placements
into each merged output run, including remainders; allocation and copy-back
bookkeeping are excluded. Half-open ranges use the ordinary floor midpoint.
"""
from __future__ import annotations
from dataclasses import asdict, dataclass
from typing import Iterable, Sequence, Union
from .validation import validate_values


@dataclass(frozen=True)
class Split:
    lo: int
    mid: int
    hi: int
    depth: int


@dataclass(frozen=True)
class MergeStart:
    lo: int
    mid: int
    hi: int
    depth: int
    left_ids: tuple[int, ...]
    right_ids: tuple[int, ...]


@dataclass(frozen=True)
class Compare:
    left_id: int
    right_id: int
    left: int
    right: int
    take_left: bool


@dataclass(frozen=True)
class Write:
    target: int
    identity: int
    value: int
    from_left: bool
    remainder: bool


@dataclass(frozen=True)
class MergeComplete:
    lo: int
    hi: int
    identities: tuple[int, ...]


@dataclass(frozen=True)
class Complete:
    values: tuple[int, ...]
    identities: tuple[int, ...]
    comparisons: int
    writes: int


Event = Union[Split, MergeStart, Compare, Write, MergeComplete, Complete]


@dataclass(frozen=True)
class Trace:
    initial: tuple[int, ...]
    final: tuple[int, ...]
    identities: tuple[int, ...]
    events: tuple[Event, ...]
    comparisons: int
    writes: int

    def to_dict(self):
        return {'algorithm':'merge', 'initial':list(self.initial), 'final':list(self.final),
                'identities':list(self.identities), 'comparisons':self.comparisons,
                'writes':self.writes,
                'events':[{'type':type(e).__name__, **asdict(e)} for e in self.events]}


def merge_trace(values: Sequence[int]) -> Trace:
    a = validate_values(list(values))
    initial = tuple(a)
    ids = list(range(len(a)))
    events: list[Event] = []
    comparisons = writes = 0

    def sort(lo, hi, depth):
        nonlocal comparisons, writes
        if hi-lo < 2:
            return
        mid = (lo+hi)//2
        events.append(Split(lo, mid, hi, depth))
        sort(lo, mid, depth+1)
        sort(mid, hi, depth+1)
        left, right = ids[lo:mid], ids[mid:hi]
        events.append(MergeStart(lo, mid, hi, depth, tuple(left), tuple(right)))
        i = j = 0
        merged = []
        while i<len(left) or j<len(right):
            remainder = i==len(left) or j==len(right)
            if not remainder:
                take_left = initial[left[i]] <= initial[right[j]]
                comparisons += 1
                events.append(Compare(left[i], right[j], initial[left[i]],
                                      initial[right[j]], take_left))
            else:
                take_left = j==len(right)
            identity = left[i] if take_left else right[j]
            events.append(Write(lo+len(merged), identity, initial[identity], take_left, remainder))
            merged.append(identity)
            writes += 1
            if take_left:i += 1
            else:j += 1
        ids[lo:hi] = merged
        events.append(MergeComplete(lo, hi, tuple(merged)))

    sort(0, len(a), 0)
    final = tuple(initial[i] for i in ids)
    events.append(Complete(final, tuple(ids), comparisons, writes))
    return Trace(initial, final, tuple(ids), tuple(events), comparisons, writes)


def replay(values: Sequence[int], events: Iterable[Event]) -> tuple[int, ...]:
    """Rebuild the result solely from event identities, checking merge semantics."""
    initial = tuple(values)
    ids = list(range(len(initial)))
    active = None
    comparisons = writes = 0
    for ev in events:
        if isinstance(ev, Split):
            if not (0 <= ev.lo < ev.mid < ev.hi <= len(ids)):
                raise ValueError('invalid split bounds')
        elif isinstance(ev, MergeStart):
            if active is not None or tuple(ids[ev.lo:ev.mid])!=ev.left_ids or tuple(ids[ev.mid:ev.hi])!=ev.right_ids:
                raise ValueError('merge runs disagree with state')
            if any(list(run)!=sorted(run,key=lambda i:initial[i]) for run in (ev.left_ids,ev.right_ids)):
                raise ValueError('input run is not ordered')
            active = {'event':ev,'left':list(ev.left_ids),'right':list(ev.right_ids),'output':[],'choice':None}
        elif isinstance(ev, Compare):
            if active is None or not active['left'] or not active['right']:
                raise ValueError('comparison without two run heads')
            left,right = active['left'][0],active['right'][0]
            if (ev.left_id,ev.right_id,ev.left,ev.right,ev.take_left)!=(left,right,initial[left],initial[right],initial[left]<=initial[right]):
                raise ValueError('comparison disagrees with run heads')
            active['choice'] = ev.take_left
            comparisons += 1
        elif isinstance(ev, Write):
            if active is None:raise ValueError('write outside merge')
            run = active['left'] if ev.from_left else active['right']
            remainder = not active['left'] or not active['right']
            if not run or ev.target!=active['event'].lo+len(active['output']) or run[0]!=ev.identity or initial[ev.identity]!=ev.value or remainder!=ev.remainder:
                raise ValueError('write disagrees with next output slot')
            if not remainder and active['choice']!=ev.from_left:
                raise ValueError('write must follow comparison choice')
            active['output'].append(run.pop(0));active['choice']=None;writes+=1
        elif isinstance(ev, MergeComplete):
            if active is None or active['left'] or active['right'] or tuple(active['output'])!=ev.identities or (ev.lo,ev.hi)!=(active['event'].lo,active['event'].hi):
                raise ValueError('incomplete merge')
            ids[ev.lo:ev.hi]=ev.identities
            active=None
        elif isinstance(ev, Complete):
            if active is not None or (tuple(initial[i] for i in ids),tuple(ids),comparisons,writes)!=(ev.values,ev.identities,ev.comparisons,ev.writes):
                raise ValueError('completion disagrees with replay')
    if active is not None:raise ValueError('unfinished merge')
    return tuple(initial[i] for i in ids)
