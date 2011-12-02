import os

from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    (r'^cash/$','cash.views.index'),
    (r'^cash/',include('cash.controllers.urls')),
    (r'^admin/', include(admin.site.urls)),
)

if settings.DEV:
    urlpatterns += patterns('',
        (r'^cash/media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT}),
        (r'^cash/images/(?P<path>.*)$', 'django.views.static.serve',{'document_root': os.path.join(settings.MEDIA_ROOT,"images")}),
    )