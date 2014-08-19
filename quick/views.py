import json
# import datetime
from time import mktime
import datetime
from django.http import HttpResponse
import pytz
from pytz import timezone
from tzlocal import get_localzone
import dateutil.parser
from dateutil.relativedelta import relativedelta

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, render_to_response
from django.utils.formats import localize
from django.views.decorators.csrf import csrf_exempt
import googleapiclient
from googleapiclient.http import HttpRequest
from pyzipcode import ZipCodeDatabase


# Create your views here.
from googleapiclient import http
from googleapiclient.discovery import build
import httplib2
from oauth2client.client import AccessTokenCredentials
from requests import get
from quick.forms import EmailUserCreationForm, ProfileCreationForm


# @login_required
from quick.models import Profile, FreeTimes, Event


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
        event = (str(calendar2['items'][i]['summary']))
        curent_event_end_dateTime = datetime.datetime.strptime(current_end, '%Y-%m-%dT%H:%M:%S-07:00')
        next_event_start_dateTime = datetime.datetime.strptime(next_start, '%Y-%m-%dT%H:%M:%S-07:00')


        difference = next_event_start_dateTime - curent_event_end_dateTime
        if difference >= datetime.timedelta(hours=3):
            if difference >= datetime.timedelta(days=1):
                hours_added = 12
                for j in range(difference.days):
                    if j == 0:
                        free_start_dateTime = curent_event_end_dateTime
                        free_end_dateTime = free_start_dateTime+relativedelta(hours=7)
                        free_time_start = free_start_dateTime.strftime('%Y-%m-%dT%H:%M:%S-07:00')
                        free_time_end = free_end_dateTime.strftime('%Y-%m-%dT%H:%M:%S-07:00')
                        free_time_amount = free_end_dateTime - free_start_dateTime
                    else:
                        free_start_dateTime = curent_event_end_dateTime + relativedelta(hours=hours_added)
                        free_end_dateTime = free_start_dateTime + relativedelta(hours=14)
                        free_time_start = free_start_dateTime.strftime('%Y-%m-%dT%H:%M:%S-07:00')
                        free_time_end = free_end_dateTime.strftime('%Y-%m-%dT%H:%M:%S-07:00')
                        free_time_amount = free_end_dateTime - free_start_dateTime
                    hours_added += 26

                    FreeTimes.objects.create(
                        user=request.user,
                        free_time_start=free_time_start,
                        free_time_end=free_time_end,
                        free_time_amount=free_time_amount,
                        previous_event=event,
                        free_start_dateTime=free_start_dateTime,
                        free_end_dateTime=free_end_dateTime
                    )
            else:
                FreeTimes.objects.create(
                    user=request.user,
                    free_time_start=current_end,
                    free_time_end=next_start,
                    free_time_amount=difference,
                    previous_event=event,
                    free_start_dateTime=curent_event_end_dateTime,
                    free_end_dateTime=next_event_start_dateTime
                )
    for row in FreeTimes.objects.filter(user=request.user):
        if FreeTimes.objects.filter(free_start_dateTime=row.free_start_dateTime).count() > 1:
            row.delete()
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
            profile.user = request.user
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


@csrf_exempt
def api_test(request):
    profile = Profile.objects.get(user=request.user)
    interests = profile.interests.filter(interests__in=['MUSIC', 'TECHNOLOGY', 'COMEDY', 'CAR', 'FOOD', 'SPORTS'])
    zcdb = ZipCodeDatabase()
    zipcode = zcdb[profile.zipcode]
    eventbrite_list = []
    free_times = FreeTimes.objects.filter(user=request.user)
    eventbrite_url='https://www.eventbriteapi.com/v3/events/search/?'
    for free_time in free_times:
        start_time =  "{}Z".format(free_time.free_time_start[:-6])
        end_time = "{}Z".format(free_time.free_time_end[:-6])
        for interest in interests:
            eventbrite_params = {
            "token": 'VMJ33HPKLUJ3INR7ASCM',
            'popular': True,
            'q': str(interest.interests),
            'location.latitude': zipcode.latitude,
            'location.longitude': zipcode.longitude,
            'location.within': '20mi',
            'start_date.range_start': start_time,
            'start_date.range_end': end_time
            }
            eventbrite_resp = get(url=eventbrite_url, params=eventbrite_params)
            eventbrite_data = json.loads(eventbrite_resp.text)
            eventbrite_list.append(eventbrite_data)

            for event in eventbrite_data['events']:
                formatted_start = event['start']['utc'][:-1] + '-7:00'
                formatted_end = event['end']['utc'][:-1] + '-7:00'
                datetime_start = dateutil.parser.parse(event['start']['utc'])
                datetime_end = dateutil.parser.parse(event['end']['utc'])
                Event.objects.create(
                    name=event['name']['text'],
                    category=interest.interests,
                    venue=event['venue']['name'],
                    description=event['description']['text'],
                    latitude=event['venue']['latitude'],
                    longitude=event['venue']['longitude'],
                    start_time=formatted_start,
                    end_time=formatted_end,
                    picture=event['logo_url'],
                    event_url=event['url'],
                    user=request.user,
                    start_dateTime=datetime_start,
                    end_dateTime=datetime_end
                )

    data = {'data': eventbrite_list}

    return render(request, 'api_test.html', {'event_json': json.dumps(data)})
    # return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def meetup_api(request):
    profile = Profile.objects.get(user=request.user)
    interests = profile.interests.filter(interests__in=['MUSIC', 'TECHNOLOGY', 'COMEDY', 'CAR', 'FOOD', 'SPORTS'])
    zcdb = ZipCodeDatabase()
    zipcode = zcdb[profile.zipcode]
    tz=get_localzone()
    meetup_list = []
    meetup_category = {
        'MUSIC': 21,
        'TECHNOLOGY': 2,
        'COMEDY': 17,
        'CAR': 3,
        'FOOD': 10,
        'SPORTS': 9
    }
    free_times = FreeTimes.objects.filter(user=request.user)
    meetup_url= 'https://api.meetup.com/2/open_events.json?'
    for free_time in free_times:
        meetup_start = datetime.datetime.strptime(free_time.free_time_start, '%Y-%m-%dT%H:%M:%S-07:00')
        meetup_end = datetime.datetime.strptime(free_time.free_time_end, '%Y-%m-%dT%H:%M:%S-07:00')
        meetup_epoch_start=int(meetup_start.strftime('%s'))*1000
        meetup_epoch_end=int(meetup_end.strftime('%s'))*1000
        for interest in interests:
            meetup_params = {
                'key': 'd5b2260514d3173733494e1a292e59',
                'zip': profile.zipcode,
                'category': meetup_category[interest.interests],
                'time': '{},{}'.format(meetup_epoch_start, meetup_epoch_end),
                'page': 1
            }
            meetup_resp = get(url=meetup_url, params=meetup_params)
            meetup_data = json.loads(meetup_resp.text)
            meetup_list.append(meetup_data)
            for event in meetup_data['results']:
                epoch_time = event['time']
                start_dateTime_obj = datetime.datetime.fromtimestamp(epoch_time/1000)
                start_dateTime = tz.localize(start_dateTime_obj)
                start_time = start_dateTime.strftime('%Y-%m-%dT%H:%M:%S-07:00')
                if event.get('duration'):
                    end_time_epoch = event['time'] + event['duration']
                    end_dateTime_obj = datetime.datetime.fromtimestamp(end_time_epoch/1000)
                    end_dateTime = tz.localize(end_dateTime_obj)
                    end_time=end_dateTime.strftime('%Y-%m-%dT%H:%M:%S-07:00')
                else:
                    end_dateTime = start_dateTime+relativedelta(hours=5)
                    end_time=end_dateTime.strftime('%Y-%m-%dT%H:%M:%S-07:00')
                if event.get('venue'):
                    venue = event['venue']['name'] or event['venue']['city']
                    if event.get('description'):
                        description = event['description'] or None
                        Event.objects.create(
                            name=event['name'],
                            category=interest.interests,
                            venue=venue,
                            description=description,
                            latitude=event['venue']['lat'],
                            longitude=event['venue']['lon'],
                            start_time=start_time,
                            end_time=end_time,
                            picture='http://img2.meetupstatic.com/img/8308650022681532654/header/logo-2x.png',
                            event_url=event['event_url'],
                            user=request.user,
                            start_dateTime=start_dateTime,
                            end_dateTime=end_dateTime
                    )
    data = {'data': meetup_list}
    return render(request, 'meetup_api.html', {'event_json': json.dumps(data)})
    # return HttpResponse(json.dumps(data), content_type='application/json')

@csrf_exempt
def trail_api(request):
    profile = Profile.objects.get(user=request.user)
    interests = profile.interests.filter(interests__in=['HIKING', "BIKING", "TRAIL"])
    zcdb = ZipCodeDatabase()
    zipcode = zcdb[profile.zipcode]
    trail_list = []
    for interest in interests:
        activity = interest
        city = zipcode.city
        url = ('https://outdoor-data-api.herokuapp.com/api.json?api_key=e65652575b4c95b8d78fae0621bf7428&q[city_eq]={}&q[activities_activity_type_name_cont]={}&q[radius]=40'.format(city, activity))
        resp = get(url=url)
        data = json.loads(resp.text)
        for outdoor in data['places']:
            Event.objects.create(
                name=outdoor['name'],
                venue=outdoor['city'],
                latitude=outdoor['lat'],
                longitude=outdoor['lon'],
                description=outdoor['directions'],
                picture="http://38.media.tumblr.com/e5c079497b3a6a338f6d7c9b90be871f/tumblr_n5wawiu3Lm1st5lhmo1_1280.jpg",
                category=activity,
                user=request.user)
        trail_list.append(data)


    data = {'data': trail_list}
    return render(request, 'trail_api.html', {'event_json': json.dumps(data)})
    # return HttpResponse(json.dumps(data), content_type='application/json')


def bootstrap(request):
    return render(request, "bootstrap.html")


def matching(request):
    for row in Event.objects.filter(user=request.user):
        if Event.objects.filter(name=row.name).count() > 1:
            row.delete()
    free_times = FreeTimes.objects.filter(user=request.user)
    events = Event.objects.filter(user=request.user).distinct()
    matched_event = {'MUSIC':[], 'CAR': [], "TECHNOLOGY":[], "COMEDY": [], "HIKING": [], "BIKING":[], "TRAIL": [], "FOOD": [], "SPORTS": []}
    for free_time in free_times:
        for event in events:
            if event.start_dateTime and event.start_dateTime >= free_time.free_start_dateTime and free_time.free_end_dateTime:
                if event not in matched_event[event.category]:
                    matched_event[event.category].append(event)
            else:
                if event not in matched_event[event.category]:
                    matched_event[event.category].append(event)


    return render(request, 'bootstrap.html', {'matched': matched_event})



