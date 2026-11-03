from pathlib import Path
import hashlib,json,ast
import numpy as np
R=Path(__file__).resolve().parent
SOURCE=R.parent/'claude-open-world-intake-v1/sources/FRR/lineage/sources/claude-open-world-guard-2026-11-02/open_world_guard.py'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,v):
 with p.open('x') as f:json.dump(v,f,indent=2,allow_nan=False);f.write('\n')
def main():
 pins=json.loads((R/'FREEZE.json').read_text());assert all(sha(Path(p))==v for p,v in pins['files'].items())
 source=ast.parse(SOURCE.read_text().split('# ---------------- PHASE 1')[0]);ns={};exec(compile(source,str(SOURCE),'exec'),ns);gen,feats=ns['gen'],ns['feats']
 names=('IND','DIFF','SHARED');worlds=('IND','DIFF','COMMON');summary=[];params=[];raw=[]
 for seed in (2026110301,2026110302):
  for M in (400,1600):
   refs=[]
   for j,w in enumerate(worlds):
    f=feats(*gen(w,M,800,np.random.default_rng(np.random.SeedSequence([seed,M,j,1])),.05))[0];mu=f.mean(0);sd=np.maximum(f.std(0),.001)
    fc=feats(*gen(w,M,800,np.random.default_rng(np.random.SeedSequence([seed,M,j,2])),.05))[0];dist=(((fc-mu)/sd)**2).mean(1);bands={q:float(np.quantile(dist,q)) for q in (.95,.99)};refs.append((mu,sd,bands));params.append({'seed':seed,'M':M,'class':names[j],'mean':mu.tolist(),'sd':sd.tolist(),'thresholds':bands})
   for j,w in enumerate(worlds):
    for eps in (.025,.05,.10):
     evalseed=[seed,M,j,3];a,b=gen(w,M,500,np.random.default_rng(np.random.SeedSequence(evalseed)),eps);f=feats(a,b)[0];inputsha=hashlib.sha256(a.tobytes()+b.tobytes()).hexdigest();D=np.stack([(((f-mu)/sd)**2).mean(1) for mu,sd,_ in refs],1)
     for q in (.95,.99):
      dn=D/np.array([bands[q] for _,_,bands in refs]);mask=(dn<=1);bits=(mask*np.array([1,2,4])).sum(1);count=mask.sum(1);labels=np.full(500,4,dtype=int);labels[count==0]=3;single=count==1;labels[single]=mask[single].argmax(1)
      row={'seed':seed,'M':M,'world':w,'noise':eps,'quantile':q,'n':500,'true_class_compatible':float(mask[:,j].mean()),'correct_singleton':float((labels==j).mean()),'wrong_singleton':float(((labels<3)&(labels!=j)).mean()),'UNKNOWN':float((labels==3).mean()),'UNRESOLVED':float((labels==4).mean())};assert abs(sum(row[k] for k in ['correct_singleton','wrong_singleton','UNKNOWN','UNRESOLVED'])-1)<1e-12;summary.append(row)
      raw.append({'seed':seed,'M':M,'world':w,'noise':eps,'quantile':q,'evaluation_seed':evalseed,'observed_A_B_sha256':inputsha,'labels':labels.tolist(),'candidate_masks':bits.tolist(),'normalized_distances':dn.tolist()})
 dump(R/'PARAMETERS.json',params);dump(R/'SUMMARY.json',{'numpy':np.__version__,'source_sha256':sha(SOURCE),'rows':summary});dump(R/'RAW_COMPACT.json',{'label_vocabulary':['IND','DIFF','SHARED','UNKNOWN','UNRESOLVED'],'rows':raw})
 assert all(sha(Path(p))==v for p,v in pins['files'].items());dump(R/'CHECKS.json',{'status':'pass','cells':len(summary),'paired_evaluations':18000,'threshold_evaluations':36000,'frozen_files_unchanged':True,'every_cell_partition_sums_to_one':True})
 print(json.dumps({'cells':len(summary),'matched_noise_shared':[(x['seed'],x['M'],x['true_class_compatible']) for x in summary if x['world']=='COMMON' and x['noise']==.05 and x['quantile']==.99],'mismatched_shared_M1600':[(x['seed'],x['noise'],x['true_class_compatible']) for x in summary if x['world']=='COMMON' and x['noise']!=.05 and x['M']==1600 and x['quantile']==.99]},indent=2))
if __name__=='__main__':main()
