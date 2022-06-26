"""
Test ajax calls
"""

# Standard Library
from http import HTTPStatus

# Django
from django.contrib.auth.models import Group
from django.test import TestCase, modify_settings
from django.urls import reverse

# AA Fleet Pings
from fleetpings.tests.utils import create_fake_user


class TestAccess(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        """
        Set up groups and users
        """

        super().setUpClass()

        cls.group = Group.objects.create(name="Superhero")

        # User cannot access fleetpings
        cls.user_1001 = create_fake_user(1001, "Peter Parker")

        # User can access fleetpings
        cls.user_1002 = create_fake_user(
            1002, "Bruce Wayne", permissions=["fleetpings.basic_access"]
        )

        # User can add srp (aasrp)
        cls.user_1003 = create_fake_user(
            1003,
            "Clark Kent",
            permissions=[
                "fleetpings.basic_access",
                "aasrp.create_srp",
                "srp.add_srpfleetmain",
            ],
        )

    def test_ajax_get_ping_targets_no_access(self):
        """
        Test ajax call to get ping targets available for
        the current user without access to it
        :return:
        """

        # given
        self.client.force_login(self.user_1001)

        # when
        res = self.client.get(reverse("fleetpings:ajax_get_ping_targets"))

        # then
        self.assertEqual(res.status_code, HTTPStatus.FOUND)

    def test_ajax_get_ping_targets_general(self):
        """
        Test ajax call to get ping targets available for the current user
        :return:
        """

        # given
        self.client.force_login(self.user_1002)

        # when
        res = self.client.get(reverse("fleetpings:ajax_get_ping_targets"))

        # then
        self.assertEqual(res.status_code, HTTPStatus.OK)

    def test_ajax_get_webhooks_no_access(self):
        """
        Test ajax call to get webhooks available for
        the current user without access to it
        :return:
        """

        # given
        self.client.force_login(self.user_1001)

        # when
        res = self.client.get(reverse("fleetpings:ajax_get_webhooks"))

        # then
        self.assertEqual(res.status_code, HTTPStatus.FOUND)

    def test_ajax_get_webhooks_general(self):
        """
        Test ajax call to get webhooks available for the current user
        :return:
        """

        # given
        self.client.force_login(self.user_1002)

        # when
        res = self.client.get(reverse("fleetpings:ajax_get_webhooks"))

        # then
        self.assertEqual(res.status_code, HTTPStatus.OK)

    def test_ajax_get_fleet_types_no_access(self):
        """
        Test ajax call to get fleet types available for
        the current user without access to it
        :return:
        """

        # given
        self.client.force_login(self.user_1001)

        # when
        res = self.client.get(reverse("fleetpings:ajax_get_fleet_types"))

        # then
        self.assertEqual(res.status_code, HTTPStatus.FOUND)

    def test_ajax_get_fleet_types_general(self):
        """
        Test ajax call to get fleet types available for the current user
        :return:
        """

        # given
        self.client.force_login(self.user_1002)

        # when
        res = self.client.get(reverse("fleetpings:ajax_get_fleet_types"))

        # then
        self.assertEqual(res.status_code, HTTPStatus.OK)

    def test_ajax_get_formup_locations_no_access(self):
        """
        Test ajax call to get formup locations available for
        a user without access to it
        :return:
        """

        # given
        self.client.force_login(self.user_1001)

        # when
        res = self.client.get(reverse("fleetpings:ajax_get_formup_locations"))

        # then
        self.assertEqual(res.status_code, HTTPStatus.FOUND)

    def test_ajax_get_formup_locations_general(self):
        """
        Test ajax call to get formup locations available for the current user
        :return:
        """

        # given
        self.client.force_login(self.user_1002)

        # when
        res = self.client.get(reverse("fleetpings:ajax_get_formup_locations"))

        # then
        self.assertEqual(res.status_code, HTTPStatus.OK)

    def test_ajax_get_fleet_comms_no_access(self):
        """
        Test ajax call to get fleet comms available for
        a user without access to it
        :return:
        """

        # given
        self.client.force_login(self.user_1001)

        # when
        res = self.client.get(reverse("fleetpings:ajax_get_fleet_comms"))

        # then
        self.assertEqual(res.status_code, HTTPStatus.FOUND)

    def test_ajax_get_fleet_comms_general(self):
        """
        Test ajax call to get fleet comms available for the current user
        :return:
        """

        # given
        self.client.force_login(self.user_1002)

        # when
        res = self.client.get(reverse("fleetpings:ajax_get_fleet_comms"))

        # then
        self.assertEqual(res.status_code, HTTPStatus.OK)

    def test_ajax_get_fleet_doctrines_no_access(self):
        """
        Test ajax call to get fleet doctrines available for
        a user without access to it
        :return:
        """

        # given
        self.client.force_login(self.user_1001)

        # when
        res = self.client.get(reverse("fleetpings:ajax_get_fleet_doctrines"))

        # then
        self.assertEqual(res.status_code, HTTPStatus.FOUND)

    def test_ajax_get_fleet_doctrines_general(self):
        """
        Test ajax call to get fleet doctrines available for the current user
        :return:
        """

        # given
        self.client.force_login(self.user_1002)

        # when
        res = self.client.get(reverse("fleetpings:ajax_get_fleet_doctrines"))

        # then
        self.assertEqual(res.status_code, HTTPStatus.OK)

    def test_ajax_create_fleet_ping_no_access(self):
        """
        Test ajax call to create fleet pings available for
        a user without access to it
        :return:
        """

        # given
        self.client.force_login(self.user_1001)

        # when
        res = self.client.get(reverse("fleetpings:ajax_create_fleet_ping"))

        # then
        self.assertEqual(res.status_code, HTTPStatus.FOUND)

    def test_ajax_create_fleet_ping_general(self):
        """
        Test ajax call to create fleet pings for the current user
        :return:
        """

        # given
        self.client.force_login(self.user_1002)

        # when
        res = self.client.get(reverse("fleetpings:ajax_create_fleet_ping"))

        # then
        self.assertEqual(res.status_code, HTTPStatus.OK)

    def test_ajax_create_fleet_ping_general_with_form_data(self):
        """
        Test ajax call to create fleet pings for the current user with form data
        :return:
        """

        # given
        self.client.force_login(self.user_1002)
        form_data = {
            "ping_target": "@here",
            "pre_ping": 0,
            "ping_channel": "",
            "fleet_type": "CTA",
            "fleet_commander": "Jean Luc Picard",
            "fleet_name": "Starfleet",
            "formup_location": "Utopia Planitia",
            "formup_time": "",
            "formup_timestamp": "",
            "formup_now": 1,
            "fleet_comms": "Mumble",
            "fleet_doctrine": "Federation Ships",
            "fleet_doctrine_url": "",
            "webhook_embed_color": "",
            "srp": 1,
            "srp_link": 1,
            "additional_information": "Borg to slaughter!",
        }

        # when
        response = self.client.post(
            reverse("fleetpings:ajax_create_fleet_ping"), data=form_data
        )

        # then
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(
            response, "fleetpings/partials/ping/copy-paste-text.html"
        )
        self.assertContains(response, "@here")
        self.assertContains(response, "**FC:** Jean Luc Picard")
        self.assertContains(response, "**Fleet Name:** Starfleet")
        self.assertContains(response, "**Formup Location:** Utopia Planitia")
        self.assertContains(response, "**Comms:** Mumble")
        self.assertContains(response, "**Ships / Doctrine:** Federation Ships")
        self.assertContains(response, "**SRP:** Yes")
        self.assertContains(response, "Borg to slaughter!")

    @modify_settings(
        INSTALLED_APPS={
            "remove": ["allianceauth.srp", "aasrp"],  # Remove all SRP modules
            "append": "aasrp",  # Add allianceauth.srp
        }
    )
    def test_aasrp_link_creation(self):
        # given
        self.client.force_login(self.user_1003)
        form_data = {
            "ping_target": "@here",
            "pre_ping": 0,
            "ping_channel": "",
            "fleet_type": "CTA",
            "fleet_commander": "Jean Luc Picard",
            "fleet_name": "Starfleet",
            "formup_location": "Utopia Planitia",
            "formup_time": "",
            "formup_timestamp": "",
            "formup_now": 1,
            "fleet_comms": "Mumble",
            "fleet_doctrine": "Federation Ships",
            "fleet_doctrine_url": "",
            "webhook_embed_color": "",
            "srp": 1,
            "srp_link": 1,
            "additional_information": "Borg to slaughter!",
        }

        # when
        response = self.client.post(
            reverse("fleetpings:ajax_create_fleet_ping"), data=form_data
        )

        # then
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "*SRP:** Yes")
        self.assertContains(response, "SRP Link:")

    @modify_settings(
        INSTALLED_APPS={
            "remove": ["allianceauth.srp", "aasrp"],  # Remove all SRP modules
            "append": "allianceauth.srp",  # Add allianceauth.srp
        }
    )
    def test_allianceauth_srp_link_creation(self):
        # given
        self.client.force_login(self.user_1003)
        form_data = {
            "ping_target": "@here",
            "pre_ping": 0,
            "ping_channel": "",
            "fleet_type": "CTA",
            "fleet_commander": "Jean Luc Picard",
            "fleet_name": "Starfleet",
            "formup_location": "Utopia Planitia",
            "formup_time": "",
            "formup_timestamp": "",
            "formup_now": 1,
            "fleet_comms": "Mumble",
            "fleet_doctrine": "Federation Ships",
            "fleet_doctrine_url": "",
            "webhook_embed_color": "",
            "srp": 1,
            "srp_link": 1,
            "additional_information": "Borg to slaughter!",
        }

        # when
        response = self.client.post(
            reverse("fleetpings:ajax_create_fleet_ping"), data=form_data
        )

        # then
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "*SRP:** Yes")
        self.assertContains(response, "SRP Link:")
