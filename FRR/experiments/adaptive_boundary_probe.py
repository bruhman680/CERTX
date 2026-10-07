"""Constructed substrate experiment, not an AI-swarm or FRR efficacy test.

Local difference-sensitive conductance is deliberately programmed. Input geometry,
readers, and targets are explicit. Equal initial geometry does not make the local
rule neutral: it directly encodes resistance to mixing different values.
"""
import json
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SETTINGS = dict(training_steps=300, dt=.2, decay=.002, adaptation=.06,
                contrast_scale=.3, conductance_floor=.02, write_steps=40,
                observation_noise=.08, calibration_cases=160, evaluation_cases=512,
                horizons=[0, 20, 80, 200, 600], sizes=[32, 64, 128], seeds=list(range(6)))


def evolve(x, w, decay=0.):
    flux = w * (np.roll(x, -1, axis=-1) - x)
    return (x + SETTINGS['dt'] * (flux - np.roll(flux, 1, axis=-1))) * (1-decay)


def prepare(n, sign=1):
    x = np.zeros(n)
    w = np.ones(n)
    for _ in range(SETTINGS['training_steps']):
        x = evolve(x, w)
        x[0], x[n//2] = sign, -sign
        delta = np.roll(x, -1) - x
        desired = SETTINGS['conductance_floor'] + (1-SETTINGS['conductance_floor']) * np.exp(-(delta/SETTINGS['contrast_scale'])**2)
        w += SETTINGS['adaptation'] * (desired-w)
    return x, w


def write_messages(messages, w):
    n = len(w)
    x = np.zeros((len(messages), n))
    for _ in range(SETTINGS['write_steps']):
        x = evolve(x, w)
        x[:, 0] = messages[:, 0]
        x[:, n//2] = messages[:, 1]
    return x


def graph_stats(w):
    n = len(w)
    L = np.zeros((n,n))
    for i in range(n):
        j = (i+1)%n
        L[i,i] += w[i]; L[j,j] += w[i]
        L[i,j] -= w[i]; L[j,i] -= w[i]
    spectrum = np.linalg.eigvalsh(L)
    return dict(fiedler=float(spectrum[1]), min_weight=float(w.min()),
                mean_weight=float(w.mean()), weak_edges=int(np.sum(w < .1)))


def decode_score(x, labels, rng):
    n = x.shape[1]
    # Fresh readers see only two local observations, not targets or training graph.
    features = x[:, [0,n//2]] + rng.normal(0, SETTINGS['observation_noise'], (len(x),2))
    features = np.column_stack([features, np.ones(len(x))])
    c = SETTINGS['calibration_cases']
    fit = np.linalg.solve(features[:c].T@features[:c]+.01*np.eye(3), features[:c].T@labels[:c])
    pred = np.where(features[c:]@fit >= 0, 1, -1)
    accuracy = np.mean(pred == labels[c:])
    opposite = labels[c:,0] != labels[c:,1]
    return dict(bit_accuracy=float(accuracy), opposite_message_accuracy=float(np.mean(pred[opposite] == labels[c:][opposite])),
                raw_local_contrast=float(np.mean(abs(x[:,0]-x[:,n//2]))))


def transmission(w):
    # Source-independent impulse and a fixed distance reveal a mixing cost.
    n = len(w)
    u = np.zeros(n); u[0] = 1
    for _ in range(200):
        u = evolve(u,w)
    # Near-neighbor beyond the trained bottleneck is an operational receiver.
    edge = int(np.argmin(w))
    v = np.zeros(n); v[edge] = 1
    for _ in range(80):
        v = evolve(v,w)
    return dict(opposite_site_impulse=float(u[n//2]),
                across_weakest_edge=float(v[(edge+1)%n]), mass=float(v.sum()))


def main():
    records=[]
    invariants=[]
    for n in SETTINGS['sizes']:
        x,w = prepare(n)
        neg,wn = prepare(n,-1)
        assert np.allclose(w,wn) and np.allclose(x,-neg)
        assert np.all((w>=SETTINGS['conductance_floor']) & (w<=1))
        # Convex stencil ensures no artificial oscillation/explosion here.
        assert SETTINGS['dt']*2 <= 1
        invariants.append(dict(size=n, sign_reversal_same_graph=True,
                               graph_cannot_discriminate_these_histories=True,
                               geometry='periodic nearest-neighbor ring',
                               stats=graph_stats(w)))
        for seed in SETTINGS['seeds']:
            rng=np.random.default_rng(seed)
            count=SETTINGS['calibration_cases']+SETTINGS['evaluation_cases']
            labels=rng.choice([-1,1],size=(count,2))
            shuffled=w[rng.permutation(n)]
            controls={'fixed_uniform':np.ones(n), 'learned_frozen':w,
                      'shuffled_learned':shuffled,
                      'uniform_same_mean':np.full(n,w.mean())}
            for name,cw in controls.items():
                state=write_messages(labels,cw)
                previous=0
                for horizon in SETTINGS['horizons']:
                    for _ in range(horizon-previous):
                        state=evolve(state,cw,SETTINGS['decay'])
                    # Same observation-noise draws by condition, paired comparison.
                    readrng=np.random.default_rng(10000+seed*1000+n+horizon)
                    records.append(dict(size=n,seed=seed,condition=name,horizon=horizon,
                                        **decode_score(state,labels,readrng)))
                    previous=horizon
            # Matched inscription isolates retention from graph-dependent writing.
            common=write_messages(labels,np.ones(n))
            for name,cw in [('common_payload_learned',w),('common_payload_shuffled',shuffled)]:
                state=common.copy()
                previous=0
                for horizon in SETTINGS['horizons']:
                    for _ in range(horizon-previous):
                        state=evolve(state,cw,SETTINGS['decay'])
                    records.append(dict(size=n,seed=seed,condition=name,horizon=horizon,
                                        **decode_score(state,labels,np.random.default_rng(10000+seed*1000+n+horizon))))
                    previous=horizon
            # Retain written field but reset its learned transport rules.
            state=write_messages(labels,w)
            for _ in range(200):
                state=evolve(state,np.ones(n),SETTINGS['decay'])
            records.append(dict(size=n,seed=seed,condition='reopen_after_write',horizon=200,
                                **decode_score(state,labels,np.random.default_rng(10000+seed*1000+n+200))))
            # Erasure includes payload; retained graph only is sign-ambiguous.
            erased=np.zeros_like(state)
            records.append(dict(size=n,seed=seed,condition='erased_payload',horizon=200,
                                **decode_score(erased,labels,np.random.default_rng(10000+seed*1000+n+200))))
    summary=[]
    for n in SETTINGS['sizes']:
        conditions=sorted({r['condition'] for r in records if r['size']==n})
        for name in conditions:
            for horizon in SETTINGS['horizons']:
                cases=[r for r in records if r['size']==n and r['condition']==name and r['horizon']==horizon]
                if cases:
                    summary.append(dict(size=n,condition=name,horizon=horizon,
                         mean_bit_accuracy=float(np.mean([r['bit_accuracy'] for r in cases])),
                         mean_opposite_accuracy=float(np.mean([r['opposite_message_accuracy'] for r in cases])),
                         seed_sd=float(np.std([r['bit_accuracy'] for r in cases])),
                         mean_local_contrast=float(np.mean([r['raw_local_contrast'] for r in cases]))))
    transfers=[]
    for n in SETTINGS['sizes']:
        _,w=prepare(n)
        # Pair exactly the same edge for learned versus restored comparison.
        edge=int(np.argmin(w))
        learned=np.zeros(n); learned[edge]=1
        restored=learned.copy()
        for _ in range(80):
            learned=evolve(learned,w); restored=evolve(restored,np.ones(n))
        transfers.append(dict(size=n,receiver=(edge+1)%n,
                              learned_received=float(learned[(edge+1)%n]),
                              restored_received=float(restored[(edge+1)%n]),
                              learned_total_mass=float(learned.sum()),restored_total_mass=float(restored.sum())))
    result=dict(kind='constructed adaptive substrate; no LLM agents',settings=SETTINGS,
                invariants=invariants,summary=summary,records=records,transfer=transfers,
                limitations=['Local contrast-based resistance is programmed, not spontaneous discovery.',
                             'Prototype preparation writes a particular contrasting input; test all pairs including agreeing inputs.',
                             'Six seeds vary messages/shuffles/noise, not six independently prepared training graphs.',
                             'Reader targets and known source locations are explicit; decoding does not establish semantic truth.',
                             'Size varies ring distance; effects are not evidence of a scale-independent swarm law.',
                             'Fixed horizon and imposed read noise make persistence operational rather than permanent.',
                             'Conductance has a positive floor; all graphs stay connected. Boundaries are weak links, not walls.',
                             'No FRR-versus-baseline reasoning, nonlinear frequency birth, or autonomous role emergence tested.'])
    out=ROOT/'evaluation/results/adaptive-boundary-expansion.json'
    out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(invariants=invariants,transfer=transfers,
                         horizon200=[s for s in summary if s['horizon']==200]),indent=2))


if __name__=='__main__':
    main()
