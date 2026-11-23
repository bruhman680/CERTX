"""Construct a two-choice panel with reversed assignments for every item."""
import json
from pathlib import Path
import random


def make_panel(stage, items, goal, check):
    folder = Path(stage)
    folder.mkdir(exist_ok=False)
    cases = []
    for item, row, question, options, expected, seed_style in items:
        for order, labels in (("forward", options), ("reverse", options[::-1])):
            assert len(set(labels)) == 2 and expected in labels
            text = (
                f"{row}\n\n{question}\n"
                f"A. {labels[0]}\nB. {labels[1]}\n\nReply with A or B only."
            )
            cases.append({
                "id": f"{item}-{order}",
                "item": item,
                "order": order,
                "correct_option": expected,
                "choices": dict(zip(("A", "B"), labels)),
                "gold": "AB"[labels.index(expected)],
                "text": text,
                "seed_style": seed_style,
            })
    random.Random(2411).shuffle(cases)
    (folder / "CASES.json").write_text(json.dumps({
        "goal": goal, "comparison": check, "cases": cases
    }, indent=2) + "\n")


def make_first():
    items = []
    for block, (a, b) in enumerate(
        [("mip", "zav"), ("ket", "ful"), ("wug", "dap"), ("bim", "vok")], 1
    ):
        for i, last in enumerate((a, b), 1):
            options = ("First and third", "Second and third")
            items.append((
                f"p{block}-{i}", f"Row: {a} {b} {last}",
                "Which positions contain the same symbol?", options,
                options[i - 1], "garden",
            ))
    make_panel(
        "01", items, "Can the model name which positions repeat in a single row?",
        "Each symbol pair supports both repeat positions, and each row is repeated with the two options reversed.",
    )


if __name__ == "__main__":
    make_first()
