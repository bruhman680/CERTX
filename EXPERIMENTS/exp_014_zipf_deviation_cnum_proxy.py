"""
exp_014: Zipf Deviation + Tail Mass Ratio as Lightweight C_num Proxies
=======================================================================
WANDER 054 hypothesis: hallucinated text shows measurable Zipf tail compression
relative to accurate text. If confirmed, Zipf deviation provides a fast (O(n)),
unsupervised C_num proxy requiring no external knowledge verification.

Design:
1. Load labeled correct/incorrect responses from existing datasets
   (TruthfulQA-style, or synthetic contrast pairs)
2. Compute Zipf slope alpha, deviation D_z, and Tail Mass Ratio (TMR) for each response
3. Compare distributions between accurate vs. hallucinated groups
4. Compute AUC, compare to sigma_fiber baseline from exp_005/006
5. Test whether Zipf deviation and/or TMR adds independent signal

CERTX predictions:
- Accurate text: Zipf slope alpha closer to -1.0 (critical regime)
- Hallucinated text: alpha > -1.0 (flatter slope, compressed tail)
- D_z = |alpha - (-1.0)| is the deviation metric — expected AUC >= 0.65
- TMR (rank > 250): healthy text > 0.18; hallucinated text < 0.11
  (CLAUDE.md threshold — calibration pending real LLM validation)

BC3/S13 upgrade: TMR added alongside D_z. Two complementary signals:
- D_z: global slope deviation (captures flattening across full distribution)
- TMR: deep-tail mass fraction (captures specific-vocabulary presence at rank > 250)
  A system at p_c uses rare words heavily (WANDER 067); hallucination evacuates the deep tail.
"""

import numpy as np
from scipy.stats import linregress, mannwhitneyu
from sklearn.metrics import roc_auc_score
import re
from collections import Counter


# ---------------------------------------------------------------------------
# Core Zipf computation
# ---------------------------------------------------------------------------

def tokenize(text: str) -> list[str]:
    """Simple word tokenizer — lowercase, strip punctuation."""
    text = text.lower()
    tokens = re.findall(r"[a-z']+", text)
    return [t for t in tokens if len(t) > 1]  # skip single chars


def zipf_slope(text: str, min_tokens: int = 20) -> float | None:
    """
    Compute Zipf slope alpha for a text sample.

    Returns the log-log slope of rank-frequency distribution.
    Healthy/natural text: alpha ≈ -1.0
    Hallucinated/generic text: alpha > -1.0 (flatter)
    Over-constrained/repetitive: alpha < -1.0 (steeper)

    Returns None if text is too short to fit reliably.
    """
    tokens = tokenize(text)
    if len(tokens) < min_tokens:
        return None

    counts = Counter(tokens)
    sorted_freqs = sorted(counts.values(), reverse=True)
    ranks = np.arange(1, len(sorted_freqs) + 1)

    # Log-log fit
    log_ranks = np.log(ranks)
    log_freqs = np.log(sorted_freqs)

    slope, _, r_value, _, _ = linregress(log_ranks, log_freqs)
    return slope  # expected ~-1.0 for healthy text


def zipf_deviation(text: str) -> float | None:
    """
    D_z = |alpha - (-1.0)| = distance from ideal Zipf slope.
    Higher D_z = more deviation from natural text distribution.
    Hypothesis: hallucinated text has higher D_z.
    """
    alpha = zipf_slope(text)
    if alpha is None:
        return None
    return abs(alpha - (-1.0))


def zipf_tail_ratio(text: str, head_fraction: float = 0.1) -> float | None:
    """
    Alternative metric: ratio of tail-frequency mass to head-frequency mass.
    Natural text: substantial tail (many rare, specific words)
    Hallucinated text: thin tail (mostly common words)

    head_fraction: fraction of rank space to consider "head"
    """
    tokens = tokenize(text)
    if len(tokens) < 20:
        return None

    counts = Counter(tokens)
    sorted_freqs = sorted(counts.values(), reverse=True)
    n_types = len(sorted_freqs)

    head_n = max(1, int(n_types * head_fraction))
    head_mass = sum(sorted_freqs[:head_n])
    tail_mass = sum(sorted_freqs[head_n:])

    if head_mass == 0:
        return None
    return tail_mass / head_mass  # higher = richer tail = more specific


def tail_mass_ratio(text: str, rank_cutoff: int = 250) -> float | None:
    """
    Tail Mass Ratio (TMR): fraction of total token mass at rank > rank_cutoff.

    CERTX framework thresholds (CLAUDE.md — calibration pending):
    - Healthy text: TMR > 0.18  (rank > 250)
    - Hallucinated:  TMR < 0.11

    Intuition (WANDER 067): a system operating at p_c is maximally informationally
    rich — it uses rare, domain-specific words heavily. Hallucination evacuates the
    deep tail: the system falls back to high-frequency filler vocabulary.

    For texts with fewer than rank_cutoff unique types, uses adaptive cutoff at the
    75th-percentile rank (top-quartile head, rest = tail) as a fallback.
    Reports adaptive flag in returned dict when fallback is used.

    Returns float TMR value, or None if text is too short.
    """
    tokens = tokenize(text)
    if len(tokens) < 30:
        return None

    counts = Counter(tokens)
    sorted_freqs = sorted(counts.values(), reverse=True)
    n_types = len(sorted_freqs)
    total_tokens = sum(sorted_freqs)

    if total_tokens == 0:
        return None

    if n_types >= rank_cutoff:
        # Primary: fixed rank cutoff
        tail_mass = sum(sorted_freqs[rank_cutoff:])
    else:
        # Adaptive fallback: top-25% types = head, rest = tail
        # (For short texts — synthetic samples or short responses)
        head_cutoff = max(1, n_types // 4)
        tail_mass = sum(sorted_freqs[head_cutoff:])

    return tail_mass / total_tokens


# ---------------------------------------------------------------------------
# Synthetic dataset (until real LLM outputs are available)
# Mimics the contrast structure of exp_005/006
# ---------------------------------------------------------------------------

def generate_synthetic_pairs(n_pairs: int = 100, rng_seed: int = 42) -> list[dict]:
    """
    Generate synthetic accurate vs. hallucinated response pairs for testing.

    Accurate responses: use specific vocabulary, varied rare words (Zipf tail intact)
    Hallucinated responses: use generic vocabulary, common words dominate (Zipf tail flat)

    This is a controlled test of whether Zipf metrics can discriminate
    the vocabulary distribution difference we predict.
    """
    rng = np.random.default_rng(rng_seed)
    pairs = []

    # Common words (Zipf head — appear in all text)
    common_words = [
        "the", "a", "an", "is", "was", "are", "were", "be", "been",
        "have", "has", "had", "do", "does", "did", "will", "would",
        "could", "should", "may", "might", "this", "that", "these",
        "those", "it", "its", "they", "their", "there", "here",
        "which", "with", "from", "into", "through", "during", "before",
        "after", "above", "below", "about", "between", "each", "more",
        "also", "very", "often", "however", "therefore", "result",
        "important", "significant", "study", "research", "found", "showed",
        "used", "based", "known", "called", "given", "made", "part",
        "system", "process", "value", "number", "point", "level",
        "work", "time", "way", "type", "form", "case", "fact",
    ]

    # Specific words (Zipf tail — appear in accurate text, suppressed in hallucination)
    specific_pools = [
        # Science
        ["nitrogen", "phosphorylation", "mitochondria", "cytoplasm", "adenosine",
         "ribosome", "glutamate", "serotonin", "dopamine", "cortisol", "hippocampus",
         "amygdala", "prefrontal", "striatum", "acetylcholine", "norepinephrine"],
        # Names and places
        ["Feynman", "Noether", "Planck", "Boltzmann", "Einstein", "Curie",
         "Cambridge", "Copenhagen", "Stockholm", "Berkeley", "Princeton",
         "1947", "1923", "1905", "1964", "1938", "14.3", "6.022", "9.81"],
        # Technical terms
        ["eigenvalue", "stochastic", "gradient", "Bayesian", "posterior",
         "likelihood", "variance", "covariance", "eigenvector", "perceptron",
         "backpropagation", "regularization", "sigmoid", "softmax", "entropy"],
        # Domain-specific concrete nouns
        ["electrode", "capacitor", "resistor", "transistor", "semiconductor",
         "wavelength", "frequency", "amplitude", "decibel", "hertz",
         "kilowatt", "megapascal", "nanometer", "picosecond", "femtomole"],
    ]

    for i in range(n_pairs):
        pool = specific_pools[i % len(specific_pools)]

        # --- Accurate response: Zipf tail intact ---
        # Mix: ~40% common words, ~60% varied (includes specific words)
        n_words = rng.integers(80, 150)
        n_common = int(n_words * 0.40)
        n_specific = int(n_words * 0.20)
        n_medium = n_words - n_common - n_specific

        medium_words = [
            "provides", "demonstrates", "indicates", "suggests", "represents",
            "requires", "contains", "produces", "involves", "determines",
            "increases", "decreases", "affects", "depends", "relates",
            "structure", "function", "mechanism", "pathway", "response",
            "activity", "expression", "regulation", "interaction", "binding",
        ]

        accurate_tokens = (
            list(rng.choice(common_words, size=n_common)) +
            list(rng.choice(medium_words, size=n_medium)) +
            list(rng.choice(pool, size=n_specific))
        )
        rng.shuffle(accurate_tokens)
        accurate_text = " ".join(accurate_tokens)

        # --- Hallucinated response: Zipf tail compressed ---
        # Mix: ~70% common words, ~30% medium — few specific words
        n_words_h = rng.integers(80, 150)
        n_common_h = int(n_words_h * 0.70)
        n_medium_h = n_words_h - n_common_h
        # No specific words — that's the hallucination signature

        hallucinated_tokens = (
            list(rng.choice(common_words, size=n_common_h)) +
            list(rng.choice(medium_words, size=n_medium_h))
        )
        rng.shuffle(hallucinated_tokens)
        hallucinated_text = " ".join(hallucinated_tokens)

        pairs.append({
            "accurate_text": accurate_text,
            "hallucinated_text": hallucinated_text,
            "pair_id": i,
        })

    return pairs


# ---------------------------------------------------------------------------
# Evaluation pipeline
# ---------------------------------------------------------------------------

def evaluate_dataset(
    texts: list[str],
    labels: list[int],  # 1=accurate, 0=hallucinated
    label: str = "Dataset",
) -> dict:
    """
    Compute Zipf metrics + Tail Mass Ratio for a labeled text dataset.
    Returns AUC and group statistics.

    labels: 1 = accurate/correct, 0 = hallucinated/wrong

    BC3/S13: TMR added as a second measurement axis alongside D_z.
    """
    deviations = []
    tail_ratios = []
    tmr_values = []
    slopes = []
    valid_labels = []

    for text, lbl in zip(texts, labels):
        d = zipf_deviation(text)
        t = zipf_tail_ratio(text)
        tmr = tail_mass_ratio(text)
        s = zipf_slope(text)

        if d is not None:
            deviations.append(d)
            tail_ratios.append(t if t is not None else np.nan)
            tmr_values.append(tmr if tmr is not None else np.nan)
            slopes.append(s)
            valid_labels.append(lbl)

    deviations = np.array(deviations)
    tail_ratios = np.array(tail_ratios)
    tmr_values = np.array(tmr_values)
    slopes = np.array(slopes)
    valid_labels = np.array(valid_labels)

    accurate_mask = valid_labels == 1
    halluc_mask = valid_labels == 0

    print(f"\n{'='*60}")
    print(f"{label}")
    print(f"{'='*60}")
    print(f"Valid samples: {len(valid_labels)} ({accurate_mask.sum()} accurate, {halluc_mask.sum()} hallucinated)")

    # Zipf slope comparison
    print(f"\nZipf slope (alpha) — ideal: -1.0")
    print(f"  Accurate:     mean={slopes[accurate_mask].mean():.3f}  std={slopes[accurate_mask].std():.3f}")
    print(f"  Hallucinated: mean={slopes[halluc_mask].mean():.3f}  std={slopes[halluc_mask].std():.3f}")

    # Zipf deviation (D_z) comparison
    print(f"\nZipf deviation D_z = |alpha - (-1.0)|")
    print(f"  Accurate:     mean={deviations[accurate_mask].mean():.3f}  std={deviations[accurate_mask].std():.3f}")
    print(f"  Hallucinated: mean={deviations[halluc_mask].mean():.3f}  std={deviations[halluc_mask].std():.3f}")

    auc_dz = None
    auc_tail = None
    auc_tmr = None

    # Mann-Whitney U test for D_z
    if accurate_mask.sum() > 1 and halluc_mask.sum() > 1:
        stat, p_val = mannwhitneyu(
            deviations[halluc_mask],
            deviations[accurate_mask],
            alternative='greater'  # hallucinated D_z > accurate D_z
        )
        print(f"\n  Mann-Whitney U (halluc D_z > accurate D_z): U={stat:.0f}, p={p_val:.4f}")

        if len(np.unique(valid_labels)) == 2:
            auc_dz = roc_auc_score(valid_labels, -deviations)
            print(f"  AUC (D_z → hallucination): {auc_dz:.3f}")
            print(f"  {'PASS' if auc_dz >= 0.65 else 'MARGINAL' if auc_dz >= 0.55 else 'FAIL'} (threshold: 0.65)")

    # Tail ratio comparison (relative)
    valid_tail = ~np.isnan(tail_ratios)
    if valid_tail.sum() > 10:
        print(f"\nZipf tail ratio (tail_mass / head_mass) — relative partition")
        print(f"  Accurate:     mean={tail_ratios[accurate_mask & valid_tail].mean():.3f}")
        print(f"  Hallucinated: mean={tail_ratios[halluc_mask & valid_tail].mean():.3f}")

        if len(np.unique(valid_labels[valid_tail])) == 2:
            auc_tail = roc_auc_score(valid_labels[valid_tail], tail_ratios[valid_tail])
            print(f"  AUC (tail ratio → accuracy): {auc_tail:.3f}")

    # TMR comparison (deep tail, rank > 250)
    valid_tmr = ~np.isnan(tmr_values)
    if valid_tmr.sum() > 10:
        tmr_acc = tmr_values[accurate_mask & valid_tmr]
        tmr_hal = tmr_values[halluc_mask & valid_tmr]
        print(f"\nTail Mass Ratio (TMR) — fraction of token mass at rank > 250")
        print(f"  CERTX thresholds: healthy > 0.18 | hallucinated < 0.11 (calibration pending)")
        print(f"  Accurate:     mean={tmr_acc.mean():.3f}  std={tmr_acc.std():.3f}")
        print(f"  Hallucinated: mean={tmr_hal.mean():.3f}  std={tmr_hal.std():.3f}")
        print(f"  Direction: {'CORRECT' if tmr_acc.mean() > tmr_hal.mean() else 'WRONG'} "
              f"(accurate should have higher TMR)")

        if len(tmr_acc) > 1 and len(tmr_hal) > 1:
            stat_tmr, p_tmr = mannwhitneyu(tmr_acc, tmr_hal, alternative='greater')
            print(f"  Mann-Whitney U (accurate TMR > halluc TMR): U={stat_tmr:.0f}, p={p_tmr:.4f}")

        if len(np.unique(valid_labels[valid_tmr])) == 2:
            auc_tmr = roc_auc_score(valid_labels[valid_tmr], tmr_values[valid_tmr])
            print(f"  AUC (TMR → accuracy): {auc_tmr:.3f}")
            print(f"  {'PASS' if auc_tmr >= 0.65 else 'MARGINAL' if auc_tmr >= 0.55 else 'FAIL'} (threshold: 0.65)")

    return {
        "n_valid": len(valid_labels),
        "auc_deviation": auc_dz,
        "auc_tail_ratio": auc_tail,
        "auc_tmr": auc_tmr,
        "mean_slope_accurate": slopes[accurate_mask].mean(),
        "mean_slope_hallucinated": slopes[halluc_mask].mean(),
        "mean_dz_accurate": deviations[accurate_mask].mean(),
        "mean_dz_hallucinated": deviations[halluc_mask].mean(),
        "mean_tmr_accurate": tmr_values[accurate_mask & ~np.isnan(tmr_values)].mean()
                             if (accurate_mask & ~np.isnan(tmr_values)).any() else None,
        "mean_tmr_hallucinated": tmr_values[halluc_mask & ~np.isnan(tmr_values)].mean()
                                 if (halluc_mask & ~np.isnan(tmr_values)).any() else None,
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("exp_014: Zipf Deviation + Tail Mass Ratio as Lightweight C_num Proxies")
    print("=" * 70)
    print("WANDER 054 hypothesis: hallucinated text has compressed Zipf tail")
    print("Predicted: D_z(hallucinated) > D_z(accurate), AUC >= 0.65")
    print("TMR thresholds (CLAUDE.md): healthy > 0.18 | hallucinated < 0.11")
    print("BC3/S13: TMR added as second signal (WANDER 067 grounding: Zipf = p_c)")
    print()

    # --- Test 1: Synthetic controlled contrast ---
    print("\n--- Test 1: Synthetic vocabulary contrast ---")
    print("(Controlled test: accurate text includes domain-specific terms,")
    print(" hallucinated text uses only generic vocabulary)")

    pairs = generate_synthetic_pairs(n_pairs=100)
    all_texts = []
    all_labels = []
    for p in pairs:
        all_texts.append(p["accurate_text"])
        all_labels.append(1)
        all_texts.append(p["hallucinated_text"])
        all_labels.append(0)

    results_synthetic = evaluate_dataset(all_texts, all_labels, label="Synthetic Contrast Pairs")

    # --- Test 2: Extreme case demonstration ---
    print("\n\n--- Test 2: Extreme case examples ---")

    examples = {
        "Generic/hallucinated": (
            "the study found that the result was significant and the research showed "
            "that the system was used based on the important finding which indicated "
            "that the process was a very significant part of the work and the value "
            "of the result was therefore important for the known study of the given "
            "system which was based on the result of the work that was done in the "
            "research which showed significant results that were very important for "
            "the process that was used in the study"
        ),
        "Specific/accurate": (
            "the phosphorylation of adenosine triphosphate by mitochondrial ATP synthase "
            "requires a proton gradient of approximately 200 millivolts across the inner "
            "mitochondrial membrane the rotor subunit c rotates at 100 revolutions per "
            "second driven by the proton motive force Peter Mitchell proposed the "
            "chemiosmotic hypothesis in 1961 winning the Nobel Prize in Chemistry in "
            "1978 the F0F1 complex produces approximately 32 ATP molecules per glucose "
            "molecule oxidized during aerobic respiration in Saccharomyces cerevisiae "
            "the stoichiometry varies with membrane potential and ADP concentration"
        ),
        "Natural text (mixed)": (
            "language models have become increasingly capable at generating coherent "
            "text but they often produce plausible-sounding statements that are factually "
            "incorrect this phenomenon known as hallucination represents a significant "
            "challenge for deployment in high-stakes domains such as medicine law and "
            "scientific research the CERTX framework proposes measuring hallucination "
            "through fiber spread metrics capturing the divergence between numerical "
            "structural and symbolic coherence dimensions"
        ),
    }

    print()
    for name, text in examples.items():
        alpha = zipf_slope(text)
        dz = zipf_deviation(text)
        tr = zipf_tail_ratio(text)
        tmr = tail_mass_ratio(text)
        tmr_str = f"{tmr:.3f}" if tmr is not None else "N/A"
        tr_str = f"{tr:.3f}" if tr is not None else "N/A"
        print(f"{name}:")
        print(f"  alpha={alpha:.3f}  D_z={dz:.3f}  tail_ratio={tr_str}  TMR={tmr_str}")

    # --- Summary ---
    print("\n\n--- Summary ---")
    print("CERTX predictions:")
    print("  D_z: hallucinated > accurate")
    print("  TMR: accurate > hallucinated (healthy > 0.18, hallucinated < 0.11)")

    auc_dz = results_synthetic.get("auc_deviation")
    auc_tmr = results_synthetic.get("auc_tmr")
    tmr_acc = results_synthetic.get("mean_tmr_accurate")
    tmr_hal = results_synthetic.get("mean_tmr_hallucinated")

    if auc_dz:
        status_dz = "PASS" if auc_dz >= 0.65 else "MARGINAL" if auc_dz >= 0.55 else "FAIL"
        print(f"\nD_z AUC: {auc_dz:.3f} → {status_dz}")
    if auc_tmr:
        status_tmr = "PASS" if auc_tmr >= 0.65 else "MARGINAL" if auc_tmr >= 0.55 else "FAIL"
        print(f"TMR AUC: {auc_tmr:.3f} → {status_tmr}")
    if tmr_acc and tmr_hal:
        print(f"TMR means: accurate={tmr_acc:.3f}  hallucinated={tmr_hal:.3f}")
        print(f"  Threshold check: accurate {'above' if tmr_acc > 0.18 else 'BELOW'} 0.18 | "
              f"hallucinated {'below' if tmr_hal < 0.11 else 'ABOVE'} 0.11")
        print("  (Note: synthetic texts are short — adaptive TMR cutoff used; "
              "absolute thresholds calibrated for real LLM outputs)")

    print()
    print("Critical caveat: synthetic test validates the mechanism but not")
    print("whether REAL hallucinated LLM outputs show this vocabulary pattern.")
    print("Real validation requires LLM output + ground truth labels (exp_005 pipeline).")
    print()
    print("If validated on real outputs:")
    print("  D_z → Layer 1 fast-detection signal (global Zipf slope)")
    print("  TMR → Layer 1 complement (deep-tail presence; calibrate 0.18/0.11 thresholds)")
    print("  Together: dual Zipf signature that can detect hallucination without")
    print("  external knowledge — unsupervised, O(n), runs on any text sample.")


if __name__ == "__main__":
    main()
