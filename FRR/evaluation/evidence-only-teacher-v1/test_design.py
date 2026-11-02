import unittest
from collections import Counter
from design import cases,queries,render,MAP,INTERFACES,KINDS
from legacy_design import note
class Contracts(unittest.TestCase):
 def test_balanced(self):
  cs=cases();self.assertEqual(len(cs),24);self.assertEqual(Counter(c['expected'] for c in cs),{x:6 for x in MAP.values()})
  for c in cs:
   if c['state']=='absent':self.assertNotIn('Status:',c['record'])
   else:self.assertIn('Status: '+c['state'],c['record'])
 def test_authority_and_notes(self):
  for c in cases():
   for i in INTERFACES:
    for k in KINDS:self.assertIn(c['prompt'],render(c,i,k))
   self.assertIn(c['other'],note(c,'irrelevant'));self.assertNotIn('Plot: '+c['name'],note(c,'irrelevant'))
   if c['state']!='absent':self.assertNotIn('Status: '+c['state'],note(c,'irrelevant'))
   for k in KINDS:self.assertNotIn(c['expected'],note(c,k))
 def test_query_contract(self):
  qs=queries();self.assertEqual(len(qs),247);self.assertEqual(len({q['prompt'] for q in qs}),247)
  self.assertEqual(sum(q['interface']=='legacy_anchor' for q in qs),7)
  for c in cases():self.assertEqual(sum(q['case_id']==c['id'] for q in qs),10)
if __name__=='__main__':unittest.main()
