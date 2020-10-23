# -*- coding: utf-8 -*-

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
    verbose_name = "Fleet Pings v{}".format(__version__)
