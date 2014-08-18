
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bookit.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^$', 'quick.views.home', name='home'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': 'home'}, name='logout'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^profile/$', 'quick.views.profile', name='profile'),
    url(r'^create_profile/$', 'quick.views.create_profile', name='create_profile'),
    url(r'^api_test/$', 'quick.views.api_test', name='api_test'),
    url(r'^meetup_api/$', 'quick.views.meetup_api', name='meetup_api'),
    url(r'^trail_api/$', 'quick.views.trail_api', name='trail_api'),
    url(r'^bootstrap/$', 'quick.views.bootstrap', name='bootstrap'),
    url(r'^match/$', 'quick.views.matching', name='match'),

)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)