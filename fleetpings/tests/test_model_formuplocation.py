"""
Tests for model FormupLocation
"""

# Django
from django.test import TestCase

# AA Fleet Pings
from fleetpings.models import FormupLocation


class TestModelFormupLocation(TestCase):
    """
    Testing the FormupLocation model
    """

    def test_should_return_formuplocation_model_string_name(self):
        """
        Test should return the FormupLocation model string name
        :return:
        :rtype:
        """

        test_object = FormupLocation(name="Alliance HQ")
        test_object.save()

        self.assertEqual(str(test_object), "Alliance HQ")
