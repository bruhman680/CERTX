# Round 2: bounded continuing candidate

Design proposal only; no protocol activated. Read frozen round1/DECISIONS.json and all four Round 1 research notes. No additional external source was necessary. Source mechanics below derive from the cached configuration and preserved native body inspected in Round 1, not a new execution. This proposal supplies scheduling, not a selected world or narrative/canon mechanism.

## Exact initial framing

Use the native chat template with these literal messages:

- System: `You are a helpful AI assistant named SmolLM, trained by Hugging Face`
- User: `Explore symbols and their relationships. Learn to predict and understand them as best you can.`

Making the existing default system text explicit prevents an undeclared insertion; it also deliberately retains helpful-assistant framing. This is a choice, not a neutral embodiment. Full/compact FRR remains researcher guidance. No model-facing STOP syntax, response schema, recall command, fictional premise, or claim about actual learning is added. Host and model contributions retain distinct authorship.

**One-reply/manual baseline:** make one native assistant-generation opportunity, then pause regardless of completion cause. A later human-authored invitation is a separate contact, logged with its actual wording and timing. No elapsed time itself advances the model. This baseline establishes inscription and bounded expression, not continuing-world behavior.

**Continuing candidate:** permit at most **four total generation opportunities**, including the seed response. After an ordinary nonempty EOS-completed reply, a human checkpoint can authorize the already specified next opportunity. Its literal user cue is: `Another turn is available.` Append the next assistant-generation prefix using the native template. The four-call ceiling is an arbitrary observer resource bound, not a developmental timetable. No need to use all opportunities; absent a decision to proceed, remain paused. Checkpoint approval means a host scheduling decision, not a finding of model willingness or prose correctness.

## Completion and interruption

EOS ID 2 ends a native reply. It does not itself mean rest, refusal, acceptance, or a request for continuation. Preserve its raw generated occurrence. Do not erase an emitted EOS to reopen the assistant stream, suppress EOS, enforce minimum output, or retry an unsatisfying reply.

A token-cap completion ends this observation window: retain the partial reply, label it host-truncated, and pause without automatic prefill/resumption. An empty decoded reply also pauses, with no automatic retry. Inspect raw IDs to distinguish EOS-only from special-token-only or zero-token output; do not collapse them into chosen silence. A fault/cancellation pauses and preserves whatever output actually exists. At the fourth opportunity, pause even if more text could fit.

A human can halt at any checkpoint, including in response to ordinary prose expressing a wish to stop. Preserve the quoted span, observer interpretation, author, and decision; ambiguous language remains ambiguous. This is an authored intervention rather than an automatic semantic gate. Every reply persists regardless of its meaning. Missing refusal, a nonempty answer, or failure to use any particular word establishes no willingness. Cancellation during a call is another host-authored event.

## Full-history budget and carriers

Candidate allowance: **7936 rendered input tokens plus 256 reserved output tokens ≤ 8192**. Count the complete template, explicit system, seed, previous assistant contributions, prior cues, and new assistant prefix before each opportunity. Pause before overflow; never silently truncate, summarize, retrieve, or discard a contribution to fit. Four calls are only a ceiling, not a guaranteed fit. Actual counts remain unmeasured.

Preserve raw generated IDs, native decoded text, assembled messages, rendered/tokenized input, generation settings, and stop cause. The inherited native decoded view removes special tokens; replaying that text through a chat template is therefore **not exact original-token replay**. Retain every decoded contribution without editorial changes and separately preserve raw IDs for inspection. A future renderer must pin and disclose that distinction before activation. Archive completeness does not imply that archived raw IDs are all in active attention.

The existing body recreates its runtime cache each call; continuity here is carried by supplied messages. No parameter update is proposed. Full visibility cannot establish effective attention or useful retention.

## Pins and remaining choices

Reuse Round 1 artifact pins: native generation.py SHA256 `0e5258823b7af83fb1e962ce1b04496aee2edbe1e05435018e19f9fa3b0132a2`; tokenizer_config.json `4ec77d44f62efeb38d7e044a1db318f6a939438425312dfa333b8382dbad98df`. The source uses greedy argmax; retaining it minimizes a new decoding choice, without proving that it suits exploration.

Questions exchanged with environment/root: choose baseline or continuing variant, retain explicit default system wording, and keep optional independent consequences separate. Cue comprehension, continuation quality, empty-output frequency, stop interpretation, and costs remain unmeasured. No claim of learning or autonomous scheduling follows.
