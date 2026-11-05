# A small discoverable world, built beside the continuous garden

5 November 2026. **Prepared and host-tested; not activated in the real primary. No model generation or training in this contact.**

The current garden remains paused at entry **305**, active runner `boundary_routine.py`, version `generation-boundary-view-v1`, verification `0055`. This build does not replace that garden or put demonstration actions into its history.

[Evidence and design overview](OVERVIEW.md) explains which prior observations motivated the change. [Host tests](HOST_TEST_LOG.txt) and [integration checks](INTEGRATION_CHECKS.json) establish the narrower implementation result.

## The patch

The world contains an integer in −8 through 8 and two objects, A and B. Initial state is 0. Its controls are `LOOK`, `TOUCH A` and `TOUCH B`. One complete command is accepted per generated reply. Ordinary writing and the existing tool dispatcher remain available. Malformed world commands return a factual grammar receipt without changing the number. Case and surrounding whitespace are tolerated. Commands quoted or narrated inside ordinary prose do not execute.

Observer-known rules:

* LOOK observes without changing state.
* A adds one, except at 8, where it is blocked and leaves the number unchanged.
* B changes the sign. At 0 it is accepted and unchanged.

The model-facing view states the current number, range, objects, grammar, persistence and absence of a target or score. It supplies no formulas or worked examples. The model can revisit and compare consequences, or ignore the patch. Rules are deterministic; the model still samples its own replies. All 17 states are mutually reachable. B applied twice returns the original number. Order can matter: from 0, A then B gives −1, while B then A gives 1. These are properties of the host world, **not discoveries made by the model**.

The range is a deliberate small-world boundary, not a model usage quota or monetary pressure. There is no model-accessible reset, reward or enforced exploration agenda. The user's existing curiosity sentence and seed shelf are retained unchanged.

## Persistence without a second live authority

[world.py](world.py) defines pure transitions. [primary_adapter.py](primary_adapter.py) provides the integration bridge. On eventual introduction, the primary's immutable action receipts will be the authority for the world's state. The bridge replays only entries at or after an explicit activation boundary. It rejects missing, forged, stale or rule-mismatched receipts. Earlier prose and earlier legacy actions cannot silently become new world actions.

A new action's state transition is stored in the same primary event as its generated reply. If the process stops before the event commits, no world action has committed. If it stops after the event commits but before a derived view updates, replay recovers the action once. There is no independent live world-state journal to get ahead of or behind the garden notebook.

[journal.py](journal.py) and [world_cli.py](world_cli.py) instead supply an explicitly separate host-only demo/fixture journal. Its hash chain and immutable event creation let us test persistence and interrupted projections. Its demonstrations are never imported into the primary. A hash chain detects inconsistency against its configuration; hashes do not prove semantic accuracy or defeat an adversary rewriting every authority.

## Prepared integration

[prepare_primary.py](prepare_primary.py) defaults to a read-only plan. It checks the exact paused 305 boundary, saved passing verification and frozen bundle. Explicit activation would create a new manifest, new frozen runner and new policy freeze without replacing older source files. Repeated activation refuses overwrite/reinitialization. Activation itself keeps the garden paused and does not generate a model reply.

[prepared_world_routine.py](prepared_world_routine.py) is the generated candidate for the actual primary location. It is an inspection artifact, not the active runner. It retains the legacy renderers/dispatchers so previous prompts and action results continue to verify under their original versions. Existing old runners must remain available for replay. The prepared artifacts use this workspace's absolute paths; a restored workspace must deliberately rebuild its path configuration rather than assuming the candidate is portable unchanged.

## Validation

Eight host test groups passed:

* Exhaustive independent expected-result checks for 17 states × 3 valid controls, including blocked and accepted-unchanged outcomes.
* Reachability from every state to every state, B's double-application identity and an order-sensitive example.
* Grammar and invalid/prose handling, strict state/rule validation and a model view without transformation formulas.
* Durable replay and projection recovery after an injected post-commit failure, including missing/corrupt derived STATE.
* Event overwrite refusal, repeat initialization refusal, write-lock enforcement and event/configuration tampering detection.
* Bridge delegation to old tools, unchanged legacy history, actual-receipt replay and rejection of forged/stale/missing receipts.

An isolated copy of the primary replayed all **257 saved generations plus 48 origin entries** under the prepared runner. Its temporary verifier advanced to 0056; **the real verifier stayed 0055**. All cloned raw event bytes matched the source. Repeated installation in the clone refused reinitialization. This fixture was disposed of after testing.

A cached-tokenizer-only preview of the next input used **3175 / 8096** allowed input tokens. This was not a model call. The preview's initial world number is 0 and is explicitly a future condition, not current primary experience.

The integration check compared **908 primary-study files**, excluding generated Python bytecode, before and after. All bytes and file membership were unchanged. A separate final comparison against the pre-build inventory is in [PRIMARY_PRESERVATION.json](PRIMARY_PRESERVATION.json).

## Limits and next contact

No claim of reasoning improvement, environment recognition, emergent phase, emotional state, curiosity or learning follows from these host checks. The model may repeat examples, write fiction, ignore the objects or fail the grammar. Those outcomes should be preserved rather than replaced by successful reruns. An action sequence alone would not establish an internal rule representation; a later predeclared prediction or transfer probe could provide stronger evidence if naturally warranted.

The next practical contact is a **versioned introduction into the same continuing primary**, followed by ten entries in two five-entry integrity windows. Keep all raw events, summarize broadly, and zoom in on actual changes or failed actions. Do not enlarge to another 100-entry block before checking the introduction. This initial contact observes use and failure modes; it is not a controlled performance claim. No additional approval is required by the implementation; this contact stops at a concrete prepared build to keep the environment change and first model exposure separately recorded.

If the primary advances before introduction, the installer deliberately refuses its old 305 plan. Prepare a new explicit boundary rather than resetting or substituting a new primary. If an installation is interrupted, keep PAUSE in place and inspect existing artifacts before any recovery; do not blindly rerun or delete history.

## Does this overwrite the garden?

**No.** The old garden, earlier seasons, raw events, plans, prompts and source versions remain intact. The current navigation files are refreshed, with their previous bytes archived under [before/](before/). The new demo is a separate plot. A later introduction would append a versioned change to the same continuing garden, not replace its past. Derived state and current pointers may then update as projections of preserved history; immutable source events do not get rewritten.
