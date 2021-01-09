# -*- coding: utf-8 -*-

"""
our app setting
"""

import re

from django.conf import settings

from fleetpings.utils import clean_setting

from packaging import version

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


def optimer_installed() -> bool:
    """
    check if optimer_installed is installed
    :return: bool
    """

    return "allianceauth.optimer" in settings.INSTALLED_APPS


def get_timzones_version():
    """
    get the version of aa-timezones, when installed
    :return: string or None
    """

    if timezones_installed():
        from timezones import __version__ as timezones_version

        return timezones_version

    return None


def use_new_timezone_links() -> bool:
    """
    determins whether to use then new link format from aa-timezones or not
    the new link format has been introduced with aa-timezones v1.2.1
    :return: bool
    """

    return_value = True

    if get_timzones_version() and version.parse(get_timzones_version()) < version.parse(
        "1.2.1"
    ):
        return_value = False

    return return_value


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
    :return: bool
    """

    return "allianceauth.services.modules.discord" in settings.INSTALLED_APPS


def srp_module_installed() -> bool:
    return_value = False

    if (
        "allianceauth.srp" in settings.INSTALLED_APPS
        or "aasrp" in settings.INSTALLED_APPS
    ):
        return_value = True

    return return_value


def srp_module_is(module_name: str) -> str:
    """
    check for a specific SRP module
    :param module_name:
    """

    return module_name in settings.INSTALLED_APPS
