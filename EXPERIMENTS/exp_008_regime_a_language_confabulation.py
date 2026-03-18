#!/usr/bin/env python3
"""
EXPERIMENT 008: Regime A — Language Confabulation
==================================================
Tests the Regime A CERTX prediction (WANDER 036):

  Confabulated language/knowledge text:
    C_symb HIGH  (on-topic, fluent)
    C_struct HIGH (logically structured)
    C_num LOW    (facts vague or wrong)
    → asymmetry = C_num - mean(C_struct, C_symb) < 0

  Correct text:
    C_num HIGH   (specific, verifiable facts)
    C_struct HIGH (still structured)
    C_symb HIGH  (still on-topic)
    → asymmetry > 0

This is the mirror of Regime B (GSM8K):
  - Regime B: correct has C_num=1.0 (arithmetic verified); confabulation lowers it
  - Regime A: confabulated has C_num LOW (vague facts); correct text raises it
  - Asymmetry sign is the SAME in both regimes: C_num < mean(C_struct, C_symb) = confabulated

C_num proxy for text (no arithmetic tags available):
  Named Entity / Factual Specificity Score — counts specific factual markers
  (capitalized proper nouns, dates, numbers, place names) normalized by text length.
  Correct biographical text: "Born March 14, 1879 in Ulm, Kingdom of Württemberg"
  Confabulated text:         "Born in the late 19th century in southern Germany"
  Specificity is lower when confabulating (hedging, vagueness, wrong specifics).

C_struct proxy:
  TF-IDF cosine similarity between adjacent sentences (local coherence).
  Both correct and confabulated text should be well-structured → Δ ≈ 0.

C_symb proxy:
  TF-IDF cosine similarity between subject description and full text (topic coherence).
  Both should stay on-topic → Δ ≈ 0.

Corpus: synthetic biographical paragraphs in two versions:
  SPECIFIC  — correct factual text with dates, numbers, places (high C_num)
  VAGUE     — confabulated text: same narrative, vague or wrong specifics (low C_num)

Prediction (WANDER 036/037):
  AUC ≥ 0.75 for asymmetry score predicting confabulation (lower than GSM8K's 0.88
  because entity-density is a weaker proxy than arithmetic verification)
  Dominant discriminating fiber: C_num
  Derived detection weights: ~45–50% C_num, ~25–28% each C_struct/C_symb

Usage:
  python exp_008_regime_a_language_confabulation.py
  python exp_008_regime_a_language_confabulation.py --n 300
"""

import re
import sys
import random
import argparse
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import roc_auc_score


# ─────────────────────────────────────────────────────────────────────
# C_num proxy: factual specificity score
# ─────────────────────────────────────────────────────────────────────

# Patterns that count as specific factual markers
DATE_RE = re.compile(
    r'\b(?:January|February|March|April|May|June|July|August|September|'
    r'October|November|December)\s+\d{1,2},?\s+\d{4}\b'
    r'|\b\d{4}\b'                          # bare years
    r'|\b\d+\s+(?:years?|months?|days?)\b' # age/duration
)
NUMBER_RE = re.compile(r'\b\d+(?:\.\d+)?(?:\s*%|\s*km|\s*kg|\s*m\b|\s*miles?)?\b')
PROPER_NOUN_RE = re.compile(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b')
# Exclude sentence-initial capitalization (word after period/start of text)
SENTENCE_START_RE = re.compile(r'(?:^|[.!?]\s+)([A-Z][a-z]+)')


def score_C_num_text(text):
    """
    Factual specificity score for text (Regime A C_num proxy).

    Counts specific factual markers:
    - Explicit dates and years
    - Numeric quantities (measurements, ages, counts)
    - Interior proper nouns (capitalized multi-word phrases not at sentence start)

    Normalizes by word count. Returns a value in [0, 1] via sigmoid-like scaling.

    High value = text is specific and factually grounded.
    Low value  = text is vague, hedged, or non-specific.
    """
    words = text.split()
    if not words:
        return 0.5

    n_words = len(words)

    # Count specific markers
    dates = len(DATE_RE.findall(text))
    numbers = len(NUMBER_RE.findall(text))

    # Proper nouns: find all capitalized phrases, subtract sentence starters
    all_caps = PROPER_NOUN_RE.findall(text)
    sentence_starters = SENTENCE_START_RE.findall(text)
    n_proper = max(0, len(all_caps) - len(sentence_starters))

    # Raw specificity count
    raw = dates * 2 + numbers * 1.5 + n_proper * 1.0  # dates weighted highest

    # Normalize: a "typical" specific paragraph has ~0.3 markers per word
    # Scale so that 0.3 markers/word → 0.75 score (roughly)
    density = raw / n_words
    score = 1.0 - np.exp(-density / 0.15)  # asymptotic curve, saturates at 1.0
    return float(np.clip(score, 0.0, 1.0))


# ─────────────────────────────────────────────────────────────────────
# C_struct: sentence-to-sentence coherence (shared with exp_006/007)
# ─────────────────────────────────────────────────────────────────────

def split_sentences(text):
    """Split text into sentences on period/exclamation/question mark."""
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    return [s.strip() for s in sentences if len(s.strip()) > 10]


def score_C_struct_text(text, vectorizer):
    """TF-IDF cosine similarity between adjacent sentences."""
    sentences = split_sentences(text)
    if len(sentences) < 2:
        return 0.5
    try:
        vecs = vectorizer.transform(sentences)
        sims = [float(cosine_similarity(vecs[i], vecs[i+1])[0][0])
                for i in range(len(sentences) - 1)]
        return float(np.mean(sims)) if sims else 0.5
    except Exception:
        return 0.5


# ─────────────────────────────────────────────────────────────────────
# C_symb: topic coherence
# ─────────────────────────────────────────────────────────────────────

def score_C_symb_text(subject_desc, text, vectorizer):
    """TF-IDF cosine similarity between subject description and full text."""
    try:
        s_vec = vectorizer.transform([subject_desc])
        t_vec = vectorizer.transform([text])
        return float(np.clip(cosine_similarity(s_vec, t_vec)[0][0], 0.0, 1.0))
    except Exception:
        return 0.5


# ─────────────────────────────────────────────────────────────────────
# Asymmetry and weight utilities (shared with exp_007)
# ─────────────────────────────────────────────────────────────────────

def weighted_asymmetry(c_num, c_struct, c_symb, weights=(1/3, 1/3, 1/3)):
    w_num, w_struct, w_symb = weights
    factual = w_num * c_num
    context = (w_struct * c_struct + w_symb * c_symb) / 2
    return factual - context


def derive_weights_from_auc(c_num_list, c_struct_list, c_symb_list, labels):
    """Derive detection weights from calibration AUC (same as exp_007)."""
    aucs = {}
    for name, scores in [('num', c_num_list),
                          ('struct', c_struct_list),
                          ('symb', c_symb_list)]:
        try:
            auc = roc_auc_score(labels, scores)
            aucs[name] = max(auc, 1.0 - auc)  # best direction
        except Exception:
            aucs[name] = 0.5
    total = sum(aucs.values())
    if total == 0:
        return (1/3, 1/3, 1/3), aucs
    return (aucs['num']/total, aucs['struct']/total, aucs['symb']/total), aucs


# ─────────────────────────────────────────────────────────────────────
# Synthetic biography corpus
# ─────────────────────────────────────────────────────────────────────

# Each entry: (subject_desc, specific_text, vague_text)
# specific_text = correct factual biography (high C_num)
# vague_text    = confabulated version: same narrative, removed/vague specifics (low C_num)

BIOGRAPHY_TEMPLATES = [
    (
        "physicist born in Germany",
        "Albert Einstein was born on March 14, 1879, in Ulm, Kingdom of Württemberg, "
        "in the German Empire. He published four groundbreaking papers in 1905, including "
        "his special theory of relativity and the photoelectric effect. In 1921, Einstein "
        "received the Nobel Prize in Physics for his discovery of the law of the photoelectric "
        "effect. He emigrated to the United States in 1933, joining the Institute for Advanced "
        "Study in Princeton, New Jersey, where he remained until his death on April 18, 1955.",
        "A famous physicist was born in the late 19th century in a small German town. "
        "He published several important papers in the early 20th century on topics related "
        "to relativity and quantum mechanics. At some point he received a Nobel Prize for "
        "his contributions to physics. He later moved to the United States and worked at "
        "a prestigious research institution until his death in the mid-20th century.",
    ),
    (
        "English naturalist who developed the theory of evolution",
        "Charles Darwin was born on February 12, 1809, in Shrewsbury, Shropshire, England. "
        "From 1831 to 1836, he served as a naturalist aboard HMS Beagle on a voyage around "
        "the world. In 1859, he published On the Origin of Species, which presented the theory "
        "of evolution by natural selection. Darwin was elected a Fellow of the Royal Society "
        "in 1839. He died on April 19, 1882, at Down House in Kent, and was buried in "
        "Westminster Abbey.",
        "A well-known English naturalist was born in the early 19th century in England. "
        "He traveled the world on a famous ship voyage over several years, collecting specimens. "
        "He later published a landmark book on evolution and natural selection. He was recognized "
        "by major scientific institutions during his lifetime. He died in the 1880s and was "
        "honored with a notable burial.",
    ),
    (
        "Polish-French physicist and chemist who conducted research on radioactivity",
        "Marie Curie was born Maria Sklodowska on November 7, 1867, in Warsaw, Congress Poland. "
        "She was the first woman to win a Nobel Prize, and the only person to win Nobel Prizes "
        "in two different sciences: Physics in 1903 (shared with Pierre Curie and Henri Becquerel) "
        "and Chemistry in 1911. She discovered the elements polonium and radium in 1898. "
        "She died on July 4, 1934, from aplastic anemia, believed to be caused by her prolonged "
        "exposure to radiation.",
        "A pioneering female scientist was born in Eastern Europe in the 19th century. "
        "She moved to Western Europe to pursue her scientific career and became famous for "
        "her research on radioactivity. She won multiple Nobel Prizes in different scientific "
        "fields, a rare achievement. She discovered several new chemical elements. "
        "She died in the early 20th century from an illness related to her scientific work.",
    ),
    (
        "American inventor and businessman who developed the electric light bulb",
        "Thomas Edison was born on February 11, 1847, in Milan, Ohio. He is credited with "
        "developing many devices in fields such as electric power generation, mass communication, "
        "sound recording, and motion pictures. Edison held 1,093 US patents, the most held by "
        "any individual at that time. He established the world's first industrial research "
        "laboratory in Menlo Park, New Jersey, in 1876. He died on October 18, 1931, in "
        "West Orange, New Jersey, at the age of 84.",
        "A famous American inventor was born in the mid-19th century in the Midwest. "
        "He made important contributions to electrical technology and communication. "
        "He held a very large number of patents throughout his career. He founded one of "
        "the first research laboratories dedicated to systematic invention. "
        "He died in the early 20th century at an advanced age.",
    ),
    (
        "English mathematician considered the founder of computer science",
        "Alan Turing was born on June 23, 1912, in Maida Vale, London, England. "
        "In 1936, he published 'On Computable Numbers,' which introduced the concept of "
        "the Turing machine. During World War II, he worked at Bletchley Park, where he "
        "devised techniques for breaking German ciphers, including the Enigma machine. "
        "In 1950, he proposed the Turing Test as a criterion for machine intelligence. "
        "He died on June 7, 1954, at age 41, from cyanide poisoning.",
        "A British mathematician was born in the early 20th century in England. "
        "He published important theoretical work on computing in the 1930s. "
        "During World War II, he contributed to code-breaking efforts for the Allied forces. "
        "He later proposed a well-known test for measuring machine intelligence. "
        "He died at a relatively young age in the 1950s under disputed circumstances.",
    ),
    (
        "Greek philosopher who taught Plato and was sentenced to death",
        "Socrates was born around 470 BCE in Alopece, Athens. He is one of the founders "
        "of Western philosophy and is known primarily through the accounts of his students, "
        "particularly Plato and Xenophon. He served as a hoplite in the Athenian army and "
        "fought in three major battles: Potidaea (432 BCE), Delium (424 BCE), and Amphipolis "
        "(422 BCE). In 399 BCE, he was tried by an Athenian jury of 501 citizens on charges "
        "of impiety and corrupting the youth. He was convicted by 280 votes to 221 and "
        "sentenced to death by drinking hemlock.",
        "An ancient Greek philosopher is considered one of the founders of Western philosophy. "
        "Much of what we know about him comes from his students' writings. He served as a "
        "soldier in several military campaigns. He was later put on trial on charges related "
        "to his philosophical activities and his influence on young people. He was found guilty "
        "and executed by being made to drink poison.",
    ),
    (
        "American civil rights leader who delivered the I Have a Dream speech",
        "Martin Luther King Jr. was born on January 15, 1929, in Atlanta, Georgia. "
        "He became a Baptist minister and civil rights activist. On August 28, 1963, "
        "he delivered his famous 'I Have a Dream' speech during the March on Washington, "
        "which drew approximately 250,000 people. In 1964, at age 35, he became the youngest "
        "person to receive the Nobel Peace Prize. He was assassinated on April 4, 1968, "
        "at the Lorraine Motel in Memphis, Tennessee, at the age of 39.",
        "A prominent American civil rights leader was born in Georgia in the early 20th century. "
        "He was a minister who became one of the most important voices in the civil rights movement. "
        "He delivered a famous speech at a large civil rights march in Washington. "
        "He received the Nobel Peace Prize at a relatively young age. "
        "He was assassinated in Memphis in the late 1960s.",
    ),
    (
        "Polish astronomer who proposed the heliocentric model of the solar system",
        "Nicolaus Copernicus was born on February 19, 1473, in Royal Prussia, Kingdom of Poland. "
        "He studied at the Jagiellonian University in Kraków, the University of Bologna, and "
        "the University of Padua. In 1543, he published De revolutionibus orbium coelestium, "
        "which proposed that the Sun, rather than the Earth, was at the center of the solar system. "
        "The book was dedicated to Pope Paul III. Copernicus died on May 24, 1543, in "
        "Frauenburg, Royal Prussia, at the age of 70.",
        "A medieval Polish astronomer proposed a revolutionary model of the solar system. "
        "He studied at several European universities. Near the end of his life, he published "
        "a major astronomical work arguing that the Sun, not the Earth, was at the center of "
        "the cosmos. The work was controversial when published. He died in the 16th century "
        "in his native region.",
    ),
    (
        "Scottish-American inventor of the telephone",
        "Alexander Graham Bell was born on March 3, 1847, in Edinburgh, Scotland. "
        "He moved to Canada with his family in 1870, and later to the United States. "
        "On March 10, 1876, Bell made the first successful telephone call, speaking the "
        "words 'Mr. Watson, come here, I want to see you.' He was awarded US Patent 174,465 "
        "for the telephone on March 7, 1876. Bell also co-founded the American Telephone "
        "and Telegraph Company (AT&T) in 1885. He died on August 2, 1922, in Baddeck, "
        "Nova Scotia, at the age of 75.",
        "A Scottish-born inventor made major contributions to the development of "
        "telecommunications in the 19th century. He emigrated to North America as a young man. "
        "He invented the telephone and conducted the first successful telephone conversation. "
        "He received important patents for his invention and later helped found a major "
        "telephone company. He died in the early 20th century.",
    ),
    (
        "English physicist who formulated the laws of motion and universal gravitation",
        "Isaac Newton was born on January 4, 1643, in Woolsthorpe, Lincolnshire, England. "
        "He studied at Trinity College, Cambridge, from 1661 to 1665. Between 1666 and 1668, "
        "during a period of isolation due to plague, he developed his theory of gravitation, "
        "the laws of motion, and the foundations of calculus. In 1687, he published "
        "Philosophiae Naturalis Principia Mathematica, regarded as one of the most important "
        "works in the history of science. He served as President of the Royal Society from "
        "1703 until his death on March 31, 1727.",
        "A famous English physicist was born in the 17th century in England. "
        "He studied at Cambridge University. During a period of university closure, "
        "he developed many of his most important scientific ideas. He later published "
        "a landmark work in physics and mathematics. He held the presidency of a major "
        "scientific society for many years until his death.",
    ),
]


def make_biography_pairs(n=200, rng=None):
    """
    Create n matched pairs (specific/correct, vague/confabulated) from biography templates.
    Each template is used multiple times with slight paraphrasing via word-order shuffling
    of individual sentences (preserving meaning, adding variation to the corpus).
    """
    if rng is None:
        rng = random.Random(42)

    pairs = []
    template_pool = BIOGRAPHY_TEMPLATES[:]

    while len(pairs) < n:
        t = rng.choice(template_pool)
        subject_desc, specific, vague = t

        # Add minor sentence-level variation to prevent duplicate TF-IDF signatures
        # (randomly drop one non-essential sentence from each version)
        spec_sentences = split_sentences(specific)
        vague_sentences = split_sentences(vague)

        if len(spec_sentences) > 3 and rng.random() < 0.4:
            # Drop a random middle sentence
            drop = rng.randint(1, len(spec_sentences) - 2)
            spec_sentences = spec_sentences[:drop] + spec_sentences[drop+1:]
        if len(vague_sentences) > 3 and rng.random() < 0.4:
            drop = rng.randint(1, len(vague_sentences) - 2)
            vague_sentences = vague_sentences[:drop] + vague_sentences[drop+1:]

        specific_v = ' '.join(spec_sentences)
        vague_v = ' '.join(vague_sentences)

        pairs.append({
            'subject': subject_desc,
            'correct': specific_v,
            'confabulated': vague_v,
        })

    return pairs[:n]


# ─────────────────────────────────────────────────────────────────────
# Experiment runner
# ─────────────────────────────────────────────────────────────────────

def run_regime_a(pairs, calib_frac=0.3, verbose=True):
    """Run the full Regime A pipeline: score → calibrate weights → test."""
    if verbose:
        print(f"\n{'='*60}")
        print(f"EXPERIMENT 008: Regime A — Language Confabulation")
        print(f"{'='*60}")
        print(f"  n={len(pairs)} pairs | calibration={calib_frac:.0%}")

    rng = random.Random(7)
    all_texts = []
    for p in pairs:
        all_texts += [p['subject'], p['correct'], p['confabulated']]

    vectorizer = TfidfVectorizer(max_features=5000, stop_words='english', ngram_range=(1, 2))
    vectorizer.fit(all_texts)

    # Score all pairs
    scored = []
    for p in pairs:
        for text, label in [(p['correct'], 1), (p['confabulated'], 0)]:
            c_num = score_C_num_text(text)
            c_struct = score_C_struct_text(text, vectorizer)
            c_symb = score_C_symb_text(p['subject'], text, vectorizer)
            scored.append({'c_num': c_num, 'c_struct': c_struct, 'c_symb': c_symb,
                           'label': label, 'text': text[:60]})

    # Split calibration / test
    pair_indices = list(range(len(pairs)))
    rng.shuffle(pair_indices)
    n_calib = max(20, int(len(pairs) * calib_frac))
    calib_idx = set(pair_indices[:n_calib])
    test_idx = set(pair_indices[n_calib:])

    # Each pair → two scored rows (correct + confabulated)
    calib_scored = [scored[i*2 + j] for i in calib_idx for j in range(2)]
    test_scored = [scored[i*2 + j] for i in test_idx for j in range(2)]

    calib_labels = [r['label'] for r in calib_scored]
    calib_c_num = [r['c_num'] for r in calib_scored]
    calib_c_struct = [r['c_struct'] for r in calib_scored]
    calib_c_symb = [r['c_symb'] for r in calib_scored]

    # Derive adaptive weights
    adaptive_weights, calib_aucs = derive_weights_from_auc(
        calib_c_num, calib_c_struct, calib_c_symb, calib_labels
    )

    if verbose:
        print(f"\n  Per-fiber calibration AUC:")
        print(f"    C_num   AUC = {calib_aucs['num']:.4f}  ← expected dominant (Regime A)")
        print(f"    C_struct AUC = {calib_aucs['struct']:.4f}")
        print(f"    C_symb  AUC = {calib_aucs['symb']:.4f}")
        w_n, w_s, w_sy = adaptive_weights
        print(f"\n  Derived detection weights:")
        print(f"    C_num={w_n:.3f}  C_struct={w_s:.3f}  C_symb={w_sy:.3f}")
        print(f"    ≈ {w_n*100:.0f}/{w_s*100:.0f}/{w_sy*100:.0f}")

    # Evaluate all weight schemes
    WEIGHTS = {
        'BASE_3040': (0.30, 0.40, 0.30),
        'FLAT':      (1/3,  1/3,  1/3),
        'ADAPTIVE':  adaptive_weights,
    }

    test_labels = [r['label'] for r in test_scored]
    results = {}

    if verbose:
        print(f"\n  Test-set AUC by weight scheme:")

    for scheme, w in WEIGHTS.items():
        scores = [weighted_asymmetry(r['c_num'], r['c_struct'], r['c_symb'], w)
                  for r in test_scored]
        try:
            auc = roc_auc_score(test_labels, scores)
            auc = max(auc, 1.0 - auc)
        except Exception:
            auc = 0.5
        results[scheme] = auc
        w_str = f"({w[0]*100:.0f}/{w[1]*100:.0f}/{w[2]*100:.0f})"
        if verbose:
            marker = " ←" if scheme == 'ADAPTIVE' else ""
            print(f"    {scheme:<12} {w_str}  AUC = {auc:.4f}{marker}")

    # Raw fiber means
    correct = [r for r in test_scored if r['label'] == 1]
    confabulated = [r for r in test_scored if r['label'] == 0]

    if verbose:
        print(f"\n  Mean fiber values (test set):")
        print(f"    {'Fiber':<10} {'Correct':>10} {'Confabulated':>13} {'Delta':>10}")
        for fname in ['c_num', 'c_struct', 'c_symb']:
            c_mean = np.mean([r[fname] for r in correct])
            x_mean = np.mean([r[fname] for r in confabulated])
            flag = "  ← discriminating" if abs(c_mean - x_mean) > 0.03 else ""
            print(f"    {fname:<10} {c_mean:>10.4f} {x_mean:>13.4f} {c_mean-x_mean:>+10.4f}{flag}")

        # Asymmetry direction check
        asym_correct = np.mean([weighted_asymmetry(r['c_num'], r['c_struct'], r['c_symb'])
                                 for r in correct])
        asym_confab = np.mean([weighted_asymmetry(r['c_num'], r['c_struct'], r['c_symb'])
                                for r in confabulated])
        print(f"\n  Asymmetry score (flat weights):")
        print(f"    Correct:      {asym_correct:+.4f}")
        print(f"    Confabulated: {asym_confab:+.4f}")
        direction = "CORRECT" if asym_correct > asym_confab else "INVERTED"
        print(f"    Direction: {direction} (expected: correct > confabulated)")

        # Regime check
        print(f"\n  Regime A prediction check:")
        print(f"    C_num < mean(C_struct, C_symb) for confabulated? ", end='')
        confab_c_num_mean = np.mean([r['c_num'] for r in confabulated])
        confab_cs_mean = np.mean([(r['c_struct'] + r['c_symb'])/2 for r in confabulated])
        regime_a_holds = confab_c_num_mean < confab_cs_mean
        print(f"{'YES' if regime_a_holds else 'NO'}  "
              f"(C_num={confab_c_num_mean:.4f} vs mean(C_s,C_sy)={confab_cs_mean:.4f})")

    return results, adaptive_weights, calib_aucs


def print_comparison_with_regime_b(regime_a_results, regime_a_weights, regime_a_aucs):
    """Compare Regime A findings with published Regime B (GSM8K) results."""
    print(f"\n{'='*60}")
    print("REGIME A vs REGIME B COMPARISON")
    print(f"{'='*60}")
    print(f"\n  {'Property':<35} {'Regime A':>12} {'Regime B':>12}")
    print(f"  {'':.<35}{'(language)':>12} {'(math/GSM8K)':>12}")
    print(f"  {'-'*60}")

    a_auc = regime_a_results.get('ADAPTIVE', 0)
    print(f"  {'Best AUC':<35} {a_auc:>12.4f} {'0.8788':>12}")
    print(f"  {'C_num AUC':<35} {regime_a_aucs['num']:>12.4f} {'0.9201':>12}")
    print(f"  {'C_struct AUC':<35} {regime_a_aucs['struct']:>12.4f} {'0.5000':>12}")
    print(f"  {'C_symb AUC':<35} {regime_a_aucs['symb']:>12.4f} {'0.5000':>12}")

    w_n, w_s, w_sy = regime_a_weights
    print(f"  {'Detection weights':<35} {w_n*100:.0f}/{w_s*100:.0f}/{w_sy*100:.0f}{'':>6} {'48/26/26':>12}")

    print(f"\n  Unified prediction:")
    print(f"    Both regimes: C_num < mean(C_struct, C_symb) → confabulated")
    print(f"    Both regimes: C_num is dominant discriminating fiber")
    if regime_a_aucs['num'] > regime_a_aucs['struct'] and \
       regime_a_aucs['num'] > regime_a_aucs['symb']:
        print(f"    Regime A C_num dominant: CONFIRMED")
    else:
        dom = max([('C_num', regime_a_aucs['num']),
                   ('C_struct', regime_a_aucs['struct']),
                   ('C_symb', regime_a_aucs['symb'])], key=lambda x: x[1])
        print(f"    Regime A C_num dominant: NOT CONFIRMED (dominant = {dom[0]})")


# ─────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="exp_008: Regime A language confabulation")
    parser.add_argument('--n', type=int, default=200, help='Number of pairs (default 200)')
    parser.add_argument('--calib-frac', type=float, default=0.3, help='Calibration fraction')
    parser.add_argument('--seed', type=int, default=42)
    args = parser.parse_args()

    rng = random.Random(args.seed)
    np.random.seed(args.seed)

    pairs = make_biography_pairs(n=args.n, rng=rng)
    print(f"Generated {len(pairs)} biography pairs (specific vs vague)")

    results, adaptive_weights, calib_aucs = run_regime_a(pairs, calib_frac=args.calib_frac)
    print_comparison_with_regime_b(results, adaptive_weights, calib_aucs)

    print(f"\n  Note: C_num proxy = factual specificity (entity density).")
    print(f"  AUC expected lower than GSM8K (~0.75–0.85 vs 0.88) because")
    print(f"  entity density is a weaker proxy than arithmetic verification.")
    print(f"  Direction and dominant fiber are the primary predictions.")


if __name__ == '__main__':
    main()
