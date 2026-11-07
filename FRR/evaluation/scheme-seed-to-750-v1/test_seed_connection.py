"""Disposable copy only. Synthetic record is labelled; zero model inference calls."""
from pathlib import Path
import importlib.util,json,shutil,sys,tempfile
import seeded_routine as c
from world_bundle import export_world
H=c.H;live=c.E
before={p:c.h(c.G/p) for p in c.read(H/'before/PRIMARY_INVENTORY.json')}
with tempfile.TemporaryDirectory(prefix='seed-connection-') as t:
 copy=Path(t)/'primary';shutil.copytree(c.G,copy,ignore=shutil.ignore_patterns('__pycache__'))
 c.E=copy/'cycle3/environment';c.old.ENV=c.E
 c.activate();events=c.Journal(c.E).state()[1];assert len(events)==650
 assert (c.E/'NOTEBOOK.jsonl').read_bytes()==(H/'before/NOTEBOOK.jsonl').read_bytes()
 assert c.read(c.E/c.SEED_CARD)['text']=='You may do and act on anything and anywhere within your environment, explore, play, create, build, grow, learn, and reason in pattern and thought. 😁'
 spec=importlib.util.spec_from_file_location('prior_seed_renderer',c.D/'connected_routine_v2.py');prior=importlib.util.module_from_spec(spec);spec.loader.exec_module(prior)
 for n in (500,512,550,649):
  snap=c.snapshot_bundle(c.E/'scheme_world/bundles'/f'{n:06d}_before.json')
  assert c.render(events[:n],snap)==prior.render(events[:n],snap)
 snap=c.snapshot_bundle(c.E/'scheme_world/bundles/000649_after.json')
 old=prior.render(events,snap);q=c.render(events,snap);seed=c.read(c.E/c.SEED_CARD)['text']
 assert q==old.removesuffix('\n\nYour next move:')+'\n\nUSER TEXT SEED (invitation within this environment):\n'+seed+'\n\nYour next move:'
 assert q.count(seed)==1
 from transformers import AutoTokenizer
 tok=AutoTokenizer.from_pretrained(c.old.parent.BASE,local_files_only=True,trust_remote_code=False)
 ids=tok.apply_chat_template([{'role':'user','content':q}],tokenize=True,add_generation_prompt=True);assert len(ids)<=8096
 try:c.run(11)
 except AssertionError:pass
 else:raise AssertionError('11-entry window accepted')
 try:c.run(10)
 except AssertionError as e:assert 'Resume explicitly' in str(e)
 else:raise AssertionError('Paused runner did not stop before inference')
 assert not c.should_zoom(dict(host_result=dict(kind='record_receipt')))
 for kind in ('scheme_receipt','history_receipt','play_patch_receipt'):assert c.should_zoom(dict(host_result=dict(kind=kind)))
 c.verify()
 # Exercise new record and verifier paths using a plainly synthetic note.
 step=650;path=c.E/'scheme_world/bundles/000650_before.json';snap=c.export(path)
 plan=dict(run_id='continuous_000650',step=step,prompt=q,input_token_ids=ids,rng_seed=1201*100+step-45,environment_sha256=c.h(c.E/c.MANIFEST),history_steps=c.old.memory_view.view_steps(events),archive_available_range=[0,step],scheme_before_bundle=str(path.relative_to(c.E)),scheme_before_sha256=c.h(path),scheme_before_snapshot=snap,user_seed_sha256=c.h(c.E/c.SEED_CARD))
 c.old.immutable(c.E/'plans/000650.json',plan)
 text='NOTE Trusted host connection fixture; not a model output.';out=tok.encode(text,add_special_tokens=False)+[tok.eos_token_id]
 raw=dict(run_id=plan['run_id'],prompt=q,input_token_ids=ids,generated_token_ids=out,text=text,stop='eos',seconds=0,rng_seed=plan['rng_seed'],temperature=.8,top_p=.9,fixture_not_model_inference=True)
 c.old.immutable(c.E/'scheme_world/raw/000650.json',raw);row=c.complete(step)
 number=len(list((c.E/'sessions').glob('*.json')))
 c.old.immutable(c.E/'sessions'/f'{number:04d}.json',dict(session=f'{number:04d}',start_step=650,next_step=651,calls=1,requested_steps=1,input_limit=8096,environment_version=c.VERSION,delay_seconds=0,stop_reason='fixture_only',boundary=None,weights_unchanged=True,training_updates=0,fixture_not_model_inference=True))
 c.verify();assert row['environment_version']==c.VERSION
 with tempfile.TemporaryDirectory() as x:
  path=Path(x)/'world.json';c.export(path);assert path.read_bytes()==(c.E/'scheme_world/bundles/000649_after.json').read_bytes()
 assert all(c.h(c.G/p)==v for p,v in before.items()),'Live primary changed during copy test'
 checks=dict(status='pass',model_calls=0,synthetic_records_on_copy=1,synthetic_records_imported_to_live=0,old_prompt_render_matches=4,full_historical_replay_entries=150,new_record_transport_verified=True,seed_exact_with_emoji=True,activation_input_tokens=len(ids),input_limit=8096,ten_entry_gate_accepts_when_armed=True,eleven_entry_gate_rejects=True,zoom_condition_checked=True,world_unchanged=True,live_cursor=650,old_primary_files_unchanged=len(before))
 (H/'CONNECTION_CHECKS.json').write_text(json.dumps(checks,indent=2)+'\n');print(json.dumps(checks))
