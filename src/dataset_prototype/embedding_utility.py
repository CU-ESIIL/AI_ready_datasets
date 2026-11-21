"""Offline analysis helpers; no model output, source access or execution authority."""
import math


def strict_break_even(preparation, direct_per_query, embedding_per_query, *, refresh=0):
    """First integer query count with strictly lower embedding cost.

    All inputs use the same declared cost unit. Refresh is a fixed cost over the
    analysis horizon, not an inferred refresh frequency. Equal costs are not wins.
    """
    values = (preparation, direct_per_query, embedding_per_query, refresh)
    if any(not math.isfinite(v) or v < 0 for v in values):
        raise ValueError('costs must be finite and nonnegative')
    saving = direct_per_query - embedding_per_query
    if saving <= 0:
        return None
    return math.floor((preparation + refresh) / saving) + 1


def ridge_predictions(train, y, validation, validation_y, test):
    """Train-only scaling, validation-only alpha selection, then predictions.

    Test labels deliberately are not an argument. Arrays are bounded caller-owned
    synthetic analysis inputs; this helper is not a scientific execution backend.
    """
    import numpy as np
    arrays = [np.asarray(a, dtype=float) for a in (train, y, validation, validation_y, test)]
    x, y, v, vy, t = arrays
    if (x.ndim != 2 or v.ndim != 2 or t.ndim != 2 or y.ndim != 1 or vy.ndim != 1
            or not 2 <= len(x) <= 1024 or not 1 <= x.shape[1] <= 1024
            or not 1 <= len(v) <= 1024 or not 1 <= len(t) <= 1024
            or len(y) != len(x) or len(vy) != len(v)
            or x.shape[1] != v.shape[1] or x.shape[1] != t.shape[1]
            or not all(np.isfinite(a).all() for a in arrays)):
        raise ValueError('finite bounded compatible training/validation/test arrays required')
    mean, scale = x.mean(0), x.std(0)
    scale[scale < 1e-10] = 1
    x, v, t = ((a - mean) / scale for a in (x, v, t))
    intercept = float(y.mean())
    candidates = []
    for alpha in (.01, 1., 100.):
        if x.shape[1] <= len(x):
            coef = np.linalg.solve(x.T @ x + alpha * np.eye(x.shape[1]), x.T @ (y - intercept))
        else:
            coef = x.T @ np.linalg.solve(x @ x.T + alpha * np.eye(len(x)), y - intercept)
        loss = float(np.mean((v @ coef + intercept - vy) ** 2))
        candidates.append((loss, alpha, coef))
    _, alpha, coef = min(candidates, key=lambda row: (row[0], row[1]))
    return t @ coef + intercept, alpha


def generated_tile(seed, index, *, side=12):
    """One generated in-memory tile; no observations, geospatial or agent claim."""
    import numpy as np
    if seed < 0 or index < 0 or not 4 <= side <= 32:
        raise ValueError('nonnegative identities and bounded tile side required')
    rng = np.random.default_rng(np.random.SeedSequence([seed, index]))
    brightness = rng.uniform(.1, .8)
    amplitude = rng.uniform(.01, .12)
    return brightness + amplitude * rng.normal(size=(side, side))
