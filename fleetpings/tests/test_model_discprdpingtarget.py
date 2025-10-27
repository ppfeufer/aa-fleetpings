"""
Tests for model DiscordPingTargets
"""

# Standard Library
from unittest.mock import patch

# Third Party
from requests.exceptions import HTTPError

# Django
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError

# AA Fleet Pings
from fleetpings.models import DiscordPingTarget, _get_discord_group_info
from fleetpings.tests import BaseTestCase


class TestModelDiscordPingTarget(BaseTestCase):
    """
    Testing the DiscordPingTarget model
    """

    def test_saves_discord_id_when_discord_service_is_active(self):
        """
        Test that the discord_id is saved when the Discord service is active

        :return:
        :rtype:
        """

        group = Group.objects.create(name="Test Group")
        discord_ping_target = DiscordPingTarget(name=group)

        with (
            patch(
                "fleetpings.models._get_discord_group_info",
                return_value={"id": "12345"},
            ),
            patch("fleetpings.models.discord_service_installed", return_value=True),
        ):
            discord_ping_target.save()

        self.assertEqual(discord_ping_target.discord_id, "12345")

    def test_raises_validation_error_when_discord_service_is_inactive(self):
        """
        Test that a ValidationError is raised when the Discord service is inactive

        :return:
        :rtype:
        """

        group = Group.objects.create(name="Test Group")
        discord_ping_target = DiscordPingTarget(name=group)

        with patch("fleetpings.models.discord_service_installed", return_value=False):
            # Django
            from django.core.exceptions import ValidationError

            with self.assertRaises(ValidationError):
                discord_ping_target.clean()

    def test_string_representation_returns_group_name(self):
        """
        Test that the string representation of DiscordPingTarget returns the group name

        :return:
        :rtype:
        """

        group = Group.objects.create(name="Test Group")

        discord_ping_target = DiscordPingTarget(name=group)

        self.assertEqual(str(discord_ping_target), "Test Group")


class TestHelperGetDiscordGroupInfo(BaseTestCase):
    """
    Testing the _get_discord_group_info helper function
    """

    def test_raises_validation_error_when_discord_service_not_installed(self):
        """
        Test that a ValidationError is raised when the Discord service is not installed

        :return:
        :rtype:
        """

        group = Group.objects.create(name="Test Group")

        with patch("fleetpings.models.discord_service_installed", return_value=False):
            with self.assertRaises(ValidationError) as context:
                _get_discord_group_info(group)

            self.assertIn(
                "You might want to install the Discord service first …",
                str(context.exception),
            )

    def test_raises_validation_error_when_discord_group_not_synced(self):
        """
        Test that a ValidationError is raised when the Discord group is not synced

        :return:
        :rtype:
        """

        group = Group.objects.create(name="Unsynced Group")

        with (
            patch("fleetpings.models.discord_service_installed", return_value=True),
            patch(
                "fleetpings.models.DiscordUser.objects.group_to_role", return_value=None
            ),
        ):
            with self.assertRaises(ValidationError) as context:
                _get_discord_group_info(group)

            self.assertIn(
                "This group has not been synced to Discord yet.", str(context.exception)
            )

    def test_raises_validation_error_when_http_error_occurs(self):
        """
        Test that a ValidationError is raised when an HTTPError occurs

        :return:
        :rtype:
        """

        group = Group.objects.create(name="Test Group")

        with (
            patch("fleetpings.models.discord_service_installed", return_value=True),
            patch(
                "fleetpings.models.DiscordUser.objects.group_to_role",
                side_effect=HTTPError,
            ),
        ):
            with self.assertRaises(ValidationError) as context:
                _get_discord_group_info(group)

            self.assertIn(
                "Are you sure you have your Discord linked to your Alliance Auth?",
                str(context.exception),
            )

    def test_returns_discord_group_info_when_valid(self):
        group = Group.objects.create(name="Synced Group")
        mock_discord_info = {"id": "12345"}
        with (
            patch("fleetpings.models.discord_service_installed", return_value=True),
            patch(
                "fleetpings.models.DiscordUser.objects.group_to_role",
                return_value=mock_discord_info,
            ),
        ):
            result = _get_discord_group_info(group)
            self.assertEqual(result, mock_discord_info)
