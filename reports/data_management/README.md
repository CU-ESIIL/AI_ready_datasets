# Data management design report

A 23 October 2026 source-audited report for drafting a data management plan.
The PDF distinguishes CURRENT IMPLEMENTATION, DESIGN REQUIREMENTS and PROPOSED
DMP COMMITMENTS. It is funder-neutral and does not invent institutional services,
retention periods, archive commitments or model-processing terms.

- Final PDF: `../../output/pdf/AI_ready_data_management_report.pdf`
- `report.md` / `report.json`: editable narrative (generated from the builder).
- `data_inventory.csv` / `data_inventory.json`: 12 storage/lifecycle classes.
- `run_manifest.json`: audit commit, input/source hashes, output identity and limits.
- `build_report.py`: ReportLab authoring source; no source acquisition/inference.
- `verify.py`: checks PDF, source/input hashes and inventory consistency.

From the repository root, using Python with ReportLab and pypdf:

```sh
python reports/data_management/build_report.py
python reports/data_management/verify.py
pdftoppm -scale-to 1000 -png output/pdf/AI_ready_data_management_report.pdf /tmp/dmp-page
```

Inspect rendered pages after rebuilding. Files under `build/` are ignored render
intermediates. Creation timestamps may change PDF hashes; reproducibility refers
to the documented content and source evidence, not byte-identical PDF metadata.
The report does not read runtime credential contents or infer backup/encryption
from directory names. Historical snapshots and caches are explicitly distinguished
from new bounded streaming paths. The generated 32-by-32 example is illustrative,
not a scientifically approved real source release or a production volume benchmark.

## NSF planning draft

`nsf_plan.md` is the editable prospective plan organized around the five categories
on NSF's general guidance page. `build_nsf_plan.py` creates the two-page
`../../output/pdf/NSF_data_management_and_sharing_plan.pdf`. This is a planning
artifact for entry into Research.gov under NSF 26-202, not a claim that PDF upload
is the current submission mechanism. Bracketed institutional storage, archive,
backup, retention and license commitments require finalization; check the selected
solicitation's additional requirements. This draft does not change the implemented
pipeline or supersede the source-audited design report.
