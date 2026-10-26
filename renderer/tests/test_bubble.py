import itertools
import json
import random

import pytest

from arena.bubble import Compare, Complete, PassComplete, Swap, bubble_trace, replay
from arena.validation import InputError, parse_values, validate_values


CASES = [
    [5, 2, 4, 1, 3],
    [8, 3, 7, 2, 6],
    [1, 2],
    [2, 1],
    [7, 7, 7, 7],
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    [10, 9, 8, 7, 6, 5, 4, 3, 2, 1],
    [-99, 99, 0, -1, 1],
    [99, -99],
    [3, -3, 3, -3, 0, 0],
]


@pytest.mark.parametrize("values", CASES)
def test_matches_python_sorted(values):
    trace = bubble_trace(values)
    assert trace.final == tuple(sorted(values))
    assert trace.events[-1] == Complete(values=tuple(sorted(values)),
                                        comparisons=trace.comparisons,
                                        swaps=trace.swaps)


def test_random_arrays_match_sorted():
    rng = random.Random(7623)
    for _ in range(500):
        n = rng.randint(2, 10)
        values = [rng.randint(-99, 99) for _ in range(n)]
        trace = bubble_trace(values)
        assert trace.final == tuple(sorted(values))
        assert replay(values, trace.events) == trace.final


@pytest.mark.parametrize("values", CASES)
def test_events_use_valid_adjacent_indices(values):
    n = len(values)
    for ev in bubble_trace(values).events:
        if isinstance(ev, (Compare, Swap)):
            assert 0 <= ev.i < n - 1 and ev.j == ev.i + 1


@pytest.mark.parametrize("values", CASES)
def test_swap_follows_its_compare_and_only_when_out_of_order(values):
    events = bubble_trace(values).events
    for prev, ev in zip(events, events[1:]):
        if isinstance(ev, Swap):
            assert isinstance(prev, Compare) and prev.swap
            assert (prev.i, prev.j) == (ev.i, ev.j)
            assert prev.left > prev.right
    for k, ev in enumerate(events):
        if isinstance(ev, Compare):
            assert ev.swap == (ev.left > ev.right)
            assert isinstance(events[k + 1], Swap) == ev.swap


@pytest.mark.parametrize("values", CASES)
def test_counts_and_replay(values):
    trace = bubble_trace(values)
    assert trace.comparisons == sum(isinstance(e, Compare) for e in trace.events)
    assert trace.swaps == sum(isinstance(e, Swap) for e in trace.events)
    assert replay(values, trace.events) == tuple(sorted(values))


def test_compare_values_reflect_current_state():
    values = [5, 2, 4, 1, 3]
    state = list(values)
    for ev in bubble_trace(values).events:
        if isinstance(ev, Compare):
            assert (state[ev.i], state[ev.j]) == (ev.left, ev.right)
        elif isinstance(ev, Swap):
            state[ev.i], state[ev.j] = state[ev.j], state[ev.i]


def test_already_sorted_exits_after_one_pass():
    trace = bubble_trace([1, 2, 3, 4, 5])
    assert trace.comparisons == 4 and trace.swaps == 0
    passes = [e for e in trace.events if isinstance(e, PassComplete)]
    assert len(passes) == 1 and passes[0].early_exit


def test_reversed_is_worst_case():
    n = 10
    trace = bubble_trace(list(range(n, 0, -1)))
    assert trace.comparisons == n * (n - 1) // 2
    assert trace.swaps == n * (n - 1) // 2


@pytest.mark.parametrize("values", CASES)
def test_pass_complete_marks_growing_sorted_suffix(values):
    n = len(values)
    passes = [e for e in bubble_trace(values).events if isinstance(e, PassComplete)]
    # each non-final pass fixes one more slot; the final pass fixes everything
    for k, p in enumerate(passes[:-1]):
        assert p.number == k + 1 and not p.early_exit
        assert p.sorted_from == n - (k + 1)
    assert passes[-1].sorted_from == 0


def test_known_trace_5_2_4_1_3():
    t = bubble_trace([5, 2, 4, 1, 3])
    assert (t.comparisons, t.swaps) == (10, 7)


def test_trace_is_json_serializable():
    t = bubble_trace([5, 2, 4, 1, 3])
    json.dumps(t.to_dict())


def test_input_not_mutated():
    values = [3, 1, 2]
    bubble_trace(values)
    assert values == [3, 1, 2]


# ---------- validation ----------

@pytest.mark.parametrize("text,expected", [
    ("5,2,4,1,3", [5, 2, 4, 1, 3]),
    (" 5 , -2 ,0 ", [5, -2, 0]),
    ("-99,99", [-99, 99]),
    ("+7,7", [7, 7]),
    ("1,2,3,4,5,6,7,8,9,10", list(range(1, 11))),
])
def test_parse_accepts(text, expected):
    assert parse_values(text) == expected


@pytest.mark.parametrize("text", [
    "", "5", "1,,2", "1,2,", ",1,2", "1.5,2", "1e2,3", "a,b", "100,1", "-100,1",
    "NaN,1", "inf,1", "1+1,2", "__import__('os'),1", "1;2", "1 2", "0x10,1",
    "1,2,3,4,5,6,7,8,9,10,11", "１,２",  # full-width digits
])
def test_parse_rejects(text):
    with pytest.raises(InputError):
        parse_values(text)


@pytest.mark.parametrize("values", [
    [1], [], list(range(11)), [1, 100], [1.0, 2], [True, False], ["1", 2],
    None, "1,2", [1, None], {"a": 1},
])
def test_validate_rejects_bad_json_values(values):
    with pytest.raises(InputError):
        validate_values(values)


def test_validate_accepts_ints():
    assert validate_values([0, -99, 99]) == [0, -99, 99]
