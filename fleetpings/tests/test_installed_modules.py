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
        Set up groups and users
        """

        super().setUpClass()

    @modify_settings(INSTALLED_APPS={"remove": "timezones"})
    def test_for_timezones_installed_when_not_installed(self):
        """
        Test for timezones_installed when it is not
        :return:
        """

        self.assertFalse(timezones_installed())

    @modify_settings(INSTALLED_APPS={"append": "timezones"})
    def test_for_timezones_installed_when_installed(self):
        """
        Test for timezones_installed when it is installed
        :return:$FilePath$
        """

        self.assertTrue(timezones_installed())

    @modify_settings(INSTALLED_APPS={"remove": "allianceauth.optimer"})
    def test_for_optimer_installed_when_not_installed(self):
        """
        Test for optimer_installed when it is not
        :return:
        """

        self.assertFalse(optimer_installed())

    @modify_settings(INSTALLED_APPS={"append": "allianceauth.optimer"})
    def test_for_optimer_installed_when_installed(self):
        """
        Test for optimer_installed when it is installed
        :return:
        """

        self.assertTrue(optimer_installed())

    @modify_settings(INSTALLED_APPS={"remove": "allianceauth.services.modules.discord"})
    def test_for_discord_service_installed_when_not_installed(self):
        """
        Test for discord_service_installed when it is not
        :return:
        """

        self.assertFalse(discord_service_installed())

    @modify_settings(INSTALLED_APPS={"append": "allianceauth.services.modules.discord"})
    def test_for_discord_service_installed_when_installed(self):
        """
        Test for discord_service_installed when it is installed
        :return:
        """

        self.assertTrue(discord_service_installed())

    @modify_settings(INSTALLED_APPS={"remove": ["allianceauth.srp", "aasrp"]})
    def test_for_srp_module_installed_when_not_installed(self):
        """
        Test for srp_module_installed when it is not
        :return:
        """

        self.assertFalse(srp_module_installed())

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
        """

        self.assertTrue(srp_module_installed())
        self.assertTrue(srp_module_is("aasrp"))

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
        """

        self.assertTrue(srp_module_installed())
        self.assertTrue(srp_module_is("allianceauth.srp"))
