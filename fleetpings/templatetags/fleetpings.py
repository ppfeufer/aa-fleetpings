"""
Template tags
"""

# Django
from django.template.defaulttags import register
from django.templatetags.static import static

# Alliance Auth (External Libs)
from app_utils.urls import reverse_absolute

# AA Fleet Pings
from fleetpings import __version__


@register.simple_tag
def fleetpings_reverse_url(view: str, *args) -> str:
    """
    Absolute URL
    :param view:
    :param args:
    :return:
    """

    return reverse_absolute(view, list(args))


@register.simple_tag
def fleetpings_static(path: str) -> str:
    """
    Versioned static URL
    :param path:
    :type path:
    :return:
    :rtype:
    """

    static_url = static(path)
    versioned_url = static_url + "?v=" + __version__

    return versioned_url
