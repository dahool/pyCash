from django.utils.translation import ugettext as _
from django.http import HttpResponse
from django.shortcuts import render_to_response
from cash.models import Person
from cash.services import JsonParser
from cash.services.RequestUtils import param_exist, sortMethod
from django.db.models import Q
from django.db import IntegrityError
import _mysql_exceptions

def urls(self):
    urlpatterns = patterns('',
        (r'^list$', self.list),
        (r'^save$', self.save),
        (r'^update$', self.update),
        (r'^delete$', self.delete),
        (r'^$', self.index),    
    )    

def index(request):
    return render_to_response('cash/person/index.html', {})

def list(request):
    req = request.REQUEST
    q = Person.objects.filter()
    if param_exist("sort",req):
        q = q.order_by(sortMethod(req))
    if param_exist("limit",req):
        start = req['start']
        limit = req['limit']
        list = q[start:limit]
    else:
        list = q
    data = '{"total": %s, "rows": %s}' % (Person.objects.count(), JsonParser.parse(list))
    return HttpResponse(data, mimetype='text/javascript;')

def save(request):
    req = request.REQUEST
    p = Person(name=req['name'])
    
    data = '{"success":true}'
    try:
        p.save()
    except IntegrityError:
        data = '{"success":false, msg: "%s"}' % (_("Person '%s' already exists.") % (req['name']))
    except _mysql_exceptions.Warning:
        pass        
    except Exception, e1:
        data = '{"success":false, msg: "%s"}' % (e1.args)  
    return HttpResponse(data, mimetype='text/javascript;')
    
def update(request):
    p = Person(pk=request.REQUEST['id'],name=request.REQUEST['name'])
    
    data = '{"success":true}'
    try:
        p.save()
    except IntegrityError:
        data = '{"success":false, msg: "%s"}' % (_("Person '%s' already exists.") % (req['name']))
    except _mysql_exceptions.Warning:
        pass        
    except Exception, e1:
        data = '{"success":false, msg: "%s"}' % (e1.args)    
    return HttpResponse(data, mimetype='text/javascript;')

def delete(request):
    p = Person(pk=request.REQUEST['id'])
    try:
        p.delete()
        data = '{"success":true}'
    except Exception, e1:
        data = '{"success":false, msg: "%s"}' % (e1.args)     
    return HttpResponse(data, mimetype='text/javascript;')