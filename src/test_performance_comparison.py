import pytest
import numpy as np
from performance_comparison import PerformanceComparison

def test_performance_comparison():
    model = np.array([0.5, 0.5, 0.5])
    other_models = [np.array([0.2, 0.2, 0.2]), np.array([0.6, 0.6, 0.6])]
    performance_comparison = PerformanceComparison()
    result = performance_comparison.compare_performance(model, other_models)
    assert isinstance(result, bool)
