"""Independent retained-artifact audit; tokenizer only, no model inference."""
from pathlib import Path
import json, hashlib, sys
import torch
from transformers import AutoTokenizer

H=Path(__file__).resolve().parent;E=H.parent
C=E/'minimal-garden-candidate-v1';P=E/'error-feedback-contact-v1'
sys.path[:0]=[str(C),str(C/'world'),str(E/'source-access-three-cycle-v1')]
import candidate
from garden_world import verify_store

def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    result=read(H/'RESULTS.json');plan=read(H/'PLAN.json')
    tok=AutoTokenizer.from_pretrained('/workspace/cache_backend_models/smollm2-135m',local_files_only=True,trust_remote_code=False)
    parent_raw=read(P/'raw/full_traceback_27201.json');parent_batch=read(P/'batches/full_traceback_27201.json')
    expected_messages=read(P/'INPUT_MESSAGES.json')['full_traceback']+[
        {'role':'assistant','content':parent_raw['text']},
        {'role':'user','content':candidate.project_feedback(parent_batch)}]
    checks={'initial_messages_exact_parent_continuation':read(H/'INITIAL_MESSAGES.json')==expected_messages,
        'initial_bundle_exact_parent':read(H/'INITIAL_WORLD.json')==read(Path(plan['parent_world'])),
        'parent_bundle_hash':sha(Path(plan['parent_world']))==plan['parent_world_sha256'],
        'running_source_pinned':sha(H/'run.py')==plan['source_sha256']}
    expected_rng=torch.Generator(device='cpu').manual_seed(27301).get_state().tolist()
    previous=None;previous_world_id=read(H/'INITIAL_WORLD.json')['id'];rows=[]
    for loop in range(1,result['completed_loops']+1):
        p=read(H/f'plans/{loop:02d}.json');raw=read(H/f'raw/{loop:02d}.json')
        batch=read(H/f'batches/{loop:02d}.json');record=read(H/f'records/{loop:02d}.json')
        world_before=read(H/'world/bundles'/p['world_state']['bundle'])
        ids=tok.apply_chat_template(expected_messages,tokenize=True,add_generation_prompt=True)
        feedback=candidate.project_feedback(batch)
        flags={'plan_exact_actual_transcript':p['messages']==expected_messages,
          'plan_and_raw_exact_token_input':p['input_token_ids']==ids==raw['input_token_ids'],
          'raw_text_matches_generated_ids':raw['text']==tok.decode(raw['generated_token_ids'],skip_special_tokens=True),
          'rng_exact_prior_after':p['rng_state']==expected_rng,
          'previous_record_plan_and_row':p['previous_record_sha256']==record['previous_record_sha256']==previous,
          'raw_record_hash':sha(H/f'raw/{loop:02d}.json')==record['raw_sha256'],
          'batch_record_hash':sha(H/f'batches/{loop:02d}.json')==record['batch_sha256'],
          'plan_world_id_exact_previous_after':world_before['id']==previous_world_id,
          'first_op_world_before_exact':batch['operations'][0]['before_id']==previous_world_id,
          'last_op_world_after_exact':batch['operations'][-1]['after_id']==record['after_world_id'],
          'batch_text_exact_output':batch['raw_text']==raw['text'],
          'feedback_exact_projection':record['feedback']==feedback,
          'capacity_respected':len(ids)+512<=8192,
          'parsed_cell_count_matches':raw['parsed']['complete_executable_cells']==record['complete_executable_cells']}
        assert all(flags.values()),(loop,flags)
        rows.append({'loop':loop,'checks':flags,'before_world_id':previous_world_id,'after_world_id':record['after_world_id'],
           'rng_before_sha256':hashlib.sha256(bytes(p['rng_state'])).hexdigest(),
           'rng_after_sha256':hashlib.sha256(bytes(raw['rng_state_after'])).hexdigest()})
        expected_messages += [{'role':'assistant','content':raw['text']},{'role':'user','content':feedback}]
        previous=sha(H/f'records/{loop:02d}.json');previous_world_id=record['after_world_id']
        expected_rng=raw['rng_state_after']
    checks.update(final_messages_exact_actual_chain=read(H/'FINAL_MESSAGES.json')==expected_messages,
      completed_three_loops=result['completed_loops']==3,
      no_pending=not (H/'PENDING.json').exists() and not result['pending'],
      final_world_id_exact_previous_after=read(H/'world/bundles'/read(H/'world/STATE.json')['bundle'])['id']==previous_world_id,
      canonical_unchanged_reported=result['canonical_run_unchanged'],parent_unchanged_reported=result['parent_diagnostic_unchanged'],
      weights_unchanged_reported=result['weights_unchanged'])
    assert all(checks.values()),checks
    verification=verify_store(H/'world')
    audit={'status':'pass','checks':checks,'rows':rows,'world_verification':verification,
      'inference_calls':0,'weights_loaded':False,
      'scope':'Independent artifact/tokenizer audit and world verifier. Canonical/parent/weights unchanged flags are runner assertions, not a new model execution.'}
    (H/'AUDIT.json').write_text(json.dumps(audit,indent=2)+'\n')
    print(json.dumps({'status':'pass','loops':len(rows),'checks':checks,'world_verification':verification},indent=2))

if __name__=='__main__':main()
