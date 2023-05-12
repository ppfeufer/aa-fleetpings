"""
Test models
"""

# Standard Library
from unittest import mock

# Django
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase

# AA Fleet Pings
from fleetpings.models import (
    DiscordPingTargets,
    FleetComm,
    FleetDoctrine,
    FleetType,
    FormupLocation,
    Setting,
    Webhook,
)
from fleetpings.tests.utils import create_setting


class TestModels(TestCase):
    """
    Test the models
    """

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

    @mock.patch(
        "fleetpings.models.Setting.webhook_verification",
        new_callable=mock.PropertyMock,
    )
    def test_discord_webhook_should_not_throw_exception_with_verification_false(
        self, webhook_verification
    ):
        """
        Test we do not get a ValidationError for an invalid Discord webhook when
        settings.webhook_verification is set to False
        :return:
        """

        # given
        webhook_verification.return_value = False

        # when
        webhook = Webhook(url="http://test/a/bad/webhook")

        # then
        self.assertIsNone(webhook.clean())

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

    def test_should_return_fleetcomm_model_string_name(self):
        """
        Test should return the FleetComm model string name
        :return:
        :rtype:
        """

        test_object = FleetComm(name="Alliance Mumble")

        test_object.save()

        self.assertEqual(str(test_object), "Alliance Mumble")

    def test_should_return_fleetdoctrine_model_string_name(self):
        """
        Test should return the FleetDoctrine model string name
        :return:
        :rtype:
        """

        test_object = FleetDoctrine(name="Awesome Ships")

        test_object.save()

        self.assertEqual(str(test_object), "Awesome Ships")

    def test_should_return_formuplocation_model_string_name(self):
        """
        Test should return the FormupLocation model string name
        :return:
        :rtype:
        """

        test_object = FormupLocation(name="Alliance HQ")

        test_object.save()

        self.assertEqual(str(test_object), "Alliance HQ")

    def test_should_return_pingtarget_model_string_name(self):
        """
        Test should return the DiscordPingTargets model string name
        :return:
        :rtype:
        """

        test_object = DiscordPingTargets(name=self.group)

        self.assertEqual(str(test_object), self.group.name)

    def test_should_return_fleettype_model_string_name(self):
        """
        Test should return the FleetType model string name
        :return:
        :rtype:
        """

        test_object = FleetType(name="Fun Fleet")

        test_object.save()

        self.assertEqual(str(test_object), "Fun Fleet")

    def test_should_return_webhook_model_string_name(self):
        """
        Test should return the Webhook model string name
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

        self.assertEqual(str(test_object), "Test Webhook")


class TestSetting(TestCase):
    """
    Tests for Settings model
    """

    def test_model_string_name(self):
        """
        Test model string name
        :return:
        """

        # given
        setting = Setting.objects.get(pk=1)

        # when/then
        self.assertEqual(str(setting), "Fleet Pings Settings")

    def test_setting_save(self):
        """
        Test if there can't be another setting created
        and the existing setting is changed instead
        :return:
        """

        # given
        use_default_fleet_types = True
        use_default_ping_targets = True
        setting = Setting(
            pk=2,
            use_default_fleet_types=use_default_fleet_types,
            use_default_ping_targets=use_default_ping_targets,
        )
        setting.save()

        # then
        self.assertEqual(setting.pk, 1)
        self.assertEqual(setting.use_default_fleet_types, use_default_fleet_types)
        self.assertEqual(setting.use_default_ping_targets, use_default_ping_targets)

    def test_setting_create(self):
        """
        Test that create method throwing the following exception
        django.db.utils.IntegrityError: (1062, "Duplicate entry '1' for key 'PRIMARY'")
        :return:
        """

        # No pk given
        with self.assertRaises(IntegrityError):
            create_setting()

    def test_setting_create_with_pk(self):
        """
        Test that create method throwing the following exception no matter the given pk
        django.db.utils.IntegrityError: (1062, "Duplicate entry '1' for key 'PRIMARY'")
        :return:
        """

        # Set pk=2
        with self.assertRaises(IntegrityError):
            create_setting(pk=2)

    def test_cannot_be_deleted(self):
        """
        Test that the settings object cannot be deleted
        :return:
        """

        # given
        settings_old = Setting.objects.get(pk=1)

        # when
        Setting.objects.all().delete()

        # then
        settings = Setting.objects.all()
        settings_first = settings.first()

        # See if there is still only ONE Setting object
        self.assertEqual(settings.count(), 1)

        # Check if both of our objects are identical
        self.assertEqual(settings_old, settings_first)
