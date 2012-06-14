from django.conf.urls.defaults import *
from cash.controllers import PaymentController as controller

urlpatterns = patterns('',
    (r'^list$', controller.list),
    url(r'^save$', controller.save_or_update, name="payment_save"),
    url(r'^update$', controller.save_or_update, name="payment_update"),
    url(r'^delete$', controller.delete, name="payment_delete"),
    (r'^calc$', controller.calcPayment)
)
