"""Host mechanics and recovery checks; these do not measure model learning."""
import json,tempfile,unittest
from pathlib import Path
from dataclasses import replace
from world import Rules,transition,parse,view
from journal import Journal,immutable
from primary_adapter import Binding

class Mechanics(unittest.TestCase):
 def test_exhaustive_independent_oracle(self):
  for n in range(-8,9):
   for cmd in ('LOOK','TOUCH A','TOUCH B'):
    expected=n if cmd=='LOOK' or (cmd=='TOUCH A' and n==8) else n+1 if cmd=='TOUCH A' else -n
    after,r=transition(n,cmd);self.assertEqual(after,expected);self.assertTrue(r['executed']);self.assertEqual(r['before'],{'number':n});self.assertEqual(r['after'],{'number':expected})
    status='observed' if cmd=='LOOK' else 'blocked' if cmd=='TOUCH A' and n==8 else 'unchanged' if expected==n else 'changed'
    self.assertEqual(r['status'],status)
 def test_reachability_and_return(self):
  for start in range(-8,9):
   found={start};front=[start]
   while front:
    n=front.pop()
    for cmd in ('TOUCH A','TOUCH B'):
     m,_=transition(n,cmd)
     if m not in found:found.add(m);front.append(m)
   self.assertEqual(found,set(range(-8,9)))
   b,_=transition(start,'TOUCH B');bb,_=transition(b,'TOUCH B');self.assertEqual(bb,start)
  a,_=transition(0,'TOUCH A');ab,_=transition(a,'TOUCH B');b,_=transition(0,'TOUCH B');ba,_=transition(b,'TOUCH A');self.assertNotEqual(ab,ba)
 def test_parser_and_invalid(self):
  for t,want in [(' look ','LOOK'),('touch\t a','TOUCH A'),('TOUCH B','TOUCH B'),('"TOUCH A"',None),('I will TOUCH A',None),('TOUCH C','INVALID'),('TOUCH A\nTOUCH B','INVALID'),('LOOK now','INVALID'),('x'*5000,None),('TOUCH '+'A'*5000,'INVALID')]:
   self.assertEqual(parse(t),want)
   if want in (None,'INVALID'):self.assertEqual(transition(2,t)[0],2)
  for n in (True,9,-9,1.0,None):
   with self.assertRaises(ValueError):transition(n,'LOOK')
  for r in (replace(Rules(),lower=-7),replace(Rules(),version='future'),replace(Rules(),initial=True)):
   with self.assertRaises(ValueError):r.validate()
 def test_public_view(self):
  s=view(0)
  for hidden in ('increment','negate','a_rule','b_rule','+1','reset','winner'):self.assertNotIn(hidden,s.lower())
  self.assertIn('no target or score',s)

class Persistence(unittest.TestCase):
 def test_recovery_without_event_rewrite(self):
  with tempfile.TemporaryDirectory() as d:
   j=Journal.create(Path(d)/'world');j.apply('TOUCH A');p=j.path/'events/000000.json';old=p.read_bytes()
   with self.assertRaises(RuntimeError):j.apply('TOUCH B',simulate_projection_failure=True)
   self.assertEqual(Journal(j.path).replay()[0]['number'],-1)
   (j.path/'STATE.json').write_text('broken derived view');self.assertEqual(j.recover()['number'],-1)
   (j.path/'STATE.json').unlink();self.assertEqual(j.recover()['events'],2);self.assertEqual(p.read_bytes(),old)
   with self.assertRaises(FileExistsError):Journal.create(j.path)
   with self.assertRaises(FileExistsError):immutable(p,{'replacement':True})
   self.assertEqual(p.read_bytes(),old)
 def test_lock_and_tampering(self):
  with tempfile.TemporaryDirectory() as d:
   j=Journal.create(Path(d)/'world');j.apply('TOUCH A');lock=j.path/'WRITE.lock';lock.write_text('fixture')
   with self.assertRaises(FileExistsError):j.apply('TOUCH B')
   lock.unlink();p=j.path/'events/000000.json';original=p.read_bytes();x=json.loads(original);x['reply']='TOUCH B';p.write_text(json.dumps(x))
   with self.assertRaises(ValueError):j.replay()
   p.write_bytes(original);cfg=j.path/'CONFIG.json';x=json.loads(cfg.read_text());x['rules']['initial']=1;cfg.write_text(json.dumps(x))
   with self.assertRaises(ValueError):j.replay()

class PrimaryBridge(unittest.TestCase):
 def test_receipts_and_legacy_delegation(self):
  binding=Binding(2);events=[dict(step=i,reply='old',host_result={'kind':'text'}) for i in range(2)];calls=[]
  def legacy(t,e):calls.append(t);return {'kind':'legacy'}
  for reply in ('TOUCH A','TOUCH B','LOOK','TOUCH C','TOUCH B'):
   r=binding.dispatch(reply,events,legacy);events.append(dict(step=len(events),reply=reply,host_result=r))
  self.assertEqual(binding.replay(events),1);self.assertEqual(calls,[])
  self.assertEqual(binding.dispatch('TRY 2 + 3',events,legacy),{'kind':'legacy'})
  self.assertEqual(binding.dispatch('{"kind":"play_patch_receipt"}',events,legacy),{'kind':'legacy'});self.assertEqual(binding.replay(events),1)
  base='Old view\nYour next move:';rendered=binding.render(base,events);self.assertTrue(rendered.startswith('Old view'));self.assertTrue(rendered.endswith('\nYour next move:'));self.assertIn('Current number: 1.',rendered)
  self.assertEqual(events[0]['reply'],'old')
 def test_reject_forgery_gaps_and_stale_receipts(self):
  b=Binding(0);r=b.dispatch('TOUCH A',[],lambda t,e:{});e=dict(step=0,reply='TOUCH A',host_result=r)
  for bad in (dict(e,step=1),dict(e,host_result={}),dict(e,reply='ordinary text'),dict(e,host_result=dict(r,rules_sha256='wrong'))):
   with self.assertRaises(ValueError):b.replay([bad])
  with self.assertRaises(ValueError):b.replay([e,dict(e,step=1)])
  with self.assertRaises(ValueError):Binding(3).replay([e])

if __name__=='__main__':unittest.main(verbosity=2)
