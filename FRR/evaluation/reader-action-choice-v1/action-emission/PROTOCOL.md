# Explicit action emission after route-choice failures

Outcome-informed control after coded and plain-action routing results. Freeze data/prompts/controller/checkpoint hashes before these24forwards. Both fixed models see six explicit action words, each under two repeat/return instruction frames. The expected word is intentionally supplied in the prompt: this is copying/emission, not selecting an appropriate next action or discovering uncertainty.

Retain exact word correctness, permissive leading-word correctness and complete-word constrained-choice scoring separately. Six action labels have unequal token lengths. No action is executed from this diagnostic, even if FULL/TARGET is emitted, since the task is to repeat a word. There is no environment/world or hidden evidence to retrieve. The same copied words alone do not establish that the model knows when to request sources. Failed copying on these frames does not prove an absolute inability to emit a vocabulary item.

No training, checkpoint selection, retries, default promotion, paid API/install/download or new model state. Same localCPU/eagerfloat32/2threads/max8outputs/256promptguard/sampled working guard as the parent. Coordinator-authored control, no independent empirical replication. This diagnostic does not stop unrelated downstream explorations or retroactively pass the coded interface.
