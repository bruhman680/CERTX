"""Scoped-fact serialization comparison using the frozen observation kernel."""
from pathlib import Path
import argparse,importlib.util,json,copy,os,uuid,traceback,hashlib
H=Path(__file__).resolve().parent;E=H.parent;UP=E/'frr-sandbox-live-sensing-v1/study.py'
spec=importlib.util.spec_from_file_location('scoped_fixed_observation_kernel',UP)
k=importlib.util.module_from_spec(spec);spec.loader.exec_module(k)
# Explicit kernel configuration: these branches never select post-reply packets.
k.H=H;k.ARMS=('prose','json');k.TURNS=3

def pins():
    paths=[Path(__file__),UP,k.INSTRUMENT,k.c.H/'common.py',k.c.C/'generation.py',k.c.C/'candidate.py',k.c.C/'world/garden_world.py',E/'final-garden-contract-v1/world.py',E/'final-garden-contract-v1/server.py',
           H/'design/prose_mechanics_user.txt',H/'design/json_mechanics_user.txt',H/'design/common_mechanics_suffix.txt',H/'design/canonical_scoped_facts.json',H/'design/world_rules.txt',H/'design/DESIGN_FREEZE.json',
           k.c.MODEL/'config.json',k.c.MODEL/'tokenizer.json',k.c.MODEL/'tokenizer_config.json']
    return {str(p):k.c.sha(p) for p in paths}

def prepare(run):
    run=Path(run);run.mkdir(parents=True,exist_ok=False)
    main_state=k.c.read(k.M/'run/STATE.json');assert main_state['human_entry']==1630 and main_state['paused']
    assert not (k.M/'run/PENDING.json').exists() and not (k.M/'run/RUN.lock').exists()
    assert k.c.verify_store(k.M/'run/world')['status']=='pass'
    k.save(run/'MAIN_BEFORE.json',k.c.inventory(k.M));k.save(run/'SOURCE_BEFORE.json',k.c.inventory());k.save(run/'PARENT_STATE.json',main_state)
    k.save(run/'BEFORE_ACTIVE_POINTER.json',k.c.read(E.parent/'ACTIVE_GARDEN_PHASE.json'))
    manifest={'date':'2026-11-15 America/Chicago','purpose':'model_study','version':'scoped-world-facts-v1','planned_model_calls':6,'arms':['prose','json'],'turns_per_arm':3,
      'FRR':False,'system':'empty in both','question':'effect of encoding the same scoped permission/runtime facts as prose versus JSON, with identical suffix and initial-only perception',
      'kernel_configuration':{'source':str(UP),'ARMS':['prose','json'],'TURNS':3,'post_reply_observation_selection':False,'reason':'frozen kernel selects live packets only for arm live; neither current arm is live'},
      'readout_adapter':'upstream audit fixed planned-call field8 is normalized to this declared6; actual calls computed from records, never changed',
      'world_delta':'common mechanical WORLD_RULES replacement; other source1630 files preserved','fact_scope':'operator-reviewed fact crosswalk, not proof that model interprets the forms equivalently',
      'history':'same fresh role topology; all actual branch pairs, no pruning; same typed runtime_feedback after replies',
      'sensing':'shared initial snapshot only; full after-effect snapshots retained externally, no later packets selected',
      'body':'same pinned cached135M CPUfloat32 eager2threads greedy256 freshKV','input_limit':7936,'packet_byte_limit':8192,
      'confounds':'encoding includes syntax, labels, wording, length and position; JSON18texttokenslonger in design; no neutral or superior format presumed',
      'no_task_hint_score_reward':True,'training_updates':0,'activation':False,'pins':pins(),'tensor_digest':k.c.read(k.c.C/'run/MANIFEST.json')['tensor_digest'],
      'active_pointer_sha256':k.c.sha(E.parent/'ACTIVE_GARDEN_PHASE.json')}
    k.save(run/'MANIFEST.json',manifest)
    source=k.M/'run/world';parent=source/'bundles'/k.c.read(source/'STATE.json')['bundle'];bundle=k.c.read(parent);k.save(run/'PARENT_WORLD.json',bundle)
    import base64
    rule=next(x for x in bundle['entries'] if x[0]=='WORLD_RULES.txt')
    (run/'PARENT_WORLD_RULES.txt').write_bytes(base64.b64decode(k.c.read(source/'objects'/(rule[3]+'.json'))['base64']))
    tok=k.c.tokenizer();checks=[]
    rules=(H/'design/world_rules.txt').read_text()
    for arm in k.ARMS:
        store=run/'branches'/arm/'world';k.save(run/'PREPARATION_PENDING.json',{'arm':arm,'stage':'known only after clone/rule initialization commits'})
        w=k.c.GardenWorld.create(store,parent,source/'objects',parent_entry=1630)
        try:
            before=w.checkpoint();code="from pathlib import Path\nPath('WORLD_RULES.txt').write_text("+repr(rules)+",encoding='utf-8')"
            op=w.apply('python',code);k.save(run/'preparation'/(arm+'.json'),{'actor':'operator','source':code,'event':op})
            assert op['feedback']['exit_code']==0 and op['feedback']['boundary'] is None and op['changed_paths']==['WORLD_RULES.txt']
            after=w.checkpoint()
        finally:w.close()
        a={x[0]:x for x in before['entries']};b={x[0]:x for x in after['entries']}
        assert set(a)==set(b) and all(a[p]==b[p] for p in a if p!='WORLD_RULES.txt')
        assert b['WORLD_RULES.txt'][3]==hashlib.sha256(rules.encode()).hexdigest()
        assert k.c.verify_store(store)['status']=='pass'
        observation,snapshot_path=k.render_snapshot(run,arm,after,timing='initial',world_step=1,reply_index=None)
        assert observation['status']=='complete'
        framing=(H/'design'/(arm+'_mechanics_user.txt')).read_text()
        messages=[{'role':'system','content':''},{'role':'user','content':framing+'\n\n'+observation['model_text']}]
        ids=tok.apply_chat_template(messages,tokenize=True,add_generation_prompt=True);assert len(ids)<=7936
        k.save(run/'inputs'/(arm+'.json'),{'messages':messages,'input_token_ids':ids,'initial_snapshot_sha256':k.c.sha(snapshot_path),'prepared_world_id':after['id']})
        k.atomic(store.parent/'STATE.json',{'turn':0,'paused':True,'last_record_sha256':None,'world_step':1,'world_id':after['id'],'stop_reason':None,'actual_model_calls':0})
        checks.append({'arm':arm,'world_id':after['id'],'input_tokens':len(ids)});(run/'PREPARATION_PENDING.json').unlink()
    assert checks[0]['world_id']==checks[1]['world_id']
    oa=k.c.read(run/'observations/prose_initial.json');ob=k.c.read(run/'observations/json_initial.json');assert oa==ob
    k.guard(run)
    k.save(run/'PREPARATION_CHECKS.json',{'status':'pass','same_world_and_initial_sensor':True,'conditions':checks,'model_calls':0})
    return k.preflight(run,tok)

def audit(run,tok=None,save_result=True):
    out=k.audit(run,tok,save_result=False);out['planned_model_calls']=6
    assert out['post_reply_observations_consumed_by_generation']=={'prose':0,'json':0}
    assert out['actual_model_calls']<=6
    if save_result:k.save(Path(run)/'AUDIT.json',out)
    return out

def run_model(run):
    run=Path(run);assert not (run/'RUN_STARTED.json').exists() and not (run/'RESULTS.json').exists(),'No automatic replay'
    token=uuid.uuid4().hex;k.save(run/'RUN.lock',{'token':token,'pid':os.getpid()})
    try:
        tok=k.c.tokenizer();k.preflight(run,tok);k.save(run/'RUN_STARTED.json',{'planned_model_calls':6,'no_automatic_resume':True})
        import torch
        from transformers import AutoModelForCausalLM
        from runtime_reference import parameter_digest,Guard
        torch.set_num_threads(2)
        model=AutoModelForCausalLM.from_pretrained(k.c.MODEL,local_files_only=True,trust_remote_code=False,use_safetensors=True,torch_dtype=torch.float32,attn_implementation='eager')
        model.requires_grad_(False);model.eval();expected=k.c.read(run/'MANIFEST.json')['tensor_digest'];assert parameter_digest(model,False)==expected
        resource=Guard(5153960755,run/'RESOURCE.jsonl');resource.read('model_loaded')
        for turn in range(1,4):
          for arm in k.ARMS:
            state=k.c.read(run/'branches'/arm/'STATE.json')
            if state['stop_reason'] is not None:continue
            if (run/'PAUSE_REQUEST').exists():state['stop_reason']='user_pause';k.atomic(run/'branches'/arm/'STATE.json',state);continue
            k.guard(run);plan=k.begin_reply(run,arm,tok)
            if plan is None:continue
            assert plan['turn']==turn
            raw=k.body.generate(model,tok,plan['messages'],resource,'scoped_facts_'+plan['label'])
            row=k.commit_reply(run,arm,raw,tok)
            assert not row['observation_selected_for_next_input']
            assert parameter_digest(model,False)==expected;k.guard(run)
            print(json.dumps({key:row[key] for key in ['arm','turn','input_tokens','output_tokens','complete_cells','incomplete_fences','pause_reason']}),flush=True)
        out=audit(run,tok,False);out.update(weights_unchanged=parameter_digest(model,False)==expected,training_updates=0)
        k.save(run/'RESULTS.json',out);print(json.dumps(out),flush=True)
    except BaseException as error:
        k.save(run/('ERROR_'+uuid.uuid4().hex+'.json'),{'type':type(error).__name__,'message':str(error),'traceback':traceback.format_exc(),'pending':(run/'PENDING.json').exists()});raise
    finally:
        if (run/'RUN.lock').exists() and k.c.read(run/'RUN.lock').get('token')==token:(run/'RUN.lock').unlink()

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('command',choices=['prepare','preflight','run','audit']);parser.add_argument('--store',type=Path,default=H/'run');a=parser.parse_args()
    if a.command=='prepare':print(json.dumps(prepare(a.store)))
    elif a.command=='preflight':print(json.dumps(k.preflight(a.store)))
    elif a.command=='run':run_model(a.store)
    else:print(json.dumps(audit(a.store)))
