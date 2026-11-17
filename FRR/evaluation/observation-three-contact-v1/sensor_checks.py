"""Prospective sensor-only checks; no model input/contract/world changes."""
import json,base64,hashlib,tempfile
from pathlib import Path
import sensor_v2 as v

def main():
    with tempfile.TemporaryDirectory() as tmp:
        root=Path(tmp);clock={'replies':0,'ticks':0,'actor_operations':0};directory={'path':'/world','entries':[]}
        def fixture(data):
            sha=hashlib.sha256(data).hexdigest();(root/(sha+'.json')).write_text(json.dumps({'sha256':sha,'bytes':len(data),'base64':base64.b64encode(data).decode()}))
            return {'entries':[['field.bin','file',0o644,sha,len(data)]]}
        initial=b'\x01'+bytes(61);b=fixture(initial)
        p=v.packet(b,root,directory,clock,'rle');assert p['material']['runs']==[[1,1],[0,61]]
        b=fixture(bytes(65536));assert v.packet(b,root,directory,clock,'rle')['material']['runs']==[[0,65536]]
        missing={'entries':[['field.bin','file',0o644,'not-an-object',65536]]}
        assert 'material' not in v.packet(missing,root,directory,clock,'directory')
        b=fixture(bytes([0,1])*32768)
        try:v.packet(b,root,directory,clock,'rle')
        except v.CapacityError:pass
        else:raise AssertionError('large final encoding admitted')
        b=fixture(b'abc');b['entries'][0][0]='alias';b['entries'].append(['field.bin','hardlink','alias'])
        assert v.packet(b,root,directory,clock,'rle')['material']['runs']==[[97,1],[98,1],[99,1]]
        for kind,row in [('absent',None),('symlink',['field.bin','symlink','elsewhere']),('dir',['field.bin','dir',0o755])]:
            assert v.packet({'entries':[] if row is None else [row]},root,directory,clock,'rle')['material']['kind']==kind
        b=fixture(b'x');obj=root/(b['entries'][0][3]+'.json');o=json.loads(obj.read_text());o['base64']=base64.b64encode(b'y').decode();obj.write_text(json.dumps(o))
        try:v.packet(b,root,directory,clock,'rle')
        except ValueError:pass
        else:raise AssertionError('bad hash admitted')
    result={'status':'pass','checks':['62-byte lossless representation','64KiB compressible material fits final bound','directory sensor never reads byte object','large final encoding refused','hardlink resolution','absent/symlink/directory semantics','corrupt material object refused'],'model_calls':0,'activated':False,'scope':'prospective sensor helper, not the frozen runner'}
    Path(__file__).with_name('SENSOR_V2_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
