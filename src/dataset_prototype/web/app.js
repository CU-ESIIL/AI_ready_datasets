'use strict';
const $ = id => document.getElementById(id);
let kind = 'release', cursor = '', selected = '', requestVersion = 0, detailVersion = 0;
const human = n => n >= 1e9 ? `${(n / 1e9).toFixed(2)} GB` : `${(n / 1e6).toFixed(2)} MB`;
function node(tag, text, cls) { const n = document.createElement(tag); n.textContent = text; if (cls) n.className = cls; return n; }
async function get(url, options) { const response = await fetch(url, options); const data = await response.json(); if (!response.ok) throw Error(data.error || 'Request failed'); return data; }
function state(r) { return r.payload.state || r.payload.model_consensus || r.payload.status || r.payload.capability || (r.fixture ? 'generated diagnostic' : 'metadata record'); }
async function overview() {
  const data = await get('/api/summary'); $('overview').replaceChildren();
  for (const [name, value] of [['Artifact records', data.artifacts], ['Stored output files', human(data.registered_blob_bytes)], ['Metadata index', human(data.database_bytes)], ['Actual dataset bundles', data.counts.dataset || 0]]) {
    const card = node('div', '', 'metric'); card.append(node('span', name), node('strong', String(value))); $('overview').append(card);
  }
}
async function load(more = false) {
  const version = ++requestVersion; $('message').textContent = 'Loading…';
  const params = new URLSearchParams({limit: '30'}); if (kind) params.set('kind', kind); if ($('track').value) params.set('track', $('track').value); if (more && cursor) params.set('after', cursor);
  try {
    const data = await get(`/api/artifacts?${params}`); if (version !== requestVersion) return;
    if (!more) $('items').replaceChildren();
    for (const r of data.items) { const button = node('button', '', 'record'); const shape = r.kind === 'dataset' ? ` · ${r.payload.records} rows × ${r.payload.dimensions} features` : ''; button.append(node('strong', r.title), node('small', `${r.kind} · ${state(r)}${shape} · ${r.track || 'shared'} · ${r.fixture ? 'generated' : 'metadata / see evidence'}`)); button.onclick = () => inspect(r.artifact_id); $('items').append(button); }
    cursor = data.next; $('more').hidden = !cursor; $('message').textContent = data.items.length ? 'Select a versioned record. Filters apply to records, not scientific compatibility.' : 'No records match this view. Planned products do not imply generated scientific data.';
  } catch (e) { $('message').textContent = e.message; }
}
async function inspect(id) {
  const version = ++detailVersion;
  try {
    const data = await get(`/api/artifacts/${id}`), r = data.record; if (version !== detailVersion) return; selected = id; $('target').value = id;
    const panel = $('detail'); panel.replaceChildren(node('h2', r.title), node('p', `${r.kind} · ${state(r)} · ${r.visibility}`, 'pill'), node('p', r.fixture ? 'Generated evidence. No independent scientific approval.' : 'Inspect evidence and limitations; registration is not approval.'), node('code', r.artifact_id));
    for (const name of ['parents', 'children']) { panel.append(node('h3', name === 'parents' ? 'Upstream evidence' : 'Downstream records (up to 100)')); const list = node('div', '', 'links'); for (const item of data.related[name]) { const b = node('button', `${item.kind}: ${item.title}`); b.onclick = () => inspect(item.artifact_id); list.append(b); } if (!list.children.length) list.append(node('p', 'None recorded.')); panel.append(list); }
    panel.append(node('h3', 'Registered files')); if (!r.blobs.length) panel.append(node('p', 'Metadata-only record.'));
    for (const blob of r.blobs) { const a = node('a', `${blob.name} · ${human(blob.bytes)}`, 'file'); a.href = `/api/blobs/${id}/${encodeURIComponent(blob.name)}`; a.download = blob.name; panel.append(a); }
    if (r.kind === 'dataset') { const preview = node('button', 'Preview numerical features and observation lineage'); preview.onclick = async () => { preview.disabled = true; try { const page = await get(`/api/datasets/${id}/rows?limit=3`); const view = page.rows.map(row => ({patch: row.record.patch_id, split: row.record.split, units: row.record.units, dimensions: row.vector.length, first_eight_features: row.vector.slice(0,8), lineage: row.record.lineage})); preview.replaceWith(node('pre', JSON.stringify(view, null, 2))); } catch(e) { preview.textContent = e.message; preview.disabled = false; } }; panel.append(preview); }
    const details = node('details', ''); details.append(node('summary', 'Inspect exact metadata'), node('pre', JSON.stringify(r.payload, null, 2))); panel.append(details);
    history.replaceState(null, '', `#${id}`);
  } catch (e) { $('message').textContent = e.message; }
}
document.querySelectorAll('nav button').forEach(button => { button.onclick = () => { kind = button.dataset.kind; document.querySelectorAll('nav button').forEach(b => b.setAttribute('aria-pressed', String(b === button))); $('list-title').textContent = button.textContent; load(); }; });
$('track').onchange = () => load(); $('more').onclick = () => load(true);
$('feedback-form').onsubmit = async event => {
  event.preventDefault(); const button = event.submitter; button.disabled = true;
  try { if (!selected) throw Error('Select an artifact first.'); await get('/api/feedback', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({target_id: selected, group_id: $('group').value, category: $('category').value, summary: $('summary').value, detail: $('issue-detail').value})}); $('feedback-status').textContent = 'Feedback recorded. Scientific decisions and releases are unchanged.'; $('summary').value = ''; $('issue-detail').value = ''; await overview(); if (kind === 'feedback') await load(); }
  catch (e) { $('feedback-status').textContent = e.message; } finally { button.disabled = false; }
};
async function start() { await overview(); const groups = await get('/api/artifacts?kind=workspace&limit=100'); groups.items.sort((a,b) => a.payload.group_id.localeCompare(b.payload.group_id)); for (const g of groups.items) { const o = node('option', g.title); o.value = g.payload.group_id; $('group').append(o); } await load(); if (/^#[a-f0-9]{64}$/.test(location.hash)) await inspect(location.hash.slice(1)); }
start().catch(e => { $('message').textContent = e.message; });
