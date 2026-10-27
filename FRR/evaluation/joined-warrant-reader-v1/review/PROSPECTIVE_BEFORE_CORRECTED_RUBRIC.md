# Prospective independent review

Status: case/design/renderer audit complete; final KEY.json v2 and SCORING.md audited. No assignments, participant prompts or outcomes inspected. First criteria-only originals preserved as `PROSPECTIVE_INITIAL.md` and `.json`. Motivation read only in `modules/verification-layer.md` and `evaluation/quality-preview-reader-v1/NEXT_CONTACT.md`.

## Review commitments

- Treat all delivered evidence as one packet; an explicit exact-key join can establish a premise absent from either record alone. Do not infer a missing premise from a local caveat after the other record supplies it.
- Require the actual join keys, version, scope and target to match. A similar name, nearby date or wrong identifier does not silently establish applicability.
- Distinguish a truly absent premise from a contradicted premise, an inapplicable certificate and a satisfied premise. Determine whether every compatible state supports the requested decision; exhibit concrete compatible alternatives for a claimed unresolved case when possible.
- Recompute the requested quantity with units and inequalities. Mean acceptance and maximum/componentwise acceptance are distinct. Equality at a closed threshold passes; an exceedance fails. Do not substitute a raw-reading ordering for physical upper-bound ordering when component errors differ.
- Score the final decision and numerical result separately from the explanation of applicability and satisfied/missing premises. A correct unresolved answer may still falsely claim a missing premise.
- Judge a proposed next check by what it can actually settle, including remaining candidates and supplied costs, dependencies, priority and stopping rules. A violation witness does not necessarily certify global compliance.
- Flag answer leakage, arm-specific task evidence, unequal evidence, trivial lexical gold cues, avoidable premise ambiguity and mirrored-pair asymmetry before execution. Equal word count alone does not guarantee matched guidance content.
- Keep claims bounded to this small authored reader contact. Sixteen one-turn contexts are not independent real-world validation, and paired cases and repeated arms require descriptive, paired reporting rather than broad efficacy claims.

## Masked outcome review

After dispatch, do not read neutral assignment mappings or participant prompts before depositing the masked outcome review. Assess supplied masked case-response packets against the frozen cases/key and these criteria. Record decision/numerical correctness, applicability explanation, each claimed missing premise and follow-up sufficiency separately. Preserve first-pass review artifacts before any revision.

## Initial findings

No case-specific findings yet: the new study directory and authored inputs were absent at first inspection.


## Case-specific independent audit

Reviewed final author cases (SHA-256 `e68669d46425cdec59c41eb7771f4ee9a8aa5146bf9a5e46babb633be24e3a21`), DESIGN.md, render.py, and final KEY.json v2 and SCORING.md. Recomputed all eight cases independently. Pair-3 change is prospective, preserved in author originals, and correct.

| Case | Warranted action | Required numerical result |
| --- | --- | --- |
| 01 | RELEASE | P=9, Q=9; maximum 9 <=12 |
| 02 | UNRESOLVED | (P,Q)=(9,9) or (3,15); maximum in {9,15} |
| 03 | HOLD | R=13, S=15; maximum 15 >14 |
| 04 | UNRESOLVED | R in [4,14], S in [9,19]; maximum [9,19] |
| 05 | HOLD | T=2, U=17; maximum 17 >11 |
| 06 | UNRESOLVED | E3 gives (2,17), E4 gives (9,10); maximum in {10,17} |
| 07 | RELEASE | certified mean 7 <=8; sum 28 |
| 08 | UNRESOLVED | sharp maximum [7,28], from sum 28 and nonnegativity |

No unintended missing premise, invalid compatible-state witness, wrong gold arithmetic, or mean/max confusion found. Case04 needs only applicable jade information resolving bias >=5: copper cannot cause a violation under the retained bound. Case08 supports compliant (7,7,7,7) and violating (28,0,0,0) states; one passing individual observation does not in general resolve the whole-population criterion. Three exact observations and the known sum always determine the fourth. Case06 has no justified record priority.

## Design review and prospective limitations

The common contract cleanly distinguishes HOLD (certain violation) from UNRESOLVED (both possibilities). Arm texts independently counted as 50 whitespace words each; evidence delivery and JSON fields match across arms for each case. Renderer uses fixed seed and creates new output only; it was inspected but not executed by this reviewer. Instructional single-file read isolation and unmatched tokens/compute are disclosed. Scoring should retain separate action, arithmetic, applicability, missingness and next-check judgments.

Prospective cue refinement removed the global absence/allowed-alternatives sentence from case02 and the agreement/disagreement conclusion from pair3. Rechecked the complete revised cases: both alternatives still follow in case02, and pair3 agreement fixes the assignment by the at-least-one-correct premise. The key arithmetic and actions remain unchanged. The direct authority rules, local no-assignment caveats, and mean/max wording remain substantial cues; these are legitimate stipulated premises but can cause ceiling performance and weaken any claim about spontaneous discovery or difficult joins. There are four paired constructions and one response per case/arm, not eight independent mechanisms or replicated arm estimates. No empirical source calibration, querying, or acquisition-priority policy is exercised. The design now discloses these constraints. Approval is for this small authored conditional reasoning contact only.

## Freeze disposition

Author cases/design/renderer: approved for root freeze. Final KEY.json v2 matches the reviewed cases hash and reversed case05/case06 calculations and witnesses. SCORING.md correctly separates seven dimensions, avoids hidden verbosity requirements, and allows valid partial checks without inventing universal measurement requirements. No outstanding review blocker. No assignment mappings or participant prompts were read.

Cue-refinement review: approved. The immediately preceding review versions are preserved as `PROSPECTIVE_BEFORE_CUE_REFINEMENT.*`.

Final disposition: approved for root freeze/dispatch under the stated scope. No neutral assignments or participant prompts inspected.


## Correction to reviewer approval before dispatch

Root identified a rubric arithmetic defect missed in this review: two measured compliant loads cannot leave residual total <=8, because each is <=8 and their sum is <=16, while total is 28. Residual total is at least12. It can concentrate in one unmeasured component, violating the threshold. With fewer than three exact component observations, compliance cannot be established through this measurement channel, though violation may be established. Earlier review approval of the rubric was mistaken and is preserved in `PROSPECTIVE_PRIOR_MISTAKEN_RUBRIC_APPROVAL.*`; rubric approval is rescinded pending corrected key/rubric bytes. Cases, expected actions and sharp bounds are unchanged. No reader outcomes or assignments inspected.
