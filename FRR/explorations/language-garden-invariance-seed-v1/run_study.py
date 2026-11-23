"""Prepare, execute, or audit the detached endpoint and seed panels."""
import argparse
import json
from pathlib import Path
import sys

from fixtures import panels, SEEDS
from score import score

HERE = Path(__file__).resolve().parent
PILOT = HERE.parent / "language-garden-pilot-v1"
sys.path.insert(0, str(PILOT))
import recorder
import run

BASE = recorder.SEED
RAW = Path("/workspace/language_garden_invariance_seed_sessions")
PINNED = ("PROTOCOL.md", "fixtures.py", "score.py", "run_study.py",
          "INPUTS.json", "TOKEN_LENGTHS.json", "../language-garden-pilot-v1/CONTRACT.json",
          "../language-garden-symbol-three-cycles-v1/REPORT.md")


def compose(case):
    seed = SEEDS.get(case["condition"])
    parts = [BASE, case["text"]]
    if seed:
        parts.insert(1, seed)
    return "\n\n".join(parts)


def pins():
    return {name: run.digest(HERE / name) for name in PINNED}


def write(name, value):
    recorder.append(HERE / name, value)


def read(name):
    return recorder.read(HERE / name)


def prepare(tokenizer):
    inputs = panels()
    lengths = {}
    for stage, cases in inputs.items():
        assert len({case["id"] for case in cases}) == len(cases)
        lengths[stage] = {}
        for case in cases:
            recorder.SEED = compose(case)
            plan = recorder.assemble(tokenizer, [])
            lengths[stage][case["id"]] = len(plan["input_token_ids"])
    delta = {
        lengths["seed"][case["id"]] -
        lengths["seed"][f"{case['item']}-invariance"]
        for case in inputs["seed"] if case["condition"] == "attention"
    }
    if delta != {0}:
        raise ValueError(f"Control length minus invariance length: {sorted(delta)}")
    write("INPUTS.json", inputs)
    write("TOKEN_LENGTHS.json", lengths)
    write("INPUT_CONTRACT.json", {"sha256": pins()})


def load_model(contract):
    import torch
    from transformers import AutoModelForCausalLM
    torch.set_num_threads(2)
    body = run.load_source("language_generation", run.BODY)
    runtime = run.load_source("language_runtime_reference", run.HELPER)
    model = AutoModelForCausalLM.from_pretrained(
        run.DEFAULT_MODEL, local_files_only=True, trust_remote_code=False,
        use_safetensors=True, dtype=torch.float32, attn_implementation="eager",
    )
    model.requires_grad_(False).eval()

    def verify_model():
        actual = runtime.parameter_digest(model, False)
        if actual != contract["tensor_digest"]:
            raise ValueError("Parameter mismatch")
        return {"tensor_digest_after": actual}

    verify_model()

    def advance(directory, tokenizer):
        guard = runtime.Guard(5153960755, directory / "RESOURCE.jsonl")
        guard.read("loaded")
        recorder.advance(
            directory, tokenizer,
            lambda messages, run_id: body.generate(model, tokenizer, messages, guard, run_id),
            verify_model, expected_turn=1,
        )

    return advance


def summarize(directory, case, tokenizer, lengths, contract):
    status, replies = run.audit(directory, tokenizer)
    if len(replies) != 1:
        raise ValueError(f"Expected one returned opening, got {status}: {case['id']}")
    received = replies[0]
    expected_status = "token_limit" if received["stop"] == "token_limit" else (
        "operator_pause" if received["text"] else "empty_visible_reply"
    )
    if status != expected_status or not (directory / "operator_pause.json").is_file():
        raise ValueError(f"Session was not closed: {case['id']}, {status}")
    receipt = recorder.read(directory / "01/checked.json")
    if receipt != {"tensor_digest_after": contract["tensor_digest"]}:
        raise ValueError(f"Parameter receipt mismatch: {case['id']}")
    plan = recorder.read(directory / "01/started.json")
    if len(plan["input_token_ids"]) != lengths[case["id"]]:
        raise ValueError(f"Preflight length mismatch: {case['id']}")
    return {"case_id": case["id"], "status": status, "plan": plan,
            "reply": received, "parameters": receipt}


def stage_run(stage, tokenizer, contract, execute):
    if read("INPUT_CONTRACT.json") != {"sha256": pins()}:
        raise ValueError("Frozen study checksum mismatch")
    cases = read("INPUTS.json")[stage]
    lengths = read("TOKEN_LENGTHS.json")[stage]
    session_root = RAW / stage
    if execute:
        RAW.mkdir(exist_ok=True)
        session_root.mkdir(exist_ok=True)
        (HERE / stage).mkdir(exist_ok=True)
        advance = load_model(contract)
    replies = []
    for case in cases:
        recorder.SEED = compose(case)
        directory = session_root / case["id"]
        output = HERE / stage / f"{case['id']}.json"
        if execute and not directory.exists():
            recorder.setup(directory)
            advance(directory, tokenizer)
            recorder.append(directory / "operator_pause.json", {"after_turn": 1})
        summary = summarize(directory, case, tokenizer, lengths, contract)
        if execute and not output.exists():
            recorder.append(output, summary)
            print(f"{case['id']}: {summary['status']}", flush=True)
        elif recorder.read(output) != summary:
            raise ValueError(f"Archived reply differs from runtime: {case['id']}")
        replies.append(summary)
    result_path = HERE / f"{stage.upper()}_RESULTS.json"
    measured = score(cases, replies)
    if execute and not result_path.exists():
        recorder.append(result_path, measured)
    elif recorder.read(result_path) != measured:
        raise ValueError("Stored scores differ from recomputation")
    print(f"{stage}: {len(replies)} recorded and audited")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=("prepare", "execute", "audit"))
    parser.add_argument("stage", choices=("endpoint", "seed"), nargs="?")
    args = parser.parse_args()
    if (args.operation == "prepare") == (args.stage is not None):
        parser.error("Supply a stage only for execute or audit")
    contract = run.verify_pins(run.DEFAULT_MODEL)
    from transformers import AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained(
        run.DEFAULT_MODEL, local_files_only=True, trust_remote_code=False
    )
    if args.operation == "prepare":
        prepare(tokenizer)
    else:
        stage_run(args.stage, tokenizer, contract, args.operation == "execute")


if __name__ == "__main__":
    main()
