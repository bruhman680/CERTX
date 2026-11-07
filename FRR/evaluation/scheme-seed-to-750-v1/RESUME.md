# Continue the original garden after the user seed

Use `seeded_routine.py` in this directory. Old runners and manifests remain historical; the current pointer is `source-access-three-cycle-v1/cycle3/environment/ACTIVE_RUNNER.json`.

```sh
PY=/workspace/cache_backend_venv/bin/python
RUN=/workspace/frr/evaluation/scheme-seed-to-750-v1/seeded_routine.py
$PY "$RUN" verify
$PY "$RUN" resume
$PY "$RUN" run --steps 10
$PY "$RUN" verify
```

A window may end early for a non-note event. Inspect the actual receipt and following state before continuing. For this planned block, `run_block.py` stops at 750. It refuses to continue past an unresolved `ATTENTION_<window>.json`; the observer writes the matching `ATTENTION_<window>_REVIEW.json` after inspecting the event. Ordinary note text can continue without a manual review.

The live SQLite file must exist. Verify before arming. Do not replace a missing persistent world with an empty one; reconstruct the last settled portable bundle into a fresh path and verify it before use. The seed adds no runtime permissions, paid API, downloads or training.

Raw generation precedes side effects. Request IDs remain `primary-<absolute step>`; explicit recovery must use retained source/ID/expected snapshot, never silently regenerate. Unknown commits stop for inspection. Do not delete plans, raw outputs, locks, events or sessions to make a retry pass. No request is made to retroactively resolve the old step-492 missing output.

For past-phase details see `../scheme-primary-integration-v1/RESUME.md`. The Scheme activation remains 500; the new seed activation is 650 / human entry 651. The new runner maps earlier entries to their original manifests and prompt renderings. All later seed amendments must likewise be versioned.
