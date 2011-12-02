from django.utils.translation import ugettext as _
from django.http import HttpResponse
from django.shortcuts import render_to_response
from cash.models import Expense, SubCategory, PaymentType, Income
from cash.services import JsonParser, DateService
from django.db.models import Q
import datetime
from cash.services.RequestUtils import param_exist, sortMethod
import _mysql_exceptions
from django.db import connection

def index(request):
    return render_to_response('cash/stats/index.html', {})

def calc(request):
    req = request.REQUEST
    if param_exist("date",req):
        date = DateService.parse(req['date'])
    else:
        date = DateService.today()

    fromDate = DateService.firstDateOfMonth(date)
    toDate = DateService.lastDateOfMonth(date)
    
    q = Expense.objects.filter(date__gte=fromDate, date__lte=toDate)
    if param_exist("subC",req):
        q = q.filter(subCategory=req['subC'])
    elif param_exist("cat",req):
        c = SubCategory.objects.filter(category=req['cat'])
        q = q.filter(subCategory__in=c)
    if param_exist("payT",req):
        q = q.filter(paymentType=req['payT'])
        
    sum=0
    for exp in q:
        sum+=exp.amount
    
    today = DateService.today()
    if today.tm_year==date.tm_year and today.tm_mon==date.tm_mon:
        days=today.tm_mday
    else:
        days=DateService.lastDayOfMonth(date)

    avg = sum / days
    data = '{"data":{"total":%s,"avg":%s}}' % (sum,avg)
    return HttpResponse(data, mimetype='text/javascript;') 

def monthCalc(request):
    req = request.REQUEST
    if param_exist("date",req):
        date = DateService.parse(req['date'])
    else:
        date = DateService.today()

    fromDate = DateService.firstDateOfMonth(date)
    toDate = DateService.lastDateOfMonth(date)
    
    q = Expense.objects.extra(select={'sum': 'sum(amount)'}).values('sum','date')
    #q = Expense.objects.filter(date__gte=fromDate, date__lte=toDate)
    q = q.filter(date__gte=fromDate, date__lte=toDate).order_by('date')
    if param_exist("subC",req):
        q = q.filter(subCategory=req['subC'])
    elif param_exist("cat",req):
        c = SubCategory.objects.filter(category=req['cat'])
        q = q.filter(subCategory__in=c)
    if param_exist("payT",req):
        q = q.filter(paymentType=req['payT'])
    q.query.group_by = ['date']
    
    list = []
    for exp in q:
        list.append('[%d,%s]' % (int(DateService.toLong(exp['date'])),exp['sum']))
    
    data = "[" + ",".join(list) + "]"
    return HttpResponse(data, mimetype='text/javascript;') 

def sixMonthCalc(request):
    req = request.REQUEST
    if param_exist("date",req):
        date = DateService.parse(req['date'])
    else:
        date = DateService.today()

    fromDate = DateService.addMonth(DateService.firstDateOfMonth(date),-6)
    toDate = DateService.lastDateOfMonth(date)
    
    query = "SELECT sum(amount), date FROM expense "\
            "WHERE date between '%s' and '%s'" % (str(fromDate), str(toDate))
    if param_exist("subC",req):
        query += " AND sub_category_id = '%s'" % req['subC']
    elif param_exist("cat",req):
        c = SubCategory.objects.filter(category=req['cat'])
        query += " AND sub_category_id in (%s)" % ",".join(["'"+str(s.id)+"'" for s in c])
    if param_exist("payT",req):
        query += " AND payment_type_id = '%s'" % req['payT']
    query += " group by month(date)"
    
    cursor = connection.cursor()
    cursor.execute(query)
#    q = Expense.objects.extra(select={'sum': 'sum(amount)'}).values('sum','date')
#    q = q.filter(date__gte=fromDate, date__lte=toDate).order_by('date')
#    if param_exist("subC",req):
#        q = q.filter(subCategory=req['subC'])
#    elif param_exist("cat",req):
#        c = SubCategory.objects.filter(category=req['cat'])
#        q = q.filter(subCategory__in=c)
#    if param_exist("payT",req):
#        q = q.filter(paymentType=req['payT'])
#    q.query.group_by = ['month(date)']
    list = []
    for exp in cursor.fetchall():
        sum, date = exp
        i = Income.objects.extra(select={'sum': 'sum(amount)'}).values('sum')
        i = i.filter(period = DateService.firstDateOfMonth(date.timetuple()))
        val = i[0]['sum']
        if val is None:
            val = 0
        list.append({'date': date, 'expense': sum, 'income': val})

    data = '{"rows": %s}' % (JsonParser.parse(list))
    return HttpResponse(data, mimetype='text/javascript;') 

def list(request):
    req = request.REQUEST
    q = Expense.objects.filter()
    if param_exist("amountStart",req):
        q = q.filter(amount__gte=req['amountStart'])
    if param_exist("amountEnd",req):
        q = q.filter(amount__lte=req['amountEnd'])
    if param_exist("dateStart",req):
        q = q.filter(date__gte=DateService.invert(req['dateStart']))
    if param_exist("dateEnd",req):
        q = q.filter(date__lte=DateService.invert(req['dateEnd']))
    if param_exist("subC",req):
        q = q.filter(subCategory=req['subC'])
    elif param_exist("cat",req):
        c = SubCategory.objects.filter(category=req['cat'])
        q = q.filter(subCategory__in=c)
    if param_exist("payT",req):
        q = q.filter(paymentType=req['payT'])
    if param_exist("sort",req):
        q = q.order_by(sortMethod(req))
    if param_exist("limit",req):
        list = q[req['start']:req['limit']]
    else:
        list = q
    
    res = []
    for exp in list:
        res.append({'id': exp.id, 'amount': exp.amount, 'date': exp.date,
                    'text': exp.text, 'paymentType_name': exp.paymentType.name,
                    'subCategory_name': exp.subCategory.name, 'paymentTypeId': exp.paymentType.id,
                    'subCategoryId': exp.subCategory.id})

    data = '{"total": %s, "rows": %s}' % (q.count(), JsonParser.parse(res))
    return HttpResponse(data, mimetype='text/javascript;') 

def fromParams(req):
    s = SubCategory.objects.get(pk=req['subCategory.id'])
    p = PaymentType(pk=req['paymentType.id'])
    if param_exist("text",req):
        text = req['text']
    else:
        text = s.name 

    if param_exist("id",req):
        e = Expense.objects.get(pk=req['id'])
    else:
        e = Expense()
        
    e.text=text
    e.date=DateService.invert(req['date']) 
    e.amount=req['amount']
    e.subCategory=s
    e.paymentType=p
    return e
    
def save(request):
    req = request.REQUEST
    e = fromParams(req)

    data = '{"success":true, msg: "%s"}' % (_('Created expense <b>%(text)s</b> of <b>%(date)s</b>') % {'text':e.text,'date':req['date']})    
    try:
        e.save()
    except _mysql_exceptions.Warning:
        pass
    except Exception, e1:
        data = '{"success":false, msg: "%s"}' % (e1.args)
    
    return HttpResponse(data, mimetype='text/javascript;')

def update(request):
    req = request.REQUEST
    e = fromParams(req)

    data = '{"success":true, msg: "%s"}' % (_('Updated expense <b>%(text)s</b> of <b>%(date)s</b>') % {'text':e.text,'date':req['date']})    
    try:
        e.save()
    except _mysql_exceptions.Warning:
        pass
    except Exception, e1:
        data = '{"success":false, msg: "%s"}' % (e1.args)
    
    return HttpResponse(data, mimetype='text/javascript;')

# TODO
def delete(request):
    e = Expense(pk=request.REQUEST['id'])
    try:
        e.delete()
        data = '{"success":true}'
    except Exception, e1:
        data = '{"success":false, msg: "%s"}' % (e1.args)   
    return HttpResponse(data, mimetype='text/javascript;')