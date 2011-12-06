import xmlrpclib
from cash.models import Expense, SubCategory, PaymentType
from django.conf import settings

class SyncServiceClass(object):

    def __init__(self):
        self.server = xmlrpclib.ServerProxy(settings.RPC_HOST).app
            
    def sync_expenses(self):
        try:
            data = self.server.getData()
        except Exception, e:
            raise
        else:
            if data:
                for e in data:
                    expense = Expense()
                    s = SubCategory.objects.get(pk=e['subCategory'])
                    p = PaymentType.objects.get(pk=e['paymentType'])
                    if e['text']:
                        expense.text = e['text']
                    else:
                        expense.text = s.name
                    expense.subCategory=s
                    expense.paymentType=p
                    expense.date=e['date']
                    expense.amount=e['amount']
                    expense.save()
                return len(data)
            else:
                return 0