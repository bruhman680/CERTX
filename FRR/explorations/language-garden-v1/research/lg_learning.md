# Learning mechanisms and persistent carriers

Planning only. Session date: 20 November 2026, America/Chicago; original contributor host date: 21 November 2026 UTC. Read LAB_BRIEF.json and compact.md first. No inference, training, tests, downloads, or old-world changes were performed. Intuition: an enduring symbolic space may support exploration. Hypothesis: relationships learned there may transfer elsewhere. Neither persistence nor compelling expression establishes that hypothesis.

## Three distinct options

**In-context adaptation:** fixed parameters produce different continuations when active input changes. Brown et al., *Language Models are Few-Shot Learners* (2020), evaluate textual demonstrations without gradient updates, including novel-word use. This establishes a possible mechanism, not SmolLM2-135M competence or lasting acquisition. A conversation file saved on disk is inactive until its contents, or a derived representation, reach the model. A KV cache is another runtime carrier; restarting normally removes it unless explicitly restored. None of these operations changes weights.

**Persistent external memory:** an append-only ledger survives process restarts; selected records enter later active context. Retrieval changes access, not necessarily the model. Wu et al., *Memorizing Transformers* (2022), use non-differentiable approximate nearest-neighbor lookup over stored internal key/value representations and report language-modeling gains. Their system includes architectural changes and training to use memory; it is not evidence that adding a text archive to this cached model reproduces their result. For our first design, exact text recall avoids such architectural commitments. Storage retention, retrieval success, and successful use must be reported separately.

**Parameter/adaptor learning:** explicit optimization changes persistent tensors. Hu et al., *LoRA* (2021), train low-rank update matrices while freezing pretrained weights. An adapter still contains learned parameters; “base weights frozen” does not mean the effective model is unchanged. Paper results on other models and hardware do not measure CPU feasibility here. Genuine updates require examples, objective, forward loss, backward gradients, optimizer steps, and saved changed tensors. A seed, accumulated history, summary, or claimed realization supplies none of those steps by itself.

## Minimal first design

Use the existing fixed model as a proposed inhabitant of a new, separately authorized branch. Keep an immutable raw event ledger with record IDs, authorship, branch, observation/action type, and actual consequence receipts. Preserve original records when revisions appear. Model-authored propositions remain propositions; writing them cannot certify environment truth. Permit free expression, revision, silence/rest, and stopping without treating those choices as failure.

Assemble bounded context from the unchanged candidate seed, minimal interface mechanics, and exact recent records. Reserve space before assembly; expose omitted ranges and offer optional recall by stable record ID. Preserve authorship and branch identity in recalled material. No automatic synopsis or semantic approval gate is needed. Log the exact visible input and selection policy externally. Whether this small model can use recall remains unmeasured; do not compensate preemptively with a behavioral curriculum.

Retention has multiple failure modes: omitted context, failed recall, misinterpretation despite visible evidence, and overwritten learned parameters. Keeping every byte prevents only archive loss. Summaries can erase contradictions; retrieval can repeatedly favor the same narrative. Preserve recoverable originals even if later compression is explored.

## Discriminating observations, proposed only

Observer comparisons can occur in isolated copies without becoming instructions or reward signals in the inhabitant’s world:

- Restart with identical assembled input and fixed parameters: persistence through disk/context is sufficient; restart alone proves no weight learning.
- Withhold earlier active context and recall access while preserving environment state; then restore exact relevant records. A lost-and-restored behavior implicates accessible history. Chance, decoding variation, and pretrained associations remain rivals.
- Clear active context, retrieval, caches, and relevant environment state; compare changed versus original parameters under identical fresh input. Transfer that survives only with the changed checkpoint implicates an update, subject to leakage and matched-input controls.
- Later compare recall of an old relationship after intervening material, then its use with new symbols or in a separately specified system. Verbatim repetition supports retention; cross-system understanding requires a stated mapping and novel consequences. Failure on one mapping does not refute all transfer.

No automatic grader is proposed. One discriminating next observation, after authorization, is whether access to one exact earlier record changes use of its unfamiliar relationship after a fresh-process restart. Archive survival and model uptake remain separate outcomes.

## Conditional training route and contamination

Only if durable parameter adaptation becomes a desired next objective, design a separate reversible adapter experiment: freeze a base checkpoint, retain a no-update comparator, provenance-tag every example, choose a causal language-model objective, record optimizer steps and checkpoint hashes, and save adapters separately. Evaluate fresh-context retention, transfer, and deterioration on previously available material; lower training loss alone proves neither understanding nor preserved capabilities. Throughput, memory, dependencies, and useful CPU training duration remain unmeasured.

Shumailov et al. (2024) fine-tune OPT-125m across recursively generated datasets, including conditions retaining some original data; degradation depends on that protocol. This does not prove every use of synthetic text fails. It does justify preserving independent observations and tracking self-generated ancestry. Repeated claims are not independent evidence, and held-out material must stay outside prompts, retrieval, and training. Training only on garden narration may consolidate its errors and reduce diversity.

Paired review with lg_environment agrees on these carriers and authored-status distinctions. Their warning is accepted: compulsory external observations could impose a curriculum. The first garden may remain voluntary expression/persistence; claims of grounded discovery then remain unsupported. No substantive disagreement remains; recall usability and the source of independent consequences remain open.

Primary sources read: [Brown et al.](https://arxiv.org/html/2005.14165), [Wu et al.](https://arxiv.org/html/2203.08913), [Hu et al.](https://arxiv.org/html/2106.09685), [Shumailov et al., corrected article](https://pmc.ncbi.nlm.nih.gov/articles/PMC11269175/).
