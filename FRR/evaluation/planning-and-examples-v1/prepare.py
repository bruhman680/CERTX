"""Freeze response allowance x examples before any new model forward."""
from pathlib import Path
import json
from task import render,normalized_visible
from evidence import STATES,parse
from runtime_reference import sha,dump_new

ROOT=Path(__file__).resolve().parent

def main():
    cases=[]
    for style,target,other in [('lines','Juniper','Hemlock'),('bracket','Hemlock','Juniper')]:
        for i,state in enumerate(STATES):
            for order in range(2):
                recs=[(target,state),(other,STATES[(i+1)%3])]
                if order:recs.reverse()
                body='\n\n'.join(f'Record {j+1}:\nPlot: {n}\nStatus: {s}' for j,(n,s) in enumerate(recs))
                source='Target plot: '+target+'\n\n'+body;p=parse(source)
                for kind in ('selected_visible','none_available','other_visible','none_unavailable'):
                    visible=p['crop'] if kind=='selected_visible' else p['other_crop'] if kind=='other_visible' else None
                    if visible is not None and style=='bracket':
                        lines=visible.splitlines();visible='[plot='+lines[0][6:]+'; status='+lines[1][8:]+']'
                    c={'id':f'c_{len(cases):03d}','target':target,'source':source,'state':state,'style':style,
                       'kind':kind,'visible_display':visible,'archive_available':kind!='none_unavailable'}
                    canonical=normalized_visible(c)
                    if canonical is not None:assert canonical in (p['crop'],p['other_crop'])
                    cases.append(c)
    queries=[];links=[];seen={}
    for c in cases:
        for examples in (False,True):
            for response in ('direct8','direct64','plan64'):
                prompt=render(c,examples,response);cap=8 if response=='direct8' else 64
                key=(prompt,cap)
                if key not in seen:
                    qid=f'q_{len(queries):03d}';seen[key]=qid
                    queries.append({'id':qid,'prompt':prompt,'examples':examples,'response':response,'cap':cap})
                links.append({'case_id':c['id'],'query_id':seen[key],'examples':examples,'response':response})
    assert len(cases)==48 and len(queries)==96 and len(links)==288
    dump_new(ROOT/'DATA.json',cases);dump_new(ROOT/'QUERIES.json',queries);dump_new(ROOT/'LINKS.json',links)
    acq=ROOT.parent/'simple-readout-acquisition-v1/run/canonical'
    deps=[acq/n for n in ('MANIFEST.json','final/adapter.safetensors','final/manifest.json')]
    names=['DATA.json','QUERIES.json','LINKS.json','PROTOCOL.md','task.py','generate.py','prepare.py',
           'run_study.py','score.py','test_study.py','routing_reference.py','evidence.py','runtime_reference.py','lora_cpu.py']
    dump_new(ROOT/'FREEZE.json',{'sha256':{n:sha(ROOT/n) for n in names},
        'dependencies':{str(p):sha(p) for p in deps},'timing':'before tokenizer/model load and all new forwards'})
    print('Frozen48logical scenarios,96router probes,288linked policy routes;no training')

if __name__=='__main__':main()
