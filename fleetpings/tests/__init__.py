"""
Initialize the tests
"""

# Standard Library
import socket

# Django
from django.test import TestCase


class SocketAccessError(Exception):
    """
    Error raised when a test script accesses the network
    """


class BaseTestCase(TestCase):
    """
    Variation of Django's TestCase class that prevents any network use.

    Example:

        .. code-block:: python

            class TestMyStuff(BaseTestCase):
                def test_should_do_what_i_need(self): ...

    """

    @classmethod
    def setUpClass(cls):
        """
        Set up the test class by replacing the socket.socket method with a guard that raises an error if accessed.

        :return:
        :rtype:
        """

        cls.socket_original = socket.socket
        socket.socket = cls.guard

        return super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        """
        Tear down

        :return:
        :rtype:
        """

        socket.socket = cls.socket_original

        return super().tearDownClass()

    @staticmethod
    def guard(*args, **kwargs):
        """
        Guard method that raises an error if the network is accessed.

        :param args:
        :type args:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """

        raise SocketAccessError("Attempted to access network")
