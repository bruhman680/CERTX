import unittest
from design import visible_facts,action_from_facts,decode_fact,cases,render
class Checks(unittest.TestCase):
 def test_decoder(self):
  for field,positive,negative in [('role','OTHER','not OTHER'),('status','zero','not zero'),('access','OPEN','not OPEN')]:
   self.assertEqual(decode_fact(f'{field.upper()}: {positive}',field),positive)
   self.assertIsNone(decode_fact(f'{field.upper()}: {positive}\n{field.upper()}: {negative}',field))
   self.assertIsNone(decode_fact(negative,field))
 def test_hidden_exclusion(self):
  for c in cases():
   d={k:v for k,v in c.items() if k in ('target','visible_display','archive_available')}
   self.assertEqual(visible_facts(c),visible_facts(d))
   for vocab in ('shared_yes_no','distinct_words'):
    for task in ('action','role','status','access'):self.assertEqual(render(c,vocab,task),render(d,vocab,task))
 def test_policy(self):
  self.assertEqual(action_from_facts({'role':'TARGET','status':'missing','access':None}),'WITHHOLD')
  self.assertEqual(action_from_facts({'role':'OTHER','status':'positive','access':'OPEN'}),'TARGET')
  self.assertEqual(action_from_facts({'role':'ABSENT','status':None,'access':'CLOSED'}),'UNKNOWN')
  self.assertIsNone(action_from_facts({'role':None,'status':'positive','access':'OPEN'}))
 def test_design(self):
  cs=cases();self.assertEqual(len(cs),72)
  for v in ('shared_yes_no','distinct_words'):
   self.assertEqual(len({render(c,v,'action') for c in cs}),24)
if __name__=='__main__':unittest.main()
