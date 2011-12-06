from django.conf.urls.defaults import *
from cash.controllers import LoanController as controller

urlpatterns = patterns('',
    (r'^list$', controller.list),
    url(r'^save$', controller.save_or_update, name="loan_save"),
    (r'^update$', controller.save_or_update),
    url(r'^delete$', controller.delete, name="loan_delete"),
    (r'^$', controller.index)
)