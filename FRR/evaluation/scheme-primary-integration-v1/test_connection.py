"""Connection checks use a disposable copy; no primary model calls or writes."""
import json, shutil, tempfile, unittest
from pathlib import Path
import connected_routine as c
from world_store import World
from world_bundle import export_world, import_world

class Connection(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.tmp=tempfile.TemporaryDirectory(prefix='garden-connection-')
  cls.liveE=c.E;cls.oldE=c.old.ENV
  cls.root=Path(cls.tmp.name);copy=cls.root/'original';shutil.copytree(c.G,copy,ignore=shutil.ignore_patterns('__pycache__'))
  c.E=copy/'cycle3/environment';c.old.ENV=c.E
  c.activate()
 @classmethod
 def tearDownClass(cls):
  c.E=cls.liveE;c.old.ENV=cls.oldE;cls.tmp.cleanup()
 def test_01_same_history_empty_workspace(self):
  j=c.Journal(c.E);_,events,_=j.state();self.assertEqual(len(events),500)
  self.assertTrue((c.E/'NOTEBOOK.jsonl').read_bytes()==(c.D/'before/NOTEBOOK.jsonl').read_bytes())
  with c.WorldContext() as w:self.assertEqual(w.snapshot()['aliases'],{})
  self.assertEqual(c.old.patch_binding().snapshot(events)['number'],0)
  self.assertEqual(c.old.world_dispatch('LOOK',events)['kind'],'play_patch_receipt')
 def test_02_real_dispatch_persistence_retry_and_failure(self):
  events=c.Journal(c.E).state()[1]
  with c.WorldContext() as w:before=w.snapshot()
  published=c.dispatch('(define (twice x) (+ x x))',events,before,'connection-define')
  self.assertEqual(published['status'],'PUBLISHED')
  retry=c.dispatch('(define (twice x) (+ x x))',events,before,'connection-define')
  self.assertEqual(retry,published)
  with c.WorldContext() as w:s=w.snapshot();w.verify_integrity();self.assertEqual(len(w.audit()),1)
  self.assertIn('twice',s['aliases'])
  result=c.dispatch('(run (twice 7))',events,s,'connection-run')
  self.assertEqual(result['status'],'COMPUTED');self.assertEqual(result['result']['value'],14)
  bad=c.dispatch('(run (+ 1',events,s,'connection-error')
  self.assertNotEqual(bad['status'],'COMPUTED')
  with c.WorldContext() as w:self.assertEqual(w.snapshot(),s)
  note=c.dispatch('I might explore later.',events,s,'connection-note')
  self.assertNotEqual(note['kind'],'scheme_receipt')
 def test_03_copy_restore_projection_and_readonly_history(self):
  path=self.root/'connection-export.json';s=c.export(path)
  other=self.root/'restored.sqlite';import_world(path,other,c.PROFILE)
  w=World(other,c.PROFILE)
  try:
   self.assertEqual(w.snapshot(),s);out=self.root/'restored.json';export_world(w,out)
  finally:w.close()
  self.assertEqual(path.read_bytes(),out.read_bytes())
  c.Journal(c.E).project();self.assertEqual(c.read(c.E/'STATE.json')['next_step'],500)
  c.checked()
 def test_04_prompt_bounds_and_whole_reply_route(self):
  from transformers import AutoTokenizer
  events=c.Journal(c.E).state()[1]
  with c.WorldContext() as w:s=w.snapshot()
  q=c.render(events,s);tok=AutoTokenizer.from_pretrained(c.old.parent.BASE,local_files_only=True,trust_remote_code=False)
  tokens=tok.apply_chat_template([dict(role='user',content=q)],tokenize=True,add_generation_prompt=True)
  self.assertLessEqual(len(tokens),8096)
  self.assertIn('READ HISTORY',q);self.assertIn('STABLE PLAY CHARTER',q)
  self.assertFalse(c.is_scheme('Here is code: (run (+ 1 2))'))
  self.assertFalse(c.is_scheme('```scheme\n(run (+ 1 2))\n```'))
  self.assertTrue(c.is_scheme('  (run (+ 1 2))'))
  (c.D/'CONNECTION_PROMPT_CHECK.json').write_text(json.dumps(dict(status='pass',tokens=len(tokens),limit=8096,scope='Disposable copy after host-only function publication; live workspace remains empty.'),indent=2)+'\n')
 def test_05_reconcile_committed_action_without_duplicate(self):
  events=c.Journal(c.E).state()[1];step=len(events)
  before=c.E/'scheme_world/bundles'/f'{step:06d}_before.json';snap=c.export(before)
  q=c.render(events,snap)
  plan=dict(run_id=f'continuous_{step:06d}',prompt=q,rng_seed=1201*100+step-45,
   scheme_before_bundle=str(before.relative_to(c.E)),scheme_before_sha256=c.h(before),scheme_before_snapshot=snap)
  c.old.immutable(c.E/'plans'/f'{step:06d}.json',plan)
  raw=dict(run_id=plan['run_id'],prompt=q,rng_seed=plan['rng_seed'],text='(put recovery-marker 9)')
  c.old.immutable(c.E/'scheme_world/raw'/f'{step:06d}.json',raw)
  # Trusted synthetic generation in copied environment, explicitly NOT a model result.
  committed=c.dispatch(raw['text'],events,snap,f'primary-{step:06d}')
  with c.WorldContext() as w:n=len(w.audit())
  row=c.complete(step)
  self.assertEqual(row['host_result'],committed)
  with c.WorldContext() as w:self.assertEqual(len(w.audit()),n);self.assertIn('recovery-marker',w.snapshot()['aliases'])
  self.assertEqual(c.Journal(c.E).state()[1][-1]['step'],500)
  self.assertTrue((c.E/'NOTEBOOK.jsonl').read_bytes().startswith((c.D/'before/NOTEBOOK.jsonl').read_bytes()))
if __name__=='__main__':unittest.main(verbosity=2)
