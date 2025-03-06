"""
Test the settings
"""

# Django
from django.test import TestCase, modify_settings, override_settings

# AA Fleet Pings
from fleetpings.app_settings import (
    debug_enabled,
    discord_service_installed,
    fittings_installed,
    optimer_installed,
    srp_module_installed,
    srp_module_is,
    timezones_installed,
)


class TestSettings(TestCase):
    """
    Test the settings
    """

    @override_settings(DEBUG=True)
    def test_debug_enabled_with_debug_true(self) -> None:
        """
        Test debug_enabled with DEBUG = True

        :return:
        :rtype:
        """

        self.assertTrue(debug_enabled())

    @override_settings(DEBUG=False)
    def test_debug_enabled_with_debug_false(self) -> None:
        """
        Test debug_enabled with DEBUG = False

        :return:
        :rtype:
        """

        self.assertFalse(debug_enabled())

    @modify_settings(INSTALLED_APPS={"append": "timezones"})
    def test_timezones_installed(self) -> None:
        """
        Test timezones_installed with timezones installed

        :return:
        :rtype:
        """

        self.assertTrue(timezones_installed())

    @modify_settings(INSTALLED_APPS={"remove": "timezones"})
    def test_timezones_not_installed(self) -> None:
        """
        Test timezones_installed with timezones not installed

        :return:
        :rtype:
        """

        self.assertFalse(timezones_installed())

    @modify_settings(INSTALLED_APPS={"append": "allianceauth.optimer"})
    def test_optimer_installed(self) -> None:
        """
        Test optimer_installed with optimer installed

        :return:
        :rtype:
        """

        self.assertTrue(optimer_installed())

    @modify_settings(INSTALLED_APPS={"remove": "allianceauth.optimer"})
    def test_optimer_not_installed(self) -> None:
        """
        Test optimer_installed with optimer not installed

        :return:
        :rtype:
        """

        self.assertFalse(optimer_installed())

    @modify_settings(INSTALLED_APPS={"append": "fittings"})
    def test_fittings_installed(self) -> None:
        """
        Test fittings_installed with fittings installed

        :return:
        :rtype:
        """

        self.assertTrue(fittings_installed())

    @modify_settings(INSTALLED_APPS={"remove": "fittings"})
    def test_fittings_not_installed(self) -> None:
        """
        Test fittings_installed with fittings not installed

        :return:
        :rtype:
        """

        self.assertFalse(fittings_installed())

    @modify_settings(INSTALLED_APPS={"append": "allianceauth.srp"})
    @modify_settings(INSTALLED_APPS={"remove": "aasrp"})
    def test_srp_module_allianceauth_srp_installed(self) -> None:
        """
        Test srp_module_installed with allianceauth.srp installed

        :return:
        :rtype:
        """

        self.assertTrue(srp_module_installed())
        self.assertTrue(srp_module_is(module_name="allianceauth.srp"))
        self.assertFalse(srp_module_is(module_name="aasrp"))

    @modify_settings(INSTALLED_APPS={"remove": "allianceauth.srp"})
    @modify_settings(INSTALLED_APPS={"remove": "aasrp"})
    def test_srp_module_allianceauth_srp_not_installed(self) -> None:
        """
        Test srp_module_installed with allianceauth.srp not installed

        :return:
        :rtype:
        """

        self.assertFalse(srp_module_installed())

    @modify_settings(INSTALLED_APPS={"append": "aasrp"})
    @modify_settings(INSTALLED_APPS={"remove": "allianceauth.srp"})
    def test_srp_module_aasrp_installed(self) -> None:
        """
        Test srp_module_installed with aasrp installed

        :return:
        :rtype:
        """

        self.assertTrue(srp_module_installed())
        self.assertTrue(srp_module_is(module_name="aasrp"))
        self.assertFalse(srp_module_is(module_name="allianceauth.srp"))

    @modify_settings(INSTALLED_APPS={"remove": "aasrp"})
    @modify_settings(INSTALLED_APPS={"remove": "allianceauth.srp"})
    def test_srp_module_aasrp_not_installed(self) -> None:
        """
        Test srp_module_installed with aasrp not installed

        :return:
        :rtype:
        """

        self.assertFalse(srp_module_installed())

    @modify_settings(INSTALLED_APPS={"append": "allianceauth.services.modules.discord"})
    def test_discord_service_installed(self) -> None:
        """
        Test discord_service_installed with discord_service installed

        :return:
        :rtype:
        """

        self.assertTrue(discord_service_installed())

    @modify_settings(INSTALLED_APPS={"remove": "allianceauth.services.modules.discord"})
    def test_discord_service_not_installed(self) -> None:
        """
        Test discord_service_installed with discord_service not installed

        :return:
        :rtype:
        """

        self.assertFalse(discord_service_installed())
