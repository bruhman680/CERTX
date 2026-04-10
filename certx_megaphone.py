"""
CERTX Megaphone Controller
===========================

A minimal stability layer for CERTX state management.
It translates coherence, entropy, and resonance into a gain signal
and updates coherence with a slow, bounded adaptation rule.
"""

import math
from typing import Dict, List


def sigmoid(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-10.0 * x))


class MegaphoneController:
    def __init__(
        self,
        alpha: float = 0.1,
        coherence_center: float = 0.5,
        coherence_threshold: float = 0.15,
        damping_factor: float = 0.8,
        cooling_window: int = 3,
        cooling_gain: float = 1.3,
        eps: float = 1e-6,
    ):
        self.alpha = alpha
        self.coherence_center = coherence_center
        self.coherence_threshold = coherence_threshold
        self.damping_factor = damping_factor
        self.cooling_window = cooling_window
        self.cooling_gain = cooling_gain
        self.eps = eps
        self.gain_history: List[float] = []

    def step(self, coherence: float, entropy: float, resonance: float) -> Dict[str, float]:
        """Compute a single megaphone update step."""
        raw_gain = resonance / (entropy + self.eps)
        stability_factor = sigmoid(coherence - self.coherence_center)
        gain = raw_gain * stability_factor

        if abs(coherence - self.coherence_center) > self.coherence_threshold:
            gain *= self.damping_factor

        self.gain_history.append(gain)
        if len(self.gain_history) > self.cooling_window:
            self.gain_history.pop(0)

        cooling = self._needs_cooling()
        coherence_next = coherence + self.alpha * (gain - 1.0) * (1.0 - abs(coherence - self.coherence_center))
        coherence_next = max(0.0, min(1.0, coherence_next))

        return {
            'C_next': coherence_next,
            'G': gain,
            'raw_gain': raw_gain,
            'stability_factor': stability_factor,
            'cooling': cooling,
            'gain_history': list(self.gain_history),
        }

    def _needs_cooling(self) -> bool:
        if len(self.gain_history) < self.cooling_window:
            return False
        mean_gain = sum(self.gain_history) / len(self.gain_history)
        return mean_gain > self.cooling_gain


if __name__ == '__main__':
    controller = MegaphoneController()
    state = controller.step(coherence=0.52, entropy=0.48, resonance=0.75)
    print('Megaphone state:')
    for key, value in state.items():
        print(f'  {key}: {value}')
