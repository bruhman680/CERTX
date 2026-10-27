#!/usr/bin/env python3
"""Independent artifact audit; never imports experiment.py or executes its main."""
import argparse
from collections import defaultdict
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations, product
import json
from pathlib import Path

NAMES = ('P', 'C', 'R', 'M')
VARIABLES = ('T', 'qP', 'qR', 'X', 'Y', 'u', 'v')


def freeze(x):
    return tuple(map(freeze, x)) if isinstance(x, list) else x


def audit_prior(data):
    p, r = F(data['pP']), F(data['pR'])
    worlds = data['worlds']
    assert len(worlds) == 128
    observations, target, weight = {}, {}, {}
    for i, bits in enumerate(product((0, 1), repeat=7)):
        row = worlds[i]
        assert row['world_id'] == i
        assert tuple(row['latent'][v] for v in VARIABLES) == bits
        t, a, b, x, y, u, v = bits
        observation = (x, (a, x ^ t if a else u), y, (b, y ^ t if b else v))
        mass = F(1, 32) * (p if a else 1-p) * (r if b else 1-r)
        assert tuple(freeze(row['observations'][n]) for n in NAMES) == observation
        assert F(row['probability']) == mass
        observations[i], target[i], weight[i] = observation, t, mass
    positive = tuple(i for i in weight if weight[i])
    assert sum(weight.values()) == 1
    assert data['positive_weight_microstates'] == len(positive)

    def mass(ids):
        return sum((weight[i] for i in ids), F(0))

    def certify(ids):
        targets = {target[i] for i in ids}
        assert targets
        return next(iter(targets)) if len(targets) == 1 else None

    def groups(ids, index):
        out = defaultdict(list)
        for i in ids:
            out[observations[i][index]].append(i)
        return {obs: tuple(group) for obs, group in out.items()}

    @lru_cache(None)
    def independently_solve(ids, available, budget):
        best = (F(certify(ids) is not None), F(0), 'STOP')
        if budget:
            for index in available:
                success, cost = F(0), F(1)
                rest = tuple(j for j in available if j != index)
                for child in groups(ids, index).values():
                    q, c, _ = independently_solve(child, rest, budget-1)
                    ratio = mass(child)/mass(ids)
                    success += ratio*q
                    cost += ratio*c
                if (success, -cost) > (best[0], -best[1]):
                    best = success, cost, NAMES[index]
        return best

    states_checked = 0
    def inspect_states(states):
        nonlocal states_checked
        for sid, state in states.items():
            ids = tuple(state['support_world_ids'])
            assert ids and tuple(sorted(set(ids))) == ids
            assert all(weight[i] > 0 for i in ids)
            budget, mask = state['remaining_budget'], state['queried_mask']
            assert sid == f'b{budget}_m{mask:01x}_w{sum(1 << i for i in ids):032x}'
            available = tuple(j for j in range(4) if not mask & (1 << j))
            assert state['queried_records'] == [n for j,n in enumerate(NAMES) if mask & (1 << j)]
            assert F(state['prior_mass']) == mass(ids)
            assert state['certified_T'] == certify(ids)
            assert state['feasible_T'] == sorted({target[i] for i in ids})
            assert {q['world_id']: F(q['probability']) for q in state['posterior']} == {i: weight[i]/mass(ids) for i in ids}
            # Unresolved target posterior must be exactly uniform, not merely uncertain.
            if certify(ids) is None:
                assert sum((weight[i] for i in ids if target[i] == 0), F(0)) == mass(ids)/2
            expected = independently_solve(ids, available, budget)
            assert (F(state['resolution_probability']), F(state['expected_additional_cost']), state['chosen_action']) == expected
            allowed = ['STOP'] + ([NAMES[j] for j in available] if budget else [])
            assert [a['action'] for a in state['actions']] == allowed
            for action in state['actions']:
                if action['action'] == 'STOP':
                    q, c = F(certify(ids) is not None), F(0)
                    assert action['branches'] == []
                else:
                    index = NAMES.index(action['action'])
                    children = groups(ids, index)
                    branches = {freeze(b['observation']): b for b in action['branches']}
                    assert set(branches) == set(children) and len(branches) == len(action['branches'])
                    q, c = F(0), F(1)
                    for obs, child in children.items():
                        branch = branches[obs]
                        child_state = states[branch['child_state']]
                        assert tuple(child_state['support_world_ids']) == child
                        assert child_state['remaining_budget'] == budget-1
                        assert child_state['queried_mask'] == mask | (1 << index)
                        ratio = mass(child)/mass(ids)
                        assert F(branch['conditional_probability']) == ratio
                        v = independently_solve(child, tuple(j for j in available if j != index), budget-1)
                        q += ratio*v[0]
                        c += ratio*v[1]
                assert F(action['resolution_probability']) == q
                assert F(action['expected_additional_cost']) == c
            states_checked += 1

    inspect_states(data['belief_states'])
    inspect_states(data['quality_informed_belief_states'])

    # Check duplicate-world tables independently, counting zero-mass worlds too.
    for indices, table in [((j,), data['duplicate_observations']['per_record'][n]) for j,n in enumerate(NAMES)] + [(tuple(range(4)), data['duplicate_observations']['joint_all_four'])]:
        expected_groups = defaultdict(list)
        for i in range(128):
            expected_groups[tuple(observations[i][j] for j in indices)].append(i)
        assert len(table) == len(expected_groups)
        for row in table:
            ids = expected_groups[freeze(row['observation'])]
            assert row['world_ids'] == ids
            assert row['raw_microstate_count'] == len(ids)
            assert row['positive_weight_microstate_count'] == sum(weight[i] > 0 for i in ids)
            assert F(row['probability']) == mass(ids)

    def replay(states, initial, ids, budget):
        success, cost = F(0), F(0)
        leaves = defaultdict(lambda: F(0))
        for i in ids:
            sid, path, spent = initial, [], 0
            while True:
                state = states[sid]
                assert i in state['support_world_ids']
                action = state['chosen_action']
                if action == 'STOP':
                    certificate = certify(tuple(state['support_world_ids']))
                    if certificate is not None:
                        assert certificate == target[i]
                        success += weight[i]
                    cost += weight[i]*spent
                    leaves[(tuple(path), sid, spent, certificate)] += weight[i]
                    break
                assert spent < budget
                index = NAMES.index(action)
                assert index not in [j for j, _ in path]
                obs = observations[i][index]
                branch = [b for b in state['actions'] if b['action'] == action][0]['branches']
                matches = [b for b in branch if freeze(b['observation']) == obs]
                assert len(matches) == 1
                path.append((index, obs))
                sid, spent = matches[0]['child_state'], spent+1
        return success, cost, leaves

    for budget, root in enumerate(data['roots']):
        assert root['budget'] == budget
        root_state = data['belief_states'][root['root_state']]
        assert tuple(root_state['support_world_ids']) == positive
        assert (root_state['queried_mask'],root_state['remaining_budget']) == (0,budget)
        exact = independently_solve(positive, (0,1,2,3), budget)
        assert (F(root['resolution_probability']), F(root['expected_query_cost']), root['chosen_action']) == exact
        q, c, leaves = replay(data['belief_states'], root['root_state'], positive, budget)
        assert (q,c) == exact[:2]
        saved = {}
        for leaf in root['terminal_outcomes']:
            assert leaf['feasible_T'] == data['belief_states'][leaf['terminal_state']]['feasible_T']
            path = tuple((NAMES.index(step['record']), freeze(step['observation'])) for step in leaf['path'])
            key = path, leaf['terminal_state'], leaf['query_cost'], leaf['certified_T']
            assert key not in saved
            saved[key] = F(leaf['probability'])
        assert saved == leaves
        fixed = root['fixed_subset_baseline']
        expected_subsets = list(subset for size in range(budget+1) for subset in combinations(range(4), size))
        assert len(fixed['all_subsets']) == len(expected_subsets)
        values = []
        for subset, row in zip(expected_subsets, fixed['all_subsets']):
            buckets = defaultdict(list)
            for i in positive:
                buckets[tuple(observations[i][j] for j in subset)].append(i)
            resolution = sum((mass(ids) for ids in buckets.values() if certify(ids) is not None), F(0))
            assert row['records'] == [NAMES[j] for j in subset]
            assert row['query_cost'] == len(subset)
            assert F(row['resolution_probability']) == resolution
            outcome_map = {freeze(o['observations']):o for o in row['outcomes']}
            assert set(outcome_map) == set(buckets) and len(outcome_map) == len(row['outcomes'])
            for obs, ids in buckets.items():
                outcome = outcome_map[obs]
                assert outcome['support_world_ids'] == ids
                assert F(outcome['probability']) == mass(ids)
                assert outcome['certified_T'] == certify(ids)
                assert outcome['feasible_T'] == sorted({target[i] for i in ids})
            values.append((resolution, -len(subset)))
        assert fixed['best'] == fixed['all_subsets'][max(range(len(values)), key=values.__getitem__)]
        assert F(root['resolution_advantage_over_best_fixed_subset']) == q-F(fixed['best']['resolution_probability'])
        oracle = root['quality_informed_oracle']
        oq, oc = F(0), F(0)
        quality_pairs = set()
        for branch in oracle['quality_branches']:
            pair = branch['qP'], branch['qR']
            assert pair not in quality_pairs
            quality_pairs.add(pair)
            ids = tuple(i for i in positive if (worlds[i]['latent']['qP'], worlds[i]['latent']['qR']) == pair)
            assert F(branch['probability']) == mass(ids)
            state = data['quality_informed_belief_states'][branch['state']]
            assert tuple(state['support_world_ids']) == ids
            assert (state['queried_mask'],state['remaining_budget']) == (0,budget)
            a,b,_ = independently_solve(ids, (0,1,2,3), budget)
            assert (F(branch['resolution_probability']), F(branch['expected_query_cost'])) == (a,b)
            rq, rc, _ = replay(data['quality_informed_belief_states'], branch['state'], ids, budget)
            assert (rq,rc) == (mass(ids)*a,mass(ids)*b)
            oq,oc = oq+rq,oc+rc
        assert sum(F(b['probability']) for b in oracle['quality_branches']) == 1
        assert (F(oracle['resolution_probability']), F(oracle['expected_query_cost'])) == (oq,oc)
        a,b,s = max(p,r),min(p,r),p+r-p*r
        predicted_adaptive = ((F(0),F(0)) if budget < 2 or not s else (a,1+a) if budget == 2 else (s,2+b-p*r))
        predicted_fixed = ((F(0),0) if budget < 2 or not s else (a,2) if budget < 4 else (s,4))
        predicted_oracle = (s,2*s) if budget >= 2 else (F(0),F(0))
        assert (q,c) == predicted_adaptive
        assert (F(fixed['best']['resolution_probability']),fixed['best']['query_cost']) == predicted_fixed
        assert (oq,oc) == predicted_oracle
    return {'prior': data['prior'], 'worlds_checked':128, 'belief_states_checked':states_checked, 'root_budgets_checked':5, 'status':'PASS'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('results', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    data = json.loads(args.results.read_text())
    assert data['record_order'] == list(NAMES)
    assert data['latent_order'] == list(VARIABLES)
    assert [(d['prior'],F(d['pP']),F(d['pR'])) for d in data['priors']] == [('FAIR',F(1,2),F(1,2)),('PRIMARY_FAVORED',F(3,4),F(1,4)),('REFERENCE_FAVORED',F(1,4),F(3,4)),('BOTH_BAD',F(0),F(0))]
    report = {'status':'PASS', 'method':'Standalone exact reconstruction from saved latent worlds; independent DP; full state/action inspection; per-world policy replay; prospective formula checks. Does not import main implementation. Reviewer previously read main source; this is not a blinded replication.', 'priors':[audit_prior(prior) for prior in data['priors']]}
    args.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
