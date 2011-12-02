from django.utils.translation import ugettext as _
from django.http import HttpResponse
from django.shortcuts import render_to_response
from cash.services import JsonParser
from cash.models import Category
from django.db.models import Q
from cash.services.RequestUtils import param_exist, sortMethod
from django.db import IntegrityError
from cash.decorators import json_response

def index(request):
    return render_to_response('cash/category/index.html', {})

@json_response
def list(request):
    req = request.REQUEST
    q = Category.objects.filter()
    if param_exist("sort",req):
        q = q.order_by(sortMethod(req))
    if param_exist("limit",request.REQUEST):
        start = request.REQUEST['start']
        limit = request.REQUEST['limit']
        lst = q[start:limit]
    else:
        lst = q
    data = '{"total": %s, "rows": %s}' % (Category.objects.count(), JsonParser.parse(lst))
    return data

@json_response
def save(request):
    c = Category(name=request.REQUEST['name'])
    try:
        c.save()
        data = '{"success":true}'
    except IntegrityError:
        data = '{"success":false, msg: "%s"}' % (_("Category '%s' already exists.") % (request.REQUEST['name']))
    except Exception, e1:
        data = '{"success":false, msg: "%s"}' % (e1.args)           
    return data
    
@json_response    
def update(request):
    c = Category(pk=request.REQUEST['id'],name=request.REQUEST['name'])
    try:
        c.save()
        data = '{"success":true}'
    except IntegrityError:
        data = '{"success":false, msg: "%s"}' % (_("Category '%s' already exists.") % (request.REQUEST['name']))
    except Exception, e1:
        data = '{"success":false, msg: "%s"}' % (e1.args)           
    return data

@json_response
def delete(request):
    c = Category(pk=request.REQUEST['id'])
    try:
        c.delete()
        data = '{"success":true}'
    except Exception, e1:
        data = '{"success":false, msg: "%s"}' % (e1.args)           
    return data
