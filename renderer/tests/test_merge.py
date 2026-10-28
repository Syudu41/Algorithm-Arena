"""Independent trace replay, identities, metric definitions and edge cases."""
import json
import random
from dataclasses import FrozenInstanceError, replace
import pytest
from arena.merge import (Compare, Complete, MergeComplete, MergeStart, Split, Write,
                         merge_trace, replay)


@pytest.mark.parametrize('values',[[5,2,4,1,3],[8,3,7,2,6],[4,1,6,2,5,3],
    [1,2],[2,1],[2,2],[0,0,0,0],[-99,99,0,-99,99],list(range(10)),list(range(9,-1,-1))])
def test_trace_reconstructs_stable_sorted_result(values):
    trace=merge_trace(values)
    assert trace.initial==tuple(values)
    assert trace.final==tuple(sorted(values))==replay(values,trace.events)
    # Independent identity check: stable sorting must preserve increasing original
    # indices for equal values, regardless of intermediate positions.
    assert trace.identities==tuple(sorted(range(len(values)),key=lambda i:values[i]))
    assert trace.comparisons==sum(isinstance(e,Compare) for e in trace.events)
    assert trace.writes==sum(isinstance(e,Write) for e in trace.events)
    assert trace.writes==sum(e.hi-e.lo for e in trace.events if isinstance(e,MergeStart))
    assert sum(isinstance(e,Split) for e in trace.events)==len(values)-1
    assert sum(isinstance(e,MergeComplete) for e in trace.events)==len(values)-1
    assert trace.events[-1]==Complete(trace.final,trace.identities,trace.comparisons,trace.writes)


def test_seeded_inputs_and_write_recurrence():
    rng=random.Random(7623)
    def expected_writes(n):
        return 0 if n==1 else n+expected_writes(n//2)+expected_writes(n-n//2)
    for _ in range(500):
        values=[rng.randint(-99,99) for _ in range(rng.randint(2,10))]
        trace=merge_trace(values)
        assert replay(values,trace.events)==tuple(sorted(values))
        assert trace.identities==tuple(sorted(range(len(values)),key=lambda i:values[i]))
        assert trace.writes==expected_writes(len(values))


@pytest.mark.parametrize('values,comparisons,writes',[
    ([5,2,4,1,3],8,12),([8,3,7,2,6],8,12),([4,1,6,2,5,3],10,16),
    ([1,1,1,1],4,8),(list(range(8)),12,24),(list(range(7,-1,-1)),12,24)])
def test_known_metrics(values,comparisons,writes):
    trace=merge_trace(values)
    assert (trace.comparisons,trace.writes)==(comparisons,writes)


def test_stable_left_choice_and_remainders():
    trace=merge_trace([2,1,2,1])
    assert all(e.take_left for e in trace.events if isinstance(e,Compare) and e.left==e.right)
    assert any(isinstance(e,Write) and e.remainder for e in trace.events)
    assert any(isinstance(e,Write) and not e.remainder for e in trace.events)


def test_frozen_serializable_events_and_preserved_input():
    values=[5,2,4,1,3];trace=merge_trace(values)
    assert values==[5,2,4,1,3]
    with pytest.raises(FrozenInstanceError):trace.events[0].lo=9
    data=json.loads(json.dumps(trace.to_dict()))
    assert data['algorithm']=='merge' and data['final']==[1,2,3,4,5]


@pytest.mark.parametrize('values',[[],[1],list(range(11)),[False,2],[1,2.0],[1,'2'],[-100,0],[0,100]])
def test_validation(values):
    with pytest.raises((ValueError,TypeError)):merge_trace(values)


def test_replay_rejects_corrupt_comparison_and_write():
    trace=merge_trace([5,2,4,1,3])
    for kind,changes in [(Compare,{'take_left':True}),(Write,{'target':99})]:
        events=list(trace.events)
        i=next(i for i,e in enumerate(events) if isinstance(e,kind))
        events[i]=replace(events[i],**changes)
        with pytest.raises(ValueError):replay(trace.initial,events)
