from django.core.management.base import BaseCommand

from cash.models import Expense, Debits
from cash.services import JsonParser, DateService
from django.db.models import Q
from datetime import datetime


class Command(BaseCommand):
    help = 'Update Events'

    def handle(self, *args, **options):
        list = Debits.objects.filter(Q(since__lte=datetime.now()) & (Q(last__isnull=True) | Q(last__lt=DateService.firstDateOfMonth(DateService.today()))))
        
        for debit in list:
            Expense.objects.create(text=debit.text,
                                   amount=debit.amount,
                                   subCategory=debit.subCategory,
                                   paymentType=debit.paymentType,
                                   date=DateService.invert(DateService.parse("%d/%d/%d" % (debit.day,
                                                                        DateService.today().tm_mon,
                                                                        DateService.today().tm_year))))
            debit.last = datetime.now()
            debit.save()
        
        self.stdout.write("Processed %d\n" % list.count())