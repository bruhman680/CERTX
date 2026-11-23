"""Replay the frozen first prompts and compare only the bare A and B next tokens."""
import argparse
from collections import Counter, defaultdict
from pathlib import Path

from run_panel import HERE, input_text, recorder, run


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("freeze", "execute", "audit"))
    mode = parser.parse_args().mode
    first = HERE / "01"
    stage = HERE / "02"
    cases = recorder.read(first / "CASES.json")["cases"]
    files = [Path(__file__), HERE / "run_panel.py", stage / "PROTOCOL.md",
             first / "CASES.json", first / "INPUT_CONTRACT.json", first / "RESULTS.json"]
    files.extend(first / "traces" / f"{c['id']}.json" for c in cases)
    pins = {str(path.relative_to(HERE)): run.digest(path) for path in files}
    lock = stage / "INPUT_CONTRACT.json"
    if mode == "freeze":
        recorder.append(lock, {"sha256": pins})
        return
    if recorder.read(lock) != {"sha256": pins}:
        raise ValueError("Rank replay input changed")
    contract = run.verify_pins(run.DEFAULT_MODEL)

    from transformers import AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(
        run.DEFAULT_MODEL, local_files_only=True, trust_remote_code=False
    )
    labels = {letter: tokenizer.encode(letter, add_special_tokens=False) for letter in ("A", "B")}
    if not all(len(ids) == 1 and tokenizer.decode(ids) == letter for letter, ids in labels.items()):
        raise ValueError("A and B must each have one distinct exact token")
    labels = {letter: ids[0] for letter, ids in labels.items()}
    if len(set(labels.values())) != 2:
        raise ValueError("Choice tokens collide")
    records_path = stage / "SCORES.json"
    if mode == "execute":
        if records_path.exists():
            raise FileExistsError(records_path)
        import torch
        from transformers import AutoModelForCausalLM

        torch.set_num_threads(2)
        runtime = run.load_source("rank_reference", run.HELPER)
        model = AutoModelForCausalLM.from_pretrained(
            run.DEFAULT_MODEL, local_files_only=True, trust_remote_code=False,
            use_safetensors=True, dtype=torch.float32, attn_implementation="eager",
        )
        model.requires_grad_(False).eval()
        if runtime.parameter_digest(model, False) != contract["tensor_digest"]:
            raise ValueError("Wrong input weights")
        records = []
        with torch.inference_mode():
            for case in cases:
                archived = recorder.read(first / "traces" / f"{case['id']}.json")
                x = torch.tensor([archived["plan"]["input_token_ids"]])
                logits = model(input_ids=x, attention_mask=torch.ones_like(x),
                               use_cache=True, logits_to_keep=1).logits[0, -1]
                scores = logits.log_softmax(dim=-1)
                records.append({
                    "case": case["id"],
                    "log_probabilities": {l: float(scores[t]) for l, t in labels.items()},
                    "unrestricted_top_id": int(logits.argmax()),
                })
        digest = runtime.parameter_digest(model, False)
        if digest != contract["tensor_digest"]:
            raise ValueError("Weights changed during replay")
        payload = {
            "choice_tokens": labels, "tensor_digest_after": digest, "records": records,
        }
        recorder.append(records_path, payload)
    else:
        payload = recorder.read(records_path)
    if payload["choice_tokens"] != labels or payload["tensor_digest_after"] != contract["tensor_digest"]:
        raise ValueError("Replay receipt differs")
    result = evaluate(cases, payload["records"], first, tokenizer)
    result_path = stage / "RESULTS.json"
    if mode == "execute":
        recorder.append(result_path, result)
    elif recorder.read(result_path) != result:
        raise ValueError("Replay summary differs")
    print(result)


def evaluate(cases, records, first, tokenizer):
    rows = []
    pairs = defaultdict(list)
    for case, record in zip(cases, records, strict=True):
        if case["id"] != record["case"]:
            raise ValueError("Replay case mismatch")
        archived = recorder.read(first / "traces" / f"{case['id']}.json")
        recorder.SEED = input_text(case)
        plan = recorder.assemble(tokenizer, [])
        if plan["input_token_ids"] != archived["plan"]["input_token_ids"]:
            raise ValueError("Replay prompt differs")
        recorder.verify_reply(tokenizer, plan, archived["reply"])
        if archived["reply"]["generated_token_ids"][0] != record["unrestricted_top_id"]:
            raise ValueError("Replay top token differs from archived opening token")
        scores = record["log_probabilities"]
        if set(scores) != {"A", "B"}:
            raise ValueError("Wrong score labels")
        gap = scores["A"] - scores["B"]
        picked = "A" if gap > 0 else "B" if gap < 0 else None
        row = {"case": case["id"], "gold": case["gold"], "picked": picked,
               "log_probability_A_minus_B": gap, "correct": case["gold"] == picked}
        pairs[case["item"]].append(row)
        rows.append(row)
    return {
        "replayed": len(rows), "correct": sum(r["correct"] for r in rows),
        "picked": dict(Counter(r["picked"] or "tie" for r in rows)),
        "both_orders_correct": [i for i, duo in sorted(pairs.items())
                                if all(r["correct"] for r in duo)],
        "pairs": len(pairs), "rows": rows,
    }


if __name__ == "__main__":
    main()
