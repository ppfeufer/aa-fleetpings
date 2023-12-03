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
        Setup

        :return:
        :rtype:
        """

        super().setUpClass()

        cls.group = Group.objects.create(name="Superhero")

    def test_should_return_pingtarget_model_string_name(self):
        """
        Test should return DiscordPingTarget model string name

        :return:
        :rtype:
        """

        test_object = DiscordPingTarget(name=self.group)

        self.assertEqual(first=str(test_object), second=self.group.name)
