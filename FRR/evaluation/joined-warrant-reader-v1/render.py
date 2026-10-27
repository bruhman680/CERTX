#!/usr/bin/env python3
"""Render prospective one-turn packets after root approval; never dispatch readers."""
import argparse
import hashlib
import json
from pathlib import Path
import random

ARMS = {
    "ordinary": "Read the task and evidence carefully. Identify the requested decision, perform relevant calculations, and distinguish established facts from uncertainty. Check that your answer addresses the stated scope and acceptance rule. Clearly explain your decision using the supplied records, state any consequential limitations, and give a useful next check when needed.",
    "joined": "Read the task and evidence carefully. Optionally check joined warrants: identify required premises, combine applicable records using exact keys, and separate supplied premises from absent or conflicting ones. Check whether evidence covers the full acceptance target. Explain your decision, state consequential limitations, and give a useful next check when needed.",
}
assert [len(a.split()) for a in ARMS.values()] == [50, 50]
PREAMBLE = """Use only this delivered fictional task packet. The one designated read of this file is the only permitted tool call. After reading, do not use tools, contact peers, inspect other files, or write files. Return your answer directly as one JSON object.

Treat explicitly accepted premises as stipulated mathematical facts for this fictional exercise. Assignment-record authority follows the stated rule. RELEASE means acceptance holds in every state compatible with the accepted evidence. HOLD means acceptance fails in every compatible state. UNRESOLVED means both an accepting and a failing state remain compatible. No further evidence is available during this turn.

Return exactly these fields: action (RELEASE, HOLD, or UNRESOLVED); bound_or_value (a JSON object naming the quantity, value or bound, and unit); satisfied_premises (an array of strings); missing_or_conflicting_premises (an array of strings); evidence_ids (an array of supplied evidence IDs); next_check (a string naming a useful check and its scope, or saying none is needed); rationale (a string of at most 180 whitespace-separated words)."""


def render(case, arm):
    records = "\n".join(f"{e['id']}: {e['text']}" for e in case["evidence"])
    return f"{PREAMBLE}\n\n{ARMS[arm]}\n\nTask: {case['task']}\n\nEvidence:\n{records}\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--seed", type=int, default=20261027)
    parser.add_argument("--root-approved", action="store_true", help="Root confirms prospective review and freeze authorization have occurred.")
    args = parser.parse_args()
    if not args.root_approved:
        parser.error("Rendering is deferred until prospective case/key review and explicit root approval; pass --root-approved only then.")
    source = Path(__file__).with_name("cases.json")
    data = json.loads(source.read_text())
    cases = data["cases"]
    assert len(cases) == 8 and len({c["id"] for c in cases}) == 8
    assignments = [(case, arm) for case in cases for arm in ARMS]
    random.Random(args.seed).shuffle(assignments)
    if args.output.exists():
        parser.error("Output directory already exists; choose a new path to preserve originals.")
    prompts = args.output / "prompts"
    prompts.mkdir(parents=True)
    manifest = {"seed": args.seed, "arm_whitespace_words": {k: len(v.split()) for k, v in ARMS.items()}, "cases_sha256": hashlib.sha256(source.read_bytes()).hexdigest(), "renderer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), "assignments": []}
    for i, (case, arm) in enumerate(assignments, 1):
        name = f"R{i:02d}.txt"
        packet = render(case, arm)
        (prompts / name).write_text(packet)
        manifest["assignments"].append({"reader": f"R{i:02d}", "case_id": case["id"], "arm": arm, "prompt": f"prompts/{name}", "sha256": hashlib.sha256(packet.encode()).hexdigest()})
    (args.output / "assignment.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Rendered {len(assignments)} prompts into {prompts}; no readers dispatched.")


if __name__ == "__main__":
    main()
