
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
    url(r'^eventbrite_api/$', 'quick.views.eventbrite_api', name='eventbrite_api'),
    url(r'^meetup_api/$', 'quick.views.meetup_api', name='meetup_api'),
    url(r'^trail_api/$', 'quick.views.trail_api', name='trail_api'),
    url(r'^bootstrap/$', 'quick.views.bootstrap', name='bootstrap'),
    url(r'^match/$', 'quick.views.matching', name='match'),
    url(r'^post_event/$', 'quick.views.post_event', name='post_event'),
    url(r'^loading/$', 'quick.views.loading', name='loading'),
    url(r'^friend_match/$', 'quick.views.group_match', name='friend_match'),
    url(r'^invite_friends/$', 'quick.views.invite_friends', name='invite_friends'),
    url(r'^add_friend/$', 'quick.views.add_friend', name='add_friend'),
    url(r'^edit_profile/$', 'quick.views.edit_profile', name='edit_profile'),
    url(r'^twillo/$', 'quick.views.twillo', name='twillo'),
    url(r'^business_match/$', 'quick.views.business_match', name='business_match'),
    url(r'^business/$', 'quick.views.business_home', name='business'),
    url(r'^loading_business/$', 'quick.views.business_loading', name='loading_business'),






)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)