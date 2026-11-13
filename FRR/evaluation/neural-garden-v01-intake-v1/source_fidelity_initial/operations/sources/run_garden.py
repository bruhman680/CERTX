"""Safe, bounded operator CLI for the experimental Neural Garden.

Each run advances a fixed number of steps, appends observations, and keeps a
recoverable checkpoint. No background service or automatic eternal run starts.
"""

from __future__ import annotations

import argparse
from contextlib import contextmanager
import json
import os
import signal
import sys
import tempfile
import time
from pathlib import Path

from garden import Garden


CHECKPOINT = "state.pkl"
METRICS = "metrics.jsonl"
MANIFEST = "manifest.json"
PAUSE = "PAUSE_REQUESTED"
SNAPSHOT = "snapshot.json"
LOCK = "RUNNING.lock"


@contextmanager
def _run_lock(directory: Path):
    """Single-writer lock; never silently remove a potentially live lock."""
    path = directory / LOCK
    try:
        fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError as exc:
        raise SystemExit(f"A run lock exists at {path}; inspect before retrying") from exc
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(json.dumps({"pid": os.getpid(), "created_unix": time.time()}))
            f.flush()
            os.fsync(f.fileno())
        yield
    finally:
        path.unlink(missing_ok=True)


def _json_dict(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _atomic_json(path: Path, data: dict):
    fd, temp_name = tempfile.mkstemp(prefix=".manifest-", suffix=".json", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, sort_keys=True)
            f.write("\n")
            f.flush()
            os.fsync(f.fileno())
        os.replace(temp_name, path)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


def _step_number(garden: Garden) -> int:
    values = garden.metrics()
    for key in ("tick", "step", "generation", "steps"):
        if key in values:
            return int(values[key])
    # The manifest supplies a fallback when the engine omits tick in metrics.
    return -1


def _checkpoint(directory: Path, garden: Garden, manifest: dict, completed: int):
    temp_name = ".state-" + str(os.getpid()) + ".pkl"
    temp_path = directory / temp_name
    try:
        garden.save(temp_path)
        if not temp_path.is_file():
            raise RuntimeError(f"Garden.save did not produce checkpoint: {temp_path}")
        os.replace(temp_path, directory / CHECKPOINT)
        manifest.update({"completed_steps": completed, "last_checkpoint_unix": time.time()})
        _atomic_json(directory / MANIFEST, manifest)
    finally:
        if temp_path.exists():
            temp_path.unlink()


def _snapshot(directory: Path, garden: Garden, completed: int):
    if not hasattr(garden, "snapshot"):
        raise RuntimeError("Garden.snapshot() is required for replay export")
    data = garden.snapshot()
    record = {"completed_steps": completed, "garden": data}
    _atomic_json(directory / SNAPSHOT, record)
    snapshots = directory / "snapshots"
    snapshots.mkdir(exist_ok=True)
    _atomic_json(snapshots / f"step_{completed:08d}.json", record)


def _record(directory: Path, entry: dict):
    with (directory / METRICS).open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, sort_keys=True, default=float) + "\n")
        f.flush()


def init(args):
    directory = Path(args.directory).expanduser().resolve()
    if directory.exists() and any(directory.iterdir()):
        raise SystemExit(f"Refusing to overwrite nonempty run directory: {directory}")
    directory.mkdir(parents=True, exist_ok=True)
    garden = Garden(seed=args.seed, size=args.size, learning=not args.no_learning)
    manifest = {"format": "neural-garden-run-v1", "seed": args.seed, "size": args.size,
                "learning": not args.no_learning, "completed_steps": 0,
                "created_unix": time.time()}
    _checkpoint(directory, garden, manifest, 0)
    _snapshot(directory, garden, 0)
    _record(directory, {"kind": "init", "completed_steps": 0, "metrics": garden.metrics()})
    print(json.dumps({"status": "initialized", "directory": str(directory),
                      "manifest": manifest, "metrics": garden.metrics()}, indent=2, default=float))


def _open_run(directory: Path):
    if not (directory / CHECKPOINT).exists():
        raise SystemExit(f"No checkpoint in {directory}; use init first")
    if not (directory / MANIFEST).exists():
        raise SystemExit(f"Missing manifest in {directory}; refusing uncertain resume")
    return Garden.load(directory / CHECKPOINT), _json_dict(directory / MANIFEST)


def execute(args):
    directory = Path(args.directory).expanduser().resolve()
    if not directory.is_dir():
        raise SystemExit(f"Run directory does not exist: {directory}; use init first")
    with _run_lock(directory):
        return _execute_locked(args, directory)


def _execute_locked(args, directory):
    if args.steps < 1 or args.checkpoint_every < 1 or args.report_every < 1 or args.snapshot_every < 1:
        raise SystemExit("steps, checkpoint-every, report-every and snapshot-every must be positive integers")
    garden, manifest = _open_run(directory)
    checkpoint_tick = _step_number(garden)
    manifest_tick = int(manifest["completed_steps"])
    if checkpoint_tick >= 0 and checkpoint_tick < manifest_tick:
        raise SystemExit(f"Checkpoint tick {checkpoint_tick} precedes manifest count {manifest_tick}; manual audit required")
    if checkpoint_tick > manifest_tick:
        _record(directory, {"kind": "manifest_recovery", "from": manifest_tick,
                            "to": checkpoint_tick, "reason": "state checkpoint is newer than manifest"})
        manifest["completed_steps"] = checkpoint_tick
        _atomic_json(directory / MANIFEST, manifest)
    # Per-step log may be newer than the last atomic checkpoint if a process
    # crashed. Preserve the old records and mark that a replay from checkpoint
    # can duplicate step numbers; downstream readers must segment at marker.
    log_path = directory / METRICS
    if log_path.exists():
        last_logged = None
        with log_path.open("r", encoding="utf-8") as f:
            for line in f:
                try:
                    event = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if event.get("kind") == "step":
                    last_logged = int(event["completed_steps"])
        if last_logged is not None and last_logged > int(manifest["completed_steps"]):
            _record(directory, {"kind": "checkpoint_recovery", "logged_through": last_logged,
                                "restarting_at": int(manifest["completed_steps"]),
                                "note": "subsequent step numbers replay; earlier uncheckpointed records remain historical"})
    if args.resume:
        (directory / PAUSE).unlink(missing_ok=True)
    elif (directory / PAUSE).exists():
        raise SystemExit("Run is paused; use resume to acknowledge and clear the pause request")

    interrupted = False
    previous_handlers = {}

    def _stop_handler(signum, frame):
        nonlocal interrupted
        interrupted = True

    for signum in (signal.SIGINT, signal.SIGTERM):
        previous_handlers[signum] = signal.getsignal(signum)
        signal.signal(signum, _stop_handler)

    completed = int(manifest["completed_steps"])
    initial = completed
    outcome = "step_budget_complete"
    try:
        for _ in range(args.steps):
            if interrupted or (directory / PAUSE).exists():
                outcome = "paused"
                break
            garden.step()
            completed += 1
            values = garden.metrics()
            # The CLI's durable count is authoritative for the run log; expose
            # any engine-local tick separately to facilitate consistency audit.
            _record(directory, {"kind": "step", "completed_steps": completed,
                                "engine_tick": _step_number(garden), "metrics": values})
            if (completed - initial) % args.checkpoint_every == 0:
                _checkpoint(directory, garden, manifest, completed)
            if (completed - initial) % args.snapshot_every == 0:
                _snapshot(directory, garden, completed)
            if (completed - initial) % args.report_every == 0:
                print(json.dumps({"completed_steps": completed, "metrics": values}, default=float), flush=True)
            if interrupted:
                outcome = "paused"
                break
    finally:
        _checkpoint(directory, garden, manifest, completed)
        _snapshot(directory, garden, completed)
        _record(directory, {"kind": "stop", "reason": outcome,
                            "completed_steps": completed, "metrics": garden.metrics()})
        for signum, previous in previous_handlers.items():
            signal.signal(signum, previous)
    print(json.dumps({"status": outcome, "advanced": completed - initial,
                      "completed_steps": completed, "directory": str(directory),
                      "metrics": garden.metrics()}, indent=2, default=float))


def pause(args):
    directory = Path(args.directory).expanduser().resolve()
    if not (directory / CHECKPOINT).exists():
        raise SystemExit("No run checkpoint found")
    (directory / PAUSE).write_text("Pause requested by operator.\n", encoding="utf-8")
    print(json.dumps({"status": "pause_requested", "directory": str(directory)}))


def status(args):
    directory = Path(args.directory).expanduser().resolve()
    garden, manifest = _open_run(directory)
    payload = {"directory": str(directory), "manifest": manifest,
               "pause_requested": (directory / PAUSE).exists(),
               "run_lock_present": (directory / LOCK).exists(),
               "engine_tick": _step_number(garden), "metrics": garden.metrics()}
    if args.command == "inspect":
        lines = (directory / METRICS).read_text(encoding="utf-8").splitlines()
        payload["recent_events"] = [json.loads(line) for line in lines[-args.tail:]]
    print(json.dumps(payload, indent=2, default=float))


def snapshot(args):
    directory = Path(args.directory).expanduser().resolve()
    garden, manifest = _open_run(directory)
    completed = int(manifest["completed_steps"])
    _snapshot(directory, garden, completed)
    print(json.dumps({"status": "snapshot_saved", "completed_steps": completed,
                      "latest": str(directory / SNAPSHOT)}))


def main(argv=None):
    parser = argparse.ArgumentParser(description="Neural Garden v0.1 bounded operator")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("init", help="Create one new, independent experiment")
    p.add_argument("--directory", required=True)
    p.add_argument("--size", type=int, default=16)
    p.add_argument("--seed", type=int, default=7)
    p.add_argument("--no-learning", action="store_true")
    p.set_defaults(func=init)
    for name in ("run", "resume"):
        p = sub.add_parser(name, help="Advance a bounded number of steps")
        p.add_argument("--directory", required=True)
        p.add_argument("--steps", type=int, default=100)
        p.add_argument("--checkpoint-every", type=int, default=10)
        p.add_argument("--report-every", type=int, default=50)
        p.add_argument("--snapshot-every", type=int, default=10)
        p.set_defaults(func=execute, resume=name == "resume")
    p = sub.add_parser("pause", help="Request cooperative pause at the next step boundary")
    p.add_argument("--directory", required=True)
    p.set_defaults(func=pause)
    p = sub.add_parser("snapshot", help="Export current checkpoint state for visualization")
    p.add_argument("--directory", required=True)
    p.set_defaults(func=snapshot)
    for name in ("status", "inspect"):
        p = sub.add_parser(name)
        p.add_argument("--directory", required=True)
        if name == "inspect":
            p.add_argument("--tail", type=int, default=5)
        p.set_defaults(func=status)
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()

