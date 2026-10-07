"""Synthetic NumPy algebra checks; no model inference or attention measurement."""
import json
from pathlib import Path
import numpy as np

def softmax(x):
    y = np.exp(x - np.max(x))
    return y / y.sum()

z = np.array([2.0, -1.0, 0.4, 0.4], dtype=np.float64)
original = z.copy()
rows = []
for t in [0.5, 1.0, 1.5]:
    p = softmax(z / t)
    ratio = float(np.log(p[0] / p[1]))
    assert abs(ratio - (z[0] - z[1]) / t) < 1e-12
    assert np.array_equal(z, original)
    assert np.argmax(p) == np.argmax(z)
    assert abs(p.sum() - 1) < 1e-12
    assert np.max(np.abs(softmax((z + 17) / t) - p)) < 1e-12
    rows.append(dict(temperature=t, probabilities=p.tolist(), pair_log_probability_ratio=ratio))
# Distinguish output and attention softmaxes with an explicitly separate synthetic input.
attention_scores = np.array([1., -2., 0.5])
attention = softmax(attention_scores)
assert np.array_equal(attention, softmax(attention_scores))
# Cache max-error tolerances alone do not protect a near-tie top-token decision.
full = np.array([0., 1e-5])
cached = np.array([2e-5, 1e-5])
assert np.max(np.abs(full-cached)) < 1e-3
assert np.argmax(full) != np.argmax(cached)
result = dict(evidence_scope="synthetic algebra only; no transformer/cache execution", numpy_version=np.__version__, raw_logits=z.tolist(), rows=rows, synthetic_attention=attention.tolist(), near_tie=dict(max_error=float(np.max(np.abs(full-cached))), full_argmax=int(np.argmax(full)), cached_argmax=int(np.argmax(cached))), tolerance=1e-12)
Path(__file__).with_name("temperature_controls.json").write_text(json.dumps(result, indent=2)+"\n")
print(json.dumps(result, indent=2))
