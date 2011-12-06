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
from cash.models import Expense, SubCategory, PaymentType, Tax
from cash.services import JsonParser, DateService, googlecalendar
from django.db.models import Q
from cash.services.RequestUtils import param_exist, sortMethod
try:
    import _mysql_exceptions
except:
    import cash.exceptions as _mysql_exceptions
import datetime
import time
from django.db import transaction
from django.conf import settings
from cash.services.Utils import show_sql, get_logger
import sys
from cash.decorators import json_response
 
@render('cash/tax/index.html')
def index(request):
    return {}

@render('cash/tax/upcoming.html')
def upcoming(request):
    return {}

@json_response
def upcomingList(request):
    req = request.REQUEST
    limit = (datetime.datetime.now() + datetime.timedelta(days=5))
    q = Tax.objects.filter(expire__lte=limit)
                         
    res = []
    for it in q:
        res.append({'id': it.id, 'service': it.service, 'expire': it.expire,
                    'amount': it.amount, 'nextExpire': it.nextExpire})

    data = '{"total": %s, "rows": %s}' % (q.count(), JsonParser.parse(res))
    return data 

@json_response
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
    return data

@json_response
def save(request):
    req = request.REQUEST
    e = fromParams(req)

    safe = True
    data = '{"success":true, "msg": "%s"}' % (_('Created Tax for Service <b>%(service)s</b>') % {'service':e.service})    
    try:
        elem = e.save()
    except _mysql_exceptions.Warning:
        pass
    except Exception, e1:
        safe = False
        data = '{"success":false, "msg": "%s"}' % (e1.args)
        
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
                data = '{"success":true, "msg": "%s"}' % (e1.args)
            
    return data

@json_response
def update(request):
    req = request.REQUEST
    o = Tax.objects.get(pk=req['id'])
    e = fromParams(req)

    safe = True
    data = '{"success":true, "msg": "%s"}' % (_('Updated Service <b>%(service)s</b>') % {'service':e.service})    
    try:
        e.save()
    except _mysql_exceptions.Warning:
        pass
    except Exception, e1:
        safe = False
        data = '{"success":false, "msg": "%s"}' % (e1.args)
    
    if safe:
        if settings.USE_GOOGLE_CAL:
            # ADD TO CALENDAR
            try:
                update_calendar(req['id'])
            except Exception, e1:
                pass
                    
    return data

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
        
@json_response        
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
        data = '{"success":false, "msg": "%s"}' % (e1.args)
        
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

@json_response
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
            data = '{"success":false, "msg": "%s"}' % (e1.args)
        
        if safe:
            try:
                expense.save()
                transaction.commit()
            except _mysql_exceptions.Warning:
                transaction.commit()
            except Exception, e2:
                safe = False
                transaction.rollback()
                data = '{"success":false, "msg": "%s"}' % (e2.args)

        if safe:
            if settings.USE_GOOGLE_CAL:
                # ADD TO CALENDAR
                try:
                    update_calendar(req['id'])
                except Exception, e1:
                    pass        
        
    return data 

    
