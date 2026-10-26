"""Offline accounting checks; does not validate demand or provider agreements."""
import argparse
import copy
import csv
from decimal import Decimal, ROUND_CEILING
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
D = Decimal


def require(condition, message):
    if not condition:
        raise ValueError(message)


def validate(rows, markdown):
    # Lifecycle tables repeat category labels with different columns.
    # Check those independently rather than confusing them with budget tables.
    accounting_markdown = markdown
    if '## Retention and growth ledger' in markdown:
        accounting_markdown = (markdown.split('## Retention and growth ledger', 1)[0]
                               + markdown.split('## Proposed versioned backup policy', 1)[1])
    indexed = {(int(r['year']), r['type']): r for r in rows}
    require(len(indexed) == len(rows), 'duplicate year/type rows')
    require(set(y for y, _ in indexed) == {1, 2, 3}, 'grant years')
    types = {kind for year, kind in indexed if year == 1}
    require(all({kind for year, kind in indexed if year == y} == types
                for y in (1, 2, 3)), 'consistent annual row types')

    def quantity(year, kind):
        return D(indexed[year, kind]['quantity'])

    def table(label, expected):
        found = [line for line in accounting_markdown.splitlines()
                 if line.startswith('| ' + label + ' |')]
        require(len(found) == 1, 'unique Markdown row: ' + label)
        cells = [c.strip().replace('**', '').replace(',', '')
                 for c in found[0].strip('|').split('|')]
        for column, value in expected.items():
            require(cells[column] == str(value), f'Markdown mismatch: {label}, column {column}')

    annual_costs = []
    annual_primary_costs = []
    annual_backup_costs = []
    inference = []
    services = []
    totals = []
    for year in (1, 2, 3):
        product = quantity(year, 'product_collections')
        workspace = D(3 * 2 if year == 1 else 3 * 2 + 6 * 5 if year == 2 else 6 * 5)
        require(quantity(year, 'workspace') == workspace, 'cohort quota accounting')
        mutable = workspace + quantity(year, 'shared_metadata')
        previous = (quantity(year - 1, 'workspace') + quantity(year - 1, 'shared_metadata')
                    if year > 1 else mutable)
        history = (max(mutable, previous) * (14 * D('.005') + 12 * D('.02') + 12 * D('.05'))).to_integral_value(rounding=ROUND_CEILING)
        if year == 3:
            history += 3 * 2  # Explicit reserve for governance workspace closeout.
        require(quantity(year, 'backup_history') == history, 'retained history/closeout accounting')
        primary = product + mutable
        require(quantity(year, 'backup_current_copy') == primary, 'full backup content copy')
        headroom = (primary * D('.2')).to_integral_value(rounding=ROUND_CEILING)
        require(quantity(year, 'primary_headroom') == headroom, '20 percent recovery headroom')
        primary_quota = primary + headroom
        backup_quota = primary + history
        require(quantity(year, 'primary_storage_expense') == primary_quota, 'billed primary quota')
        require(quantity(year, 'backup_storage_expense') == backup_quota, 'billed backup quota')
        expenses = [r for r in rows if int(r['year']) == year and r['cost_usd'] != '']
        require(len(expenses) == 4, 'four expense categories')
        for row in expenses:
            require(D(row['quantity']) * D(row['unit_rate_usd']) == D(row['cost_usd']), 'quantity times rate: ' + row['type'])
        for kind in ('primary_storage_expense', 'backup_storage_expense'):
            require(D(indexed[year, kind]['unit_rate_usd']) == 60, 'documented reference/assumed rate')
        cash = sum(D(r['cost_usd']) for r in expenses)
        annual_costs.append(cash)
        annual_primary_costs.append(primary_quota * 60)
        annual_backup_costs.append(backup_quota * 60)
        su = quantity(year, 'inference') * 128
        require(quantity(year, 'inference_SU') == su, 'inference SU conversion')
        service_su = D(8 * 24 * 365)
        require(quantity(year, 'persistent_services') == service_su, 'continuous CPU service')
        inference.append(su)
        services.append(service_su)
        table('Primary content subtotal', {year: primary})
        table('Backup: historical changed/deleted mutable content', {year: history})
        table('Backup allocation subtotal', {year: backup_quota})
        table('**Total allocated storage**', {year: primary_quota + backup_quota})
        table('**Cash planning total**', {year + 1: cash})
        table('Same inference expressed as Jetstream2 SUs', {year: su})
        table('Persistent standard CPU service SUs', {year: service_su})
        for label, kind in [('Three product collections, combined', 'product_collections'),
                            ('Group workspaces', 'workspace'),
                            ('Shared metadata/governance', 'shared_metadata'),
                            ('Primary recovery/publication headroom', 'primary_headroom'),
                            ('Backup: current full content copy', 'backup_current_copy')]:
            table(label, {year: quantity(year, kind)})
        for label, kind in [('Commercial inference APIs', 'commercial_api_expense'),
                            ('Hosting/distribution/access services', 'hosting_expense'),
                            ('TACC primary capacity, including headroom', 'primary_storage_expense'),
                            ('TACC additional versioned backup', 'backup_storage_expense')]:
            table(label, {year + 1: D(indexed[year, kind]['cost_usd'])})
        bounds = [su + service_su + quantity(year, 'development_cpu_' + bound) for bound in ('low', 'high')]
        table('Inference/development/service subtotal SUs', {year: f'{bounds[0]}–{bounds[1]}'})
        totals.append(bounds)
        print(f'Year {year}: {primary_quota + backup_quota} TB; cash ${cash:,}; checks passed')
    table('**Cash planning total**', {5: sum(annual_costs)})
    table('TACC primary capacity, including headroom', {5: sum(annual_primary_costs)})
    table('TACC additional versioned backup', {5: sum(annual_backup_costs)})
    for label, kind in [('Commercial inference APIs', 'commercial_api_expense'), ('Hosting/distribution/access services', 'hosting_expense')]:
        table(label, {5: sum(D(indexed[y, kind]['cost_usd']) for y in (1, 2, 3))})
    table('Same inference expressed as Jetstream2 SUs', {4: sum(inference)})
    table('Persistent standard CPU service SUs', {4: sum(services)})
    table('VERDE inference, H100 reference instance-hours', {**{y: quantity(y, 'inference') for y in (1, 2, 3)}, 4: sum(quantity(y, 'inference') for y in (1, 2, 3))})
    table('Development/cohort standard CPU SUs', {**{y: f"{quantity(y, 'development_cpu_low')}–{quantity(y, 'development_cpu_high')}" for y in (1, 2, 3)}, 4: f"{sum(quantity(y, 'development_cpu_low') for y in (1, 2, 3))}–{sum(quantity(y, 'development_cpu_high') for y in (1, 2, 3))}"})
    table('Inference/development/service subtotal SUs', {4: f'{sum(t[0] for t in totals)}–{sum(t[1] for t in totals)}'})
    print(f'Three-year cash total: ${sum(annual_costs):,}. Demand and quotes remain unverified.')


def validate_lifecycle(flows, rows, markdown):
    """Check carry-forward balances and reconcile to the existing budget."""
    indexed = {(int(r['year']), r['type']): r for r in flows}
    budget = {(int(r['year']), r['type']): D(r['quantity']) for r in rows}
    kinds = {'product_collections': 'Three product collections',
             'workspace': 'Group workspaces',
             'shared_metadata': 'Shared metadata/governance',
             'primary_content_subtotal': 'Primary content subtotal',
             'backup_current_copy': 'Backup current-copy allocation',
             'backup_history': 'Backup history allowance',
             'primary_headroom': 'Recovery/publication headroom',
             'total_allocated_storage': 'Total allocated storage'}
    require(len(indexed) == len(flows) == 24, 'unique complete lifecycle rows')
    require(set(indexed) == {(y, k) for y in (1, 2, 3) for k in kinds}, 'lifecycle coverage')
    fields = ('opening_tb', 'new_tb', 'retired_tb', 'closing_tb')

    def value(year, kind, field):
        return D(indexed[year, kind][field])

    for year in (1, 2, 3):
        for kind, label in kinds.items():
            row = indexed[year, kind]
            require(row['unit'] == 'TB', 'lifecycle units')
            opening, new, retired, closing = [D(row[f]) for f in fields]
            require(min(opening, new, retired, closing) >= 0, 'nonnegative lifecycle values')
            require(opening + new - retired == closing, 'lifecycle mass balance')
            require(opening == (value(year - 1, kind, 'closing_tb') if year > 1 else 0), 'year-to-year carry-forward')
            if kind not in ('primary_content_subtotal', 'total_allocated_storage'):
                require(closing == budget[year, kind], 'lifecycle/budget closing consistency')
            cells = [label, str(year), *[str(D(row[f])) for f in fields]]
            expected = '| ' + ' | '.join(cells) + ' |'
            require(markdown.splitlines().count(expected) == 1, 'lifecycle Markdown consistency: ' + kind)
        for field in fields:
            primary = sum(value(year, k, field) for k in ('product_collections', 'workspace', 'shared_metadata'))
            require(value(year, 'primary_content_subtotal', field) == primary, 'primary lifecycle sum')
            require(value(year, 'backup_current_copy', field) == primary, 'backup current-copy lifecycle')
            total = primary + sum(value(year, k, field) for k in ('backup_current_copy', 'backup_history', 'primary_headroom'))
            require(value(year, 'total_allocated_storage', field) == total, 'total lifecycle sum')
        require(value(year, 'product_collections', 'retired_tb') == 0, 'retained product releases')
        require(value(year, 'shared_metadata', 'retired_tb') == 0, 'retained governance metadata')
    require(value(3, 'workspace', 'retired_tb') == 6, 'explicit closeout assumption')
    print('Lifecycle: all 24 rows balance, carry forward, and match CSV/Markdown capacity.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    with (ROOT / 'docs/assets/data/grant-resource-budget.csv').open() as stream:
        rows = list(csv.DictReader(stream))
    markdown = (ROOT / 'docs/resource-budget.md').read_text()
    validate(rows, markdown)
    with (ROOT / 'docs/assets/data/grant-storage-lifecycle.csv').open() as stream:
        flows = list(csv.DictReader(stream))
    validate_lifecycle(flows, rows, markdown)
    if args.self_test:
        cases = []
        for kind, field in [('backup_history', 'quantity'), ('primary_storage_expense', 'cost_usd'), ('inference_SU', 'quantity')]:
            bad = copy.deepcopy(rows)
            item = next(r for r in bad if r['year'] == '3' and r['type'] == kind)
            item[field] = str(D(item[field]) + 1)
            cases.append((bad, markdown))
        cases.append((rows, markdown.replace('**120,160**', '**120,161**')))
        for bad_rows, bad_markdown in cases:
            try:
                validate(bad_rows, bad_markdown)
            except ValueError:
                continue
            raise ValueError('deliberately invalid input was accepted')
        print('Four invalid-input checks passed: history, expense, inference SUs, Markdown total.')
        for field in ('opening_tb', 'retired_tb'):
            bad = copy.deepcopy(flows)
            item = next(r for r in bad if r['year'] == '3' and r['type'] == 'workspace')
            item[field] = str(D(item[field]) + 1)
            try:
                validate_lifecycle(bad, rows, markdown)
            except ValueError:
                continue
            raise ValueError('invalid lifecycle input accepted')
        print('Two invalid lifecycle checks passed: opening balance and retirement.')


if __name__ == '__main__':
    main()
