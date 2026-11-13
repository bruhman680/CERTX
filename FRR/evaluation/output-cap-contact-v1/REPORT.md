# Detached reply-length contact

13 November 2026, America/Chicago. This is an inference diagnostic, not a continuation of the live garden. The active notebook remains paused at entry 1562; reference 1550 remains preserved.

## Question and protocol

Does the 256-token reply limit alone explain the lack of complete executable cells? We loaded the same locally cached 135M parameter model, checked its parameter digest, used the same float32 CPU/eager greedy decoding, and replayed exact saved inputs for turns 1 and 12. A third input is the existing runner's exact prospective turn-13 conversation. Each fresh generation could produce up to 1,024 tokens within the 8,192-position capacity. No task, hint, demonstration, continuation prompt, code repair or extra model-facing instruction was added.

Milestones at 256/512/768/1024 are prefixes of a single uninterrupted KV-cache generation, not independent samples or persistent chunked sessions. EOS ends the reply naturally. Generated cells were parsed with the unchanged live parser but never executed. Initial/final run-file inventories and parameter digests were compared.

| Input | Input tokens | Output tokens | Stop | Complete executable cells | Retained 256-token prefix exact |
|---|---:|---:|---|---:|---|
| retained_01 | 95 | 1024 | token_limit | 0 | True |
| retained_12 | 3031 | 257 | eos | 0 | True |
| prospective_13 | 3298 | 257 | eos | 0 | None |

## Interpretation

The first replay's extra output expands a network-node program and still lacks a closing fence at 1,024 tokens. The turn-12 replay instead ends naturally at token 257, with its code fence still unfinished: a parser-incomplete reply can be the model's own completed output. This distinguishes an output-budget interruption from a model that stops without satisfying the execution grammar. These observations weaken a simple universal claim that increasing the limit would resolve the observed inactivity. They do not establish impossibility at other lengths, contexts, decoders or models.

There are three deliberately selected contexts from one model and trajectory. No population-level frequency, general emergence conclusion, or causal explanation of all prior behavior follows. A complete fence would establish syntactic dispatch eligibility, not correct or useful code. Conversely, unfinished writing remains preserved writing; it is not deleted, graded into compliance, or silently repaired.

## Preservation and next contact

All three generations are detached. Canonical run files and model weights stayed unchanged. No additional live entry, training update, endpoint charge or world action was introduced. Raw prompts, token IDs, outputs and milestone counts are retained in this directory. A durable chunk-continuation protocol has not been implemented or tested by this contact.

The strongest next comparison is a declared detached decoder/context study, or explicitly designed continuation semantics, rather than silently widening the active contract. Because a retained reply naturally ends unfinished, merely increasing the live cap is not yet supported as a sufficient repair. Any altered live condition needs its own recorded contract and lineage.
