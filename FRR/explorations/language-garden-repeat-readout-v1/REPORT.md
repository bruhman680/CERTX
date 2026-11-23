# Four probes on repetition readout

We ran four sequential probes with the pinned SmolLM2-135M-Instruct language pilot. Each result informed the next design. The batch used 36 fresh greedy generations and 16 separate first-position forward passes on the original prompts. Every generation was an isolated opening with the original symbol seed, no feedback and the 256-token limit. The weights were checked throughout. The continuing garden was outside the batch.

| Probe | Requested result | Finding |
|---|---|---|
| 1. Choose the repeated positions | Bare A or B. Eight rows with the menu reversed for each. | 0/16 exact. Twelve hit the cap. |
| 2. Compare the two answer-token scores | Higher-scoring bare A or B for exactly the same prompts. | A ranked higher 16/16. 8/16 correct and 0/8 items correct in both orders. |
| 3. Select the value supplied directly | Bare A or B for an exact match to a visible field. | 0/8 exact. In the secondary review, 3/8 opened with the correct letter and option text. No item passed both orders. |
| 4. Drop the menu and name a symbol | Name either the visible Last value or the repeated value in the same labeled rows. | 0/6 exact on both tasks. In the secondary review, 6/6 visible Last values and 5/6 repeated values were named correctly. |

## The choice format itself was a weak measurement

Probe 1 elicited descriptions, echoes and cap-length loops. Three finished replies used an explicit closing answer letter. Only one of those three letters was correct. The answer options described two position pairs, and each was correct half the time in both menu orders. Probe 2 returned the same unrestricted opening token as the archived generation on all 16 prompts. Restricting the comparison to bare A and B yielded an all-A preference, with an A-minus-B log-probability gap of 2.16 to 2.95 nats. This measures initial bare tokens only. A later answer or a version with leading whitespace could follow another trajectory.

In probe 3 the model could match the value by literal readout. Even so, seven replies that opened with a complete choice line contained six A selections and one B selection. Three of the seven were correct. The eighth reply did not give a letter. This simple input shows the menu was unreliable even when the answer text was written out in the prompt. The wording in probe 3 and the absence of a row were part of that control.

## The direct-symbol result has one informative split

Probe 4 used six labeled rows, two lexical pairs crossed with AAB, ABA and ABB. For each row, separate calls asked for the visible Last value and the symbol appearing twice. All twelve finished and used sentences, so all missed the requested symbol-only format. The secondary content review looked for the uniquely named row symbol in the first assertion.

On four rows, the repeat was also the last symbol. Copying Last would get all four right. On `mip mip zav`, the model called `zav` the repeat, the same as its correct Last answer. On `ket ket ful`, it correctly called `ket` the repeat and `ful` the last symbol in separate calls. Thus the direct repeat question beat the copy-Last heuristic by one case on this panel. The decisive subset was 1/2. This is one observed instance of different answers for the two questions. More lexical blocks and conflicting positions are needed to identify when the difference is reliable.

The strongest follow-up would keep direct symbol readout and deliberately make the visible Last value a decoy on most rows. Counterbalance the repeated identity and ask for the visible Last value on the same fixtures in separate calls. Keep this control stable before asking the model to generalize the relation or reusing the broad invariance seed.

The four directories contain each opening contract, score file and either raw generation traces or the per-token score replay. [Secondary content review](CONTENT_REVIEW.json) records the excerpts behind the nonexact judgments. The pinned model and tokenizer are required for the audit commands below. The commands validate the saved records and recompute scores without new inference.

```sh
python run_panel.py audit 01
python rank_panel.py audit
python run_panel.py audit 03
python direct_panel.py audit
```
