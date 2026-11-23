"""Run a frozen paired panel using the archived symbol pilot runtime."""
from collections import Counter, defaultdict
import argparse
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
REFERENCE = HERE.parent / "language-garden-invariance-seed-v1"
sys.path.insert(0, str(REFERENCE))
from run_study import BASE, load_model, summarize, recorder, run

RAW = Path("/workspace/language_garden_repeat_readout_sessions")


def input_text(case):
    if case["seed_style"] == "native":
        return case["text"]
    if case["seed_style"] != "garden":
        raise ValueError(f"Unknown seed style: {case['seed_style']}")
    return BASE + "\n\n" + case["text"]


def contract_for(folder):
    files = [
        folder / "CASES.json", HERE / "make_panel.py", HERE / "run_panel.py",
        REFERENCE / "run_study.py", REFERENCE / "fixtures.py",
        REFERENCE / "score.py", HERE.parent / "language-garden-pilot-v1/CONTRACT.json",
    ]
    builder = HERE / f"make_{folder.name}.py"
    if builder.is_file():
        files.append(builder)
    stage = int(folder.name)
    files.append(HERE / f"{stage - 1:02d}/RESULTS.json" if stage > 1
                 else REFERENCE / "REPORT.md")
    return {str(path.relative_to(HERE.parent)): run.digest(path) for path in files}


def audit_record(record, case, tokenizer, length, contract):
    if record["case_id"] != case["id"]:
        raise ValueError("Case identity changed")
    plan = recorder.assemble(tokenizer, [])
    expected = {"turn": 1, "author": "host", "output_reserve": recorder.MAX_OUTPUT, **plan}
    if record["plan"] != expected or len(plan["input_token_ids"]) != length:
        raise ValueError("Plan differs from frozen input")
    reply = record["reply"]
    recorder.verify_reply(tokenizer, plan, reply)
    if record["parameters"] != {"tensor_digest_after": contract["tensor_digest"]}:
        raise ValueError("Wrong tensor receipt")
    status = "token_limit" if reply["stop"] == "token_limit" else (
        "operator_pause" if reply["text"] else "empty_visible_reply"
    )
    if record["status"] != status:
        raise ValueError("Wrong terminal state")


def score(cases, records):
    pairs = defaultdict(list)
    rows = []
    for case, record in zip(cases, records, strict=True):
        raw = record["reply"]["text"].strip().upper()
        answer = raw if re.fullmatch("A|B", raw) else None
        row = {
            "id": case["id"], "item": case["item"], "order": case["order"],
            "seed_style": case["seed_style"], "gold": case["gold"], "answer": answer,
            "correct": answer == case["gold"], "stop": record["reply"]["stop"],
        }
        pairs[case["item"]].append(row)
        rows.append(row)
    for pair in pairs.values():
        assert {r["gold"] for r in pair} == {"A", "B"} and len(pair) == 2
    return {
        "calls": len(rows),
        "correct": sum(r["correct"] for r in rows),
        "answers": dict(Counter(r["answer"] or "invalid" for r in rows)),
        "stops": dict(Counter(r["stop"] for r in rows)),
        "correct_by_order": {order: sum(r["correct"] for r in rows if r["order"] == order)
                             for order in ("forward", "reverse")},
        "pairs": len(pairs),
        "both_orders_correct": [i for i, pair in sorted(pairs.items())
                                if all(r["correct"] for r in pair)],
        "rows": rows,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("freeze", "execute", "audit"))
    parser.add_argument("stage", choices=("01", "02", "03", "04"))
    args = parser.parse_args()
    folder = HERE / args.stage
    cases = recorder.read(folder / "CASES.json")["cases"]
    contract = run.verify_pins(run.DEFAULT_MODEL)

    from transformers import AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained(
        run.DEFAULT_MODEL, local_files_only=True, trust_remote_code=False
    )
    lengths = {}
    for case in cases:
        recorder.SEED = input_text(case)
        plan = recorder.assemble(tokenizer, [])
        if len(plan["input_token_ids"]) > recorder.MAX_INPUT:
            raise ValueError("Preflight context overflow")
        lengths[case["id"]] = len(plan["input_token_ids"])
    if len(lengths) != len(cases):
        raise ValueError("Duplicate cases")
    pinned = {"sha256": contract_for(folder), "input_token_lengths": lengths}
    lock = folder / "INPUT_CONTRACT.json"
    if args.mode == "freeze":
        recorder.append(lock, pinned)
        return
    if recorder.read(lock) != pinned:
        raise ValueError("Input contract differs from frozen panel")
    trace_dir = folder / "traces"
    if args.mode == "execute":
        trace_dir.mkdir(exist_ok=True)
        sessions = RAW / args.stage
        sessions.mkdir(parents=True, exist_ok=True)
        advance = load_model(contract)
    records = []
    for case in cases:
        recorder.SEED = input_text(case)
        archived = trace_dir / f"{case['id']}.json"
        if args.mode == "execute":
            directory = sessions / case["id"]
            if not directory.exists():
                recorder.setup(directory)
                advance(directory, tokenizer)
                recorder.append(directory / "operator_pause.json", {"after_turn": 1})
            record = summarize(directory, case, tokenizer, lengths, contract)
            if not archived.exists():
                recorder.append(archived, record)
                print(f"{args.stage} {case['id']}: {record['status']}", flush=True)
            elif recorder.read(archived) != record:
                raise ValueError("Local session and archive differ")
        else:
            record = recorder.read(archived)
        audit_record(record, case, tokenizer, lengths[case["id"]], contract)
        records.append(record)
    if {p.stem for p in trace_dir.glob("*.json")} != {c["id"] for c in cases}:
        raise ValueError("Trace file set differs from cases")
    result_path = folder / "RESULTS.json"
    result = score(cases, records)
    if args.mode == "execute" and not result_path.exists():
        recorder.append(result_path, result)
    elif recorder.read(result_path) != result:
        raise ValueError("Score recomputation differs")
    print(json.dumps({k: v for k, v in result.items() if k != "rows"}))


if __name__ == "__main__":
    main()
