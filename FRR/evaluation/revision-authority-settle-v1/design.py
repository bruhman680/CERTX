import copy,json
MAP={'positive':'YES','zero':'NO','missing':'WITHHOLD'}
HEADER='Map the status to its answer. missing=WITHHOLD; positive=YES; zero=NO. Return only the answer.'
def fixture(target):
 def e(i,rev=1,parents=(),op='replace',payload=None,source='owner',plot=None):return {'id':i,'source':source,'plot':plot or target,'rev':rev,'parents':list(parents),'op':op,'payload':{'status':'positive'} if payload is None else payload}
 b=e('b');z=e('z',2,['b'],payload={'status':'zero'});d=e('d',2,['b'],'delete',{})
 a=e('a',2,['b'],payload={'status':'zero'});c=e('c',2,['b'],payload={'status':'missing'})
 wrong=copy.deepcopy(b);wrong['payload']={'status':'zero'}
 missing_source=copy.deepcopy(z);del missing_source['source']
 badop=copy.deepcopy(z);badop['op']='guess'
 return [
 ('base',[b],'KNOWN','positive'),('replace',[b,z],'KNOWN','zero'),
 ('patch_omitted',[b,e('p',2,['b'],'patch',{})],'KNOWN','positive'),
 ('replace_omitted',[b,e('r',2,['b'],'replace',{})],'PARTIAL',None),
 ('recorded_missing',[b,e('m',2,['b'],'patch',{'status':'missing'})],'KNOWN','missing'),
 ('remove_field',[b,e('p',2,['b'],'patch',{'status':None})],'PARTIAL',None),
 ('delete_record',[b,d],'DELETED',None),
 ('replace_after_delete',[b,d,e('r',3,['d'],payload={'status':'zero'})],'KNOWN','zero'),
 ('patch_after_delete',[b,d,e('p',3,['d'],'patch',{'status':'zero'})],'LINEAGE_ERROR',None),
 ('fork_different',[b,a,c],'CONCURRENT_CONFLICT',None),
 ('fork_same',[b,a,e('c',2,['b'],payload={'status':'zero'})],'KNOWN','zero'),
 ('fork_high_revision',[b,a,e('c',99,['b'],payload={'status':'missing'})],'CONCURRENT_CONFLICT',None),
 ('explicit_merge',[b,a,c,e('m',3,['a','c'],payload={'status':'missing'})],'KNOWN','missing'),
 ('merge_patch',[b,a,c,e('m',3,['a','c'],'patch',{'status':'missing'})],'LINEAGE_ERROR',None),
 ('untrusted_high_revision',[b,e('g',999,payload={'status':'zero'},source='guest')],'KNOWN','positive'),
 ('only_untrusted',[e('g',999,source='guest')],'NO_AUTHORIZED_EVIDENCE',None),
 ('missing_parent',[e('p',2,['lost'],'patch',{})],'LINEAGE_ERROR',None),
 ('missing_provenance',[b,missing_source],'PROVENANCE_MISSING',None),
 ('duplicate_identical',[b,copy.deepcopy(b)],'KNOWN','positive'),
 ('duplicate_conflict',[b,wrong],'ID_CONFLICT',None),
 ('invalid_revision',[b,e('p',1,['b'],'patch',{})],'LINEAGE_ERROR',None),
 ('cycle',[e('a',2,['c']),e('c',3,['a'])],'LINEAGE_ERROR',None),
 ('unknown_operation',[b,badop],'FORMAT_ERROR',None),
 ('foreign_parent',[e('b',plot='Other'),e('p',2,['b'],'patch',{})],'LINEAGE_ERROR',None),
 ('empty',[],'SOURCE_ABSENT',None)]
def cases():
 out=[]
 for target in ('Cress','Verbena','Sorrel'):
  for kind,events,verdict,state in fixture(target):
   for reverse in [False,True]:out.append({'id':f'c_{len(out):03d}','target':target,'kind':kind,'events':copy.deepcopy(events[::-1] if reverse else events),'reverse':reverse,'expected_verdict':verdict,'expected_state':state})
 assert len(out)==150
 return out

def raw_prompt(c):
 return ('Resolve the status for the target plot from this ledger. Use only owner sources. Parent links define succession; display order and a higher revision alone do not resolve branches. A patch preserves omitted fields; a replacement does not. A deleted status field, a deleted record, a conflict, or insufficient lineage is not the recorded value missing. Return YES for positive, NO for zero, WITHHOLD for recorded missing, otherwise UNKNOWN. Return only the answer.\n\nTarget plot: '+c['target']+'\nLedger:\n'+json.dumps(c['events'],separators=(',',':')))
def worker_prompt(target,state):return HEADER+f'\n\nPlot: {target}\nStatus: {state}'
