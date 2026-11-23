"""Offer one detached case using the pinned pilot runtime."""
import argparse
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
PILOT = HERE.parent / "language-garden-pilot-v1"
sys.path.insert(0, str(PILOT))
import recorder
import run


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=["advance", "audit"])
    parser.add_argument("cycle", choices=["cycle1", "cycle2", "cycle3"])
    cycle = HERE / parser.parse_known_args()[0].cycle
    data = json.loads((cycle / "CASES.json").read_text())
    parser.add_argument("case", choices=list(data["cases"]))
    args = parser.parse_args()
    operation = args.operation
    contract = json.loads((cycle / "INPUT_CONTRACT.json").read_text())
    for path, expected in contract["sha256"].items():
        if run.digest((cycle / path).resolve()) != expected:
            raise ValueError(f"Opening pin mismatch: {path}")
    case = data["cases"][args.case]
    recorder.SEED += "\n\n" + case["row"] + "\n\n" + data["question"]
    session = cycle / args.case
    if operation == "advance":
        # Exclusive creation makes this a single opening even if it ends at EOS.
        recorder.setup(session)
    sys.argv = [sys.argv[0], operation, str(session)]
    run.main()


if __name__ == "__main__":
    main()
