"""
App config
"""

# Django
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

# AA Fleet Pings
from fleetpings import __version__


class AaFleetpingsConfig(AppConfig):
    """
    Application config
    """

    name = "fleetpings"
    label = "fleetpings"
    # Translators: This is the app name and version, which will appear in the Django Backend
    verbose_name = _(f"Fleet Pings v{__version__}")
