"""Score the frozen cases by exact normalized reply."""
from collections import Counter, defaultdict
import json
from pathlib import Path
import re
import sys


def score(cases, replies):
    groups = defaultdict(list)
    items = defaultdict(dict)
    for case, reply in zip(cases, replies, strict=True):
        assert case["id"] == reply["case_id"]
        text = reply["reply"]["text"].strip().casefold()
        answer = text if re.fullmatch("yes|no", text) else None
        row = {
            **{key: case[key] for key in ("id", "panel", "condition", "pair", "item", "gold")},
            "answer": answer,
            "correct": answer == case["gold"],
            "stop": reply["reply"]["stop"],
            "input_tokens": len(reply["plan"]["input_token_ids"]),
            "output_tokens": len(reply["reply"]["generated_token_ids"]),
        }
        groups[case["panel"], case["condition"]].append(row)
        items[case["panel"], case["item"]][case["condition"]] = row
    summary = []
    for (panel, condition), rows in sorted(groups.items()):
        pairs = defaultdict(list)
        for row in rows:
            pairs[row["pair"]].append(row)
        assert all({r["gold"] for r in pair} == {"yes", "no"} for pair in pairs.values())
        summary.append({
            "panel": panel,
            "condition": condition,
            "total": len(rows),
            "correct": sum(r["correct"] for r in rows),
            "correct_by_gold": {gold: sum(r["correct"] for r in rows if r["gold"] == gold)
                                for gold in ("yes", "no")},
            "answers": dict(Counter(r["answer"] or "invalid" for r in rows)),
            "stops": dict(Counter(r["stop"] for r in rows)),
            "input_token_lengths": sorted({r["input_tokens"] for r in rows}),
            "pairs_total": len(pairs),
            "pairs_correct": sum(all(r["correct"] for r in pair) for pair in pairs.values()),
        })
    changes = []
    for panel, old, new in (
        ("endpoints", "three", "two"),
        ("codes", "base", "invariance"),
        ("codes", "attention", "invariance"),
        ("stories", "base", "invariance"),
        ("stories", "attention", "invariance"),
    ):
        if not any(key[0] == panel for key in items):
            continue
        change = {"panel": panel, "from": old, "to": new, "gains": [], "losses": []}
        for (item_panel, item), rows in sorted(items.items()):
            if item_panel == panel and rows[old]["correct"] != rows[new]["correct"]:
                change["gains" if rows[new]["correct"] else "losses"].append(item)
        changes.append(change)
    return {"summary": summary, "changes": changes, "rows": [row for rows in groups.values() for row in rows]}


if __name__ == "__main__":
    root = Path(__file__).resolve().parent
    stage = sys.argv[1]
    cases = json.loads((root / "INPUTS.json").read_text())[stage]
    replies = [json.loads((root / stage / f"{case['id']}.json").read_text())
               for case in cases]
    print(json.dumps(score(cases, replies), indent=2))
