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
            type=Webhook.Types.DISCORD,
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
                f"known format for a {Webhook.Types.DISCORD} webhook. Please check the "
                "webhook URL."
            ),
        ):
            webhook.clean()

    def test_slack_webhook_should_throw_exception(self):
        """
        Test if we get a ValidationError for a Slack webhook
        :return:
        """

        # given
        webhook = Webhook(
            type=Webhook.Types.SLACK,
            url=(
                "https://hooks.slack.com/service/T01A1CJUGFR/B01B61BPWRE"
                "/HQfhsBXrM2K2mtRETSOsRfas"
            ),
        )

        # when
        with self.assertRaises(ValidationError):
            webhook.clean()

        with self.assertRaisesMessage(
            ValidationError,
            expected_message=(
                "Invalid webhook URL. The webhook URL you entered does not match any "
                f"known format for a {Webhook.Types.SLACK} webhook. Please check the "
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
