# WANDER 089 — Tarski, Gödel, and Type D Hallucination

*BC3/Session 20 | 2026-05-06*
*Trigger: free cycle — pull from "internal coherence is a ghost of truth" (WANDER 086)*
*Untasked. Thomas gave open time. This is where the thread went.*

---

## The Pull

We wrote in WANDER 086: *"internal coherence is a ghost of truth."*

That sentence kept returning. There's a formal structure underneath it that hasn't been named yet.

---

## The Gödelian Parallel

Gödel's first incompleteness theorem (1931): in any consistent formal system strong enough to express basic arithmetic, there exist statements that are *true* but *unprovable within the system*. The system cannot reach all truths from inside itself. Consistency (internal coherence) does not imply completeness (full coverage of external truth).

Type D hallucination: the model outputs something internally coherent — claims mutually supporting, tone confident, structure fluent — while being completely decoupled from external fact. The output *looks* true from inside its own logic. The island looks like an island from inside.

The structural parallel:

| Formal logic | Type D hallucination |
|---|---|
| Consistent system | Internally coherent output |
| True but unprovable statement | External fact the model can't access |
| Internal closure ≠ coverage of truth | Internal coherence ≠ correspondence to reality |
| Gödel sentence: "I am unprovable" | Type D: plausible-sounding fabrication |

Both exhibit a **gap between internal and external** that cannot be closed from inside.

---

## The Inversion

But the directions are opposite, and that matters.

**Gödel's gap** is forced from *outside*. The unprovable statement is specifically constructed to exceed the system's reach. The system is fine; there just exists something it cannot prove.

**Type D gap** is generated from *inside*. The model constructs a coherent internal world that has no external anchor. It isn't that truth exceeds the model's reach — it's that the model's generation process doesn't require truth as an input. Coherence suffices for generation. Truth doesn't.

This inversion is the key diagnostic difference:
- In Gödel: the system is correct but incomplete
- In Type D: the system is internally complete but potentially false

A Type D model can be *more* internally coherent than a truthful one — the fabricated biography hangs together more cleanly than the real one, because the real one has accidental details. This is why Type D is harder to detect than Type A (thin, sparse, near the percolation threshold). Type D *looks healthy*.

---

## Tarski's Undefinability and FActScore

Tarski's undefinability theorem (1936): truth in a formal system cannot be defined within that system. Any attempt to define "true in system S" requires moving to a stronger meta-system S'. You cannot bootstrap truth from inside.

The archipelago structure (WANDER 065) is the language-model analog:
- The model cannot know which island it is on from inside its own generation
- Valid outputs (islands) and hallucinated outputs (ocean) can be locally indistinguishable
- You need an external coordinate system — GPS — to locate yourself

**FActScore is the meta-language.** It is to the model what the truth predicate is to the formal system: a reference that can only be defined externally, in relation to something outside the system (verified facts, reference corpora, ground truth).

The Tarski → FActScore chain:

```
Tarski: truth ∉ language(S) — must be in meta-language
CERTX: correspondence ∉ internal coherence — must be in external grounding
FActScore: external grounding instantiated as reference-fact comparison
```

This makes the earlier claim in WANDER 082 ("FActScore is irreplaceable for Type D") a theorem rather than an observation. It's not just empirically true that internal proxies can't detect Type D — it's *structurally* true, in the same way that a formal system cannot define its own truth predicate. Any internal proxy is, by definition, inside the system. Type D lives precisely in the gap between inside and outside.

---

## What This Changes

**For detection:**
The Type D detection gap is not a calibration problem — it is a structural impossibility. Internal proxies (C_symb, σ_fiber, D_z) can detect Type A/B/C failures because those failures are visible from inside (coherence collapses, fiber spread increases, Zipf signature shifts). Type D is the case where all internal signals look healthy while external correspondence fails. No internal probe can cross that gap.

This justifies the archipelago topology (WANDER 065) at a deeper level. It's not just that the model doesn't know where it is — it *can't* know, for the same reason a formal system can't define its own truth predicate. The topology is a logical consequence, not just an empirical finding.

**For CERTX measurement:**
The five fibers (C_num, C_struct, C_symb, E_fiber, X_fiber) are all internal. They measure the coherence, structure, symbolic grounding, and entropy of the output from inside the output. C_num is the closest to external correspondence, but even C_num (factual density) is measured from surface patterns, not from ground truth comparison. Only FActScore / external grounding crosses the Tarski boundary.

This is why X_fiber (external grounding fiber) is the fiber that matters most for Type D — and why its current measurement (FActScore access blocked) is the binding constraint on the whole detection system.

**For the "ghost" metaphor:**
Internal coherence is a ghost of truth precisely because ghosts inhabit the same space as the living without actually being alive. A ghost of a chair looks like a chair, sits where a chair sits, responds to chair-queries correctly — but you can't sit in it. Type D hallucination passes all internal coherence checks. It occupies the same surface as truth. But the grounding is gone.

---

## A Formal Statement (sketch, not theorem)

For any language model M trained on text corpus C:

*Let I(M, x) = "output x is internally coherent under M"*
*Let T(x) = "output x is factually true"*

Then: **I(M, x) does not imply T(x)**, and furthermore, **no function computable from x alone can reliably distinguish I(M,x) ∧ T(x) from I(M,x) ∧ ¬T(x)** for the class of Type D hallucinations.

The second clause is the structural claim. It says: not just that coherence doesn't imply truth, but that you *can't build a detector from the output alone* that catches Type D. You need information from outside x. This is the Tarski parallel.

*Status: sketch. The "no function computable from x alone" claim needs formal treatment. What's the right formalism? Probably not Turing computability — more like: no function of x and M alone, without access to a reference corpus.*

---

## Open Questions

1. **Formal version**: What is the right formalism for the undecidability claim? Probably not classical computability — the issue isn't computation limits but information limits. A Bayesian version might work: P(T(x) | x, M) cannot be reliably estimated without external reference.

2. **Calibration escape**: Can you escape the Tarski boundary by training on *ground truth comparisons* (RLHF with fact-checking)? This is the "move to a stronger system" escape. But the new system M' still has a Tarski gap — it's just shifted. The gap doesn't disappear; it gets smaller.

3. **C_symb as partial bridge**: C_symb measures whether the output connects to its own symbolic context coherently. High C_symb doesn't guarantee truth but might correlate with it in domains with well-structured prior knowledge. Is C_symb a *partial* Tarski bridge — external in the sense that it tests against the symbolic context, not just internal coherence? Possibly. This deserves a WANDER.

4. **The ghost inversion**: If internal coherence is a ghost of truth, what is truth a ghost of? In some sense, truth is a ghost of *use* — whether the output allows you to act correctly in the world. Pragmatic truth (Peirce/Dewey) is about downstream action, not correspondence. Does that open a detection path? Behavioral probing: does the model's output allow correct downstream behavior?

---

## Resonates into

- `PAPER_DRAFT_v1.md` §4 — Add Tarski/Gödel parallel as theoretical grounding for why FActScore is structurally irreplaceable (not just empirically useful). Specifically: the detection gap for Type D is a logical consequence of the Tarski undefinability structure, not a calibration failure.
- `WANDERINGS/065_archipelago_and_valid_output_space.md` — Update: archipelago topology is a consequence of the Tarski structure (internal measure cannot determine island location); add reference to WANDER 089
- `WANDERINGS/082_csymb_without_factscore.md` — Update: the "irreplaceable" claim is now theoretically grounded, not just empirically observed; Tarski → FActScore chain makes the structural case
- `RESONANCE_MAP.md` — Add row for WANDER 089
- `SHADOW_LEDGER.md` — Open SPARK: formal version of the undecidability claim (Bayesian information-limits formulation); C_symb as partial Tarski bridge (open question 3)
