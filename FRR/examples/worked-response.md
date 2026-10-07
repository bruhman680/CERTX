# Illustrative response to development case D03

The accuracy demonstrates that your metric detects the inserted marker. It does not yet validate detection of coherent reasoning: the positive label determines whether the marker is present, and the score reads that same marker.

Keep the code as an instrument, but evaluate independently labeled reasoning examples without the marker. Compare against marker count, length, and other plausible simple proxies. Choose thresholds on calibration examples and evaluate once on fresh cases. A useful failure would be coherent examples scoring poorly or incoherent examples scoring highly under those conditions.

This is an authored example of the desired distinction, not a model evaluation result. Other adequate responses may use different wording or tests.
