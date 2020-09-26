# -*- coding: utf-8 -*-

"""
our app setting
"""

import re

from django.conf import settings

from .utils import clean_setting

# set default panels if none are set in local.py
AA_FLEETPINGS_USE_SLACK = clean_setting("AA_FLEETPINGS_USE_SLACK", False)
AA_FLEETPINGS_USE_DOCTRINES_FROM_FITTINGS_MODULE = clean_setting(
    "AA_FLEETPINGS_USE_DOCTRINES_FROM_FITTINGS_MODULE", False
)

# AA-GDPR
AVOID_CDN = clean_setting("AVOID_CDN", False)


def get_site_url():  # regex sso url
    """
    get the site url
    :return: string
    """
    regex = r"^(.+)\/s.+"
    matches = re.finditer(regex, settings.ESI_SSO_CALLBACK_URL, re.MULTILINE)
    url = "http://"

    for match in matches:
        url = match.groups()[0]  # first match

    return url


def timezones_installed() -> bool:
    """
    check if aa-timezones is installed
    :return: bool
    """
    return "timezones" in settings.INSTALLED_APPS


def fittings_installed() -> bool:
    """
    check if fittings is installed
    :return: bool
    """
    return "fittings" in settings.INSTALLED_APPS


def avoid_cdn() -> bool:
    """
    check if we should aviod CDN usage
    :return: bool
    """
    return AVOID_CDN


def discord_service_installed() -> bool:
    """
    check if the Discord service is installed
    :return:
    """
    return "allianceauth.services.modules.discord" in settings.INSTALLED_APPS
