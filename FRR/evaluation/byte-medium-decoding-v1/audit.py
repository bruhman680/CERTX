"""External audit of inputs, outputs and physical effects; no model calls."""
from collections import Counter
import re,json
import run as r
s=r.s;H=r.H

def main():
    r.guard();assert not (H/'RUN.lock').exists();tok=s.c.tokenizer()
    prior=s.read(s.E/'byte-medium-model-pilot-v1/changing/raw/000001.json')
    initial=s.read(s.E/'byte-medium-model-pilot-v1/changing/INITIAL_INPUT.json')
    rows=[]
    for cfg in r.CONFIGS:
        d=H/cfg['name'];assert s.read(d/'STATE.json')==dict(turn=1,paused=True)
        assert not (d/'PENDING.json').exists() and not (d/'world/PENDING.json').exists()
        assert s.read(d/'INITIAL_INPUT.json')==initial
        raw=s.read(d/'RAW.json');rr=s.read(d/'world/replies/reply_000001.json');rec=s.read(d/'RECORD.json');bundle=s.read(d/'SNAPSHOT.json')
        batch=rr['actor_batch'];tick=rr['physical_tick']
        assert raw['messages']==initial['messages'] and raw['input_token_ids']==initial['input_token_ids']==tok.apply_chat_template(raw['messages'],tokenize=True,add_generation_prompt=True)
        assert raw['decoder']==cfg['decoder'] and raw.get('seed')==cfg['seed']
        if cfg['seed'] is not None:assert raw['temperature']==0.8 and raw['top_p']==0.95
        assert tok.decode(raw['generated_token_ids'],skip_special_tokens=True)==raw['text']==rr['raw_text']==batch['raw_text']
        assert raw['stop'] in ('eos','token_limit') and 0<len(raw['generated_token_ids'])<=256
        assert (raw['stop']=='eos' and raw['generated_token_ids'][-1]==tok.eos_token_id) or (raw['stop']=='token_limit' and len(raw['generated_token_ids'])==256)
        assert batch['parsed']==s.a.base.parse_notebook(raw['text']) and batch['automatic_note_append'] is False
        cells=[x for x in batch['parsed']['cells'] if x['executable']]
        assert len(batch['operations'])==(len(cells) if batch['status']=='completed' else 0)
        for op,cell in zip(batch['operations'],cells):assert op['source']==cell['source'] and op['channel']==('python' if cell['language']=='python' else 'shell')
        assert batch['start_step']==0 and batch['before_id']==s.read(s.E/'byte-medium-model-pilot-v1/seed/bundle.json')['id']
        assert tick['source']==s.a.tick_source('changing') and tick['step']==batch['end_step']+1 and tick['before_id']==batch['after_id']
        assert tick==s.read(d/'world/world/engine/events'/f"{tick['step']:06d}.json")
        assert tick['after_id']==bundle['id']==rec['world_id']
        assert rec['raw_sha256']==s.sha(d/'RAW.json') and rec['adapter_reply_sha256']==s.sha(d/'world/replies/reply_000001.json')
        clock=dict(replies=1,ticks=1,actor_operations=len(batch['operations']));assert s.read(d/'world/STATE.json')==clock
        assert s.read(d/'OBSERVATION.json')==s.observation(d,bundle,tick['step'],clock,1)
        verified=s.a.c.verify(d/'world/world');assert verified['bundle_id']==bundle['id'] and verified['step']==tick['step']
        assert s.read(d/'world/world/engine/STATE.json')['paused'] and not (d/'world/world/engine/LOCK.json').exists()
        sentences=re.split(r'(?<=[.!?])\s+',raw['text']);dominant,count=Counter(sentences).most_common(1)[0]
        rows.append(dict(branch=cfg['name'],seed=cfg['seed'],input_tokens=len(raw['input_token_ids']),output_tokens=len(raw['generated_token_ids']),stop=raw['stop'],seconds=raw['seconds'],actor_operations=len(batch['operations']),physical_exit_code=tick['receipt']['exit_code'],world_paths=[x[0] for x in bundle['entries']],dominant_exact_sentence=dominant,dominant_sentence_occurrences=count,sentence_segments=len(sentences),exact_latest_packet_copy=raw['text']==initial['messages'][-1]['content'],exact_prior_greedy_token_match=raw['generated_token_ids']==prior['generated_token_ids']))
    assert rows[0]['exact_prior_greedy_token_match']
    out=dict(status='pass',model_calls=3,conditions=rows,initial_contexts_token_identical=True,greedy_prior_replay_exact=True,protected_files_unchanged=len(r.protected()),reference38_unchanged=True,prior_pilots_unchanged=True,main1630_unchanged=True,training_updates=0,cleanly_paused=True,descriptors='Exact sentence segments split after .!? plus whitespace; no accuracy or internal-state score.')
    s.a.base.atomic(H/'RESULTS.json',out);print(json.dumps(out,indent=2))
if __name__=='__main__':main()
