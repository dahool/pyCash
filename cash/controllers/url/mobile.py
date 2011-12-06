from django.conf.urls.defaults import *
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.conf import settings
from cash.models import PaymentType, SubCategory, Expense, Person, Loan
import datetime
from django.db.models import Sum

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

def loansHome(request):
    q = Person.objects.all()
    q = q.order_by("name")
    return render_to_response('mobile/loans.html', {"settings": settings,
                                                            "list": q})

def loans_list(request, id):
    p = Person.objects.get(pk=id)
    llist = p.loans.active()
    if (llist.count() > 0):
        total = p.loans.active().aggregate(total=Sum('remain'))['total']
    else:
        total = 0
    return render_to_response('mobile/loans_list.html', {"settings": settings,
                                                            "person": p,
                                                            "list": llist.order_by("date"),
                                                            "total": total})

def loans_payments(request, id):
    l = Loan.objects.get(pk=id)
    return render_to_response('mobile/loans_payments.html', {"settings": settings,
                                                            "loan": l})

def loans_payments_add(request, id):
    l = Loan.objects.get(pk=id)
    return render_to_response('mobile/loans_payments_add.html', {"settings": settings,
                                                            "loan": l})

def loans_add(request, id):
    p = Person.objects.get(pk=id)
    return render_to_response('mobile/loans_add.html', {"settings": settings,
                                                            "person": p})
   
urlpatterns = patterns('',
    url(r'^expenses/$', expenses, name='expenses'),
    url(r'^expenses/add/$', expensesAdd, name='expenses_add'),
    url(r'^expenses/list/$', expensesList, name='expenses_list'),
    url(r'^loans/$', loansHome, name='loans'),
    url(r'^loans/add/(?P<id>[\d]+)/$', loans_add, name='loans_add'),
    url(r'^loans/list/(?P<id>[\d]+)/$', loans_list, name='loans_list'),
    url(r'^loans/payments/(?P<id>[\d]+)/$', loans_payments, name='loans_payments'),
    url(r'^loans/payments/(?P<id>[\d]+)/add/$', loans_payments_add, name='loans_payments_add'),
    url(r'^$', index, name='home'),
)
