# -*- coding: utf-8 -*-
import datetime
import json

from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

import pytz

from common.site_settings import (
    SEOSettings,
    SocialMediaSettings
)

register = template.Library()
TZ = pytz.timezone(settings.TIME_ZONE)


@register.filter
def get_item(dictionary, key):
    """Return value for key in dict."""
    return dictionary.get(key, None)


@register.filter
def zulu_time(date_obj):
    """Return a datetime.datetime obj and return google calendar/zulu formatted time string."""
    if isinstance(date_obj, datetime.date):
        date_obj = datetime.datetime.combine(date_obj, datetime.time.min)
    dt = date_obj.astimezone(TZ).astimezone(pytz.utc)
    return dt.strftime("%Y%m%dT%H%M00Z")


@register.filter
def strip_double_quotes(text):
    """Return string with double quote marks replaced by single quote marks."""
    return text.replace('"', "'").strip()


@register.filter
def generate_page_title(page):
    """Return a string for use in <title> and <og> tags."""
    try:
        title = page.seo_title or page.title
    except AttributeError as e:
        return ""
    return '{0} - {1}'.format(page.get_site().site_name, title)


@register.simple_tag
def organization_jsonld(request, logo='original', **kwargs):
    """Return JSON+LD for social media and SEO structured data."""
    social_media_settings = SocialMediaSettings.for_site(request.site)
    seo_settings = SEOSettings.for_site(request.site)

    if logo == 'original':
        logo = seo_settings.logo
    elif logo == 'wide':
        logo = seo_settings.logo_wide
    else:
        raise Exception(f'Unsupported logo: {logo}')
    try:
        logo_url = f'{request.site.root_url}{seo_settings.logo_wide.get_rendition(filter="original").url}'
        height, width = logo.height, logo.width
    except AttributeError:
        logo_url, height, width = None, None, None
    json_ld = {
        '@context': "http://schema.org",
        '@type': 'Organization',
        'name': request.site.site_name,
        'url': request.site.root_url,
        'logo': {
            '@type': "ImageObject",
            'url': logo_url,
            'height': height,
            'width': width
        },
        'sameAs': [
            social_media_settings.facebook,
            social_media_settings.twitter,
            social_media_settings.instagram,
            social_media_settings.youtube
        ],
        'description': strip_double_quotes(seo_settings.description)
    }
    return mark_safe(json.dumps(json_ld, indent=4))
