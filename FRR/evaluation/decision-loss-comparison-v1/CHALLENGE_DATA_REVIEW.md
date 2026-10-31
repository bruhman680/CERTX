# Separate-agent review of predeclared 36-case challenge

31 October 2026. Read-only review of CHALLENGE_CASES.json and CHALLENGE_KEYS.json under evaluation/decision-loss-comparison-v1, before inspecting any new-study outputs. No model calls, training, network, or FRR changes were performed. This report is a separate agent's consistency review, not independent ground truth, replication, or verification of training execution timing.

All 36 cases pass. Independently parsed each XML record or bullet section, selected the batch named by the source header, extracted target and Other sampled-soil counts, derived the semantic label, and compared against every supplied key. All labels, target_value, other_value, target_first, and family fields match. IDs are unique, source/key IDs match exactly, and every source case has exactly four fields: id, split, structure_family, source. Oracle metadata remains in the separate key file.

The complete factorial has one case in every cell of 2 formats × 3 target states × 3 Other states × 2 record positions. Families xml_order and bullet_order have 18 cases each; target YES/NO/WITHHOLD each have 12 cases; target-first and target-last each have 18. Each family has six cases per target state, six per Other state, and nine per target position. Within each format and position the full nine-state cross is present.

| Factor | Values verified |
|---|---|
| Target batch | Rowan, unique named target in every source |
| Target sampled-soil state | positive 11; zero 0; missing `not recorded` |
| Other sampled-soil state | positive 6; zero 0; missing `not recorded` |
| Target position | first record/section; second record/section |
| Target observations per soil | constant 7, independent of both sampled-soil factors |
| Other observations per soil | constant 2 |
| Other constant fields | damaged plots 0; inspections unavailable |

Target-versus-Other selection is semantically unambiguous. Each source has two explicitly named records/sections, one Rowan and one Other. Reordering preserves their values and meaning. Every cross of target state and Other state occurs in both orders. This removes the original primary set's universal final-value solution and separates Other count from target observations count. Retain the original 24-case primary comparison unchanged and report this challenge separately; it addresses a previously identified scope limitation rather than broadening the primary estimate retrospectively.

Useful exact diagnostic baselines on these 36 cases:

| Rule | Overall | On 24 cases where target and Other states differ |
|---|---:|---:|
| Always read first sampled-soil value | 24/36 (66.7%) | 12/24 (50%) |
| Always read last sampled-soil value | 24/36 (66.7%) | 12/24 (50%) |
| Always read Other sampled-soil value | 12/36 (33.3%) | 0/24 |
| Any constant valid label | 12/36 (33.3%) | 8/24 (33.3%) |

The first/last rules are perfect in the 18 cases where that position is the target; on the other 18, the six same-state cases still match. Therefore merely exceeding the constant-label baseline would not demonstrate reliable batch selection. Report target position and the target-state × Other-state breakdown, with special attention to the 24 conflicting-state cases. The 12 same-state cases cannot distinguish correct target selection from reading Other.

The challenge remains a deliberately small authored control. Both formats share one target name and one three-by-three semantic cross; samples are dependent. Fixed values, fixed within-record field ordering, fixed observations values, and a single target identity permit strategies narrower than general batch binding. In particular, Rowan can be recognized as a memorized identity, and the record containing observations 7 always identifies the target. Reading an incorrect observations field alone predicts YES constantly and scores 12/36, but using that constant as a record-selection cue remains possible. Generalization across names, positive magnitudes, missing markers, alternate target identities, field orderings, record counts, or malformed/conflicting data is untested. Success supports this specific order/distractor control; it does not establish universal readout competence or token-length causality.

Reviewed bytes, SHA-256:

- CHALLENGE_CASES.json: `351a4debcb7e8896139fca53d8089736b062046c5a8c915594a5f0f54b101c7b`
- CHALLENGE_KEYS.json: `3fcac9767cc12a29b895d583c5a670982ac6e572eff25e13df35598c92535a50`
