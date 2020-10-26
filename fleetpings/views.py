# -*- coding: utf-8 -*-

"""
the views
"""

from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone

from fleetpings import __title__
from fleetpings.app_settings import (
    AA_FLEETPINGS_USE_SLACK,
    AA_FLEETPINGS_USE_DOCTRINES_FROM_FITTINGS_MODULE,
    get_site_url,
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
def index(request):
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
        "mainCharacter": request.user.profile.main_character,
        "platformUsed": platform_used,
        "useFleetDoctrines": use_fleet_doctrines,
        "avoidCdn": avoid_cdn(),
    }

    return render(request, "fleetpings/index.html", context)


@login_required
@permission_required("fleetpings.basic_access")
def create_optimer_on_preping(request):
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
