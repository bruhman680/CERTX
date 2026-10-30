"""Run with cache_backend_venv/bin/python -m unittest -v test_lora_cpu."""
import copy
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

import torch
from safetensors.torch import load_file, save_file
from torch import nn

from lora_cpu import inject_lora, load_adapter, save_adapter


PIN = {"model": "synthetic-test", "revision": "fixed-v1"}


class TinyAttention(nn.Module):
    def __init__(self):
        super().__init__()
        self.q_proj = nn.Linear(6, 6)
        self.v_proj = nn.Linear(6, 2)
        self.k_proj = nn.Linear(6, 6)

    def forward(self, x):
        return self.q_proj(x) + self.k_proj(x), self.v_proj(x)


class TinyModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.self_attn = TinyAttention()

    def forward(self, x):
        a, b = self.self_attn(x)
        return torch.cat((a, b), dim=-1)


class LoRATests(unittest.TestCase):
    def setUp(self):
        torch.manual_seed(137)
        self.model = TinyModel()
        self.x = torch.randn(3, 6)

    def test_zero_init_preserves_forward_and_only_adapter_gradients(self):
        before = self.model(self.x).detach()
        inventory = inject_lora(self.model)
        torch.testing.assert_close(self.model(self.x), before, rtol=0, atol=0)
        self.assertEqual(inventory["trainable_parameter_count"], 80)
        self.assertEqual(len(inventory["trainable_names"]), 4)
        self.model(self.x).square().sum().backward()
        for name, p in self.model.named_parameters():
            if "lora_" in name:
                self.assertIsNotNone(p.grad, name)
            else:
                self.assertIsNone(p.grad, name)
                self.assertFalse(p.requires_grad, name)
        # B=0 makes A's initial gradient zero, while B can learn immediately.
        self.assertEqual(self.model.self_attn.q_proj.lora_A.grad.abs().sum(), 0)
        self.assertGreater(self.model.self_attn.q_proj.lora_B.grad.abs().sum(), 0)

    def test_synthetic_step_and_roundtrip(self):
        clone = copy.deepcopy(self.model)
        inject_lora(self.model)
        inject_lora(clone)
        frozen = {n: p.detach().clone() for n, p in self.model.named_parameters()
                  if not p.requires_grad}
        before = self.model(self.x).detach()
        optimizer = torch.optim.SGD((p for p in self.model.parameters()
                                     if p.requires_grad), lr=0.01)
        self.model(self.x).square().mean().backward()
        optimizer.step()
        after = self.model(self.x).detach()
        self.assertFalse(torch.equal(before, after))
        for n, p in self.model.named_parameters():
            if n in frozen:
                torch.testing.assert_close(p, frozen[n], rtol=0, atol=0)
        with tempfile.TemporaryDirectory() as d:
            save_adapter(self.model, d, base_pin=PIN)
            self.assertEqual(set(load_file(str(Path(d) / "adapter.safetensors"))),
                             {n for n, p in self.model.named_parameters() if p.requires_grad})
            load_adapter(clone, d, base_pin=PIN)
        torch.testing.assert_close(clone(self.x), after, rtol=0, atol=0)

    def _rewrite_weights(self, directory, mutate):
        path = Path(directory) / "adapter.safetensors"
        state = load_file(str(path))
        mutate(state)
        save_file(state, str(path))
        manifest_path = Path(directory) / "manifest.json"
        manifest = json.loads(manifest_path.read_text())
        manifest["sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
        manifest_path.write_text(json.dumps(manifest))

    def test_rejects_bad_states_before_any_parameter_changes(self):
        inject_lora(self.model)
        def missing(state):
            state.pop(next(iter(state)))
        def extra(state):
            state["unexpected"] = torch.zeros(1)
        def wrongshape(state):
            state[next(iter(state))] = torch.zeros(1)
        def nonfinite(state):
            state[next(iter(state))].flatten()[0] = float("nan")
        for mutate in (missing, extra, wrongshape, nonfinite):
            with self.subTest(mutate=mutate.__name__), tempfile.TemporaryDirectory() as d:
                save_adapter(self.model, d, base_pin=PIN)
                before = {n: p.detach().clone() for n, p in self.model.named_parameters()}
                self._rewrite_weights(d, mutate)
                with self.assertRaises(ValueError):
                    load_adapter(self.model, d, base_pin=PIN)
                for n, p in self.model.named_parameters():
                    torch.testing.assert_close(p, before[n], rtol=0, atol=0)

    def test_rejects_pin_config_and_hash_mismatch(self):
        inject_lora(self.model)
        with tempfile.TemporaryDirectory() as d:
            save_adapter(self.model, d, base_pin=PIN)
            with self.assertRaisesRegex(ValueError, "incompatible"):
                load_adapter(self.model, d, base_pin={"model": "different"})
            other = TinyModel()
            inject_lora(other, rank=2)
            with self.assertRaisesRegex(ValueError, "incompatible"):
                load_adapter(other, d, base_pin=PIN)
            weights = Path(d) / "adapter.safetensors"
            weights.write_bytes(weights.read_bytes() + b"corruption")
            with self.assertRaisesRegex(ValueError, "SHA256"):
                load_adapter(self.model, d, base_pin=PIN)

    def test_smollm_architecture_inventory_without_loading_weights(self):
        from transformers import AutoConfig, AutoModelForCausalLM
        model_path = Path("/workspace/cache_backend_models/smollm2-135m")
        if not model_path.exists():
            self.skipTest("local SmolLM2 config unavailable")
        config = AutoConfig.from_pretrained(model_path, local_files_only=True)
        with torch.device("meta"):
            model = AutoModelForCausalLM.from_config(config)
            inventory = inject_lora(model)
        self.assertEqual(config.num_hidden_layers, 30)
        self.assertEqual(len(inventory["targets"]), 60)
        self.assertEqual(len(inventory["trainable_names"]), 120)
        self.assertEqual(inventory["trainable_parameter_count"], 230400)
        self.assertTrue(all(n.endswith(("lora_A", "lora_B"))
                            for n in inventory["trainable_names"]))


if __name__ == "__main__":
    unittest.main()
