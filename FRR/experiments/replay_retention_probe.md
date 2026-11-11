# FRR v0.5 — Replay during supervised rule adaptation

**Status:** Executed synthetic retention-control pilot, 2026-11-11 UTC.  
**Code:** `replay_retention_probe.py`, imports the established parity world, GRU, and held-out accuracy evaluator.

## Question

Does continued exposure to old-rule examples reduce forgetting while a recurrent model learns an inverted rule?

## Setup

Three seeds 7,17,29. Pretrain a 16-unit GRU for 450 batches on 8-state XOR3 parity with 10% transition noise. Clone weights into two arms. Following a known switch to inverted parity, run 80 Adam update steps (`lr=.012`). **New-only** arm trains on 128 fresh inverted-rule sequences per step. **Mixed replay** arm trains on those same 128 new sequences plus 128 freshly generated original-rule sequences, with a 50/50 average of per-arm losses. Both see the same new data; replay sees twice the labeled examples and processes roughly twice the sequence volume per update. Neither arm receives an unannounced switch or performs autonomous detection.

Evaluate at fixed checkpoints on independent, fixed, never-trained test sequences of both rules; mask first two predictions per sequence. Sequence timepoints are correlated.

## Final checkpoint: 80 supervised updates

| Seed | New-only new-rule | New-only old-rule | Replay new-rule | Replay old-rule |
| --- | ---: | ---: | ---: | ---: |
| 7 | 83.24% | 77.86% | 80.43% | 86.16% |
| 17 | 84.87% | 64.96% | 84.14% | 83.19% |
| 29 | 85.16% | 65.99% | 81.97% | 85.18% |
| **Mean** | **84.42%** | **69.60%** | **82.18%** | **84.85%** |

At 20 updates, mixed replay produced new-rule accuracies 75.66–80.35% and old-rule accuracies 81.81–83.61%; new-only had new-rule 76.44–81.05% and old-rule 54.18–81.38%. The trajectories differ across seeds. At 80, replay preserved more old-rule performance while modestly sacrificing new-rule accuracy.

## Interpretation / limits

This is a conventional stability-plasticity tradeoff on a balanced synthetic task. Replay helps maintain performance on the original mapping but does not eliminate the cost of adaptation. More replay data and compute are provided to the mixed arm; this is **not a matched-compute efficiency comparison**. A fair follow-up must fix total examples/forward-backward compute and vary replay fraction while tracking both rules and combined accuracy. Original-rule replay here is freshly generated labeled data, not a capacity-bounded autobiographical memory buffer. No long-term persistence, autonomous change detection, FRR prompt benefit, or universal memory law follows.

Preserve the frozen canonical 1,550-entry Garden; it is unrelated to this neural test.
