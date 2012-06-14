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
from cash.models import Person
from cash.services import JsonParser
from cash.services.RequestUtils import param_exist, sortMethod
from django.db.models import Q
from django.db import IntegrityError
try:
    import _mysql_exceptions
except:
    import cash.exceptions as _mysql_exceptions
from cash.decorators import json_response

#def urls(self):
#    urlpatterns = patterns('',
#        (r'^list$', self.list),
#        (r'^save$', self.save),
#        (r'^update$', self.update),
#        (r'^delete$', self.delete),
#        (r'^$', self.index),    
#    )    

@render('cash/person/index.html')
def index(request):
    return {}

@json_response
def list(request):
    req = request.REQUEST
    q = Person.objects.filter()
    if param_exist("sort",req):
        q = q.order_by(sortMethod(req))
    if param_exist("limit",req):
        start = req['start']
        limit = req['limit']
        list = q[start:start+limit]
    else:
        list = q
    data = '{"total": %s, "rows": %s}' % (Person.objects.count(), JsonParser.parse(list))
    return data

@json_response
def save(request):
    req = request.REQUEST
    name=req['name']
    if not name or name.strip() == '':
        return '{"success":false, "msg": "%s"}' % _("Name is required.")  
    p = Person(name=name)
    data = '{"success":true, "msg": "%s"}' % (_("Saved '%s'.") % (name))
    try:
        p.save()
    except IntegrityError:
        data = '{"success":false, "msg": "%s"}' % (_("Person '%s' already exists.") % (name))
    except _mysql_exceptions.Warning:
        pass        
    except Exception, e1:
        data = '{"success":false, "msg": "%s"}' % (e1.args)  
    return data

@json_response    
def update(request):
    p = Person(pk=request.REQUEST['id'],name=request.REQUEST['name'])
    data = '{"success":true}'
    try:
        p.save()
    except IntegrityError:
        data = '{"success":false, "msg": "%s"}' % (_("Person '%s' already exists.") % (p.name))
    except _mysql_exceptions.Warning:
        pass        
    except Exception, e1:
        data = '{"success":false, "msg": "%s"}' % (e1.args)    
    return data

@json_response
def delete(request):
    p = Person(pk=request.REQUEST['id'])
    try:
        p.delete()
        data = '{"success":true}'
    except Exception, e1:
        data = '{"success":false, "msg": "%s"}' % (e1.args)     
    return data
