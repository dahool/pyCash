from django.conf.urls.defaults import *
from pyCash.cash.controllers import TaxController as controller

urlpatterns = patterns('',
    (r'^upcomingList$', controller.upcomingList),
    (r'^upcoming$', controller.upcoming),
    (r'^pay$', controller.pay),
    (r'^list$', controller.list),
    (r'^save$', controller.save),
    (r'^update$', controller.update),
    (r'^delete$', controller.delete),
    (r'^$', controller.index)
)