"""Observer-only checks against existing captured CAS data and scoped fixtures."""
from pathlib import Path
import argparse
import base64
import copy
import hashlib
import json
import subprocess
import sys
import tempfile

from snapshot_packet import make_snapshot, MetadataError, PacketCapacityError

HERE = Path(__file__).resolve().parent
RD = HERE.parents[1]


def checks() -> dict:
    store = RD / "pilot/branches/control/world"
    prepared_path = store / "bundles/000001.json"
    prepared = json.loads(prepared_path.read_text())
    end_record = json.loads((RD / "pilot/records/control_t3.json").read_text())
    final_step = json.loads((store / "STATE.json").read_text())["step"]
    final_path = store / "bundles" / f"{final_step:06d}.json"
    final = json.loads(final_path.read_text())
    assert prepared["id"] == json.loads((RD / "pilot/PREPARATION_CHECKS.json").read_text())["conditions"][0]["world_id"]
    assert final["id"] == end_record["after_id"]
    observed = []
    for source, timing, step, reply in [(prepared, "initial", 1, None), (final, "after_reply", final_step, 3)]:
        observation = make_snapshot(source, timing=timing, world_step=step, reply_index=reply, max_packet_bytes=16384)
        packet = json.loads(observation.model_text)["world_snapshot"]
        expected = []
        for row in sorted(source["entries"]):
            assert row[1] == "file", "Current real fixtures are regular-file only"
            obj = json.loads((store / "objects" / (row[3] + ".json")).read_text())
            data = base64.b64decode(obj["base64"], validate=True)
            assert len(data) == row[4] == obj["bytes"]
            assert hashlib.sha256(data).hexdigest() == row[3] == obj["sha256"]
            expected.append({"name": row[0], "type": "file", "bytes": len(data)})
        assert packet["entries"] == expected
        assert packet["timing"] == timing and packet["reply_index"] == reply and packet["world_step"] == step
        assert "source_bundle_id" not in observation.model_text and source["id"] not in observation.model_text
        assert observation.observer_record["source_bundle_id"] == source["id"]
        observed.append({"timing": timing, "source_bundle_id": source["id"], "entry_count": len(expected),
                         "packet_bytes": observation.observer_record["packet_bytes"]})

    # Metadata fixtures are deliberately not world captures: no filesystem action runs.
    added = copy.deepcopy(prepared)
    name = 'added"\\\n\u2603.txt'
    payload = b"three"
    added["entries"].append([name, "file", 0o600, hashlib.sha256(payload).hexdigest(), len(payload)])
    added_observation = make_snapshot(added, timing="after_reply", world_step=4, reply_index=3, max_packet_bytes=16384)
    added_entries = added_observation.model_packet["world_snapshot"]["entries"]
    assert len(added_entries) == len(prepared["entries"]) + 1 == 6
    assert next(x for x in added_entries if x["name"] == name)["bytes"] == len(payload)
    assert json.loads(added_observation.model_text) == added_observation.model_packet
    assert "\n" not in added_observation.model_text and "\\n" in added_observation.model_text
    deleted = copy.deepcopy(prepared)
    deleted["entries"] = [row for row in deleted["entries"] if row[0] != "prior_replies.jsonl"]
    deleted_entries = make_snapshot(deleted, timing="initial", world_step=1, reply_index=None, max_packet_bytes=16384).model_packet["world_snapshot"]["entries"]
    assert len(deleted_entries) == 4 and all(x["name"] != "prior_replies.jsonl" for x in deleted_entries)

    # Link/type handling projects logical payload size without opening or following paths.
    linked = copy.deepcopy(prepared)
    target = next(x for x in linked["entries"] if x[0] == "LAWS.txt")
    linked["entries"] += [["folder", "directory", 0o700], ["folder/alias", "hardlink", "LAWS.txt"],
                          ["sym", "symlink", "/outside-metadata-only"], ["pipe", "fifo", 0o600]]
    projection = make_snapshot(linked, timing="initial", world_step=0, reply_index=None, max_packet_bytes=16384)
    by_name = {x["name"]: x for x in projection.model_packet["world_snapshot"]["entries"]}
    assert by_name["folder/alias"]["bytes"] == target[4]
    assert all(by_name[x]["bytes"] is None for x in ["folder", "sym", "pipe"])
    assert "/outside-metadata-only" not in projection.model_text
    bad_mode = copy.deepcopy(prepared);bad_mode["root_mode"] = True
    bad_parent = copy.deepcopy(linked);bad_parent["entries"].append(["sym/child", "file", 0o600, "0" * 64, 0])
    bad_link = copy.deepcopy(linked);next(x for x in bad_link["entries"] if x[0] == "folder/alias")[2] = "missing"
    rejected = 0
    for fixture in [bad_mode, bad_parent, bad_link]:
        try:
            make_snapshot(fixture, timing="initial", world_step=0, reply_index=None, max_packet_bytes=16384)
        except MetadataError:
            rejected += 1
        else:
            raise AssertionError("Malformed metadata accepted")

    complete = make_snapshot(prepared, timing="initial", world_step=1, reply_index=None, max_packet_bytes=16384)
    required = len(complete.model_text.encode("utf-8"))
    assert make_snapshot(prepared, timing="initial", world_step=1, reply_index=None, max_packet_bytes=required).model_text == complete.model_text
    try:
        make_snapshot(prepared, timing="initial", world_step=1, reply_index=None, max_packet_bytes=required - 1)
    except PacketCapacityError as error:
        assert error.required_bytes == required and error.limit_bytes == required - 1 and error.entry_count == 5
        assert not hasattr(error, "model_packet")
    else:
        raise AssertionError("Overflow silently accepted")

    with tempfile.TemporaryDirectory() as temporary:
        record = Path(temporary) / "observer.json"
        args = [sys.executable, str(HERE / "snapshot_packet.py"), "--bundle", str(prepared_path),
                "--timing", "initial", "--world-step", "1", "--max-bytes", str(required)]
        cli = subprocess.run(args + ["--observer-record", str(record)], capture_output=True, text=True, check=True)
        assert cli.stdout == complete.model_text and len(cli.stdout.encode()) == required and cli.stderr == ""
        assert json.loads(record.read_text())["source_bundle_id"] == prepared["id"]
        overflow = subprocess.run(args[:-1] + [str(required - 1)], capture_output=True, text=True)
        assert overflow.returncode == 2 and overflow.stdout == ""
        assert json.loads(overflow.stderr)["model_packet_emitted"] is False
    return {"status": "pass", "real_snapshot_checks": observed,
            "real_regular_file_bytes_match_decoded_CAS": True,
            "synthetic_added_six_deleted_four_entries": True, "special_name_json_roundtrip": True,
            "link_types_and_no_target_following": True, "representative_malformed_metadata_rejected": rejected,
            "exact_budget_and_overflow_no_partial_packet": True, "CLI_stdout_packet_only": True,
            "metadata_fixtures_are_not_world_captures": True,
            "source_assumption": "caller provides verified committed bundle; instrument does not verify source hash/ancestry/CAS",
            "model_calls": 0, "sandbox_opens": 0, "wired_into_pilots": False, "M2_run": False,
            "capture_mode_contract": {"source": str(RD.parent / "final-garden-contract-v1/world.py"),
              "sha256": hashlib.sha256((RD.parent / "final-garden-contract-v1/world.py").read_bytes()).hexdigest(),
              "capture_mask": "st_mode & 0o777",
              "scope": "matches captured metadata; does not observe native sticky/setuid/setgid bits"}}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-results", type=Path)
    args = parser.parse_args()
    result = checks()
    if args.write_results is not None:
        with args.write_results.open("x", encoding="utf-8") as stream:
            stream.write(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result))
