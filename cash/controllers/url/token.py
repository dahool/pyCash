from django.conf.urls.defaults import patterns, url, include
from cash.controllers import TokenController as controller

urlpatterns = patterns('',
    url(r'^list$', controller.list, name='list'),
    url(r'^get$', controller.get, name='get'),
    url(r'^create$', controller.create, name='create'),
    url(r'^delete$', controller.delete, name='delete'),
    url(r'^login$', controller.login),
    url(r'^$', controller.index)
)
