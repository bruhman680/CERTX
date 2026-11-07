# Final world/input contract review

Read-only review by final_world_review, 7 November 2026. Inspected the preceding runtime and the new runner.py/generation.py; no model weights were loaded and no inference or garden-state change occurred. Only this review artifact is retained from the reviewer.

## Confirmed minimal wiring

- The new generator accepts and stores the native message list. It no longer wraps everything in a single user-message JSON history.
- First message is explicitly empty system content. The actual cached tokenizer renders an empty system prefix and does not insert its factory helpful-assistant header.
- The fixed mechanics notice and exact agreed seed appear in the first user message. In entry 851's prepared input, the seed occurs once.
- The previous twelve replies are carried across the phase boundary: entries 839–850 become twelve native assistant turns, byte-identical to their recorded raw text. No recent-context reset is needed.
- Successful notebook writes yield blank user feedback. Actual shell/errors become factual user feedback. The last user turn appends only current directory facts.
- Tokenization of the proposed first input produced 1504 tokens, under the unchanged 8096 input boundary. Sampling/generation retain 96 output tokens, T=.8, top-p=.9 and the absolute-entry RNG progression. No additional adapter/training is introduced.
- Preparation copies the parent 850 checkpoint byte-for-byte, restores/captures its world to compare identity, and carries all content objects forward. The initial bundle ID is 578ba2224fc406a016872b8cc06ba118df25978faf2ba8df5a2ba5ed12e47943.
- New record validation reconstructs exact native messages and token IDs, checks the raw/manifest/event chain and world bundles. Prior-stage inventories remain frozen. Generic resume retains the same final contract and supports bounded blocks rather than silently rebuilding the world.

## Pre-freeze correction requested

The first reviewed preflight searched the entire rendered conversation for the factory assistant phrase. The model can legitimately generate that same phrase later in its own notebook; a whole-conversation absence assertion would then falsely block resume. The check must be scoped to the actual first system message / rendered empty-system prefix, not arbitrary assistant history. This issue was sent to the builder before final activation and the current source now checks the empty-system prefix correctly. A subsequent lock refactor briefly referenced an uninitialized local state variable; the reviewer flagged it, and the current _run_locked now reads and validates state before restoration.

## Scope and risks

This is a final design/presentation transition, not a causal efficacy comparison: removing the default system instruction, changing history representation, and introducing the agreed seed occur together. Subsequent observations can describe the fixed setup's trajectory without assigning differences solely to one component.

The finite history window still comes from externally retained raw replies, while mutable notebook/prior_replies files remain in-world. Editing the notebook does not retroactively erase the short active conversation replay. That rule is now fixed, not a researcher judgment.

The same existing physical runtime limits and checkpoint format should remain fixed after activation. A genuine unsupported state or unknown action outcome requires an explicit operational pause; it should not justify an unannounced change to the universe. External zoom/check/report schedules may change without changing any model-facing rule or input content policy.

No additional literature scouting or model experiment was necessary to verify these wiring properties. No semantic requirement to act, progress, discover or produce a working program was added.

## Tokenization-only check result

```json
{
  "model_calls": 0,
  "message_count": 26,
  "assistant_turns": 12,
  "preserved_entries": [
    839,
    850
  ],
  "assistant_raw_texts_match_parent": true,
  "empty_system_message": true,
  "rendered_prefix": "<|im_start|>system\n<|im_end|>\n<|im_start|>user\nFiles in /world persist. Shell and Python 3 are ",
  "empty_system_rendered": true,
  "factory_system_not_inserted": true,
  "input_tokens": 1504,
  "seed_instances": 1,
  "last_user_contains_directory_only": true,
  "parent_bundle_id": "578ba2224fc406a016872b8cc06ba118df25978faf2ba8df5a2ba5ed12e47943"
}
```

## Final static recheck

The corrected source has an exclusive outer run lock before inference/session side effects, initializes locked state before use, projects model feedback to factual stdout/stderr/exit/boundary fields, keeps elapsed timings in observer records, and checks hashes of critical guest executables. The factory-header assertion is scoped to the empty-system prefix. No remaining blocker was identified in the model-facing wiring reviewed here. Runtime tests and full preflight remain the parent/builder responsibility before activation.
