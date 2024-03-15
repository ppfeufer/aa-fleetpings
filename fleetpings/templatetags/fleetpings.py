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
    Reverse URL

    :param view:
    :type view:
    :param args:
    :type args:
    :return:
    :rtype:
    """

    return reverse_absolute(viewname=view, args=list(args))


@register.simple_tag
def fleetpings_static(path: str) -> str:
    """
    Versioned Static URL

    :param path:
    :type path:
    :return:
    :rtype:
    """

    static_url = static(path=path)
    versioned_url = static_url + "?v=" + __version__

    return versioned_url
