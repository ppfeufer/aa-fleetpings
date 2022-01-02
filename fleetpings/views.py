"""
the views
"""

# Django
from django.contrib.auth.decorators import login_required, permission_required
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils import timezone

# Alliance Auth (External Libs)
from app_utils.urls import site_absolute_url

# AA Fleet Pings
from fleetpings import __title__
from fleetpings.app_settings import (
    AA_FLEETPINGS_USE_DOCTRINES_FROM_FITTINGS_MODULE,
    AA_FLEETPINGS_USE_SLACK,
    can_add_srp_links,
    fittings_installed,
    optimer_installed,
    srp_module_installed,
    srp_module_is,
    timezones_installed,
    use_new_timezone_links,
)
from fleetpings.models import (
    DiscordPingTargets,
    FleetComm,
    FleetDoctrine,
    FleetType,
    FormupLocation,
    Webhook,
)

if (
    fittings_installed() is True
    and AA_FLEETPINGS_USE_DOCTRINES_FROM_FITTINGS_MODULE is True
):
    # Third Party
    from fittings.views import _get_docs_qs

if optimer_installed():
    # Alliance Auth
    from allianceauth.optimer.models import OpTimer


@login_required
@permission_required("fleetpings.basic_access")
def index(request: WSGIRequest) -> HttpResponse:
    """
    Index view
    """
    fleet_comms = FleetComm.objects.filter(is_enabled=True).order_by("name")

    # which platform for pings we are using?
    platform_used = "Discord"
    if AA_FLEETPINGS_USE_SLACK is True:
        platform_used = "Slack"

    # do we use the doctrines from the fittings module, or our own defined?
    use_fleet_doctrines = False
    if (
        fittings_installed() is True
        and AA_FLEETPINGS_USE_DOCTRINES_FROM_FITTINGS_MODULE is True
    ):
        use_fleet_doctrines = True

    # get the webhooks for the used platform
    webhooks = (
        Webhook.objects.filter(
            Q(restricted_to_group__in=request.user.groups.all())
            | Q(restricted_to_group__isnull=True),
            type=platform_used,
            is_enabled=True,
        )
        .distinct()
        .order_by("name")
    )

    # get additional ping targets for discord
    additional_discord_ping_targets = {}
    if AA_FLEETPINGS_USE_SLACK is False:
        additional_discord_ping_targets = (
            DiscordPingTargets.objects.filter(
                Q(restricted_to_group__in=request.user.groups.all())
                | Q(restricted_to_group__isnull=True),
                is_enabled=True,
            )
            .distinct()
            .order_by("name")
        )

    # get fleet types
    fleet_types = (
        FleetType.objects.filter(
            Q(restricted_to_group__in=request.user.groups.all())
            | Q(restricted_to_group__isnull=True),
            is_enabled=True,
        )
        .distinct()
        .order_by("name")
    )

    # get doctrines
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

    # get formup locations
    formup_locations = FormupLocation.objects.filter(is_enabled=True).order_by("name")

    # srp_code = None
    srp_module_available_to_user = False
    if srp_module_installed() and (
        can_add_srp_links(request=request, module_name="aasrp")
        or can_add_srp_links(request=request, module_name="allianceauth.srp")
    ):
        srp_module_available_to_user = True

    context = {
        "title": __title__,
        "additional_discord_ping_targets": additional_discord_ping_targets,
        "additional_fleet_types": fleet_types,
        "additional_ping_webhooks": webhooks,
        "fleet_comms": fleet_comms,
        "fleet_doctrines": doctrines,
        "fleet_formup_locations": formup_locations,
        "site_url": site_absolute_url(),
        "timezones_installed": timezones_installed(),
        "optimer_installed": optimer_installed(),
        "use_new_timezone_links": use_new_timezone_links(),
        "fittings_installed": fittings_installed(),
        "main_character": request.user.profile.main_character,
        "platform_used": platform_used,
        "use_fleet_doctrines": use_fleet_doctrines,
        "srp_module_available_to_user": srp_module_available_to_user,
    }

    return render(request, "fleetpings/index.html", context)


@login_required
@permission_required("fleetpings.basic_access")
def ajax_create_optimer(request: WSGIRequest) -> JsonResponse:
    """
    adding the planned fleet to the optimers
    :param request:
    :return:
    """

    post_time = timezone.now()
    character = request.user.profile.main_character

    optimer = OpTimer()
    optimer.doctrine = request.POST["fleet_doctrine"]
    optimer.system = request.POST["formup_location"]
    optimer.start = request.POST["formup_time"]
    optimer.duration = "-"
    optimer.operation_name = request.POST["fleet_name"]
    optimer.fc = request.POST["fleet_commander"]
    optimer.post_time = post_time
    optimer.eve_character = character
    optimer.save()

    return JsonResponse([True], safe=False)


@login_required
@permission_required("fleetpings.basic_access")
def ajax_create_srp_link(request: WSGIRequest) -> JsonResponse:
    """
    create a SRP link on fleetping with formup === now and SRP === yes
    :param request:
    """

    post_time = timezone.now()
    creator = request.user.profile.main_character

    # create aasrp link
    if srp_module_is("aasrp") and can_add_srp_links(
        request=request, module_name="aasrp"
    ):
        # Third Party
        from aasrp.models import AaSrpLink

        # Django
        from django.utils.crypto import get_random_string

        srp_code = get_random_string(length=16)

        srp_link = AaSrpLink()
        srp_link.srp_name = request.POST["fleet_name"]
        srp_link.fleet_time = post_time
        srp_link.fleet_doctrine = request.POST["fleet_doctrine"]
        srp_link.srp_code = srp_code
        srp_link.fleet_commander = creator
        srp_link.creator = request.user
        srp_link.save()

    # create allianceauth.srp link
    if srp_module_is("allianceauth.srp") and can_add_srp_links(
        request=request, module_name="allianceauth.srp"
    ):
        # Alliance Auth
        from allianceauth.srp.models import SrpFleetMain
        from allianceauth.srp.views import random_string

        srp_code = random_string(8)

        srp_fleet = SrpFleetMain()
        srp_fleet.fleet_name = request.POST["fleet_name"]
        srp_fleet.fleet_doctrine = request.POST["fleet_doctrine"]
        srp_fleet.fleet_time = post_time
        srp_fleet.fleet_srp_code = srp_code
        srp_fleet.fleet_commander = creator
        srp_fleet.save()

    return JsonResponse({"success": True, "srp_code": srp_code}, safe=False)
