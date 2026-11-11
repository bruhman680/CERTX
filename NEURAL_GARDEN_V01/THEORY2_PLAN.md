# THEORY2: exact budget and clipped-energy audit

## Pre-execution hypothesis

**H1.** A Garden can exhibit an approximately stationary mean *clipped* energy while the corresponding unclipped raw ecological energy budget is still negative. This would indicate that floor saturation, rather than healthy replenishment, partly explains apparent equilibrium.

For resource `r_i`, energy `e_i`, harvest action `a_i in {0,1}`, harvest frequency `p=mean(a)`, and harvest-position yield `y=mean(r*a)/p` (if `p>0`), under the inherited world laws:

`mean(raw_energy) = p*(0.25*y - 0.063) - 0.022`.

Define `z_i = e_i + raw_i`, floor correction `U=mean(max(0,-z_i))` and ceiling correction `O=mean(max(0,z_i-1))`. Then the **exact** realized energy change is:

`Delta mean clipped energy = mean(raw_energy) + U - O`.

With periodic neighbor averaging, mean resource change before resource clipping equals:

`alpha*(1-mean(r)) - 0.18*mean(r*a)`, alpha=regrowth.

## Probe and controls

- Eight new seeds 10400-10407, size 10, 600-step training with existing reserve/resource objective.
- Matched evaluation worlds seeded `seed+20000`, online stochastic vs identical-weight frozen stochastic, 3,000 steps.
- Regrowth .06 ticks 1-999, .055 ticks 1000-1999, .06 ticks 2000-3000.
- Report per-phase signed raw budget, floor/ceiling corrections, realized drift, depletion and residuals of both exact identities. Directly check whether the low-energy phase is masked by floor saturation.
- Source separate from historical checkpoint, with no mutation of original Living Garden.

**Limit:** Proving an identity and finding its operation in this synthetic model is not biological evidence or evidence of general safe learning.
