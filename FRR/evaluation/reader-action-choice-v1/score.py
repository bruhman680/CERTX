"""Separate free routing, forced routing, mechanical policies, and actual calls."""
from pathlib import Path
from collections import Counter
import json
from runtime_reference import dump_new

ROOT=Path(__file__).resolve().parent

def metrics(rows):
    return {'n':len(rows),'valid_actions':sum(r['action'] is not None for r in rows),
        'action_counts':dict(Counter(r['action'] or 'INVALID' for r in rows)),
        'end_counts':dict(Counter(r['end'] for r in rows)),
        'grounded_answers':sum(r['grounded_answer'] for r in rows),
        'class_matches_regardless_support':sum(r['class_correct'] for r in rows),
        'unsupported_class_matches':sum(r['class_correct'] and not r['grounded_answer'] for r in rows),
        'justified_unknown':sum(r['justified_unknown'] for r in rows),
        'unknown_with_accessible_evidence':sum(r['unknown_with_accessible_evidence'] for r in rows),
        'resolved_in_this_toy':sum(r['resolved_in_this_toy'] for r in rows),
        'requests':sum(r['requested'] for r in rows),
        'unavailable_requests':sum(r['unavailable_request'] for r in rows),
        'nominal_tool_cost':sum(r['nominal_tool_cost'] for r in rows),
        'worker_cache_hits':sum(r['worker_cache_hit'] for r in rows)}

def summarize(rows,probes):
    policies={}
    for policy in sorted({r['policy'] for r in rows}):
        rs=[r for r in rows if r['policy']==policy]
        policies[policy]={'total':metrics(rs),
            'by_kind':{k:metrics([r for r in rs if r['kind']==k]) for k in sorted({r['kind'] for r in rs})},
            'by_menu':{str(m):metrics([r for r in rs if r['menu_id']==m]) for m in sorted({r['menu_id'] for r in rs},key=str)}}
    routers={}
    for model in ('original','adapted'):
        ps=[p for p in probes if p['router']==model]
        routers[model]={'unique_probes':len(ps),'valid_free_codes':sum(p['free_key'] is not None for p in ps),
            'free_texts':dict(Counter(p['text'].strip() for p in ps)),
            'forced_codes':dict(Counter(p['forced_key'] for p in ps)),
            'free_codes':dict(Counter(p['free_key'] or 'INVALID' for p in ps)),
            'probe_seconds':sum(p['seconds'] for p in ps)}
    return {'routers':routers,'policies':policies}

def main():
    rows=[json.loads(s) for s in (ROOT/'run/ROUTES.jsonl').read_text().splitlines()]
    probes=[json.loads(s) for s in (ROOT/'run/ROUTER_RAW.jsonl').read_text().splitlines()]
    assert len(rows)==480 and len(probes)==64
    dump_new(ROOT/'run/SUMMARY.json',summarize(rows,probes))
    print(json.dumps({'routers':summarize(rows,probes)['routers'],
        'policy_totals':{k:v['total'] for k,v in summarize(rows,probes)['policies'].items()}},indent=2))

if __name__=='__main__':
    main()
