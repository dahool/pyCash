from django.utils.translation import ugettext as _
from django.http import HttpResponse
from django.shortcuts import render_to_response
from cash.models import Person, Loan, Payment
from cash.services import JsonParser, DateService
from cash.services.RequestUtils import param_exist, sortMethod
from django.db.models import Q
from django.db import IntegrityError, connection
from decimal import *
import string
try:
    import _mysql_exceptions
except:
    import cash.exceptions as _mysql_exceptions
from django.utils import simplejson as json
from cash.decorators import json_response

from django.core import validators
from django.core.exceptions import ValidationError

@json_response
def list(request):
    req = request.REQUEST
    q = Payment.objects.filter()
    if param_exist("loan.id",req):
        q = q.filter(loan=req['loan.id'])
    if param_exist("sort",req):
        q = q.order_by(sortMethod(req))
    if param_exist("limit",req):
        start = req['start']
        limit = req['limit']
        list = q[start:start+limit]
    else:
        list = q
    data = '{"total": %s, "rows": %s}' % (Payment.objects.count(), JsonParser.parse(list))
    return data
    
@json_response
def save_or_update(request):
    data = '{"success":true}'
    req = request.REQUEST
    number = validators.RegexValidator('^([0-9])+(\.[0-9]{1,2})?$', code=_('Amount'))
    amount=req['amount']
    try:
        number(amount)
    except ValidationError, va1:
        return '{"success":false, "msg": "%s: %s"}' % (va1.code, "".join(va1.messages))

    l = Loan.objects.get(pk=req['loan.id'])
    if param_exist("id",req):
        p = Payment.objects.get(pk=req['id'])    
        prevAmount = p.amount
        
    else:
        p = Payment(loan=l)
        prevAmount = None
    
    if checkPayment(l,amount,prevAmount):
        if prevAmount:
            diff = float(prevAmount) - float(amount)
            l.remain = unicode(float(l.remain) + diff)
        else:
            l.remain = unicode(float(l.remain) - float(amount))

        p.amount=amount
        p.date=DateService.invert(req['date'])
        
        try:
            l.save()
        except _mysql_exceptions.Warning:
            pass        
        try:
            p.save()
        except _mysql_exceptions.Warning:
            pass        
        except Exception, e1:
            data = '{"success":false, "msg": "%s"}' % (e1.args)
    else:
        data = '{"success":false, "msg": "%s"}' % (_('The entered amount is greater than the amount owned'))
    return data
        
@json_response
def save(request):
    req = request.REQUEST
    l = Loan.objects.get(pk=req['loan.id'])
    p = Payment(loan=l,amount=req['amount'],date=DateService.invert(req['date']))
    
    if checkPayment(l,req['amount'],None):
        data = '{"success":true}'
        l.remain = unicode(float(l.remain) - float(p.amount))
        try:
            l.save()
        except _mysql_exceptions.Warning:
            pass        
        try:
            p.save()
        except _mysql_exceptions.Warning:
            pass        
        except Exception, e1:
            data = '{"success":false, "msg": "%s"}' % (e1.args)
    else:
        data = '{"success":false, "msg": "%s"}' % (_('The entered amount is greater than the amount owned'))
          
    return data
    
@json_response    
def update(request):
    req = request.REQUEST
    l = Loan.objects.get(pk=req['loan.id'])
    p = Payment.objects.get(pk=req['id'])
    if checkPayment(l,req['amount'],p.amount):
        diff = float(p.amount) - float(req['amount'])
        l.remain = unicode(float(l.remain) + diff)
        
        p.amount=req['amount']
        p.date=DateService.invert(req['date'])
            
        try:
            l.save()
        except _mysql_exceptions.Warning:
            pass        

        data = '{"success":true}'
        try:
            p.save()
        except _mysql_exceptions.Warning:
            pass        
        except Exception, e1:
            data = '{"success":false, "msg": "%s"}' % (e1.args)
    else:
        data = '{"success":false, "msg": "%s"}' % (_('The entered amount is greater than the amount owned'))
                        
    return data

def getPaymentRemain(loan):
    cursor = connection.cursor()
    cursor.execute("SELECT sum(amount) as sum FROM payment WHERE loan_id = %s", [loan.pk])
    row = cursor.fetchone()
    resto = float(loan.amount)
    if row[0]!=None:
        resto -= float(row[0])
    return resto
    
def checkPayment(loan, amount, oldAmount):
    
    resto = getPaymentRemain(loan)
    
    if oldAmount!=None: 
        resto += float(oldAmount)

    diff = float(amount) - resto
    if diff > 0.05:
        return False
    return True

@json_response
def delete(request):
    p = Payment.objects.get(pk=request.REQUEST['id'])
    l = p.loan
    l.remain = unicode(float(l.remain) + float(p.amount))
    l.save()
    try:
        p.delete()
        data = '{"success":true}'
    except Exception, e1:
        data = '{"success":false, "msg": "%s"}' % (e1.args)     
    return data

@json_response
def calcPayment(request):
    req = request.REQUEST
    q = Loan.objects.filter()
    q = q.filter(person=req['person.id'])    
    
    exclude = []
    if param_exist('exclude',req):
        exc = string.split(req['exclude'],";")
        for e in exc:
            exclude.append(long(e))
           
    modf = dict()
    if param_exist('modf',req):
        moda = json.loads(req['modf'])
        for md in moda:
            modf[md['id']] = md['value']
        
    total = Decimal(req['amount'])
    remain = total
         
    res = []
    for exp in q:
        cursor = connection.cursor()
        cursor.execute("SELECT sum(amount) as sum FROM payment WHERE loan_id = %s", [exp.id])
        row = cursor.fetchone()
        sum = exp.amount
        if row[0]!=None:
            sum = exp.amount - row[0]
        
        partial = exp.amount / exp.instalments 
        pay = 0
        dr = False
        if exp.id in modf.keys():
            remain -= modf[exp.id]
            pay = modf[exp.id]
            sum -= pay
            dr = True
            
        if sum > 0:
            res.append({'id': exp.id, 'amount': exp.amount, 'date': exp.date,
                        'reason': exp.reason, 'balance': sum, 'partial': partial,
                        'pay': pay, 'remain': sum, 'dirty': dr})
    
    while remain > 0:
        resto = 0
        for l in res:
            if not l['id'] in exclude:
                if not l['id'] in modf.keys():
                    if l['remain'] < l['partial']:
                        if l['remain'] > remain:
                            l['pay'] += remain
                            l['remain'] = l['balance'] - l['pay']
                            remain = 0
                        else:
                            l['pay'] += l['remain']
                            remain -= l['remain']
                            l['remain'] = l['balance'] - l['pay']
                    else:
                        if l['partial'] > remain:
                            l['pay'] += remain
                            l['remain'] = l['balance'] - l['pay']
                            remain = 0
                        else:
                            l['pay'] += l['partial']
                            l['remain'] = l['balance'] - l['pay']
                            remain -= l['partial']
                    resto += l['remain']                             
                if remain <= 0:
                    break
        if resto == 0:
            break
    data = '{"total": "0", "rows": %s}' % (JsonParser.parse(res))        
    return data
