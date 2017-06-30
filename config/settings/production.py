# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import os
import configparser
from django.core.exceptions import ImproperlyConfigured

from .base import *  # noqa

DEBUG = False
ALLOWED_HOSTS = ['127.0.0.1']

config = configparser.ConfigParser()

try:
    config.read(os.path.join(BASE_DIR, 'conf.ini'))  # noqa
except Exception:
    raise ImproperlyConfigured('BASE_DIR/confi.ini not found')

try:
    SECRET_KEY = config['django_keys']['secret_key']
except KeyError:
    raise ImproperlyConfigured(
        "Keys not found. Ensure you have ['django_keys']['secret_key'] properly set.")


INSTALLED_APPS += ['anymail']  # noqa
ANYMAIL = {
    "MAILGUN_API_KEY": config['mailgun']['api_key'],
    "MAILGUN_SENDER_DOMAIN": 'mg.phillydsa.com',
}

EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"
DEFAULT_FROM_EMAIL = "do-not-reply@{0}.com".format(HOST_NAME)  # noqa

GOOGLE_SITE_VERIFICATION = 'w3PEys-WERIs_IaggCLoo9sYZ8WQTMSfawrDYbfMlTc'
GOOGLE_ANALYTICS_KEY = 'UA-101255774-1'
GOOGLE_ANALYTICS_KEY_TESTING = 'UA-101255774-2'
