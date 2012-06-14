# -*- coding: utf-8 -*-
"""Copyright (c) 2011 Sergio Gabriel Teves
All rights reserved.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
from common.view.decorators import render

from django.utils.translation import ugettext as _
from django.http import HttpResponse
from django.shortcuts import render_to_response
from cash.models import Expense, SubCategory, PaymentType
from cash.services import JsonParser, DateService
from django.db.models import Q
from cash.services.RequestUtils import param_exist, sortMethod
try:
    import _mysql_exceptions
except:
    import cash.exceptions as _mysql_exceptions
from cash.decorators import json_response

from django.core import validators
from django.core.exceptions import ValidationError

@render('cash/expense/index.html')
def index(request):
    return {}

@render('cash/expense/stats.html')
def stats(request):
    return {}

@json_response
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
    return data

@json_response
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
    return data

@json_response
def sixMonthCalc(request):
    req = request.REQUEST
    if param_exist("date",req):
        date = DateService.parse(req['date'])
    else:
        date = DateService.today()

    fromDate = DateService.addMonth(DateService.firstDateOfMonth(date),-6)
    toDate = DateService.lastDateOfMonth(date)
    
    q = Expense.objects.extra(select={'sum': 'sum(amount)'}).values('sum','date')
    q = q.filter(date__gte=fromDate, date__lte=toDate).order_by('date')
    if param_exist("subC",req):
        q = q.filter(subCategory=req['subC'])
    elif param_exist("cat",req):
        c = SubCategory.objects.filter(category=req['cat'])
        q = q.filter(subCategory__in=c)
    if param_exist("payT",req):
        q = q.filter(paymentType=req['payT'])
    q.query.group_by = ['month(date)']
    
    list = []
    for exp in q:
        list.append('[%d,%s]' % (DateService.toLong(exp['date']),exp['sum']))

    data = "[" + ",".join(list) + "]"
    return data

@json_response
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
        list = q[req['start']:req['start']+req['limit']]
    else:
        list = q
    
    res = []
    for exp in list:
        res.append({'id': exp.id, 'amount': exp.amount, 'date': exp.date,
                    'text': exp.text, 'paymentType_name': exp.paymentType.name,
                    'subCategory_name': exp.subCategory.name, 'paymentTypeId': exp.paymentType.id,
                    'subCategoryId': exp.subCategory.id})

    data = '{"total": %s, "rows": %s}' % (q.count(), JsonParser.parse(res))
    return data

def fromParams(req):
    if not req['date']:
        raise ValidationError(_('Enter a valid date'))
        
    amount = req['amount']
    number = validators.RegexValidator('^([0-9])+(\.[0-9]{1,2})?$', message=_('Enter a valid amount'))
    number(amount)
    
    if not amount or float(amount) == 0.0:
        raise ValidationError(_('Enter a valid amount'))

    try:
        s = SubCategory.objects.get(pk=req['subCategory.id'])
    except SubCategory.DoesNotExist:
        raise ValidationError(_('Select a valid category'))
    try:
        p = PaymentType.objects.get(pk=req['paymentType.id'])
    except PaymentType.DoesNotExist:
        raise ValidationError(_('Select a valid payment type'))
        
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
    e.amount=amount
    e.subCategory=s
    e.paymentType=p
    return e

@json_response
def save_or_update(request):
    req = request.REQUEST
    try:
        e = fromParams(req)
    except ValidationError, e:
        data = '{"success":false, "msg": "%s"}' % ("".join(e.messages))
        return data
        
    if e.id:
        data = '{"success":true, "msg": "%s"}' % (_('Updated expense <b>%(text)s</b> for <b>%(date)s</b>') % {'text':e.text,'date':req['date']})
    else:
        data = '{"success":true, "msg": "%s"}' % (_('Created expense <b>%(text)s</b> for <b>%(date)s</b>') % {'text':e.text,'date':req['date']})
        
    try:
        e.save()
    except _mysql_exceptions.Warning:
        pass
    except Exception, e1:
        data = '{"success":false, "msg": "%s"}' % (e1.args)
    
    return data

@json_response
def delete(request):
    e = Expense(pk=request.REQUEST['id'])
    try:
        e.delete()
        data = '{"success":true}'
    except Exception, e1:
        data = '{"success":false, "msg": "%s"}' % (e1.args)   
    return data
