"""
The views
"""

# pylint: disable=import-outside-toplevel

# Standard Library
import json

# Django
from django.contrib.auth.decorators import login_required, permission_required
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# Alliance Auth
from allianceauth.services.hooks import get_extension_logger

# Alliance Auth (External Libs)
from app_utils.logging import LoggerAddTag
from app_utils.urls import reverse_absolute, site_absolute_url

# AA Fleet Pings
from fleetpings import __title__
from fleetpings.app_settings import (
    can_add_srp_links,
    fittings_installed,
    optimer_installed,
    srp_module_installed,
    srp_module_is,
    use_fittings_module_for_doctrines,
)
from fleetpings.form import FleetPingForm
from fleetpings.helper.discord_webhook import ping_discord_webhook
from fleetpings.helper.ping_context import get_ping_context_from_form_data
from fleetpings.models import (
    DiscordPingTarget,
    FleetComm,
    FleetDoctrine,
    FleetType,
    FormupLocation,
    Setting,
    Webhook,
)

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
        DiscordPingTarget.objects.filter(
            Q(restricted_to_group__in=request.user.groups.all())
            | Q(restricted_to_group__isnull=True),
            is_enabled=True,
        )
        .distinct()
        .order_by("name")
    )

    return render(
        request,
        "fleetpings/partials/form/segments/ping-targets.html",
        {
            "ping_targets": additional_discord_ping_targets,
            "use_default_ping_targets": Setting.objects.get_setting(
                Setting.Field.USE_DEFAULT_PING_TARGETS
            ),
        },
    )


@login_required
@permission_required("fleetpings.basic_access")
def ajax_get_webhooks(request: WSGIRequest) -> HttpResponse:
    """
    Get webhooks for current user
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
        .order_by("name")
    )

    return render(
        request,
        "fleetpings/partials/form/segments/ping-channel.html",
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
        "fleetpings/partials/form/segments/fleet-type.html",
        {
            "fleet_types": fleet_types,
            "use_default_fleet_types": Setting.objects.get_setting(
                Setting.Field.USE_DEFAULT_FLEET_TYPES
            ),
        },
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
        "fleetpings/partials/form/segments/fleet-formup-location.html",
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
        "fleetpings/partials/form/segments/fleet-comms.html",
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

    logger.info(f"Getting fleet doctrines for user {request.user}")

    # Get doctrines
    if use_fittings_module_for_doctrines() is True:
        # Third Party
        from fittings.views import _get_docs_qs

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
        "fleetpings/partials/form/segments/fleet-doctrine.html",
        {
            "doctrines": doctrines,
            "use_fleet_doctrines": use_fittings_module_for_doctrines(),
        },
    )


@login_required
@permission_required("fleetpings.basic_access")
def _create_optimer(request: WSGIRequest, ping_context: dict):
    """
    Adding the planned fleet to the optimers
    :param request:
    :param ping_context:
    :return:
    """

    # Alliance Auth
    from allianceauth.optimer.models import OpTimer

    post_time = timezone.now()
    character = request.user.profile.main_character

    OpTimer(
        doctrine=ping_context["doctrine"]["name"],
        system=ping_context["formup_location"],
        start=ping_context["formup_time"]["datetime_string"],
        duration="N/A",
        operation_name=ping_context["fleet_name"],
        fc=ping_context["fleet_commander"],
        post_time=post_time,
        eve_character=character,
    ).save()

    logger.info(f"Optimer created by user {request.user}")


@login_required
@permission_required("fleetpings.basic_access")
def _create_aasrp_link(request: WSGIRequest, ping_context: dict) -> dict:
    """
    Create an SRP link in AA-SRP
    :param request:
    :param ping_context:
    :return:
    """

    # Third Party
    from aasrp.models import SrpLink

    # Django
    from django.utils.crypto import get_random_string

    post_time = timezone.now()
    creator = request.user.profile.main_character
    srp_code = get_random_string(length=16)

    SrpLink(
        srp_name=ping_context["fleet_name"],
        fleet_time=post_time,
        fleet_doctrine=ping_context["doctrine"]["name"],
        srp_code=srp_code,
        fleet_commander=creator,
        creator=request.user,
    ).save()

    logger.info(f"SRP Link created by user {request.user}")

    return {
        "success": True,
        "code": srp_code,
        "link": reverse_absolute("aasrp:request_srp", [srp_code]),
    }


@login_required
@permission_required("fleetpings.basic_access")
def _create_allianceauth_srp_link(request: WSGIRequest, ping_context: dict) -> dict:
    """
    Create an SRP link in Alliance Auth SRP
    :param request:
    :param ping_context:
    :return:
    """

    # Alliance Auth
    from allianceauth.srp.models import SrpFleetMain
    from allianceauth.srp.views import random_string

    post_time = timezone.now()
    creator = request.user.profile.main_character
    srp_code = random_string(8)

    SrpFleetMain(
        fleet_name=ping_context["fleet_name"],
        fleet_doctrine=ping_context["doctrine"]["name"],
        fleet_time=post_time,
        fleet_srp_code=srp_code,
        fleet_commander=creator,
    ).save()

    logger.info(f"SRP Link created by user {request.user}")

    return {
        "success": True,
        "code": srp_code,
        "link": reverse_absolute("srp:request", [srp_code]),
    }


@login_required
@permission_required("fleetpings.basic_access")
def _create_srp_link(request: WSGIRequest, ping_context: dict) -> dict:
    """
    Create an SRP link on fleetping with formup === now and SRP === yes
    :param request:
    :param ping_context:
    :return:
    """

    if ping_context["fleet_name"] and ping_context["doctrine"]["name"]:
        # Create aasrp link (prioritized app)
        if srp_module_is("aasrp") and can_add_srp_links(
            request=request, module_name="aasrp"
        ):
            aasrp_info = _create_aasrp_link(request=request, ping_context=ping_context)

            return aasrp_info

        # Create allianceauth.srp link
        if srp_module_is("allianceauth.srp") and can_add_srp_links(
            request=request, module_name="allianceauth.srp"
        ):
            allianceauth_srp_info = _create_allianceauth_srp_link(
                request=request, ping_context=ping_context
            )

            return allianceauth_srp_info

    return {
        "success": False,
        "message": _("Not all mandatory information available to create an SRP link."),
    }


@login_required
@permission_required("fleetpings.basic_access")
def ajax_create_fleet_ping(request: WSGIRequest) -> HttpResponse:
    """
    Create the fleet ping
    :param request:
    :return:
    """

    context = {}
    success = False

    if request.method == "POST":
        form = FleetPingForm(request.POST)

        if form.is_valid():
            logger.info("Fleet ping information received")

            # Get ping context
            ping_context = get_ping_context_from_form_data(form_data=form.cleaned_data)

            # Create optimer is requested
            if optimer_installed() and ping_context["create_optimer"]:
                _create_optimer(
                    request=request,
                    ping_context=ping_context,
                )

                context["message"] = str(_("Fleet operations timer has been created …"))

            # Create an SRP link if requested
            if srp_module_installed() and ping_context["srp"]["create_srp_link"]:
                ping_context["srp"]["link"] = _create_srp_link(
                    request=request,
                    ping_context=ping_context,
                )

                context["message"] = str(_("SRP link has been created …"))

            # If we have a Discord webhook, ping it
            if ping_context["ping_channel"]["webhook"]:
                ping_discord_webhook(ping_context=ping_context, user=request.user)

            logger.info(f"Fleet ping created by user {request.user}")

            ping_context["request"] = request

            context["ping_context"] = render_to_string(
                template_name="fleetpings/partials/ping/copy-paste-text.html",
                context=ping_context,
                request=request,
            )
            success = True
        else:
            context["message"] = str(_("Form invalid. Please check your input."))
    else:
        context["message"] = str(_("No form data submitted."))

    context["success"] = success

    return HttpResponse(json.dumps(context), content_type="application/json")
