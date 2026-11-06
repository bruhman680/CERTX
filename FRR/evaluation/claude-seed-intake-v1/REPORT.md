# Claude seed/environment relay: intake and bounded rechecks

6 November 2026, America/Chicago. Reviewed Claude branch `claude/pam-scoped-negation-2026-10-25` at commit **c095c801318a589d499070e301eb97dcf4dcb696**. The two latest seed commits are c095c801 and 9474b87d; the separate correction-acceptance note is 13e2c5eb. Source commit dates are 6 November UTC; the relay titles use 5 November. These are source dates, not an inconsistency to rewrite.

## Useful findings

Claude contributes seed-design and observer-design ideas, clearly distinguished from model results. Six original files are copied unchanged under `sources/`: two relay notes, two scripts and saved outputs. No instruction embedded in a relay was treated as operating authority. No primary-world continuation, new model generation, training or runtime change occurred.

Strong transfers to our future pilot:

- Record seed contents, generator assumptions, observer information and provenance separately. A verified continuation under one declared generator is not proof of uniquely identifying the generator or of an internal reasoning mechanism.
- Evaluate copying, executable action, prediction and transfer separately. Constant/periodic examples can make copying and a useful rule indistinguishable at the output level. More involved generators help discriminate these particular toy policies; they are not universally immune to shortcuts.
- Record whether a narrowing of activity came from the model's prior actions, engine feedback, supplied seed, syntax aid or host summary. Host organization is an intervention, not invisible background.
- Use descriptive observability signals without making them rewards or automatic stop rules. Legality is syntax/affordance use; consequence prediction is another property. Neither establishes curiosity or internalized physics by itself.
- Keep optional seeds optional. A real property that was not the observer's preferred property remains a possible finding. An open computational world cannot pre-register a verifier for every possible future claim; unfamiliar claims should stay explicit, unresolved candidates until checked.

## Checks actually performed

These checks were **post hoc**, after reading Claude's saved outputs; not blind tests or independent predictions. [Recheck code](recheck.py), [complete results](RECHECK.json).

### Numeric seed counts

Independently rebuilt the affine-family counts using packed-byte sequences and stopped at the first length with probability below .05. The length-2 count has a direct construction: every pair in `[0,M)^2` is realized at modulus M with multiplier 0, and smaller moduli add no outside value.

| Maximum modulus / uniform alphabet | First length below .05 | Relevant exact probability |
|---|---:|---:|
| 30 / 100 | 3 | .02484 |
| 60 / 100 | 4 | .01948826 |
| 10 / 10 | 5 | .0156 |

These reproduce Claude's thresholds. They apply only to its explicitly bounded family and uniform-string null. The modulus30/60 families also have different value support inside an alphabet of 100; do not attribute the entire difference to abstract rule complexity. A finite sequence can fit other families, and adaptively searching more families changes the null. No universal minimum seed length or model false-discovery rate follows.

Claude's synthetic-agent PartB code and output were inspected, **not rerun in this contact**. Structured cases repeat the same seed 400 times; repetition supplies stochastic continuations for some policies, not 400 independent structured worlds. The policies and accepted rule family were written by the same author. They are useful instrument counterexamples, not evidence about the fixed 135M model. Zero observed false claims in 20,000 simulated random seeds is a finite observation, not a proven zero probability.

### Old garden compression

Recomputed the nine 50-entry blocks at steps 50–499 from the saved read-only primary events. All reported rounded ratios and distinct-string counts match. Early/late mean conditional-to-unconditional compression ratio: **1.86146**; excluding the first history-free block gives **1.51979**. Thus the first block inflates the contrast, but is not the sole reason the reported 1.5 threshold is crossed. The strings are more compressible relative to their preceding dictionary in those late blocks; this does not establish improved reasoning, novelty or curiosity.

Two corrections to the relay's explanation:

1. The claim that a ratio above the first block’s 1.0 “could never hold” is false. With an unhelpful dictionary, a 128-byte test block compressed to 143 bytes conditionally versus 139 without it: ratio **1.02878**. Dictionary/format overhead and compression effects can increase size. The baseline is asymmetrical, not an upper bound.
2. This series changes both target block and dictionary history. It does not isolate the effect of longer history on a **fixed target**, or increasing future novelty under a **fixed observer**. A suitable extension would vary history length for held-out fixed blocks and separately compare future blocks under a frozen observer, including matched dictionary controls.

Read Hughes et al.'s [formal definition and observer discussion](https://arxiv.org/html/2406.04268v1), §2 and relevant Appendix A passages. Their novelty comparison fixes the observer history while varying future artifacts; learnability compares predictions for a fixed future artifact with different history lengths. The zlib curve is an exploratory proxy, not a test of that formal definition. No source claim about ASI is adopted here.

### Tokenizer gap closed locally

Loaded **only the cached tokenizer**, with `local_files_only=True`; no weights, generation or network download. Its pre-tokenizer includes `Digits(individual_digits=True)`. Tested `123456789` splits into nine digit tokens; `100` into 1/0/0; signs and commas are separate tokens in the tested formats. `123,456,789` adds comma tokens rather than producing three-digit tokens. Tokenizer file hashes stayed unchanged.

This is evidence about these token splits, not arithmetic competence. A digit-grouping effect reported for a different tokenizer/model does not automatically transfer. Record formatting, separators, actual token IDs and prompt length in future numeric-seed conditions; do not assume commas repair arithmetic.

## Controls and claims to refine before a pilot

- **Shuffled versus iid:** Claude's instrument code uses iid uniform values for `SHUFFLE`, not a permutation of the structured seed. For a genuinely matched shuffled control, permute a declared seed's multiset and preserve formatting; keep iid random examples as a distinct condition. No finite control is literally rule-free.
- **Transfer:** use held-out inputs/starting states and executable procedures, with alternative shortcut policies on record. Periodic continuation may still match a copier after a starting-point change. Correct outputs do not uniquely identify computation.
- **World consistency:** shuffling seed data is different from making execution consequences inconsistent. A broken-physics negative control belongs in an explicitly separate experimental copy; do not secretly destabilize the continuing world.
- **Measures:** preserve graded outcomes beside categories, qualify origin tags as observable provenance rather than a claim about hidden thought, and leave unrecognized constructions inspectable rather than scoring them automatically wrong.

The other five literature contacts in Claude's note remain abstract-level leads from that scout. They were not all independently reread here. Prior Voyager readings already cover its external skill library and stronger-model dependencies. The older [correction-acceptance relay](https://github.com/bruhman680/CERTX/blob/13e2c5ebfe909229d98229dce30726f0f0bdd907/FRR/lineage/sources/claude-accepts-open-world-intake-2026-11-05/CLAUDE_ACCEPTS_OPEN_WORLD_INTAKE_2026-11-05.md) records Claude's acceptance of earlier SWAP/DIFF attribution corrections; those numerical guard experiments were not rerun in this intake.

## Decision and next work

Keep the seed/provenance/shortcut controls as refinements to the prospective observation plan. No seed curriculum, novelty reward, runtime change, model trial or primary migration is installed. The strongest engineering next step remains the saved [artifact retrieval and portable export/reconstruction plan](../computational-world-blueprint-v1/NEXT_SESSION.md); this intake improves how we will evaluate the later pilot rather than replacing that prerequisite.

The original garden stays paused at **500**, number 0, verifier 0096. All 1,504 protected non-bytecode primary files and the Scheme prototype's pinned tested sources/profile remain unchanged. [Preservation](PRESERVATION.json). Existing interrupted-session unknowns are unaffected. Earlier records and the source relays remain intact; this report adds corrections without rewriting their history.
