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

from cash.models import Expense, Debits
from cash.services import JsonParser, DateService
from django.db.models import Q
from datetime import datetime

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

print "Processed %d" % list.count()