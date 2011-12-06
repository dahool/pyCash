from django.conf.urls.defaults import *
from cash.controllers import SyncController as controller

urlpatterns = patterns('',
    (r'^expenses$', controller.cmd_expenses),
    (r'^category$', controller.cmd_category),
    (r'^paymenttype$', controller.cmd_paymenttype),
)