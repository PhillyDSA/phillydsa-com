# -*- coding: utf-8 -*-
from django.db import models

from wagtail.contrib.settings.models import BaseSetting, register_setting


@register_setting
class SocialMediaSettings(BaseSetting):
    """Set social media urls for site.

    These profiles are exported to JSON+LD for structured data.
    """

    facebook = models.URLField(blank=True, help_text='Your Facebook page URL')
    twitter = models.URLField(blank=True, help_text='Your twitter profile URL')
    instagram = models.URLField(blank=True, help_text='Your Instagram profile URL')
    youtube = models.URLField(blank=True, help_text='Your YouTube channel or user account URL')


@register_setting
class SEOSettings(BaseSetting):
    """Set site name and description for use with structured data."""

    organization_name = models.CharField(max_length=255, help_text='The actual name of your local (ie. Philly DSA')
    logo = models.URLField(help_text='The URL of the logo of your local')
    description = models.CharField(max_length=500, help_text='A short description of your local. City, what you are trying to achieve, etc.')
