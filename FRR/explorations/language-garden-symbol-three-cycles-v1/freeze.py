"""Bind each cycle before inference, including prior results where applicable."""
import hashlib
import json
from pathlib import Path
import sys

cycle = Path(sys.argv[1])
paths = ["CASES.json", "PROTOCOL.md", "../run_cycle.py", "../freeze.py",
         "../../language-garden-pilot-v1/CONTRACT.json"]
if cycle.name != "cycle1":
    paths.append(f"../cycle{int(cycle.name[-1]) - 1}/RESULTS.json")
else:
    paths.append("../../language-garden-endpoint-match-v1/RESULTS.json")
pins = {p: hashlib.sha256((cycle / p).read_bytes()).hexdigest() for p in paths}
with (cycle / "INPUT_CONTRACT.json").open("x") as stream:
    json.dump({"sha256": pins}, stream, indent=2)
    stream.write("\n")
