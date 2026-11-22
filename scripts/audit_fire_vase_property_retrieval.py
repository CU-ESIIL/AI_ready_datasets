"""Exact observed-area retrieval baseline over the full real observed population, no learned model."""
import argparse,hashlib,heapq,json,sqlite3,time
from pathlib import Path
import numpy as np
from dataset_prototype.embedding_study.lake_methods import exact_neighbors


def main():
    p=argparse.ArgumentParser();p.add_argument('--census',required=True);p.add_argument('--output',required=True);a=p.parse_args();c=Path(a.census);out=Path(a.output)
    start=time.perf_counter()
    with sqlite3.connect(c/'cohort-metadata.sqlite') as db:
        rows=db.execute("SELECT f.id,f.observations,f.observed_sum,s.random_fold FROM fire f JOIN proposed_splits s USING(id) WHERE f.source='native' ORDER BY f.id").fetchall()
    gallery=[r for r in rows if r[3]=='train'];gallery_ids=np.asarray([r[0] for r in gallery]);features=np.log1p(np.array([r[2] for r in gallery],dtype=float))[:,None]
    queries=[]
    for n in (1,2,3):
        candidates=[r for r in rows if (r[1]==n if n<3 else r[1]>=3) and r[3]=='test'];candidates.sort(key=lambda r:hashlib.sha256(('property-query-v1:'+r[0]).encode()).hexdigest());queries.extend(candidates[:16])
    assert not set(r[0] for r in queries)&set(gallery_ids)
    construction=time.perf_counter()-start;durations=[];receipts=[]
    scalar=features[:,0].tolist()
    for event,n,total,fold in queries:
        q=np.log1p(total);started=time.perf_counter_ns();neighbors=exact_neighbors(np.array([q]),features,gallery_ids,event,10);durations.append(time.perf_counter_ns()-started)
        # Independent heap-based scalar ranking; tie order follows sorted gallery IDs.
        oracle=heapq.nsmallest(10,range(len(scalar)),key=lambda j:(abs(scalar[j]-float(q)),j))
        assert neighbors==oracle
        receipts.append({'query_event':event,'observations':n,'matched_gallery_ids':[str(gallery_ids[j]) for j in neighbors],'oracle_agreement':True})
    result={'status':'REAL_OBSERVED_PROPERTY_RETRIEVAL_BASELINE_VALIDATED','scientific_relevance':'nearest total of retained observed native increments in log1p source-reported km2; not ecological analogs or future outcomes','gallery_fires':len(gallery),'query_fires':len(queries),'k':10,'same_fire_exclusion':True,'query_gallery_fire_disjoint':True,'query_selection':'first16 per1/2/3+-observation stratum by independent deterministic hash among candidate test folds; diagnostic sample not confirmatory generalization','source':'source-verified census observed_sum metadata, not a new raw-data copy','information':'optimized cached native aggregate and interpretable total provide the same scalar input; full lineage/source lookup remains available','independent_oracle_agreement_queries':sum(r['oracle_agreement'] for r in receipts),'precision_scope':'exact declared-property retrieval implementation, not independent ecological or learned-model accuracy','distinct_gallery_scalar_values':len(set(scalar)),'index_preparation_seconds_this_invocation':construction,'query_median_ns':float(np.median(durations)),'cost_limit':'warm in-memory queries and cached aggregates; original census/refresh/storage costs not included, no end-to-end cost frontier','learned_model_evaluation':False,'normalized_payload_only_scale_query':'requires explicit source or cached-native aggregate access; not assigned invented ranking scores','query_receipts':receipts,'seconds':time.perf_counter()-start}
    (out/'property-retrieval-baseline.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k] for k in ('gallery_fires','query_fires','independent_oracle_agreement_queries','query_median_ns','seconds')},indent=2))
if __name__=='__main__':main()
