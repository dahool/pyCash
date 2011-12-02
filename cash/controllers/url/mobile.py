from django.conf.urls.defaults import *
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.conf import settings
from cash.models import PaymentType
from cash.models import SubCategory

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
    return render_to_response('mobile/expenses_list.html', {"settings": settings})


urlpatterns = patterns('',
    url(r'^expenses/$', expenses, name='mobile_expenses'),
    url(r'^expenses/add/$', expensesAdd, name='mobile_expenses_add'),
    url(r'^expenses/list/$', expensesList, name='mobile_expenses_list'),
    url(r'^$', index, name='mobile_home'),
)