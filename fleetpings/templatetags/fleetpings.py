"""
Template tags
"""

# Django
from django.template.defaulttags import register

# Alliance Auth
from allianceauth.services.hooks import get_extension_logger

# Alliance Auth (External Libs)
from app_utils.logging import LoggerAddTag
from app_utils.urls import reverse_absolute

# AA Fleet Pings
from fleetpings import __title__

logger = LoggerAddTag(my_logger=get_extension_logger(__name__), prefix=__title__)


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
