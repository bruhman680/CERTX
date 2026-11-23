"""Freeze, record and audit short direct-answer prompts."""
import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

from run_panel import HERE, RAW, audit_record, input_text, load_model, recorder, run, summarize


def score_direct(cases, records):
    groups = defaultdict(list)
    for case, record in zip(cases, records, strict=True):
        row = {
            "id": case["id"], "item": case["item"], "relation": case["relation"],
            "prompt": case["prompt"], "gold": case["gold"],
            "answer": record["reply"]["text"].strip(),
            "stop": record["reply"]["stop"],
        }
        row["correct"] = row["answer"].casefold() == row["gold"].casefold()
        groups[case["prompt"]].append(row)
    return {
        prompt: {
            "calls": len(rows),
            "correct": sum(r["correct"] for r in rows),
            "stops": dict(Counter(r["stop"] for r in rows)),
            "rows": rows,
        }
        for prompt, rows in groups.items()
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("freeze", "execute", "audit"))
    mode = parser.parse_args().mode
    folder = HERE / "04"
    cases = recorder.read(folder / "CASES.json")["cases"]
    files = [Path(__file__), HERE / "run_panel.py", HERE / "make_04.py",
             HERE / "03/RESULTS.json", folder / "CASES.json",
             HERE.parent / "language-garden-pilot-v1/CONTRACT.json"]
    contract = run.verify_pins(run.DEFAULT_MODEL)
    from transformers import AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(
        run.DEFAULT_MODEL, local_files_only=True, trust_remote_code=False
    )
    lengths = {}
    for case in cases:
        recorder.SEED = input_text(case)
        lengths[case["id"]] = len(recorder.assemble(tokenizer, [])["input_token_ids"])
    if len(lengths) != len(cases) or max(lengths.values()) > recorder.MAX_INPUT:
        raise ValueError("Unexpected input set")
    frozen = {
        "sha256": {str(path.relative_to(HERE.parent)): run.digest(path) for path in files},
        "input_token_lengths": lengths,
    }
    lock = folder / "INPUT_CONTRACT.json"
    if mode == "freeze":
        recorder.append(lock, frozen)
        return
    if recorder.read(lock) != frozen:
        raise ValueError("Frozen input mismatch")
    trace_dir = folder / "traces"
    if mode == "execute":
        trace_dir.mkdir(exist_ok=True)
        sessions = RAW / "04"
        sessions.mkdir(parents=True, exist_ok=True)
        advance = load_model(contract)
    records = []
    for case in cases:
        recorder.SEED = input_text(case)
        path = trace_dir / f"{case['id']}.json"
        if mode == "execute":
            directory = sessions / case["id"]
            if not directory.exists():
                recorder.setup(directory)
                advance(directory, tokenizer)
                recorder.append(directory / "operator_pause.json", {"after_turn": 1})
            record = summarize(directory, case, tokenizer, lengths, contract)
            if not path.exists():
                recorder.append(path, record)
                print(f"04 {case['id']}: {record['status']}", flush=True)
            elif recorder.read(path) != record:
                raise ValueError("Archived reply differs from local session")
        else:
            record = recorder.read(path)
        audit_record(record, case, tokenizer, lengths[case["id"]], contract)
        records.append(record)
    if {p.stem for p in trace_dir.glob("*.json")} != set(lengths):
        raise ValueError("Trace file set differs from cases")
    result = score_direct(cases, records)
    path = folder / "RESULTS.json"
    if mode == "execute" and not path.exists():
        recorder.append(path, result)
    elif recorder.read(path) != result:
        raise ValueError("Score recomputation differs")
    print(json.dumps({k: {key: v for key, v in entry.items() if key != "rows"}
                      for k, entry in result.items()}))


if __name__ == "__main__":
    main()
