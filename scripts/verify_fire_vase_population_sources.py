"""Verify only relevant census sources under the existing direct instruction record."""
import argparse,hashlib,json,time
from pathlib import Path
from dataset_prototype.embedding_study.population_profile import DAILY,EVENTS,SLICES,TRAITS


def main():
    p=argparse.ArgumentParser();p.add_argument('--lake',required=True);p.add_argument('--output',required=True);a=p.parse_args()
    root=Path(a.lake).resolve();out=Path(a.output)
    authorization=json.loads((out/'direct-execution-authorization.json').read_text())
    if authorization.get('origin')!='DIRECT_USER_INSTRUCTION':raise PermissionError('existing direct instruction required; verifier never creates approval')
    catalog=json.loads(Path('reports/embedding_utility/fire_vase/milestone-7/metadata-v1/catalog.json').read_text());expected={r['relative_path']:r['reported_sha256'] for r in catalog}
    record=out/'source-verification.json';prior=json.loads(record.read_text()) if record.exists() else []
    context=out/'source-verification-context.json';known=json.loads(context.read_text()) if context.exists() else {}
    verified=[]
    for rel in (DAILY,EVENTS,SLICES,TRAITS):
        path=(root/rel).resolve()
        if not path.is_relative_to(root):raise ValueError('source outside canonical root')
        st=path.stat();old=next((r for r in prior if r['relative_path']==rel),None)
        if known.get('canonical_lake')==str(root) and old and old['sha256']==expected[rel] and (old['bytes'],old['mtime_ns'])==(st.st_size,st.st_mtime_ns):
            verified.append(old);print('REUSED verified identity '+rel,flush=True);continue
        h=hashlib.sha256();start=time.perf_counter()
        with path.open('rb') as f:
            for block in iter(lambda:f.read(1048576),b''):h.update(block)
        after=path.stat()
        if (st.st_size,st.st_mtime_ns)!=(after.st_size,after.st_mtime_ns):raise ValueError('source changed during hashing')
        if h.hexdigest()!=expected[rel]:raise ValueError('unexpected source identity: '+rel)
        verified.append({'relative_path':rel,'sha256':h.hexdigest(),'historical_sha256':expected[rel],'historical_match':True,'bytes':st.st_size,'mtime_ns':st.st_mtime_ns,'seconds':time.perf_counter()-start})
        print('VERIFIED '+rel,flush=True)
    if record.exists() and {r['relative_path']:r for r in verified}!={r['relative_path']:r for r in prior}:raise FileExistsError('preserve prior verification; use fresh output for newly verified identities')
    if not record.exists():record.write_text(json.dumps(verified,indent=2)+'\n')
    context.write_text(json.dumps({'canonical_lake':str(root),'source_hash_scope':'complete relevant source container bytes, no unrelated data'},indent=2)+'\n')
if __name__=='__main__':main()
