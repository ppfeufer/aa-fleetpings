"""
App config
"""

# Django
from django.apps import AppConfig
from django.utils.text import format_lazy

# AA Fleet Pings
from fleetpings import __title_translated__, __version__


class AaFleetpingsConfig(AppConfig):
    """
    Application config
    """

    name = "fleetpings"
    label = "fleetpings"
    verbose_name = format_lazy(
        "{app_title} v{version}", app_title=__title_translated__, version=__version__
    )
