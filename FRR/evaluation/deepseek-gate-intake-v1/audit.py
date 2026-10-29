from pathlib import Path
import runpy,random,io,contextlib,json,csv,hashlib,math
import numpy as np
import torch
P=Path(__file__).resolve().parent
for n,h in json.loads((P/'FREEZE.json').read_text())['sha256'].items():assert hashlib.sha256((P/n).read_bytes()).hexdigest()==h
random.seed(0);buf=io.StringIO()
with contextlib.redirect_stdout(buf):scope=runpy.run_path(str(P/'original_simulation.py'))
(P/'ORIGINAL_SEED0.txt').write_text(buf.getvalue())
Agent=scope['DynamicAgent'];counts={};variances={2.0:[],15.0:[]}
with (P/'SEED_AUDIT.csv').open('w',newline='') as f:
 w=csv.writer(f);w.writerow(['seed','pressure','variance','gate','policy_weight','avoidance_entries'])
 for seed in range(1000):
  for pressure in [2.0,15.0]:
   random.seed(seed);a=Agent();x=a.generate_trajectory(pressure);v=float(a.compute_de(x));gate=a.dynamic_rsd(x,pressure)
   kind=gate.split(':')[0];counts[str(pressure)+':'+kind]=counts.get(str(pressure)+':'+kind,0)+1;variances[pressure].append(v)
   w.writerow([seed,pressure,repr(v),kind,a.policy_weight,len(a.avoidance_memory)])
noise=np.array([-.1,-.08,-.02,0,.01,.03,.05,.06,.08,.1]);shifted={str(k):float(np.var(1-.1*k+noise)) for k in [2,15]}
x=np.array([-1.,1.,-1.,1.]);y=np.array([-1.,-1.,1.,1.])
rough=lambda z:float(np.sum(np.diff(z)**2))
complete=lambda z:float(sum((z[i]-z[j])**2 for i in range(len(z)) for j in range(i+1,len(z))))
constant=[{'stipulated_truth':truth,'variance':float(np.var([value]*10)),'gate':Agent().dynamic_rsd([value]*10,0)} for truth,value in [('correct',1.),('incorrect',0.)]]
student=torch.tensor([2.,0.],requires_grad=True);teacher_logits=torch.zeros(2);teacher=torch.softmax(teacher_logits,dim=0)
loss=torch.nn.functional.kl_div(torch.log_softmax(student,dim=0),teacher,reduction='sum');loss.backward()
saturated=torch.tensor([20.,0.],requires_grad=True);ce=torch.nn.functional.cross_entropy(saturated[None,:],torch.tensor([0]));ce.backward()
q=math.exp(-20)/(1+math.exp(-20))
result={'scope':'Supplied simulation plus authored mathematical/numerical diagnostics; no model training, distillation or real context-collapse measurement.',
        'seeded_original_execution':'ORIGINAL_SEED0.txt','seed_audit_counts':counts,'variance_ranges':{str(k):[min(v),max(v)] for k,v in variances.items()},
        'exact_arithmetic':{'noise_interval_width':.2,'population_variance_upper_bound':.2**2/4,'high_gate_threshold':.5,'expected_ddof0_variance_n10_uniform_noise':.9*(.1**2/3),'qualification':'Variance strictly below0.01 for generic interior draws; exact upper-bound equality would enter healthy branch. Floating arithmetic qualifications remain.'},
        'identical_noise_pressure_shift_variance':shifted,
        'permutation_counterexample':{'first':x.tolist(),'second':y.tolist(),'variances':[float(np.var(x)),float(np.var(y))],'adjacent_difference_energy':[rough(x),rough(y)],'complete_graph_energy_over_n_squared':[complete(x)/len(x)**2,complete(y)/len(y)**2]},
        'constant_quality_counterexamples':constant,
        'zero_teacher_logits':{'teacher_probabilities':teacher.tolist(),'student_gradient':student.grad.tolist(),'nonzero_gradient':bool(torch.any(student.grad!=0))},
        'saturated_float32':{'logits':saturated.detach().tolist(),'computed_gradient':saturated.grad.tolist(),'gradient_sum':float(saturated.grad.sum()),'stable_mathematical_reference':[-q,q],'scope':'One synthetic cross-entropy example; not an RSD experiment or estimate of affected published work.'}}
assert counts=={'2.0:FROZEN':1000,'15.0:FROZEN':1000}
assert rough(x)!=rough(y) and np.var(x)==np.var(y)
assert result['zero_teacher_logits']['nonzero_gradient']
(P/'RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'gate_counts':counts,'variance_ranges':result['variance_ranges'],'path_energies':[rough(x),rough(y)],'teacher_gradient':student.grad.tolist(),'saturated_gradient':saturated.grad.tolist()},indent=2))
