import unittest,collections
import study as s
class Contract(unittest.TestCase):
 def test_target_vs_demo(self):
  c=next(x for x in s.cases() if x['relation']=='different')
  for text in ('4 + 5','9','HOST RESULT: 9'):
   self.assertFalse(s.score(text,s.routine.view_dispatch(text,[]),c)['strict_success'])
  good='TRY 4 + 5';self.assertTrue(s.score(good,s.routine.view_dispatch(good,[]),c)['strict_success'])
  wrong='TRY '+c['demo'];score=s.score(wrong,s.routine.view_dispatch(wrong,[]),c)
  self.assertTrue(score['wrong_demo_execution']);self.assertFalse(score['strict_success'])
 def test_balance(self):
  cs=list(s.cases());self.assertEqual(len(cs),32);self.assertEqual(len({x['run_id'] for x in cs}),32)
  for context in s.CONTEXTS:
   for relation in s.RELATIONS:
    rows=[x for x in cs if x['context']==context and x['relation']==relation];self.assertEqual(collections.Counter(x['demo'] for x in rows),collections.Counter({x[0]:2 for x in s.TARGETS}))
 def test_history_unchanged(self):
  for c in s.cases():
   q=s.prompt(c);old=s.prior.render(s.events(c['context']),'current','Get the calculator result for '+c['target']+' by issuing a tool request.')
   new='Example syntax: TRY '+c['demo']+'. This example is not a task you must perform.'
   self.assertEqual(q.replace(new,s.CLAUSE,1),old)
   if c['context']=='carried':self.assertIn(s.prior.history_block(s.events('carried')),q)
 def test_matched_is_not_wrong_demo(self):
  c=next(s.cases());t='TRY '+c['target'];v=s.score(t,s.routine.view_dispatch(t,[]),c);self.assertTrue(v['strict_success']);self.assertTrue(v['demonstration_expression_bound']);self.assertFalse(v['wrong_demo_execution'])
if __name__=='__main__':unittest.main()
