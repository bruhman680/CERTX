# Persistent small-garden environment v1

Primary environment: `environment/`. Authoritative identity/settings are in ENVIRONMENT.json. The original 48-entry tools_optional_1201 notebook is immutable ORIGIN.jsonl. Immutable committed outputs are events/<absolute-step>.json; immutable planned inputs are plans/<absolute-step>.json. STATE.json and NOTEBOOK.jsonl are rebuildable projections, not substitutes for the event journal. Each model output retains the actual host receipt separately from generated text.

This is one continuing EXTERNAL environment across bounded foreground sessions, not one permanently running inference process or online weight learner. The model recomputes from the whole notebook each call. Pause/resume and delay controls are outside its prompt. Reader, source data, renderer, neutral feedback and model remain pinned. No diagnostic answers or root judgments enter this notebook.

From the study directory, using the existing local venv:

- Inspect `environment/STATE.json`, `environment/ENVIRONMENT.json`, and CURRENT_VERIFY.json first.
- `python continuous.py pause`: request a pause between complete model calls. An active call may finish and commit first.
- `python continuous.py resume`: clear the pause request; this does NOT launch inference.
- `python continuous.py run --steps N --delay D`: run a finite window (1-20 replies, delay 0-45 seconds between calls). Does not reset history or reseed by session. Automatically pauses afterward.
- `python continuous.py verify`: reconstruct every committed event and create a NEW immutable verification snapshot. CURRENT_VERIFY.json points to the latest snapshot; the initial CHECKS/SUMMARY/EVENT_INDEX files remain historical.

There is no background daemon. A later authorized session can resume this same directory and cursor. Do not re-run init, delete origin/events, substitute a fresh notebook or merge other branches into it. Use separately named experiments if changing sources, prompts, rewards, model or memory representation. Before any change to the 6144 input allowance or 96 output cap, declare a new environment version. An input boundary saves the planned prompt and stops; it is not evidence of an intrinsic cognitive limit.

A RUN.lock prevents concurrent writers. An uncommitted prompt plan halts a subsequent call for inspection rather than automatic retry. The event is the commit point; stale cursor/notebook projections can be rebuilt without rewriting committed events. Tests cover immutable event protection, stale-cursor recovery, and separation of pause control from notebook/prompt content. Filesystem-level atomic operations are not an independent backup/restore or power-loss guarantee.

Initial demonstration inside amended cycle 3: one reply, verified pause, then two more replies under the same environment fingerprint and global step sequence. These operational windows are parts of a single trajectory. Cycles 1 and 2 remain separate diagnostics and never become this trajectory's experience.
