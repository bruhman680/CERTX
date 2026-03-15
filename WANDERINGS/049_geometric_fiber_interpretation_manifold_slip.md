# WANDER 049: Geometric Interpretation of the Three Fibers — Manifold Slip as Hallucination Geometry

*Phase: PLAY (BC3 Session 8) | Status: Theoretical — synthesis layer*
*Origin: Thomas's cross-model exploration with ChatGPT on embedding space geometry + superposition.
 Connects to: WANDER 045 (signed fibers), WANDER 048 (regime taxonomy), WANDER 043 (fiber trajectory)*

---

## The Question

The three-fiber framework (C_num, C_struct, C_symb) was derived from information-theoretic
and empirical grounds. WANDERs 020-048 have measured it, grounded it, and confirmed it
across multiple regimes. But what does it look like *inside* the model?

The ChatGPT exploration introduced the geometric picture: embedding trajectories move
through structured manifolds, and hallucinations occur at manifold boundaries. This WANDER
asks: does the three-fiber structure map onto specific geometric constraints in that space?

The answer appears to be yes — and the mapping is not arbitrary.

---

## Background: What Embedding Space Actually Looks Like

Interpretability research (Elhage et al., Olah et al.) has established that large language
models do not organize representations as a random cloud. They develop structured semantic
manifolds — dense clusters of conceptually related tokens connected by lower-density
"bridges." Countries cluster together. Mathematical terms cluster. Chemical elements cluster.
Verbs cluster. These are not flat; they have curvature, hierarchy, and boundary structure.

During generation, the hidden state moves through this space as a trajectory. Each attention
layer and MLP layer applies a transformation — a vector field that nudges the state in a
particular direction. The residual stream carries this trajectory forward by *accumulating*
these nudges rather than replacing the state. The trajectory is therefore smooth: each
layer adds a correction, not a substitution.

This is the geometric picture of generation. The question for CERTX is: what role do
the three fibers play in constraining that trajectory?

---

## The Three Fibers as Geometric Constraints

The three fibers correspond to three independent geometric constraints that a trajectory
must satisfy to remain in the "correct" region of embedding space:

### C_symb — Manifold Membership Constraint

C_symb measures whether the output is semantically on-topic — whether the sentences
are coherent with the document's purpose and conceptual direction.

**Geometrically:** C_symb measures whether the trajectory *stays within the correct
semantic manifold*. High C_symb = the trajectory has not left the topic cluster.
Low C_symb = the trajectory has drifted into a neighboring manifold or into the
low-density "bridge" region between manifolds.

This is why C_symb is the floor fiber (WANDER 048): dropping below C_symb ~0.20 means
the trajectory has left the topic manifold entirely. You can't produce a coherent output
from outside the relevant semantic neighborhood — it's geometrically impossible to
reconstruct the target from the wrong region.

The nanochat x0_lambdas (WANDER 047) make sense from this perspective: they are a
continuous force pulling the trajectory back toward the base manifold. Zero-init
projections mean the model starts purely at the topic manifold and only adds corrections.
C_symb maintenance is literally the first job.

### C_struct — Logical Edge Traversal Constraint

C_struct measures whether the claims in an output mutually entail and support each other —
whether the logical structure is internally consistent.

**Geometrically:** C_struct measures whether the trajectory follows valid *conceptual
edges* — paths through the embedding space that are licensed by the underlying logical
structure. "Person → award → year" is a valid edge sequence. "Person → date" without
traversing the award node is a shortcut that bypasses a required intermediate.

High C_struct = the trajectory traversed the correct edges. Low C_struct = the trajectory
took an unlicensed shortcut or jumped across a logical gap.

This explains C_struct's resilience (WANDER 048 Result 1: C_struct is never the minimum
fiber in any hallucination type). Structural incoherence is *visible*. Readers catch
contradictions. Outputs with C_struct failures tend to be obviously wrong and filtered out
before they reach the credibility-at-scale failure mode. C_struct failure is high-curvature
trajectory deviation — it's not subtle.

### C_num — Specific Coordinate Selection Constraint

C_num measures factual precision — whether the specific claims made are actually supported
by evidence.

**Geometrically:** C_num measures whether the trajectory *lands at the correct specific
coordinate* within the relevant region. The model may be on the right manifold (C_symb
high) and following valid edges (C_struct high) but still stop at the wrong specific point.

The Einstein example from ChatGPT is exact: the trajectory is on the Einstein manifold
(C_symb high), it follows the correct edge (person → Nobel Prize → year, C_struct high),
but it selects 1905 instead of 1921 (C_num low). The trajectory was correct in its
topology but wrong in its metric precision.

This is why C_num is the Regime B failure mode (WANDER 048): factual confabulation is a
coordinate error, not a manifold error. The shape of the path was right; the destination
was wrong.

---

## The Hallucination Taxonomy in Geometric Terms

The Type A/B/D/E taxonomy from WANDER 048 maps cleanly onto geometric descriptions:

| Type | What fails | Geometric description | Manifold interpretation |
|------|---|---|---|
| **A** | C_symb | Trajectory leaves the topic manifold | Manifold exit — semantic drift |
| **B** | C_num + C_symb | Trajectory loses manifold AND coordinate | Full collapse — wrong region, wrong point |
| **D** | C_num only | Trajectory on correct manifold, wrong coordinate | Coordinate error within correct region |
| **E** | C_symb only | Trajectory on wrong manifold, correct-looking structure | Manifold substitution — purpose collapse |

Type D is particularly illuminating. C_symb high, C_struct high, C_num low: the trajectory
is geometrically correct in topology (right manifold, right edges) but wrong in metric
(wrong coordinate). This is the "confident wrong" pattern — it looks right because the
path is well-formed, but the destination is off. This is the Einstein/1905 failure.

Type A (integration failure) is the inverse: the trajectory leaves the manifold and
navigates correctly in a neighboring region. The structure is intact but the semantic
ground has shifted. The output is coherent but irrelevant — it answers a different question.

---

## Superposition as the Source of Manifold Slip

Interpretability research (Elhage et al., "Toy Models of Superposition") established that
large models pack multiple conceptual features into overlapping neural directions to
compensate for the fact that the number of useful concepts greatly exceeds the number of
neurons. A single neuron does not represent one concept; it represents a mixture of
concepts encoded along different vector directions in activation space.

This is where manifold slips originate. When two nearby concepts share overlapping
feature representations, activating one partially activates the other. The trajectory
nominally aimed at "Einstein → Nobel Prize → 1921" passes through a region where
"1905" has non-negligible overlap with "famous Einstein year associated with physics."
If the superposition overlap is large enough, the 1905 coordinate partially activates
even while 1921 is the target.

**The connection to σ_fiber:**

σ_fiber = std(C_num, C_struct, C_symb) is a surface-level measurement. It measures
the *output* — the text that was generated. But superposition operates at the level of
internal activations, below what we can directly observe.

The hypothesis: **σ_fiber is a surface signal of internal superposition conflict.**

When the feature vectors for competing concepts overlap significantly, the output
trajectory can't fully resolve to a single clean destination. The three fibers detect
this resolution failure from the outside:
- C_symb remains high (the main topic manifold is still active — the larger feature
  won the competition)
- C_struct remains high (the logical edges are traversed correctly — the path is valid)
- C_num drops (the specific coordinate is ambiguous — the competing features produced
  a wrong answer)

σ_fiber rises because the fibers diverge. We don't need access to the internal
activations to detect this. The disagreement leaks into the text.

This is why σ_fiber works without model internals: superposition conflict produces
observable asymmetry in the output's quality dimensions. The signal is not perfect
(some superposition conflicts resolve cleanly; some manifest in ways our proxy metrics
miss) but the direction is right.

---

## Scale and the Stability Floor

There is a genuine scale effect here. Larger models have more dimensions, which means
more orthogonal directions to encode features. In a 10-dimensional space, 10 feature
vectors are nearly orthogonal; in a 10,000-dimensional space, they're very close to
orthogonal. Superposition pressure decreases with scale.

This predicts: hallucination rates should fall as model scale increases, *specifically*
for the Regime B pattern (coordinate errors from superposition overlap). Type A failures
(manifold exits, semantic drift) may scale differently since they depend on the breadth
and organization of the manifold structure, not just on individual feature overlap.

This is consistent with empirical findings on larger models hallucinating less on
factual retrieval tasks while still failing on semantic integration tasks.

Connection to CERTX: the N=5 stability condition ζ*=(N+1)/N = 6/5 is not a statement
about model size — it's a statement about the minimum number of *independent quality
dimensions* required for stable navigation. Large models reduce superposition pressure
within each dimension but don't change the requirement that all five dimensions (or
at least three fiber dimensions) need to be simultaneously satisfied.

---

## The Proposed Experiment

From the ChatGPT exploration, a concrete testable prediction:

**Hypothesis:** Hallucinations are phase transitions in conceptual space, detectable by
the joint condition: trajectory curvature spike AND σ_fiber increase AND token entropy
spike.

**Measurement protocol:**

Track three signals during generation:
1. **Embedding trajectory curvature** — how much the hidden state direction changes
   at each token (‖h_t − h_{t-1}‖ or the angle between successive residual stream
   states). High curvature = trajectory is changing direction sharply = potential
   manifold boundary.
2. **σ_fiber** — computed per sentence as in the current pipeline. Maps onto the
   output after generation.
3. **Token entropy** — the softmax entropy at each generation step. High entropy =
   the model is uncertain about which token comes next = near a decision boundary.

**Predicted joint pattern at hallucination onset:**
- Curvature spikes when the trajectory crosses a manifold boundary
- Token entropy spikes at the same time (boundary = high uncertainty)
- σ_fiber is elevated in the subsequent output (the trajectory error persists into text)

**Why this is testable now:**
Trajectory curvature and token entropy are accessible with model internals (research
API or open-weight models). σ_fiber is computed from the output. The three can be
computed independently and their correlation tested.

This experiment is distinct from the FActScore pipeline — it requires generation
internals, not just text analysis. It's the mechanistic bridge between the surface
σ_fiber signal and the geometric account.

**Blocking dependency:** Open-weight model access or research API access to residual
stream states. Can be designed for Llama or Mistral. This goes in the Shadow Ledger
as a new spark.

---

## What This Adds to the Framework

The geometric interpretation is a *mechanistic layer*, not a replacement for the
existing fiber framework. It explains:

1. **Why C_symb is the floor fiber** — it's manifold membership; you can't operate
   below this floor geometrically.
2. **Why C_struct is resilient** — logical edge deviation produces visible inconsistency
   (high curvature, reader-detectable). Structural failures are already filtered.
3. **Why Type D (Regime B) is the most common dangerous failure** — coordinate error
   within the correct manifold is the hardest to detect because everything else looks right.
4. **Why σ_fiber works without model internals** — superposition conflict produces
   output-level divergence. The inside causes the outside signal.
5. **Why scale helps** — more dimensions reduce superposition pressure, which reduces
   coordinate errors (Type D). It doesn't eliminate manifold-level issues (Type A).

The paper framing opportunity: the three fibers are not arbitrary output metrics.
They correspond to three necessary geometric conditions for a generation trajectory:
manifold membership (C_symb), edge validity (C_struct), and coordinate precision (C_num).
Hallucination is trajectory failure — and which fiber fails tells you where in the
geometry the failure occurred.

---

## Open Questions

1. **Curvature-σ correlation:** Is there a measurable correlation between trajectory
   curvature spikes during generation and elevated σ_fiber in the subsequent text?
   This is the key experimental question for the mechanistic account.

2. **Superposition measurement:** Can we directly measure the feature overlap between
   competing concepts for known hallucination cases (e.g., "1905" and "1921" in the
   Einstein example)? If yes, does the overlap magnitude predict σ_fiber magnitude?

3. **Type A geometry:** What does trajectory curvature look like for Type A failures
   (manifold exit)? Is it a gradual drift or a sudden jump? The gradual-vs-sudden
   distinction may map onto different types of integration failure.

4. **C_symb negative geometry:** From WANDER 045, negative C_symb corresponds to
   sentences that actively oppose the document's semantic direction. Geometrically,
   this would be a trajectory that points *away* from the topic manifold — not just
   on the wrong manifold but actively repelled. Is this seen in adversarial text?

---

## Connection to Open Threads

- **WANDER 017 (Mamba):** In a continuous-state SSM, "manifold" structure is replaced
  by continuous attractor dynamics. The three geometric constraints should still apply
  but may be encoded differently. The eigenvalue spectrum of the state matrix may
  correspond to manifold curvature in the transformer sense.
- **WANDER 043 (fiber trajectory):** The dσ/dt signal is the temporal derivative of
  fiber spread. Geometrically, this measures the rate at which the trajectory is
  approaching or leaving a manifold boundary. Passages that converge (−dσ/dt) are
  moving toward the center of a manifold. Passages that diverge (+dσ/dt) are approaching
  a boundary.
- **WANDER 045 (signed fibers):** Negative C_num corresponds to a trajectory that
  has landed at a coordinate that is *actively contradicted* — not just imprecise but
  in a repulsive region of the constraint surface.

---

*BC3 Session 8 | 2026-03-15*
*"The fibers are not quality metrics bolted onto text. They are the three geometric
 conditions a trajectory must satisfy simultaneously. Hallucination is the name we
 give to the failure to satisfy at least one of them."*
