# Guard calibration and observation-noise sensitivity

2 November2026, client date. Small CPU NumPy contact while the fixed-weight model experiment runs. No model calls or training. Source reuse, not an independent generator/feature rebuild.

Reuse reviewed source definitions from claude-open-world-intake-v1; fit descriptive IND,DIFF,SHARED on noise epsilon=.05. Two separately seeded calibrations, M400 and1600,800fit plus800calibration runs per class. Empirical distance quantiles.95 and.99 share each saved calibration sample. Evaluate only known IND,DIFF,COMMON/SHARED with500runs each at true noise.025,.05,.10. Reinitialize the identical evaluation seed across noise levels so raw latent sequences and uniform noise draws are paired, changing only flip thresholds. Preserve exact observed-input hashes. No oracle probes or causal-route claims.

Fit/calibration/evaluation streams are separate. For each threshold retain all three normalized distances, candidate-set masks and descriptive labels; report correct-class compatibility, correct/wrong singleton, UNKNOWN and UNRESOLVED separately. Two calibrations are a narrow sensitivity check, not robust validation. Both quantiles and all noise cells are fixed before outputs; no selected best threshold/default.

Prospective questions: do matched-noise true-class compatibility rates stay near the empirical calibration target? How do wrong noise assumptions alter false rejection/misclassification? Is any direction consistent across both seeds/sample sizes? Expected shared-class compatibility under mismatched noise is lower at M1600 than at matched noise; no precise rate predicted. More data can strengthen rejection of the assumed observation model. A failure here does not prove the underlying descriptive pattern disappeared.

Save code/source/protocol hashes before running, all parameters, labels, distances and input hashes. This experiment preserves compact measurements and regeneration seeds, not the full A/B arrays; a hash alone is not an input backup. Future cross-version regeneration must check those hashes. All older results remain untouched.
