import unittest
from design import cases,note,review,schedules,MAP
class Checks(unittest.TestCase):
 def test_counts(self):self.assertEqual(len(cases()),21);self.assertEqual(len(schedules()),168)
 def test_notes(self):
  for c in cases():
   self.assertEqual(c['expected'],MAP[c['state']]);v=note(c,'verified')
   if c['state']!='absent':self.assertEqual(v,c['record'])
   self.assertIn('Plot: '+c['other'],note(c,'irrelevant'));self.assertIn('Plot: '+c['name'],note(c,'misleading'))
   self.assertNotEqual(v,note(c,'misleading'))
 def test_previous_attempt(self):
  c=cases()[0];self.assertNotIn('<<<',review(c,'verified',False,'WRONG'))
  self.assertIn('<<<\nWRONG\n>>>',review(c,'verified',True,'WRONG'))
 def test_no_oracle_metadata(self):
  c=cases()[0];d={k:v for k,v in c.items() if k not in ('id','expected','frame')}
  for kind in ('none','verified','irrelevant','misleading'):self.assertEqual(review(c,kind,True,'NO'),review(d,kind,True,'NO'))
if __name__=='__main__':unittest.main()
