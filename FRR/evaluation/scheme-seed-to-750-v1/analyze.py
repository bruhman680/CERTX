"""Post-block descriptive audit; no inference calls, semantic repairs or significance claims."""
from pathlib import Path
from collections import Counter
import hashlib,json,sys
D=Path(__file__).resolve().parent;G=D.parent/'source-access-three-cycle-v1';E=G/'cycle3/environment'
def read(p):return json.loads(p.read_text())
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert read(D/'COMPLETED.json')['next_step']==750
rows=[read(E/'events'/f'{i:06d}.json') for i in range(650,750)]
assert len(rows)==100 and read(E/'STATE.json')['next_step']==750
windows=[read(p) for p in sorted(D.glob('WINDOW_*_SUMMARY.json'))];assert len(windows)>=10
assert windows[0]['start_step']==650 and windows[-1]['next_step']==750 and all(0<w['calls']<=10 for w in windows)
assert all(a['next_step']==b['start_step'] for a,b in zip(windows,windows[1:]))
latest=read(E.parent/'CURRENT_VERIFY.json');checks=read(E.parent/latest['checks']);assert latest['next_step']==750 and checks['status']=='pass'
changed=[p for p,v in read(D/'before/PRIMARY_INVENTORY.json').items() if not (G/p).exists() or h(G/p)!=v]
expected=['cycle3/CURRENT_VERIFY.json','cycle3/environment/NOTEBOOK.jsonl','cycle3/environment/STATE.json','cycle3/environment/ACTIVE_RUNNER.json'];assert sorted(changed)==sorted(expected),changed
assert (E/'NOTEBOOK.jsonl').read_bytes().startswith((D/'before/NOTEBOOK.jsonl').read_bytes())
assert (E/'PAUSE').exists() and not (E/'RUN.lock').exists() and not (D/'BLOCK.lock').exists()
sessions=[read(p) for p in sorted((E/'sessions').glob('*.json')) if 650<=read(p)['start_step']<750]
assert len(sessions)==len(windows) and sum(s['calls'] for s in sessions)==100 and all(s['weights_unchanged'] and s['training_updates']==0 for s in sessions)
texts=[r['text'] for r in rows];longest=streak=1
for a,b in zip(texts,texts[1:]):
 streak=streak+1 if a==b else 1;longest=max(longest,streak)
features=lambda rs:dict(dollar_containing=sum('$' in r['text'] for r in rs),snapshot_containing=sum('snapshot' in r['text'].lower() for r in rs),seed_shelf_containing=sum('SEED SHELF' in r['text'] for r in rs),scheme_looking=sum(r['text'].lstrip().startswith('(') for r in rs))
seed=read(D/'USER_SEED.json')['text']
for r in rows:assert '\nUSER TEXT SEED (invitation within this environment):\n'+seed+'\n' in r['prompt']
for w in windows:
 subset=[r for r in rows if w['start_step']<=r['step']<w['next_step']];w['text_features']=features(subset);w['exact_unique_texts']=len({r['text'] for r in subset})
scheme=[r for r in rows if r['host_result']['kind']=='scheme_receipt']
analysis=dict(user_seed=seed,seed_present_in_all_prompts=True,seed_verbatim_replies=sum(seed in r['text'] for r in rows),conditions='User seed plus max checked window 10 and observer pause on non-note events; no causal attribution to seed alone.',status='pass',start=650,next_step=750,calls=100,windows=windows,
 host_kinds=dict(Counter(r['host_result']['kind'] for r in rows)),stops=dict(Counter(r['stop'] for r in rows)),
 scheme_submissions=len(scheme),scheme_terminal_receipts=sum(bool(r['host_result'].get('executed')) for r in scheme),
 successful_scheme_statuses=dict(Counter(r['host_result'].get('status') for r in scheme if r['host_result'].get('status') in ('COMPUTED','PUBLISHED','OBSERVED','ALIAS_DROPPED'))),
 scheme_events=[dict(step=r['step'],human_entry=r['step']+1,status=r['host_result'].get('status'),error=r['host_result'].get('result',{}).get('error'),source=r['text']) for r in scheme],
 scheme_statuses=dict(Counter(r['host_result'].get('status') for r in scheme)),
 text_features=features(rows),exact_unique_texts=len(set(texts)),longest_exact_adjacent_repeat=longest,
 max_input_tokens=max(len(r['input_token_ids']) for r in rows),max_output_tokens=max(len(r['generated_token_ids']) for r in rows),
 generated_tokens=sum(len(r['generated_token_ids']) for r in rows),generation_seconds=sum(r['seconds'] for r in rows),
 scheme_snapshot=read(E/'STATE.json')['scheme_snapshot'],
 final_bundle_matches_start=(E/'scheme_world/bundles/000649_after.json').read_bytes()==(E/'scheme_world/bundles/000749_after.json').read_bytes(),
 artifact_tables_unchanged=read(E/'scheme_world/bundles/000649_after.json')['tables']['artifacts']==read(E/'scheme_world/bundles/000749_after.json')['tables']['artifacts'],
 alias_tables_unchanged=read(E/'scheme_world/bundles/000649_after.json')['tables']['aliases']==read(E/'scheme_world/bundles/000749_after.json')['tables']['aliases'],
 final_verification=latest,parameter_checks_all_windows=True,training_updates=0,
 old_inventory_files=len(read(D/'before/PRIMARY_INVENTORY.json')),changed_old_files=changed,
 old_notebook_prefix_preserved=True,paused=True,run_lock_absent=True,legacy_unknown_attempt='Old step 492 remains unknown',
 inference='Descriptive continuation, not independent trials or evidence of weight learning. Text features are literal string counts, not internal-state measurements. The runtime executed flag indicates a terminal host event, including rejected validation; it does not establish successful guest evaluation.')
(D/'ANALYSIS.json').write_text(json.dumps(analysis,indent=2)+'\n')
print(json.dumps({k:v for k,v in analysis.items() if k not in ('windows','final_verification','scheme_events')}))
