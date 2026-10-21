# Agent Benchmark: Reliable Tool-Call Ledger

[![Python Tests](https://github.com/kolawolepeter65-ai/reliable-tool-ledger-benchmark/actions/workflows/tests.yml/badge.svg)](https://github.com/kolawolepeter65-ai/reliable-tool-ledger-benchmark/actions/workflows/tests.yml)

**[▶ Try the live Streamlit demo](https://reliable-tool-ledger-benchmark-cpjheacqbbygrnkllwme6v.streamlit.app/)**

An original, self-contained Python coding benchmark for software-engineering agents. Implement an **event-sourced tool-call ledger** robust to duplicate events, out-of-order arrivals, and conflicting outcomes.

**Skills:** task specification, test-driven development, Python, deterministic evaluation, adversarial tests, Docker, and software-agent reliability.

## Interactive demo

This repository includes a Streamlit companion app for exploring event reconciliation with example cases and editable JSON.

**Live app:** [Open the interactive benchmark](https://reliable-tool-ledger-benchmark-cpjheacqbbygrnkllwme6v.streamlit.app/).

**Deploy your own copy:** Open [Streamlit Community Cloud](https://share.streamlit.io/), create a new app from `kolawolepeter65-ai/reliable-tool-ledger-benchmark`, select branch `main`, and choose entry point `app.py`. The host will install dependencies using `requirements.txt`. Do not mistake the deployed demo for an autonomous agent; it illustrates the benchmark's reference logic.

Run the demo locally:

```bash
python -m pip install -e .
streamlit run app.py
```

## Run

```bash
python -m pip install -e '.[test]'
python -m pytest -q
```

With Docker:

```bash
docker build -t reliable-tool-ledger .
docker run --rm reliable-tool-ledger
```

## Repository layout

- [Task specification](task/TASK.md): input, behavior, expected output, evaluation rules
- [Reference solution](src/agent_benchmark/ledger.py): correct deterministic event reconciliation
- [Pytest tests](tests/test_ledger.py): 21 test cases, including 11 invalid input cases
- [Dockerfile](Dockerfile): reproducible container build
- [pyproject.toml](pyproject.toml): installable Python package and test dependencies

## Evaluation approach

Naive agents can inflate successful-call counts by counting replayed delivery events as distinct tool completions. This benchmark prevents that by requiring event-ID deduplication, active-attempt tracking, deterministic tie resolution, and input validation. A clean reference implementation passes **21 local pytest tests**. For blind agent evaluation, remove or hide the reference solution before distributing the task, and retain private tests separately.

## Example

```python
from agent_benchmark.ledger import summarize
events = [
    {"id":"a", "call_id":"tool-1", "event":"started", "seq":1},
    {"id":"b", "call_id":"tool-1", "event":"succeeded", "seq":2},
    {"id":"b", "call_id":"tool-1", "event":"succeeded", "seq":2},
]
assert summarize(events)["successful_calls"] == 1
```

## Integrity

Portfolio demonstration, not an official platform benchmark or evidence of testing production agents. All examples are synthetic. Do not claim synthetic scenarios are prior client incidents.

## Author

Kolawole Peter Olusola · [Portfolio](https://techbykhay.site/) · [LinkedIn](https://www.linkedin.com/in/kolawole-peter-olusola/)
