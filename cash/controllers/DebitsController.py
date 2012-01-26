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
from cash.models import Debits, SubCategory, PaymentType
from cash.services import JsonParser, DateService
from cash.services.RequestUtils import param_exist, sortMethod
from django.db.models import Q
from django.db import IntegrityError
try:
    import _mysql_exceptions
except:
    import cash.exceptions as _mysql_exceptions
from cash.decorators import json_response

@render('cash/debits/index.html')
def index(request):
    return {}

@json_response
def list(request):
    req = request.REQUEST
    q = Debits.objects.filter()
    if param_exist("sort",req):
        q = q.order_by(sortMethod(req))
    if param_exist("limit",req):
        start = req['start']
        limit = req['limit']
        list = q[start:start+limit]
    else:
        list = q

    res = []
    for exp in list:
        res.append({'id': exp.id, 'amount': exp.amount, 'since': exp.since,
                    'text': exp.text, 'paymentType_name': exp.paymentType.name,
                    'subCategory_name': exp.subCategory.name, 'paymentTypeId': exp.paymentType.id,
                    'subCategoryId': exp.subCategory.id,
                    'day': exp.day,'last': exp.last})
                
    data = '{"total": %s, "rows": %s}' % (q.count(), JsonParser.parse(res))
    return data

def req_to_obj(request):
    req = request.REQUEST
    if req.has_key('id'):
        obj = Debits.objects.get(pk=req['id'])
    else:
        obj = Debits()
    obj.day = req['day']
    obj.subCategory = SubCategory.objects.get(pk=req['subCategory.id'])
    obj.paymentType = PaymentType.objects.get(pk=req['paymentType.id'])
    obj.text = req['text']
    obj.amount = req['amount']
    obj.since = DateService.invert(req['since']) 
    return obj
    
@json_response    
def save(request):
    p = req_to_obj(request)
    data = '{"success":true}'
    try:
        p.save()
    except IntegrityError, e:
        print e
        data = '{"success":false, "msg": "%s"}' % (_("Debit '%s' already exists.") % (p.text))
    except _mysql_exceptions.Warning:
        pass
    except Exception, e1:
        data = '{"success":false, "msg": "%s"}' % (e1.args)
    return data
    
@json_response    
def update(request):
    p = req_to_obj(request)
    data = '{"success":true}'
    try:
        p.save()
    except IntegrityError:
        data = '{"success":false, "msg": "%s"}' % (_("Debit '%s' already exists.") % (p.text))
    except _mysql_exceptions.Warning:
        pass
    except Exception, e1:
        data = '{"success":false, "msg": "%s"}' % (e1.args)
    return data

@json_response
def delete(request):
    p = Debits(pk=request.REQUEST['id'])
    try:
        p.delete()
        data = '{"success":true}'
    except Exception, e1:
        data = '{"success":false, "msg": "%s"}' % (e1.args)
    return data
