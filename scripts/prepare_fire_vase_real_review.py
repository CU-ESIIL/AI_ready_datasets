"""M6 metadata-only evidence inventory and unapproved review packet. No row reader."""
import argparse,csv,json,hashlib,sqlite3
from datetime import datetime,timezone
from pathlib import Path
import pyarrow.parquet as pq
from dataset_prototype.contracts import digest
from dataset_prototype.embedding_study.real_study_contracts import (
 RealSourceIdentity,RecipeProposal,BoundedReadProposal,RealStudyPacket,RealStudyReview,ScientificReviewItem,DOMAINS)
from dataset_prototype.embedding_study.real_study_validation import assess_preconditions


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def write(path,value):path.write_text(json.dumps(value,indent=2,sort_keys=True,allow_nan=False)+'\n')


def prepare(upstream,output):
    upstream=Path(upstream).resolve();lake=upstream/'data_lake/fire-vase-data-lake-v0.1';output=Path(output)
    output.mkdir(parents=True,exist_ok=False)
    manifest=json.loads((lake/'manifest.json').read_text())
    with (lake/'file_manifest.csv').open() as f:inventory=list(csv.DictReader(f))
    identities=[];inspections=[]
    wanted={
      'fired_conus-ak_daily_nov2001-march2021.gpkg':('fired_daily','Native FIRED dated area field dy_ar_km2; scientific one-day support pending review'),
      'fired_conus-ak_events_nov2001-march2021.gpkg':('fired_events','Catalog event boundaries and total area; not a daily increment'),
      'vase_slices.parquet':('cached_slices','Upstream copy ring_area_km2=dy_ar_km2; reconstructed cumulative sum distinct from catalog total'),
      'fire_traits.parquet':('cached_traits','Event attributes for source reconciliation and evaluation-only strata; not predictors')}
    for filename,(identifier,meaning) in wanted.items():
        candidates=[r for r in inventory if Path(r['path']).name==filename]
        if len(candidates)!=1:raise ValueError('ambiguous source inventory: '+filename)
        row=candidates[0];path=lake/row['path']
        if not path.resolve().is_relative_to(lake.resolve()):raise ValueError('source path escapes packaged lake')
        if not path.is_file():raise FileNotFoundError('declared packaged source absent: '+filename)
        metadata={'source_id':identifier,'path':str(path),'current_size_bytes':path.stat().st_size,
          'inventory_size_bytes':int(row['size_bytes']),'size_matches_inventory':path.stat().st_size==int(row['size_bytes']),
          'reported_sha256':row['sha256'],'current_full_content_checksum':'NOT_REVERIFIED','observation_rows_read':0}
        if path.suffix=='.parquet':
            file=pq.ParquetFile(path);fields=tuple(file.schema_arrow.names)
            metadata.update(scope='Parquet footer only',rows_from_footer=file.metadata.num_rows,row_groups=file.metadata.num_row_groups,
              schema=str(file.schema_arrow),quality_caveat='Climate flags do not establish native burned-area QA or measurement uncertainty')
        else:
            with sqlite3.connect(path.as_uri()+'?mode=ro&immutable=1',uri=True) as db:
                tables=db.execute('SELECT table_name,srs_id FROM gpkg_contents').fetchall();table_metadata=[];allfields=[]
                for name,srs in tables:
                    columns=[{'name':r[1],'type':r[2]} for r in db.execute('PRAGMA table_info("'+name.replace('"','""')+'")')]
                    allfields.extend(c['name'] for c in columns);table_metadata.append({'table':name,'native_srs_id':srs,'columns':columns})
                spatial=db.execute('SELECT srs_id,organization,organization_coordsys_id,definition FROM gpkg_spatial_ref_sys').fetchall()
            fields=tuple(dict.fromkeys(allfields));metadata.update(scope='GeoPackage catalog/schema/CRS metadata only',tables=table_metadata,
               spatial_reference_metadata=[{'srs_id':s,'organization':o,'native_code':c,'definition':d} for s,o,c,d in spatial])
        inspections.append(metadata)
        identities.append(RealSourceIdentity(source_id=identifier,package_release=manifest['release_id'],package_relative_path=row['path'],
          local_path=str(path),file_format=path.suffix[1:],expected_size_bytes=int(row['size_bytes']),reported_sha256=row['sha256'],
          checksum_evidence='data_lake/fire-vase-data-lake-v0.1/file_manifest.csv; historical full-container SHA, not current content verification',
          measurement_semantics=meaning,native_fields=fields,rights_evidence=('package README retains upstream FIRED/gridMET terms; dataset-specific permission evidence pending',)))
    recipes=[
      RecipeProposal(operation='native_increment_identity',source_fields=('dy_ar_km2','ring_area_km2'),intended_meaning='Preserve original native daily-bin area and compare copied cached values by exact source ID/date; no cumulative differencing or unit inference from label alone',
        preconditions=('human semantic/units/support review','exact source/version identity','one-to-one source/cache ID-date match','no negative/nonfinite/missing area imputation'),
        preserved_evidence=('native source field/value/unit','source ID/date and row identity','native support/quality','recipe and source digest'),
        implementation_evidence=('scripts/fire_vase_build_climate_tables.py:normalize_daily','scripts/fire_vase_v2_inputs.py:audit_inputs')),
      RecipeProposal(operation='calendar_support_validation',source_fields=('id','fire_id','date','timestamp','event_day'),intended_meaning='Validate exact one-calendar-day support and event separation; reject duplicate/ambiguous/missing windows',
        preconditions=('calendar and time-zone semantics reviewed','no sorting/merging that hides source duplicates','gap is not observed zero'),preserved_evidence=('original dates/order','gap/missing/zero categories','event grouping'),implementation_evidence=('src/cubedynamics/analysis_v2.py:exact_transitions',)),
      RecipeProposal(operation='observed_prefix_only',source_fields=('dy_ar_km2','date','availability'),intended_meaning='Build only observed prefix inputs after approval; observed-window sum is not automatically catalog final area or complete-fire cumulative area',
        preconditions=('origin/support defined','prospective availability evidenced or explicit retrospective-only study decision','no completed-fire endpoints or future climate'),preserved_evidence=('cutoff and unknown availability','original units','uncertainty and quality','source lineage'),implementation_evidence=('embedding_study.learned_contracts:PrefixInput requires known availability; no synthetic timestamps for real data',)),
      RecipeProposal(operation='independent_future_targets',source_fields=('native_daily_increment','native_date'),intended_meaning='A next day, B next-three total, C relative future/past mean, D next-three population SD and E future-pattern relevance only with full independent future support',
        preconditions=('reviewed exact-day area semantics','future observations excluded from inputs','no manufactured future rows'),preserved_evidence=('target observation identities/dates','missing future exclusion','target recipe'),implementation_evidence=('embedding_study.transfer_targets:future_targets; currently synthetic-only',)),
      RecipeProposal(operation='fire_grouped_holdouts',source_fields=('native_event_id','year','region','observation_support'),intended_meaning='Freeze whole-fire temporal/geographic folds and calibration cohorts without fitting on held-out data',
        preconditions=('reviewed region definitions and event boundaries','train-only preprocessing','selection thresholds fixed without test performance','post-outcome size/stage descriptors evaluation-only'),preserved_evidence=('fire/fold membership','region/year support','cohort exclusions/denominators'),implementation_evidence=('M5 grouped split protocol; real fold identities pending approval',))]
    packet=RealStudyPacket(purpose='Review a bounded native-value/source-cache alignment audit before any real observation read, adapter or training',
      proposed_claim='retrospective_reconstructed',sources=identities,recipes=recipes,sample=BoundedReadProposal(),
      scientific_requirements=('No source rows until independent human review and actual data identity evidence are complete','No new geometry/calibration/resampling','Prospective cohort requires actual availability; cannot use real data in synthetic-only runners','No public observations/embeddings/checkpoints before derivative-rights review'),
      exclusions=('gridMET/climate covariates','completed morphospace/features','final normalized VASE width','source peak-as-total/duration legacy metric','source downloads or copies','model training and public release'),
      unresolved=('dataset-specific rights/attribution and derivative/publication conditions','original daily-bin/time-zone/unit definitions','native QA/uncertainty evidence','source/cache equivalence for these exact bytes','operational availability and event-prefix origin','current full-container byte verification before any decoding'))
    rationales={
      'semantic':'Copy operation is documented upstream; source measurement equivalence still requires expert review',
      'units':'km2 labels/code present; daily area versus physical rate and date-bin meaning require source evidence',
      'support':'Exact-day upstream checks known; actual interval/geometry/event boundary support not approved',
      'rights':'Source terms not established by code or article license; authoritative dataset page returned 403',
      'integrity':'Historical package hashes and stat sizes recorded; current full-byte identity not verified',
      'quality':'Source uncertainty/QA survival unresolved; climate flags are not burn-area QA',
      'availability':'Retrospective reconstruction documented; real availability not established; prospective claim remains unsupported'}
    review=RealStudyReview(packet_digest=packet.packet_digest,findings=tuple(ScientificReviewItem(domain=d,status='NEEDS_EVIDENCE',
      evidence_ids=('metadata-evidence-v1:'+d,),rationale=rationales[d]) for d in DOMAINS))
    docs=['config/data_release.yml','docs/datasets/fired.md','docs/reanalysis-v2.md',
      'docs/manuscripts/fire_vase_developmental_morphology/manuscript_v2.md','scripts/fire_vase_build_climate_tables.py',
      'scripts/fire_vase_v2_inputs.py','src/cubedynamics/analysis_v2.py','src/cubedynamics/fire_time_hull.py',
      'analysis/v2/input_hashes.json','analysis/v2/input_audit.json','analysis/scientific_validation/population_audit.json',
      'analysis/scientific_validation/final_report.md','analysis/submission_freeze/release_readiness.md']
    evidence={'version':'fire-m6-metadata-v1','timestamp':datetime.now(timezone.utc).isoformat(),
      'lake_root':str(lake),'package_manifest':manifest,'lake_metadata_sha256':{n:sha(lake/n) for n in ('manifest.json','README.md','file_manifest.csv','checksums.sha256')},
      'upstream_document_sha256':{n:sha(upstream/n) for n in docs},'inspections':inspections,
      'upstream_reported_population':json.loads((upstream/'analysis/scientific_validation/population_audit.json').read_text()),
      'population_scope':'Historical upstream aggregate, not this milestone real cohort or operational evidence',
      'new_cohort_counts':None,'source_observation_rows_read':0,'real_models_trained':0,'copies_or_downloads':0,
      'local_lake_discovery':'User clarified canonical packaged lake location; prior audits only established expected-root absence/legacy presence. Current packaged files verified present by stat, not full checksum.'}
    write(output/'metadata-evidence.json',evidence);write(output/'packet.json',packet.model_dump(mode='json'))
    write(output/'review-template.json',review.model_dump(mode='json'));write(output/'preconditions.json',assess_preconditions(packet,review))
    write(output/'manifest.json',{'version':'fire-m6-review-manifest-v1','status':'PENDING_HUMAN_REVIEW',
      'packet_digest':packet.packet_digest,'source_observation_rows_read':0,'models_trained':0,
      'output_sha256':{p.name:sha(p) for p in output.iterdir() if p.is_file()},
      'code_sha256':{str(p.resolve().relative_to(Path.cwd())):sha(p) for p in [Path(__file__).resolve(),*Path('src/dataset_prototype/embedding_study').glob('real_study_*.py')]}})
    print(json.dumps({'status':'PENDING_HUMAN_REVIEW','packet_digest':packet.packet_digest,'observation_rows_read':0,'sources':len(identities)}))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--upstream',default='../fire_vase');p.add_argument('--output',required=True);a=p.parse_args();prepare(a.upstream,a.output)
