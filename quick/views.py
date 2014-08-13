from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import googleapiclient
from googleapiclient.http import HttpRequest


# Create your views here.
from googleapiclient import http
from googleapiclient.discovery import build
import httplib2
from oauth2client.client import AccessTokenCredentials
from quick.forms import EmailUserCreationForm


@login_required
def home(request):
    user_social_auth = request.user.social_auth.filter(provider='google-oauth2').first()
    print user_social_auth
    access_token = user_social_auth.extra_data['access_token']
    print access_token
    credentials = AccessTokenCredentials(access_token, 'my-user-agent/1.0')
    http= httplib2.Http()
    http = credentials.authorize(http)
    service = build(serviceName='calendar', version='v3', http=http, developerKey='HFs_k7g6ml38NKohwrzfi_ii')
    calendar = service.calendars().get(calendarId='founder@bookitquick.co').execute()
    print calendar['summary']
    print calendar
    # calendar2 = service.events().list(calendarId='founder@bookitquick.co').execute()
    # print calendar2
    return render(request, 'home.html')


def register(request):
    if request.method == 'POST':
        form = EmailUserCreationForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect("home")
    else:
        form = EmailUserCreationForm()

    return render(request, "registration/register.html", {
        'form': form,
    })
