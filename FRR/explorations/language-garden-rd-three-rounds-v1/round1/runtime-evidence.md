# Round 1: runtime evidence and honest bounds

Planning/source inspection only, 2026-11-21. Read the new brief, verbatim compact FRR and prior DESIGN. No weights were loaded, model called, tokenizer instantiated, or files in prior studies edited. Two local source groups suffice: cached metadata and the preserved native generation/call path; no new external scouting.

**Metadata.** Under `/workspace/cache_backend_models/smollm2-135m/`, `config.json` declares LlamaForCausalLM, 30 layers, hidden size 576, nine attention heads/three KV heads, vocabulary 49152, `max_position_embeddings=8192`, no RoPE scaling, EOS/pad ID 2 and BOS ID 1. `tokenizer_config.json` independently declares `model_max_length=8192`, GPT2Tokenizer and EOS `<|im_end|>`. These establish declared bounds, not effective reasoning or retention across 8192 tokens. SHA256:

- `config.json`: `8eb740e8bbe4cff95ea7b4588d17a2432deb16e8075bc5828ff7ba9be94d982a`
- `tokenizer_config.json`: `4ec77d44f62efeb38d7e044a1db318f6a939438425312dfa333b8382dbad98df`
- `tokenizer.json`: `9ca9acddb6525a194ec8ac7a87f24fbba7232a9a15ffa1af0c1224fcd888e47c`

The cached `generation_config.json` specifies special-token IDs, without a decoding-policy temperature or output allowance. Those come from the caller/body, not an intrinsic model preference.

**Actual source mechanics.** Read the full `/workspace/frr/evaluation/minimal-garden-candidate-v1/generation.py` (SHA256 `0e5258823b7af83fb1e962ce1b04496aee2edbe1e05435018e19f9fa3b0132a2`) and native baseline call/preflight/audit sources. The preserved native baseline calls its inherited `s.ref.body.generate`; contracts pin this body. It uses `apply_chat_template(..., tokenize=True, add_generation_prompt=True)`, rejects input above 7936 without truncation/summary, and greedily chooses argmax for at most 256 generated tokens. Input plus reserved output is 8192. This conservative existing division is available as a candidate operational bound; it is not a newly chosen language-world policy.

The native template wraps role/content in `<|im_start|>`/`<|im_end|>`, appends an assistant prefix, and injects “You are a helpful AI assistant named SmolLM, trained by Hugging Face” if the first message is not system. An explicit system message prevents that insertion. Therefore “seed only” must name its role and rendering: it can still contain host-supplied assistant framing.

Each call creates its KV cache from supplied input; no cross-call cache is returned. Continuity requires host-carried messages or another explicit mechanism. The body stops only at EOS ID 2 or token limit. EOS remains in raw generated IDs but `skip_special_tokens=True` removes it from visible text. EOS-only output can look empty. EOS, an expressed stop, budget truncation, fault and host suspension cannot honestly share a “rest” interpretation.

**First-window limit.** Require complete rendered input tokens plus 256 ≤ 8192, including seed, assistant/system text, all prior outputs, turn delimiters and host cues. Preserve raw IDs, rendered input, output IDs and stop cause. Pause before the next call exceeds 7936. No exact seed token count or guaranteed turn count was measured here; arbitrary symbol strings defeat character-based estimates.

**Consequential gap.** Neither metadata nor source proves competence with retrieval commands, branch navigation, record identifiers, JSON actions, an opt-out command, or sustained autonomous exploration. Record-first minimizes an action parser but supplies no independent nontext consequences. A raw continuation interface could remove recurring user cues, while departing from the native conversational template; its competence is also unmeasured. Scheduling, explicit-stop interpretation, partial output treatment, special-token handling and a concrete first-window allowance remain policy decisions. These belong in a later blueprint, not silently in this round's source findings.
