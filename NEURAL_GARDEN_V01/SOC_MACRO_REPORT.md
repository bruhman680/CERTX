# Thirteen FRR research loops — eight-state Garden coarse-graining

**Status:** Executed, including a separate untouched-seed confirmation. This is a synthetic, instrumented inquiry into information-preserving coarse descriptions of local cells—not a demonstration of consciousness, `C_symb`, or a new Markov theorem.

## The question

Our prior eight-state experiments found that collapsing distinct states can erase differences in their futures. Does that phenomenon also appear when we take *actual simulated Neural Garden trajectories*, compress each cell to a few visible symbols, and try to predict what comes next?

We define a cell's discrete microcategory by three booleans: local resource `>=.48`, energy `>=.12`, and whether it just harvested. These give **eight** categories. The simulator still has continuous resources/energy, neural recurrent memory, neighboring resources, and individual learned weights; the eight categories intentionally hide much of this state.

Data: eight training worlds (seeds4100–4107) and eight initially untouched test worlds (5100–5107), size10×10, 420 ticks, original learned v0.1 rules. The test metric is mean **negative log-likelihood of the NEXT eight-state category**, regardless of how few coarse labels we retain. Thus collapsing to one label cannot win by making the target trivial. The unit of independent replication is a world seed, not 100 cells or hundreds of time steps.

## 13 distinct representation/memory decisions

| Loop | Hypothesis/probe | Coarse labels | History lags | Heldout next-micro NLL | Weighted within-fibre TV defect |
| ---: | --- | ---: | ---: | ---: | ---: |
| 1 | Keep all eight current labels (reference) | 8 | 0 | .79198 | .00000 (vacuous) |
| 2 | Greedy merge with smallest train information loss | 7 | 0 | .79197 | .01907 |
| 3 | Merge another near-equivalent current category | 6 | 0 | .79198 | .01006 |
| 4 | Force stronger compression | 5 | 0 | .79631 | .06372 |
| 5 | Compress to four labels | 4 | 0 | .80322 | .04414 |
| 6 | Compress to three labels | 3 | 0 | .82677 | .02316 |
| 7 | Compress to two labels | 2 | 0 | .86140 | .00652 |
| 8 | Restore one previous three-label macrostate | 3 | 1 | .81078 | .02316 |
| 9 | Restore two previous macrostates | 3 | 2 | .80272 | .02316 |
| 10 | Restore three previous macrostates | 3 | 3 | .79939 | .02316 |
| 11 | Test resource bit alone | 2 | 0 | 1.37115 | .03889 |
| 12 | Test energy bit alone | 2 | 0 | .86140 | .00652 |
| 13 | Test last action bit alone | 2 | 0 | 1.41371 | .05526 |

These are 13 distinct experimental decisions on representations/memory burden, **not** 13 independently discovered laws or 13 independent datasets. The merge path is selected only on TRAIN data to minimize next-eight-state prediction error. Each row reports performance on unseen TEST seeds. When the macro partition changes, its coarse-target TV defect also changes, so defect values are *not* directly monotonic. A full eight-label partition has zero within-fibre defect simply because it has no merged fibres; it is not an assertion that the eight-state process is Markov.

The greedy three-label partition was `[0,0,1,1,0,0,2,2]`, with original 0..7 encoding the three booleans above. This retains **energy low versus high**, and differentiates resource states while energy is high, but merges action differences. The two-label optimum coincides with the **energy bit alone**. This is a descriptive result for an energy-depleting v0.1 Garden, not a universal priority ordering of observations.

## Independent confirmation and aligned-time comparison

We froze the three-label mapping *without retuning* and ran eight additional fresh worlds (seeds6100–6107). The three-label one-step heldout micro NLL was `.82459`; when predicting the same target ticks accessible to three-lag models, it was `.82125`. Including three prior coarse states reduced that to `.79758`, a gain of **`.02367` nats per predicted microcategory**, with the same target time window. The full eight-label current-only model scored `.79093` on its full test window: even three lags of our compressed partition do **not** clearly reconstruct all lost information.

Memory helps partly repair predictive loss, without restoring all omitted details. But the 81 possible three-label/four-time histories need more parameters than the three current-only rows, and the data derive from the *same simulator family*. We cannot infer true minimal sufficient memory or generalize to other policies or physical systems.

## Faithful interpretation

1. **Microstate ≠ complete simulator state.** The eight-bit category loses continuous values, neighbors, neural weights, and recurrent hidden states even before any macro merging. This is a controlled projection, not a ground-truth Markov chain.
2. **Macrostate ≠ `C_num`, `C_struct`, `C_symb`.** Those conceptual measures would need independently defined projection/measurement maps. Here each label is merely an observable energy/resource/action bin.
3. **Coarse-graining can erase predictive distinctions**, even when it reduces descriptive complexity. Reintroducing temporal history improves heldout predictive accuracy in this particular simulation.
4. **TV fibre defect and NLL test different burdens.** TV compares outgoing coarse distributions from two current eight-state microcategories merged into one macro label; NLL asks whether that compressed/memoried view predicts the original eight-valued target. A low TV defect need not imply high retained micro predictive information.
5. **All results are exploratory.** The variable cuts (.48/.12), greedy merge family, and memory depths were research choices, not preregistered; sample sizes describe variation within this simulator, not a natural phenomenon.

## Next honest pressure

Repeat with fixed-threshold `.50`, frozen neural and evolving demographic worlds; use independently held-out seeds and changed environments. Compare whether low-energy collapse makes energy dominate, whereas a viable ecological phase makes resource and neighbor context more informative. Then test explicit neighbor information before interpreting temporal memory as a required physical memory state. Maintain the eight-state lineage, distinguish lumpability from predictive sufficiency, and avoid assigning symbolic cognition labels prematurely.

**Reproducible artifacts:** `SOC_MACRO_probe.py`, `SOC_MACRO_results.json`, `SOC_MACRO_confirm.py`, `SOC_MACRO_confirm_results.json`; each study carries original source hashes and seed/horizon records. No existing Garden source was changed.
