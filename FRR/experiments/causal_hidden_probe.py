"""Paired hidden-state interventions in trained eight-state parity GRUs.

For each held-out trajectory we replace the GRU hidden state before a fixed
prediction step with the state obtained from a counterfactual prior-observation
history. The current observation is then held identical. Flip a relevant bit
(two steps back) versus an equally large irrelevant older-bit sham.
"""

import json
import torch
from hidden_representation_probe import train_predictor
from eight_state_nonlumpable_rnn import trajectories


@torch.no_grad()
def forward_from_prior(model, x, t):
    # Recompute hidden through t-1; feed exactly the same x_t in every arm.
    _, h = model.gru(x[:, :t])
    current_output, _ = model.gru(x[:, t:t+1], h)
    return model.head(current_output[:, 0]).flatten()


def trial(seed, nseq=2048, t=12):
    _, model = train_predictor(seed)
    x, _ = trajectories(nseq, 18, .1, torch.Generator().manual_seed(900000 + seed))
    relevant = x.clone()
    sham = x.clone()
    relevant[:, t-2] = 1 - relevant[:, t-2]
    sham[:, t-5] = 1 - sham[:, t-5]
    base_logits = forward_from_prior(model, x, t)
    relevant_logits = forward_from_prior(model, relevant, t)
    sham_logits = forward_from_prior(model, sham, t)
    base_decision = base_logits >= 0
    relevant_decision = relevant_logits >= 0
    sham_decision = sham_logits >= 0
    expected_parity = ((x[:, t] != x[:, t-1]) != x[:, t-2]).flatten()
    expected_relevant = ~expected_parity
    return {
        "seed": seed, "nseq": nseq, "t": t,
        "baseline_rule_accuracy": round((base_decision == expected_parity).float().mean().item(), 6),
        "relevant_edit_counterfactual_rule_accuracy": round((relevant_decision == expected_relevant).float().mean().item(), 6),
        "sham_edit_original_rule_accuracy": round((sham_decision == expected_parity).float().mean().item(), 6),
        "relevant_edit_prediction_flip_fraction": round((relevant_decision != base_decision).float().mean().item(), 6),
        "sham_edit_prediction_flip_fraction": round((sham_decision != base_decision).float().mean().item(), 6),
        "relevant_mean_absolute_logit_change": round((relevant_logits - base_logits).abs().mean().item(), 6),
        "sham_mean_absolute_logit_change": round((sham_logits - base_logits).abs().mean().item(), 6),
    }


if __name__ == "__main__":
    print(json.dumps({"results": [trial(seed) for seed in [7, 17, 29]],
                      "note": "Counterfactual hidden state via edited history, same current input; not neural-unit localization"}, indent=2))
