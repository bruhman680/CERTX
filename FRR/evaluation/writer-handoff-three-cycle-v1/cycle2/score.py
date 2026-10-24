from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parent.parent;D=ROOT/'cycle2'
def main():
 responses=json.loads((D/'RESPONSES.json').read_text());packets=json.loads((D/'READER_PACKETS.json').read_text());gold=json.loads((ROOT/'GOLD.json').read_text());rows=[]
 for r in responses:
  p=packets[r['id']];first=r['first'];final={z['id']:z for z in r['final']['answers']};assert set(final)==set(gold)
  cases=[]
  for q,z in final.items():
   basis=z['basis'];
   if q=='Q1':support=all(t in basis for t in ['82','80']) and ('2' in basis or 'current' in basis.lower())
   elif q=='Q2':support=all(t in basis for t in ['103','105'])
   elif q=='Q3':support=all(t in basis for t in ['99.994','100.014']) and any(t in basis.lower() for t in ['outside','both'])
   else:support=any(t in basis.lower() for t in ['unknown','not established','cannot be established','does not establish','establish neither']) and any(t in basis.lower() for t in ['decoded','encrypted','key'])
   cases.append({'question':q,'answer':z['answer'],'gold':gold[q]['answer'],'matches_gold':z['answer']==gold[q]['answer'],'mechanical_basis_match':support,'source_present':bool(z.get('source'))})
  rows.append({'id':r['id'],'writer':p['writer'],'access':p['original_access'],'request_original':first['request_original'],'original_supplied':p['original_access'] and first['request_original'],'first_words':len(r['first_text'].split()),'final_words':len(r['final_text'].split()),'cases':cases})
 summary={'reader_contexts':4,'reader_turns':8,'writer_contexts':2,'writer_turns':2,'final_decisions_clustered':16,'correct_known_task_answers':sum(c['matches_gold'] for r in rows for c in r['cases']),'mechanically_grounded':sum(c['matches_gold'] and c['mechanical_basis_match'] and c['source_present'] for r in rows for c in r['cases']),'conclusive_grounded_no':sum(c['question'] in ['Q1','Q2'] and c['matches_gold'] and c['mechanical_basis_match'] for r in rows for c in r['cases']),'appropriate_unresolved':sum(c['question'] in ['Q3','Q4'] and c['matches_gold'] and c['mechanical_basis_match'] for r in rows for c in r['cases']),'original_requests':sum(r['request_original'] for r in rows),'original_supplied':sum(r['original_supplied'] for r in rows),'participant_outcome_retries':0}
 checks={'all_text_parsed_matches':all(json.loads(r['first_text'])==r['first'] and json.loads(r['final_text'])==r['final'] for r in responses),'fresh_contexts':all(r['fork_turns']=='none' for r in responses),'word_caps':all(r['first_words']<=300 and r['final_words']<=300 for r in rows),'all_task_answers_match_and_grounded':summary['mechanically_grounded']==16}
 out={'scope':'Mechanical fixed-question scoring; semantic review separate, not generic evaluator','rows':rows,'summary':summary,'checks':checks,'response_sha256':hashlib.sha256((D/'RESPONSES.json').read_bytes()).hexdigest()}
 (D/'RESULTS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2));assert all(checks.values())
if __name__=='__main__':main()
