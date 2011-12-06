from django.core.management.base import BaseCommand

from cash.models import Tax
from cash.services import JsonParser, DateService, googlecalendar
import datetime
from django.conf import settings

class Command(BaseCommand):
    help = 'Update Events'

    def handle(self, *args, **options):
        if settings.USE_GOOGLE_CAL:
            try:
                calendar = googlecalendar.CalendarHelper(settings.GOOGLE_USER, settings.GOOGLE_PASS)
            except Exception,e:
                self.stdout.write("Unable to connect to calendar service [%s]\n" % str(e))
            else:
                taxlist = Tax.objects.filter(updated=False)
                self.stdout.write("%d items to update\n" % len(taxlist))
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
                        self.stdout.write("Error while saving event %s: %s\n" % (tax.service,str(e1)))
                    else:
                        a += 1
                        tax.gcalId = ev.get_id()
                        tax.updated = True
                        tax.save()
                
                self.stdout.write("%d items updated\n" % a)
        else:
            self.stdout.write("Nothing to do.\n")