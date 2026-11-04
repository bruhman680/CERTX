import sys,json,unittest
from pathlib import Path
R=Path(__file__).resolve().parent;G=R.parent/'source-access-three-cycle-v1';sys.path.insert(0,str(G));import routine as old;import fundamental_routine as new
class Transition(unittest.TestCase):
 def setUp(self):self.events=old.Journal(old.ENV).state()[1];self.assertEqual(len(self.events),205)
 def test_only_shelf_and_message_change(self):
  a=old.view_render(self.events);b=new.fundamental_view_render(self.events);anchor='OPTIONAL SEED SHELF (operator play prompts, not evidence or tasks):'
  self.assertEqual(a.split(anchor)[0],b.split(anchor)[0]);tail='STABLE PLAY CHARTER:';self.assertEqual(a.split(tail)[1],b.split(tail)[1]);message=json.loads((old.ENV/'seed_shelf/0002.json').read_text())['user_message'];self.assertEqual(b.count(message),1)
 def test_legacy_renderers_stay_exact(self):
  for fn in ('seed_render','play_render','view_render'):
   for n in (48,75,100,205):self.assertEqual(getattr(old,fn)(self.events[:n]),getattr(new,fn)(self.events[:n]))
 def test_parameters_and_dispatch_unchanged(self):
  a=json.loads((old.ENV/'ENVIRONMENT_VIEW_V1.json').read_text());b=json.loads((old.ENV/new.NEW_MANIFEST).read_text())
  for key in ('model_base_pin','adapter_sha256','charter_sha256','play_tools_sha256','reader_sha256','input_limit','output_limit','temperature','top_p','recent_visible_entries','history_read_max_entries','seed_rule','feedback'):self.assertEqual(a[key],b[key],key)
  for text in ('TRY 0 + 1','READ HISTORY 203 205','READ HISTORY','NOTE zero','READ NOTES','ordinary text'):
   self.assertEqual(old.view_dispatch(text,self.events),new.view_dispatch(text,self.events))
  self.assertEqual(new.view_dispatch('TRY 0 + 1',self.events)['result'],1)
 def test_old_rows_replay_and_new_manifest_distinct(self):
  self.assertNotEqual(old.sha(old.ENV/'ENVIRONMENT_VIEW_V1.json'),new.sha(old.ENV/new.NEW_MANIFEST));new.freeze_check()
  for x in old.Journal(old.ENV).state()[2]:
   if x.get('environment_version')=='archive-view-v1':self.assertEqual(x['prompt'],new.view_render(self.events[:x['step']]))
if __name__=='__main__':unittest.main()
