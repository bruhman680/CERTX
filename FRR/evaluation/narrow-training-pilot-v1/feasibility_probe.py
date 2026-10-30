import os,time,json,resource,hashlib
os.environ['HF_HUB_OFFLINE']='1'
import torch
from transformers import AutoTokenizer,AutoModelForCausalLM
from pathlib import Path
p=Path('/workspace/cache_backend_models/smollm2-135m');o=Path('/workspace/frr/evaluation/narrow-training-pilot-v1')
torch.set_num_threads(2);torch.manual_seed(20261030)
tok=AutoTokenizer.from_pretrained(p,local_files_only=True,trust_remote_code=False)
m=AutoModelForCausalLM.from_pretrained(p,local_files_only=True,trust_remote_code=False,use_safetensors=True,torch_dtype=torch.float32,attn_implementation='eager')
s='Determine whether the recorded soil count is positive. YES means an explicit positive count, NO means an explicit zero, and WITHHOLD means the soil count is unavailable. Other fields do not supply the soil count. Return only YES, NO or WITHHOLD.\nRecord: There are 7 soils. Each soil has 0 observations.\nQuestion: Is the recorded soil count positive?'
x=tok.apply_chat_template([{'role':'user','content':s}],add_generation_prompt=True,tokenize=True)
y=tok.encode('YES',add_special_tokens=False)+[tok.eos_token_id]
a=torch.tensor([x+y,x+y]);labels=a.clone();labels[:,:len(x)]=-100
start=time.perf_counter();m.train();v=m(input_ids=a,attention_mask=torch.ones_like(a),labels=labels,use_cache=False);v.loss.backward();elapsed=time.perf_counter()-start
params=sum(v.numel() for v in m.parameters());rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024
result={'probe':'one batch2 forward/backward, no optimizer update or checkpoint; disk source unchanged','sequence_tokens':a.shape[1],'parameters':params,'backward_seconds':elapsed,'process_peak_rss_bytes':rss,'estimated_weights_gradients_two_adam_moments_bytes':params*4*4,'cpu_threads':2,'planned_steps':48,'estimated_training_seconds_1_5x_probe':48*elapsed*1.5,'feasible_for_bounded_pilot':elapsed<8 and rss+params*8<6*1024**3}
(o/'FEASIBILITY.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)
