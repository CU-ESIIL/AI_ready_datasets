"""Independent analysis oracles, invalid inputs and deterministic generation."""
import numpy as np
import pytest
from dataset_prototype.embedding_utility import strict_break_even, ridge_predictions, generated_tile


def test_strict_break_even_and_no_crossing():
    assert strict_break_even(120, 3, 1) == 61
    assert strict_break_even(120, 3, 1, refresh=20) == 71
    assert strict_break_even(0, 3, 1) == 1
    assert strict_break_even(120, 1, 1) is None
    assert strict_break_even(120, 1, 2) is None
    for bad in (-1, float('nan'), float('inf')):
        with pytest.raises(ValueError):
            strict_break_even(bad, 3, 1)


def test_linear_oracle_constant_column_and_no_test_label_access():
    x = np.linspace(-2, 2, 80)
    features = np.column_stack([x, np.ones(len(x))])
    prediction, alpha = ridge_predictions(features[:40], 2*x[:40]+3,
        features[40:60], 2*x[40:60]+3, features[60:])
    assert np.max(np.abs(prediction - (2*x[60:]+3))) < .01
    assert alpha == .01
    same, _ = ridge_predictions(features[:40], 2*x[:40]+3,
        features[40:60], 2*x[40:60]+3, features[60:])
    assert np.array_equal(prediction, same)


def test_invalid_ridge_and_generator():
    x = np.ones((4, 2))
    for bad in (np.ones((4, 3)), np.full((4, 2), np.nan), np.ones(4)):
        with pytest.raises(ValueError):
            ridge_predictions(x, np.ones(4), bad, np.ones(4), x)
    with pytest.raises(ValueError):
        generated_tile(0, -1)
    assert np.array_equal(generated_tile(3, 4), generated_tile(3, 4))
    assert not np.array_equal(generated_tile(3, 4), generated_tile(3, 5))
