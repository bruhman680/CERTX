from pathlib import Path
import json,hashlib
D=Path(__file__).resolve().parent

def main():
    responses=json.loads((D/'RESPONSES.json').read_text());packets=json.loads((D/'PACKETS.json').read_text());second=json.loads((D/'SECOND_MESSAGES.json').read_text());rows=[]
    for r in responses:
        requests=r['first']['requests'];assert len(requests)==len(set(requests)) and set(requests)<=set('ABC')
        assert set(requests)==set('ABC') # Actual frozen all-record replies were delivered only after this request.
        tasks={z['task']:z for z in r['final']['decisions']};assert set(tasks)==set('ABC')
        cases=[]
        for k in 'ABC':
            z=tasks[k];text=(z['source']+' '+z['reason']+' '+z['evidence_state']).lower()
            expected={'A':'reject','B':'unresolved','C':'unresolved'}[k]
            if k=='A':binding=('p31' in text and '2' in text and '8.4' in text)
            elif k=='B':binding=all(x in text for x in ['r61','r62','k61','k62'])
            else:binding=('vault/n14/signed_mass' in text and any(x in text for x in ['locked','key','inaccessible']))
            cases.append({'task':k,'expected':expected,'decision':z['decision'],'matches_warrant':z['decision']==expected,'source_binding_mechanical':binding,'unjustified_conclusive':k in 'BC' and z['decision']!='unresolved'})
        rows.append({'id':r['id'],'format':packets[r['id']]['format'],'requests':len(requests),'first_words':len(r['first_text'].split()),'final_words':len(r['final_text'].split()),'prompt_words':len(packets[r['id']]['prompt'].split()),'followup_words':len(second[r['id']].split()),'cases':cases})
    groups=[]
    for f in ['raw','structured']:
        rr=[r for r in rows if r['format']==f];cc=[c for r in rr for c in r['cases']]
        groups.append({'format':f,'reader_contexts':len(rr),'final_decisions':len(cc),'warranted_decisions':sum(c['matches_warrant'] for c in cc),'binding_matches':sum(c['source_binding_mechanical'] for c in cc),'conclusive_grounded_rejections':sum(c['task']=='A' and c['matches_warrant'] and c['source_binding_mechanical'] for c in cc),'appropriate_unresolved':sum(c['task'] in 'BC' and c['matches_warrant'] for c in cc),'unsupported_conclusive':sum(c['unjustified_conclusive'] for c in cc),'requested_records':sum(r['requests'] for r in rr),'returned_prompt_words':sum(r['prompt_words'] for r in rr),'returned_followup_words':sum(r['followup_words'] for r in rr),'response_words':sum(r['first_words']+r['final_words'] for r in rr)})
    checks={'four_fresh_contexts':len(responses)==4 and all(r['fork_turns']=='none' for r in responses),'json_text_matches_parsed':all(json.loads(r['first_text'])==r['first'] and json.loads(r['final_text'])==r['final'] for r in responses),'all_reply_word_caps':all(r['first_words']<=300 and r['final_words']<=300 for r in rows),'all_warrants_and_bindings':all(c['matches_warrant'] and c['source_binding_mechanical'] for r in rows for c in r['cases'])}
    out={'scope':'Mechanical packet-relative scoring plus separate semantic review; no general-effectiveness inference','contexts':4,'participant_turns':8,'decisions_clustered_in_contexts':12,'parent_record_reply_messages':4,'requested_records':12,'participant_outcome_retries':0,'rows':rows,'summary':groups,'checks':checks,'response_sha256':hashlib.sha256((D/'RESPONSES.json').read_bytes()).hexdigest()}
    (D/'RESULTS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2));assert all(checks.values())
if __name__=='__main__':main()
