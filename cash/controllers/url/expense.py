from django.conf.urls.defaults import *
from cash.controllers import ExpenseController as controller

urlpatterns = patterns('',
    (r'^stats$', controller.stats),
    (r'^calc$', controller.calc),
    (r'^monthCalc$', controller.monthCalc),
    (r'^sixMonthCalc$', controller.sixMonthCalc),
    (r'^list$', controller.list),
    (r'^save$', controller.save),
    (r'^update$', controller.update),
    (r'^delete$', controller.delete),
    (r'^$', controller.index)
)


