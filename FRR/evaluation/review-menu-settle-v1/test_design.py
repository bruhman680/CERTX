import unittest
from design import cases,render,queries,MENUS,ENDING,LABELS
from design_reference import review
class Checks(unittest.TestCase):
 def test_query_count(self):self.assertEqual(len(queries()),231);self.assertEqual(len({q['prompt'] for q in queries()}),231)
 def test_exact_baseline(self):
  for c in cases():
   for kind in ['none','verified']:self.assertEqual(render(c,kind,'rotation_0'),review(c,kind,False,'ignored'))
 def test_context_preserved(self):
  for c in cases():
   for kind in ['none','verified']:
    original=review(c,kind,False,'ignored');prefix=original[:-len(ENDING)]
    for menu in MENUS:self.assertTrue(render(c,kind,menu).startswith(prefix))
 def test_label_rotations(self):
  for i in range(4):
   values=MENUS['rotation_'+str(i)];self.assertEqual(set(values),set(LABELS));self.assertEqual(values[0],LABELS[i])
if __name__=='__main__':unittest.main()
