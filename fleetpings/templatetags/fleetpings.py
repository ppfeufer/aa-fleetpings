"""
Template tags
"""

# Django
from django.template.defaulttags import register

# Alliance Auth
from allianceauth.services.hooks import get_extension_logger

# AA Fleet Pings
from fleetpings import __title__
from fleetpings.helper.urls import reverse_absolute
from fleetpings.providers import AppLogger

logger = AppLogger(my_logger=get_extension_logger(__name__), prefix=__title__)


@register.simple_tag
def fleetpings_reverse_url(view: str, *args) -> str:
    """
    Reverse URL

    :param view:
    :type view:
    :param args:
    :type args:
    :return:
    :rtype:
    """

    return reverse_absolute(viewname=view, args=list(args))
