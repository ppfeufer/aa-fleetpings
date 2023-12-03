"""
Tests for model Webhook
"""

# Standard Library
from unittest import mock

# Django
from django.core.exceptions import ValidationError
from django.test import TestCase

# AA Fleet Pings
from fleetpings.models import Webhook


class TestModelWebhook(TestCase):
    """
    Testing the Webhook model
    """

    def test_should_return_webhook_model_string_name(self):
        """
        Test should return Webhook model string name

        :return:
        :rtype:
        """

        test_object = Webhook(
            name="Test Webhook",
            url=(
                "https://discord.com/api/webhooks/754119343402302920F/x-BfFCdEG"
                "-qGg_39_mFUqRSLoz2dm6Oa8vxNdaAxZdgKOAyesVpy-Bzf8wDU_vHdFpm-"
            ),
        )

        test_object.save()

        self.assertEqual(first=str(test_object), second="Test Webhook")

    def test_discord_webhook_should_throw_exception(self):
        """
        Test if we get a ValidationError for an invalid Discord webhook

        :return:
        :rtype:
        """

        # given
        webhook = Webhook(
            url=(
                "https://discord.com/api/webhooks/754343402302911920F/x-BfFCdEG"
                "-qGg_39_mFwDU_vHdFUqRSLozaAxZdgKO2dm6Oa8vxNdAyesVpy-Bzf8pm-"
            ),
        )

        # when
        with self.assertRaises(expected_exception=ValidationError):
            webhook.clean()

        with self.assertRaisesMessage(
            expected_exception=ValidationError,
            expected_message=(
                "Invalid webhook URL. The webhook URL you entered does not match any "
                "known format for a Discord webhook. Please check the "
                "webhook URL."
            ),
        ):
            webhook.clean()

    @mock.patch(
        target="fleetpings.models.Setting.webhook_verification",
        new_callable=mock.PropertyMock,
    )
    def test_discord_webhook_should_not_throw_exception_with_verification_false(
        self, webhook_verification
    ):
        """
        Test we do not get a ValidationError for an invalid Discord webhook when
        settings.webhook_verification is set to False

        :param webhook_verification:
        :type webhook_verification:
        :return:
        :rtype:
        """

        # given
        webhook_verification.return_value = False

        # when
        webhook = Webhook(url="http://test/a/bad/webhook")

        # then
        self.assertIsNone(obj=webhook.clean())
