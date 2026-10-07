"""An explicit candidate reconstructed from a figure, not recovered source code.

Run: python experiment.py --out results
No parameters are fit to the attached retention curves.
"""
from pathlib import Path
import argparse
import json
from dataclasses import asdict, dataclass

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


@dataclass(frozen=True)
class Config:
    dt: float = 0.20
    edge_threshold: float = 0.20
    conductance_floor: float = 0.02
    adaptation_rate: float = 0.20
    preparation_steps: int = 60
    writing_steps: int = 80
    noise_sd: float = 0.008
    seeds: int = 6
    seed_offset: int = 0
    writer_shift: int = 0
    horizons: tuple = (0, 20, 80, 200, 600)


def preparation(n):
    """Visible piecewise ramps with two spikes; edge i joins i to i+1."""
    half = n // 2
    p = np.zeros(n)
    p[0], p[half] = 1.0, -1.0
    p[1:half] = np.linspace(1/3, -1/3, half-1)
    p[half+1:] = np.linspace(-1/3, 1/3, half-1)
    return p


def learn(p, cfg):
    target = np.where(np.abs(np.roll(p, -1)-p) > cfg.edge_threshold,
                      cfg.conductance_floor, 1.0)
    g = np.ones(len(p))
    for _ in range(cfg.preparation_steps):
        g += cfg.adaptation_rate * (target-g)
    return g


def diffuse(x, g, dt):
    flux = g * (np.roll(x, -1)-x)
    return x + dt * (flux-np.roll(flux, 1))


def message(n, rng, cfg):
    # Two opposite bits, randomized polarity. The writer knows only anchors.
    # Held-out labels are explicitly supplied by nearest-anchor geometry.
    polarity = rng.choice([-1.0, 1.0])
    idx = (np.arange(n)-cfg.writer_shift) % n
    d0 = np.minimum(idx, n-idx)
    d1 = np.abs(idx-n//2)
    labels = np.where(d0 < d1, polarity, -polarity)
    mask = (d0 != d1) & (idx != 0) & (idx != n//2)
    return polarity, labels, mask


def write(n, g, polarity, noise, cfg):
    x = np.zeros(n)
    for z in noise:
        x = diffuse(x, g, cfg.dt) + z
        x[cfg.writer_shift % n], x[(cfg.writer_shift+n//2) % n] = polarity, -polarity
    return x


def accuracy(x, labels, mask):
    # A zero carries half credit, avoiding an arbitrary positive tie-break.
    return float(np.mean((1 + np.sign(x[mask])*labels[mask])/2))


def hold(x, g, labels, mask, noise, cfg):
    scores = {0: accuracy(x, labels, mask)}
    for t, z in enumerate(noise, 1):
        x = diffuse(x, g, cfg.dt) + z
        if t in cfg.horizons:
            scores[t] = accuracy(x, labels, mask)
    return [scores[t] for t in cfg.horizons]


def laplacian(g):
    n = len(g)
    L = np.zeros((n, n))
    for i, weight in enumerate(g):
        j = (i+1) % n
        L[i, i] += weight
        L[j, j] += weight
        L[i, j] -= weight
        L[j, i] -= weight
    return L


def verify(cfg):
    # Verify conservation, maximum principle, and Euler spectral stability.
    rng = np.random.default_rng(90210)
    for n in (32, 64, 128):
        g = learn(preparation(n), cfg)
        assert np.sum(g < 0.1) == 4
        x = rng.normal(size=n)
        y = diffuse(x, g, cfg.dt)
        assert np.isclose(x.sum(), y.sum())
        assert y.min() >= x.min()-1e-12 and y.max() <= x.max()+1e-12
        ev = np.linalg.eigvalsh(laplacian(g))
        assert ev[0] > -1e-12 and cfg.dt*ev[-1] < 2
    # Same reset state and same field imply identical deterministic replay.
    x = rng.normal(size=64)
    g = learn(preparation(64), cfg)
    assert np.array_equal(diffuse(x, g, cfg.dt), diffuse(x.copy(), g.copy(), cfg.dt))
    # Field alone is not message storage: zero remains zero without drive/noise.
    assert np.array_equal(diffuse(np.zeros(64), g, cfg.dt), np.zeros(64))


def run(cfg, sizes=(32, 64, 128)):
    data = {}
    for n in sizes:
        learned = learn(preparation(n), cfg)
        curves = {name: [] for name in (
            'Uniform write + hold', 'Learned write + hold',
            'Uniform write, learned hold', 'Shuffled write + hold',
            'Uniform write, shuffled hold', 'Uniform write, mean-matched hold')}
        margins = []
        for seed in range(cfg.seeds):
            rng = np.random.default_rng(1000+cfg.seed_offset+seed)
            polarity, labels, mask = message(n, rng, cfg)
            writing_noise = rng.normal(0, cfg.noise_sd, (cfg.writing_steps, n))
            holding_noise = rng.normal(0, cfg.noise_sd, (max(cfg.horizons), n))
            # Permutation has a separate stream and preserves the weight histogram.
            shuffled = np.random.default_rng(2000+cfg.seed_offset+seed).permutation(learned)
            uniform = np.ones(n)
            common = write(n, uniform, polarity, writing_noise, cfg)
            conditions = {
                'Uniform write + hold': (common, uniform),
                'Learned write + hold': (write(n, learned, polarity, writing_noise, cfg), learned),
                'Uniform write, learned hold': (common, learned),
                'Shuffled write + hold': (write(n, shuffled, polarity, writing_noise, cfg), shuffled),
                'Uniform write, shuffled hold': (common, shuffled),
                'Uniform write, mean-matched hold': (common, np.full(n, learned.mean())),
            }
            margins.append({name: float(np.mean(x[mask]*labels[mask]))
                            for name, (x, _) in conditions.items()})
            for name, (x, g) in conditions.items():
                curves[name].append(hold(x.copy(), g, labels, mask, holding_noise, cfg))
        eigenvalues = np.linalg.eigvalsh(laplacian(learned))
        data[str(n)] = {
            'per_seed_accuracy': curves,
            'mean_accuracy': {k: np.mean(v, axis=0).tolist() for k, v in curves.items()},
            'write_signed_margin': margins,
            'weak_edges': np.flatnonzero(learned < 0.1).tolist(),
            'learned_spectral_gap': float(eigenvalues[1]),
            'uniform_spectral_gap': float(2-2*np.cos(2*np.pi/n)),
        }
    return data


def plot(data, cfg, out):
    colors = ['#667085', '#bd5943', '#24858e', '#9a7aac']
    names = list(data['64']['mean_accuracy'])[:4]
    fig, axes = plt.subplots(1, 3, figsize=(16, 4.5), layout='constrained')
    fig.suptitle('Candidate reconstruction — six seeds; parameters not fitted to original figure')
    p = preparation(64)
    axes[0].plot(p, label='Constructed preparation')
    axes[0].plot(learn(p, cfg), label='Locally adapted conductance')
    axes[0].set(title='Four weak links from spike gradients', xlabel='Site / outgoing edge', ylabel='State / conductance')
    axes[0].legend(fontsize=8)
    for name, color in zip(names, colors):
        values = np.array(data['64']['per_seed_accuracy'][name])
        for row in values:
            axes[1].plot(cfg.horizons, row, color=color, alpha=.12)
        axes[1].plot(cfg.horizons, values.mean(axis=0), 'o-', color=color, label=name)
    axes[1].axhline(.5, color='gray', linestyle=':')
    axes[1].set(title='Writing and holding can differ', xlabel='Steps after writing', ylabel='Held-out site bit accuracy', ylim=(.35, 1.03))
    axes[1].legend(fontsize=8)
    selected = names[:3]
    for i, (name, color) in enumerate(zip(selected, colors)):
        values = [data[str(n)]['mean_accuracy'][name][3] for n in (32, 64, 128)]
        axes[2].bar(np.arange(3)+(i-1)*.25, values, width=.25, color=color, label=name)
    axes[2].set(xticks=np.arange(3), xticklabels=['32', '64', '128'], ylim=(0, 1.03), title='200 steps; fixed site-time scale', xlabel='Sites (not AI agents)', ylabel='Held-out site bit accuracy')
    fig.savefig(out/'candidate-reconstruction.png', dpi=180)
    plt.close(fig)
    fig, ax = plt.subplots(figsize=(8, 4.5), layout='constrained')
    for name in list(data['64']['mean_accuracy'])[0:1]+list(data['64']['mean_accuracy'])[2:3]+list(data['64']['mean_accuracy'])[4:]:
        ax.plot(cfg.horizons, data['64']['mean_accuracy'][name], 'o-', label=name)
    ax.set(title='Same written state and noise; only holding field changes', xlabel='Steps after writing', ylabel='Held-out site bit accuracy', ylim=(.35, 1.03))
    ax.axhline(.5, color='gray', linestyle=':')
    ax.legend(fontsize=8)
    fig.savefig(out/'matched-field-controls.png', dpi=180)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, default=Path(__file__).parent/'results')
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    cfg = Config()
    verify(cfg)
    data = run(cfg)
    (args.out/'results.json').write_text(json.dumps({'config': asdict(cfg), 'data': data}, indent=2)+'\n')
    plot(data, cfg, args.out)
    for n, result in data.items():
        print(n, 'sites; weak edges:', result['weak_edges'])
        for name, scores in result['mean_accuracy'].items():
            print(' ', name, ':', ', '.join(f'{v:.3f}' for v in scores))


if __name__ == '__main__':
    main()
