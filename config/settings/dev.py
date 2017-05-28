# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from .base import *  # noqa

DEBUG = True

SECRET_KEY = '00wh+stv9wh8&w#*+p#6487$(!d!_^8q=u*!+%8)!7gsc=sfe)'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


try:
    from .local import *  # noqa
except ImportError:
    pass
