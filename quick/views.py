# Date imports
import datetime
from dateutil import tz
from django.utils import timezone
from tzlocal import get_localzone
import dateutil.parser
from dateutil.relativedelta import relativedelta

# Django imports
from django.contrib.auth.models import User
from django.db.models import Q, Count
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from django.views.decorators.csrf import csrf_exempt

# Import Models/Forms
from bookit.flashtrader_directory.flashtrade import eventbrite_token, meetup_key, outdoor_key, developer_key, \
    sendgrid_key, sendgrid_login
from quick.forms import ProfileCreationForm
from quick.models import Profile, FreeTimes, Event, Friend

# Google oauth imports
from googleapiclient.discovery import build
import httplib2
from oauth2client.client import AccessTokenCredentials
from requests import get

# Other imports
import json
import sendgrid
from pyzipcode import ZipCodeDatabase

# Create your views here.
from quick.utils import sign_in_google


def home(request):
    form = ProfileCreationForm()
    if request.user.is_authenticated():
        profile2 = Profile.objects.get(user=request.user)
    else:
        profile2 = {'stuff': "styff"}
        pass
    return render(request, 'home.html', {'form': form, 'profile2': profile2 })


def profile(request):
    """User logs in through google using python social login. Once the user is logged in, google calendar information is
    pulled from there account. Records of free times are created based on the time in betweeen events"""

    calendar2 = sign_in_google(request)


    # # Loops through events and determines the time your calendar event ends, and how much time you have until your
    # # next one
    for i in range(len(calendar2['items']) - 1):
        next_start = calendar2['items'][i + 1]['start']['dateTime']
        current_end = calendar2['items'][i]['end']['dateTime']
        event = (str(calendar2['items'][i]['summary']))
        # print next_start, current_end

        # Converts unicode information from Google into datetime objects, remember to change for daylight savings
        curent_event_end_dateTime = datetime.datetime.strptime(current_end, '%Y-%m-%dT%H:%M:%S-08:00')
        next_event_start_dateTime = datetime.datetime.strptime(next_start, '%Y-%m-%dT%H:%M:%S-08:00')

        #find todays date
        current_date = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S-08:00')
        real_current = datetime.datetime.strptime(current_date, '%Y-%m-%dT%H:%M:%S-08:00')
        #only allow freetimes for the next four weeks
        if next_event_start_dateTime <= real_current + datetime.timedelta(weeks=4):

            # Currently only working with free slots greater than 3 hours
            difference = next_event_start_dateTime - curent_event_end_dateTime
            if difference >= datetime.timedelta(hours=3):

                # If freetime block is greater than 1 day, will create separate blocks of free time for each day
                if difference >= datetime.timedelta(days=1):
                    hours_added = 12
                    for j in range(difference.days):
                        if j == 0:
                            free_start_dateTime = curent_event_end_dateTime
                            free_end_dateTime = free_start_dateTime + relativedelta(hours=7)
                            free_time_start = free_start_dateTime.strftime('%Y-%m-%dT%H:%M:%S-08:00')
                            free_time_end = free_end_dateTime.strftime('%Y-%m-%dT%H:%M:%S-08:00')
                            free_time_amount = free_end_dateTime - free_start_dateTime
                        else:
                            free_start_dateTime = curent_event_end_dateTime + relativedelta(hours=hours_added)
                            free_end_dateTime = free_start_dateTime + relativedelta(hours=14)
                            free_time_start = free_start_dateTime.strftime('%Y-%m-%dT%H:%M:%S-08:00')
                            free_time_end = free_end_dateTime.strftime('%Y-%m-%dT%H:%M:%S-08:00')
                            free_time_amount = free_end_dateTime - free_start_dateTime
                        hours_added += 12
                        # print free_time_end

                        FreeTimes.objects.bulk_create({FreeTimes(
                            user=request.user,
                            free_time_start=free_time_start,
                            free_time_end=free_time_end,
                            free_time_amount=free_time_amount,
                            previous_event=event,
                            free_start_dateTime=free_start_dateTime,
                            free_end_dateTime=free_end_dateTime)}
                        )
                else:
                    FreeTimes.objects.bulk_create({FreeTimes(
                        user=request.user,
                        free_time_start=current_end,
                        free_time_end=next_start,
                        free_time_amount=difference,
                        previous_event=event,
                        free_start_dateTime=curent_event_end_dateTime,
                        free_end_dateTime=next_event_start_dateTime

                    )})
        else:
            pass

    # Deletes any duplicate free times in database for current user
    duplicate_freeTimes = FreeTimes.objects.filter(user=request.user)
    for row in duplicate_freeTimes:
        if duplicate_freeTimes.filter(free_start_dateTime=row.free_start_dateTime).count() > 1:
            row.delete()
    success = {'success': 'success'}
    return HttpResponse(json.dumps(success), content_type="application/json")


# User creates a profile that saves their current interests and location
def create_profile(request):
    # Pulls information about the user from database to save
    user_social_auth = request.user.social_auth.filter(provider='google-oauth2').first()
    # access_token = user_social_auth.extra_data['access_token']
    calID = user_social_auth.uid
    if request.method == "POST":
        form = ProfileCreationForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.email = calID
            # profile.oauth_token = access_token
            profile.user = request.user
            profile.save()
            form.save_m2m()
            return HttpResponseRedirect('/loading/')
    else:
        form = ProfileCreationForm()
    data = {'form': form}
    return render(request, 'create_profile.html', data)


"""Pulls events from eventbrite Api using information from user profile. Will search for events that match the open
times and the interests of the user"""


@csrf_exempt
def eventbrite_api(request):
    profile = Profile.objects.get(user=request.user)
    interests = profile.interests.filter(interests__in=['MUSIC', 'TECHNOLOGY', 'COMEDY', 'CAR', 'FOOD', 'SPORTS'])
    zcdb = ZipCodeDatabase()

    #geocodes users zipcode to use lat and lng in search
    zipcode = zcdb[profile.zipcode]
    free_times = FreeTimes.objects.filter(user=request.user)
    eventbrite_url = 'https://www.eventbriteapi.com/v3/events/search/?'

    # for free_time in free_times:

    # formats time to match eventbrite api
    start_time = "{}Z".format(free_times.first().free_time_start[:-6])
    end_time = "{}Z".format(free_times.last().free_time_end[:-6])
    print start_time, end_time
    for interest in interests:
        eventbrite_params = {
            "token": eventbrite_token,
            'popular': True,
            'q': str(interest.interests),
            'location.latitude': zipcode.latitude,
            'location.longitude': zipcode.longitude,
            'location.within': '40mi',
            'start_date.range_start': start_time,
            'start_date.range_end': end_time
        }
        eventbrite_resp = get(url=eventbrite_url, params=eventbrite_params)
        eventbrite_data = json.loads(eventbrite_resp.text)

        # Saves returned events to database
        for event in eventbrite_data['events']:
            formatted_start = event['start']['local'] + str('.000-08:00')

            # print formatted_start.astimezone(est)
            formatted_end = str(event['end']['local']) + str('.000-08:00')

            # print  str(str(event['start']['utc'][:-1]) + str('.000-08:00')), event['start']['utc']
            # real_format = datetime.datetime.strptime(formatted_start,'%Y-%m-%dT%H:%M:%S%f-08:00')

            # Creates a datetime object from the time returned by Api

            datetime_start = dateutil.parser.parse(event['start']['utc'])

            datetime_end = dateutil.parser.parse(event['end']['utc'])

            if event['description'] is not None:

                Event.objects.bulk_create({Event(
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
                    end_dateTime=datetime_end)}
                )
            else:
                Event.objects.bulk_create({Event(
                    name=event['name']['text'],
                    category=interest.interests,
                    venue=event['venue']['name'],
                    description="No description",
                    latitude=event['venue']['latitude'],
                    longitude=event['venue']['longitude'],
                    start_time=formatted_start,
                    end_time=formatted_end,
                    picture=event['logo_url'],
                    event_url=event['url'],
                    user=request.user,
                    start_dateTime=datetime_start,
                    end_dateTime=datetime_end)})

        success = {'success': eventbrite_data}
    return HttpResponse(json.dumps(success), content_type="application/json")


"""Pulls events from meetup Api using information from user profile. Will search for events that match the open
times and the interests of the user"""


@csrf_exempt
def meetup_api(request):
    profile = Profile.objects.get(user=request.user)
    interests = profile.interests.filter(interests__in=['MUSIC', 'TECHNOLOGY', 'COMEDY', 'CAR', 'FOOD', 'SPORTS'])
    zcdb = ZipCodeDatabase()
    zipcode = zcdb[profile.zipcode]
    tz = get_localzone()

    # Maps profile interests to Meetup API's category keys
    meetup_category = {
        'MUSIC': 21,
        'TECHNOLOGY': 2,
        'COMEDY': 17,
        'CAR': 3,
        'FOOD': 10,
        'SPORTS': 9
    }
    free_times = FreeTimes.objects.filter(user=request.user)
    meetup_url = 'https://api.meetup.com/2/open_events.json?'
    start_time = free_times.first().free_time_start
    end_time = free_times.last().free_time_end
    meetup_start = datetime.datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S-08:00')
    meetup_end = datetime.datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%S-08:00')

    # Converts free times to unix time for Meetup Api
    meetup_epoch_start = int(meetup_start.strftime('%s')) * 1000
    meetup_epoch_end = int(meetup_end.strftime('%s')) * 1000
    for interest in interests:
        meetup_params = {
            'key': meetup_key,
            'zip': profile.zipcode,
            'radius': 50,
            'category': meetup_category[interest.interests],
            'time': '{},{}'.format(meetup_epoch_start, meetup_epoch_end),
            'page': 1
        }
        meetup_resp = get(url=meetup_url, params=meetup_params)
        meetup_data = json.loads(meetup_resp.text)

        # Saves events returned from Meetup Api
        for event in meetup_data['results']:

            # Converts all times into strings and datetime objects from Unix time.
            # Also adds a timezone to datetime objects
            epoch_time = event['time']
            start_dateTime_obj = datetime.datetime.fromtimestamp(epoch_time / 1000)
            start_dateTime = tz.localize(start_dateTime_obj)
            start_time = start_dateTime.strftime('%Y-%m-%dT%H:%M:%S-08:00')


            #Checks if returned event has a duration
            if event.get('duration'):
                end_time_epoch = event['time'] + event['duration']
                end_dateTime_obj = datetime.datetime.fromtimestamp(end_time_epoch / 1000)
                end_dateTime = tz.localize(end_dateTime_obj)
                end_time = end_dateTime.strftime('%Y-%m-%dT%H:%M:%S-08:00')
            else:
                end_dateTime = start_dateTime + relativedelta(hours=5)
                end_time = end_dateTime.strftime('%Y-%m-%dT%H:%M:%S-08:00')

            #Checks if event has venue and description
            if event.get('venue') and event.get('time') and event.get('name'):
                venue = event['venue']['name'] or event['venue']['city']
                if event.get('description'):
                    description = event['description'] or None
                    Event.objects.bulk_create({Event(
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
                        start_dateTime=start_dateTime_obj,
                        end_dateTime=end_dateTime_obj)}
                    )
    success = {'success': 'success'}
    return HttpResponse(json.dumps(success), content_type="application/json")


"""Pulls biking, hiking, and trail related locations using Trail API"""


@csrf_exempt
def trail_api(request):
    profile = Profile.objects.get(user=request.user)
    interests = profile.interests.filter(interests__in=['HIKING', "BIKING", "TRAIL"])
    zcdb = ZipCodeDatabase()
    zipcode = zcdb[profile.zipcode]
    for interest in interests:
        activity = interest
        city = zipcode.city
        url = (
        'https://outdoor-data-api.herokuapp.com/api.json?api_key=' + outdoor_key + '&q[city_eq]={}&q[activities_activity_type_name_cont]={}&q[radius]=80'.format(
            city, activity))
        resp = get(url=url)
        data = json.loads(resp.text)
        for outdoor in data['places']:
            Event.objects.bulk_create({Event(
                name=outdoor['name'],
                venue=outdoor['city'],
                latitude=outdoor['lat'],
                longitude=outdoor['lon'],
                description=outdoor['directions'],
                picture="http://38.media.tumblr.com/e5c079497b3a6a338f6d7c9b90be871f/tumblr_n5wawiu3Lm1st5lhmo1_1280.jpg",
                category=activity,
                user=request.user)})

    success = {'success': 'success'}
    return HttpResponse(json.dumps(success), content_type="application/json")


def bootstrap(request):
    return render(request, "matched.html")


"""Matches events with users based if their free times match the event start dates and if those events fit the duration
of their free times"""


def matching(request):
    # Deletes any duplicate events from database for that specific user
    event_delete = Event.objects.filter(user=request.user)
    event_past_delete = Event.objects.filter(start_dateTime__lte=datetime.datetime.now())
    for row in event_delete:
        if event_delete.filter(name=row.name).count() > 1:
            row.delete()
    for row in event_past_delete:
        row.delete()
    # Deletes any events that have already happened
    for row in event_delete:
        now = datetime.date.today()
        if event_delete.exclude(end_dateTime__isnull=True):
            if row.start_dateTime is not None and row.end_dateTime is not None:
                if event_delete.filter(start_dateTime__lte=now):
                    row.delete()
            else:
                pass

    free_times = FreeTimes.objects.filter(user=request.user)
    events = Event.objects.filter(user=request.user).distinct()

    # Hash table with list of recommended events organized by category
    matched_event = {'MUSIC': [], 'CAR': [], "TECHNOLOGY": [], "COMEDY": [], "HIKING": [], "BIKING": [], "TRAIL": [],
                     "FOOD": [], "SPORTS": []}
    for free_time in free_times:
        for event in events:
            if event.start_dateTime and event.start_dateTime >= free_time.free_start_dateTime and free_time.free_end_dateTime:
                # Ensures the event is only recommended once
                if event not in matched_event[event.category]:
                    matched_event[event.category].append(event)
            else:
                # Ensures the event is only recommended once
                if event not in matched_event[event.category]:
                    matched_event[event.category].append(event)

    profile = Profile.objects.get(user=request.user)
    form = ProfileCreationForm()

    return render(request, 'matched.html', {'matched': matched_event, 'timezone': profile.timezone, 'form': form})


"""Posts event to users google calendar"""


@csrf_exempt
def post_event(request):
    if request.method == 'POST':
        event_id = json.loads(request.body)
        event = Event.objects.get(pk=event_id)

        # Parameters for event being saved to google calendar
        print str(event.end_dateTime) + '.000-08.00', event.start_dateTime

        event_info = {
            "end": {
                "dateTime": event.end_time
            },

            "start": {
                'dateTime': event.start_time
            },

            "summary": event.name,
            "location": event.venue,

        }

        # Builds google calendar service with appropriate credentials
        user_social_auth = request.user.social_auth.filter(provider='google-oauth2').first()
        access_token = user_social_auth.extra_data['access_token']
        calID = user_social_auth.uid
        credentials = AccessTokenCredentials(access_token, 'my-user-agent/1.0')
        http = httplib2.Http()
        http = credentials.authorize(http)
        service = build(serviceName='calendar', version='v3', http=http, developerKey=developer_key)
        created_event = service.events().insert(calendarId='primary', body=event_info).execute()

        return HttpResponse(json.dumps(event_id), content_type='application/json')


def loading(request):
    return render(request, 'loading.html')


# Finds events that match your friends recommended events
def group_match(request):
    matched = {}

    # Loop through a list of your friends
    for friend in Friend.objects.filter(user=request.user):
        list = []
        name_list = []
        friend_user = User.objects.get(email=friend.email)

        # Queries the DB for events that match both users
        friend_user_events = Event.objects.filter(Q(user=request.user) | Q(user=friend_user))
        duplicate_events = friend_user_events.values('name').annotate(Count('id')).order_by().filter(id__count__gt=1)
        matching = friend_user_events.filter(name__in=[item['name'] for item in duplicate_events])

        # Suggests events that have been recommended for both you and your friend
        for event in matching:
            if event.name not in name_list:
                name_list.append(event.name)
                list.append(event)
        matched[friend_user] = list
    print matched
    return render(request, 'friend_match.html', {'matched': matched})


@csrf_exempt
def invite_friends(request):
    if request.method == "POST":
        data = json.loads(request.body)
        friends = data.split(",")
        print data
        print friends
        for friend in friends:
            Friend.objects.create(user=request.user, email=friend)
            print friend
            sg = sendgrid.SendGridClient(sendgrid_login, sendgrid_key)

            message = sendgrid.Mail()
            message.add_to(friend)
            message.set_subject('You friend {} has invited you to BookIt'.format(request.user.first_name))
            message.set_text('Click the following link to get started now! http://localhost:8000/')
            message.set_html(
                "<h2>Welcome to BookIt</h2><p><a href='http://localhost:8000/'>Click Here To Get Started</a></p>")
            message.set_from(request.user.email)
            status, msg = sg.send(message)
        success = {'success': 'success'}
        return HttpResponse(json.dumps(success), content_type="application/json")


@csrf_exempt
def add_friend(request):
    if request.method == "POST":
        data = json.loads(request.body)
        Friend.objects.create(user=request.user, email=data)
        friend_delete = Friend.objects.filter(user=request.user)
        for row in friend_delete:
            if friend_delete.filter(email=row.email).count() > 1:
                row.delete()
        return redirect("/friend_match/")


def edit_profile(request):
    profile = Profile.objects.filter(user=request.user).first()
    if request.method == 'POST':

        form = ProfileCreationForm(request.POST, instance=profile)
        if form.is_valid():
            if form.save():
                for row in Event.objects.filter(user=request.user):
                    row.delete()

                return redirect('loading')

    else:
        form = ProfileCreationForm(instance=profile)

    data = {'form': form}

    return render(request, 'matched.html', data)


def twillo(request):
    return render(request, 'twillo.html')


def business_match(request):
    business_free_times = FreeTimes.objects.filter(user=request.user)
    profile = Profile.objects.get(user=request.user)
    free_time_dict = {'timezone': profile.timezone}
    userdict = {}
    list_free_time = []
    free_time_delete = FreeTimes.objects.all()
    # Deletes any events that have already happened
    for row in free_time_delete:
        now = datetime.date.today()
        if free_time_delete.filter(free_start_dateTime__lte=now):
            row.delete()
        else:
            pass
    for free_time in business_free_times:
        bus_free_start = free_time.free_start_dateTime
        bus_free_end = free_time.free_end_dateTime
        users_free_times = FreeTimes.objects.filter(free_start_dateTime__gte=bus_free_start).filter(
            free_end_dateTime__lte=bus_free_end)
        for user2 in users_free_times:
            # if user2 not in userdict[user2.user]:
            list_free_time.append(user2)
            userdict[user2.user] = list_free_time
    free_time_dict['info'] = userdict
    return render(request, 'business_match.html', free_time_dict)


def contact_user_email(request):
    if request.method == "POST":
        data = json.loads(request.body)
        find_user = User.objects.get(data.id)





