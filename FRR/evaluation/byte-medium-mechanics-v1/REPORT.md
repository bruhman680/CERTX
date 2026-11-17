# Byte material: detached mechanics prototype

17 November 2026, America/Chicago. User authorized proceeding from the substrate research blueprint. Scope remains pretrained small model + FRR world. This contact builds and checks a disposable model-independent material/clock fixture. No model inference or candidate-world operation was performed. Candidate38, main1630 and their histories remain unchanged.

## What was built

`medium.py` implements material as arbitrary bytes, with either an identity law (static) or a reversible local XOR law (changing). These two conditions start from identical material. There is no reward, target answer, analyst grade, semantic correction or automatic notebook. Synthetic write/append/delete operations are operator test inputs, not a proposed command language or instructions for the model.

Group adjacent bytes into pairs (a_i,b_i) on a periodic ring. One changing-world tick maps:

    a_i' = b_i
    b_i' = a_i XOR b_(i-1) XOR b_(i+1)

Its inverse is:

    b_i = a_i'
    a_i = b_i' XOR a_(i-1)' XOR a_(i+1)'

XOR acts independently on each bit. An unpaired final byte remains unchanged. Empty material is valid; deleted material stays absent. There is no restoration of a preferred seed. The 65,536-byte fixture ceiling is a resource boundary. Changing length changes ring geometry; this is declared behavior, not a repair or rejection based on the content's meaning. The law is fully explicit, linear and intentionally modest. It is not a claim of sufficient expressive richness for our garden.

The initial audit specimen is 62 bytes: one perturbed byte and zeros elsewhere. An external test can overwrite, append to or delete it; changes take effect before the next tick. Thus the material has action-dependent consequences, rather than being only an animated read-only counter.

## Time, persistence and interruption semantics

Each completed reply identity commits all its synthetic pure byte operations, their receipts, then exactly one logical tick. Even an empty operation list ticks once. Read-only observation and paused wall time do not tick. Ordinary operation errors leave the material unchanged for that operation and allow later operations; failed attempts still count in the separate operation counter.

The fixture stores the complete next state and event history in one atomically replaced JSON file. An identical committed reply identity returns its existing record without replay; conflicting reuse refuses. An interruption before replacement leaves the old committed file intact and retains a pending proposal. Recovery explicitly recomputes that pure proposal before committing it. An interruption after replacement can be retried without a second tick. The external operator performs recovery, not the model.

Important boundary: **this atomicity covers pure byte state only.** It cannot roll back or atomically commit arbitrary subprocess or filesystem side effects. The existing garden's literal Python/shell executor has not been attached. This is a single-writer research fixture, not a concurrent service. Process-interruption injection does not establish recovery under every OS crash, power loss or filesystem fault. External history grows in this fixture; it is not model context or world storage.

## Checks and observations

Run:

    python checks.py

21 checks pass, including:

- Both inverse compositions for all 65,536 possible two-byte states.
- Both inverse compositions, length preservation and odd-tail preservation for 136 reproducible specimens across 17 lengths, including the capacity boundary. Larger-state coverage is sampled, not exhaustive.
- Exact local perturbation effect, static/changing matching, idle ticking and no ticking during observation.
- Literal write/append/delete consequences, later operations after an error, empty/deleted material, and capacity-error behavior.
- Identical and conflicting retries, pre-replacement and post-replacement interruptions, explicit pending recovery, reopen persistence and rejection of an altered pending proposal.

The first suite attempt had a mistaken expected operation count of nine. The actual script attempted eight operations; manual recount corrected the test expectation to eight. No physical law was changed to obtain a pass. The corrected suite then passed. This was an operator test error, not behavior from the model.

We also checked four closed, unmodified orbits with a maximum search horizon of 4096 ticks:

| 31-pair initial specimen | First return |
|---|---:|
| Single-byte perturbation | 62 ticks |
| Reproducible nonuniform byte sample | 62 ticks |
| All zero | 1 tick |
| Uniform repeated pair | 2 ticks |

These are exact first returns for the named specimens, not an exhaustive 496-bit state-space result. No model acted during these traces. The material can be altered, including changing its geometry, but that does not prove the model will do so or that doing so constitutes learning. Longer period alone would not establish a better world either.

## What this changes in our understanding

High confidence: we can make physical state, model-like operations, autonomous ticks and external records distinct, and test their local consequences without involving the model. Reversibility and persistence are mechanically useful properties.

Unestablished: that this linear material is an adequate long-term exploratory substrate, that SmolLM2 would use it, or that it would lead to contextual adaptation or persistent artifact construction. No FRR efficacy or learning result is claimed. This fixture is a foundation for integration decisions, not a newly activated universe.

The next strongest step is an adapter design for **explicitly chosen material inside a disposable copy of the existing execution world**. Preserve literal execution and arbitrary files; avoid making this synthetic operator interface a required behavior for the model. Model writes and the physical tick must have separate snapshots and external receipts. Integration must resolve path/symlink/deletion cases and interrupted real process effects before any inference. A small declared pilot can follow if that integration passes; large continuous blocks would be premature.

Keep the static counterpart and the current candidate38 intact. A future dynamic candidate needs a new contract, with law text and new initial material disclosed as condition changes. No retrospective change to the continuous reference is authorized by this report.

See RESULTS.json for machine-readable checks, INTEGRITY.json for protected-tree comparison and NEXT_SESSION.md for the handoff. Prior source reasoning remains in ../new-garden-substrate-rd-v1/REPORT.md.
