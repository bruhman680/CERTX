"""One detached call to the original generator, plus independent support checks."""
from pathlib import Path
import json, os, sys
for k,v in {'HF_HUB_OFFLINE':'1','OMP_NUM_THREADS':'2','OPENBLAS_NUM_THREADS':'1','MKL_NUM_THREADS':'2'}.items():
    os.environ[k] = v
H = Path(__file__).resolve().parent
P = H.parent / 'final-garden-contract-v1'
sys.path[:0] = [str(P), str(P.parent / 'source-access-three-cycle-v1')]
import runner
from generation import generate
from runtime_reference import Guard, parameter_digest
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

def dump(name, value):
    with (H / name).open('x') as f:
        json.dump(value,f,indent=2,ensure_ascii=False,allow_nan=False)
        f.write('\n')

def main():
    before = runner.read(H / 'CANONICAL_BEFORE.json')
    assert runner.file_inventory(P) == before
    t = runner.read(H / 'SAMPLER_TRACE.json')
    assert t['all_positions_singleton_target_support']
    # Independent scalar criterion: if the leading probability exceeds top-p,
    # the production shifted cumulative rule retains exactly the leader.
    minimum = min(s['target_full_probability'] for s in t['steps'])
    assert minimum > .9 and all(s['target_rank'] == 1 for s in t['steps'])
    torch.set_num_threads(2)
    tok = AutoTokenizer.from_pretrained(runner.BASE,local_files_only=True,trust_remote_code=False)
    model = AutoModelForCausalLM.from_pretrained(runner.BASE,local_files_only=True,trust_remote_code=False,
        use_safetensors=True,torch_dtype=torch.float32,attn_implementation='eager')
    model.requires_grad_(False)
    model.eval()
    pin = runner.read(runner.R / 'MODEL_CONDITION.json')['tensor_digest']
    assert parameter_digest(model,False) == pin
    last = runner.read(runner.R / 'raw/001550.json')
    guard = Guard(5153960755,H / 'CONFIRM_RESOURCE.jsonl')
    raw = generate(model,tok,last['messages'],guard,'external_tool_path_audit_original_generator',runner.entry_seed(1551))
    assert raw['generated_token_ids'] == last['generated_token_ids']
    assert raw['input_token_ids'] == last['input_token_ids']
    assert parameter_digest(model,False) == pin
    dump('DETACHED_GENERATION.json',raw)
    text_bytes = len((raw['text']+'\n').encode())
    bundle = runner.read(runner.R / 'bundles/001550.json')
    nbytes = next(x[4] for x in bundle['entries'] if x[0] == 'notebook.txt')
    remaining_complete = (262144-nbytes)//text_bytes
    assert runner.file_inventory(P) == before
    result = {'status':'pass','canonical_entry':1550,'canonical_calls':0,'external_generation_calls':1,
        'original_generator_imported_without_modification':True,'seed_matches_hypothetical_entry_1551':True,
        'same_input_ids':True,'same_output_ids':True,'same_stop':raw['stop']==last['stop'],
        'minimum_leading_probability_over_32_positions':minimum,'every_leader_exceeds_top_p':True,
        'canonical_inventory_unchanged':True,'training_updates':0,
        'boundary_projection':{'current_notebook_bytes':nbytes,'per_file_limit':262144,
            'bytes_per_identical_append':text_bytes,'further_complete_appends_before_limit':remaining_complete,
            'first_predicted_overlimit_entry':1550+remaining_complete+1,
            'remaining_bytes_after_complete_appends':(262144-nbytes)%text_bytes,
            'scope':'Arithmetic projection conditional on identical replies, no earlier operational changes and ordinary appends. No long continuation or overlimit action was performed. A real storage error would change delivered feedback and break identical-input assumptions.'}}
    dump('CONFIRMATION.json',result)
    print(json.dumps(result))

if __name__ == '__main__':
    main()
