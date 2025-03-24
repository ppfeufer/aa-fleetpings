"""
Handling ping context data
"""

# Alliance Auth (External Libs)
from app_utils.urls import reverse_absolute

# AA Fleet Pings
from fleetpings.app_settings import (
    fittings_installed,
    optimer_installed,
    timezones_installed,
)
from fleetpings.models import DiscordPingTarget, Setting, Webhook


def get_ping_context_from_form_data(form_data: dict) -> dict:
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
            ping_target_at_mention = str(form_data["ping_target"])
        else:
            try:
                # Check if we deal with a custom ping target
                ping_target = (
                    DiscordPingTarget.objects.get(  # pylint: disable=no-member
                        discord_id=form_data["ping_target"]
                    )
                )
            except DiscordPingTarget.DoesNotExist:  # pylint: disable=no-member
                pass
            else:
                # We deal with a custom ping target, gather the information we need
                ping_target_group_id = int(ping_target.discord_id)
                ping_target_group_name = str(ping_target.name)
                ping_target_at_mention = (
                    str(ping_target.name)
                    if str(ping_target.name).startswith("@")
                    else f"@{ping_target.name}"
                )

    # Check for webhooks
    ping_channel_webhook = None
    ping_channel_webhook_embed_color = Setting.objects.get_setting(
        Setting.Field.DEFAULT_EMBED_COLOR
    )

    if form_data["ping_channel"]:
        try:
            ping_channel = Webhook.objects.get(  # pylint: disable=no-member
                pk=form_data["ping_channel"]
            )
        except Webhook.DoesNotExist:  # pylint: disable=no-member
            pass
        else:
            ping_channel_webhook = ping_channel.url

    if form_data["webhook_embed_color"]:
        ping_channel_webhook_embed_color = form_data["webhook_embed_color"]

    ping_context = {
        "ping_target": {
            "group_id": int(ping_target_group_id) if ping_target_group_id else None,
            "group_name": str(ping_target_group_name),
            "at_mention": str(ping_target_at_mention) if ping_target_at_mention else "",
        },
        "ping_channel": {
            "webhook": ping_channel_webhook,
            "embed_color": ping_channel_webhook_embed_color,
        },
        "fleet_type": str(form_data["fleet_type"]),
        "fleet_commander": str(form_data["fleet_commander"]),
        "fleet_name": str(form_data["fleet_name"]),
        "fleet_duration": str(form_data["fleet_duration"]),
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
            "create_srp_link": bool(form_data["srp_link"]),
        },
        "create_optimer": bool(form_data["optimer"]),
        "additional_information": str(form_data["additional_information"]),
        "timezones_installed": timezones_installed(),
        "optimer_installed": optimer_installed(),
        "fittings_installed": fittings_installed(),
    }

    return ping_context


# pylint: disable=too-many-statements too-many-branches
def _get_webhook_ping_context(ping_context: dict) -> dict:
    """
    Getting the webhook ping context
    :param ping_context:
    :return:
    """

    webhook_ping_text_header = ""
    webhook_ping_text_content = ""
    webhook_ping_text_footer = ""
    webhook_ping_target = ""

    # Ping target
    if ping_context["ping_target"]["group_id"]:
        ping_target_at_mention = f'<@&{ping_context["ping_target"]["group_id"]}>'
    else:
        ping_target_at_mention = str(ping_context["ping_target"]["at_mention"])

    if ping_target_at_mention != "":
        webhook_ping_text_header += ping_target_at_mention
        webhook_ping_text_header += " :: "

    webhook_ping_text_header += "**"

    # Check if it's a pre-ping or not
    if ping_context["is_pre_ping"]:
        webhook_ping_text_header += r"\### PRE PING ###"

        if ping_context["fleet_type"]:
            webhook_ping_text_header += (
                f' / (Upcoming) {ping_context["fleet_type"]} Fleet'
            )
    else:
        if ping_context["fleet_type"]:
            webhook_ping_text_header += f'{ping_context["fleet_type"]} '

        webhook_ping_text_header += "Fleet is up"

        # Add FC name if we have one
        if ping_context["fleet_commander"]:
            webhook_ping_text_header += f' under {ping_context["fleet_commander"]}'

    webhook_ping_text_header += "**\n** **"

    # Add FC name if we have one
    if ping_context["fleet_commander"]:
        webhook_ping_text_content += f'\n**FC:** {ping_context["fleet_commander"]}'

    # Check if fleet name is available
    if ping_context["fleet_name"]:
        webhook_ping_text_content += f'\n**Fleet Name:** {ping_context["fleet_name"]}'

    # Check if form-up location is available
    if ping_context["formup_location"]:
        webhook_ping_text_content += (
            f'\n**Formup Location:** {ping_context["formup_location"]}'
        )

    # Check if form-up time is available
    if ping_context["is_formup_now"]:
        webhook_ping_text_content += "\n**Formup Time:** NOW"
    else:
        if ping_context["formup_time"]["datetime_string"]:
            webhook_ping_text_content += (
                "\n**Formup (EVE time):** "
                f'{ping_context["formup_time"]["datetime_string"]}'
            )

        if ping_context["formup_time"]["timestamp"]:
            if timezones_installed():
                # Add timezones conversion to the ping text
                timezones_url = reverse_absolute(
                    "timezones:index",
                    args=[ping_context["formup_time"]["timestamp"]],
                )
                webhook_ping_text_content += (
                    f" ([Time Zone Conversion]({timezones_url}))"
                )

            # Add local time
            webhook_ping_text_content += (
                "\n**Formup (Local Time):** "
                f'<t:{ping_context["formup_time"]["timestamp"]}:F>'
                f' (<t:{ping_context["formup_time"]["timestamp"]}:R>)'
            )

    # Check if fleet duration is available
    if ping_context["fleet_duration"]:
        webhook_ping_text_content += (
            f'\n**Duration (approximately):** {ping_context["fleet_duration"]}'
        )

    # Check if fleet comms is available
    if ping_context["fleet_comms"]:
        webhook_ping_text_content += f'\n**Comms:** {ping_context["fleet_comms"]}'

    # Check if doctrine is available
    if ping_context["doctrine"]["name"]:
        webhook_ping_text_content += (
            f'\n**Ships / Doctrine:** {ping_context["doctrine"]["name"]}'
        )

        # Grab the doctrine link if there is one
        if ping_context["doctrine"]["link"]:
            webhook_ping_text_content += (
                f' ([Doctrine Link]({ping_context["doctrine"]["link"]}))'
            )

    # Check if srp is available
    if ping_context["srp"]["has_srp"]:
        webhook_ping_text_content += "\n**SRP:** Yes"

        # Check if we have an SRP link
        if ping_context["srp"]["create_srp_link"] and "link" in ping_context["srp"]:
            webhook_ping_text_content += (
                f' (SRP Code: [{ping_context["srp"]["link"]["code"]}]'
                f'({ping_context["srp"]["link"]["link"]}))'
            )

    # Check if additional information is available
    if ping_context["additional_information"]:
        webhook_ping_text_content += (
            f'\n\n**Additional Information**:\n{ping_context["additional_information"]}'
        )

    return {
        "target": webhook_ping_target,
        "header": webhook_ping_text_header,
        "content": webhook_ping_text_content,
        "footer": webhook_ping_text_footer,
    }
