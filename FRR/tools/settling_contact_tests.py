"""Focused checks for canon batch 3; no model inference or external validation."""
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    results = []
    # Fixed row: alpha' = alpha*Z/(Z+B), B>0, decreases.
    old_scores = [2, 0]
    z = sum(math.exp(s) for s in old_scores)
    alpha = math.exp(2) / z
    added_mass = 10 * math.exp(0)
    after = math.exp(2) / (z + added_mass)
    assert after < alpha
    assert math.isclose(after, alpha * z / (z + added_mass))
    results.append(dict(id='fixed_row_dilution', before=alpha, after=after,
                        scope='Fixed query and original scores; positive added exponential mass.'))

    # For m tokens, score first token log(4*(m-1)), others 0: alpha=0.8.
    rows = []
    for m in [2, 10, 100, 1000]:
        score = math.log(4 * (m - 1))
        a = math.exp(score) / (math.exp(score) + m - 1)
        assert math.isclose(a, .8)
        rows.append(dict(tokens=m, target_score=score, target_attention=a))
    results.append(dict(id='normalization_not_universal_decay', rows=rows,
                        scope='Constructed changing queries/scores; no claim that an actual model follows this family.'))

    # The v1.1 displayed average tuple is not a tuple yielding its reported CQ.
    c, e, r, t, d = .72, .82, .98, .55, .05
    cq = c * r * (1-d) / (e*t)
    t_for_3_2 = c * r * (1-d) / (e*3.2)
    assert not math.isclose(cq, 3.2, rel_tol=.1)
    results.append(dict(id='cq_tuple', formula_at_printed_values=cq,
                        printed_cq=3.2, required_t_for_tuple=t_for_3_2,
                        scope='Ratio at means is not mean of ratios; this check alone does not falsify a reported time average.'))

    # Claimed optimal drift range does not contain this quadratic's maximum.
    k, maximum = 2.8, .3
    multiplier = lambda drift: 1 + k*drift*(1-drift/maximum)
    optimum = maximum / 2
    assert optimum == .15
    assert multiplier(.15) > multiplier(.12)
    results.append(dict(id='drift_model_optimum', optimum=optimum,
                        gain_at_0_12=multiplier(.12)-1,
                        scope='Maximum of displayed novelty model only; an unmodeled cost can change an efficiency optimum.'))

    # AF-22 calls this frequency, but the expression falls with increasing D.
    frequency = lambda drift: 1/(drift+.01)
    assert frequency(.2) < frequency(.05)
    results.append(dict(id='scan_frequency_direction', at_0_05=frequency(.05),
                        at_0_20=frequency(.2),
                        scope='If this were an interval rather than frequency, interpretation would differ.'))

    # High-E history values do not lie in the written high-E bands.
    assert not (.82 > .85) and not (.72 < .70) and not (3.4 <= 3.2 <= 3.6)
    results.append(dict(id='high_e_membership', e_passes=False, c_passes=False,
                        cq_passes=False,
                        scope='The displayed mode averages do not satisfy their described bands; full trajectories are unavailable.'))

    out = ROOT / 'evaluation/results/settling-contact.json'
    out.write_text(json.dumps(dict(kind='focused local mathematical checks',
                                  model_comparison=False, results=results), indent=2)+'\n')
    print(f'{len(results)} focused checks completed; {out}')


if __name__ == '__main__':
    main()
