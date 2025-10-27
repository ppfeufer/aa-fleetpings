"""
Tests for the ping context helper functions.
"""

# Django
from django.contrib.auth.models import Group

# AA Fleet Pings
from fleetpings.helper.ping_context import (
    _get_webhook_ping_context,
    get_ping_context_from_form_data,
)
from fleetpings.models import DiscordPingTarget, Webhook
from fleetpings.tests import BaseTestCase


class TestGetPingContextFromFormData(BaseTestCase):
    """
    Test the get_ping_context_from_form_data function.
    """

    def test_returns_correct_ping_context_for_here_mention(self):
        """
        Test that the function returns the correct ping context for @here mention.

        :return:
        :rtype:
        """

        form_data = {
            "ping_target": "@here",
            "ping_channel": None,
            "webhook_embed_color": None,
            "fleet_type": "PvP",
            "fleet_commander": "John Doe",
            "fleet_name": "Alpha Fleet",
            "fleet_duration": "2 hours",
            "formup_location": "Jita",
            "pre_ping": False,
            "formup_now": True,
            "formup_time": "",
            "formup_timestamp": "",
            "fleet_comms": "Discord",
            "fleet_doctrine": "Shield Fleet",
            "fleet_doctrine_url": "http://example.com",
            "srp": True,
            "srp_link": False,
            "optimer": False,
            "additional_information": "Bring ammo",
        }

        result = get_ping_context_from_form_data(form_data)

        self.assertEqual(result["ping_target"]["at_mention"], "@here")

    def test_returns_correct_ping_context_for_custom_ping_target(self):
        """
        Test that the function returns the correct ping context for a custom ping target.

        :return:
        :rtype:
        """

        group = Group.objects.create(name="Custom Target")
        DiscordPingTarget.objects.bulk_create(
            [DiscordPingTarget(name=group, discord_id=12345)]
        )

        form_data = {
            "ping_target": "12345",
            "ping_channel": None,
            "webhook_embed_color": None,
            "fleet_type": "PvP",
            "fleet_commander": "John Doe",
            "fleet_name": "Alpha Fleet",
            "fleet_duration": "2 hours",
            "formup_location": "Jita",
            "pre_ping": False,
            "formup_now": True,
            "formup_time": "",
            "formup_timestamp": "",
            "fleet_comms": "Discord",
            "fleet_doctrine": "Shield Fleet",
            "fleet_doctrine_url": "http://example.com",
            "srp": True,
            "srp_link": False,
            "optimer": False,
            "additional_information": "Bring ammo",
        }

        result = get_ping_context_from_form_data(form_data)

        self.assertEqual(result["ping_target"]["group_id"], 12345)
        self.assertEqual(result["ping_target"]["group_name"], "Custom Target")
        self.assertEqual(result["ping_target"]["at_mention"], "@Custom Target")

    def test_handles_missing_ping_target_gracefully(self):
        """
        Test that the function handles missing ping target gracefully.

        :return:
        :rtype:
        """

        form_data = {
            "ping_target": None,
            "ping_channel": None,
            "webhook_embed_color": None,
            "fleet_type": "PvP",
            "fleet_commander": "John Doe",
            "fleet_name": "Alpha Fleet",
            "fleet_duration": "2 hours",
            "formup_location": "Jita",
            "pre_ping": False,
            "formup_now": True,
            "formup_time": "",
            "formup_timestamp": "",
            "fleet_comms": "Discord",
            "fleet_doctrine": "Shield Fleet",
            "fleet_doctrine_url": "http://example.com",
            "srp": True,
            "srp_link": False,
            "optimer": False,
            "additional_information": "Bring ammo",
        }

        result = get_ping_context_from_form_data(form_data)

        self.assertIsNone(result["ping_target"]["group_id"])
        self.assertEqual(result["ping_target"]["at_mention"], "")

    def test_returns_correct_webhook_url_and_embed_color(self):
        """
        Test that the function returns the correct webhook URL and embed color.

        :return:
        :rtype:
        """

        webhook = Webhook.objects.create(name="Test Webhook", url="http://webhook.url")
        form_data = {
            "ping_target": None,
            "ping_channel": webhook.pk,
            "webhook_embed_color": "#FF5733",
            "fleet_type": "PvP",
            "fleet_commander": "John Doe",
            "fleet_name": "Alpha Fleet",
            "fleet_duration": "2 hours",
            "formup_location": "Jita",
            "pre_ping": False,
            "formup_now": True,
            "formup_time": "",
            "formup_timestamp": "",
            "fleet_comms": "Discord",
            "fleet_doctrine": "Shield Fleet",
            "fleet_doctrine_url": "http://example.com",
            "srp": True,
            "srp_link": False,
            "optimer": False,
            "additional_information": "Bring ammo",
        }

        result = get_ping_context_from_form_data(form_data)

        self.assertEqual(result["ping_channel"]["webhook"], "http://webhook.url")
        self.assertEqual(result["ping_channel"]["embed_color"], "#FF5733")

    def test_handles_missing_webhook_gracefully(self):
        """
        Test that the function handles missing webhook gracefully.

        :return:
        :rtype:
        """

        form_data = {
            "ping_target": None,
            "ping_channel": 999999,
            "webhook_embed_color": None,
            "fleet_type": "PvP",
            "fleet_commander": "John Doe",
            "fleet_name": "Alpha Fleet",
            "fleet_duration": "2 hours",
            "formup_location": "Jita",
            "pre_ping": False,
            "formup_now": True,
            "formup_time": "",
            "formup_timestamp": "",
            "fleet_comms": "Discord",
            "fleet_doctrine": "Shield Fleet",
            "fleet_doctrine_url": "http://example.com",
            "srp": True,
            "srp_link": False,
            "optimer": False,
            "additional_information": "Bring ammo",
        }

        result = get_ping_context_from_form_data(form_data)

        self.assertIsNone(result["ping_channel"]["webhook"])

    def test_handles_nonexistent_ping_target_gracefully(self):
        """
        Test that the function handles nonexistent ping target gracefully.

        :return:
        :rtype:
        """

        form_data = {
            "ping_target": "99999",  # Nonexistent discord_id
            "ping_channel": None,
            "webhook_embed_color": None,
            "fleet_type": "PvP",
            "fleet_commander": "John Doe",
            "fleet_name": "Alpha Fleet",
            "fleet_duration": "2 hours",
            "formup_location": "Jita",
            "pre_ping": False,
            "formup_now": True,
            "formup_time": "",
            "formup_timestamp": "",
            "fleet_comms": "Discord",
            "fleet_doctrine": "Shield Fleet",
            "fleet_doctrine_url": "http://example.com",
            "srp": True,
            "srp_link": False,
            "optimer": False,
            "additional_information": "Bring ammo",
        }

        result = get_ping_context_from_form_data(form_data)

        self.assertIsNone(result["ping_target"]["group_id"])
        self.assertIn(result["ping_target"]["group_name"], (None, "None"))
        self.assertEqual(result["ping_target"]["at_mention"], "")


class TestHelperGetWebhookPingContext(BaseTestCase):
    """
    Test the _get_webhook_ping_context function.
    """

    def test_generates_correct_ping_context_with_all_fields_provided(self):
        """
        Test that the function generates the correct ping context with all fields provided.

        :return:
        :rtype:
        """

        ping_context = {
            "ping_target": {
                "group_id": 12345,
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
        result = _get_webhook_ping_context(ping_context)
        self.assertIn(
            "<@&12345> :: **PvP Fleet is up under John Doe**", result["header"]
        )
        self.assertIn("**FC:** John Doe", result["content"])
        self.assertIn("**Formup Time:** NOW", result["content"])
        self.assertIn(
            "**Ships / Doctrine:** Shield Doctrine ([Doctrine Link](http://example.com))",
            result["content"],
        )

    def test_handles_missing_ping_target_gracefully(self):
        """
        Test that the function handles missing ping target gracefully.

        :return:
        :rtype:
        """

        ping_context = {
            "ping_target": {"group_id": None, "group_name": None, "at_mention": ""},
            "is_pre_ping": True,
            "fleet_type": "Mining",
            "fleet_commander": None,
            "fleet_name": None,
            "formup_location": None,
            "is_formup_now": False,
            "formup_time": {"datetime_string": "", "timestamp": ""},
            "fleet_duration": None,
            "fleet_comms": None,
            "doctrine": {"name": None, "link": None},
            "srp": {"has_srp": False, "create_srp_link": False},
            "additional_information": None,
        }

        result = _get_webhook_ping_context(ping_context)

        self.assertEqual(
            result["header"], "**\\### PRE PING ### / (Upcoming) Mining Fleet**\n** **"
        )
        self.assertEqual(result["content"], "")

    def test_includes_timezones_link_when_installed(self):
        """
        Test that the function includes time zone conversion link when timezones are installed.

        :return:
        :rtype:
        """

        ping_context = {
            "ping_target": {"group_id": None, "group_name": None, "at_mention": ""},
            "is_pre_ping": False,
            "fleet_type": "PvP",
            "fleet_commander": None,
            "fleet_name": None,
            "formup_location": None,
            "is_formup_now": False,
            "formup_time": {
                "datetime_string": "2023-10-01 18:00",
                "timestamp": "1696173600",
            },
            "fleet_duration": None,
            "fleet_comms": None,
            "doctrine": {"name": None, "link": None},
            "srp": {"has_srp": False, "create_srp_link": False},
            "additional_information": None,
        }

        with self.settings(TIMEZONES_INSTALLED=True):
            result = _get_webhook_ping_context(ping_context)

            self.assertIn("[Time Zone Conversion]", result["content"])

    def test_includes_srp_code_and_link_when_provided(self):
        """
        Test that the function includes SRP code and link when provided.

        :return:
        :rtype:
        """

        ping_context = {
            "ping_target": {"group_id": None, "group_name": None, "at_mention": ""},
            "is_pre_ping": False,
            "fleet_type": "PvP",
            "fleet_commander": None,
            "fleet_name": None,
            "formup_location": None,
            "is_formup_now": False,
            "formup_time": {"datetime_string": "", "timestamp": ""},
            "fleet_duration": None,
            "fleet_comms": None,
            "doctrine": {"name": None, "link": None},
            "srp": {
                "has_srp": True,
                "create_srp_link": True,
                "link": {"code": "SRP123", "link": "http://example.com/srp123"},
            },
            "additional_information": None,
        }
        result = _get_webhook_ping_context(ping_context)
        self.assertIn(
            "(SRP Code: [SRP123](http://example.com/srp123))", result["content"]
        )
