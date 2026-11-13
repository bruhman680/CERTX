# Continuation and decoder scout

13 November 2026, America/Chicago. Primary-source scout plus a token-only local check. No model inference, paid endpoint, world mutation, or canonical source change was performed. The existing output-length report and `minimal-garden-candidate-v1/generation.py` were read. This note proposes distinctions and tests; literature is not a diagnosis of this model.

## What the sources actually contribute

| Primary source | Material read | Useful contribution | Limit for this garden |
|---|---|---|---|
| [Holtzman et al., The Curious Case of Neural Text Degeneration](https://arxiv.org/html/1904.09751v2) | Abstract and selected full-text sections: introduction, decoding definitions, experimental setup/results; not the complete paper or appendices | With the same GPT-2 model, decoding choice changes repetition and diversity. Their nucleus method selects a dynamic probability-mass set; likelihood maximization can yield repetitive open-ended text. | Experiments use GPT-2 and general prose, not our 135M instruction model, notebook grammar, or environmental interaction. This motivates a decoder comparison; it does not demonstrate which decoder is best here. |
| [Hugging Face, How caching works](https://huggingface.co/docs/transformers/en/cache_explanation) | Relevant official documentation on causal KV reuse and masks | Past K/V can be reused for inference; custom loops must match the attention mask to cached plus new tokens. | A KV cache is a computational representation of a prefix, not additional learned knowledge or unlimited memory. Exact numerical equivalence to a fresh prefill still needs local testing. |
| [Hugging Face, Chat templates](https://huggingface.co/docs/transformers/en/chat_templating) | Official sections on token structure, `add_generation_prompt`, and `continue_final_message` | Continuing the last assistant message differs from starting another turn. Final-message continuation removes the terminal closure; it must not be combined with `add_generation_prompt=True`. | Current online docs may differ from installed APIs. Verify actual token IDs, especially where text decoding/re-encoding or whitespace could change a prefix. |
| [HuggingFaceTB, SmolLM2-135M-Instruct model card](https://huggingface.co/HuggingFaceTB/SmolLM2-135M-Instruct) | Model summary, usage, evaluations and limitations | The author's example uses sampling with temperature 0.2 and top-p 0.9. The card lists instruction fine-tuning and cautions about factual/logical consistency. | An example is not an optimized setting for this task. Function-calling support is explicitly described for the 1.7B model, so the family description cannot establish robust tools for the 135M model. |

Online documentation was accessed on this date. No paper result or model-card example is adopted as a live-world setting.

## Three different things that can be called “continue”

1. **Pause the token loop, retain its exact state, then resume.** The input token prefix does not change. This is an execution boundary. Cache position, attention length, the last sampled token, and (for sampling) RNG state must be explicit.
2. **Reconstruct the exact raw prefix in a fresh process and prefill it.** This should target the same conditional distribution, subject to finite-precision/kernel differences. Preserve token IDs, not only decoded text. An exact output match must be observed rather than assumed.
3. **Add a user “continue” message, append receipts, or open another assistant turn.** This changes the token prefix and therefore the modeled conditional distribution. It is a new context intervention, not a transparent pause.

Removing an EOS after the model naturally emits it also defines a new condition. In particular, a deliberate final-message continuation can be useful, but is different from respecting the original completed-message boundary. This matters because two prior length probes naturally ended at token 257 with unfinished fences.

## Local token-only check

The cached tokenizer uses `<|im_end|>` as EOS (token ID 2). Its normal chat template closes each assistant message with that token and a newline. Under installed Transformers **4.57.1**, `template_probe.py` compares saved input IDs plus saved generated IDs with two retemplated forms for retained turns 1 and 12.

For turn 12, `continue_final_message=True, add_generation_prompt=False` reproduces the exact raw prefix. For turn 1 it **does not**: raw final token IDs `[198, 198]` become `[1116]` when the text is reconstructed and tokenized. Normal templating also changes the prefix; in turn 12 it appends `[2, 198]`, closing the reply. The first script version assumed both continuation forms would match and its assertion failed on turn 1; that rejected assumption is recorded in `TOKEN_PROBE_NOTE.md`. The corrected diagnostic retains mismatches as results. Thus even an apparently correct continuation API does not guarantee identical raw tokens. Results and the tokenizer-config hash are retained in `TEMPLATE_RESULTS.json`. No weights are loaded by this check.

## A concrete cache boundary hazard in the existing loop

At its cap, `generation.py` records the final chosen token but does not feed that token through the model: its `if index < MAX_OUTPUT - 1` branch skips the last forward. Thus, after selecting token 256, cache length is prompt length plus 255. A future cached continuation must feed the selected token 256 **exactly once** before sampling token 257. Merely preserving the cache loses that final token; preserving a fully advanced cache and feeding it again duplicates the token. This observation is a code-read consequence, not a reproduced cache-resume failure.

Two honest durable representations are possible: save “cache before last chosen token” plus that token, or advance the last token and save cache plus the resulting next-token logits. Either needs an explicit invariant, version pinning and integrity checks. Saving only raw prefix IDs and regenerating the cache avoids serializing model-specific cache objects, at the cost of prefill time.

## Strongest next tests

- **Decoder only:** exact saved inputs, same cap, no extra instruction; compare greedy with explicitly seeded temperature/top-p sampling. Report every outcome, EOS/cap, complete-cell counts and repetition separately. A closed code fence does not establish correctness or successful action. Do not select only the prettiest sampled output for live continuation.
- **Transparent chunk invariant:** compare one uninterrupted greedy sequence with an in-process cache pause/resume and exact-token fresh-prefill at a fixed boundary. Record the first divergence, logits error, attention/cache lengths and whether token 256 is represented. Repeat one sampled case with restored RNG state. Pauses should not insert chat tokens, receipts, or coercive closure.
- **Context only, separately:** compare current full history with a declared alternate history or same-message final continuation. This measures context sensitivity, not repair under the unchanged live contract. Do not silently remove actual historical errors to make an attractive branch.

Confidence is high in the token/template distinction and the loop's last-token cache accounting. Confidence is moderate that a decoder comparison will reveal useful behavioral variation. No confidence is claimed that sampling, continuation, or a complete cell produces sustained environmental competence or emergence.
