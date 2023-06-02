"""
Tests for model FleetType
"""

# Django
from django.test import TestCase

# AA Fleet Pings
from fleetpings.models import FleetType


class TestModelFleetType(TestCase):
    """
    Testing the FleetType model
    """

    def test_should_return_fleettype_model_string_name(self):
        """
        Test should return the FleetType model string name
        :return:
        :rtype:
        """

        fleet_type = FleetType(name="Fun Fleet")
        fleet_type.save()

        self.assertEqual(str(fleet_type), "Fun Fleet")
