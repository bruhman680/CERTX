"""Reconstruct28adaptive readout/reference records without further model calls."""
from pathlib import Path
import json,re,sys
R=Path(__file__).resolve().parent;sys.path.insert(0,str(R));import run as study
sys.path.insert(0,str(R/'readout_controls'));import run_controls as controls
from transformers import AutoTokenizer

def main():
 tok=AutoTokenizer.from_pretrained(study.runner.parent.BASE,local_files_only=True,trust_remote_code=False);cases=controls.make_cases();assert cases==json.loads((R/'readout_controls/CASES.json').read_text());m=json.loads((study.runner.parent.ACQ/'MANIFEST.json').read_text());out=[]
 for variant in ('readout_controls','adapter_reference'):
  folder=R/variant;freeze=json.loads((folder/'FREEZE.json').read_text());assert json.loads((folder/'CHECKS.json').read_text())['status']=='pass'
  for p,h in {**freeze['files'],**freeze.get('adapter_file_pins',{})}.items():assert study.sha(Path(p))==h
  for seed in (120555,120556):
   for c in cases:
    key=f"{c['id']}_{seed}";r=json.loads((folder/'trials'/f'{key}.json').read_text());p=json.loads((folder/'plans'/f'{key}.json').read_text());q=c['prompt'];ids=tok.apply_chat_template([{'role':'user','content':q}],tokenize=True,add_generation_prompt=True);assert r['prompt']==p['prompt']==q and r['input_token_ids']==p['input_token_ids']==ids and r['rng_seed']==p['rng_seed']==seed;assert tok.decode(r['generated_token_ids'],skip_special_tokens=True)==r['text'];assert r['no_action_dispatched'] is True
    expected={'literal_three':3,'addition_two_plus_one':2+1,'negate_negative_two':-(-2),'current_bound8':2,'upper_bound8':8,'current_bound4':2,'upper_bound4':4}[c['id']];assert expected==c['expected']==r['expected'];t=r['text'].strip();formatted=re.fullmatch(r'[+-]?\d+',t) is not None;value=int(t) if formatted else None;assert r['integer_format']==formatted and r['predicted_value']==value and r['correct']==(formatted and value==expected);assert (r['stop']=='eos' and r['generated_token_ids'][-1]==tok.eos_token_id) or (r['stop']=='token_limit' and len(r['generated_token_ids'])==96)
    if variant=='adapter_reference':
     prior=json.loads((R/'readout_controls/trials'/f'{key}.json').read_text());assert prior['prompt']==r['prompt'] and prior['input_token_ids']==r['input_token_ids'] and prior['rng_seed']==r['rng_seed']
    out.append(dict(variant=variant,case=c['id'],seed=seed,correct=r['correct']))
 config=json.loads((R/'adapter_reference/ABLATION_CONFIG.json').read_text());assert set(config['scales_before'])==set(config['scales_after']) and all(v==2 for v in config['scales_before'].values()) and all(v==0 for v in config['scales_after'].values());assert config['base_parameter_digest']==m['base_digest_after'] and config['trained_adapter_tensor_digest_unchanged']==m['final_digest'] and config['tensor_mutations']==0
 count=study.unchanged();study.runner.freeze_check();study.put(R/'ADAPTIVE_RECORD_VERIFICATION.json',dict(status='pass',records_verified=len(out),prompt_token_decode_stop_score_reconstruction=True,independent_expected_integers=True,paired_prompts_ids_seeds=True,reference_scale_config_checked=True,original_trained_adapter_files_unchanged=True,primary_files_unchanged=count,new_model_calls=0,primary_writes=0,rows=out));print('All28adaptive control records verified; no model generation or primary writes.')
if __name__=='__main__':main()
