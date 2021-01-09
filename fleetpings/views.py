# -*- coding: utf-8 -*-

"""
the views
"""

from django.contrib.auth.decorators import login_required, permission_required
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils import timezone

from fleetpings import __title__
from fleetpings.app_settings import (
    AA_FLEETPINGS_USE_SLACK,
    AA_FLEETPINGS_USE_DOCTRINES_FROM_FITTINGS_MODULE,
    srp_module_installed,
    get_site_url,
    srp_module_is,
    timezones_installed,
    optimer_installed,
    use_new_timezone_links,
    fittings_installed,
    avoid_cdn,
)
from fleetpings.models import (
    FleetComm,
    DiscordPingTargets,
    FleetType,
    Webhook,
    FleetDoctrine,
    FormupLocation,
)

if (
    fittings_installed() is True
    and AA_FLEETPINGS_USE_DOCTRINES_FROM_FITTINGS_MODULE is True
):
    from fittings.views import _get_docs_qs

if optimer_installed():
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

    srp_code = None
    if srp_module_installed():
        if srp_module_is("aasrp"):
            from django.utils.crypto import get_random_string

            srp_code = get_random_string(length=16)

        if srp_module_is("allianceauth.srp"):
            from allianceauth.srp.views import random_string

            srp_code = random_string(8)

    context = {
        "title": __title__,
        "additionalPingTargets": additional_discord_ping_targets,
        "additionalFleetTypes": fleet_types,
        "additionalPingWebhooks": webhooks,
        "fleetComms": fleet_comms,
        "fleetDoctrines": doctrines,
        "fleetFormupLocations": formup_locations,
        "site_url": get_site_url(),
        "timezones_installed": timezones_installed(),
        "optimer_installed": optimer_installed(),
        "use_new_timezone_links": use_new_timezone_links(),
        "fittings_installed": fittings_installed(),
        "main_character": request.user.profile.main_character,
        "platform_used": platform_used,
        "useFleetDoctrines": use_fleet_doctrines,
        "avoidCdn": avoid_cdn(),
        "srp_module_installed": srp_module_installed(),
        "srp_code": srp_code,
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

    # create allianceauth.srp link
    # if "allianceauth.srp" in settings.INSTALLED_APPS:
    if srp_module_is("allianceauth.srp"):
        from allianceauth.srp.models import SrpFleetMain

        # from allianceauth.srp.views import random_string

        srp_fleet = SrpFleetMain()
        srp_fleet.fleet_name = request.POST["fleet_name"]
        srp_fleet.fleet_doctrine = request.POST["fleet_doctrine"]
        srp_fleet.fleet_time = post_time
        srp_fleet.fleet_srp_code = request.POST["srp_code"]
        srp_fleet.fleet_commander = creator
        srp_fleet.save()

    # create aasrp link
    # if "aasrp" in settings.INSTALLED_APPS:
    if srp_module_is("aasrp"):
        from aasrp.models import AaSrpLink

        # from django.utils.crypto import get_random_string

        srp_link = AaSrpLink()
        srp_link.srp_name = request.POST["fleet_name"]
        srp_link.fleet_time = post_time
        srp_link.fleet_doctrine = request.POST["fleet_doctrine"]
        srp_link.srp_code = request.POST["srp_code"]
        srp_link.fleet_commander = creator
        srp_link.creator = request.user
        srp_link.save()

    return JsonResponse([True], safe=False)
