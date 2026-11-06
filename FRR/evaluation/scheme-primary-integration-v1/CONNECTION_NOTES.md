# Connection design and scope

The user clarified that Scheme was intended to become part of the original continuous environment. The former either/or choice between original and Scheme gardens was a framing error. Implementation tests were isolated; the live design now adds a fresh Scheme workspace at original step 500 without restarting the notebook or copying test artifacts into it.

The old number patch remains replayed from its own historical receipts. Scheme owns a separate bounded artifact namespace inside that same environment; its actions are tied to the continuing primary step and appear as host receipts in the same notebook. This division separates state authorities, not model histories or seasons.

Persistence is external, not an always-running neural process: each reply uses fresh inference state with the same frozen base and adapter, a bounded recent-history view, retained archive access and current world state. Pauses preserve published Scheme data/functions and all raw entry history. They do not preserve hidden activations across calls or update weights.

## Checks performed

- Full old-prefix prompt/token/dispatch verification on a disposable copy: 500 entries, including 48 origin entries and 452 saved generations. All 1,504 pre-existing non-bytecode primary files were unchanged during that baseline check.
- Five connection tests: unchanged history and number patch; actual function publication/use, idempotent retry and malformed-source failure; portable reconstruction; prompt bounds/whole-reply routing; and recovery after an action committed but before notebook commit.
- Recovery test used a clearly synthetic host fixture on the copy. Its marker and function are absent from the live genesis.
- The first test invocation selected an older module with the same `world_cli` filename and exited during argument parsing. Import-path selection was corrected before activation; that failure is retained in `CONNECTION_TEST_ATTEMPT1.stderr`.
- The first live run preflight rejected the deliberately removed pause marker before loading the model or recording a prompt. V1 is preserved; V2 narrowly corrects the mutable-marker check. Both armed and paused preflights then passed, and all five connection tests passed again on a copy.
- Activation verifies an empty live namespace, with no imported calibration, test, practice or demonstration history. Old manifestations and source pins are not overwritten.

## Bounds and limitations

The runtime is the previously tested bounded Scheme subset and portability store, not unrestricted Scheme or Python. Local parser, evaluator, storage, process, time and output limits remain. No network, imports or arbitrary host files are exposed. Some aggregate delivery accounting remains provisional. The small model is not assumed to know command syntax reliably; its failures remain observations, rather than a prerequisite to using the extension.

The new verifier independently reconstructs each new prompt and replays its world dispatch from a before-bundle, compares after-bundles byte for byte, checks the live store, retained notebook prefix, RNG seeds, token boundaries, manifest pins and all historical protected file hashes. It uses the copy-verified old prefix and hash preservation rather than rewriting old verifications. A finite successful check supports these local properties, not arbitrary security or autonomous learning claims.

Standard model-generation settings remain the original CPU model plus canonical LoRA, temperature 0.8, top-p 0.9, maximum 96 generated tokens and maximum 8,096 input tokens, with seed `1201*100 + absolute_step -45`. No training or model downloads are introduced.
