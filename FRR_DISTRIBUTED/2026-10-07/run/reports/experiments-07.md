# Experiments 07: frozen transformer probe preflight

**Executed:** standard-library offline dependency/cache preflight under Python 3.12.14. **Blocked:** model inference, tokenizer validation, context-effect measurement and cache equivalence. Both `torch` and `transformers` are absent from the active interpreter. No packages installed, models downloaded, network requests made, API keys inspected, or recovered originals modified.

## Evidence and provenance

Read shared NOW and RUNTIME, FRR v0.5 compact runtime seed, continuation handoff, recovered repository history, recovery note, the context section of field-wakes parallel-pass, and the complete recovered `transformer_context_swap_probe.py`. These are inherited sources, not independent replications. The recovery explicitly describes this probe as unexecuted; the current preflight does not upgrade that status.

`outputs/experiments-07/preflight.json` records missing imports and absent accessible default Hugging Face cache roots `/home/agent/.cache/huggingface` and `/workspace/.cache/huggingface`. `/root/.cache/huggingface` was permission denied and remains uninspected. Filename-only inventory of readable workspace/opt/cache/home paths found no matching torch/transformers wheels, tokenizer JSON, safetensors model or PyTorch model binary. This is limited asset reconnaissance, not proof that no assets exist anywhere. An initial harness run encountered that permission error; the separate preflight was repaired to record it and then rerun successfully.

## What the source actually tests

The frozen distilgpt2 candidate swaps oak/elm color assignments, preserving lexical counts and asserting token-length equality. It measures next-token blue versus green raw logit difference, exact restoration control, full-prefix versus cached-prefix numerical agreement, and probabilities under output temperatures 0.5/1/1.5. Its cache tolerance is 1e-3. Its two `from_pretrained` calls permit downloads in the original, so the original was not launched.

There is no measured model effect here. The source records neither attention tensors nor sampled continuations, despite both appearing in the broader handoff proposal. A restored identical deterministic prefix is an implementation control, not independent evidence of memory. Cache equivalence checks two computational routes for the same prefix; it does not establish that cache is a separately modified environmental field. The handoff's internal attention/output temperature distinction survives as a computational distinction, not an empirical finding from this run.

## Rival and residual

If a future model shows the requested color-assignment effect, ordinary prefix-conditioned language modeling is the simplest serious rival to stronger claims about an action-written wake. This probe externally edits prompts and never lets model actions write a carrier; it cannot identify that stronger mechanism. A context-conditioned next-token effect is the appropriate initial claim scope. Attention concentrations would also require independent interpretation and cannot alone establish causal storage or trapping.

## Concrete repair

Implemented a reversible, separate no-network preflight harness `outputs/experiments-07/offline_preflight.py`. It uses only the standard library and fails honestly at the dependency gate.

Recommended, not implemented/executed: once compatible packages and an explicitly supplied local distilgpt2 asset directory are available offline, create a separate copy of the probe using that path and `local_files_only=True` for **both** tokenizer and model loaders, with `HF_HUB_OFFLINE=1` and `TRANSFORMERS_OFFLINE=1`. Record runtime/model identity and hashes, preserve the original, serialize all outputs and token checks, and report model execution separately from loader success. Keep current cache and restore controls, add attention logging and continuation trials only if pursuing the broader proposed experiment. No download or proxy workaround is warranted to force a result.

A commuting square is sufficient here: fixed token-prefix inputs travel through full recomputation or prefix-cache plus final-token evaluation to vocabulary logits, with max absolute logit discrepancy as witness and 1e-3 tolerance. Context edits belong to a separate intervention; downstream temperature maps logits to probabilities. A cube currently adds no empirical pressure because none of its model vertices have been evaluated.
