#!/usr/bin/env python
import os, sys
sys.path.append('/home/gabriel/public_html')

os.environ['DJANGO_SETTINGS_MODULE'] = 'pyCash.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
