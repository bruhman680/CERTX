"""Build stage prompts, using only results already observed."""
from collections import defaultdict

BASE = "garden"
NATIVE = "native"
REPEAT_QUESTION = "Which symbol appears twice in this row?"
LAST_QUESTION = "What is the last symbol in this row?"
STATE = {
    "opaque": [("nef", "zol"), ("rud", "bem"), ("taz", "wip"), ("kef", "dov")],
    "digits": [("4", "7"), ("6", "2"), ("8", "3"), ("5", "9")],
    "words": [("leaf", "stone"), ("pond", "hill"), ("bird", "fish"), ("rain", "wind")],
}
ROLES = ("First", "Middle", "Last")


def make_row(key, pair, pattern):
    return {"key": key, "values": [pair["AB".index(mark)] for mark in pattern],
            "shape": pattern}


def rows(kind, patterns):
    return [
        make_row(f"{kind}-{i + 1}-{pattern.lower()}", STATE[kind][i % len(STATE[kind])], pattern)
        for i, pattern in enumerate(patterns)
    ]


def case(row, task="repeat", seed=BASE, layout="fields", *, target=None, contrast=None):
    values = row["values"]
    symbols = sorted(set(values))
    repeat = next(symbol for symbol in symbols if values.count(symbol) == 2)
    shown = ("\n".join(f"{role}: {value}" for role, value in zip(ROLES, values, strict=True))
             if layout == "fields" else "Row: " + " ".join(values))
    if task == "repeat":
        question, gold = REPEAT_QUESTION, repeat
    elif task == "last":
        question, gold = LAST_QUESTION, values[-1]
    elif task == "count":
        question = f"How many times does the exact symbol {target} appear in the row? Reply with one or two only."
        gold = str(values.count(target))
    elif task == "hint":
        positions = [role for role, value in zip(ROLES, values, strict=True) if value == repeat]
        question = f"Which symbol is written in both the {positions[0]} and {positions[1]} fields?"
        gold = repeat
    else:
        raise ValueError(task)
    if task != "count":
        question += " Reply with the symbol only."
    lead = {
        BASE: "Explore symbols and their relationships. Learn to predict and understand them as best you can.",
        NATIVE: "",
        "invariance": "Explore symbols and their relationships. Learn to predict and understand them as best you can.\n\nWhen something changes, look for what stays the same.",
        "attention": "Explore symbols and their relationships. Learn to predict and understand them as best you can.\n\nWhen you read a question, take time to think.",
    }[seed]
    text = "\n\n".join(part for part in (lead, shown, question) if part)
    identifier = f"{row['key']}-{task}-{seed}-{layout}"
    if target is not None:
        identifier += f"-{target}"
    return dict(row, id=identifier, task=task, seed=seed, layout=layout,
                target=target, gold=gold, options=symbols, text=text, contrast=contrast)


def panel(number, prior):
    if number == 1:
        panel_rows = rows("opaque", ("AAB",) * 4)
        return "Repeat versus Last on four fresh rows where they differ.", [
            case(row, task) for row in panel_rows for task in ("repeat", "last")
        ]
    if number == 2:
        good = metric(prior[1], task="repeat") >= 3
        kind = "opaque" if good else "digits"
        patterns = ("ABB", "ABA", "ABB", "ABA") if good else ("AAB",) * 4
        goal = ("Check whether readout survives moving repetition away from the first two positions."
                if good else "Replace opaque labels with familiar digits on the same AAB structure.")
        return goal, [case(row) for row in rows(kind, patterns)]
    if number == 3:
        return "Replay cycle 2 exactly except for removing the broad garden preface.", [
            case(row, seed=NATIVE) for row in prior[2]["rows"]
        ]
    seed = NATIVE if metric(prior[3]) > metric(prior[2]) else BASE
    kind = "digits" if metric(prior[2]) >= 3 and prior[2]["rows"][0]["key"].startswith("digits") else "opaque"
    if number == 4:
        return "Cross all three repetition positions. Include every shape twice.", [
            case(row, seed=seed) for row in rows(kind, ("AAB", "ABA", "ABB", "ABB", "AAB", "ABA"))
        ]
    if number == 5:
        by_shape = defaultdict(list)
        for row in prior[4]["rows"]:
            by_shape[row["shape"]].append(row)
        selected = [
            min(group, key=lambda row: (row["content_correct"], row["id"]))
            for group in by_shape.values()
        ]
        return "Ask for the count of one named symbol, testing both candidates on each selected row.", [
            case(row, "count", seed, target=symbol, contrast=row["id"])
            for row in selected for symbol in row["options"]
        ]
    if number == 6:
        focus = 4 if metric(prior[5]) >= 4 else 5
        return f"Flatten cycle {focus} from labeled fields to a plain row, keeping every question fixed.", [
            case(row, row["task"], row["seed"], "flat", target=row["target"], contrast=row["id"])
            for row in prior[focus]["rows"]
        ]
    flat_repeat = (number >= 7 and prior[6]["rows"][0]["task"] == "repeat"
                   and metric(prior[6]) > metric(prior[4]))
    layout = "flat" if flat_repeat else "fields"
    if number == 7:
        return "Use everyday words instead of the earlier vocabulary with each repetition shape preserved.", [
            case(row, seed=seed, layout=layout)
            for row in rows("words", ("AAB", "ABA", "ABB", "ABB", "AAB", "ABA"))
        ]
    if number == 8:
        candidate = max((prior[4], prior[7]), key=metric)
        if metric(candidate) >= 5:
            tests = sorted(candidate["rows"], key=lambda r: r["key"])[:4]
            return "Compare the broad invariance cue against the length-matched attention cue on the same rows.", [
                case(row, seed=cue, layout=row["layout"])
                for row in tests for cue in ("invariance", "attention")
            ]
        return "Supply the relevant pair of fields and test whether the model can read the reported match.", [
            case(row, "hint", seed, contrast=row["id"])
            for row in prior[4]["rows"]
        ]
    if number == 9:
        recoveries = [r for r in prior[8]["rows"] if r["content_correct"]]
        pair = ("oak", "reed") if len(recoveries) >= 4 else ("7", "9")
        third = "fern" if len(recoveries) >= 4 else "2"
        # Near neighbors isolate a Last edit that should preserve the answer, or switch it.
        a, b = pair
        values = [(a, a, b), (a, a, third), (a, b, a), (a, b, b),
                  (b, a, b), (b, a, a)]
        return "Perturb the last cell. Contrast an edit that keeps the answer with edits that switch it.", [
            case({"key": f"edit-{i + 1}", "values": list(value),
                  "shape": "AAB" if i < 2 else "ABA" if i % 2 == 0 else "ABB"},
                 seed=seed, layout=layout)
            for i, value in enumerate(values)
        ]
    assert number == 10
    everyday = metric(prior[7]) > metric(prior[4])
    reserved = ([("cloud", "rock"), ("duck", "goat"), ("thread", "paper"), ("lake", "grove")]
                if everyday else [("fep", "lem"), ("nop", "ral"), ("git", "mux"), ("suv", "zen")])
    if not everyday and kind == "digits":
        reserved = [("1", "0"), ("3", "8"), ("2", "5"), ("9", "4")]
    return "Test the selected direct-readout setup on a reserved panel where First, Middle and Last each fail on four rows.", [
        case(make_row(f"reserve-{i + 1}-{shape.lower()}", pair, shape), seed=seed, layout=layout)
        for i, pair in enumerate(reserved) for shape in ("AAB", "ABA", "ABB")
    ]


def metric(result, task=None):
    return sum(row["content_correct"] for row in result["rows"]
               if task is None or row["task"] == task)
