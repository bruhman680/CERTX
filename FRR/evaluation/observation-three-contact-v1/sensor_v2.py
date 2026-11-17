"""Prospective observer repair, NOT wired into the frozen model experiment.

Bound the final sensor encoding, not an intermediate full-hex representation.
No world mutation, process execution, or policy feedback.
"""
import base64,hashlib,json
from pathlib import Path

class CapacityError(RuntimeError):pass

def encode_runs(data):
    out=[]
    for value in data:
        if out and out[-1][0]==value:out[-1][1]+=1
        else:out.append([value,1])
    return out

def packet(bundle,objects,directory,clock,style,max_bytes=8192):
    if style not in ('rle','directory'):raise ValueError('unknown sensor')
    out={'world_observation':directory,'clock':clock}
    if style=='rle':
        rows={r[0]:r for r in bundle['entries']};row=rows.get('field.bin')
        if row is None:material={'kind':'absent'}
        else:
            if row[1]=='hardlink':row=rows[row[2]]
            if row[1]!='file':material={'kind':row[1]}
            else:
                obj=json.loads((Path(objects)/(row[3]+'.json')).read_text());data=base64.b64decode(obj['base64'],validate=True)
                if hashlib.sha256(data).hexdigest()!=row[3] or len(data)!=row[4] or obj['bytes']!=len(data) or obj['sha256']!=row[3]:raise ValueError('material snapshot integrity')
                material={'kind':'regular','bytes':len(data),'runs':encode_runs(data)}
        out['material']=material
    wire=json.dumps(out,sort_keys=True,ensure_ascii=True,separators=(',',':'))
    if len(wire.encode())>max_bytes:raise CapacityError('final sensor packet capacity; no partial packet')
    return out
