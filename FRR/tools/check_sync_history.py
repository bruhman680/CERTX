"""Check a partial deposit log and construct a pinned navigation view, not a truth engine."""
import argparse,json
from pathlib import Path

def check(path, through=None, previous=None):
    raw=path.read_bytes()
    if previous is not None and not raw.startswith(previous.read_bytes()):
        raise ValueError('Historical byte prefix rewritten or removed')
    events=[json.loads(line) for line in raw.decode().splitlines() if line.strip()]
    assert events, 'Empty log'
    ids=set();commits=set()
    for i,event in enumerate(events):
        assert event['event_id'] not in ids and event['source_commit'] not in commits
        assert len(event['source_commit'])==40 and all(c in '0123456789abcdef' for c in event['source_commit'])
        assert event['kind']=='repository_deposit' and event['artifacts']
        if i:assert events[i-1]['source_commit'] in event['parent_commits'], 'Nonconsecutive imported branch'
        ids.add(event['event_id']);commits.add(event['source_commit'])
    missing=[]
    if through:
        idx=next((i for i,e in enumerate(events) if e['source_commit']==through),None)
        if idx is None:raise ValueError('Orientation base outside this partial log')
        missing=[e['topic'] for e in events[idx+1:]]
    return {'events':len(events),'latest_deposit':events[-1]['source_commit'],
            'orientation_uncovered_topics':missing,
            'navigation':[{'topic':e['topic'],'links':[f'https://github.com/bruhman680/CERTX/blob/{e["source_commit"]}/{p}' for p in e['artifacts']]} for e in events],
            'scope':'Structural checks of supplied records. Does not fetch artifacts, independently authenticate commits, determine claim validity, or measure AI reasoning.'}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('log',type=Path);p.add_argument('--orientation-through');p.add_argument('--previous',type=Path)
    a=p.parse_args();print(json.dumps(check(a.log,a.orientation_through,a.previous),indent=2))
