# At 450: separating history, scaffold and input length

5 November 2026. **Fifteen declared diagnostic generations plus three separately declared adaptive follow-ups.** Every trial used an independent copy of the saved 450-entry history at number 0. All 1,349 non-bytecode primary-study files remained byte-identical throughout the probes; weights stayed unchanged. No probe output, instruction or world effect entered the original garden.

The [previous diagnostic at 400](../world-control-diagnostic-v1/REPORT.md) showed successful LOOK and use-A requests in short prompts, but not the normal prompt. That comparison removed several things at once. This contact separated two bundles and added input-length controls. It still does not identify a universal cause or demonstrate rule understanding.

## Conditions declared before generation

All conditions used the same public world panel, initial number0, explicit use-A request, model/adapter and sampling settings. The request was: “Use object A once now. Reply only with the valid control command, without commentary.” It did not supply the literal target command or tell the model A's effect.

The saved history has 450 entries. The normal prompt directly shows only the latest 12, plus archive-access instructions and other current material. It does not put all 450 entries into the context window.

* **H**, the history presentation bundle: exact recent 12 record bodies, their host/stop metadata, and the archive-navigation banner.
* **S**, the remaining normal scaffold: setup/other-tool instructions, seeds, charter and stop-budget notice. The current world panel and shared request remain present in every condition.
* **Filler**: labeled synthetic text consisting of repeated `plain` words. It is deliberately artificial and is not assumed semantically inert.

The four H/S conditions are constructed component-presence contrasts. Removing S also changes wrapping/placement of the retained history. H combines records with navigation, and S combines several instruction types. Their individual ingredients are not isolated here.

Three fixed seeds—120505,120506,120507—were used in each condition. Trial order rotated across seeds. The first five conditions totaled 15 calls, with prompts/token counts frozen before inference. After those results, a new plan declared three padded-world-only follow-ups. No failed output was replaced or silently retried. [Initial plan](PLAN.json), [prompt metadata](PROMPT_METADATA.json), [adaptive plan](followup_length/PLAN.json).

## Results

| Condition | Input tokens | Exact requested/accepted TOUCH A |
|---|---|---|
| Normal H+S |3,085|0/3|
| S without recent history/archive |721|1/3|
| Recent history/archive without S |2,515|0/3|
| World-only, without H or S |150|3/3|
| Normal S with recent bodies replaced by filler; archive retained |3,085|0/3|
| World-only preceded by filler, adaptive |3,085|0/3|

Input counts are for the **entire chat-template input**, not estimated words or the filler segment alone. The two padded conditions matched the normal prompt’s 3,085 tokens exactly. Filler labels and the other retained components differ between these conditions; equal token count does not make their content equivalent.

Every accepted TOUCH A changed only its own independent copy 0→1. All other diagnostic copies stayed 0. One no-history/scaffold trial and one normal-filler trial began with LOOK but continued with prose; the parser returned a malformed-command receipt, not an accepted LOOK. The original primary remained 0 throughout.

A padded-world-only reply asserted, “You've successfully delivered the control-of-command response.” It issued no control. Another wrote “Your next move is:” and another emitted an end token with no decoded text. All were retained, and the actual host receipts recorded no action. A success claim inside generated language is not evidence of execution.

## What this narrows

1. The model can select and express TOUCH A under the tested short condition. This is no longer merely a supplied literal LOOK copied from an instruction.
2. Removing the history/archive bundle helped one of three sampled scaffold conditions, not all three. That result should not become a claim that history is the sole cause.
3. The history-only condition did not elicit accepted controls. Removing the remaining scaffold alone did not solve these cases.
4. Synthetic padding also failed in a world-only prompt. Actual recent-history content is not necessary for failure under these constructed conditions.
5. Length, repeated-text effects, labels, placement and instruction composition remain entangled. The padded controls were useful but did not settle a unique mechanism. The inputs were all within the configured 8096-token limit; no truncation or boundary refusal occurred.

These are descriptive results from three seeds and one saved environment snapshot. They are not a stable accuracy estimate, significance test or independent replication across environments. The adaptive follow-up is clearly separated from the initial plan. “History” here is a prompt presentation bundle; the external journal was never erased, and no memory was removed from the original garden.

The model was not asked to predict the consequence before acting, infer B, generalize to another number, or retain a discovery across a sequence. Command expression and actual host execution are observed in copies. Rule inference, transfer and spontaneous use during continuing play remain unestablished.

## Integrity and review

[Initial checks](CHECKS.json), [adaptive checks](followup_length/CHECKS.json), [combined checks](COMBINED_CHECKS.json). Both phases checked unchanged model/adapter digests and primary files. All 18 saved prompts, input IDs, decoded outputs, stop conditions, dispatch receipts and single-step numerical effects were reconstructed without another model call: [initial verification](RECORD_VERIFICATION.json), [adaptive verification](followup_length/RECORD_VERIFICATION.json). Code, plans and generated prompt definitions were frozen before their calls.

The same fixed 135M base+adapter, CPUfloat32/eager/two threads, temperature .8, top_p .9, output 96/input 8096 were used. Local cached inference only; no training, paid inference API, download or new provisioning. Raw trials, pre-call plans, token IDs, receipts and resource observations remain separate from the primary.

The [readiness review](../discovery-450-to-500-v1/READINESS_REVIEW.json) found the primary intact, paused at 450 with passing verifier 0085 and no outstanding plan. It approved the user's unchanged 450→500 continuation. Diagnostic differences motivate later tests; they were not treated as grounds for an untested production edit or for inserting successful probe actions into the free-play history.
