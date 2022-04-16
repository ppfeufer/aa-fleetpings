"""
Handling ping context data
"""

# Alliance Auth (External Libs)
from app_utils.urls import reverse_absolute

# AA Fleet Pings
from fleetpings.app_settings import timezones_installed


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
    if ping_context["ping_target"]["at_mention"]:
        webhook_ping_text_header += ping_context["ping_target"]["at_mention"]
        webhook_ping_text_header += " :: "

    webhook_ping_text_header += "**"

    # Check if it's a pre-ping or not
    if ping_context["is_pre_ping"]:
        webhook_ping_text_header += "### PRE PING ###"

        if ping_context["fleet_type"]:
            webhook_ping_text_header += (
                f' / (Upcoming) {ping_context["fleet_type"]} Fleet'
            )
    else:
        if ping_context["fleet_type"]:
            webhook_ping_text_header += f'{ping_context["fleet_type"]} '

        webhook_ping_text_header += "Fleet is up"

        # Add fcName if we have one
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
            webhook_ping_text_content += f'\n**Formup (EVE Time):** {ping_context["formup_time"]["datetime_string"]}'

        if ping_context["formup_time"]["timestamp"]:
            if timezones_installed():
                # Add timezones conversion to ping text
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
