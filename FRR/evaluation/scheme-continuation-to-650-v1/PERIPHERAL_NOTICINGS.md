# Recorded alongside the unchanged 100-entry block

The legacy renderer wraps raw replies between `<<<` and `>>>`, then appends host feedback/result text. Raw replies can themselves contain those delimiters, labels such as Feedback or HOST GENERATION STOP, and JSON shaped like host receipts. Saved step 548 / human entry 549 is a retained example with `>>>` and Feedback inside model text. The renderer does not escape that text before framing it.

The external structured records preserve attribution, and verification compares those records. This is not evidence that a copied status became a real host action. However, the model-facing plain-text view can contain visually competing boundaries. We have not tested whether that ambiguity causes the observed repetitions or failures.

A future controlled contact could compare a clearly escaped/length-delimited reply view against the existing view on isolated frozen histories. Any live change must be versioned and preserve replay of old prompts. **No renderer, marker, prompt or inference setting was changed during this block.**

The previously documented executed-field ambiguity also remains: terminal validation rejection is not successful guest evaluation. Count actual statuses and state effects, not that flag alone.

## History transport is also a condition

`source-access-three-cycle-v1/generate_capacity.py` line 5 supplies the entire rendered notebook as one user message to the chat template, then starts generation. Prior replies and host feedback are quoted inside that message; they are not separate chat turns. The model also uses fresh KV state per call. These are concrete protocol conditions, not a claim that its history is absent.

A future isolated comparison could hold the world, weights, sampling, history and budget fixed while changing how roles and boundaries are represented. Token counts and exact payloads would need separate recording; equal semantics would not guarantee equal model behavior. This could help separate limited tool capability from presentation effects. It has not been tested here, and **no role, framing or context-format change was made during this 100-entry block**.

## Generated environment claims remain unverified

Saved step 616 / human entry 617 includes a claimed Windows version and a HOST ACCESS heading inside the generated reply. The live host has not been changed by that text, and the reply was handled as a plain notebook record. Such statements must not be promoted into host capabilities, platform metadata or execution evidence. The raw event and its separate host result retain their provenance.
