from django.conf.urls.defaults import *
from cash.controllers import PaymentController as controller

urlpatterns = patterns('',
    (r'^list$', controller.list),
    url(r'^save$', controller.save, name="payment_save"),
    url(r'^update$', controller.update, name="payment_update"),
    (r'^delete$', controller.delete),
    (r'^calc$', controller.calcPayment)
)