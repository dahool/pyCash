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
from cash.services import JsonParser
from cash.models import SubCategory, Category
from django.db.models import Q
from cash.services.RequestUtils import param_exist, sortMethod
from django.db import IntegrityError
from cash.decorators import json_response

@json_response
def list(request):
    req = request.REQUEST
    q = SubCategory.objects.filter()
    if param_exist("filter[0][field]",req):
        q = q.filter(category=req['filter[0][data][value]'])
    if param_exist("sort",req):
        if req['sort'] == "category":
            q = q.order_by(sortMethod(req,"category__name"), "name")
        else:
            q = q.order_by(sortMethod(req))
    if param_exist("limit",request.REQUEST):
        start = request.REQUEST['start']
        limit = request.REQUEST['limit']
        list = q[start:limit]
    else:
        list = q
        
    res = []
    for elem in list:
        res.append({'id': elem.id, 'name': elem.name, 'category': elem.category.name,
                    'categoryId': elem.category.id})
        
    data = '{"total": %s, "rows": %s}' % (SubCategory.objects.count(), JsonParser.parse(res))
    return data

@json_response
def save(request):
    c = Category(pk=request.REQUEST['category.id'])
    try:
        s = SubCategory.objects.get(name=request.REQUEST['name'], category=c)
    except:
        s = SubCategory(name=request.REQUEST['name'], category=c)
        try:
            s.save()
            data = '{"success":true}'
        except IntegrityError:
            data = '{"success":false, msg: "%s"}' % (_("Sub Category '%s' already exists.") % (request.REQUEST['name']))
        except:
            data = '{"success":true}'
            #s = SubCategory.objects.get(name=request.REQUEST['name'])
    else:
        data = '{"success":false, msg: "%s"}' % (_("Sub Category '%s' already exists.") % (request.REQUEST['name']))
        
    return data
    
@json_response    
def update(request):
    c = Category(pk=request.REQUEST['category.id'])
    s = SubCategory(pk=request.REQUEST['id'],name=request.REQUEST['name'], category=c)
    try:
        s.save()
        data = '{"success":true}'
    except IntegrityError:
        data = '{"success":false, msg: "%s"}' % (_("Sub Category '%s' already exists.") % (request.REQUEST['name']))
    except:
        data = '{"success":true}' 
    return data

@json_response
def delete(request):
    s = SubCategory(pk=request.REQUEST['id'])
    try:
        s.delete()
        data = '{"success":true}'
    except:
        data = '{"success":false}'    
    return data
