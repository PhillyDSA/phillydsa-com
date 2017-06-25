# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from .base import *  # noqa

INTERNAL_IPS = (
    'localhost',
    '0.0.0.0',
    '127.0.0.1',
)

DEBUG = True
INSTALLED_APPS += ['template_debug']  # noqa

[t.get('OPTIONS').update({'debug': True}) for t in TEMPLATES]  # noqa

SECRET_KEY = '00wh+stv9wh8&w#*+p#6487$(!d!_^8q=u*!+%8)!7gsc=sfe)'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

ALLOWED_HOSTS = ['*']


try:
    from .local import *  # noqa
except ImportError:
    pass
