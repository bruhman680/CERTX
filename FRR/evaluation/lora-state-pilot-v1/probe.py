from experiment import *
import json
assert not (P/'PROBE_RESULT.json').exists()
for n,h in json.loads((P/'PROBE_FREEZE.json').read_text())['sha256'].items():assert sha(P/n)==h,n
train=json.loads((P/'TRAIN.json').read_text());m,tok=setup(73102)
lengths=[len(encode(tok,c,True)[0]) for c in train];evals=json.loads((P/'EVAL_CASES.json').read_text());assert max(lengths+[len(encode(tok,c)) for c in evals])<=256
m.eval();x=torch.tensor([encode(tok,train[0])]);startmem=mem('loaded_base')
with torch.no_grad():before=m(input_ids=x,use_cache=False).logits.clone()
inv=inject_lora(m,rank=4,alpha=8,dropout=0.);m.eval()
with torch.no_grad():after=m(input_ids=x,use_cache=False).logits
assert torch.equal(before,after),'Zero-product LoRA changed logits'
initial=base_digest(m);opt=torch.optim.AdamW([p for p in m.parameters() if p.requires_grad],lr=.001,weight_decay=.01,foreach=False)
result=balanced_step(m,tok,opt,train[:3]);final=base_digest(m);assert initial==final
folder=Path('/workspace/lora_resource_probe_v1');assert not folder.exists();save_adapter(m,folder,base_pin=pin());torch.save(opt.state_dict(),folder/'optimizer_state.pt')
eligible=result['completed'] and result['seconds']<8 and all(p['working_estimate']<p['working_limit'] for p in result['points'])
dump(P/'PROBE_RESULT.json',{'eligible_for_fixed_pilot':eligible,'inventory':inv,'max_training_tokens':max(lengths),'max_evaluation_prompt_tokens':max(len(encode(tok,c)) for c in evals),'zero_init_logits_equal':True,'base_frozen_digest_before':initial,'base_frozen_digest_after':final,'loaded_base_memory':startmem,'balanced_update':result,'separate_probe_checkpoint':str(folder),'probe_checkpoint_sha256':{f.name:sha(f) for f in folder.iterdir() if f.is_file()},'note':'probe uses trainingexamples;mainpilotmuststartfresh;evalsources tokenizedforlengthonly,noforwardorlabelsread'})
print(json.dumps({'eligible':eligible,'seconds':result['seconds'],'trainable':inv['trainable_parameter_count'],'max_tokens':max(lengths),'max_working':max(p['working_estimate'] for p in result['points'])}),flush=True)
