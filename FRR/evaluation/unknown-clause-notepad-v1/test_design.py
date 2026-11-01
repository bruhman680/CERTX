import unittest
from design import queries,decode,render
class Checks(unittest.TestCase):
 def test_decode(self):
  self.assertEqual(decode('UNKNOWN\nNOTE: no record')['answer'],'UNKNOWN')
  self.assertEqual(decode('NO\nNOTE: Status: zero\nANSWER: YES')['answer'],'NO')
  self.assertEqual(decode('ANSWER: no.\nNOTE: Status: zero')['answer'],'NO')
  self.assertIsNone(decode('YES or NO')['answer']);self.assertIsNone(decode('NOTE: zero\nNO')['answer'])
  self.assertEqual(decode('NO\nNOTE: Status: zero')['status_quotes'],['zero'])
 def test_count(self):
  qs=queries();self.assertEqual(len(qs),672);self.assertEqual(len({q['prompt'] for q in qs}),560)
 def test_factor_invariance(self):
  for q in queries():
   self.assertEqual(q['expected'],{'positive':'YES','zero':'NO','missing':'WITHHOLD','absent':'UNKNOWN'}[q['state']])
   self.assertEqual('If there is no visible record return UNKNOWN.' in q['prompt'],q['absence'])
   self.assertEqual('Then write NOTE:' in q['prompt'],q['note_requested'])
 def test_absence_separate(self):
  self.assertNotIn('Status: missing',render('Maple','absent','none',False,True,False))
  self.assertIn('Status: missing',render('Maple','missing','none',False,True,False))
if __name__=='__main__':unittest.main()
