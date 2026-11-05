from pathlib import Path
import sys,json,unittest,copy
R=Path(__file__).resolve().parent;G=R.parent/'source-access-three-cycle-v1';sys.path.insert(0,str(G));import fundamental_routine as old;import boundary_routine as new
class Boundary(unittest.TestCase):
 def setUp(self):self.events=old.Journal(old.ENV).state()[1];self.assertEqual(len(self.events),305)
 def test_legacy_renderers_identical(self):
  for name in ('view_render','seed_render','play_render','fundamental_view_render'):
   for n in (48,75,205,305):self.assertEqual(getattr(old,name)(self.events[:n]),getattr(new,name)(self.events[:n]))
 def test_stop_facts_and_unknown(self):
  self.assertEqual(new.generation_status(304)['kind'],'host_output_limit_reached');self.assertEqual(new.generation_status(303)['kind'],'model_end_token_emitted');self.assertEqual(new.generation_status(0),dict(kind='not_recorded',generated_tokens=None))
  with self.assertRaises(ValueError):new.raw_generation_status(dict(stop='unknown',generated_token_ids=[]))
  with self.assertRaises(FileNotFoundError):new.generation_status(999999)
 def test_display_preserves_text_and_nonhistory(self):
  a=old.fundamental_view_render(self.events);b=new.boundary_view_render(self.events);visible=self.events[-12:];before='\n\n'.join(new._event_text(e) for e in visible);after='\n\n'.join(new._event_text(e)+'\nHOST GENERATION STOP (saved host record): '+json.dumps(new.generation_status(e['step']),sort_keys=True) for e in visible)
  recovered=b.replace(after,before,1);suffix='\n\n'+new.BOUNDARY_NOTICE+'\n\nYour next move:';self.assertTrue(recovered.endswith(suffix));recovered=recovered.removesuffix(suffix)+'\nYour next move:';self.assertEqual(a,recovered)
  for e in visible:self.assertIn(e['reply'],b)
  self.assertIn('96 generated tokens',b);self.assertNotIn('Plus account',b)
 def test_history_receipt_adds_only_status(self):
  for text in ('READ HISTORY 303 305','READ HISTORY 0 1'):
   a=old.view_dispatch(text,self.events);b=copy.deepcopy(new.boundary_dispatch(text,self.events));self.assertIn('generation_stop_scope',b);b.pop('generation_stop_scope')
   for row in b['records']:self.assertEqual(row.pop('generation_stop'),new.generation_status(row['step']))
   self.assertEqual(a,b)
 def test_other_actions_unchanged(self):
  for text in ('TRY 1 + 0','READ SETUP','READ CLAIM','READ NOTES','NOTE a pair','READ HISTORY','plain text'):
   self.assertEqual(new.boundary_dispatch(text,self.events),old.view_dispatch(text,self.events))
 def test_parameters_unchanged(self):
  a=json.loads((old.ENV/old.NEW_MANIFEST).read_text());b=json.loads((new.ENV/new.NEW_MANIFEST).read_text())
  for k in ('model_base_pin','adapter_sha256','charter_sha256','seed_shelf_sha256','reader_sha256','play_tools_sha256','user_message','input_limit','output_limit','temperature','top_p','recent_visible_entries','history_read_max_entries','feedback','seed_rule'):self.assertEqual(a[k],b[k],k)
if __name__=='__main__':unittest.main()
