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
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.template import RequestContext
from django.contrib.auth import views as auth_views

@login_required
def index(request):
    if request.is_mobile:
        return render_to_response('mobile/index.html', {"settings": settings}, context_instance=RequestContext(request))    
    return render_to_response('cash/index.html', {"settings": settings}, context_instance=RequestContext(request))
def login(request, template_name='login.html'):
    if not request.POST.has_key('remember'):
        request.session.set_expiry(0)
    return auth_views.login(request, template_name)