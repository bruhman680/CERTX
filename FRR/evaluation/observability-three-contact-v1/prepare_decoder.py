"""Fixed decoder arms; fixture preparation only, no model inference."""
from pathlib import Path
from copy import deepcopy
import common as c
def main():
    h=c.H/'decoder';h.mkdir(exist_ok=True)
    view=c.base_view();jobs=[]
    c.save(h/'PLAN.json',{'seeds':[27401,27402,27403],'temperature':.8,'top_p':[.9,1.0],
      'same_exact_input_all_cases':True,'greedy_reference':'prototype raw/01.json',
      'scope':'three paired random seeds, one context; diversity is not competence',
      'profile':'teacher-forced greedy path nucleus sizes; not all possible sampled paths'})
    for seed in [27401,27402,27403]:
      for p in [.9,1.0]:
        name=f'decode_p{int(p*100)}_s{seed}';store=h/'worlds'/name;store.parent.mkdir(exist_ok=True)
        w,event=c.clone(store)
        try:c.save(h/'preparation'/f'{name}.json',{'actor':'operator','event':event,'snapshot':w.checkpoint()})
        finally:w.close()
        jobs.append({'case_id':name,'messages':deepcopy(view['messages']),'decoder':'nucleus','temperature':.8,'top_p':p,'seed':seed,
          'world_store':str(store),'max_turns':1,'metadata':{'experiment':'decoder','included_entries':view['included_entries']}})
    c.save(h/'jobs.json',jobs)
if __name__=='__main__':main()
