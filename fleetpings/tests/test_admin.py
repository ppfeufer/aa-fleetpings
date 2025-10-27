"""
Tests for the admin module.
"""

# Standard Library
from types import SimpleNamespace
from unittest.mock import patch

# Django
from django.contrib.auth.models import Group

# AA Fleet Pings
from fleetpings.admin import (
    DiscordPingTargetsAdmin,
    FleetCommAdmin,
    FleetDoctrineAdmin,
    FleetTypeAdmin,
    WebhookAdmin,
    _custom_filter,
)
from fleetpings.form import SettingAdminForm
from fleetpings.models import (
    DiscordPingTarget,
    FleetComm,
    FleetDoctrine,
    FleetType,
    FormupLocation,
    Setting,
    Webhook,
)
from fleetpings.tests import BaseTestCase


class TestHelperCustomFilter(BaseTestCase):
    """
    Test the _custom_filter helper function.
    """

    def test_sets_title_on_created_instance(self):
        """
        Test that the _custom_filter sets the title on the created instance.

        :return:
        :rtype:
        """

        wrapper = _custom_filter("Custom Title")
        mock_instance = SimpleNamespace()

        with patch(
            "django.contrib.admin.FieldListFilter.create", return_value=mock_instance
        ) as mock_create:
            result = wrapper("field", "request", {"p": "v"}, "model", "model_admin")

            self.assertIs(result, mock_instance)
            self.assertEqual(result.title, "Custom Title")
            mock_create.assert_called_once_with(
                "field", "request", {"p": "v"}, "model", "model_admin"
            )

    def test_forwards_args_and_kwargs_to_create(self):
        """
        Test that the _custom_filter forwards arguments and keyword arguments to the create method.

        :return:
        :rtype:
        """

        wrapper = _custom_filter("Forwarded Title")
        mock_instance = SimpleNamespace()

        with patch(
            "django.contrib.admin.FieldListFilter.create", return_value=mock_instance
        ) as mock_create:
            result = wrapper(1, 2, key="value")
            mock_create.assert_called_once_with(1, 2, key="value")

            self.assertEqual(result.title, "Forwarded Title")

    def test_accepts_non_string_title_and_sets_it(self):
        """
        Test that the _custom_filter accepts a non-string title and sets it correctly.

        :return:
        :rtype:
        """

        wrapper = _custom_filter(12345)
        mock_instance = SimpleNamespace()

        with patch(
            "django.contrib.admin.FieldListFilter.create", return_value=mock_instance
        ):
            result = wrapper()

            self.assertEqual(result.title, 12345)


class TestClassFleetCommAdmin(BaseTestCase):
    """
    Test the FleetCommAdmin class.
    """

    def test_returns_correct_name_for_fleet_comm(self):
        """
        Test that the _name method returns the correct name for a FleetComm instance.

        :return:
        :rtype:
        """

        fleet_comm = FleetComm.objects.create(name="Test Fleet", channel="Test Channel")

        result = FleetCommAdmin._name(fleet_comm)

        self.assertEqual(result, "Test Fleet")

    def test_handles_empty_name_gracefully(self):
        """
        Test that the _name method handles an empty name gracefully.

        :return:
        :rtype:
        """

        fleet_comm = FleetComm.objects.create(name="", channel="Test Channel")

        result = FleetCommAdmin._name(fleet_comm)

        self.assertEqual(result, "")


class TestClassFleetDoctrineAdmin(BaseTestCase):
    """
    Test the FleetDoctrineAdmin class.
    """

    def test_returns_correct_name_for_fleet_doctrine(self):
        """
        Test that the _name method returns the correct name for a FleetDoctrine instance.

        :return:
        :rtype:
        """

        fleet_doctrine = FleetDoctrine(name="Test Doctrine")

        result = FleetDoctrineAdmin._name(fleet_doctrine)

        self.assertEqual(result, "Test Doctrine")

    def test_returns_correct_link_for_fleet_doctrine(self):
        """
        Test that the _link method returns the correct link for a FleetDoctrine instance.

        :return:
        :rtype:
        """

        fleet_doctrine = FleetDoctrine(name="Test Doctrine", link="http://example.com")

        result = FleetDoctrineAdmin._link(fleet_doctrine)

        self.assertEqual(result, "http://example.com")

    def test_returns_group_restrictions_as_comma_separated_string(self):
        """
        Test that the _restricted_to_group method returns group restrictions as a comma-separated string.

        :return:
        :rtype:
        """

        group1 = Group.objects.create(name="Group A")
        group2 = Group.objects.create(name="Group B")

        fleet_doctrine = FleetDoctrine.objects.create(name="Test Doctrine")
        fleet_doctrine.restricted_to_group.add(group1, group2)

        result = FleetDoctrineAdmin._restricted_to_group(fleet_doctrine)

        self.assertEqual(result, "Group A, Group B")

    def test_returns_none_when_no_group_restrictions_exist(self):
        """
        Test that the _restricted_to_group method returns None when no group restrictions exist.

        :return:
        :rtype:
        """

        fleet_doctrine = FleetDoctrine.objects.create(name="Test Doctrine")

        result = FleetDoctrineAdmin._restricted_to_group(fleet_doctrine)

        self.assertIsNone(result)


class TestClassFormupLocationAdmin(BaseTestCase):
    """
    Test the FormupLocationAdmin class.
    """

    def test_displays_correct_fields_in_list_view(self):
        """
        Test that the list_display attribute contains the correct fields.

        :return:
        :rtype:
        """

        formup_location = FormupLocation.objects.create(
            name="Staging Area", notes="Main staging area", is_enabled=True
        )

        self.assertEqual(formup_location.name, "Staging Area")
        self.assertEqual(formup_location.notes, "Main staging area")
        self.assertTrue(formup_location.is_enabled)

    def test_orders_by_name_ascending(self):
        """
        Test that the ordering attribute orders by name ascending.

        :return:
        :rtype:
        """

        FormupLocation.objects.create(
            name="Alpha", notes="First location", is_enabled=True
        )
        FormupLocation.objects.create(
            name="Beta", notes="Second location", is_enabled=True
        )

        locations = list(FormupLocation.objects.all().order_by("name"))

        self.assertEqual([location.name for location in locations], ["Alpha", "Beta"])

    def test_filters_by_is_enabled(self):
        """
        Test that filtering by is_enabled works correctly.

        :return:
        :rtype:
        """

        FormupLocation.objects.create(
            name="Enabled Location", notes="Active", is_enabled=True
        )
        FormupLocation.objects.create(
            name="Disabled Location", notes="Inactive", is_enabled=False
        )

        enabled_locations = FormupLocation.objects.filter(is_enabled=True)

        self.assertEqual(enabled_locations.count(), 1)
        self.assertEqual(enabled_locations[0].name, "Enabled Location")


class TestClassDiscordPingTargetsAdmin(BaseTestCase):
    """
    Test the DiscordPingTargetsAdmin class.
    """

    def test_displays_correct_name_in_list_view(self):
        """
        Test that the _name method returns the correct name for a DiscordPingTarget instance.

        :return:
        :rtype:
        """

        name_group = Group.objects.create(name="Ping Target")
        restricted_group = Group.objects.create(name="Test Group")

        with patch(
            "fleetpings.models._get_discord_group_info", return_value={"id": "12345"}
        ):
            discord_ping_target = DiscordPingTarget.objects.create(
                name=name_group, discord_id="12345"
            )
            discord_ping_target.restricted_to_group.add(restricted_group)

        self.assertEqual(
            str(DiscordPingTargetsAdmin._name(discord_ping_target)), "Ping Target"
        )

    def test_displays_group_restrictions_as_comma_separated_string(self):
        """
        Test that the _restricted_to_group method returns group restrictions as a comma-separated string.

        :return:
        :rtype:
        """

        name_group = Group.objects.create(name="Ping Target")
        group1 = Group.objects.create(name="Group A")
        group2 = Group.objects.create(name="Group B")

        with patch(
            "fleetpings.models._get_discord_group_info", return_value={"id": "12345"}
        ):
            discord_ping_target = DiscordPingTarget.objects.create(
                name=name_group, discord_id="12345"
            )

            discord_ping_target.restricted_to_group.add(group1, group2)

        result = DiscordPingTargetsAdmin._restricted_to_group(discord_ping_target)

        self.assertEqual(result, "Group A, Group B")

    def test_returns_none_when_no_group_restrictions_exist(self):
        """
        Test that the _restricted_to_group method returns None when no group restrictions exist.

        :return:
        :rtype:
        """

        name_group = Group.objects.create(name="Ping Target")

        with patch(
            "fleetpings.models._get_discord_group_info", return_value={"id": "12345"}
        ):
            discord_ping_target = DiscordPingTarget.objects.create(
                name=name_group, discord_id="12345"
            )

        result = DiscordPingTargetsAdmin._restricted_to_group(discord_ping_target)

        self.assertIsNone(result)

    def test_handles_empty_group_restrictions_gracefully(self):
        """
        Test that the _restricted_to_group method handles empty group restrictions gracefully.

        :return:
        :rtype:
        """

        name_group = Group.objects.create(name="Ping Target")

        with patch(
            "fleetpings.models._get_discord_group_info", return_value={"id": "12345"}
        ):
            discord_ping_target = DiscordPingTarget.objects.create(
                name=name_group, discord_id="12345"
            )

        discord_ping_target.restricted_to_group.clear()

        result = DiscordPingTargetsAdmin._restricted_to_group(discord_ping_target)

        self.assertIsNone(result)


class TestClassFleetTypeAdmin(BaseTestCase):
    """
    Test the FleetTypeAdmin class.
    """

    def test_displays_correct_fleet_type_name(self):
        """
        Test that the _name method returns the correct fleet type name.

        :return:
        :rtype:
        """

        fleet_type = FleetType.objects.create(name="Logistics")

        self.assertEqual(FleetTypeAdmin._name(fleet_type), "Logistics")

    def test_displays_embed_color_as_html(self):
        """
        Test that the _embed_color method displays the embed color as HTML.

        :return:
        :rtype:
        """

        fleet_type = FleetType.objects.create(name="Logistics", embed_color="#FF5733")

        result = FleetTypeAdmin._embed_color(fleet_type)

        self.assertIn(
            '<span style="display: inline-block; width: 16px; background-color: #FF5733;">',
            result,
        )
        self.assertIn("#FF5733", result)

    def test_displays_group_restrictions_as_comma_separated_string(self):
        """
        Test that the _restricted_to_group method returns group restrictions as a comma-separated string.

        :return:
        :rtype:
        """

        group1 = Group.objects.create(name="Group A")
        group2 = Group.objects.create(name="Group B")

        fleet_type = FleetType.objects.create(name="Logistics")
        fleet_type.restricted_to_group.add(group1, group2)

        result = FleetTypeAdmin._restricted_to_group(fleet_type)

        self.assertEqual(result, "Group A, Group B")

    def test_returns_none_when_no_group_restrictions_exist(self):
        """
        Test that the _restricted_to_group method returns None when no group restrictions exist.

        :return:
        :rtype:
        """

        fleet_type = FleetType.objects.create(name="Logistics")

        result = FleetTypeAdmin._restricted_to_group(fleet_type)

        self.assertIsNone(result)

    def test_handles_empty_embed_color_gracefully(self):
        fleet_type = FleetType.objects.create(name="Logistics", embed_color="")
        result = FleetTypeAdmin._embed_color(fleet_type)
        self.assertEqual("", result)


class TestClassWebhookAdmin(BaseTestCase):
    """
    Test the WebhookAdmin class.
    """

    def test_displays_correct_webhook_name(self):
        """
        Test that the _name method returns the correct webhook name.

        :return:
        :rtype:
        """

        webhook = Webhook.objects.create(name="Test Webhook", url="https://example.com")

        self.assertEqual(WebhookAdmin._name(webhook), "Test Webhook")

    def test_displays_correct_webhook_url(self):
        """
        Test that the _url method returns the correct webhook URL.

        :return:
        :rtype:
        """

        webhook = Webhook.objects.create(name="Test Webhook", url="https://example.com")

        self.assertEqual(WebhookAdmin._url(webhook), "https://example.com")

    def test_displays_group_restrictions_as_comma_separated_string(self):
        """
        Test that the _restricted_to_group method returns group restrictions as a comma-separated string.

        :return:
        :rtype:
        """

        group1 = Group.objects.create(name="Group A")
        group2 = Group.objects.create(name="Group B")

        webhook = Webhook.objects.create(name="Test Webhook", url="https://example.com")
        webhook.restricted_to_group.add(group1, group2)

        result = WebhookAdmin._restricted_to_group(webhook)

        self.assertEqual(result, "Group A, Group B")

    def test_returns_none_when_no_group_restrictions_exist(self):
        """
        Test that the _restricted_to_group method returns None when no group restrictions exist.

        :return:
        :rtype:
        """

        webhook = Webhook.objects.create(name="Test Webhook", url="https://example.com")

        result = WebhookAdmin._restricted_to_group(webhook)

        self.assertIsNone(result)

    def test_handles_empty_webhook_name_gracefully(self):
        """
        Test that the _name method handles an empty webhook name gracefully.

        :return:
        :rtype:
        """

        webhook = Webhook.objects.create(name="", url="https://example.com")

        self.assertEqual(WebhookAdmin._name(webhook), "")

    def test_handles_empty_webhook_url_gracefully(self):
        """
        Test that the _url method handles an empty webhook URL gracefully.

        :return:
        :rtype:
        """

        webhook = Webhook.objects.create(name="Test Webhook", url="")

        self.assertEqual(WebhookAdmin._url(webhook), "")


class TestClassSettingAdmin(BaseTestCase):
    """
    Test the SettingAdmin class.
    """

    def test_displays_correct_setting_form(self):
        """
        Test that the SettingAdmin form displays correctly.

        :return:
        :rtype:
        """

        setting = Setting.get_solo()

        form = SettingAdminForm(instance=setting)

        self.assertIsInstance(form, SettingAdminForm)
