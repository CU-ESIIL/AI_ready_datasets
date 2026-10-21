/* Progressive enhancement: canonical inventory remains a complete no-JS table. */
(() => {
  const host = document.getElementById('semantic-filters');
  const data = document.getElementById('semantic-filter-data');
  if (!host || !data) return;
  const resources = JSON.parse(data.dataset.resources);
  const rows = new Map();
  document.querySelectorAll('table tbody tr').forEach(row => {
    const link = row.querySelector('a[href^="#"]');
    if (link) rows.set(link.getAttribute('href').slice(1), row);
  });
  const fields = [['era','Era'], ['domain','Domain'], ['kind','Resource type'],
    ['level','Biological level'], ['role','Project role'], ['status','Status'],
    ['category','Candidate category'], ['dimension','Semantic dimension']];
  const controls = [];
  fields.forEach(([key, title]) => {
    const label = document.createElement('label');
    label.textContent = title;
    const select = document.createElement('select');
    select.id = `semantic-${key}`;
    select.setAttribute('aria-label', title);
    select.add(new Option('All', ''));
    const values = [...new Set(resources.flatMap(r => r[key]))].sort();
    values.forEach(value => select.add(new Option(value.replaceAll('_', ' '), value)));
    label.append(select); host.append(label); controls.push([key,select]);
    select.addEventListener('change', update);
  });
  const searchLabel = document.createElement('label'); searchLabel.textContent = 'Name or acronym';
  const search = document.createElement('input'); search.type = 'search';
  search.id = 'semantic-search'; search.setAttribute('aria-label','Name or acronym');
  searchLabel.append(search); host.prepend(searchLabel); search.addEventListener('input', update);
  const reset = document.createElement('button'); reset.type = 'button'; reset.textContent = 'Reset filters';
  reset.addEventListener('click', () => { search.value=''; controls.forEach(([,s]) => s.value=''); update(); });
  host.append(reset); host.hidden=false;
  function update() {
    let count=0; const query=search.value.trim().toLowerCase();
    resources.forEach(r => {
      const matches = `${r.name} ${r.acronym}`.toLowerCase().includes(query) && controls.every(([k,s]) =>
        !s.value || (Array.isArray(r[k]) ? r[k].includes(s.value) : r[k]===s.value));
      const row=rows.get(r.id); if (row) row.hidden=!matches;
      if (matches) count++;
    });
    document.getElementById('semantic-count').textContent = `${count} of ${resources.length} resources shown. Details below retain the complete inventory.`;
  }
  function openTarget() {
    const target=document.getElementById(decodeURIComponent(location.hash.slice(1)));
    if (target?.tagName === 'DETAILS') target.open=true;
  }
  window.addEventListener('hashchange',openTarget); openTarget(); update();
})();
