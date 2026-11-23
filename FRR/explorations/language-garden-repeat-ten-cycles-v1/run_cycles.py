"""Run ten frozen stages or audit their portable records without inference."""
import argparse
from collections import Counter
from pathlib import Path
import random
import re
import sys

from design import panel

HERE = Path(__file__).resolve().parent
REFERENCE = HERE.parent / "language-garden-invariance-seed-v1"
sys.path.append(str(REFERENCE))
from run_study import load_model, summarize, recorder, run

RAW = Path("/workspace/language_garden_repeat_ten_cycles_sessions")


def decode_content(case, reply):
    text = reply.strip()
    task = case["task"]
    exact = text.casefold()
    if task == "count":
        variants = {"one": "1", "two": "2", "1": "1", "2": "2"}
        if exact in variants:
            return variants[exact], True, text
        candidates = ["one", "two", "1", "2"]
    else:
        candidates = case["options"]
        if exact in candidates:
            return exact, True, text
    claim = text.split("\n\n", 1)[0].split("\n", 1)[0].casefold()
    if not re.search(r"\b(?:is|are|occurs?|appears?|written|shows?|contains?)\b", claim):
        return None, False, claim
    if task == "count":
        numbers = re.findall(r'\b(?:(one|two|1|2)\s+times?|(?:appears?|occurs?)\s+(once|twice))\b', claim)
        cited = {variants.get(a, {"once": "1", "twice": "2"}.get(b)) for a, b in numbers}
    else:
        cited = {token for token in candidates if re.search(r"\b" + re.escape(token) + r"\b", claim)}
        if not cited and claim.rstrip(".") in candidates:
            cited = {claim.rstrip(".")}
    return (next(iter(cited)) if len(cited) == 1 else None), False, claim


def score(cases, traces):
    rows = []
    for case, trace in zip(cases, traces, strict=True):
        if case["id"] != trace["case_id"]:
            raise ValueError("Trace belongs to a different prompt")
        reply = trace["reply"]
        picked, exact, excerpt = decode_content(case, reply["text"])
        rows.append({**case, "picked": picked, "content_correct": picked == case["gold"],
                     "exact_correct": exact and picked == case["gold"],
                     "evidence": excerpt, "stop": reply["stop"]})
    repeat = [row for row in rows if row["task"] == "repeat"]
    metrics = {}
    for task in sorted({row["task"] for row in rows}):
        task_rows = [row for row in rows if row["task"] == task]
        metrics[task] = {
            "n": len(task_rows), "content": sum(r["content_correct"] for r in task_rows),
            "exact": sum(r["exact_correct"] for r in task_rows),
            "invalid": sum(r["picked"] is None for r in task_rows),
        }
    return {
        "tasks": metrics, "stops": dict(Counter(row["stop"] for row in rows)),
        "repeat_baselines": {role: sum(r["values"][i] == r["gold"] for r in repeat)
                             for i, role in enumerate(("first", "middle", "last"))},
        "rows": rows,
    }


def prep(number, prior, folder, tokenizer, execute):
    question, cases = panel(number, prior)
    random.Random(3091 + number).shuffle(cases)
    lengths = {}
    for case in cases:
        recorder.SEED = case["text"]
        plan = recorder.assemble(tokenizer, [])
        lengths[case["id"]] = len(plan["input_token_ids"])
    if len(lengths) != len(cases) or max(lengths.values()) > recorder.MAX_INPUT:
        raise ValueError("Preflight input count or length")
    paths = [HERE / path for path in ("design.py", "run_cycles.py", "PROTOCOL.md")]
    paths.extend([REFERENCE / path for path in ("run_study.py", "score.py", "fixtures.py")])
    paths.append(HERE.parent / "language-garden-pilot-v1/CONTRACT.json")
    paths.append(HERE / f"{number - 1:02d}/RESULTS.json" if number > 1
                 else HERE.parent / "language-garden-repeat-readout-v1/REPORT.md")
    pins = {str(path.relative_to(HERE.parent)): run.digest(path) for path in paths}
    inputs = {"question": question, "sha256": pins, "input_lengths": lengths, "cases": cases}
    lock = folder / "INPUTS.json"
    if execute and not lock.exists():
        recorder.append(lock, inputs)
    elif recorder.read(lock) != inputs:
        raise ValueError(f"Stage {number} opening changed")
    return question, cases, lengths


def verify_trace(record, case, tokenizer, length, contract):
    plan = recorder.assemble(tokenizer, [])
    expected = {"turn": 1, "author": "host", "output_reserve": recorder.MAX_OUTPUT, **plan}
    if record["plan"] != expected or len(plan["input_token_ids"]) != length:
        raise ValueError("Archived prompt differs from planned prompt")
    recorder.verify_reply(tokenizer, plan, record["reply"])
    if record["parameters"] != {"tensor_digest_after": contract["tensor_digest"]}:
        raise ValueError("Tensor receipt mismatch")
    stop = record["reply"]["stop"]
    expected_status = "token_limit" if stop == "token_limit" else (
        "operator_pause" if record["reply"]["text"] else "empty_visible_reply"
    )
    if record["status"] != expected_status:
        raise ValueError("Unexpected session state")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("execute", "audit"))
    parser.add_argument("--through", type=int, choices=range(1, 11), default=10)
    args = parser.parse_args()
    execute = args.mode == "execute"
    from transformers import AutoTokenizer

    contract = run.verify_pins(run.DEFAULT_MODEL)
    tokenizer = AutoTokenizer.from_pretrained(
        run.DEFAULT_MODEL, local_files_only=True, trust_remote_code=False
    )
    if execute:
        advance = load_model(contract)
    prior = {}
    for number in range(1, args.through + 1):
        folder = HERE / f"{number:02d}"
        trace_dir = folder / "traces"
        if execute:
            trace_dir.mkdir(parents=True, exist_ok=True)
            sessions = RAW / folder.name
            sessions.mkdir(parents=True, exist_ok=True)
        question, cases, lengths = prep(number, prior, folder, tokenizer, execute)
        traces = []
        for case in cases:
            recorder.SEED = case["text"]
            path = trace_dir / f"{case['id']}.json"
            if execute:
                directory = sessions / case["id"]
                if not directory.exists():
                    recorder.setup(directory)
                    advance(directory, tokenizer)
                    recorder.append(directory / "operator_pause.json", {"after_turn": 1})
                record = summarize(directory, case, tokenizer, lengths, contract)
                if not path.exists():
                    recorder.append(path, record)
                elif recorder.read(path) != record:
                    raise ValueError("Archived response differs from live trace")
            else:
                record = recorder.read(path)
            verify_trace(record, case, tokenizer, lengths[case["id"]], contract)
            traces.append(record)
        if {p.stem for p in trace_dir.glob("*.json")} != set(lengths):
            raise ValueError("Unexpected trace files")
        result = score(cases, traces)
        path = folder / "RESULTS.json"
        if execute and not path.exists():
            recorder.append(path, result)
        elif recorder.read(path) != result:
            raise ValueError("Stored score differs from recomputation")
        prior[number] = result
        print(number, question, {k: v for k, v in result.items() if k != "rows"}, flush=True)


if __name__ == "__main__":
    main()
