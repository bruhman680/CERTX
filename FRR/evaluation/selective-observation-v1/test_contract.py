import unittest,importlib.util
from pathlib import Path
import study,observer
class Contract(unittest.TestCase):
 def test_model_interface_identity(self):
  spec=importlib.util.spec_from_file_location('old',study.P/'study.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
  for key in ('HEADER','OBS','FEEDBACK'):self.assertEqual(getattr(study,key),getattr(m,key))
  e=[dict(step=29,observation='x',reply='<<< y >>>',feedback=study.FEEDBACK)];self.assertEqual(study.render(e),m.render(e))
 def test_quiet_sampling_and_limits(self):
  def row(i,text='YES'):return dict(run_id=str(i),episode='e',seed=1,step=i,arm='full',text=text,input_token_ids=[1],generated_token_ids=[1,2],stop='eos')
  old=[row(i) for i in range(5)];new=[row(i) for i in range(5,10)];x=observer.index(old,new,[]);self.assertEqual(x['flagged_total'],0);self.assertIn(x['quiet_sample_id'],[str(i) for i in range(5,10)]);self.assertEqual(x,observer.index(old,new,[]))
 def test_novelty_not_truth(self):
  self.assertEqual(observer.form('<<< NO >>>'),'record');self.assertEqual(observer.form('NO'),'label');self.assertEqual(observer.norm('Round 21'),observer.norm('Round 22'))
if __name__=='__main__':unittest.main()
