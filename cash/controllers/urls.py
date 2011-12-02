from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^mobile/',include('cash.controllers.url.mobile')),
    (r'^paymentType/',include('cash.controllers.url.paymentType')),
    (r'^subCategory/',include('cash.controllers.url.subCategory')),
    (r'^tax/',include('cash.controllers.url.tax')),
    (r'^loan/',include('cash.controllers.url.loan')),
    (r'^payment/',include('cash.controllers.url.payment')),
    (r'^income/',include('cash.controllers.url.income')),
    (r'^expense/',include('cash.controllers.url.expense')),
    (r'^stats/',include('cash.controllers.url.stats')),
    (r'^category/',include('cash.controllers.url.category')),
    (r'^person/',include('cash.controllers.url.person')),
    (r'^card/',include('cash.controllers.url.card')),                       
    (r'^cardDates/',include('cash.controllers.url.cardDates')),
    (r'^cardExpense/',include('cash.controllers.url.cardExpense')),
    (r'^debits/',include('cash.controllers.url.debits')),
)