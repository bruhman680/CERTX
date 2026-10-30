"""Small local LoRA utility for Llama-style q/v projections; no PEFT dependency.

The caller supplies a JSON base_pin (for example model revision and weight hash).
The pin is compared on load; the caller is responsible for establishing it from
the actual base model. Adapter files never contain frozen model parameters.
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import torch
from safetensors.torch import load_file, save_file
from torch import nn
from torch.nn import functional as F


class LoRALinear(nn.Module):
    def __init__(self, base: nn.Linear, rank=4, alpha=8, dropout=0.0):
        super().__init__()
        if not isinstance(rank, int) or isinstance(rank, bool) or rank < 1:
            raise ValueError("rank must be a positive integer")
        if not math.isfinite(alpha) or alpha <= 0:
            raise ValueError("alpha must be positive and finite")
        if not math.isfinite(dropout) or not 0 <= dropout < 1:
            raise ValueError("dropout must be in [0, 1)")
        self.base = base
        self.base.requires_grad_(False)
        self.rank, self.alpha, self.dropout_p = rank, float(alpha), float(dropout)
        self.scale = self.alpha / rank
        self.dropout = nn.Dropout(dropout)
        self.lora_A = nn.Parameter(base.weight.new_empty((rank, base.in_features)))
        self.lora_B = nn.Parameter(base.weight.new_zeros((base.out_features, rank)))
        nn.init.kaiming_uniform_(self.lora_A, a=math.sqrt(5))
        self.train(base.training)

    def forward(self, x):
        return self.base(x) + self.scale * F.linear(
            F.linear(self.dropout(x), self.lora_A), self.lora_B
        )


def _adapters(model):
    return {name: module for name, module in model.named_modules()
            if isinstance(module, LoRALinear)}


def inject_lora(model, rank=4, alpha=8, dropout=0.0):
    """Freeze the model and replace every self_attn q_proj/v_proj with LoRA.

    Returns adapter_inventory(model). Call before constructing an optimizer.
    """
    if _adapters(model):
        raise ValueError("model already has LoRA adapters")
    targets = []
    for name, module in model.named_modules():
        if name.split(".")[-1] == "self_attn":
            for child in ("q_proj", "v_proj"):
                layer = getattr(module, child, None)
                if not isinstance(layer, nn.Linear):
                    raise ValueError(f"{name}.{child} is not a Linear")
                targets.append((module, child, LoRALinear(layer, rank, alpha, dropout)))
    if not targets:
        raise ValueError("no self_attn q_proj/v_proj targets found")
    model.requires_grad_(False)
    for parent, child, adapter in targets:
        adapter.lora_A.requires_grad_(True)
        adapter.lora_B.requires_grad_(True)
        setattr(parent, child, adapter)
    return adapter_inventory(model)


def adapter_inventory(model):
    """Return exact trainable parameter names, counts, and wrapped targets."""
    trainable = {name: p.numel() for name, p in model.named_parameters()
                 if p.requires_grad}
    return {"targets": list(_adapters(model)), "trainable_names": list(trainable),
            "trainable_parameter_count": sum(trainable.values()),
            "trainable_parameter_counts": trainable}


def _state(model):
    adapters = _adapters(model)
    if not adapters:
        raise ValueError("model has no LoRA adapters")
    return {f"{name}.{key}": getattr(module, key)
            for name, module in adapters.items() for key in ("lora_A", "lora_B")}


def _description(model, base_pin):
    if not isinstance(base_pin, dict) or not base_pin:
        raise ValueError("base_pin must be a nonempty JSON object")
    # Reject non-JSON and NaN pins and normalize tuples to JSON lists.
    pin = json.loads(json.dumps(base_pin, sort_keys=True, allow_nan=False))
    adapters = _adapters(model)
    state = _state(model)
    return {"format_version": 1, "base_pin": pin,
            "targets": {name: {"rank": m.rank, "alpha": m.alpha,
                                "dropout": m.dropout_p,
                                "in_features": m.base.in_features,
                                "out_features": m.base.out_features}
                        for name, m in adapters.items()},
            "tensors": {name: {"shape": list(p.shape), "dtype": str(p.dtype)}
                        for name, p in state.items()}}


def _validate_state(state, expected):
    if set(state) != set(expected):
        raise ValueError("adapter tensor names do not match (missing or extra keys)")
    for name, tensor in state.items():
        if tensor.shape != expected[name].shape:
            raise ValueError(f"wrong shape for {name}")
        if tensor.dtype != expected[name].dtype:
            raise ValueError(f"wrong dtype for {name}")
        if not torch.isfinite(tensor).all().item():
            raise ValueError(f"nonfinite adapter tensor: {name}")


def save_adapter(model, directory, *, base_pin):
    """Write adapter.safetensors and a validated, hashed manifest.json."""
    manifest = _description(model, base_pin)
    expected = _state(model)
    state = {name: p.detach().cpu().contiguous() for name, p in expected.items()}
    _validate_state(state, expected)
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    weights = directory / "adapter.safetensors"
    save_file(state, str(weights))
    manifest["sha256"] = hashlib.sha256(weights.read_bytes()).hexdigest()
    (directory / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True, allow_nan=False) + "\n")
    return manifest


def load_adapter(model, directory, *, base_pin):
    """Validate pin/config/targets/shapes/hash/finiteness before copying tensors.

    The model must already have matching adapters installed by inject_lora.
    """
    directory = Path(directory)
    manifest = json.loads((directory / "manifest.json").read_text())
    expected_manifest = _description(model, base_pin)
    if not isinstance(manifest, dict) or set(manifest) != set(expected_manifest) | {"sha256"}:
        raise ValueError("invalid adapter manifest fields")
    if {k: v for k, v in manifest.items() if k != "sha256"} != expected_manifest:
        raise ValueError("adapter manifest is incompatible with base pin or model config")
    weights = directory / "adapter.safetensors"
    if hashlib.sha256(weights.read_bytes()).hexdigest() != manifest["sha256"]:
        raise ValueError("adapter SHA256 mismatch")
    state, expected = load_file(str(weights), device="cpu"), _state(model)
    _validate_state(state, expected)
    with torch.no_grad():
        for name, param in expected.items():
            param.copy_(state[name])
    return manifest
