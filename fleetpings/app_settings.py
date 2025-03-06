"""
App settings for fleetpings
"""

# Standard Library
from re import RegexFlag

# Django
from django.apps import apps
from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest


def timezones_installed() -> bool:
    """
    Check if timezones is installed

    :return:
    :rtype:
    """

    return apps.is_installed(app_name="timezones")


def optimer_installed() -> bool:
    """
    Check if allianceauth.optimer is installed

    :return:
    :rtype:
    """

    return apps.is_installed(app_name="allianceauth.optimer")


def fittings_installed() -> bool:
    """
    Check if the Fittings module is installed

    :return:
    :rtype:
    """

    return apps.is_installed(app_name="fittings")


def discord_service_installed() -> bool:
    """
    Check if the Discord service module is installed

    :return:
    :rtype:
    """

    return apps.is_installed(app_name="allianceauth.services.modules.discord")


def srp_module_installed() -> bool:
    """
    Check if any SRP module is installed

    :return:
    :rtype:
    """

    return apps.is_installed(app_name="allianceauth.srp") or apps.is_installed(
        app_name="aasrp"
    )


def srp_module_is(module_name: str) -> bool:
    """
    Check if the given SRP module is installed

    :param module_name:
    :type module_name:
    :return:
    :rtype:
    """

    return apps.is_installed(app_name=module_name)


def can_add_srp_links(request: WSGIRequest, module_name: str) -> bool:
    """
    Check if the user can add SRP links

    :param request:
    :type request:
    :param module_name:
    :type module_name:
    :return:
    :rtype:
    """

    return_value = False

    if module_name == "aasrp" and (
        request.user.has_perm(perm="aasrp.manage_srp")
        or request.user.has_perm(perm="aasrp.create_srp")
    ):
        return_value = True

    if module_name == "allianceauth.srp" and (
        request.user.has_perm(perm="auth.srp_management")
        or request.user.has_perm(perm="srp.add_srpfleetmain")
    ):
        return_value = True

    return return_value


def use_fittings_module_for_doctrines() -> bool:
    """
    Check if the Fittings module is used for doctrines

    :return:
    :rtype:
    """

    # AA Fleet Pings
    from fleetpings.models import (  # pylint: disable=import-outside-toplevel, cyclic-import
        Setting,
    )

    return (
        fittings_installed() is True
        and Setting.objects.get_setting(
            setting_key=Setting.Field.USE_DOCTRINES_FROM_FITTINGS_MODULE
        )
        is True
    )


def debug_enabled() -> RegexFlag:
    """
    Check if DEBUG is enabled

    :return:
    :rtype:
    """

    return settings.DEBUG
