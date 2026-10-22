"""Explicit bounded vocabulary metadata acquisition; never follows ontology imports."""
from pathlib import Path
import json,hashlib
from datetime import datetime,timezone
from dataset_prototype.network import request_bytes
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).parent/'data/graphs'
def main():
 OUT.mkdir(exist_ok=True);plan=json.loads((ROOT/'data/semantics/validation/acquisition_plan.json').read_text());records=[]
 for s in plan['sources']:
  r={**s,'retrieved_at':datetime.now(timezone.utc).isoformat()}
  try:
   b=request_bytes(s['url'],max_bytes=s['max_bytes']);(OUT/(s['id']+'.ttl')).write_bytes(b);r.update(status='retrieved',bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
  except Exception as e:r.update(status='unavailable',error=type(e).__name__)
  records.append(r)
 (OUT/'manifest.json').write_text(json.dumps(records,indent=2)+'\n');print([(r['id'],r['status'],r.get('bytes')) for r in records])
if __name__=='__main__':main()
