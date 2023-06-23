"""
Handling Discord webhooks
"""

# Third Party
from dhooks_lite import Embed, Footer, Webhook

# Django
from django.contrib.auth.models import User
from django.utils import timezone

# AA Fleet Pings
from fleetpings.helper.eve_images import get_character_portrait_from_evecharacter
from fleetpings.helper.ping_context import _get_webhook_ping_context


def ping_discord_webhook(ping_context: dict, user: User):
    """
    Ping a Discord webhook
    :param ping_context:
    :type ping_context:
    :param user:
    :type user:
    :return:
    :rtype:
    """

    webhook_ping_context = _get_webhook_ping_context(ping_context=ping_context)

    discord_webhook = Webhook(ping_context["ping_channel"]["webhook"])
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
        footer=Footer(f"Ping sent by: {author_eve_name}", author_eve_avatar),
    )

    discord_webhook.execute(
        webhook_ping_context["header"], embeds=[embed], wait_for_response=True
    )
