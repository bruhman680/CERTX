"""Independent artifact/tokenizer audit. No inference or mutable world open."""
from pathlib import Path
import json,hashlib,base64,sys,os,copy
os.environ['HF_HUB_OFFLINE']='1'
from transformers import AutoTokenizer
H=Path(__file__).resolve().parent;E=H.parent;C=E/'minimal-garden-candidate-v1'
sys.path.insert(0,str(C/'world'))
from garden_world import verify_store,parse_notebook
def read(p):return json.loads(Path(p).read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def tokenhash(ids):return hashlib.sha256(json.dumps(ids).encode()).hexdigest()
def inv():return {str(p.relative_to(C)):sha(p) for p in C.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
def file_bytes(bundle,path):
    x=next(x for x in bundle['entries'] if x[0]==path);assert x[1]=='file'
    data=base64.b64decode(read(H/'world/objects'/f'{x[3]}.json')['base64'])
    assert hashlib.sha256(data).hexdigest()==x[3] and len(data)==x[4]
    return data
def feedback(batch):
    values=[]
    for o in batch['operations']:
        if o['feedback'] is not None:values.append({'channel':o['channel'],**{k:o['feedback'][k] for k in ('stdout','stderr','exit_code','boundary')}})
    return '' if not values and batch['boundary'] is None else json.dumps({'receipts':values,'boundary':batch['boundary']},ensure_ascii=False,sort_keys=True)
def main():
    before=inv();plan=read(H/'PLAN.json');results=read(H/'RESULTS.json');source=read(H/'INITIAL_ARCHIVE.json')
    initial=read(C/'run/INITIAL_MESSAGES.json');events=[read(p) for p in sorted((C/'run/events').glob('*.json'))]
    xs=[{'entry':e['human_entry'],'assistant':e['text'],'receipt':e['feedback']} for e in events]
    parent=read(C/'run/world/bundles/000031.json');initialized=read(H/'INITIAL_WORLD.json')
    init=read(H/'INITIALIZATION.json')['event'];oldpaths={x[0]:x for x in parent['entries']};newpaths={x[0]:x for x in initialized['entries']}
    checks={'canonical_at_1580_paused':read(C/'run/STATE.json')['human_entry']==1580 and read(C/'run/STATE.json')['paused'],
      'canonical_inventory_exact_before':before==read(H/'CANONICAL_BEFORE.json'),
      'parent_bundle_pinned':sha(C/'run/world/bundles/000031.json')==plan['parent_bundle_sha256'],
      'clone_parent_bundle_exact':read(H/'world/bundles/000000.json')==parent,
      'source_archive_exact':source['initial_messages']==initial and source['exchanges']==xs,
      'initial_messages_unchanged':read(H/'INITIAL_MESSAGES.json')==initial,
      'old_world_paths_preserved_except_declared_rules':all(newpaths[p]==v for p,v in oldpaths.items() if p!='WORLD_RULES.txt'),
      'new_paths_only_archive':all(p=='conversation_archive_v1' or p.startswith('conversation_archive_v1/') for p in set(newpaths)-set(oldpaths)),
      'declared_rules_content_exact':file_bytes(initialized,'WORLD_RULES.txt')==(H/'PROTOTYPE_WORLD_RULES.txt').read_bytes(),
      'original_rules_exact':(H/'ORIGINAL_WORLD_RULES.txt').read_bytes()==file_bytes(parent,'WORLD_RULES.txt'),
      'initialization_link':init['before_id']==parent['id'] and init['after_id']==initialized['id'],
      'initialization_world_event_exact':init==read(H/'world/events/000001.json'),
      'declared_pins_unchanged':all(sha(p)==v for p,v in plan['pins'].items()),
      'not_activated':not results['activation'] and read(H/'STATUS.json')['canonical_entry']==1580}
    checks['initial_archive_files_exact']=json.loads(file_bytes(initialized,'conversation_archive_v1/initial_messages.json'))==initial and all(
      json.loads(file_bytes(initialized,f"conversation_archive_v1/entries/{x['entry']:06d}.json"))==x for x in xs)
    tok=AutoTokenizer.from_pretrained('/workspace/cache_backend_models/smollm2-135m',local_files_only=True,trust_remote_code=False)
    rows=[];previous_sha=None;previous_world=initialized['id'];input_hashes=[];output_hashes=[];text_hashes=[]
    for loop in range(1,results['completed_loops']+1):
        entry=1580+loop;p=read(H/f'plans/{loop:02d}.json');raw=read(H/f'raw/{loop:02d}.json');b=read(H/f'batches/{loop:02d}.json');arch=read(H/f'archive_operations/{loop:02d}.json')['event'];r=read(H/f'records/{loop:02d}.json')
        selected=xs[-8:];expected=copy.deepcopy(initial)
        for x in selected:expected.extend([{'role':'assistant','content':x['assistant']},{'role':'user','content':x['receipt']}])
        ids=tok.apply_chat_template(expected,tokenize=True,add_generation_prompt=True)
        assert len(ids)<=7936,'Actual audited pilot should fit all8 pairs'
        action=feedback(b);ar=arch['feedback']
        delivered=action
        if ar['exit_code']!=0 or ar['boundary'] is not None:
            data=json.loads(action) if action else {'receipts':[],'boundary':None}
            data['receipts'].append({'channel':'history_archive',**{k:ar[k] for k in ('stdout','stderr','exit_code','boundary')}})
            delivered=json.dumps(data,ensure_ascii=False,sort_keys=True)
        action_record={'entry':entry,'assistant':raw['text'],'receipt':action}
        exchange={'entry':entry,'assistant':raw['text'],'receipt':delivered}
        opchecks=[]
        for o in b['operations']:
            plain={k:v for k,v in o.items() if k not in ('cell_index','source_start','source_end')}
            opchecks.append(plain==read(H/'world/events'/f"{o['step']:06d}.json"))
        local={'entry_exact':p['entry']==r['candidate_entry']==entry,
          'full_external_archive_ids_exact':p['archive_entries']==[x['entry'] for x in xs],
          'view_exact_chronological_suffix':p['view']['messages']==raw['messages']==expected,
          'included_entries_exact':p['view']['included_entries']==r['included_entries']==[x['entry'] for x in selected],
          'omitted_entries_exact':p['view']['omitted_entries']==r['omitted_entries']==[x['entry'] for x in xs[:-8]],
          'token_ids_exact':p['view']['input_token_ids']==raw['input_token_ids']==ids,
          'token_hash_exact':r['input_ids_sha256']==tokenhash(ids),
          'raw_decode_exact':tok.decode(raw['generated_token_ids'],skip_special_tokens=True)==raw['text'],
          'decoder_unchanged':raw['decoder']=='greedy_argmax' and len(raw['generated_token_ids'])<=256,
          'raw_batch_and_parse_exact':b['raw_text']==raw['text'] and b['parsed']==parse_notebook(raw['text']),
          'batch_world_copy_exact':b==read(H/'world/batches'/(b['batch_id']+'.json')),
          'model_operations_link':all(opchecks),
          'before_world_link':r['before_id']==previous_world and b['operations'][0]['before_id']==previous_world,
          'archive_follows_actual_batch':arch['before_id']==b['operations'][-1]['after_id'],
          'archive_event_exact':arch==read(H/'world/events'/f"{arch['step']:06d}.json"),
          'after_world_link':r['after_id']==arch['after_id'],
          'action_record_exact':read(H/f'action_records/{entry}.json')==action_record,
          'final_feedback_exact':r['action_feedback']==action and r['final_feedback']==delivered and read(H/f'exchanges/{entry}.json')==exchange,
          'record_hash_chain':r['previous_record_sha256']==p['previous_record_sha256']==previous_sha,
          'artifact_hashes':r['raw_sha256']==sha(H/f'raw/{loop:02d}.json') and r['batch_sha256']==sha(H/f'batches/{loop:02d}.json') and r['archive_operation_sha256']==sha(H/f'archive_operations/{loop:02d}.json'),
          'results_record_exact':results['records'][loop-1]==r}
        if ar['exit_code']==0 and ar['boundary'] is None:
            bundle=read(H/'world/bundles'/f"{arch['step']:06d}.json")
            local['successful_archive_copy_exact']=json.loads(file_bytes(bundle,f'conversation_archive_v1/entries/{entry:06d}.json'))==action_record
            local['successful_copy_only_declared_new_path']=arch['changed_paths']==[f'conversation_archive_v1/entries/{entry:06d}.json']
        rows.append({'candidate_entry':entry,'checks':local,'input_tokens':len(ids),'input_ids_sha256':tokenhash(ids),
          'output_ids_sha256':tokenhash(raw['generated_token_ids']),'text_sha256':hashlib.sha256(raw['text'].encode()).hexdigest(),
          'model_code_operations':sum(o['channel']!='note' for o in b['operations'])})
        xs.append(exchange);previous_sha=sha(H/f'records/{loop:02d}.json');previous_world=r['after_id']
        input_hashes.append(tokenhash(ids));output_hashes.append(tokenhash(raw['generated_token_ids']));text_hashes.append(rows[-1]['text_sha256'])
    checks['final_external_archive_exact']=read(H/'FINAL_ARCHIVE.json')=={'initial_messages':initial,'exchanges':xs}
    finalread=read(H/'FINAL_ARCHIVE_READ.json')['event']
    checks['final_read_follows_last_world']=finalread['before_id']==previous_world and finalread==read(H/'world/events'/f"{finalread['step']:06d}.json")
    checks['clean_pause_no_pending_or_lock']=read(H/'STATUS.json')['paused'] and not any((H/p).exists() for p in ('PENDING.json','world/PENDING.json','world/BATCH_PENDING.json','world/LOCK.json'))
    verification=verify_store(H/'world');checks['store_verify_pass']=verification['status']=='pass'
    checks['canonical_unchanged_by_audit']=before==inv()
    out={'status':'pass' if all(checks.values()) and all(all(r['checks'].values()) for r in rows) else 'fail',
      'checks':checks,'rows':rows,'world_verification':verification,
      'distinct_input_token_sequences':len(set(input_hashes)),'distinct_output_token_sequences':len(set(output_hashes)),
      'distinct_output_texts':len(set(text_hashes)),
      'identical_input_output_across_pilot':len(rows)>1 and len(set(input_hashes))==len(set(output_hashes))==1,
      'canonical_entry':1580,'model_calls':0,'world_operations':0,'canonical_writes':False,
      'limits':'Artifact/tokenizer check, not independent inference, weight reload, hard crash or durability test. Mutable archive contents are observations, not a correctness gate.'}
    (H/'AUDIT.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ('status','distinct_input_token_sequences','distinct_output_token_sequences','identical_input_output_across_pilot')}))
    assert out['status']=='pass'
if __name__=='__main__':main()
