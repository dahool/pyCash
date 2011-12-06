import xmlrpclib

from cash.models import PaymentType, Category
from cash.services.SyncService import SyncServiceClass
from django.http import HttpResponse
from django.conf import settings

def service():
    server = xmlrpclib.ServerProxy(settings.RPC_HOST)
    return server.app
    
def cmd_expenses(request):
    sync = SyncServiceClass()
    try:
        r = sync.sync_expenses()
    except Exception, e:
        ret = '{"success":false, err: "%s"}' % (str(e))
    else:
        ret = '{"success":true, value: "%d"}' % (r)
    return HttpResponse(ret, mimetype='text/javascript;')

def cmd_category(request):
    list = Category.objects.all()
    res = []
    for cat in list:
        subs = []
        for sub in cat.subcategory_set.all():
            subs.append({'id':sub.id,
                         'name': sub.name})
        res.append({'id': cat.id,
                    'name': cat.name,
                    'sub': subs
                    })
    try:
        service().setCategories(res)
    except Exception, e:
        ret = '{"success":false, msg: "%s"}' % (str(e))
    else:
        ret = '{"success":true}'
    return HttpResponse(ret, mimetype='text/javascript;')

def cmd_paymenttype(request):
    list = PaymentType.objects.all()
    res = []
    for pt in list:
        res.append({'id': pt.id,
                    'name': pt.name,
                    })
    try:
        service().setPaymentTypes(res)
    except Exception, e:
        ret = '{"success":false, msg: "%s"}' % (str(e))
    else:
        ret = '{"success":true}'
    return HttpResponse(ret, mimetype='text/javascript;')