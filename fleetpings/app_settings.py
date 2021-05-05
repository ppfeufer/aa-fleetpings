"""
our app setting
"""

import re

from packaging import version

from django.apps import apps
from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest

from fleetpings.utils import clean_setting

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

    return apps.is_installed("timezones")


def optimer_installed() -> bool:
    """
    check if optimer_installed is installed
    :return: bool
    """

    return apps.is_installed("allianceauth.optimer")


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

    return apps.is_installed("fittings")


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

    return apps.is_installed("allianceauth.services.modules.discord")


def srp_module_installed() -> bool:
    return_value = False

    if apps.is_installed("allianceauth.srp") or apps.is_installed("aasrp"):
        return_value = True

    return return_value


def srp_module_is(module_name: str) -> bool:
    """
    check for a specific SRP module
    :param module_name:
    """

    return apps.is_installed(module_name)


def can_add_srp_links(request: WSGIRequest, module_name: str) -> bool:
    """
    check if the current user has the rights to add SRP links for the module
    :param request:
    :param module_name:
    """

    return_value = False

    if module_name == "aasrp" and (
        request.user.has_perm("aasrp.manage_srp")
        or request.user.has_perm("aasrp.create_srp")
    ):
        return_value = True

    if module_name == "allianceauth.srp" and (
        request.user.has_perm("auth.srp_management")
        or request.user.has_perm("srp.add_srpfleetmain")
    ):
        return_value = True

    return return_value
