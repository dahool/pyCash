from django.conf.urls.defaults import *
from pyCash.cash.controllers import StatsController as controller

urlpatterns = patterns('',
    (r'^calc$', controller.calc),                       
    (r'^monthCalc$', controller.monthCalc),
    (r'^sixMonthCalc$', controller.sixMonthCalc),
    (r'^$', controller.index)
)