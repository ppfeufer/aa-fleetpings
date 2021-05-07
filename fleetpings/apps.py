"""
app config
"""

from django.apps import AppConfig

from fleetpings import __version__


class AaFleetpingsConfig(AppConfig):
    """
    application config
    """

    name = "fleetpings"
    label = "fleetpings"
    verbose_name = f"Fleet Pings v{__version__}"
