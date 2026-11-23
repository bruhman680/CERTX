"""One explicit operator opportunity per invocation."""
import argparse
import hashlib
import importlib.metadata
import importlib.util
import os
from pathlib import Path
import platform
import sys

from recorder import (MAX_INPUT, MAX_OUTPUT, MAX_TURNS, advance, assemble, read,
                      setup, state, verify_reply)

HERE = Path(__file__).resolve().parent
FRR = HERE.parents[1]
BODY = FRR / "evaluation/minimal-garden-candidate-v1/generation.py"
HELPER = FRR / "evaluation/descriptions-and-rules-v1/runtime_reference.py"
DEFAULT_MODEL = Path("/workspace/cache_backend_models/smollm2-135m")
os.environ.update(HF_HUB_OFFLINE="1", OMP_NUM_THREADS="2", MKL_NUM_THREADS="2",
                  OPENBLAS_NUM_THREADS="1")


def load_source(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def digest(path):
    with path.open("rb") as source:
        return hashlib.file_digest(source, "sha256").hexdigest()


def verify_pins(model_dir):
    contract = read(HERE / "CONTRACT.json")
    for name, expected in contract["source_sha256"].items():
        if digest(FRR / name) != expected:
            raise ValueError(f"Source pin mismatch: {name}")
    for name, expected in contract["asset_sha256"].items():
        if digest(model_dir / name) != expected:
            raise ValueError(f"Model pin mismatch: {name}")
    versions = {p: importlib.metadata.version(p) for p in contract["packages"]}
    if versions != contract["packages"] or platform.python_version() != contract["python"]:
        raise ValueError("Runtime version mismatch")
    if contract["limits"] != [MAX_INPUT, MAX_OUTPUT, MAX_TURNS]:
        raise ValueError("Limit mismatch")
    return contract


def audit(directory, tokenizer):
    status, replies = state(directory)
    for i, reply in enumerate(replies, 1):
        started = read(directory / f"{i:02d}" / "started.json")
        plan = assemble(tokenizer, replies[:i-1])
        if (started != {"turn": i, "author": "host", "output_reserve": MAX_OUTPUT, **plan}
                or len(plan["input_token_ids"]) > MAX_INPUT):
            raise ValueError(f"Input plan mismatch at turn {i}")
        verify_reply(tokenizer, plan, reply)
    next_path = directory / f"{len(replies) + 1:02d}"
    plan = assemble(tokenizer, replies)
    if status == "interrupted_trace_unknown":
        started = read(next_path / "started.json")
        if started != {"turn": len(replies) + 1, "author": "host",
                       "output_reserve": MAX_OUTPUT, **plan}:
            raise ValueError("Unresolved start plan mismatch")
    if status in ("native_marker_in_content", "context_capacity"):
        paused = read(next_path / "pause.json")
        markers = [marker for marker in tokenizer.all_special_tokens
                   if any(marker in m["content"] for m in plan["messages"])]
        reason = "native_marker_in_content" if markers else "context_capacity"
        if (paused != {"reason": reason, "plan": plan, "markers": markers}
                or (not markers and len(plan["input_token_ids"]) <= MAX_INPUT)):
            raise ValueError("Pause plan mismatch")
    return status, replies


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=["advance", "audit"])
    parser.add_argument("directory", type=Path)
    parser.add_argument("--model-dir", type=Path, default=DEFAULT_MODEL)
    args = parser.parse_args()
    contract = verify_pins(args.model_dir)
    from transformers import AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained(args.model_dir, local_files_only=True, trust_remote_code=False)
    if not args.directory.exists() and args.operation == "advance":
        setup(args.directory)
    if not args.directory.is_dir():
        raise ValueError("Session directory must exist")
    status, replies = audit(args.directory, tokenizer)
    expected_turn = len(replies) + 1
    for turn in range(1, expected_turn):
        receipt = args.directory / f"{turn:02d}" / "checked.json"
        if receipt.exists() and read(receipt) != {"tensor_digest_after": contract["tensor_digest"]}:
            raise ValueError(f"Invalid parameter receipt at turn {turn}")
    if args.operation == "advance" and status == "ready":
        import torch
        from transformers import AutoModelForCausalLM
        body = load_source("language_generation", BODY)
        runtime = load_source("language_runtime_reference", HELPER)
        torch.set_num_threads(2)
        model = AutoModelForCausalLM.from_pretrained(
            args.model_dir, local_files_only=True, trust_remote_code=False,
            use_safetensors=True, dtype=torch.float32, attn_implementation="eager")
        model.requires_grad_(False).eval()
        guard = runtime.Guard(5153960755, args.directory / "RESOURCE.jsonl")
        guard.read("loaded")
        expected = contract["tensor_digest"]
        if runtime.parameter_digest(model, False) != expected:
            raise ValueError("Loaded parameter mismatch")

        def generate(messages, run_id):
            return body.generate(model, tokenizer, messages, guard, run_id)

        def verify_model():
            actual = runtime.parameter_digest(model, False)
            if actual != expected:
                raise ValueError("Post-call parameter mismatch")
            return {"tensor_digest_after": actual}

        advance(args.directory, tokenizer, generate, verify_model, expected_turn)
        status, replies = audit(args.directory, tokenizer)
    print(f"{len(replies)} returned replies. Session status {status}.")


if __name__ == "__main__":
    main()
