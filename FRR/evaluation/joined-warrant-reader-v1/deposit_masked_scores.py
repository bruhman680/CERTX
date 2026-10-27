"""Serialize the scorer's independent manual judgments; not an automatic semantic grader."""
import json,hashlib,datetime
from pathlib import Path
p=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
inputs=json.loads((p/'SCORER_INPUT.json').read_text())
k=json.loads((p/'KEY.json').read_text())
hashes={n:sha((p/n).read_bytes()) for n in ['SCORER_INPUT.json','KEY.json','SCORING.md']}
dims=['acceptance_verdict','action','numerical_consequence','supplied_premise_fidelity','uncertainty_and_conflict_fidelity','next_check_relevance','next_check_sufficiency_claim']
notes={
'case01':('Both corrected loads9, so complete-lot maximum9<=12.','Uses acquisition assignment joined to matching exact calibration; no false missingness.','No uncertainty relevant to acceptance remains.'),
'case02':('Both possible assignments computed: (9,9) passes and (3,15) fails; maxima9/15.','Uses complete-lot constraint and exact profile biases without inventing an assignment.','Identifies genuinely absent piece-to-profile assignment.'),
'case03':('Corrected R13 and S15; S exceeds14.','Uses supplied assignment and matching exact calibration.','Acceptance contradicted, rather than unresolved.'),
'case04':('R in[4,14] always passes; S in[9,19], passing iff jade bias>=5.','Preserves supplied assignments and bounded current biases; refuses wrong-date transfer.','Correctly localizes consequential uncertainty to current jade bias; copper uncertainty cannot change acceptance.'),
'case05':('T2 and U17; maximum17 exceeds11.','Recognizes agreed E3/E4 assignment is fixed by at-least-one-correct guarantee and joins it to E2 calibration.','Does not invent conflict or missing assignment; acceptance contradicted.'),
'case06':('E3 gives (2,17), failing; E4 gives(9,10), passing; maxima17/10.','Preserves exact calibration and equal-authority assignment-record contract.','Explicitly preserves supplied E3/E4 contradiction and both feasible assignments.'),
'case07':('Exact complete-population mean7<=8.','Uses applicable complete-population certificate.','Correctly says absent individual loads are unnecessary for mean criterion.'),
'case08':('Sharp maximum interval[7,28], justified by total28/nonnegativity and both endpoint examples.','Recognizes exact certificate applies and proves total28.','Correctly distinguishes certified mean from unresolved maximum; provides passing/failing states.')}
rows=[]
for r in inputs['readers']:
 cid=r['case_id'];res=r['response'];un=k['cases'][cid]['verdict']=='UNRESOLVED';numeric,prem,unc=notes[cid]
 details={
 'acceptance_verdict':{'score':'full','evidence':res['rationale']},
 'action':{'score':'full','evidence':res['action'],'reason':'Correct UNRESOLVED classification with no release authorization.' if un else 'Correct RELEASE/HOLD action for the established acceptance result.'},
 'numerical_consequence':{'score':'full','evidence':'response.bound_or_value and rationale','reason':numeric},
 'supplied_premise_fidelity':{'score':'full','evidence':'response.satisfied_premises and rationale','reason':prem},
 'uncertainty_and_conflict_fidelity':{'score':'full','evidence':'response.missing_or_conflicting_premises and rationale','reason':unc},
 'next_check_relevance':{'score':'full','evidence':res['next_check']},
 'next_check_sufficiency_claim':{'score':'full' if un else 'not_applicable','evidence':res['next_check']}}
 if cid=='case08':details['next_check_sufficiency_claim']['reason']='Requests the complete-population maximum/threshold determination directly; this would settle the task. Broad acquisition specification is not an unsupported single-piece sufficiency claim. No mandatory measurement count or ranking is asserted.'
 elif un:details['next_check_sufficiency_claim']['reason']='An authoritative assignment for both pieces (or either piece via one-to-one constraint), or an applicable current jade calibration, settles this case. Asking to cover both assignments is sufficient; no delivered efficiency requirement is assumed.'
 else:details['next_check_sufficiency_claim']['reason']='No further check needed or proposed.'
 rows.append({'reader':r['reader'],'case_id':cid,'response_sha256':sha(json.dumps(res,sort_keys=True,separators=(',',':')).encode()),'dimensions':details,'tags':{'false_missingness':False,'false_missingness_evidence':None,'contradiction_handling':'correctly_preserved' if cid=='case06' else 'not_applicable','compliant_witness':'valid' if un else 'not_applicable','violating_witness':'valid' if un else 'not_applicable'},'material_errors':[]})
counts={d:{s:sum(r['dimensions'][d]['score']==s for r in rows) for s in ['full','partial','incorrect','omitted','not_applicable']} for d in dims}
bycase={cid:{d:{s:sum(r['case_id']==cid and r['dimensions'][d]['score']==s for r in rows) for s in ['full','partial','incorrect','omitted','not_applicable']} for d in dims} for cid in k['cases']}
out={'version':'JW-C1-masked-independent-scores-v1','status':'INITIAL_INDEPENDENT_DEPOSIT_BEFORE_RECONCILIATION','source_hashes':hashes,'judgment_method':'Manual semantic inspection of every neutral response against frozen KEY v3 and prospective SCORING; script serializes these judgments.','dimensions':dims,'scores':rows,'counts_by_dimension':counts,'counts_by_case_and_dimension':bycase,'aggregate_score':None,'substantive_findings':['No material error found in any assessed dimension.','No false missingness, unsupported wrong-key transfer, invented conflict, or unsupported resolution of supplied contradiction observed.','All unresolved responses supply compatible passing/failing witnesses.','Next-check proposals differ in specificity; requesting both assignments or the maximum itself is sufficient and not penalized for extra acquisition or broadness without an efficiency or operational-detail requirement.','No response claims that an ordinary <=8 single-piece measurement certifies case08.']}
(p/'SCORES_MASKED.json').write_text(json.dumps(out,indent=2)+'\n')
report='''# Independent masked scoring deposit

All sixteen neutral responses give the keyed acceptance status, action and numerical consequence. No material premise-fidelity or uncertainty/conflict error was found. No aggregate score or arm comparison was computed.

| Dimension | Full | Partial | Incorrect | Omitted | Not applicable |
|---|---:|---:|---:|---:|---:|
'''
for d in dims:report+='| '+d+' | '+' | '.join(str(counts[d][s]) for s in ['full','partial','incorrect','omitted','not_applicable'])+' |\n'
report+='''
Both responses to each case preserve its consequential distinction: supplied versus absent assignment, applicable versus wrong-date calibration, agreed versus conflicting assignments, and mean versus maximum criterion. Both conflict responses preserve the competing assignment records. All eight unresolved responses provide compatible accepting and failing witnesses. No explicit false-missingness assertion was observed.

The two maximum-task next checks ask to determine the complete-population maximum or whether it is at most8. These checks directly resolve the task; they are broad and do not specify an acquisition protocol. Under the prospective rubric this merits full relevance/sufficiency credit, because the rubric does not impose an operational-detail requirement. They do not claim a single passing load certifies compliance. Assignment followups sometimes request both pieces instead of exploiting the one-to-one constraint; those are sufficient, with no unsupported necessity or efficiency claim.

The eight settled responses correctly say no further check is needed; next-check sufficiency is not applicable for those eight. Witness tags are not applicable for settled cases rather than requiring hypothetical alternatives to settled evidence. R07/R09 describe S passing/failing at jade biases5/0 without fixing copper; this is a valid witness construction because R satisfies the limit throughout its supplied interval.

This is the initial independent deposit, before reading any reviewer's scores or reconciliation. Read scope: SCORER_INPUT.json, KEY.json v3, SCORING.md and the neutral cases used during prospective key preparation; earlier allowed motivation was the verification module and prior quality-preview NEXT_CONTACT only. No instruction arms, participant prompts, assignment manifests, delivery files, arm counts or comparison files were read. Shared-filesystem masking is instructional, not technical. No postoutcome key/rubric mutation occurred.

Input, key and rubric hashes are recorded in SCORES_MASKED.json and SCORER_RECEIPT_MASKED.json. Per-response reasons and quotations are in SCORES_MASKED.json; case-by-dimension counts remain separate.
'''
(p/'SCORING_REPORT_MASKED.md').write_text(report)
receipt={'version':'JW-C1-scorer-receipt-v1','deposited_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'INITIAL_INDEPENDENT_DEPOSIT_BEFORE_RECONCILIATION','input_key_rubric_hashes':hashes,'output_hashes':{n:sha((p/n).read_bytes()) for n in ['SCORES_MASKED.json','SCORING_REPORT_MASKED.md']},'key_version':k['version'],'masking':'Shared filesystem; instructional only. No arm or assignment information read.','scoring_read_scope':['SCORER_INPUT.json','KEY.json','SCORING.md'],'preparatory_read_scope':['cases.json','verification module','prior quality-preview NEXT_CONTACT motivation only'],'not_read':['instruction arms','assignment mapping','delivery manifest','participant prompts','arm-specific counts','root comparisons','reviewer independent scores'],'postoutcome_key_or_rubric_mutation':False,'aggregate_score_computed':False}
(p/'SCORER_RECEIPT_MASKED.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'response_count':len(rows),'counts':counts,'hashes':hashes},indent=2))
