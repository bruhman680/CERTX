"""Read-only tokenizer/artifact audit, without model weights or execution."""
from pathlib import Path
import hashlib,json,os,sys
os.environ['HF_HUB_OFFLINE']='1'
from transformers import AutoTokenizer
H=Path(__file__).resolve().parent;C=H.parent/'minimal-garden-candidate-v1'
sys.path.insert(0,str(C/'world'))
from garden_world import parse_notebook
def inv():
    return {str(p.relative_to(C)):hashlib.sha256(p.read_bytes()).hexdigest()
      for p in C.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
def read(p):return json.loads(p.read_text())
def main():
    before=inv();source=read(H/'SOURCE_ARCHIVE.json');results=read(H/'RESULTS.json')
    initial=read(C/'run/INITIAL_MESSAGES.json')
    events=[read(p) for p in sorted((C/'run/events').glob('*.json'))]
    xs=[{'entry':x['human_entry'],'assistant':x['text'],'receipt':x['feedback']} for x in events]
    tok=AutoTokenizer.from_pretrained('/workspace/cache_backend_models/smollm2-135m',local_files_only=True,trust_remote_code=False)
    checks={'source_initial_exact':source['initial_messages']==initial,
      'source_archive_exact':source['exchanges']==xs,
      'source_state_exact':source['canonical_state']==read(C/'run/STATE.json'),
      'source_count_thirty':len(xs)==30,'canonical_at_1580_paused':source['canonical_state']['human_entry']==1580 and source['canonical_state']['paused'],
      'canonical_matches_probe_before_inventory':before==read(H/'BEFORE_INVENTORY.json'),
      'exactly_three_declared_views':[r['recent_pairs'] for r in results['rows']]==[4,8,12],
      'no_code_execution_or_adoption_reported':results['code_executions']==0 and not results['policy_adopted']}
    full=initial.copy()
    for x in xs:full += [{'role':'assistant','content':x['assistant']},{'role':'user','content':x['receipt']}]
    checks['full_input_exact_8104']=len(tok.apply_chat_template(full,tokenize=True,add_generation_prompt=True))==results['full_history_input_tokens']==8104
    rows=[]
    for n in (4,8,12):
        v=read(H/f'views/recent{n}.json');raw=read(H/f'raw/recent{n}.json')
        expected=initial.copy()
        for x in xs[-n:]:expected += [{'role':'assistant','content':x['assistant']},{'role':'user','content':x['receipt']}]
        ids=tok.apply_chat_template(expected,tokenize=True,add_generation_prompt=True)
        parsed=parse_notebook(raw['text'])
        local={'complete_exact_suffix':v['messages']==expected,
          'included_ids_exact':[x['entry'] for x in xs[-n:]]==v['included_entries']==raw['included_entries'],
          'omitted_ids_exact':[x['entry'] for x in xs[:-n]]==v['omitted_entries']==raw['omitted_entries'],
          'exact_input_ids':v['input_token_ids']==ids,
          'declared_input_length':len(ids)==raw['input_tokens'],
          'fits_bound':len(ids)<=7936,
          'decoded_text_exact':tok.decode(raw['generated_token_ids'],skip_special_tokens=True)==raw['text'],
          'raw_parse_exact':raw['parsed']==parsed,
          'stop_and_cap':raw['stop']=='token_limit' and len(raw['generated_token_ids'])==raw['output_tokens']==256,
          'prior_text_match_observed':raw['text'] in {x['assistant'] for x in xs},
          'no_complete_cell':parsed['complete_executable_cells']==0,
          'results_row_matches':all(raw[k]==r[k] for r in results['rows'] if r['recent_pairs']==n for k in r)}
        rows.append({'recent_pairs':n,'checks':local,'input_tokens':len(ids),
          'output_text_sha256':hashlib.sha256(raw['text'].encode()).hexdigest()})
    checks['canonical_unchanged_by_audit']=before==inv()
    out={'status':'pass' if all(checks.values()) and all(all(x['checks'].values()) for x in rows) else 'fail',
      'checks':checks,'rows':rows,'model_calls':0,'weights_loaded':False,'code_executed':False,
      'limits':'Checks artifacts and tokenizer mapping; does not independently rerun inference or reload model weights.'}
    (H/'AUDIT.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'status':out['status'],'rows':len(rows)}));assert out['status']=='pass'
if __name__=='__main__':main()
