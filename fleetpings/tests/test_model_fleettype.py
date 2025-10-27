"""
Tests for model FleetType
"""

# AA Fleet Pings
from fleetpings.models import FleetType
from fleetpings.tests import BaseTestCase


class TestModelFleetType(BaseTestCase):
    """
    Testing the FleetType model
    """

    def test_should_return_fleettype_model_string_name(self):
        """
        Test should return FleetType model string name

        :return:
        :rtype:
        """

        fleet_type = FleetType(name="Fun Fleet")
        fleet_type.save()

        self.assertEqual(first=str(fleet_type), second="Fun Fleet")
