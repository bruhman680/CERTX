"""Bounded context-wake probe. Requires torch and transformers; downloads distilgpt2.

Run: python transformer_context_swap_probe.py
This file has not been executed against a model in the current workspace.
"""

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


MODEL_ID = "distilgpt2"
torch.manual_seed(20261005)
tok = AutoTokenizer.from_pretrained(MODEL_ID)
model = AutoModelForCausalLM.from_pretrained(MODEL_ID).eval()

# Equal token counts and identical lexical counts; only the rule assignments differ.
suffix = "oak:"
contexts = {
    "blue_rule": ("oak: blue\nelm: green\n" * 4) + suffix,
    "green_rule": ("oak: green\nelm: blue\n" * 4) + suffix,
    "restored_blue": ("oak: blue\nelm: green\n" * 4) + suffix,
}
ids = {name: tok(prompt, return_tensors="pt").input_ids for name, prompt in contexts.items()}
assert len({v.shape[1] for v in ids.values()}) == 1, "Reword prompts to match token length."

candidate_ids = {}
for word in [" blue", " green"]:
    encoded = tok.encode(word, add_special_tokens=False)
    assert len(encoded) == 1, (word, encoded)
    candidate_ids[word] = encoded[0]


@torch.no_grad()
def raw_logits(input_ids):
    # Both routes have the same complete token prefix and position indices.
    full = model(input_ids=input_ids, use_cache=False).logits[:, -1, :]
    first = model(input_ids=input_ids[:, :-1], use_cache=True)
    cached = model(
        input_ids=input_ids[:, -1:], past_key_values=first.past_key_values,
        use_cache=True,
    ).logits[:, -1, :]
    max_cache_error = (full - cached).abs().max().item()
    return full[0], max_cache_error


measurements = {}
for name, input_ids in ids.items():
    logits, cache_error = raw_logits(input_ids)
    log_odds = (logits[candidate_ids[" blue"]] - logits[candidate_ids[" green"]]).item()
    # Temperature operates downstream on output logits; it cannot change these raw values.
    temperature_probs = {}
    for temperature in [0.5, 1.0, 1.5]:
        probs = torch.softmax(logits / temperature, dim=-1)
        temperature_probs[str(temperature)] = {
            word.strip(): round(probs[token_id].item(), 8)
            for word, token_id in candidate_ids.items()
        }
    measurements[name] = (log_odds, cache_error)
    print(name, "log_odds(blue/green)=", round(log_odds, 6),
          "cache_max_abs_error=", round(cache_error, 8),
          "sampling_probabilities=", temperature_probs)

print("effect: log_odds(blue_rule) - log_odds(green_rule) =",
      measurements["blue_rule"][0] - measurements["green_rule"][0])
print("restore control delta =",
      measurements["blue_rule"][0] - measurements["restored_blue"][0])
# Passing this equivalence check only verifies this model/runtime's cache implementation.
assert max(error for _, error in measurements.values()) < 1e-3
