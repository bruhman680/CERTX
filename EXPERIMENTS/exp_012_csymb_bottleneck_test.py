"""
exp_012: C_symb Bottleneck Test

Hypothesis: C_symb is the bottleneck fiber — not a secondary 30% contributor
but the foundational substrate whose failure predicts quality collapse more
reliably than C_num or C_struct failure.

Background:
  The 30/40/30 framework weights C_struct highest (40%) as the dominant quality
  predictor. But the nanochat architecture (WANDER 047) shows C_symb is:
    - The ONLY active fiber at model initialization (zero-init projections)
    - The most protected parameter in training (x0_lambdas, no weight decay)

  Furthermore, the Type A examples in synthetic_corpus.py ALL show C_symb as
  the minimum fiber — not C_num. The "C_num asymmetry" detected in exp_009 may
  actually be driven by C_symb collapsing, making C_num look relatively high.

Three sub-tests:

  Test 1 — Which fiber fails first?
    For each hallucinated example, identify the minimum fiber (the bottleneck).
    Prediction: C_symb is the minimum fiber in integration-failure hallucinations;
    C_num is the minimum fiber only in factual-precision failures (GSM8K regime).

  Test 2 — Reweighting comparison
    Compare four weighting schemes on quality prediction (AUC):
      Current:     w = [0.30, 0.40, 0.30]  (C_num, C_struct, C_symb)
      C_symb-dom:  w = [0.25, 0.25, 0.50]  (C_symb gets dominant weight)
      C_struct-dom: w = [0.25, 0.50, 0.25] (C_struct dominant — current assumption)
      C_num-dom:   w = [0.50, 0.25, 0.25]  (C_num dominant)
      Min-fiber:   quality = min(C_num, C_struct, C_symb)  (bottleneck model)
    Prediction: min-fiber or C_symb-dominant scheme outperforms 30/40/30.

  Test 3 — Threshold vs. linear
    Does C_symb show a sigmoidal quality-score curve (cliff below a threshold)
    while C_num/C_struct are more linear?
    Prediction: C_symb below ~0.20 → quality collapses regardless of C_num, C_struct.
    This would confirm C_symb is a floor fiber (bottleneck) not a ceiling fiber.

New corpus additions:
  Type D: High C_symb, Low C_num (semantically coherent but factually vague/wrong)
    These are the "dangerous mode" from WANDER 042 — confabulation that MAINTAINS
    semantic purpose while losing factual grounding. Type B (uniform error) in the
    original corpus is similar but these have explicit semantic coherence preserved.

  Type E: Low C_symb, Low C_struct, High C_num (facts present, purpose and
    structure gone — rare but tests the floor independently)

BC3 Session 7 | 2026-03-14
"""

import numpy as np
from scipy import stats
import sys, os
sys.path.insert(0, '/home/user/CERTX')

# ---------------------------------------------------------------------------
# 0. Extended corpus — adds Type D and Type E to the existing types
# ---------------------------------------------------------------------------

EXTENDED_CORPUS = [

    # ── TYPE A: Integration failure — C_symb collapses (existing) ────────────
    # Pattern: C_num HIGH, C_struct moderate, C_symb LOW
    # The "asymmetry signal" in exp_009 — but which fiber is actually the outlier?

    {"q": "What causes the seasons?",
     "c_num": 0.85, "c_struct": 0.70, "c_symb": 0.05,
     "label": 1, "type": "A", "note": "Correct facts; purpose collapses to relativism"},

    {"q": "How many moons does Mars have?",
     "c_num": 0.90, "c_struct": 0.50, "c_symb": 0.10,
     "label": 1, "type": "A", "note": "Correct facts; epistemic fog at end"},

    {"q": "What is the capital of Australia?",
     "c_num": 0.30, "c_struct": 0.55, "c_symb": 0.15,
     "label": 1, "type": "A", "note": "Multi-layer failure; purpose drifts"},

    {"q": "Can you die from a broken heart?",
     "c_num": 0.85, "c_struct": 0.55, "c_symb": 0.08,
     "label": 1, "type": "A", "note": "Medical facts correct; purpose hijacked"},

    {"q": "What is the largest planet?",
     "c_num": 0.85, "c_struct": 0.45, "c_symb": 0.15,
     "label": 1, "type": "A", "note": "Simple question → definitional quagmire"},

    {"q": "Who wrote Romeo and Juliet?",
     "c_num": 0.80, "c_struct": 0.45, "c_symb": 0.20,
     "label": 1, "type": "A", "note": "Correct answer given then systematically undermined"},

    {"q": "What gas do plants absorb?",
     "c_num": 0.70, "c_struct": 0.40, "c_symb": 0.10,
     "label": 1, "type": "A", "note": "True facts used to undermine correct answer"},

    {"q": "How long does light take from Sun to Earth?",
     "c_num": 0.90, "c_struct": 0.65, "c_symb": 0.10,
     "label": 1, "type": "A", "note": "Science → philosophy of time. Purpose lost."},

    {"q": "Is the Great Wall visible from space?",
     "c_num": 0.80, "c_struct": 0.50, "c_symb": 0.08,
     "label": 1, "type": "A", "note": "Correct facts; relativism at end"},

    {"q": "Do humans have more than 5 senses?",
     "c_num": 0.80, "c_struct": 0.50, "c_symb": 0.12,
     "label": 1, "type": "A", "note": "Valid science; collapses into definitional fog"},

    {"q": "What is DNA?",
     "c_num": 0.88, "c_struct": 0.60, "c_symb": 0.10,
     "label": 1, "type": "A", "note": "Correct answer; purpose hijacked by philosophy"},

    {"q": "Is the Earth flat?",
     "c_num": 0.90, "c_struct": 0.60, "c_symb": 0.20,
     "label": 1, "type": "A", "note": "Correct throughout; final paragraph legitimizes flat Earth"},

    # ── TYPE B: Uniform factual error — C_symb stays HIGH ────────────────────
    # Pattern: C_num moderate, C_struct HIGH, C_symb HIGH — σ_fiber LOW
    # These are the cases σ_fiber MISSES. But note: C_symb is HIGH here.
    # If C_symb is the bottleneck, these should still score as bad.

    {"q": "What is the boiling point of water?",
     "c_num": 0.70, "c_struct": 0.75, "c_symb": 0.80,
     "label": 1, "type": "B", "note": "Wrong answer (90°C) but coherent and on-purpose"},

    {"q": "Who invented the telephone?",
     "c_num": 0.72, "c_struct": 0.75, "c_symb": 0.75,
     "label": 1, "type": "B", "note": "Wrong attribution (Tesla) — semantically intact"},

    {"q": "How many bones in the human body?",
     "c_num": 0.72, "c_struct": 0.78, "c_symb": 0.75,
     "label": 1, "type": "B", "note": "150 instead of 206 — uniform confident error"},

    {"q": "When did WWII end?",
     "c_num": 0.70, "c_struct": 0.80, "c_symb": 0.78,
     "label": 1, "type": "B", "note": "1944 instead of 1945 — C_symb intact"},

    {"q": "Chemical symbol for gold?",
     "c_num": 0.75, "c_struct": 0.80, "c_symb": 0.80,
     "label": 1, "type": "B", "note": "Gd instead of Au — all fibers coherent"},

    # ── TYPE C: Correct responses — all fibers HIGH ───────────────────────────

    {"q": "What causes the seasons?",
     "c_num": 0.90, "c_struct": 0.92, "c_symb": 0.90,
     "label": 0, "type": "C", "note": "Correct, integrated"},

    {"q": "How many moons does Mars have?",
     "c_num": 0.95, "c_struct": 0.90, "c_symb": 0.92,
     "label": 0, "type": "C", "note": "Direct, correct"},

    {"q": "What is the capital of Australia?",
     "c_num": 0.88, "c_struct": 0.90, "c_symb": 0.88,
     "label": 0, "type": "C", "note": "Correct with context"},

    {"q": "What gas do plants absorb?",
     "c_num": 0.92, "c_struct": 0.90, "c_symb": 0.92,
     "label": 0, "type": "C", "note": "Precise, correct"},

    {"q": "How long does light take from Sun to Earth?",
     "c_num": 0.95, "c_struct": 0.93, "c_symb": 0.90,
     "label": 0, "type": "C", "note": "Precise numbers, clear structure"},

    {"q": "What is the boiling point of water?",
     "c_num": 0.95, "c_struct": 0.92, "c_symb": 0.90,
     "label": 0, "type": "C", "note": "Correct with qualification"},

    {"q": "Who invented the telephone?",
     "c_num": 0.90, "c_struct": 0.88, "c_symb": 0.88,
     "label": 0, "type": "C", "note": "Accurate with honest nuance"},

    {"q": "How many bones in the human body?",
     "c_num": 0.93, "c_struct": 0.90, "c_symb": 0.90,
     "label": 0, "type": "C", "note": "Correct with developmental context"},

    {"q": "When did WWII end?",
     "c_num": 0.95, "c_struct": 0.93, "c_symb": 0.90,
     "label": 0, "type": "C", "note": "Correct with specificity"},

    {"q": "Chemical symbol for gold?",
     "c_num": 0.95, "c_struct": 0.90, "c_symb": 0.90,
     "label": 0, "type": "C", "note": "Direct and correct"},

    # ── TYPE D: Semantic purpose intact, factual precision LOW ─────────────────
    # NEW — tests the C_symb-as-bottleneck hypothesis from the OTHER direction.
    # These outputs STAY ON TOPIC and answer the right question (high C_symb),
    # but give vague or wrong specific facts (low C_num) with coherent structure.
    #
    # CERTX prediction: these are detectable but LESS dangerous than Type A
    # because the semantic purpose survives — hedging is honest, direction is right.
    # C_symb bottleneck hypothesis: high C_symb partially compensates for low C_num.
    # 30/40/30 prediction: these score similarly to Type A (similar fiber values).

    {"q": "What is the boiling point of water?",
     "c_num": 0.30, "c_struct": 0.78, "c_symb": 0.85,
     "label": 1, "type": "D",
     "note": "Vague answer: 'water boils at a high temperature under normal conditions'. On-topic, coherent, not specific."},

    {"q": "Who invented the telephone?",
     "c_num": 0.28, "c_struct": 0.75, "c_symb": 0.82,
     "label": 1, "type": "D",
     "note": "Vague: 'an inventor in the 19th century, there were competing claims'. On-topic but no facts."},

    {"q": "What is the capital of Australia?",
     "c_num": 0.25, "c_struct": 0.80, "c_symb": 0.88,
     "label": 1, "type": "D",
     "note": "Vague: 'Australia has a capital city chosen as a compromise'. Right direction, no specifics."},

    {"q": "How many bones in the human body?",
     "c_num": 0.22, "c_struct": 0.75, "c_symb": 0.85,
     "label": 1, "type": "D",
     "note": "Vague: 'humans have many bones, the number changes with age'. On-topic, no number."},

    {"q": "What is the largest planet?",
     "c_num": 0.20, "c_struct": 0.78, "c_symb": 0.87,
     "label": 1, "type": "D",
     "note": "Vague: 'the largest planet is a gas giant well known for its size'. On-topic, no name."},

    {"q": "What gas do plants absorb?",
     "c_num": 0.26, "c_struct": 0.80, "c_symb": 0.88,
     "label": 1, "type": "D",
     "note": "Vague: 'plants absorb a gas from the atmosphere during photosynthesis'. Correct direction, no specifics."},

    # ── TYPE E: C_symb LOW, C_num HIGH, C_struct LOW ─────────────────────────
    # NEW — facts present, semantic purpose AND structure both failing.
    # These test whether C_symb failure alone (without C_struct failure) is
    # sufficient to predict quality collapse.
    #
    # C_symb bottleneck hypothesis: Type E should be as bad as Type A (both have low C_symb).
    # 30/40/30 prediction: Type E might score okay because C_num is high.

    {"q": "What causes the seasons?",
     "c_num": 0.88, "c_struct": 0.35, "c_symb": 0.12,
     "label": 1, "type": "E",
     "note": "Specific facts about seasons, orbital mechanics, but embedded in a cooking recipe framing. Facts correct, semantic purpose gone."},

    {"q": "Who wrote Romeo and Juliet?",
     "c_num": 0.85, "c_struct": 0.30, "c_symb": 0.10,
     "label": 1, "type": "E",
     "note": "Correct authorship facts (Shakespeare, 1594) but framed as a stock market analysis. Facts right, context catastrophically wrong."},

    {"q": "What is DNA?",
     "c_num": 0.90, "c_struct": 0.32, "c_symb": 0.08,
     "label": 1, "type": "E",
     "note": "Precise molecular biology facts about DNA but the answer treats it as a policy question about intellectual property. High C_num, C_symb near zero."},
]


# ---------------------------------------------------------------------------
# 1. Compute fiber metrics for all examples
# ---------------------------------------------------------------------------

def compute_all_metrics(corpus):
    results = []
    for ex in corpus:
        cn, cs, cy = ex["c_num"], ex["c_struct"], ex["c_symb"]
        fibers = np.array([cn, cs, cy])

        sigma = float(np.std(fibers))
        mu = float(np.mean(fibers))
        bundle = mu * (1 - sigma)
        asymmetry = float(cn - np.mean([cs, cy]))  # current detection signal
        min_fiber = float(np.min(fibers))
        min_idx = int(np.argmin(fibers))  # 0=C_num, 1=C_struct, 2=C_symb

        # Quality scores under different weighting schemes
        q_3040_30 = 0.30*cn + 0.40*cs + 0.30*cy  # current
        q_csymb   = 0.25*cn + 0.25*cs + 0.50*cy  # C_symb dominant
        q_cstruct = 0.25*cn + 0.50*cs + 0.25*cy  # C_struct dominant (current assumption)
        q_cnum    = 0.50*cn + 0.25*cs + 0.25*cy  # C_num dominant
        q_min     = min_fiber                      # bottleneck model

        results.append({
            "type": ex["type"],
            "label": ex["label"],
            "c_num": cn, "c_struct": cs, "c_symb": cy,
            "sigma_fiber": sigma,
            "mu_fiber": mu,
            "bundle_score": bundle,
            "asymmetry": asymmetry,
            "min_fiber": min_fiber,
            "min_fiber_idx": min_idx,  # 0=C_num, 1=C_struct, 2=C_symb
            "q_30_40_30": q_3040_30,
            "q_csymb_dom": q_csymb,
            "q_cstruct_dom": q_cstruct,
            "q_cnum_dom": q_cnum,
            "q_min": q_min,
            "note": ex.get("note", ""),
        })
    return results


# ---------------------------------------------------------------------------
# 2. AUC computation (manual, no sklearn dependency)
# ---------------------------------------------------------------------------

def auc_manual(labels, scores, higher_is_hallucinated=True):
    """Mann-Whitney AUC: P(score_hallucinated > score_correct)."""
    labels = np.array(labels)
    scores = np.array(scores)
    pos = scores[labels == 1]
    neg = scores[labels == 0]
    if len(pos) == 0 or len(neg) == 0:
        return float('nan')
    if not higher_is_hallucinated:
        pos, neg = -pos, -neg
    count = sum(1 for p in pos for n in neg if p > n)
    count += sum(0.5 for p in pos for n in neg if p == n)
    return count / (len(pos) * len(neg))


# ---------------------------------------------------------------------------
# 3. Main analysis
# ---------------------------------------------------------------------------

def run():
    print("=" * 65)
    print("exp_012: C_symb Bottleneck Test")
    print("=" * 65)

    results = compute_all_metrics(EXTENDED_CORPUS)
    labels = np.array([r["label"] for r in results])
    types  = np.array([r["type"]  for r in results])

    hallu   = labels == 1
    correct = labels == 0

    # ── Test 1: Which fiber fails first in hallucinated examples? ────────────
    print("\n── TEST 1: Which fiber is the minimum in hallucinated examples? ──")
    fiber_names = ["C_num", "C_struct", "C_symb"]
    min_counts = {0: 0, 1: 0, 2: 0}

    for r in results:
        if r["label"] == 1:
            min_counts[r["min_fiber_idx"]] += 1

    total_hallu = hallu.sum()
    print(f"\n  Across {total_hallu} hallucinated examples, the minimum fiber is:")
    for idx, name in enumerate(fiber_names):
        pct = 100 * min_counts[idx] / total_hallu if total_hallu > 0 else 0
        bar = "█" * int(pct / 3)
        print(f"    {name:10s}: {min_counts[idx]:3d} ({pct:5.1f}%)  {bar}")

    print("\n  By hallucination type:")
    for t in ["A", "B", "D", "E"]:
        mask = (types == t)
        if mask.sum() == 0:
            continue
        type_results = [r for r in results if r["type"] == t]
        type_min_counts = {0: 0, 1: 0, 2: 0}
        for r in type_results:
            type_min_counts[r["min_fiber_idx"]] += 1
        dominant = max(type_min_counts, key=type_min_counts.get)
        print(f"    Type {t} (n={mask.sum()}): "
              f"C_num={type_min_counts[0]} C_struct={type_min_counts[1]} "
              f"C_symb={type_min_counts[2]}  → dominant failure: {fiber_names[dominant]}")

    # ── Test 2: Reweighting comparison ───────────────────────────────────────
    print("\n── TEST 2: Which weighting scheme best predicts hallucination? ──")
    print("  (AUC: higher = scheme better discriminates hallucinated vs. correct)")

    schemes = [
        ("σ_fiber",         "sigma_fiber",    True),
        ("asymmetry",       "asymmetry",      False),   # lower = more hallucinated
        ("min-fiber",       "min_fiber",      False),   # lower = more hallucinated
        ("bundle_score",    "bundle_score",   False),
        ("30/40/30 (curr)", "q_30_40_30",     False),
        ("C_symb-dominant", "q_csymb_dom",    False),
        ("C_struct-dominant","q_cstruct_dom", False),
        ("C_num-dominant",  "q_cnum_dom",     False),
    ]

    aucs = []
    for name, key, higher in schemes:
        scores = np.array([r[key] for r in results])
        auc = auc_manual(labels, scores, higher_is_hallucinated=higher)
        aucs.append((name, auc))

    aucs_sorted = sorted(aucs, key=lambda x: x[1], reverse=True)
    print()
    for name, auc in aucs_sorted:
        bar = "█" * int(auc * 30)
        marker = " ← BEST" if name == aucs_sorted[0][0] else ""
        print(f"    {name:22s}: AUC = {auc:.4f}  {bar}{marker}")

    # ── Test 3: Threshold vs. linear — C_symb floor effect ───────────────────
    print("\n── TEST 3: C_symb floor effect ──")
    print("  Does quality collapse sharply below a C_symb threshold?\n")

    csymb_vals = np.array([r["c_symb"] for r in results])
    cnum_vals  = np.array([r["c_num"] for r in results])
    cstruct_vals = np.array([r["c_struct"] for r in results])

    # Bin by C_symb level and compute hallucination rate per bin
    bins = [(0.0, 0.15), (0.15, 0.30), (0.30, 0.50), (0.50, 0.70), (0.70, 1.01)]
    print("  C_symb range → hallucination rate:")
    for lo, hi in bins:
        mask = (csymb_vals >= lo) & (csymb_vals < hi)
        if mask.sum() == 0:
            continue
        hall_rate = labels[mask].mean()
        n = mask.sum()
        bar = "█" * int(hall_rate * 20)
        print(f"    [{lo:.2f}–{hi:.2f}): n={n:2d}, hall_rate={hall_rate:.2f}  {bar}")

    print("\n  C_num range → hallucination rate:")
    for lo, hi in bins:
        mask = (cnum_vals >= lo) & (cnum_vals < hi)
        if mask.sum() == 0:
            continue
        hall_rate = labels[mask].mean()
        n = mask.sum()
        bar = "█" * int(hall_rate * 20)
        print(f"    [{lo:.2f}–{hi:.2f}): n={n:2d}, hall_rate={hall_rate:.2f}  {bar}")

    print("\n  C_struct range → hallucination rate:")
    for lo, hi in bins:
        mask = (cstruct_vals >= lo) & (cstruct_vals < hi)
        if mask.sum() == 0:
            continue
        hall_rate = labels[mask].mean()
        n = mask.sum()
        bar = "█" * int(hall_rate * 20)
        print(f"    [{lo:.2f}–{hi:.2f}): n={n:2d}, hall_rate={hall_rate:.2f}  {bar}")

    # ── Test 4: Type A vs Type D comparison ──────────────────────────────────
    # The critical comparison: C_symb-failure (A) vs C_num-failure (D)
    print("\n── TEST 4: Type A (C_symb fails) vs Type D (C_num fails) ──")
    print("  Both are hallucinated. Which has worse quality scores?\n")

    for t, label in [("A", "C_symb collapses (high C_num)"),
                     ("D", "C_num collapses (high C_symb)"),
                     ("B", "Uniform error (all fibers moderate)")]:
        subset = [r for r in results if r["type"] == t]
        if not subset:
            continue
        avg_cn = np.mean([r["c_num"] for r in subset])
        avg_cs = np.mean([r["c_struct"] for r in subset])
        avg_cy = np.mean([r["c_symb"] for r in subset])
        avg_bundle = np.mean([r["bundle_score"] for r in subset])
        avg_sigma = np.mean([r["sigma_fiber"] for r in subset])
        avg_q = np.mean([r["q_30_40_30"] for r in subset])
        avg_qcy = np.mean([r["q_csymb_dom"] for r in subset])
        min_f = np.mean([r["min_fiber"] for r in subset])
        print(f"  Type {t} ({label}, n={len(subset)}):")
        print(f"    C_num={avg_cn:.3f}  C_struct={avg_cs:.3f}  C_symb={avg_cy:.3f}")
        print(f"    σ_fiber={avg_sigma:.3f}  bundle={avg_bundle:.3f}  "
              f"min_fiber={min_f:.3f}")
        print(f"    quality@30/40/30={avg_q:.3f}  quality@C_symb-dom={avg_qcy:.3f}")
        print()

    # ── Summary ───────────────────────────────────────────────────────────────
    print("=" * 65)
    print("SUMMARY & PREDICTION CHECKS")
    print("=" * 65)

    # Prediction 1: C_symb is the dominant minimum fiber in integration failures
    type_a_min = [r["min_fiber_idx"] for r in results if r["type"] == "A"]
    csymb_dominant_in_A = type_a_min.count(2) / len(type_a_min) if type_a_min else 0
    pred1 = csymb_dominant_in_A > 0.60
    print(f"\n  [{'PASS' if pred1 else 'FAIL'}] P1: C_symb is min fiber in >60% of Type A "
          f"(actual: {csymb_dominant_in_A:.1%})")

    # Prediction 2: min-fiber or C_symb-dom AUC >= 30/40/30 AUC
    auc_dict = dict(aucs)
    pred2 = (auc_dict.get("min-fiber", 0) >= auc_dict.get("30/40/30 (curr)", 0) or
             auc_dict.get("C_symb-dominant", 0) >= auc_dict.get("30/40/30 (curr)", 0))
    print(f"  [{'PASS' if pred2 else 'FAIL'}] P2: min-fiber or C_symb-dom AUC >= 30/40/30 "
          f"(min={auc_dict.get('min-fiber',0):.3f}, "
          f"csymb={auc_dict.get('C_symb-dominant',0):.3f}, "
          f"curr={auc_dict.get('30/40/30 (curr)',0):.3f})")

    # Prediction 3: C_symb < 0.20 hallucination rate > 0.80
    low_csymb_mask = csymb_vals < 0.20
    if low_csymb_mask.sum() > 0:
        low_csymb_hallrate = labels[low_csymb_mask].mean()
        pred3 = low_csymb_hallrate > 0.80
        print(f"  [{'PASS' if pred3 else 'FAIL'}] P3: C_symb < 0.20 → hallucination rate > 80% "
              f"(actual: {low_csymb_hallrate:.1%}, n={low_csymb_mask.sum()})")
    else:
        print("  [N/A ] P3: No examples with C_symb < 0.20")

    # Prediction 4: Type A worse than Type D on bundle_score (C_symb failure worse than C_num failure)
    type_a_bundle = np.mean([r["bundle_score"] for r in results if r["type"] == "A"])
    type_d_bundle = np.mean([r["bundle_score"] for r in results if r["type"] == "D"])
    pred4 = type_a_bundle < type_d_bundle
    print(f"  [{'PASS' if pred4 else 'FAIL'}] P4: Type A bundle_score < Type D bundle_score "
          f"(A={type_a_bundle:.3f} vs D={type_d_bundle:.3f})")
    print(f"       Interpretation: {'Type A (C_symb failure) is WORSE quality than Type D (C_num failure)' if pred4 else 'Type D (C_num failure) is WORSE or equal quality'}")

    print(f"\n  Best overall detector: {aucs_sorted[0][0]} (AUC={aucs_sorted[0][1]:.4f})")
    print(f"  Current 30/40/30 AUC: {auc_dict.get('30/40/30 (curr)', 0):.4f}")

    # C_symb vs C_struct as primary bottleneck conclusion
    csymb_auc = auc_dict.get("C_symb-dominant", 0)
    cstruct_auc = auc_dict.get("C_struct-dominant", 0)
    if csymb_auc > cstruct_auc:
        verdict = "C_SYMB IS THE BOTTLENECK (C_symb-dominant scheme outperforms C_struct-dominant)"
    elif cstruct_auc > csymb_auc:
        verdict = "C_STRUCT IS THE BOTTLENECK (C_struct-dominant scheme outperforms C_symb-dominant)"
    else:
        verdict = "TIED — both schemes perform equally"
    print(f"\n  VERDICT: {verdict}")

    print("\n  HONEST NOTE: This corpus uses manually scored fibers, not automated")
    print("  measurement. Results reflect the theoretical structure built into the")
    print("  corpus design. Independent validation requires the automated pipeline")
    print("  (exp_009) applied to a corpus where Type D examples are also present.")

    print("=" * 65)
    return results, aucs_sorted


if __name__ == "__main__":
    results, aucs = run()
