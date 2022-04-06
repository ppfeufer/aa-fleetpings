"""
our app setting
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
        # Third Party
        from timezones import __version__ as timezones_version

        return timezones_version

    return None


def fittings_installed() -> bool:
    """
    check if fittings is installed
    :return: bool
    """

    return apps.is_installed("fittings")


def discord_service_installed() -> bool:
    """
    check if the Discord service is installed
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
