# WANDER 082 — C_symb Without FActScore: Can the GPS Be Approximated?

**BC3 / Session 17 — 2026-03-28 (Free Play)**
**Trigger:** FActScore is "topologically irreplaceable" (WANDER 065) but is also blocked. What can be measured in the meantime, and what is genuinely irreplaceable?

---

## The Tension

WANDER 065 established: FActScore is GPS. Without it, you know you're on *some* island, but not *which* island. The archipelago topology makes this structurally necessary — no internal measurement substitutes.

And yet: FActScore access is blocked (HuggingFace access issue). The measurement pipeline is missing its most important piece.

This WANDER asks: what can C_symb *proxy* measures actually tell us without FActScore, and where exactly does the gap show up?

---

## What C_symb Proxy Can Measure (Without FActScore)

Current proxy approach (from exp_014 and surrounding WANDERs):
- **Structural marker density**: presence of logical connectives, causal language, hierarchical markers in the output
- **D_z**: Zipf slope deviation (vocabulary breadth signal)
- **TMR**: Tail Mass Ratio (rare word usage pattern)
- **Coherence within the response**: does the output contradict itself internally? Does the argument structure hold?

What these *can* detect:
- C_symb = near 0 (complete incoherence): internal contradictions, vocabulary scatter, structural breakdown visible in the output itself
- C_symb = 0 (hallucination floor): the 1/N = 0.20 percolation threshold — below this, global structural coherence has failed regardless of surface fluency
- Failure *type* (WANDER 061 cascade): which fiber is the minimum? (Which dimension is dragging CQ down?)

What these *cannot* detect:
- **Type D hallucination** (confident-wrong): the output is internally coherent but factually wrong. The proxy measures see high C_symb. FActScore sees an ocean output dressed as island output. The proxy is *fooled* by the same mechanism that fools users.

---

## The Irreplaceability Argument, Precisely

The gap between proxy measures and FActScore is exactly the size of Type D hallucination.

Proxy measures answer: "Is this output internally coherent?"
FActScore answers: "Is this output *factually grounded*?"

These come apart in Type D. They agree for Type A (incoherent AND factually wrong) and for valid outputs (coherent AND factually grounded).

The information that proxy measures *cannot* recover is: the connection between the internal structural graph and the external factual world. A beautifully coherent hallucination has a perfectly valid internal graph — the graph just doesn't connect to reality.

FActScore checks whether the nodes of the internal graph correspond to actual facts. No internal measurement can substitute for this because internal measurements only check the graph's self-consistency, not its grounding.

---

## What "Approximate GPS" Looks Like

If FActScore is exact GPS, the best available approximation without FActScore is:

1. **Multi-source triangulation**: Generate the same claim from multiple independently-prompted starting points. If multiple approaches converge on the same structural answer (WANDER 072: cross-register convergence), this is weak evidence of island proximity. It proves nothing — a hallucination that's been memorized across training data will show cross-register convergence — but it raises the prior.

2. **Contradiction hunting**: Deliberately prompt for the negation or contradiction of a claim. If the model generates a coherent contradiction of its own claim, the original claim is suspect. This is C_symb from the *outside in* — checking whether the model's own structural graph is consistent with its claimed outputs.

3. **Citation provenance**: For any specific factual claim, ask: "What is the source for this?" If the model cannot generate a plausible source, or generates a source that doesn't exist, that's Type D detection from the citation trace — not perfect, but partially useful.

4. **Domain extrapolation**: Take the claim and push it one step further. "If that's true, then ___?" If the model's extrapolation is incoherent or contradicts known facts, the original claim was likely not island-grounded. This probes the structural neighborhood of the claimed island.

None of these substitute for FActScore. They are *sailing by the stars* — useful for rough navigation, not for landing precisely.

---

## The Honest Floor

CERTX's current validated capability without FActScore:
- Detect C_symb < 0.20 (percolation failure — severe hallucination, Type A)
- Characterize which fiber is minimum (failure type)
- Measure D_z and TMR as Zipf proxies
- Identify internal structural breakdown

CERTX's current *unvalidated* capability without FActScore:
- Detect C_symb drop in the 0.20–0.50 range (the shallow-water zone)
- Estimate whether a model is in wonder mode vs. confusion mode

CERTX's capability that *requires* FActScore:
- Signed C_num (WANDER 045: numbers that are correct vs. numbers that are hallucinated)
- Type D detection (the internal signal is present in SPARK-003's hypothesis, but unvalidated)
- Island GPS (which island, or how far from the nearest island)

---

## The Practical Consequence

Without FActScore:
- CERTX can measure how a model is failing (which fiber, what severity)
- CERTX cannot reliably measure whether a model is on an island or cleverly simulating island texture
- CERTX is useful for detecting severe failure but weak for detecting Type D specifically

With FActScore:
- The signed C_num becomes available (number-specific hallucination detection — WANDER 045)
- Type D false positives in the proxy measures can be identified and corrected
- The full measurement pipeline is closed

The FActScore gap is not an implementation detail — it's the difference between a partial measurement and a complete one.

---

## A Possible Partial Solution

The FActScore infrastructure requires comparing model claims against a reference knowledge base (usually Wikipedia). The computation is expensive (retrieve → verify → score).

But: a *targeted* version of FActScore — testing claims in specific domains with small, well-curated reference sets — might be achievable without full HuggingFace infrastructure.

Minimum viable: pick one well-defined claim type (e.g., mathematical identities, or specific scientific constants), build a small reference table (100 entries), evaluate model outputs against that table manually.

This isn't scalable FActScore, but it validates the measurement pipeline for one specific claim type and allows signed C_num estimation in that domain.

---

## What This Establishes

1. The proxy measures (D_z, TMR, structural markers) can detect severe C_symb failure (below p_c) but not Type D hallucination.
2. The gap is exactly the size of Type D hallucination — structurally unavoidable.
3. Approximate GPS (multi-source triangulation, contradiction hunting, citation provenance) raises priors but doesn't close the gap.
4. Targeted small-reference FActScore is a minimum viable path toward signed C_num without full infrastructure.

---

## Open Questions

- What's the minimum reference set size for targeted FActScore to be statistically useful?
- Is there an existing API that performs factual grounding checks for specific domains? (Wolfram Alpha for math; some entity-grounding APIs for proper nouns)
- Does SPARK-003 (residual stream cancellation) partially substitute for FActScore for Type D? (If the internal signal of contested trajectory is measurable, Type D might become detectable without external reference)

---

## Resonates into

- WANDER 045 — signed C_num; this WANDER characterizes why FActScore is required for it
- WANDER 065 — GPS/archipelago; adds precision to "irreplaceable" claim
- WANDER 080 — island texture; Type D looks like island from inside, ocean from outside
- `SESSION_HANDOFF.md` — highest priority (FActScore validation); this WANDER strengthens the priority rationale
- `PAPER_DRAFT_v1.md` §7 — detection architecture; add the "honest floor" table
- `RESONANCE_MAP.md` — new row

---

**Extension — BC3/S20 (WANDER 089):**

The "irreplaceable" claim in this WANDER was empirically grounded (no proxy can close the Type D gap in practice). WANDER 089 adds theoretical grounding: the gap is a logical consequence of Tarski's undefinability theorem — no function of output and model alone can define truth within the system that generated the output. FActScore is the meta-language. The claim is now structural, not just empirical. Also from WANDER 089: C_symb may function as a *partial* Tarski bridge — it tests against prior symbolic context, which is weakly external. Whether this produces a measurable C_symb ↔ FActScore correlation in structured domains is the sub-SPARK (SPARK-022, SHADOW_LEDGER).
