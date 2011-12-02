from django.utils.translation import ugettext as _
from django.http import HttpResponse
from django.shortcuts import render_to_response
from cash.models import CardDates, Card, CardData, Person, Loan
from cash.services import JsonParser, DateService, FinancialService
from cash.services.RequestUtils import param_exist, sortMethod
from django.db.models import Q
from django.db import IntegrityError
import _mysql_exceptions

from django.db import connection

def index(request):
    return render_to_response('cash/cardExpense/index.html', {})

def list(request):
    req = request.REQUEST
    
    # find close date
    
    dateQuery = CardDates.objects.filter(closeDate__gt=DateService.todayDate())
    dateQuery = dateQuery.order_by('closeDate')
    if dateQuery.count()>0:
        dt = dateQuery[:1][0]
    else:
        dt = CardDates(closeDate=DateService.todayDate(), expireDate=DateService.todayDate())
    
    q = CardData.objects.extra(where=["ADDDATE(date, INTERVAL ((instalments+1) * 30) DAY) > '%s'" % DateService.invert(dt.closeDate)])
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
        rem = FinancialService.remainInstalments(exp.date, dt.closeDate, exp.instalments)
        if rem >= 0:
            res.append({'id': exp.id, 'date': exp.date,
                            'shop': exp.shop, 'instalments': exp.instalments,
                            'card_id': exp.card.id, 'card_name': exp.card.name,
                            'total': exp.total, 'own': exp.own,
                            'partial': exp.total / exp.instalments,
                            'remain': rem })
    
    data = '{"total": %s,"close": "%s", "expire": "%s", "rows": %s}' % (CardData.objects.count(), DateService.format(dt.closeDate),DateService.format(dt.expireDate), JsonParser.parse(res))
    return HttpResponse(data, mimetype='text/javascript;')

def fromParams(req):
    if param_exist("id",req):
        e = CardData(pk=req['id'])
    else:
        e = CardData()
    
    c = Card(pk=req['card.id'])
    
    e.date=DateService.invert(req['date'])
    e.shop=req['shop']
    e.instalments=req['instalments']
    e.total=req['total']
    e.card = c
    
    return e

def save(request):
    req = request.REQUEST
    p = fromParams(req);
    
    if param_exist("loan",req):
        p.own = False
    else:
        p.own = True
    
    data = '{"success":true}'
    safe = True
    try:
        p.save()
    except _mysql_exceptions.Warning:
        pass
    except Exception, e1:
        safe = False
        data = '{"success":false, msg: "%s"}' % (e1.args)
        
    if safe:
        if param_exist("addloan",req):
            pe = Person(pk=req['person.id'])
            l = Loan(person=pe, amount=p.total, date=p.date, reason=p.shop)
            try:
                l.save()
            except _mysql_exceptions.Warning:
                pass
            except Exception, e1:
                safe = False
                data = '{"success":false, msg: "%s"}' % (e1.args)
    
    return HttpResponse(data, mimetype='text/javascript;')
    
def update(request):
    req = request.REQUEST
    p = fromParams(req);
    
    data = '{"success":true}'    
    try:
        p.save()
    except _mysql_exceptions.Warning:
        pass
    except Exception, e1:
        data = '{"success":false, msg: "%s"}' % (e1.args)
            
    return HttpResponse(data, mimetype='text/javascript;')

def delete(request):
    p = CardData(pk=request.REQUEST['id'])
    try:
        p.delete()
        data = '{"success":true}'
    except Exception, e1:
        data = '{"success":false, msg: "%s"}' % (e1.args)
    
    return HttpResponse(data, mimetype='text/javascript;')