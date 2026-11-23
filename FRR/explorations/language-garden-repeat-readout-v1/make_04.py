"""Remove the menu, contrasting exposed Last with an inferred repeated symbol."""
import json
from pathlib import Path
import random

cases = []
for block, (a, b) in enumerate([("mip", "zav"), ("ket", "ful")], 1):
    for shape, values in (("AAB", (a, a, b)), ("ABA", (a, b, a)), ("ABB", (a, b, b))):
        for prompt, question, gold in (
            ("visible_last", "What is the last symbol in this row?", values[-1]),
            ("repeated_symbol", "Which symbol appears twice in this row?",
             a if values.count(a) == 2 else b),
        ):
            item = f"s{block}-{shape.lower()}"
            row = "\n".join(f"{position}: {value}" for position, value in
                            zip(("First", "Middle", "Last"), values, strict=True))
            cases.append({
                "id": f"{item}-{prompt}", "item": item, "relation": shape,
                "prompt": prompt, "gold": gold, "values": list(values),
                "seed_style": "garden",
                "text": row + "\n\n" + question + " Reply with the symbol only.",
            })
random.Random(2413).shuffle(cases)
folder = Path("04")
folder.mkdir()
(folder / "CASES.json").write_text(json.dumps({
    "goal": "Can a direct symbol answer recover an observable readout and distinguish it from repetition?",
    "comparison": "The same labeled row is reused for both questions. AAB breaks the heuristic of always returning Last. ABA and ABB connect to the original position probe.",
    "cases": cases,
}, indent=2) + "\n")
