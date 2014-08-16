from django.contrib import admin

# Register your models here.
from quick.models import Interest, Profile, Event, FreeTimes

admin.site.register(Profile)
admin.site.register(Interest)
admin.site.register(Event)
admin.site.register(FreeTimes)