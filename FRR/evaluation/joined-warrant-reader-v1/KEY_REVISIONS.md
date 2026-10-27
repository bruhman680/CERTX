# Prospective key revision before reader contact

KEY_INITIAL.json and SCORING_INITIAL.md preserve the first independent key/rubric bytes.

The builder then changed case05 agreement to T->violet/U->ivory, making acceptance contradicted (T2,U17,max17), and reversed the record labels in case06 without changing its two possibilities. Case02's explicit missingness cue and pair3's explicit agreement/disagreement interpretation sentence were removed, with no logical change. Current KEY.json v2 follows the revised cases and SCORING.md updates the action list. No responses or instruction arms have been inspected.

Initial cases hash recorded by initial key: bd9a5472ea18c27134e5967ad7427511da8274ea0d4b071e4983cd3d882e29ac
Current cases hash: e68669d46425cdec59c41eb7771f4ee9a8aa5146bf9a5e46babb633be24e3a21

These changes were prospective fixture changes requested through root/builder, not scoring relabeling after outcomes.

## Prospective maximum-check correction

Root identified an arithmetic defect in the c8 rubric: two compliant measured loads cannot sum to at least20 and leave residual sum at most8, since each is at most8. The rubric now states that zero to two measurements cannot certify compliance when compliance remains possible, while fewer than three can detect violation (a load >8 or <4 suffices). Three exact loads determine the fourth from sum28. KEY v3 clarifies its formerly ambiguous fewer-measurements statement. KEY_BEFORE_MAX_CHECK_FIX.json and SCORING_BEFORE_MAX_CHECK_FIX.md preserve prior bytes. No outcomes existed or were inspected.

The action list was checked again and correctly says release01/07, reject03/05 in the saved current rubric.
