"""Scoped fail-closed review conditions and bounded byte verification, no self-grants."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib
from .lake_contracts import JURISDICTIONS,SCOPES


def scope_reasons(plan,authorization,scope):
    if scope not in SCOPES:raise ValueError('unregistered execution scope')
    reasons=[]
    if authorization.plan_digest!=plan.plan_digest:reasons.append('plan_digest_mismatch')
    if authorization.origin!='EXTERNAL_HUMAN_REVIEW':reasons.append('external_human_review_missing')
    if not authorization.reviewer or authorization.timestamp is None or authorization.timestamp.utcoffset() is None:reasons.append('attributed_timestamped_review_missing')
    if not authorization.human_receipt_reference or not authorization.receipt_verified_by:reasons.append('verified_external_human_receipt_missing')
    if scope not in authorization.approved_scopes:reasons.append('scope_not_approved')
    relevant={f.jurisdiction:f for f in authorization.findings if f.scope==scope}
    for domain in JURISDICTIONS:
        if domain not in relevant:reasons.append(domain+':NEEDS_EVIDENCE');continue
        allowed={'PASS'}
        if domain=='availability' and plan.claim=='retrospective_reconstructed':allowed.add('NOT_APPLICABLE')
        if domain=='publication' and scope!='publish_outputs':allowed.add('NOT_APPLICABLE')
        # Verification is a permitted precursor to current integrity evidence, not a row read.
        if domain=='integrity' and scope=='verify_container_bytes':allowed.add('NEEDS_EVIDENCE')
        if relevant[domain].status not in allowed:reasons.append(domain+':'+relevant[domain].status)
    if scope in ('train_neural','retrospective_prediction','retrieval') and any(v is None for v in plan.minimum_effect_sizes.values()):reasons.append('scientist_effect_sizes_not_reviewed')
    return reasons


def require_scope(plan,authorization,scope):
    reasons=scope_reasons(plan,authorization,scope)
    if reasons:raise PermissionError('Full-lake '+scope+' blocked: '+','.join(reasons))


def contained(root,relative):
    root=Path(root).resolve();path=(root/relative).resolve()
    if not path.is_relative_to(root):raise ValueError('source escapes canonical lake')
    return path


def verify_container(root,relative,expected,plan,authorization):
    require_scope(plan,authorization,'verify_container_bytes')
    path=contained(root,relative);before=path.stat();hasher=hashlib.sha256();size=0
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):hasher.update(block);size+=len(block)
    after=path.stat()
    if (before.st_size,before.st_mtime_ns)!=(after.st_size,after.st_mtime_ns):raise ValueError('source changed during verification')
    actual=hasher.hexdigest()
    if actual!=expected:raise ValueError('current source checksum mismatch')
    return {'relative_path':relative,'sha256':actual,'bytes':size,'scope':'complete_container_bytes_no_decoding',
      'mtime_ns':after.st_mtime_ns,'verified_at':datetime.now(timezone.utc).isoformat(),'plan_digest':plan.plan_digest}
