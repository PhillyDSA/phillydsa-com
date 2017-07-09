# -*- coding: utf-8 -*-
from django import template
from django.conf import settings

import pytz

register = template.Library()
TZ = pytz.timezone(settings.TIME_ZONE)


@register.filter
def get_item(dictionary, key):
    """Return value for key in dict."""
    return dictionary.get(key, None)


@register.filter
def zulu_time(date_obj):
    """Return a datetime.datetime obj and return google calendar/zulu formatted time string."""
    dt = date_obj.astimezone(TZ).astimezone(pytz.utc)
    return dt.strftime("%Y%m%dT%H%M00Z")


@register.filter
def strip_double_quotes(text):
    """Return string with double quote marks replaced by single quote marks."""
    return text.replace('"', "'")


@register.filter
def generate_page_title(page):
    """Return a string for use in <title> and <og> tags."""
    title = page.seo_title or page.title
    return '{0} - {1}'.format(page.get_site().site_name, title)
