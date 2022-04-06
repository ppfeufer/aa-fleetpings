"""
URLs for render in templates

Uses: Allianceauth App Utils
"""

# Django
from django.template.defaulttags import register

# Alliance Auth (External Libs)
from app_utils.urls import reverse_absolute


@register.simple_tag
def fleetpings_reverse_url(view: str, *args) -> str:
    """
    Absolute URL
    :param view:
    :param args:
    :return:
    """

    return reverse_absolute(view, list(args))
