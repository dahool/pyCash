from django.utils.translation import ugettext as _
from django.http import HttpResponse
from django.shortcuts import render_to_response
from cash.models import Debits, SubCategory, PaymentType
from cash.services import JsonParser, DateService
from cash.services.RequestUtils import param_exist, sortMethod
from django.db.models import Q
from django.db import IntegrityError
import _mysql_exceptions

def index(request):
    return render_to_response('cash/debits/index.html', {})

def list(request):
    req = request.REQUEST
    q = Debits.objects.filter()
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
        res.append({'id': exp.id, 'amount': exp.amount, 'since': exp.since,
                    'text': exp.text, 'paymentType_name': exp.paymentType.name,
                    'subCategory_name': exp.subCategory.name, 'paymentTypeId': exp.paymentType.id,
                    'subCategoryId': exp.subCategory.id,
                    'day': exp.day,'last': exp.last})
                
    data = '{"total": %s, "rows": %s}' % (q.count(), JsonParser.parse(res))
    return HttpResponse(data, mimetype='text/javascript;')

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
    
def save(request):
    p = req_to_obj(request)
    data = '{"success":true}'
    try:
        p.save()
    except IntegrityError, e:
        print e
        data = '{"success":false, msg: "%s"}' % (_("Debit '%s' already exists.") % (p.text))
    except _mysql_exceptions.Warning:
        pass
    except Exception, e1:
        data = '{"success":false, msg: "%s"}' % (e1.args)
    return HttpResponse(data, mimetype='text/javascript;')
    
def update(request):
    p = req_to_obj(request)
    data = '{"success":true}'
    try:
        p.save()
    except IntegrityError:
        data = '{"success":false, msg: "%s"}' % (_("Debit '%s' already exists.") % (p.text))
    except _mysql_exceptions.Warning:
        pass
    except Exception, e1:
        data = '{"success":false, msg: "%s"}' % (e1.args)
    return HttpResponse(data, mimetype='text/javascript;')

def delete(request):
    p = Debits(pk=request.REQUEST['id'])
    try:
        p.delete()
        data = '{"success":true}'
    except Exception, e1:
        data = '{"success":false, msg: "%s"}' % (e1.args)

    return HttpResponse(data, mimetype='text/javascript;')