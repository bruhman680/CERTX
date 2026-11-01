import unittest
from design import queries,records,conditions,render,fields,MAP
class Checks(unittest.TestCase):
 def test_count(self):self.assertEqual(len(queries()),531);self.assertEqual(len({q['prompt'] for q in queries()}),531)
 def test_record_fixed(self):
  rs={r['id']:r for r in records()}
  for q in queries():
   self.assertEqual(q['expected'],MAP[q['state']]);self.assertEqual(q['prompt'].count(rs[q['source_id']]['record']),1)
 def test_control_pairs(self):
  cs={c['id']:c for c in conditions()}
  for r in records():
   for c in conditions():
    if c['kind']!='relevant':continue
    d=cs[c['id'].replace('relevant','unrelated',1)]
    a,b=fields(r,c);x,y=fields(r,d)
    self.assertEqual([s.replace('Target','Label') for s in a],x)
    self.assertEqual([s.replace('Archive','Window') for s in b],y)
 def test_placement(self):
  r=records()[0];c=next(c for c in conditions() if c['id']=='relevant_both_different_no');p=render(r,c,'canonical')
  self.assertLess(p.index('Target plot:'),p.index('Visible record:'))
  self.assertLess(p.index(r['record']),p.index('Archive accessible:'))
if __name__=='__main__':unittest.main()
