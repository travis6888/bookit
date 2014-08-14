import json
# import datetime
from time import mktime
import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.formats import localize
import googleapiclient
from googleapiclient.http import HttpRequest


# Create your views here.
from googleapiclient import http
from googleapiclient.discovery import build
import httplib2
from oauth2client.client import AccessTokenCredentials
from quick.forms import EmailUserCreationForm


# @login_required
def home(request):

    return render(request, 'home.html')


# @login_required
def profile(request):
    user_social_auth = request.user.social_auth.filter(provider='google-oauth2').first()
    access_token = user_social_auth.extra_data['access_token']
    calID=user_social_auth.uid
    credentials = AccessTokenCredentials(access_token, 'my-user-agent/1.0')
    http= httplib2.Http()
    http = credentials.authorize(http)
    service = build(serviceName='calendar', version='v3', http=http, developerKey='HFs_k7g6ml38NKohwrzfi_ii')
    current_datetime = datetime.datetime.now().isoformat()[:-3] + 'Z'
    calendar2 = service.events().list(calendarId=calID, timeMin=current_datetime, singleEvents=True, orderBy='startTime').execute()

    greater_than_three = []
    i = 0
    while i < len(calendar2['items'])-1:
        next_start = calendar2['items'][i + 1]['start']['dateTime']
        current_end = calendar2['items'][i]['end']['dateTime']

        dateTime_end = datetime.datetime.strptime(current_end, '%Y-%m-%dT%H:%M:%S-07:00')
        dateTime_start = datetime.datetime.strptime(next_start, '%Y-%m-%dT%H:%M:%S-07:00')
        difference = dateTime_start - dateTime_end
        print difference
        i+=1
        if difference >= datetime.timedelta(hours=3):
            print 'yes'
            freeInfo = {
                'event': calendar2['items'][i]['summary'],
                'end': current_end,
                'difference': difference,
            }
            greater_than_three.append(freeInfo)

        else:
            print 'no'
        print greater_than_three

    return render(request, 'profile.html', {'calendar_json': json.dumps(calendar2)})


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
