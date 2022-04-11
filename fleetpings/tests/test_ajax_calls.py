"""
Test ajax calls
"""

# Django
from django.contrib.auth.models import Group
from django.test import TestCase
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
            permissions=["fleetpings.basic_access", "aasrp.create_srp"],
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
        self.assertEqual(res.status_code, 302)

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
        self.assertEqual(res.status_code, 200)

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
        self.assertEqual(res.status_code, 302)

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
        self.assertEqual(res.status_code, 200)

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
        self.assertEqual(res.status_code, 302)

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
        self.assertEqual(res.status_code, 200)

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
        self.assertEqual(res.status_code, 302)

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
        self.assertEqual(res.status_code, 200)

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
        self.assertEqual(res.status_code, 302)

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
        self.assertEqual(res.status_code, 200)

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
        self.assertEqual(res.status_code, 302)

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
        self.assertEqual(res.status_code, 200)

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
        self.assertEqual(res.status_code, 302)

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
        self.assertEqual(res.status_code, 200)
