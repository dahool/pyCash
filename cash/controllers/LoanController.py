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
from cash.models import Person, Loan, Payment
from cash.services import JsonParser, DateService
from cash.services.RequestUtils import param_exist, sortMethod
from django.db.models import Q
from django.db import IntegrityError, connection
try:
    import _mysql_exceptions
except:
    import cash.exceptions as _mysql_exceptions
from cash.decorators import json_response

@render('cash/loan/index.html')
def index(request):
    return {}

@json_response
def list(request):
    req = request.REQUEST
    q = Loan.objects.filter()
    if param_exist("person.id",req):
        q = q.filter(person=req['person.id'])    
    if param_exist("sort",req):
        q = q.order_by(sortMethod(req))
    if param_exist("limit",req):
        start = int(req['start'])
        limit = int(req['limit'])
        #list = q[start:limit]
        list = q
    else:
        list = q
        
    if param_exist("all",req):
        showAll = True
    else:
        showAll = False
         
    res = []
    for exp in list:
        cursor = connection.cursor()
        cursor.execute("SELECT sum(amount) as sum FROM payment WHERE loan_id = %s", [exp.id])
        row = cursor.fetchone()
        sum = exp.amount
        if row[0]!=None:
            sum = exp.amount - row[0]
        
        if sum == 0:
            partial = 0
        else:
            partial = exp.amount / exp.instalments 
        if sum < partial:
            partial = sum
             
        if showAll or sum > 0:
            res.append({'id': exp.id, 'amount': exp.amount, 'date': exp.date,
                        'reason': exp.reason, 'person': exp.person.name, 'instalments': exp.instalments,
                        'personId': exp.person.id, 'balance': sum, 'partial': partial})
    
    data = '{"total": %s, "rows": %s}' % (len(res), JsonParser.parse(res[start:limit]))
    return data

@json_response
def save(request):
    req = request.REQUEST
    p = Person(pk=req['person.id'])
    l = Loan(person=p,amount=req['amount'],date=DateService.invert(req['date']), reason=req['reason'], remain=req['amount'])
    
    if param_exist("instalments",req):
        l.instalments = req['instalments']
    else:
        l.instalments = 1
            
    data = '{"success":true}'
    try:
        l.save()
    except _mysql_exceptions.Warning:
        pass        
    except Exception, e1:
        data = '{"success":false, "msg": "%s"}' % (e1.args)  
    return data
    

def from_request(request):
    req = request.REQUEST
    p = Person(pk=req['person.id'])
    l = Loan(person=p,amount=req['amount'],date=DateService.invert(req['date']), reason=req['reason'], remain=req['amount'])
    if param_exist("id",req):
        l.pk = req['id']

    if param_exist("instalments",req):
        l.instalments = req['instalments']
    else:
        l.instalments = 1
    
    return l

@json_response
def save_or_update(request):
    l = from_request(request)
    data = '{"success":true}'
    try:
        l.save()
    except _mysql_exceptions.Warning:
        pass        
    except Exception, e1:
        data = '{"success":false, "msg": "%s"}' % (e1.args)    
    return data

@json_response
def update(request):
    req = request.REQUEST
    p = Person(pk=req['person.id'])
    l = Loan(pk=req['id'],person=p,amount=req['amount'],date=DateService.invert(req['date']), reason=req['reason'])

    if param_exist("instalments",req):
        l.instalments = req['instalments']
    else:
        l.instalments = 1
            
    data = '{"success":true}'
    try:
        l.save()
    except _mysql_exceptions.Warning:
        pass        
    except Exception, e1:
        data = '{"success":false, "msg": "%s"}' % (e1.args)    
    return data

@json_response
def delete(request):
    l = Loan(pk=request.REQUEST['id'])
    try:
        l.delete()
        data = '{"success":true}'
    except Exception, e1:
        data = '{"success":false, "msg": "%s"}' % (e1.args)     
    return data
