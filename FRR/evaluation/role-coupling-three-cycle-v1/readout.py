"""External cycle readout: literal artifacts and actual action opportunities."""
from pathlib import Path
import json, argparse, hashlib

ROOT=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text())

def describe(cycle):
    h=ROOT/f'cycle{cycle}';r=h/'run';result=read(r/'RESULTS.json');cfg=read(h/'design/CONDITION.json')
    assert result['status']=='pass' and result['actual_model_calls']==6
    arms={}
    for arm in cfg['arms']:
        rows=[read(r/'records'/f'{arm}_t{n}.json') for n in range(1,4)]
        raw=[read(r/'raw'/f'{arm}_t{n}.json') for n in range(1,4)]
        errors=[]
        for n,row in enumerate(rows,1):
            for action in row['model_initiated_actions']:
                feedback=action['feedback']
                if feedback.get('exit_code') not in (None,0) or feedback.get('boundary') is not None:
                    errors.append({'turn':n,'feedback':feedback,'has_later_reply':n<3})
        arms[arm]={
            'input_tokens':[x['input_tokens'] for x in rows],
            'output_tokens':[x['output_tokens'] for x in rows],
            'unique_input_token_sequences':len({tuple(x['input_token_ids']) for x in raw}),
            'unique_output_token_sequences':len({tuple(x['generated_token_ids']) for x in raw}),
            'output_sha256':[hashlib.sha256(x['text'].encode()).hexdigest() for x in raw],
            'complete_cells':sum(x['complete_cells'] for x in rows),
            'incomplete_fences':sum(x['incomplete_fences'] for x in rows),
            'model_initiated_actions':sum(len(x['model_initiated_actions']) for x in rows),
            'automatic_note_operations':sum(len(x['automatic_note_operations']) for x in rows),
            'stop_reasons':[x['stop'] for x in rows],
            'literal_reply_bytes':sum(len(x['text'].encode()) for x in raw),
            'model_action_errors':errors,
            'feedback_messages':[x['feedback_for_next_input'] for x in rows],
        }
    return {'status':'pass','cycle':cycle,'arms':arms,'actual_model_calls':6,
            'weights_unchanged':result['weights_unchanged'],'main_unchanged':result['main_unchanged'],
            'main_entry':1630,'training_updates':0,
            'scope':'two short dependent greedy trajectories, not six independent replications; no semantic success score'}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--cycle',type=int,required=True,choices=(1,2,3));a=p.parse_args()
    out=describe(a.cycle)
    with (ROOT/f'cycle{a.cycle}'/'READOUT.json').open('x') as f:json.dump(out,f,indent=2,sort_keys=True)
    print(json.dumps(out))
