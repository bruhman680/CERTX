# Optional measurement-compatibility receipt

Added after [big three-step cycle](../evaluation/big-three-cycle-v1/REPORT.md). This is a small pure-Python utility, not a fitted guard or default control policy. See measurement_compatibility.py.

Supply accepted descriptive-class/measurement-setting pairs and independently allowed measurement settings. The helper records an empty calibration grid, absence of a compatible retained pair, multiple surviving classes, or one compatible class. An empty calibration grid can result from sampling error, a coarse candidate grid or misspecified calibration; it does not prove which. No compatible pair also does not identify the causal reason. One surviving class only means compatibility within the supplied alternatives.

The helper never fetches evidence, knows the true class, estimates a confidence interval, adjusts thresholds or trains a model. Accepted pair sets and independent measurement information remain the caller's responsibility. Unit tests cover distinct empty conditions, ambiguity, filtered support, duplicate pairs and invalid classes. An artifact audit reconstructs108,000saved decisions. Research runners remain frozen and are not retrospectively refactored into this helper.
