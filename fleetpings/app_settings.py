"""
App setting
"""

# Django
from django.apps import apps
from django.core.handlers.wsgi import WSGIRequest

# AA Fleet Pings
from fleetpings.utils import clean_setting

# Set default panels if none are set in local.py
AA_FLEETPINGS_USE_DOCTRINES_FROM_FITTINGS_MODULE = clean_setting(
    "AA_FLEETPINGS_USE_DOCTRINES_FROM_FITTINGS_MODULE", False
)

# Allow non discord webhook url's
AA_FLEETPINGS_WEBHOOK_VERIFICATION = clean_setting(
    "AA_FLEETPINGS_WEBHOOK_VERIFICATION", True
)


def timezones_installed() -> bool:
    """
    Check if aa-timezones is installed
    :return: bool
    """

    return apps.is_installed("timezones")


def optimer_installed() -> bool:
    """
    Check if optimer_installed is installed
    :return: bool
    """

    return apps.is_installed("allianceauth.optimer")


def fittings_installed() -> bool:
    """
    Check if fittings is installed
    :return: bool
    """

    return apps.is_installed("fittings")


def discord_service_installed() -> bool:
    """
    Check if the Discord service is installed
    :return: bool
    """

    return apps.is_installed("allianceauth.services.modules.discord")


def srp_module_installed() -> bool:
    """
    Check if any of the SRP modules is installed
    :return:
    """

    return apps.is_installed("allianceauth.srp") or apps.is_installed("aasrp")


def srp_module_is(module_name: str) -> bool:
    """
    Check for a specific SRP module
    :param module_name:
    """

    return apps.is_installed(module_name)


def can_add_srp_links(request: WSGIRequest, module_name: str) -> bool:
    """
    Check if the current user has the rights to add SRP links for the module
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
