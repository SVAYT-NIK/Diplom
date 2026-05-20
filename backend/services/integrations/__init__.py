"""
Integration submodules for external systems: GIS ZKH, 1C billing, Rosgidromet weather API.
Implements adapters for XML/JSON exports and protocol converters.
"""

from backend.services.integrations.gis_zkh import GISZKHConnector
from backend.services.integrations.weather import WeatherAPIConnector
from backend.services.integrations.billing import BillingConnector

__all__ = [
    "GISZKHConnector",
    "WeatherAPIConnector",
    "BillingConnector",
]