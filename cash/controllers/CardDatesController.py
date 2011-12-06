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
from django.utils.translation import ugettext as _
from django.http import HttpResponse
from django.shortcuts import render_to_response
from cash.models import CardDates, Card
from cash.services import JsonParser, DateService
from cash.services.RequestUtils import param_exist, sortMethod
from django.db.models import Q
from django.db import IntegrityError
from cash.decorators import json_response
try:
    import _mysql_exceptions
except:
    import cash.exceptions as _mysql_exceptions
    
@json_response
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
    return data

@json_response
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
        data = '{"success":false, "msg": "%s"}' % (e1.args)
        
    return data
    
@json_response    
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
        data = '{"success":false, "msg": "%s"}' % (e1.args)
            
    return data

@json_response
def delete(request):
    p = CardDates(pk=request.REQUEST['id'])
    try:
        p.delete()
        data = '{"success":true}'
    except Exception, e1:
        data = '{"success":false, "msg": "%s"}' % (e1.args)
    
    return data