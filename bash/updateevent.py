#!/usr/bin/python
import sys
import os

PATH = os.path.normpath(os.path.abspath(os.path.dirname(__file__)))
root, path = os.path.split(PATH)
sys.path.append(root)

# django settings setup
from django.core.management import setup_environ

try:
    import settings
except ImportError:
    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n(If the file settings.py does indeed exist, it's causing an ImportError somehow.)\n" % __file__)
    sys.exit(1)

setup_environ(settings)
# -- * --

from cash.models import Tax
from cash.services import JsonParser, DateService, googlecalendar
import datetime

if settings.USE_GOOGLE_CAL:
    try:
        calendar = googlecalendar.CalendarHelper(settings.GOOGLE_USER, settings.GOOGLE_PASS)
    except Exception,e:
        print "Unable to connect to calendar service [%s]" % str(e)
    else:
        taxlist = Tax.objects.filter(updated=False)
        print "%d items to update" % len(taxlist)
        a = 0
        for tax in taxlist:
            event = None
            if tax.gcalId != '':
                event = calendar.get_event(tax.gcalId)
            
            if not event:
                event = googlecalendar.CalendarEvent(title=tax.service + ' [$ ' + str(tax.amount) + ']',
                                                     start_date=DateService.midNight(tax.expire),
                                                     end_date=DateService.midNight(tax.expire)+datetime.timedelta(days=1),
                                                     description=tax.account)
            else:
                event.set_title(tax.service + ' [$ ' + str(tax.amount) + ']')
                event.set_start_date(DateService.midNight(tax.expire))
                event.set_end_date(DateService.midNight(tax.expire)+datetime.timedelta(days=1))
                event.set_description(tax.account)
            
            try:
                ev = calendar.save_event(event)
            except Exception, e1:
                print "Error while saving event %s: %s" % (tax.service,str(e1))
            else:
                a += 1
                tax.gcalId = ev.get_id()
                tax.updated = True
                tax.save()
        
        print "%d items updated" % a
else:
    print "Nothing to do."