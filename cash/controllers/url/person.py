from django.conf.urls.defaults import *
from cash.controllers import PersonController as controller

urlpatterns = patterns('',
    (r'^list$', controller.list),
    (r'^save$', controller.save),
    (r'^update$', controller.update),
    (r'^delete$', controller.delete),
)