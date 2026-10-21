import copy
import itertools
import pytest
from agent_benchmark.ledger import summarize


def ev(event_id, call_id, event, seq):
    return {"id": event_id, "call_id": call_id, "event": event, "seq": seq}


def test_empty():
    assert summarize([]) == {"total_calls": 0, "successful_calls": 0, "failed_calls": 0,
                             "pending_calls": 0, "conflicted_calls": 0, "orphan_calls": 0, "calls": {}}


def test_success_and_failure():
    data = [ev("1", "z", "started", 1), ev("2", "z", "succeeded", 3),
            ev("3", "a", "started", 1), ev("4", "a", "failed", 2)]
    result = summarize(data)
    assert result["successful_calls"] == 1
    assert result["failed_calls"] == 1
    assert list(result["calls"]) == ["a", "z"]


def test_duplicate_delivery_does_not_inflate_success():
    data = [ev("1", "x", "started", 0), ev("2", "x", "succeeded", 1)]
    assert summarize(data + [copy.deepcopy(data[1])] * 50)["successful_calls"] == 1


def test_conflicting_same_id_rejected():
    with pytest.raises(ValueError):
        summarize([ev("same", "x", "started", 0), ev("same", "x", "succeeded", 1)])


def test_tied_terminal_states_produce_conflict():
    data = [ev("1", "x", "started", 1), ev("2", "x", "succeeded", 2), ev("3", "x", "failed", 2)]
    assert summarize(data)["calls"]["x"] == "conflict"
    assert summarize(data)["successful_calls"] == 0


def test_latest_start_resets_attempt():
    data = [ev("1", "x", "started", 1), ev("2", "x", "succeeded", 2), ev("3", "x", "started", 3)]
    assert summarize(data)["calls"]["x"] == "pending"


def test_orphan_terminal():
    assert summarize([ev("1", "x", "succeeded", 5)])["calls"]["x"] == "orphan"


def test_terminal_same_seq_as_start_not_eligible():
    assert summarize([ev("1", "x", "started", 2), ev("2", "x", "succeeded", 2)])["calls"]["x"] == "pending"


def test_deterministic_under_permutations():
    data = [ev("1", "b", "started", 1), ev("2", "b", "succeeded", 2),
            ev("3", "a", "failed", 4), ev("4", "a", "started", 1)]
    expected = summarize(data)
    for perm in itertools.permutations(data):
        assert summarize(list(perm)) == expected


def test_does_not_mutate_input():
    data = [ev("1", "x", "started", 0)]
    original = copy.deepcopy(data)
    summarize(data)
    assert data == original


@pytest.mark.parametrize("invalid", [None, {}, "hello", [None], [{}],
    [ev("", "x", "started", 1)], [ev("1", "", "started", 1)],
    [ev("1", "x", "unknown", 1)], [ev("1", "x", "started", True)],
    [ev("1", "x", "started", -1)], [ev("1", "x", "started", 2.0)]])
def test_invalid_input(invalid):
    with pytest.raises(ValueError):
        summarize(invalid)
