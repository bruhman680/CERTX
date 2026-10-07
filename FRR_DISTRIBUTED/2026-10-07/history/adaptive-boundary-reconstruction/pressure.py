"""Fixed independent seeds, horizon extension, and floor sensitivity; no fitting."""
from dataclasses import asdict, replace
import json
from pathlib import Path
import numpy as np
from experiment import Config, run, learn, preparation, diffuse
import matplotlib.pyplot as plt

out = Path(__file__).parent/'results'
cfg = replace(Config(), seeds=24, seed_offset=10000, horizons=(0, 200, 600, 2400))
data = run(cfg, sizes=(64,))['64']
uniform = np.array(data['per_seed_accuracy']['Uniform write + hold'])
paired = {}
for name in ('Uniform write, learned hold', 'Uniform write, shuffled hold',
             'Uniform write, mean-matched hold', 'Learned write + hold'):
    delta = np.array(data['per_seed_accuracy'][name])-uniform
    rng = np.random.default_rng(7654)
    boot = delta[rng.integers(0, cfg.seeds, (5000, cfg.seeds))].mean(axis=1)
    paired[name] = {'mean_delta': delta.mean(axis=0).tolist(),
                    'seed_bootstrap_95_interval': np.quantile(boot, [.025, .975], axis=0).tolist()}
floors = {}
for floor in (.005, .02, .1, .5, 1.0):
    local = replace(cfg, seeds=6, conductance_floor=floor, horizons=(0, 200, 600))
    floors[str(floor)] = run(local, sizes=(64,))['64']['mean_accuracy']

# Reset the message state, preserve versus erase prepared conductance, then replay
# an identical novel probe. A dynamic field effect need not store the old message.
g = learn(preparation(64), Config())
probe = np.zeros(64)
probe[0] = 1
left, right = probe.copy(), probe.copy()
for _ in range(20):
    left = diffuse(left, g, cfg.dt)
    right = diffuse(right, np.ones(64), cfg.dt)
reset = {'steps': 20, 'retained_field_source_mass': float(left[0]),
         'erased_field_source_mass': float(right[0]),
         'response_l2_difference': float(np.linalg.norm(left-right)),
         'zero_state_remains_zero': bool(np.all(diffuse(np.zeros(64), g, cfg.dt)==0))}
payload = {'independent_config': asdict(cfg), 'independent_data': data,
           'paired_differences': paired, 'floor_sensitivity': floors, 'reset_replay': reset,
           'scope': 'Bootstrap unit is a noise/message-polarity seed, not a site. Only two complementary bits; no claim of arbitrary-message generalization.'}
relocated = replace(cfg, writer_shift=16)
payload['relocated_writer_config'] = asdict(relocated)
payload['relocated_writer_data'] = run(relocated, sizes=(64,))['64']
(out/'pressure-results.json').write_text(json.dumps(payload, indent=2)+'\n')
fig, axes = plt.subplots(1, 2, figsize=(12, 4.5), layout='constrained', sharey=True)
names = ('Uniform write + hold', 'Learned write + hold', 'Uniform write, learned hold')
for ax, row, title in zip(axes, (data, payload['relocated_writer_data']),
                          ('Writers at isolated spikes', 'Writers inside broad regions')):
    for name, color in zip(names, ('#667085', '#bd5943', '#24858e')):
        ax.plot(cfg.horizons, row['mean_accuracy'][name], 'o-', label=name, color=color)
    ax.axhline(.5, color='gray', linestyle=':')
    ax.set(title=title, xlabel='Steps after writing', ylim=(.4, 1.03))
axes[0].set_ylabel('Held-out site bit accuracy')
axes[1].legend(fontsize=8)
fig.suptitle('Same prepared field, different writer placement — 24 independent seeds')
fig.savefig(out/'writer-placement-boundary.png', dpi=180)
plt.close(fig)
for name, row in data['mean_accuracy'].items():
    print(name, [round(x, 4) for x in row])
print('Reset/replay:', reset)
print('Paired learned hold delta:', paired['Uniform write, learned hold'])
print('Relocated writers, same prepared field:')
for name, row in payload['relocated_writer_data']['mean_accuracy'].items():
    print(name, [round(x, 4) for x in row])
