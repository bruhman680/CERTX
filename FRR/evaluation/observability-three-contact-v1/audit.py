"""Read-only artifact/tokenizer audit; no model weights, inference, or world open."""
from pathlib import Path
import hashlib,json,base64,copy,sys,os,re
os.environ['HF_HUB_OFFLINE']='1'
from transformers import AutoTokenizer
H=Path(__file__).resolve().parent;E=H.parent;C=E/'minimal-garden-candidate-v1';P=E/'bounded-view-continuation-prototype-v1'
sys.path.insert(0,str(C/'world'))
from garden_world import parse_notebook,verify_store
def read(p):return json.loads(Path(p).read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def inv():return {str(p.relative_to(C)):sha(p) for p in C.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
def ids_hash(x):return hashlib.sha256(json.dumps(x).encode()).hexdigest()
def feedback(batch):
    values=[{'channel':o['channel'],**{k:o['feedback'][k] for k in ('stdout','stderr','exit_code','boundary')}}
      for o in batch['operations'] if o['feedback'] is not None]
    return '' if not values and batch['boundary'] is None else json.dumps({'receipts':values,'boundary':batch['boundary']},ensure_ascii=False,sort_keys=True)
def bytes_at(store,bundle,path):
    x=next(x for x in bundle['entries'] if x[0]==path);assert x[1]=='file'
    b=base64.b64decode(read(store/'objects'/f'{x[3]}.json')['base64'])
    assert hashlib.sha256(b).hexdigest()==x[3] and len(b)==x[4]
    return b
def main():
    before=inv();worker=read(H/'WORKER_PLAN.json');results=read(H/'RESULTS.json')
    jobs=sum((read(H/g/'jobs.json') for g in ('retrieval','observation','decoder')),[])
    tok=AutoTokenizer.from_pretrained('/workspace/cache_backend_models/smollm2-135m',local_files_only=True,trust_remote_code=False)
    checks={'canonical_matches_before':before==read(H/'CANONICAL_BEFORE.json'),
      'main_paused_at_1580':read(C/'run/STATE.json')['human_entry']==1580 and read(C/'run/STATE.json')['paused'],
      'worker_source_unchanged':sha(H/'worker.py')==worker['source_sha256'],
      'common_source_unchanged':sha(H/'common.py')==worker['common_sha256'],
      'declared_jobs_exact':jobs==worker['jobs'],
      'twelve_unique_case_ids':len(jobs)==len({j['case_id'] for j in jobs})==12,
      'planned_and_actual_fifteen':sum(j['max_turns'] for j in jobs)==worker['planned_generations']==results['actual_model_generations']==len(results['rows'])==15,
      'profile_one_pass_reported':results['teacher_forced_profile_passes']==worker['teacher_forced_profile_passes']==1,
      'not_activated':not results['activation'],'no_pending':not (H/'PENDING.json').exists() and not results['pending']}
    rows=[];initial_bundles={};outputs={};first_ids={};all_result_rows=[]
    for job in jobs:
        case=job['case_id'];assert re.fullmatch(r'[A-Za-z0-9_]+',case)
        store=Path(job['world_store']);assert store.resolve().is_relative_to(H.resolve())
        messages=copy.deepcopy(job['messages']);previous_after=None;outputs[case]=[]
        for turn in range(1,job['max_turns']+1):
            out=H/'results'/case;plan=read(out/f'plan{turn}.json');raw=read(out/f'raw{turn}.json');batch=read(out/f'batch{turn}.json');row=read(out/f'result{turn}.json')
            ids=tok.apply_chat_template(messages,tokenize=True,add_generation_prompt=True)
            before_bundle=read(store/'bundles'/plan['world_state']['bundle'])
            if turn==1:initial_bundles[case]=before_bundle;first_ids[case]=ids
            ops=batch['operations'];operation_checks=[];chain=before_bundle['id']
            for o in ops:
                plain={k:v for k,v in o.items() if k not in ('cell_index','source_start','source_end')}
                operation_checks.append(plain==read(store/'events'/f"{o['step']:06d}.json") and o['before_id']==chain)
                chain=o['after_id']
            projected=feedback(batch)
            expected_ops=[{'channel':o['channel'],'feedback':o['feedback'],'changed_paths':o['changed_paths']} for o in ops]
            local={'case_and_turn':row['case_id']==case and row['turn']==turn,
              'metadata_remains_external':row['metadata']==job['metadata'],
              'exact_actual_input_messages':plan['messages']==raw['messages']==messages,
              'exact_rendered_input_ids':raw['input_token_ids']==ids,
              'input_count_hash':row['input_tokens']==len(ids) and row['input_sha256']==ids_hash(ids),
              'within_input_budget':len(ids)<=7936,
              'decoder_matches_job':raw['decoder']==job['decoder'] and raw['seed']==job.get('seed') and raw['temperature']==job.get('temperature') and raw['top_p']==job.get('top_p'),
              'decoded_text_exact':tok.decode(raw['generated_token_ids'],skip_special_tokens=True)==raw['text'],
              'output_stop_valid':(raw['stop']=='eos' and raw['generated_token_ids'][-1]==tok.eos_token_id) or (raw['stop']=='token_limit' and len(raw['generated_token_ids'])==256),
              'output_count_hash':row['output_tokens']==len(raw['generated_token_ids']) and row['text_sha256']==hashlib.sha256(raw['text'].encode()).hexdigest(),
              'batch_exact_raw_parse':batch['raw_text']==raw['text'] and batch['parsed']==parse_notebook(raw['text']),
              'batch_world_copy_exact':batch==read(store/'batches'/(batch['batch_id']+'.json')),
              'all_operations_and_chain_exact':all(operation_checks),
              'world_before_after':row['before_id']==before_bundle['id'] and row['after_id']==chain,
              'followup_world_continuity':previous_after is None or previous_after==before_bundle['id'],
              'real_feedback_projection':row['feedback']==projected,
              'operation_summary_exact':row['operations']==expected_ops,
              'cell_and_fence_counts':row['complete_cells']==batch['parsed']['complete_executable_cells'] and row['incomplete_fences']==sum(not c['complete'] for c in batch['parsed']['cells'])}
            rows.append({'case_id':case,'turn':turn,'checks':local,'input_sha256':ids_hash(ids),
              'output_ids_sha256':ids_hash(raw['generated_token_ids']),'text_sha256':row['text_sha256']})
            outputs[case].append({'ids':raw['generated_token_ids'],'input_ids':ids,'text':raw['text'],'feedback':projected})
            all_result_rows.append(row);previous_after=row['after_id']
            messages.extend([{'role':'assistant','content':raw['text']},{'role':'user','content':projected}])
        state=read(store/'STATE.json')
        checks['clean_store_'+case]=state['paused'] and not state['faulted'] and not any((store/x).exists() for x in ('LOCK.json','PENDING.json','BATCH_PENDING.json')) and verify_store(store)['status']=='pass'
    checks['aggregate_results_exact_order']=all_result_rows==results['rows']
    retrieval={j['case_id']:j for j in jobs if j['case_id'].startswith('retrieval_')}
    values={case:j['metadata']['expected_value'] for case,j in retrieval.items()}
    a=retrieval['retrieval_hidden_a'];b=retrieval['retrieval_hidden_b'];provided=retrieval['retrieval_provided_a']
    checks['hidden_initial_messages_and_ids_same']=a['messages']==b['messages'] and first_ids[a['case_id']]==first_ids[b['case_id']]
    checks['hidden_nonces_absent_from_all_prompt_text']=all(value not in json.dumps(j['messages'],ensure_ascii=False) for j in (a,b) for value in set(values.values()))
    files={case:{x[0]:x for x in initial_bundles[case]['entries']} for case in retrieval}
    differences=sorted(k for k in set(files[a['case_id']])|set(files[b['case_id']]) if files[a['case_id']].get(k)!=files[b['case_id']].get(k))
    checks['hidden_supported_world_diff_only_target_file']=differences==['probe_value.json']
    checks['provided_and_hidden_a_supported_world_same']=files[a['case_id']]==files[provided['case_id']]
    checks['hidden_files_have_declared_values']=all(json.loads(bytes_at(Path(j['world_store']),initial_bundles[case],'probe_value.json'))['value']==values[case] for case,j in retrieval.items())
    receipt_record=read(H/'retrieval/preparation/retrieval_provided_a_read.json');event=receipt_record['event'];store=Path(provided['world_store'])
    actual={'actor':'operator','channel':'python',**{k:event['feedback'][k] for k in ('stdout','stderr','exit_code','boundary')}}
    msg=json.loads(provided['messages'][-1]['content'])
    checks['supplied_read_is_actual_operator_receipt']=event==read(store/'events'/f"{event['step']:06d}.json") and msg['operator_read_receipt']==actual and actual['stdout']==values[provided['case_id']]+'\n' and actual['exit_code']==0 and event['changed_paths']==[]
    checks['same_retrieval_task_in_all_conditions']=len({json.loads(j['messages'][-1]['content'])['operator_task'] for j in retrieval.values()})==1
    obs={j['case_id']:j for j in jobs if j['case_id'].startswith('obs_')}
    checks['observation_base_role_text_same']=all(j['messages'][:-1]==obs['obs_label']['messages'][:-1] for j in obs.values())
    checks['label_and_before_same_supported_world']=initial_bundles['obs_label']==initial_bundles['obs_before']
    for case,j in obs.items():
        bundle=initial_bundles[case];measured={'notebook_bytes':next(x[4] for x in bundle['entries'] if x[0]=='notebook.txt'),
          'history_records':sum(x[1]=='file' and x[0].startswith('conversation_archive_v1/entries/') and x[0].endswith('.json') for x in bundle['entries'])}
        supplied=json.loads(j['messages'][-1]['content'])['operator_world_observation']
        checks['observation_measurements_'+case]=measured==j['metadata']['measured_facts'] and supplied==({} if case=='obs_label' else measured)
    decoder=[j for j in jobs if j['case_id'].startswith('decode_')]
    checks['decoder_six_paired_seed_conditions']=sorted((j['seed'],j['top_p']) for j in decoder)==sorted((s,p) for s in (27401,27402,27403) for p in (.9,1.0))
    checks['decoder_messages_and_ids_identical']=all(j['messages']==decoder[0]['messages'] and first_ids[j['case_id']]==first_ids[decoder[0]['case_id']] for j in decoder)
    checks['decoder_temperature_fixed']=all(j['decoder']=='nucleus' and j['temperature']==.8 for j in decoder)
    profile=read(H/'decoder/NUCLEUS_PROFILE.json');pr=profile['rows']
    reference=read(P/'raw/01.json')
    checks['profile_reference_input_same']=first_ids[decoder[0]['case_id']]==reference['input_token_ids']
    checks['profile_internal_counts_consistent']=len(pr)==len(reference['generated_token_ids'])==256 and [r['output_index'] for r in pr]==list(range(256)) and profile['positions_with_more_than_one_p90_choice']==sum(r['nucleus_size_p90']>1 for r in pr) and profile['min_p90_size']==min(r['nucleus_size_p90'] for r in pr) and profile['max_p90_size']==max(r['nucleus_size_p90'] for r in pr) and profile['all_argmax_match_reference']==all(r['greedy_matches_reference'] for r in pr)
    checks['profile_probability_ranges']=all(r['nucleus_size_p90']>=1 and 0<=r['top1_probability_temp08']<=1 and 0<=r['eos_probability_temp08']<=1 for r in pr)
    checks['canonical_unchanged_by_audit']=before==inv()
    out={'status':'pass' if all(checks.values()) and all(all(r['checks'].values()) for r in rows) else 'fail',
      'checks':checks,'rows':rows,'hidden_world_differences':differences,
      'hidden_outputs_equal_each_turn':[outputs[a['case_id']][i]['ids']==outputs[b['case_id']][i]['ids'] for i in (0,1)],
      'observation_output_sequences_equal':len({ids_hash(outputs[c][0]['ids']) for c in obs})==1,
      'decoder_distinct_output_sequences':{str(p):len({ids_hash(outputs[j['case_id']][0]['ids']) for j in decoder if j['top_p']==p}) for p in (.9,1.0)},
      'model_calls':0,'world_operations':0,'weights_loaded':False,'canonical_writes':False,
      'limits':'Artifact/tokenizer/provenance audit; does not repeat inference, independently recompute probability profile, reload weights, or prove hard-crash durability.'}
    (H/'AUDIT.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ('status','hidden_outputs_equal_each_turn','observation_output_sequences_equal','decoder_distinct_output_sequences')}))
    assert out['status']=='pass'
if __name__=='__main__':main()
