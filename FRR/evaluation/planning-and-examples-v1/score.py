"""Separate response format, public text length, conditional choices and outcomes."""
from pathlib import Path
from collections import Counter
import json
from runtime_reference import dump_new

ROOT=Path(__file__).resolve().parent

def metrics(rows):
    return {'n':len(rows),'actions':dict(Counter(r['action'] or 'INVALID' for r in rows)),
        'grounded_answers':sum(r['grounded_answer'] for r in rows),'justified_unknown':sum(r['justified_unknown'] for r in rows),
        'resolved':sum(r['resolved_in_this_toy'] for r in rows),'invalid_actions':sum(r['end']=='INVALID_ACTION' for r in rows),
        'requests':sum(r['requested'] for r in rows),'unavailable_requests':sum(r['unavailable_request'] for r in rows),
        'unknown_policy':sum(r['end']=='UNKNOWN_POLICY' for r in rows),'unknown_tool':sum(r['end']=='UNKNOWN_TOOL' for r in rows),
        'deferred_with_evidence':sum(r['unknown_with_accessible_evidence'] for r in rows),
        'nominal_cost':sum(r['nominal_tool_cost'] for r in rows)}

def summarize(rows,probes):
    policies={}
    for policy in sorted({r['policy'] for r in rows}):
        rs=[r for r in rows if r['policy']==policy]
        policies[policy]={'total':metrics(rs),'by_kind':{k:metrics([r for r in rs if r['kind']==k]) for k in sorted({r['kind'] for r in rs})},
            'by_style':{k:metrics([r for r in rs if r['style']==k]) for k in ('lines','bracket')}}
    cells={}
    for examples in (False,True):
        for response in ('direct8','direct64','plan64'):
            ps=[p for p in probes if (p['examples'],p['response'])==(examples,response)]
            cells[('examples' if examples else 'none')+'__'+response]={'n':len(ps),
                'decision_methods':dict(Counter(p['decision']['method'] for p in ps)),
                'actions':dict(Counter(p['decision']['action'] or 'INVALID' for p in ps)),
                'nonempty_text_before_final_tag':sum(bool(p['decision']['text_before_final_tag']) for p in ps),
                'multiple_action_tags':sum(p['decision']['tag_count']>1 for p in ps),
                'token_limit_stops':sum(p['stop']=='token_limit' for p in ps),
                'input_tokens':sum(len(p['input_token_ids']) for p in ps),'output_tokens':sum(len(p['generated_token_ids']) for p in ps),
                'generation_seconds':sum(p['seconds'] for p in ps)}
    return {'policies':policies,'router_cells':cells}

def main():
    rows=[json.loads(s) for s in (ROOT/'run/ROUTES.jsonl').read_text().splitlines()]
    probes=[json.loads(s) for s in (ROOT/'run/ROUTER_RAW.jsonl').read_text().splitlines()]
    assert len(rows)==480 and len(probes)==96
    dump_new(ROOT/'run/SUMMARY.json',summarize(rows,probes))
    print(json.dumps({k:v['total'] for k,v in summarize(rows,probes)['policies'].items()},indent=2))

if __name__=='__main__':main()
