"""
Tests for model FleetDoctrine
"""

# Django
from django.core.exceptions import ValidationError
from django.test import TestCase

# AA Fleet Pings
from fleetpings.models import FleetDoctrine


class TestModelFleetDoctrine(TestCase):
    """
    Testing the FleetDoctrine model
    """

    def test_should_return_fleetdoctrine_model_string_name(self):
        """
        Test should return FleetDoctrine model string name

        :return:
        :rtype:
        """

        doctrine = FleetDoctrine(name="Awesome Ships")
        doctrine.save()

        self.assertEqual(first=str(doctrine), second="Awesome Ships")

    def test_doctrine_link_should_throw_exception(self):
        """
        Test if we get a ValidationError for a doctrine link that is not valid

        :return:
        :rtype:
        """

        # given
        doctrine = FleetDoctrine(
            name="Awesome Doctrine", link="htp://invalid-doctrine.url"
        )

        # when
        with self.assertRaises(expected_exception=ValidationError):
            doctrine.clean()

        with self.assertRaisesMessage(
            expected_exception=ValidationError,
            expected_message="Your doctrine URL is not valid.",
        ):
            doctrine.clean()
