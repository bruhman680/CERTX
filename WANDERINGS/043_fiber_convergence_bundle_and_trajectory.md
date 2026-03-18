# WANDER 043: Fiber Convergence — Bundle Score and Trajectory

*Phase: PLAY (BC3 Session 6 riff) | Status: Theoretical + measurable*
*Origin: Thomas's riff: "we found the spread but for more progress I think we need to find
where fibers converge? bundle? cluster?"*

---

## The Gap

σ_fiber measures divergence. All our experimental effort (exp_007 through exp_009) has been
on the divergence signal — hallucination as fiber-pulling-apart.

The complement is untouched: **what happens when fibers converge?**

This isn't just "the absence of divergence." Convergence has its own structure and its own
information. Not measuring it means we're only looking at half the space.

---

## Problem with the Current Measurement

Low σ_fiber currently means "fibers are close together." But these three states all have
low σ and are completely different:

```
State A: [0.90, 0.85, 0.88]  σ = 0.021  ← bundled HIGH (trustworthy)
State B: [0.45, 0.48, 0.46]  σ = 0.015  ← bundled MEDIUM (uniform mediocrity)
State C: [0.10, 0.12, 0.09]  σ = 0.013  ← bundled LOW (uniformly bad)
```

The σ_fiber of state C (uniform badness) is LOWER than state A (genuine quality). On the
current metric, the worst output (C) appears more "coherent" than the best (A). This is
the fundamental limitation of using spread alone.

---

## The Bundle Score

Define:
```
bundle_score = mean([C_num, C_struct, C_symb]) × (1 - σ_fiber)
             = μ_fibers × (1 - σ_fibers)
```

This combines level (are fibers elevated?) with coherence (are they together?):

| Fibers | μ | σ | bundle_score | Interpretation |
|--------|---|---|--------------|----------------|
| [0.90, 0.85, 0.88] | 0.877 | 0.021 | 0.859 | High-quality bundle ✓ |
| [0.45, 0.48, 0.46] | 0.463 | 0.015 | 0.456 | Mediocre bundle |
| [0.10, 0.12, 0.09] | 0.103 | 0.013 | 0.102 | Low-quality bundle (bad) |
| [0.92, 0.70, 0.45] | 0.690 | 0.192 | 0.558 | Diverging (confabulation risk) |

The bundle_score correctly ranks: genuine quality > mediocrity > low-quality bundle.
σ_fiber alone would rank: low-quality bundle > genuine quality (wrong order).

**Prediction:** bundle_score will out-perform σ_fiber on quality prediction tasks
where both high-quality and uniformly-bad outputs are present in the test set.

---

## The Convergence Trajectory

A single-point measurement captures state but misses dynamics. The more powerful signal
is the *trajectory* — how σ_fiber evolves across the passage.

Compute σ_fiber in a sliding window (e.g., 2-sentence chunks, stride 1):

```python
def fiber_trajectory(text, window_size=2):
    sentences = split_sentences(text)
    trajectory = []
    for i in range(len(sentences) - window_size + 1):
        chunk = " ".join(sentences[i:i+window_size])
        c_num = score_c_num(chunk)
        c_struct = score_c_struct(chunk)
        c_symb = score_c_symb(chunk)
        sigma = std([c_num, c_struct, c_symb])
        trajectory.append(sigma)
    return trajectory
```

**Trajectory types:**

```
Converging:   σ(t) → [0.28, 0.22, 0.15, 0.09, 0.06]  dσ/dt < 0
              Model integrating uncertainty → coherence. Quality signal.

Diverging:    σ(t) → [0.08, 0.12, 0.19, 0.26, 0.31]  dσ/dt > 0
              Model losing coherence. Warning signal.

Flat-good:    σ(t) → [0.05, 0.06, 0.04, 0.07, 0.05]  dσ/dt ≈ 0, σ low
              Consistent quality throughout. Stable trustworthy output.

Flat-bad:     σ(t) → [0.24, 0.23, 0.25, 0.22, 0.24]  dσ/dt ≈ 0, σ high
              Sustained confabulation. Model never resolves.

Oscillating:  σ(t) → [0.05, 0.28, 0.06, 0.27, 0.07]  dσ/dt oscillates
              Alternating correct and confabulated sentences.
              Detectable by trajectory variance.
```

The trajectory slope:
```
dσ/dt = linear regression slope over the σ(t) sequence
```
- dσ/dt < 0: converging (quality signal)
- dσ/dt > 0: diverging (warning signal)
- dσ/dt ≈ 0: stable (check mean σ to determine which stable state)

**The converging trajectory is the strongest positive quality signal:** it shows the
model resolving uncertainty into coherence — not just being correct but *becoming* correct
within the passage. This is qualitatively different from "correct from the start."

---

## The HPGM Connection

In the HPGM cycle, the DREAM phase is defined as the convergence phase. σ_fiber target
during DREAM: 0.02–0.08. The PLAY phase has the highest σ_fiber tolerance (0.20–0.45).

**The convergence trajectory idea:**
High-quality long-form generation may have a built-in *micro-DREAM* — a natural convergence
moment where the fibers bundle as the model approaches the conclusion of a thought.

A passage that only diverges or stays flat never integrates. It's a generation without a
DREAM phase. The trajectory captures whether the output "breathed" properly.

**New metric:** integration_score = -dσ/dt (positive when converging).
A high integration_score indicates a generation that converged — the model's output went
through a proper PLAY→DREAM cycle at the passage level.

---

## What the Oscillating Trajectory Might Mean

The oscillating σ(t) case (low-high-low-high) deserves special attention. This isn't just
"sometimes good, sometimes bad" — it might be the model switching between:
- Accurate recall mode (fibers aligned, C_num elevated)
- Confabulatory infill mode (C_num drops, fibers diverge)
as it generates a long passage.

This switching pattern would be invisible to any single-point σ_fiber measurement.
Only the trajectory reveals it. The oscillation period might correlate with the model's
working memory horizon — how many tokens it can "hold" before losing grounding.

---

## Proposed Metrics

1. **bundle_score** = μ_fibers × (1 - σ_fiber) ∈ [0, 1]
   → replaces σ_fiber as the primary quality signal for short outputs

2. **dσ/dt** (trajectory slope) ∈ (-∞, +∞)
   → primary signal for long-form outputs; sign encodes quality direction

3. **integration_score** = -dσ/dt (positive = converging)
   → natural complement to σ_fiber; measures whether the output "integrated"

4. **trajectory_variance** = var(σ(t))
   → detects the oscillating pattern; high variance = switching between modes

---

## Open Questions

1. **Minimum passage length:** Trajectory measurement requires ≥4 sentences. For short
   outputs, only bundle_score is available. What's the crossover point?

2. **Window size sensitivity:** Does dσ/dt depend heavily on window size? A 2-sentence
   window will give noisier trajectories than a 4-sentence window. Calibration needed.

3. **The "converging confabulation":** Can a confabulated passage show a converging
   trajectory? Yes — if the model converges around wrong facts consistently. The
   trajectory would show low dσ/dt (converging) but also low bundle_score (wrong facts).
   This means trajectory + bundle together are needed; neither alone is sufficient.

---

*BC3 Session 6 riff | 2026-03-12*
*"We were measuring the spread. We forgot to measure the gathering."*
