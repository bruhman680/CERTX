"""Build the two balanced panels before model inference."""
import random


ENDPOINT_QUESTION = (
    "Do the first and last symbols in this row match? Reply with Yes or No."
)
SEEDS = {
    "base": "",
    "attention": "When you read a question, take time to think.",
    "invariance": "When something changes, look for what stays the same.",
}


def endpoint_cases():
    cases = []
    for block, (a, b, middle) in enumerate(
        [("lu", "ne", "fi"), ("go", "do", "bi")], 1
    ):
        for i, left in enumerate((a, b), 1):
            for j, right in enumerate((a, b), 1):
                for condition in ("two", "three"):
                    fields = [f"First: {left}"]
                    if condition == "three":
                        fields.append(f"Middle: {middle}")
                    fields.append(f"Last: {right}")
                    cases.append({
                        "id": f"e{block}-{i}{j}-{condition}",
                        "panel": "endpoints",
                        "condition": condition,
                        "pair": f"e{block}-{i}",
                        "item": f"e{block}-{i}{j}",
                        "text": "\n".join(fields) + "\n\n" + ENDPOINT_QUESTION,
                        "gold": "yes" if left == right else "no",
                        "values": fields,
                    })
    return cases


def render(panel, first, second):
    if panel == "codes":
        return (
            f"Sequence 1: {' '.join(first)}\nSequence 2: {' '.join(second)}\n\n"
            "Do the two sequences have the same repetition pattern? Reply with Yes or No."
        )
    return (
        f"Round 1: {first[0]} waved, then {first[1]} waved, then {first[2]} waved.\n"
        f"Round 2: {second[0]} waved, then {second[1]} waved, then {second[2]} waved.\n\n"
        "Do the two rounds have the same pattern of who repeats? Reply with Yes or No."
    )


def pattern(values):
    return [values.index(value) for value in values]


def seed_cases():
    panels = {
        "codes": [
            (("zi", "po"), ("fa", "re")),
            (("nu", "to"), ("be", "ki")),
        ],
        "stories": [
            (("Maya", "Imani"), ("Nora", "Leila")),
            (("Jules", "Omar"), ("Ravi", "Hugo")),
        ],
    }
    cases = []
    for panel, blocks in panels.items():
        for block, ((a, b), (c, d)) in enumerate(blocks, 1):
            for i, first in enumerate(((a, b, a), (a, b, b)), 1):
                for j, second in enumerate(((c, d, c), (c, d, d)), 1):
                    item = f"{panel}-{block}-{i}{j}"
                    for condition in SEEDS:
                        cases.append({
                            "id": f"{item}-{condition}",
                            "panel": panel,
                            "condition": condition,
                            "pair": f"{panel}-{block}-{i}",
                            "item": item,
                            "text": render(panel, first, second),
                            "gold": "yes" if pattern(first) == pattern(second) else "no",
                            "values": [first, second],
                        })
    return cases


def panels():
    randomizer = random.Random(2407)
    stages = {"endpoint": endpoint_cases(), "seed": seed_cases()}
    for stage in stages.values():
        randomizer.shuffle(stage)
    return stages
