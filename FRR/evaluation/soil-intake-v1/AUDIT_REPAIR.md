# Audit harness repair

The first execution of the new audit harness failed with NameError: alpha is not defined, inside the source-isolated ewma_excess function. The harness loaded definitions but omitted the original module-level alpha=0.3 constant. The complete initial harness is preserved as AUDIT_INITIAL_FAILED.py. It produced no AUDIT.json scientific output. The corrected harness supplies alpha=0.3 explicitly in its isolated environment. Supplied originals and their successful unchanged reproduction remain untouched. This was an audit-wiring failure, not a failed model prediction.

A second execution completed the numerical calculations but failed JSON serialization because a check used a NumPy boolean scalar. AUDIT_SECOND_FAILED.py preserves that version. The repair converts the check dictionary to plain Python booleans before serialization; it changes no numerical calculation. Again no AUDIT.json was written before failure.
