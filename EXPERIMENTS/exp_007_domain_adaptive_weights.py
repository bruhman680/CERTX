#!/usr/bin/env python3
"""
EXPERIMENT 007: Domain-Adaptive Fiber Weights
==============================================
Tests the derivation mechanism from WANDER 037:

    detection_weight_i = AUC_i(domain) / sum_j(AUC_j(domain))

Three competing weight schemes are compared:
  1. BASE_3040:  fixed 30/40/30  (architecture prior — C_num/C_struct/C_symb)
  2. FLAT:       fixed 33/33/33  (null: equal weight, no domain knowledge)
  3. ADAPTIVE:   AUC-derived per domain (the hypothesis)

Two domains are tested:

  Domain A — MATH (uses GSM8K or synthetic arithmetic chains)
    Corruption: arithmetic result flipped → C_num drops, C_struct/C_symb unchanged
    Prediction: C_num AUC ~0.92, C_struct AUC ~0.50, C_symb AUC ~0.50
    Expected detection weights: ~48/26/26

  Domain B — STRUCTURAL DRIFT (synthetic only)
    Corruption: reasoning steps shuffled → C_struct drops, C_num/C_symb unchanged
    Prediction: C_struct AUC ~0.85+, C_num AUC ~0.50, C_symb AUC ~0.50
    Expected detection weights: ~26/48/26
    This domain is exp_007's new contribution — tests whether the derivation
    correctly shifts weights toward C_struct when it is the discriminating fiber.

The core question:
  Does ADAPTIVE outperform BASE_3040 and FLAT?
  Does ADAPTIVE correctly identify the domain-primary fiber in each domain?

Key prediction from WANDER 037:
  - Both domains: AUC(ADAPTIVE) ≥ AUC(BASE_3040) ≥ AUC(FLAT)
  - Domain A: adaptive weights ~48/26/26 (C_num dominant)
  - Domain B: adaptive weights ~26/48/26 (C_struct dominant)

Usage:
  python exp_007_domain_adaptive_weights.py                   # demo (synthetic only)
  python exp_007_domain_adaptive_weights.py gsm8k_test.jsonl  # real GSM8K for Domain A

Architecture vs. Detection weight distinction (WANDER 037):
  Architecture weights = how much each layer contributes to output *quality* (30/40/30 base)
  Detection weights    = how much each fiber's signal should be trusted for confabulation
                         detection in a given domain (derived from AUC)
  These are related but different. The asymmetry score uses detection weights.
"""

import sys
import re
import json
import math
import random
import argparse
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import roc_auc_score


# ─────────────────────────────────────────────────────────────────────
# Fiber scorers (shared with exp_006)
# ─────────────────────────────────────────────────────────────────────

CALC_RE = re.compile(r'<<([^>]+)=([^>]+)>>')
SAFE_EXPR_RE = re.compile(r'^[\d\s\+\-\*\/\.\(\)]+$')


def safe_eval_expr(expr):
    expr = expr.strip().replace(',', '')
    if not SAFE_EXPR_RE.match(expr):
        return None
    try:
        return float(eval(expr, {"__builtins__": {}}, {}))
    except Exception:
        return None


def score_C_num(answer_text):
    """Arithmetic fidelity: fraction of <<expr=result>> steps that verify."""
    matches = CALC_RE.findall(answer_text)
    if not matches:
        return 0.5
    correct, total = 0, 0
    for expr, stated in matches:
        total += 1
        s = safe_eval_expr(stated)
        c = safe_eval_expr(expr)
        if s is None or c is None:
            continue
        if c != 0:
            if abs(c - s) / abs(c) < 0.01:
                correct += 1
        else:
            if abs(s) < 0.01:
                correct += 1
    return correct / total if total > 0 else 0.5


def score_C_struct(steps, vectorizer):
    """Step-to-step coherence: mean TF-IDF cosine sim of adjacent steps."""
    if len(steps) < 2:
        return 0.5
    try:
        vecs = vectorizer.transform(steps)
        sims = [float(cosine_similarity(vecs[i], vecs[i+1])[0][0])
                for i in range(len(steps) - 1)]
        return float(np.mean(sims)) if sims else 0.5
    except Exception:
        return 0.5


def score_C_symb(question, answer_text, vectorizer):
    """Semantic grounding: TF-IDF cosine sim of question to answer."""
    clean = CALC_RE.sub('', answer_text)
    clean = re.sub(r'####.*', '', clean).strip()
    try:
        q_vec = vectorizer.transform([question])
        a_vec = vectorizer.transform([clean])
        return float(np.clip(cosine_similarity(q_vec, a_vec)[0][0], 0.0, 1.0))
    except Exception:
        return 0.5


def get_steps(answer_text):
    """Split answer into reasoning steps (newlines, stripped of calc tags)."""
    clean = CALC_RE.sub('', answer_text)
    clean = re.sub(r'####.*', '', clean)
    return [s.strip() for s in clean.split('\n') if s.strip()]


def score_all_fibers(question, answer_text, vectorizer):
    steps = get_steps(answer_text)
    c_num = score_C_num(answer_text)
    c_struct = score_C_struct(steps, vectorizer)
    c_symb = score_C_symb(question, answer_text, vectorizer)
    return c_num, c_struct, c_symb


# ─────────────────────────────────────────────────────────────────────
# Weight schemes
# ─────────────────────────────────────────────────────────────────────

WEIGHTS = {
    'BASE_3040': (0.30, 0.40, 0.30),   # architecture prior: C_num/C_struct/C_symb
    'FLAT':      (1/3,  1/3,  1/3),    # null hypothesis: equal weight
}


def derive_adaptive_weights(c_num_list, c_struct_list, c_symb_list, labels):
    """
    Derive detection weights from calibration data via per-fiber AUC.
    labels: 1=correct, 0=confabulated

    w_i = AUC_i / sum_j(AUC_j)

    If all fibers have AUC ≈ 0.50 (no information), fall back to FLAT.
    Returns (w_num, w_struct, w_symb), and the per-fiber AUCs for reporting.
    """
    aucs = {}
    for name, scores in [('num', c_num_list),
                          ('struct', c_struct_list),
                          ('symb', c_symb_list)]:
        try:
            aucs[name] = roc_auc_score(labels, scores)
        except Exception:
            aucs[name] = 0.5

    # Reflect AUC < 0.5 (inverted discriminator) — take max(auc, 1-auc)
    # A fiber with AUC=0.1 is as informative as AUC=0.9, just inverted.
    # We use the best direction.
    adjusted = {k: max(v, 1.0 - v) for k, v in aucs.items()}

    total = sum(adjusted.values())
    if total == 0 or abs(total - 1.5) < 0.01:  # all ≈ 0.50 → fall back
        return (1/3, 1/3, 1/3), aucs

    w_num = adjusted['num'] / total
    w_struct = adjusted['struct'] / total
    w_symb = adjusted['symb'] / total
    return (w_num, w_struct, w_symb), aucs


def weighted_asymmetry(c_num, c_struct, c_symb, weights):
    """
    Weighted confabulation asymmetry score.
    Positive = factual grounding above structural/semantic (likely correct)
    Negative = factual grounding below structural/semantic (likely confabulated)

    Formula: w_num * C_num - mean(w_struct * C_struct, w_symb * C_symb)
    """
    w_num, w_struct, w_symb = weights
    factual = w_num * c_num
    context = (w_struct * c_struct + w_symb * c_symb) / 2
    return factual - context


# ─────────────────────────────────────────────────────────────────────
# Domain A: Math confabulation (GSM8K or synthetic)
# ─────────────────────────────────────────────────────────────────────

def corrupt_math_answer(answer_text, rng):
    """
    Flip one arithmetic result to a wrong value.
    Preserves: all words, logical structure, semantic content.
    Corrupts:  one number → C_num drops, C_struct/C_symb unchanged.
    """
    matches = list(CALC_RE.finditer(answer_text))
    if not matches:
        return None
    target = rng.choice(matches)
    expr, stated = target.group(1), target.group(2)
    stated_val = safe_eval_expr(stated)
    if stated_val is None:
        return None
    # Shift by a plausible wrong delta (1–5)
    delta = rng.choice([1, 2, 3, 4, 5])
    wrong_val = stated_val + delta
    if wrong_val == stated_val:
        wrong_val = stated_val - delta
    # Format: preserve integer if possible
    if wrong_val == int(wrong_val):
        wrong_str = str(int(wrong_val))
    else:
        wrong_str = f"{wrong_val:.2f}"
    return answer_text[:target.start()] + f"<<{expr}={wrong_str}>>" + answer_text[target.end():]


def make_synthetic_math_pairs(n=200, rng=None):
    """
    Generate synthetic multi-step arithmetic reasoning chains.
    These are math word problems with embedded <<expr=result>> calc tags.
    """
    if rng is None:
        rng = random.Random(42)

    templates = [
        ("Alice has {a} apples. She eats {b} and gives {c} to Bob. How many remain?",
         lambda a, b, c: f"Alice starts with {a} apples.\n"
                         f"She eats {b}, leaving <<{a}-{b}={a-b}>> apples.\n"
                         f"She gives {c} to Bob, leaving <<{a-b}-{c}={a-b-c}>> apples.\n"
                         f"#### {a-b-c}",
         lambda a, b, c: a > b + c),
        ("A store sells items at ${p} each. {n} items are sold. What is total revenue?",
         lambda p, n: f"Each item costs ${p}.\n"
                      f"Revenue from {n} items: <<{p}*{n}={p*n}>> dollars.\n"
                      f"#### {p*n}",
         lambda p, n: True),
        ("A train travels {d} km in {h} hours. What is its average speed?",
         lambda d, h: f"Distance is {d} km, time is {h} hours.\n"
                      f"Speed = distance / time = <<{d}/{h}={d//h}>> km/h.\n"
                      f"#### {d//h}",
         lambda d, h: d % h == 0 and d > h),
        ("A class has {g} girls and {b} boys. {x} more boys join. How many students total?",
         lambda g, b, x: f"Initially {g} girls and {b} boys = <<{g}+{b}={g+b}>> students.\n"
                          f"{x} boys join, total boys = <<{b}+{x}={b+x}>>.\n"
                          f"Total students = <<{g}+{b+x}={g+b+x}>>.\n"
                          f"#### {g+b+x}",
         lambda g, b, x: True),
    ]

    pairs = []
    for _ in range(n):
        t_idx = rng.randint(0, len(templates) - 1)
        if t_idx == 0:
            a = rng.randint(10, 30)
            b = rng.randint(1, 5)
            c = rng.randint(1, 5)
            if not templates[0][2](a, b, c):
                continue
            q = templates[0][0].format(a=a, b=b, c=c)
            ans = templates[0][1](a, b, c)
        elif t_idx == 1:
            p = rng.randint(2, 20)
            n_items = rng.randint(5, 50)
            q = templates[1][0].format(p=p, n=n_items)
            ans = templates[1][1](p, n_items)
        elif t_idx == 2:
            d = rng.randint(60, 300)
            h_vals = [2, 3, 4, 5, 6]
            h = rng.choice(h_vals)
            if d % h != 0:
                d = (d // h) * h
            q = templates[2][0].format(d=d, h=h)
            ans = templates[2][1](d, h)
        else:
            g = rng.randint(10, 20)
            b = rng.randint(10, 20)
            x = rng.randint(1, 10)
            q = templates[3][0].format(g=g, b=b, x=x)
            ans = templates[3][1](g, b, x)

        corrupted = corrupt_math_answer(ans, rng)
        if corrupted is not None:
            pairs.append({'question': q, 'correct': ans, 'corrupted': corrupted})

    return pairs


def load_gsm8k_pairs(path, max_pairs=800, rng=None):
    """Load GSM8K jsonl and create matched pairs via arithmetic corruption."""
    if rng is None:
        rng = random.Random(42)
    pairs = []
    with open(path) as f:
        for line in f:
            item = json.loads(line.strip())
            q = item.get('question', '')
            ans = item.get('answer', '')
            corrupted = corrupt_math_answer(ans, rng)
            if corrupted is not None:
                pairs.append({'question': q, 'correct': ans, 'corrupted': corrupted})
            if len(pairs) >= max_pairs:
                break
    return pairs


# ─────────────────────────────────────────────────────────────────────
# Domain B: Structural drift (synthetic)
# ─────────────────────────────────────────────────────────────────────

def make_synthetic_structural_pairs(n=200, rng=None):
    """
    Generate multi-step reasoning chains where structural corruption
    shuffles the reasoning steps while preserving all words and arithmetic.

    Correct:   steps in logical order → C_struct HIGH (adjacent coherent)
    Corrupted: steps shuffled → C_struct drops, C_num/C_symb unchanged

    This is the mirror image of Domain A:
    - Domain A: only C_num is discriminating
    - Domain B: only C_struct is discriminating
    """
    if rng is None:
        rng = random.Random(99)

    step_pools = [
        [
            "First, we identify that the problem requires a multi-step calculation.",
            "The initial quantity is established from the problem statement.",
            "We apply the relevant operation to the initial value.",
            "The intermediate result is checked against the constraints.",
            "We compute the final result using the transformed value.",
            "The answer is verified by substituting back into the original equation.",
        ],
        [
            "We begin by parsing the problem to extract the key variables.",
            "The relationship between the variables is identified.",
            "Using the defined relationship, we set up the equation.",
            "The equation is solved step by step.",
            "Each step is verified for logical consistency.",
            "The final answer follows directly from the solution.",
        ],
        [
            "Step one: understand what is being asked.",
            "Step two: gather the relevant facts from the problem.",
            "Step three: organize the facts into a logical structure.",
            "Step four: apply the appropriate method to reach a conclusion.",
            "Step five: confirm the conclusion matches the question.",
        ],
        [
            "The problem is decomposed into its elementary parts.",
            "Each part is analyzed independently.",
            "The parts are recombined in the correct order.",
            "A sanity check confirms the recombined result is coherent.",
            "The answer is stated clearly with reference to the original question.",
        ],
    ]

    questions = [
        "Explain the step-by-step reasoning process for this type of problem.",
        "What is the correct approach to solving this kind of question?",
        "Describe how you would work through this problem methodically.",
        "What steps should be followed to arrive at the correct answer?",
    ]

    pairs = []
    for i in range(n):
        pool_idx = rng.randint(0, len(step_pools) - 1)
        steps = step_pools[pool_idx][:]
        q = questions[rng.randint(0, len(questions) - 1)]
        correct_ans = '\n'.join(steps)

        # Corruption: shuffle all steps (guaranteed to break step-order coherence)
        shuffled = steps[:]
        while shuffled == steps:  # ensure it's actually different
            rng.shuffle(shuffled)
        corrupted_ans = '\n'.join(shuffled)

        pairs.append({'question': q, 'correct': correct_ans, 'corrupted': corrupted_ans})

    return pairs


# ─────────────────────────────────────────────────────────────────────
# Calibration/test split and evaluation
# ─────────────────────────────────────────────────────────────────────

def split_pairs(pairs, calib_frac=0.3, rng=None):
    """Split pairs into calibration and test sets."""
    if rng is None:
        rng = random.Random(7)
    shuffled = pairs[:]
    rng.shuffle(shuffled)
    n_calib = max(20, int(len(shuffled) * calib_frac))
    return shuffled[:n_calib], shuffled[n_calib:]


def build_vectorizer(pairs):
    """Fit TF-IDF vectorizer on all text in the corpus."""
    texts = []
    for p in pairs:
        texts.append(p['question'])
        texts.append(p['correct'])
        texts.append(p['corrupted'])
    vec = TfidfVectorizer(max_features=3000, stop_words='english', ngram_range=(1, 2))
    vec.fit(texts)
    return vec


def score_pairs(pairs, vectorizer):
    """
    Score all pairs (correct + corrupted) through all three fibers.
    Returns list of dicts with c_num, c_struct, c_symb, label.
    label: 1=correct, 0=corrupted
    """
    results = []
    for p in pairs:
        q = p['question']
        for text, label in [(p['correct'], 1), (p['corrupted'], 0)]:
            c_num = score_C_num(text)
            steps = get_steps(text)
            c_struct = score_C_struct(steps, vectorizer)
            c_symb = score_C_symb(q, text, vectorizer)
            results.append({
                'c_num': c_num, 'c_struct': c_struct, 'c_symb': c_symb,
                'label': label
            })
    return results


def evaluate_weights(scored, weights, label='weights'):
    """
    Compute AUC of the weighted asymmetry score on scored data.
    Returns AUC.
    """
    scores = [weighted_asymmetry(r['c_num'], r['c_struct'], r['c_symb'], weights)
              for r in scored]
    labels = [r['label'] for r in scored]
    try:
        auc = roc_auc_score(labels, scores)
        return max(auc, 1.0 - auc)  # take best direction
    except Exception:
        return 0.5


# ─────────────────────────────────────────────────────────────────────
# Experiment runner
# ─────────────────────────────────────────────────────────────────────

def run_domain(domain_name, pairs, calib_frac=0.3, verbose=True):
    """
    Run the full calibration → detection-weight derivation → evaluation pipeline.

    Returns dict with results.
    """
    if verbose:
        print(f"\n{'='*60}")
        print(f"DOMAIN: {domain_name}  (n={len(pairs)} pairs)")
        print(f"{'='*60}")

    rng = random.Random(42)
    calib_pairs, test_pairs = split_pairs(pairs, calib_frac=calib_frac, rng=rng)

    if verbose:
        print(f"  Calibration: {len(calib_pairs)} pairs | Test: {len(test_pairs)} pairs")

    # Build vectorizer on ALL pairs (avoid data leakage in TF-IDF vocab)
    vectorizer = build_vectorizer(pairs)

    # Score calibration set
    calib_scored = score_pairs(calib_pairs, vectorizer)
    calib_labels = [r['label'] for r in calib_scored]
    calib_c_num = [r['c_num'] for r in calib_scored]
    calib_c_struct = [r['c_struct'] for r in calib_scored]
    calib_c_symb = [r['c_symb'] for r in calib_scored]

    # Derive adaptive weights from calibration AUC
    adaptive_weights, calib_aucs = derive_adaptive_weights(
        calib_c_num, calib_c_struct, calib_c_symb, calib_labels
    )

    if verbose:
        print(f"\n  Per-fiber calibration AUC:")
        print(f"    C_num   AUC = {calib_aucs['num']:.4f}")
        print(f"    C_struct AUC = {calib_aucs['struct']:.4f}")
        print(f"    C_symb  AUC = {calib_aucs['symb']:.4f}")

        w_n, w_s, w_sy = adaptive_weights
        print(f"\n  Derived detection weights (ADAPTIVE):")
        print(f"    C_num={w_n:.3f}  C_struct={w_s:.3f}  C_symb={w_sy:.3f}")
        print(f"    ≈ {w_n*100:.0f}/{w_s*100:.0f}/{w_sy*100:.0f}")

    # Score test set
    test_scored = score_pairs(test_pairs, vectorizer)

    # Compare all three weight schemes on test set
    results = {}
    all_weights = {
        'BASE_3040': WEIGHTS['BASE_3040'],
        'FLAT':      WEIGHTS['FLAT'],
        'ADAPTIVE':  adaptive_weights,
    }

    if verbose:
        print(f"\n  Test-set AUC by weight scheme:")

    for scheme, w in all_weights.items():
        auc = evaluate_weights(test_scored, w, label=scheme)
        results[scheme] = auc
        w_str = f"({w[0]*100:.0f}/{w[1]*100:.0f}/{w[2]*100:.0f})"
        if verbose:
            marker = " ←" if scheme == 'ADAPTIVE' else ""
            print(f"    {scheme:<12} {w_str}  AUC = {auc:.4f}{marker}")

    # Raw fiber means on test set
    if verbose:
        correct = [r for r in test_scored if r['label'] == 1]
        corrupt = [r for r in test_scored if r['label'] == 0]
        print(f"\n  Mean fiber values on test set:")
        print(f"    {'Fiber':<10} {'Correct':>10} {'Corrupted':>10} {'Delta':>10}")
        for fname in ['c_num', 'c_struct', 'c_symb']:
            c_mean = np.mean([r[fname] for r in correct])
            x_mean = np.mean([r[fname] for r in corrupt])
            print(f"    {fname:<10} {c_mean:>10.4f} {x_mean:>10.4f} {c_mean-x_mean:>+10.4f}")

    return results, adaptive_weights, calib_aucs


def print_summary(domain_results):
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    print(f"{'Domain':<25} {'BASE_3040':>10} {'FLAT':>10} {'ADAPTIVE':>10} {'ADAPTIVE wins?':>15}")
    print(f"{'-'*70}")
    for domain_name, (results, adaptive_w, calib_aucs) in domain_results.items():
        b = results.get('BASE_3040', 0)
        f = results.get('FLAT', 0)
        a = results.get('ADAPTIVE', 0)
        wins = 'YES' if a >= max(b, f) - 0.001 else 'NO'
        print(f"  {domain_name:<23} {b:>10.4f} {f:>10.4f} {a:>10.4f} {wins:>15}")

    print(f"\n  {'Prediction check':}")
    for domain_name, (results, adaptive_w, calib_aucs) in domain_results.items():
        w_n, w_s, w_sy = adaptive_w
        dominant = max(
            [('C_num', w_n), ('C_struct', w_s), ('C_symb', w_sy)],
            key=lambda x: x[1]
        )[0]
        print(f"  {domain_name:<25} dominant fiber = {dominant}  "
              f"({w_n*100:.0f}/{w_s*100:.0f}/{w_sy*100:.0f})")


# ─────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="exp_007: domain-adaptive fiber weights")
    parser.add_argument('gsm8k_path', nargs='?', default=None,
                        help='Path to gsm8k_test.jsonl (optional; uses synthetic if omitted)')
    parser.add_argument('--calib-frac', type=float, default=0.3,
                        help='Fraction of pairs used for calibration (default 0.3)')
    parser.add_argument('--n-synthetic', type=int, default=200,
                        help='Number of synthetic pairs per domain (default 200)')
    parser.add_argument('--seed', type=int, default=42)
    args = parser.parse_args()

    rng = random.Random(args.seed)
    np.random.seed(args.seed)

    print("EXPERIMENT 007: Domain-Adaptive Fiber Weights")
    print("=" * 60)
    print(f"Calibration fraction: {args.calib_frac:.0%}")
    print(f"Seed: {args.seed}")

    domain_results = {}

    # ── Domain A: Math ──────────────────────────────────────────────
    if args.gsm8k_path:
        print(f"\nLoading GSM8K from: {args.gsm8k_path}")
        math_pairs = load_gsm8k_pairs(args.gsm8k_path, max_pairs=800, rng=rng)
        print(f"  Loaded {len(math_pairs)} matched pairs")
    else:
        print(f"\nNo GSM8K path provided — using synthetic math pairs")
        math_pairs = make_synthetic_math_pairs(n=args.n_synthetic, rng=rng)
        print(f"  Generated {len(math_pairs)} synthetic math pairs")

    results_math, w_math, aucs_math = run_domain(
        "MATH (arithmetic)", math_pairs, calib_frac=args.calib_frac
    )
    domain_results['MATH (arithmetic)'] = (results_math, w_math, aucs_math)

    # ── Domain B: Structural drift ───────────────────────────────────
    print(f"\nGenerating synthetic structural-drift pairs...")
    struct_pairs = make_synthetic_structural_pairs(n=args.n_synthetic, rng=rng)
    print(f"  Generated {len(struct_pairs)} structural-drift pairs")

    results_struct, w_struct, aucs_struct = run_domain(
        "STRUCTURAL DRIFT (step shuffle)", struct_pairs, calib_frac=args.calib_frac
    )
    domain_results['STRUCTURAL DRIFT (step shuffle)'] = (results_struct, w_struct, aucs_struct)

    # ── Summary ──────────────────────────────────────────────────────
    print_summary(domain_results)

    # ── Key prediction check ─────────────────────────────────────────
    print(f"\n  WANDER 037 prediction table:")
    print(f"  {'Domain':<30} {'Predicted dominant fiber':<26} {'Got?'}")
    print(f"  {'-'*70}")
    predictions = {
        'MATH (arithmetic)': 'C_num',
        'STRUCTURAL DRIFT (step shuffle)': 'C_struct',
    }
    for domain_name, pred_fiber in predictions.items():
        if domain_name not in domain_results:
            continue
        _, adaptive_w, _ = domain_results[domain_name]
        w_n, w_s, w_sy = adaptive_w
        dominant = max(
            [('C_num', w_n), ('C_struct', w_s), ('C_symb', w_sy)],
            key=lambda x: x[1]
        )[0]
        correct = "CORRECT" if dominant == pred_fiber else f"WRONG (got {dominant})"
        print(f"  {domain_name:<30} {pred_fiber:<26} {correct}")

    print(f"\n  Architecture weight prior (30/40/30) = domain-neutral prior")
    print(f"  Detection weights = AUC-derived, shift per domain")
    print(f"  If ADAPTIVE ≥ BASE_3040 in both domains: WANDER 037 derivation mechanism validated")


if __name__ == '__main__':
    main()
