from experiment import *
import random,gc
assert json.loads((P/'PROBE_RESULT.json').read_text())['eligible_for_fixed_pilot']
assert not (P/'RAW_OUTPUTS.jsonl').exists()
for n,h in json.loads((P/'FREEZE.json').read_text())['sha256'].items():assert sha(P/n)==h,n
for n,h in json.loads((P/'PRESERVATION_BEFORE.json').read_text())['files_sha256'].items():assert sha(Path(n))==h,n
train=json.loads((P/'TRAIN.json').read_text());cases=json.loads((P/'EVAL_CASES.json').read_text())
state_root=Path('/workspace/smollm_lora_state_states_v1');assert not state_root.exists();state_root.mkdir()
initial=Path('/workspace/lora_state_initial_v1');final=Path('/workspace/lora_state_checkpoint_v1');assert not initial.exists() and not final.exists()
m,tok=setup(73103);inventory=inject_lora(m,rank=4,alpha=8,dropout=0.);basepin=pin();frozen_before=base_digest(m)
save_adapter(m,initial,base_pin=basepin)
count=0

def evaluate(chosen,arm):
 global count
 for c in chosen:
  row=generate(m,tok,c,arm,state_root)
  with (P/'RAW_OUTPUTS.jsonl').open('a') as f:f.write(json.dumps(row)+'\n')
  count+=1;print(json.dumps({'run':row['run_id'],'text':row['text'],'stop':row['stop']}),flush=True)

evaluate([c for c in cases if c['split']=='dev'],'original_dev')
params=[p for p in m.parameters() if p.requires_grad];assert sum(p.numel() for p in params)==230400
opt=torch.optim.AdamW(params,lr=.001,weight_decay=.01,foreach=False)
groups=[train[i:i+3] for i in range(0,len(train),3)];assert all({c['label'] for c in g}=={'YES','NO','WITHHOLD'} for g in groups)
order=[];rng=random.Random(73103)
for epoch in range(2):
 ids=list(range(24));rng.shuffle(ids);order.extend(ids)
completed=0;stop='fixed_48_updates';trigger=None;start=time.perf_counter();completed_exposure={'YES':0,'NO':0,'WITHHOLD':0}
for i,groupid in enumerate(order):
 point=mem('before_effective_update')
 if time.perf_counter()-start>=300:stop='wall_time_cap';trigger=point;break
 if point['working_estimate']>=point['working_limit']:stop='memory_headroom';trigger=point;break
 group=groups[groupid];group=group[i%3:]+group[:i%3]
 try:record=balanced_step(m,tok,opt,group)
 except Stop as exc:stop=str(exc);trigger=mem('unexpected_guard_exception');break
 record['effective_update']=i+1
 with (P/'TRAINING_LOG.jsonl').open('a') as f:f.write(json.dumps(record)+'\n')
 if not record['completed']:stop=record['stop'];trigger=record['points'][-1];break
 completed+=1
 for c in group:completed_exposure[c['label']]+=1
 if record['points'][-1]['working_estimate']>=record['points'][-1]['working_limit']:stop='memory_headroom_after_update';trigger=record['points'][-1];break
 if completed%8==0:print(json.dumps({'completed_updates':completed,'loss':record['loss']}),flush=True)
training_seconds=time.perf_counter()-start
assert frozen_before==base_digest(m),'Frozen base changed during adaptertraining'
save_adapter(m,final,base_pin=basepin);torch.save({'optimizer':opt.state_dict(),'completed_steps':completed,'group_order':order,'seed':73103},final/'optimizer_state.pt')
dump(P/'TRAINING_MANIFEST.json',{'completed_updates':completed,'planned_updates':48,'stop':stop,'trigger_memory':trigger,'training_seconds':training_seconds,'completed_class_exposure':completed_exposure,'inventory':inventory,'frozen_base_before':frozen_before,'frozen_base_after':base_digest(m),'base_pin':basepin,'adapter_checkpoint':str(final),'checkpoint_sha256':{f.name:sha(f) for f in final.iterdir() if f.is_file()},'initial_adapter':str(initial),'initial_adapter_sha256':{f.name:sha(f) for f in initial.iterdir() if f.is_file()},'probe_not_warmstart':True,'seed':73103,'learning_rate':.001,'effective_batch':3,'microbatch':1})
opt.zero_grad(set_to_none=True);del opt;gc.collect()
evaluate([c for c in cases if c['split']=='dev'],'adapted_dev')
evaluate([c for c in cases if c['split']=='test'],'adapted_test')
m.eval();diag=torch.tensor([encode(tok,train[0])])
with torch.no_grad():expected_logits=m(input_ids=diag,use_cache=False).logits[:,-1,:].detach().clone()
del m;gc.collect();m,tok=setup(73103);inject_lora(m,rank=4,alpha=8,dropout=0.)
evaluate([c for c in cases if c['split']=='test'],'original_test')
load_adapter(m,final,base_pin=basepin);m.eval()
with torch.no_grad():roundtrip=m(input_ids=diag,use_cache=False).logits[:,-1,:]
assert torch.equal(expected_logits,roundtrip),'Freshmodel adapterroundtrip changed diagnosticlogits'
dump(P/'RUN_MANIFEST.json',{'calls':count,'actual_updates':completed,'test_not_forwarded_until_training_and_checkpoint_complete':True,'evalkeys_hashed_not_parsed_or_prompted':True,'baseline':'fresh base pluszero-productadapters; probeverified exactforwardequivalence','training_labels_supervised':True,'generation_cap':8,'adapter_roundtrip_diagnostic_logits_exact':True,'roundtrip_logits_sha256':hashlib.sha256(roundtrip.cpu().contiguous().numpy().tobytes()).hexdigest(),'original_disk_unchanged':True,'default_not_promoted':True})
