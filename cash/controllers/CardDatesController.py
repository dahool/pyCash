from django.utils.translation import ugettext as _
from django.http import HttpResponse
from django.shortcuts import render_to_response
from pyCash.cash.models import CardDates, Card
from pyCash.cash.services import JsonParser, DateService
from pyCash.cash.services.RequestUtils import param_exist, sortMethod
from django.db.models import Q
from django.db import IntegrityError

def list(request):
    req = request.REQUEST
    q = CardDates.objects.filter()
    if param_exist("sort",req):
        q = q.order_by(sortMethod(req))
    if param_exist("limit",req):
        start = req['start']
        limit = req['limit']
        list = q[start:limit]
    else:
        list = q

    res = []
    for exp in list:
        res.append({'id': exp.id, 'closeDate': exp.closeDate,
                    'expireDate': exp.expireDate, 'card': exp.card.name,
                    'card_id': exp.card.id})
    
    data = '{"total": %s, "rows": %s}' % (CardDates.objects.count(), JsonParser.parse(res))
    return HttpResponse(data, mimetype='text/javascript;')

def save(request):
    req = request.REQUEST
    c = Card(pk=req['card.id'])
    p = CardDates(closeDate=DateService.invert(req['closeDate']),
                    expireDate=DateService.invert(req['expireDate']),
                    card=c)
    
    data = '{"success":true}'
    try:
        p.save()
    except _mysql_exceptions.Warning:
        pass
    except Exception, e1:
        data = '{"success":false, msg: "%s"}' % (e1.args)
        
    return HttpResponse(data, mimetype='text/javascript;')
    
def update(request):
    req = request.REQUEST
    c = Card(pk=req['card.id'])
    p = CardDates(pk=req['id'],closeDate=DateService.invert(req['closeDate']),
                    expireDate=DateService.invert(req['expireDate']),
                    card=c)
    
    data = '{"success":true}'    
    try:
        p.save()
    except _mysql_exceptions.Warning:
        pass
    except Exception, e1:
        data = '{"success":false, msg: "%s"}' % (e1.args)
            
    return HttpResponse(data, mimetype='text/javascript;')

def delete(request):
    p = CardDates(pk=request.REQUEST['id'])
    try:
        p.delete()
        data = '{"success":true}'
    except Exception, e1:
        data = '{"success":false, msg: "%s"}' % (e1.args)
    
    return HttpResponse(data, mimetype='text/javascript;')