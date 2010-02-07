from django.utils.translation import ugettext as _
from django.http import HttpResponse
from django.shortcuts import render_to_response
from pyCash.cash.services import JsonParser
from pyCash.cash.models import SubCategory, Category
from django.db.models import Q
from pyCash.cash.services.RequestUtils import param_exist, sortMethod
from django.db import IntegrityError

def list(request):
    req = request.REQUEST
    q = SubCategory.objects.filter()
    if param_exist("filter[0][field]",req):
        q = q.filter(category=req['filter[0][data][value]'])
    if param_exist("sort",req):
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
    return HttpResponse(data, mimetype='text/javascript;')

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
        
    return HttpResponse(data, mimetype='text/javascript;')
    
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
    return HttpResponse(data, mimetype='text/javascript;')

def delete(request):
    s = SubCategory(pk=request.REQUEST['id'])
    try:
        s.delete()
        data = '{"success":true}'
    except:
        data = '{"success":false}'    
    return HttpResponse(data, mimetype='text/javascript;')