# Round 3: runtime/source audit

2026-11-21. Audited frozen `round2/DECISIONS.json`, CANDIDATE, all three Round 2 blueprints and Round 1 runtime evidence. Re-read cached JSON metadata and preserved generation source as text; recomputed hashes. Candidate and blueprint hashes match DECISIONS. Metadata/body hashes match Round 1. No weights/tokenizer were loaded, inference performed, implementation built or frozen file edited. This is a separate checking pass with access to earlier findings, not blind independent evidence.

**Verdict: reviewable, not activation-ready.** The candidate accurately states its planning status. Its central mechanics are compatible with the inspected body. One preservation promise exceeds existing demonstrated behavior; several exact execution choices remain for the implementation specification.

## Supported mechanics

Cached `/workspace/cache_backend_models/smollm2-135m/config.json` and `tokenizer_config.json` declare 8192 positions/model maximum length. EOS and pad are ID 2; EOS text is `<|im_end|>`. No RoPE scaling is configured. These values support a declared boundary, not effective attention, comprehension or long-history reliability.

The candidate's explicit system sentence exactly matches the tokenizer template's automatically inserted default sentence, without an added period. Its system/user role choice avoids duplicate automatic insertion; `add_generation_prompt=True` supplies the assistant prefix. Helpful-assistant framing is therefore disclosed. Full message bytes, role order and rendering still need freezing; prose alone cannot stand in for the actual input.

`/workspace/frr/evaluation/minimal-garden-candidate-v1/generation.py` has SHA256 `0e5258823b7af83fb1e962ce1b04496aee2edbe1e05435018e19f9fa3b0132a2`. It rejects rendered input above 7936, reserves at most 256 emitted tokens and uses greedy argmax. The candidate's 7936+256=8192 accounting is conservative and supported. Count the complete newly rendered input every call, including system, seed, cues, historical messages and assistant prefix. Four opportunities are an upper bound, not measured fit or useful duration. Exact initial counts remain unmeasured.

The body records EOS among generated IDs, checks it before continuing, then decodes with `skip_special_tokens=True`. Candidate preservation of original IDs alongside decoded-text replay is honest: re-rendered prior text is not the original token stream. “Never delete emitted EOS” must mean preserving the raw artifact; visible-history replay legitimately strips it and inserts host template boundaries. Cache is recreated from supplied input each call, with no cross-call cache returned. Nothing here updates weights.

## Required correction before implementation

Round 2 says faults/cancellation preserve whatever output exists. The existing body accumulates `new` in memory and returns output only after generation and the final `guard.read`. It has no partial-output checkpoint or streaming callback. A generation error, cancellation, or final guard exception can prevent return of already generated IDs. The preservation statement is a requirement, not a capability established by this source. Two policies remain unselected: disclose potentially unavailable interrupted output and fail closed without replay, or add a separately tested durable token journal before claiming complete token capture. The lifecycle is pre-call guard → model/token loop → `guard.read('after_generate', run_id=run_id)` → returned IDs/text; no durable token write occurs inside that loop. Unavailable tokens must not become zero-token generation or chosen silence.

## Limits and unselected options

EOS ends a reply, including when emitted as token 256; the source then labels it EOS, not cap. Normal successful generation emits at least one ID; visible emptiness may reflect special-token-only output. The blueprint should freeze whether “empty” means zero decoded characters or also whitespace-only text. No force-minimum output, EOS suppression, semantic retry or automatic capped-stream repair is justified.

Before activation, select one scheduling variant and pin exact model/checkpoint identity, decoder, library/runtime settings, renderer and stop/event handling. Metadata hashes do not verify current weight tensors or establish throughput/resource feasibility. Logged interpretation of ordinary stop prose may affect scheduling while every contribution remains admitted; this is disclosed semantic influence, not a truth gate.

Mechanical actions, partner interaction, raw-stream continuation and later training remain unselected. No read artifact demonstrates those interfaces' competence, lasting learning or transfer. The candidate appropriately leaves these claims untested. Evaluation/root received the interruption-recovery gap; evaluation agrees missing traces must remain distinct from empty output.
