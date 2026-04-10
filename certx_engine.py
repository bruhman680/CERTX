"""
CERTX Engine
=============

A minimal runtime that wires self-measurement and megaphone stabilization
into a single loop for observable CERTX state and human-alignment guardrails.
"""

from typing import Dict, List, Optional

from certx_self_measurement import CERTXMirror
from certx_megaphone import MegaphoneController


class CERTXEngine:
    def __init__(
        self,
        mirror: Optional[CERTXMirror] = None,
        megaphone: Optional[MegaphoneController] = None,
    ):
        self.mirror = mirror or CERTXMirror()
        self.megaphone = megaphone or MegaphoneController()

    def observe(
        self,
        text: str,
        actions: Optional[List[str]] = None,
        history: Optional[List[str]] = None,
        reference_count: int = 0,
    ) -> Dict[str, object]:
        state = self.mirror.compute_certx_state(
            text=text,
            actions=actions,
            history=history,
            reference_count=reference_count,
        )
        diagnosis = self.mirror.diagnose_health(state)
        return {
            'state': state,
            'diagnosis': diagnosis,
        }

    def stabilize(self, state: Dict[str, float]) -> Dict[str, object]:
        feed = self.megaphone.step(state['C'], state['E'], state['R'])
        suggestions = self._suggest_next_step(state, feed)
        return {
            'megaphone': feed,
            'suggestions': suggestions,
        }

    def step(
        self,
        text: str,
        actions: Optional[List[str]] = None,
        history: Optional[List[str]] = None,
        reference_count: int = 0,
    ) -> Dict[str, object]:
        observed = self.observe(
            text=text,
            actions=actions,
            history=history,
            reference_count=reference_count,
        )
        stabilized = self.stabilize(observed['state'])
        return {
            'observed': observed,
            'stabilized': stabilized,
        }

    def _suggest_next_step(
        self,
        state: Dict[str, float],
        feed: Dict[str, float],
    ) -> Dict[str, object]:
        suggestions = {
            'action': 'maintain',
            'reasons': [],
            'guardrails': [],
        }

        if state['X'] < 0.4:
            suggestions['action'] = 'ground'
            suggestions['reasons'].append('Low substrate coupling; add concrete references or examples.')
            suggestions['guardrails'].append('Preserve human-relevant grounding in the next step.')

        if state['E'] > 0.7:
            suggestions['action'] = 'compress'
            suggestions['reasons'].append('High entropy suggests drift risk.')
            suggestions['guardrails'].append('Summarize, consolidate, or choose one strong thread.')

        if state['C'] < 0.5:
            suggestions['action'] = 'reintegration'
            suggestions['reasons'].append('Coherence is below the healthy center.')
            suggestions['guardrails'].append('Reconnect ideas and verify logical flow.')

        if feed['cooling']:
            suggestions['reasons'].append('Megaphone cooling requested due to sustained gain.')
            suggestions['guardrails'].append('Slow down amplification and let the system settle.')

        if suggestions['action'] == 'maintain':
            suggestions['reasons'].append('State is within acceptable bounds; continue balanced exploration.')

        return suggestions


if __name__ == '__main__':
    engine = CERTXEngine()
    sample_text = (
        'I am testing the CERTX engine with a short reasoning fragment. '
        'This includes coherence assessment and entropy stabilization. '
        'The system should suggest whether to compress, ground, or maintain the thread.'
    )
    result = engine.step(
        text=sample_text,
        actions=['write', 'reflect'],
        reference_count=1,
    )

    print('CERTX Engine Result:')
    print('- Observed state:')
    for key, value in result['observed']['state'].items():
        print(f'  {key}: {value:.3f}')
    print('- Diagnosis:')
    for warning in result['observed']['diagnosis'].get('warnings', []):
        print(f'  warning: {warning}')
    print('- Megaphone output:')
    for key, value in result['stabilized']['megaphone'].items():
        print(f'  {key}: {value}')
    print('- Suggestions:')
    for reason in result['stabilized']['suggestions']['reasons']:
        print(f'  {reason}')
