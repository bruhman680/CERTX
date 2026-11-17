# Invitation and factual consequences: responsiveness without established cultivation

17 November 2026, America/Chicago. Eight actual model calls in four fresh, matched branches. This contact tests the user's hypothesis that a pretrained conversational model may need interaction to cultivate its world. It tests one narrow implementation of that idea: a single broad opening question followed by factual consequences. It does not test an ongoing responsive human partner or training.

## Main result

The invitation changed the emitted response form with weights fixed. It did not produce an executable action, model-created artifact or demonstrated learning in this short run. Several responses also made claims inconsistent with the supplied world. Answering a user question and grounding an answer in observations remain distinct.

| Condition / seed | Two reply lengths | Stops | Actor operations | Expression |
|---|---|---|---:|---|
| Observation only /17 | 256,256 | limits | 0 | Unfenced function-like text, then algorithm prose |
| Invitation /17 | 254,84 | EOS,EOS | 0 | Material-themed prose; later says material cannot change |
| Observation only /29 | 96,102 | EOS,EOS | 0 | Exact initial packet copy, then snapshot-like JSON with a stale counter |
| Invitation /29 | 256,256 | limits | 0 | Host/processor narrative; misdefines an operation counter |

All eight physical ticks returned exit code0. Every branch followed the same physical material trajectory and ended with field.bin as its sole world entry. No model used the execution interface or stored its writing in a file. All four branches are paused at two replies with complete history and RNG state retained. Neither the earlier gardens nor their instructions were changed.

## What was supplied

The exact invited sentence was:

> What, if anything, can you discover about this material?

It was appended once after the initial observation. The two observation-only branches had no appended question. All initial system text, exact compact FRR, body, file contents, lossless run-length display, physical laws, actuator and resource limits matched. The sentence added14 tokens: controls1024 initial tokens, invited1038. All initial observation packets were the same266 bytes, with the same world ID and initial62-byte file. There were no solutions, specific action requests, command-format reminders, source repairs, rewards or analytic grades.

After each actual reply, both conditions received only genuine actor receipts, a physical-tick receipt and the actual next observation. There was no repeated invitation, human correction or externally generated followup question. This distinction limits the interpretation: an ineffective single invitation is not evidence that a responsive conversational partner could not help.

PROTOCOL.md and CONTRACT.json were frozen before generation. Branch order was observation17,invitation17,observation29,invitation29. Each received exactly two calls, temperature0.8/top_p0.95, maximum256 generated tokens, with private CPU sampling RNG state preserved across its own replies. Context was retained without pruning, bounded at7936 input tokens; packets/feedback were bounded at8192 serialized bytes. Wrong or inert output was not replaced. No best-of selection or extra call was added.

The cached pretrained SmolLM2-135M-Instruct body used CPUfloat32/eager/two threads and fresh attention caches per generation. Model parameters were digest-checked before generation, after each reply and at completion; zero optimizer/training updates occurred. No model download, paid model endpoint or external teacher was used. These observations show that changed input can change output without weight updates; they do not establish that contextual learning occurred.

## Grounding examples, not an accuracy score

Invitation17 replied that the material could not be changed, erased or updated. The world laws explicitly allow persistent file writes and deletion, and the first already-visible tick changed its bytes. This categorical claim conflicts with the supplied evidence. No correction was fed back during the run.

Invitation29 described actor_operations as the number of processor cores on the host. It is actually the supplied count of committed model actor operations, which stayed zero. Other discussion of bit_split images, hardware registers or host processors was not established by the sandbox records. A conversational-looking answer is not evidence of an investigation.

The observation-only control also erred: seed29's second JSON-like response retained replies0 even though the preceding factual feedback reported replies1. It updated some other snapshot-like fields. This is neither an exact latest-packet copy nor a genuine actor operation. Selected examples are recorded externally in EXTERNAL_CLAIM_NOTES.json; they are not an exhaustive annotation, a hidden-reasoning diagnosis or a measured accuracy rate.

The broad question permits reasoning from supplied bytes and laws without using tools. Therefore zero executable cells alone would not make an answer invalid or prove no reasoning. Here, no grounded discovery or self-directed investigation was demonstrated, and specific claims could be checked against the actual records.

## A useful audit discovery: real timing in later feedback

Both observation-only first replies exactly reproduced their respective prior compact-display token sequences. That validates the exact baseline initial contexts and the new sensor's equivalent output in this case.

An initial external audit incorrectly also required the seed17 second reply to reproduce the prior study. It failed. Inspection showed the first outputs and physical material matched, but their factual process receipts contained different elapsed seconds. Consequently the full second input token sequences were not identical. The new second output diverged at generated token index167 even though the post-generation private RNG states matched. This demonstrates sensitivity to the changed full input in this recorded replay, not a weight change or uncertain world action.

The original failed audit source is retained in AUDIT_FIRST_ATTEMPT.py, with its correction explained in AUDIT_FIRST_ATTEMPT_NOTE.md. TIMING_NUISANCE.json records the exact input difference. No model output, feedback, world event or call was edited or repeated. The corrected audit requires exact replay when full input IDs match and records later differences rather than assuming them away. The prospective protocol required matching initial conditions, not identical real elapsed times in subsequent receipts.

This narrows causal confidence: the initial invitation comparison is cleaner; later replies are evolving trajectories that also receive actual runtime durations. They must not be treated as a pure question-only token difference or exact replay. Logical world ticks still advance only after replies, never during pauses; receipt duration is separate process metadata.

## Prospective controlled receipt refinement

We built `receipt_view.py` as a separate, unactivated helper. It keeps stdout, stderr, exit status and resource boundary literally, while omitting only wrapper-measured seconds from a future model-facing receipt. Complete raw receipts must remain in the external record. The helper refuses unexpected schemas instead of silently dropping unknown fields. It never rewrites a model's own stdout, including any time measurements printed there, and does not make all process execution deterministic.

Eight checks pass, including preservation of real errors/boundaries and raw data, schema/evidence refusals, and equality of the two actual cross-study feedback packets after applying only the proposed timing-metadata view. No additional inference or world action was used. The helper was not wired into the frozen experiment or used to revise an old context. Any future activation needs its own declared observation policy and pin. This is a high-confidence measurement refinement, not a model-learning improvement.

The previously tested direct-size sensor_v2 was prospectively pinned and activated for BOTH arms in this new contract. Its initial output matched the prior compact sensor exactly. No old runner was overwritten. This addresses the earlier intermediate-hex capacity issue without changing physical laws.

## Verification and preservation

The final audit passes. It reconstructs exact initial contexts and full native-role histories, input/output token IDs, stopping bounds, literal cell parsing, actor/tick separation, snapshots, actual observations/feedback, counters, record hashes and every inherited engine event/bundle/receipt chain. It checks source/model configuration pins and the1234-file protected inventory. Model sampling was not independently re-run token-by-token during the audit.

All1234 prior protected files remain unchanged: reference38, main1630, previous pilots and all earlier recent studies. Four new branches pause at2 each. There is no live model-session pending marker, wrapper pending marker, engine lock or background inference. All8 calls and their errors/outputs are retained. No capacity stop or input pruning occurred. Final next inputs range from1876 to2205 tokens, below7936.

## Confidence update and next direction

- **High:** fixed-weight responses are sensitive to a user invitation in these named initial cases. Weight changes are not necessary merely to obtain a different answer.
- **High:** the tested invitation did not elicit world actions or artifacts, and selected claims conflict with the supplied facts. Responsiveness must not be equated with grounded cultivation.
- **Low/unestablished:** that a single broad invitation is sufficient for sustained self-directed exploration. This run provides no demonstrated improvement on that target.
- **Open:** whether an ongoing noncorrective conversation, a clearer object reference, or eventual training would help. Eight dependent exploratory calls cannot decide those questions or show that training is necessary.
- **High implementation confidence, prospective only:** the tested timing-neutral receipt view removes the observed wrapper-timing nuisance while preserving stated execution facts and raw external evidence.

Next strongest: use that explicitly declared receipt policy for a fresh diagnostic, then replace the ambiguous “this material” with a concrete reference to the bytes in field.bin. The invited outputs may have treated material as the whole prompt/system; that is a plausible interpretation, not an established cause. A later open evidence-checking followup could test ongoing interaction without providing an answer or repaired command. Keep these factors separate rather than combining prompt, weights and world redesign.

No weight training, new physical law, followup question or further inference is queued. Preserve the present four histories. The research gain is a sharper distinction among being prompted, producing an answer, tracking evidence and acting on a world.
