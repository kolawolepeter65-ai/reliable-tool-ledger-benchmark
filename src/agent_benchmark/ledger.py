"""Reference solution for a deterministic tool-call ledger."""
from collections import defaultdict

FIELDS = ("id", "call_id", "event", "seq")
KINDS = {"started", "succeeded", "failed"}


def summarize(events):
    """Validate, reconcile, and count tool-call lifecycle events."""
    if not isinstance(events, list):
        raise ValueError("events must be a list")
    by_id = {}
    for item in events:
        if not isinstance(item, dict) or any(key not in item for key in FIELDS):
            raise ValueError("malformed event")
        event_id, call_id, kind, seq = (item[key] for key in FIELDS)
        if not isinstance(event_id, str) or not event_id:
            raise ValueError("invalid id")
        if not isinstance(call_id, str) or not call_id:
            raise ValueError("invalid call_id")
        if kind not in KINDS or not isinstance(kind, str):
            raise ValueError("invalid event type")
        if type(seq) is not int or seq < 0:
            raise ValueError("invalid sequence number")
        canonical = (event_id, call_id, kind, seq)
        if event_id in by_id and by_id[event_id] != canonical:
            raise ValueError("conflicting event id")
        by_id[event_id] = canonical

    grouped = defaultdict(list)
    for _, call_id, kind, seq in by_id.values():
        grouped[call_id].append((kind, seq))

    statuses = {}
    for call_id in sorted(grouped):
        items = grouped[call_id]
        starts = [seq for kind, seq in items if kind == "started"]
        if not starts:
            statuses[call_id] = "orphan"
            continue
        latest_start = max(starts)
        terminals = [(kind, seq) for kind, seq in items
                     if kind in {"succeeded", "failed"} and seq > latest_start]
        if not terminals:
            statuses[call_id] = "pending"
            continue
        latest_terminal = max(seq for _, seq in terminals)
        kinds = {kind for kind, seq in terminals if seq == latest_terminal}
        statuses[call_id] = ("conflict" if len(kinds) > 1
                             else "success" if "succeeded" in kinds else "failure")

    return {
        "total_calls": len(statuses),
        "successful_calls": list(statuses.values()).count("success"),
        "failed_calls": list(statuses.values()).count("failure"),
        "pending_calls": list(statuses.values()).count("pending"),
        "conflicted_calls": list(statuses.values()).count("conflict"),
        "orphan_calls": list(statuses.values()).count("orphan"),
        "calls": statuses,
    }
