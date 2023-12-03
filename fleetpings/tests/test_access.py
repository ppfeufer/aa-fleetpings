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
        Setup

        :return:
        :rtype:
        """

        super().setUpClass()

        cls.group = Group.objects.create(name="Superhero")

        # User cannot access fleetpings
        cls.user_1001 = create_fake_user(
            character_id=1001, character_name="Peter Parker"
        )

        # User can access fleetpings
        cls.user_1002 = create_fake_user(
            character_id=1002,
            character_name="Bruce Wayne",
            permissions=["fleetpings.basic_access"],
        )

        # User can add srp (aasrp)
        cls.user_1003 = create_fake_user(
            character_id=1003,
            character_name="Clark Kent",
            permissions=["fleetpings.basic_access", "aasrp.create_srp"],
        )

    def test_has_no_access(self):
        """
        Test that a user without access gets redirected

        :return:
        :rtype:
        """

        # given
        self.client.force_login(user=self.user_1001)

        # when
        res = self.client.get(path=reverse(viewname="fleetpings:index"))

        # then
        self.assertEqual(first=res.status_code, second=HTTPStatus.FOUND)

    def test_has_access(self):
        """
        Test that a user with access gets to see it

        :return:
        :rtype:
        """

        # given
        self.client.force_login(user=self.user_1002)

        # when
        res = self.client.get(path=reverse(viewname="fleetpings:index"))

        # then
        self.assertEqual(first=res.status_code, second=HTTPStatus.OK)

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
        Test that a user with access gets to see it (without additional modules)

        :return:
        :rtype:
        """

        # given
        self.client.force_login(user=self.user_1002)

        # when
        response = self.client.get(path=reverse(viewname="fleetpings:index"))

        # then
        self.assertEqual(first=response.status_code, second=HTTPStatus.OK)

        # context data
        self.assertEqual(first=response.context["optimer_installed"], second=False)
        self.assertEqual(first=response.context["fittings_installed"], second=False)
        self.assertEqual(
            first=response.context["srp_module_available_to_user"], second=False
        )

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
        Test that a user with access gets to see it (aasrp access)

        :return:
        :rtype:
        """

        # given
        self.client.force_login(user=self.user_1003)

        # when
        response = self.client.get(path=reverse(viewname="fleetpings:index"))

        # then
        self.assertEqual(first=response.status_code, second=HTTPStatus.OK)

        # context data
        self.assertEqual(first=response.context["optimer_installed"], second=False)
        self.assertEqual(first=response.context["fittings_installed"], second=False)
        self.assertEqual(
            first=response.context["srp_module_available_to_user"], second=True
        )

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
        Test that a user with access gets to see it (allianceauth.srp access)

        :return:
        :rtype:
        """

        # given
        self.client.force_login(user=self.user_1003)

        # when
        response = self.client.get(path=reverse(viewname="fleetpings:index"))

        # then
        self.assertEqual(first=response.status_code, second=HTTPStatus.OK)

        # context data
        self.assertEqual(first=response.context["optimer_installed"], second=False)
        self.assertEqual(first=response.context["fittings_installed"], second=False)
        self.assertEqual(
            first=response.context["srp_module_available_to_user"], second=True
        )

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
        Test that a user with access gets to see it (timezones access)

        :return:
        :rtype:
        """

        # given
        self.client.force_login(user=self.user_1003)

        # when
        response = self.client.get(path=reverse(viewname="fleetpings:index"))

        # then
        self.assertEqual(first=response.status_code, second=HTTPStatus.OK)

        # context data
        self.assertEqual(first=response.context["optimer_installed"], second=False)
        self.assertEqual(first=response.context["fittings_installed"], second=False)
        self.assertEqual(
            first=response.context["srp_module_available_to_user"], second=False
        )

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
        Test that a user with access gets to see it (allianceauth.optimer access)

        :return:
        :rtype:
        """

        # given
        self.client.force_login(user=self.user_1003)

        # when
        response = self.client.get(path=reverse(viewname="fleetpings:index"))

        # then
        self.assertEqual(first=response.status_code, second=HTTPStatus.OK)

        # context data
        self.assertEqual(first=response.context["optimer_installed"], second=True)
        self.assertEqual(first=response.context["fittings_installed"], second=False)
        self.assertEqual(
            first=response.context["srp_module_available_to_user"], second=False
        )
