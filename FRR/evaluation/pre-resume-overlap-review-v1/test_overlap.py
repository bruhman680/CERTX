import unittest
from analyze import words,grams,covered
class Overlap(unittest.TestCase):
 def test_partial_union(self):
  self.assertEqual(covered(words('a b c d e NEW'),grams(words('a b c d e old'))),5)
 def test_repeated_windows_count_positions_once(self):
  self.assertEqual(covered(words('a a a a a a'),grams(words('a a a a a'))),6)
 def test_short_is_not_zero(self):
  self.assertIsNone(covered(words('Fiona Wilson'),grams(words('Fiona Wilson'))))
 def test_case_punctuation_definition(self):
  self.assertEqual(words('F1: 0, 1; SAME—and different.'),['f1','0','1','same','and','different'])
if __name__=='__main__':unittest.main()
