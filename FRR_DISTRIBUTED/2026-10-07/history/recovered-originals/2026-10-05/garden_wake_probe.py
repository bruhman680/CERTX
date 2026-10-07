"""Controlled probes of the submitted TrueGardenEngine, without editing it."""
from copy import deepcopy
from statistics import mean
from true_garden_fluid_settled import TrueGardenEngine, compute_fitness


def record(g):
    s = g.snapshot()
    s['soil_count'] = len(g.soil)
    s['wake_total'] = sum(g.soil_field.values())
    s['fitness_field_delta'] = mean(
        compute_fitness(c.genome, g.fitness_table, g.soil_field)
        - compute_fitness(c.genome, g.fitness_table, {})
        for c in g.candidates.values() if c.status != 'extinct'
    ) if s['pop'] else 0.0
    return s


def compare_from_checkpoint(seed=99, start=40, horizon=100):
    g = TrueGardenEngine(K=3, mut_rate=.08, seed_rng=seed)
    g.seed()
    g.run(start)
    variants = {}
    for name, clear_field, clear_archive in (
        ('unaltered', False, False),
        ('clear_wake_field', True, False),
        ('clear_soil_archive', False, True),
        ('clear_both', True, True),
    ):
        v = deepcopy(g)
        if clear_field: v.soil_field.clear()
        if clear_archive: v.soil.clear()
        before = record(v)
        v.run(horizon)
        variants[name] = (before, record(v))
    return variants


if __name__ == '__main__':
    for start in (40, 120):
        print('checkpoint', start)
        for name, (before, after) in compare_from_checkpoint(start=start).items():
            print(name,
                  'before K,soil,wake,archive,fit_delta=',
                  tuple(round(float(before[k]), 4) for k in
                        ('K','soil_richness','wake_total','soil_count','fitness_field_delta')),
                  'after=',
                  tuple(round(float(after[k]), 4) for k in
                        ('K','soil_richness','wake_total','soil_count','fitness_field_delta')))
