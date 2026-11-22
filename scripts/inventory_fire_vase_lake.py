"""Metadata-only full-lake inventory and full-scope DRAFT authorization amendment."""
import argparse,json,hashlib
from pathlib import Path
from dataset_prototype.contracts import digest
from dataset_prototype.embedding_study.lake_inventory import inventory
from dataset_prototype.embedding_study.lake_contracts import LakePlan,LakeAuthorization,ScopeFinding,SCOPES,JURISDICTIONS
from dataset_prototype.embedding_study.lake_authorization import scope_reasons


def write(path,value):path.write_text(json.dumps(value,indent=2,sort_keys=True,allow_nan=False)+'\n')
def main():
    p=argparse.ArgumentParser();p.add_argument('--lake',default='../fire_vase/data_lake/fire-vase-data-lake-v0.1');p.add_argument('--output',required=True);a=p.parse_args();out=Path(a.output);out.mkdir(parents=True,exist_ok=False)
    catalog,summary=inventory(a.lake);write(out/'catalog.json',catalog);write(out/'inventory-summary.json',summary)
    plan=LakePlan(inventory_digest=digest(catalog),source_release='fire-vase-data-lake-v0.1');write(out/'amendment.json',plan.model_dump(mode='json'))
    review=LakeAuthorization(plan_digest=plan.plan_digest,findings=tuple(ScopeFinding(scope=s,jurisdiction=j,status='NEEDS_EVIDENCE',
      evidence_ids=('M6:pending-review','M7:metadata-only-inventory'),rationale='Requires explicit source/science/rights/execution human review; inventory is not permission') for s in SCOPES for j in JURISDICTIONS))
    write(out/'authorization-template.json',review.model_dump(mode='json'));write(out/'preconditions.json',{s:scope_reasons(plan,review,s) for s in SCOPES})
    write(out/'manifest.json',{'version':'full-lake-preapproval-v1','status':'PENDING_FULL_LAKE_HUMAN_REVIEW','plan_digest':plan.plan_digest,
      'observation_rows_read':0,'data_array_values_read':0,'output_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in out.iterdir() if p.is_file()}})
    print(json.dumps({k:summary[k] for k in ('current_files_stat','current_total_bytes_stat','schema_status','metadata_errors','observation_rows_read')}))

if __name__=='__main__':main()
