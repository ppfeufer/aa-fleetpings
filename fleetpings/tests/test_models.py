"""
Test models
"""

# Django
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.test import TestCase

# AA Fleet Pings
from fleetpings.models import FleetDoctrine, Webhook


class TestModels(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        """
        Set up groups and users
        """

        super().setUpClass()

        cls.group = Group.objects.create(name="Superhero")

    def test_discord_webhook_should_throw_exception(self):
        """
        Test if we get a ValidationError for a Discord webhook
        :return:
        """

        # given
        webhook = Webhook(
            url=(
                "https://discord.com/api/webhooks/754343402302911920F/x-BfFCdEG"
                "-qGg_39_mFwDU_vHdFUqRSLozaAxZdgKO2dm6Oa8vxNdAyesVpy-Bzf8pm-"
            ),
        )

        # when
        with self.assertRaises(ValidationError):
            webhook.clean()

        with self.assertRaisesMessage(
            ValidationError,
            expected_message=(
                "Invalid webhook URL. The webhook URL you entered does not match any "
                "known format for a Discord webhook. Please check the "
                "webhook URL."
            ),
        ):
            webhook.clean()

    def test_doctrine_link_should_throw_exception(self):
        """
        Test if we get a ValidationError for a doctrine link
        :return:
        """

        # given
        doctrine = FleetDoctrine(
            name="Awesome Doctrine",
            link=("htp://invalid-doctrine.url"),
        )

        # when
        with self.assertRaises(ValidationError):
            doctrine.clean()

        with self.assertRaisesMessage(
            ValidationError,
            expected_message=("Your doctrine URL is not valid."),
        ):
            doctrine.clean()

    # def test_discord_ping_target_should_throw_not_synced_yet_exception(self):
    #     """
    #     Test if we get a ValidationError for a doctrine link
    #     :return:
    #     """
    #
    #     # given
    #     ping_target = DiscordPingTargets(name=self.group)
    #
    #     # when
    #     with self.assertRaises(ValidationError):
    #         ping_target.clean()
    #
    #     with self.assertRaisesMessage(
    #         ValidationError,
    #         expected_message=("This group has not been synced to Discord yet."),
    #     ):
    #         ping_target.clean()
