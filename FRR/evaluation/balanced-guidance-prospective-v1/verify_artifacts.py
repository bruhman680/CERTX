"""Post-run byte/token/cache checks; no forward passes or semantic re-judging."""
from pathlib import Path
import json,hashlib,os
os.environ['HF_HUB_OFFLINE']='1'
from transformers import AutoTokenizer
from safetensors import safe_open
P=Path(__file__).resolve().parent

def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()
old=json.loads((P/'PRESERVATION_BEFORE.json').read_text())
assert all(sha(Path(k))==v for k,v in old['model_and_cache_sha256'].items())
for freeze in ('FREEZE.json','RAW_FREEZE.json'):
    assert all(sha(P/k)==v for k,v in json.loads((P/freeze).read_text())['sha256'].items())
tok=AutoTokenizer.from_pretrained('/workspace/cache_backend_models/smollm2-135m',local_files_only=True,trust_remote_code=False)
rows=[json.loads(l) for l in (P/'RAW_OUTPUTS.jsonl').read_text().splitlines()]
cases=json.loads((P/'CASES.json').read_text());guide=json.loads((P/'GUIDANCE.json').read_text())
assert len(rows)==len(cases)==len({r['run_id'] for r in rows})==24
for r,c in zip(rows,cases):
    assert r['run_id']==c['id']
    expected=guide[c['arm']]+'\n\nRecord:\n'+c['source']+'\n\nQuestion: '+c['question']
    assert r['messages']==[{'role':'user','content':expected}]
    assert tok.decode(r['generated_token_ids'],skip_special_tokens=True)==r['text']
    assert tok.apply_chat_template(r['messages'],tokenize=False,add_generation_prompt=True)==r['rendered_prompt']
    assert tok.apply_chat_template(r['messages'],tokenize=True,add_generation_prompt=True)==r['input_token_ids']
    a=r['cache_artifact'];f=Path(a['local_path'])
    assert sha(f)==a['sha256'] and f.stat().st_size==a['bytes']
    ids=r['input_token_ids']+r['generated_token_ids']
    assert ids==a['all_sequence_token_ids'] and a['cache_token_count']==len(ids)-1
    assert hashlib.sha256(json.dumps(ids[:a['cache_token_count']],separators=(',',':')).encode()).hexdigest()==a['cached_token_prefix_sha256']
    with safe_open(str(f),framework='pt',device='cpu') as opened:
        assert all(opened.get_slice(k).get_shape()[-2]==a['cache_token_count'] for k in opened.keys())
result={'pass':True,'actual_generations':24,'new_cache_byte_shape_prefix_checks':24,'prompt_and_output_tokenizer_checks':24,'old_model_and_cache_files_unchanged':len(old['model_and_cache_sha256']),'frozen_inputs_and_raw_unchanged':True,'scope':'coordinator checks, no independent or masked replication'}
with (P/'ARTIFACT_CHECKS.json').open('x') as f:f.write(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
