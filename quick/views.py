import json
# import datetime
from time import mktime
import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.formats import localize
from django.views.decorators.csrf import csrf_exempt
import googleapiclient
from googleapiclient.http import HttpRequest


# Create your views here.
from googleapiclient import http
from googleapiclient.discovery import build
import httplib2
from oauth2client.client import AccessTokenCredentials
from requests import get
from quick.forms import EmailUserCreationForm, ProfileCreationForm


# @login_required
from quick.models import Profile


def home(request):

    return render(request, 'home.html')


# @login_required
def profile(request):
    user_social_auth = request.user.social_auth.filter(provider='google-oauth2').first()
    access_token = user_social_auth.extra_data['access_token']
    calID=user_social_auth.uid
    print calID
    credentials = AccessTokenCredentials(access_token, 'my-user-agent/1.0')
    http= httplib2.Http()
    http = credentials.authorize(http)
    service = build(serviceName='calendar', version='v3', http=http, developerKey='HFs_k7g6ml38NKohwrzfi_ii')
    current_datetime = datetime.datetime.now().isoformat()[:-3] + 'Z'
    calendar2 = service.events().list(calendarId=calID, timeMin=current_datetime, singleEvents=True, orderBy='startTime').execute()
    # Profile.objects.create(email=calID)
    greater_than_three = []
    for i in range(len(calendar2['items'])-1):
        next_start = calendar2['items'][i + 1]['start']['dateTime']
        current_end = calendar2['items'][i]['end']['dateTime']
        # print current_end
        dateTime_end = datetime.datetime.strptime(current_end, '%Y-%m-%dT%H:%M:%S-07:00')
        dateTime_start = datetime.datetime.strptime(next_start, '%Y-%m-%dT%H:%M:%S-07:00')
        difference = dateTime_start - dateTime_end
        # print difference
        if difference >= datetime.timedelta(hours=3):
            # print 'yes'
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

def create_profile(request):
    user_social_auth = request.user.social_auth.filter(provider='google-oauth2').first()
    access_token = user_social_auth.extra_data['access_token']
    calID=user_social_auth.uid
    if request.method == "POST":

        form = ProfileCreationForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.email =calID
            profile.oauth_token = access_token
            profile.save()
            form.save_m2m()
            return redirect('home')
    else:
        form = ProfileCreationForm()
    data = {'form': form}
    return render(request, 'create_profile.html', data)

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


def eventuful_api():
    city='san francisco'
    eventful_url = 'http://api.eventful.com/json/events/search?'
    eventful_params = {
        'app_key': 'pXS5JztFCZDmbxbG',
        'keywords': 'music',
        'loaction': city,
        'date': 'Future'
    }

    eventful_resp = get(url=eventful_url, params=eventful_params)
    print eventful_resp.text


def eventbrite_api():
    city = 'san fransciso'
    eventbrite_url='https://www.eventbriteapi.com/v3/events/search/?'
    eventbrite_params = {
        "token": 'VMJ33HPKLUJ3INR7ASCM',
        'venue.city': city
    }
    eventbrite_resp = get(url=eventbrite_url, params=eventbrite_params)
    print eventbrite_resp.url
    eventbrite_data = json.loads(eventbrite_resp.text)
    print eventbrite_data


def trail_api():
    city = 'San+Jose'
    activity = 'hiking'
    url = ('https://outdoor-data-api.herokuapp.com/api.json?api_key=e65652575b4c95b8d78fae0621bf7428&q[city_eq]={}&q[activities_activity_type_name_cont]={}&q[radius]=30'.format(city, activity))
    resp = get(url=url)
    data = json.loads(resp.text)
    print data
    print resp.url