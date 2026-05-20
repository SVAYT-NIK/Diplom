"""
ML Models package for statistical analysis, forecasting, and anomaly detection.
Implements regression, time series (ARIMA/Prophet), clustering, and consensus-based anomaly detection.
"""

__version__ = "1.0.0"
__author__ = "Energy Analytics ML Team"

from ml_models.base import BaseModelWrapper
from ml_models.regression.models import RegressionModels
from ml_models.time_series.forecasters import TimeSeriesForecasters
from ml_models.anomaly_detection.detectors import AnomalyDetectors
from ml_models.clustering.clusterers import ClusteringAlgorithms

__all__ = [
    "BaseModelWrapper",
    "RegressionModels",
    "TimeSeriesForecasters",
    "AnomalyDetectors",
    "ClusteringAlgorithms",
]