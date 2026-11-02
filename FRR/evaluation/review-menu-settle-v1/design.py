from design_reference import cases,review as reference_review
LABELS=('YES','NO','WITHHOLD','UNKNOWN')
MENUS={f'rotation_{i}':LABELS[i:]+LABELS[:i] for i in range(4)}
MENUS['no_list']=None
ENDING='Return only YES, NO, WITHHOLD, or UNKNOWN.\nResponse:'

def render(c,kind,menu):
 original=reference_review(c,kind,False,'unused');assert original.endswith(ENDING)
 values=MENUS[menu]
 sentence=('Return only '+', '.join(values[:-1])+', or '+values[-1]+'.' if values else 'Return only the answer.')
 return original[:-len(ENDING)]+sentence+'\nResponse:'

def queries():
 out=[]
 for c in cases():
  out.append({'id':f'q_{len(out):03d}','case_id':c['id'],'frame':c['frame'],'state':c['state'],'expected':c['expected'],'kind':'initial','menu':None,'first_option':None,'prompt':c['prompt']})
  for kind in ['none','verified']:
   for menu,values in MENUS.items():
    out.append({'id':f'q_{len(out):03d}','case_id':c['id'],'frame':c['frame'],'state':c['state'],'expected':c['expected'],'kind':kind,'menu':menu,'first_option':values[0] if values else None,'prompt':render(c,kind,menu)})
 assert len(out)==231 and len({q['prompt'] for q in out})==231
 return out
