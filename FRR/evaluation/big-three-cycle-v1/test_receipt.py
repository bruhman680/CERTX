import unittest,importlib.util
from pathlib import Path
spec=importlib.util.spec_from_file_location('receipt',Path(__file__).resolve().parents[2]/'modules/measurement_compatibility.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Receipt(unittest.TestCase):
 def test_distinct_failure_states(self):
  f=m.describe_compatibility
  self.assertEqual(f([('A',.05)],[],['A'])['status'],'CALIBRATION_GRID_EMPTY')
  self.assertEqual(f([('A',.05)],[.1],['A'])['status'],'NO_COMPATIBLE_PAIR')
 def test_ambiguity_and_filtered_support(self):
  f=m.describe_compatibility;pairs=[('A',.05),('B',.1),('A',.05)]
  self.assertEqual(f(pairs,[.05,.1],['A','B'])['status'],'AMBIGUOUS_CLASSES')
  x=f(pairs,[.05],['A','B']);self.assertEqual(x['status'],'COMPATIBLE_CLASS');self.assertEqual(x['compatible_classes'],['A']);self.assertEqual(len(x['retained_pairs']),1)
 def test_invalid_class(self):
  with self.assertRaises(ValueError):m.describe_compatibility([('C',.05)],[.05],['A'])
if __name__=='__main__':unittest.main()
