# Saved bytes and scorer object hashes

During final integrity checks, root initially compared `SCORES_MASKED.json`'s `response_sha256` to the raw `answers/Rxx.json` bytes. That assertion failed for all16. Inspection of the preserved `deposit_masked_scores.py` showed that this field hashes the parsed response after `json.dumps(response, sort_keys=True, separators=(',', ':'))`, with default ASCII escaping. It is an object-serialization binding, not a raw response-file hash.

Root corrected the audit's hash domain, without changing any answer, scorer judgment or frozen receipt. All16 saved parsed objects equal their `SCORER_INPUT.json` response objects, and all16 canonical response hashes match their scorer rows. `DELIVERY_CHECKS.json` and `RESPONSE_BINDING_CHECKS.json` retain the separate raw-file hashes. The initial wrong-domain assertion and corrected checks are recorded in the latter.

This was a root audit-assumption failure, not a reader failure or corrupted scientific data. Byte identity and equality under a specified serialization are distinct claims; neither authenticates an independently exported collaboration transcript.
