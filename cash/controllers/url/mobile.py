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
from django.conf.urls.defaults import patterns, url, include
from cash.controllers import MobileController as controller
  
urlpatterns = patterns('',
    url(r'^expenses/$', controller.expenses, name='expenses'),
    url(r'^expenses/add/$', controller.expensesAdd, name='expenses_add'),
    url(r'^expenses/edit/(?P<id>[\d]+)/$', controller.expensesAdd, name='expenses_edit'),
    url(r'^expenses/list/$', controller.expensesList, name='expenses_list'),
    url(r'^loans/$', controller.loansHome, name='loans'),
    url(r'^loans/add/(?P<id>[\d]+)/$', controller.loans_add, name='loans_add'),
    url(r'^loans/list/(?P<id>[\d]+)/$', controller.loans_list, name='loans_list'),
    url(r'^loans/payments/(?P<id>[\d]+)/$', controller.loans_payments, name='loans_payments'),
    url(r'^loans/payments/(?P<id>[\d]+)/add/$', controller.loans_payments_add, name='loans_payments_add'),
    url(r'^$', controller.index, name='home'),
)
