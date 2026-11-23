"""Run or audit the one-word paired replay using the earlier pinned scorer."""
import argparse
from collections import Counter
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent / "language-garden-repeat-ten-cycles-v1"
sys.path.insert(0, str(PARENT))
from run_cycles import load_model, recorder, run, score, summarize, verify_trace

STAGE = PARENT / "10"
RAW = Path("/workspace/language_garden_word_wording_sessions")
ORIGINAL = "Which symbol appears twice in this row?"
NEW = "Which word appears twice in this row?"


def read(path):
    return recorder.read(path)


def prep(tokenizer, contract):
    base = read(STAGE / "INPUTS.json")
    manifest = read(PARENT / "MANIFEST.json")["sha256"]
    paired = []
    pins = [HERE / "PROTOCOL.md", HERE / "run_word_probe.py", PARENT / "MANIFEST.json",
            PARENT / "run_cycles.py", STAGE / "INPUTS.json", STAGE / "RESULTS.json"]
    for case in base["cases"]:
        path = STAGE / "traces" / f"{case['id']}.json"
        pins.append(path)
        trace = read(path)
        if trace["case_id"] != case["id"]:
            raise ValueError("Wrong reference trace")
        recorder.SEED = case["text"]
        verify_trace(trace, case, tokenizer, base["input_lengths"][case["id"]], contract)
        if case["text"].count(ORIGINAL) != 1:
            raise ValueError("Expected exactly one occurrence of the original question")
        text = case["text"].replace(ORIGINAL, NEW)
        updated = {**case, "id": f"{case['id']}-word", "text": text}
        recorder.SEED = text
        length = len(recorder.assemble(tokenizer, [])["input_token_ids"])
        paired.append({"original_case": case, "case": updated,
                       "original_tokens": base["input_lengths"][case["id"]],
                       "word_tokens": length})
    for path in pins:
        if path.is_relative_to(PARENT) and path.name != "MANIFEST.json":
            if run.digest(path) != manifest[str(path.relative_to(PARENT))]:
                raise ValueError("Archived reference changed")
    return {
        "sha256": {str(path.relative_to(HERE.parent)): run.digest(path) for path in pins},
        "paired": paired,
    }


def compare(original, wording, paired):
    by_word = {r["id"]: r for r in wording["rows"]}
    by_symbol = {r["id"]: r for r in original["rows"]}
    rows = []
    for pair in paired:
        a, b = by_symbol[pair["original_case"]["id"]], by_word[pair["case"]["id"]]
        rows.append({
            "key": a["key"], "shape": a["shape"], "values": a["values"], "gold": a["gold"],
            "symbol": a["picked"], "word": b["picked"],
            "symbol_correct": a["content_correct"], "word_correct": b["content_correct"],
            "symbol_evidence": a["evidence"], "word_evidence": b["evidence"],
            "symbol_tokens": pair["original_tokens"], "word_tokens": pair["word_tokens"],
        })
    families = []
    for _group in sorted({tuple(sorted(set(r["values"]))) for r in rows}):
        shapes = {r["shape"]: r for r in rows if tuple(sorted(set(r["values"]))) == _group}
        assert set(shapes) == {"AAB", "ABA", "ABB"}
        for start in ("AAB", "ABA"):
            assert shapes[start]["gold"] != shapes["ABB"]["gold"]
            families.append({
                "family": list(_group), "shapes": [start, "ABB"],
                **{arm: all(shapes[shape][f"{arm}_correct"] for shape in (start, "ABB"))
                   for arm in ("symbol", "word")},
            })
    return {
        "rows": rows, "family_pairs_where_answer_switches": families,
        "correct_switch_pairs": {arm: sum(f[arm] for f in families) for arm in ("symbol", "word")},
        "gains": [r["key"] for r in rows if r["word_correct"] and not r["symbol_correct"]],
        "losses": [r["key"] for r in rows if r["symbol_correct"] and not r["word_correct"]],
        "in_row_answers": {arm: sum(r[arm] is not None for r in rows) for arm in ("symbol", "word")},
        "correct": {arm: sum(r[f"{arm}_correct"] for r in rows) for arm in ("symbol", "word")},
        "input_length_deltas": dict(Counter(str(r["word_tokens"] - r["symbol_tokens"]) for r in rows)),
        "word_results": wording["tasks"], "word_stops": wording["stops"],
        "fixed_position_baselines": wording["repeat_baselines"],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("execute", "audit"))
    mode = parser.parse_args().mode
    from transformers import AutoTokenizer

    contract = run.verify_pins(run.DEFAULT_MODEL)
    tokenizer = AutoTokenizer.from_pretrained(
        run.DEFAULT_MODEL, local_files_only=True, trust_remote_code=False
    )
    pinned = prep(tokenizer, contract)
    lock = HERE / "INPUTS.json"
    if mode == "execute" and not lock.exists():
        recorder.append(lock, pinned)
    elif read(lock) != pinned:
        raise ValueError("Pinned prompts differ")
    traces = HERE / "traces"
    if mode == "execute":
        RAW.mkdir(exist_ok=True)
        traces.mkdir(exist_ok=True)
        advance = load_model(contract)
    cases = []
    replies = []
    prior_cases = []
    prior_traces = []
    for item in pinned["paired"]:
        case = item["case"]
        recorder.SEED = case["text"]
        archived = traces / f"{case['id']}.json"
        if mode == "execute":
            directory = RAW / case["id"]
            if not directory.exists():
                recorder.setup(directory)
                advance(directory, tokenizer)
                recorder.append(directory / "operator_pause.json", {"after_turn": 1})
            reply = summarize(directory, case, tokenizer, {case["id"]: item["word_tokens"]}, contract)
            if not archived.exists():
                recorder.append(archived, reply)
                print(case["id"], reply["status"], flush=True)
            elif read(archived) != reply:
                raise ValueError("Archived response differs from session")
        else:
            reply = read(archived)
        verify_trace(reply, case, tokenizer, item["word_tokens"], contract)
        cases.append(case)
        replies.append(reply)
        prior_case = item["original_case"]
        prior_cases.append(prior_case)
        prior_traces.append(read(STAGE / "traces" / f"{prior_case['id']}.json"))
    if {p.stem for p in traces.glob("*.json")} != {c["id"] for c in cases}:
        raise ValueError("Unexpected trace set")
    original = score(prior_cases, prior_traces)
    if original != read(STAGE / "RESULTS.json"):
        raise ValueError("Archived reference score differs from recomputation")
    comparison = compare(original, score(cases, replies), pinned["paired"])
    path = HERE / "RESULTS.json"
    if mode == "execute" and not path.exists():
        recorder.append(path, comparison)
    elif read(path) != comparison:
        raise ValueError("Scores differ from published comparison")
    print({k: v for k, v in comparison.items() if k not in ("rows", "family_pairs_where_answer_switches")})


if __name__ == "__main__":
    main()
