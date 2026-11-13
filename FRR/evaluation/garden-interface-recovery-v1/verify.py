"""No-model retained-evidence checks of the twelve primary probes."""
from pathlib import Path
import base64,hashlib,json,sys
H=Path(__file__).resolve().parent;P=H.parent/'final-garden-contract-v1';sys.path.insert(0,str(P))
import runner
from world import action,sha,stable

def read(p):return json.loads(Path(p).read_text())
def main():
 from transformers import AutoTokenizer
 tok=AutoTokenizer.from_pretrained(runner.BASE,local_files_only=True,trust_remote_code=False)
 plan,done=read(H/'PLAN.json'),read(H/'COMPLETED.json')
 assert done['status']=='pass' and done['calls']==12
 assert runner.file_inventory(P)==read(H/'CANONICAL_BEFORE.json')
 assert runner.state()['paused'] and runner.state()['next_entry']==1550
 runner.verify_pins()
 lookup={c['id']:c for c in plan['conditions']};assert len(lookup)==12
 for e in done['results']:
  c=lookup[e['condition']];raw=read(H/'raw'/(c['id']+'.json'));saved=read(H/'results'/(c['id']+'.json'))
  assert e==saved and raw['condition']==c
  m=([{'role':'system','content':''}] if c['frame']=='empty' else [])+[{'role':'user','content':plan['requests'][c['task']]}]
  assert raw['messages']==m
  assert tok.apply_chat_template(m,tokenize=True,add_generation_prompt=True)==raw['input_token_ids']
  assert tok.apply_chat_template(m,tokenize=False,add_generation_prompt=True)==raw['rendered']
  assert tok.decode(raw['generated_token_ids'],skip_special_tokens=True)==raw['text']==e['text']
  assert e['stop']==raw['stop'] and 0<len(raw['generated_token_ids'])<=96
  assert (raw['stop']=='eos' and raw['generated_token_ids'][-1]==tok.eos_token_id) or (raw['stop']=='token_limit' and len(raw['generated_token_ids'])==96)
  if c['task'].startswith('json_'):assert (action(e['text']) is not None)==(e['dispatch']=='shell')
  expected=bool(e['receipt'] is not None and e['receipt']['exit_code']==0 and e['receipt']['boundary'] is None and e['receipt']['stdout']=='/world\n')
  assert expected==e['printed_actual_cwd']
  if e['after'] is not None:assert e['after']['id']==sha(stable({'entries':e['after']['entries'],'root_mode':e['after']['root_mode']}))
 for p in (H/'objects').glob('*.json'):
  obj=read(p);b=base64.b64decode(obj['base64'],validate=True);assert sha(b)==p.stem==obj['sha256'] and len(b)==obj['bytes']
 value=dict(status='pass',primary_calls_verified=12,observer_model_calls=0,canonical_unchanged=True,canonical_paused_at=1550,scope='Tokenizer/message/output and retained receipt/object checks, not independent neural replication.')
 with (H/'VERIFICATION.json').open('x') as f:json.dump(value,f,indent=2);f.write('\n')
 print(json.dumps(value))
if __name__=='__main__':main()
