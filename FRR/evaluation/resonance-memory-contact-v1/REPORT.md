# RM-C1: phase memory, information and retrieval

2026-10-25. User returned with a ResonanceDB screenshot and authorized resumed exploration. Completed: primary PDF reading (all sections and appendix), pinned repository README inspection, one predeclared formula experiment and a rational scalar check. No database installation, product-kernel execution, training or fresh-agent trial. The previous resting checkpoint remains historical.

## Source intake

[Listopad, arXiv:2509.09691v1](https://arxiv.org/abs/2509.09691v1), submitted21August2025, is the screenshot paper. It supplies amplitude/phase encoding, a deterministic score, compact operator tests and scan-based timing. Phases are externally supplied; no learned modulator is tested. Reported500K-pattern scalar timings are roughly135–145ms on the stated CPU; the paper identifies O(NL) scans and phase-noise/calibration limitations. These results do not establish general linguistic negation handling or adaptive shared memory.

[Repository README pinned at f059f06](https://github.com/LexProfi/ResonanceDB/blob/f059f06b0875f3e15ea058815202d332c772ee43/README.md) describes later phase-weighted routing and says exact current scoring details are undisclosed. Its quantum analogy is expressly descriptive. Do not equate that product with the paper formula or label this a code reproduction.

Access history: an initial guessed v2 HTML URL returned404; the arXiv record exposes v1. The v1 PDF was downloaded and converted with pdftotext. Source hashes and access records are in [SOURCES.json](SOURCES.json); PDF/text remain local source cache, not redistributed here.

## Independent analysis and executed checks

For arbitrary complex vectors, concatenate real and imaginary coordinates into real vectors u,v. This preserves all information and uses the same number of real scalars. Let c be ordinary cosine on those coordinates and R=2||u||||v||/(||u||²+||v||²). Expanding the published expression gives:

`S = R/2 + R² c/2`.

This identity extends beyond purely real inputs. At equal nonzero norms, `S=(1+c)/2`: rankings and ties are identical to ordinary cosine on these information-matched coordinates. At unequal norms, energy balance can change rankings. This does not make energy-aware scoring useless; it locates its contribution and gives a fair control. Amplitude-only cosine discards phase, so a comparison against it cannot isolate the scoring rule from information supplied to the representation.

[PLAN.md](PLAN.md) fixed seed/dimensions/scales/checks before execution. [check.py](check.py) tested1,200 constructed pairs. [RESULTS.json](RESULTS.json): all8 declared checks pass; maximum absolute real-coordinate equivalence error5.55e-16, equal-norm reduction error2.22e-16. A separate Fraction calculation gives exactly18/25=.72 for a doubled-amplitude scalar witness. Finite examples supplement the algebra; they are not a new retrieval benchmark. The same coordinator prepared and checked them, without a blinded or independent reviewer.

Development witnesses also show: supplied opposite phases distinguish records that an amplitude-only view makes identical; summing opposite records erases their separate presence; encoding both unknown and measured-zero as zero cannot distinguish them afterward. Those labels are stipulated, not learned from language. Missingness/cancellation witnesses concern lossy encodings, not a demonstrated defect in ResonanceDB storage. High similarity also does not establish correctness, authority or currency.

## What we can use

In our garden, keep record content and its status available separately from any aggregate. Matching a query's position is different from being evidence relevant to the query: a contradiction may deserve retrieval precisely because it disagrees. A single phase flip is not automatically a valid model of scoped linguistic negation.

This sharpens the saved MEM-04 direction: compare equal-information encodings; distinguish evidence coverage, correct version/status, and downstream warranted decisions; preserve contradictory originals even when an aggregate cancels. [NEXT_CONTACT.md](NEXT_CONTACT.md) makes the next design concrete. It is unexecuted and not fully registered: independently prepared source/questions, participants and budget still need freezing. No forced omission or post-summary question selection.

The optional context module receives one scoped representation reminder. Queue counts/statuses, core runtime and inquiry schema remain unchanged. No evidence here validates the old fluid-swarm constants or establishes FRR efficacy, quantum behavior, or physical diffusion of semantic memory.
