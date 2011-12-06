#!/usr/bin/env python
import os, sys
sys.path.insert(0,'/home/gabriel/public_html/pyCash')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
