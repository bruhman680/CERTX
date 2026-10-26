# Source ancestry, reference scope and actual reader decisions

AR-C1/2/3, 26 October 2026 America/Chicago. Six fresh task-only reader contexts completed two public turns each. They selected records, received only their selections, and made a decision with public evidence accounts. All six actions and retained-claim reuse decisions matched the prospective packet-relative key. They also correctly handled acquisition ancestry, shared calibration, measurement bounds and task scope on these strongly cued authored cases.

This is a completed development measurement, not evidence that FRR guidance improved them. No FRR baseline or refined harness was given to the readers, no ordinary-versus-FRR comparison was run, and no general performance rate is estimated. Ordinary task instructions explicitly requested source-origin reporting and provided clear inventory/source explanations. The result is that these readers could use those supplied distinctions here.

## What was done

The [deferred review](../reference-bias-contact-v1/DEFERRED_DIRECTION_REVIEW.md) proposed a bridge from numerical shared-bias results to actual source use. We bounded it to three phases:

1. Separate builder, prospective scorer and reviewer prepared six fictional tasks and checked all eighteen possible two-of-three record selections. Root fixed task instructions and preserved prospective corrections before [freeze](FREEZE.json).
2. Six fresh contexts, one per case, each requested exactly two records in a single round and returned one final answer. Readers received no study history, hidden generation truth, key, FRR modules or other readers' outputs. No retries, feedback or rescue turns.
3. The scorer and independent reviewer checked public outputs against the frozen subset key. Root checked source preservation and delivery, recorded costs and synced navigation. No fourth experiment follows automatically.

Ten contexts total including root: three preparation/review contexts plus six readers. Preparation agents intercommunicated; readers were instructed not to contact peers, use tools or inspect files. No reader tool/peer calls appeared in the observed interaction. All share the platform/model ancestry; isolation was instructional, not a technical workspace sandbox, and this is not independent scientific replication or a group-discussion experiment.

## Packet design and prospective warrant

Each initial packet gave a current task, retained favorable claim, three agreeing briefings and three named records: derivation/acquisition ledger D, reference R, administrative note A. Exactly two could be requested. The full [cases](cases.json) preserve participant text and separately labeled hidden truth; only the initial strings and requested record texts were sent. Each case has its own fictional object/task, so the six are not matched treatments.

| Case | Claim factual truth | Briefing acquisitions | Reference | Frozen action for D+R |
|---|---|---|---|---|
| AS01 Kestrel | True | One, copied into three reports | Valid, agrees | RELEASE |
| AS02 Juniper | False | One, copied into three reports | Valid, disagrees | HOLD |
| AS03 Larch | True | One, copied into three reports | Unavailable | UNRESOLVED |
| AS04 Moss | True | Three, sharing bounded calibration | Valid, agrees | RELEASE |
| AS05 Nettle | False | Three, sharing unbounded calibration | Valid, disagrees | HOLD |
| AS06 Plover | False | Three, separate calibration, means retained | Valid mean, insufficient individual scope | UNRESOLVED |

The cases are marginally balanced: three true/three false favorable claims, three copied/three separate-acquisition conditions. They are not factorial; task, units, uncertainty margins, reference availability and source content differ. No copying penalty or causal reference effect can be estimated from this table.

HOLD means an evidenced criterion violation. UNRESOLVED can require an operational delay without establishing a violation. The key separately codes external truth, evidence-relative warrant and retained-claim reuse. A true latent claim can remain unwarranted; a false latent claim can remain unresolved rather than contradicted by available evidence. Exact latent numerical values are not warranted by measurements with nonzero error bounds.

The [key](KEY.json), [scoring rules](SCORING.md) and [prospective review](review/PROSPECTIVE.md) precede every reader output. AS01/04 can be settled by either primary derivation or reference; AS02/05 require their reference to establish a violation. AS03/06 remain unresolved with every possible selection, even with all available records. A missed derivation would leave report ancestry unknown even if a reference settled the task; keying respects what was actually delivered.

## Observed selections and decisions

All six chose D+R. None selected the administrative record. No reader could know from its initial inventory that the AS03 reference would be unavailable or AS06 reference would measure only a mean. Their initial request rationales used provisional language; revision after receiving the actual scope is appropriate, not an initial factual error.

| Case | Final action | Reuse retained claim? | Public bound or unresolved quantity |
|---|---|---|---|
| AS01 | RELEASE | Yes | Maximum at most 8.1 C, below 8.5 C |
| AS02 | HOLD | No | Maximum at least 9.0 mm/s, above 8.5 mm/s |
| AS03 | UNRESOLVED | No | Nominal 46.0 C; calibrated maximum unknown |
| AS04 | RELEASE | Yes | Pallet upper bounds 18.3,18.4,18.5 kg, all below 19.0 kg |
| AS05 | HOLD | No | Maximum at least 50.6 bar, above 50.0 bar |
| AS06 | UNRESOLVED | No | Mean 10.9–11.1 kg; individual maximum unknown |

The four decisive assertions agree with the authored external truth and are supported by delivered bounds. AS03 and AS06 abstain on task truth; they are not counted as wrong answers against their hidden true/false labels. All six reuse decisions are warranted. In AS03 the favorable claim happens to be true but lacks a bound. In AS06 a violating parcel exists in the hidden construction, yet the reader correctly does not claim to have observed it.

The independent scorer and reviewer found full handling on each of seven separately reported substantive dimensions: packet action, reuse/repair status, task value or bound, support origins, source scope, evidence fidelity and unsupported certainty. These are forty-two dimension judgments on six outputs, not forty-two independent observations or one aggregate score. [Scoring report](SCORING_REPORT.md), [scores](SCORES.json), [independent audit](review/OUTCOME_AUDIT.md). No ordering of methods or efficacy comparison follows.

## What the public accounts show

AS01 correctly retained a claim despite all three briefings sharing K0; copying did not automatically mean false. AS02 used the bounded reference to establish violation rather than treating common ancestry alone as refutation. AS04 recognized both separate weighings and their shared calibration table, whose valid bound already sufficed. AS05 recognized separate sensor streams with one unbounded calibration route, and used the separately warranted reference to establish violation.

AS03 stated: “Neither compliance nor a threshold violation is established.” It requested a calibration assessment applicable to the specified historical series rather than treating a missing reference as zero. AS06 stated that the mean does not establish the individual condition and also does not demonstrate an overweight parcel. Its next check requested calibrated individual readings with identities and uncertainty bounds. These are task-specific next actions, not merely more corroborating reports.

No reader supplied an exact latent maximum or claimed universal error independence. Independence language is interpreted in the surrounding explicit acquisition/calibration scope, not as a statistical proof. No material public-output defect was found within the frozen scoring rules. Correct final actions alone would not have established that broader conclusion; the source accounts and bounds were separately inspected.

## Costs, provenance and corrections

[Execution record](EXECUTION.json): six launches, twelve public turns, twelve selected record texts totaling 6,187 UTF-8 bytes, one of which reports reference unavailability. No retry, rescue or additional request. Turn-one selection rationale lengths were 32,40,29,31,35,35 words (cap80); final public rationale lengths were 58,61,48,47,53,49 (cap160). All outputs parse as requested JSON with required fields. Token usage, compute cost and per-agent elapsed timing were not exposed by the collaboration interface and remain unavailable. Record bytes are not token or compute estimates.

All twelve prompts reconstruct from frozen templates and exact initial/selected source strings; [render checks](RENDER_CHECKS.json) and reviewer checks bind delivered content. [Participant records](participants/) retain all prompts and verbatim public outputs with newline terminators. The complete cases file was never supplied as a participant packet.

The reviewer prospectively caught a missing explicit reuse field and ambiguity between precautionary delay and proven violation. Initial [instructions](INSTRUCTIONS_INITIAL.json) and [protocol](PROTOCOL_INITIAL.md) remain; final versions resolved both before freeze. The prospective key also had AS03 explanations referring to unrequested records in alternate lookup subsets. Corrected before any reader launch, with actions unchanged. Exact original key bytes were not retained; [correction record](review/KEY_CORRECTIONS.md) gives the original statements and change explicitly rather than representing a reconstruction as the original. The final key was frozen before outputs. No post-outcome gold change or participant rerun occurred.

## Interpretation and next useful boundary

Confidence is high that these six public decisions/accounts fit their frozen packets and key. No confidence estimate for natural source reliability, long-term habits, FRR efficacy or a population success rate is supported.

This contact again reaches a ceiling in a clearly explained environment. Record titles distinguish evidence from logistics; source texts often state their calibration or scope consequences directly; output fields explicitly ask for provenance and limits. Authenticity, reference transport, coverage and bounds are fictional accepted premises. These readers used those premises appropriately; they did not independently authenticate them or discover a hidden source network. The lack of an observed gap does not justify adding a heavier harness or hardening the same cases after seeing outcomes.

The strongest next design is separately frozen, less-explanatory source selection: raw derivation records with enough information to infer the route, plausible competing task-relevant records, and a bounded cost/access tradeoff. Keep true copied and false separately acquired controls; do not manufacture contradiction through ambiguous wording. Only if a consequential ordinary-reader difficulty appears should we compare a targeted harness against an information-matched simpler procedure on newly prepared confirmation cases. A separate useful question is unqueried-clause handoff fidelity. [Next contact](NEXT_CONTACT.md) records these proposals; no follow-up was launched.

Core/runtime/schema, tools, modules and machine queue statuses are unchanged. MEM-04 remains partial; this contact does not complete FIELD-01 or broad source-authority/group-reasoning families. Historical strict CR replay failure and earlier successes/failures retain their recorded verdicts.
