"""Host-only message/counter/lock tests. No model inference or live changes."""
import importlib.util,json,tempfile,types,unittest
from pathlib import Path
from unittest.mock import patch
import runner

class MessageTests(unittest.TestCase):
 def test_cross_boundary_raw_roles_and_empty_system(self):
  old=[dict(entry=i,text=f'prior{i}',visible_feedback=None) for i in range(751,851)]
  before={'entries':[['notebook.txt','file',384,'x',0]]}
  with patch.object(runner,'parent_rows',return_value=old):
   m=runner.native_messages(before,[])
   self.assertEqual(m[0],{'role':'system','content':''})
   self.assertIn(runner.SEED,m[1]['content'])
   self.assertEqual([x['content'] for x in m if x['role']=='assistant'],[f'prior{i}' for i in range(839,851)])
   self.assertTrue(m[-1]['content'].startswith('\nDirectory entries:'))
 def test_sliding_context_includes_new_reply(self):
  old=[dict(entry=i,text=str(i),visible_feedback=None) for i in range(839,851)]
  new=[dict(entry=851,text='new',visible_feedback=None)]
  with patch.object(runner,'parent_rows',return_value=old):m=runner.native_messages({'entries':[]},new)
  self.assertEqual([x['content'] for x in m if x['role']=='assistant'],[str(i) for i in range(840,851)]+['new'])
 def test_environment_feedback_excludes_timing_and_evaluation(self):
  actual={'stdout':'42\n','stderr':'','exit_code':0,'boundary':None,'seconds':.1,'observer_label':'good'}
  self.assertEqual(runner.model_feedback(actual),{k:actual[k] for k in ['stdout','stderr','exit_code','boundary']})
 def test_native_template_does_not_remove_legitimate_history(self):
  from transformers import AutoTokenizer
  tok=AutoTokenizer.from_pretrained('/workspace/cache_backend_models/smollm2-135m',local_files_only=True,trust_remote_code=False)
  phrase='You are a helpful AI assistant named SmolLM, trained by Hugging Face'
  old=[dict(entry=850,text=phrase,visible_feedback=None)]
  with patch.object(runner,'parent_rows',return_value=old):m=runner.native_messages({'entries':[]},[])
  rendered=tok.apply_chat_template(m,tokenize=False,add_generation_prompt=True)
  self.assertTrue(rendered.startswith('<|im_start|>system\n<|im_end|>\n<|im_start|>user\n'))
  self.assertIn(phrase,rendered) # remains as historical assistant text, not system

class StateTests(unittest.TestCase):
 def setUp(self):
  self.t=tempfile.TemporaryDirectory();self.f=Path(self.t.name)/'frr';self.h=self.f/'evaluation/final-garden-contract-v1';self.r=self.h/'run';self.r.mkdir(parents=True)
  for n in ['sessions','events','plans','raw','results','bundles','objects','checks','reports','observer']:(self.r/n).mkdir()
  (self.r/'STATE.json').write_text(json.dumps({'next_entry':850,'paused':True,'latest_bundle':'000850.json','last_event_sha256':'parent'}));(self.r/'PAUSE').touch()
  self.contract=self.h/'CONTRACT.json';self.contract.write_text('{}');(self.r/'MANIFEST.json').write_text('{}')
  (self.f/'ACTIVE_GARDEN_PHASE.json').write_text(json.dumps({'phase':str(self.h.relative_to(self.f)),'state':str((self.r/'STATE.json').relative_to(self.f))}))
  self.patches=[patch.object(runner,'F',self.f),patch.object(runner,'H',self.h),patch.object(runner,'R',self.r),patch.object(runner,'CONTRACT',self.contract),patch.object(runner,'verify_pins',return_value={})]
  for p in self.patches:p.start()
 def tearDown(self):
  for p in reversed(self.patches):p.stop()
  self.t.cleanup()
 def test_losing_invocation_leaves_existing_lock_and_pause_untouched(self):
  lock=self.r/'RUN.lock';lock.write_text('{"token":"owner"}');before=(self.r/'STATE.json').read_bytes()
  with self.assertRaises(FileExistsError):runner.run_block('start',100)
  self.assertEqual(lock.read_text(),'{"token":"owner"}');self.assertEqual((self.r/'STATE.json').read_bytes(),before);self.assertEqual(list((self.r/'sessions').iterdir()),[])
 def test_owned_failure_always_pauses_and_releases_only_owned_lock(self):
  def fail(*a):
   s=runner.state();s['paused']=False;runner.atomic(self.r/'STATE.json',s);(self.r/'PAUSE').unlink();raise RuntimeError('fixture startup failure')
  with patch.object(runner,'_run_locked',side_effect=fail):
   with self.assertRaises(RuntimeError):runner.run_block('start',100)
  self.assertTrue(runner.state()['paused']);self.assertTrue((self.r/'PAUSE').exists());self.assertFalse((self.r/'RUN.lock').exists());self.assertEqual(len(list((self.r/'sessions').glob('*_ERROR.json'))),1)
 def test_pending_and_plan_block_without_model_call(self):
  (self.r/'PENDING.json').write_text('{}')
  with self.assertRaises(AssertionError):runner.run_block('start',100)
  (self.r/'PENDING.json').unlink();(self.r/'plans/000851.json').write_text('{}')
  with self.assertRaises(AssertionError):runner.run_block('start',100)
  self.assertFalse((self.r/'RUN.lock').exists())
 def test_observer_request_bounded_and_consumed_once(self):
  p=self.r/'observer/ZOOM_REQUEST.json';p.write_text('{"through_entry":855}')
  key,n,error=runner.observer_request(851,None);self.assertEqual(n,5);self.assertIsNone(error)
  self.assertEqual(runner.observer_request(852,key),(key,None,None))
  p.write_text('{"through_entry":999}')
  _,n,error=runner.observer_request(851,key);self.assertIsNone(n);self.assertIsNotNone(error)
 def test_malformed_observer_request_is_external_error(self):
  p=self.r/'observer/ZOOM_REQUEST.json';p.write_text('not JSON')
  key,n,error=runner.observer_request(851,None);self.assertIsNone(n);self.assertIsNotNone(error)
  self.assertEqual(runner.observer_request(852,key),(key,None,None))
 def test_observer_cadence_options_are_bounded(self):
  with self.assertRaises(AssertionError):runner.run_block('start',100,11,50)
  with self.assertRaises(AssertionError):runner.run_block('start',100,10,25)
  self.assertFalse((self.r/'RUN.lock').exists())
 def test_one_entry_full_control_flow_with_fake_inference(self):
  # Exercise boot, first restore, record order, counter, reporting and cleanup;
  # all neural inference is explicitly replaced with an inert fixture.
  bundle={'id':'fixture','entries':[['notebook.txt','file',384,'x',0]],'root_mode':448}
  (self.r/'bundles/000850.json').write_text(json.dumps(bundle))
  class W:
   def restore(self,*a):pass
   def capture(self,*a):return bundle
   def close(self):pass
  class Tok:
   def apply_chat_template(self,*a,**kw):return [1,2]
  class Model:
   def requires_grad_(self,*a):pass
   def eval(self):pass
  class Guard:
   def __init__(self,*a):pass
   def read(self,*a,**kw):pass
  def generated(model,tok,messages,guard,run_id,seed):return {'messages':messages,'text':'fixture writing','generated_token_ids':[4],'input_token_ids':[1,2],'stop':'eos','rng_seed':seed}
  modules={'torch':types.SimpleNamespace(set_num_threads=lambda n:None,float32='fixture_float32'),
   'transformers':types.SimpleNamespace(AutoTokenizer=types.SimpleNamespace(from_pretrained=lambda *a,**k:Tok()),AutoModelForCausalLM=types.SimpleNamespace(from_pretrained=lambda *a,**k:Model())),
   'runtime_reference':types.SimpleNamespace(Guard=Guard,parameter_digest=lambda *a:'fixture'),
   'generation':types.SimpleNamespace(generate=generated)}
  with patch.dict('sys.modules',modules),patch.object(runner,'World',W),patch.object(runner,'validate',return_value={'status':'pass'}),patch.object(runner,'parent_rows',return_value=[]),patch.object(runner,'receive',return_value={'kind':'notebook','feedback':None,'storage_receipt':{'exit_code':0}}):
   runner.run_block('start',1)
  self.assertEqual(runner.state()['next_entry'],851);self.assertTrue(runner.state()['paused']);self.assertFalse((self.r/'RUN.lock').exists());self.assertFalse((self.r/'PENDING.json').exists())
  self.assertTrue((self.r/'events/000851.json').exists());self.assertTrue((self.r/'reports/000851_000851.json').exists())

if __name__=='__main__':unittest.main(verbosity=2)
