# -*- coding: utf-8 -*-

"""
our app setting
"""

import re

from django.conf import settings

from .utils import clean_setting

# set default panels if none are set in local.py
AA_FLEETPINGS_USE_SLACK = clean_setting("AA_FLEETPINGS_USE_SLACK", False)


def get_site_url():  # regex sso url
    """
    get the site url
    :return: string
    """
    regex = r"^(.+)\/s.+"
    matches = re.finditer(regex, settings.ESI_SSO_CALLBACK_URL, re.MULTILINE)
    url = "http://"

    for match in matches:
        url = match.groups()[0]  # first match

    return url


def timezones_installed() -> bool:
    """
    check if aa-timezones is installed
    :return: bool
    """
    return "timezones" in settings.INSTALLED_APPS
