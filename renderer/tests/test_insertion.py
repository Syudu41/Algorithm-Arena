import json
import random

import pytest

from arena.insertion import Compare, Complete, InsertKey, PassComplete, SelectKey, Shift, insertion_trace, replay
from arena.validation import InputError

CASES = [[5,2,4,1,3],[8,3,7,2,6],[1,2],[2,1],[7,7,7,7],
         list(range(1,11)),list(range(10,0,-1)),[-99,99,0,-1,1],
         [99,-99],[3,-3,3,-3,0,0]]


@pytest.mark.parametrize('values', CASES)
def test_insertion_matches_sorted_and_replays(values):
    trace = insertion_trace(values)
    assert trace.final == tuple(sorted(values)) == replay(values, trace.events)
    assert trace.comparisons == sum(isinstance(e,Compare) for e in trace.events)
    assert trace.shifts == sum(isinstance(e,Shift) for e in trace.events)
    assert trace.placements == sum(isinstance(e,InsertKey) for e in trace.events) == len(values)-1
    assert trace.events[-1] == Complete(trace.final,trace.comparisons,trace.shifts,trace.placements)
    json.dumps(trace.to_dict())


def test_random_arrays_and_inversion_count():
    rng=random.Random(7623)
    for _ in range(500):
        values=[rng.randint(-99,99) for _ in range(rng.randint(2,10))]
        trace=insertion_trace(values)
        assert trace.final == tuple(sorted(values)) == replay(values,trace.events)
        assert trace.shifts == sum(a>b for i,a in enumerate(values) for b in values[i+1:])


@pytest.mark.parametrize('values',CASES)
def test_trace_tracks_hole_and_preserves_equal_value_identity(values):
    # Track original identities as well as values, to prove stability.
    state=list(enumerate(values)); key=None; gap=None; comparisons=shifts=placements=0
    events=insertion_trace(values).events
    for k,ev in enumerate(events):
        if isinstance(ev,SelectKey):
            assert key is None and 1<=ev.index<len(values)
            key=state[ev.index];gap=ev.index;state[gap]=None
            assert key[1]==ev.value
        elif isinstance(ev,Compare):
            comparisons+=1
            assert 0<=ev.left_index<len(values)-1 and ev.gap==ev.left_index+1==gap
            assert state[ev.left_index][1]==ev.left and key[1]==ev.key
            assert ev.shift==(ev.left>ev.key)
            assert isinstance(events[k+1],Shift)==ev.shift
        elif isinstance(ev,Shift):
            shifts+=1
            assert ev.target==gap and ev.target==ev.source+1
            assert state[ev.source][1]>key[1]
            state[ev.target],state[ev.source]=state[ev.source],None;gap=ev.source
        elif isinstance(ev,InsertKey):
            placements+=1
            assert ev.index==gap and key[1]==ev.value
            state[gap]=key;gap=key=None
        elif isinstance(ev,PassComplete):
            assert key is None
            assert [v for _,v in state[:ev.sorted_until+1]]==sorted(values[:ev.sorted_until+1])
    assert state==sorted(enumerate(values),key=lambda pair:pair[1])


def test_sorted_best_case_and_reversed_worst_case():
    for n in range(2,11):
        best=insertion_trace(list(range(n)))
        worst=insertion_trace(list(range(n,0,-1)))
        assert (best.comparisons,best.shifts,best.placements)==(n-1,0,n-1)
        assert worst.comparisons==worst.shifts==n*(n-1)//2


def test_known_metrics_and_input_not_mutated():
    values=[5,2,4,1,3];original=values.copy();trace=insertion_trace(values)
    assert values==original
    assert (trace.comparisons,trace.shifts,trace.placements)==(9,7,4)


@pytest.mark.parametrize('values', [[],[1],list(range(11)),[1,100],[True,2],[1.5,2],['1',2]])
def test_rejects_invalid_values(values):
    with pytest.raises(InputError): insertion_trace(values)
