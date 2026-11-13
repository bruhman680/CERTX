from pathlib import Path
import hashlib,json,shutil
H=Path(__file__).resolve().parent
p=json.loads((H/'PROVENANCE.json').read_text())
backup=H/'replication/executed_sources_attempt1'
backup.mkdir()
for row in p['sources']:
    source=H/'sources'/row['file'];b=source.read_bytes()
    shutil.copyfile(source,backup/source.name)
    matches=[]
    for count in range(4):
        candidate=b if count==0 else b[:-count]
        digest=hashlib.sha1(b'blob '+str(len(candidate)).encode()+bytes([0])+candidate).hexdigest()
        if digest==row['expected_git_blob_sha']:matches.append((count,candidate))
    assert len(matches)==1,source
    count,candidate=matches[0]
    assert not b[len(candidate):].strip(),source
    source.write_bytes(candidate)
for name in ['RESULT.json','RUN.stdout','RUN.stderr']:
    path=H/'replication'/name
    if path.exists():path.rename(path.with_name('ATTEMPT1_'+name))
print('Recovered exact Git blob bytes; attempt1 sources and output preserved')
