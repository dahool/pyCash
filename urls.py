import os

from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views

admin.autodiscover()

urlpatterns = patterns('',
#    (r'^cash/$','cash.views.index'),
#    url(r'^cash/',include('cash.controllers.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', 'cash.views.login', name='user_signin'),
    url(r'^logout/$', auth_views.logout, {'next_page': settings.LOGOUT_REDIRECT_URL }, name='auth_logout'),
    url(r'^$','cash.views.index'),
    url(r'',include('cash.controllers.urls')),
)

urlpatterns += staticfiles_urlpatterns()

#if settings.DEV:
#    urlpatterns += patterns('',
#        (r'^cash/media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT}),
#        (r'^cash/images/(?P<path>.*)$', 'django.views.static.serve',{'document_root': os.path.join(settings.MEDIA_ROOT,"images")}),
#    )