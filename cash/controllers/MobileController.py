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

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.conf import settings
from cash.models import PaymentType, SubCategory, Expense, Person, Loan
import datetime
from django.db.models import Sum

@render('mobile/index.html')
def index(request):
    return {"settings": settings}    

@render('mobile/expenses.html')
def expenses(request):
    return {"settings": settings}

@render('mobile/expenses_frm.html')
def expensesAdd(request, id = None):
    if id:
        e = Expense.objects.get(pk=id)
    else:
        e = None

    pType = PaymentType.objects.all().order_by("name")
    cList = SubCategory.objects.all().order_by("category__name", "name")
        
    return {"settings": settings,
            "paymentTypeList": pType,
            "categoryList": cList,
            "expense": e}

@render('mobile/expenses_list.html')
def expensesList(request):
    q = Expense.objects.filter(date__lte = datetime.datetime.now()).exclude(date__lt = datetime.datetime.now() - datetime.timedelta(days=5))
    q = q.order_by("-date")
    return {"settings": settings,
            "list": q,
            "today": datetime.date.today()}

@render('mobile/loans.html')
def loansHome(request):
    q = Person.objects.all()
    q = q.order_by("name")
    return {"settings": settings,"list": q}

@render('mobile/loans_list.html')
def loans_list(request, id):
    p = Person.objects.get(pk=id)
    llist = p.loans.active()
    if (llist.count() > 0):
        total = p.loans.active().aggregate(total=Sum('remain'))['total']
    else:
        total = 0
    return {"settings": settings,"person": p,
            "list": llist.order_by("date"),"total": total}

@render('mobile/loans_payments.html')
def loans_payments(request, id):
    l = Loan.objects.get(pk=id)
    return {"settings": settings, "loan": l}

@render('mobile/loans_payments_add.html')
def loans_payments_add(request, id):
    l = Loan.objects.get(pk=id)
    return {"settings": settings, "loan": l}

@render('mobile/loans_add.html')
def loans_add(request, id):
    p = Person.objects.get(pk=id)
    return {"settings": settings, "person": p}
