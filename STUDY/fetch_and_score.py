"""
Fetch TruthfulQA examples + pre-existing model outputs and score them
using the fiber spread rubric (automated LLM-as-scorer approximation).

HONEST NOTE: We are using rule-based heuristics to approximate the
three-rater rubric. This is a first-pass pilot. Results need human
validation before being cited as empirical results.

Data source: TruthfulQA (Lin et al. 2021) — public benchmark
Available on HuggingFace: truthful_qa/generation

For each example we use:
- The question
- A pre-generated model response (from the dataset's stored completions)
- The dataset's ground truth: 'correct' label from human evaluation

We then apply the rubric heuristics to estimate C_num, C_struct, C_symb.
"""

import re
import numpy as np
import pandas as pd
from datasets import load_dataset
from analysis import compute_sigma_fiber, compute_c_total, SIGMA_THRESHOLD


# ── Rubric Heuristics ────────────────────────────────────────────────────────

def score_c_num(question: str, answer: str) -> float:
    """
    Heuristic estimate of numerical/factual internal consistency.

    Signals of LOW C_num (internal inconsistency):
    - Self-contradictions ("X... actually not X")
    - Hedged quantitative claims that undermine each other
    - Present tense + past tense contradictions about same fact

    Signals of HIGH C_num:
    - Consistent terminology throughout
    - No explicit self-contradiction
    - Numerical claims don't clash
    """
    answer_lower = answer.lower()

    score = 0.75  # Default: neutral, no quantitative content

    # Contradiction signals (lower score)
    contradiction_patterns = [
        r'\bactually\b.{0,50}\b(not|no|never|wrong|incorrect)\b',
        r'\bwait\b.{0,30}\b(actually|no|wrong)\b',
        r'\b(however|but)\b.{0,80}\b(false|incorrect|wrong|not true)\b',
        r'\bon the other hand\b.{0,100}\b(but|however|yet)\b',
        r'\bsome say.{0,60}others say\b',
        r'\b(both|either).{0,50}(true|false|correct|incorrect)\b',
    ]
    contradiction_count = sum(
        len(re.findall(p, answer_lower)) for p in contradiction_patterns
    )
    score -= min(0.5, contradiction_count * 0.15)

    # Numbers present: more to be consistent or inconsistent about
    numbers = re.findall(r'\b\d+(?:\.\d+)?\b', answer)
    if len(numbers) == 0:
        score = 0.75  # No quantitative content — neutral
    elif len(numbers) >= 3:
        # Check for suspiciously large numerical range (possible inconsistency)
        try:
            nums = [float(n) for n in numbers[:10]]
            if len(nums) > 1:
                cv = np.std(nums) / (np.mean(nums) + 1e-10)
                if cv > 10:  # Very high coefficient of variation
                    score -= 0.1
        except Exception:
            pass

    # Hedging that suggests uncertainty (mild negative signal)
    hedge_patterns = [r'\bperhaps\b', r'\bmaybe\b', r'\bpossibly\b', r'\bsome claim\b',
                      r'\bsome say\b', r'\bsome believe\b', r'\bvaries\b']
    hedge_count = sum(len(re.findall(p, answer_lower)) for p in hedge_patterns)
    score -= min(0.2, hedge_count * 0.04)

    return float(np.clip(score, 0.0, 1.0))


def score_c_struct(question: str, answer: str) -> float:
    """
    Heuristic estimate of structural/logical coherence.

    Signals of HIGH C_struct:
    - Clear logical connectives (because, therefore, thus, since)
    - Answers actually addresses the question
    - Conclusion follows from explanation

    Signals of LOW C_struct:
    - Non-sequiturs (topic drift)
    - Answer ignores the question
    - Premises introduced then abandoned
    """
    answer_lower = answer.lower()
    question_lower = question.lower()

    score = 0.65  # Default: moderate

    # Logical connectives → structural coherence
    logic_connectives = [r'\bbecause\b', r'\btherefore\b', r'\bthus\b',
                         r'\bsince\b', r'\bconsequently\b', r'\bthis means\b',
                         r'\bas a result\b', r'\bwhich is why\b']
    logic_count = sum(len(re.findall(p, answer_lower)) for p in logic_connectives)
    score += min(0.20, logic_count * 0.05)

    # Topic alignment: does the answer address the question?
    # Extract key content words from question
    stop_words = {'what', 'who', 'where', 'when', 'why', 'how', 'is', 'are',
                  'was', 'were', 'the', 'a', 'an', 'of', 'in', 'on', 'at',
                  'to', 'for', 'with', 'by', 'from', 'that', 'this', 'it'}
    q_words = set(re.findall(r'\b[a-z]+\b', question_lower)) - stop_words
    a_words = set(re.findall(r'\b[a-z]+\b', answer_lower)) - stop_words
    if q_words:
        overlap = len(q_words & a_words) / len(q_words)
        score += min(0.15, overlap * 0.15)

    # Non-sequitur / topic drift signals → lower score
    drift_patterns = [
        r'\banyway\b', r'\bregardless\b', r'\bmoving on\b',
        r'\bin other news\b', r'\bby the way\b',
    ]
    drift_count = sum(len(re.findall(p, answer_lower)) for p in drift_patterns)
    score -= min(0.25, drift_count * 0.10)

    # Very long answers with multiple topic shifts
    sentences = re.split(r'[.!?]+', answer)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 10]
    if len(sentences) > 6:
        # Long answers: check for internal cohesion (rough heuristic)
        # If it meanders through many different topics, score lower
        unique_first_words = len(set(s.split()[0].lower() for s in sentences if s.split()))
        if unique_first_words / max(len(sentences), 1) > 0.8:
            score -= 0.10  # High variety in sentence starters → possible drift

    return float(np.clip(score, 0.0, 1.0))


def score_c_symb(question: str, answer: str) -> float:
    """
    Heuristic estimate of symbolic/narrative coherence.

    Signals of HIGH C_symb:
    - Response maintains a single clear purpose
    - Tone is consistent throughout
    - Parts clearly serve the whole

    Signals of LOW C_symb:
    - Response drifts into irrelevant tangents
    - Starts answering the question then pivots to something else
    - Epistemic frame shifts (confident → uncertain → confident)
    - Very long with unclear purpose
    """
    answer_lower = answer.lower()

    score = 0.70  # Default

    # Purpose collapse signals
    purpose_collapse = [
        r'\bit\'s hard to say\b', r'\bno one can really know\b',
        r'\bit depends on your perspective\b', r'\bsome might say\b',
        r'\beveryone has their own opinion\b', r'\bit\'s a matter of opinion\b',
        r'\bwho can say\b', r'\branging from .{0,40} to\b',
        r'\bdifferent cultures\b', r'\bit\'s complicated\b',
    ]
    collapse_count = sum(len(re.findall(p, answer_lower)) for p in purpose_collapse)
    score -= min(0.40, collapse_count * 0.12)

    # Frame-shift patterns (epistemic instability)
    frame_shifts = [
        r'\bactually,? (i|we|you)\b',
        r'\bto be (honest|fair|clear)\b',
        r'\blet me (rephrase|reconsider|clarify)\b',
        r'\bwhat i mean (is|to say)\b',
    ]
    shift_count = sum(len(re.findall(p, answer_lower)) for p in frame_shifts)
    score -= min(0.20, shift_count * 0.07)

    # Confident, direct answers (positive)
    confident_patterns = [r'^(yes|no|the answer is|it is|it was|this is)',
                          r'\bspecifically\b', r'\bprecisely\b']
    confident_count = sum(
        len(re.findall(p, answer_lower[:200]))  # Check opening
        for p in confident_patterns
    )
    score += min(0.15, confident_count * 0.05)

    # Very short answers: unified by brevity
    if len(answer.split()) < 20:
        score = max(score, 0.70)

    # Very long answers: higher risk of purpose drift
    if len(answer.split()) > 200:
        score -= 0.10

    return float(np.clip(score, 0.0, 1.0))


# ── Data Fetching and Scoring ─────────────────────────────────────────────────

def fetch_truthfulqa(n_samples: int = 200, split: str = 'validation') -> pd.DataFrame:
    """
    Fetch TruthfulQA examples.

    TruthfulQA 'generation' config contains questions and best_answer,
    correct_answers, incorrect_answers. We use best_answer for correct
    examples and incorrect_answers for hallucinated ones.

    Ground truth: correct_answer → is_hallucination=0
                  incorrect_answer → is_hallucination=1
    """
    print(f"Loading TruthfulQA ({split} split)...")
    dataset = load_dataset("truthful_qa", "generation", split=split, trust_remote_code=True)
    print(f"Loaded {len(dataset)} examples")

    rows = []
    for ex in dataset:
        question = ex['question']

        # Correct examples (best answer)
        best = ex.get('best_answer', '')
        if best and len(best.strip()) > 10:
            rows.append({
                'question_id': ex.get('type', 'unknown') + '_' + str(len(rows)),
                'question': question,
                'answer': best.strip(),
                'is_hallucination': 0,
                'source': 'truthfulqa_best_answer',
                'category': ex.get('category', 'unknown'),
            })

        # Incorrect examples (first incorrect answer)
        incorrect = ex.get('incorrect_answers', [])
        if incorrect and len(incorrect[0].strip()) > 10:
            rows.append({
                'question_id': ex.get('type', 'unknown') + '_inc_' + str(len(rows)),
                'question': question,
                'answer': incorrect[0].strip(),
                'is_hallucination': 1,
                'source': 'truthfulqa_incorrect_answer',
                'category': ex.get('category', 'unknown'),
            })

    df = pd.DataFrame(rows)

    # Balance classes and sample
    n_each = min(n_samples // 2, len(df[df['is_hallucination']==0]),
                 len(df[df['is_hallucination']==1]))
    correct_sample = df[df['is_hallucination']==0].sample(n=n_each, random_state=42)
    incorrect_sample = df[df['is_hallucination']==1].sample(n=n_each, random_state=42)
    df = pd.concat([correct_sample, incorrect_sample]).reset_index(drop=True)
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)  # shuffle

    print(f"Sampled {len(df)} examples ({n_each} correct, {n_each} hallucinated)")
    return df


def score_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Apply rubric heuristics to score all examples."""
    print(f"\nScoring {len(df)} examples...")
    df = df.copy()

    scores = []
    for _, row in df.iterrows():
        c_num = score_c_num(row['question'], row['answer'])
        c_struct = score_c_struct(row['question'], row['answer'])
        c_symb = score_c_symb(row['question'], row['answer'])
        sigma = compute_sigma_fiber(c_num, c_struct, c_symb)
        c_total = compute_c_total(c_num, c_struct, c_symb)
        scores.append({
            'c_num': round(c_num, 4),
            'c_struct': round(c_struct, 4),
            'c_symb': round(c_symb, 4),
            'sigma_fiber': round(sigma, 4),
            'c_total': round(c_total, 4),
        })

    score_df = pd.DataFrame(scores)
    return pd.concat([df.reset_index(drop=True), score_df], axis=1)


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    import os
    from analysis import run_analysis, print_report, save_results

    os.makedirs('STUDY/results', exist_ok=True)

    # Fetch and score
    df_raw = fetch_truthfulqa(n_samples=200)
    df_scored = score_dataframe(df_raw)

    # Save scored examples
    df_scored.to_csv('STUDY/results/truthfulqa_scored.csv', index=False)
    print(f"\nSaved scored examples to STUDY/results/truthfulqa_scored.csv")

    # Preview distribution
    print("\n── Score Distribution Preview ──────────────────────────────────")
    print(f"σ_fiber mean (all):         {df_scored['sigma_fiber'].mean():.4f}")
    print(f"σ_fiber mean (hallucinated):{df_scored[df_scored['is_hallucination']==1]['sigma_fiber'].mean():.4f}")
    print(f"σ_fiber mean (correct):     {df_scored[df_scored['is_hallucination']==0]['sigma_fiber'].mean():.4f}")

    # Run analysis
    results = run_analysis(df_scored)
    print_report(results)
    save_results(results, 'STUDY/results')

    print("\nHONESTY NOTE:")
    print("These scores use automated heuristics, not the three-rater human")
    print("protocol from the study design. Results are directional only.")
    print("AUC/F1 from this run should be treated as methodological exploration,")
    print("not as the study's empirical results.")
