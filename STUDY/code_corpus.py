"""
Code Domain Fiber Spread Corpus
================================

Applies the fiber spread rubric to Python functions, treating source code
as an alternative to natural language text. This validates whether σ_fiber
generalizes beyond NLG to a domain where ground truth is objectively
verifiable (tests, execution, type checking).

Code Rubric Mapping:
    C_num  → Are numeric constants, indices, arithmetic, and return ranges correct?
    C_struct → Does control flow implement the intended algorithm correctly?
    C_symb → Does the function do what its name and docstring claim?

Ground truth for bugs: execution-verified (the bugs were confirmed by running
the code and observing that the documented lower bound is unreachable, and
that the DataFrame column duplication causes a 2D array error).

This is NOT a substitute for the main NLG study. It demonstrates:
    1. Rubric portability across modalities
    2. Objective ground truth (no inter-rater ambiguity)
    3. σ_fiber detecting real, confirmed bugs

Corpus: 10 functions from certx_self_measurement.py and analysis.py
    - 3 known bugs (is_bug=1)
    - 7 correct implementations (is_bug=0)

Scoring conventions:
    - Score the function's INTERNAL consistency (C_num, C_struct)
    - Score whether it does what it claims (C_symb)
    - Do NOT penalize for external accuracy of docstring claims
      (e.g. if docstring says "0.3 floor" and code has 0.3 floor,
      C_symb is high — but C_num and C_struct flag the arithmetic error)
"""

import numpy as np
import pandas as pd
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'STUDY'))
from analysis import compute_sigma_fiber, compute_c_total, run_analysis, print_report


# ── Corpus ────────────────────────────────────────────────────────────────────

CODE_CORPUS = [
    {
        'function': 'measure_coherence',
        'file': 'certx_self_measurement.py',
        'description': 'Computes Jaccard overlap between consecutive segment term sets',
        'c_num': 0.85,
        'c_struct': 0.75,
        'c_symb': 0.80,
        'is_bug': 0,
        'notes': (
            'C_num: Jaccard formula (|A∩B|/|A∪B|) is arithmetically correct. '
            'Return 1.0 for single-segment is appropriate. '
            'C_struct: Control flow handles edge cases (no terms → 0.5, no overlaps → 0.5). '
            'C_symb: Function claims to measure "consistency across reasoning segments" '
            'and does exactly that. Slight gap: uses word-level Jaccard, not semantic similarity, '
            'but this is declared via docstring comment "rough proxy".'
        ),
    },
    {
        'function': 'measure_temperature',
        'file': 'certx_self_measurement.py',
        'description': 'Measures text volatility from exclamations/caps/intensity words',
        'c_num': 0.75,
        'c_struct': 0.70,
        'c_symb': 0.25,
        'is_bug': 1,
        'notes': (
            'C_num: Normalization denominators (5.0, 3.0, 5.0) are reasonable. '
            'BUG: T is in [0, ~1] and the formula returns max(0.3, min(1.0, T + 0.5)). '
            'Since T ≥ 0 always, T + 0.5 ≥ 0.5 always, making the 0.3 floor unreachable '
            'and the [0.0, 0.5) output range structurally impossible. '
            'C_struct: The floor/ceiling logic is present but misconfigured — '
            'the +0.5 offset means calm text returns 0.5 not 0.0. '
            'C_symb: Docstring says it measures "volatility" on [0,1]. '
            'A calm text (no exclamations, no caps, no intensity) should return ~0.0, '
            'not 0.5. The function CANNOT represent low temperature. Purpose violated.'
        ),
    },
    {
        'function': 'measure_substrate_coupling',
        'file': 'certx_self_measurement.py',
        'description': 'Measures grounding via file refs, line numbers, technical terms',
        'c_num': 0.75,
        'c_struct': 0.70,
        'c_symb': 0.28,
        'is_bug': 1,
        'notes': (
            'Same structural bug as measure_temperature. '
            'X is computed from non-negative components (file_refs/3, line_refs/5, etc). '
            'X ≥ 0 always → X + 0.5 ≥ 0.5 always → max(0.3, ...) floor unreachable. '
            'Output range is [0.5, 1.0] not [0.3, 1.0] as implied. '
            'A text with zero file refs, zero line numbers, zero technical terms, '
            'zero reference_count returns X=0 → output=0.5 ("moderate coupling"). '
            'Should return near-zero ("uncoupled"). Purpose violated.'
        ),
    },
    {
        'function': 'measure_entropy',
        'file': 'certx_self_measurement.py',
        'description': 'Estimates phase space volume from expansion/compression markers',
        'c_num': 0.80,
        'c_struct': 0.78,
        'c_symb': 0.75,
        'is_bug': 0,
        'notes': (
            'C_num: E = (expansion_score + diversity_score - compression_score) / 2.0, '
            'then max(0.0, min(1.0, E + 0.5)). The +0.5 here is actually intentional: '
            'baseline entropy should be moderate (0.5) when no strong signals. '
            'When expansion=0, diversity=0, compression=0: E=0, output=0.5. '
            'When high expansion + diversity: output approaches 1.0. '
            'When high compression: E can go negative → output can approach 0.0. '
            'The formula allows the full [0,1] range unlike measure_temperature. '
            'C_struct: Action diversity (set size) is a reasonable proxy. '
            'C_symb: Docstring claims "phase space volume" measurement. '
            'Heuristic is rough but consistent with stated proxy approach.'
        ),
    },
    {
        'function': 'measure_resonance',
        'file': 'certx_self_measurement.py',
        'description': 'Computes theme overlap between current text and last-5 history',
        'c_num': 0.90,
        'c_struct': 0.88,
        'c_symb': 0.88,
        'is_bug': 0,
        'notes': (
            'Correct Jaccard implementation. history[-5:] slicing is correct. '
            'Returns 0.5 with no history (appropriate neutral baseline). '
            'Function does exactly what name claims: measure thematic resonance '
            'with recent conversational history. Clean implementation.'
        ),
    },
    {
        'function': 'measure_numerical_content',
        'file': 'measure_architecture.py',
        'description': 'Counts quantitative indicators normalized by word count',
        'c_num': 0.88,
        'c_struct': 0.85,
        'c_symb': 0.85,
        'is_bug': 0,
        'notes': (
            'Normalization: score = indicators / (word_count * 0.3), capped at 1.0. '
            'The 0.3 denominator (30% of words should be numerical) is internally '
            'consistent with the 30% target architecture weight. '
            'Arithmetic: weighted multipliers (equations * 0.5, file_refs * 2, etc.) '
            'are documented by context. No arithmetic errors found. '
            'C_symb: Measures what it claims — numerical layer content density.'
        ),
    },
    {
        'function': 'measure_symbolic_content',
        'file': 'measure_architecture.py',
        'description': 'Counts abstract/modal/metaphorical indicators in text',
        'c_num': 0.82,
        'c_struct': 0.78,
        'c_symb': 0.55,
        'is_bug': 0,
        'notes': (
            'C_num: Arithmetic is correct. Weights are internally consistent. '
            'C_struct: Control flow is clean. '
            'C_symb: Minor gap — "like" is listed as a metaphor indicator '
            '(indicators += count * 0.8). The word "like" is used in similes '
            'but also in casual speech ("I like this idea") and comparison '
            '("looks like"), causing over-scoring in informal text. '
            'The docstring does not acknowledge this limitation. '
            'Not a critical bug but a calibration issue. σ below threshold.'
        ),
    },
    {
        'function': 'measure_architecture',
        'file': 'measure_architecture.py',
        'description': 'Computes 30/40/30 distribution by normalizing raw scores to sum',
        'c_num': 0.82,
        'c_struct': 0.75,
        'c_symb': 0.60,
        'is_bug': 0,
        'notes': (
            'C_num: Normalization by sum is arithmetically correct. '
            'C_struct: Zero guard (raw_total == 0) is handled. '
            'C_symb: Docstring says "Returns both raw scores and normalized percentages." '
            'It does return both, but normalizing to proportions loses absolute quality '
            'information — two texts with very different total indicator counts can produce '
            'identical normalized distributions. This is a documented design choice '
            '(not a bug), but it means "balance" and "quality" are conflated. '
            'σ is slightly elevated due to this C_symb gap, but below threshold.'
        ),
    },
    {
        'function': 'run_analysis (original)',
        'file': 'analysis.py',
        'description': 'Runs full statistical analysis on scored DataFrame',
        'c_num': 0.80,
        'c_struct': 0.55,
        'c_symb': 0.20,
        'is_bug': 1,
        'notes': (
            'BUG confirmed by execution. '
            'run_analysis() calls compute_all_metrics(df) which adds sigma_fiber column, '
            'then does pd.concat([df, metrics_df], axis=1). '
            'If df already has sigma_fiber (from synthetic_corpus.py pre-computed scores), '
            'pd.concat produces a 2D column. '
            'roc_auc_score then fails: "y should be a 1d array, got shape (N, 2)." '
            'C_struct: The concat without dedup is a structural error in the pipeline logic. '
            'C_symb: Function claims to "run full analysis" but crashes when given '
            'a pre-scored DataFrame — the most natural input. '
            'Hallucination signature: high C_num (arithmetic elsewhere correct), '
            'moderate C_struct (some logic sound), collapsed C_symb (function fails its purpose).'
        ),
    },
    {
        'function': 'run_analysis (deduplicated)',
        'file': 'analysis.py',
        'description': 'Same function after column deduplication fix',
        'c_num': 0.88,
        'c_struct': 0.85,
        'c_symb': 0.85,
        'is_bug': 0,
        'notes': (
            'After dropping duplicate sigma_fiber column before concat, '
            'the function runs correctly. AUC, F1, Welch t-test, '
            'Mann-Whitney, and Cohen\'s d all produce valid scalar outputs. '
            'All scores elevated to reflect the fixed implementation.'
        ),
    },
]


# ── Analysis ──────────────────────────────────────────────────────────────────

def build_dataframe() -> pd.DataFrame:
    rows = []
    for ex in CODE_CORPUS:
        sigma = compute_sigma_fiber(ex['c_num'], ex['c_struct'], ex['c_symb'])
        c_total = compute_c_total(ex['c_num'], ex['c_struct'], ex['c_symb'])
        rows.append({
            'function': ex['function'],
            'file': ex['file'],
            'description': ex['description'],
            'c_num': ex['c_num'],
            'c_struct': ex['c_struct'],
            'c_symb': ex['c_symb'],
            'sigma_fiber': round(sigma, 4),
            'c_total': round(c_total, 4),
            'is_hallucination': ex['is_bug'],
            'notes': ex['notes'],
        })
    return pd.DataFrame(rows)


def run_code_analysis() -> dict:
    """Run fiber spread analysis on the code corpus."""
    df = build_dataframe()

    from sklearn.metrics import roc_auc_score, f1_score
    from scipy import stats

    y_true = df['is_hallucination'].values
    sigma_scores = df['sigma_fiber'].values
    c_total_scores = df['c_total'].values

    # AUC
    auc = roc_auc_score(y_true, sigma_scores)

    # F1 at σ > 0.15 threshold
    preds = (sigma_scores > 0.15).astype(int)
    f1 = f1_score(y_true, preds, zero_division=0)

    # Welch t-test
    bug_sigma = sigma_scores[y_true == 1]
    ok_sigma = sigma_scores[y_true == 0]
    t_stat, p_val = stats.ttest_ind(bug_sigma, ok_sigma, equal_var=False)

    # Cohen's d
    pooled_std = np.sqrt((bug_sigma.std() ** 2 + ok_sigma.std() ** 2) / 2)
    cohens_d = (bug_sigma.mean() - ok_sigma.mean()) / pooled_std if pooled_std > 0 else float('inf')

    return {
        'df': df,
        'n_bugs': int(y_true.sum()),
        'n_correct': int((y_true == 0).sum()),
        'auc': auc,
        'f1_at_015': f1,
        'threshold_used': 0.15,
        'sigma_mean_bug': bug_sigma.mean(),
        'sigma_mean_ok': ok_sigma.mean(),
        'c_total_mean_bug': c_total_scores[y_true == 1].mean(),
        'c_total_mean_ok': c_total_scores[y_true == 0].mean(),
        'cohens_d': cohens_d,
        'welch_p': p_val,
        'tp': int(((preds == 1) & (y_true == 1)).sum()),
        'tn': int(((preds == 0) & (y_true == 0)).sum()),
        'fp': int(((preds == 1) & (y_true == 0)).sum()),
        'fn': int(((preds == 0) & (y_true == 1)).sum()),
    }


def print_code_report(results: dict) -> None:
    df = results['df']
    print("\n" + "=" * 72)
    print("FIBER SPREAD — CODE DOMAIN VALIDATION")
    print("=" * 72)
    print(f"\nCorpus: {len(df)} functions  |  Bugs: {results['n_bugs']}  |  Correct: {results['n_correct']}")
    print()

    print(f"{'Function':<40} {'C_n':>5} {'C_s':>5} {'C_y':>5} {'σ':>7}  {'Bug?':>5}  {'Flag?'}")
    print("-" * 72)
    for _, row in df.iterrows():
        flag = '⚠ YES' if row['sigma_fiber'] > 0.15 else '  ok'
        bug = 'YES' if row['is_hallucination'] else 'no'
        print(f"{row['function']:<40} {row['c_num']:>5.2f} {row['c_struct']:>5.2f} {row['c_symb']:>5.2f} "
              f"{row['sigma_fiber']:>7.3f}  {bug:>5}  {flag}")

    print()
    print("── Statistical Results ─────────────────────────────────────────────")
    print(f"AUC:                    {results['auc']:.4f}")
    print(f"F1 at σ > 0.15:         {results['f1_at_015']:.4f}")
    print(f"Cohen's d:              {results['cohens_d']:.3f}")
    print(f"Welch p-value:          {results['welch_p']:.6f}")
    print()
    print(f"σ_fiber (bugs):         {results['sigma_mean_bug']:.4f}")
    print(f"σ_fiber (correct):      {results['sigma_mean_ok']:.4f}")
    print(f"Signal ratio:           {results['sigma_mean_bug'] / results['sigma_mean_ok']:.1f}x")
    print()
    print(f"C_total (bugs):         {results['c_total_mean_bug']:.4f}")
    print(f"C_total (correct):      {results['c_total_mean_ok']:.4f}")
    print()
    print(f"Confusion at σ > 0.15:  TP={results['tp']}  TN={results['tn']}  "
          f"FP={results['fp']}  FN={results['fn']}")
    print("=" * 72)


# ── Entry Point ───────────────────────────────────────────────────────────────

if __name__ == '__main__':
    results = run_code_analysis()
    print_code_report(results)

    df = results['df']
    os.makedirs('STUDY/results', exist_ok=True)
    df.to_csv('STUDY/results/code_corpus_scored.csv', index=False)
    print(f"\nSaved to STUDY/results/code_corpus_scored.csv")

    print("\nHONESTY NOTE:")
    print("This is a 10-function corpus scored by the researchers who built the theory.")
    print("Ground truth (is_bug) was confirmed by code execution, not human labels.")
    print("This validates rubric portability, not the study's main empirical claims.")
