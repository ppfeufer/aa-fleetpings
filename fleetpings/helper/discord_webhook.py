"""
Handling Discord webhooks
"""

# Third Party
from dhooks_lite import Embed, Footer, UserAgent, Webhook

# Django
from django.contrib.auth.models import User
from django.utils import timezone

# AA Fleet Pings
from fleetpings import __version__
from fleetpings.constants import APP_NAME, GITHUB_URL
from fleetpings.helper.eve_images import get_character_portrait_from_evecharacter
from fleetpings.helper.ping_context import _get_webhook_ping_context


def get_user_agent() -> UserAgent:
    """
    Set the user agent

    :return: User agent
    :rtype: UserAgent
    """

    return UserAgent(APP_NAME, GITHUB_URL, __version__)


def ping_discord_webhook(ping_context: dict, user: User) -> None:
    """
    Sends a ping to a Discord webhook

    :param ping_context: The ping context
    :type ping_context: dict
    :param user: The user who sent the ping
    :type user: User
    :return:
    :rtype: None
    """

    webhook_ping_context = _get_webhook_ping_context(ping_context=ping_context)

    discord_webhook = Webhook(
        url=ping_context["ping_channel"]["webhook"], user_agent=get_user_agent()
    )
    message_to_send = webhook_ping_context["content"]
    embed_color = ping_context["ping_channel"]["embed_color"]
    author_eve_avatar = get_character_portrait_from_evecharacter(
        character=user.profile.main_character, size=256
    )
    author_eve_name = user.profile.main_character.character_name

    embed = Embed(
        description=message_to_send,
        title=".: Fleet Details :.",
        timestamp=timezone.now(),
        color=int(embed_color.lstrip("#"), 16),
        footer=Footer(
            text=f"Ping sent by: {author_eve_name}", icon_url=author_eve_avatar
        ),
    )

    discord_webhook.execute(
        content=webhook_ping_context["header"], embeds=[embed], wait_for_response=True
    )
