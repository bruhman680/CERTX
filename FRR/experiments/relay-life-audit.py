"""Exact finite 4x4 torus audit. No infinite-lattice GoE or empirical-AI claims.
Predictions fixed before this extension's first execution:
1 Independent bitwise successors match all supplied successors.
2 Forward observable partitions refine and exact equality of consecutive partitions is stable.
3 Full-state depth-k past sets for distinct target states are disjoint: number of nonempty
  distinct sets equals number of depth-k reachable targets, plus one empty-set class if present.
4 Past observation-word SETS need not have monotone class counts with depth.
5 With O fixed, refining A never increases maximum deterministic TV defect (0 or 1),
  nor the share of states in ambiguous A-fibres. Finer O can expose a defect hidden by coarse O.
These are construction checks, not evidence that this is the correct model of information movement.
"""
import contextlib
import io
import json
import runpy
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "lineage/sources/claude-relay-2026-10-15/life_nodes.py"
OUT = ROOT / "evaluation/results/relay-life-audit.json"

def labels(values):
    return np.unique(values, return_inverse=True)[1]

def independent_successors():
    states = np.arange(65536, dtype=np.uint32)
    answer = np.zeros(65536, dtype=np.uint32)
    for r in range(4):
        for c in range(4):
            neighbours = np.zeros(65536, dtype=np.uint8)
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    if dr or dc:
                        j = ((r+dr) % 4)*4 + ((c+dc) % 4)
                        neighbours += ((states >> j) & 1).astype(np.uint8)
            alive = (states >> (r*4+c)) & 1
            output = (neighbours == 3) | ((neighbours == 2) & (alive == 1))
            answer |= output.astype(np.uint32) << (r*4+c)
    return answer.astype(np.int64)

def forward(o, succ, horizon=40):
    c = labels(o)
    counts = [len(np.unique(c))]
    stable = None
    for t in range(1, horizon+1):
        nxt = labels(np.stack((o, c[succ]), axis=1).view(
            np.dtype((np.void, 16))).ravel())
        counts.append(len(np.unique(nxt)))
        if counts[-1] == counts[-2] and stable is None:
            stable = t
        assert counts[-1] >= counts[-2]
        c = nxt
    assert stable is not None
    assert len(set(counts[stable-1:])) == 1
    return c, counts, stable

def backward_word_sets(o, succ, max_depth=12):
    # For every target v at depth k, exact SET of words
    # (O(u), O(f(u)), ..., O(f**(k-1)(u))) for f**k(u)=v.
    # No stationary measure, no probabilities, current O(v) excluded.
    N = len(succ)
    endpoint = np.arange(N)
    history = [tuple() for _ in range(N)]
    output = []
    partitions = {}
    for k in range(1, max_depth+1):
        history = [history[i] + (int(o[endpoint[i]]),) for i in range(N)]
        endpoint = succ[endpoint]
        sets = [set() for _ in range(N)]
        for i in range(N):
            sets[int(endpoint[i])].add(history[i])
        signatures = [frozenset(x) for x in sets]
        mapping = {}
        c = np.empty(N, dtype=np.int64)
        for i, signature in enumerate(signatures):
            if signature not in mapping:
                mapping[signature] = len(mapping)
            c[i] = mapping[signature]
        output.append({"depth": k, "past_word_set_classes": len(mapping),
                       "empty_past_states": sum(not x for x in sets),
                       "max_distinct_past_words": max(map(len, sets)),
                       "same_partition_as_previous": None if k == 1 else (
                           ambiguity(c, partitions[k-1])["max_deterministic_tv"] == 0
                           and ambiguity(partitions[k-1], c)["max_deterministic_tv"] == 0)})
        partitions[k] = c
    return output, partitions

def ambiguity(A, target):
    n = int(A.max()) + 1
    lo = np.full(n, np.iinfo(np.int64).max, dtype=np.int64)
    hi = np.full(n, -1, dtype=np.int64)
    np.minimum.at(lo, A, target)
    np.maximum.at(hi, A, target)
    bad = hi != lo
    return {"max_deterministic_tv": int(bad.any()),
            "ambiguous_fibres": int(bad.sum()),
            "total_fibres": n,
            "states_in_ambiguous_fibres": int(bad[A].sum()),
            "uniform_state_ambiguous_share": float(bad[A].mean())}

def main():
    stream = io.StringIO()
    with contextlib.redirect_stdout(stream):
        original = runpy.run_path(str(SOURCE))
    succ = original["succ"]
    assert np.array_equal(succ, independent_successors())
    N = len(succ)
    pop = original["obs"]["popcount (all cells)"]
    left = original["obs"]["left-window count (cols 0-1)"]
    observables = {"constant": np.zeros(N, dtype=np.int64), "popcount": pop,
                   "left_window_count": left, "full_state": np.arange(N, dtype=np.int64)}
    partitions = {}; forward_result = {}
    for name, o in observables.items():
        c, counts, stable = forward(o, succ)
        partitions[name] = c
        forward_result[name] = {"counts": counts, "first_equal_count_horizon": stable}
    # Independent Kahn peeling: delete transient nodes; what's left is cycles.
    indeg = np.bincount(succ, minlength=N)
    work = indeg.copy(); queue = list(np.flatnonzero(work == 0)); at = 0
    while at < len(queue):
        v = queue[at]; at += 1; w = succ[v]; work[w] -= 1
        if work[w] == 0: queue.append(int(w))
    recurrent = np.flatnonzero(work > 0)
    assert np.array_equal(recurrent, original["R"])
    endpoint = np.arange(N); preimages = []
    for k in range(1, 13):
        endpoint = succ[endpoint]
        sizes = np.bincount(endpoint, minlength=N)
        reachable = int((sizes > 0).sum())
        preimages.append({"depth": k, "reachable_states": reachable,
                          "empty_past_states": int((sizes == 0).sum()),
                          "max_ancestors": int(sizes.max()),
                          "sum_preimages": int(sizes.sum()),
                          "full_state_past_set_classes": reachable + int(reachable < N)})
    past = {}; past_comparison = []; past_membership_witness = None
    for name in ("constant", "popcount", "left_window_count"):
        rows, pcs = backward_word_sets(observables[name], succ)
        past[name] = rows
        if name == "left_window_count":
            for cls in np.unique(pcs[9]):
                members = np.flatnonzero(pcs[9] == cls)
                varied = members[pcs[10][members] != pcs[10][members[0]]]
                if len(varied):
                    past_membership_witness = {"states": [int(members[0]), int(varied[0])],
                                               "equal_past_set_at_depth_9": True,
                                               "equal_past_set_at_depth_10": False}
                    break
        for k in (1, 2, 5, 9, 12):
            # Does partition B determine forward-F class? Does F determine B?
            B, F = pcs[k], partitions[name]
            past_comparison.append({"observable": name, "past_depth": k,
                                    "B_to_F": ambiguity(B, F), "F_to_B": ambiguity(F, B)})
    A = {"constant": observables["constant"], "popcount": labels(pop),
         "popcount_and_left": labels(pop*9 + left), "left_window_count": labels(left),
         "forward_pop_stable": partitions["popcount"],
         "forward_left_stable": partitions["left_window_count"],
         "full_state": observables["full_state"]}
    defects = []; endpoint = np.arange(N)
    for t in range(13):
        for oname, o in observables.items():
            for aname, a in A.items():
                defects.append({"A": aname, "O": oname, "horizon": t,
                                **ambiguity(a, o[endpoint])})
            # State-wise ambiguity cannot grow when A is refined, for fixed O,t.
            chain = [ambiguity(A[x], o[endpoint]) for x in ("constant", "popcount", "popcount_and_left", "full_state")]
            for x, y in zip(chain, chain[1:]):
                assert y["max_deterministic_tv"] <= x["max_deterministic_tv"]
                assert y["states_in_ambiguous_fibres"] <= x["states_in_ambiguous_fibres"]
        assert ambiguity(A["forward_pop_stable"], pop[endpoint])["max_deterministic_tv"] == 0
        endpoint = succ[endpoint]
    forward_cross_witness = None
    future_left = left[succ]
    for cls in np.unique(partitions["popcount"]):
        members = np.flatnonzero(partitions["popcount"] == cls)
        varied = members[future_left[members] != future_left[members[0]]]
        if len(varied):
            u, v = int(members[0]), int(varied[0])
            forward_cross_witness = {"states": [u,v], "future_popcount_equal_all_times": True,
                                     "left_window_at_t1": [int(future_left[u]),int(future_left[v])]}
            break
    result = {"witnesses": {"perfect_popcount_not_left_window": forward_cross_witness,
                             "equal_past_counts_not_stable_partition": past_membership_witness}, "source": str(SOURCE.relative_to(ROOT)), "source_stdout": stream.getvalue(),
              "scope": "Exhaustive deterministic 4x4 periodic torus, 65536 states; no physical EPR, infinite-lattice, or AI-effectiveness inference",
              "successor_crosscheck": {"method": "independent per-cell bitwise neighbour enumeration", "states_equal": N},
              "node_statistics": {"garden_of_eden_count": int((indeg == 0).sum()),
                                  "merge_count": int((indeg >= 2).sum()), "maximum_indegree": int(indeg.max()),
                                  "recurrent_count": len(recurrent), "cycles": len(original["lens"]),
                                  "cycle_length_counts": {str(int(x)): int(y) for x,y in zip(*np.unique(original["lens"], return_counts=True))},
                                  "largest_basin": int(original["basin"].max()),
                                  "max_transient": int(original["trans"].max())},
              "forward_partitions": forward_result, "full_state_past_sets": preimages,
              "observable_past_word_sets": past, "past_forward_partition_comparison": past_comparison,
              "abstraction_observable_defects": defects,
              "checks": {"independent_successor_equal": True, "independent_recurrent_equal": True,
                         "forward_refinement_stable": True, "refinement_defect_monotonic": True}}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result["node_statistics"], indent=2))
    print("past popcount class counts:", [r["past_word_set_classes"] for r in past["popcount"]])
    print("past left-window class counts:", [r["past_word_set_classes"] for r in past["left_window_count"]])
    print("saved", OUT)

if __name__ == "__main__":
    main()
