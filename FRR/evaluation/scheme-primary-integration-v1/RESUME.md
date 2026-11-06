# Continue this same garden

This is an extension of the original continuing garden at entry 500. The original event sequence, notebook, model and canonical adapter continue. The Scheme calibration worlds remain test benches; none was imported into the primary.

The active runner is `connected_routine_v2.py` in this directory. Do not use the frozen older `world_routine.py`, or this directory's first `connected_routine.py`, for future live steps. V1 was stopped at resume preflight before any model call because it incorrectly protected the removable PAUSE marker. Both the code and failed record remain available. V2 treats that operational marker as mutable; old event, plan, source, seed and session files remain protected.

## Normal five-entry continuation

Use the cached environment, without model downloads or paid APIs:

```sh
PY=/workspace/cache_backend_venv/bin/python
RUN=/workspace/frr/evaluation/scheme-primary-integration-v1/connected_routine_v2.py
$PY "$RUN" verify
$PY "$RUN" resume
$PY "$RUN" run --steps 5
$PY "$RUN" verify
```

Each run pauses itself after at most five replies. Check its result and CURRENT_VERIFY before continuing. The user has authorized continuation, not erasure of history or replacement of the original garden. A new wider cadence would still contain checked windows.

## Before running

The live SQLite file must exist at `source-access-three-cycle-v1/cycle3/environment/scheme_world/world.sqlite`. Do not create an empty database to replace a missing one. Portable JSON bundles retain the complete world state and request/audit history independently of this local database. Verify that the last after-bundle, or genesis at cursor 500, reproduces the live state. The integrated verifier does this comparison. Stop on a failed verification rather than arming another run.

The run's input is the original last-twelve-entry view, archive access, seed shelf, user message, play charter, generation boundary and number patch, plus the Scheme workspace panel. The entire reply beginning with `(` is a Scheme submission. Prose and existing commands go through the old dispatcher. No extraction, delimiter repair, forced decoding, target answer or automatic inference retry occurs.

## If interrupted

Do not delete a prompt plan, raw generation, event, receipt, session record or lock without inspecting what happened. Check whether a lock holder is actually alive. Request IDs are `primary-<absolute step>`. A saved raw generation precedes execution; the same request ID/source/expected snapshot retrieves an existing terminal receipt instead of executing it again. The `recover` action completes a saved raw generation without another model call, but its explicit session-accounting instruction must be followed. It is not a general repair for a missing raw output or an unknown host commit.

Unknown commits pause; they are not assigned a result. Recovery of an admitted but interrupted Scheme computation may record an abort, rather than resume the guest evaluator. No claim is made that wall-time aborts have deterministic counterfactual replay.

The earlier unknown attempt at old step 492 remains unknown. These connection checks do not resolve it.

## Portability

Export/import helpers are in `computational-world-portability-v1/prototype/world_bundle.py`. Import a saved bundle to a **fresh** database path using the pinned profile in `ENVIRONMENT_SCHEME_V2.json`, then verify integrity and byte-identical export before placing it into service. Bundles are data, not SQL or guest host code. Keep the original notebook, plans, raw outputs, manifests, sources and adapter provenance with them. The local SQLite and owner-lock files are working storage and are excluded from Git publication; all settled bundles and new entry records are published.
