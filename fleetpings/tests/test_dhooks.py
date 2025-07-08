"""
Test cases for the `fleetpings.helper.discord_webhook` module.
"""

# Standard Library
from unittest import TestCase

# AA Fleet Pings
from fleetpings import __app_name_useragent__, __github_url__, __version__
from fleetpings.helper.discord_webhook import get_user_agent


class TestUserAgent(TestCase):
    """
    Test cases for the `UserAgent` class
    """

    def test_create_useragent(self):
        """
        Test creating a user agent
        :return:
        :rtype:
        """

        obj = get_user_agent()

        self.assertEqual(first=obj.name, second=__app_name_useragent__)
        self.assertEqual(first=obj.url, second=__github_url__)
        self.assertEqual(first=obj.version, second=__version__)

    def test_useragent_str(self):
        """
        Test the string representation of the user agent
        :return:
        :rtype:
        """

        obj = get_user_agent()

        self.assertEqual(
            first=str(obj),
            second=f"{__app_name_useragent__} ({__github_url__}, {__version__})",
        )
