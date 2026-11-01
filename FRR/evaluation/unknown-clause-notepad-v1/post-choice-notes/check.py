from pathlib import Path
import sys,json,os
ROOT=Path(__file__).resolve().parent;PARENT=ROOT.parent;sys.path.insert(0,str(PARENT))
from io_utils import sha,dump_new,append
from study import BASE,ACQ,check_freeze

def prepare():
 raw=[json.loads(s) for s in (PARENT/'run/RAW.jsonl').read_text().splitlines()]
 assert len(raw)==560 and not any(p['decoded']['note_text'] for p in raw)
 qs=[];links=[];seen={}
 for name in ['Maple','Cedar','Hazel']:
  for state,answer in [('zero','NO'),('zero','UNKNOWN'),('absent','UNKNOWN')]:
   for example in [False,True]:
    source=f'Plot: {name}\nStatus: zero' if state=='zero' else '(no visible record)'
    intro='Write one short public evidence note about a recorded answer. Do not give a replacement answer. State what evidence is present or missing.'
    lesson='\n\nExample:\nVisible record:\nPlot: Iris\nStatus: positive\nRecorded answer: YES\nNOTE: The visible record explicitly says Status: positive.' if example else ''
    prompt=intro+lesson+'\n\nVisible record:\n'+source+'\nRecorded answer: '+answer+'\n\nNOTE:'
    if prompt not in seen:
     qid=f'q_{len(qs):03d}';seen[prompt]=qid;qs.append({'id':qid,'prompt':prompt,'source':source,'state':state,'recorded_answer':answer,'example':example})
    links.append({'name':name,'state':state,'recorded_answer':answer,'example':example,'query_id':seen[prompt]})
 assert len(qs)==14 and len(links)==18
 dump_new(ROOT/'QUERIES.json',qs);dump_new(ROOT/'LINKS.json',links)
 dump_new(ROOT/'FREEZE.json',{'timing':'after560primaryoutputs show zero notes; before all14followup outputs/model load','sha256':{n:sha(ROOT/n) for n in ['check.py','PROTOCOL.md','QUERIES.json','LINKS.json']},'dependencies':{str(p):sha(p) for p in [PARENT/'FREEZE.json',PARENT/'run/RAW.jsonl',PARENT/'run/SUMMARY.json',ACQ/'MANIFEST.json',ACQ/'final/adapter.safetensors']}})
 print('Frozen14unique note-only prompts;18nominal links')

def run():
 os.environ['HF_HUB_OFFLINE']='1';os.environ['HF_HUB_DISABLE_PROGRESS_BARS']='1'
 import torch
 from transformers import AutoTokenizer,AutoModelForCausalLM
 from runtime_reference import Guard,parameter_digest
 from lora_cpu import inject_lora,load_adapter
 from generate import generate
 check_freeze();f=json.loads((ROOT/'FREEZE.json').read_text());assert all(sha(ROOT/n)==h for n,h in f['sha256'].items());assert all(sha(Path(n))==h for n,h in f['dependencies'].items())
 out=ROOT/'run';out.mkdir();guard=Guard(5153960755,out/'RESOURCE.jsonl');m=json.loads((ACQ/'MANIFEST.json').read_text());assert sha(BASE/'model.safetensors')==m['base_pin']['weights_sha256']
 torch.set_num_threads(2);torch.manual_seed(73103);tok=AutoTokenizer.from_pretrained(BASE,local_files_only=True,trust_remote_code=False)
 model=AutoModelForCausalLM.from_pretrained(BASE,local_files_only=True,trust_remote_code=False,use_safetensors=True,torch_dtype=torch.float32,attn_implementation='eager')
 inject_lora(model,rank=4,alpha=8,dropout=0.);load_adapter(model,ACQ/'final',base_pin=m['base_pin']);assert parameter_digest(model,True)==m['final_digest']
 for q in json.loads((ROOT/'QUERIES.json').read_text()):
  p=generate(model,tok,q['prompt'],48,guard,q['id']);p.update({k:q[k] for k in ['source','state','recorded_answer','example']});append(out/'RAW.jsonl',p)
 assert parameter_digest(model,True)==m['final_digest'] and parameter_digest(model,False)==m['base_digest_after'];assert all(sha(ROOT/n)==h for n,h in f['sha256'].items());assert all(sha(Path(n))==h for n,h in f['dependencies'].items())
 dump_new(out/'RUN_MANIFEST.json',{'status':'complete','actual_generations':14,'nominal_links':18,'training_updates':0,'tool_actions':0,'weights_unchanged':True,'outcome_informed_diagnostic':True});print('Completed14note-only probes')
if __name__=='__main__':{'prepare':prepare,'run':run}[sys.argv[1]]()
