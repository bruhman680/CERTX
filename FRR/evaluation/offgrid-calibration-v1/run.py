from pathlib import Path
import json,hashlib,ast,sys
import numpy as np
R=Path(__file__).resolve().parent;PARENT=R.parent/'joint-noise-candidates-v1';SOURCE=R.parent/'claude-open-world-intake-v1/sources/FRR/lineage/sources/claude-open-world-guard-2026-11-02/open_world_guard.py'
sys.path.insert(0,str(PARENT));from run import wilson,labels
GRID=np.array([.025,.0375,.05,.075,.1]);CLASSES=('IND','DIFF','SHARED');WORLDS=('IND','DIFF','COMMON')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,v):
 with p.open('x') as f:json.dump(v,f,separators=(',',':'),allow_nan=False);f.write('\n')
def main():
 pins=json.loads((R/'FREEZE.json').read_text());assert all(sha(Path(p))==v for p,v in pins['files'].items());ns={};exec(compile(ast.parse(SOURCE.read_text().split('# ---------------- PHASE 1')[0]),str(SOURCE),'exec'),ns);gen,feats=ns['gen'],ns['feats'];old=json.loads((PARENT/'PARAMETERS.json').read_text());lookup={(x['seed'],x['M'],x['cls'],x['noise']):x for x in old};params=[];cells=[];summary=[]
 for seed in (2026110311,2026110312):
  for M in (400,1600):
   ref=[]
   for j,w in enumerate(WORLDS):
    for g,eps in enumerate(GRID):
     key=(seed,M,CLASSES[j],float(eps))
     if key in lookup:
      d=lookup[key];mu=np.array(d['mean']);sd=np.array(d['sd']);threshold=d['threshold'];origin='parent exact'
     else:
      f=feats(*gen(w,M,800,np.random.default_rng(np.random.SeedSequence([seed,M,j,g,11])),eps))[0];mu=f.mean(0);sd=np.maximum(f.std(0),.001);fc=feats(*gen(w,M,800,np.random.default_rng(np.random.SeedSequence([seed,M,j,g,12])),eps))[0];threshold=float(np.quantile((((fc-mu)/sd)**2).mean(1),.99));origin='new noise pair'
     ref.append((mu,sd,threshold));params.append(dict(seed=seed,M=M,cls=CLASSES[j],noise=float(eps),mean=mu.tolist(),sd=sd.tolist(),threshold=threshold,origin=origin))
   for j,w in enumerate(WORLDS):
    for eg,eps in enumerate((.0375,.05,.075)):
     es=[seed,M,j,eg,13];a,b=gen(w,M,300,np.random.default_rng(np.random.SeedSequence(es)),eps);F=feats(a,b)[0];D=np.stack([(((F-mu)/sd)**2).mean(1)/threshold for mu,sd,threshold in ref],1);pair=D<=1;k=np.random.default_rng(np.random.SeedSequence([seed,M,j,eg,14])).binomial(4000,eps,300);lo,hi=wilson(k,4000);gold=(GRID[None,:]>=lo[:,None])&(GRID[None,:]<=hi[:,None]);coarse=np.tile(np.isin(GRID,[.025,.05,.1]),(300,1));dense=np.ones((300,5),bool);oracle=np.tile(GRID==eps,(300,1));arms={}
     for name,allow in [('coarse_union',coarse),('dense_union',dense),('coarse_gold4000',coarse&gold),('dense_gold4000',gold),('oracle',oracle)]:
      filtered=pair&np.tile(allow,(1,3));bits=(filtered.reshape(-1,3,5).any(2)*np.array([1,2,4])).sum(1).astype(int);lab=labels(bits);trueindex=int(np.flatnonzero(GRID==eps)[0]);arms[name]=dict(class_masks=bits.tolist(),labels=lab.tolist(),noise_masks=(allow*(1<<np.arange(5))).sum(1).astype(int).tolist());summary.append(dict(seed=seed,M=M,world=w,noise=eps,arm=name,n=300,true_pair_compatible=float(filtered[:,j*5+trueindex].mean()),correct_singleton=float((lab==j).mean()),wrong_singleton=float(((lab<3)&(lab!=j)).mean()),UNKNOWN=float((lab==3).mean()),UNRESOLVED=float((lab==4).mean()),calibration_grid_empty=float((~allow.any(1)).mean()),true_noise_retained=float(allow[:,trueindex].mean())))
     cells.append(dict(seed=seed,M=M,world=w,noise=eps,eval_seed=es,observed_A_B_sha256=hashlib.sha256(a.tobytes()+b.tobytes()).hexdigest(),pair_masks=(pair*(1<<np.arange(15))).sum(1).astype(int).tolist(),gold4000=k.tolist(),arms=arms))
 dump(R/'PARAMETERS.json',params);dump(R/'RAW.json',{'numpy':np.__version__,'grid':GRID.tolist(),'classes':CLASSES,'cells':cells});dump(R/'SUMMARY.json',{'rows':summary});assert all(sha(Path(p))==v for p,v in pins['files'].items());dump(R/'CHECKS.json',{'status':'pass','input_cells':36,'observations':10800,'arm_evaluations':54000,'parent_parameters_unchanged':True,'frozen_files_unchanged':True});print(json.dumps({'shared_M1600':[(x['seed'],x['noise'],x['arm'],x['correct_singleton'],x['calibration_grid_empty']) for x in summary if x['M']==1600 and x['world']=='COMMON']},indent=2))
if __name__=='__main__':main()
