"""
The views
"""

# Django
from django.contrib.auth.decorators import login_required, permission_required
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
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
    AA_FLEETPINGS_USE_DOCTRINES_FROM_FITTINGS_MODULE,
    can_add_srp_links,
    fittings_installed,
    optimer_installed,
    srp_module_installed,
    srp_module_is,
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

if (
    fittings_installed() is True
    and AA_FLEETPINGS_USE_DOCTRINES_FROM_FITTINGS_MODULE is True
):
    # Third Party
    from fittings.views import _get_docs_qs


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
    :param srp_data:
    :return:
    """

    # Third Party
    from aasrp.models import AaSrpLink

    # Django
    from django.utils.crypto import get_random_string

    post_time = timezone.now()
    creator = request.user.profile.main_character
    srp_code = get_random_string(length=16)

    AaSrpLink(
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


def _get_at_mention_from_ping_target(ping_target: str) -> str:
    """
    Returning the @-mention for a ping target
    :param ping_target:
    :return:
    """

    return (
        str(ping_target) if str(ping_target).startswith("@") else "@" + str(ping_target)
    )


def _get_ping_context_from_form_data(form_data: dict) -> dict:
    """
    Getting ping context from form data
    :param form_data:
    :return:
    """

    ping_target_group_id = None
    ping_target_group_name = None
    ping_target_at_mention = None

    if form_data["ping_target"]:
        if (
            form_data["ping_target"] == "@here"
            or form_data["ping_target"] == "@everyone"
        ):
            ping_target_at_mention = _get_at_mention_from_ping_target(
                form_data["ping_target"]
            )
        else:
            try:
                # Check if we deal with a custom ping target
                ping_target = DiscordPingTargets.objects.get(
                    discord_id=form_data["ping_target"]
                )
            except DiscordPingTargets.DoesNotExist:
                pass
            else:
                # We deal with a custom ping target, gather the information we need
                ping_target_group_id = int(ping_target.discord_id)
                ping_target_group_name = str(ping_target.name)
                ping_target_at_mention = _get_at_mention_from_ping_target(
                    ping_target.name
                )

    # Check for webhooks
    ping_channel_type = None
    ping_channel_webhook = None

    if form_data["ping_channel"]:
        try:
            ping_channel = Webhook.objects.get(pk=form_data["ping_channel"])
        except Webhook.DoesNotExist:
            pass
        else:
            ping_channel_type = ping_channel.type
            ping_channel_webhook = ping_channel.url

    ping_context = {
        "ping_target": {
            "group_id": int(ping_target_group_id) if ping_target_group_id else None,
            "group_name": str(ping_target_group_name),
            "at_mention": ping_target_at_mention,
        },
        "ping_channel": {
            "type": str(ping_channel_type),
            "webhook": str(ping_channel_webhook),
        },
        "fleet_type": str(form_data["fleet_type"]),
        "fleet_commander": str(form_data["fleet_commander"]),
        "fleet_name": str(form_data["fleet_name"]),
        "formup_location": str(form_data["formup_location"]),
        "is_pre_ping": bool(form_data["pre_ping"]),
        "is_formup_now": bool(form_data["formup_now"]),
        "formup_time": {
            "datetime_string": str(form_data["formup_time"]),
            "timestamp": str(form_data["formup_timestamp"]),
        },
        "fleet_comms": str(form_data["fleet_comms"]),
        "doctrine": {
            "name": str(form_data["fleet_doctrine"]),
            "link": str(form_data["fleet_doctrine_url"]),
        },
        "srp": {
            "has_srp": bool(form_data["srp"]),
            "create_srp_link": str(form_data["srp_link"]),
        },
        "create_optimer": bool(form_data["optimer"]),
        "additional_information": str(form_data["additional_information"]),
    }

    return ping_context


def _get_ping_text(context: dict) -> dict:
    """
    Getting the ping text
    :param context:
    :return:
    """

    webhook_ping_text_header = ""
    webhook_ping_text_content = ""
    webhook_ping_text_footer = ""
    webhook_ping_target = ""
    discord_ping_target = ""
    ping_text = ""

    # Ping target
    if context["ping_target"]["at_mention"]:
        ping_text = " :: "
        webhook_ping_target = context["ping_target"]["at_mention"]
        discord_ping_target = context["ping_target"]["at_mention"]

    # Fleet Announcement
    ping_text += "**"

    # Check if it's a pre-ping or not
    if context["is_pre_ping"]:
        ping_text += "### PRE PING ###"
        webhook_ping_text_header += "### PRE PING ###"

        if context["fleet_type"]:
            ping_text += f' / (Upcoming) {context["fleet_type"]} Fleet'
            webhook_ping_text_header += f' / (Upcoming) {context["fleet_type"]} Fleet'
    else:
        if context["fleet_type"]:
            ping_text += f'{context["fleet_type"]} '
            webhook_ping_text_header += f'{context["fleet_type"]} '

        ping_text += "Fleet is up"
        webhook_ping_text_header += "Fleet is up"

        # Add fcName if we have one
        if context["fleet_commander"]:
            ping_text += f' under {context["fleet_commander"]}'
            webhook_ping_text_header += f' under {context["fleet_commander"]}'

    ping_text += "**\n"

    # Add FC name if we have one
    if context["fleet_commander"]:
        ping_text += f'\n**FC:** {context["fleet_commander"]}'
        webhook_ping_text_content += f'\n**FC:** {context["fleet_commander"]}'

    # Check if fleet name is available
    if context["fleet_name"]:
        ping_text += f'\n**Fleet Name:** {context["fleet_name"]}'
        webhook_ping_text_content += f'\n**Fleet Name:** {context["fleet_name"]}'

    # Check if form-up location is available
    if context["formup_location"]:
        ping_text += f'\n**Formup Location:** {context["formup_location"]}'
        webhook_ping_text_content += (
            f'\n**Formup Location:** {context["formup_location"]}'
        )

    # Check if form-up time is available
    if context["is_formup_now"]:
        ping_text += "\n**Formup Time:** NOW"
        webhook_ping_text_content += "\n**Formup Time:** NOW"
    else:
        if context["formup_time"]["datetime_string"]:
            ping_text += (
                f'\n**Formup (EVE Time):** {context["formup_time"]["datetime_string"]}'
            )
            webhook_ping_text_content += (
                f'\n**Formup (EVE Time):** {context["formup_time"]["datetime_string"]}'
            )

        if context["formup_time"]["timestamp"]:
            if timezones_installed():
                # Add timezones conversion to ping text
                timezones_url = reverse_absolute(
                    "timezones:index",
                    args=[context["formup_time"]["timestamp"]],
                )
                ping_text += f" - {timezones_url}"
                webhook_ping_text_content += (
                    f" ([Time Zone Conversion]({timezones_url}))"
                )

            # Add local time
            ping_text += (
                "\n**Formup (Local Time):** "
                f'&lt;t:{context["formup_time"]["timestamp"]}:F&gt;'
            )
            webhook_ping_text_content += (
                "\n**Formup (Local Time):** "
                f'<t:{context["formup_time"]["timestamp"]}:F>'
            )
    # Check if fleet comms is available
    if context["fleet_comms"]:
        ping_text += f'\n**Comms:** {context["fleet_comms"]}'
        webhook_ping_text_content += f'\n**Comms:** {context["fleet_comms"]}'

    # Check if doctrine is available
    if context["doctrine"]["name"]:
        ping_text += f'\n**Ships / Doctrine:** {context["doctrine"]["name"]}'
        webhook_ping_text_content += (
            f'\n**Ships / Doctrine:** {context["doctrine"]["name"]}'
        )

        # Grab the doctrine link if there is one
        if context["doctrine"]["link"]:
            ping_text += f' - {context["doctrine"]["link"]}'
            webhook_ping_text_content += (
                f' ([Doctrine Link]({context["doctrine"]["link"]}))'
            )

    # Check if srp is available
    if context["srp"]["has_srp"]:
        ping_text += "\n**SRP:** Yes"
        webhook_ping_text_content += "\n**SRP:** Yes"

        # Check if we have an SRP link
        # if context["srp"]["link"]:
        #     ping_text += f' (SRP Link: {context["srp"]["link"]})'
        #     webhook_ping_text_content += f' (SRP Link: {context["srp"]["link"]})'

    # Check if additional information is available
    if context["additional_information"]:
        ping_text += (
            f'\n\n**Additional Information**:\n{context["additional_information"]}'
        )
        webhook_ping_text_content += (
            f'\n\n**Additional Information**:\n{context["additional_information"]}'
        )

    return {
        "ping_text": ping_text,
        "ping_target": discord_ping_target,
        "webhook": {
            "target": webhook_ping_target,
            "header": webhook_ping_text_header,
            "content": webhook_ping_text_content,
            "footer": webhook_ping_text_footer,
        },
    }


@login_required
@permission_required("fleetpings.basic_access")
def ajax_create_fleet_ping(request: WSGIRequest) -> JsonResponse:
    """
    Create the fleet ping
    :param request:
    :return:
    """

    success = False
    context = {}

    if request.method == "POST":
        form = FleetPingForm(request.POST)

        if form.is_valid():
            logger.info("Fleet ping information received")

            # Get ping context
            ping_context = _get_ping_context_from_form_data(form_data=form.cleaned_data)

            # Get ping text
            context["ping_text"] = _get_ping_text(context=ping_context)

            # Just for Debug for the time being ...
            context["ping_context"] = ping_context

            # Create optimer is requested
            if optimer_installed() and ping_context["create_optimer"]:
                _create_optimer(
                    request=request,
                    ping_context=ping_context,
                )

            # Create SRP link if requested
            if srp_module_installed() and ping_context["srp"]["create_srp_link"]:
                context["srp"] = _create_srp_link(
                    request=request,
                    ping_context=ping_context,
                )

            logger.info(f"Fleet ping created by user {request.user}")

            success = True

            return JsonResponse(
                {"success": success, "context": context["ping_text"]}, safe=False
            )

        return JsonResponse(
            {
                "success": success,
                "context": {"message": _("Form not valid. Please check.")},
            },
            safe=False,
        )

    return JsonResponse(
        {"success": success, "context": {"message": _("No form submitted")}}, safe=False
    )
