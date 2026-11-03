import unittest
from design import schedule,render,feedback,answer
class Contracts(unittest.TestCase):
 def test_schedule(self):
  a=schedule('persistent_failure');self.assertEqual([x['state'] for x in a],['zero']*8+['missing']*2);b=schedule('evidence_availability');self.assertEqual([x['state'] for x in b],['absent']*4+['positive']*2+['absent']*4)
 def test_feedback_without_answer(self):
  self.assertEqual(answer('NO\nMaybe another route.'),'NO');self.assertIsNone(answer('Could we check the source?'));self.assertTrue(feedback('question','NO').startswith('No scored'))
  self.assertEqual(feedback('YES','NO'),feedback('YES','WITHHOLD'))
 def test_history_verbatim(self):
  e=dict(step=0,observation='old',reply='Question?\nunchanged',feedback='No scored task answer.')
  p=render('current',[e]);self.assertIn(e['reply'],p);self.assertIn('old',p);self.assertTrue(p.endswith('Next response:'))
if __name__=='__main__':unittest.main()
