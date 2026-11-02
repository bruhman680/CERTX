"""Bounded reconstruction candidates; never modifies source capture/study."""
from pathlib import Path
import datetime, hashlib, itertools, json, subprocess

SOURCE=Path('/workspace/frr/evaluation/real-artifact-provenance-v1/CAPTURE.json')
OUT=Path('/workspace/git-commit-binding-offset-candidates-2026-11-01.json')
def digest(data):
    return hashlib.sha1(b'commit '+str(len(data)).encode()+b'\0'+data).hexdigest()
def offset(minutes):
    return ('-' if minutes<0 else '+')+f'{abs(minutes)//60:02}{abs(minutes)%60:02}'
offsets=[offset(m) for m in range(-12*60,14*60+1,15)]+['-0000']
results=[]
for c in json.loads(SOURCE.read_text())['commits']:
    attempts=[];matches=[]
    def identity(key,off):
        a=c[key]
        ts=int(datetime.datetime.fromisoformat(a['date'].replace('Z','+00:00')).timestamp())
        return f"{key} {a['name']} <{a['email']}> {ts} {off}\n"
    prefix='tree '+c['tree']['sha']+'\n'+''.join('parent '+p['sha']+'\n' for p in c['parents'])
    for ao,co in itertools.product(offsets,repeat=2):
        base=prefix+identity('author',ao)+identity('committer',co)+'\n'+c['message']
        for ending in range(3):
            data=(base+'\n'*ending).encode('utf-8');sha=digest(data)
            attempt={'author_offset':ao,'committer_offset':co,'appended_newlines':ending,'candidate_sha':sha}
            attempts.append(attempt)
            if sha==c['sha']:
                path=Path('/workspace/reconstructed-commit-'+sha+'.bin')
                path.write_bytes(data)
                independent=subprocess.run(['git','hash-object','-t','commit','--stdin'],input=data,capture_output=True,check=True).stdout.decode().strip()
                matches.append({**attempt,'path':str(path),'bytes':len(data),'git_hash_object_sha':independent,'git_hash_object_match':independent==sha})
    results.append({'captured_sha':c['sha'],'attempt_count':len(attempts),'matches':matches,'attempts':attempts})
OUT.write_text(json.dumps({'source_capture':str(SOURCE),'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'assumptions':{'encoding':'UTF-8','headers':['tree','parent*','author','committer'],'no_extra_headers':True,'dates':'API instants converted to unix seconds; original numeric offsets unknown','message':'exact API string, followed by zero/one/two LF','offset_search':'-1200 to +1400 at 15min increments, plus -0000, independently for author/committer'},'results':results},indent=2)+'\n')
print(json.dumps([{k:v for k,v in r.items() if k!='attempts'} for r in results],indent=2))
