"""A controlled eight-microstate test of observable-history information.

The microstate is (current_bit, previous_bit, spare_bit). The observed bit is
current_bit; its next value is current_bit XOR previous_bit. The spare bit is
unobserved and has no causal role in this constructed transition. Every
microstate is given equal weight. No claim about natural cognition is implied.
"""

import json
import itertools

import torch


def experiment(seed=7, epochs=1000):
    torch.manual_seed(seed)
    torch.set_num_threads(2)
    states = torch.tensor(list(itertools.product((0., 1.), repeat=3)))
    current = states[:, :1]
    history = states[:, :2]
    target = (states[:, :1] != states[:, 1:2]).float()

    def train(features):
        model = torch.nn.Sequential(
            torch.nn.Linear(features.shape[1], 16),
            torch.nn.Tanh(),
            torch.nn.Linear(16, 1),
        )
        optimizer = torch.optim.Adam(model.parameters(), lr=0.04)
        criterion = torch.nn.BCEWithLogitsLoss()
        for _ in range(epochs):
            optimizer.zero_grad()
            loss = criterion(model(features), target)
            loss.backward()
            optimizer.step()
        with torch.no_grad():
            probabilities = torch.sigmoid(model(features)).flatten()
            predictions = (probabilities >= .5).float()
            accuracy = (predictions == target.flatten()).float().mean().item()
            return {"accuracy": accuracy, "loss": criterion(model(features), target).item(),
                    "probabilities": [round(v, 4) for v in probabilities.tolist()]}

    without_history = train(current)
    with_history = train(history)
    # Exact conditional distributions on the exhaustive, uniformly weighted toy.
    # Each visible current bit has two equally likely hidden previous bits.
    return {"seed": seed, "microstates": 8, "observed_current_only": without_history,
            "observed_current_and_previous": with_history,
            "bayes_accuracy_current_only": 0.5,
            "bayes_accuracy_with_history": 1.0,
            "evaluation": "Same exhaustive eight states used for fitting and scoring; no held-out generalization claim"}


if __name__ == "__main__":
    print(json.dumps(experiment(), indent=2))
