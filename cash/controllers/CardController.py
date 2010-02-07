from django.utils.translation import ugettext as _
from django.http import HttpResponse
from django.shortcuts import render_to_response
from pyCash.cash.models import Card, PaymentType
from pyCash.cash.services import JsonParser
from pyCash.cash.services.RequestUtils import param_exist, sortMethod
from django.db.models import Q
from django.db import IntegrityError

def index(request):
    return render_to_response('cash/card/index.html', {})

def list(request):
    req = request.REQUEST
    q = Card.objects.filter()
    if param_exist("sort",req):
        q = q.order_by(sortMethod(req))
    if param_exist("limit",req):
        start = req['start']
        limit = req['limit']
        list = q[start:limit]
    else:
        list = q
    data = '{"total": %s, "rows": %s}' % (Card.objects.count(), JsonParser.parse(list))
    return HttpResponse(data, mimetype='text/javascript;')

def save(request):
    req = request.REQUEST
    t = PaymentType(pk=req['paymentType.id'])
    p = Card(name=req['name'].capwords(), paymentType=t)
    data = '{"success":true}'
    try:
        p.save()
    except IntegrityError:
        data = '{"success":false, msg: "%s"}' % (_("Card '%s' already exists.") % (req['name']))
    except _mysql_exceptions.Warning:
        pass
    except Exception, e1:
        data = '{"success":false, msg: "%s"}' % (e1.args)

    return HttpResponse(data, mimetype='text/javascript;')
    
def update(request):
    req = request.REQUEST
    t = PaymentType(pk=req['paymentType.id'])
    p = Card(pk=req['id'],name=req['name'],paymentType=t)
    
    data = '{"success":true}'
    try:
        p.save()
    except IntegrityError:
        data = '{"success":false, msg: "%s"}' % (_("Card '%s' already exists.") % (req['name']))
    except _mysql_exceptions.Warning:
        pass
    except Exception, e1:
        data = '{"success":false, msg: "%s"}' % (e1.args)
    
    return HttpResponse(data, mimetype='text/javascript;')

def delete(request):
    p = Card(pk=request.REQUEST['id'])
    try:
        p.delete()
        data = '{"success":true}'
    except Exception, e1:
        data = '{"success":false, msg: "%s"}' % (e1.args)
    return HttpResponse(data, mimetype='text/javascript;')