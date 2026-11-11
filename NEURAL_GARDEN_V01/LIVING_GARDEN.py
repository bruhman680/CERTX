"""Operator controls for one long-lived Neural Garden world.

Unlike a batch sweep, this tool advances the SAME checkpoint, and can pause,
throttle, inspect, fork, and log explicit interventions. The world never runs
autonomously after the process exits; `advance --ticks 0` stays foreground and
requires manual interruption/pause. No original Garden physics are changed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import signal
import time

from garden import Garden
import run_garden as base


EVENTS = "LIVING_EVENTS.jsonl"


def _physics_hash():
    return hashlib.sha256((Path(__file__).resolve().parent / "garden.py").read_bytes()).hexdigest()


def _event(directory: Path, payload: dict):
    record = {"utc_unix": time.time(), **payload}
    with (directory / EVENTS).open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(record, sort_keys=True) + "\n")
        stream.flush()
        os.fsync(stream.fileno())


def _open(directory: Path):
    if not directory.is_dir():
        raise SystemExit(f"Missing Garden directory: {directory}")
    garden, manifest = base._open_run(directory)
    if not manifest.get("living_garden"):
        raise SystemExit("Not initialized as a Living Garden; refusing uncertain mutation")
    if manifest.get("physics_source_sha256") != _physics_hash():
        raise SystemExit("Garden physics source has changed since initialization; do not silently continue this lineage")
    if garden.tick < manifest["completed_steps"]:
        raise SystemExit("Checkpoint behind manifest; manual recovery needed")
    return garden, manifest


def _directory(args):
    return Path(args.directory).expanduser().resolve()


def initialize(args):
    directory = _directory(args)
    if directory.exists() and any(directory.iterdir()):
        raise SystemExit(f"Refusing overwrite of existing directory {directory}")
    directory.mkdir(parents=True, exist_ok=True)
    garden = Garden(seed=args.seed, size=args.size, learning=not args.no_learning)
    manifest = {
        "format": "neural-garden-living-v1", "living_garden": True,
        "seed": args.seed, "size": args.size,
        "learning": garden.learning, "completed_steps": 0,
        "created_unix": time.time(), "parent": None,
        "intervention_count": 0,
        "physics_source_sha256": _physics_hash(),
    }
    base._checkpoint(directory, garden, manifest, 0)
    base._snapshot(directory, garden, 0)
    _event(directory, {"kind": "init", "tick": 0,
                       "seed": args.seed, "size": args.size,
                       "fingerprint": garden.fingerprint()})
    print(json.dumps({"status": "initialized", "directory": str(directory),
                      "tick": 0, "fingerprint": garden.fingerprint()}, indent=2))


def advance(args):
    directory = _directory(args)
    if args.ticks < 0:
        raise SystemExit("--ticks must be >= 0 (zero means until paused/interrupted)")
    if args.delay_ms < 0 or args.checkpoint_every < 1 or args.snapshot_every < 1 or args.report_every < 1:
        raise SystemExit("delay must be >= 0; checkpoint/snapshot/report intervals must be positive")
    with base._run_lock(directory):
        garden, manifest = _open(directory)
        if garden.tick != manifest["completed_steps"]:
            raise SystemExit("Checkpoint tick and manifest differ; manual audit needed")
        if args.resume:
            (directory / base.PAUSE).unlink(missing_ok=True)
        elif (directory / base.PAUSE).exists():
            raise SystemExit("Garden paused; use `resume`, not `advance`")
        requested = args.ticks
        initial = garden.tick
        ended = "budget_completed"
        stop_requested = False
        old_handlers = {}

        def request_stop(signum, frame):
            nonlocal stop_requested
            stop_requested = True

        for signum in (signal.SIGINT, signal.SIGTERM):
            old_handlers[signum] = signal.getsignal(signum)
            signal.signal(signum, request_stop)
        _event(directory, {"kind": "advance_start", "tick": initial,
                           "requested_ticks": requested, "delay_ms": args.delay_ms,
                           "resuming": args.resume})
        advanced = 0
        try:
            while requested == 0 or advanced < requested:
                if stop_requested or (directory / base.PAUSE).exists():
                    ended = "paused"
                    break
                garden.step()
                advanced += 1
                tick = garden.tick
                base._record(directory, {"kind": "step", "completed_steps": tick,
                                         "engine_tick": tick, "metrics": garden.metrics()})
                if advanced % args.checkpoint_every == 0:
                    base._checkpoint(directory, garden, manifest, tick)
                if advanced % args.snapshot_every == 0:
                    base._snapshot(directory, garden, tick)
                if advanced % args.report_every == 0:
                    print(json.dumps({"tick": tick, "metrics": garden.metrics()}), flush=True)
                if args.delay_ms:
                    time.sleep(args.delay_ms / 1000.)
        finally:
            base._checkpoint(directory, garden, manifest, garden.tick)
            base._snapshot(directory, garden, garden.tick)
            _event(directory, {"kind": "advance_stop", "tick": garden.tick,
                               "advanced_ticks": advanced, "reason": ended,
                               "fingerprint": garden.fingerprint()})
            for signum, handler in old_handlers.items():
                signal.signal(signum, handler)
        print(json.dumps({"status": ended, "advanced": advanced,
                          "tick": garden.tick, "directory": str(directory),
                          "metrics": garden.metrics()}, indent=2))


def pause(args):
    directory = _directory(args)
    _open(directory)
    (directory / base.PAUSE).write_text("Operator requested pause.\n", encoding="utf-8")
    _event(directory, {"kind": "pause_requested"})
    print(json.dumps({"status": "pause_requested", "directory": str(directory)}))


def inspect(args):
    directory = _directory(args)
    garden, manifest = _open(directory)
    events = []
    if (directory / EVENTS).exists():
        with (directory / EVENTS).open(encoding="utf-8") as stream:
            for row in stream:
                events.append(json.loads(row))
    print(json.dumps({"tick": garden.tick, "metrics": garden.metrics(),
                      "manifest": manifest,
                      "paused": (directory / base.PAUSE).exists(),
                      "running_lock_present": (directory / base.LOCK).exists(),
                      "fingerprint": garden.fingerprint(),
                      "recent_events": events[-args.tail:]}, indent=2))


def intervene(args):
    directory = _directory(args)
    if args.learning is None and args.resource_multiplier is None and args.energy_multiplier is None:
        raise SystemExit("Specify at least one explicit intervention")
    for key in ("resource_multiplier", "energy_multiplier"):
        value = getattr(args, key)
        if value is not None and not 0. <= value <= 2.:
            raise SystemExit(f"{key} must be between 0 and 2")
    with base._run_lock(directory):
        garden, manifest = _open(directory)
        if not (directory / base.PAUSE).exists():
            raise SystemExit("Intervention requires paused world; run `pause` first")
        if garden.tick != manifest["completed_steps"]:
            raise SystemExit("Checkpoint mismatch; do not intervene")
        previous = garden.fingerprint()
        change = {"learning": args.learning,
                  "resource_multiplier": args.resource_multiplier,
                  "energy_multiplier": args.energy_multiplier}
        # Preserve the last pre-intervention visual state. A same-tick
        # intervention must not silently replace its historical snapshot.
        archive = directory / "snapshots" / "interventions"
        archive.mkdir(parents=True, exist_ok=True)
        index = int(manifest.get("intervention_count", 0)) + 1
        base._atomic_json(archive / f"tick_{garden.tick:08d}_pre_{index:04d}.json",
                          {"completed_steps": garden.tick, "garden": garden.snapshot(),
                           "fingerprint": previous, "phase": "pre_intervention"})
        # A visual snapshot cannot restore neural weights, hidden states, or
        # the RNG stream. Preserve the *full* pre-intervention checkpoint
        # before touching the current world. Recovery makes a new fork rather
        # than rewriting the historical lineage in place.
        backups = directory / "backups" / "interventions"
        backups.mkdir(parents=True, exist_ok=True)
        backup_name = f"tick_{garden.tick:08d}_pre_{index:04d}.pkl"
        backup = backups / backup_name
        if backup.exists():
            raise SystemExit(f"Refusing to overwrite existing intervention backup: {backup}")
        garden.save(backup)
        if Garden.load(backup).fingerprint() != previous:
            raise RuntimeError("Pre-intervention full-state backup mismatch; refusing intervention")
        base._atomic_json(backups / f"{backup_name}.json", {
            "tick": garden.tick,
            "fingerprint": previous,
            "checkpoint_sha256": hashlib.sha256(backup.read_bytes()).hexdigest(),
            "intervention_index": index,
            "physics_source_sha256": manifest["physics_source_sha256"],
        })
        _event(directory, {"kind": "intervention_prepare", "tick": garden.tick,
                           "previous_fingerprint": previous,
                           "reason": args.reason, "change": change,
                           "pre_intervention_checkpoint": backup_name})
        if args.learning is not None:
            garden.learning = args.learning == "on"
        if args.resource_multiplier is not None:
            garden.resource = (garden.resource * args.resource_multiplier).clip(0., 1.)
        if args.energy_multiplier is not None:
            garden.energy = (garden.energy * args.energy_multiplier).clip(0., 1.)
        base._checkpoint(directory, garden, manifest, garden.tick)
        base._snapshot(directory, garden, garden.tick)
        manifest["learning"] = garden.learning
        manifest["intervention_count"] = int(manifest.get("intervention_count", 0)) + 1
        base._atomic_json(directory / base.MANIFEST, manifest)
        _event(directory, {"kind": "intervention_applied", "tick": garden.tick,
                           "reason": args.reason, "change": change,
                           "previous_fingerprint": previous,
                           "new_fingerprint": garden.fingerprint()})
    print(json.dumps({"status": "intervention_applied", "tick": garden.tick,
                      "change": change, "fingerprint": garden.fingerprint(),
                      "pre_intervention_checkpoint": backup_name}, indent=2))


def restore_fork(args):
    """Recover an exact pre-intervention state as a NEW paused branch.

    Never roll back an existing live world in place. Pickle input is restricted
    to backup files produced by our own intervention command and is still
    trusted local code-executable data, not safe for untrusted imports.
    """
    source = _directory(args)
    destination = Path(args.destination).expanduser().resolve()
    if Path(args.backup).name != args.backup:
        raise SystemExit("--backup must be the basename shown by intervene")
    backups = source / "backups" / "interventions"
    checkpoint_path = backups / args.backup
    meta_path = backups / (args.backup + ".json")
    if not checkpoint_path.is_file() or not meta_path.is_file():
        raise SystemExit("No matching local full-state intervention backup and metadata")
    if destination.exists() and any(destination.iterdir()):
        raise SystemExit("Restore destination must be empty; refusing overwrite")
    with base._run_lock(source):
        _, current_manifest = _open(source)
        meta = base._json_dict(meta_path)
        if meta["physics_source_sha256"] != current_manifest["physics_source_sha256"]:
            raise SystemExit("Backup physics lineage mismatch")
        if hashlib.sha256(checkpoint_path.read_bytes()).hexdigest() != meta["checkpoint_sha256"]:
            raise SystemExit("Backup SHA-256 mismatch; refusing load")
        garden = Garden.load(checkpoint_path)
        if garden.fingerprint() != meta["fingerprint"] or garden.tick != meta["tick"]:
            raise SystemExit("Backup state fingerprint or tick mismatch")
        destination.mkdir(parents=True, exist_ok=True)
        restored_manifest = dict(current_manifest)
        restored_manifest.update({
            "completed_steps": garden.tick,
            "learning": garden.learning,
            "created_unix": time.time(),
            "intervention_count": max(0, int(meta["intervention_index"]) - 1),
            "parent": {"directory": str(source), "backup": args.backup,
                       "tick": garden.tick, "fingerprint": garden.fingerprint()},
        })
        base._checkpoint(destination, garden, restored_manifest, garden.tick)
        base._snapshot(destination, garden, garden.tick)
        (destination / base.PAUSE).write_text("Restored fork starts paused.\n", encoding="utf-8")
        _event(destination, {"kind": "restore_fork_init", "tick": garden.tick,
                             "parent": restored_manifest["parent"]})
        _event(source, {"kind": "restored_fork_created", "tick": garden.tick,
                        "backup": args.backup, "destination": str(destination)})
    print(json.dumps({"status": "restored_fork", "tick": garden.tick,
                      "directory": str(destination),
                      "fingerprint": garden.fingerprint()}, indent=2))


def fork(args):
    source = _directory(args)
    destination = Path(args.destination).expanduser().resolve()
    if destination.exists() and any(destination.iterdir()):
        raise SystemExit("Fork destination must be empty; refusing overwrite")
    with base._run_lock(source):
        parent, manifest = _open(source)
        if not (source / base.PAUSE).exists():
            raise SystemExit("Pause parent before forking to preserve exact lineage")
        destination.mkdir(parents=True, exist_ok=True)
        child_manifest = dict(manifest)
        child_manifest["parent"] = {"directory": str(source),
                                     "tick": parent.tick,
                                     "fingerprint": parent.fingerprint()}
        child_manifest["created_unix"] = time.time()
        base._checkpoint(destination, parent, child_manifest, parent.tick)
        base._snapshot(destination, parent, parent.tick)
        (destination / base.PAUSE).write_text("Fork starts paused.\n", encoding="utf-8")
        _event(source, {"kind": "forked", "tick": parent.tick,
                        "destination": str(destination),
                        "fingerprint": parent.fingerprint()})
        _event(destination, {"kind": "fork_init", "tick": parent.tick,
                             "parent": child_manifest["parent"]})
    print(json.dumps({"status": "fork_created", "destination": str(destination),
                      "tick": parent.tick, "fingerprint": parent.fingerprint()}, indent=2))


def main(argv=None):
    parser = argparse.ArgumentParser(description="Persistent, pauseable Neural Garden")
    cmds = parser.add_subparsers(dest="command", required=True)
    p = cmds.add_parser("init")
    p.add_argument("--directory", required=True)
    p.add_argument("--seed", type=int, default=37)
    p.add_argument("--size", type=int, default=16)
    p.add_argument("--no-learning", action="store_true")
    p.set_defaults(func=initialize)
    for name in ("advance", "resume"):
        p = cmds.add_parser(name)
        p.add_argument("--directory", required=True)
        p.add_argument("--ticks", type=int, default=100,
                       help="0 means run until pause or signal; foreground only")
        p.add_argument("--delay-ms", type=float, default=0.)
        p.add_argument("--checkpoint-every", type=int, default=25)
        p.add_argument("--snapshot-every", type=int, default=25)
        p.add_argument("--report-every", type=int, default=100)
        p.set_defaults(func=advance, resume=name == "resume")
    p = cmds.add_parser("pause")
    p.add_argument("--directory", required=True)
    p.set_defaults(func=pause)
    p = cmds.add_parser("status")
    p.add_argument("--directory", required=True)
    p.add_argument("--tail", type=int, default=8)
    p.set_defaults(func=inspect)
    p = cmds.add_parser("intervene", help="Recorded changes to a paused world")
    p.add_argument("--directory", required=True)
    p.add_argument("--reason", required=True)
    p.add_argument("--learning", choices=("on", "off"))
    p.add_argument("--resource-multiplier", type=float)
    p.add_argument("--energy-multiplier", type=float)
    p.set_defaults(func=intervene)
    p = cmds.add_parser("fork", help="Branch paused checkpoint into an independent world")
    p.add_argument("--directory", required=True)
    p.add_argument("--destination", required=True)
    p.set_defaults(func=fork)
    p = cmds.add_parser("restore-fork", help="Restore a pre-intervention full backup into a NEW paused world")
    p.add_argument("--directory", required=True)
    p.add_argument("--backup", required=True, help="Backup basename reported by intervene")
    p.add_argument("--destination", required=True)
    p.set_defaults(func=restore_fork)
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
