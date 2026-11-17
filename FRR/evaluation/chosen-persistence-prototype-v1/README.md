# Current checkpoint: candidate turn13

17 November2026, America/Chicago. The same candidate completed ten further replies4–13 with contract unchanged. All copied the latest supplied packet and ended at EOS. World remains empty/step0; no code or automatic world notes. Main1630 remains preserved. [Continuation report](../chosen-persistence-continuation-v1/REPORT.md), [current handoff](NEXT_SESSION.md). Exact next input2177/7936tokens; a proposed next window up to25 is not queued.

Original build and initial-pilot documentation follows; its three-reply observations refer to turns1–3.

---

# Chosen-persistence computational garden prototype

Built16 November2026, America/Chicago. Target: the user's newer **pretrained model + FRR world**. Main1630 and all prior history remain unchanged. This is a fresh detached candidate with its own turn count, not main entry1631 or a reset of the original run.

The world is a persistent writable filesystem with a bounded Python/shell runtime. The model can express programs and create its own files. Ordinary writing is retained by observers outside the world and has no automatic filesystem effect. There is no required task, puzzle, workflow, reward, performance gate or autonomous world clock. Exact FRR/mechanics, initial state, observation and history policy are frozen in candidate/CONTRACT.json and PROTOCOL.md.

## What is working

- Complete exact Python/shell fences execute literally; prose/unknown/incomplete fences remain writing. The parser and physical runtime are pinned existing machinery, not new semantic command extraction.
- Explicit writes persist; actual errors return and do not gate later lawful cells. Observer logs stay external. No automatic notebook file or mandatory artifact organization.
- Known batch prefixes can be explicitly sealed after inspection without replaying committed effects. Unknown individual operations block that recovery. Tested interruption windows preserve committed state and distinguish a saved final record from an incomplete batch.
- A continuous model-session controller retains exact native-role history and actual world state over normal pause/resume. Full input is bounded7936tokens; no hidden pruning. Full directory observations have an8192-byte complete-or-pause bound.

## Actual checks and pilot

Nine operator-only mechanics checks passed, plus one final-record cleanup-window check. These use real sandbox operations and injected logical interruptions. They do not prove every host-crash/power-loss case. Fixtures contain operator test files, but none was copied into the candidate.

The fresh candidate started with **zero world files** and the exact archived compact FRR adaptation in system context, alongside mechanical laws. The full FRR source is retained externally; compact exposure is not neural installation. Three cached135M replies ran as budgets1 then2 on the **same** candidate. Pause/resume history joins, world state, raw tokens, observations/receipts, main/source pins and weights verify. See PILOT_SUMMARY.json and candidate/audits/.

Replies copied the latest supplied structured message and ended at EOS:34,52,52tokens. Inputs719,814,927tokens. Zero executable cells, zero model-created world files, zero automatic world notes. The empty world ID stayed fixed while external conversation history grew. This is not proof of FRR benefit, learning, an attractor or a capability ceiling. No behavior-dependent repair or prompt change followed these outcomes.

## Resume this candidate

From the same workspace:

```sh
/workspace/cache_backend_venv/bin/python /workspace/frr/evaluation/chosen-persistence-prototype-v1/session.py audit
/workspace/cache_backend_venv/bin/python /workspace/frr/evaluation/chosen-persistence-prototype-v1/session.py run --budget 10
```

Audit is read-only apart from its new external audit record. Run advances from the actual saved candidate turn; it does not prepare/reset a world. No run is scheduled automatically. A PAUSE_REQUEST file cooperatively stops before another call; explicit operator review/removal is needed before continuing after that request. Input/observation capacity or unresolved transaction state requires an explicit design/reconciliation decision, not quiet truncation or replay.

Do not rerun prepare against candidate, clear pending markers to force replay, or call legacy receive_notebook on this engine. The authoritative coupling is coupling.py plus world/COUPLING.json. It uses pinned engine transaction internals; it is not a generic unversioned API. The underlying engine manifest retains legacy capability descriptions, while the outer coupling specifies which interface is used here.

The intentionally blocked unknown-marker fixture is at checks/attempt001/unknown_marker. Its synthetic marker represents no actual attempted action and is retained as test evidence. It is not an unresolved live candidate transaction. Candidate is currently cleanly paused at turn13 with no pending marker or lock; the initial pilot below remains historical.

World-level prefix recovery does not by itself reconcile an interrupted model-session transaction. session.py intentionally blocks unknown session outcomes for explicit forensic review; it does not automatically regenerate a reply or replay an action. Complete external records and preserved raw outputs make that distinction inspectable. No blanket completeness claim is made for uncheckpointable OS state.
