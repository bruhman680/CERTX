"""No model calls or world execution; prospective view checks only."""
import json,copy
from pathlib import Path
from receipt_view import model_receipt
H=Path(__file__).resolve().parent

def main():
    a=dict(stdout='measured 0.1 seconds\n',stderr='',exit_code=0,boundary=None,seconds=0.1);b=dict(a,seconds=0.9)
    saved=copy.deepcopy(a);assert model_receipt(a)==model_receipt(b) and a==saved
    assert model_receipt(a)['stdout']=='measured 0.1 seconds\n'
    err=dict(a,stdout='',stderr='ValueError: genuine\n',exit_code=1,boundary='wall_time');v=model_receipt(err)
    assert v==dict(stdout='',stderr='ValueError: genuine\n',exit_code=1,boundary='wall_time')
    for bad in [dict(a,unknown=3),dict(a,seconds=float('nan')),dict(a,exit_code=True)]:
        try:model_receipt(bad)
        except ValueError:pass
        else:raise AssertionError('invalid schema/evidence admitted')
    # Verify the exact observed cross-study nuisance maps to equal model views.
    old=json.loads((H.parent/'observation-three-contact-v1/rle17/records/000001.json').read_text())
    new=json.loads((H/'observation17/records/000001.json').read_text())
    aa=json.loads(old['feedback']);bb=json.loads(new['feedback']);assert aa!=bb
    before_a, before_b=copy.deepcopy(aa),copy.deepcopy(bb)
    aa['physical_feedback']=model_receipt(aa['physical_feedback']);bb['physical_feedback']=model_receipt(bb['physical_feedback']);assert aa==bb
    assert 'seconds' in before_a['physical_feedback'] and 'seconds' in before_b['physical_feedback']
    result={'status':'pass','checks':['time-only differences map to same view','raw receipt remains unchanged','stdout timing content preserved literally','real error/exit/boundary preserved','unknown schema refused','nonfinite elapsed evidence refused','boolean exit status refused','actual cross-study timing nuisance removed by proposed metadata view'],'model_calls':0,'activated':False,'scope':'prospective metadata policy; does not make process execution deterministic'}
    (H/'RECEIPT_VIEW_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
