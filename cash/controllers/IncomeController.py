from django.utils.translation import ugettext as _
from django.http import HttpResponse
from django.shortcuts import render_to_response
from cash.models import Income
from cash.services import JsonParser, DateService
from django.db.models import Q
from cash.services.RequestUtils import param_exist, sortMethod
import _mysql_exceptions
import datetime

def index(request):
    return render_to_response('cash/income/index.html', {})

def stats(request):
    req = request.REQUEST
    toDate = DateService.today()
    fromDate = datetime.date(toDate.tm_year, toDate.tm_mon, 1)
    fromDate = DateService.addMonth(fromDate,-12)
    toDate = datetime.date(toDate.tm_year, toDate.tm_mon, 1)
    
    
    q = Income.objects.extra(select={'sum': 'sum(amount)'}).values('sum','period')
    #q = Expense.objects.filter(date__gte=fromDate, date__lte=toDate)
    q = q.filter(period__gte=fromDate, period__lte=toDate).order_by('period')
    q.query.group_by = ['period']
        
    #q = Income.objects.filter(period__gte=fromDate, period__lte=toDate).order_by('period')
    
    list = []
    for exp in q:
        #list.append('[%d,%s]' % (int(DateService.toLong(exp.period)),exp.amount))
        list.append('[%d,%s]' % (int(DateService.toLong(exp['period'])),exp['sum']))
        
    data = "[" + ",".join(list) + "]"
    return HttpResponse(data, mimetype='text/javascript;') 

def list(request):
    req = request.REQUEST
    q = Income.objects.filter()
    if param_exist("sort",req):
        q = q.order_by(sortMethod(req))
    if param_exist("limit",req):
        start = req['start']
        limit = req['limit']
        list = q[start:limit]
    else:
        list = q
    data = '{"total": %s, "rows": %s}' % (Income.objects.count(), JsonParser.parse(list))
    return HttpResponse(data, mimetype='text/javascript;')

def save(request):
    req = request.REQUEST
    dt = DateService.parse(req['period']) 
    dt = datetime.date(dt.tm_year, dt.tm_mon, 1)
    p = Income(period=dt, amount=req['amount'])
    
    try:
        data = '{"success":true}'
        p.save()
    except _mysql_exceptions.Warning:
        pass
    except Exception, e1:
        data = '{"success":false, msg: "%s"}' % (e1.args)
            
    return HttpResponse(data, mimetype='text/javascript;')
    
def update(request):
    req = request.REQUEST
    dt = DateService.parse(req['period']) 
    dt = datetime.date(dt.tm_year, dt.tm_mon, 1)
    p = Income(pk=request.REQUEST['id'],period=dt, amount=req['amount'])
    try:
        data = '{"success":true}'
        p.save()
    except _mysql_exceptions.Warning:
        pass
    except Exception, e1:
        data = '{"success":false, msg: "%s"}' % (e1.args)

    return HttpResponse(data, mimetype='text/javascript;')

def delete(request):
    p = Income(pk=request.REQUEST['id'])
    try:
        p.delete()
        data = '{"success":true}'
    except Exception, e1:
        data = '{"success":false, msg: "%s"}' % (e1.args)

    return HttpResponse(data, mimetype='text/javascript;')
