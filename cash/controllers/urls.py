from django.conf.urls.defaults import *
#from pyCash.cash.controllers import PaymentTypeController, ExpenseController, CategoryController, SubCategoryController, TaxController, IncomeController

urlpatterns = patterns('',
    (r'^paymentType/',include('pyCash.cash.controllers.url.paymentType')),
    (r'^subCategory/',include('pyCash.cash.controllers.url.subCategory')),
    (r'^tax/',include('pyCash.cash.controllers.url.tax')),
    (r'^loan/',include('pyCash.cash.controllers.url.loan')),
    (r'^payment/',include('pyCash.cash.controllers.url.payment')),
    (r'^income/',include('pyCash.cash.controllers.url.income')),
    (r'^expense/',include('pyCash.cash.controllers.url.expense')),
    (r'^stats/',include('pyCash.cash.controllers.url.stats')),
    (r'^category/',include('pyCash.cash.controllers.url.category')),
    (r'^person/',include('pyCash.cash.controllers.url.person')),
    (r'^card/',include('pyCash.cash.controllers.url.card')),                       
    (r'^cardDates/',include('pyCash.cash.controllers.url.cardDates')),
    (r'^cardExpense/',include('pyCash.cash.controllers.url.cardExpense')),
    (r'^debits/',include('pyCash.cash.controllers.url.debits')),
)