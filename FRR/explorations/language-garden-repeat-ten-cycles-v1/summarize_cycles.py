"""Summarize per-cycle measurements and paired changes from audited result rows."""
from collections import defaultdict
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
stages = {i: json.loads((HERE / f"{i:02d}/RESULTS.json").read_text()) for i in range(1, 11)}
prompts = {i: json.loads((HERE / f"{i:02d}/INPUTS.json").read_text())["question"] for i in stages}


def outcomes(rows, index):
    return {row[index]: row for row in rows}


def compare(left, right, keys):
    a = outcomes(left, keys[0])
    b = outcomes(right, keys[1])
    if a.keys() != b.keys():
        raise ValueError("Comparison contains unpaired cases")
    return {
        "pairs": len(a),
        "same_reply_label": sum(a[k]["picked"] == b[k]["picked"] for k in a),
        "gains": [k for k in a if not a[k]["content_correct"] and b[k]["content_correct"]],
        "losses": [k for k in a if a[k]["content_correct"] and not b[k]["content_correct"]],
        "both_correct": [k for k in a if a[k]["content_correct"] and b[k]["content_correct"]],
    }


first = stages[1]["rows"]
paired = {
    "last_to_repeat": compare(
        [r for r in first if r["task"] == "last"],
        [r for r in first if r["task"] == "repeat"], ("key", "key"),
    ),
    "garden_to_native": compare(stages[2]["rows"], stages[3]["rows"], ("key", "key")),
}
layout = stages[6]["rows"]
prior = [r for n in (4, 5) for r in stages[n]["rows"] if r["id"] in {r["contrast"] for r in layout}]
paired["labeled_to_flat"] = compare(prior, layout, ("id", "contrast"))

counts = defaultdict(list)
for row in stages[5]["rows"]:
    counts[row["key"]].append(row)
count_pairs = {key: [r["content_correct"] for r in group] for key, group in counts.items()}
last_edit = {r["key"]: r for r in stages[9]["rows"]}


def edit_result(a, b, should_change):
    left, right = last_edit[f"edit-{a}"], last_edit[f"edit-{b}"]
    return {
        "should_change": should_change,
        "gold": [left["gold"], right["gold"]],
        "picked": [left["picked"], right["picked"]],
        "both_correct": left["content_correct"] and right["content_correct"],
    }


final = defaultdict(list)
for row in stages[10]["rows"]:
    final[row["shape"]].append(row)

summary = {
    "fresh_calls": sum(len(stage["rows"]) for stage in stages.values()),
    "distinct_rendered_user_inputs": len({r["text"] for stage in stages.values() for r in stage["rows"]}),
    "cycles": [
        {"cycle": i, "goal": prompts[i], "tasks": d["tasks"], "stops": d["stops"],
         "distinct_chat_inputs": len({r["text"] for r in d["rows"]}),
         "repeat_baselines": d["repeat_baselines"]}
        for i, d in stages.items()
    ],
    "paired": paired,
    "both_counts_correct": sum(all(group) for group in count_pairs.values()),
    "count_pairs": len(count_pairs),
    "last_edits": [edit_result(1, 2, False), edit_result(3, 4, True),
                   edit_result(5, 6, True)],
    "final_by_shape": {
        shape: {"correct": sum(r["content_correct"] for r in group), "total": len(group)}
        for shape, group in sorted(final.items())
    },
    "final_copy_baselines": stages[10]["repeat_baselines"],
}
trace = HERE / "SUMMARY.json"
if len(sys.argv) > 1 and sys.argv[1] == "audit":
    if json.loads(trace.read_text()) != summary:
        raise ValueError("Saved summary differs from recomputation")
else:
    with trace.open("x") as output:
        json.dump(summary, output, indent=2)
        output.write("\n")
print(json.dumps(summary))
