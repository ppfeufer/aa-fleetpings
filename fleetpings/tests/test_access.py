"""
Test checks for access to fleetpings
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
            permissions=["fleetpings.basic_access", "aasrp.create_srp"],
        )

    def test_has_no_access(self):
        """
        Test that a user without access get a 302
        :return:
        """

        # given
        self.client.force_login(self.user_1001)

        # when
        res = self.client.get(reverse("fleetpings:index"))

        # then
        self.assertEqual(res.status_code, HTTPStatus.FOUND)

    def test_has_access(self):
        """
        Test that a user with access get to see it
        :return:
        """

        # given
        self.client.force_login(self.user_1002)

        # when
        res = self.client.get(reverse("fleetpings:index"))

        # then
        self.assertEqual(res.status_code, HTTPStatus.OK)

    @modify_settings(
        INSTALLED_APPS={
            "remove": [
                "allianceauth.srp",
                "aasrp",
                "timezones",
                "allianceauth.optimer",
                "fittings",
            ]
        }
    )
    def test_has_access_without_additional_modules(self):
        """
        Test that a user with access get to see it
        :return:
        """

        # given
        self.client.force_login(self.user_1002)

        # when
        response = self.client.get(reverse("fleetpings:index"))

        # then
        self.assertEqual(response.status_code, HTTPStatus.OK)

        # context data
        self.assertEqual(response.context["optimer_installed"], False)
        self.assertEqual(response.context["fittings_installed"], False)
        self.assertEqual(response.context["srp_module_available_to_user"], False)

    @modify_settings(
        INSTALLED_APPS={
            "remove": [
                "allianceauth.srp",
                "aasrp",
                "timezones",
                "allianceauth.optimer",
                "fittings",
            ],
            "append": "aasrp",
        }
    )
    def test_has_access_with_aasrp(self):
        """
        Test that a user with access get to see it
        :return:
        """

        # given
        self.client.force_login(self.user_1003)

        # when
        response = self.client.get(reverse("fleetpings:index"))

        # then
        self.assertEqual(response.status_code, HTTPStatus.OK)

        # context data
        self.assertEqual(response.context["optimer_installed"], False)
        self.assertEqual(response.context["fittings_installed"], False)
        self.assertEqual(response.context["srp_module_available_to_user"], True)

    @modify_settings(
        INSTALLED_APPS={
            "remove": [
                "allianceauth.srp",
                "aasrp",
                "timezones",
                "allianceauth.optimer",
                "fittings",
            ],
            "append": "allianceauth.srp",
        }
    )
    def test_has_access_with_allianceauth_srp(self):
        """
        Test that a user with access get to see it
        :return:
        """

        # given
        self.client.force_login(self.user_1003)

        # when
        response = self.client.get(reverse("fleetpings:index"))

        # then
        self.assertEqual(response.status_code, HTTPStatus.OK)

        # context data
        self.assertEqual(response.context["optimer_installed"], False)
        self.assertEqual(response.context["fittings_installed"], False)
        self.assertEqual(response.context["srp_module_available_to_user"], True)

    @modify_settings(
        INSTALLED_APPS={
            "remove": [
                "allianceauth.srp",
                "aasrp",
                "timezones",
                "allianceauth.optimer",
                "fittings",
            ],
            "append": "timezones",
        }
    )
    def test_has_access_with_timezones(self):
        """
        Test that a user with access get to see it
        :return:
        """

        # given
        self.client.force_login(self.user_1003)

        # when
        response = self.client.get(reverse("fleetpings:index"))

        # then
        self.assertEqual(response.status_code, HTTPStatus.OK)

        # context data
        self.assertEqual(response.context["optimer_installed"], False)
        self.assertEqual(response.context["fittings_installed"], False)
        self.assertEqual(response.context["srp_module_available_to_user"], False)

    @modify_settings(
        INSTALLED_APPS={
            "remove": [
                "allianceauth.srp",
                "aasrp",
                "timezones",
                "allianceauth.optimer",
                "fittings",
            ],
            "append": "allianceauth.optimer",
        }
    )
    def test_has_access_with_allianceauth_optimer(self):
        """
        Test that a user with access get to see it
        :return:
        """

        # given
        self.client.force_login(self.user_1003)

        # when
        response = self.client.get(reverse("fleetpings:index"))

        # then
        self.assertEqual(response.status_code, HTTPStatus.OK)

        # context data
        self.assertEqual(response.context["optimer_installed"], True)
        self.assertEqual(response.context["fittings_installed"], False)
        self.assertEqual(response.context["srp_module_available_to_user"], False)
