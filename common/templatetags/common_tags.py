# -*- coding: utf-8 -*-
from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    """Return value for key in dict."""
    return dictionary.get(key, None)
