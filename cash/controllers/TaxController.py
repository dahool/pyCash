from django.utils.translation import ugettext as _
from django.http import HttpResponse
from django.shortcuts import render_to_response
from pyCash.cash.models import Expense, SubCategory, PaymentType, Tax
from pyCash.cash.services import JsonParser, DateService, googlecalendar
from django.db.models import Q
from pyCash.cash.services.RequestUtils import param_exist, sortMethod
import _mysql_exceptions
import datetime
import time
from django.db import transaction
from pyCash import settings
from pyCash.cash.services.Utils import show_sql, get_logger
import sys
 
def index(request):
    return render_to_response('cash/tax/index.html', {})

def upcoming(request):
    return render_to_response('cash/tax/upcoming.html', {})

def upcomingList(request):
    req = request.REQUEST
    limit = (datetime.datetime.now() + datetime.timedelta(days=5))
    q = Tax.objects.filter(expire__lte=limit)
                         
    res = []
    for it in q:
        res.append({'id': it.id, 'service': it.service, 'expire': it.expire,
                    'amount': it.amount, 'nextExpire': it.nextExpire})

    data = '{"total": %s, "rows": %s}' % (q.count(), JsonParser.parse(res))
    return HttpResponse(data, mimetype='text/javascript;') 

def list(request):
    req = request.REQUEST
    q = Tax.objects.filter()
    if param_exist("sort",req):
        q = q.order_by(sortMethod(req))
    if param_exist("limit",req):
        start = req['start']
        limit = req['limit']
        list = q[start:limit]
    else:
        list = q
            
    res = []
    for it in list:
        res.append({'id': it.id, 'service': it.service, 'expire': it.expire,
                    'amount': it.amount, 'nextExpire': it.nextExpire,
                    'subCategory': it.subCategory.name, 'subCategoryId': it.subCategory.id,
                    'nextExpire': it.nextExpire, 'lastPay': it.lastPay, 'paymentType': it.paymentType.name,
                    'paymentTypeId': it.paymentType.id, 'account': it.account})

    data = '{"total": %s, "rows": %s}' % (q.count(), JsonParser.parse(res))
    return HttpResponse(data, mimetype='text/javascript;')

def save(request):
    req = request.REQUEST
    e = fromParams(req)

    safe = True
    data = '{"success":true, msg: "%s"}' % (_('Created Tax for Service <b>%(service)s</b>') % {'service':e.service})    
    try:
        elem = e.save()
    except _mysql_exceptions.Warning:
        pass
    except Exception, e1:
        safe = False
        data = '{"success":false, msg: "%s"}' % (e1.args)
        
    if safe:
        if settings.USE_GOOGLE_CAL:
            try:
                t = Tax.objects.get(id=elem.id)
                event = googlecalendar.CalendarEvent(title=t.service + ' [$ ' + str(t.amount) + ']',
                                                     start_date=DateService.midNight(t.expire),
                                                     end_date=DateService.midNight(t.expire)+datetime.timedelta(days=1),
                                                     description=t.account)
                calendar = googlecalendar.CalendarHelper(settings.GOOGLE_USER, settings.GOOGLE_PASS)
                ev = calendar.save_event(event)
                t.gcalId = ev.get_id()
                t.save()
            except Exception, e1:
                data = '{"success":true, msg: "%s"}' % (e1.args)
            
    return HttpResponse(data, mimetype='text/javascript;')

def update(request):
    req = request.REQUEST
    o = Tax.objects.get(pk=req['id'])
    e = fromParams(req)

    safe = True
    data = '{"success":true, msg: "%s"}' % (_('Updated Service <b>%(service)s</b>') % {'service':e.service})    
    try:
        e.save()
    except _mysql_exceptions.Warning:
        pass
    except Exception, e1:
        safe = False
        data = '{"success":false, msg: "%s"}' % (e1.args)
    
    if safe:
        if settings.USE_GOOGLE_CAL:
            # ADD TO CALENDAR
            try:
                update_calendar(req['id'])
            except Exception, e1:
                #data = '{"success":true, msg: "%s"}' % (e1.args)
                pass
                    
    return HttpResponse(data, mimetype='text/javascript;')

@transaction.autocommit
def update_calendar(id):
    tax = Tax.objects.get(pk=id)
    calendar = googlecalendar.CalendarHelper(settings.GOOGLE_USER, settings.GOOGLE_PASS)
    event = False

    if tax.gcalId != '':
        event = calendar.get_event(tax.gcalId)

    if event is False:
        event = googlecalendar.CalendarEvent(title=tax.service + ' [$ ' + str(tax.amount) + ']',
                                             start_date=DateService.midNight(tax.expire),
                                             end_date=DateService.midNight(tax.expire)+datetime.timedelta(days=1),
                                             description=tax.account)
    else:
        event.set_title(tax.service + ' [$ ' + str(tax.amount) + ']')
        event.set_start_date(DateService.midNight(tax.expire))
        event.set_end_date(DateService.midNight(tax.expire)+datetime.timedelta(days=1))
        event.set_description(tax.account)
        
    try:
        ev = calendar.save_event(event)
    except Exception, e1:
        get_logger().error(str(e1))
        tax.updated = False
    else:
        tax.gcalId = ev.get_id()
        tax.updated = True
    finally:
        tax.save()
        
def delete(request):
    e = Tax.objects.get(pk=request.REQUEST['id'])
    try:
        if settings.USE_GOOGLE_CAL:
            try:
                if e.gcalId != '':
                    calendar = googlecalendar.CalendarHelper(settings.GOOGLE_USER, settings.GOOGLE_PASS)
                    event = calendar.get_event(e.gcalId)
                    if event is not False:
                        calendar.delete_event(event);
            except:
                pass
        e.delete()
        data = '{"success":true}'
    except Exception, e1:
        data = '{"success":false, msg: "%s"}' % (e1.args)
        
    return HttpResponse(data, mimetype='text/javascript;')
    
def fromParams(req):
    s = SubCategory.objects.get(pk=req['subCategory.id'])
    p = PaymentType(pk=req['paymentType.id'])

    if param_exist("id",req):
        e = Tax.objects.get(pk=req['id'])
    else:
        e = Tax()
        
    e.service=req['service']
    e.amount=req['amount']
    e.expire=DateService.invert(req['expire'])
    if param_exist("nextExpire",req):
        e.nextExpire=DateService.invert(req['nextExpire'])
    if param_exist("lastPay",req):
        e.lastPay=DateService.invert(req['lastPay'])
    e.account=req['account']
    e.subCategory=s
    e.paymentType=p
    return e

@transaction.commit_manually
def pay(request):
    req = request.REQUEST
    e = Tax.objects.get(pk=req['id'])
    if e:
        if param_exist("nextExpire",req):
            e.expire = DateService.invert(req['nextExpire'])
        else:
            e.expire = e.nextExpire
        if param_exist("nextExpire2",req):
            e.nextExpire = DateService.invert(req['nextExpire2'])
        else:
            e.nextExpire = None
        e.amount = req['amount']
        e.lastPay = DateService.todayDate()
        if e.account=="":
            service = e.service
        else:
            service = "%s (%s)" % (e.service, e.account)
        expense = Expense(date=DateService.todayDate(), text=service, amount=e.amount, subCategory=e.subCategory, paymentType=e.paymentType)
        
        data = '{"success":true}'
        
        safe = True
        try:
            e.save()
        except _mysql_exceptions.Warning:
            pass
        except Exception, e1:
            safe = False
            transaction.rollback()
            data = '{"success":false, msg: "%s"}' % (e1.args)
        
        if safe:
            try:
                expense.save()
                transaction.commit()
            except _mysql_exceptions.Warning:
                transaction.commit()
            except Exception, e2:
                safe = False
                transaction.rollback()
                data = '{"success":false, msg: "%s"}' % (e2.args)

        if safe:
            if settings.USE_GOOGLE_CAL:
                # ADD TO CALENDAR
                try:
                    update_calendar(req['id'])
                except Exception, e1:
                    #data = '{"success": true, msg: "%s"}' % (e1.args)
                    pass        
        
    return HttpResponse(data, mimetype='text/javascript;') 

    
