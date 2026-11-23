"""Score returned text and verify each opening against its declared prompt."""
import json
from pathlib import Path
import re
import sys

cycle = Path(sys.argv[1])
data = json.loads((cycle / "CASES.json").read_text())
pilot = Path("../language-garden-pilot-v1")
sys.path.insert(0, str(pilot.resolve()))
from recorder import append, read, SEED, SYSTEM

rows = []
for name, case in data["cases"].items():
    case_dir = cycle / name
    assert sorted(p.name for p in case_dir.iterdir() if p.is_dir()) == ["01"]
    raw = read(case_dir / "01/returned.json")
    assert raw["messages"] == [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": SEED + "\n\n" + case["row"] + "\n\n" + data["question"]},
    ]
    text = raw["text"].strip().casefold()
    if text.endswith("."):
        text = text[:-1]
    valid = re.fullmatch(data["label_regex"], text) is not None
    rows.append(dict(case=name, row=case["row"], expected=case["expected"], reply=raw["text"],
                     parsed=text if valid else None, correct=valid and text == case["expected"],
                     input_tokens=len(raw["input_token_ids"]), output_tokens=len(raw["generated_token_ids"]),
                     stop=raw["stop"]))
    append(case_dir / "operator_pause.json", {"author": "host", "reason": "one-opening case complete"})
with (cycle / "RESULTS.json").open("x") as stream:
    json.dump(dict(calls=len(rows), correct=sum(r["correct"] for r in rows),
                   valid=sum(r["parsed"] is not None for r in rows), rows=rows), stream, indent=2)
    stream.write("\n")
for row in rows:
    print(json.dumps({**row, "reply": row["reply"][:300]}))
