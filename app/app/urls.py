from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'app.views.index'),
    # Examples:
    url(r'^about/$', 'app.views.about'),
    url(r'^category/(?P<category_name>[-\w\d]+)/$', 'app.views.category'),
    url(r'^profile/(?P<slug>[-\w\d]+)/$', 'app.views.profile'),
    url(r'^calendar/$', 'app.views.calendar'),
    url(r'^calendar/(?P<category_name>[-\w\d]+)/$', 'app.views.events_view'),
    # url(r'^app/', include('app.foo.urls')),
    url(r'^accounts/', include('institutions.urls')),
    url(r'^signin/$', 'institutions.views.signin'),
    url(r'^signup/$', 'institutions.views.signup'),
    url(r'^dashboard/$', 'app.views.dashboard'),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^user_validation/$', 'app.views.user_validation'),
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

)

# Uncomment the next line to serve media files in dev.
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#if settings.DEBUG:
#    import debug_toolbar
#    urlpatterns += patterns('',
#                            url(r'^__debug__/', include(debug_toolbar.urls)),
#                            )

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT})) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
