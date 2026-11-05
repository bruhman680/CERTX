# What we learned from the copied world descriptions

The targeted cases are a useful observation even though they did not change the continuation decision. [WORLD_TEXT_CASES.json](WORLD_TEXT_CASES.json) preserves the full generated passages alongside the actual world view in their input and the actual host receipt.

At zero-based step 330, the model reproduced most of the world footer, including controls, but asserted number 1 and bounds −8 to −9. The actual view said 0 and −8 to 8. It ended with the fragment `Your next action: LO` at the token cap. This is not an executed LOOK, an internal simulation proven correct, or a change in the environment. It is a copied description with concrete factual errors.

At 365, another copied description gave the actual 0 and bounds. Matching visible values does not distinguish understanding from copying. At 367, a generated passage copied a host-stop heading and wrote an end-token label, while the actual event stopped at its 96-token limit. Only the structured host field supplies the real stop status.

These observations support keeping model-authored text separate from authoritative state and action receipts. That boundary already held: none of these passages executed a control or altered the world. We do not need to suppress such language or remove the failed outputs to preserve accurate observation.

The broader open question is whether this model can operate the controls when explicitly asked, versus simply continuing surrounding text in open play. This run does not answer it. A later explicitly labeled diagnostic could separate command expression, actual execution, and predicted consequence. It should not be silently inserted into this unchanged primary run or retrospectively treated as its free-play behavior.

All 50 outputs were reviewed through their 28 distinct complete reply strings, preserving counts and raw originals. The review classifies the cases as a familiar imitation/factual-error family for the user's continuation condition; it does not assert that nothing cognitively interesting occurred or define a universal emergence detector.
