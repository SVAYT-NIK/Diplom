"""
Regression models submodule.
Implements HuberRegressor, Ridge/Lasso, QuantileRegressor, pyGAM for energy consumption modeling.
"""

from ml_models.regression.models import RegressionModels
from ml_models.regression.huber import HuberEnergyRegressor
from ml_models.regression.quantile import QuantileEnergyRegressor

__all__ = [
    "RegressionModels",
    "HuberEnergyRegressor",
    "QuantileEnergyRegressor",
]