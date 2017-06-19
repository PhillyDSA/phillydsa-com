# -*- coding: utf-8 -*-
from django.conf import settings


def global_settings(request):
    """Return values from settings to templates."""
    return {
        'GOOGLE_ANALYTICS': getattr(settings, 'GOOGLE_ANALYTICS', None),
        'GOOGLE_API_KEY': getattr(settings, 'GOOGLE_API_KEY', None),
        'GOOGLE_VERIFICATION_KEY': getattr(settings, 'GOOGLE_SITE_VERIFICATION', None),
    }
