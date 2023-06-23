"""
Tests for model DiscordPingTargets
"""

# Django
from django.contrib.auth.models import Group
from django.test import TestCase

# AA Fleet Pings
from fleetpings.models import DiscordPingTarget


class TestModelDiscordPingTarget(TestCase):
    """
    Testing the DiscordPingTarget model
    """

    @classmethod
    def setUpClass(cls) -> None:
        """
        Set up groups and users
        """

        super().setUpClass()

        cls.group = Group.objects.create(name="Superhero")

    def test_should_return_pingtarget_model_string_name(self):
        """
        Test should return the DiscordPingTargets model string name
        :return:
        :rtype:
        """

        test_object = DiscordPingTarget(name=self.group)

        self.assertEqual(str(test_object), self.group.name)
