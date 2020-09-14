# -*- coding: utf-8 -*-

"""
the views
"""

from django import template

register = template.Library()


@register.simple_tag
def set_variable(value):
    """Allows to set a variable in template"""
    return value
