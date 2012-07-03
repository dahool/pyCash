# -*- coding: utf-8 -*-
"""Copyright (c) 2012 Sergio Gabriel Teves
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
from django.contrib.auth import authenticate
from django.utils.translation import ugettext as _
from django.http import HttpResponse
from django.shortcuts import render_to_response
from cash.models import AuthToken, TokenUsage
from cash.services import JsonParser
from cash.services.RequestUtils import param_exist, sortMethod
from django.db.models import Q
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
try:
    import _mysql_exceptions
except:
    import cash.exceptions as _mysql_exceptions
from cash.decorators import json_response
from django.utils.crypto import salted_hmac
import time
from common.middleware.exceptions import Http403

@login_required
@render('cash/token/index.html')
def index(request):
    return {}
    
@json_response
def login(request):
    if request.method != 'POST':
        raise Http403
    username = request.POST['u']
    password = request.POST['p']
    user = authenticate(username=username, password=password)
    data = '{"success":false}'
    if user is not None:
        if user.is_active:
            try:
                tk = AuthToken.objects.get(user=user)
                data = '{"success":true, "response": "%s"}' % tk.token
            except AuthToken.DoesNotExist:
                pass
    return data
                    
@login_required    
@json_response
def get(request):
    if request.method != 'POST':
        raise Http403    
    data = '{"created":false}'
    try:
        tk = AuthToken.objects.get(user=request.user)
        data = '{"created":"%s"}' % tk.created.strftime('%d-%m-%Y %H:%M')
    except AuthToken.DoesNotExist:
        pass
    return data

@login_required    
@json_response
def list(request):
    if request.method != 'POST':
        raise Http403   
    res = []
    try:
        tk = AuthToken.objects.get(user=request.user)
        
        q = TokenUsage.objects.filter(token=tk)
        
        for utk in q:
            res.append({'date': utk.access, 'ip': utk.ip})

    except AuthToken.DoesNotExist:
        pass

    data = '{"total": %s, "rows": %s}' % (len(res), JsonParser.parse(res))
    return data    

@login_required    
@json_response
def create(request):
    if request.method != 'POST':
        raise Http403    
    salt = unicode(time.time())
    value = unicode(request.user.username) + unicode(time.time()) + request.user.password + request.user.last_login.strftime('%Y-%m-%d %H:%M:%S')
    hash = salted_hmac(salt, value).hexdigest()[::2]
    
    try:
        # remove old tokens
        AuthToken.objects.filter(user=request.user).delete()
        
        # create new token
        obj = AuthToken.objects.create(user=request.user, token=hash)
        data = '{"success":true, "response": "%s"}' % obj.created.strftime('%d-%m-%Y %H:%M')
    except IntegrityError:
        data = '{"success":false, "msg": "%s"}' % (_("Token already exists."))
    except _mysql_exceptions.Warning:
        pass
    except Exception, e1:
        data = '{"success":false, "msg": "%s"}' % (e1.args)
    return data
    
@login_required    
@json_response
def delete(request):
    if request.method != 'POST':
        raise Http403    
    data = '{"success":true}'
    try:
        # remove old tokens
        AuthToken.objects.filter(user=request.user).delete()
    except _mysql_exceptions.Warning:
        pass
    except Exception, e1:
        data = '{"success":false, "msg": "%s"}' % (e1.args)
    return data
