"""Exact eight-state Bayesian filter for the noisy parity / noisy sensor world.

The first three true bits are iid fair, matching robustness_observation.make_world.
Observations independently flip each true bit with probability sensor_error.
The state at t>=2 is (x_t,x_(t-1),x_(t-2)). Filtering uses no future data.
"""

import argparse
import itertools
import json

import numpy as np
import torch

from robustness_observation import make_world, train


STATES = list(itertools.product((0, 1), repeat=3))
INDEX = {s: i for i, s in enumerate(STATES)}


def transition_matrix(transition_error):
    P = np.zeros((8, 8), dtype=np.float64)
    for i, (a, b, c) in enumerate(STATES):
        parity = a ^ b ^ c
        for bit, probability in ((parity, 1-transition_error),
                                 (parity ^ 1, transition_error)):
            P[i, INDEX[(bit, a, b)]] += probability
    return P


def filtered_next_probabilities(observations, transition_error=.1, sensor_error=.1):
    """Return B×(T-2) P(x_(t+1)=1 | observations through t), t>=2."""
    observed = np.asarray(observations, dtype=np.float64)
    assert observed.ndim == 2 and observed.shape[1] >= 3
    assert np.all((observed == 0) | (observed == 1))
    B, T = observed.shape
    P = transition_matrix(transition_error)
    prior = np.full((B, 8), 1/8, dtype=np.float64)
    # Prior on (x2,x1,x0) is uniform; assimilate the first 3 observations.
    for obs_t, state_axis in ((0, 2), (1, 1), (2, 0)):
        latent_bit = np.array([s[state_axis] for s in STATES])[None, :]
        likelihood = np.where(observed[:, obs_t:obs_t+1] == latent_bit,
                              1-sensor_error, sensor_error)
        prior *= likelihood
        prior /= prior.sum(axis=1, keepdims=True)
    next_bit_one = np.array([s[0] for s in STATES], dtype=float)
    next_true_prob = P @ next_bit_one
    result = np.empty((B, T-2), dtype=np.float64)
    for t in range(2, T):
        result[:, t-2] = prior @ next_true_prob
        if t+1 < T:
            predicted_state = prior @ P
            latent_bit = np.array([s[0] for s in STATES])[None, :]
            likelihood = np.where(observed[:, t+1:t+2] == latent_bit,
                                  1-sensor_error, sensor_error)
            prior = predicted_state * likelihood
            prior /= prior.sum(axis=1, keepdims=True)
    return result


def logloss(prob, y):
    p = np.clip(prob, 1e-12, 1-1e-12)
    return float(-(y*np.log(p) + (1-y)*np.log(1-p)).mean())


def evaluate(seed=7, sensor_error=.1, train_steps=350, test_sequences=2048, length=24):
    generator = torch.Generator().manual_seed(990000 + seed + int(1000*sensor_error))
    x, y = make_world(test_sequences, length, .1, sensor_error, generator)
    observed = x.squeeze(-1).numpy()
    target = y[:, 2:, 0].numpy()
    bayes = filtered_next_probabilities(observed, .1, sensor_error)
    bayes_acc = float(((bayes >= .5) == target).mean())
    model = train(seed, sensor_error, train_steps)
    with torch.no_grad():
        logits = model(x)[:, 2:, 0]
        gru_prob = torch.sigmoid(logits).numpy()
    gru_acc = float(((gru_prob >= .5) == target).mean())
    return {"seed": seed, "sensor_error": sensor_error,
            "bayes_accuracy": round(bayes_acc, 6),
            "bayes_logloss": round(logloss(bayes, target), 6),
            "gru_accuracy": round(gru_acc, 6),
            "gru_logloss": round(logloss(gru_prob, target), 6),
            "test_sequences": test_sequences, "evaluated_tokens": target.size}


def validate():
    P = transition_matrix(.1)
    assert np.allclose(P.sum(axis=1), 1)
    assert np.allclose(P.sum(axis=0), 1)
    # Clear observations reveal the three-bit state exactly; next-event
    # probability is .1 or .9 according to parity.
    bits = np.array([[0, 0, 0], [0, 1, 1], [1, 0, 0], [1, 1, 1]], dtype=float)
    expected = np.array([.1, .1, .9, .9])
    assert np.allclose(filtered_next_probabilities(bits, .1, 0)[:, 0], expected)
    # With completely uninformative sensor, forecasts are 1/2 under the
    # stationary uniform prior, independent of observation string.
    observations = np.zeros((4, 9))
    assert np.allclose(filtered_next_probabilities(observations, .1, .5), .5)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument('--steps', type=int, default=350)
    p.add_argument('--sensor-error', type=float, default=.1)
    p.add_argument('--seeds', type=int, nargs='+', default=[7,17,29])
    args = p.parse_args()
    validate()
    results = [evaluate(s, args.sensor_error, args.steps) for s in args.seeds]
    print(json.dumps({"validation": "passed", "results": results,
                      "scope": "Exact Bayesian filter under known model/sensor parameters; matched synthetic held-out streams"}, indent=2))
