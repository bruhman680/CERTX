# Current primary garden: same history, play extension

Primary directory remains `cycle3/environment`. Current runner is `play.py`. This is the same garden that reached entry 51, with a user-requested, documented charter/tool extension at that step. No earlier event or history was reset. ENVIRONMENT_PLAY.json links the original ENVIRONMENT.json and pins the charter/tools. Events identify which environment version generated them; verification reconstructs each version's actual prompt and dispatch.

Current controls from the study directory with the existing local venv:

- Inspect `cycle3/environment/STATE.json`, both environment manifests, and `cycle3/CURRENT_VERIFY.json`.
- `python play.py pause`: ask to pause after the current complete call.
- `python play.py resume`: arm resumption without launching inference.
- `python play.py run --steps N --delay D`: bounded foreground work on the SAME cursor (1-20 replies, 0-45 second pacing). No new notebook or session seed reset; automatically pauses after the window.
- `python play.py verify`: create another immutable verification snapshot covering all versions, with CURRENT_VERIFY as latest pointer.

Do not use the obsolete `study.py run 3` or the original `continuous.py run/verify` after the play extension. They are historical implementations retained for audit. Do not re-run init or choose a new branch because current replies are repetitive. Further diagnostic experiments belong outside this garden.

Stable current affordances: optional free text, READ SETUP/CLAIM, NOTE <text>, READ NOTES, TRY <bounded arithmetic>. Notes are unverified model content. Calculator results have narrow arithmetic scope and are not task success scores. Full replies and typed actual host results are retained. PLAY_CHARTER.md is the actual appended instruction; tools and exploration are optional, with no required repair/novelty/progress output.

Input allowance stays 6144; output cap 96; fixed canonical model and sampling, neutral feedback, no online training. The optional charter and tools are an explicit version change, not unchanged-condition data. Keep the current setup stable over future windows to observe trajectories. Pausing/slowing is outside the model's prompt. Temporary inference state may restart; the external environment/history/cursor persists. No background inference after the declared window.
