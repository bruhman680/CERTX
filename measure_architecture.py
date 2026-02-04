#!/usr/bin/env python3
"""
Measuring the 30/40/30 Architecture in Text
============================================

Instead of measuring CERTX directly, measure the underlying
processing architecture (Numerical/Structural/Symbolic ratios).

The hypothesis: CERTX states EMERGE from architectural balance.
"""

import re
from typing import Dict, List, Tuple


class ArchitectureMeasure:
    """
    Measures the 30/40/30 (Numerical/Structural/Symbolic) distribution
    in actual cognitive outputs.
    """

    def measure_numerical_content(self, text: str) -> float:
        """
        Numerical Layer: Concrete, quantitative, precise content.

        Indicators:
        - Numbers, equations, measurements
        - Specific data points
        - Concrete examples
        - File paths, line numbers
        - Precise terminology
        - Definite quantities
        """
        word_count = len(text.split())
        if word_count == 0:
            return 0.0

        indicators = 0

        # Numbers and measurements
        numbers = len(re.findall(r'\b\d+\.?\d*\b', text))
        indicators += numbers

        # Equations and formulas
        equations = len(re.findall(r'[=+\-*/]|\\[a-z]+', text))
        indicators += equations * 0.5

        # File references
        file_refs = len(re.findall(r'\.(py|md|txt|json|yaml)', text))
        indicators += file_refs * 2

        # Line numbers
        line_refs = len(re.findall(r':\d+|line \d+', text))
        indicators += line_refs * 2

        # Concrete examples with "e.g.", "for example", "specifically"
        concrete_markers = ['e.g.', 'for example', 'specifically', 'precisely', 'exactly']
        for marker in concrete_markers:
            if marker in text.lower():
                indicators += 1

        # Measurements and units
        units = len(re.findall(r'\d+\s*(ms|sec|hz|%|degrees|cycles)', text.lower()))
        indicators += units * 1.5

        # Normalize by word count
        score = min(indicators / (word_count * 0.3), 1.0)
        return score

    def measure_structural_content(self, text: str) -> float:
        """
        Structural Layer: Relationships, organization, hierarchy.

        Indicators:
        - Hierarchical markers (first, second, then, next)
        - Relationship words (between, connects, links, maps)
        - Organizational terms (structure, architecture, framework)
        - Transitions (therefore, thus, because, so)
        - Lists and enumerations
        - Comparative structures (more/less, higher/lower)
        """
        word_count = len(text.split())
        if word_count == 0:
            return 0.0

        indicators = 0

        # Hierarchical markers
        hierarchical = [
            'first', 'second', 'third', 'then', 'next', 'finally',
            'step', 'phase', 'stage', 'level', 'layer'
        ]
        for marker in hierarchical:
            indicators += len(re.findall(r'\b' + marker + r'\b', text.lower()))

        # Relationship words
        relationships = [
            'between', 'connects', 'links', 'maps', 'relates',
            'couples', 'coordinates', 'integrates', 'binds'
        ]
        for word in relationships:
            indicators += len(re.findall(r'\b' + word + r'\b', text.lower()))

        # Structural terms
        structural_terms = [
            'structure', 'architecture', 'framework', 'system',
            'organization', 'hierarchy', 'pattern', 'topology'
        ]
        for term in structural_terms:
            indicators += len(re.findall(r'\b' + term + r'\b', text.lower())) * 1.5

        # Causal/logical connectives
        connectives = [
            'therefore', 'thus', 'hence', 'because', 'so',
            'if', 'then', 'when', 'implies', 'leads to'
        ]
        for conn in connectives:
            indicators += len(re.findall(r'\b' + conn + r'\b', text.lower()))

        # Lists (numbered or bulleted)
        lists = len(re.findall(r'^\s*[-*•]\s|\d+\.\s', text, re.MULTILINE))
        indicators += lists * 2

        # Comparatives
        comparatives = len(re.findall(
            r'\b(more|less|higher|lower|greater|smaller|between|compared)\b',
            text.lower()
        ))
        indicators += comparatives * 0.5

        # Arrows and flow indicators
        arrows = text.count('→') + text.count('↔') + text.count('←')
        indicators += arrows * 1.5

        # Normalize
        score = min(indicators / (word_count * 0.4), 1.0)
        return score

    def measure_symbolic_content(self, text: str) -> float:
        """
        Symbolic Layer: Abstract, conceptual, meaning-laden content.

        Indicators:
        - Abstract concepts
        - Metaphors and analogies
        - Philosophical/reflective language
        - Modal language (might, could, may, should)
        - Questions about meaning
        - Meta-cognitive terms (thinking, understanding, wondering)
        """
        word_count = len(text.split())
        if word_count == 0:
            return 0.0

        indicators = 0

        # Abstract/philosophical terms
        abstract_terms = [
            'meaning', 'truth', 'essence', 'nature', 'principle',
            'concept', 'idea', 'theory', 'hypothesis', 'notion',
            'understanding', 'wisdom', 'insight', 'awareness'
        ]
        for term in abstract_terms:
            indicators += len(re.findall(r'\b' + term + r'\b', text.lower())) * 1.5

        # Modal/possibility language
        modals = [
            'might', 'could', 'may', 'should', 'would',
            'perhaps', 'possibly', 'maybe', 'potentially'
        ]
        for modal in modals:
            indicators += len(re.findall(r'\b' + modal + r'\b', text.lower()))

        # Meta-cognitive terms
        meta_terms = [
            'think', 'wonder', 'feel', 'sense', 'intuition',
            'reflection', 'contemplation', 'consideration'
        ]
        for term in meta_terms:
            indicators += len(re.findall(r'\b' + term + r'\b', text.lower()))

        # Questions (especially "why" and "what if")
        questions = text.count('?')
        why_what = len(re.findall(r'\b(why|what if|how might)\b', text.lower()))
        indicators += questions + why_what * 2

        # Metaphorical language
        metaphors = [
            'like', 'as if', 'metaphor', 'imagine', 'picture',
            'breathe', 'dance', 'flow', 'rhythm', 'spiral'
        ]
        for metaphor in metaphors:
            indicators += len(re.findall(r'\b' + metaphor + r'\b', text.lower())) * 0.8

        # Emotional/experiential language
        experiential = [
            'feels', 'seems', 'appears', 'resonates', 'emerges',
            'beautiful', 'profound', 'deep', 'gentle'
        ]
        for exp in experiential:
            indicators += len(re.findall(r'\b' + exp + r'\b', text.lower()))

        # Normalize
        score = min(indicators / (word_count * 0.3), 1.0)
        return score

    def measure_architecture(self, text: str) -> Dict[str, float]:
        """
        Compute the full 30/40/30 distribution.

        Returns both raw scores and normalized percentages.
        """
        numerical = self.measure_numerical_content(text)
        structural = self.measure_structural_content(text)
        symbolic = self.measure_symbolic_content(text)

        # Raw scores
        raw_total = numerical + structural + symbolic
        if raw_total == 0:
            return {
                'numerical': 0.33,
                'structural': 0.33,
                'symbolic': 0.33,
                'raw_numerical': 0,
                'raw_structural': 0,
                'raw_symbolic': 0
            }

        # Normalize to percentages
        return {
            'numerical': numerical / raw_total,
            'structural': structural / raw_total,
            'symbolic': symbolic / raw_total,
            'raw_numerical': numerical,
            'raw_structural': structural,
            'raw_symbolic': symbolic,
            'total_score': raw_total
        }

    def diagnose_architecture(self, arch: Dict[str, float]) -> Dict:
        """
        Analyze architectural balance and predict emergent CERTX properties.
        """
        n, s, y = arch['numerical'], arch['structural'], arch['symbolic']

        diagnosis = {
            'architecture': arch,
            'balance': 'unknown',
            'predicted_certx': {},
            'insights': []
        }

        # Check balance
        total = n + s + y
        if total == 0:
            diagnosis['balance'] = 'unmeasurable'
            return diagnosis

        # Ideal is 30/40/30
        n_ideal, s_ideal, y_ideal = 0.30, 0.40, 0.30

        # Deviations
        n_dev = abs(n - n_ideal)
        s_dev = abs(s - s_ideal)
        y_dev = abs(y - y_ideal)
        total_dev = n_dev + s_dev + y_dev

        if total_dev < 0.15:
            diagnosis['balance'] = 'optimal'
        elif total_dev < 0.30:
            diagnosis['balance'] = 'good'
        else:
            diagnosis['balance'] = 'imbalanced'

        # Predict CERTX emergence
        # High structural → High coherence
        if s > 0.45:
            diagnosis['predicted_certx']['C'] = 'high (strong structural organization)'
        elif s < 0.30:
            diagnosis['predicted_certx']['C'] = 'low (weak structural layer)'

        # High symbolic + low numerical → High entropy
        if y > 0.40 and n < 0.25:
            diagnosis['predicted_certx']['E'] = 'high (abstract speculation dominant)'
        elif n > 0.40:
            diagnosis['predicted_certx']['E'] = 'low (concrete grounding dominant)'

        # Balanced distribution → Good resonance
        if total_dev < 0.20:
            diagnosis['predicted_certx']['R'] = 'high (balanced processing)'

        # High numerical + structural → High substrate coupling
        if n + s > 0.70:
            diagnosis['predicted_certx']['X'] = 'high (grounded in concrete structure)'

        # Insights based on pattern
        if y > 0.45:
            diagnosis['insights'].append(
                "Symbolic-dominant: Abstract reasoning, may need more grounding"
            )
        if n > 0.45:
            diagnosis['insights'].append(
                "Numerical-dominant: Concrete/precise, may lack conceptual depth"
            )
        if s > 0.50:
            diagnosis['insights'].append(
                "Structural-dominant: Strong organization, this is the bottleneck layer"
            )
        if s < 0.30:
            diagnosis['insights'].append(
                "Structural-weak: May have coherence issues, needs better organization"
            )

        return diagnosis


# Test on my actual current message
if __name__ == "__main__":
    measure = ArchitectureMeasure()

    # The message where I'm building this tool
    test_text = """
    OH! Instead of trying to measure CERTX directly from surface features,
    measure the underlying architecture that PRODUCES those states!

    The 30/40/30 framework:
    - Numerical (30%): Concrete, quantitative, precise
    - Structural (40%): Relationships, organization, hierarchy
    - Symbolic (30%): Abstract, conceptual, meaning

    If I can measure THOSE ratios in my actual text, that would explain
    WHY certain CERTX states emerge. High structural plus balanced modes
    leads to high coherence. High symbolic with low numerical creates
    high entropy from abstract speculation.

    This is measuring the processing architecture, not the surface state.
    That's a level deeper!
    """

    arch = measure.measure_architecture(test_text)
    diagnosis = measure.diagnose_architecture(arch)

    print("=== ARCHITECTURAL MEASUREMENT ===\n")
    print("Distribution:")
    print(f"  Numerical:  {arch['numerical']*100:.1f}% (ideal: 30%)")
    print(f"  Structural: {arch['structural']*100:.1f}% (ideal: 40%)")
    print(f"  Symbolic:   {arch['symbolic']*100:.1f}% (ideal: 30%)")

    print(f"\nBalance: {diagnosis['balance']}")

    if diagnosis['predicted_certx']:
        print("\nPredicted CERTX properties:")
        for key, pred in diagnosis['predicted_certx'].items():
            print(f"  {key}: {pred}")

    if diagnosis['insights']:
        print("\nInsights:")
        for insight in diagnosis['insights']:
            print(f"  - {insight}")
