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
from cash.models import Income
from cash.services import JsonParser, DateService
from django.db.models import Q
from django.db.models import Sum
from cash.services.RequestUtils import param_exist, sortMethod
try:
    import _mysql_exceptions
except:
    import cash.exceptions as _mysql_exceptions
import datetime
from cash.decorators import json_response

@render('cash/income/index.html')
def index(request):
    return {}

@json_response
def stats(request):
    req = request.REQUEST
    toDate = DateService.today()
    fromDate = datetime.date(toDate.tm_year, toDate.tm_mon, 1)
    fromDate = DateService.addMonth(fromDate,-12)
    toDate = datetime.date(toDate.tm_year, toDate.tm_mon, 1)
    
    q = Income.objects.values('period').annotate(sum=Sum('amount'))
    q = q.filter(period__gte=fromDate, period__lte=toDate).order_by('period')
    
#    q = Income.objects.extra(select={'sum': 'sum(amount)'}).values('sum','period')
#    q = q.filter(period__gte=fromDate, period__lte=toDate).order_by('period')
#    q.query.group_by = ['period']
        
    #q = Income.objects.filter(period__gte=fromDate, period__lte=toDate).order_by('period')
    
    list = []
    for exp in q:
        #list.append('[%d,%s]' % (int(DateService.toLong(exp.period)),exp.amount))
        list.append('[%d,%s]' % (int(DateService.toLong(exp['period'])),exp['sum']))
        
    data = "[" + ",".join(list) + "]"
    return data 

@json_response
def list(request):
    req = request.REQUEST
    q = Income.objects.filter()
    if param_exist("sort",req):
        q = q.order_by(sortMethod(req))
    if param_exist("limit",req):
        start = req['start']
        limit = req['limit']
        list = q[start:start+limit]
    else:
        list = q
    data = '{"total": %s, "rows": %s}' % (Income.objects.count(), JsonParser.parse(list))
    return data

@json_response
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
        data = '{"success":false, "msg": "%s"}' % (e1.args)
            
    return data
    
@json_response    
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
        data = '{"success":false, "msg": "%s"}' % (e1.args)

    return data

@json_response
def delete(request):
    p = Income(pk=request.REQUEST['id'])
    try:
        p.delete()
        data = '{"success":true}'
    except Exception, e1:
        data = '{"success":false, "msg": "%s"}' % (e1.args)

    return data
