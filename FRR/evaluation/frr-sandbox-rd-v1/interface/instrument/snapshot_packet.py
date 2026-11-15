"""Pure metadata projection of an already verified, committed world snapshot.

NOT WIRED INTO PILOTS. This module does not open a world or execute model code.
Its metadata checks do not establish cryptographic or storage validity.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
from pathlib import Path
import re
import sys
from typing import Any


class MetadataError(ValueError):
    """The supplied metadata does not have the supported snapshot shape."""


class PacketCapacityError(ValueError):
    """The complete packet exceeds the caller's declared byte allowance."""
    def __init__(self, required_bytes: int, limit_bytes: int, entry_count: int):
        self.required_bytes = required_bytes
        self.limit_bytes = limit_bytes
        self.entry_count = entry_count
        super().__init__(f"Complete packet needs {required_bytes} bytes; limit is {limit_bytes}. No partial packet emitted.")


@dataclass
class SnapshotObservation:
    model_packet: dict[str, Any]
    model_text: str
    observer_record: dict[str, Any]


def _integer(value: Any, name: str, minimum: int = 0, maximum: int | None = None) -> int:
    if type(value) is not int or value < minimum or (maximum is not None and value > maximum):
        raise MetadataError(f"Invalid {name}")
    return value


def _relative_path(value: Any, name: str) -> str:
    if type(value) is not str or not value or "\x00" in value or value.startswith("/"):
        raise MetadataError(f"Invalid {name}")
    if any(part in ("", ".", "..") for part in value.split("/")):
        raise MetadataError(f"Invalid {name}")
    return value


def _hash_shape(value: Any, name: str) -> str:
    if type(value) is not str or re.fullmatch(r"[0-9a-f]{64}", value) is None:
        raise MetadataError(f"Invalid {name} shape")
    return value


def _validated_entries(bundle: Any) -> dict[str, list[Any]]:
    if type(bundle) is not dict or type(bundle.get("entries")) is not list:
        raise MetadataError("A snapshot object with an entries array is required")
    _hash_shape(bundle.get("id"), "source bundle id")
    _integer(bundle.get("root_mode"), "root mode", maximum=0o777)
    rows: dict[str, list[Any]] = {}
    for row in bundle["entries"]:
        if type(row) is not list or len(row) < 2:
            raise MetadataError("Invalid entry row")
        name = _relative_path(row[0], "entry path")
        if name in rows:
            raise MetadataError("Duplicate entry path")
        kind = row[1]
        if type(kind) is not str:
            raise MetadataError("Invalid entry kind")
        if kind == "file":
            if len(row) != 5:
                raise MetadataError("Invalid file row")
            _integer(row[2], "file mode", maximum=0o777)
            _hash_shape(row[3], "file object hash")
            _integer(row[4], "file byte count")
        elif kind in ("directory", "fifo"):
            if len(row) != 3:
                raise MetadataError("Invalid directory/fifo row")
            _integer(row[2], "entry mode", maximum=0o777)
        elif kind == "hardlink":
            if len(row) != 3:
                raise MetadataError("Invalid hardlink row")
            _relative_path(row[2], "hardlink target")
        elif kind == "symlink":
            if len(row) != 3 or type(row[2]) is not str or not row[2] or "\x00" in row[2]:
                raise MetadataError("Invalid symlink row")
            # A symlink's text may be absolute or contain '..'. It is never followed.
        else:
            raise MetadataError("Unsupported entry kind")
        rows[name] = row
    for name, row in rows.items():
        parts = name.split("/")
        for n in range(1, len(parts)):
            parent = "/".join(parts[:n])
            if parent not in rows or rows[parent][1] != "directory":
                raise MetadataError("Entry has a missing or non-directory ancestor")
        if row[1] == "hardlink" and (row[2] not in rows or rows[row[2]][1] != "file"):
            raise MetadataError("Hardlink target must be a captured regular file")
    return rows


def make_snapshot(bundle: Any, *, timing: str, world_step: int,
                  reply_index: int | None, max_packet_bytes: int) -> SnapshotObservation:
    """Project every supported entry; return all or raise, never choose a subset.

    Timing/step truth, committed-source identity, CAS bytes and ancestry remain
    the caller's responsibility. No metadata path is read or followed here.
    """
    rows = _validated_entries(bundle)
    _integer(world_step, "world step")
    _integer(max_packet_bytes, "packet byte allowance", minimum=1)
    if timing not in ("initial", "after_reply"):
        raise MetadataError("Timing must be initial or after_reply")
    if timing == "initial":
        if reply_index is not None:
            raise MetadataError("An initial snapshot has no completed reply index")
    else:
        _integer(reply_index, "completed reply index", minimum=1)
    entries = []
    for name in sorted(rows):
        row = rows[name]
        size = row[4] if row[1] == "file" else rows[row[2]][4] if row[1] == "hardlink" else None
        entries.append({"name": name, "type": row[1], "bytes": size})
    packet = {"world_snapshot": {"path": "/world", "timing": timing,
              "world_step": world_step, "reply_index": reply_index, "entries": entries}}
    text = json.dumps(packet, ensure_ascii=True, sort_keys=True, separators=(",", ":"), allow_nan=False)
    size = len(text.encode("utf-8"))
    if size > max_packet_bytes:
        raise PacketCapacityError(size, max_packet_bytes, len(entries))
    record = {"instrument": "snapshot_packet_v1", "source_bundle_id": bundle["id"],
              "source_root_mode": bundle["root_mode"], "entry_count": len(entries),
              "packet_bytes": size, "packet_byte_allowance": max_packet_bytes,
              "timing": timing, "world_step": world_step, "reply_index": reply_index,
              "scope": "metadata projection only; caller supplies verified committed source and truthful timing"}
    return SnapshotObservation(packet, text, record)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bundle", type=Path, required=True)
    parser.add_argument("--timing", choices=["initial", "after_reply"], required=True)
    parser.add_argument("--world-step", type=int, required=True)
    parser.add_argument("--reply-index", type=int)
    parser.add_argument("--max-bytes", type=int, required=True)
    parser.add_argument("--observer-record", type=Path)
    args = parser.parse_args(argv)
    try:
        observation = make_snapshot(json.loads(args.bundle.read_text()), timing=args.timing,
                                    world_step=args.world_step, reply_index=args.reply_index,
                                    max_packet_bytes=args.max_bytes)
        if args.observer_record is not None:
            record = {**observation.observer_record, "source_bundle_path": str(args.bundle)}
            with args.observer_record.open("x", encoding="utf-8") as stream:
                stream.write(json.dumps(record, ensure_ascii=True, sort_keys=True) + "\n")
        sys.stdout.write(observation.model_text)
        return 0
    except PacketCapacityError as error:
        sys.stderr.write(json.dumps({"observer_error": "packet_capacity", "required_bytes": error.required_bytes,
                                    "limit_bytes": error.limit_bytes, "entry_count": error.entry_count,
                                    "model_packet_emitted": False}) + "\n")
        return 2
    except (MetadataError, json.JSONDecodeError, OSError) as error:
        sys.stderr.write(json.dumps({"observer_error": type(error).__name__, "message": str(error),
                                    "model_packet_emitted": False}) + "\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
