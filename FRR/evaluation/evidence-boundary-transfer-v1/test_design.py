import unittest
from design import cases,render,LAYOUTS
from verifier import verify
class Checks(unittest.TestCase):
 def test_all_cases(self):
  cs=cases();self.assertEqual(len(cs),324)
  for c in cs:
   for policy in ['strict','supported']:
    v=verify(c['source'],c['layout'],c['target'],policy)
    self.assertEqual(v['verdict'],c['expected_'+policy],(c['id'],policy))
    if v['verdict']=='READY':self.assertEqual(v['state'],c['expected_state'])
 def test_duplicates_rejected(self):
  for source,layout in [('[{"plot":"A","status":"positive","status":"zero"}]','json'),('Plot: A\nStatus: positive\nStatus: zero','lines'),('[plot=A; status=positive; status=zero]','brackets')]:
   self.assertEqual(verify(source,layout,'A','supported')['verdict'],'FORMAT_ERROR')
 def test_source_boundaries(self):
  for layout in LAYOUTS:
   source=render([{'plot':'A','status':'positive'},{'plot':'A','status':'zero'}],layout)
   self.assertEqual(verify(source,layout,'A','supported')['verdict'],'CONFLICT')
   source=render([{'plot':'B'},{'plot':'A','status':'zero'}],layout)
   self.assertEqual(verify(source,layout,'A','supported')['state'],'zero')
   source=render([{'status':'missing'},{'plot':'A','status':'zero'}],layout)
   self.assertEqual(verify(source,layout,'A','supported')['verdict'],'UNATTRIBUTED')
 def test_partial_policies(self):
  for layout in LAYOUTS:
   source=render([{'plot':'A'},{'plot':'A','status':'missing'}],layout)
   self.assertEqual(verify(source,layout,'A','strict')['verdict'],'PARTIAL_TARGET')
   v=verify(source,layout,'A','supported');self.assertEqual(v['state'],'missing');self.assertIn('target_record_without_status_retained',v['warnings'])
if __name__=='__main__':unittest.main()
