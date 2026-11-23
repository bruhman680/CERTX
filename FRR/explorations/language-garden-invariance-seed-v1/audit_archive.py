"""Check the portable model traces and scores without the live session directories."""
from collections import Counter, defaultdict
from pathlib import Path

from run_study import HERE, compose, pins, read, recorder, run
from score import score


def check_design(stage, cases):
    by_condition = defaultdict(list)
    for case in cases:
        by_condition[case["panel"], case["condition"]].append(case)
        if stage == "endpoint":
            first, last = (case["values"][index].split(": ")[1] for index in (0, -1))
            actual = first == last
        else:
            first, last = case["values"]
            assert set(first).isdisjoint(last)
            relation = [(0, 1), (0, 2), (1, 2)]
            actual = all((first[a] == first[b]) == (last[a] == last[b]) for a, b in relation)
        assert case["gold"] == ("yes" if actual else "no")
    assert all(Counter(c["gold"] for c in group) == {"yes": 4, "no": 4}
               for group in by_condition.values())
    assert len(by_condition) == (2 if stage == "endpoint" else 6)


def main():
    from transformers import AutoTokenizer

    contract = run.verify_pins(run.DEFAULT_MODEL)
    assert read("INPUT_CONTRACT.json") == {"sha256": pins()}
    tokenizer = AutoTokenizer.from_pretrained(
        run.DEFAULT_MODEL, local_files_only=True, trust_remote_code=False
    )
    total = 0
    for stage, cases in read("INPUTS.json").items():
        check_design(stage, cases)
        lengths = read("TOKEN_LENGTHS.json")[stage]
        assert {path.stem for path in (HERE / stage).glob("*.json")} == {c["id"] for c in cases}
        records = []
        for case in cases:
            record = read(Path(stage) / f"{case['id']}.json")
            recorder.SEED = compose(case)
            plan = recorder.assemble(tokenizer, [])
            assert record["plan"] == {"turn": 1, "author": "host",
                                      "output_reserve": recorder.MAX_OUTPUT, **plan}
            assert len(plan["input_token_ids"]) == lengths[case["id"]]
            recorder.verify_reply(tokenizer, plan, record["reply"])
            assert record["parameters"] == {"tensor_digest_after": contract["tensor_digest"]}
            expected_status = "token_limit" if record["reply"]["stop"] == "token_limit" else (
                "operator_pause" if record["reply"]["text"] else "empty_visible_reply"
            )
            assert record["status"] == expected_status
            records.append(record)
        assert score(cases, records) == read(f"{stage.upper()}_RESULTS.json")
        total += len(records)
        print(f"{stage}: validated {len(records)} portable traces and recomputed scores")
    assert total == 64


if __name__ == "__main__":
    main()
