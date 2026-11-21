"""Private isolated worker for pinned, trusted upstream operations, never model code.

Run only through UpstreamBackend. It imports one hash-verified source file, not
this repository's or the upstream's top-level cubedynamics package.
"""
import importlib.util
import hashlib
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
from time import perf_counter_ns

PIN = '2e20e15a42610f77cdd0583bb5a43fcc6f6c8959'
SHA = '5b8fddd59c552fea22dc9a68fff911674a5a61c41399455e9fba1a9902c4ae9a'


def emit(value):
    print(json.dumps(value, allow_nan=False, separators=(',',':')), flush=True)


def main():
    root = Path(sys.argv[1]).resolve()
    actual = subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD'], text=True).strip()
    if actual != PIN:
        raise ValueError('upstream checkout must match pinned commit')
    path = root/'src/cubedynamics/analysis_v2.py'
    expected_git_blob = subprocess.check_output(['git','-C',str(root),'show',f'{PIN}:src/cubedynamics/analysis_v2.py'])
    if hashlib.sha256(path.read_bytes()).hexdigest() != SHA or path.read_bytes() != expected_git_blob:
        raise ValueError('modified or incompatible upstream operation source')
    # This fixed, reviewed upstream file contains only trusted static code.
    spec = importlib.util.spec_from_file_location('_pinned_fire_vase_analysis', path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    import numpy as np
    import pandas as pd
    import scipy
    versions = {'python':sys.version.split()[0], 'numpy':np.__version__, 'pandas':pd.__version__, 'scipy':scipy.__version__}
    emit({'ready':True, 'commit':actual, 'sha256':SHA, 'versions':versions})
    for line in sys.stdin:
        started = perf_counter_ns()
        try:
            if len(line) > 1_000_000:
                raise ValueError('request exceeds bounded protocol')
            request = json.loads(line)
            if set(request) != {'operation','input'}:
                raise ValueError('invalid worker envelope')
            operation, values = request['operation'], request['input']
            if operation == 'features':
                g = np.asarray(values, dtype=float)
                if g.ndim != 1 or not 3 <= len(g) <= 512 or not np.isfinite(g).all() or (g < 0).any() or g.sum() <= 0:
                    raise ValueError('features require bounded complete nonnegative positive-total growth')
                summary, probabilities = module.growth_summary(g, len(g), float(g.sum()))
                traits, profile = module.shape_traits(probabilities, bins=20)
                # Same padded peak detector/threshold as pinned pulse_counts; locations
                # add bookkeeping, not a new scientific prominence definition.
                locations, _ = module.find_peaks(np.r_[0.,g,0.], prominence=.20*g.max())
                locations = (locations-1).tolist()
                count, reactivations = module.pulse_counts(g)
                if count != len(locations):
                    raise ValueError('pulse location/count inconsistency')
                result = {'profile':profile.tolist(), 'traits':{**traits, 'normalized_entropy':summary['normalized_entropy']},
                    'pulse_indices':locations, 'pulse_count':count, 'reactivation_count':reactivations,
                    'peak_growth_km2_per_day':summary['peak_growth_km2_per_day']}
            elif operation == 'pulses':
                g = np.asarray(values, dtype=float)
                if g.ndim != 1 or not 1 <= len(g) <= 512 or not np.isfinite(g).all() or (g < 0).any():
                    raise ValueError('pulse counts need finite nonnegative observed increments')
                count, reactivations = module.pulse_counts(g)
                locations, _ = module.find_peaks(np.r_[0.,g,0.], prominence=.20*g.max())
                result = {'pulse_count':count,'pulse_indices':(locations-1).tolist(),'reactivation_count':reactivations}
                if len(result['pulse_indices']) != count:
                    raise ValueError('pulse locations differ from upstream count')
            elif operation == 'fit_pca':
                x = np.asarray(values, dtype=float)
                if x.ndim != 2 or not 2 <= len(x) <= 64 or x.shape[1] != 20 or not np.isfinite(x).all():
                    raise ValueError('PCA requires bounded training matrix with 20 declared features')
                fit = module.fit_pca(x)
                result = {'mean':fit.mean.tolist(), 'scale':fit.scale.tolist(),
                    'loadings':fit.loadings.T.tolist(), 'explained_variance':fit.evr.tolist()}
            else:
                raise ValueError('unknown worker operation; closed dispatch only')
            rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            emit({'ok':True, 'result':result, 'compute_ns':perf_counter_ns()-started,
                'worker_peak_rss_bytes':int(rss if sys.platform=='darwin' else rss*1024)})
        except Exception as error:
            emit({'ok':False, 'error_type':type(error).__name__, 'error':str(error),
                'compute_ns':perf_counter_ns()-started})


if __name__ == '__main__':
    main()
