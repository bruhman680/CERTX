"""Token-only diagnostic: no weights loaded, model calls, or world writes."""
from pathlib import Path
import json, hashlib, transformers
from transformers import AutoTokenizer

H=Path(__file__).resolve().parent
C=H.parents[1]/'minimal-garden-candidate-v1'
BASE=Path('/workspace/cache_backend_models/smollm2-135m')
t=AutoTokenizer.from_pretrained(BASE,local_files_only=True,trust_remote_code=False)
rows=[]
for n in (1,12):
    raw=json.loads((C/f'run/raw/{n:06d}.json').read_text())
    messages=raw['messages']+[{'role':'assistant','content':raw['text']}]
    exact=raw['input_token_ids']+raw['generated_token_ids']
    continued=t.apply_chat_template(messages,tokenize=True,continue_final_message=True,add_generation_prompt=False)
    ordinary=t.apply_chat_template(messages,tokenize=True,add_generation_prompt=False)
    rows.append({'retained_turn':n,'exact_raw_length':len(exact),'continued_template_length':len(continued),
      'ordinary_template_length':len(ordinary),'continue_final_message_exact_raw_token_match':continued==exact,
      'ordinary_template_exact_raw_token_match':ordinary==exact,'ordinary_extra_suffix':ordinary[len(exact):],
      'raw_generated_tokens':len(raw['generated_token_ids']),
      'first_continuation_difference':next((i for i,(a,b) in enumerate(zip(continued,exact)) if a!=b),min(len(continued),len(exact))) if continued!=exact else None,
      'exact_tail':exact[-10:],'continued_tail':continued[-10:]})
    assert ordinary!=exact
result={'transformers_version':transformers.__version__,'eos_id':t.eos_token_id,
 'tokenizer_config_sha256':hashlib.sha256((BASE/'tokenizer_config.json').read_bytes()).hexdigest(),
 'model_calls':0,'weights_loaded':False,'canonical_mutation':False,'rows':rows,
 'limit':'Two retained outputs; no guarantee that decode/re-encode preserves arbitrary raw token sequences.'}
(H/'TEMPLATE_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
