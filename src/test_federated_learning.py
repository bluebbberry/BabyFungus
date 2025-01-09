import numpy as np
from federated_learning import FederatedLearning

def test_model_initialization():
    fl = FederatedLearning()
    assert fl.model.shape == (3,)
    assert np.all(fl.local_gradients == 0)

def test_training_step():
    fl = FederatedLearning()
    initial_model = fl.model.copy()
    fl.train()
    assert not np.array_equal(initial_model, fl.model)
    assert np.all(fl.local_gradients != 0)
