from django.conf.urls import *
from django.contrib.auth.views import logout

urlpatterns = patterns('',
        url(r'^signin/$', 'institutions.views.signin'),
        url(r'^logout/$', logout, {'next_page': '/'}, name='logout'),
        url(r'^signup/$', 'institutions.views.signup', name='signup'),
        url(r'^password_change/$', 'institutions.views.password_change'),
        url(r'^picture/$', 'app.views.picture_update'),
        )


