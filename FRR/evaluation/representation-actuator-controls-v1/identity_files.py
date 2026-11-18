"""Read-only pinned Hugging Face metadata comparison; no weight download."""
from pathlib import Path
import json,urllib.request,hashlib
H=Path(__file__).resolve().parent

def main():
    previous=json.loads((H/'MODEL_IDENTITY_AUDIT.json').read_text());model=Path('/workspace/cache_backend_models/smollm2-135m');url=previous['primary_source'];result={'source':url,'model_calls':0,'downloaded_weights':False,'files':[]}
    try:
        with urllib.request.urlopen(url,timeout=20) as response:tree=json.load(response)
        lookup={x['path']:x for x in tree}
        for name in ['config.json','tokenizer.json','tokenizer_config.json','generation_config.json','special_tokens_map.json','merges.txt','vocab.json']:
            data=(model/name).read_bytes();row=lookup[name]
            actual=hashlib.sha256(data).hexdigest() if row.get('lfs') else hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
            expected=row['lfs']['oid'] if row.get('lfs') else row['oid']
            result['files'].append({'name':name,'algorithm':'sha256' if row.get('lfs') else 'git_blob_sha1','actual':actual,'official':expected,'match':actual==expected,'bytes':len(data)})
        result['status']='verified' if all(x['match'] for x in result['files']) else 'mismatch'
    except Exception as error:result.update(status='incomplete',error_type=type(error).__name__,error=str(error))
    (H/'TOKENIZER_CONFIG_IDENTITY.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
