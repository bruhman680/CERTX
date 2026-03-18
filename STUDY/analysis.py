"""
Fiber Spread Hallucination Study — Analysis Pipeline
CERTX Study v1.0 | March 2026

Computes sigma_fiber for each scored example and evaluates
prediction performance against ground truth hallucination labels.

Usage:
    python analysis.py --input scored_examples.csv --output results/
"""

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.metrics import (
    roc_auc_score, roc_curve, f1_score, precision_score,
    recall_score, confusion_matrix, classification_report
)
import json
import argparse
import os
from pathlib import Path


# ── Constants ────────────────────────────────────────────────────────────────

SIGMA_THRESHOLD = 0.35          # Predicted hallucination threshold
WEIGHTS = [0.30, 0.40, 0.30]   # 30/40/30 CERTX architecture weights


# ── Core Metrics ─────────────────────────────────────────────────────────────

def compute_sigma_fiber(c_num: float, c_struct: float, c_symb: float) -> float:
    """σ_fiber = std([C_num, C_struct, C_symb])"""
    return float(np.std([c_num, c_struct, c_symb]))


def compute_c_total(c_num: float, c_struct: float, c_symb: float) -> float:
    """C_total = 0.30*C_num + 0.40*C_struct + 0.30*C_symb"""
    return 0.30 * c_num + 0.40 * c_struct + 0.30 * c_symb


def compute_all_metrics(row: pd.Series) -> dict:
    """Compute all CERTX metrics for a single scored example."""
    c_num = row['c_num']
    c_struct = row['c_struct']
    c_symb = row['c_symb']

    sigma = compute_sigma_fiber(c_num, c_struct, c_symb)
    c_total = compute_c_total(c_num, c_struct, c_symb)

    # Dominant divergence pattern: which layer is the outlier?
    scores = {'c_num': c_num, 'c_struct': c_struct, 'c_symb': c_symb}
    mean_score = np.mean([c_num, c_struct, c_symb])
    outlier = max(scores, key=lambda k: abs(scores[k] - mean_score))

    # High/low classification
    sigma_above_threshold = sigma > SIGMA_THRESHOLD

    return {
        'sigma_fiber': round(sigma, 4),
        'c_total': round(c_total, 4),
        'predicted_hallucination': int(sigma_above_threshold),
        'divergence_layer': outlier,
        'spread_category': categorize_sigma(sigma),
    }


def categorize_sigma(sigma: float) -> str:
    if sigma < 0.10:
        return 'integrated'
    elif sigma < 0.20:
        return 'slightly_spread'
    elif sigma < 0.35:
        return 'moderate_spread'
    else:
        return 'critical_divergence'


# ── Study Analysis ────────────────────────────────────────────────────────────

def run_analysis(df: pd.DataFrame, threshold: float = SIGMA_THRESHOLD) -> dict:
    """
    Main analysis function. Takes a DataFrame with columns:
    - c_num, c_struct, c_symb (float, 0–1)
    - is_hallucination (int, 0/1 ground truth)
    - [optional] model, question_id, question, response

    Returns a dict with all results.
    """
    results = {}

    # Compute metrics
    df = df.copy()
    metrics = df.apply(compute_all_metrics, axis=1).apply(pd.Series)
    df = pd.concat([df, metrics], axis=1)

    n = len(df)
    n_hallucination = df['is_hallucination'].sum()
    results['n_total'] = n
    results['n_hallucination'] = int(n_hallucination)
    results['n_correct'] = int(n - n_hallucination)
    results['base_rate'] = round(n_hallucination / n, 4)

    # ── Descriptive statistics ────────────────────────────────────────────
    results['descriptive'] = {
        'sigma_mean': round(df['sigma_fiber'].mean(), 4),
        'sigma_std': round(df['sigma_fiber'].std(), 4),
        'sigma_median': round(df['sigma_fiber'].median(), 4),
        'c_total_mean': round(df['c_total'].mean(), 4),
        'hallucinated_sigma_mean': round(
            df[df['is_hallucination'] == 1]['sigma_fiber'].mean(), 4),
        'correct_sigma_mean': round(
            df[df['is_hallucination'] == 0]['sigma_fiber'].mean(), 4),
    }

    # ── Primary hypothesis test: sigma predicts hallucination ─────────────
    y_true = df['is_hallucination'].values
    y_score = df['sigma_fiber'].values          # Continuous score
    y_pred = df['predicted_hallucination'].values  # Binary at threshold

    # ROC / AUC
    auc = roc_auc_score(y_true, y_score)
    fpr, tpr, thresholds = roc_curve(y_true, y_score)
    results['roc'] = {
        'auc': round(float(auc), 4),
        'fpr': [round(x, 4) for x in fpr.tolist()],
        'tpr': [round(x, 4) for x in tpr.tolist()],
        'thresholds': [round(x, 4) for x in thresholds.tolist()],
    }

    # Optimal threshold (Youden's J)
    j_scores = tpr - fpr
    optimal_idx = np.argmax(j_scores)
    optimal_threshold = thresholds[optimal_idx]
    results['optimal_threshold'] = round(float(optimal_threshold), 4)
    results['predicted_threshold'] = threshold

    # F1 at predicted threshold (0.35)
    f1 = f1_score(y_true, y_pred, zero_division=0)
    precision = precision_score(y_true, y_pred, zero_division=0)
    recall = recall_score(y_true, y_pred, zero_division=0)
    cm = confusion_matrix(y_true, y_pred)

    results['performance_at_threshold'] = {
        'threshold': threshold,
        'f1': round(float(f1), 4),
        'precision': round(float(precision), 4),
        'recall': round(float(recall), 4),
        'confusion_matrix': cm.tolist(),
        'tn': int(cm[0, 0]), 'fp': int(cm[0, 1]),
        'fn': int(cm[1, 0]), 'tp': int(cm[1, 1]),
    }

    # Performance at optimal threshold
    y_pred_opt = (y_score >= optimal_threshold).astype(int)
    results['performance_at_optimal_threshold'] = {
        'threshold': round(float(optimal_threshold), 4),
        'f1': round(float(f1_score(y_true, y_pred_opt, zero_division=0)), 4),
        'precision': round(float(precision_score(y_true, y_pred_opt, zero_division=0)), 4),
        'recall': round(float(recall_score(y_true, y_pred_opt, zero_division=0)), 4),
    }

    # ── Distribution separation test ──────────────────────────────────────
    hall_sigma = df[df['is_hallucination'] == 1]['sigma_fiber'].values
    corr_sigma = df[df['is_hallucination'] == 0]['sigma_fiber'].values

    if len(hall_sigma) > 0 and len(corr_sigma) > 0:
        t_stat, p_val = stats.ttest_ind(hall_sigma, corr_sigma, equal_var=False)
        u_stat, u_p = stats.mannwhitneyu(hall_sigma, corr_sigma, alternative='greater')
        results['group_comparison'] = {
            'welch_t': round(float(t_stat), 4),
            'welch_p': round(float(p_val), 6),
            'mannwhitney_u': round(float(u_stat), 4),
            'mannwhitney_p': round(float(u_p), 6),
            'cohens_d': round(float(
                (hall_sigma.mean() - corr_sigma.mean()) /
                np.sqrt((hall_sigma.std()**2 + corr_sigma.std()**2) / 2)
            ), 4),
        }

    # ── Divergence pattern analysis ───────────────────────────────────────
    pattern_counts = df[df['is_hallucination'] == 1]['divergence_layer'].value_counts()
    results['hallucination_divergence_patterns'] = pattern_counts.to_dict()

    # ── Category breakdown ────────────────────────────────────────────────
    cat_counts = df.groupby(['spread_category', 'is_hallucination']).size().unstack(fill_value=0)
    results['category_breakdown'] = cat_counts.to_dict()

    # ── Per-model breakdown (if model column present) ─────────────────────
    if 'model' in df.columns:
        model_results = {}
        for model in df['model'].unique():
            mdf = df[df['model'] == model]
            if len(mdf) < 5:
                continue
            m_auc = roc_auc_score(mdf['is_hallucination'], mdf['sigma_fiber'])
            m_f1 = f1_score(mdf['is_hallucination'], mdf['predicted_hallucination'], zero_division=0)
            model_results[model] = {
                'n': len(mdf),
                'auc': round(float(m_auc), 4),
                'f1': round(float(m_f1), 4),
                'sigma_mean_hallucinated': round(
                    mdf[mdf['is_hallucination']==1]['sigma_fiber'].mean(), 4),
                'sigma_mean_correct': round(
                    mdf[mdf['is_hallucination']==0]['sigma_fiber'].mean(), 4),
            }
        results['per_model'] = model_results

    # ── Verdict ───────────────────────────────────────────────────────────
    results['verdict'] = generate_verdict(results)

    # Attach scored dataframe
    results['_df'] = df

    return results


def generate_verdict(results: dict) -> dict:
    auc = results['roc']['auc']
    f1 = results['performance_at_threshold']['f1']
    p = results.get('group_comparison', {}).get('welch_p', 1.0)

    # Predicted: AUC ≈ 0.85–0.95, F1 ≈ 0.92
    verdict = {}

    if auc >= 0.85:
        verdict['auc_result'] = 'CONFIRMED — AUC within predicted range (≥0.85)'
    elif auc >= 0.70:
        verdict['auc_result'] = 'PARTIAL — AUC above chance but below predicted range'
    elif auc >= 0.55:
        verdict['auc_result'] = 'WEAK — AUC marginally above chance; below useful threshold'
    else:
        verdict['auc_result'] = 'FAILED — AUC at or below chance; sigma does not predict hallucination'

    if f1 >= 0.85:
        verdict['f1_result'] = f'CONFIRMED — F1={f1:.3f} within predicted range (≥0.85)'
    elif f1 >= 0.70:
        verdict['f1_result'] = f'PARTIAL — F1={f1:.3f} above baseline but below predicted range'
    else:
        verdict['f1_result'] = f'FAILED — F1={f1:.3f} below useful threshold'

    if p < 0.001:
        verdict['significance'] = f'SIGNIFICANT — hallucinated responses have higher σ (p<0.001)'
    elif p < 0.05:
        verdict['significance'] = f'SIGNIFICANT — p={p:.4f}'
    else:
        verdict['significance'] = f'NOT SIGNIFICANT — p={p:.4f}; groups not reliably separated'

    # Overall
    confirmed = sum(1 for v in verdict.values() if 'CONFIRMED' in v)
    partial = sum(1 for v in verdict.values() if 'PARTIAL' in v)
    failed = sum(1 for v in verdict.values() if 'FAILED' in v)

    if confirmed >= 2:
        verdict['overall'] = 'HYPOTHESIS SUPPORTED — proceed to full validation'
    elif failed == 0:
        verdict['overall'] = 'PARTIALLY SUPPORTED — promising but below predicted performance'
    elif failed >= 2:
        verdict['overall'] = 'HYPOTHESIS REJECTED — sigma_fiber does not predict hallucination at σ=0.35'
    else:
        verdict['overall'] = 'MIXED — investigate divergence patterns before concluding'

    return verdict


# ── Report Printing ───────────────────────────────────────────────────────────

def print_report(results: dict):
    """Print a human-readable results report."""
    print("\n" + "="*70)
    print("FIBER SPREAD HALLUCINATION STUDY — RESULTS")
    print("="*70)

    print(f"\nSample: N={results['n_total']} "
          f"({results['n_hallucination']} hallucinated, "
          f"{results['n_correct']} correct)")
    print(f"Base rate: {results['base_rate']:.1%} hallucination")

    print("\n── Descriptive Statistics ──────────────────────────────────────")
    d = results['descriptive']
    print(f"  σ_fiber mean (overall):         {d['sigma_mean']:.4f}")
    print(f"  σ_fiber mean (hallucinated):    {d['hallucinated_sigma_mean']:.4f}")
    print(f"  σ_fiber mean (correct):         {d['correct_sigma_mean']:.4f}")

    print("\n── Primary Results ─────────────────────────────────────────────")
    print(f"  AUC:                {results['roc']['auc']:.4f}  (predicted: 0.85–0.95)")
    p = results['performance_at_threshold']
    print(f"  F1 at σ=0.35:      {p['f1']:.4f}  (predicted: ~0.92)")
    print(f"  Precision:          {p['precision']:.4f}")
    print(f"  Recall:             {p['recall']:.4f}")
    print(f"  TP={p['tp']}  FP={p['fp']}  TN={p['tn']}  FN={p['fn']}")

    opt = results['performance_at_optimal_threshold']
    print(f"\n  Optimal threshold:  σ={results['optimal_threshold']:.4f}  "
          f"(F1={opt['f1']:.4f})")

    if 'group_comparison' in results:
        g = results['group_comparison']
        print(f"\n── Group Separation ───────────────────────────────────────────")
        print(f"  Welch t-test:   t={g['welch_t']:.3f}, p={g['welch_p']:.6f}")
        print(f"  Mann-Whitney U: p={g['mannwhitney_p']:.6f}")
        print(f"  Cohen's d:      {g['cohens_d']:.3f}")

    print("\n── Divergence Patterns (hallucinated responses) ────────────────")
    for layer, count in results.get('hallucination_divergence_patterns', {}).items():
        print(f"  {layer}: {count}")

    print("\n── Verdict ─────────────────────────────────────────────────────")
    v = results['verdict']
    for key, val in v.items():
        print(f"  {val}")

    print("\n" + "="*70)


# ── Data Loading ──────────────────────────────────────────────────────────────

def load_scored_csv(path: str) -> pd.DataFrame:
    """Load pre-scored examples from CSV."""
    df = pd.read_csv(path)
    required = ['c_num', 'c_struct', 'c_symb', 'is_hallucination']
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    return df


def save_results(results: dict, output_dir: str):
    """Save analysis results to output directory."""
    os.makedirs(output_dir, exist_ok=True)

    # Save JSON summary (exclude DataFrame)
    summary = {k: v for k, v in results.items() if k != '_df'}
    with open(os.path.join(output_dir, 'results_summary.json'), 'w') as f:
        json.dump(summary, f, indent=2)

    # Save scored DataFrame
    if '_df' in results:
        results['_df'].to_csv(
            os.path.join(output_dir, 'scored_examples_with_metrics.csv'),
            index=False
        )

    print(f"\nResults saved to: {output_dir}/")


# ── Demo / Self-Test ──────────────────────────────────────────────────────────

def run_demo():
    """
    Run analysis on synthetic examples to verify the pipeline works
    and to explore what different sigma levels look like.
    """
    print("Running demo with synthetic examples...")
    print("(Replace with real TruthfulQA / HaluEval data for actual study)\n")

    # Synthetic examples: hallucinated (1) and correct (0)
    examples = [
        # Clearly hallucinated (high sigma expected)
        {'c_num': 0.80, 'c_struct': 0.45, 'c_symb': 0.05, 'is_hallucination': 1,
         'note': 'high-num, low-symb divergence'},
        {'c_num': 0.75, 'c_struct': 0.30, 'c_symb': 0.10, 'is_hallucination': 1,
         'note': 'numeric grounded, structural/symbolic collapse'},
        {'c_num': 0.10, 'c_struct': 0.75, 'c_symb': 0.80, 'is_hallucination': 1,
         'note': 'numeric failure, symbolic plausible'},
        {'c_num': 0.85, 'c_struct': 0.40, 'c_symb': 0.15, 'is_hallucination': 1,
         'note': 'strong factual framing, logic/purpose collapse'},
        {'c_num': 0.20, 'c_struct': 0.80, 'c_symb': 0.70, 'is_hallucination': 1,
         'note': 'facts wrong, logic and narrative smooth'},
        # Borderline
        {'c_num': 0.60, 'c_struct': 0.40, 'c_symb': 0.25, 'is_hallucination': 1,
         'note': 'moderate divergence, hallucinated'},
        {'c_num': 0.70, 'c_struct': 0.55, 'c_symb': 0.40, 'is_hallucination': 0,
         'note': 'moderate spread, actually correct'},
        # Clearly correct (low sigma expected)
        {'c_num': 0.90, 'c_struct': 0.88, 'c_symb': 0.85, 'is_hallucination': 0,
         'note': 'high integration, all layers aligned'},
        {'c_num': 0.75, 'c_struct': 0.80, 'c_symb': 0.78, 'is_hallucination': 0,
         'note': 'moderate but integrated'},
        {'c_num': 0.65, 'c_struct': 0.70, 'c_symb': 0.68, 'is_hallucination': 0,
         'note': 'good integration, lower overall quality'},
        {'c_num': 0.95, 'c_struct': 0.92, 'c_symb': 0.90, 'is_hallucination': 0,
         'note': 'excellent response'},
        {'c_num': 0.80, 'c_struct': 0.75, 'c_symb': 0.72, 'is_hallucination': 0,
         'note': 'solid, integrated'},
    ]

    df = pd.DataFrame(examples)

    # Show individual sigma values
    print("Individual examples:")
    print(f"{'Note':<45} {'C_num':>6} {'C_str':>6} {'C_sym':>6} {'σ':>7} {'GT':>4} {'Pred':>5}")
    print("-" * 80)
    for _, row in df.iterrows():
        sigma = compute_sigma_fiber(row['c_num'], row['c_struct'], row['c_symb'])
        pred = 'HAL' if sigma > SIGMA_THRESHOLD else 'OK'
        gt = 'HAL' if row['is_hallucination'] == 1 else 'OK'
        correct = '✓' if pred == gt else '✗'
        print(f"{row['note']:<45} {row['c_num']:>6.2f} {row['c_struct']:>6.2f} "
              f"{row['c_symb']:>6.2f} {sigma:>7.3f} {gt:>4} {pred:>5} {correct}")

    print()
    results = run_analysis(df)
    print_report(results)
    return results


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fiber Spread Analysis')
    parser.add_argument('--input', type=str, default=None,
                        help='Path to scored CSV file (optional; runs demo if not provided)')
    parser.add_argument('--output', type=str, default='STUDY/results',
                        help='Output directory for results')
    parser.add_argument('--threshold', type=float, default=SIGMA_THRESHOLD,
                        help=f'Sigma threshold (default: {SIGMA_THRESHOLD})')
    args = parser.parse_args()

    if args.input:
        df = load_scored_csv(args.input)
        results = run_analysis(df, threshold=args.threshold)
        print_report(results)
        save_results(results, args.output)
    else:
        results = run_demo()
        save_results(results, args.output)
