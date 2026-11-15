# Cached template observation, not a demonstrated cause

Read-only source contact during the three-cycle run. Exact cached tokenizer config and source hash are recorded in TOKENIZER_TEMPLATE_OBSERVATION.json. No new source download, model call or world action was needed.

The Jinja chat template prepends `You are a helpful AI assistant named SmolLM, trained by Hugging Face` only if the first supplied message is not a system message. These studies explicitly supply system/user roles, even when the system content is empty; therefore the default is not silently inserted. This matches exact saved tokenized messages. It is a declared framing condition, not evidence of a tokenizer failure.

This creates a useful future comparison: native-default identity context versus the explicit empty-system baseline, under otherwise fixed world/observation/action mechanics. Such a comparison would add identity/helpfulness orientation and tokens/positions; it would not be neutral, instruction-free or proof that the native default is required. No such experiment was performed in the present three cycles, and the observation did not alter their frozen conditions. It cannot establish how much native-default wording occurred in training or explain the current repetition on its own.
