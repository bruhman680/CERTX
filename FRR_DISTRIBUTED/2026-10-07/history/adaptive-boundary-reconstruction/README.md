# Adaptive boundary expansion: reconstructed candidate

Re-engineered on 2026-10-07 from Thomas's `adaptive-boundary-expansion.png`, using the FRR v0.5 seed. This is new code built from observable constraints, not the original experiment recovered from chat history. The original figure is preserved as `original-figure.png`. No parameters were fitted to its retention curves. There is no claim of novelty or cross-domain validation.

## What the image supplies

The title declares six message/noise seeds and explicit local adaptation. The left panel has a periodic ring of roughly 64 sites, smooth preparation ramps interrupted by spikes near 0 and 32, and four weak links beside those spikes. The center compares four writing/holding protocols over up to 600 steps. The right compares 32, 64, and 128 sites at 200 steps and emphasizes common writing.

Approximate visually read endpoints at 600 steps: uniform write/hold 0.71; learned write/hold 0.53; uniform write/learned hold 0.74; shuffled write/hold 0.82. The right panel's teal bars are 1.0 at all sizes. Its legend is absent; identifying them with the center's teal protocol is an inference from consistent color use. These are visual readings, not recovered numerical data.

The image does not reveal message encoding, decoder, held-out split, edge indexing, noise distribution, adaptation equation, whether adaptation continues during holding, writing duration, shuffling operation, site spacing, seed independence, or error bars. In particular, four weak links do not specify four equal regions: this geometry nearly isolates two single sites and leaves two large arcs.

## Executable interpretation

For a ring, edge `i` joins site `i` to `(i+1) mod N`. Preparation `p` is constructed from the visible ramps and two spikes. A local target conductance is 0.02 when `abs(p[i+1]-p[i]) > 0.20`, and 1 otherwise. Starting from 1, conductance moves 20% toward its target for 60 preparation updates, then freezes. The spikes and threshold deliberately construct four weak links; they are not independently discovered structure.

The evolution rule is conservative weighted diffusion:

```
J_i = g_i (x_{i+1} - x_i)
x_i(next) = x_i + dt (J_i - J_{i-1}) + noise_i
dt = 0.20; independent Gaussian noise SD = 0.008
```

Writing lasts 80 steps. Two opposite bits are clamped at two sites after each diffusion/noise update. Only polarity is randomized; this is not an arbitrary-message corpus. Labels at other sites are defined by nearest-writer geometry, with equidistant sites and writing sites excluded. The decoder reads each site's sign. Zero receives half credit. The scorer has the intended labels, but the holding evolution does not. Labels are a constructed target; accuracy does not independently establish that this encoding is the original or generally useful.

Shuffling permutes conductances and preserves their histogram. It does not shuffle the message. Preparation is independent of message polarity. The learned field does not itself encode that polarity.

`Uniform write, learned hold`, `Uniform write, shuffled hold`, and `Uniform write, mean-matched hold` reuse exactly the uniform-written state. All protocols share writing and holding noise within a seed. The mean-matched control replaces all conductances by their mean; it distinguishes placement from a simple decrease in overall coupling. Keeping writing and holding in separate conditions prevents differences in written state from impersonating a holding effect.

## Results and the surviving relationship

The six-seed candidate reproduces four weak links and a writing penalty when writers are at the isolated spikes. It does not reproduce the original retention curves or the original perfect learned-hold bars. At 64 sites and 600 steps, candidate uniform write/hold is 0.936, learned write/hold 0.600, and common-write/learned-hold 0.936. A mismatch remains a result, rather than being removed by tuning to the image.

A fixed second set of 24 independent noise/polarity seeds extends the horizon to 2400 steps. These were not used to select parameters. At 64 sites:

| Writers | Protocol | 200 steps | 600 steps | 2400 steps |
|---|---|---:|---:|---:|
| At spikes | Uniform write + hold | 0.9903 | 0.9486 | 0.5111 |
| At spikes | Learned write + hold | 0.8035 | 0.6729 | 0.5000 |
| At spikes | Uniform write, learned hold | 0.9882 | 0.9347 | 0.5160 |
| Inside arcs | Uniform write + hold | 0.9868 | 0.9340 | 0.5062 |
| Inside arcs | Learned write + hold | 1.0000 | 1.0000 | 0.9979 |
| Inside arcs | Uniform write, learned hold | 1.0000 | 1.0000 | 0.9979 |

Moving writers and their corresponding labels by a quarter-ring retains the preparation and conductances. It changes how message regions align with boundaries. The contrast is strong in this constructed model: boundary placement can obstruct writing or protect written regions. It does not identify the unknown placement used by the original experiment. Indeed, the relocated candidate loses the original learned-writing penalty.

For spike writers, the paired learned-hold minus uniform-hold difference at 600 steps is -0.01389 with a seed bootstrap 95% interval [-0.02500, -0.00486]. This measures sensitivity across 24 noise/polarity seeds conditional on the construction. Sites are correlated and are not bootstrap units. There are only two complementary message bits; the interval is not evidence of arbitrary-message generalization.

The shuffled common-write field is worse at 200 steps but better at 2400 steps for spike writers. Ranking changes with horizon. A small spectral gap alone does not guarantee useful retention: mode alignment, written amplitude, decoder and accumulated noise also matter. The learned gap at N=64 is about 0.00118 versus 0.00963 for uniform coupling, despite its lack of a holding benefit for spike writers.

Floor sensitivity examines 0.005, 0.02, 0.1, 0.5 and 1.0 on six new seeds. The writing penalty shrinks as the floor rises. At floor 1 all six protocols agree exactly, a meaningful ablation of the prepared-field difference. These diagnostics do not select a preferred floor.

## Locating persistence

Reset all message values, retain versus erase conductance, then apply an identical fresh impulse at site 0. After 20 deterministic steps, retained-field source mass is 0.85454 versus 0.14062 after erasing the field. The response L2 difference is 0.74960. Retaining the changed field therefore changes a later response after focal state reset: a model-level wake under this declared system/field boundary.

However, a zero state stays zero in either field without input/noise. The retained conductance is independent of message polarity. This test establishes persistence of a transport constraint, not recovery of the erased message. Calling both effects memory without distinguishing their carriers would erase the important difference.

## Source weave

The functional searches covered edge-sensitive smoothing, state-dependent network change, relaxation times, environmental traces, and diffusion failures/repairs. No exact source for the supplied image was identified. Search absence is not a novelty claim. These sources supply different jobs rather than independent validations of one mechanism:

- [Perona and Malik (1990), Scale-space and edge detection using anisotropic diffusion](https://people.eecs.berkeley.edu/~malik/papers/MP-aniso.pdf): the closest mathematical relative for lowering diffusivity across strong local gradients while smoothing elsewhere. Our ring uses a thresholded, prepared-and-frozen field; it is not their evolving image PDE. The connection motivates a candidate, not recovered genealogy.
- [Catté, Lions, Morel and Coll (1992), Image Selective Smoothing and Edge Detection by Nonlinear Diffusion](https://epubs.siam.org/doi/10.1137/0729012): a repair lineage offering a noise-stable version with existence and uniqueness results. It matters if preparation is noisy or the model is extended toward a continuum. Those guarantees do not automatically transfer to this thresholded scheme.
- [Kichenassamy (1997), The Perona–Malik Paradox](https://epubs.siam.org/doi/10.1137/S003613999529558X): explains why stable-looking discretizations do not settle well-posedness of the original continuum equation. Our finite positive-weight diffusion has its own explicit conservation and stability checks; it makes no continuum-limit claim.
- [Delvenne, Lambiotte and Rocha (2015), Diffusion on networked systems is a question of time or structure](https://arxiv.org/abs/1309.4155): relates network structure and event timing to relaxation and examines when reduced descriptions work. This makes horizon and timescale serious variables; it does not establish bit-memory performance here.
- [Gross, Dommar D'Lima and Blasius (2006), Epidemic Dynamics on an Adaptive Network](https://doi.org/10.1103/PhysRevLett.96.208701): a domain-specific example of node states changing connections and altering later dynamics. Epidemic rewiring differs from prepared conductance adaptation; their bifurcation results are not imported.
- [Boldini, Civitella and Porfiri (2024), Stigmergy: from mathematical modelling to control](https://pubmed.ncbi.nlm.nih.gov/39233720/): models how environmental modifications affect swarm behavior and derives traces for target formations. It helps formulate the system/environment boundary and asks what a trace makes possible; our sites are not agents and our transport-field replay is not swarm communication.

The diffusion failure and its repair were searched explicitly, rather than citing only a favorable resemblance. Primary author copies, publisher abstracts, arXiv and bibliographic records were used; not every source's full proof was inspected.

## Next contacts

The smallest useful recovered fragment would specify where and how messages were written, whether holding readapts conductance, and what the decoder treats as a bit. Those choices separate the candidate branches demonstrated here.

Then cross writer placement, boundary placement and adaptation timing without fitting to the target curves. Compare frozen preparation, live adaptation from current message values, and a random field with matched spectrum or transport rate. The existing histogram and mean controls address only part of that rival family.

For a claim about increasing size, predeclare whether sites extend a domain at fixed spacing or refine a fixed domain. Fixed 80-step writing and fixed holding horizons do not provide equal exposure across N: diffusive times grow approximately with distance squared. Run scaled writing/horizons and richer, independently generated messages before interpreting the three sizes as transfer or uniform retention.

## Run and artifacts

Requires Python, NumPy and Matplotlib. From this directory:

```
python experiment.py
python pressure.py
```

`results/results.json` contains every six-seed score and spectral diagnostics. `results/pressure-results.json` contains independent seed scores, paired bootstrap intervals, floor sensitivity, relocated-writer results and reset/replay output. Figures are `candidate-reconstruction.png`, `matched-field-controls.png`, and `writer-placement-boundary.png` in `results/`.

Verified: exactly four weak edges for the selected preparation at each tested size; deterministic diffusion conserves total state, respects its maximum principle, and has stable Euler multipliers; identical reset/replay inputs reproduce exactly; field-only zero state remains zero. These establish execution properties of the candidate. They do not validate the missing original source or a general cognitive mechanism.
