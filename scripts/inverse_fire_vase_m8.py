"""Grade deterministic training-only PCA inverse; no downstream labels are fitted."""
import argparse
import csv
from pathlib import Path
import numpy as np
from dataset_prototype.embedding_study.observed_state import NAMES


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    out = Path(parser.parse_args().output)
    private = out / 'private'
    with np.load(private / 'observed-state.npz', allow_pickle=False) as f:
        ds = dict(f)
    prep = dict(np.load(private / 'preprocess-1p0.npz', allow_pickle=False))
    scales = np.load(private / 'evaluation-scales.npz', allow_pickle=False)['scale']
    x = (np.column_stack([np.where(ds['mask'], ds['y'], prep['median']), ds['mask'].astype(float)]) - prep['mean']) / prep['scale']
    rows = []
    for d in (4, 8, 16, 32, 64):
        components = np.load(private / f'pca-{d}-1p0.npz', allow_pickle=False)['components']
        back = (x @ components @ components.T) * prep['scale'] + prep['mean']
        for label, subset in [('all', ds['fold'] == 'test'), ('one', (ds['fold'] == 'test') & (ds['n'] == 1)), ('two', (ds['fold'] == 'test') & (ds['n'] == 2)), ('three_plus', (ds['fold'] == 'test') & (ds['n'] >= 3))]:
            for j, name in enumerate(NAMES):
                use = subset & ds['mask'][:, j]
                error = back[use, j] - ds['y'][use, j]
                rows.append(dict(requested_dimension=d, effective_rank=components.shape[1], stratum=label, property=name, eligible_test_fires=int(use.sum()), standardized_mse=float(np.mean((error / scales[j]) ** 2)) if len(error) else None, max_absolute_transformed_error=float(abs(error).max()) if len(error) else None, support_mask_error_rate=float(np.mean((back[subset, j + 10] >= .5) != ds['mask'][subset, j])), scope='deterministic PCA inverse, no downstream scientific labels; full-rank numerical state roundtrip is not source-bit preservation'))
    with (out / 'pca-inverse-recovery.csv').open('w') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == '__main__':
    main()
