"""
The views
"""

# Django
from django.contrib.auth.decorators import login_required, permission_required
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Alliance Auth
from allianceauth.services.hooks import get_extension_logger

# Alliance Auth (External Libs)
from app_utils.logging import LoggerAddTag
from app_utils.urls import site_absolute_url

# AA Fleet Pings
from fleetpings import __title__
from fleetpings.app_settings import (  # srp_module_is,
    AA_FLEETPINGS_USE_DOCTRINES_FROM_FITTINGS_MODULE,
    can_add_srp_links,
    fittings_installed,
    optimer_installed,
    srp_module_installed,
    timezones_installed,
)
from fleetpings.form import FleetPingForm
from fleetpings.models import (
    DiscordPingTargets,
    FleetComm,
    FleetDoctrine,
    FleetType,
    FormupLocation,
    Webhook,
)

# from django.utils import timezone


if (
    fittings_installed() is True
    and AA_FLEETPINGS_USE_DOCTRINES_FROM_FITTINGS_MODULE is True
):
    # Third Party
    from fittings.views import _get_docs_qs

# if optimer_installed():
#     # Alliance Auth
#     from allianceauth.optimer.models import OpTimer

logger = LoggerAddTag(get_extension_logger(__name__), __title__)


@login_required
@permission_required("fleetpings.basic_access")
def index(request: WSGIRequest) -> HttpResponse:
    """
    Index view
    """

    logger.info(f"Fleet pings view called by user {request.user}")

    srp_module_available_to_user = False
    if srp_module_installed() and (
        can_add_srp_links(request=request, module_name="aasrp")
        or can_add_srp_links(request=request, module_name="allianceauth.srp")
    ):
        srp_module_available_to_user = True

    context = {
        "title": __title__,
        "webhooks_configured": Webhook.objects.filter(
            Q(restricted_to_group__in=request.user.groups.all())
            | Q(restricted_to_group__isnull=True),
            is_enabled=True,
        ).exists(),
        "site_url": site_absolute_url(),
        "timezones_installed": timezones_installed(),
        "optimer_installed": optimer_installed(),
        "fittings_installed": fittings_installed(),
        "main_character": request.user.profile.main_character,
        "srp_module_available_to_user": srp_module_available_to_user,
        "form": FleetPingForm,
    }

    return render(request, "fleetpings/index.html", context)


@login_required
@permission_required("fleetpings.basic_access")
def ajax_get_ping_targets(request: WSGIRequest) -> HttpResponse:
    """
    Get ping targets for the current user
    :param request:
    :return:
    """

    logger.info(f"Getting ping targets for user {request.user}")

    additional_discord_ping_targets = (
        DiscordPingTargets.objects.filter(
            Q(restricted_to_group__in=request.user.groups.all())
            | Q(restricted_to_group__isnull=True),
            is_enabled=True,
        )
        .distinct()
        .order_by("name")
    )

    return render(
        request,
        "fleetpings/form/pingTargets.html",
        {"ping_targets": additional_discord_ping_targets},
    )


@login_required
@permission_required("fleetpings.basic_access")
def ajax_get_webhooks(request: WSGIRequest) -> HttpResponse:
    """
    Get webhooks for ccurrent user
    :param request:
    :return:
    """

    logger.info(f"Getting webhooks for user {request.user}")

    webhooks = (
        Webhook.objects.filter(
            Q(restricted_to_group__in=request.user.groups.all())
            | Q(restricted_to_group__isnull=True),
            is_enabled=True,
        )
        .distinct()
        .order_by("type", "name")
    )

    return render(
        request,
        "fleetpings/form/pingChannel.html",
        {"webhooks": webhooks},
    )


@login_required
@permission_required("fleetpings.basic_access")
def ajax_get_fleet_types(request: WSGIRequest) -> HttpResponse:
    """
    Get fleet types for current user
    :param request:
    :return:
    """

    logger.info(f"Getting fleet types for user {request.user}")

    fleet_types = (
        FleetType.objects.filter(
            Q(restricted_to_group__in=request.user.groups.all())
            | Q(restricted_to_group__isnull=True),
            is_enabled=True,
        )
        .distinct()
        .order_by("name")
    )

    return render(
        request,
        "fleetpings/form/fleetType.html",
        {"fleet_types": fleet_types},
    )


@login_required
@permission_required("fleetpings.basic_access")
def ajax_get_formup_locations(request: WSGIRequest) -> HttpResponse:
    """
    Get formup locations
    :param request:
    :return:
    """

    logger.info(f"Getting formup locations for user {request.user}")

    formup_locations = FormupLocation.objects.filter(is_enabled=True).order_by("name")

    return render(
        request,
        "fleetpings/form/formupLocation.html",
        {"formup_locations": formup_locations},
    )


@login_required
@permission_required("fleetpings.basic_access")
def ajax_get_fleet_comms(request: WSGIRequest) -> HttpResponse:
    """
    Get fleet comms
    :param request:
    :return:
    """

    logger.info(f"Getting formup locations for user {request.user}")

    fleet_comms = FleetComm.objects.filter(is_enabled=True).order_by("name")

    return render(
        request,
        "fleetpings/form/fleetComms.html",
        {"fleet_comms": fleet_comms},
    )


@login_required
@permission_required("fleetpings.basic_access")
def ajax_get_fleet_doctrines(request: WSGIRequest) -> HttpResponse:
    """
    Get fleet doctrines for the current user
    :param request:
    :return:
    """

    logger.info(f"Getting ffleet doctrines for user {request.user}")

    use_fleet_doctrines = False
    if (
        fittings_installed() is True
        and AA_FLEETPINGS_USE_DOCTRINES_FROM_FITTINGS_MODULE is True
    ):
        use_fleet_doctrines = True

    # Get doctrines
    if use_fleet_doctrines is True:
        groups = request.user.groups.all()
        doctrines = _get_docs_qs(request, groups).order_by("name")
    else:
        doctrines = (
            FleetDoctrine.objects.filter(
                Q(restricted_to_group__in=request.user.groups.all())
                | Q(restricted_to_group__isnull=True),
                is_enabled=True,
            )
            .distinct()
            .order_by("name")
        )

    return render(
        request,
        "fleetpings/form/fleetDoctrine.html",
        {"doctrines": doctrines, "use_fleet_doctrines": use_fleet_doctrines},
    )


# @login_required
# @permission_required("fleetpings.basic_access")
# def ajax_create_optimer(request: WSGIRequest) -> JsonResponse:
#     """
#     Adding the planned fleet to the optimers
#     :param request:
#     :return:
#     """
#
#     post_time = timezone.now()
#     character = request.user.profile.main_character
#
#     optimer = OpTimer()
#     optimer.doctrine = request.POST["fleet_doctrine"]
#     optimer.system = request.POST["formup_location"]
#     optimer.start = request.POST["formup_time"]
#     optimer.duration = "-"
#     optimer.operation_name = request.POST["fleet_name"]
#     optimer.fc = request.POST["fleet_commander"]
#     optimer.post_time = post_time
#     optimer.eve_character = character
#     optimer.save()
#
#     logger.info(f"Optimer created by user {request.user}")
#
#     return JsonResponse([True], safe=False)


# @login_required
# @permission_required("fleetpings.basic_access")
# def ajax_create_srp_link(request: WSGIRequest) -> JsonResponse:
#     """
#     Create an SRP link on fleetping with formup === now and SRP === yes
#     :param request:
#     """
#
#     post_time = timezone.now()
#     creator = request.user.profile.main_character
#
#     # Create aasrp link
#     if srp_module_is("aasrp") and can_add_srp_links(
#         request=request, module_name="aasrp"
#     ):
#         # Third Party
#         from aasrp.models import AaSrpLink
#
#         # Django
#         from django.utils.crypto import get_random_string
#
#         srp_code = get_random_string(length=16)
#
#         srp_link = AaSrpLink()
#         srp_link.srp_name = request.POST["fleet_name"]
#         srp_link.fleet_time = post_time
#         srp_link.fleet_doctrine = request.POST["fleet_doctrine"]
#         srp_link.srp_code = srp_code
#         srp_link.fleet_commander = creator
#         srp_link.creator = request.user
#         srp_link.save()
#
#     # Create allianceauth.srp link
#     if srp_module_is("allianceauth.srp") and can_add_srp_links(
#         request=request, module_name="allianceauth.srp"
#     ):
#         # Alliance Auth
#         from allianceauth.srp.models import SrpFleetMain
#         from allianceauth.srp.views import random_string
#
#         srp_code = random_string(8)
#
#         srp_fleet = SrpFleetMain()
#         srp_fleet.fleet_name = request.POST["fleet_name"]
#         srp_fleet.fleet_doctrine = request.POST["fleet_doctrine"]
#         srp_fleet.fleet_time = post_time
#         srp_fleet.fleet_srp_code = srp_code
#         srp_fleet.fleet_commander = creator
#         srp_fleet.save()
#
#     logger.info(f"SRP Link created by user {request.user}")
#
#     return JsonResponse({"success": True, "srp_code": srp_code}, safe=False)


@login_required
@permission_required("fleetpings.basic_access")
def ajax_create_fleet_ping(request: WSGIRequest) -> JsonResponse:
    """
    Create the fleet ping
    :param request:
    :return:
    """

    # default_embed_color = "#FAA61A"

    if request.method == "POST":
        logger.info("Fleet ping information received")

    logger.info(f"Fleet ping created by user {request.user}")

    return JsonResponse({"success": True, "ping_text": ""}, safe=False)
