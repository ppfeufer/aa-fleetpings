"""
Test checks for installed modules we might use
"""

# Django
from django.test import TestCase, modify_settings

# AA Fleet Pings
from fleetpings.app_settings import (
    discord_service_installed,
    optimer_installed,
    srp_module_installed,
    srp_module_is,
    timezones_installed,
)


class TestModulesInstalled(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        """
        Setup

        :return:
        :rtype:
        """

        super().setUpClass()

    @modify_settings(INSTALLED_APPS={"remove": "timezones"})
    def test_for_timezones_installed_when_not_installed(self):
        """
        Test for timezones_installed when it is not installed

        :return:
        :rtype:
        """

        self.assertFalse(expr=timezones_installed())

    @modify_settings(INSTALLED_APPS={"append": "timezones"})
    def test_for_timezones_installed_when_installed(self):
        """
        Test for timezones_installed when it is installed

        :return:
        :rtype:
        """

        self.assertTrue(expr=timezones_installed())

    @modify_settings(INSTALLED_APPS={"remove": "allianceauth.optimer"})
    def test_for_optimer_installed_when_not_installed(self):
        """
        Test for optimer_installed when it is not installed

        :return:
        :rtype:
        """

        self.assertFalse(expr=optimer_installed())

    @modify_settings(INSTALLED_APPS={"append": "allianceauth.optimer"})
    def test_for_optimer_installed_when_installed(self):
        """
        Test for optimer_installed when it is installed

        :return:
        :rtype:
        """

        self.assertTrue(expr=optimer_installed())

    @modify_settings(INSTALLED_APPS={"remove": "allianceauth.services.modules.discord"})
    def test_for_discord_service_installed_when_not_installed(self):
        """
        Test for discord_service_installed when it is not installed

        :return:
        :rtype:
        """

        self.assertFalse(expr=discord_service_installed())

    @modify_settings(INSTALLED_APPS={"append": "allianceauth.services.modules.discord"})
    def test_for_discord_service_installed_when_installed(self):
        """
        Test for discord_service_installed when it is installed

        :return:
        :rtype:
        """

        self.assertTrue(expr=discord_service_installed())

    @modify_settings(INSTALLED_APPS={"remove": ["allianceauth.srp", "aasrp"]})
    def test_for_srp_module_installed_when_not_installed(self):
        """
        Test for srp_module_installed when it is not installed

        :return:
        :rtype:
        """

        self.assertFalse(expr=srp_module_installed())

    @modify_settings(
        INSTALLED_APPS={
            "remove": ["allianceauth.srp", "aasrp"],  # Remove all SRP modules
            "append": "aasrp",  # Add aasrp
        }
    )
    def test_for_srp_module_installed_when_aasrp_installed(self):
        """
        Test for srp_module_installed when it is aasrp

        :return:
        :rtype:
        """

        self.assertTrue(expr=srp_module_installed())
        self.assertTrue(expr=srp_module_is("aasrp"))

    @modify_settings(
        INSTALLED_APPS={
            "remove": ["allianceauth.srp", "aasrp"],  # Remove all SRP modules
            "append": "allianceauth.srp",  # Add allianceauth.srp
        }
    )
    def test_for_srp_module_installed_when_allianceauth_srp_installed(self):
        """
        Test for srp_module_installed when it is allianceauth.srp

        :return:
        :rtype:
        """

        self.assertTrue(expr=srp_module_installed())
        self.assertTrue(expr=srp_module_is("allianceauth.srp"))
