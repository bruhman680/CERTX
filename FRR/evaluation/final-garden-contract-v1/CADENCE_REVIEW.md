# External cadence and continuation review

Read-only code review by observer_cadence_review, 7 November 2026. Inspected the preceding world/runtime/runner and the new final-contract runner, generation wiring and contract. No model calls, state migration, configuration changes or live-world changes were performed by this reviewer. This document is the sole reviewer-authored artifact.

## Initial requested routine

The latest authorized block is 100 entries: **851–950**, following the preserved total of 850. Default integrity checks are every ten entries, giving 860 through 950. Default reports are every fifty entries, giving 900 and 950. A final check and a partial summary also apply if the block stops early. No result, action, novelty or phase transition is required to reach the next entry.

Every entry retains raw generated text and tokens, exact native messages, action/storage results, before/after world identities and externally stored content objects. Wider reports are not evidence downsampling. Quiet intervals remain recoverable for later comparison.

## Confirmed observer separation

The new runner supports explicit bounded start/resume blocks, up to 250 entries, rather than requiring another redesign for the next continuation. It accepts external integrity intervals of one through ten and report intervals of fifty or one hundred. Session plans record these choices. No such observer choice changes the frozen model, sampling, memory policy, action grammar, world limits or seed.

A shell action, actual environmental error, or non-notebook checkpoint delta triggers immediate checking plus five following entry checks. Additional external zoom requests are consumed once and restricted to at most five entries including their current entry; invalid requests are recorded externally and do not become model feedback. Non-notebook deltas include indirect modifications through a model-created notebook alias. The trigger is not a requirement that the action succeed.

For text-only changes, the external observer can inspect surrounding entries and request a bounded zoom. Labels such as stable, unstable, lull or phase remain provisional descriptions, not automatically inferred internal states. Reporting may widen after sustained comparable windows, while preserving all raw data; ten-entry integrity remains the initial baseline. No automatic block extension is present.

## Preservation and input continuity

Preparation requires a paused, settled parent at 850, without an outstanding action or lock. It copies the final 850 bundle byte-for-byte, carries its stored objects forward, then restores/captures it to check identity. Existing notebook and prior-replies bytes are not rewritten or replaced by probe results. Frozen inventories protect both earlier phases.

The first new input retains entries 839–850 as native assistant turns and their actual consequences as user feedback. An explicitly empty first system message prevents the tokenizer from inserting its factory behavioral header. The only fixed invitation is the agreed curiosity seed; the remainder describes mechanics and current directory facts. Observer interpretations, attention requests and report fields are not inserted.

Native message reconstruction, tokenizer IDs and stop checks are included in validation. The longer mutable notebook and the immediate externally retained twelve-reply context remain distinct, explicitly declared memory surfaces. The first is available through actions; the second is replayed as recent experience.

## Lock and interruption review

The initial reviewed runner acquired a lock late and cleaned it up unconditionally. Concurrent invocations with different block targets could therefore interfere: the losing invocation could pause the winning run and remove its lock. This issue was reported before preparation/activation.

The revised runner acquires an exclusive ownership-token lock before model/session side effects. Failed acquisition does not enter owner cleanup. The outer cleanup covers startup, model loading and initial-world failures and only updates pause/lock state if the token still belongs to that invocation. Session attempt IDs are unique, retaining failed starts rather than overwriting them.

A plan and durable PENDING record precede generation. Exact raw output is retained before dispatch. Results, bundle, event and state are committed before removing PENDING. Resume refuses an outstanding pending attempt or next-entry plan; it never silently repeats generation or execution. Unknown outcomes require an explicit recovery investigation. Ordinary known shell errors are not semantic rejections or approval gates.

The root active-phase pointer must be archived and updated externally before inference. The runner verifies that it identifies this phase and its state. Earlier stages remain lineage parents rather than being renumbered or relabeled as new experience.

## Scope of a fixed universe

The inherited no-truncation input boundary remains 8096 tokens. Large action outputs can make even the recent twelve-turn window exceed that limit; the fixed runner then pauses. This is an explicit capacity boundary, not permission for a later silent compression or framing change. No new fit-to-context memory policy was introduced.

Checkpoint continuity preserves supported file contents, types, permission bits and links. It does not promise original inode numbers, timestamps, processes, temporary files or a retained model KV cache. Unsupported or unreadable checkpoint state causes an explicit integrity stop. Guest content must not be silently chmodded, deleted, repaired or replaced to make reconstruction pass.

Read-only review does not establish every possible Linux workload or an aggregate cgroup memory bound. Existing resource and checkpoint limitations remain declared in the contract. Once the final configuration is activated, an infrastructure fault or needed universe change must be recorded as an interruption/new condition rather than hidden redesign.

The same checkpoint decoder is used for restore checks. Fresh-mount reconstruction and separate byte verification are useful integrity evidence, not an independently implemented model of filesystem semantics or proof of the small model's reasoning ability.
