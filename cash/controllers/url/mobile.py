from django.conf.urls.defaults import *
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.conf import settings
from cash.models import PaymentType, SubCategory, Expense
import datetime

def index(request):
    return render_to_response('mobile/index.html', {"settings": settings})    

def expenses(request):
    return render_to_response('mobile/expenses.html', {"settings": settings})

def expensesAdd(request):
    pType = PaymentType.objects.filter()
    pType.order_by("name")
    
    cList = SubCategory.objects.filter()
    cList.order_by("category__name", "name")
        
    return render_to_response('mobile/expenses_add.html', {"settings": settings,
                                                           "paymentTypeList": pType,
                                                           "categoryList": cList})

def expensesList(request):
    q = Expense.objects.filter()
    q = q.order_by("-date")
    liste = q[0:5]
    return render_to_response('mobile/expenses_list.html', {"settings": settings,
                                                            "list": liste,
                                                            "today": datetime.date.today()})

urlpatterns = patterns('',
    url(r'^expenses/$', expenses, name='expenses'),
    url(r'^expenses/add/$', expensesAdd, name='expenses_add'),
    url(r'^expenses/list/$', expensesList, name='expenses_list'),
    url(r'^$', index, name='home'),
)
