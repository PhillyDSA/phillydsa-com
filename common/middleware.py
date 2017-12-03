#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
from django.utils.deprecation import MiddlewareMixin


class CSSCacheCookieMiddleware(MiddlewareMixin):
    """Class for setting cookies."""

    def process_response(self, request, response):
        """Set css_cached cookie for better performance from caching css on 2nd load."""
        max_age = 7 * 24 * 60 * 60  # 7 days
        expires = datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age)
        response.set_cookie('css_cached', True, expires=expires)
        return response
