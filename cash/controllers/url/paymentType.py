from django.conf.urls.defaults import *
from cash.controllers import PaymentTypeController as controller

urlpatterns = patterns('',
    url(r'^list$', controller.list, name="payment_type_list"),
    url(r'^save$', controller.save, name="payment_type_save"),
    url(r'^update$', controller.update, name="payment_type_update"),
    url(r'^delete$', controller.delete, name="payment_type_delete"),
    url(r'^$', controller.index, name="payment_type")
)