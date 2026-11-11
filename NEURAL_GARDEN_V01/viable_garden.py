"""Neural Garden v0.3: explicit world-law viability intervention.

The only difference from v0.2 is baseline metabolism .02 instead of .03.
This *changes the world*, not just learning. It creates a positive expected
energy-drift region under homogeneous mean-field resource equilibrium:
    r*(p) = .06/(.06+.18p) = 1/(1+3p)
    drift(p) = p*(.25*r*(p)-.063) - .012
For example, at p=1/3 drift is positive (~+.00867), unlike the v0.1/v0.2
mean-field maximum (~-.00133). Actual spatial behavior remains empirical.
"""

from stewardship_garden import StewardshipGarden


class ViableGarden(StewardshipGarden):
    METABOLISM = .02
