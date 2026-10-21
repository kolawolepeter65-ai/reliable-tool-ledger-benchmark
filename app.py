"""Interactive companion demo for the tool-call ledger coding benchmark."""
import json
import streamlit as st
from agent_benchmark.ledger import summarize

st.set_page_config(page_title="Reliable Tool-Call Ledger", page_icon="🧪", layout="wide")
st.title("Reliable Tool-Call Ledger")
st.caption("Interactive companion to a Python SWE-agent benchmark: deduplication, retries, conflicts, and out-of-order tool events.")
st.info("This is a deterministic coding benchmark demo, not a deployed autonomous agent.")

EXAMPLES = {
    "Duplicate delivery": [
        {"id": "start-1", "call_id": "search", "event": "started", "seq": 1},
        {"id": "finish-1", "call_id": "search", "event": "succeeded", "seq": 2},
        {"id": "finish-1", "call_id": "search", "event": "succeeded", "seq": 2},
    ],
    "Conflicting outcomes": [
        {"id": "a", "call_id": "checkout", "event": "started", "seq": 1},
        {"id": "b", "call_id": "checkout", "event": "succeeded", "seq": 2},
        {"id": "c", "call_id": "checkout", "event": "failed", "seq": 2},
    ],
    "Stale success after retry": [
        {"id": "a", "call_id": "upload", "event": "started", "seq": 1},
        {"id": "b", "call_id": "upload", "event": "succeeded", "seq": 2},
        {"id": "c", "call_id": "upload", "event": "started", "seq": 3},
    ],
}
example = st.selectbox("Choose an example", list(EXAMPLES))
if st.session_state.get("example") != example:
    st.session_state.example = example
    st.session_state.events = json.dumps(EXAMPLES[example], indent=2)
data = st.text_area("Edit JSON tool events", key="events", height=260)
if st.button("Reconcile events", type="primary"):
    try:
        result = summarize(json.loads(data))
    except (ValueError, TypeError, json.JSONDecodeError) as error:
        st.error(f"Invalid input: {error}")
    else:
        a, b, c = st.columns(3)
        a.metric("Logical calls", result["total_calls"])
        b.metric("Successful", result["successful_calls"])
        c.metric("Conflicted", result["conflicted_calls"])
        st.subheader("Reconciled statuses")
        st.json(result)
        st.caption("Compare the results with the task specification and 21 pytest cases in the source repository.")
st.markdown("[Task specification](https://github.com/kolawolepeter65-ai/reliable-tool-ledger-benchmark/blob/main/task/TASK.md) · [Source code](https://github.com/kolawolepeter65-ai/reliable-tool-ledger-benchmark)")
