"""Offer one detached opening using the pinned pilot runtime."""
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
    operation = parser.parse_args().operation
    contract = json.loads((HERE / "INPUT_CONTRACT.json").read_text())
    for path, expected in contract["sha256"].items():
        if run.digest((HERE / path).resolve()) != expected:
            raise ValueError(f"Opening pin mismatch: {path}")
    original = recorder.SEED
    recorder.SEED = original + "\n\n" + (HERE / "MATERIAL.txt").read_bytes().decode("utf-8")
    session = HERE / "session"
    if operation == "advance":
        # Exclusive creation makes this a single opening even if it ends at EOS.
        recorder.setup(session)
    sys.argv = [sys.argv[0], operation, str(session)]
    run.main()


if __name__ == "__main__":
    main()
