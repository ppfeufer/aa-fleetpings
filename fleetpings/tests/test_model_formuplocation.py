"""
Tests for model FormupLocation
"""

# AA Fleet Pings
from fleetpings.models import FormupLocation
from fleetpings.tests import BaseTestCase


class TestModelFormupLocation(BaseTestCase):
    """
    Testing the FormupLocation model
    """

    def test_should_return_formuplocation_model_string_name(self):
        """
        Test should return FormupLocation model string name

        :return:
        :rtype:
        """

        test_object = FormupLocation(name="Alliance HQ")
        test_object.save()

        self.assertEqual(first=str(test_object), second="Alliance HQ")
