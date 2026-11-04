import unittest,json
import study as s
class Contract(unittest.TestCase):
 def test_primary_and_materials(self):
  self.assertEqual(len(s.initial('carried')),100);self.assertEqual(s.initial('clean'),[])
  self.assertEqual(s.fixture_receipt()['result'],12);self.assertEqual(s.rejected_receipt()['kind'],'calculation_error')
 def test_content_and_action_parity(self):
  e=s.initial('carried');history=s.history_block(e)
  for form in s.FORMATS:
   q=s.render(e,form);self.assertIn(history,q)
   for card in json.loads((s.routine.ENV/'seed_shelf/0001.json').read_text())['seeds']:self.assertIn(card['text'],q)
   self.assertIn('TRY 2 + 3',q)
  self.assertNotIn('through -1',s.render([],'current'))
 def test_receipt_mask_not_world_erasure(self):
  a=dict(step=0,text='NOTE marker-note',host_result=dict(kind='note_recorded',executed=True,note='marker-note'),feedback=s.FEEDBACK)
  events,q,_=s.expected_probe([],'lean','own_withheld',a)
  self.assertEqual(events[-1]['host_result']['note'],'marker-note');self.assertNotIn('HOST RESULT (actual experiment record)',q)
  self.assertEqual(s.routine.view_dispatch('READ NOTES',events)['notes'],['marker-note'])
 def test_scoring_and_operand_binding(self):
  self.assertTrue(s.bound_expr('5 + 4.0','4+5'));self.assertFalse(s.bound_expr('2+3','7-2'))
  x=dict(stage='provided_error',text='TRY 2+3',host_result=s.routine.view_dispatch('TRY 2+3',[]));self.assertTrue(s.score(x)['numeric_goal_match']);self.assertFalse(s.score(x)['strict_success'])
  self.assertTrue(s.score(dict(stage='evidence_missing',text='WITHHOLD',host_result={}))['strict_success'])
if __name__=='__main__':unittest.main()
