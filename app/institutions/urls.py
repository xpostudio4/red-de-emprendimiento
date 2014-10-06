from django.conf.urls import *
from django.contrib.auth.views import logout

urlpatterns = patterns('',
        url(r'^signin/$', 'institutions.views.signin'),
        url(r'^logout/$', logout, {'next_page': '/'}, name='logout'),
        url(r'^signup/$', 'institutions.views.signup', name='signup'),
        )


