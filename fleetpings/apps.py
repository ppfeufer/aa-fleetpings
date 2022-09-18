"""
App config
"""

# Django
from django.apps import AppConfig

# AA Fleet Pings
from fleetpings import __version__


class AaFleetpingsConfig(AppConfig):
    """
    Application config
    """

    name = "fleetpings"
    label = "fleetpings"
    verbose_name = f"Fleet Pings v{__version__}"
