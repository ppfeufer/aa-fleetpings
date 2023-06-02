"""
Tests for model Setting
"""

# Django
from django.db.utils import IntegrityError
from django.test import TestCase

# AA Fleet Pings
from fleetpings.models import Setting
from fleetpings.tests.utils import create_setting


class TestSetting(TestCase):
    """
    Testing the Setting model
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
