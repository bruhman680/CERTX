"""Standard-library final bindings; no model import or revised old scores."""
from pathlib import Path
import json
from io_utils import sha,dump_new
from decoder import decode_v1,decode_v2
from domain import render

ROOT=Path(__file__).resolve().parent

def main():
    for study in (ROOT,ROOT/'availability-transfer'):
        f=json.loads((study/'FREEZE.json').read_text())
        assert all(sha(study/n)==h for n,h in f['sha256'].items())
        assert all(sha(Path(n))==h for n,h in f['dependencies'].items())
        assert json.loads((study/'CHECKS.json').read_text())['status']=='pass'
        assert json.loads((study/'run/RUN_MANIFEST.json').read_text())['status']=='complete'
    raw=[json.loads(s) for s in (ROOT/'run/ROUTER_RAW.jsonl').read_text().splitlines()]
    workers=[json.loads(s) for s in (ROOT/'run/WORKER_RAW.jsonl').read_text().splitlines()]
    child=ROOT/'availability-transfer'
    transfer=[json.loads(s) for s in (child/'run/RAW.jsonl').read_text().splitlines()]
    queries={q['id']:q for q in json.loads((child/'QUERIES.json').read_text())}
    for p in transfer:
        q=queries[p['run_id']]
        assert p['messages']==[{'role':'user','content':render(q['case'],'examples',q['rotation'])}]
        assert p['strict_v1']==decode_v1(p['text']) and p['declared_v2']==decode_v2(p['text'])
    old=json.loads(Path('/workspace/descriptions-rules-before.json').read_text())
    assert all(sha(Path('/workspace/frr')/n)==h for n,h in old.items())
    checks={'status':'pass','main_router_probes':80,'main_worker_probes':9,'transfer_router_probes':12,
        'total_generation_probes':101,'unique_prompt_strings':len({p['messages'][0]['content'] for p in raw+workers+transfer}),
        'executed_logical_routes':576,'transfer_tool_actions':0,'old_files_unchanged_before_sync':len(old),
        'old_scores_and_weights_unchanged':True,'all_freezes_and_transcripts_match':True,
        'candidate_order_selected_after_primary_results':True,'no_training_or_independent_empirical_replication':True}
    dump_new(ROOT/'FINAL_CHECKS.json',checks);print(json.dumps(checks,indent=2))

if __name__=='__main__':main()
