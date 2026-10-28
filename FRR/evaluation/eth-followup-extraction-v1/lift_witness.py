"""Independent exact arithmetic illustration; does not run the ETH algorithm."""
import json

cases = []
for name, op in [("addition", lambda x: x + x), ("multiplication", lambda x: x * x)]:
    original = 3
    low_modulus, high_modulus = 4, 16
    frozen = (op(original) % low_modulus) % high_modulus
    recomputed = op(original % high_modulus) % high_modulus
    assert frozen != recomputed
    assert frozen % low_modulus == recomputed % low_modulus
    cases.append({"operation": name, "original": original,
                  "creation_precision_bits": 2, "later_precision_bits": 4,
                  "creation_residue_lifted": frozen,
                  "expression_recomputed_at_later_precision": recomputed,
                  "same_at_creation_precision": True})
print(json.dumps({"scope": "canonical representatives do not preserve ring operations across precision changes", "cases": cases}, indent=2))
