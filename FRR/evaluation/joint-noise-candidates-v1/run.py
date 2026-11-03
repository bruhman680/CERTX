from pathlib import Path
import json,hashlib,ast
import numpy as np
R=Path(__file__).resolve().parent;SOURCE=R.parent/'claude-open-world-intake-v1/sources/FRR/lineage/sources/claude-open-world-guard-2026-11-02/open_world_guard.py'
GRID=np.array([.025,.05,.10]);NAMES=('IND','DIFF','SHARED');WORLDS=('IND','DIFF','COMMON')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,x):
 with p.open('x') as f:json.dump(x,f,separators=(',',':'),allow_nan=False);f.write('\n')
def wilson(k,n):
 p=np.asarray(k)/n;z=1.96;d=1+z*z/n;c=(p+z*z/(2*n))/d;h=z*np.sqrt(p*(1-p)/n+z*z/(4*n*n))/d;return c-h,c+h
def project(pair):
 return ((pair.reshape(-1,3,3).any(2))*np.array([1,2,4])).sum(1).astype(int)
def labels(bits):
 out=np.full(len(bits),4);out[bits==0]=3
 for b,j in [(1,0),(2,1),(4,2)]:out[bits==b]=j
 return out

def main():
 pins=json.loads((R/'FREEZE.json').read_text());assert all(sha(Path(p))==v for p,v in pins['files'].items());ns={};exec(compile(ast.parse(SOURCE.read_text().split('# ---------------- PHASE 1')[0]),str(SOURCE),'exec'),ns);gen,feats=ns['gen'],ns['feats'];params=[];cells=[];summary=[]
 for seed in (2026110311,2026110312):
  for M in (400,1600):
   ref=[]
   for j,w in enumerate(WORLDS):
    for g,eps in enumerate(GRID):
     a=feats(*gen(w,M,800,np.random.default_rng(np.random.SeedSequence([seed,M,j,g,1])),eps))[0];mu=a.mean(0);sd=np.maximum(a.std(0),.001);b=feats(*gen(w,M,800,np.random.default_rng(np.random.SeedSequence([seed,M,j,g,2])),eps))[0];threshold=float(np.quantile((((b-mu)/sd)**2).mean(1),.99));ref.append((mu,sd,threshold));params.append(dict(seed=seed,M=M,cls=NAMES[j],noise=float(eps),mean=mu.tolist(),sd=sd.tolist(),threshold=threshold))
   for j,w in enumerate(WORLDS):
    for g,eps in enumerate(GRID):
     es=[seed,M,j,g,3];a,b=gen(w,M,300,np.random.default_rng(np.random.SeedSequence(es)),eps);F=feats(a,b)[0];D=np.stack([(((F-mu)/sd)**2).mean(1)/threshold for mu,sd,threshold in ref],1);pair=D<=1;pairbits=(pair*(1<<np.arange(9))).sum(1).astype(int)
     rg=np.random.default_rng(np.random.SeedSequence([seed,M,j,g,4]));k40=rg.binomial(40,eps,300);k400=k40+rg.binomial(360,eps,300)
     allnoise=np.ones((300,3),bool);fixed=np.tile(GRID==.05,(300,1));oracle=np.tile(GRID==eps,(300,1));allowed={'fixed':fixed,'union':allnoise,'oracle':oracle}
     for G,K in [(40,k40),(400,k400)]:
      lo,hi=wilson(K,G);allowed['gold'+str(G)]=(GRID[None,:]>=lo[:,None])&(GRID[None,:]<=hi[:,None])
     arms={}
     for name,allow in allowed.items():
      filtered=pair&np.tile(allow,(1,3));bits=project(filtered);lab=labels(bits);truepair=filtered[:,j*3+g];arm=dict(class_masks=bits.tolist(),labels=lab.tolist(),allowed_noise_masks=(allow*np.array([1,2,4])).sum(1).astype(int).tolist());arms[name]=arm
      summary.append(dict(seed=seed,M=M,world=w,noise=float(eps),arm=name,n=300,true_pair_compatible=float(truepair.mean()),correct_singleton=float((lab==j).mean()),wrong_singleton=float(((lab<3)&(lab!=j)).mean()),UNKNOWN=float((lab==3).mean()),UNRESOLVED=float((lab==4).mean()),calibration_grid_empty=float((~allow.any(1)).mean()),true_noise_retained=float(allow[:,g].mean())))
     cells.append(dict(seed=seed,M=M,world=w,noise=float(eps),eval_seed=es,observed_A_B_sha256=hashlib.sha256(a.tobytes()+b.tobytes()).hexdigest(),pair_masks=pairbits.tolist(),gold40=k40.tolist(),gold400=k400.tolist(),arms=arms))
 dump(R/'PARAMETERS.json',params);dump(R/'RAW.json',{'numpy':np.__version__,'grid':GRID.tolist(),'classes':NAMES,'labels':['IND','DIFF','SHARED','UNKNOWN','UNRESOLVED'],'pair_order':'class-major then noise index','cells':cells});dump(R/'SUMMARY.json',{'rows':summary});assert all(sha(Path(p))==v for p,v in pins['files'].items());dump(R/'CHECKS.json',{'status':'pass','input_cells':36,'observations':10800,'arm_evaluations':54000,'frozen_files_unchanged':True});print(json.dumps({'cells':36,'arm_evaluations':54000,'shared_M1600':[(x['seed'],x['noise'],x['arm'],x['correct_singleton'],x['UNKNOWN']) for x in summary if x['M']==1600 and x['world']=='COMMON']},indent=2))
if __name__=='__main__':main()
