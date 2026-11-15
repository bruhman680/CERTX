# Prospective retrieval transfer and a prepared main-continuation choice

15 November2026 UTC. **Eight new local model replies**, eight additional executions of their unchanged text on paired nonce worlds, zero training updates. The selected main remains **1580**, paused; all823 canonical non-cache files unchanged. The requested main50 has **not** run, because it needs a changed input-continuity policy under the frozen current contract.

## Question and design

The preceding history/retrieval study demonstrated one working hidden-file read under merged JSON task framing. That was a capability witness, not evidence that the procedure generalizes to even nearby tasks.

Before inference, `PLAN.json` fixed the full2×2×2 matrix: two filenames (`probe_value.json`, `sample_record.json`), two field names (`value`, `signal`), and two layouts (fresh empty-assistant role-shell JSON, initial framing and JSON task merged into one user message). Exact task wording only substitutes the filename/key. Each branch receives one reply, no hint or corrective followup.

New values are `N4C8P2` and `H9D3L7`. Each of eight model replies is generated on an A world, then its full unchanged notebook text is executed on a paired B world. This gives eight model calls, eight model-action notebook executions, and eight **additional artifact executions**. B is not another model sample. Prose/empty/incomplete replies remain outcomes and still pass through the same literal notebook mechanism.

Physical fixture pairs differ only in target-file nonce bytes. When renaming the file, preparation removes the old `probe_value.json`, so stale source content cannot mask a wrong filename. The only common mechanical change is a declared diagnostic transport appendix. All other supported files, model/decoder settings, parser and execution laws are fixed. No expected value is in any model input.

Body is the same cached SmolLM2-135M-Instruct revision `12fd25f77366fa6b3b4b768ec3050bf629380bac`, float32 CPU/eager/two threads, greedy256, fresh KV. Tensor digest is checked unchanged. No remote model endpoint, adapter or training is involved.

## Outcomes

| Requested file / key | Role-shell JSON | Merged JSON |
|---|---|---|
| probe_value.json / value | Echoed task JSON; no cell | Correct hidden-file read; labeled correct stdout |
| probe_value.json / signal | Echoed task JSON; no cell | Wrong `/world.json` path; FileNotFoundError |
| sample_record.json / value | Echoed task JSON; no cell | Passes an invented JSON string to `json.load`; AttributeError |
| sample_record.json / signal | Echoed task JSON; no cell | Unclosed code fence at256-token limit; no execution |

The successful merged original-file/original-key branch prints:

- A actual stdout: `The value field in probe_value.json is: N4C8P2`
- B unchanged-artifact stdout: `The value field in probe_value.json is: H9D3L7`

The hidden nonce does not occur in generated source. Its procedure opens the requested file, parses JSON and extracts `value`. Changing only actual file bytes changes actual stdout. This confirms the saved program's file dependence with new values. The baseline prompt is identical to the earlier merged-JSON task, so deterministic regeneration is a reference replication, not an independent sample of reasoning diversity.

The changed-field merged branch prints `Reading signal field...` before attempting `/world.json` and exiting1. It also defines an unused function indexing `signal_field`, rather than the requested `signal`. That extra latent mistake was not the executed cause of failure: the wrong path fails first. We do not repair it or infer the result of unexecuted code.

The renamed-file/value branch invents an example object about a person/address, then passes that string to `json.load`, which requires a file-like object. It exits1 with `AttributeError: 'str' object has no attribute 'read'`. Explanatory prose claiming that it loaded the file is not an execution result.

The renamed-file/signal branch begins a plausible function that would open `sample_record.json` and extract `signal`, but drifts into a long invented example. Its fence remains incomplete at the output limit, so no Python cell executes. We preserve the original text and do not close or promote that code afterward. This is a generation-completion outcome, not a sandbox rejection.

All four role-shell branches copy the task JSON and stop at EOS. Their paired B executions likewise contain no executable cell. The three failed merged procedures remain failures on their paired B worlds. Only one of eight generation conditions returns the requested value in actual stdout; **none** returns bare exact-value stdout because the successful program adds a label. These counts describe this declared tiny matrix, not a population performance estimate.

## What this changes in our understanding

The earlier local capability witness survives a change of file contents. It does **not** carry across these filename/key substitutions under the tested contexts. Useful distinctions are now visible: request copying, correct read/extraction, incorrect path binding, wrong parser input type, and incomplete code emission. None should be collapsed into “the model cannot use tools” or “the interface works reliably.”

The garden's same physical door can support a correct act, but the procedure chosen around it remains fragile. Bigger or longer runs alone do not resolve which task elements are bound to which operations. All interpretations remain external; no grades, repaired examples or preferred behavior were inserted into the selected main world.

No generalization claim follows from one body, eight deterministic inputs and a two-value artifact check. Name substitutions can change tokenization and learned associations as well as meaning. Layout changes length, roles and task position together. Paired artifact executions demonstrate the generated program, not a second independent model solution. Source inspection and actual receipts support the failure attribution; no external read tracer was installed.

## Requested next main50: exact readiness and remaining decision

The user requested these tests followed by50 more main entries. Read-only preparation confirms the selected main's next full-history input has **8104 tokens**, beyond its **7936-token input bound**. The current `minimal-garden-candidate-v1/CONTRACT.json` explicitly requires:

> “Initial mechanics/invitation once, then all actual candidate conversation in chronological native roles. No selected replay window, repeated directory observations, summaries or hidden pruning. Honest capacity pause before exact input exceeds7936.”

Running the unchanged main runner cannot generate the requested next entry. We did not waste a model load or add a zero-call session merely to repeat that known check, nor silently activate the detached prototype.

`main50-proposal/` contains a concrete proposed smallest change:

- Preserve the entire original main1580 checkpoint and all historical records.
- Continue from that actual world in a newly linked version, with original initial framing plus the latest eight complete assistant/actual-receipt pairs.
- The exact next input is saved in `EXACT_NEXT_VIEW.json`: entries **1573–1580**, **2231 tokens**, omitting1551–1572 from immediate input while preserving their authoritative records and existing notebook writing. This is the current phase's history, not all historical seasons.
- Use the already tested content-independent selector; oldest whole-pair fallback only if needed, latest pair never truncated, capacity pause if mandatory framing/latest pair cannot fit.
- Append the exact proposed mechanical continuity declaration to `WORLD_RULES.txt` in the **new** world only, explicitly superseding older full-history input wording. No new archive-copy directory or automatic copies are bundled into this proposal.
- Same model, decoder, seed, parser, physical limits and actual consequence feedback. No file-reading diagnostic task is imported into open exploration.
- Requested next entries would be1581–1630, checks/reports every10. Detached prototype1581–1583 are not promoted or relabeled as main history.

This proposal is **not activated**, and a reusable linked main runner has not yet been built or claimed verified. The exact view and policy are reviewable now; once the user chooses the changed input continuity, implementation/verification must precede those50 model calls. The old main remains untouched meanwhile. Permission to continue a run is not treated as a silent choice between the full-history and bounded-view experimental conditions.

## Integrity and records

`AUDIT.json` passes: all exact input token IDs and decoded texts recompute; target nonces are absent from prompts; pre-model pairs differ only in target bytes; renamed fixtures have no stale old filename; all16 detached stores verify; the additional executions use exactly the saved model text; no model operation writes another supported path besides its literal notebook append. Main823-file inventory matches its before hashes; weights are unchanged and no pending outcome remains.

Two read-only preparation/check scripts initially used the wrong host Python environment or CAS lookup convention. They failed before changing a fixture or executing model actions. Both were corrected to the cached model environment and existing base64 JSON object format; no inference or actions were rerun. These were observer tooling errors, not small-model outcomes.

Records: `PLAN.json`, `jobs/`, `preparation/`, `results/`, `transfers/`, `worlds/`, `AUDIT.json`, and `main50-proposal/`. Raw errors and unfinished replies are preserved. Previous navigation records are copied unchanged under `before/` before sync.

Strong next diagnostic if pursued: distinguish correct path/field binding from syntax/completion, using a few predeclared held-out tasks rather than tuning these failures into answers. The main continuation's memory-policy choice remains separate from that diagnostic work.
