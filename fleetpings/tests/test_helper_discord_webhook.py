# Standard Library
from unittest.mock import Mock, patch

# AA Fleet Pings
from fleetpings import __app_name_useragent__, __github_url__, __version__
from fleetpings.helper.discord_webhook import get_user_agent, ping_discord_webhook
from fleetpings.tests import BaseTestCase


class TestGetUserAgent(BaseTestCase):
    """
    Test the get_user_agent function
    """

    def test_returns_correct_user_agent_with_valid_inputs(self):
        """
        Test that get_user_agent returns the correct UserAgent object when valid inputs are provided.

        :return:
        :rtype:
        """

        user_agent = get_user_agent()

        self.assertEqual(user_agent.name, __app_name_useragent__)
        self.assertEqual(user_agent.url, __github_url__)
        self.assertEqual(user_agent.version, __version__)


class TestPingDiscordWebhook(BaseTestCase):
    def test_sends_ping_with_valid_context_and_user(self):
        """
        Test that ping_discord_webhook sends a ping successfully when provided with valid context and user.

        :return:
        :rtype:
        """

        ping_context = {
            "ping_channel": {
                "webhook": "https://discord.com/api/webhooks/12345",
                "embed_color": "#FF5733",
            },
            "ping_target": {
                "group_id": 1,
                "group_name": "Test Group",
                "at_mention": "@Test Group",
            },
            "is_pre_ping": False,
            "fleet_type": "PvP",
            "fleet_commander": "John Doe",
            "fleet_name": "Alpha Fleet",
            "formup_location": "Jita",
            "is_formup_now": True,
            "formup_time": {
                "datetime_string": "2023-10-01 18:00",
                "timestamp": "1696173600",
            },
            "fleet_duration": "2 hours",
            "fleet_comms": "Discord",
            "doctrine": {"name": "Shield Doctrine", "link": "http://example.com"},
            "srp": {"has_srp": True, "create_srp_link": False},
            "additional_information": "Bring ammo",
        }

        user = Mock()
        user.profile.main_character.character_name = "Test Character"
        user.profile.main_character = Mock()
        user.profile.main_character.character_name = "Test Character"
        user.profile.main_character.character_id = 123456

        with (
            patch("fleetpings.helper.discord_webhook.Webhook.execute") as mock_execute,
            patch(
                "fleetpings.helper.discord_webhook.get_character_portrait_from_evecharacter",
                return_value="http://example.com/avatar.png",
            ),
        ):
            ping_discord_webhook(ping_context, user)
            mock_execute.assert_called_once()

    def test_raises_error_when_webhook_url_is_missing(self):
        """
        Test that ping_discord_webhook raises an error when the webhook URL is missing.

        :return:
        :rtype:
        """

        ping_context = {
            "ping_channel": {"webhook": None, "embed_color": "#FF5733"},
            "ping_target": {
                "group_id": 1,
                "group_name": "Test Group",
                "at_mention": "@Test Group",
            },
        }

        user = Mock()

        with self.assertRaises(KeyError):
            ping_discord_webhook(ping_context, user)
