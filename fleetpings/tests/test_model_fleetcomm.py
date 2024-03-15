"""
Tests for model FleetComm
"""

# Django
from django.db.utils import IntegrityError
from django.test import TestCase

# AA Fleet Pings
from fleetpings.models import FleetComm


class TestModelFleetComm(TestCase):
    """
    Testing FleetComm model
    """

    def test_should_return_fleetcomm_model_string_name(self):
        """
        Test should return FleetComm model string name

        :return:
        :rtype:
        """

        test_object = FleetComm(name="Alliance Mumble")
        test_object_with_channel = FleetComm(name="Alliance Mumble", channel="Fleet 1")

        test_object.save()
        test_object_with_channel.save()

        self.assertEqual(first=str(test_object), second="Alliance Mumble")
        self.assertEqual(
            first=str(test_object_with_channel), second="Alliance Mumble » Fleet 1"
        )

    def test_should_throw_integrity_error_for_duplicate_comms_without_channel(self):
        """
        Test should throw an IntegrityError for duplicate comms without a channel

        :return:
        :rtype:
        """

        FleetComm(name="Alliance Mumble").save()

        new_fleetcomm = FleetComm(name="Alliance Mumble")

        with self.assertRaises(expected_exception=IntegrityError):
            new_fleetcomm.save()

    def test_should_throw_integrity_error_for_duplicate_comms_with_channel(self):
        """
        Test should throw an IntegrityError for duplicate comms with a channel

        :return:
        :rtype:
        """

        FleetComm(name="Alliance Mumble", channel="Fleet 1").save()

        new_fleetcomm = FleetComm(name="Alliance Mumble", channel="Fleet 1")

        with self.assertRaises(expected_exception=IntegrityError):
            new_fleetcomm.save()
